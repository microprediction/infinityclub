"""Site checks: broken links and anchors, sheet structure, hub cards, inline JS syntax.

    python3 tools/check_site.py      (exit code 1 if anything is wrong)
"""
import glob, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
problems = []
html = sorted(glob.glob('*.html') + glob.glob('grade-*/*.html') + glob.glob('grade-*/sheets/*.html') + glob.glob('demos/*.html'))
ids = {f: set(re.findall(r'id="([^"]+)"', open(f, encoding='utf-8').read())) for f in html}
nlinks = 0
for f in html:
    s = open(f, encoding='utf-8').read()
    for href in re.findall(r'href="([^"]+)"', s):
        if href.startswith(('http', 'mailto')):
            continue
        path, _, frag = href.partition('#')
        if path.startswith('/'):
            target = os.path.normpath(path.lstrip('/') or 'index.html')
        else:
            target = os.path.normpath(os.path.join(os.path.dirname(f), path)) if path else f
        nlinks += 1
        if not os.path.exists(target):
            problems.append('MISSING link %s -> %s' % (f, href)); continue
        if frag and target in ids and frag not in ids[target]:
            problems.append('NO ANCHOR %s -> %s' % (f, href))
NEED = ['class="sheet-head"', 'section class="idea"', 'section class="example"', 'section class="exercises"',
        'section class="stretch"', 'section class="answers"', 'class="sheet-nav"', 'katex', 'site.js', 'class="kicker"']
TRACK = {'a': 'Sharpen', 'b': 'Around the corner', 'c': 'Connections'}
for f in sorted(glob.glob('grade-*/sheets/*.html')):
    s = open(f, encoding='utf-8').read()
    miss = [n for n in NEED if n not in s]
    if miss:
        problems.append('STRUCTURE %s missing %s' % (f, miss))
    m = re.match(r'grade-(\d+)/sheets/([abc])(\d+)-', f)
    k = re.search(r'<div class="kicker">(.*?)</div>', s)
    want = 'Infinity Club · Grade %s · %s · %s' % (m.group(1), TRACK[m.group(2)], m.group(3))
    if k and k.group(1).strip() != want:
        problems.append('KICKER %s says "%s", expected "%s"' % (f, k.group(1).strip(), want))
    hub = open('grade-%s/index.html' % m.group(1), encoding='utf-8').read()
    if 'href="sheets/%s"' % os.path.basename(f) not in hub:
        problems.append('NO HUB CARD for %s in grade-%s/index.html' % (f, m.group(1)))
tmpdir = tempfile.mkdtemp()  # private, so parallel runs cannot overwrite each other's files
for f in html:
    s = open(f, encoding='utf-8').read()
    for i, js in enumerate(re.findall(r'<script>(.*?)</script>', s, re.S)):
        p = os.path.join(tmpdir, '_ic_chk_%d.js' % i)
        open(p, 'w').write(js)
        r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
        if r.returncode:
            problems.append('JS SYNTAX %s: %s' % (f, r.stderr.strip().splitlines()[-1] if r.stderr.strip() else '?'))
print('\n'.join(problems))
print('links %d, sheets %d, demos %d, problems %d' % (nlinks, len(glob.glob('grade-*/sheets/*.html')), len(glob.glob('demos/*.html')), len(problems)))
sys.exit(1 if problems else 0)
