# Search Agent Study Group

Public website and teaching-materials workspace for a weekly study group on
agentic AI systems.

- [Study group website](https://absurdwall.github.io/search-agent-study-group/)
- [Learner lab](https://github.com/absurdwall/search-agent-lab)
- [Notion resources](https://outrageous-tango-920.notion.site/Agent-Study-Group-Home-1566f86e0b05832bbbac817d762daad8?pvs=74)

## Repository map

- `weeks/`: weekly pages, preparation notes, demos, and HTML presentations
- `glossary/`: source-backed agent concept definitions and the public glossary
- `raw/`: immutable source captures, assets, and external-repository snapshots
- `meta/`: project organization, publishing workflow, indexes, and logs
- `templates/`: reusable weekly and HTML-deck starters
- `scripts/`: small dependency-free maintenance and validation tools

See [`meta/project-organization.md`](meta/project-organization.md) for the full
working agreement.

## Local preview

From the repository root:

```bash
python3 -m http.server 8765
```

Then open <http://127.0.0.1:8765/>. The public site is published from `main`
through GitHub Pages.
