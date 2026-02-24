---
name: dietary-management
description: This skill should be used when the user asks to "check this recipe for dietary restrictions", "is this recipe family-friendly", "does this have pork", "find a substitute for canola oil", "what can replace vegetable oil", "make this recipe compliant", "our family dietary rules", "substitute the seed oil in this recipe", "no pork alternative", "scan recipe for violations", or when evaluating any recipe against the Johnson family's dietary guidelines. Covers NO PORK, NO SEED OILS, mild heat calibration, and scaling for 6.
version: 1.0.0
---

# Dietary Management

Evaluate recipes for compliance with the Johnson family's dietary guidelines and provide compliant substitutions when violations are found.

## The Two Hard Rules

### Rule 1: NO PORK

No pork or pork-derived products, period. This includes obvious pork and hidden pork-derived ingredients.

**Common violations to scan for:**
bacon · ham · lard · prosciutto · pancetta · guanciale · pork sausage · Italian sausage (unless beef/turkey) · salami · pepperoni · chorizo (unless beef/chicken-based) · pork shoulder · pork chops · pork loin · carnitas · pulled pork · pork ribs · pork belly · pork rinds · chicharrones · fatback

**Substitution principle:** Replace pork-based richness with beef-based richness.
- Bacon → beef bacon, or omit and add smoked paprika for color/depth
- Ham → turkey thigh, diced cooked chicken
- Pork sausage → ground beef with fennel seed + Italian seasoning, or turkey sausage
- Prosciutto/pancetta in pasta → skip or use thinly sliced beef bresaola
- Lard → tallow (equivalent fat, better flavor)
- Chorizo → beef chorizo (exists commercially), or ground beef with ancho + cumin

### Rule 2: NO SEED OILS

No industrially processed seed or vegetable oils.

**Common violations:**
vegetable oil · canola oil · sunflower oil · safflower oil · corn oil · soybean oil · cottonseed oil · grapeseed oil · rice bran oil · shortening (most commercial kinds) · margarine

**Hidden seed oil sources:** Many store-bought broths, sauces, dressings, and condiments contain canola or soybean oil. Note these when they appear in a recipe.

**Compliant substitutions by use case:**

| Use | Best Substitute | Why |
|-----|----------------|-----|
| High-heat searing (>400°F) | Avocado oil or tallow | High smoke points (~520°F and ~400°F) |
| Oven roasting | Avocado oil or tallow | Neutral or beefy flavor; handles heat |
| Sautéing aromatics | Butter or ghee | Adds flavor; handles moderate heat |
| Stir-fry | Avocado oil | Neutral, very high heat |
| Salad dressings | Olive oil or avocado oil | Excellent flavor profile |
| Baking (cakes, muffins) | Butter (melted) or coconut oil | Adds richness |
| Finishing / drizzle | Olive oil or butter | Flavor-forward |
| Deep frying | Tallow or avocado oil | Both handle high sustained heat |

---

## Evaluating a Recipe

### Step 1: Retrieve the Recipe

Use `mcp__plugin_mealie_mealie__get_recipe(slug)` to get the full recipe with ingredient list.

### Step 2: Scan Ingredients

Work through `recipeIngredient` and check:
- **Food field**: look for pork products and seed oils
- **Note/comment field**: look for preparation notes that imply a forbidden ingredient (e.g., "rendered lard" or "fry in vegetable oil")
- **Instructions**: sometimes oils or fats are mentioned in instruction text but not listed as ingredients

### Step 3: Check Heat Level

Scan instructions and ingredients for:
- Habanero, scotch bonnet, bird's eye chili → **flag** (too hot)
- Ghost pepper, Carolina Reaper → **flag** (absolutely not)
- Jalapeño with seeds → **note** (suggest seeding)
- Cayenne > 1/2 tsp for 6 servings → **note**
- Red pepper flakes > 1 tsp for 6 servings → **note**

### Step 4: Check Servings

Confirm the recipe is scaled for 6. If `recipeServings` is set to a different number, note what adjustments would bring it to 6.

### Step 5: Report

Summarize findings clearly:
- List each violation by ingredient name and location (ingredient list or instruction step)
- Provide a specific compliant substitution for each violation
- Confirm what IS compliant (positive reinforcement — show what the family CAN eat in this recipe)
- Offer to update the recipe in Mealie if violations need correcting

---

## Updating a Non-Compliant Recipe

If the user wants to make a fetched recipe compliant, use `mcp__plugin_mealie_mealie__update_recipe` with only the `ingredients` parameter updated — replacing violation items with compliant alternatives.

The dietary guardrail hook will re-scan on save and confirm compliance.

---

## Soft Defaults

Beyond the two hard rules, apply these when creating or evaluating recipes:

| Default | Behavior |
|---------|----------|
| Servings | Always 6 unless specified |
| Heat level | Mild to moderate; jalapeños seeded; no super-hot chilis |
| Fats | Default to avocado oil or butter; never suggest seed oils as backups |
| Stock | Homemade preferred but store-bought is fine to list |
| Grains | White flour is fine; whole grain where it makes sense |

---

## Quick Compliance Checklist

Before saving any recipe to Mealie, verify:

- [ ] No pork or pork-derived ingredients
- [ ] No seed oils (check both ingredient list and instruction text)
- [ ] Heat level is mild to moderate
- [ ] Servings scaled to 6
- [ ] Fats are compliant (avocado oil, tallow, ghee, butter, olive oil, coconut oil)

---

## Additional Resources

### Reference Files

- **`references/dietary-rules.md`** — Complete forbidden/allowed ingredient lists with edge cases and notes
- **`references/substitutions.md`** — Comprehensive substitution tables for oils, pork products, and heat adjustment

### Related Skills

- **`recipe-creation`** skill — For building compliant recipes from scratch
- **`cooking-tips`** skill — For understanding why certain fats are used in specific techniques
