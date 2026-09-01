# Chapter 4 reference material

Status: planning packet. Two bounded Matt Pocock additions are approved: the
seven-Skill delivery path and a short introduction to `writing-for-agents`. The
full source spine, teardown set, chapter contract, narrative, and readiness
decision remain open.

Last link check: 2026-08-25.

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
| Approved short workflow example | [Matt Pocock — Engineering Skills](https://github.com/mattpocock/skills/tree/84fdeffd12f2ee307994d1eb6feb48173b6e0502/skills/engineering) | A practical path through `wayfinder`, `grill-with-docs`, `prototype`, `to-spec`, `to-tickets`, `implement`, and `code-review` | Pinned practitioner example; added to the planned page |
| Approved main teaching reference | [Matt Pocock — The /writing-for-agents Skill](https://www.aihero.dev/skills-writing-for-agents) | What the Skill does, when to use it, the two loads, five levers, common failures, and success signals | Practitioner source published 2026-07-07 and modified 2026-08-24; added to the planned page |
| Approved frozen verification source | [Matt Pocock — Writing for Agents source files](https://github.com/mattpocock/skills/tree/84fdeffd12f2ee307994d1eb6feb48173b6e0502/skills/productivity/writing-for-agents) | Verify context pointers, hierarchy, completion criteria, leading words, pruning, and invocation mechanics against a stable commit | Pinned non-canonical source; added to the planned page |
| Historical practitioner artifact | [Matt Pocock — Writing Great Skills](https://github.com/mattpocock/skills/blob/6bcbcb09e2f1ed5fa20b4e890c732ecbb58c6b64/skills/productivity/writing-great-skills/SKILL.md) | Preserve the original reference that appeared in the placeholder | Historical only; the old main-branch path returned 404 |
| Proposed main teardown | [OpenAI Gmail Skill](https://github.com/openai/plugins/blob/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/gmail/skills/gmail/SKILL.md) | Critically examine routing, sibling trigger overlap, reference boundaries, stop conditions, eval definitions, and maintenance | Recommendation not yet approved |
| Proposed short contrast | [Superpowers systematic-debugging](https://github.com/obra/superpowers/blob/44c9b2d6e889982ac18c27d05a19fefe335194e1/skills/systematic-debugging/SKILL.md) | Contrast strong workflow structure with over-prescriptive doctrine and weak behavioral evidence | Recommendation not yet approved |
| Excluded from main teardown | [Anthropic docx Skill](https://github.com/anthropics/skills/tree/f17010c9bb483898c1d9c9f42dde2b3a98889434/skills/docx) | Possible extended example for deterministic machinery and visual validation | Too large, domain-heavy, and reuse-sensitive for the main teardown |

## Approved bounded additions

### Practical delivery path

The planned page presents this useful composition:

`wayfinder → grill-with-docs → prototype → to-spec → to-tickets → implement → code-review`

This sequence is book synthesis from the pinned Skills, not a claim that the
repository declares one mandatory pipeline. The names are plural exactly as the
repository defines them: `grill-with-docs` and `to-tickets`. `prototype` sits
before `to-spec`: it uses throwaway code to make one unresolved visual or state
question concrete, then carries the validated decision rather than the prototype
code into the specification. With that stage included, no main stage is missing.
`setup-matt-pocock-skills` is a once-per-repository prerequisite, `tdd` is invoked
inside `implement` where possible, and `triage` is not a required stage for the
agent-ready tickets produced by `to-tickets`.

### Writing for Agents

The section follows the current AI Hero explainer's teaching sequence: what the
Skill does, when to use it, the two loads, five authoring levers, a practical
review pass, and observable success signals. The pinned `SKILL.md` and
`SKILL-MECHANICS.md` remain frozen verification sources for the underlying model
and Skill-specific invocation mechanics. The page labels the account as a
practitioner perspective rather than an Agent Skills specification.

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
