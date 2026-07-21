---
name: product-shopping
description: Use for finding products, inspecting full product details, and making grounded product comparisons.
---

# Product shopping

Use this skill whenever a user asks you to find, inspect, compare, or recommend products.

The bundled script is `scripts/product_catalog.py`. Use `run_skill_script` with `args` as a complete list of command-line arguments.

## Available operations

Search for candidates:

```text
run_skill_script(
  skill_name="product-shopping",
  file_path="scripts/product_catalog.py",
  args=["search", "--query", "55-inch 4K TV under $400"]
)
```

Retrieve authoritative details for one product ID returned by search:

```text
run_skill_script(
  skill_name="product-shopping",
  file_path="scripts/product_catalog.py",
  args=["details", "--product-id", "123456789"]
)
```

## Procedure

1. Search before making a recommendation. Include the user's meaningful constraints in one concise query.
2. Use only returned search rows when selecting candidates. Discard rows that clearly violate requested constraints such as product type, screen size, or budget. For “highly rated,” consider both rating and review count.
3. When the user asks to compare full details, run `details` separately for every selected product ID.
4. Compare only fields present in the returned records. Clearly identify missing availability, seller, brand, or specification data.
5. Recommend one product only after retrieving the necessary detail records, and explain the evidence behind the choice.

## Grounding and errors

- Never invent a product, product ID, price, rating, availability, seller, brand, or specification.
- Never treat search snippets as complete product details.
- If search returns fewer candidates than requested, say how many were found.
- If the script returns an error, report it plainly and stop rather than guessing another product ID or script path.
