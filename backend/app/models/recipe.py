from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

class GeneratedRecipe(BaseModel):
    """Recipe fields produced by the LLM."""
    title: str = Field(description="The name of the recipe")
    ingredients: List[str] = Field(description="All ingredients required, including quantities")
    instructions: List[str] = Field(description="Step-by-step preparation instructions")
    cooking_time: int = Field(description="Total cooking time in minutes")
    difficulty: str = Field(description="Difficulty level: Easy, Medium or Hard")
    servings: int = Field(description="How many people the recipe serves")
    tags: List[str] = Field(description='Relevant tags, e.g. "vegetarian", "quick", "dinner"')

class ShoppingList(BaseModel):
    """Ingredients the user still needs to buy."""
    shopping_list: List[str] = Field(description="Recipe ingredients the user does not have, without quantities")

class Recipe(GeneratedRecipe):
    shopping_list: Optional[List[str]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Pasta with Tomato Sauce",
                "ingredients": [
                    "200g pasta",
                    "2 tomatoes",
                    "1 onion",
                    "2 cloves garlic",
                    "2 tbsp olive oil",
                    "Salt and pepper to taste"
                ],
                "instructions": [
                    "Bring a large pot of salted water to boil",
                    "Cook pasta according to package instructions",
                    "Meanwhile, heat olive oil in a pan",
                    "Sauté chopped onion and garlic until fragrant",
                    "Add chopped tomatoes and cook until softened",
                    "Season with salt and pepper",
                    "Toss cooked pasta with the sauce"
                ],
                "cooking_time": 20,
                "difficulty": "Easy",
                "servings": 2,
                "tags": ["pasta", "vegetarian", "quick"],
                "shopping_list": []
            }
        }
    )
