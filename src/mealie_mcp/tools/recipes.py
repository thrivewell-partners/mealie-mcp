from __future__ import annotations

import uuid
from typing import Any

from fastmcp import Context

from ..client import MealieClient
from ..formatting import (
    format_ingredient_list,
    format_recipe_detail,
    format_recipe_summary,
)


async def _resolve_ingredients(client: MealieClient, ingredients: list[dict]) -> list[dict]:
    """Convert ingredient dicts to Mealie recipeIngredient format.

    Each dict may have:
        quantity (float | None): numeric amount
        unit (str | None): unit name or abbreviation (e.g. "g", "cup", "tbsp")
        food (str | None): ingredient name (e.g. "bread flour", "butter")
        comment (str | None): extra info (e.g. "softened", "about 1¾ tsp")
    """
    # Build unit lookup (name, abbreviation, plural variants → unit object)
    all_units = (await client.get_units()).get("items", [])
    unit_lookup: dict[str, dict] = {}
    for u in all_units:
        for key in [
            u.get("name", ""),
            u.get("abbreviation", ""),
            u.get("pluralName", ""),
            u.get("pluralAbbreviation", ""),
        ]:
            if key:
                unit_lookup[key.lower()] = u

    result = []
    for ing in ingredients:
        item: dict[str, Any] = {"referenceId": str(uuid.uuid4()), "title": None}

        # Quantity
        qty = ing.get("quantity")
        item["quantity"] = float(qty) if qty is not None else None

        # Unit
        unit_str = (ing.get("unit") or "").strip().lower()
        if unit_str:
            matched = unit_lookup.get(unit_str)
            if matched:
                item["unit"] = {
                    "id": matched["id"],
                    "name": matched["name"],
                    "abbreviation": matched.get("abbreviation", ""),
                }
            else:
                item["unit"] = None
        else:
            item["unit"] = None

        # Food — search existing, create if not found
        food_name = (ing.get("food") or "").strip()
        if food_name:
            foods = (await client.search_foods(food_name, per_page=10)).get("items", [])
            matched_food = next(
                (f for f in foods if f["name"].lower() == food_name.lower()), None
            )
            if matched_food:
                item["food"] = {"id": matched_food["id"], "name": matched_food["name"]}
            else:
                new_food = await client.create_food(food_name)
                if new_food:
                    item["food"] = {"id": new_food["id"], "name": new_food["name"]}
                else:
                    # Already exists but not in top results — search wider
                    wider = (await client.search_foods(food_name, per_page=50)).get("items", [])
                    food_lower = food_name.lower()
                    # Also try hyphen-normalized variant (Mealie strips hyphens internally)
                    food_normalized = food_lower.replace("-", " ")
                    matched_food = next(
                        (
                            f for f in wider
                            if f["name"].lower() in (food_lower, food_normalized)
                        ),
                        None,
                    )
                    item["food"] = (
                        {"id": matched_food["id"], "name": matched_food["name"]}
                        if matched_food
                        else None
                    )
        else:
            item["food"] = None

        # Comment / note
        item["note"] = (ing.get("comment") or "").strip()

        result.append(item)

    return result


