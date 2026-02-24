# Mealie Plugin for Claude Code

A Claude Code plugin that bundles a full-featured Mealie MCP server (27 tools) with skills, agents, and commands for family-centered recipe management, homesteading cooking guidance, and dietary compliance.

> Maintained by [Thrivewell Partners](https://github.com/thrivewell-partners)

---

## Features

- **27-tool MCP server** — Direct access to Mealie's recipes, shopping lists, meal plans, organizers, foods, and units
- **5 Claude Code skills** — Auto-activating knowledge libraries for recipe creation, Foundation recipes, dietary management, cooking tips, and meal planning
- **3 intelligent agents** — Recipe advisor, meal planner, and cooking teacher — auto-triggered on relevant conversations
- **3 slash commands** — `/mealie:quick-recipe`, `/mealie:weekly-menu`, `/mealie:find-recipe`
- **Dietary guardrail hook** — Scans ingredients for pork products and seed oils before any recipe is saved to Mealie
- **Family-aware defaults** — Serves 6, mild heat, no pork, no seed oils throughout all components

---

## Installation

### As a Claude Code Plugin (Recommended)

**1. Add the Marketplace**
```bash
/plugin marketplace add https://github.com/thrivewell-partners/mealie-mcp
```

**2. Install the Plugin**
```bash
/plugin install mealie@thrivewell-marketplace
```

**3. Set Environment Variables**
```bash
export MEALIE_URL="https://your-mealie-instance.com"
export MEALIE_API_KEY="your-api-token"
```

Get your API token: Mealie UI → User Profile → API Tokens → Generate

**4. Restart Claude Code** — MCP server and hooks load on startup.

---

### Standalone MCP Server (Advanced / Development)

**1. Install**
```bash
git clone https://github.com/thrivewell-partners/mealie-mcp
cd mealie-mcp
uv pip install -e .
```

**2. Configure**
```bash
# Create .env file with your Mealie credentials
echo "MEALIE_URL=https://your-mealie-instance.com" > .env
echo "MEALIE_API_KEY=your-api-token" >> .env
```

**3. Add to Claude Code MCP settings**

In `.claude/settings.json` or your project's MCP config:
```json
{
  "mcpServers": {
    "mealie": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mealie-mcp", "mealie-mcp"],
      "env": {
        "MEALIE_URL": "https://your-mealie-instance.com",
        "MEALIE_API_KEY": "your-api-token"
      }
    }
  }
}
```

---

## Plugin Components

### Skills (Auto-Activated)

Skills load automatically when you ask related questions — no command needed.

| Skill | Trigger Phrases | Description |
|-------|----------------|-------------|
| `recipe-creation` | "add a recipe", "create a recipe for [dish]", "save this recipe to Mealie" | Structured Mealie v3 recipe authoring with family defaults |
| `foundations` | "foundation recipe", "the why behind the how", "educational recipe" | Educational Foundation recipe paradigm with full technique documentation |
| `dietary-management` | "check for dietary issues", "substitute the oil", "is this family-friendly" | Compliance checking, pork/seed-oil detection, substitution guidance |
| `cooking-tips` | "how do I braise", "homesteading cooking", "what is fond", "how to render tallow" | Scratch cooking techniques with food science explanations |
| `meal-planning` | "plan meals for the week", "weekly menu", "what should we eat" | Weekly meal planning via Mealie API |

### Agents

| Agent | Color | Triggers | Role |
|-------|-------|---------|------|
| `recipe-advisor` | Green | Recipe modification discussions, dietary evaluation, substitution requests | Read-only recipe consultant — evaluates and advises |
| `meal-planner` | Blue | "Plan the week's meals", "fill in the meal plan", multi-day meal requests | Drafts weekly menus, gets approval, creates Mealie entries |
| `cooking-teacher` | Cyan | "Teach me how to", technique questions, troubleshooting cooking failures | Explains the science and technique behind cooking methods |

### Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `/mealie:quick-recipe` | `/mealie:quick-recipe [recipe name]` | Guided step-by-step recipe creation into Mealie |
| `/mealie:weekly-menu` | `/mealie:weekly-menu [YYYY-MM-DD]` | Plan a week of dinners, get approval, create Mealie entries |
| `/mealie:find-recipe` | `/mealie:find-recipe [query] [--tag name] [--category name]` | Search with dietary context and direct actions |

### Dietary Guardrail Hook

A `PreToolUse` hook fires before every `create_recipe` and `update_recipe` MCP call. It uses a Claude prompt to scan the ingredients list for:

- **Pork products**: bacon, ham, lard, prosciutto, pork sausage, chorizo, carnitas, and all variants
- **Seed oils**: canola, vegetable, sunflower, safflower, corn, soybean, cottonseed, grapeseed, rice bran oils

If violations are found, Claude receives a warning with the specific ingredient names and suggested compliant alternatives. The operation is not blocked — Claude decides whether to correct and retry or proceed.

---

## Family Dietary Guidelines

These rules are enforced by all plugin components:

### NO PORK
No pork or pork-derived products. This includes: pork chops, bacon, ham, lard, prosciutto, pancetta, guanciale, salami, pepperoni, pork sausage, carnitas, pork ribs, pork belly, pork rinds, fatback.

### NO SEED OILS
No industrially extracted seed or vegetable oils. Forbidden: vegetable oil, canola oil, sunflower oil, safflower oil, corn oil, soybean oil, cottonseed oil, grapeseed oil, rice bran oil, margarine.

**Compliant fats:** avocado oil · tallow · ghee · butter · olive oil · coconut oil · duck fat

### SCALE FOR 6
Default all recipes to serve 6 people. Numeric servings field enables Mealie's scaling feature.

### MILD TO MODERATE HEAT
Kid-friendly heat. Jalapeños seeded. No habaneros, scotch bonnets, or super-hot chilis.

---

## MCP Server Tools (27)

### Recipes

| Tool | Description |
|------|-------------|
| `search_recipes` | Search by keyword with category/tag filters |
| `get_recipe` | Full recipe detail including ingredients, instructions, nutrition, notes |
| `get_recipe_ingredients` | Ingredient list only |
| `create_recipe_from_url` | Import from URL (Mealie scrapes automatically) |
| `create_recipe` | Create manually with full structured content |
| `update_recipe` | Update any fields on an existing recipe |
| `delete_recipe` | Permanently delete a recipe |

### Shopping Lists

| Tool | Description |
|------|-------------|
| `get_shopping_lists` | List all shopping lists |
| `get_shopping_list` | View list with all items (checked/unchecked) |
| `create_shopping_list` | Create new empty list |
| `delete_shopping_list` | Delete a list |
| `add_shopping_list_item` | Add item to a list |
| `remove_shopping_list_item` | Remove item from a list |
| `check_shopping_list_item` | Check or uncheck an item |
| `add_recipe_to_shopping_list` | Add all recipe ingredients to a list |

### Meal Plans

| Tool | Description |
|------|-------------|
| `get_meal_plans` | View plans for a date range |
| `create_meal_plan_entry` | Add entry (recipe or freeform) for a date |
| `delete_meal_plan_entry` | Remove an entry |
| `generate_random_meal_plan` | Auto-fill date range with random recipes |

### Organizers

| Tool | Description |
|------|-------------|
| `get_categories` | List all recipe categories |
| `get_tags` | List all tags |
| `get_cookbooks` | List all cookbooks |
| `get_cookbook_recipes` | Recipes in a specific cookbook |
| `create_category` | Create a new category |
| `create_tag` | Create a new tag |

### Foods & Units

| Tool | Description |
|------|-------------|
| `search_foods` | Search Mealie's foods database |
| `get_units` | List all measurement units |

---

## Requirements

- **Python 3.11+**
- **[uv](https://docs.astral.sh/uv/)** package manager
- **[Mealie](https://mealie.io/) v3.0+** — self-hosted recipe manager
- **Claude Code** with plugin support

---

## Development

### Run Tests
```bash
uv run pytest
```

### Project Structure
```
mealie-mcp/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── marketplace.json             # GitHub Marketplace directory
├── src/mealie_mcp/              # MCP server source
│   ├── server.py                # FastMCP app and tool registration
│   ├── client.py                # Async Mealie API client (httpx)
│   ├── config.py                # Pydantic settings (MEALIE_URL, MEALIE_API_KEY)
│   ├── formatting.py            # Markdown output formatters
│   └── tools/                   # Tool modules
│       ├── recipes.py           # 7 recipe tools
│       ├── shopping.py          # 8 shopping list tools
│       ├── mealplan.py          # 4 meal plan tools
│       ├── organizers.py        # 6 organizer tools
│       └── foods.py             # 2 food/unit tools
├── skills/                      # Claude Code skills
│   ├── recipe-creation/         # Mealie v3 recipe authoring
│   ├── foundations/             # Foundation recipe paradigm
│   ├── dietary-management/      # Compliance and substitutions
│   ├── cooking-tips/            # Homesteading techniques
│   └── meal-planning/           # Weekly planning workflow
├── agents/                      # Claude Code agents
│   ├── recipe-advisor.md        # Recipe evaluation and adaptation
│   ├── meal-planner.md          # Weekly meal planning
│   └── cooking-teacher.md       # Technique education
├── commands/                    # Slash commands
│   ├── quick-recipe.md          # Guided recipe creation
│   ├── weekly-menu.md           # Weekly meal plan
│   └── find-recipe.md           # Recipe search
├── hooks/
│   └── hooks.json               # Dietary guardrail PreToolUse hook
├── tests/                       # Test suite (pytest + respx)
├── .mcp.json                    # MCP server config (env var references)
└── pyproject.toml               # Python project metadata
```

---

## License

MIT
