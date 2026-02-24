---
name: weekly-menu
description: Plan a week of family dinners in Mealie's meal planner using the recipe library and family dietary preferences. Creates meal plan entries in Mealie after user approval.
argument-hint: "[start date YYYY-MM-DD]"
allowed-tools: mcp__plugin_mealie_mealie__search_recipes, mcp__plugin_mealie_mealie__get_meal_plans, mcp__plugin_mealie_mealie__create_meal_plan_entry, mcp__plugin_mealie_mealie__delete_meal_plan_entry, mcp__plugin_mealie_mealie__add_recipe_to_shopping_list, mcp__plugin_mealie_mealie__get_shopping_lists, mcp__plugin_mealie_mealie__create_shopping_list, mcp__plugin_mealie_mealie__get_recipe
---

Plan a balanced week of family dinners and optionally build a shopping list.

## Step 1: Determine the Week

- If $ARGUMENTS contains a date in YYYY-MM-DD format, use it as the start date
- Otherwise, default to the upcoming Monday as start date
- Calculate the end date (7 days from start)
- Confirm with the user: "Planning [Monday date] through [Sunday date] — is that right?"

## Step 2: Check What's Already Planned

Call `get_meal_plans(start_date=..., end_date=...)` for the week.

List which days already have entries and which are open. Ask: "I see [days] are already planned. Should I fill in the remaining days, or replace everything and start fresh?"

## Step 3: Search for Recipes

Browse the library to find viable options. Aim for variety across protein types:

```
search_recipes(tags=["beef"])      # Beef options
search_recipes(tags=["chicken"])   # Chicken options
search_recipes(categories=["Main Courses"])  # All mains
```

Note available recipes and their categories, tags, and time estimates.

## Step 4: Draft the Week Plan

Build a balanced dinner plan:
- **Monday**: Chicken (lighter transition from weekend)
- **Tuesday**: Beef (hearty midweek)
- **Wednesday**: Quick reheat or leftovers from a batch (note with `title` not slug)
- **Thursday**: Variable protein (lamb, turkey, duck)
- **Friday**: Fish, eggs as main, or lighter dish
- **Saturday**: Elaborate or celebratory dinner
- **Sunday**: Batch cook anchor (stew, chili, braised chicken) that feeds tonight and provides leftovers

Adjust based on available recipes and user requests.

## Step 5: Present the Plan for Approval

Show the draft before creating any entries:

```
Here's the plan for [dates]:

Mon [date] — [Recipe Name] ([time]) — [slug or "new recipe needed"]
Tue [date] — [Recipe Name] ([time])
Wed [date] — Leftover [dish from Sunday]
Thu [date] — [Recipe Name] ([time])
Fri [date] — [Recipe Name] ([time])
Sat [date] — [Recipe Name] ([time])
Sun [date] — [Recipe Name] (batch cook, ~3 hrs)

Shall I add these to Mealie? Any swaps?
```

Wait for explicit confirmation before making API calls.

## Step 6: Create Meal Plan Entries

For each approved day, call `create_meal_plan_entry`:
- Use `recipe_slug` for recipes that exist in Mealie
- Use `title` parameter for leftover nights or placeholder meals
- `entry_type`: use "dinner" for all unless user requested other meal types

## Step 7: Offer Shopping List

Ask: "Should I add the ingredients for all planned recipes to a shopping list?"

If yes:
1. Call `get_shopping_lists` to find available lists
2. Ask which list to use, or offer to create a new one with `create_shopping_list`
3. Call `add_recipe_to_shopping_list(list_id=..., recipe_slug=...)` for each recipe-based entry
4. Report total: "Added ingredients for [N] recipes to [list name]"

## Notes

- Comply with family rules: no pork, no seed oils, mild heat, serve 6
- If a desired dish doesn't exist in Mealie yet, note it and suggest creating it with `/mealie:quick-recipe` before adding to the plan
- Leftover and batch-cook entries use `title` instead of `recipe_slug`
