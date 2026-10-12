# Math Detours

*The more you see, the less you have to remember.*

Printable math sheets, one a night, organised by grade. Grade 5 (48 sheets), grade 6 (76 sheets), grade 7 (65 sheets), grade 8 (79 sheets), grade 9 (63 sheets), grade 10 (74 sheets), grade 11 (58 sheets) and grade 12 (67 sheets) are live, each in three tracks. Shared interactive demos (100) live in `demos/`. Live at [mathdetours.com](https://mathdetours.com).

## Layout

- `index.html`: grade chooser.
- `grade-5/`, `grade-6/`, `grade-7/`, `grade-8/`, `grade-9/`, `grade-10/`, `grade-11/`, `grade-12/`: one folder per grade with `index.html` (the hub, all sheets by track), `plan.html` (first thirty nights and tick-off card) and `sheets/`.
- `map.html`: the map of mathematics (built from `tools/map/`).
- `demos/index.html`: gallery of every demo; `demos/*.html` the demos themselves, shared across grades.
- `sheets/*.html` and `plan.html` are redirect stubs for the original URLs.

To add a grade, write a spec table (file, title, teaser) for its three tracks, copy a recent grade folder to `grade-N/`, replace the sheets, update the kickers (`Math Detours · Grade N · Track · n`), and turn that grade's card on `index.html` from `soon` to `live`.

Three tracks in every grade:

- **Sharpen** (`grade-N/sheets/a*.html`): that year's school course, with the why.
- **Around the corner** (`grade-N/sheets/b*.html`): ideas usually met later or never.
- **Connections** (`grade-N/sheets/c*.html`): where the math shows up in the world.

Sheets are ten to fifteen minutes: a short idea, one worked example, four exercises (grade 6 has up to six), a stretch, and answers on their own printed page. Grades 1 to 4 are on hold.

`demos/` holds standalone vanilla-JS pages.

## Structure

Plain static HTML, no build step. `.nojekyll` disables Jekyll on GitHub Pages. Shared styles in `assets/site.css` (screen and print), shared behaviour in `assets/site.js` (KaTeX auto-render, answers toggle, print button). Math is written as `\( ... \)` and rendered by KaTeX from cdnjs.

## Adding a sheet

See [CONTRIBUTING.md](CONTRIBUTING.md): the full sheet spec, the accuracy checklist, and how to claim a `new-sheet` issue. In short: copy a sheet from the same grade and track, keep the section structure (`idea`, `example`, `exercises`, `stretch`, `answers`), add a card to that grade's `index.html`, add the sheet to `tools/map/pages.json`, then run `python3 tools/relink.py` and `python3 tools/map/build_map.py`.

## Tools and checks

- `tools/relink.py`: rebuilds every sheet's prev/next links from file order.
- `tools/check_site.py`: links, anchors, sheet structure, kickers, hub cards, inline JS syntax.
- `tools/check_math.js`: KaTeX errors, exercise/answer counts, tag balance, house style (`cd tools && npm install` first).
- `tools/pagecount.py`: printed page count via headless Chrome (3 expected, 4 allowed).
- `tools/map/`: data and builder for `map.html`, the map of all 534 MSC2020 sections against the site.

The same checks run on every pull request (`.github/workflows/checks.yml`).

## Local preview

    python3 -m http.server 8000

then open http://localhost:8000.

- `research.html`: a running, verified list of rigorous studies (RCTs, meta-analyses, natural experiments) on what works in math(s) teaching, with designs, effect sizes and DOIs. To add one, open an issue with the DOI; entries are checked against the original record before they go in.
