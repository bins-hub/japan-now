"""Apply researched editorial panels after the existing locale generators. No deployment."""
from pathlib import Path
from html import escape,unescape
import re,json
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'content/airport-decision-guides.json').read_text())
LANGS=['ko','en','ja','zh-cn']
def a(url,label,cls=''):
 return '<a class="'+cls+'" href="'+escape(unescape(url),quote=True)+'" target="_blank" rel="noopener noreferrer">'+escape(label)+'</a>'
def p(s):return '<p>'+escape(s)+'</p>'
def section(title,s):return '<section class="panel"><h2>'+escape(title)+'</h2>'+s+'</section>'
def table(c,title,rows):
 return '<div class="jp-decision-scroll" tabindex="0" role="region" aria-label="'+escape(title,quote=True)+'"><table class="jp-decision-table"><thead><tr>'+''.join('<th scope="col">'+escape(x)+'</th>' for x in c)+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+escape(row[0])+'</th>'+''.join('<td>'+escape(x)+'</td>' for x in row[1:])+'</tr>' for row in rows)+'</tbody></table></div>'
changed=[]
for i,lang in enumerate(LANGS):
 prefix='' if lang=='ko' else lang+'/'
 for route,d in DATA['routes'].items():
  file=ROOT/prefix/'move'/route/'index.html';h=file.read_text();old=h;c=d['locales'][lang];common=DATA['common'];heads=common['heads'][i]
  sections=list(re.finditer(r'<section class="panel">.*?</section>',h,re.S));assert len(sections)>=4
  original=''.join(x[0] for x in sections[:3]);maps=re.findall(r'href="(https://www.google.com/maps/dir/[^\"]+)"',original);assert maps
  body=section(heads[0],p(c['summary'])+table(common['cols'][i],heads[0],c['rows']))
  body+=section(heads[1],''.join(p(x) for x in c['steps'])+a(maps[0],common['map'][i],'btn'))
  body+=section(heads[2],''.join(p(x) for x in c['rules'])+p(common['unknown'][i])+p(common['checked'][i])+'<ul class="jp-decision-sources">'+''.join('<li>'+a(url,name)+'</li>' for url,name in d['sources'])+'</ul>')
  h=h.replace(original,body,1)
  css='<link rel="stylesheet" href="/assets/decision-guides.css?v=20261030">'
  if css not in h:h=h.replace('</head>',css+'</head>')
  if h!=old:file.write_text(h);changed.append(str(file.relative_to(ROOT)))
 # Fill the associated four airport cards without changing filtering or planner scripts.
 file=ROOT/prefix/'move/index.html';h=file.read_text();old=h
 cards=list(re.finditer(r'<article\b[^>]*data-airport="[^"]+"[^>]*>.*?</article>',h,re.S))
 assert len(cards)==8
 for index,card in enumerate(cards):
  route=[None,None,'haneda-shinagawa','haneda-hamamatsucho','kansai-namba','kansai-kyoto','kansai-shin-osaka','new-chitose-sapporo'][index]
  if route is None:continue
  c=DATA['routes'][route]['locales'][lang];new=card[0]
  # First descriptive paragraph follows h3 + operator strong.
  new,n=re.subn(r'(<strong>.*?</strong>)<p>.*?</p>',lambda m:m[1]+p(c['summary']),new,count=1,flags=re.S);assert n==1,(lang,route)
  ds=re.search(r'<details\b.*?</details>',new,re.S);assert ds
  paragraphs=list(re.finditer(r'<p>.*?</p>',ds[0],re.S));assert len(paragraphs)>=2
  last=paragraphs[-1][0];assert '<strong>' in last
  label=re.search(r'<strong>.*?</strong>',last)[0]
  fares=' / '.join(row[0]+': '+row[1] for row in c['rows'])
  replacement='<p>'+label+' '+escape(fares)+'</p>'
  new=new.replace(last,replacement,1)
  h=h.replace(card[0],new)
 if h!=old:file.write_text(h);changed.append(str(file.relative_to(ROOT)))
print(json.dumps({'changed':changed},ensure_ascii=False))
