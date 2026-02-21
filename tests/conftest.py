import pytest
import respx
from httpx import Response

from mealie_mcp.client import MealieClient
from mealie_mcp.config import settings


@pytest.fixture
def mock_api():
    """respx mock router for Mealie API calls."""
    with respx.mock(base_url=settings.mealie_url.rstrip("/"), assert_all_called=False) as router:
        yield router


@pytest.fixture
async def client():
    """Create a MealieClient for testing."""
    c = MealieClient()
    yield c
    await c.close()


# ── Sample data fixtures ────────────────────────────────────

@pytest.fixture
def sample_recipe():
    return {
        "id": "abc-123",
        "slug": "chicken-tikka-masala",
        "name": "Chicken Tikka Masala",
        "description": "A classic Indian curry dish",
        "totalTime": "45 minutes",
        "prepTime": "15 minutes",
        "performTime": "30 minutes",
        "recipeYield": "4 servings",
        "recipeCategory": [{"name": "Indian", "slug": "indian"}],
        "tags": [{"name": "Dinner", "slug": "dinner"}],
        "recipeIngredient": [
            {"quantity": 2, "unit": {"name": "lbs"}, "food": {"name": "chicken breast"}, "note": "cubed"},
            {"quantity": 1, "unit": {"name": "cup"}, "food": {"name": "yogurt"}, "note": ""},
            {"quantity": 1, "unit": {"name": "can"}, "food": {"name": "tomato sauce"}, "note": "14 oz"},
        ],
        "recipeInstructions": [
            {"text": "Marinate chicken in yogurt and spices for 30 minutes."},
            {"text": "Grill or pan-fry the chicken until charred."},
            {"text": "Simmer in tomato sauce with cream and spices."},
        ],
        "nutrition": {"calories": "450", "protein": "35g"},
        "notes": [],
        "rating": 5,
    }


@pytest.fixture
def sample_shopping_list():
    return {
        "id": "list-001",
        "name": "Weekly Groceries",
        "listItems": [
            {"id": "item-1", "note": "Chicken breast", "quantity": 2, "unit": {"name": "lbs"}, "food": {"name": "chicken"}, "checked": False},
            {"id": "item-2", "note": "Milk", "quantity": 1, "unit": {"name": "gallon"}, "food": {"name": "milk"}, "checked": True},
        ],
    }
