"""Apply Korean-source winter choices with explicit facility, age and event-date scopes."""
from pathlib import Path
from html import escape
import re,json
R=Path(__file__).resolve().parents[1];d=json.loads((R/'content/sapporo-winter-decisions.json').read_text());inventory=json.loads((R/'content/search-intent-metadata.json').read_text());changed=[]
def p(t):return '<p>'+escape(t)+'</p>'
def a(u,t,cls=''):return '<a class="'+escape(cls,quote=True)+'" href="'+escape(u,quote=True)+'" target="_blank" rel="noopener noreferrer">'+escape(t)+'</a>'
for lang,c in d['locales'].items():
 prefix='' if lang=='ko' else lang+'/';file=R/prefix/'season/winter/sapporo/index.html';h=file.read_text();old=h
 main=re.search(r'<main\b[^>]*>(.*?)</main>',h,re.S)[1]
 nav=re.search(r'<nav class="jp-global-services".*?</nav>',main,re.S)[0];h1=re.search(r'<h1>.*?</h1>',main,re.S)[0].replace('겨울 여행 여행','겨울 여행');photo=re.search(r'<figure\b.*?</figure>',main,re.S)[0]
 # Keep the existing cross-region links after rebuilding the editorial body.
 related=[]
 for link in re.findall(r'<a\b[^>]*href="/[^"]*season/winter/(?:tokyo|kyoto|osaka)/"[^>]*>.*?</a>',main,re.S):
  if link not in related:related.append(link)
 maps=['https://www.google.com/maps/search/?api=1&query=Odori+Park+Sapporo','https://www.google.com/maps/search/?api=1&query=Maruyama+Park+Sapporo','https://www.google.com/maps/search/?api=1&query=Shiroi+Koibito+Park','https://www.google.com/maps/search/?api=1&query=Sapporo+Moiwa+Ropeway+Base+Station']
 table='<div class="jp-decision-scroll" tabindex="0" role="region" aria-label="'+escape(c['heads'][1],quote=True)+'"><table class="jp-decision-table"><thead><tr>'+''.join('<th scope="col">'+escape(x)+'</th>' for x in c['cols'])+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+escape(row[0])+'</th>'+''.join('<td>'+escape(x)+'</td>' for x in row[1:])+'</tr>' for row in c['rows'])+'</tbody></table></div>'
 details=''.join('<details><summary>'+escape(c['places'][i])+'</summary>'+p(c['access'][i])+a(maps[i],c['places'][i]+' · Google Maps','jp-decision-map')+'</details>' for i in range(4))
 map_route='https://www.google.com/maps/dir/?api=1&origin=Odori+Station+Sapporo&destination=Shiroi+Koibito+Park&travelmode=transit'
 links=['현재 날씨·이동','Weather and transport','天気・交通','天气与交通'][['ko','en','ja','zh-cn'].index(lang)]
 local='<nav class="links" aria-label="'+escape(links,quote=True)+'"><a href="/'+prefix+'now/">'+escape(links)+'</a> · <a href="/'+prefix+'move/">'+escape(c['heads'][2])+'</a></nav>'
 bodies=[photo,table,details,''.join(p(x) for x in c['plans'])+a(map_route,'Google Maps','jp-decision-map')+a('https://www.google.com/maps/dir/?api=1&origin=Shiroi+Koibito+Park&destination=Sapporo+Moiwa+Ropeway+Base+Station&travelmode=transit','Google Maps · 2','jp-decision-map'),''.join(p(x) for x in c['shiroi']),''.join(p(x) for x in c['moiwa']),''.join('<h3>'+escape(q)+'</h3>'+p(ans) for q,ans in c['faq'])+local,'<p>2026-10-30</p><ul>'+''.join('<li>'+a(u,t)+'</li>' for u,t in d['sources'])+'</ul>']
 content=nav+h1+p(c['description'])+''.join('<section class="panel"><h2>'+escape(title)+'</h2>'+body+'</section>' for title,body in zip(c['heads'],bodies))+('<nav class="links">'+ ' · '.join(related)+'</nav>' if related else '')
 h=re.sub(r'(<main\b[^>]*>).*?</main>',lambda m:m[1]+content+'</main>',h,count=1,flags=re.S)
 h=re.sub(r'(<meta name="description"[^>]*>)>',r'\1',h)
 css='<link rel="stylesheet" href="/assets/decision-guides.css?v=20261030">'
 if css not in h:h=h.replace('</head>',css+'</head>')
 for name in ['description','og:description']:
  attr='name' if name=='description' else 'property'
  h=re.sub(r'(<meta '+attr+'="'+name+r'" content=")[^"]*',lambda m:m[1]+escape(c['description'],quote=True),h)
 url='https://japulse.com/'+prefix+'season/winter/sapporo/'
 def update(m):
  j=json.loads(m[2]);assert j['url']==url;j['description']=c['description'];j['dateModified']='2026-10-30';return m[1]+json.dumps(j,ensure_ascii=False,separators=(',',':'))+m[3]
 h=re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)',update,h,flags=re.S)
 for row in inventory:
  if row['url']==url:row['description']=c['description']
 if h!=old:file.write_text(h);changed.append(str(file.relative_to(R)))
(R/'content/search-intent-metadata.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'changed':changed},ensure_ascii=False))
