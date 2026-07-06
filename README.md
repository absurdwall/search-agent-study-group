# Search Agent Study Group

Weekly study and presentation workspace for agent-related material selected by the user.

## Operating Contract

- The weekly source material comes from the user.
- Codex helps understand the material deeply and prepares HTML slides for the presentation.
- Extended reading is allowed when it helps explain a concept, but source discovery is not the default task.
- Slides should use the web well: animation, demos, interaction, responsive layouts, and speaker-friendly structure.
- The Presentations plugin is out of scope unless a PPTX or Google Slides export is explicitly requested.

## Project Shape

- `weeks/`: dated meeting preparation folders
- `raw/`: immutable clips, assets, and repo snapshots
- `meta/`: project rules, publishing workflow, index, and log
- `templates/`: reusable week and deck starters

See `meta/project-organization.md` for the full contract.

## Suggested Weekly Folder

Create a dated folder such as:

```text
weeks/2026-07-07-topic-name/
weeks/2026-07-07-topic-name/slides/
```

The reusable starters live in `templates/week/` and `templates/html-deck/`.

## Local Preview

```bash
python3 -m http.server 8765
```

Then open `http://127.0.0.1:8765/`.
