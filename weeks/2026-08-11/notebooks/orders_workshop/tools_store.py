"""Deterministic ecommerce store information for the workshop."""

from __future__ import annotations

from typing import Any


_DAYS = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)

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


def _normalize(value: str) -> str:
    return " ".join(value.split()).casefold()


def get_store_hours(store_name: str, day_of_week: str) -> dict[str, Any]:
    """Return synthetic opening hours for a named store and weekday.

    Args:
        store_name: Store name, such as ``Seattle Downtown``.
        day_of_week: Full weekday name, such as ``Saturday``.

    Returns:
        A structured success result with opening and closing times, or a
        structured error listing the supported choices.
    """

    normalized_store = _normalize(store_name)
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

    normalized_day = _normalize(day_of_week)
    canonical_day = next(
        (day for day in _DAYS if day.casefold() == normalized_day),
        None,
    )
    if canonical_day is None:
        return {
            "status": "error",
            "error": "unsupported_day",
            "store_name": store["store_name"],
            "day": day_of_week.strip(),
            "supported_days": list(_DAYS),
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
