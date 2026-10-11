"""Rebuild the prev/next links at the bottom of every sheet from file order.

Order within a grade: Sharpen a1, a2, ..., then Around the corner b1, b2, ...,
then Connections c1, c2, ... (numeric order). Run after adding or renaming a
sheet:  python3 tools/relink.py  (add --check to only report differences).
"""
import glob, html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAV = re.compile(r'<div class="sheet-nav">.*?</div>', re.S)


def key(path):
    m = re.match(r'([abc])(\d+)-', os.path.basename(path))
    return ('abc'.index(m.group(1)), int(m.group(2)))


def title(path):
    t = open(path, encoding='utf-8').read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S)
    return re.sub(r'\s+', ' ', m.group(1)).strip()


def main():
    check = '--check' in sys.argv
    changed = 0
    for gdir in sorted(glob.glob(os.path.join(ROOT, 'grade-*'))):
        files = sorted(glob.glob(os.path.join(gdir, 'sheets', '[abc]*.html')), key=key)
        for i, f in enumerate(files):
            prev = ('<a href="%s">← Previous</a>' % os.path.basename(files[i - 1])) if i else '<a href="../index.html#sheets">← All sheets</a>'
            nxt = ('<a href="%s">Next: %s →</a>' % (os.path.basename(files[i + 1]), title(files[i + 1]))) if i + 1 < len(files) else '<a href="../index.html#sheets">← All sheets</a>'
            want = '<div class="sheet-nav">%s%s</div>' % (prev, nxt)
            t = open(f, encoding='utf-8').read()
            if not NAV.search(t):
                print('NO sheet-nav in', os.path.relpath(f, ROOT)); continue
            new = NAV.sub(lambda m: want, t, count=1)
            if new != t:
                changed += 1
                if check: print('would relink', os.path.relpath(f, ROOT))
                else: open(f, 'w', encoding='utf-8').write(new)
    print(('%d sheets need relinking' if check else '%d sheets relinked') % changed)
    if check and changed: sys.exit(1)


if __name__ == '__main__':
    main()
