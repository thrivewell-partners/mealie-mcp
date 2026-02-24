---
name: recipe-creation
description: This skill should be used when the user asks to "create a recipe", "add a recipe to Mealie", "write a recipe for [dish]", "add [dish name] to Mealie", "make a new recipe", "I want to save a recipe", "build a recipe", "put this recipe in Mealie", or provides recipe details and wants them saved. Covers the full workflow for authoring structured recipes against the Mealie v3 API with family dietary defaults.
version: 1.0.0
---

# Recipe Creation

Create well-structured recipes in Mealie using the MCP server tools, following the family's dietary guidelines and the Mealie v3 data format.

## Overview

Every recipe creation follows the same two-phase flow:

1. **Gather** — collect name, description, times, servings, ingredients, instructions, categories, tags, and notes from the user
2. **Create** — call `mcp__plugin_mealie_mealie__create_recipe` with all fields in one pass (the tool handles the create-then-patch sequence internally)

Apply the family's defaults automatically unless the user specifies otherwise:
- Servings: **6** (scale all quantities accordingly)
- Heat level: mild to moderate — no habanero, bird's eye, or scotch bonnet; jalapeño seeded is fine
- No pork, no seed oils — see the dietary-management skill for details

---

## Step 1: Gather Recipe Information

Collect the following, asking the user only for what they haven't already provided:

| Field | Parameter | Notes |
|-------|-----------|-------|
| Name | `name` | Required |
| Description | `description` | One-sentence summary |
| Servings | `servings` | Numeric; default 6 |
| Yield text | `recipe_yield` | e.g., "6 servings", "1 loaf", "15–18 rolls" |
| Total time | `total_time` | e.g., "1 hour 30 minutes" |
| Prep time | `prep_time` | e.g., "20 minutes" |
| Cook time | `perform_time` | e.g., "1 hour 10 minutes" |
| Categories | `categories` | List of category names (e.g., "Main Courses") |
| Tags | `tags` | List of tag names (e.g., "beef", "winter") |

---

## Step 2: Structure the Ingredients

Pass ingredients as a list of dicts to the `ingredients` parameter. Two kinds of items are supported:

### Section Headers

Group ingredients visually. Use a dict with only a `"section"` key:

```json
{"section": "The Aromatics"}
```

Section names should be descriptive and meaningful: "The Protein", "The Liquid Base", "The Vegetables", "For the Dough", "For the Filling", "Seasoning Blend".

### Ingredient Items

Each ingredient is a dict with these optional keys:

| Key | Type | Description |
|-----|------|-------------|
| `quantity` | float | Numeric amount (e.g., `2`, `0.5`, `300`) |
| `unit` | string | Unit name or abbreviation (e.g., `"cup"`, `"g"`, `"tbsp"`, `"lb"`) |
| `food` | string | Ingredient name (e.g., `"bread flour"`, `"avocado oil"`, `"beef chuck"`) |
| `comment` | string | Preparation note displayed alongside (e.g., `"softened"`, `"roughly chopped"`, `"about 1¾ tsp"`) |

```json
[
  {"section": "The Protein"},
  {"quantity": 2, "unit": "lb", "food": "beef chuck", "comment": "cut into 1½-inch cubes"},
  {"quantity": 1, "unit": "tsp", "food": "kosher salt"},
  {"section": "The Aromatics"},
  {"quantity": 1, "food": "onion", "comment": "diced"},
  {"quantity": 4, "food": "garlic cloves", "comment": "minced"}
]
```

**Important:** Omit keys that don't apply — don't pass `null` or empty strings. The food lookup auto-creates missing foods in Mealie's database.

---

## Step 3: Structure the Instructions

Pass instructions as a list to the `instructions` parameter. Each item can be a plain string or an enhanced dict:

### Plain String (simple recipes)

```json
"Brown the beef in batches over high heat. Do not crowd the pan."
```

### Enhanced Dict (preferred — enables Cook Mode)

```json
{
  "title": "Sear the Beef",
  "summary": "Develop fond and flavor with high-heat browning",
  "text": "Pat the beef cubes dry with paper towels — moisture is the enemy of browning. Heat 2 tbsp avocado oil in a Dutch oven over high heat until shimmering. Working in batches of 6–8 pieces, sear each cube undisturbed for 90 seconds per side. The goal is deep mahogany crust on at least two faces. Transfer to a plate and repeat, adding oil as needed. Do not skip this step — the fond left in the pot is where the flavor lives."
}
```

