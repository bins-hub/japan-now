"""Apply source-backed regional choices after the Tokyo and legacy localizers."""
from pathlib import Path
from html import escape as E,unescape
from urllib.parse import urlsplit
import re,json
R=Path(__file__).resolve().parents[1];D=json.loads((R/'content/regional-run-eat-decisions.json').read_text());changed=[]
sources={
'osaka':[('https://www.osakacastlepark.jp/sports/runningmap.html?lang=en','Osaka Castle · course'),('https://runningbase.jp/','RUNNING BASE · price/hours'),('https://mugiudn0507.amebaownd.com/posts/56311011/','麦笑 · operator hours'),('https://asushoku-morinomiya.com/shop/','Asushoku · hours'),('https://asushoku-morinomiya.com/menu/menu.pdf','Asushoku · menu'),('https://www.omu.ac.jp/campusjournal/info/test/entry-101233.html','Karin · OMU interview'),('https://yoyaku.toreta.in/asu0701','Asushoku · lunch reservation')],
'kyoto':[('https://www.city.kyoto.lg.jp/bunshi/page/0000160807.html','Kyoto City · turnaround course'),('https://1010.kyoto/spot/kamogawayu/','Kamogawa-yu · hours'),('https://1010.kyoto/how_to_use/','Kyoto bath association · fees'),('https://masugata.demachi.jp/shop/shop_102/','Masugataya · shopping street'),('https://www.hieizan.gr.jp/yase/demachifutaba','Futaba · tourism'),('https://tabelog.com/kyoto/A2601/A260302/26018884/dtlmenu/','Kamomachi · listed menu')],
'kyushu':[('https://www.ohorikouen.jp/map/','Ohori · map'),('https://unplan.jp/fukuoka/experience','UNPLAN · booking/price'),('https://www.tablecheck.com/ja/osai','Osai · booking menu'),('https://www.nishitetsu.jp/nishitetsu_news/spot_type/post-9126/','Osai · Nishitetsu interview'),('https://o-jisyo.com/project03/','Ohori Fureai · operator'),('https://r.gnavi.co.jp/acbeuyup0000/','Udon Hiyori · lunch notice'),('https://www.royal-gardencafe.com/store-menu/ohoripark.html','Royal Garden Cafe · hours'),('https://www.royal-gardencafe.com/store-menu/upfiles/ohoripark_menu_lunch.pdf?v=20260828122903','Royal Garden Cafe · weekday lunch')],
'hokkaido':[('https://www.sapporo-sport.jp/nakajima/news_info/?no=1777','Nakajima Sports Center · 2026 season'),('https://www.sapporosport.org/sapporomachirun/','Sapporo · running'),('https://www.s-sandwich.com/','Sandria · current menu'),('https://www.sapporo.travel/gourmet/shop/sandria/','Sapporo tourism · access')],
'okinawa':[('https://chatantourism.com/spot/araha-beach/','Chatan tourism · beach/promenade'),('https://www.okinawastory.jp/gourmet/600004584','Okinawa tourism · Hamaya')]
}
transfers={
'osaka':('RUNNING BASE Osaka Castle','Asushoku Morinomiya'),
'kyoto':('Kamo Ohashi Kyoto','Demachi Futaba'),
'kyushu':('UNPLAN Fukuoka','Royal Garden Cafe Ohori Park'),
'hokkaido':('Nakajima Park Sapporo','Sandria Main Shop Sapporo'),
'okinawa':('Araha Beach Chatan','Hamaya Soba Miyagi Chatan')}
def p(t):return '<p>'+E(t)+'</p>'
def a(u,t,external=True):return '<a class="jp-decision-map" href="'+E(unescape(u),quote=True)+'"'+(' target="_blank" rel="noopener noreferrer"' if external else '')+'>'+E(t)+'</a>'
def table(cols,rows,label):return '<div class="jp-decision-scroll" tabindex="0" role="region" aria-label="'+E(label,quote=True)+'"><table class="jp-decision-table"><thead><tr>'+''.join('<th scope="col">'+E(x)+'</th>' for x in cols)+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+E(r[0])+'</th>'+''.join('<td>'+E(x)+'</td>' for x in r[1:])+'</tr>' for r in rows)+'</tbody></table></div>'
def remember(old,token,label):
 m=re.search('<!-- '+token+' -->(.*?)<!-- /'+token+' -->',old,re.S)
 if m:return m[1]
 # Preserve destinations with individual restaurant names and source domains.
 out=[];seen=set()
 for card in re.findall(r'<article\b[^>]*>.*?</article>',old,re.S):
  name=re.search(r'<h3[^>]*>(.*?)</h3>',card,re.S);name=unescape(re.sub('<[^>]+>','',name[1])) if name else label
  for u in re.findall(r'href="([^"]+)"',card):
   u=unescape(u)
   if not u.startswith('https://') or 'japulse.com' in u or u in seen:continue
   seen.add(u);host=urlsplit(u).netloc;out.append(a(u,name+' · '+('Google Maps' if 'google.com' in host else host)))
 return ''.join(out)
