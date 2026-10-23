import uuid
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models.recipe import RecipeRequest, RecipeSuggestions
from app.services.recipe_service import RecipeService, LLMConfigurationError, RecipeGenerationError
from app.core.database import get_db
from app.services.database_service import DatabaseService

router = APIRouter()

class UserCreateResponse(BaseModel):
    user_id: uuid.UUID
    message: str

def get_recipe_service(db: Session = Depends(get_db)) -> RecipeService:
    return RecipeService(db)

@router.post("/recipes/recommend", response_model=RecipeSuggestions)
async def recommend_recipes(
    request: RecipeRequest,
    recipe_service: RecipeService = Depends(get_recipe_service)
):
    """
    Suggest one or more recipes based on available ingredients and filters
    """
    ingredients = [i.strip().lower() for i in request.ingredients if i.strip()]
    if not ingredients:
        raise HTTPException(status_code=422, detail="Please provide at least one ingredient.")
    request = request.model_copy(update={"ingredients": ingredients})

    try:
        recipes = await recipe_service.get_recipe_suggestions(request)
    except LLMConfigurationError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except RecipeGenerationError as e:
        raise HTTPException(status_code=502, detail=str(e))
    return RecipeSuggestions(recipes=recipes)

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
