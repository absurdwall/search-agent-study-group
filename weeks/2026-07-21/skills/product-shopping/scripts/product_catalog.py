"""Trusted CLI and function client for the product catalog service."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any, Sequence

import httpx


PRODUCT_API_BASE_URL = "https://walmart-demo-api-k2yx3oubha-ue.a.run.app"
REQUEST_TIMEOUT_SECONDS = 200.0


def _get_json(
    path: str,
    *,
    params: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Fetch one bounded JSON response without exposing unexpected bodies."""
    try:
        with httpx.Client(
            base_url=PRODUCT_API_BASE_URL,
            timeout=REQUEST_TIMEOUT_SECONDS,
        ) as client:
            response = client.get(path, params=params)
            response.raise_for_status()
            payload = response.json()
    except httpx.TimeoutException as exc:
        raise RuntimeError("The product service timed out.") from exc
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"The product service returned HTTP {exc.response.status_code}."
        ) from exc
    except (httpx.HTTPError, ValueError) as exc:
        raise RuntimeError("The product service returned an invalid response.") from exc

    if not isinstance(payload, dict):
        raise RuntimeError("The product service returned non-object JSON.")
    return payload


def search_products(query: str) -> dict[str, Any]:
    """Search products matching a concise natural-language query.

    Args:
        query: Product keywords and constraints such as size, features, or budget.
    """
    normalized = " ".join(query.split())
    if not normalized:
        raise ValueError("query must not be empty")
    return _get_json("/v1/products/search", params={"q": normalized})


def get_product_details(product_id: str) -> dict[str, Any]:
    """Retrieve authoritative details for one numeric product ID.

    Args:
        product_id: The numeric product ID returned by product search.
    """
    if not re.fullmatch(r"[0-9]{1,32}", product_id):
        raise ValueError("product_id must contain 1–32 digits")
    return _get_json(f"/v1/products/{product_id}")


def build_parser() -> argparse.ArgumentParser:
    """Build the skill CLI parser."""
    parser = argparse.ArgumentParser(
        description="Search the product catalog or retrieve product details."
    )
    commands = parser.add_subparsers(dest="operation", required=True)

    search = commands.add_parser("search", help="Search for product candidates.")
    search.add_argument("--query", required=True, help="Natural-language search query.")

    details = commands.add_parser("details", help="Retrieve one complete product record.")
    details.add_argument(
        "--product-id",
        required=True,
        help="Numeric product ID returned by search.",
    )
    return parser


def _run_command(arguments: argparse.Namespace) -> dict[str, Any]:
    if arguments.operation == "search":
        return search_products(arguments.query)
    return get_product_details(arguments.product_id)


def main(argv: Sequence[str] | None = None) -> int:
    """Run one operation and emit machine-readable JSON."""
    arguments = build_parser().parse_args(argv)
    try:
        payload = _run_command(arguments)
    except (RuntimeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
