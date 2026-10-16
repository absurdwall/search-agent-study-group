---
id: guardrail
term: Guardrail
aliases: ["agent guardrail", "safety guardrail", "action gate"]
category: control-and-quality
sources: [{"title": "Chapter 5: Guardrails", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/guardrails-hooks-and-evals/#guardrails", "note": "Defines the term and its role in the chapter’s examples."}, {"title": "Chapter 5: Prevent an accidental overwrite", "url": "https://tykswtr.github.io/search-agent-study-group-backup/book/guardrails-hooks-and-evals/#action-boundary", "note": "Shows why an early check and enforcement inside the acting tool serve complementary purposes."}]
relations: [{"type": "related", "target": "hook"}, {"type": "related", "target": "tool"}, {"type": "related", "target": "evaluation"}, {"type": "related", "target": "callback"}]
status: published
last_reviewed: 2026-10-16
---

## Simple definition

A check or limit intended to keep an agent’s behavior within a rule.

## Working definition

A guardrail checks or restricts access, operations, content, approvals, or outputs. It may be implemented through permissions, tool behavior, validators, hooks, or an approval flow. Its protection depends on its timing, coverage, authority, and failure policy; a framework’s named Guardrails API covers only particular kinds of checks.

## Why it matters

Agents can affect files and external systems. Appropriate controls can limit those effects and provide feedback for safe recovery when an operation is denied or cannot be validated.

## Example

A pre-tool check rejects moving a receipt onto an occupied path. The move tool also enforces a no-replace rule at execution, protecting the original if the earlier check becomes stale or is skipped.

## Common confusion

A prompt stating a rule is not strong enforcement. A content scan can miss problems, an output check cannot undo a completed upload, and a validator error is not a passing check.

## Study-group notes

Start with the rule, then choose a component with the information and authority to enforce it. Test allowed, denied, unavailable-validator, and safely incomplete outcomes separately.
