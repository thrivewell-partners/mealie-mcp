# The Foundations Paradigm

Complete philosophy, design rationale, and specification for Foundation recipes in the Johnson family Mealie library.

---

## The Problem Foundations Solve

A standard recipe says: "Sear the beef over high heat until browned."

A cook who understands the Maillard reaction, fond development, and why surface moisture destroys browning will execute this correctly every time. A cook who doesn't will crowd the pan, use medium heat, and wonder why the stew lacks depth.

**Foundations are structured to transfer the understanding, not just the steps.**

The goal is a family library where the recipes make the family better cooks — not just a list of procedures to follow.

---

## Philosophy: "The Why Behind the How"

Foundation recipes document techniques at the level that allows mastery, not just replication. Each Foundation recipe answers:

1. **What is happening?** — Name the process (Maillard reaction, collagen conversion, gluten development, yeast fermentation)
2. **Why does it matter?** — What is the outcome of doing this correctly vs. skipping it?
3. **How do I know it's working?** — Visual, tactile, and aromatic cues
4. **What goes wrong?** — Common failure modes and why they happen

Foundations are not exhaustive science textbooks. They are focused on the moments in a recipe where technique separates a great result from a mediocre one.

---

## What Earns "Foundation" Status

Not every recipe should be a Foundation. The designation is reserved for:

1. **Technique anchors** — Recipes that teach a transferable method (braising, bread making, emulsification, fermentation, stock making)
2. **Canonical versions** — The definitive family version of a dish that variants will reference
3. **Science-dense recipes** — Dishes where understanding the process meaningfully improves results (bread, custard, caramel, hollandaise)

**Examples of Foundation-worthy dishes:**
- Beef Stew (braising fundamentals)
- Chili (built sauce development, bloom technique)
- Dinner Rolls (yeast bread: fermentation, gluten, shaping)
- Chicken Stock (extraction, clarification)
- Sourdough Bread (long fermentation, wild yeast, scoring)
- Roast Chicken (dry brining, carryover cooking, resting)
- Hollandaise / Béarnaise (emulsification)
- Caramel (sugar work, Maillard vs caramelization)

**Examples that do NOT need Foundation status:**
- A quick weeknight pasta dish
- Simple salads and dressings
- Most side dishes
- Imported recipes from URLs

---

## The Four Structural Requirements

### 1. The `isFoundation` Flag

```json
"extras": {"isFoundation": "1"}
```

This enables filtering in Mealie. The value is the string `"1"` — not boolean `true`. Mealie stores extra fields as strings internally.

Combined with the "Foundations" category, this allows:
- Browsing all Foundation recipes: `search_recipes(categories=["Foundations"])`
- Checking if a recipe is a Foundation: look for `extras.isFoundation == "1"`

### 2. Ingredient Section Headers

Foundation ingredients are grouped by their **role in the recipe**, not just by type. The groupings teach the cook how the dish is structured.

**Standard section naming patterns:**

| Group | Example Names |
|-------|---------------|
| Main protein | "The Protein", "The Meat" |
| Aromatics | "The Aromatics", "The Flavor Base" |
| Liquid components | "The Liquid Base", "The Braising Liquid" |
| Fat and seasoning | "Fat & Seasoning", "For Searing" |
| Finishing elements | "For Finishing", "The Garnish" |
| Dough components | "For the Dough", "The Dry Ingredients", "The Wet Ingredients" |
| Filling or topping | "For the Filling", "For the Topping" |

The section names should answer the question: "What is the job of these ingredients in this dish?"

### 3. Enhanced Instruction Dicts

Every instruction in a Foundation uses the full dict format:

```json
{
  "title": "Verb Phrase Describing the Action",
  "summary": "One-sentence outcome statement",
  "text": "Action instruction. Then: why this matters, what is happening, what to look for, what goes wrong."
}
```

**Writing the `text` field:**
- Lead with the action instruction: what to do, how to do it, specific parameters (temperature, time, quantity)
- Follow with the science/technique: what is happening physically or chemically
- Add the failure mode: what happens if this step is skipped or done wrong
- Use specific sensory cues: "smoke means your pan is too hot", "the dough should be tacky but not stick to a clean hand"

Target 3–6 sentences per step text for technique-heavy steps. Simple steps ("Preheat the oven to 325°F") can be brief.

