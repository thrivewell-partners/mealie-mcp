---
name: find-recipe
description: Search Mealie for recipes with family-aware filtering and dietary context. Shows results with detail options and integrates with meal planning and shopping lists.
argument-hint: "[search terms] [--category name] [--tag name]"
allowed-tools: mcp__plugin_mealie_mealie__search_recipes, mcp__plugin_mealie_mealie__get_recipe, mcp__plugin_mealie_mealie__get_categories, mcp__plugin_mealie_mealie__get_tags, mcp__plugin_mealie_mealie__create_meal_plan_entry, mcp__plugin_mealie_mealie__add_recipe_to_shopping_list, mcp__plugin_mealie_mealie__get_shopping_lists
---

Search the Mealie recipe library with family context.

## Step 1: Parse the Arguments

From $ARGUMENTS, extract:
- **Search query**: the main search terms (e.g., "beef stew", "chicken", "bread")
- **`--category`**: optional category filter (e.g., `--category "Main Courses"`)
- **`--tag`**: optional tag filter (e.g., `--tag beef` or `--tag winter`)

If $ARGUMENTS is empty, ask: "What are you looking for? (e.g., 'beef recipes', 'quick dinners', 'breads')"

## Step 2: Run the Search

Call `search_recipes` with the extracted parameters:
- `query`: search terms
- `categories`: category filter if provided (as a list)
- `tags`: tag filter if provided (as a list)
- `per_page`: 10 (default)

If no results, broaden the search: try fewer terms, or search by category/tag only.

## Step 3: Display Results

Show results in a clean format:

```
Found [N] recipes:

1. **Beef Stew — Foundation** (`beef-stew-foundation`)
   Categories: Foundations | Tags: beef, winter, braised
   Total time: 3 hrs 30 min

2. **Texas-Style Chili** (`texas-style-chili`)
   Categories: Main Courses | Tags: beef, chili, winter
   Total time: 1 hr 30 min

[...]
```

For any Foundation recipes (category "Foundations" or name contains "Foundation"), add a note: "This is a Foundation recipe — includes full technique explanation."

## Step 4: Offer Detail View

Ask: "Would you like the full details for any of these? (Enter a number or recipe name)"

If yes, call `get_recipe(slug)` and display the full formatted recipe including ingredients, instructions, and notes.

## Step 5: Dietary Notes

For each result, scan visible metadata (name, description, tags) for potential concerns:
- If a recipe name or description contains potential pork terms → note "Check this recipe for pork compliance before using"
- If a recipe name suggests heat → note "Check heat level for kid-friendliness"

This is a lightweight flag, not a full ingredient scan. For full compliance checking, use the dietary-management skill.

## Step 6: Next Actions

After displaying results, offer:

```
What would you like to do next?
1. Add one of these to the meal plan
2. Add ingredients to a shopping list
3. Search for something else
4. Create a new recipe
```

**For meal plan**: ask which recipe and which date, then call `create_meal_plan_entry`

**For shopping list**: ask which recipe and which list (call `get_shopping_lists` to show options), then call `add_recipe_to_shopping_list`

**For new recipe**: point to the `/mealie:quick-recipe` command
