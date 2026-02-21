from __future__ import annotations

from ..client import MealieClient
from ..formatting import format_foods, format_units


def register(mcp, get_client):
    """Register food and unit tools with the MCP server."""

    @mcp.tool()
    async def search_foods(
        query: str = "", page: int = 1, per_page: int = 10
    ) -> str:
        """Search the foods database.

        Args:
            query: Search text
            page: Page number (default 1)
            per_page: Results per page (default 10)
        """
        client: MealieClient = get_client()
        try:
            data = await client.search_foods(query, page, per_page)
            items = data.get("items", [])
            return format_foods(items)
        except Exception as e:
            return f"Error searching foods: {e}"

    @mcp.tool()
    async def get_units() -> str:
        """List all measurement units available in Mealie."""
        client: MealieClient = get_client()
        try:
            data = await client.get_units()
            items = data.get("items", [])
            return format_units(items)
        except Exception as e:
            return f"Error fetching units: {e}"
