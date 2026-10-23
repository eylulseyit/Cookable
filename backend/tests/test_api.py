from app.models.recipe import GeneratedRecipe, ShoppingList
from app.services.recipe_service import RecipeService
from tests.conftest import FakeLLM, SAMPLE_RECIPE


def test_health(client):
    assert client.get("/health").json()["status"] == "healthy"


def test_recommend_returns_recipe_without_shopping_list(client, fake_llm):
    response = client.post("/api/v1/recipes/recommend", json={"ingredients": ["pasta", "Tomato", "garlic"]})

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Garlic Tomato Pasta"
    assert body["shopping_list"] == []
    # Shopping list is only generated when extra ingredients are allowed
    assert fake_llm.structured[ShoppingList].prompts == []
    # Ingredients are normalised before reaching the prompt
    assert "pasta, tomato, garlic" in fake_llm.structured[GeneratedRecipe].prompts[0]


def test_recommend_with_external_ingredients_builds_shopping_list(client):
    response = client.post(
        "/api/v1/recipes/recommend",
        json={"ingredients": ["pasta", "tomato"], "allow_external_ingredients": True},
    )

    assert response.status_code == 200
    assert response.json()["shopping_list"] == ["fresh basil"]


def test_prompt_includes_constraints(client, fake_llm):
    client.post(
        "/api/v1/recipes/recommend",
        json={"ingredients": ["rice"], "dietary_preferences": ["vegan"], "max_cooking_time": 30},
    )

    prompt = fake_llm.structured[GeneratedRecipe].prompts[0]
    assert "suitable for vegan" in prompt
    assert "must not exceed 30 minutes" in prompt
    assert "\\n" not in prompt


def test_recommend_rejects_empty_ingredients(client):
    assert client.post("/api/v1/recipes/recommend", json={"ingredients": []}).status_code == 422
    assert client.post("/api/v1/recipes/recommend", json={"ingredients": ["  "]}).status_code == 422


def test_llm_failure_returns_502(client, fake_llm):
    fake_llm.structured[GeneratedRecipe].response = RuntimeError("boom")

    response = client.post("/api/v1/recipes/recommend", json={"ingredients": ["egg"]})

    assert response.status_code == 502
    assert "boom" not in response.json()["detail"]


def test_llm_failure_does_not_count_ingredient_popularity(client, fake_llm):
    fake_llm.structured[GeneratedRecipe].response = RuntimeError("boom")

    client.post("/api/v1/recipes/recommend", json={"ingredients": ["kohlrabi"]})

    assert client.get("/api/v1/ingredients/suggestions", params={"query": "kohlrabi"}).json()["suggestions"] == []


def test_shopping_list_failure_still_returns_recipe(client, fake_llm):
    fake_llm.structured[ShoppingList].response = RuntimeError("boom")

    response = client.post(
        "/api/v1/recipes/recommend",
        json={"ingredients": ["pasta"], "allow_external_ingredients": True},
    )

    assert response.status_code == 200
    assert response.json()["shopping_list"] == []


def test_missing_api_key_returns_503():
    from fastapi.testclient import TestClient
    from main import app

    response = TestClient(app).post("/api/v1/recipes/recommend", json={"ingredients": ["egg"]})

    assert response.status_code == 503
    assert "GOOGLE_API_KEY" in response.json()["detail"]


def test_ingredient_suggestions_use_popularity(client):
    client.post("/api/v1/recipes/recommend", json={"ingredients": ["zucchini"]})

    response = client.get("/api/v1/ingredients/suggestions", params={"query": "zucc"})

    assert response.json()["suggestions"] == ["zucchini"]


def test_suggestions_fall_back_to_common_ingredients():
    import asyncio
    service = RecipeService(llm=FakeLLM({GeneratedRecipe: SAMPLE_RECIPE}))

    assert asyncio.run(service.get_ingredient_suggestions("garl")) == ["garlic"]
