# Publishing Workflow

The intended publishing target is GitHub Pages.

## Current Repository

- Repository: <https://github.com/absurdwall/search-agent-study-group>
- Pages source: branch `main`, folder `/ (root)`.
- GitHub Pages URL: <https://absurdwall.github.io/search-agent-study-group/>
- Primary local remote: `origin`.
- The temporary repository, <https://github.com/tykswtr/search-agent-study-group-backup>,
  is retained as `backup-origin` for recovery; it is no longer a publishing target.

The original `absurdwall` repository is the primary repository again. Its Pages
configuration was verified through the GitHub API on October 17, 2026: branch
`main`, folder `/ (root)`. Migration preserves the six commits added on the
temporary repository, including the Chapter 5 demos and Site version 14 sync.
The historical [Site version 14 source sync](site-sync-v14.md) record retains
the backup URLs used at that time; current navigation and glossary citations
point to the original repository and Pages URL above.

## Default Model

- Keep publishable files in the repository root.
- Keep each deck at `weeks/YYYY-MM-DD-topic-slug/slides/index.html`.
- Link Notion to the stable deck URL after GitHub Pages is enabled.

## First-Time GitHub Setup

1. Create a GitHub repository for this local repo.
2. Push the `main` branch.
3. In GitHub, enable Pages from the root of the `main` branch.
4. Confirm the homepage loads.
5. Attach weekly deck URLs to Notion.

## Local Verification

From the repository root:

```bash
python3 -m http.server 8765
```

Then open:

```text
http://127.0.0.1:8765/
```

Weekly decks will be available locally at:

```text
http://127.0.0.1:8765/weeks/YYYY-MM-DD-topic-slug/slides/
```

Verify every deck before publishing:

- browser loads without console errors
- keyboard navigation works
- text does not overlap at presentation size
- animations clarify the talk
- all source claims are traceable to weekly material or noted extended reading
