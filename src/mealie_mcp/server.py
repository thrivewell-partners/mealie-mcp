from __future__ import annotations

from contextlib import asynccontextmanager

from fastmcp import FastMCP

from .client import MealieClient
from .tools import foods, mealplan, organizers, recipes, shopping

_client: MealieClient | None = None


def get_client() -> MealieClient:
    assert _client is not None, "MealieClient not initialized"
    return _client


@asynccontextmanager
async def lifespan(app: FastMCP):
    global _client
    _client = MealieClient()
    try:
        yield
    finally:
        await _client.close()
        _client = None


mcp = FastMCP(
    "Mealie",
    instructions="MCP server for Mealie recipe manager — search recipes, manage shopping lists, plan meals, and more.",
    lifespan=lifespan,
)

# Register all tool modules
recipes.register(mcp, get_client)
shopping.register(mcp, get_client)
mealplan.register(mcp, get_client)
organizers.register(mcp, get_client)
foods.register(mcp, get_client)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
