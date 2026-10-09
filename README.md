# Infinity Club

Printable math sheets, one a night, organised by grade. Grade 6 (58 sheets) and grade 10 (57 sheets) are live, each in three tracks; other grades will follow. Shared interactive demos (43) live in `demos/`. Live at [infinityclub.net](https://infinityclub.net).

## Layout

- `index.html`: grade chooser.
- `grade-6/`, `grade-10/`: one folder per grade with `index.html` (the hub, all sheets by track), `plan.html` (first thirty nights and club card) and `sheets/`.
- `demos/index.html`: gallery of every demo; `demos/*.html` the demos themselves, shared across grades.
- `sheets/*.html` and `plan.html` are redirect stubs for the original URLs.

To add a grade, copy `grade-6/` to `grade-N/`, replace the sheets, update the kickers (`Infinity Club · Grade N · Track · n`), and turn that grade's card on `index.html` from `soon` to `live`.

Three tracks:

- **Sharpen** (`grade-6/sheets/a*.html`): grade 6 curriculum topics one notch harder, with the why.
- **Around the corner** (`grade-6/sheets/b*.html`): primes, binary, modular arithmetic, Pascal, Fibonacci, imaginary numbers, matrices, infinity, graphs, probability.
- **Connections** (`grade-6/sheets/c*.html`): music, astronomy, magic.

`demos/` holds standalone vanilla-JS pages.

## Structure

Plain static HTML, no build step. `.nojekyll` disables Jekyll on GitHub Pages. Shared styles in `assets/site.css` (screen and print), shared behaviour in `assets/site.js` (KaTeX auto-render, answers toggle, print button). Math is written as `\( ... \)` and rendered by KaTeX from cdnjs.

## Adding a sheet

Copy any sheet in `grade-6/sheets/`, keep the section structure (`idea`, `example`, `exercises`, `stretch`, `answers`), update the kicker, title, prev/next links, and add a card to that grade's `index.html` and `plan.html` club card. Answers are hidden on screen and always print on their own page. Use `<div class="space"></div>` (`short`, `tall` variants) for ruled writing room, which only appears in print.

## Local preview

    python3 -m http.server 8000

then open http://localhost:8000.

- `research.html`: a running, verified list of rigorous studies (RCTs, meta-analyses, natural experiments) on what works in maths teaching, with designs, effect sizes and DOIs. To add one, open an issue with the DOI; entries are checked against the original record before they go in.
