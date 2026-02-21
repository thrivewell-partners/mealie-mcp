import pytest
from httpx import Response


@pytest.mark.asyncio
async def test_search_recipes(client, mock_api, sample_recipe):
    mock_api.get("/api/recipes").mock(
        return_value=Response(200, json={"items": [sample_recipe], "total": 1})
    )
    result = await client.search_recipes(query="chicken")
    assert result["total"] == 1
    assert result["items"][0]["slug"] == "chicken-tikka-masala"


@pytest.mark.asyncio
async def test_get_recipe(client, mock_api, sample_recipe):
    mock_api.get("/api/recipes/chicken-tikka-masala").mock(
        return_value=Response(200, json=sample_recipe)
    )
    result = await client.get_recipe("chicken-tikka-masala")
    assert result["name"] == "Chicken Tikka Masala"


@pytest.mark.asyncio
async def test_create_recipe(client, mock_api):
    mock_api.post("/api/recipes").mock(
        return_value=Response(201, json="my-new-recipe")
    )
    slug = await client.create_recipe("My New Recipe")
    assert slug == "my-new-recipe"


@pytest.mark.asyncio
async def test_delete_recipe(client, mock_api):
    mock_api.delete("/api/recipes/old-recipe").mock(
        return_value=Response(204)
    )
    await client.delete_recipe("old-recipe")


@pytest.mark.asyncio
async def test_get_shopping_lists(client, mock_api, sample_shopping_list):
    mock_api.get("/api/groups/shopping/lists").mock(
        return_value=Response(200, json={"items": [sample_shopping_list]})
    )
    result = await client.get_shopping_lists()
    assert len(result["items"]) == 1


@pytest.mark.asyncio
async def test_get_categories(client, mock_api):
    mock_api.get("/api/organizers/categories").mock(
        return_value=Response(200, json={"items": [{"name": "Indian", "slug": "indian", "recipes": []}]})
    )
    result = await client.get_categories()
    assert result["items"][0]["name"] == "Indian"
