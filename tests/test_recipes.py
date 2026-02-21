import pytest
from httpx import Response
from fastmcp import FastMCP

from mealie_mcp.tools.recipes import register


def _get_text(result) -> str:
    """Extract text from a ToolResult."""
    return result.content[0].text


@pytest.mark.asyncio
async def test_search_recipes_tool(client, mock_api, sample_recipe):
    mock_api.get("/api/recipes").mock(
        return_value=Response(200, json={"items": [sample_recipe], "total": 1})
    )

    test_mcp = FastMCP("test")
    register(test_mcp, lambda: client)

    result = await test_mcp.call_tool("search_recipes", {"query": "chicken"})
    text = _get_text(result)
    assert "Chicken Tikka Masala" in text
    assert "chicken-tikka-masala" in text
    assert "Found 1 recipes" in text


@pytest.mark.asyncio
async def test_get_recipe_tool(client, mock_api, sample_recipe):
    mock_api.get("/api/recipes/chicken-tikka-masala").mock(
        return_value=Response(200, json=sample_recipe)
    )

    test_mcp = FastMCP("test")
    register(test_mcp, lambda: client)

    result = await test_mcp.call_tool("get_recipe", {"slug": "chicken-tikka-masala"})
    text = _get_text(result)
    assert "Chicken Tikka Masala" in text
    assert "## Ingredients" in text
    assert "## Instructions" in text
    assert "chicken breast" in text


@pytest.mark.asyncio
async def test_get_recipe_not_found(client, mock_api):
    mock_api.get("/api/recipes/nonexistent").mock(
        return_value=Response(404)
    )

    test_mcp = FastMCP("test")
    register(test_mcp, lambda: client)

    result = await test_mcp.call_tool("get_recipe", {"slug": "nonexistent"})
    text = _get_text(result)
    assert "not found" in text.lower() or "error" in text.lower()
