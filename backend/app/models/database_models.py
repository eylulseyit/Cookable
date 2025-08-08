from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

# Association table for recipe-ingredient relationship
recipe_ingredients = Table(
    'recipe_ingredients',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'))
)

# Association table for recipe-tag relationship
recipe_tags = Table(
    'recipe_tags',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    queries = relationship("UserQuery", back_populates="user")
    ratings = relationship("RecipeRating", back_populates="user")

class Ingredient(Base):
    __tablename__ = "ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    popularity_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    recipes = relationship("Recipe", secondary=recipe_ingredients, back_populates="ingredients")

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    recipes = relationship("Recipe", secondary=recipe_tags, back_populates="tags")

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    cooking_time = Column(Integer)  # in minutes
    difficulty = Column(String)  # Easy, Medium, Hard
    servings = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    ingredients = relationship("Ingredient", secondary=recipe_ingredients, back_populates="recipes")
    tags = relationship("Tag", secondary=recipe_tags, back_populates="recipes")
    instructions = relationship("RecipeInstruction", back_populates="recipe")
    ratings = relationship("RecipeRating", back_populates="recipe")

class RecipeInstruction(Base):
    __tablename__ = "recipe_instructions"
    
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    step_number = Column(Integer)
    instruction = Column(Text)
    
    # Relationships
    recipe = relationship("Recipe", back_populates="instructions")

class UserQuery(Base):
    __tablename__ = "user_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ingredients = Column(Text)  # JSON string of ingredients
    dietary_preferences = Column(Text)  # JSON string of preferences
    max_cooking_time = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="queries")

class RecipeRating(Base):
    __tablename__ = "recipe_ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Float)  # 1-5 stars
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    recipe = relationship("Recipe", back_populates="ratings")
    user = relationship("User", back_populates="ratings") 