### 4. Three Named Note Blocks

Every Foundation ends with exactly these three note sections:

**Non-Negotiables**
The critical technique points that define the dish. Numbered list. These are the things that if you don't do them, you don't have the dish.

**Technique Notes**
Deeper dives — the science, the equipment rationale, the "why" that didn't fit into individual steps. Can include comparisons (why cast iron vs. nonstick), explanations of chemical processes, or detailed equipment guidance.

**Scaling & Variations**
How to scale the recipe, plus 3–5 variant ideas that build on the Foundation. This is where the Foundation→Variant relationship is documented — "See Texas-Style Chili for a regional variation built on this base."

---

## Variant Recipes and the Foundation Reference

Foundation recipes spawn variant recipes. A variant is a recipe that builds on the Foundation's techniques but customizes for a specific occasion, cuisine, or preference.

### How to Reference a Foundation

In the variant recipe's description:
```
"A Texas-style variation of the Chili Foundation — dried chili paste instead of chili powder, beef chuck in larger chunks, no beans. See chili-foundation for the underlying techniques."
```

In the variant's notes:
```json
{
  "title": "Foundation Reference",
  "text": "This recipe assumes familiarity with the Chili Foundation (slug: chili-foundation). Review that recipe for the 'why' behind the bloom technique, the layering of aromatics, and the meat preparation."
}
```

### Existing Foundation → Variant Relationships

| Foundation | Variant(s) |
|------------|-----------|
| Chili — Foundation | Texas-Style Chili |
| Yeast Dinner Roll — Foundation | Yeast Dinner Rolls — 65% Hydration |

---

## Complete Foundation Example: Structural Breakdown

Below is the structure of "Beef Stew — Foundation" as a reference implementation.

### Metadata
```json
{
  "name": "Beef Stew — Foundation",
  "description": "The canonical family braised beef stew — a study in fond development, collagen conversion, and the architecture of a long braise",
  "categories": ["Foundations"],
  "tags": ["beef", "braised", "winter"],
  "extras": {"isFoundation": "1"},
  "servings": 6,
  "total_time": "3 hours 30 minutes",
  "prep_time": "30 minutes",
  "perform_time": "3 hours"
}
```

### Ingredient Sections
```
The Protein
  → beef chuck (2.5 lb, cut to 1.5-inch cubes)
  → kosher salt, black pepper

Fat & Seasoning
  → avocado oil (2 tbsp, for searing)

The Aromatics
  → yellow onion, garlic, carrots, celery

The Liquid Base
  → beef stock (2 cups, homemade preferred)
  → dry red wine (1 cup)
  → tomato paste (2 tbsp)
  → fresh thyme, bay leaves

Late Additions
  → potatoes (Yukon Gold, cut to 1-inch cubes)
  → frozen peas (optional, added at the end)
```

### Instruction Flow
1. **Prep the Beef** — dry thoroughly; explain why surface moisture prevents browning
2. **Sear the Beef** — high heat, in batches; explain Maillard reaction and fond
3. **Build the Aromatics** — sweat onions, then carrots/celery; explain aromatics releasing water
4. **Bloom the Tomato Paste** — cook paste in the fat; explain caramelization
5. **Deglaze** — wine into fond; explain dissolving and concentrating flavor
6. **Braise** — combine, oven 325°F, 2+ hours; explain collagen → gelatin conversion
7. **Add Late Vegetables** — potatoes in last 45 min; explain why timing matters
8. **Finish and Adjust** — skim fat, taste, season; explain salt as flavor amplifier

### Notes Blocks
- **Non-Negotiables**: 4 items — dry the beef, sear in batches, deglaze completely, low and slow
- **Technique Notes**: Why cast iron/Dutch oven, why cold beef, the gelatin explanation, the deglaze science
- **Scaling & Variations**: Scales linearly to 3x; variant ideas (Irish stew, Texas-style, harvest root vegetable); make-ahead notes

---

## Quick Assessment: Is This a Foundation?

Ask these three questions:
1. Does executing this recipe well require understanding a technique (not just following steps)?
2. Will this recipe be referenced or adapted by other recipes in the library?
3. Does the dish reward the cook for understanding what's happening during cooking?

If yes to 2 of 3: it's Foundation-worthy.
