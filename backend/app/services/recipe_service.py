import asyncio
import json
import os
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from app.services.database_service import DatabaseService
from app.core.config import settings

# --- Gemini Integration ---
from langchain_google_genai import ChatGoogleGenerativeAI

class RecipeService:
    def __init__(self, db: Session = None):
        self.db = db
        self.db_service = DatabaseService(db) if db else None
        
        print("--- Initializing RecipeService ---")
        if not settings.GOOGLE_API_KEY:
            print("!!! FATAL ERROR: GOOGLE_API_KEY is not being read from settings. Check your .env file and config.py.")
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        
        print(f"Found GOOGLE_API_KEY, starting with: '{settings.GOOGLE_API_KEY[:5]}...'")

        try:
            # Initialize the Google Gemini model
            self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, google_api_key=settings.GOOGLE_API_KEY)
            print("--- Google Gemini Model Initialized SUCCESSFULLY ---")
        except Exception as e:
            print(f"!!! FATAL ERROR: FAILED to initialize Google Gemini Model !!!")
            print(f"The error is: {e}")
            print("This usually means the API key is invalid or the 'Generative Language API' is not enabled in your Google Cloud project.")
            raise
        
        self.common_ingredients = [
            "onion", "garlic", "tomato", "potato", "carrot", "bell pepper",
            "chicken", "beef", "pork", "fish", "rice", "pasta", "bread",
            "egg", "milk", "cheese", "butter", "olive oil", "salt", "pepper"
        ]
    
    def _build_recipe_prompt(
        self,
        ingredients: List[str],
        dietary_preferences: Optional[List[str]],
        max_cooking_time: Optional[int],
        allow_external_ingredients: bool
    ) -> str:
        """Helper function to build the prompt for the LLM."""
        
        ingredients_str = ", ".join(ingredients)
        prompt = f"""
You are a creative chef. Generate a single, delicious recipe based on the following ingredients: {ingredients_str}.
"""

        if not allow_external_ingredients:
            prompt += "\nYou MUST ONLY use the ingredients provided. Do not suggest any extra ingredients that are not on the list."
        else:
            prompt += "\nYou can suggest a recipe that requires a few extra simple ingredients if it makes the dish significantly better. Assume the user has basic pantry staples like salt, pepper, and oil."

        prompt += "\nPlease adhere to these constraints:\n"

        if dietary_preferences:
            preferences_str = ", ".join(dietary_preferences)
            prompt += f"- Dietary Preferences: The recipe must be suitable for {preferences_str}.\\n"
        
        if max_cooking_time:
            prompt += f"- Maximum Cooking Time: The total cooking time should not exceed {max_cooking_time} minutes.\\n"

        prompt += """
Your response MUST be a single, valid JSON object with the following exact keys and value types:
- "title": (string) The name of the recipe.
- "ingredients": (list of strings) A list of all ingredients required, including quantities.
- "instructions": (list of strings) Step-by-step instructions for preparing the dish.
- "cooking_time": (integer) The total cooking time in minutes.
- "difficulty": (string) The difficulty level (e.g., "Easy", "Medium", "Hard").
- "servings": (integer) How many people the recipe serves.
- "tags": (list of strings) Relevant tags for the recipe (e.g., "vegetarian", "quick", "dinner").

Do not include any text, explanation, or markdown formatting outside of the JSON object.
"""
        return prompt.strip()

    def _build_shopping_list_prompt(
        self,
        user_ingredients: List[str],
        recipe_ingredients: List[str]
    ) -> str:
        """Helper function to build the shopping list prompt."""
        user_ingredients_str = ", ".join(user_ingredients)
        recipe_ingredients_str = ", ".join(recipe_ingredients)

        prompt = f"""
        A user has the following ingredients: {user_ingredients_str}.
        A recipe requires these ingredients: {recipe_ingredients_str}.

        Compare the two lists and generate a shopping list of ingredients the user needs to buy.
        The shopping list should only include items from the recipe that the user does not have.
        - If the user has 'chicken', and the recipe needs '1 lb boneless, skinless chicken breasts', consider it as available. General terms match specific ones.
        - Do not include quantities in the final list.
        - If the user has all the ingredients, return an empty list.

        Your response MUST be a single, valid JSON object with a single key "shopping_list" which contains a list of strings.
        Example: {{"shopping_list": ["boneless, skinless chicken breasts", "olive oil", "black pepper"]}}
        
        Do not include any text, explanation, or markdown formatting outside of the JSON object.
        """
        return prompt.strip()

    async def _generate_shopping_list(
        self,
        user_ingredients: List[str],
        recipe_ingredients: List[str]
    ) -> List[str]:
        """Generates a shopping list using the LLM."""
        if not recipe_ingredients:
            return []

        prompt = self._build_shopping_list_prompt(user_ingredients, recipe_ingredients)
        try:
            llm_response = await self.llm.ainvoke(prompt)
            response_content = llm_response.content
            
            if response_content.strip().startswith("```json"):
                response_content = response_content.strip()[7:-4].strip()

            data = json.loads(response_content)
            return data.get("shopping_list", [])
        except (json.JSONDecodeError, KeyError):
            # If parsing fails, return an empty list as a fallback
            return []

    async def get_recipe_recommendation(
        self, 
        ingredients: List[str], 
        dietary_preferences: Optional[List[str]] = None,
        max_cooking_time: Optional[int] = None,
        allow_external_ingredients: bool = False,
        user_id: Optional[int] = None
    ) -> Recipe:
        """
        Generate a recipe recommendation based on available ingredients using Google Gemini.
        """
        if self.db_service:
            for ingredient in ingredients:
                self.db_service.increment_ingredient_popularity(ingredient)
            
            if user_id:
                self.db_service.save_user_query(
                    user_id=user_id,
                    ingredients=ingredients,
                    dietary_preferences=dietary_preferences,
                    max_cooking_time=max_cooking_time
                )
        
        # Construct the prompt for Gemini
        prompt = self._build_recipe_prompt(ingredients, dietary_preferences, max_cooking_time, allow_external_ingredients)
        print("--- PROMPT SENT TO GEMINI ---")
        print(prompt)
        print("-----------------------------")
        
        try:
            # Invoke the LLM asynchronously
            llm_response = await self.llm.ainvoke(prompt)
            response_content = llm_response.content

            print("--- RAW RESPONSE FROM GEMINI ---")
            print(response_content)
            print("--------------------------------")

            # Clean up the response if it's wrapped in a markdown code block
            if response_content.strip().startswith("```json"):
                response_content = response_content.strip()[7:-4].strip()

            recipe_data = json.loads(response_content)
            
            # Create a Recipe Pydantic model instance
            recipe = Recipe(**recipe_data)

            # Generate shopping list only if external ingredients are allowed
            if allow_external_ingredients:
                shopping_list = await self._generate_shopping_list(
                    user_ingredients=ingredients,
                    recipe_ingredients=recipe.ingredients
                )
                recipe.shopping_list = shopping_list
            else:
                recipe.shopping_list = []

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"!!! FAILED TO PARSE LLM RESPONSE !!!")
            print(f"Error: {e}")
            print(f"Original non-JSON response was: {response_content}")
            raise ValueError("Failed to generate a valid recipe from the AI model.")
        
        if self.db_service:
            self.db_service.create_recipe(recipe)
        
        return recipe
    
    async def get_ingredient_suggestions(self, query: str) -> List[str]:
        """
        Get ingredient suggestions based on partial input
        """
        query_lower = query.lower()
        
        # If database is available, get popular ingredients
        if self.db_service:
            popular_ingredients = self.db_service.get_popular_ingredients(10)
            suggestions = [ingredient.name for ingredient in popular_ingredients]
        else:
            suggestions = self.common_ingredients
        
        # Filter by query
        filtered_suggestions = [
            ingredient for ingredient in suggestions
            if query_lower in ingredient.lower()
        ]
        
        return filtered_suggestions[:10]  # Limit to 10 suggestions
    
    def _filter_by_dietary_preferences(
        self, 
        recipe: Recipe, 
        preferences: List[str]
    ) -> bool:
        """
        Filter recipe based on dietary preferences
        """
        if not preferences:
            return True
        
        recipe_tags = [tag.lower() for tag in recipe.tags]
        
        for preference in preferences:
            preference_lower = preference.lower()
            if preference_lower in recipe_tags:
                return True
        
        return False
    
    def _filter_by_cooking_time(
        self, 
        recipe: Recipe, 
        max_time: int
    ) -> bool:
        """
        Filter recipe based on maximum cooking time
        """
        return recipe.cooking_time <= max_time 