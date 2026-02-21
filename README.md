# Mealie MCP Server

An MCP (Model Context Protocol) server that wraps the [Mealie](https://mealie.io/) self-hosted recipe manager API, enabling AI assistants to interact with your Mealie instance.

## Features

- **Recipes** — Search, view, create, import from URL, update, delete
- **Shopping Lists** — Create lists, add/remove/check items, add recipe ingredients
- **Meal Plans** — View, create, delete entries, auto-generate random plans
- **Organizers** — Browse categories, tags, and cookbooks
- **Foods & Units** — Search foods database and measurement units

## Setup

### 1. Install

```bash
uv pip install -e .
```

### 2. Configure

Copy `.env.example` to `.env` and fill in your Mealie details:

```bash
cp .env.example .env
```

- `MEALIE_URL` — Your Mealie instance URL (e.g. `http://localhost:9925`)
- `MEALIE_API_KEY` — API token from Mealie UI → User Profile → API Tokens

### 3. Run

```bash
uv run mealie-mcp
```

### 4. Connect to Claude Code

Add to your Claude Code MCP config (`.claude/settings.json` or project settings):

```json
{
  "mcpServers": {
    "mealie": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mealie", "mealie-mcp"],
      "env": {
        "MEALIE_URL": "http://localhost:9925",
        "MEALIE_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Tools (27)

### Recipes
| Tool | Description |
|------|-------------|
| `search_recipes` | Search by keyword with category/tag filters |
| `get_recipe` | Full recipe detail |
| `get_recipe_ingredients` | Ingredient list only |
| `create_recipe_from_url` | Import from URL |
| `create_recipe` | Create manually |
| `update_recipe` | Update existing recipe |
| `delete_recipe` | Delete a recipe |

### Shopping Lists
| Tool | Description |
|------|-------------|
| `get_shopping_lists` | List all shopping lists |
| `get_shopping_list` | View list with items |
| `create_shopping_list` | Create new list |
| `delete_shopping_list` | Delete a list |
| `add_shopping_list_item` | Add item to list |
| `remove_shopping_list_item` | Remove item |
| `check_shopping_list_item` | Check/uncheck item |
| `add_recipe_to_shopping_list` | Add recipe ingredients to list |

### Meal Plans
| Tool | Description |
|------|-------------|
| `get_meal_plans` | View plans for date range |
| `create_meal_plan_entry` | Add meal plan entry |
| `delete_meal_plan_entry` | Remove entry |
| `generate_random_meal_plan` | Auto-fill with random recipes |

### Organizers
| Tool | Description |
|------|-------------|
| `get_categories` | List categories |
| `get_tags` | List tags |
| `get_cookbooks` | List cookbooks |
| `get_cookbook_recipes` | Recipes in a cookbook |
| `create_category` | Create category |
| `create_tag` | Create tag |

### Foods & Units
| Tool | Description |
|------|-------------|
| `search_foods` | Search foods database |
| `get_units` | List measurement units |
