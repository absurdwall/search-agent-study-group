# Chapter 4 reference material

Status: reference-only planning packet; no source spine, teardown set, chapter
contract, narrative, or readiness decision is approved.

Last link check: 2026-08-24.

## Chapter boundary

Chapter 2 already owns Skill basics: why Skills exist, package anatomy,
discovery and loading, progressive disclosure, host differences, and when a
Skill fits. Chapter 3 owns general prompting and context engineering.

The proposed Chapter 4 teaching job is narrower: turn a recurring workflow into
the smallest Skill that is discoverable, executable, verifiable, and
improvable.

## Candidate source roles

| Role | Material | Intended use | Status |
| --- | --- | --- | --- |
| Current official product guidance | [OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills) | Skill structure, discovery, progressive disclosure, resources, and testing | Link verified 2026-08-24 |
| Open specification | [Agent Skills specification](https://agentskills.io/specification) | Required metadata, directory structure, references, scripts, assets, and validation | Link verified 2026-08-24 |
| Practitioner perspective | [Matt Pocock — Writing for Agents](https://github.com/mattpocock/skills/blob/1fc6573e0e300118ce342fb9365521c9c34eefd4/skills/productivity/writing-for-agents/SKILL.md) | Invocation, descriptions, information hierarchy, completion criteria, and progressive disclosure | Pinned rename-era artifact; non-canonical |
| Historical practitioner artifact | [Matt Pocock — Writing Great Skills](https://github.com/mattpocock/skills/blob/6bcbcb09e2f1ed5fa20b4e890c732ecbb58c6b64/skills/productivity/writing-great-skills/SKILL.md) | Preserve the original reference that appeared in the placeholder | Historical only; the old main-branch path returned 404 |
| Proposed main teardown | [OpenAI Gmail Skill](https://github.com/openai/plugins/blob/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/gmail/skills/gmail/SKILL.md) | Critically examine routing, sibling trigger overlap, reference boundaries, stop conditions, eval definitions, and maintenance | Recommendation not yet approved |
| Proposed short contrast | [Superpowers systematic-debugging](https://github.com/obra/superpowers/blob/44c9b2d6e889982ac18c27d05a19fefe335194e1/skills/systematic-debugging/SKILL.md) | Contrast strong workflow structure with over-prescriptive doctrine and weak behavioral evidence | Recommendation not yet approved |
| Excluded from main teardown | [Anthropic docx Skill](https://github.com/anthropics/skills/tree/f17010c9bb483898c1d9c9f42dde2b3a98889434/skills/docx) | Possible extended example for deterministic machinery and visual validation | Too large, domain-heavy, and reuse-sensitive for the main teardown |

## Frozen Gmail packet

- [Core `SKILL.md`](https://github.com/openai/plugins/blob/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/gmail/skills/gmail/SKILL.md)
- [Pasted-link workflow](https://github.com/openai/plugins/blob/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/gmail/skills/gmail/references/pasted-link-workflow.md)
- [Eval definitions](https://github.com/openai/plugins/blob/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/gmail/skills/gmail/evals/evals.json)
- [`agents/openai.yaml`](https://github.com/openai/plugins/blob/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/gmail/skills/gmail/agents/openai.yaml)
- [Maintenance commit `344910e`](https://github.com/openai/plugins/commit/344910e)
- [Maintenance commit `c22c1de`](https://github.com/openai/plugins/commit/c22c1de)

## Decisions to resume before drafting

1. Confirm the reader and the chapter outcome.
2. Approve or replace the proposed teaching-resource spine.
3. Approve the Gmail teardown and systematic-debugging contrast.
4. Decide which examples, exercises, and visual teaching jobs belong on-page.
5. Define what counts as structural validation, proposed eval coverage, and
   executed behavioral evidence without treating them as interchangeable.
