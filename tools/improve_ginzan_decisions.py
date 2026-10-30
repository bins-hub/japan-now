"""Replace generic Ginzan editorial content, preserving the optimized image and search head."""
from pathlib import Path
from html import escape
import re,json
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'content/ginzan-decision-guide.json').read_text())
def p(s):return '<p>'+escape(s)+'</p>'
def link(u,t):return '<a href="'+escape(u,quote=True)+'" target="_blank" rel="noopener noreferrer">'+escape(t)+'</a>'
changed=[]
for lang,c in d['locales'].items():
 prefix='' if lang=='ko' else lang+'/'
 file=ROOT/prefix/'onsen/ginzan/index.html';h=file.read_text();old=h
 title=c['heads'];table='<div class="jp-decision-scroll" tabindex="0" role="region" aria-label="'+escape(title[1],quote=True)+'"><table class="jp-decision-table"><thead><tr>'+''.join('<th scope="col">'+escape(x)+'</th>' for x in c['cols'])+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+escape(row[0])+'</th>'+''.join('<td>'+escape(x)+'</td>' for x in row[1:])+'</tr>' for row in c['rows'])+'</tbody></table></div>'
 bodies=[p(c['intro']),table,p(c['bus'])+p(c['itinerary'])+p(c['period'])+link('https://www.google.com/maps/dir/?api=1&origin=Oishida+Station&destination=Shirogane-yu+Ginzan&travelmode=transit','Google Maps'),p(c['parking'])+p(c['winter']),''.join('<h3>'+escape(q)+'</h3>'+p(a) for q,a in c['faq']),'<p>2026-10-30</p><ul>'+''.join('<li>'+link(u,t)+'</li>' for u,t in d['sources'])+'</ul>']
 body=''.join('<section class="panel"'+(' id="verified-ginzan"' if t==title[1] else '')+'><h2>'+escape(t)+'</h2>'+b+'</section>' for t,b in zip(title,bodies))
 # Only the original main editorial area after the facts; photo/attribution stays intact.
 start=h.index('<!--ginzan-decisions-->') if '<!--ginzan-decisions-->' in h else h.index('<h2>',h.index('<main'))
 end=h.index('</main>',start);h=h[:start]+'<!--ginzan-decisions-->'+body+h[end:]
 css='<link rel="stylesheet" href="/assets/decision-guides.css?v=20261030">'
 if css not in h:h=h.replace('</head>',css+'</head>')
 if h!=old:file.write_text(h);changed.append(str(file.relative_to(ROOT)))
print(json.dumps({'changed':changed},ensure_ascii=False))
