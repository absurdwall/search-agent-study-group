"""Orders API tools used by the Orders-agent workshop."""

from __future__ import annotations

import re
from datetime import date
from typing import Any

import httpx


ORDER_API_BASE_URL = "https://walmart-demo-api-k2yx3oubha-ue.a.run.app"
REQUEST_TIMEOUT_SECONDS = 30.0
ORDER_ID_PATTERN = re.compile(r"WM-DEMO-[0-9]{4}")


class OrderAPIError(RuntimeError):
    """A concise, learner-safe failure from the teaching orders API."""


def _get_json(path: str, *, params: dict[str, str] | None = None) -> Any:
    try:
        with httpx.Client(
            base_url=ORDER_API_BASE_URL,
            timeout=REQUEST_TIMEOUT_SECONDS,
        ) as client:
            response = client.get(path, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException as exc:
        raise OrderAPIError("The orders service timed out; retry the cell once.") from exc
    except httpx.HTTPStatusError as exc:
        raise OrderAPIError(
            f"The orders service returned HTTP {exc.response.status_code}."
        ) from exc
    except (httpx.HTTPError, ValueError) as exc:
        raise OrderAPIError("The orders service returned an invalid response.") from exc


def healthcheck() -> None:
    payload = _get_json("/health")
    if payload != {"status": "ok"}:
        raise OrderAPIError("The orders service health check did not return status=ok.")


def list_orders(start_date: str, end_date: str) -> list[dict[str, Any]]:
    """List order summaries for an inclusive YYYY-MM-DD date range."""
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
    except ValueError as exc:
        raise ValueError("dates must use YYYY-MM-DD format") from exc
    if start > end:
        raise ValueError("start_date must not be after end_date")
    payload = _get_json(
        "/v1/orders",
        params={"start_date": start.isoformat(), "end_date": end.isoformat()},
    )
    if not isinstance(payload, list) or not all(isinstance(row, dict) for row in payload):
        raise OrderAPIError("The orders service returned invalid order summaries.")
    return payload


def get_order(order_id: str) -> dict[str, Any]:
    """Retrieve full details for one demo order ID."""
    if ORDER_ID_PATTERN.fullmatch(order_id) is None:
        raise ValueError("order_id must match WM-DEMO-####")
    payload = _get_json(f"/v1/orders/{order_id}")
    if not isinstance(payload, dict):
        raise OrderAPIError("The orders service returned invalid order details.")
    return payload
