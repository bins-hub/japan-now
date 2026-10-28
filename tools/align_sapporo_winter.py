"""Use the Korean winter itinerary, route labels and operating caveats."""
from pathlib import Path
import json,re,html
ROOT=Path(__file__).resolve().parent.parent
DATA=json.loads((ROOT/'content/sapporo-winter-locales.json').read_text())

def run():
 source=(ROOT/'season/winter/sapporo/index.html').read_text()
 route=re.search(r'<section><h2>삿포로 여행 동선.*?</section>',source,re.S)[0]
 day=re.search(r'<section><h2>삿포로 겨울 1일.*?</section>',source,re.S)[0]
 route_urls=re.findall(r'<a href="([^"]+)"',route)
 day_url=re.search(r'<a href="([^"]+)"',day)[1]
 official=re.search(r'<section><h2>공식 정보 및 JAPULSE 연계.*?</section>',source,re.S)[0]
 official_urls=re.findall(r'<a[^>]+href="([^"]+)"',official)
 assert len(route_urls)==2 and len(official_urls)==5
 def link(url,label,lang):
  if 'japulse.com/' in url:url=url.replace('japulse.com/','japulse.com/'+lang+'/')
  elif url.startswith('/'):url='/'+lang+url
  return '<a class="btn" href="'+url+'"'+(' target="_blank" rel="noopener noreferrer"' if not ('japulse.com/' in url or url.startswith('/')) else '')+'>'+html.escape(label)+'</a>'
 for lang,d in DATA.items():
  path=ROOT/lang/'season/winter/sapporo/index.html';s=path.read_text()
  r=d['route'];t=d['day'];p=d['prep'];q=d['faq']
  blocks=[
   '<section class="panel"><h2>'+r[0]+'</h2><p>'+r[1]+'</p>'+''.join(link(u,label,lang) for u,label in zip(route_urls,r[2:4]))+'<p>'+r[4]+'</p></section>',
   '<section class="panel" id="jp-sapporo-winter-itinerary"><h2>'+t[0]+'</h2><ol>'+''.join('<li><strong>'+t[i]+'</strong> — '+t[i+1]+'</li>' for i in [1,3,5])+'</ol><p>'+t[7]+'</p>'+link(day_url,t[8],lang)+'</section>',
   '<section class="panel"><h2>'+p[0]+'</h2><p>'+p[1]+'</p><p>'+p[2]+'</p></section>',
   '<section class="panel"><h2>'+q[0]+'</h2><h3>'+q[1]+'</h3><p>'+q[2]+'</p><h3>'+q[3]+'</h3><p>'+q[4]+'</p></section>'
  ]
  # On initial generation these four generic panels follow the place directory.
  # Markers support exact replacement on subsequent runs.
  start='<!-- JP SAPPORO WINTER START -->';end='<!-- JP SAPPORO WINTER END -->'
  block=start+''.join(blocks)+end
  if start in s:s=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda m:block,s,flags=re.S)
  else:
   matches=list(re.finditer(r'<section class="panel">.*?</section>',s,re.S));assert len(matches)==7
   s=s[:matches[1].start()]+block+s[matches[4].end():]
  intro='<p class="note" id="jp-sapporo-source-context">'+d['intro']+'</p>'
  if 'id="jp-sapporo-source-context"' in s:s=re.sub(r'<p class="note" id="jp-sapporo-source-context">.*?</p>',lambda m:intro,s,flags=re.S)
  else:s=re.sub(r'(</h1>)',lambda m:m[0]+intro,s,count=1)
  refs='<section class="panel" id="jp-sapporo-official"><h2>'+d['official']+'</h2>'+''.join(link(u,label,lang) for u,label in zip(official_urls,d['officialLinks']))+'</section>'
  refs+='<section class="panel" id="jp-sapporo-related"><h2>'+d['related']+'</h2>'
  for city in ['tokyo','kyoto','osaka']:
   target=ROOT/lang/'season/winter'/city/'index.html'
   title=re.search(r'<h1[^>]*>(.*?)</h1>',target.read_text(),re.S)[1]
   refs+=link('/season/winter/'+city+'/',re.sub('<[^>]+>','',title),lang)
  refs+='</section>'
  ref_start='<!-- JP SAPPORO REFERENCES START -->';ref_end='<!-- JP SAPPORO REFERENCES END -->'
  if ref_start in s:s=re.sub(re.escape(ref_start)+r'.*?'+re.escape(ref_end),lambda m:ref_start+refs+ref_end,s,flags=re.S)
  else:s=s.replace('</main>',ref_start+refs+ref_end+'</main>')
  path.write_text(s)
 print('Aligned three Sapporo winter itineraries with Korean route, winter caveats, FAQs and sources.')
if __name__=='__main__':run()
