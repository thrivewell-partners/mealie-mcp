from __future__ import annotations

from ..client import MealieClient
from ..formatting import format_shopping_list_detail, format_shopping_list_summary


def register(mcp, get_client):
    """Register shopping list tools with the MCP server."""

    @mcp.tool()
    async def get_shopping_lists() -> str:
        """List all shopping lists."""
        client: MealieClient = get_client()
        try:
            data = await client.get_shopping_lists()
            items = data.get("items", [])
            if not items:
                return "No shopping lists found. Use create_shopping_list to make one."
            lines = ["## Shopping Lists\n"]
            for sl in items:
                lines.append(format_shopping_list_summary(sl))
            return "\n".join(lines)
        except Exception as e:
            return f"Error fetching shopping lists: {e}"

    @mcp.tool()
    async def get_shopping_list(list_id: str) -> str:
        """Get a shopping list with all its items.

        Args:
            list_id: Shopping list ID (from get_shopping_lists)
        """
        client: MealieClient = get_client()
        try:
            sl = await client.get_shopping_list(list_id)
            return format_shopping_list_detail(sl)
        except Exception as e:
            return f"Error fetching shopping list: {e}"

    @mcp.tool()
    async def create_shopping_list(name: str) -> str:
        """Create a new empty shopping list.

        Args:
            name: Name for the new list
        """
        client: MealieClient = get_client()
        try:
            sl = await client.create_shopping_list(name)
            return f"Shopping list '{name}' created! ID: `{sl.get('id', '')}`"
        except Exception as e:
            return f"Error creating shopping list: {e}"

    @mcp.tool()
    async def delete_shopping_list(list_id: str) -> str:
        """Delete a shopping list.

        Args:
            list_id: Shopping list ID to delete
        """
        client: MealieClient = get_client()
        try:
            await client.delete_shopping_list(list_id)
            return f"Shopping list deleted."
        except Exception as e:
            return f"Error deleting shopping list: {e}"

    @mcp.tool()
    async def add_shopping_list_item(
        list_id: str,
        note: str,
        quantity: float | None = None,
        unit_id: str | None = None,
        food_id: str | None = None,
    ) -> str:
        """Add an item to a shopping list.

        Args:
            list_id: Shopping list ID
            note: Item description (e.g. "2 lbs chicken breast")
            quantity: Numeric quantity (optional, for structured items)
            unit_id: Unit ID from get_units (optional)
            food_id: Food ID from search_foods (optional)
        """
        client: MealieClient = get_client()
        try:
            item = await client.add_shopping_list_item(
                list_id, note=note, quantity=quantity, unit_id=unit_id, food_id=food_id
            )
            return f"Item added: {note} (item_id: `{item.get('id', '')}`)"
        except Exception as e:
            return f"Error adding item: {e}"

    @mcp.tool()
    async def remove_shopping_list_item(list_id: str, item_id: str) -> str:
        """Remove an item from a shopping list.

        Args:
            list_id: Shopping list ID (for context)
            item_id: Item ID to remove (from get_shopping_list)
        """
        client: MealieClient = get_client()
        try:
            await client.delete_shopping_list_item(item_id)
            return "Item removed from shopping list."
        except Exception as e:
            return f"Error removing item: {e}"

    @mcp.tool()
    async def check_shopping_list_item(
        list_id: str, item_id: str, checked: bool = True
    ) -> str:
        """Check or uncheck a shopping list item.

        Args:
            list_id: Shopping list ID
            item_id: Item ID to check/uncheck
            checked: True to check, False to uncheck (default True)
        """
        client: MealieClient = get_client()
        try:
            # Get current item data first
            sl = await client.get_shopping_list(list_id)
            item_data = None
            for item in sl.get("listItems", []):
                if item.get("id") == item_id:
                    item_data = item
                    break
            if not item_data:
                return f"Item '{item_id}' not found in list."
            item_data["checked"] = checked
            await client.update_shopping_list_item(item_id, item_data)
            status = "checked" if checked else "unchecked"
            return f"Item {status}."
        except Exception as e:
            return f"Error updating item: {e}"

    @mcp.tool()
    async def add_recipe_to_shopping_list(list_id: str, recipe_slug: str) -> str:
        """Add all ingredients from a recipe to a shopping list.

        Args:
            list_id: Shopping list ID
            recipe_slug: Recipe slug to add ingredients from
        """
        client: MealieClient = get_client()
        try:
            recipe = await client.get_recipe(recipe_slug)
            recipe_id = recipe.get("id")
            if not recipe_id:
                return f"Could not find recipe ID for '{recipe_slug}'."
            await client.add_recipe_ingredients_to_list(list_id, recipe_id)
            name = recipe.get("name", recipe_slug)
            count = len(recipe.get("recipeIngredient", []))
            return f"Added {count} ingredients from '{name}' to shopping list."
        except Exception as e:
            return f"Error adding recipe to shopping list: {e}"
