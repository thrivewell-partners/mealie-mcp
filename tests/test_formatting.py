from mealie_mcp.formatting import (
    format_recipe_summary,
    format_recipe_detail,
    format_ingredient_list,
    format_shopping_list_detail,
    format_meal_plans,
    format_categories,
    format_tags,
    format_foods,
    format_units,
)


def test_format_recipe_summary(sample_recipe):
    result = format_recipe_summary(sample_recipe)
    assert "Chicken Tikka Masala" in result
    assert "chicken-tikka-masala" in result
    assert "Indian" in result
    assert "Dinner" in result


def test_format_recipe_detail(sample_recipe):
    result = format_recipe_detail(sample_recipe)
    assert "# Chicken Tikka Masala" in result
    assert "## Ingredients" in result
    assert "## Instructions" in result
    assert "chicken breast" in result
    assert "Marinate" in result
    assert "## Nutrition" in result
    assert "calories" in result


def test_format_ingredient_list(sample_recipe):
    result = format_ingredient_list(sample_recipe)
    assert "Ingredients for" in result
    assert "chicken breast" in result
    assert "yogurt" in result


def test_format_shopping_list_detail(sample_shopping_list):
    result = format_shopping_list_detail(sample_shopping_list)
    assert "Weekly Groceries" in result
    assert "To Get" in result
    assert "Done" in result
    assert "item-1" in result
    assert "item-2" in result


def test_format_shopping_list_empty():
    result = format_shopping_list_detail({"name": "Empty", "id": "x", "listItems": []})
    assert "empty list" in result


def test_format_meal_plans_empty():
    result = format_meal_plans([])
    assert "No meal plan" in result


def test_format_meal_plans():
    entries = [
        {"date": "2025-01-01", "entryType": "dinner", "id": "e1",
         "recipe": {"name": "Pasta", "slug": "pasta"}},
        {"date": "2025-01-02", "entryType": "lunch", "id": "e2",
         "title": "Leftovers", "text": ""},
    ]
    result = format_meal_plans(entries)
    assert "Pasta" in result
    assert "Leftovers" in result


def test_format_categories():
    result = format_categories([{"name": "Italian", "slug": "italian", "recipes": []}])
    assert "Italian" in result


def test_format_tags():
    result = format_tags([{"name": "Quick", "slug": "quick"}])
    assert "Quick" in result


def test_format_foods():
    result = format_foods([{"name": "Chicken", "id": "f1"}])
    assert "Chicken" in result


def test_format_units():
    result = format_units([{"name": "Cup", "id": "u1", "abbreviation": "c"}])
    assert "Cup" in result
    assert "(c)" in result
