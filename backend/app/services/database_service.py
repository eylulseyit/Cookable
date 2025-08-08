import json
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.database_models import Recipe, Ingredient, Tag, RecipeInstruction, UserQuery, User
from app.models.recipe import Recipe as RecipeSchema

class DatabaseService:
    def __init__(self, db: Session):
        self.db = db
    
    # Recipe operations
    def create_recipe(self, recipe_data: RecipeSchema) -> Recipe:
        """Create a new recipe in the database"""
        # Create recipe
        db_recipe = Recipe(
            title=recipe_data.title,
            cooking_time=recipe_data.cooking_time,
            difficulty=recipe_data.difficulty,
            servings=recipe_data.servings
        )
        self.db.add(db_recipe)
        self.db.flush()  # Get the ID
        
        # Add ingredients
        for ingredient_name in recipe_data.ingredients:
            ingredient = self.get_or_create_ingredient(ingredient_name)
            db_recipe.ingredients.append(ingredient)
        
        # Add tags
        for tag_name in recipe_data.tags:
            tag = self.get_or_create_tag(tag_name)
            db_recipe.tags.append(tag)
        
        # Add instructions
        for i, instruction in enumerate(recipe_data.instructions, 1):
            db_instruction = RecipeInstruction(
                recipe_id=db_recipe.id,
                step_number=i,
                instruction=instruction
            )
            self.db.add(db_instruction)
        
        self.db.commit()
        return db_recipe
    
    def get_recipe_by_id(self, recipe_id: int) -> Optional[Recipe]:
        """Get recipe by ID"""
        return self.db.query(Recipe).filter(Recipe.id == recipe_id).first()
    
    def get_recipes_by_ingredients(self, ingredient_names: List[str], limit: int = 5) -> List[Recipe]:
        """Get recipes that contain any of the specified ingredients"""
        return (
            self.db.query(Recipe)
            .join(Recipe.ingredients)
            .filter(Ingredient.name.in_(ingredient_names))
            .limit(limit)
            .all()
        )
    
    # Ingredient operations
    def get_or_create_ingredient(self, name: str) -> Ingredient:
        """Get existing ingredient or create new one"""
        ingredient = self.db.query(Ingredient).filter(Ingredient.name == name.lower()).first()
        if not ingredient:
            ingredient = Ingredient(name=name.lower())
            self.db.add(ingredient)
            self.db.flush()
        return ingredient
    
    def get_popular_ingredients(self, limit: int = 10) -> List[Ingredient]:
        """Get most popular ingredients"""
        return (
            self.db.query(Ingredient)
            .order_by(Ingredient.popularity_count.desc())
            .limit(limit)
            .all()
        )
    
    def increment_ingredient_popularity(self, ingredient_name: str):
        """Increment popularity count for an ingredient"""
        ingredient = self.get_or_create_ingredient(ingredient_name)
        ingredient.popularity_count += 1
        self.db.commit()
    
    # Tag operations
    def get_or_create_tag(self, name: str) -> Tag:
        """Get existing tag or create new one"""
        tag = self.db.query(Tag).filter(Tag.name == name.lower()).first()
        if not tag:
            tag = Tag(name=name.lower())
            self.db.add(tag)
            self.db.flush()
        return tag
    
    # User query operations
    def save_user_query(self, user_id: int, ingredients: List[str], 
                       dietary_preferences: Optional[List[str]] = None,
                       max_cooking_time: Optional[int] = None) -> UserQuery:
        """Save a user query for analytics"""
        query = UserQuery(
            user_id=user_id,
            ingredients=json.dumps(ingredients),
            dietary_preferences=json.dumps(dietary_preferences or []),
            max_cooking_time=max_cooking_time
        )
        self.db.add(query)
        self.db.commit()
        return query
    
    # User operations
    def create_user(self) -> User:
        """Create a new user"""
        user = User()
        self.db.add(user)
        self.db.commit()
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    # Analytics
    def get_most_searched_ingredients(self, limit: int = 10) -> List[str]:
        """Get most frequently searched ingredients"""
        # This would require a more complex query to analyze user queries
        # For now, return popular ingredients
        popular_ingredients = self.get_popular_ingredients(limit)
        return [ingredient.name for ingredient in popular_ingredients] 