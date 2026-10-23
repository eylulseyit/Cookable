import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from sqlalchemy import BigInteger, CheckConstraint, Column, DateTime, ForeignKey, Identity, Integer, Numeric, String, Table, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def id_column(type_=Integer) -> Mapped[int]:
    # Identity columns are the modern SQL-standard replacement for SERIAL
    return mapped_column(type_, Identity(), primary_key=True)


def created_at_column() -> Mapped[datetime]:
    return mapped_column(DateTime(timezone=True), server_default=func.now())


recipe_tags = Table(
    "recipe_tags",
    Base.metadata,
    Column("recipe_id", ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    # UUIDs don't reveal how many users exist and work with any auth provider later
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = created_at_column()

    llm_requests: Mapped[list["LLMRequest"]] = relationship(back_populates="user")


class Ingredient(Base):
    """Canonical ingredient catalog; nutrition values are per 100 g."""

    __tablename__ = "ingredients"

    id: Mapped[int] = id_column()
    name: Mapped[str] = mapped_column(String(200), unique=True)
    category: Mapped[Optional[str]] = mapped_column(String(100))
    # USDA FoodData Central id, used to look up nutrition data
    fdc_id: Mapped[Optional[int]]
    kcal: Mapped[Optional[Decimal]] = mapped_column(Numeric(7, 2))
    protein_g: Mapped[Optional[Decimal]] = mapped_column(Numeric(6, 2))
    carbs_g: Mapped[Optional[Decimal]] = mapped_column(Numeric(6, 2))
    fat_g: Mapped[Optional[Decimal]] = mapped_column(Numeric(6, 2))
    created_at: Mapped[datetime] = created_at_column()


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = id_column()
    name: Mapped[str] = mapped_column(String(100), unique=True)

    recipes: Mapped[list["Recipe"]] = relationship(secondary=recipe_tags, back_populates="tags")


class Recipe(Base):
    __tablename__ = "recipes"
    __table_args__ = (
        CheckConstraint("source IN ('generated', 'dataset')", name="source"),
    )

    id: Mapped[int] = id_column()
    title: Mapped[str] = mapped_column(String(300))
    servings: Mapped[Optional[int]]
    cooking_time_minutes: Mapped[Optional[int]]
    difficulty: Mapped[Optional[str]] = mapped_column(String(20))
    # Ordered list of instruction strings; always read together with the recipe
    steps: Mapped[list[str]] = mapped_column(JSONB, default=list)
    source: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = created_at_column()

    ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="recipe", cascade="all, delete-orphan", order_by="RecipeIngredient.position"
    )
    tags: Mapped[list[Tag]] = relationship(secondary=recipe_tags, back_populates="recipes")


class RecipeIngredient(Base):
    """One ingredient line of a recipe, e.g. "2 cloves garlic"."""

    __tablename__ = "recipe_ingredients"

    id: Mapped[int] = id_column()
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"), index=True)
    position: Mapped[int]
    # The line as written; quantity, unit and ingredient are parsed from it when known
    raw_text: Mapped[str] = mapped_column(Text)
    ingredient_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ingredients.id"), index=True)
    quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 3))
    unit: Mapped[Optional[str]] = mapped_column(String(30))

    recipe: Mapped[Recipe] = relationship(back_populates="ingredients")
    ingredient: Mapped[Optional[Ingredient]] = relationship()


class LLMRequest(Base):
    """One call to the LLM, kept for usage stats, performance metrics and evals."""

    __tablename__ = "llm_requests"

    id: Mapped[int] = id_column(BigInteger)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    # What the call was for, e.g. "recipe" or "shopping_list"
    operation: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(100))
    input: Mapped[dict[str, Any]] = mapped_column(JSONB)
    latency_ms: Mapped[int]
    input_tokens: Mapped[Optional[int]]
    output_tokens: Mapped[Optional[int]]
    error: Mapped[Optional[str]] = mapped_column(Text)
    recipe_id: Mapped[Optional[int]] = mapped_column(ForeignKey("recipes.id", ondelete="SET NULL"))
    created_at: Mapped[datetime] = created_at_column()

    user: Mapped[Optional[User]] = relationship(back_populates="llm_requests")
