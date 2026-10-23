import logging
import time
import uuid
from functools import lru_cache
from typing import Any, List, Optional
from sqlalchemy.orm import Session
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.recipe import Recipe, RecipeRequest, RecipeSuggestions
from app.services.database_service import RECIPE_SUGGESTIONS, DatabaseService
from app.core.config import settings

logger = logging.getLogger(__name__)

class LLMConfigurationError(RuntimeError):
    """Raised when the LLM cannot be set up (e.g. missing API key)."""

class RecipeGenerationError(RuntimeError):
    """Raised when the LLM fails to produce usable recipes."""

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

    def _build_prompt(self, request: RecipeRequest) -> str:
        """Helper function to build the prompt for the LLM."""
        count = request.count
        lines = [
            f"You are a creative chef. Suggest {count} distinct recipe{'s' if count > 1 else ''} "
            f"based on the following ingredients: {', '.join(request.ingredients)}.",
        ]
        if count > 1:
            lines.append("Each recipe must be a clearly different dish, not a variation of another.")

        if request.allow_external_ingredients:
            lines.append(
                "A recipe may need a few extra simple ingredients if it makes the dish significantly "
                "better. Assume the user has basic pantry staples like salt, pepper, and oil. List "
                "the ingredients the user would need to buy in shopping_list, without quantities."
            )
        else:
            lines.append(
                "You MUST ONLY use the ingredients provided. Do not suggest any extra ingredients "
                "that are not on the list. Leave shopping_list empty."
            )

        constraints = []
        if request.meal_type:
            constraints.append(f"- Meal: every recipe must be a {request.meal_type.value}.")
        if request.cuisine:
            constraints.append(f"- Cuisine: every recipe must be {request.cuisine} cuisine.")
        if request.difficulty:
            constraints.append(f"- Difficulty: every recipe must be {request.difficulty.value}.")
        if request.servings:
            constraints.append(f"- Servings: every recipe must serve {request.servings}.")
        if request.dietary_preferences:
            constraints.append(
                f"- Dietary preferences: every recipe must be suitable for {', '.join(request.dietary_preferences)}."
            )
        if request.max_cooking_time:
            constraints.append(
                f"- Maximum cooking time: the total cooking time must not exceed {request.max_cooking_time} minutes."
            )
        if constraints:
            lines.append("Please adhere to these constraints:")
            lines.extend(constraints)

        return "\n".join(lines)

    def _log_llm_request(self, input: dict[str, Any], latency_ms: int, **fields) -> Optional[int]:
        if not self.db_service:
            return None
        request = self.db_service.log_llm_request(
            operation=RECIPE_SUGGESTIONS, model=settings.GEMINI_MODEL, input=input, latency_ms=latency_ms, **fields
        )
        return request.id

    async def get_recipe_suggestions(
        self, request: RecipeRequest, user_id: Optional[uuid.UUID] = None
    ) -> List[Recipe]:
        """
        Generate several recipe suggestions in a single LLM call using Google Gemini.
        """
        prompt = self._build_prompt(request)
        logger.debug("Recipe prompt:\n%s", prompt)

        log_input = request.model_dump(mode="json")
        llm = self.llm  # Raises LLMConfigurationError before anything is timed or logged
        started = time.perf_counter()
        try:
            result = await llm.with_structured_output(RecipeSuggestions).ainvoke(prompt)
            if result is None or not result.recipes:
                raise RecipeGenerationError("The AI model returned no recipes.")
        except Exception as e:
            logger.exception("LLM recipe generation failed")
            self._log_llm_request(log_input, _elapsed_ms(started), error=repr(e), user_id=user_id)
            if isinstance(e, RecipeGenerationError):
                raise
            raise RecipeGenerationError("Failed to generate valid recipes from the AI model.") from e

        # The model occasionally returns more than asked for
        recipes = result.recipes[: request.count]
        if not request.allow_external_ingredients:
            for recipe in recipes:
                recipe.shopping_list = []

        llm_request_id = self._log_llm_request(log_input, _elapsed_ms(started), user_id=user_id)
        if self.db_service:
            for recipe in recipes:
                self.db_service.create_recipe(recipe, llm_request_id=llm_request_id)

        return recipes

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
