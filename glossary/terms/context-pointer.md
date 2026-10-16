---
id: context-pointer
term: Context pointer
aliases: ["document pointer", "reference pointer"]
category: control-and-quality
sources: [{"title": "Chapter 4: Writing Great Skills — Writing for Agents", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/writing-great-skills/#writing-for-agents-heading", "note": "Context pointers and the practical review pass require a description of the material and the distinct trigger branches that should load it."}]
relations: [{"type": "related", "target": "progressive-disclosure"}, {"type": "related", "target": "skill-activation"}, {"type": "related", "target": "instruction-file"}, {"type": "related", "target": "completion-criteria"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

A short instruction that says what further material exists and when the agent should load it.

## Working definition

A context pointer directs an agent to supporting material while stating the distinct task conditions that make it relevant. The target may be a policy, Skill, reference, or other document. The pointer’s wording is part of the discovery mechanism: a good target alone cannot ensure that the agent finds it.

## Why it matters

Pointers make progressive disclosure practical. They preserve a concise active path while keeping the necessary branch-specific guidance reachable at the moment it matters.

## Example

“When verifying factual claims or adding citations, read source-policy.md for approved sources and citation rules” identifies both the material and its trigger.

## Common confusion

A bare filename or vague “see the docs” link may not explain when to load the target. Repeating synonyms for one trigger does not cover a genuinely different branch, and hidden mandatory steps are not a good hierarchy.

## Study-group notes

Chapter 4 makes pointer quality a behavior question: will the agent take the intended branch? Review the pointer together with its target, rather than polishing the target in isolation.
