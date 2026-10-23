import logging
import time
import uuid
from functools import lru_cache
from typing import Any, List, Optional
from sqlalchemy.orm import Session
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.recipe import GeneratedRecipe, Recipe, ShoppingList
from app.services.database_service import DatabaseService
from app.core.config import settings

logger = logging.getLogger(__name__)

class LLMConfigurationError(RuntimeError):
    """Raised when the LLM cannot be set up (e.g. missing API key)."""

class RecipeGenerationError(RuntimeError):
    """Raised when the LLM fails to produce a usable recipe."""

def _elapsed_ms(started: float) -> int:
    return round((time.perf_counter() - started) * 1000)

@lru_cache
def get_llm() -> BaseChatModel:
    """Create the Gemini chat model once and reuse it across requests."""
    if not settings.GOOGLE_API_KEY:
        raise LLMConfigurationError("GOOGLE_API_KEY is not set. Add it to backend/.env.")
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        temperature=0.7,
        google_api_key=settings.GOOGLE_API_KEY,
    )

class RecipeService:
    def __init__(self, db: Optional[Session] = None, llm: Optional[BaseChatModel] = None):
        self.db_service = DatabaseService(db) if db else None
        self._llm = llm

        self.common_ingredients = [
            "onion", "garlic", "tomato", "potato", "carrot", "bell pepper",
            "chicken", "beef", "pork", "fish", "rice", "pasta", "bread",
            "egg", "milk", "cheese", "butter", "olive oil", "salt", "pepper"
        ]

    @property
    def llm(self) -> BaseChatModel:
        # Resolved lazily so endpoints that don't need the LLM work without an API key
        if self._llm is None:
            self._llm = get_llm()
        return self._llm

    def _build_recipe_prompt(
        self,
        ingredients: List[str],
        dietary_preferences: Optional[List[str]],
        max_cooking_time: Optional[int],
        allow_external_ingredients: bool
    ) -> str:
        """Helper function to build the prompt for the LLM."""
        lines = [
            "You are a creative chef. Generate a single, delicious recipe based on "
            f"the following ingredients: {', '.join(ingredients)}.",
        ]

        if allow_external_ingredients:
            lines.append(
                "You can suggest a recipe that requires a few extra simple ingredients if it makes "
                "the dish significantly better. Assume the user has basic pantry staples like salt, "
                "pepper, and oil."
            )
        else:
            lines.append(
                "You MUST ONLY use the ingredients provided. Do not suggest any extra ingredients "
                "that are not on the list."
            )

        constraints = []
        if dietary_preferences:
            constraints.append(f"- Dietary preferences: the recipe must be suitable for {', '.join(dietary_preferences)}.")
        if max_cooking_time:
            constraints.append(f"- Maximum cooking time: the total cooking time must not exceed {max_cooking_time} minutes.")
        if constraints:
            lines.append("Please adhere to these constraints:")
            lines.extend(constraints)

        return "\n".join(lines)

    def _build_shopping_list_prompt(
        self,
        user_ingredients: List[str],
        recipe_ingredients: List[str]
    ) -> str:
        """Helper function to build the shopping list prompt."""
        return "\n".join([
            f"A user has the following ingredients: {', '.join(user_ingredients)}.",
            f"A recipe requires these ingredients: {', '.join(recipe_ingredients)}.",
            "",
            "Compare the two lists and generate a shopping list of ingredients the user needs to buy.",
            "The shopping list should only include items from the recipe that the user does not have.",
            "- If the user has 'chicken' and the recipe needs '1 lb boneless, skinless chicken breasts', "
            "consider it available. General terms match specific ones.",
            "- Assume basic pantry staples (salt, pepper, oil, water) are available.",
            "- Do not include quantities in the final list.",
            "- If the user has all the ingredients, return an empty list.",
        ])

    def _log_llm_request(self, operation: str, input: dict[str, Any], latency_ms: int, **fields) -> None:
        if self.db_service:
            self.db_service.log_llm_request(
                operation=operation, model=settings.GEMINI_MODEL, input=input, latency_ms=latency_ms, **fields
            )

    async def _generate_shopping_list(
        self,
        user_ingredients: List[str],
        recipe_ingredients: List[str]
    ) -> List[str]:
        """Generates a shopping list using the LLM."""
        if not recipe_ingredients:
            return []

        prompt = self._build_shopping_list_prompt(user_ingredients, recipe_ingredients)
        log_input = {"user_ingredients": user_ingredients, "recipe_ingredients": recipe_ingredients}
        started = time.perf_counter()
        try:
            result = await self.llm.with_structured_output(ShoppingList).ainvoke(prompt)
        except Exception as e:
            # The recipe is still useful without a shopping list, so don't fail the request
            logger.exception("Failed to generate shopping list")
            self._log_llm_request("shopping_list", log_input, _elapsed_ms(started), error=repr(e))
            return []
        self._log_llm_request("shopping_list", log_input, _elapsed_ms(started))
        return result.shopping_list

    async def get_recipe_recommendation(
        self,
        ingredients: List[str],
        dietary_preferences: Optional[List[str]] = None,
        max_cooking_time: Optional[int] = None,
        allow_external_ingredients: bool = False,
        user_id: Optional[uuid.UUID] = None
    ) -> Recipe:
        """
        Generate a recipe recommendation based on available ingredients using Google Gemini.
        """
        prompt =self._build_recipe_prompt(ingredients, dietary_preferences, max_cooking_time, allow_external_ingredients)
        logger.debug("Recipe prompt:\n%s", prompt)

        log_input = {
            "ingredients": ingredients,
            "dietary_preferences": dietary_preferences or [],
            "max_cooking_time": max_cooking_time,
            "allow_external_ingredients": allow_external_ingredients,
        }
        llm = self.llm  # Raises LLMConfigurationError before anything is timed or logged
        started = time.perf_counter()
        try:
            generated = await llm.with_structured_output(GeneratedRecipe).ainvoke(prompt)
            if generated is None:
                raise RecipeGenerationError("The AI model returned an empty response.")
        except Exception as e:
            logger.exception("LLM recipe generation failed")
            self._log_llm_request("recipe", log_input, _elapsed_ms(started), error=repr(e), user_id=user_id)
            if isinstance(e, RecipeGenerationError):
                raise
            raise RecipeGenerationError("Failed to generate a valid recipe from the AI model.") from e
        latency_ms = _elapsed_ms(started)

        recipe = Recipe(**generated.model_dump())

        # Generate shopping list only if external ingredients are allowed
        if allow_external_ingredients:
            recipe.shopping_list = await self._generate_shopping_list(
                user_ingredients=ingredients,
                recipe_ingredients=recipe.ingredients
            )
        else:
            recipe.shopping_list = []

        if self.db_service:
            db_recipe = self.db_service.create_recipe(recipe)
            self._log_llm_request(
                "recipe", log_input, latency_ms, recipe_id=db_recipe.id, user_id=user_id
            )

        return recipe

    async def get_ingredient_suggestions(self, query: str) -> List[str]:
        """
        Get ingredient suggestions based on partial input
        """
        query_lower = query.lower()

        # If database is available, get popular ingredients
        if self.db_service:
            suggestions = [name for name, _ in self.db_service.get_popular_ingredients(50)]
        else:
            suggestions = self.common_ingredients

        # Filter by query
        filtered_suggestions = [
            ingredient for ingredient in suggestions
            if query_lower in ingredient.lower()
        ]

        return filtered_suggestions[:10]  # Limit to 10 suggestions
