"""Replace generic LIVE/NOW referrals with localized travel decision tables."""
from pathlib import Path
from html import escape as E
import json,re
R=Path(__file__).resolve().parents[1];D=json.loads((R/'content/live-now-decisions.json').read_text());inventory=json.loads((R/'content/search-intent-metadata.json').read_text());changed=[]
def p(t):return '<p>'+E(t)+'</p>'
def a(u,t):return '<a class="jp-decision-map" href="'+E(u,quote=True)+'"'+(' target="_blank" rel="noopener noreferrer"' if u.startswith('https://') else '')+'>'+E(t)+'</a>'
for lang,C in D['locales'].items():
 pre='' if lang=='ko' else lang+'/'
 for service,c in C.items():
  f=R/pre/service/'index.html';h=f.read_text();before=h
  pat=r'<section id="jp-'+service+r'-practical-guide".*?</section>';old=re.search(pat,h,re.S);assert old,f
  tag=re.match(r'<section[^>]*>',old[0])[0]
  block=tag+'<h2 id="jp-'+service+'-practical-title">'+E(c['title'])+'</h2>'+p(c['intro'])
  block+='<div class="jp-decision-scroll" tabindex="0" role="region" aria-label="'+E(c['title'],quote=True)+'"><table class="jp-decision-table"><thead><tr>'+''.join('<th scope="col">'+E(t)+'</th>' for t in c['cols'])+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+E(r[0])+'</th>'+''.join('<td>'+E(x)+'</td>' for x in r[1:])+'</tr>' for r in c['rows'])+'</tbody></table></div>'+''.join(p(x) for x in c['paras'])
  urls=['run-eat/#tokyo','run-eat/#osaka','run-eat/#kyoto','season/winter/sapporo/','cameras/fuji/','now/'] if service=='live' else ['run-eat/','local-food/','season/winter/sapporo/','move/']
  if service=='now':block+=''.join('<h3>'+E(q)+'</h3>'+p(ans) for q,ans in c['faq'])
  block+='<div>'+''.join(a('/'+pre+u,t) for u,t in zip(urls,c['links']))
  if service=='now':block+=a('https://www.jma.go.jp/jma/kishou/know/bosai/warning.html',c['links'][4])+a('https://www.wbgt.env.go.jp/alert.php',c['links'][5])
  block+='</div></section>';h=re.sub(pat,lambda m:block,h,count=1,flags=re.S)
  css='<link rel="stylesheet" href="/assets/decision-guides.css?v=20261030">'
  if css not in h:h=h.replace('</head>',css+'</head>')
  for attr,key in [('name','description'),('property','og:description')]:
   h=re.sub(r'(<meta '+attr+'="'+key+r'" content=")[^"]*',lambda m:m[1]+E(c['desc'],quote=True),h)
  url='https://japulse.com/'+pre+service+'/'
  def schema(m):
   j=json.loads(m[2])
   if j.get('url')==url:j['description']=c['desc'];j['dateModified']='2026-10-30'
   return m[1]+json.dumps(j,ensure_ascii=False,separators=(',',':'))+m[3]
  h=re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)',schema,h,flags=re.S)
  for row in inventory:
   if row['url']==url:row['description']=c['desc']
  if h!=before:f.write_text(h);changed.append(str(f.relative_to(R)))
(R/'content/search-intent-metadata.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'changed':changed},ensure_ascii=False))
