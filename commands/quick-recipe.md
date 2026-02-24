---
name: quick-recipe
description: Quickly create a new recipe in Mealie with guided ingredient and instruction entry. Applies family dietary defaults (servings 6, no pork, no seed oils, mild heat).
argument-hint: "[recipe name]"
allowed-tools: mcp__plugin_mealie_mealie__create_recipe, mcp__plugin_mealie_mealie__update_recipe, mcp__plugin_mealie_mealie__get_categories, mcp__plugin_mealie_mealie__get_tags, mcp__plugin_mealie_mealie__search_foods, mcp__plugin_mealie_mealie__get_units, mcp__plugin_mealie_mealie__get_recipe
---

Create a new recipe in Mealie following the family's dietary guidelines and Mealie v3 format.

## Step 1: Get the Recipe Name

Use $ARGUMENTS as the recipe name. If $ARGUMENTS is empty, ask the user: "What's the name of the recipe?"

## Step 2: Gather Basic Details

Ask for (or accept from context):
- **Description**: One-sentence summary (optional but encouraged)
- **Servings**: Default to 6. Ask if different.
- **Total time**: e.g., "45 minutes", "1 hour 30 minutes"
- **Prep time** and **cook time** (optional breakdown)
- **Categories**: e.g., "Main Courses", "Sides", "Breads", "Soups & Stews", "Desserts"
- **Tags**: e.g., "beef", "chicken", "winter", "quick", "make-ahead"

## Step 3: Collect Ingredients

Ask: "Would you like to group ingredients with section headers? (e.g., 'The Protein', 'The Aromatics') — or list them all together?"

Then collect ingredients interactively. For each, gather:
- Quantity (number, or blank for "to taste")
- Unit (cup, tbsp, g, lb, oz — or blank)
- Food name
- Preparation note (optional — e.g., "diced", "softened", "room temperature")

After all ingredients are collected, run a dietary compliance check:
- Flag any pork products (bacon, ham, lard, pork sausage, prosciutto, etc.)
- Flag any seed oils (canola, vegetable, sunflower, safflower, corn, soybean, grapeseed)
- If violations found, notify the user and suggest compliant alternatives before proceeding

## Step 4: Collect Instructions

Ask: "Should I format the instructions with step titles and summaries (for Cook Mode), or just as plain numbered steps?"

Collect each step. For titled steps, get:
- **Title**: Brief verb phrase (e.g., "Sear the Beef")
- **Summary**: One-line takeaway (e.g., "Build deep browning for flavor")
- **Body**: Full instruction text

For plain steps: just the instruction text.

## Step 5: Add Notes (Optional)

Ask: "Any notes to add? (e.g., make-ahead tips, storage, substitutions, serving suggestions)"

Collect as named sections: ask for a title and the note text.

## Step 6: Create the Recipe

Call `create_recipe` with all collected fields structured as:
- `name`: recipe name
- `description`: description if provided
- `servings`: number (default 6)
- `recipe_yield`: yield string if provided
- `total_time`, `prep_time`, `perform_time`: as provided
- `ingredients`: list with section dicts and ingredient dicts
- `instructions`: list of dicts with title/summary/text, or plain strings
- `categories`: list of category names
- `tags`: list of tag names
- `notes`: list of `{title, text}` dicts

## Step 7: Confirm

After the recipe is created, call `get_recipe` with the returned slug to display the full formatted recipe. Confirm with the user: "Recipe '[name]' saved! Slug: `[slug]`"

If anything looks wrong, offer to use `update_recipe` to fix it.
