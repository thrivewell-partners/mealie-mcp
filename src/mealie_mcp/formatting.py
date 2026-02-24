from __future__ import annotations

from typing import Any


def format_recipe_summary(recipe: dict) -> str:
    """Format a recipe for search results / list views."""
    parts = [f"**{recipe.get('name', 'Untitled')}**"]
    parts.append(f"  Slug: `{recipe.get('slug', '')}`")
    if recipe.get("description"):
        parts.append(f"  {recipe['description'][:120]}")
    cats = recipe.get("recipeCategory") or []
    if cats:
        cat_names = [c["name"] if isinstance(c, dict) else c for c in cats]
        parts.append(f"  Categories: {', '.join(cat_names)}")
    tags = recipe.get("tags") or []
    if tags:
        tag_names = [t["name"] if isinstance(t, dict) else t for t in tags]
        parts.append(f"  Tags: {', '.join(tag_names)}")
    if recipe.get("totalTime"):
        parts.append(f"  Time: {recipe['totalTime']}")
    if recipe.get("rating"):
        parts.append(f"  Rating: {'★' * int(recipe['rating'])}")
    return "\n".join(parts)


def format_recipe_detail(recipe: dict) -> str:
    """Format a full recipe for detailed view."""
    lines: list[str] = []
    lines.append(f"# {recipe.get('name', 'Untitled')}")
    lines.append(f"Slug: `{recipe.get('slug', '')}`")
    if recipe.get("description"):
        lines.append(f"\n{recipe['description']}")
    if recipe.get("totalTime"):
        lines.append(f"\nTotal Time: {recipe['totalTime']}")
    if recipe.get("prepTime"):
        lines.append(f"Prep Time: {recipe['prepTime']}")
    if recipe.get("performTime"):
        lines.append(f"Cook Time: {recipe['performTime']}")
    if recipe.get("recipeYield"):
        lines.append(f"Servings: {recipe['recipeYield']}")

    cats = recipe.get("recipeCategory") or []
    if cats:
        cat_names = [c["name"] if isinstance(c, dict) else c for c in cats]
        lines.append(f"Categories: {', '.join(cat_names)}")
    tags = recipe.get("tags") or []
    if tags:
        tag_names = [t["name"] if isinstance(t, dict) else t for t in tags]
        lines.append(f"Tags: {', '.join(tag_names)}")

    ingredients = recipe.get("recipeIngredient") or []
    if ingredients:
        lines.append("\n## Ingredients")
        for ing in ingredients:
            if isinstance(ing, dict) and ing.get("title") and not ing.get("food") and not ing.get("note") and not ing.get("quantity"):
                lines.append(f"\n### {ing['title']}")
            else:
                lines.append(f"- {_format_ingredient(ing)}")

    instructions = recipe.get("recipeInstructions") or []
    if instructions:
        lines.append("\n## Instructions")
        for i, step in enumerate(instructions, 1):
            if isinstance(step, dict):
                title = step.get("title", "")
                text = step.get("text", "")
                summary = step.get("summary", "")
                if title:
                    lines.append(f"{i}. **{title}**")
                    if summary:
                        lines.append(f"   *{summary}*")
                    if text:
                        lines.append(f"   {text}")
                else:
                    lines.append(f"{i}. {text}")
            else:
                lines.append(f"{i}. {str(step)}")

    nutrition = recipe.get("nutrition") or {}
    nutrition_items = {
        k: v for k, v in nutrition.items() if v and k != "nutritionId"
    }
    if nutrition_items:
        lines.append("\n## Nutrition")
        for key, val in nutrition_items.items():
            lines.append(f"- {key}: {val}")

    notes = recipe.get("notes") or []
    if notes:
        lines.append("\n## Notes")
        for note in notes:
            if isinstance(note, dict):
                title = note.get("title", "")
                text = note.get("text", "")
                if title:
                    lines.append(f"\n### {title}")
                if text:
                    lines.append(text)
            else:
                lines.append(f"- {str(note)}")

    return "\n".join(lines)


def format_ingredient_list(recipe: dict) -> str:
    """Format just the ingredients from a recipe."""
    lines = [f"## Ingredients for {recipe.get('name', 'Untitled')}"]
    lines.append(f"Slug: `{recipe.get('slug', '')}`")
    for ing in recipe.get("recipeIngredient", []):
        if isinstance(ing, dict) and ing.get("title") and not ing.get("food") and not ing.get("note") and not ing.get("quantity"):
            lines.append(f"\n### {ing['title']}")
        else:
            lines.append(f"- {_format_ingredient(ing)}")
    return "\n".join(lines)


def _format_ingredient(ing: Any) -> str:
    if isinstance(ing, str):
        return ing
    parts: list[str] = []
    if ing.get("quantity") and ing["quantity"] > 0:
        q = ing["quantity"]
        parts.append(str(int(q)) if q == int(q) else str(q))
    if ing.get("unit"):
        unit = ing["unit"]
        parts.append(unit["name"] if isinstance(unit, dict) else str(unit))
    if ing.get("food"):
        food = ing["food"]
        parts.append(food["name"] if isinstance(food, dict) else str(food))
    if ing.get("note"):
        parts.append(f"({ing['note']})")
    if not parts:
        return ing.get("display", ing.get("note", "unknown ingredient"))
    return " ".join(parts)


