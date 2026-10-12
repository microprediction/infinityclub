"""Build map.html from tools/map/*.json.

    python3 tools/map/build_map.py          rebuild map.html
    python3 tools/map/build_map.py --check  fail if a sheet/demo is missing from pages.json,
                                            a code is unknown, or map.html is out of date

Data:
  sections.json  the 63 MSC2020 areas and 534 sections (codes like "11A")
  ideas.json     per section: key idea, elementary way in, lowest grade, fit
  pages.json     per sheet or demo: list of {"code": "11A", "level": "core"|"touch"}
                 core = the page is mostly about this section; touch = it uses the idea
"""
import json, re, collections, html, glob, os, sys
D = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(os.path.dirname(D))
areas_j = json.load(open(os.path.join(D, 'sections.json'), encoding='utf-8'))
ideas = json.load(open(os.path.join(D, 'ideas.json'), encoding='utf-8'))
cls = json.load(open(os.path.join(D, 'pages.json'), encoding='utf-8'))
areas = [[a['code'], a['name'], [(s['code'], s['name']) for s in a['sections']]] for a in areas_j]
known = {s['code'] for a in areas_j for s in a['sections']}
problems = []
pagefiles = sorted(glob.glob(os.path.join(R, 'grade-*/sheets/*.html')) + [f for f in glob.glob(os.path.join(R, 'demos/*.html')) if not f.endswith('index.html')])
rel = [os.path.relpath(f, R) for f in pagefiles]
for p in rel:
    if p not in cls: problems.append('pages.json has no entry for ' + p)
for p, L in cls.items():
    if p not in rel: problems.append('pages.json lists a page that does not exist: ' + p)
    for e in L:
        if e.get('code') not in known: problems.append('unknown code %r for %s' % (e.get('code'), p))
        if e.get('level') not in ('core', 'touch'): problems.append('bad level %r for %s' % (e.get('level'), p))
def page_title(p):
    t = open(os.path.join(R, p), encoding='utf-8').read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S) or re.search(r'<title>(.*?)(?: · Math Detours)?</title>', t, re.S)
    return re.sub(r'<[^>]+>', '', html.unescape(re.sub(r'\s+', ' ', m.group(1)))).strip()
items = {p: {'title': page_title(p)} for p in cls if p in rel}
cls = {p: L for p, L in cls.items() if p in rel}
core=collections.defaultdict(list); touch=collections.defaultdict(list)
for p,L in cls.items():
    for e in L: (core if e['level']=='core' else touch)[e['code']].append(p)
E=html.escape
def label(p):
    it=items[p]; t=it['title']
    m=re.match(r'grade-(\d+)/',p)
    return (f'G{m.group(1)}' if m else 'Demo'), t
def sortkey(p):
    m=re.match(r'grade-(\d+)/',p); return (0,int(m.group(1)),p) if m else (1,0,p)
def links(ps,cls_):
    out=[]
    for p in sorted(set(ps),key=sortkey):
        g,t=label(p); out.append(f'<a class="pg {cls_}" href="{E(p)}"><span class="g">{g}</span> {E(t)}</a>')
    return ''.join(out)
FIT={'natural':'Natural fit','stretch':'Stretch','hard':'Hard','n/a':''}
secs=[s for a in areas for s in a[2]]
ncore=sum(1 for c,_ in secs if core[c]); ntouch=sum(1 for c,_ in secs if not core[c] and touch[c])
nareas=sum(1 for a in areas if any(core[c] or touch[c] for c,_ in a[2]))
gapnat=sum(1 for c,_ in secs if not core[c] and not touch[c] and ideas[c]['fit']=='natural')
body=[]
for code,name,ss in areas:
    n=len(ss); k=sum(1 for c,_ in ss if core[c] or touch[c])
    rows=[]
    for c,nm in ss:
        d=ideas[c]; st='core' if core[c] else ('touch' if touch[c] else 'none')
        fit=d['fit']
        mark={'core':'●','touch':'◐','none':'○'}[st]
        stt={'core':'Main idea of a sheet','touch':'Touched on','none':'Not yet'}[st]
        seeds=''
        if st!='none':
            allp=[(p,'c') for p in sorted(set(core[c]),key=sortkey)]+[(p,'t') for p in sorted(set(touch[c])-set(core[c]),key=sortkey)]
            first=''.join(links([p],k) for p,k in allp[:10]); rest=''.join(links([p],k) for p,k in allp[10:])
            more=f'<details class="more"><summary>{len(allp)-10} more</summary><div class="seeds">{rest}</div></details>' if rest else ''
            seeds=f'<div class="seeds">{first}</div>{more}'
        way=''
        if fit!='n/a' and d.get('entry'):
            g=d.get('grade'); gl=f'grade {g}' if g else ''
            way=f'<p class="way"><span class="fit {fit.replace("/","")}">{FIT[fit]}</span> <b>Way in{(" ("+gl+")") if gl else ""}:</b> {E(d["entry"])}</p>'
        rows.append(f'<div class="sec {st} f-{fit.replace("/","")}" id="{c}"><div class="hd"><span class="mk {st}" title="{stt}">{mark}</span> <span class="cd">{c}</span> <span class="nm">{E(nm)}</span></div><p class="idea">{E(d["idea"])}</p>{way}{seeds}</div>')
    pct=k/n
    body.append(f'<details class="fold area" id="a{code}"><summary><span class="cd">{code}</span> {E(name)} <span class="cnt">{k} of {n}</span><span class="bar"><i style="width:{pct*100:.0f}%"></i></span></summary>\n'+'\n'.join(rows)+'\n</details>')
