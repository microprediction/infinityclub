"""Rebuild sitemap.xml from the pages on disk.

    python3 tools/build_sitemap.py           (rewrite sitemap.xml)
    python3 tools/build_sitemap.py --check   (exit code 1 if it is out of date)

Pages whose title starts with "Moved" (old addresses that only redirect) are left out.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE = 'https://' + open('CNAME').read().strip() + '/'


def natural(f):
    return [int(p) if p.isdigit() else p for p in re.split(r'(\d+)', f)]


def moved(f):
    return bool(re.search(r'<title>\s*Moved', open(f, encoding='utf-8').read(2000)))


top = ['index.html'] + sorted(f for f in glob.glob('*.html') if f != 'index.html')
rest = sorted(glob.glob('demos/*.html') + glob.glob('grade-*/*.html') + glob.glob('grade-*/sheets/*.html'), key=natural)
pages = [f for f in top + rest if not moved(f)]
xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
       + ''.join('  <url><loc>%s%s</loc></url>\n' % (SITE, f) for f in pages) + '</urlset>\n')
if '--check' in sys.argv:
    ok = os.path.exists('sitemap.xml') and open('sitemap.xml', encoding='utf-8').read() == xml
    print('sitemap check: %s' % ('0 problems' if ok else 'out of date, run python3 tools/build_sitemap.py'))
    sys.exit(0 if ok else 1)
open('sitemap.xml', 'w', encoding='utf-8').write(xml)
print('sitemap.xml: %d pages' % len(pages))
