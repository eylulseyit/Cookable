from pydantic import BaseModel
from typing import List

class Recipe(BaseModel):
    title: str
    ingredients: List[str]
    instructions: List[str]
    cooking_time: int  # in minutes
    difficulty: str  # Easy, Medium, Hard
    servings: int
    tags: List[str]  # e.g., ["vegetarian", "quick", "pasta"]
    
    class Config:
        json_schema_extra = {
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
                "tags": ["pasta", "vegetarian", "quick"]
            }
        } 