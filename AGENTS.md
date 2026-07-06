# Search Agent Study Group Working Agreements

This project supports a weekly study group on agent-related work.

Follow `meta/project-organization.md` for the folder structure and publishing workflow.

## Role Split

- The user selects and provides the weekly material.
- Codex does not scout for weekly material unless the user explicitly asks.
- Codex helps study the selected material in depth, including targeted extended reading when a concept needs more context.
- Codex helps produce the weekly presentation as direct HTML slides, using interaction, animation, demos, CSS, JavaScript, and web-native affordances where they improve the talk.
- Do not use the Presentations plugin for this project unless the user explicitly asks for a PPTX or Google Slides export.

## Weekly Workflow

1. Read the provided material and produce a grounded first-pass map: thesis, key concepts, claims, mechanisms, examples, uncertainties, and presentation angles.
2. Walk through the material with the user section by section.
3. Add targeted extended reading only when it helps explain a concept or validate a claim.
4. Draft a slide brief before building: audience, talk objective, narrative arc, demo opportunities, and slide-by-slide intent.
5. Build the HTML slide deck under `weeks/YYYY-MM-DD-topic-slug/slides/` and verify it locally in a browser.

## Slide Principles

- Prefer HTML-native strengths over PowerPoint imitation: live demos, animated diagrams, progressive disclosure, interactive controls, code panes, canvas/WebGL, scroll-driven or keyboard-driven narrative, and responsive layouts.
- Keep the deck presentation-ready: legible from a meeting screen, navigable by keyboard, and stable on common desktop viewports.
- Use visual motion to clarify structure or causality, not as decoration.
- Keep speaker-facing notes separate from on-slide copy.
- Preserve user-provided material and notes by default. Do not rewrite source notes unless asked.
- Keep published deck URLs stable after sharing them in Notion.

## Files

- `weeks/` stores dated weekly study notes, material links, slide briefs, and that week’s `slides/` folder.
- `raw/` stores immutable source captures and repo snapshots.
- `meta/` stores project rules, logs, publishing workflow, and indexes.
- `templates/` stores reusable weekly and HTML-deck starters.
- `.agents/skills/` stores reusable workflows for this project.