| Key | Purpose |
|-----|---------|
| `title` | Step heading shown in Cook Mode |
| `summary` | One-liner takeaway for step-navigation |
| `text` | Full instruction body — include the "why" |

Use enhanced dicts for any recipe with more than 5 steps. Plain strings are fine for quick/simple recipes where the user just wants to save something fast.

---

## Step 4: Structure the Notes

Pass notes as a list of dicts to the `notes` parameter. Each note has a title and body:

```json
[
  {
    "title": "Make-Ahead",
    "text": "This stew is better the next day. Make it through step 5, cool completely, refrigerate overnight. Reheat gently and finish with the herb garnish fresh."
  },
  {
    "title": "Substitutions",
    "text": "Beef chuck is ideal but short ribs or oxtail also work beautifully. Increase braising time to 3–4 hours for oxtail. For a richer result, use tallow instead of avocado oil for the sear."
  }
]
```

Use notes for: make-ahead instructions, storage, substitutions, troubleshooting, serving suggestions, scaling notes.

---

## Step 5: Check Dietary Compliance

Before calling `create_recipe`, run a mental compliance check:

- **No pork**: No bacon, ham, lard, pork sausage, prosciutto, chorizo (pork-based), pork rinds, pork chops, carnitas
- **No seed oils**: No vegetable oil, canola oil, sunflower oil, safflower oil, corn oil, soybean oil, cottonseed oil, grapeseed oil
- **Compliant oils**: avocado oil, tallow, ghee, butter, olive oil, coconut oil

If the recipe as described contains violations, flag them and suggest compliant alternatives before saving. The PreToolUse hook will also catch violations, but catching them before the tool call is better UX.

---

## Step 6: Call create_recipe

Assemble the full call:

```json
{
  "name": "Braised Beef Stew",
  "description": "A rich, slow-braised beef stew built on fond and aromatic vegetables",
  "servings": 6,
  "recipe_yield": "6 generous servings",
  "total_time": "3 hours",
  "prep_time": "30 minutes",
  "perform_time": "2 hours 30 minutes",
  "ingredients": [...],
  "instructions": [...],
  "categories": ["Main Courses"],
  "tags": ["beef", "winter", "braised"],
  "notes": [...]
}
```

After creation, call `mcp__plugin_mealie_mealie__get_recipe` with the returned slug to confirm everything saved correctly, then show the user the formatted result.

---

## Extras and Foundation Flag

For **Foundation recipes** (educational "why behind the how" recipes), add:

```json
"extras": {"isFoundation": "1"}
```

Note: Mealie stores this as the string `"1"`, not boolean `true`. See the **foundations** skill for full Foundation recipe authoring guidance.

---

## Categories and Tags Strategy

Standard category names in use:
- "Main Courses", "Sides", "Breads", "Soups & Stews", "Desserts", "Foundations", "Breakfasts"

Standard tag patterns:
- Protein: `"beef"`, `"chicken"`, `"lamb"`, `"fish"`, `"turkey"`, `"vegetarian"`
- Season: `"winter"`, `"summer"`, `"fall"`, `"spring"`
- Method: `"braised"`, `"roasted"`, `"baked"`, `"grilled"`, `"fermented"`
- Character: `"quick"`, `"make-ahead"`, `"kid-favorite"`, `"batch-cook"`

---

## Quick Reference

```
create_recipe(
  name="...",
  description="...",
  servings=6,
  recipe_yield="...",
  total_time="...", prep_time="...", perform_time="...",
  ingredients=[
    {"section": "Group Name"},
    {"quantity": N, "unit": "...", "food": "...", "comment": "..."},
    ...
  ],
  instructions=[
    {"title": "...", "summary": "...", "text": "..."},
    ...
  ],
  categories=["..."],
  tags=["..."],
  notes=[{"title": "...", "text": "..."}, ...],
  extras={"isFoundation": "1"}  # only for Foundation recipes
)
```

---

## Additional Resources

### Reference Files

- **`references/mealie-v3-format.md`** — Complete format specification with full annotated examples for ingredients, instructions, and notes
- **`references/family-guidelines.md`** — Full family dietary rules, preferred ingredients, and scaling guidance

### Related Skills

- **`foundations`** skill — For creating educational Foundation recipes with the full paradigm (section headers, named notes, isFoundation extras)
- **`dietary-management`** skill — For evaluating existing recipes and finding compliant substitutions
