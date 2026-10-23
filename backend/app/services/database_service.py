import uuid
from typing import Any, List, Optional

from sqlalchemy import func, select, true
from sqlalchemy.orm import Session

from app.models.database_models import LLMRequest, Recipe, RecipeIngredient, Tag, User
from app.models.recipe import Recipe as RecipeSchema


class DatabaseService:
    def __init__(self, db: Session):
        self.db = db

    # Recipe operations
    def create_recipe(self, recipe_data: RecipeSchema, source: str = "generated") -> Recipe:
        """Save a recipe with its ingredient lines and tags"""
        db_recipe = Recipe(
            title=recipe_data.title,
            servings=recipe_data.servings,
            cooking_time_minutes=recipe_data.cooking_time,
            difficulty=recipe_data.difficulty,
            steps=recipe_data.instructions,
            source=source,
            ingredients=[
                RecipeIngredient(position=i, raw_text=line)
                for i, line in enumerate(recipe_data.ingredients, 1)
            ],
            tags=[self.get_or_create_tag(name) for name in recipe_data.tags],
        )
        self.db.add(db_recipe)
        self.db.commit()
        return db_recipe

    # Tag operations
    def get_or_create_tag(self, name: str) -> Tag:
        """Get existing tag or create new one"""
        name = name.strip().lower()
        tag = self.db.scalar(select(Tag).where(Tag.name == name))
        if not tag:
            tag = Tag(name=name)
            self.db.add(tag)
            self.db.flush()
        return tag

    # LLM request log
    def log_llm_request(
        self,
        operation: str,
        model: str,
        input: dict[str, Any],
        latency_ms: int,
        error: Optional[str] = None,
        recipe_id: Optional[int] = None,
        user_id: Optional[uuid.UUID] = None,
    ) -> LLMRequest:
        """Record one LLM call"""
        request = LLMRequest(
            operation=operation,
            model=model,
            input=input,
            latency_ms=latency_ms,
            error=error,
            recipe_id=recipe_id,
            user_id=user_id,
        )
        self.db.add(request)
        self.db.commit()
        return request

    def get_popular_ingredients(self, limit: int = 10) -> List[tuple[str, int]]:
        """Most requested ingredients across successful recipe requests, with their counts"""
        ingredient = func.jsonb_array_elements_text(LLMRequest.input["ingredients"]).table_valued("value")
        count = func.count().label("count")
        rows = self.db.execute(
            select(ingredient.c.value, count)
            .select_from(LLMRequest)
            .join(ingredient, true())
            .where(LLMRequest.operation == "recipe", LLMRequest.error.is_(None))
            .group_by(ingredient.c.value)
            .order_by(count.desc(), ingredient.c.value)
            .limit(limit)
        )
        return [(name, n) for name, n in rows]

    # User operations
    def create_user(self) -> User:
        """Create a new user"""
        user = User()
        self.db.add(user)
        self.db.commit()
        return user
