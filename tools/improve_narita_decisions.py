"""Replace three thin editorial panels only; preserve navigation, media, URLs and FAQ schema."""
from pathlib import Path
from html import escape, unescape
import json,re
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'content/narita-decision-guides.json').read_text())
STYLE='''<style id="narita-decision-style">.decision-table-scroll{max-width:100%;overflow-x:auto}.decision-table-scroll:focus-visible{outline:3px solid #ffaf9e}.decision-table{width:100%;border-collapse:collapse;table-layout:fixed}.decision-table th,.decision-table td{padding:12px 8px;border-bottom:1px solid #69848c;text-align:left;vertical-align:top;overflow-wrap:anywhere}.decision-table th:first-child{width:26%}.decision-table th:nth-child(2){width:24%}.decision-source-links{overflow-wrap:anywhere}@media(max-width:600px){.decision-table th,.decision-table td{padding:9px 5px;font-size:14px}}</style>'''
def ext(url,label,cls=''):
 return f'<a class="{cls}" href="{escape(url,quote=True)}" target="_blank" rel="noopener noreferrer">{escape(label)}</a>'
def panel(title,body):return '<section class="panel"><h2>'+escape(title)+'</h2>'+body+'</section>'
def para(s):return '<p>'+escape(s)+'</p>'
def table(c,rows,title):
 return '<div class="decision-table-scroll" tabindex="0" role="region" aria-label="'+escape(title,quote=True)+'"><table class="decision-table"><thead><tr>'+''.join('<th scope="col">'+escape(x)+'</th>' for x in c['cols'])+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+escape(row[0])+'</th>'+''.join('<td>'+escape(x)+'</td>' for x in row[1:])+'</tr>' for row in rows)+'</tbody></table></div>'
changed=[]
for lang,c in data['locales'].items():
 prefix='' if lang=='ko' else lang+'/'
 for route in ['narita-shinjuku','narita-ueno']:
  p=ROOT/prefix/'move'/route/'index.html';h=p.read_text();before=h
  sections=list(re.finditer(r'<section class="panel">.*?</section>',h,re.S));assert len(sections)>=4
  old=''.join(m[0] for m in sections[:3]);maps=re.findall(r'href="(https://www.google.com/maps/dir/[^\"]+)"',old);assert maps
  while unescape(maps[0])!=maps[0]:maps[0]=unescape(maps[0])
  nex=route.endswith('shinjuku');ps=c['nexp'] if nex else c['skyp'];heads=c['head'][:3] if nex else c['head'][3:]
  ids=[0,1,4,5,6] if nex else [2,3,4]
  sources='<p class="note">'+escape(c['sources'])+'</p><ul class="decision-source-links">'+''.join('<li>'+ext(data['sources'][i],c['sourceNames'][i])+'</li>' for i in ids)+'</ul>'
  # Time source for Ueno journey is Keisei's overview, not its ticket FAQ.
  if not nex:sources+='<p>'+ext('https://www.keisei.co.jp/keisei/tetudou/skyliner/us/skyliner/index.php','Skyliner · 41 min')+'</p>'
  body=panel(heads[0],para(ps[0])+table(c,c['nexrows'] if nex else c['skyrows'],heads[0]))
  body+=panel(heads[1],para(ps[1])+para(ps[2])+ext(maps[0],c['map'],'btn'))
  tail=para(ps[3])+(para(c['notice']) if nex else '')+para(c['unknown'])
  tail+=ext('https://www.jreast.co.jp/en/multi/nex/' if nex else 'https://keisei.ekitan.com/naritaacs-i/timetable',c['time'],'btn')+sources
  body+=panel(heads[2],tail)
  h=h.replace(old,body,1)
  # Idempotent style injection.
  h=re.sub(r'<style id="narita-decision-style">.*?</style>','',h,flags=re.S).replace('</head>',STYLE+'</head>')
  if h!=before:p.write_text(h);changed.append(str(p.relative_to(ROOT)))
 # Update ONLY Skyliner fare in the NRT card, not the unrelated Hakone ¥2,470 fare.
 p=ROOT/prefix/'move/index.html';h=p.read_text();before=h
 h=re.sub(r'<p id="narita-verified-fare".*?</p>','',h,flags=re.S)
 h=re.sub(r'<aside id="narita-service-notice".*?</aside>','',h,flags=re.S)
 cards=list(re.finditer(r'<article\b[^>]*data-airport="NRT"[^>]*>.*?</article>',h,re.S))
 for card in cards:
  if '2,470' in card[0]:h=h.replace(card[0],card[0].replace('2,470','2,580'))
 for card in re.finditer(r'<article\b[^>]*data-airport="NRT"[^>]*>.*?</article>',h,re.S):
  if '2,580' in card[0]:
   h=h.replace(card[0],card[0].replace('</article>','<p id="narita-verified-fare" class="note">'+escape(c['hubFareNote'])+'</p></article>'))
 notice='<aside id="narita-service-notice" class="panel"><p>'+escape(c['notice'])+'</p>'+ext(data['sources'][6],c['sourceNames'][6])+'</aside>'
 h=h.replace('</h1>','</h1>'+notice,1)
 if h!=before:p.write_text(h);changed.append(str(p.relative_to(ROOT)))
print(json.dumps({'changed':changed},ensure_ascii=False))
