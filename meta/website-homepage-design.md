# Study Group Website: Homepage Content Design

Status: proposed for review before visual or production implementation.

## Purpose

The homepage is a stable, practical entry point for the Search Agent Study
Group. It should help a prospective or returning participant answer four
questions quickly:

1. What is this group and when does it meet?
2. Where are the shared materials and community spaces?
3. What are we studying now, and how do I open a week?
4. Is there any optional work to do between meetings?

It is not a course landing page, a promotional page, or a summary of the
week's intellectual content. The weekly pages hold the substantive material.

## Homepage structure

The page uses one reading column with ordinary document flow. Sections appear
in this order.

### 1. Header and short introduction

- Group name: `Search Agent Study Group`.
- A one- or two-sentence description of the group and its purpose.
- A compact navigation row: `Home`, `Weeks`, and external links when useful.
- No hero treatment, taglines, feature panels, or introductory animation.

### 2. Logistics

This is the practical participation information section. It contains only
information someone needs to participate:

- meeting cadence, day, time, and time zone;
- location or video-call link;
- who the group is for / expected level of background;
- a short description of how a typical meeting works, only if useful;
- how to join or get in touch.

Use a compact definition list or two-column facts list, not cards. Unknown
details should be visibly marked as `TBD` during the initial build rather than
invented.

### 3. Shared resources

This section is a small directory for ongoing, group-level resources:

- Notion workspace or resource hub;
- GitHub repository;
- shared notes, chat/community space, or calendar if those exist;
- an optional one-line explanation for each destination.

These links should not be repeated as large calls to action. The goal is to
make the ecosystem findable, not to compete with the weekly schedule.

### 4. Weekly schedule

The schedule is the central working index of the site. It is a standard table,
not a set of cards. Each row represents one study-group meeting and links to
its own week page.

Suggested columns:

| Week | Date | Topic / focus | Material | Assignment |
| --- | --- | --- | --- | --- |
| `Week 0` | Jul 7, 2026 | [title] | short source label or `TBA` | short status or `—` |

Guidelines:

- Show the current or next meeting first, then earlier meetings in reverse
  chronological order, unless the group later adopts a fixed syllabus-like
  progression.
- Put the linked week label first (for example, `Week 0`) and use it as the
  page title. Keep row descriptions brief. A week page, not the homepage,
  explains the reading plan, discussion plan, and any related task.
- Mark future entries as `Planned` or `TBA`; do not imply material has been
  selected before it has.
- Keep completed weeks in the table as a lightweight archive rather than
  splitting the homepage into an additional archive section at first.

### 5. Assignments

Place this at the bottom and keep it deliberately low-key. Its purpose is to
make any current work visible without overwhelming the main index.

Initial content:

- a compact table or list with the relevant week, a one-line task description,
  and an optional deadline or status;
- a link to the relevant week page for the full prompt;
- an explicit empty state when no assignments have been posted yet.

The full prompt lives on its week page. If the group later develops recurring,
cross-week work, this can become a dedicated `/work/` page.

## Content ownership

| Information | Canonical home | Homepage representation |
| --- | --- | --- |
| Meeting logistics | Homepage | Full, concise facts list |
| Resource links | Homepage | Full, concise directory |
| Week title, date, source | Week page + schedule | One table row |
| Reading plan and discussion plan | Week page | Link only |
| Assignment | Week page | One-line status and link |
| Slides and notes | Week page | Link only |

## Week page boundary

Each week gets an ordinary, readable page with:

1. date, title, and a short framing note;
2. selected materials and resource links;
3. coverage or discussion plan;
4. assignment, when relevant;
5. links to notes, slides, or recordings when available.

The homepage should never try to reproduce this detail. That separation keeps
the index calm even as the group accumulates material.

## Editorial and visual guardrails

- Describe it consistently as a **study group**, never as a course.
- Use calm, conventional document layout: a modest title, horizontal rules,
  headings, paragraphs, a facts list, and a table.
- Keep the primary reading column compact (around 700--760px on desktop); do
  not make every section fill a viewport.
- Avoid sections whose only job is atmosphere: hero banners, cards, marketing
  copy, value propositions, feature grids, decorative illustrations, and
  animation.
- Make the schedule easy to scan on a phone; a responsive table may become
  stacked rows, but its information hierarchy must remain tabular.
- Keep the visual system restrained but not bare: a very light neutral
  background, dark blue-gray text, one muted blue link/accent color, a clean
  system sans-serif, and compact ordinary reading spacing. Keep the logistics
  facts visually grouped without individual row dividers. Compactness should
  come from vertical rhythm, not from cramped table columns or undersized text.

## Initial build data needed from the organizers

Before implementation, fill the following rather than guessing:

- meeting cadence, time zone, and venue/video link;
- participation/contact route;
- Notion/resource-hub URL and any other permanent links;
- the title and source label for each known week;
- whether the current Week 0 should appear as `Week 0`, `Kickoff`, or another
  label;
- whether optional follow-up should be present from day one or introduced only
  when a week actually has one.

## Proposed first implementation scope

Build only the homepage and a reusable week-page template after this content
design is approved. Populate the schedule from existing, user-provided weekly
material; preserve the existing Week 0 slide deck at its current URL. Do not
invent a curriculum, resource list, or assignments.
