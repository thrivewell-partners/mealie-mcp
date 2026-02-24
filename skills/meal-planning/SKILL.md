---
name: meal-planning
description: This skill should be used when the user asks to "plan meals for the week", "what should we eat this week", "weekly menu", "meal plan", "plan dinners for the week", "plan the week", "fill in the meal plan", "what's for dinner this week", "help me plan meals", "set up the meal plan for [dates]", or wants to use Mealie's meal planning feature to organize a week of family meals.
version: 1.0.0
---

# Meal Planning

Build weekly meal plans in Mealie using the family's recipe library, protein rotation philosophy, and batch cooking strategy.

## Mealie Meal Plan API Overview

### Reading the Current Plan

```
get_meal_plans(start_date="YYYY-MM-DD", end_date="YYYY-MM-DD")
```

Always check what's already planned before filling in a week. This avoids duplicating entries.

### Creating an Entry

```
create_meal_plan_entry(
  date="YYYY-MM-DD",       # Required
  entry_type="dinner",      # "breakfast" | "lunch" | "dinner" | "side"
  recipe_slug="beef-stew-foundation"  # Or use title/note for no-recipe entries
)
```

**Entry types:**
- `"dinner"` — default for weekly planning
- `"breakfast"` — morning meals
- `"lunch"` — midday meals
- `"side"` — accompaniments to a main

**Dates must be in `YYYY-MM-DD` format.** Always verify the date format before making API calls.

### Deleting an Entry

```
delete_meal_plan_entry(entry_id="...")
```

Entry IDs are returned by `get_meal_plans`.

### Adding Ingredients to a Shopping List

After planning the week, add all recipe ingredients to a shopping list:

```
add_recipe_to_shopping_list(list_id="...", recipe_slug="...")
```

Call this for each planned recipe to build a comprehensive grocery list.

---

## The Planning Process

### Step 1: Determine the Date Range

- If the user provides a start date, use it
- If not, default to the upcoming Monday–Sunday
- Always plan Sunday through Saturday or Monday through Sunday (7 days)
- Date format: `YYYY-MM-DD`

### Step 2: Check What's Already Planned

Call `get_meal_plans` for the week. Note which dates are already filled and which are open.

### Step 3: Find Available Recipes

Use `search_recipes` to browse the library. Get a variety across:
- Protein types (beef, chicken, lamb/turkey, fish, vegetarian)
- Preparation methods (braised, roasted, quick stovetop)
- Time commitment (batch-cook dishes for Sunday, quick dishes for busy weeknights)

Useful searches:
- `search_recipes(tags=["beef"])` — beef recipes
- `search_recipes(tags=["chicken"])` — chicken recipes
- `search_recipes(categories=["Main Courses"])` — all mains
- `search_recipes(tags=["quick"])` — weeknight-friendly

### Step 4: Draft the Week

Build a balanced plan following the protein rotation:

| Day | Protein Anchor | Character |
|-----|---------------|-----------|
| Monday | Chicken | Often lighter, transitioning from weekend |
| Tuesday | Beef | Hearty midweek |
| Wednesday | Quick / Leftovers | Busy night — use Monday's extra batch |
| Thursday | Lamb or Turkey | Variety protein |
| Friday | Fish or Pasta | End-of-week flexibility |
| Saturday | Beef or Chicken | Family dinner — more elaborate |
| Sunday | Batch cook + Soup/Stew | Sets up the week |

Adjust based on what's in the recipe library and what the user requests.

### Step 5: Present the Plan for Approval

Before creating entries in Mealie, present the draft plan to the user:

```
Here's the week I'm planning:

Monday 2/24 — Roasted Chicken Thighs with Root Vegetables (45 min)
Tuesday 2/25 — Beef Stew — Foundation (3 hrs, batch cook Sunday)
Wednesday 2/26 — Leftover stew + fresh bread rolls
Thursday 2/27 — [Turkey dish or lamb if available]
Friday 2/28 — [Fish or pasta dish]
Saturday 3/1 — [Elaborate beef or chicken dish]
Sunday 3/2 — Batch cook: stock + chili

Shall I add these to Mealie's meal planner? I can also suggest recipes if any slots are empty.
```

### Step 6: Create Entries in Mealie

On approval, call `create_meal_plan_entry` for each dinner. For recipes that don't have a slug yet or are placeholder ideas, use the `title` parameter instead of `recipe_slug`.

### Step 7: Offer Shopping List Integration

```
Would you like me to add all the ingredients to a shopping list?
```

If yes: call `get_shopping_lists` to find or create a list, then `add_recipe_to_shopping_list` for each planned recipe.

---

## Planning Philosophy for This Family

### Protein Rotation

Rotate through four protein anchors each week:
1. **Beef** (2x/week) — chuck roast, ground beef, short ribs, brisket
2. **Chicken** (2x/week) — whole birds, thighs, drumsticks
3. **Variable** (1–2x/week) — lamb, turkey, duck, game
4. **Fish/Other** (1x/week) — salmon, cod, sardines, eggs-as-main

Avoid the same protein two days in a row unless using leftovers intentionally.

### Batch Cooking Anchor

Sunday (or a designated batch cook day) sets up the week:
- Cook a large braise (stew, chili, braised chicken) that provides dinner Sunday + at least one quick reheat night
- Make a stock if bones are available
- Mix and cold-ferment bread dough for rolls or loaves later in the week
- Prep aromatics (dice onions, mince garlic) for the week

### Leftovers as a Feature

Plan intentional leftovers rather than treating them as accidents:
- Double the stew recipe → dinner Tuesday AND Wednesday lunch
- Roast a full chicken → dinner Monday, chicken salad Tuesday lunch
- Big pot of chili → two dinners + a lunch

In the meal plan, list "Leftover [dish]" using the `title` parameter instead of a recipe slug.

### Seasonality

Adjust plans by season:
- **Winter**: braised meats, root vegetables, soups, hearty bread
- **Summer**: grilled meats, fresh vegetables, lighter sides
- **Fall**: roasted dishes, squash, apples, warm spices
- **Spring**: lighter proteins, fresh greens, asparagus, herbs

---

## Additional Resources

### Reference Files

- **`references/planning-approach.md`** — Weekly planning templates, protein rotation tables, batch cooking strategies, and shopping list integration patterns

### Related Skills

- **`recipe-creation`** skill — For adding new recipes to the library before planning
- **`dietary-management`** skill — For verifying planned recipes are family-compliant
