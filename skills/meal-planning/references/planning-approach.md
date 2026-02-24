# Meal Planning Approach — Reference

Weekly planning templates, protein rotation strategies, and batch cooking guidelines.

---

## Weekly Planning Templates

### Standard Week (Dinners Only)

| Day | Protein Anchor | Dish Character | Source |
|-----|---------------|---------------|--------|
| Monday | Chicken | Lighter, weeknight accessible | New cook or quick reheat |
| Tuesday | Beef | Hearty midweek | New cook or leftover from Sunday |
| Wednesday | Leftover | Reheat + fresh side | Sunday batch cook |
| Thursday | Variable (lamb/turkey/duck) | Variety break | New cook |
| Friday | Fish or eggs as main | End-of-week lighter | Quick cook (20–30 min) |
| Saturday | Beef or chicken, elevated | Family dinner | More time, more elaborate |
| Sunday | Batch anchor | Stew, chili, or braised dish | Sets up the week |

### Compressed Week (4 Cooking Nights)

| Day | Plan |
|-----|------|
| Monday | Batch cook: large braise (beef stew, chili) |
| Tuesday | Batch leftover |
| Wednesday | Quick protein + vegetables (chicken thighs, 30 min) |
| Thursday | Quick protein + side |
| Friday | Fish or egg dish |
| Saturday | Celebratory or guest meal |
| Sunday | Prep: bread dough, stock, refrigerator reset |

---

## Protein Rotation Guide

### Why Rotate Proteins

Rotating proteins ensures:
- Nutritional variety (different fatty acid profiles, minerals, vitamins)
- Flavor variety (avoids palate fatigue)
- Budget balance (beef and lamb tend to cost more; chicken and turkey are economical)
- Skill building (different techniques for different proteins)

### Suggested Rotation

**Week A**: Beef heavy (2 beef, 2 chicken, 1 turkey, 1 fish)
**Week B**: Chicken heavy (2 chicken, 1 beef, 1 lamb, 1 turkey, 1 fish)
**Week C**: Variable heavy (2 chicken, 1 beef, 1 lamb, 1 duck, 1 fish)

Rotate through A → B → C → A.

### Protein Cooking Time Reference

| Protein | Cut | Technique | Active Time | Total Time |
|---------|-----|-----------|-------------|------------|
| Beef chuck | Braised stew | Dutch oven braise | 30 min | 3–4 hrs |
| Beef ground | Chili or tacos | Stovetop | 30 min | 45 min |
| Beef short ribs | Braised | Dutch oven | 30 min | 3.5 hrs |
| Chicken thighs | Roasted | Sheet pan | 10 min | 45 min |
| Chicken thighs | Braised | Stovetop/oven | 20 min | 1 hr |
| Whole chicken | Roasted | Oven | 15 min | 1.5 hrs |
| Ground turkey | Chili, meatballs | Stovetop | 20 min | 45 min |
| Lamb shoulder chops | Pan-seared | Stovetop | 15 min | 30 min |
| Lamb shoulder | Braised | Dutch oven | 20 min | 3 hrs |
| Salmon fillet | Baked/pan-seared | Stovetop/oven | 5 min | 20 min |
| Cod fillet | Baked | Oven | 5 min | 15 min |

---

## Batch Cooking Strategy

### What to Batch Cook

**The Anchor Dish** (makes 2+ dinners):
- Beef stew or chili (6-serving batch → dinner + leftovers for 2)
- Braised chicken thighs (large batch → dinner + chicken in salads/tacos)
- Bone broth (large pot → stock for the week)

**Supporting Prep** (saves time on weeknights):
- Bread dough (cold-ferment in fridge; bake fresh rolls mid-week in 25 minutes)
- Cooked beans (dried beans soaked and cooked → 3–4 cups for multiple uses)
- Roasted vegetables (sheet pan of root vegetables → sides for 2–3 days)
- Hard-cooked eggs (quick protein for lunches)
- Rendered stock (simmer from bones; use all week)

### Batch Day Planning (Sunday)

Suggested Sunday batch cook order:

**Morning:**
1. Start beef or chicken stock (set it and let it simmer)
2. Mix bread dough → refrigerator for slow fermentation
3. Soak dried beans if making beans

**Afternoon:**
4. While stock simmers, prepare the week's anchor dish (stew, chili)
5. Roast a sheet pan of root vegetables for the week
6. Hard-cook eggs if needed for lunches

**Evening:**
7. Strain and cool stock
8. Portion and label anchor dish (serving sizes clearly marked)
9. Refrigerator reset: organized, labeled, ready for the week

Total active time: 2–3 hours. Passive simmering time: 4–6 hours.

---

## Shopping List Integration

### Workflow After Planning

1. Finalize the week's meal plan in Mealie
2. For each recipe-based dinner, call `add_recipe_to_shopping_list`
3. Add additional pantry restocks manually (staples that run low)
4. Review the list and deduplicate (e.g., "onion" may appear from multiple recipes — combine quantities)
5. Organize the list by store section before shopping

### Creating a Weekly Shopping List

When starting a new week, create or use a dedicated weekly list:
- Name: "Week of [start date]"
- Use `create_shopping_list` if creating fresh
- Or use an existing list and clear checked items first

### Pantry Staples to Always Keep Stocked

The family can improvise more dinners from a well-stocked pantry:

**Proteins (freezer)**:
- Ground beef (2 lbs), beef chuck (2–3 lb roast), chicken thighs (6–8 pieces)

**Dry goods**:
- All-purpose and bread flour (5 lbs each), rolled oats, white rice, dried lentils, canned beans
- Pasta (for quick nights)

**Canned and jarred**:
- Canned whole tomatoes (4 cans), tomato paste, coconut milk, beef and chicken stock (backup for when homemade runs out)

**Aromatics**:
- Yellow onions, garlic bulbs, carrots, celery

**Fats**:
- Avocado oil (1 large bottle), butter (2 lbs), ghee (1 jar), tallow (jar)

**Spices**:
- Kosher salt, black pepper, cumin, coriander, smoked paprika, chili powder, oregano, thyme, bay leaves, cinnamon, turmeric

---

## Mealie API Quick Reference for Meal Planning

```python
# Read what's already planned
get_meal_plans(start_date="2026-02-24", end_date="2026-03-02")

# Create a dinner entry with a recipe
create_meal_plan_entry(
  date="2026-02-24",
  entry_type="dinner",
  recipe_slug="beef-stew-foundation"
)

# Create a non-recipe entry (leftovers, etc.)
create_meal_plan_entry(
  date="2026-02-26",
  entry_type="dinner",
  title="Leftover Beef Stew"
)

# Delete an entry
delete_meal_plan_entry(entry_id="...")

# Add recipe ingredients to shopping list
add_recipe_to_shopping_list(
  list_id="...",
  recipe_slug="beef-stew-foundation"
)

# View shopping lists to find the ID
get_shopping_lists()
```

**Date format**: Always `YYYY-MM-DD`. Never use `MM/DD/YYYY` or other formats.

**Entry types**: `"breakfast"`, `"lunch"`, `"dinner"`, `"side"` — default to `"dinner"` for weekly planning.
