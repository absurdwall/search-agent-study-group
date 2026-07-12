---
id: skill
term: Skill
aliases: ["agent skill", "SKILL.md"]
category: agent-systems
status: published
introduced_in: week-01
last_reviewed: 2026-07-12
relations: [
  {"type": "related", "target": "context-window"},
  {"type": "related", "target": "llm-agent"}
]
sources: [
  {
    "title": "Skills for ADK agents",
    "url": "https://adk.dev/skills/",
    "note": "Defines an ADK Skill as a modular task-specific unit of instructions, resources, and tools that can be loaded incrementally."
  }
]
---

## Simple definition

A modular package of task-specific instructions, resources, and tools that an agent can load when needed.

## Working definition

An agent Skill packages specialized guidance for a task or domain so it can be discovered and loaded incrementally. In ADK, a Skill can include metadata, instructions, reference resources, scripts, assets, and associated tools rather than requiring all domain knowledge to remain in the base prompt.

## Why it matters

Skills organize expertise into reusable modules and reduce unnecessary context. They let an agent load detailed guidance only when relevant, improving maintainability and conserving context-window space.

## Example

A recipe Skill exposes a short description for discovery and loads detailed dietary rules, tool instructions, and reference material only after the agent recognizes a recipe request.

## Common confusion

A Skill is not another agent. Loading one enriches the current agent's available instructions and resources; it does not inherently create a separate model call, execution loop, or isolated session.

## Study-group notes

Week 1 used a simple two-tier `SKILL.md` pattern: short metadata always available, with fuller Markdown instructions loaded on demand. Current ADK Skills can also package resources and tools, and the feature is experimental as of this review.
