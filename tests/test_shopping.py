import pytest
from httpx import Response
from fastmcp import FastMCP

from mealie_mcp.tools.shopping import register


def _get_text(result) -> str:
    return result.content[0].text


@pytest.mark.asyncio
async def test_get_shopping_lists_tool(client, mock_api, sample_shopping_list):
    mock_api.get("/api/groups/shopping/lists").mock(
        return_value=Response(200, json={"items": [sample_shopping_list]})
    )

    test_mcp = FastMCP("test")
    register(test_mcp, lambda: client)

    result = await test_mcp.call_tool("get_shopping_lists", {})
    text = _get_text(result)
    assert "Weekly Groceries" in text
    assert "list-001" in text


@pytest.mark.asyncio
async def test_get_shopping_list_detail(client, mock_api, sample_shopping_list):
    mock_api.get("/api/groups/shopping/lists/list-001").mock(
        return_value=Response(200, json=sample_shopping_list)
    )

    test_mcp = FastMCP("test")
    register(test_mcp, lambda: client)

    result = await test_mcp.call_tool("get_shopping_list", {"list_id": "list-001"})
    text = _get_text(result)
    assert "Weekly Groceries" in text
    assert "To Get" in text
    assert "Done" in text


@pytest.mark.asyncio
async def test_add_item_tool(client, mock_api):
    mock_api.post("/api/groups/shopping/items").mock(
        return_value=Response(201, json={"id": "new-item-1", "note": "Eggs"})
    )

    test_mcp = FastMCP("test")
    register(test_mcp, lambda: client)

    result = await test_mcp.call_tool("add_shopping_list_item", {"list_id": "list-001", "note": "Eggs"})
    text = _get_text(result)
    assert "Item added" in text
    assert "new-item-1" in text