page=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Map of Mathematics · Math Detours</title>
<meta name="description" content="All 534 sections of the Mathematics Subject Classification, the key idea of each in one sentence, an elementary way in, and the Math Detours sheets that already plant it.">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.11/katex.min.css">
<link rel="stylesheet" href="assets/site.css">
<style>
.stats {{ display:flex; flex-wrap:wrap; gap:.6rem; margin:1rem 0 1.2rem; }}
.stats div {{ border:1px solid var(--rule); border-radius:10px; padding:.5rem .8rem; flex:1 1 9rem; }}
.stats b {{ display:block; font-size:1.5rem; color:var(--accent); }}
.filters {{ display:flex; flex-wrap:wrap; gap:.4rem; margin:.4rem 0 1.2rem; }}
.filters button {{ font:inherit; font-weight:700; font-size:.9rem; border:2px solid var(--accent); background:transparent; color:var(--accent); border-radius:999px; padding:.2rem .8rem; cursor:pointer; }}
.filters button.on {{ background:var(--accent); color:#fff; }}
details.area > summary {{ display:flex; flex-wrap:wrap; align-items:center; gap:.2rem .5rem; color:var(--ink); border-top:1px solid var(--rule); padding:.55rem 0; list-style:none; }}
details.area > summary::-webkit-details-marker {{ display:none; }}
details.area > summary::before {{ content:"▸"; color:var(--accent); width:.8rem; }}
details.area[open] > summary::before {{ content:"▾"; }}
details.area {{ margin:0; }}
.area .cd {{ font-variant-numeric:tabular-nums; color:var(--muted); font-weight:800; min-width:1.6rem; }}
.area .cnt {{ margin-left:auto; color:var(--muted); font-size:.85rem; font-weight:700; white-space:nowrap; }}
.area .bar {{ width:4.5rem; height:.45rem; background:var(--accent-soft); border-radius:99px; overflow:hidden; }}
.area .bar i {{ display:block; height:100%; background:var(--accent); }}
.sec {{ border-left:3px solid var(--rule); padding:.35rem 0 .35rem .8rem; margin:.5rem 0 .5rem 1.2rem; }}
.sec.core {{ border-color:var(--accent); }}
.sec.touch {{ border-color:#9ea1e6; }}
.sec .hd {{ font-weight:700; }}
.sec .cd {{ color:var(--muted); font-size:.85rem; margin-right:.15rem; }}
.mk {{ color:var(--rule); }} .mk.core {{ color:var(--accent); }} .mk.touch {{ color:#7b7fdc; }}
.sec p {{ margin:.2rem 0; }}
.sec .idea {{ color:var(--ink); }}
.sec .way {{ font-size:.92rem; color:var(--muted); }}
.fit {{ display:inline-block; font-size:.72rem; font-weight:800; text-transform:uppercase; letter-spacing:.04em; border-radius:999px; padding:.05em .55em; background:#e4efe6; color:#2f6b3a; }}
.fit.stretch {{ background:#efe7d6; color:#7a5a1c; }}
.fit.hard {{ background:#f3e1e1; color:#8a3030; }}
.seeds {{ display:flex; flex-wrap:wrap; gap:.3rem; margin-top:.3rem; }}
.pg {{ font-size:.85rem; text-decoration:none; border:1px solid var(--rule); border-radius:8px; padding:.05rem .45rem; }}
.pg.c {{ background:var(--accent-soft); border-color:transparent; }}
.pg .g {{ font-weight:800; color:var(--muted); font-size:.75rem; }}
.hide {{ display:none; }}
details.more > summary {{ cursor:pointer; font-size:.85rem; font-weight:700; color:var(--accent); margin-top:.3rem; }}
@media (max-width:600px) {{ .sec {{ margin-left:.4rem; }} .area .bar {{ width:3rem; }} }}
@media print {{ .filters {{ display:none; }} .sec {{ break-inside:avoid; }} }}
</style>
</head>
<body>
<nav class="top">
  <a class="brand" href="index.html"><span class="inf">∞</span> Math Detours</a>
  <a href="index.html#grades">Grades</a>
  <a href="demos/index.html">Demos</a>
  <a href="parents.html">Parents</a>
  <a href="research.html">Research</a>
  <a href="map.html">Map</a>
</nav>

<main class="paper">
<h1>The map of mathematics</h1>
<p>Mathematicians sort their research into the <a href="https://msc2020.org/">Mathematics Subject Classification</a>: 63 areas, split into 534 sections. This page lists every section, says its key idea in one sentence, suggests an elementary way in for a curious kid, and links the sheets and demos where the idea is already planted.</p>
<p>The bet behind it: almost every part of mathematics has an intuitive example a 12-year-old can hold. Where we think that is hard, we say so.</p>
<div class="stats">
<div><b>{ncore+ntouch}</b> of 534 sections touched</div>
<div><b>{ncore}</b> are the main idea of a sheet or demo</div>
<div><b>{nareas}</b> of 63 areas reached</div>
<div><b>{gapnat}</b> gaps with a natural way in</div>
</div>
<details class="fold howto"><summary>How to read this page</summary>
<ul>
<li><b>● Main idea</b>: at least one sheet or demo is mostly about this section. <b>◐ Touched</b>: a sheet uses the idea in an exercise or stretch. <b>○ Not yet</b>: no sheet plants it yet.</li>
<li><b>Way in</b> is a suggested elementary entry point, with the lowest grade we think it works for. <span class="fit">Natural fit</span> means a normal sheet could do it. <span class="fit stretch">Stretch</span> means a glimpse, or real care. <span class="fit hard">Hard</span> means an honest elementary taste is difficult.</li>
<li>Shaded links are sheets where the section is the main idea; outlined links only touch it. G8 means grade 8.</li>
<li>Plain school arithmetic has no section of its own, so sheets on fractions, percentages and estimation mostly sit under 00A or 11A.</li>
<li>The sorting was done with AI help and checked by eye, so some calls are judgement. Corrections are welcome as <a href="https://github.com/microprediction/mathdetours/issues">GitHub issues</a>.</li>
</ul>
</details>
<div class="filters" role="group" aria-label="Filter sections">
<button data-f="all" class="on">All</button><button data-f="seeded">On the site</button><button data-f="gap">Not yet</button><button data-f="natural-gap">Easy gaps</button><button id="openall">Open all</button>
</div>
{chr(10).join(body)}
<p class="small" style="margin-top:1.5rem">Section names are from MSC2020 (msc2020.org, CC BY-NC-SA). Key ideas, ways in and the matching of sheets are ours.</p>
</main>
<footer>Math Detours · mathdetours.com · Print one sheet a night.</footer>
<script>
(function(){{
  var secs=[].slice.call(document.querySelectorAll('.sec')), areas=[].slice.call(document.querySelectorAll('details.area'));
  function apply(f){{
    secs.forEach(function(s){{
      var show = f==='all' || (f==='seeded' && !s.classList.contains('none')) || (f==='gap' && s.classList.contains('none')) || (f==='natural-gap' && s.classList.contains('none') && s.classList.contains('f-natural'));
      s.classList.toggle('hide',!show);
    }});
    areas.forEach(function(a){{ var any=a.querySelector('.sec:not(.hide)'); a.classList.toggle('hide',!any); if(f!=='all'&&any) a.open=true; }});
  }}
  document.querySelectorAll('.filters button[data-f]').forEach(function(b){{ b.addEventListener('click',function(){{
    document.querySelectorAll('.filters button[data-f]').forEach(function(x){{x.classList.remove('on');}}); b.classList.add('on'); apply(b.dataset.f); }}); }});
  var oa=document.getElementById('openall'); oa.addEventListener('click',function(){{ var open=oa.textContent==='Open all'; areas.forEach(function(a){{a.open=open;}}); oa.textContent=open?'Close all':'Open all'; }});
  function reveal(){{ var id=decodeURIComponent(location.hash.slice(1)); if(!id) return; var el=document.getElementById(id); if(!el) return; var d=el.closest('details'); if(d) d.open=true; if(el.tagName==='DETAILS') el.open=true; el.scrollIntoView(); }}
  window.addEventListener('hashchange',reveal); window.addEventListener('DOMContentLoaded',reveal);
  window.addEventListener('beforeprint',function(){{ areas.forEach(function(a){{a.open=true;}}); }});
}})();
</script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.11/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.11/contrib/auto-render.min.js"></script>
<script defer src="assets/site.js"></script>
</body>
</html>
'''
out = os.path.join(R, 'map.html')
if '--check' in sys.argv:
    if os.path.exists(out) and open(out, encoding='utf-8').read() != page:
        problems.append('map.html is out of date: run python3 tools/map/build_map.py')
    print('\n'.join(problems)); print('map check: %d problems' % len(problems)); sys.exit(1 if problems else 0)
open(out, 'w', encoding='utf-8').write(page)
print('map.html: %d of %d sections touched (%d main idea), %d areas, %d natural gaps' % (ncore + ntouch, len(secs), ncore, nareas, gapnat))
if problems: print('\n'.join(problems)); sys.exit(1)
