"""Small local ecommerce tools used in the teaching notebooks."""

from __future__ import annotations

import re
from datetime import date
from typing import Any

import httpx


ORDER_API_BASE_URL = "https://walmart-demo-api-k2yx3oubha-ue.a.run.app"
ORDER_ID_PATTERN = re.compile(r"WM-DEMO-[0-9]{4}")
REQUEST_TIMEOUT_SECONDS = 30.0


class OrderAPIError(RuntimeError):
    """A concise, learner-safe failure from the teaching Orders API."""


def _get_json(path: str, *, params: dict[str, str] | None = None) -> Any:
    try:
        with httpx.Client(
            base_url=ORDER_API_BASE_URL,
            timeout=REQUEST_TIMEOUT_SECONDS,
        ) as client:
            response = client.get(path, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException as error:
        raise OrderAPIError(
            "The teaching Orders service timed out. Please run the cell once more."
        ) from error
    except httpx.HTTPStatusError as error:
        raise OrderAPIError(
            f"The teaching Orders service returned HTTP {error.response.status_code}."
        ) from error
    except (httpx.HTTPError, ValueError) as error:
        raise OrderAPIError(
            "The teaching Orders service returned an invalid response."
        ) from error


def list_orders(start_date: str, end_date: str) -> list[dict[str, Any]]:
    """List order summaries for an inclusive YYYY-MM-DD date range."""

    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
    except ValueError as error:
        raise ValueError("dates must use YYYY-MM-DD format") from error
    if start > end:
        raise ValueError("start_date must not be after end_date")
    payload = _get_json(
        "/v1/orders",
        params={"start_date": start.isoformat(), "end_date": end.isoformat()},
    )
    if not isinstance(payload, list) or not all(
        isinstance(row, dict) for row in payload
    ):
        raise OrderAPIError("The teaching Orders service returned invalid summaries.")
    return payload


def get_order(order_id: str) -> dict[str, Any]:
    """Retrieve full details for one synthetic order ID."""

    if ORDER_ID_PATTERN.fullmatch(order_id) is None:
        raise ValueError("order_id must match WM-DEMO-####")
    payload = _get_json(f"/v1/orders/{order_id}")
    if not isinstance(payload, dict):
        raise OrderAPIError("The teaching Orders service returned invalid details.")
    return payload


_STORE_HOURS = {
    "seattle downtown": {
        "store_name": "Seattle Downtown",
        "timezone": "America/Los_Angeles",
        "hours": {
            "Monday": ("9:00 AM", "9:00 PM"),
            "Tuesday": ("9:00 AM", "9:00 PM"),
            "Wednesday": ("9:00 AM", "9:00 PM"),
            "Thursday": ("9:00 AM", "9:00 PM"),
            "Friday": ("9:00 AM", "9:00 PM"),
            "Saturday": ("9:00 AM", "8:00 PM"),
            "Sunday": ("10:00 AM", "7:00 PM"),
        },
    },
    "bellevue marketplace": {
        "store_name": "Bellevue Marketplace",
        "timezone": "America/Los_Angeles",
        "hours": {
            "Monday": ("8:00 AM", "10:00 PM"),
            "Tuesday": ("8:00 AM", "10:00 PM"),
            "Wednesday": ("8:00 AM", "10:00 PM"),
            "Thursday": ("8:00 AM", "10:00 PM"),
            "Friday": ("8:00 AM", "10:00 PM"),
            "Saturday": ("8:00 AM", "10:00 PM"),
            "Sunday": ("9:00 AM", "9:00 PM"),
        },
    },
}


def get_store_hours(store_name: str, day_of_week: str) -> dict[str, Any]:
    """Return synthetic opening hours for a named store and weekday."""

    normalized_store = " ".join(store_name.split()).casefold()
    store = _STORE_HOURS.get(normalized_store)
    if store is None:
        return {
            "status": "error",
            "error": "unknown_store",
            "store_name": store_name.strip(),
            "available_stores": sorted(
                item["store_name"] for item in _STORE_HOURS.values()
            ),
        }
    canonical_day = next(
        (
            day
            for day in store["hours"]
            if day.casefold() == " ".join(day_of_week.split()).casefold()
        ),
        None,
    )
    if canonical_day is None:
        return {
            "status": "error",
            "error": "unsupported_day",
            "store_name": store["store_name"],
            "day": day_of_week.strip(),
            "supported_days": list(store["hours"]),
        }
    opens, closes = store["hours"][canonical_day]
    return {
        "status": "ok",
        "store_name": store["store_name"],
        "day": canonical_day,
        "opens": opens,
        "closes": closes,
        "timezone": store["timezone"],
    }
