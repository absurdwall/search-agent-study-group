---
id: skill
term: Skill
aliases: ["agent skill", "Agent Skills", "SKILL.md"]
category: agent-systems
sources: [{"title": "Chapter 2: A Map of Modern Agent Systems — Skills", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/modern-agent-systems/#skills", "note": "Defines the portable package, SKILL.md, optional directories, discovery and activation, progressive disclosure, and neighboring concepts."}, {"title": "Chapter 4: Writing Great Skills — Writing for Agents", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/writing-great-skills/#writing-for-agents-heading", "note": "Applies the writing-for-agents review model to Skill descriptions, procedures, pointers, and completion criteria."}]
relations: [{"type": "contrasts_with", "target": "instruction-file"}, {"type": "contrasts_with", "target": "tool"}, {"type": "contrasts_with", "target": "model-context-protocol"}, {"type": "related", "target": "skill-activation"}, {"type": "uses", "target": "progressive-disclosure"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

A reusable package of procedural instructions and optional references, scripts, and assets that an agent can load when relevant.

## Working definition

A Skill packages a recognizable task method in a folder whose entry point is SKILL.md. Compact metadata supports discovery; the main instructions describe inputs, steps, decisions, boundaries, and outputs. References, scripts, and assets supply optional depth. A compatible client determines discovery locations, activation, access, and execution rules.

## Why it matters

Skills preserve a team’s method without repeating a full playbook in every request or loading every procedure permanently. They can combine model judgment with maintained references and deterministic helpers.

## Example

A documentation-review Skill directs the agent to read the chapter, consult a source policy, execute a link checker, apply a review rubric, and use a report template.

## Common confusion

A Skill is neither one callable Tool nor another agent. It supplies a method; MCP supplies a connection, and tools perform operations. Following the package format does not guarantee identical activation or execution in every host.

## Study-group notes

Chapter 2 provides the full introduction and three-level loading model. Chapter 4 remains planned overall, with bounded delivery and writing examples rather than a complete authoring guide.