def format_shopping_list_summary(sl: dict) -> str:
    """Format a shopping list for list views."""
    name = sl.get("name", "Untitled")
    list_id = sl.get("id", "")
    items = sl.get("listItems") or []
    checked = sum(1 for i in items if i.get("checked"))
    return f"**{name}** (id: `{list_id}`) — {len(items)} items, {checked} checked"


def format_shopping_list_detail(sl: dict) -> str:
    """Format a shopping list with all items."""
    lines = [f"# {sl.get('name', 'Untitled')}"]
    lines.append(f"List ID: `{sl.get('id', '')}`")
    items = sl.get("listItems") or []
    if not items:
        lines.append("\n(empty list)")
        return "\n".join(lines)

    unchecked = [i for i in items if not i.get("checked")]
    checked = [i for i in items if i.get("checked")]

    if unchecked:
        lines.append(f"\n## To Get ({len(unchecked)})")
        for item in unchecked:
            lines.append(f"- [ ] {_format_shopping_item(item)}")
    if checked:
        lines.append(f"\n## Done ({len(checked)})")
        for item in checked:
            lines.append(f"- [x] {_format_shopping_item(item)}")
    return "\n".join(lines)


def _format_shopping_item(item: dict) -> str:
    parts: list[str] = []
    if item.get("quantity") and item["quantity"] > 0:
        q = item["quantity"]
        parts.append(str(int(q)) if q == int(q) else str(q))
    if item.get("unit"):
        u = item["unit"]
        parts.append(u["name"] if isinstance(u, dict) else str(u))
    if item.get("food"):
        f = item["food"]
        parts.append(f["name"] if isinstance(f, dict) else str(f))
    if item.get("note"):
        parts.append(item["note"])
    text = " ".join(parts) if parts else "unnamed item"
    return f"{text} (item_id: `{item.get('id', '')}`)"


def format_meal_plan_entry(entry: dict) -> str:
    """Format a single meal plan entry."""
    date = entry.get("date", "?")
    entry_type = entry.get("entryType", "?")
    entry_id = entry.get("id", "")
    recipe = entry.get("recipe")
    if recipe:
        name = recipe.get("name", "Untitled")
        slug = recipe.get("slug", "")
        return f"- [{date}] {entry_type}: **{name}** (slug: `{slug}`, entry_id: `{entry_id}`)"
    title = entry.get("title", "")
    note = entry.get("text", "")
    desc = title or note or "No details"
    return f"- [{date}] {entry_type}: {desc} (entry_id: `{entry_id}`)"


def format_meal_plans(entries: list[dict]) -> str:
    """Format a list of meal plan entries."""
    if not entries:
        return "No meal plan entries found for this date range."
    lines = ["## Meal Plan"]
    for entry in sorted(entries, key=lambda e: (e.get("date", ""), e.get("entryType", ""))):
        lines.append(format_meal_plan_entry(entry))
    return "\n".join(lines)


def format_categories(items: list[dict]) -> str:
    if not items:
        return "No categories found."
    lines = ["## Categories"]
    for c in items:
        name = c.get("name", "?")
        slug = c.get("slug", "")
        count = c.get("recipes", [])
        n = len(count) if isinstance(count, list) else count
        lines.append(f"- **{name}** (slug: `{slug}`, {n} recipes)")
    return "\n".join(lines)


def format_tags(items: list[dict]) -> str:
    if not items:
        return "No tags found."
    lines = ["## Tags"]
    for t in items:
        name = t.get("name", "?")
        slug = t.get("slug", "")
        lines.append(f"- **{name}** (slug: `{slug}`)")
    return "\n".join(lines)


def format_cookbooks(items: list[dict]) -> str:
    if not items:
        return "No cookbooks found."
    lines = ["## Cookbooks"]
    for cb in items:
        name = cb.get("name", "?")
        slug = cb.get("slug", "")
        lines.append(f"- **{name}** (slug: `{slug}`)")
    return "\n".join(lines)


def format_foods(items: list[dict]) -> str:
    if not items:
        return "No foods found."
    lines = ["## Foods"]
    for f in items:
        name = f.get("name", "?")
        fid = f.get("id", "")
        lines.append(f"- {name} (id: `{fid}`)")
    return "\n".join(lines)


def format_units(items: list[dict]) -> str:
    if not items:
        return "No units found."
    lines = ["## Units"]
    for u in items:
        name = u.get("name", "?")
        uid = u.get("id", "")
        abbr = u.get("abbreviation", "")
        suffix = f" ({abbr})" if abbr else ""
        lines.append(f"- {name}{suffix} (id: `{uid}`)")
    return "\n".join(lines)
