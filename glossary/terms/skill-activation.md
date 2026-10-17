---
id: skill-activation
term: Skill activation
aliases: ["Skill invocation", "implicit activation", "explicit invocation"]
category: agent-systems
sources: [{"title": "Chapter 2: A Map of Modern Agent Systems — Skills", "url": "https://absurdwall.github.io/search-agent-study-group/book/modern-agent-systems/#skills", "note": "Discovery and activation separates catalog metadata, implicit or explicit selection, core instructions, and later support-file access."}, {"title": "Chapter 4: Writing Great Skills — Writing for Agents", "url": "https://absurdwall.github.io/search-agent-study-group/book/writing-great-skills/#writing-for-agents-heading", "note": "Connects model-invoked and user-invoked documents to context load and human cognitive load."}]
relations: [{"type": "related", "target": "skill"}, {"type": "related", "target": "progressive-disclosure"}, {"type": "related", "target": "context-load"}, {"type": "related", "target": "cognitive-load"}, {"type": "related", "target": "context-pointer"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

The step that selects a discovered Skill and makes its full procedure available for the current task.

## Working definition

After a host discovers Skill metadata, a model or host may match the task to a description and activate the Skill implicitly, or a user may invoke it explicitly. Activation loads the main procedure; supporting files can remain deferred. Exact commands, selection policies, and access rules are host-specific.

## Why it matters

A good procedure cannot help if it is never selected. Clear descriptions and explicit invocation help diagnose misses while controlling how much context and human attention discovery requires.

## Example

The host shows a short documentation-review description. A chapter-review request triggers it, or the user names that Skill directly; the agent then reads its full SKILL.md.

## Common confusion

Discovery is not activation: seeing a name and description does not mean the procedure has been loaded. Implicit matching is not guaranteed, and invocation does not by itself create tools, permissions, or a new agent.

## Study-group notes

Chapter 2 traces discovery through loading. Chapter 4’s two-load model adds the tradeoff: autonomous selection uses model-visible discovery material, while deliberate invocation requires the human to remember the right method.
