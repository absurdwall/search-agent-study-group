---
id: context-load
term: Context load
aliases: ["always-loaded context cost"]
category: control-and-quality
sources: [{"title": "Chapter 4: Writing Great Skills — Writing for Agents", "url": "https://absurdwall.github.io/search-agent-study-group/book/writing-great-skills/#writing-for-agents-heading", "note": "The two loads defines context load, and the hierarchy and pruning sections explain how authoring choices affect it."}]
relations: [{"type": "contrasts_with", "target": "cognitive-load"}, {"type": "related", "target": "context-window"}, {"type": "related", "target": "progressive-disclosure"}, {"type": "related", "target": "instruction-file"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

The token and attention cost of material kept in the agent’s context whether or not the current task needs it.

## Working definition

In Chapter 4’s Writing for Agents model, context load is the ongoing cost of material such as instruction-file lines and Skill descriptions that is loaded for discovery or general guidance. Choosing what to keep immediately visible, defer, or remove changes that cost and the agent’s ability to find the important instructions.

## Why it matters

Always-present text makes relevant guidance easier to encounter, but unnecessary text consumes space and attention. Good authoring preserves behavior while avoiding material that does no useful work.

## Example

A catalog keeps short Skill descriptions visible so the model can choose a method, while the full source-policy reference loads only during a citation review.

## Common confusion

Context load is not the context window’s maximum capacity, and it is not simply document length. A short but misleading pointer can save tokens while making the workflow less reliable.

## Study-group notes

This term comes from Chapter 4’s practitioner model, not a universal runtime metric. Discuss it alongside cognitive load: moving selection work out of model context may move it onto the human.
