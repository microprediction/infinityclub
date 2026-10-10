# Infinity Club

Printable math sheets, one a night, organised by grade. Grade 5 (48 sheets), grade 6 (61 sheets), grade 7 (48 sheets), grade 8 (56 sheets), grade 9 (48 sheets), grade 10 (59 sheets), grade 11 (48 sheets) and grade 12 (58 sheets) are live, each in three tracks. Shared interactive demos (100) live in `demos/`. Live at [infinityclub.net](https://infinityclub.net).

## Layout

- `index.html`: grade chooser.
- `grade-5/`, `grade-6/`, `grade-7/`, `grade-8/`, `grade-9/`, `grade-10/`, `grade-11/`, `grade-12/`: one folder per grade with `index.html` (the hub, all sheets by track), `plan.html` (first thirty nights and club card) and `sheets/`.
- `demos/index.html`: gallery of every demo; `demos/*.html` the demos themselves, shared across grades.
- `sheets/*.html` and `plan.html` are redirect stubs for the original URLs.

To add a grade, write a spec table (file, title, teaser) for its three tracks, copy a recent grade folder to `grade-N/`, replace the sheets, update the kickers (`Infinity Club · Grade N · Track · n`), and turn that grade's card on `index.html` from `soon` to `live`.

Three tracks in every grade:

- **Sharpen** (`grade-N/sheets/a*.html`): that year's school course, with the why.
- **Around the corner** (`grade-N/sheets/b*.html`): ideas usually met later or never.
- **Connections** (`grade-N/sheets/c*.html`): where the math shows up in the world.

Sheets are ten to fifteen minutes: a short idea, one worked example, four exercises (grade 6 has up to six), a stretch, and answers on their own printed page. Grades 1 to 4 are on hold.

`demos/` holds standalone vanilla-JS pages.

## Structure

Plain static HTML, no build step. `.nojekyll` disables Jekyll on GitHub Pages. Shared styles in `assets/site.css` (screen and print), shared behaviour in `assets/site.js` (KaTeX auto-render, answers toggle, print button). Math is written as `\( ... \)` and rendered by KaTeX from cdnjs.

## Adding a sheet

Copy any sheet in the same grade's `sheets/` folder, keep the section structure (`idea`, `example`, `exercises`, `stretch`, `answers`), update the kicker, title, prev/next links, and add a card to that grade's `index.html` and `plan.html` club card. Answers are hidden on screen and always print on their own page. Use `<div class="space"></div>` (`short`, `tall` variants) for ruled writing room, which only appears in print.

## Local preview

    python3 -m http.server 8000

then open http://localhost:8000.

- `research.html`: a running, verified list of rigorous studies (RCTs, meta-analyses, natural experiments) on what works in math(s) teaching, with designs, effect sizes and DOIs. To add one, open an issue with the DOI; entries are checked against the original record before they go in.
