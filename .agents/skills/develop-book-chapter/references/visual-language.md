# Book visual and table language

## Content-first, source-led visuals

Get the teaching content, source coverage, and chapter sequence right first.
Treat visuals as part of chapter composition, but do not let original media
production displace the harder work of representing the selected material
accurately.

Start with the selected teaching resources. Reuse, embed, or link their strong
visuals when they already explain the concept well and the permission,
attribution, and technical constraints are acceptable. Creating a visually
consistent wrapper is often more valuable than redrawing the source.

Create a new visual only when:

- existing resource visuals do not perform the required teaching job;
- the visual is necessary enough to justify production effort; and
- the exact content, states, labels, and exclusions are already clear.

Visuals can still make the book exciting, reduce intimidation, make mechanisms
easier to understand, and create memorable anchors.

During drafting, put visual placeholders directly in the reader-facing work-in-
progress page at the intended locations. Internal visual notes supplement these
placeholders; they do not replace them.

Review the page's visual rhythm before producing media:

- Are long text stretches interrupted at useful moments?
- Does each important mechanism have an appropriate visual anchor?
- Are neighboring visuals teaching different things?
- Does the opening create curiosity?
- Can the reader see where state or responsibility changes?

## Required placeholder brief

Never write only “add image here.” Give each placeholder a stable ID and include:

- **Teaching job:** What the reader should understand, notice, or feel.
- **Medium:** Image, source figure, animation, video, interaction, or another
  justified format.
- **Exact scene or sequence:** Actors, objects, composition, states, transitions,
  camera/view, and reading order.
- **Required content:** Labels, relationships, values, examples, annotations,
  and any source-derived elements that must appear.
- **Visual direction:** Tone, density, typography, palette, framing, and how it
  should fit this long-form book.
- **Avoid:** Misconceptions, misleading arrows, decorative clutter, excessive
  text, unwanted product branding, and concepts owned by another chapter.
- **Placement and transition:** Exact section location and how surrounding prose
  introduces and interprets it.
- **Source strategy:** Reuse or link an existing teaching visual, search for an
  accurate source, or—only when necessary—generate from the brief or build a
  native diagram. Name the preferred existing visual when one is known.
- **Accessibility and fallback:** Alt-text goal, caption, mobile behavior,
  reduced-motion behavior, and static/no-JavaScript equivalent.
- **Reuse or production brief:** Name the preferred source visual and intended
  treatment. If an original is necessary, provide a consolidated description
  detailed enough to paste into an image generator or hand to a
  designer/developer.

When a visual derives from a selected teaching resource, state which parts come
from it and which parts are original adaptation. Do not recreate it merely to
make it look more proprietary or stylistically uniform.

## Suggested HTML placeholder

Match the project's current classes when available. A work-in-progress chapter
may use this semantic shape:

```html
<details class="draft-visual-placeholder" open>
  <summary>
    Planned visual · C2-V01
    <span>Animation with static fallback</span>
  </summary>
  <dl class="draft-visual-brief">
    <div><dt>Teaching job</dt><dd>...</dd></div>
    <div><dt>Scene</dt><dd>...</dd></div>
    <div><dt>Required</dt><dd>...</dd></div>
    <div><dt>Avoid</dt><dd>...</dd></div>
    <div><dt>Source visual</dt><dd>...</dd></div>
    <div><dt>Fallback</dt><dd>...</dd></div>
    <div><dt>Production brief</dt><dd>Only if an original is necessary...</dd></div>
  </dl>
</details>
```

Keep the placeholder visible while the chapter is being collaboratively
drafted. Replace it only after the visual is approved and implemented.

## Native visuals

Use stable semantic roles where relevant:

- model;
- runtime or host;
- tool or external capability;
- context, state, or data;
- observation or result;
- final output.

Do not rely on color alone. Use labels, shape, position, borders, or line style.
Use motion to explain causality or changing state, not as decoration. Avoid
autoplay; respect reduced motion and provide a meaningful static fallback.

## External figures

Preserve third-party figures unmodified unless the license and user decision
permit adaptation. Create consistency through:

- a restrained wrapper;
- descriptive caption;
- creator and source link;
- caveat when the figure is product-specific;
- full-size link;
- useful alt text or accessible narrative;
- provenance record for local copies.

Verify creator, source URL, license or permission status, transformations,
attribution requirements, and checksum when appropriate.

If copying or embedding is not appropriate, prefer a direct source link, linked
preview, or textual pointer over rebuilding the same visual from scratch.

## Tables

Classify the content relationship rather than the current markup.

- Stable repeated row/column comparison: use a semantic table.
- Chronological sequence: use a process list or sequence visual.
- Causal mechanism: use a diagram or progressive explanation.
- Simple label/value facts without cross-row comparison: a definition list may
  be sufficient.

The current book table default is the selected restrained framed matrix:

- clear outer frame;
- caption or title band;
- explicit column headers;
- full cell grid;
- emphasized row headers or first column;
- semantic `caption`, `thead`, `th`, and `scope` attributes.

At narrow widths, preserve the matrix in a focusable horizontal-scroll region.
Do not convert it into cards or records that obscure column relationships. Keep
the page itself free of horizontal overflow and make focus visible.

## Callouts and interaction

Use a small semantic callout vocabulary such as:

- Key idea;
- Important distinction;
- Try it yourself;
- Caveat.

Do not build dashboard cards or promotional panels. Use progressive enhancement:
required content remains usable without JavaScript, keyboard behavior is
supported, ARIA relationships are correct, and interaction does not hide the
chapter's only explanation.

## Visual validation

Check:

- teaching job and placement;
- desktop and approximately 390px rendering;
- text and label legibility;
- page and component overflow;
- keyboard focus and controls;
- alt text, caption, and accessible fallback;
- reduced-motion and no-JavaScript behavior;
- local asset loading and console errors;
- source attribution and provenance;
- whether the completed visual should replace the placeholder.
