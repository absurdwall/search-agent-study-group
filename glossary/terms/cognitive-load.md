---
id: cognitive-load
term: Cognitive load
aliases: ["human discovery burden"]
category: control-and-quality
sources: [{"title": "Chapter 4: Writing Great Skills — Writing for Agents", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/writing-great-skills/#writing-for-agents-heading", "note": "The two loads defines the human discovery burden and compares user-invoked with model-invoked Skills."}]
relations: [{"type": "contrasts_with", "target": "context-load"}, {"type": "related", "target": "skill-activation"}, {"type": "related", "target": "context-pointer"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

In the chapter’s writing model, the effort a person spends remembering which documents exist and when to invoke them.

## Working definition

Chapter 4 uses cognitive load for the human side of document discovery. When a workflow requires deliberate invocation, the person must remember the available document or Skill and recognize the right moment to call it. This preserves human selection but makes the human responsible for indexing the available guidance.

## Why it matters

Removing discovery material from model context does not eliminate the selection problem. It can shift that work to a person, who may forget a valuable procedure or choose the wrong one.

## Example

A user-invoked review Skill stays out of autonomous discovery, so the user must remember to request it whenever a chapter needs that review.

## Common confusion

The chapter uses a bounded authoring meaning, not a general psychological measure or the model’s reasoning effort. Lower context load can increase this human burden, but the tradeoff depends on the host’s invocation design.

## Study-group notes

Use the two-load comparison from Chapter 4 when choosing whether a document should be found automatically or deliberately called. The goal is reliable behavior, not minimizing one budget in isolation.
