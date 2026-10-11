# Writing a sheet for Infinity Club

Infinity Club is free, printable math(s) for curious kids in grades 5 to 12 (ages 10 to 18). Each sheet is one evening: ten to fifteen minutes, one big idea, a worked example, four exercises, a starred stretch, and answers. This guide is written so that a person or an automated agent can turn a `new-sheet` issue into a pull request that can be merged without edits.

The most important rule: **everything on the sheet must be true.** Outside reviewers have found real errors on this site (missing conditions, reversed logic, wrong answers). A charming sheet with a false claim does harm. Verify every number and every claim before opening the PR.

## 1. Pick and claim an issue

Issues labelled `new-sheet` each describe one sheet: its file name, grade, track, the map sections it should plant, and a suggested way in.

1. Take the **lowest-numbered** open `new-sheet` issue that has no `in-progress` label and no open PR mentioning it.
2. Claim it immediately: add the `in-progress` label (or comment "Claimed" if you cannot label), so a parallel job skips it.
3. One issue per PR. Do not bundle.
4. If the issue's idea turns out to be wrong or unworkable, comment on the issue explaining why and stop. Do not force a false sheet.

## 2. Files you change

| File | What to do |
|---|---|
| `grade-N/sheets/<file>.html` | The new sheet. Use exactly the file name given in the issue. |
| `grade-N/index.html` | Add one card at the **end** of the right track section (see below). |
| `tools/map/pages.json` | Add one entry for the new sheet (see section 6). |
| other sheets in `grade-N/sheets/` | Only the prev/next line, and only by running `python3 tools/relink.py`. |
| `map.html` | Only by running `python3 tools/map/build_map.py`. |

Do not edit `plan.html`, other sheets' content, `assets/`, or the demos (unless the issue explicitly asks for a demo).

## 3. Build the sheet

Copy a recent sheet from the **same grade and track** (for example `grade-8/sheets/b27-half-planes.html`) and replace the content. Keep the HTML skeleton exactly: head, nav, `<main class="paper">`, `header.sheet-head`, the five sections, `div.sheet-nav`, footer, and the three scripts at the bottom.

- `<title>`: `Sheet title · Infinity Club`.
- `<meta name="description">`: one or two plain sentences saying what the sheet does. Only promise what is on the sheet.
- Kicker: `Infinity Club · Grade N · Track · n`, where Track is `Sharpen` (a), `Around the corner` (b) or `Connections` (c), and n is the number in the file name.
- `<h1>`: a short, curious title, often a question.
- `p.teaser`: one or two sentences, the hook. The hub card uses the same text.

The five sections, in order:

1. **`section.idea`** ("Tonight's idea"): at most about 180 words. Start from something concrete, then name the idea. One `p.callout` with the key fact is typical.
2. **`section.example`** ("Watch one: ..."): one fully worked example.
3. **`section.exercises`** ("Your turn"): an `<ol>` with **exactly 4** items (grade 6 may have up to 6). Each `<li>` ends with writing room: `<div class="space short"></div>`, `<div class="space"></div>` or `<div class="space tall"></div>`. Build up from a direct check to something that needs thought.
4. **`section.stretch`** ("Stretch: ..."): one harder question, then `<div class="space"></div>`.
5. **`section.answers`** ("Answers"): an `<ol>` with one answer per exercise, in order, then `<p><b>Stretch.</b> ...</p>`. Answers explain, not just state.

The page must print on **3 pages** (answers on their own page). Four is acceptable when a figure needs the room. Check with `python3 tools/pagecount.py grade-N/sheets/<file>.html`.

### Writing style

- Short, plain sentences. Talk to the kid ("you"). No exclamation marks. No em-dashes.
- Write **math(s)**, never "maths". The audience is **curious kids**, never "bright" or "gifted" children.
- Be honest about scope: if a rule has exceptions, say so; if something is a model or an idealisation, say so; if a result is an open problem, say so.
- History and real-world facts must be right (dates, names, numbers). If unsure, leave it out.

### Maths markup

- Inline maths `\( ... \)`, display `\[ ... \]`, rendered by KaTeX.
- Inside maths write `\lt` and `\gt` instead of bare `<` and `>`. Escape a dollar sign as `\$`.
- No HTML tags inside maths.

### Figures

Inline SVG inside `<figure>`, with a `<figcaption>` if useful.

- `viewBox` no larger than about 520 × 200; set `width`/`height` attributes.
- `font-family="Nunito, sans-serif"`, font sizes 11 to 15.
- Colours: ink `#1d1f3a`, blue `#3f44c9`, orange `#f5a524`, light fills `#dcdcf5` / `#fde8c4`, grey `#555`/`#999`.
- `role="img"` and an `aria-label` that describes the picture accurately.
- Compute coordinates with a script. Every label in the figure must match the text, and nothing may spill outside the viewBox.

## 4. The hub card

In `grade-N/index.html`, inside the right track's `<div class="cards">`, add at the end:

```html
  <a class="card" href="sheets/b28-example.html"><div class="num">Corner 28</div><h3>Sheet title</h3><p>Teaser text, same as the sheet.</p></a>
```

The label is `Sharpen n`, `Corner n` or `Connections n`. Grade 6 cards use a shorter one-line description instead of the full teaser; follow the neighbouring cards.

## 5. Check the maths, line by line

Before opening the PR, go through this list and fix anything that fails.

- **Recompute every number**: worked example, every answer, every figure label. Use a script for anything non-trivial and say in the PR what you computed.
- **Answers match the exercises as worded**, in the same order and count.
- **Conditions**: every rule states what it needs (nonzero, positive, prime, distinct, not vertical, in lowest terms, x > 0, ...). Try the edge cases 0, 1, negative, equal values, n = 1, n = 2.
- **Direction of logic**: "if" versus "only if", divides versus is divisible by, converse versus theorem.
- **No overclaims**: "always", "never", "the only", "best possible", "every" must be true as stated. Rules of thumb are labelled as such.
- **Text, figure and caption agree.**
- Try to break each claim with a counterexample. If you find one, fix the claim.

## 6. Add the sheet to the map

`map.html` shows how the site covers the 534 sections of the Mathematics Subject Classification. Add your sheet to `tools/map/pages.json`:

```json
  "grade-8/sheets/b28-example.html": [{"code": "20N", "level": "core"}, {"code": "05B", "level": "touch"}],
```

Use the codes listed in the issue (codes are the first three characters, like `20N`; all codes are in `tools/map/sections.json`). `core` means the sheet is mostly about that section; `touch` means it genuinely uses the idea in an exercise or the stretch. Be honest rather than generous.

## 7. Run the checks

```sh
python3 tools/relink.py                 # fix prev/next links in the grade
python3 tools/map/build_map.py          # rebuild map.html
(cd tools && npm install)               # once, for KaTeX
node tools/check_math.js                # KaTeX, exercise/answer counts, tags, style
python3 tools/check_site.py             # links, structure, kicker, hub card
python3 tools/pagecount.py grade-N/sheets/<file>.html
```

All must pass. The same checks run on every pull request.

## 8. Open the pull request

- Title: `New sheet: <h1 title> (grade N)`.
- Body: `Closes #<issue>`, the map sections planted, a short summary of the sheet, and a **Verification** section listing what you computed or checked (for example "brute-forced all 24 arrangements in Python; answers 1 to 4 match").
- One sheet per PR. Keep the diff to the files in section 2.

## Local preview

```sh
python3 -m http.server 8000
```

then open http://localhost:8000.
