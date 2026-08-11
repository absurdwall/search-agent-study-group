---
name: product-shopping-mcp
description: Use when finding, inspecting, comparing, or recommending products through the remote product catalog.
metadata:
  adk_additional_tools:
    - execute
---

# Product shopping through MCP

Use the activated Code Mode tool for grounded product discovery, inspection, comparison, and recommendations.

## Procedure

1. Call `execute` once with one sandboxed Python program for the whole product request.
2. Inside that program, use `await call_tool(...)` to call `search_products` before retrieving details. Put the user's product type, size, feature, and budget constraints into one concise search query.
3. Select exactly two qualifying product IDs only from returned search rows. Enforce visible constraints and consider both rating and review count when the user asks for highly rated products.
4. Keep each returned product ID exactly as supplied, then call `product_details` twice—once for each selected ID.
5. Return one compact object containing both full product records. After `execute` returns, compare only returned fields, clearly identify missing availability, seller, brand, or specification data, and recommend one candidate from the returned evidence.

## Grounding rules

- Never invent a product, product ID, price, rating, review count, seller, availability, brand, or specification.
- Do not treat a search snippet as a complete product record or compare before both detail records return.
- If search returns fewer qualifying candidates than requested, state how many were found.
- If a tool returns an error, report it plainly and stop rather than guessing another ID or result.
