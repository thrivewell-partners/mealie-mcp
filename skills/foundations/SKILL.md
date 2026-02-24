---
name: foundations
description: This skill should be used when the user asks to "create a foundation recipe", "write a foundation for [dish]", "foundation recipe", "the why behind the how", "educational recipe", "teaching recipe", "mark as foundation", "isFoundation", "technique foundation", "document why this works", or wants to create a recipe that teaches the underlying science and technique rather than just listing steps. Foundation recipes are a special category that explain cooking principles alongside procedures.
version: 1.0.0
---

# Foundation Recipe Authoring

Foundation recipes are the intellectual core of this family's Mealie library — structured differently from ordinary recipes because they teach the **why behind the how**. A Foundation doesn't just say "sear the beef." It explains what the Maillard reaction is, why surface dryness matters, what fond is, and why skipping this step produces a fundamentally different dish.

## What Makes a Foundation Recipe

A Foundation recipe is distinguished by four characteristics:

1. **Explanatory instructions** — Each step explains the underlying principle, not just the action. The `text` field is where the science lives.
2. **Section-grouped ingredients** — Ingredients are organized into meaningful groups that illuminate the recipe's structure (e.g., "The Aromatics", "The Liquid Base", "The Protein").
3. **Three named note blocks** — Every Foundation ends with "Non-Negotiables", "Technique Notes", and "Scaling & Variations".
4. **The `isFoundation` flag** — `extras: {"isFoundation": "1"}` marks the recipe for filtering and reference.

Foundations are categorized under **"Foundations"** and referenced by variant recipes (e.g., "Texas-Style Chili" references "Chili — Foundation").

---

## Naming Convention

Always follow this pattern:

```
[Dish] — Foundation
```

Examples:
- `Beef Stew — Foundation`
- `Chili — Foundation`
- `Yeast Dinner Roll — Foundation`
- `Braised Short Ribs — Foundation`
- `Sourdough Bread — Foundation`

The em dash and "Foundation" suffix make foundations easy to identify in search results.

---

## Required Structure

### Metadata

```json
{
  "name": "Beef Stew — Foundation",
  "description": "The canonical braised beef stew — a study in fond development, collagen conversion, and the architecture of a braise",
  "categories": ["Foundations"],
  "tags": ["beef", "braised", "winter"],
  "extras": {"isFoundation": "1"},
  "servings": 6,
  "recipe_yield": "6 servings"
}
```

### Ingredients with Section Headers

Every Foundation ingredient list uses `{"section": "Name"}` headers to group ingredients by their role in the recipe. This grouping is pedagogical — it teaches the cook how the dish is architected.

```json
[
  {"section": "The Protein"},
  {"quantity": 2.5, "unit": "lb", "food": "beef chuck", "comment": "cut into 1½-inch cubes, cold from fridge"},

  {"section": "The Aromatics"},
  {"quantity": 1, "food": "yellow onion", "comment": "medium dice"},
  {"quantity": 3, "food": "garlic cloves", "comment": "minced"},
  {"quantity": 2, "food": "carrots", "comment": "½-inch rounds"},
  {"quantity": 2, "food": "celery stalks", "comment": "½-inch slices"},

  {"section": "The Liquid Base"},
  {"quantity": 2, "unit": "cup", "food": "beef stock", "comment": "homemade preferred"},
  {"quantity": 1, "unit": "cup", "food": "dry red wine", "comment": "something you'd drink"},
  {"quantity": 2, "unit": "tbsp", "food": "tomato paste"},

  {"section": "Fat & Seasoning"},
  {"quantity": 2, "unit": "tbsp", "food": "avocado oil"},
  {"quantity": 1, "unit": "tsp", "food": "kosher salt"},
  {"quantity": 0.5, "unit": "tsp", "food": "black pepper", "comment": "freshly ground"}
]
```

**Section naming guidelines:**
- Use "The ___" for main component groups (The Protein, The Aromatics, The Liquid Base)
- Use direct labels for supporting elements (Fat & Seasoning, Garnish, For the Dough, For the Filling)
- Name sections to teach structure, not just categorize

---

## Instructions: The Teaching Layer

Foundation instructions use the full enhanced dict format. The `text` field is where the teaching happens — it should be 2–5 sentences that explain the principle, not just the action.

### Format

```json
{
  "title": "Step Name",
  "summary": "One-sentence takeaway for Cook Mode navigation",
  "text": "The action instruction. Then the WHY — what is happening chemically or physically, why this matters, what goes wrong if you skip it, what to look for visually or by feel."
}
```

### Example: The Sear Step

```json
{
  "title": "Sear the Beef",
  "summary": "Build the flavor foundation via Maillard browning",
  "text": "Pat the beef cubes completely dry with paper towels — surface moisture turns to steam and prevents browning. Heat avocado oil in a Dutch oven over high heat until shimmering. Working in batches of 6–8 pieces (never crowd the pan), sear each cube undisturbed for 90 seconds per side until deeply browned on at least two faces. You are not cooking the beef here — you are building flavor. The mahogany crust develops through the Maillard reaction, a cascade of chemical changes above 280°F that creates hundreds of new flavor compounds. The brown residue left on the pan bottom (fond) is concentrated flavor that will dissolve into your liquid and define the stew's character. Do not rush this step and do not skip it."
}
```

