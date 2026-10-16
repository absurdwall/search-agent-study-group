---
id: sub-agent
term: Sub-agent
aliases: ["subagent", "child agent"]
category: agent-systems
status: published
last_reviewed: 2026-10-16
relations: [{"type": "broader", "target": "agent"}, {"type": "related", "target": "runner"}]
sources: [{"title": "Chapter 1 · Keep context efficient", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/minimal-agentic-system/#context", "note": "Introduces delegation into a separate context and returning findings."}]
---

## Simple definition

An agent assigned a bounded part of another agent’s work.

## Working definition

A sub-agent handles delegated work with its own instructions and execution context, then returns findings or takes responsibility according to the host’s design. Isolation, inherited context, available tools, and control transfer are product-specific.

## Why it matters

Delegation can keep a large investigation in a separate context and return only the useful findings, leaving the parent more room for the main task.

## Example

A parent asks a research sub-agent to inspect a large source set and return relevant findings, keeping the full investigation out of the parent’s context.

## Common confusion

Loading a Skill adds guidance to an agent; delegating to a sub-agent runs another agent. Call-and-return and transfer of conversational control are different patterns, not universal synonyms.

## Study-group notes

Chapter 1 uses subagents as a context-efficiency strategy. Chapter 2’s dedicated Subagents section is still planned.
