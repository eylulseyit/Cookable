import asyncio
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from app.services.database_service import DatabaseService

class RecipeService:
    def __init__(self, db: Session = None):
        self.db = db
        self.db_service = DatabaseService(db) if db else None
        self.common_ingredients = [
            "onion", "garlic", "tomato", "potato", "carrot", "bell pepper",
            "chicken", "beef", "pork", "fish", "rice", "pasta", "bread",
            "egg", "milk", "cheese", "butter", "olive oil", "salt", "pepper"
        ]
    
    async def get_recipe_recommendation(
        self, 
        ingredients: List[str], 
        dietary_preferences: Optional[List[str]] = None,
        max_cooking_time: Optional[int] = None,
        user_id: Optional[int] = None
    ) -> Recipe:
        """
        Generate a recipe recommendation based on available ingredients
        """
        # Track ingredient popularity in database
        if self.db_service:
            for ingredient in ingredients:
                self.db_service.increment_ingredient_popularity(ingredient)
            
            # Save user query for analytics
            if user_id:
                self.db_service.save_user_query(
                    user_id=user_id,
                    ingredients=ingredients,
                    dietary_preferences=dietary_preferences,
                    max_cooking_time=max_cooking_time
                )
        
        # For now, return a mock recipe
        # TODO: Integrate with AI model for real recipe generation
        recipe = Recipe(
            title="Pasta with Tomato Sauce",
            ingredients=[
                "200g pasta",
                "2 tomatoes",
                "1 onion",
                "2 cloves garlic",
                "2 tbsp olive oil",
                "Salt and pepper to taste"
            ],
            instructions=[
                "Bring a large pot of salted water to boil",
                "Cook pasta according to package instructions",
                "Meanwhile, heat olive oil in a pan",
                "Sauté chopped onion and garlic until fragrant",
                "Add chopped tomatoes and cook until softened",
                "Season with salt and pepper",
                "Toss cooked pasta with the sauce"
            ],
            cooking_time=20,
            difficulty="Easy",
            servings=2,
            tags=["pasta", "vegetarian", "quick"]
        )
        
        # Save recipe to database if available
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