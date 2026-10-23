import os
import tempfile

# Point the app at a throwaway database and make sure no real key is used
# before any app module is imported
_db_dir = tempfile.mkdtemp()
os.environ["DATABASE_URL"] = f"sqlite:///{_db_dir}/test.db"
os.environ["GOOGLE_API_KEY"] = ""

import pytest
from fastapi.testclient import TestClient

from main import app
from app.api.routes import get_recipe_service
from app.core.database import get_db
from app.models.recipe import GeneratedRecipe, ShoppingList
from app.services.recipe_service import RecipeService


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


SAMPLE_RECIPE = GeneratedRecipe(
    title="Garlic Tomato Pasta",
    ingredients=["200g pasta", "3 tomatoes", "2 cloves garlic", "fresh basil"],
    instructions=["Boil pasta", "Make sauce", "Combine"],
    cooking_time=20,
    difficulty="Easy",
    servings=2,
    tags=["pasta", "vegetarian"],
)


@pytest.fixture
def fake_llm():
    return FakeLLM({
        GeneratedRecipe: SAMPLE_RECIPE,
        ShoppingList: ShoppingList(shopping_list=["fresh basil"]),
    })


@pytest.fixture
def client(fake_llm):
    def override():
        db = next(get_db())
        return RecipeService(db, llm=fake_llm)

    app.dependency_overrides[get_recipe_service] = override
    yield TestClient(app)
    app.dependency_overrides.clear()
