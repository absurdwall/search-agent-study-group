---
id: instruction-file
term: Instruction file
aliases: ["AGENTS.md", "CLAUDE.md", "project instructions"]
category: agent-systems
sources: [{"title": "Chapter 2: A Map of Modern Agent Systems — Instruction files", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/modern-agent-systems/#instruction-files", "note": "Defines instruction files and explains discovery, composition, scoping, host-specific precedence, and the limits of natural-language guidance."}]
relations: [{"type": "contrasts_with", "target": "skill"}, {"type": "related", "target": "prompt"}, {"type": "related", "target": "context-window"}, {"type": "related", "target": "context-pointer"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

A file of durable project guidance that a compatible host loads according to its own discovery and scope rules.

## Working definition

An instruction file stores guidance that should recur across tasks, such as repository structure, validation commands, coding conventions, and human decision boundaries. A compatible host finds applicable files, combines their text, resolves precedence, and places the selected guidance in model context. Filename, location, and loading behavior depend on the product.

## Why it matters

Keeping recurring rules beside the project makes them reviewable and versionable. Appropriate scoping helps the agent receive relevant rules without loading every team’s procedures for every task.

## Example

While editing a book chapter, the host may combine repository-wide guidance with book-specific instructions to preserve stable URLs and run the book checks. Instructions in an unrelated frontend subtree need not apply.

## Common confusion

Writing AGENTS.md does not guarantee that every host reads it, and natural-language instructions are not hard enforcement. AGENTS.md and CLAUDE.md can share content without sharing identical loaders or precedence rules.

## Study-group notes

Chapter 2 begins here: durable guidance answers “What rules apply while I work here?” Compare it with a Skill’s task-specific method and MCP’s connection boundary. Check the host before assuming that the nearest file wins.
