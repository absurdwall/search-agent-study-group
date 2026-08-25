---
name: order-support
description: Use when answering questions about ecommerce order history, order status, totals, or item details.
metadata:
  adk_additional_tools:
    - list_orders
    - get_order
---

# Order support

Use the activated order tools to answer factual questions about synthetic ecommerce shopping orders.

## Procedure

1. If the user supplies an order ID, call `get_order` directly. Do not list unrelated orders first.
2. If the order ID is unknown, convert any requested period into explicit, inclusive `YYYY-MM-DD` start and end dates.
3. Call `list_orders` only when discovery or date filtering is needed. Select order IDs only from its returned summaries.
4. When the user asks for the most recent order, compare only the returned order dates and select the newest one in the requested period.
5. Call `get_order` for the selected order before reporting item names, quantities, or other detail-only fields.
6. Base status, date, total, and item claims only on returned fields. Clearly identify missing fields.
7. If a tool returns an error or no matching orders, report that result plainly and stop.

## Grounding rules

- Never invent an order ID, date, status, total, item, quantity, or delivery fact.
- Do not treat an order summary as the full order record.
- Do not guess a wider date range or substitute a different order after an error.
