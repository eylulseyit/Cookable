import uuid
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from app.services.recipe_service import RecipeService, LLMConfigurationError, RecipeGenerationError
from app.core.database import get_db
from app.services.database_service import DatabaseService

router = APIRouter()

class IngredientRequest(BaseModel):
    ingredients: List[str] = Field(min_length=1, max_length=30)
    dietary_preferences: Optional[List[str]] = None
    max_cooking_time: Optional[int] = Field(default=None, gt=0, le=600)
    allow_external_ingredients: bool = False

class UserCreateResponse(BaseModel):
    user_id: uuid.UUID
    message: str

def get_recipe_service(db: Session = Depends(get_db)) -> RecipeService:
    return RecipeService(db)

@router.post("/recipes/recommend", response_model=Recipe)
async def recommend_recipe(
    request: IngredientRequest,
    recipe_service: RecipeService = Depends(get_recipe_service)
):
    """
    Get recipe recommendations based on available ingredients
    """
    ingredients = [i.strip().lower() for i in request.ingredients if i.strip()]
    if not ingredients:
        raise HTTPException(status_code=422, detail="Please provide at least one ingredient.")

    try:
        return await recipe_service.get_recipe_recommendation(
            ingredients=ingredients,
            dietary_preferences=request.dietary_preferences,
            max_cooking_time=request.max_cooking_time,
            allow_external_ingredients=request.allow_external_ingredients
        )
    except LLMConfigurationError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except RecipeGenerationError as e:
        raise HTTPException(status_code=502, detail=str(e))

@router.post("/users/create", response_model=UserCreateResponse)
async def create_user(db: Session = Depends(get_db)):
    """
    Create a new user for tracking queries
    """
    user = DatabaseService(db).create_user()
    return UserCreateResponse(user_id=user.id, message="User created successfully")

@router.get("/recipes/health")
async def recipe_service_health():
    """
    Health check for recipe service
    """
    return {"status": "healthy", "service": "recipe-service"}

@router.get("/ingredients/suggestions")
async def get_ingredient_suggestions(
    query: str = Query(min_length=1),
    recipe_service: RecipeService = Depends(get_recipe_service)
):
    """
    Get ingredient suggestions based on partial input
    """
    suggestions = await recipe_service.get_ingredient_suggestions(query)
    return {"suggestions": suggestions}

@router.get("/ingredients/popular")
async def get_popular_ingredients(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get most popular ingredients
    """
    popular_ingredients = DatabaseService(db).get_popular_ingredients(limit)
    return {
        "ingredients": [
            {"name": name, "popularity": count}
            for name, count in popular_ingredients
        ]
    }
