---
id: progressive-disclosure
term: Progressive disclosure
aliases: ["on-demand loading", "staged loading"]
category: agent-systems
sources: [{"title": "Chapter 2: A Map of Modern Agent Systems — Skills", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/modern-agent-systems/#skills", "note": "The Progressive disclosure subsection explains metadata, core instructions, support material, and available versus model-visible information."}, {"title": "Chapter 4: Writing Great Skills — Writing for Agents", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/writing-great-skills/#writing-for-agents-heading", "note": "Explains why progressive disclosure protects the document’s information hierarchy as well as its context budget."}]
relations: [{"type": "related", "target": "skill"}, {"type": "related", "target": "skill-activation"}, {"type": "related", "target": "context-window"}, {"type": "related", "target": "context-pointer"}, {"type": "related", "target": "context-load"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

Loading a small discovery description first, the selected procedure next, and deeper material only when needed.

## Working definition

Progressive disclosure keeps retrievable knowledge available without putting all of it in every model call. For Skills, compact metadata supports discovery, the main SKILL.md loads after activation, and references or other supporting files are accessed when a step calls for them. Available files and model-visible context are different sets.

## Why it matters

It preserves a clear active workflow and limits irrelevant context. The procedure can remain readable while detailed policies, rubrics, and templates stay accessible at the right point.

## Example

A review Skill exposes its name and description, loads the review sequence when selected, and opens the detailed citation policy only when checking sources.

## Common confusion

This is not merely shortening a document or hiding required instructions. Essential steps must remain discoverable, pointers must name their triggers, and a supporting script can execute without its full source entering the prompt.

## Study-group notes

Chapter 2 teaches the three levels. Chapter 4 treats the same mechanism as information hierarchy: keep immediate steps visible and put branch-specific depth behind reliable pointers.
