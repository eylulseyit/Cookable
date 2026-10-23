from app.core.database import SessionLocal
from app.models.database_models import LLMRequest, Recipe as RecipeRow
from app.models.recipe import RecipeSuggestions
from app.services.recipe_service import RecipeService
from tests.conftest import FakeLLM, SAMPLE_SUGGESTIONS

RECOMMEND = "/api/v1/recipes/recommend"


def prompt_of(fake_llm) -> str:
    return fake_llm.structured[RecipeSuggestions].prompts[0]


def test_health(client):
    assert client.get("/health").json()["status"] == "healthy"


def test_recommend_returns_requested_number_of_recipes(client):
    response = client.post(RECOMMEND, json={"ingredients": ["pasta", "tomato"], "count": 2})

    assert response.status_code == 200
    titles = [r["title"] for r in response.json()["recipes"]]
    assert titles == ["Garlic Tomato Pasta", "Pasta Puttanesca"]


def test_recommend_defaults_to_three_recipes(client, fake_llm):
    response = client.post(RECOMMEND, json={"ingredients": ["pasta"]})

    assert len(response.json()["recipes"]) == 3
    assert "Suggest 3 distinct recipes" in prompt_of(fake_llm)


def test_ingredients_are_normalised_before_the_prompt(client, fake_llm):
    client.post(RECOMMEND, json={"ingredients": ["pasta", "Tomato", " garlic "]})

    assert "pasta, tomato, garlic" in prompt_of(fake_llm)


def test_prompt_includes_all_filters(client, fake_llm):
    client.post(RECOMMEND, json={
        "ingredients": ["rice"],
        "count": 1,
        "meal_type": "dinner",
        "cuisine": "Turkish",
        "difficulty": "easy",
        "servings": 4,
        "dietary_preferences": ["vegan"],
        "max_cooking_time": 30,
    })

    prompt = prompt_of(fake_llm)
    assert "Suggest 1 distinct recipe " in prompt
    assert "must be a dinner" in prompt
    assert "must be Turkish cuisine" in prompt
    assert "must be easy" in prompt
    assert "must serve 4" in prompt
    assert "suitable for vegan" in prompt
    assert "must not exceed 30 minutes" in prompt


def test_shopping_lists_are_empty_without_extras(client):
    response = client.post(RECOMMEND, json={"ingredients": ["pasta"]})

    assert all(r["shopping_list"] == [] for r in response.json()["recipes"])


def test_shopping_lists_are_kept_with_extras(client):
    response = client.post(RECOMMEND, json={"ingredients": ["pasta"], "allow_external_ingredients": True})

    assert response.json()["recipes"][0]["shopping_list"] == ["fresh basil"]


def test_recommend_rejects_invalid_input(client):
    assert client.post(RECOMMEND, json={"ingredients": []}).status_code == 422
    assert client.post(RECOMMEND, json={"ingredients": ["  "]}).status_code == 422
    assert client.post(RECOMMEND, json={"ingredients": ["egg"], "count": 6}).status_code == 422
    assert client.post(RECOMMEND, json={"ingredients": ["egg"], "meal_type": "brunch"}).status_code == 422


def test_llm_failure_returns_502(client, fake_llm):
    fake_llm.structured[RecipeSuggestions].response = RuntimeError("boom")

    response = client.post(RECOMMEND, json={"ingredients": ["egg"]})

    assert response.status_code == 502
    assert "boom" not in response.json()["detail"]


def test_empty_llm_response_returns_502(client, fake_llm):
    fake_llm.structured[RecipeSuggestions].response = RecipeSuggestions(recipes=[])

    assert client.post(RECOMMEND, json={"ingredients": ["egg"]}).status_code == 502


def test_missing_api_key_returns_503():
    from fastapi.testclient import TestClient
    from main import app

    response = TestClient(app).post(RECOMMEND, json={"ingredients": ["egg"]})

    assert response.status_code == 503
    assert "GOOGLE_API_KEY" in response.json()["detail"]


def test_recipes_are_saved_and_linked_to_one_logged_request(client):
    client.post(RECOMMEND, json={"ingredients": ["pasta", "tomato"], "count": 2})

    with SessionLocal() as db:
        request = db.query(LLMRequest).one()
        recipes = db.query(RecipeRow).order_by(RecipeRow.id).all()

    assert request.operation == "recipe_suggestions"
    assert request.error is None
    assert request.input["ingredients"] == ["pasta", "tomato"]
    assert request.input["count"] == 2
    assert [r.title for r in recipes] == ["Garlic Tomato Pasta", "Pasta Puttanesca"]
    assert all(r.llm_request_id == request.id for r in recipes)
    assert recipes[0].description == "A quick garlic tomato pasta."


def test_failed_llm_call_is_logged_with_error(client, fake_llm):
    fake_llm.structured[RecipeSuggestions].response = RuntimeError("boom")

    client.post(RECOMMEND, json={"ingredients": ["egg"]})

    with SessionLocal() as db:
        request = db.query(LLMRequest).one()
        assert db.query(RecipeRow).count() == 0
    assert "boom" in request.error


def test_popular_ingredients_count_successful_requests(client, fake_llm):
    client.post(RECOMMEND, json={"ingredients": ["egg", "tomato"]})
    client.post(RECOMMEND, json={"ingredients": ["egg"]})
    fake_llm.structured[RecipeSuggestions].response = RuntimeError("boom")
    client.post(RECOMMEND, json={"ingredients": ["kohlrabi"]})

    response = client.get("/api/v1/ingredients/popular")

    assert response.json()["ingredients"] == [
        {"name": "egg", "popularity": 2},
        {"name": "tomato", "popularity": 1},
    ]


def test_ingredient_suggestions_use_popularity(client):
    client.post(RECOMMEND, json={"ingredients": ["zucchini"]})

    response = client.get("/api/v1/ingredients/suggestions", params={"query": "zucc"})

    assert response.json()["suggestions"] == ["zucchini"]


def test_suggestions_fall_back_to_common_ingredients():
    import asyncio
    service = RecipeService(llm=FakeLLM({RecipeSuggestions: SAMPLE_SUGGESTIONS}))

    assert asyncio.run(service.get_ingredient_suggestions("garl")) == ["garlic"]
