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
        total_time: str = "",
        prep_time: str = "",
        perform_time: str = "",
        ingredients: list[str] | None = None,
        instructions: list[str] | None = None,
        categories: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> str:
        """Create a new recipe manually.

        Args:
            name: Recipe name
            description: Short description
            recipe_yield: Servings (e.g. "4 servings")
            total_time: Total time (e.g. "45 minutes")
            prep_time: Prep time
            perform_time: Cook time
            ingredients: List of ingredient strings (e.g. ["2 cups flour", "1 tsp salt"])
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
            if total_time:
                update_data["totalTime"] = total_time
            if prep_time:
                update_data["prepTime"] = prep_time
            if perform_time:
                update_data["performTime"] = perform_time
            if ingredients:
                update_data["recipeIngredient"] = [
                    {"note": ing, "referenceId": str(uuid.uuid4())} for ing in ingredients
                ]
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
        total_time: str | None = None,
        prep_time: str | None = None,
        perform_time: str | None = None,
        ingredients: list[str] | None = None,
        instructions: list[str] | None = None,
        categories: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> str:
        """Update fields on an existing recipe. Only provided fields are changed.

        Args:
            slug: Recipe slug to update
            name: New recipe name
            description: New description
            recipe_yield: New servings
            total_time: New total time
            prep_time: New prep time
            perform_time: New cook time
            ingredients: Replace ingredient list
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
            if total_time is not None:
                update_data["totalTime"] = total_time
            if prep_time is not None:
                update_data["prepTime"] = prep_time
            if perform_time is not None:
                update_data["performTime"] = perform_time
            if ingredients is not None:
                update_data["recipeIngredient"] = [
                    {"note": ing, "referenceId": str(uuid.uuid4())} for ing in ingredients
                ]
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
