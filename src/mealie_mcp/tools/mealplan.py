from __future__ import annotations

from datetime import date, timedelta

from ..client import MealieClient
from ..formatting import format_meal_plans


def register(mcp, get_client):
    """Register meal plan tools with the MCP server."""

    @mcp.tool()
    async def get_meal_plans(start_date: str, end_date: str) -> str:
        """Get meal plan entries for a date range.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        """
        client: MealieClient = get_client()
        try:
            data = await client.get_meal_plans(start_date, end_date)
            entries = data.get("items", [])
            return format_meal_plans(entries)
        except Exception as e:
            return f"Error fetching meal plans: {e}"

    @mcp.tool()
    async def create_meal_plan_entry(
        date: str,
        entry_type: str = "dinner",
        recipe_slug: str | None = None,
        title: str | None = None,
        note: str | None = None,
    ) -> str:
        """Add a meal plan entry for a specific date.

        Args:
            date: Date for the entry (YYYY-MM-DD)
            entry_type: Meal type — "breakfast", "lunch", "dinner", or "side"
            recipe_slug: Recipe slug to plan (use this OR title/note)
            title: Free-text title (for non-recipe entries)
            note: Additional note text
        """
        client: MealieClient = get_client()
        try:
            entry_data: dict = {
                "date": date,
                "entryType": entry_type,
            }
            if recipe_slug:
                recipe = await client.get_recipe(recipe_slug)
                entry_data["recipeId"] = recipe["id"]
            else:
                entry_data["title"] = title or "Meal"
                entry_data["text"] = note or ""

            result = await client.create_meal_plan_entry(entry_data)
            entry_id = result.get("id", "")
            if recipe_slug:
                return f"Meal plan entry created: {recipe_slug} on {date} ({entry_type}). Entry ID: `{entry_id}`"
            return f"Meal plan entry created: '{title or 'Meal'}' on {date} ({entry_type}). Entry ID: `{entry_id}`"
        except Exception as e:
            return f"Error creating meal plan entry: {e}"

    @mcp.tool()
    async def delete_meal_plan_entry(entry_id: str) -> str:
        """Remove a meal plan entry.

        Args:
            entry_id: Meal plan entry ID (from get_meal_plans)
        """
        client: MealieClient = get_client()
        try:
            await client.delete_meal_plan_entry(entry_id)
            return "Meal plan entry deleted."
        except Exception as e:
            return f"Error deleting meal plan entry: {e}"

    @mcp.tool()
    async def generate_random_meal_plan(
        start_date: str,
        end_date: str,
        entry_type: str = "dinner",
    ) -> str:
        """Auto-fill a date range with random recipes from your collection.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            entry_type: Meal type — "breakfast", "lunch", "dinner", or "side" (default "dinner")
        """
        client: MealieClient = get_client()
        try:
            start = date.fromisoformat(start_date)
            end = date.fromisoformat(end_date)
            num_days = (end - start).days + 1
            if num_days <= 0:
                return "End date must be after start date."
            if num_days > 14:
                return "Please limit to 14 days at a time."

            recipes = await client.get_random_recipes(count=num_days)
            if not recipes:
                return "No recipes found in your collection to plan with."

            created = []
            for i in range(num_days):
                d = start + timedelta(days=i)
                recipe = recipes[i % len(recipes)]
                entry_data = {
                    "date": d.isoformat(),
                    "entryType": entry_type,
                    "recipeId": recipe["id"],
                }
                await client.create_meal_plan_entry(entry_data)
                created.append(f"- {d.isoformat()}: {recipe.get('name', '?')}")

            lines = [f"Created {len(created)} meal plan entries:\n"]
            lines.extend(created)
            return "\n".join(lines)
        except Exception as e:
            return f"Error generating meal plan: {e}"
