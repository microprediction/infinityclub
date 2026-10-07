# Infinity Club

Printable math sheets, one a night, for bright kids around grade 6, plus a few interactive demos. Live at [infinityclub.net](https://infinityclub.net).

Three tracks:

- **Sharpen** (`sheets/a*.html`): grade 6 curriculum topics one notch harder, with the why.
- **Around the corner** (`sheets/b*.html`): primes, binary, modular arithmetic, Pascal, Fibonacci, imaginary numbers, matrices, infinity, graphs, probability.
- **Connections** (`sheets/c*.html`): music, astronomy, magic.

`demos/` holds standalone vanilla-JS pages.

## Structure

Plain static HTML, no build step. `.nojekyll` disables Jekyll on GitHub Pages. Shared styles in `assets/site.css` (screen and print), shared behaviour in `assets/site.js` (KaTeX auto-render, answers toggle, print button). Math is written as `\( ... \)` and rendered by KaTeX from cdnjs.

## Adding a sheet

Copy any sheet in `sheets/`, keep the section structure (`idea`, `example`, `exercises`, `stretch`, `answers`), update the kicker, title, prev/next links, and add a card to `index.html`. Answers are hidden on screen and always print on their own page. Use `<div class="space"></div>` (`short`, `tall` variants) for ruled writing room, which only appears in print.

## Local preview

    python3 -m http.server 8000

then open http://localhost:8000.
