"""Apply Korean-source Tokyo running and lunch decisions after legacy localization."""
from pathlib import Path
from html import escape as E, unescape
import re,json
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'content/tokyo-run-eat-decisions.json').read_text())
def p(t):return '<p>'+E(t)+'</p>'
def a(u,t):return '<a class="jp-decision-map" href="'+E(u,quote=True)+'" target="_blank" rel="noopener noreferrer">'+E(t)+'</a>'
def table(cols,rows,label):
 return '<div class="jp-decision-scroll" tabindex="0" role="region" aria-label="'+E(label,quote=True)+'"><table class="jp-decision-table"><thead><tr>'+''.join('<th scope="col">'+E(x)+'</th>' for x in cols)+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+E(r[0])+'</th>'+''.join('<td>'+E(x)+'</td>' for x in r[1:])+'</tr>' for r in rows)+'</tbody></table></div>'
changed=[]
for lang,c in d['locales'].items():
 prefix='' if lang=='ko' else lang+'/'
 for service in ['run-eat','local-food']:
  f=R/prefix/service/'index.html';h=f.read_text();before=h;L=c['links']
  if service=='run-eat':
   pat=r'<!-- JAPULSE VERIFIED RUN START tokyo -->.*?<!-- JAPULSE VERIFIED RUN END tokyo -->'
   content='<section class="jp-run-proof" aria-labelledby="jp-proof-tokyo"><h3 id="jp-proof-tokyo">'+E(c['run_head'])+'</h3>'+p(c['run_intro'])+table(c['cols'],c['run_rows'],c['run_head'])+p(c['run_hours'])+p(c['run_plan'])+p(c['run_choice'])
   urls=[('https://www.google.com/maps/search/?api=1&query=Imperial+Palace+Sakuradamon',L[0]),('https://www.asics.com/jp/ja-jp/mk/store/asicsruntokyo-marunouchi',L[1]),('https://www.asics.com/jp/ja-jp/customer-service/notification/news/2025/a332/',L[2]),('https://www.env.go.jp/garden/kokyogaien/2_guide/running.html',L[3]),('https://www.gotokyo.org/jp/story/guide/running-course-guide-for-runners/index.html','GO TOKYO')]
   content+='<div class="jp-source-links">'+''.join(a(u,t) for u,t in urls)+'<a class="jp-decision-map" href="/'+prefix+'local-food/#tokyo">'+E(L[4])+'</a></div>'+p(c['checked'])+'</section>'
   replacement='<!-- JAPULSE VERIFIED RUN START tokyo -->'+content+'<!-- JAPULSE VERIFIED RUN END tokyo -->'
  else:
   pat=r'<section class="lf-section" id="tokyo">.*?</section>'
   original=re.search(pat,h,re.S)[0]
   # Retain both existing restaurants' outbound map and review URLs without reusing stale prose.
   old=re.search(r'<!-- TOKYO EXISTING LINKS -->(.*?)<!-- /TOKYO EXISTING LINKS -->',original,re.S)
   if old:
    from urllib.parse import urlsplit
    def label(m):
     u=unescape(m[1]);name='キッチン南海' if any(t in u for t in ['13249021','/388','%E3%82%AD']) else 'さぼうる2'
     host=urlsplit(u).netloc
     return a(u,name+' · '+('Google Maps' if 'google.com' in host else host))
    links=re.sub(r'<a[^>]*href="([^"]+)"[^>]*>.*?</a>',label,old[1],flags=re.S)
   else:
    links='';seen=set()
    for u in re.findall(r'<a[^>]*href="([^"]+)"',original):
     if u.startswith('https://') and 'japulse.com' not in u and u not in seen:
      seen.add(u);links+=a(u,L[9])
   replacement='<section class="lf-section" id="tokyo"><div class="lf-h"><h2>'+E(c['eat_head'])+'</h2></div>'+p(c['eat_intro'])+table(c['eat_cols'],c['eat_rows'],c['eat_head'])+''.join(p(x) for x in c['eat_detail'])
   urls=[('https://bondy.co.jp/web/contents/home.html',L[7]),('https://bondy.co.jp/web/contents/menu.html','Bondy · menu'),('https://visit-chiyoda.tokyo/app/spot/detail/388',L[8]),('https://www.google.com/maps/dir/?api=1&origin=ASICS+RUN+TOKYO+MARUNOUCHI&destination=Bondy+Jimbocho+Main+Shop&travelmode=walking',L[6])]
   replacement+=''.join(a(u,t) for u,t in urls)+'<a class="jp-decision-map" href="/'+prefix+'run-eat/#tokyo">'+E(L[5])+'</a><details><summary>'+E(L[9])+'</summary><!-- TOKYO EXISTING LINKS -->'+links+'<!-- /TOKYO EXISTING LINKS --></details>'+p(c['checked'])+'</section>'
  h,n=re.subn(pat,lambda m:replacement,h,count=1,flags=re.S);assert n==1,f
  css='<link rel="stylesheet" href="/assets/decision-guides.css?v=20261030">'
  if css not in h:h=h.replace('</head>',css+'</head>')
  if h!=before:f.write_text(h);changed.append(str(f.relative_to(R)))
print(json.dumps({'changed':changed},ensure_ascii=False))
