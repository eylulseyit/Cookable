import os
from pathlib import Path

from sqlalchemy import create_engine, make_url, text

# Tests run against a separate database on the same Postgres server, so the
# dev data in "cookable" is never touched. Set before any app module is
# imported, because the engine is created at import time.
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql+psycopg://cookable:cookable@localhost:5432/cookable_test"
)
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ["GOOGLE_API_KEY"] = ""

import pytest
from alembic import command
from alembic.config import Config
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from app.api.routes import get_recipe_service
from app.core.database import Base, engine, get_db
from app.models.recipe import Recipe, RecipeSuggestions
from app.services.recipe_service import RecipeService


def _create_test_database() -> None:
    url = make_url(TEST_DATABASE_URL)
    admin = create_engine(url.set(database="postgres"), isolation_level="AUTOCOMMIT")
    with admin.connect() as conn:
        exists = conn.scalar(text("SELECT 1 FROM pg_database WHERE datname = :name"), {"name": url.database})
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{url.database}"'))
    admin.dispose()


@pytest.fixture(scope="session", autouse=True)
def database():
    """Build the schema from scratch with the real migrations once per test run."""
    _create_test_database()
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public"))
    command.upgrade(Config(str(Path(__file__).resolve().parents[1] / "alembic.ini")), "head")


@pytest.fixture(autouse=True)
def clean_tables(database):
    yield
    tables = ", ".join(table.name for table in Base.metadata.sorted_tables)
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE"))


class FakeStructuredLLM:
    def __init__(self, response):
        self.response = response
        self.prompts = []

    async def ainvoke(self, prompt):
        self.prompts.append(prompt)
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


class FakeLLM:
    """Stands in for ChatGoogleGenerativeAI, returning canned responses per schema."""

    def __init__(self, responses):
        self.structured = {schema: FakeStructuredLLM(r) for schema, r in responses.items()}

    def with_structured_output(self, schema):
        return self.structured[schema]


def make_recipe(title: str, shopping_list: list[str] | None = None) -> Recipe:
    return Recipe(
        title=title,
        description=f"A quick {title.lower()}.",
        ingredients=["200g pasta", "3 tomatoes", "2 cloves garlic", "fresh basil"],
        instructions=["Boil pasta", "Make sauce", "Combine"],
        cooking_time=20,
        difficulty="Easy",
        servings=2,
        tags=["pasta", "vegetarian"],
        shopping_list=shopping_list or [],
    )


SAMPLE_SUGGESTIONS = RecipeSuggestions(recipes=[
    make_recipe("Garlic Tomato Pasta", ["fresh basil"]),
    make_recipe("Pasta Puttanesca", ["olives", "capers"]),
    make_recipe("Tomato Orzo"),
])


@pytest.fixture
def fake_llm():
    # A deep copy per test, because the service edits the recipes it gets back
    return FakeLLM({RecipeSuggestions: SAMPLE_SUGGESTIONS.model_copy(deep=True)})


@pytest.fixture
def client(fake_llm):
    # Depends(get_db) lets FastAPI close the session after each request; an
    # open session would otherwise block the TRUNCATE in clean_tables
    def override(db: Session = Depends(get_db)):
        return RecipeService(db, llm=fake_llm)

    app.dependency_overrides[get_recipe_service] = override
    yield TestClient(app)
    app.dependency_overrides.clear()
