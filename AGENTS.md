# AGENTS.md

Instructions for AI coding agents working in this repository. Humans should read [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## What this is

Math Detours ([mathdetours.com](https://mathdetours.com)) is a free, static website of printable math(s) sheets for curious kids in grades 5 to 12, plus interactive demos. It is plain HTML, CSS and vanilla JS with no build step, served by GitHub Pages from `main`. Anything merged to `main` is live within minutes, so treat every merge as publishing.

```
grade-N/index.html          hub: one card per sheet, in three tracks
grade-N/plan.html           first thirty nights
grade-N/sheets/aK-*.html    Sharpen: that grade's course, with the why
grade-N/sheets/bK-*.html    Around the corner: new mathematics
grade-N/sheets/cK-*.html    Connections: where math(s) shows up in the world
demos/*.html                standalone interactive demos, shared across grades
map.html                    generated from tools/map/: all 534 MSC2020 sections vs the site
research.html               verified studies on how children learn math(s)
tools/                      checks and generators (see below)
```

## The one rule that matters most

**Everything on the site must be true.** It is read by children and their parents, and outside reviewers do find errors. Before you change or add any mathematical content:

- recompute every number (use a script for anything non-trivial);
- state every condition a claim needs (nonzero, positive, distinct, convex, in lowest terms, ...) and test edge cases (0, 1, negatives, equal values, n = 1, n = 2);
- check the direction of every implication and divisibility statement;
- make sure "always", "never", "every", "the only" and "best" are literally true;
- make the text, figure labels, aria-labels and answers agree.

If you cannot verify a claim, leave it out. If an issue asks for something false, say so on the issue instead of writing it.

## Common tasks

**A `new-sheet` issue.** Follow CONTRIBUTING.md exactly: claim the lowest-numbered unclaimed issue with the `in-progress` label, write one sheet at the exact path the issue gives, add its hub card and its `tools/map/pages.json` entry, regenerate, run the checks, and open one PR with `Closes #N` and a Verification section saying what you computed.

**An issue reporting an error.** Reproduce it first (compute it, or construct the counterexample). If the report is right, make the smallest edit that makes the page true, check the same claim on related sheets and demos, and close the issue from the PR. If the report is wrong, explain why on the issue.

**Editing a demo.** Keep it dependency-free vanilla JS. Every readout message must be true at every slider setting, including the extremes; test the pure functions at the boundaries. Confirm the script still parses.

## Generated files: never hand-edit

| File or part | Regenerate with |
|---|---|
| prev/next line at the bottom of every sheet | `python3 tools/relink.py` |
| `map.html` | `python3 tools/map/build_map.py` |
| `sitemap.xml` | `python3 tools/build_sitemap.py` |

## Checks (CI runs the same ones on every PR)

```sh
(cd tools && npm install)                  # once, installs KaTeX
node tools/check_math.js                   # KaTeX errors, exercise/answer counts, tags, house style
python3 tools/check_site.py                # links, anchors, structure, kickers, hub cards, JS syntax, old site name
python3 tools/relink.py --check
python3 tools/map/build_map.py --check
python3 tools/build_sitemap.py --check
python3 tools/pagecount.py grade-N/sheets/<file>.html   # 3 printed pages expected, 4 allowed
```

All must pass before you open a PR. Passing CI does not mean the maths is right; the checks only see structure.

## House style

- Write **math(s)**, never "maths". The audience is **curious kids**, never "bright" or "gifted" children.
- The site is **Math Detours**. Never use the old name, Infinity Club.
- Short, plain sentences, addressed to the reader. No exclamation marks. No em-dashes.
- Sheets: idea (at most about 180 words), one worked example, exactly 4 exercises (grade 6 allows up to 6), a stretch, and answers that match the exercises one for one. Kicker format: `Math Detours · Grade N · Track · K`.
- Maths in `\( \)` or `\[ \]`. Inside maths use `\lt` and `\gt`, and write a dollar sign as `\$`.
- Figures are inline SVG: at most about 520 × 200, `font-family="Nunito, sans-serif"`, site colours (`#1d1f3a`, `#3f44c9`, `#f5a524`), an accurate `aria-label`, and no labels spilling outside the viewBox.

## Scope and etiquette

- One issue per PR, with a minimal diff. Do not reformat files you did not need to touch.
- Do not edit `assets/`, `CNAME`, `.github/` or other sheets' content unless the task is about them.
- Do not add dependencies, frameworks, trackers, analytics or external scripts. The only CDN in use is cdnjs, for KaTeX.
- Keep everything free and open: no paywalls, sign-ups or ads.
- Unattended agents work on a branch and open a PR; do not push to `main` directly or force-push shared branches.
- PR title for a new sheet: `New sheet: <h1 title> (grade N)`.
