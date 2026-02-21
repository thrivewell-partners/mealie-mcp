from __future__ import annotations

from ..client import MealieClient
from ..formatting import (
    format_categories,
    format_cookbooks,
    format_recipe_summary,
    format_tags,
)


def register(mcp, get_client):
    """Register organizer tools with the MCP server."""

    @mcp.tool()
    async def get_categories() -> str:
        """List all recipe categories."""
        client: MealieClient = get_client()
        try:
            data = await client.get_categories()
            items = data.get("items", [])
            return format_categories(items)
        except Exception as e:
            return f"Error fetching categories: {e}"

    @mcp.tool()
    async def get_tags() -> str:
        """List all recipe tags."""
        client: MealieClient = get_client()
        try:
            data = await client.get_tags()
            items = data.get("items", [])
            return format_tags(items)
        except Exception as e:
            return f"Error fetching tags: {e}"

    @mcp.tool()
    async def get_cookbooks() -> str:
        """List all cookbooks."""
        client: MealieClient = get_client()
        try:
            data = await client.get_cookbooks()
            items = data.get("items", [])
            return format_cookbooks(items)
        except Exception as e:
            return f"Error fetching cookbooks: {e}"

    @mcp.tool()
    async def get_cookbook_recipes(
        cookbook_slug: str, page: int = 1, per_page: int = 10
    ) -> str:
        """Get recipes in a cookbook.

        Args:
            cookbook_slug: Cookbook slug identifier
            page: Page number (default 1)
            per_page: Results per page (default 10)
        """
        client: MealieClient = get_client()
        try:
            data = await client.get_cookbook_recipes(cookbook_slug, page, per_page)
            items = data.get("items", [])
            if not items:
                return f"No recipes found in cookbook '{cookbook_slug}'."
            lines = [f"## Recipes in cookbook '{cookbook_slug}'\n"]
            for r in items:
                lines.append(format_recipe_summary(r))
                lines.append("")
            return "\n".join(lines)
        except Exception as e:
            return f"Error fetching cookbook recipes: {e}"

    @mcp.tool()
    async def create_category(name: str) -> str:
        """Create a new recipe category.

        Args:
            name: Category name
        """
        client: MealieClient = get_client()
        try:
            cat = await client.create_category(name)
            return f"Category '{name}' created (slug: `{cat.get('slug', '')}`)."
        except Exception as e:
            return f"Error creating category: {e}"

    @mcp.tool()
    async def create_tag(name: str) -> str:
        """Create a new recipe tag.

        Args:
            name: Tag name
        """
        client: MealieClient = get_client()
        try:
            tag = await client.create_tag(name)
            return f"Tag '{name}' created (slug: `{tag.get('slug', '')}`)."
        except Exception as e:
            return f"Error creating tag: {e}"
