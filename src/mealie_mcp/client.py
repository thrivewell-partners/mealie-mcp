from __future__ import annotations

from typing import Any

import httpx

from .config import settings


class MealieClient:
    """Async HTTP client for the Mealie REST API."""

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=settings.mealie_url.rstrip("/"),
            headers={
                "Authorization": f"Bearer {settings.mealie_api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            timeout=settings.mealie_request_timeout,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
    ) -> Any:
        resp = await self._client.request(method, path, params=params, json=json)
        resp.raise_for_status()
        if resp.status_code == 204:
            return None
        return resp.json()

    # ── Recipes ──────────────────────────────────────────────

    async def search_recipes(
        self,
        query: str = "",
        page: int = 1,
        per_page: int = 10,
        categories: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> dict:
        params: dict[str, Any] = {
            "search": query,
            "page": page,
            "perPage": per_page,
            "orderBy": "created_at",
            "orderDirection": "desc",
        }
        if categories:
            params["categories"] = categories
        if tags:
            params["tags"] = tags
        return await self._request("GET", "/api/recipes", params=params)

    async def get_recipe(self, slug: str) -> dict:
        return await self._request("GET", f"/api/recipes/{slug}")

    async def create_recipe_from_url(self, url: str) -> str:
        result = await self._request(
            "POST", "/api/recipes/create-url", json={"url": url, "includeTags": True}
        )
        return result

    async def create_recipe(self, name: str) -> str:
        return await self._request("POST", "/api/recipes", json={"name": name})

    async def update_recipe(self, slug: str, data: dict) -> dict:
        existing = await self.get_recipe(slug)
        existing.update(data)
        return await self._request("PUT", f"/api/recipes/{slug}", json=existing)

    async def delete_recipe(self, slug: str) -> None:
        await self._request("DELETE", f"/api/recipes/{slug}")

    # ── Shopping Lists ───────────────────────────────────────

    async def get_shopping_lists(self) -> dict:
        return await self._request(
            "GET", "/api/groups/shopping/lists", params={"page": 1, "perPage": -1}
        )

    async def get_shopping_list(self, list_id: str) -> dict:
        return await self._request("GET", f"/api/groups/shopping/lists/{list_id}")

    async def create_shopping_list(self, name: str) -> dict:
        return await self._request(
            "POST", "/api/groups/shopping/lists", json={"name": name}
        )

    async def delete_shopping_list(self, list_id: str) -> None:
        await self._request("DELETE", f"/api/groups/shopping/lists/{list_id}")

    async def add_shopping_list_item(
        self,
        list_id: str,
        *,
        note: str = "",
        quantity: float | None = None,
        unit_id: str | None = None,
        food_id: str | None = None,
    ) -> dict:
        body: dict[str, Any] = {
            "shoppingListId": list_id,
            "note": note,
            "checked": False,
        }
        if quantity is not None:
            body["quantity"] = quantity
        if unit_id:
            body["unitId"] = unit_id
        if food_id:
            body["foodId"] = food_id
        return await self._request(
            "POST", "/api/groups/shopping/items", json=body
        )

    async def update_shopping_list_item(
        self, item_id: str, data: dict
    ) -> dict:
        return await self._request(
            "PUT", f"/api/groups/shopping/items/{item_id}", json=data
        )

    async def delete_shopping_list_item(self, item_id: str) -> None:
        await self._request("DELETE", f"/api/groups/shopping/items/{item_id}")

    async def add_recipe_ingredients_to_list(
        self, list_id: str, recipe_id: str
    ) -> dict:
        return await self._request(
            "POST",
            f"/api/groups/shopping/lists/{list_id}/recipe/{recipe_id}",
        )

    # ── Meal Plans ───────────────────────────────────────────

    async def get_meal_plans(self, start_date: str, end_date: str) -> dict:
        return await self._request(
            "GET",
            "/api/groups/mealplans",
            params={"start_date": start_date, "end_date": end_date, "perPage": -1},
        )

    async def create_meal_plan_entry(self, data: dict) -> dict:
        return await self._request("POST", "/api/groups/mealplans", json=data)

    async def delete_meal_plan_entry(self, entry_id: str) -> None:
        await self._request("DELETE", f"/api/groups/mealplans/{entry_id}")

    async def get_random_recipes(self, count: int = 7) -> list[dict]:
        resp = await self._request(
            "GET", "/api/recipes", params={"perPage": count, "orderBy": "random"}
        )
        return resp.get("items", [])

    # ── Organizers ───────────────────────────────────────────

    async def get_categories(self) -> dict:
        return await self._request(
            "GET", "/api/organizers/categories", params={"perPage": -1}
        )

    async def create_category(self, name: str) -> dict:
        return await self._request(
            "POST", "/api/organizers/categories", json={"name": name}
        )

    async def get_tags(self) -> dict:
        return await self._request(
            "GET", "/api/organizers/tags", params={"perPage": -1}
        )

    async def create_tag(self, name: str) -> dict:
        return await self._request(
            "POST", "/api/organizers/tags", json={"name": name}
        )

    async def get_cookbooks(self) -> dict:
        return await self._request(
            "GET", "/api/groups/cookbooks", params={"perPage": -1}
        )

    async def get_cookbook_recipes(
        self, cookbook_slug: str, page: int = 1, per_page: int = 10
    ) -> dict:
        cookbook = await self._request(
            "GET", f"/api/groups/cookbooks/{cookbook_slug}"
        )
        # Cookbooks filter by categories/tags; use those to query recipes
        params: dict[str, Any] = {"page": page, "perPage": per_page}
        if cookbook.get("categories"):
            params["categories"] = [c["id"] for c in cookbook["categories"]]
        if cookbook.get("tags"):
            params["tags"] = [t["id"] for t in cookbook["tags"]]
        return await self._request("GET", "/api/recipes", params=params)

    # ── Foods & Units ────────────────────────────────────────

    async def search_foods(
        self, query: str = "", page: int = 1, per_page: int = 10
    ) -> dict:
        return await self._request(
            "GET",
            "/api/foods",
            params={"search": query, "page": page, "perPage": per_page},
        )

    async def get_units(self) -> dict:
        return await self._request(
            "GET", "/api/units", params={"perPage": -1}
        )
