"""Bright Data Walmart client, response cleanup, and cache orchestration."""

import asyncio
import math
import os
import re
from decimal import Decimal, InvalidOperation
from time import monotonic
from typing import Any, Mapping

import httpx
from fastapi import HTTPException

from config import Settings
from firestore_store import FirestoreStore


BRIGHT_DATA_URL = "https://api.brightdata.com/datasets/v3"


def _first(record: Mapping[str, Any], *names: str) -> Any:
    return next((record[name] for name in names if record.get(name) is not None), None)


def _number(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        number = float(
            Decimal(str(value).strip().replace("$", "").replace(",", ""))
        )
        return number if math.isfinite(number) else None
    except (InvalidOperation, TypeError, ValueError):
        return None


def _text(value: Any, default: str | None = None) -> str | None:
    return default if value is None else str(value)


def _review_count(value: Any) -> int | str | None:
    if value in (None, ""):
        return None
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return str(value)


def _json_value(value: Any) -> Any:
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    return str(value)


def _product_id(record: Mapping[str, Any]) -> str | None:
    value = _first(record, "us_item_id", "sku", "product_id")
    return str(value) if value is not None else None


class ProductService:
    def __init__(self, settings: Settings, store: FirestoreStore):
        self.settings = settings
        self.store = store

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        api_key = os.getenv("BRIGHTDATA_API_KEY", "").strip()
        if not api_key:
            raise HTTPException(503, "BRIGHTDATA_API_KEY is not configured")
        try:
            async with httpx.AsyncClient(timeout=self.settings.provider_timeout) as client:
                response = await client.request(
                    method,
                    f"{BRIGHT_DATA_URL}/{path}",
                    headers={"Authorization": f"Bearer {api_key}"},
                    **kwargs,
                )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException as exc:
            raise HTTPException(504, "Bright Data timed out") from exc
        except (httpx.HTTPError, ValueError) as exc:
            raise HTTPException(502, "Bright Data request failed") from exc

    async def provider_search(self, query: str) -> list[dict[str, Any]]:
        trigger = await self._request(
            "POST",
            "trigger",
            params={
                "dataset_id": self.settings.dataset_id,
                "include_errors": "true",
                "type": "discover_new",
                "discover_by": "keyword",
                "limit_per_input": "10",
            },
            json=[{"keyword": query, "domain": "https://www.walmart.com"}],
        )
        snapshot_id = trigger.get("snapshot_id") if isinstance(trigger, dict) else None
        if not snapshot_id:
            raise HTTPException(502, "Bright Data returned an invalid snapshot")

        deadline = monotonic() + self.settings.provider_timeout
        while monotonic() < deadline:
            progress = await self._request("GET", f"progress/{snapshot_id}")
            status = progress.get("status") if isinstance(progress, dict) else None
            if status == "ready":
                result = await self._request(
                    "GET", f"snapshot/{snapshot_id}", params={"format": "json"}
                )
                return result if isinstance(result, list) else []
            if status in {"failed", "error", "canceled", "cancelled"}:
                raise HTTPException(502, "Bright Data snapshot failed")
            await asyncio.sleep(1)
        raise HTTPException(504, "Bright Data timed out")

    async def provider_product(self, product_id: str) -> list[dict[str, Any]]:
        result = await self._request(
            "POST",
            "scrape",
            params={
                "dataset_id": self.settings.dataset_id,
                "format": "json",
                "include_errors": "true",
            },
            json=[{"url": f"https://www.walmart.com/ip/{product_id}"}],
        )
        return result if isinstance(result, list) else []

    @staticmethod
    def clean_search(records: list[dict[str, Any]], query: str) -> dict[str, Any]:
        products = []
        for item in records:
            product_id = _product_id(item)
            name = _first(item, "name", "product_name", "title")
            if not product_id or not name:
                continue
            products.append(
                {
                    "product_id": product_id,
                    "name": str(name),
                    "price": _number(_first(item, "price", "final_price")),
                    "currency": item.get("currency") or "USD",
                    "image_url": _first(item, "image_url", "main_image"),
                    "url": _first(item, "url", "product_url"),
                    "rating": _number(_first(item, "average_rating", "rating")),
                    "review_count": _first(item, "number_of_reviews", "review_count"),
                }
            )
            if len(products) == 10:
                break
        return {"query": query, "count": len(products), "cached": False, "products": products}

    @staticmethod
    def clean_product(records: list[dict[str, Any]], product_id: str) -> dict[str, Any]:
        item = next((row for row in records if _product_id(row) == product_id), None)
        if not item:
            raise HTTPException(404, "Product not found")
        images = item.get("images") or item.get("image_urls") or [item.get("main_image")]
        specs = item.get("specifications") or {}
        if isinstance(specs, list):
            specs = {str(x.get("name")): str(x.get("value")) for x in specs if x.get("name")}
        return {
            "product_id": product_id,
            "name": str(_first(item, "name", "product_name", "title") or "Unknown"),
            "url": _first(item, "url", "product_url"),
            "price": _number(_first(item, "price", "final_price")),
            "currency": item.get("currency") or "USD",
            "availability": _first(item, "availability", "availability_text"),
            "seller": _first(item, "seller", "seller_name"),
            "brand": item.get("brand"),
            "description": _first(item, "description", "short_description"),
            "images": [str(image) for image in images if image],
            "category_path": item.get("category_path") or item.get("breadcrumbs") or [],
            "rating": _number(_first(item, "average_rating", "rating")),
            "review_count": _first(item, "number_of_reviews", "review_count"),
            "specifications": specs,
            "cached": False,
        }

    @staticmethod
    def normalize_search(
        result: Mapping[str, Any], query: str, cached: bool
    ) -> dict[str, Any]:
        products = []
        raw_products = result.get("products")
        if isinstance(raw_products, list):
            for raw_product in raw_products:
                if not isinstance(raw_product, Mapping):
                    continue
                products.append(
                    {
                        "product_id": _text(raw_product.get("product_id"), ""),
                        "name": _text(raw_product.get("name"), "Unknown"),
                        "price": _number(raw_product.get("price")),
                        "currency": _text(raw_product.get("currency"), "USD"),
                        "image_url": _text(raw_product.get("image_url")),
                        "url": _text(raw_product.get("url")),
                        "rating": _number(raw_product.get("rating")),
                        "review_count": _review_count(raw_product.get("review_count")),
                    }
                )
        return {
            "query": query,
            "count": len(products),
            "cached": cached,
            "products": products,
        }

    @staticmethod
    def normalize_product(
        result: Mapping[str, Any], product_id: str, cached: bool
    ) -> dict[str, Any]:
        raw_images = result.get("images")
        images = (
            [str(image) for image in raw_images if image is not None]
            if isinstance(raw_images, list)
            else []
        )
        raw_category_path = result.get("category_path")
        category_path = []
        if isinstance(raw_category_path, list):
            for breadcrumb in raw_category_path:
                if isinstance(breadcrumb, Mapping):
                    category_path.append(_json_value(breadcrumb))
                elif breadcrumb is not None:
                    category_path.append(str(breadcrumb))
        raw_specifications = result.get("specifications")
        specifications = (
            _json_value(raw_specifications)
            if isinstance(raw_specifications, Mapping)
            else {}
        )
        return {
            "product_id": product_id,
            "name": _text(result.get("name"), "Unknown"),
            "url": _text(result.get("url")),
            "price": _number(result.get("price")),
            "currency": _text(result.get("currency"), "USD"),
            "availability": _text(result.get("availability")),
            "seller": _text(result.get("seller")),
            "brand": _text(result.get("brand")),
            "description": _text(result.get("description")),
            "images": images,
            "category_path": category_path,
            "rating": _number(result.get("rating")),
            "review_count": _review_count(result.get("review_count")),
            "specifications": specifications,
            "cached": cached,
        }

    async def search(self, query: str) -> dict[str, Any]:
        query = " ".join(query.casefold().split())
        key = f"walmart:search:{query}"
        if cached := await self.store.get(key):
            return self.normalize_search(cached, query, cached=True)
        await self.store.reserve()
        result = self.normalize_search(
            self.clean_search(await self.provider_search(query), query),
            query,
            cached=False,
        )
        await self.store.put(key, "search", result)
        return result

    async def get(self, product_id: str) -> dict[str, Any]:
        if not re.fullmatch(r"[0-9]{1,32}", product_id):
            raise HTTPException(400, "Invalid Walmart product ID")
        key = f"walmart:product:{product_id}"
        if cached := await self.store.get(key):
            return self.normalize_product(cached, product_id, cached=True)
        await self.store.reserve()
        result = self.normalize_product(
            self.clean_product(await self.provider_product(product_id), product_id),
            product_id,
            cached=False,
        )
        await self.store.put(key, "product", result)
        return result
