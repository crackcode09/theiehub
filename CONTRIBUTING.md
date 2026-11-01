# Contributing

Improvements are welcome: corrections, clearer explanations, new exercises, real (anonymized) datasets, translations.

## Rules

1. **Every number must be reproducible.** If you change a dataset or worked example, rerun that course's `tools/make_data.py`, `tools/make_figures.py` and its analysis script (`tools/spc.py`, `tools/htest.py`, …), and update the module text and `solutions/README.md` to match.
2. **Cite primary sources** for any non-obvious claim. Each course keeps a `reference/sources.md` table (columns: ID, Source, Used for, Cited in, Verified) and modules cite an entry by its ID, for example `(montgomery-8e, ch. 6)`. A reviewer flips Verified to `yes` after checking the edition and the use; the site lists every table on its Sources page. Where authorities disagree (e.g., transforming data before charting), present both positions.
3. **Original content only.** Don't paste text, figures or exercises from copyrighted courses or books. In particular, nothing from IISE course material: we use only the public catalog's course titles and topic lists as a map of what to cover (see [NOTICE.md](NOTICE.md)). No official MODAPTS or MTM data cards, no standards text; use a simplified teaching version and say so.
4. **Plain language.** Write for someone on the shop floor with no statistics background; put the math in tables.
5. **Each module keeps the same structure:** objectives → concept → worked example → exercise → check yourself.
6. **Every course starts as `draft`.** The status cell in the catalog tables stays `draft` until a reviewer who did not write the course completes [REVIEW.md](REVIEW.md) and changes it to `verified (Name, YYYY-MM-DD)` in a `review:` pull request. Nothing is distributed as final before that.

## Layout

Courses live under `courses/<category>/<course>/`. The categories mirror the IISE course catalog (Lean & Six Sigma, Quality & Operational Excellence, Work Design & Work Measurement, …), plus categories added for subjects the catalog does not cover (Operations Research & Decision Analysis); each category folder has a README listing its courses. A new course goes in the category that fits and gets a row in both that README and the root README.

## Course README

The text under a course title follows one shape, so every overview reads the same way:

1. **One sentence of promise**, in plain words, saying what the reader will be able to do. It is the first line after the title and becomes the course's description in the catalog.
2. **Three fact lines**, each `**Label:** value` on its own line: `Length`, `Prerequisites` (the word `none`, or links to the courses required), `Roles` (O*NET codes the course maps to). The site renders them as a facts row and reads the prerequisites from this line.
3. `## What you will be able to do`: four to six outcomes, each starting with a verb.
4. The rest of the overview (running case and datasets, sessions table, related courses, getting started, folder map).
5. `## About this course`: the originality statement (what public titles or outlines were used as a map, and that everything else is original) just before `## License`.

No topic bullet list under the title: the sessions table already lists the topics.

## Site templates

One footer: every page's footer comes from `footer_html()` in `tools/roadmap_graph.py`, placed with `__FOOTER__` in each template; edit it there, never in a page. The hub's pillars and their status (`live`, `soon`, `planned`) are in `tools/hub.json`; a pillar becomes a footer link only when it is `live`. The site roadmap (`public/roadmap.html`) is built from the same file: its phases, their status, the goal and the recent updates. When a phase moves, change its `status` and add a line to `updates` (only what visitors notice; no hosting or repository details), and bump `updated`.

One width per column: inside the reader document, the catalog page and the legal pages, prose, tables, code and figures share the same right edge. Set the width once on the column (`.doc`, `.page`, `main`) and never on the text inside it; `python tools/roadmap_graph.py` refuses to build if a rule narrows content inside a column.

## Workflow

Fork → branch → pull request into `dev`. Run any checks the course ships (e.g. `python tools/check_constants.py` in Charting Process Behavior) before submitting changes to its tools.

The **Checks** workflow (`.github/workflows/checks.yml`) runs on every pull request: it rebuilds the site with `python tools/roadmap_graph.py` and fails if `public/` or `ROADMAP.md` would change (so commit the rebuild with your template or README edits), and it runs the course checks listed there.

### Branches

```text
main   what is published at theiehub.com (Cloudflare Pages builds from it)
  └── dev   where every change lands first, by pull request (Cloudflare builds a private preview at dev.theiehub.com)
        └── <type>/<short-name>   one branch per change, from dev (feat/, fix/, docs/, style/, perf/, review/)
```

- Open every pull request against `dev`, one independent change per branch. Branches are deleted automatically when merged.
- A release is a pull request from `dev` to `main`, merged with a merge commit so `dev` stays an ancestor of `main`.
- Before merging a release, check the `dev` preview (private: it sits behind Cloudflare Access and only the maintainer can open it): the home page, the catalog at `/learn`, a course with a figure, the mind map, the roadmap and the privacy page. Only `main` and `dev` get Cloudflare builds; feature branches do not.
- `main` and `dev` are protected: no direct pushes, no force pushes, no deletion, and every change arrives by pull request. The rules apply to maintainers too.
