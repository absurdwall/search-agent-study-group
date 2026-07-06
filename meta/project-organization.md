# Project Organization Rules

This repository supports the Agent Study Group: selected weekly material, collaborative study, and published HTML slide decks.

Repository status: this folder is a local Git repository on branch `main`. It is not a GitHub repository until a remote is created and pushed.

The project borrows the `raw / wiki / meta` style from the LLM-wiki pattern, but the main unit here is the weekly meeting and its published deck. For now, keep the structure simple: `weeks/`, `raw/`, `meta/`, and `templates/`.

## Core Principles

- The user selects the weekly material. Codex does not scout for weekly material unless explicitly asked.
- Preserve raw material. Do not rewrite clipped articles, copied source files, downloaded repo snapshots, or user-authored notes unless asked.
- Keep dated weekly folders as the center of work. Each meeting gets one folder under `weeks/`, including that week’s slides.
- Keep source, synthesis, and presentation separate inside each week: raw captures in `raw/`, study synthesis in weekly markdown files, published HTML in the week’s `slides/` folder.
- Prefer stable GitHub Pages URLs that can be attached to Notion.

## Top-Level Folders

### `weeks/`

Weekly preparation workspace. Folder names should start with the meeting date:

```text
weeks/YYYY-MM-DD-topic-slug/
```

If the topic is not known yet, use only the date:

```text
weeks/2026-07-07/
```

Each weekly folder may contain:

- `materials.md`: selected material, source boundaries, and user notes.
- `study-notes.md`: first-pass map, walkthrough notes, extended-reading notes.
- `slide-brief.md`: audience, objective, narrative arc, demo ideas, slide plan.
- `speaker-notes.md`: presenter-facing notes and timing.
- `source-map.md`: where the claims and examples came from.
- `slides/`: HTML deck and deck-specific assets for this week.

### `raw/`

Immutable source captures and reference material.

Suggested layout:

- `raw/clips/YYYY-MM-DD-topic-slug/`: Obsidian Web Clipper captures, article markdown, PDFs, transcripts, and copied source material for a week.
- `raw/assets/`: downloaded images or media shared across captures.
- `raw/external-repos/<owner>__<repo>/`: pinned snapshots of external repos.
- `raw/references/`: durable reference documents that are not tied to one week.

Rules:

- Treat `raw/` as evidence, not a drafting area.
- For external repo snapshots, include a `.source.json` with repo URL, commit, capture date, and reason for capture.
- Do not cite sibling project `raw/` folders as this project’s provenance unless the user explicitly asks for cross-project synthesis.

### `meta/`

Project operating layer.

Use for:

- `meta/project-organization.md`: folder rules and workflow contract.
- `meta/index.md`: navigation map for the project.
- `meta/log.md`: chronological maintenance and session log.
- `meta/external-repos.md`: index of repo snapshots and references.
- `meta/publishing.md`: GitHub Pages workflow.

### `templates/`

Reusable starters.

Use for:

- `templates/week/`: weekly markdown templates.
- `templates/html-deck/`: reusable HTML deck starter.

### `.agents/skills/`

Reusable Codex workflows for this project. When a workflow becomes repetitive, update a skill instead of expanding `AGENTS.md`.

## Weekly Workflow

1. Create `weeks/YYYY-MM-DD-topic-slug/`.
2. Add selected material links and local captures to `materials.md`.
3. Put raw clips or copied source material under `raw/clips/YYYY-MM-DD-topic-slug/`.
4. Read the selected material and produce a first-pass map before asking optional questions.
5. Walk through the material with the user.
6. Add targeted extended reading only when it clarifies a concept or checks a claim.
7. Draft `slide-brief.md`.
8. Build the deck in `weeks/YYYY-MM-DD-topic-slug/slides/`.
9. Verify the deck locally in a browser.
10. Publish through GitHub Pages and attach the stable deck URL to Notion.

## Naming

- Use ISO dates: `YYYY-MM-DD`.
- Prefer lowercase slugs after the date: `2026-07-07-agent-memory`.
- Keep deck folder names stable after publishing. If the title changes, update the deck contents, not the URL, unless a redirect plan exists.

## GitHub Pages

Default publishing model:

- Publish from the repository root.
- The homepage is `index.html`.
- Weekly deck URLs follow:

```text
https://<owner>.github.io/<repo>/weeks/YYYY-MM-DD-topic-slug/slides/
```

If this later becomes a larger app, add a build system deliberately. Until then, standalone HTML keeps the workflow inspectable and easy for Codex to edit.
