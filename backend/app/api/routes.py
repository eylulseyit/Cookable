from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from app.services.recipe_service import RecipeService
from app.core.database import get_db
from app.services.database_service import DatabaseService

router = APIRouter()

class IngredientRequest(BaseModel):
    ingredients: List[str]
    dietary_preferences: Optional[List[str]] = None
    max_cooking_time: Optional[int] = None
    allow_external_ingredients: bool = False

class RecipeResponse(BaseModel):
    title: str
    ingredients: List[str]
    instructions: List[str]
    cooking_time: int
    difficulty: str
    servings: int
    tags: List[str]
    shopping_list: Optional[List[str]] = None

class UserCreateResponse(BaseModel):
    user_id: int
    message: str

@router.post("/recipes/recommend", response_model=RecipeResponse)
async def recommend_recipe(
    request: IngredientRequest,
    db: Session = Depends(get_db)
):
    """
    Get recipe recommendations based on available ingredients
    """
    try:
        recipe_service = RecipeService(db)
        recipe = await recipe_service.get_recipe_recommendation(
            ingredients=request.ingredients,
            dietary_preferences=request.dietary_preferences,
            max_cooking_time=request.max_cooking_time,
            allow_external_ingredients=request.allow_external_ingredients
        )
        return recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recipe: {str(e)}")

@router.post("/users/create", response_model=UserCreateResponse)
async def create_user(db: Session = Depends(get_db)):
    """
    Create a new user for tracking queries
    """
    try:
        db_service = DatabaseService(db)
        user = db_service.create_user()
        return UserCreateResponse(user_id=user.id, message="User created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@router.get("/recipes/health")
async def recipe_service_health():
    """
    Health check for recipe service
    """
    return {"status": "healthy", "service": "recipe-service"}

@router.get("/ingredients/suggestions")
async def get_ingredient_suggestions(
    query: str,
    db: Session = Depends(get_db)
):
    """
    Get ingredient suggestions based on partial input
    """
    try:
        recipe_service = RecipeService(db)
        suggestions = await recipe_service.get_ingredient_suggestions(query)
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting suggestions: {str(e)}")

@router.get("/ingredients/popular")
async def get_popular_ingredients(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get most popular ingredients
    """
    try:
        db_service = DatabaseService(db)
        popular_ingredients = db_service.get_popular_ingredients(limit)
        return {
            "ingredients": [
                {"name": ingredient.name, "popularity": ingredient.popularity_count}
                for ingredient in popular_ingredients
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting popular ingredients: {str(e)}") 