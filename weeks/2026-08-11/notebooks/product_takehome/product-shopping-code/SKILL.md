---
name: product-shopping-code
description: Use when finding, inspecting, comparing, or recommending products through the remote product catalog.
metadata:
  adk_additional_tools:
    - search_products
    - product_details
---

# Product shopping through MCP

Use the activated product tools to produce grounded product comparisons and recommendations.

## Procedure

1. YOUR TURN 1: Call `search_products` first with the user's product constraints.
2. YOUR TURN 2: Preserve product IDs exactly as returned by the search results.
3. YOUR TURN 3: Call `product_details` for each selected product ID.
4. YOUR TURN 4: Compare candidates only with returned fields and ground the recommendation in that evidence.
5. YOUR TURN 5: State missing data or tool errors plainly instead of inventing an answer.

## Grounding rules

- Never invent a product, product ID, price, rating, review count, seller, availability, brand, or specification.
- If the product catalog reports an error or too few qualifying candidates, say so plainly instead of guessing.
