# Mealie v3 Recipe Format Reference

Complete format specification for the `create_recipe` and `update_recipe` MCP tools.

---

## Ingredients (`ingredients` parameter)

Pass a flat list where section headers and ingredient items are interleaved.

### Section Header

```json
{"section": "Section Name"}
```

- Only the `"section"` key is used; all other keys are ignored
- Creates a visual divider with a heading in Mealie's UI
- Use to group ingredients by role or stage

### Ingredient Item

```json
{
  "quantity": 2.5,
  "unit": "cup",
  "food": "bread flour",
  "comment": "spooned and leveled, not scooped"
}
```

| Key | Type | Required | Notes |
|-----|------|----------|-------|
| `quantity` | float | No | Omit for "to taste" or uncounted items |
| `unit` | string | No | Name or abbreviation; looked up in Mealie's units database |
| `food` | string | No | Ingredient name; auto-created if not found in database |
| `comment` | string | No | Prep/modifier note shown alongside the ingredient |

**Omit keys entirely** — do not pass `null` or empty strings.

### Unit Lookup

The server searches Mealie's unit database by name, abbreviation, and plural variants. Common units that resolve reliably:

| You pass | Resolves to |
|----------|-------------|
| `"g"` | grams |
| `"kg"` | kilograms |
| `"oz"` | ounce |
| `"lb"` | pound |
| `"cup"` | cup |
| `"tbsp"` | tablespoon |
| `"tsp"` | teaspoon |
| `"ml"` | milliliter |
| `"l"` | liter |
| `"clove"` | clove |
| `"whole"` | whole |

If a unit is not found, it is silently dropped. Use the exact unit name or abbreviation from Mealie's units list.

### Food Lookup and Auto-Create

1. Server searches existing foods by name (case-insensitive, exact match preferred)
2. If not found, attempts to create the food
3. If creation fails (food already exists with slightly different name), broadens search
4. Normalizes hyphens to spaces (e.g., `"bread-flour"` → `"bread flour"`)

### Complete Ingredients Example

```json
[
  {"section": "The Dough"},
  {"quantity": 500, "unit": "g", "food": "bread flour", "comment": "plus more for dusting"},
  {"quantity": 10, "unit": "g", "food": "kosher salt"},
  {"quantity": 7, "unit": "g", "food": "instant yeast"},
  {"quantity": 325, "unit": "ml", "food": "water", "comment": "lukewarm (80–85°F)"},
  {"quantity": 2, "unit": "tbsp", "food": "avocado oil"},

  {"section": "For Baking"},
  {"quantity": 1, "unit": "tbsp", "food": "avocado oil", "comment": "for the pan"},
  {"food": "flaky sea salt", "comment": "for finishing — optional"}
]
```

---

## Instructions (`instructions` parameter)

Pass a list where each item is either a plain string or an enhanced dict.

### Plain String

```json
"Combine the flour, salt, and yeast in a large bowl. Add the water and oil and mix until shaggy."
```

Use for simple recipes where step titles and cook-mode summaries are not needed.

### Enhanced Dict

```json
{
  "title": "Mix and Develop the Dough",
  "summary": "Combine ingredients and begin gluten development",
  "text": "Combine flour, salt, and yeast in a large mixing bowl, keeping salt and yeast on opposite sides until mixing begins (salt can inhibit yeast on direct contact). Add the lukewarm water and avocado oil. Mix with a dough hook or by hand until the dough comes together into a shaggy mass — about 2 minutes. Do not worry if it looks rough; gluten has not yet developed. Cover and rest 20 minutes (autolyse). This rest allows the flour to fully hydrate and begins gluten formation passively, reducing kneading time."
}
```

| Key | Required | Description |
|-----|----------|-------------|
| `title` | Recommended | Step heading — shown in Mealie's Cook Mode |
| `summary` | Optional | One-liner for step navigation bar |
| `text` | Required | Full instruction body |

### Mixed List (Recommended for Foundation Recipes)

```json
[
  {
    "title": "Bloom the Yeast",
    "summary": "Activate yeast and confirm viability",
    "text": "..."
  },
  {
    "title": "Mix the Dough",
    "summary": "Combine and hydrate",
    "text": "..."
  },
  "Shape into a ball and place in an oiled bowl.",
  {
    "title": "First Fermentation",
    "summary": "Bulk ferment until doubled",
    "text": "..."
  }
]
```

Plain strings and dicts can be mixed freely.

---

## Notes (`notes` parameter)

Pass a list of dicts with `title` and `text` keys:

```json
[
  {
    "title": "Storage",
    "text": "Store wrapped at room temperature for up to 3 days. Freeze sliced with parchment between slices for up to 3 months. Reheat slices in a dry skillet over medium heat for 2 minutes per side."
  },
  {
    "title": "Variations",
    "text": "Add 2 tbsp honey for a slightly sweet crumb. Substitute 20% of the bread flour with whole wheat for more flavor and fiber. Add 1 tsp garlic powder and 2 tbsp dried herbs to the flour for herb bread."
  }
]
```

Notes render as named sections in Mealie's recipe detail view. Use them for:
- Storage instructions
- Make-ahead notes
- Variations and substitutions
- Troubleshooting
- Serving suggestions
- Equipment notes

---

## Extras (`extras` parameter)

Arbitrary JSON metadata stored with the recipe. Currently used for:

