# Publishing Workflow

The intended publishing target is GitHub Pages.

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