### What to Explain in Each Step

For each significant step, answer at least one of:
- **What is happening?** (Maillard reaction, collagen converting to gelatin, gluten developing, yeast fermenting)
- **Why does this matter?** (skipping creates a different, lesser dish)
- **What to look for?** (visual, tactile, or aromatic cues that tell you it's working)
- **What goes wrong?** (what failure looks like and why it happens)

Not every step needs full explanation. Setup steps ("Preheat oven to 325°F") can be brief. Reserve depth for the technique-heavy steps.

---

## The Three Named Notes Blocks

Every Foundation recipe ends with exactly three named note sections:

### 1. Non-Negotiables

The things that cannot be compromised without fundamentally changing the dish. These are the load-bearing elements.

```json
{
  "title": "Non-Negotiables",
  "text": "1. DRY the beef before searing. Moisture is the enemy of browning.\n2. SEAR in batches. Crowding drops the pan temperature and steams instead of sears.\n3. DEGLAZE completely. Every bit of fond must dissolve into the liquid — this is your flavor base.\n4. LOW AND SLOW in the oven. Braising at 325°F for 2+ hours converts collagen to gelatin. High heat tightens the muscle fibers and makes the beef chewy."
}
```

### 2. Technique Notes

Deeper dives on technique — things that improve execution, explain the science further, or address common questions.

```json
{
  "title": "Technique Notes",
  "text": "WHY CAST IRON OR DUTCH OVEN: The mass of the vessel maintains temperature when cold meat hits hot metal. Thin pans cool instantly and you lose the sear.\n\nWHY COLD BEEF: Cold meat has less steam pressure. If you bring the beef to room temperature first, surface moisture increases. Keep it cold from the fridge and dry it right before searing.\n\nTHE GELATIN QUESTION: Chuck is ideal because it contains abundant collagen in the connective tissue. At braising temperatures (180–210°F), collagen hydrolyzes into gelatin over 2–3 hours. Gelatin gives the braising liquid its characteristic body and lip-coating richness. Lean cuts (like sirloin) lack this collagen and will be dry and tough when braised."
}
```

### 3. Scaling & Variations

How to scale the recipe up or down, and how it serves as a base for variants.

```json
{
  "title": "Scaling & Variations",
  "text": "SCALING: This recipe scales linearly up to 3x without adjustment. Beyond that, you may need two Dutch ovens or to work in batches for the sear. The braising time does not change with quantity.\n\nVARIANTS BUILT ON THIS FOUNDATION:\n- Add 1 tsp smoked paprika + 1 cup canned tomatoes → Texas-Style Stew\n- Swap red wine for stout beer + add 1 tsp caraway seeds → Irish-Style Stew\n- Add root vegetables in the last 45 minutes (parsnip, turnip, potato)\n\nMAKE-AHEAD: Stew improves overnight. The fat solidifies on top and is easy to remove cold. Reheat gently on the stovetop. Flavor deepens on day 2 and 3."
}
```

---

## Complete create_recipe Call for a Foundation

```json
{
  "name": "[Dish] — Foundation",
  "description": "Brief description that signals this is a technique study",
  "servings": 6,
  "recipe_yield": "6 servings",
  "total_time": "...",
  "prep_time": "...",
  "perform_time": "...",
  "categories": ["Foundations"],
  "tags": ["protein-type", "method", "season"],
  "extras": {"isFoundation": "1"},
  "ingredients": [
    {"section": "The Protein"},
    {"quantity": ..., "unit": "...", "food": "...", "comment": "..."},
    ...
  ],
  "instructions": [
    {
      "title": "Step Name",
      "summary": "One-line takeaway",
      "text": "Action + the WHY in 2–5 sentences"
    },
    ...
  ],
  "notes": [
    {"title": "Non-Negotiables", "text": "..."},
    {"title": "Technique Notes", "text": "..."},
    {"title": "Scaling & Variations", "text": "..."}
  ]
}
```

---

## Quality Checklist Before Saving

Before calling `create_recipe` on a Foundation, verify:

- [ ] Name follows `[Dish] — Foundation` pattern
- [ ] `extras: {"isFoundation": "1"}` is set (string "1", not boolean)
- [ ] `categories: ["Foundations"]` is included
- [ ] Ingredients use section headers with meaningful group names
- [ ] Instructions use dict format with title + summary + text
- [ ] Each significant step's `text` explains the WHY, not just the action
- [ ] Three named notes blocks: "Non-Negotiables", "Technique Notes", "Scaling & Variations"
- [ ] No pork, no seed oils in ingredient list

---

## Additional Resources

### Reference Files

- **`references/foundations-paradigm.md`** — Full philosophy, design rationale, complete worked example of an existing Foundation recipe, and guidance on which recipes are Foundation-worthy

### Related Skills

- **`recipe-creation`** skill — For non-Foundation recipe authoring
- **`dietary-management`** skill — For compliance checking and substitutions