| Key | Value | Purpose |
|-----|-------|---------|
| `"isFoundation"` | `"1"` | Marks recipe as a Foundation (string "1", not boolean) |

```json
{"isFoundation": "1"}
```

Mealie stores boolean-like values as strings internally. Always use `"1"` not `true`.

---

## Full create_recipe Example

```json
{
  "name": "Soft Yeast Dinner Rolls",
  "description": "Pillowy, pull-apart dinner rolls with a buttery crust — built for a 6-person table",
  "servings": 6,
  "recipe_yield": "12–15 rolls",
  "total_time": "3 hours",
  "prep_time": "30 minutes",
  "perform_time": "25 minutes",
  "categories": ["Breads"],
  "tags": ["bread", "yeast", "dinner", "kid-favorite"],
  "ingredients": [
    {"section": "The Dough"},
    {"quantity": 500, "unit": "g", "food": "all-purpose flour"},
    {"quantity": 7, "unit": "g", "food": "instant yeast"},
    {"quantity": 8, "unit": "g", "food": "kosher salt"},
    {"quantity": 50, "unit": "g", "food": "sugar"},
    {"quantity": 240, "unit": "ml", "food": "whole milk", "comment": "warmed to 100°F"},
    {"quantity": 60, "unit": "g", "food": "butter", "comment": "softened, not melted"},
    {"quantity": 1, "food": "egg", "comment": "room temperature"},
    {"section": "For Finishing"},
    {"quantity": 2, "unit": "tbsp", "food": "butter", "comment": "melted, for brushing"}
  ],
  "instructions": [
    {
      "title": "Activate the Yeast",
      "summary": "Confirm yeast viability before committing the full batch",
      "text": "Combine warm milk (100°F — hot bath temperature, not scalding) with a pinch of the sugar and the yeast. Whisk briefly and let stand 5–10 minutes. The mixture should become foamy and smell yeasty. If nothing happens, the yeast is dead — start over with fresh yeast. This step costs 10 minutes but saves a 3-hour failed batch."
    },
    {
      "title": "Mix and Knead",
      "summary": "Develop gluten structure for a tender, elastic crumb",
      "text": "Combine flour, remaining sugar, and salt in a stand mixer bowl. Add the yeast mixture, softened butter, and egg. Mix on low 2 minutes until combined, then increase to medium-high and knead 8–10 minutes until the dough is smooth, elastic, and slightly tacky (not sticky). The windowpane test: stretch a golf-ball-sized piece thin enough to see light through without tearing. If it tears, knead 2 more minutes."
    },
    {
      "title": "First Rise",
      "summary": "Bulk ferment until doubled — typically 60–90 minutes",
      "text": "Place dough in a lightly oiled bowl, cover with plastic wrap or a damp towel, and let rise in a warm (75–80°F) draft-free spot until doubled in size — typically 60 to 90 minutes depending on ambient temperature. Do not rush this with excessive heat; slow fermentation develops flavor. The dough is ready when it holds an indentation from a floured finger without springing back."
    },
    "Punch down the dough gently to release gas. Turn onto a lightly floured surface.",
    {
      "title": "Shape the Rolls",
      "summary": "Divide and shape uniformly for even baking",
      "text": "Divide dough into 12–15 equal pieces (a kitchen scale ensures uniformity — target 65g each). Shape each piece by cupping your hand over the dough and rolling in a tight circle on an unfloured surface. The friction of the bare surface helps build surface tension. Place shaped rolls touching in a buttered 9×13 pan — the contact keeps sides soft during baking."
    },
    {
      "title": "Second Rise",
      "summary": "Final proof until puffy and touching",
      "text": "Cover with plastic wrap and let rise 45–60 minutes until rolls are visibly puffed and just touching their neighbors. Preheat oven to 375°F during this time. Do not overbake — overproofed rolls collapse slightly and have a sour, yeasty taste."
    },
    "Bake 20–25 minutes until deep golden brown on top.",
    "Brush immediately with melted butter while hot. Serve warm."
  ],
  "notes": [
    {
      "title": "Make-Ahead",
      "text": "Rolls can be baked, cooled, and frozen in an airtight bag for up to 2 months. Reheat from frozen at 325°F for 12 minutes."
    },
    {
      "title": "Troubleshooting",
      "text": "ROLLS DIDN'T RISE: Check yeast freshness (bloom test) and dough temperature. Too cold = slow rise. Too hot (above 110°F) = dead yeast.\nROLLS TOO DENSE: Insufficient kneading — windowpane test wasn't achieved.\nROLLS TOO DRY: Overbaked. Pull at 375°F internal temperature."
    }
  ]
}
```

---

## Gotchas and Edge Cases

**`extras` values are strings**: Even boolean-like values must be strings. `{"isFoundation": "1"}` not `{"isFoundation": true}`.

**Category/tag resolution**: The server does a case-insensitive lookup. If the category exists, it passes the full `{id, name, slug}` object. If it doesn't exist, it passes `{name}` only and Mealie creates it.

**Recipe yield vs servings**: `recipe_yield` is a display string ("12–15 rolls"). `servings` is a number that enables Mealie's scaling feature. Use both.

**Food auto-creation**: If you pass a food name that doesn't exist, the server creates it. This is usually correct behavior, but spell food names carefully — "ButTer" would create a new "ButTer" food separate from "butter".
