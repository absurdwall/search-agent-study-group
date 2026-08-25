"""Deterministic fake orders linked to real Walmart product IDs."""

import json
from datetime import date, timedelta
from pathlib import Path

from fastapi import HTTPException


class OrdersService:
    def __init__(self, fixture: Path | None = None):
        path = fixture or Path(__file__).with_name("orders.json")
        self.orders: list[dict] = json.loads(path.read_text())

    def list(self, start: date | None = None, end: date | None = None) -> list[dict]:
        end = end or date.today()
        start = start or end - timedelta(days=30)
        if start > end:
            raise HTTPException(400, "start_date must not be after end_date")

        summaries = [
            {key: value for key, value in order.items() if key not in {"items", "shipping_address"}}
            for order in self.orders
            if start <= date.fromisoformat(order["order_date"]) <= end
        ]
        return sorted(summaries, key=lambda order: order["order_date"], reverse=True)

    def get(self, order_id: str) -> dict:
        order = next((order for order in self.orders if order["order_id"] == order_id), None)
        if not order:
            raise HTTPException(404, "Order not found")
        return order
