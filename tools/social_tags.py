"""Add link-preview tags (Open Graph, Twitter card) to every page, from its own title and description.

    python3 tools/social_tags.py           (rewrite the tags on every page)
    python3 tools/social_tags.py --check   (exit code 1 if any page is out of date)

The tags sit directly after the page's <meta name="description"> line. Never edit them by hand.
"""
import glob, html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE = 'https://' + open('CNAME').read().strip() + '/'
OLD = re.compile(r'^<meta (?:property="og:|name="twitter:)[^>]*>\n', re.M)
DESC = re.compile(r'^<meta name="description" content="(.*?)">\n', re.M)

pages = sorted(glob.glob('*.html') + glob.glob('grade-*/*.html') + glob.glob('grade-*/sheets/*.html') + glob.glob('demos/*.html'))
stale = []
for f in pages:
    s = open(f, encoding='utf-8').read()
    title = re.search(r'<title>(.*?)</title>', s, re.S)
    d = DESC.search(s)
    if not title or not d or title.group(1).strip().startswith('Moved'):
        continue
    esc = lambda t: html.escape(html.unescape(t.strip()), quote=True)
    block = ''.join('<meta %s content="%s">\n' % kv for kv in [
        ('property="og:type"', 'website'), ('property="og:site_name"', 'Math Detours'),
        ('property="og:title"', esc(title.group(1))), ('property="og:description"', esc(d.group(1))),
        ('property="og:url"', SITE + ('' if f == 'index.html' else f)),
        ('property="og:image"', SITE + 'assets/social.png'), ('name="twitter:card"', 'summary_large_image')])
    t = OLD.sub('', s)
    d = DESC.search(t)
    t = t[:d.end()] + block + t[d.end():]
    if t != s:
        stale.append(f)
        if '--check' not in sys.argv:
            open(f, 'w', encoding='utf-8').write(t)
if '--check' in sys.argv:
    print('\n'.join('STALE preview tags: ' + f for f in stale))
    print('social tags check: %d problems' % len(stale))
    sys.exit(1 if stale else 0)
print('social tags: %d pages updated, %d checked' % (len(stale), len(pages)))
