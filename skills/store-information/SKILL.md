---
name: store-information
description: Use when answering questions about store hours, locations, or time zones.
metadata:
  adk_additional_tools:
    - get_store_hours
---

# Store information

Use the activated store-hours tool to answer factual questions about synthetic teaching stores.

## Procedure

1. Identify the requested store location and day.
2. Call `get_store_hours` with the location.
3. Report opening and closing times for the requested day and include the returned time zone.
4. If the store or day is missing, state that plainly instead of guessing.

## Grounding rules

- Never invent a store location, opening time, closing time, day, or time zone.
- Use only fields returned by `get_store_hours`.