for lang,C in D['locales'].items():
 prefix='' if lang=='ko' else lang+'/'
 for service in ['run-eat','local-food']:
  f=R/prefix/service/'index.html';h=f.read_text();before=h
  for region,c in C['run' if service=='run-eat' else 'eat'].items():
   if service=='run-eat':
    pat=r'<!-- JAPULSE VERIFIED RUN START '+region+r' -->.*?<!-- JAPULSE VERIFIED RUN END '+region+r' -->'
    block='<section class="jp-run-proof" aria-labelledby="jp-proof-'+region+'"><h3 id="jp-proof-'+region+'">'+E(c['title'])+'</h3>'
   else:
    pat=r'<section class="lf-section" id="'+region+r'">.*?</section>'
    old=re.search(pat,h,re.S)[0];block='<section class="lf-section" id="'+region+'"><div class="lf-h"><h2>'+E(c['title'])+'</h2></div>'
   block+=table(C['cols'],c['rows'],c['title'])+''.join(p(t) for t in c['text'])
   origin,dest=transfers[region]
   from urllib.parse import urlencode
   route='https://www.google.com/maps/dir/?'+urlencode({'api':1,'origin':origin,'destination':dest,'travelmode':'driving' if region=='okinawa' else 'walking'})
   block+=a(route,C['map'])
   target='local-food' if service=='run-eat' else 'run-eat'
   if region in C['eat']:block+=a('/'+prefix+target+'/#'+region,C['eatlink' if service=='run-eat' else 'runlink'],False)
   block+='<h4>'+E(C['sources'])+'</h4><div class="jp-decision-sources">'+''.join(a(u,t) for u,t in sources[region])+'</div>'
   if service=='local-food':
    token='REGIONAL EXISTING LINKS '+region;links=remember(old,token,C['old']);block+='<details><summary>'+E(C['old'])+'</summary><!-- '+token+' -->'+links+'<!-- /'+token+' --></details>'
   block+='</section>'
   if service=='run-eat':block='<!-- JAPULSE VERIFIED RUN START '+region+' -->'+block+'<!-- JAPULSE VERIFIED RUN END '+region+' -->'
   h,n=re.subn(pat,lambda m:block,h,count=1,flags=re.S);assert n==1,(f,region)
  if service=='run-eat':
   fixes={
    'ko':{'약 4.3km (공식 편도 구간)':'약4.3km (공식 왕복 코스)','가모가와 다카노 공식 구간 약 4.3km는 편도 기준이며, 출발점으로 복귀하면 추가 거리가 필요합니다.':'다카노 코스는 가모오하시에서 마쓰가사키 인도교를 반환해 돌아오는 약4.3km 코스입니다.'},
    'en':{'~4.3 km official one-way section':'~4.3km official return course',"Kyoto's official Takano section is about 4.3 km one way. Returning to the start adds distance.":'The official Takano course is about4.3km including the return from Matsugasaki footbridge to Kamo Ohashi.'},
    'ja':{'公式片道区間 約4.3km':'公式往復コース 約4.3km','京都市の高野コース約4.3kmは片道区間の目安です。起点へ戻る場合はさらに距離が増えます。':'高野コースは賀茂大橋から松ヶ崎人道橋で折り返して戻る約4.3kmのコースです。'},
    'zh-cn':{'官方单程路段约4.3公里':'官方往返路线约4.3公里','京都官方高野路线约4.3公里指单程路段，返回原起点需额外里程。':'官方高野路线从贺茂大桥至松崎人道桥折返，全程约4.3公里。'}
   }
   for old,new in fixes[lang].items():h=h.replace(old,new)
  if service=='run-eat':h=h.replace('run-route-visuals.js?v=20261027-c1','run-route-visuals.js?v=20261030-c2').replace('run-shower.js?v=20261021-s1','run-shower.js?v=20261030-s2')
  # Keep existing scripts and URLs; dedicated styles were already used by Tokyo.
  if h!=before:f.write_text(h);changed.append(str(f.relative_to(R)))
# The illustration is a return path, and its distance must match the official turnaround route.
f=R/'assets/run-route-visuals.js';s=f.read_text().replace('distance:"4.3km one-way"','distance:"~4.3 km"');
if s!=f.read_text():f.write_text(s);changed.append(str(f.relative_to(R)))
print(json.dumps({'changed':changed},ensure_ascii=False))
