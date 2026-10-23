from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class MealType(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"
    dessert = "dessert"


class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class RecipeRequest(BaseModel):
    """What the user asks for: their ingredients plus optional filters."""
    ingredients: List[str] = Field(min_length=1, max_length=30)
    count: int = Field(default=3, ge=1, le=5, description="How many recipes to suggest")
    servings: Optional[int] = Field(default=None, ge=1, le=12)
    meal_type: Optional[MealType] = None
    cuisine: Optional[str] = Field(default=None, max_length=40)
    difficulty: Optional[Difficulty] = None
    dietary_preferences: List[str] = Field(default_factory=list, max_length=10)
    max_cooking_time: Optional[int] = Field(default=None, gt=0, le=600)
    allow_external_ingredients: bool = False


class Recipe(BaseModel):
    """One recipe as produced by the LLM and returned by the API."""
    title: str = Field(description="The name of the recipe")
    description: str = Field(description="One short sentence that makes the dish sound appealing")
    ingredients: List[str] = Field(description="All ingredients required, including quantities")
    instructions: List[str] = Field(description="Step-by-step preparation instructions")
    cooking_time: int = Field(description="Total cooking time in minutes")
    difficulty: str = Field(description="Difficulty level: Easy, Medium or Hard")
    servings: int = Field(description="How many people the recipe serves")
    tags: List[str] = Field(description='Relevant tags, e.g. "vegetarian", "quick", "dinner"')
    shopping_list: List[str] = Field(
        description="Ingredients of this recipe the user does not have, without quantities. "
        "Empty if the user has everything."
    )


class RecipeSuggestions(BaseModel):
    """Several distinct recipes for one request, generated in a single LLM call."""
    recipes: List[Recipe] = Field(description="Distinct recipes, each a different dish")