def register(mcp, get_client):
    """Register recipe tools with the MCP server."""

    @mcp.tool()
    async def search_recipes(
        query: str = "",
        page: int = 1,
        per_page: int = 10,
        categories: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> str:
        """Search recipes by keyword with optional category/tag filters.

        Args:
            query: Search text (name, description, ingredients)
            page: Page number (default 1)
            per_page: Results per page (default 10)
            categories: Filter by category slugs
            tags: Filter by tag slugs
        """
        client: MealieClient = get_client()
        try:
            data = await client.search_recipes(
                query=query,
                page=page,
                per_page=per_page,
                categories=categories,
                tags=tags,
            )
            items = data.get("items", [])
            total = data.get("total", 0)
            if not items:
                return "No recipes found. Try a different search term."
            lines = [f"Found {total} recipes (showing page {page}):\n"]
            for r in items:
                lines.append(format_recipe_summary(r))
                lines.append("")
            return "\n".join(lines)
        except Exception as e:
            return f"Error searching recipes: {e}"

    @mcp.tool()
    async def get_recipe(slug: str) -> str:
        """Get full recipe details including ingredients, instructions, and nutrition.

        Args:
            slug: Recipe slug identifier (from search results)
        """
        client: MealieClient = get_client()
        try:
            recipe = await client.get_recipe(slug)
            return format_recipe_detail(recipe)
        except Exception as e:
            return f"Recipe '{slug}' not found. Try search_recipes to find the correct slug. Error: {e}"

    @mcp.tool()
    async def get_recipe_ingredients(slug: str) -> str:
        """Get just the ingredient list for a recipe.

        Args:
            slug: Recipe slug identifier
        """
        client: MealieClient = get_client()
        try:
            recipe = await client.get_recipe(slug)
            return format_ingredient_list(recipe)
        except Exception as e:
            return f"Error fetching ingredients for '{slug}': {e}"

    @mcp.tool()
    async def create_recipe_from_url(url: str) -> str:
        """Import a recipe by scraping a URL. Mealie will extract the recipe data automatically.

        Args:
            url: URL of the recipe page to import
        """
        client: MealieClient = get_client()
        try:
            slug = await client.create_recipe_from_url(url)
            return f"Recipe imported successfully! Slug: `{slug}`\n\nUse get_recipe('{slug}') to view the imported recipe."
        except Exception as e:
            return f"Error importing recipe from URL: {e}"

    @mcp.tool()
    async def create_recipe(
        name: str,
        description: str = "",
        recipe_yield: str = "",
        servings: float | None = None,
        total_time: str = "",
        prep_time: str = "",
        perform_time: str = "",
        ingredients: list[dict] | None = None,
        instructions: list[str] | None = None,
        categories: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> str:
        """Create a new recipe manually.

        Args:
            name: Recipe name
            description: Short description
            recipe_yield: Yield description (e.g. "15–18 rolls", "1 loaf")
            servings: Numeric serving count that enables scaling (e.g. 6, 8, 15)
            total_time: Total time (e.g. "45 minutes")
            prep_time: Prep time
            perform_time: Cook time
            ingredients: List of ingredient dicts, each with optional keys:
                - quantity (float): numeric amount (e.g. 300, 2.5)
                - unit (str): unit name or abbreviation (e.g. "g", "cup", "tbsp")
                - food (str): ingredient name (e.g. "bread flour", "butter")
                - comment (str): extra info shown alongside (e.g. "softened", "about 1¾ tsp")
            instructions: List of instruction steps
            categories: Category names to assign
            tags: Tag names to assign
        """
        client: MealieClient = get_client()
        try:
            slug = await client.create_recipe(name)
            update_data: dict[str, Any] = {}
            if description:
                update_data["description"] = description
            if recipe_yield:
                update_data["recipeYield"] = recipe_yield
            if servings is not None:
                update_data["recipeServings"] = servings
            if total_time:
                update_data["totalTime"] = total_time
            if prep_time:
                update_data["prepTime"] = prep_time
            if perform_time:
                update_data["performTime"] = perform_time
            if ingredients:
                update_data["recipeIngredient"] = await _resolve_ingredients(client, ingredients)
            if instructions:
                update_data["recipeInstructions"] = [
                    {"id": str(uuid.uuid4()), "title": "", "summary": "", "text": step, "ingredientReferences": []}
                    for step in instructions
                ]
            if categories:
                all_cats = (await client.get_categories()).get("items", [])
                cat_lookup = {c["name"].lower(): c for c in all_cats}
                resolved_cats = []
                for c in categories:
                    match = cat_lookup.get(c.lower())
                    if match:
                        resolved_cats.append({"id": match["id"], "name": match["name"], "slug": match["slug"]})
                    else:
                        resolved_cats.append({"name": c})
                update_data["recipeCategory"] = resolved_cats
            if tags:
                all_tags = (await client.get_tags()).get("items", [])
                tag_lookup = {t["name"].lower(): t for t in all_tags}
                resolved_tags = []
                for t in tags:
                    match = tag_lookup.get(t.lower())
                    if match:
                        resolved_tags.append({"id": match["id"], "name": match["name"], "slug": match["slug"]})
                    else:
                        resolved_tags.append({"name": t})
                update_data["tags"] = resolved_tags

            if update_data:
                await client.update_recipe(slug, update_data)

            return f"Recipe '{name}' created! Slug: `{slug}`\n\nUse get_recipe('{slug}') to view it."
        except Exception as e:
            return f"Error creating recipe: {e}"

    @mcp.tool()
    async def update_recipe(
        slug: str,
        name: str | None = None,
        description: str | None = None,
        recipe_yield: str | None = None,
        servings: float | None = None,
        total_time: str | None = None,
        prep_time: str | None = None,
        perform_time: str | None = None,
        ingredients: list[dict] | None = None,
        instructions: list[str] | None = None,
        categories: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> str:
        """Update fields on an existing recipe. Only provided fields are changed.

        Args:
            slug: Recipe slug to update
            name: New recipe name
            description: New description
            recipe_yield: Yield description (e.g. "15–18 rolls", "1 loaf")
            servings: Numeric serving count that enables scaling (e.g. 6, 8, 15)
            total_time: New total time
            prep_time: New prep time
            perform_time: New cook time
            ingredients: Replace ingredient list. Each dict has optional keys:
                - quantity (float): numeric amount (e.g. 300, 2.5)
                - unit (str): unit name or abbreviation (e.g. "g", "cup", "tbsp")
                - food (str): ingredient name (e.g. "bread flour", "butter")
                - comment (str): extra info shown alongside (e.g. "softened", "about 1¾ tsp")
            instructions: Replace instruction steps
            categories: Replace categories
            tags: Replace tags
        """
        client: MealieClient = get_client()
        try:
            update_data: dict[str, Any] = {}
            if name is not None:
                update_data["name"] = name
            if description is not None:
                update_data["description"] = description
            if recipe_yield is not None:
                update_data["recipeYield"] = recipe_yield
            if servings is not None:
                update_data["recipeServings"] = servings
            if total_time is not None:
                update_data["totalTime"] = total_time
            if prep_time is not None:
                update_data["prepTime"] = prep_time
            if perform_time is not None:
                update_data["performTime"] = perform_time
            if ingredients is not None:
                update_data["recipeIngredient"] = await _resolve_ingredients(client, ingredients)
            if instructions is not None:
                update_data["recipeInstructions"] = [
                    {"id": str(uuid.uuid4()), "title": "", "summary": "", "text": step, "ingredientReferences": []}
                    for step in instructions
                ]
            if categories is not None:
                all_cats = (await client.get_categories()).get("items", [])
                cat_lookup = {c["name"].lower(): c for c in all_cats}
                resolved_cats = []
                for c in categories:
                    match = cat_lookup.get(c.lower())
                    if match:
                        resolved_cats.append({"id": match["id"], "name": match["name"], "slug": match["slug"]})
                    else:
                        resolved_cats.append({"name": c})
                update_data["recipeCategory"] = resolved_cats
            if tags is not None:
                all_tags = (await client.get_tags()).get("items", [])
                tag_lookup = {t["name"].lower(): t for t in all_tags}
                resolved_tags = []
                for t in tags:
                    match = tag_lookup.get(t.lower())
                    if match:
                        resolved_tags.append({"id": match["id"], "name": match["name"], "slug": match["slug"]})
                    else:
                        resolved_tags.append({"name": t})
                update_data["tags"] = resolved_tags

            if not update_data:
                return "No fields to update. Provide at least one field to change."

            recipe = await client.update_recipe(slug, update_data)
            return f"Recipe updated! Slug: `{recipe.get('slug', slug)}`"
        except Exception as e:
            return f"Error updating recipe '{slug}': {e}"

    @mcp.tool()
    async def delete_recipe(slug: str) -> str:
        """Delete a recipe permanently.

        Args:
            slug: Recipe slug to delete
        """
        client: MealieClient = get_client()
        try:
            await client.delete_recipe(slug)
            return f"Recipe '{slug}' deleted."
        except Exception as e:
            return f"Error deleting recipe '{slug}': {e}"
