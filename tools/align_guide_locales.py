"""Generate foreign ONSEN/MOVE pages directly from Korean DOM, data and behavior.

Translations are local, reviewed source phrase mappings. No external service is used.
Default writes diagnostics and staging pages; --apply updates live source files.
"""
from pathlib import Path
import re,json,sys
from html import unescape,escape
from html.parser import HTMLParser
from complete_onsen_context import ACCESS,CONTEXT
ROOT=Path(__file__).resolve().parent.parent
LANGS=['en','ja','zh-cn']
phrases={}
for filename in ['guide_terms.tsv','guide_names.tsv','guide_sentences.tsv','move_terms.tsv']:
 p=ROOT/'tools'/filename
 if not p.exists():continue
 for line in p.read_text().splitlines():
  if not line.strip():continue
  row=line.split('|||')
  if len(row)!=4:raise ValueError(filename+': '+line)
  phrases[row[0]]=row[1:]
for family in ['onsen','move']:
 p=ROOT/'tools'/f'{family}_translations.tsv'
 if not p.exists():continue
 source=json.loads((ROOT/'content'/f'{family}-source-strings.json').read_text())
 for line in p.read_text().splitlines():
  if not line.strip():continue
  row=line.split('|||')
  if len(row)!=4:raise ValueError(str(p)+': '+line)
  phrases[source[int(row[0])]]=row[1:]
for slug,access in ACCESS.items():
 source=(ROOT/'onsen'/slug/'index.html').read_text()
 m=re.search(r'주요 교통</[^>]+>\s*<[^>]+>(.*?)</',source)
 if m:phrases[m[1]]=[x.rstrip('.。') for x in access]
 m=re.search(r'<p class="lead">(.*?)</p>',source)
 if m:phrases[m[1].split('. 지역의')[0]]=[x.rstrip('.。') for x in CONTEXT[slug]]
pattern=re.compile('|'.join(map(re.escape,sorted(phrases,key=len,reverse=True))))
def translate(text,i):
 # Templates keep destination-specific information instead of replacing it with a summary.
 text=re.sub(r'먼저 (.*?)에 가까운 구역과 숙박·당일치기 중 원하는 형태를 선택하세요\.',lambda m:[f'First choose an area near {m[1]} and decide between an overnight stay and a day visit.',f'まず{m[1]}に近いエリアを選び、宿泊か日帰りかを決めましょう。',f'先选择靠近{m[1]}的区域，再决定住宿或当天往返。'][i],text)
 text=re.sub(r'([가-힣]+)에서 당일치기 온천을 할 수 있나요\?',lambda m:[f'Can I take a day-use bath in {m[1]}?',f'{m[1]}で日帰り入浴できますか？',f'可以在{m[1]}当天入浴吗？'][i],text)
 text=pattern.sub(lambda m:phrases[m[0]][i],text)
 text=re.sub(r'([\d,]+)엔',lambda m:[m[1]+' yen',m[1]+'円',m[1]+'日元'][i],text)
 text=re.sub(r'(\d+)개 지역',lambda m:[m[1]+' areas',m[1]+'地域',m[1]+'个地区'][i],text)
 return text
class TextReader(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.rows=[]
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip-=1
 def handle_data(self,d):
  if not self.skip and re.search('[가-힣]',d):self.rows.append(d.strip())
def build(apply=False):
 missing={};count=0
 for family in ['onsen','move']:
  for p in (ROOT/family).rglob('index.html'):
   rel=p.relative_to(ROOT);source=p.read_text()
   for i,lang in enumerate(LANGS):
    target=ROOT/lang/rel;previous=target.read_text();h=source
    h=re.sub(r'<nav\b[^>]*id="jp-language-route-switch"[^>]*>.*?</nav>','',h,flags=re.S)
    # Existing native names stay native; all practical content is generated from Korean.
    for tag,regex in [('title',r'<title>.*?</title>'),('description',r'<meta name="description" content="[^"]*">')]:
     original=re.search(regex,previous,re.S)
     if original:h=re.sub(regex,lambda m:original[0],h,count=1,flags=re.S)
    native_title=translate(unescape(re.sub('<[^>]+>',' ',re.search(r'<h1\b[^>]*>(.*?)</h1>',source,re.S)[1])),i)
    def image_alt(m):
     raw=unescape(m[2]);translated=translate(raw,i)
     if re.search('[가-힣]',translated):translated=native_title
     return m[1]+escape(translated,quote=True)+m[3]
    h=re.sub(r'(<img\b[^>]*\balt=")([^"]*)(")',image_alt,h)
    h=translate(h,i)
    h=re.sub(r'<html lang="[^"]+"','<html lang="'+('zh-CN' if lang=='zh-cn' else lang)+'"',h)
    h=h.replace("toLocaleLowerCase('ko')",f"toLocaleLowerCase('{lang}')").replace("textContent,'ko'",f"textContent,'{lang}'")
    # Translate only public page links; media/assets and source operators keep their original URLs.
    routes=['onsen','move','season','live','now','run-eat','local-food','regions','cameras','about','privacy','contact','guides']
    for route in routes:
     h=h.replace('https://japulse.com/'+route+'/',f'https://japulse.com/{lang}/{route}/')
     h=h.replace('href="/'+route+'/',f'href="/{lang}/{route}/')
    h=h.replace('href="https://japulse.com/"',f'href="https://japulse.com/{lang}/"').replace('href="/"',f'href="/{lang}/"')
    # hreflang is regenerated after applying. Do not localize its alternate destinations.
    h=re.sub(r'<link\b(?=[^>]*hreflang=)[^>]*>','',h)
    base=str(rel).removesuffix('index.html')
    alternates={'ko':'','en':'en/','ja':'ja/','zh-CN':'zh-cn/','x-default':''}
    h=h.replace('</head>',''.join(f'<link rel="alternate" hreflang="{code}" href="https://japulse.com/{prefix}{base}">' for code,prefix in alternates.items())+'</head>')
    h=re.sub(r'<link rel="canonical" href="[^"]+">',f'<link rel="canonical" href="https://japulse.com/{lang}/{base}">',h)
    h=h.replace('"inLanguage":"ko"','"inLanguage":"'+('zh-CN' if lang=='zh-cn' else lang)+'"')
    description=unescape(re.search(r'<meta name="description" content="([^"]*)"',h)[1])
    def schema(m):
     data=json.loads(m[1]);data['name']=native_title;data['description']=description
     data['url']=f'https://japulse.com/{lang}/{base}';data['inLanguage']='zh-CN' if lang=='zh-cn' else lang
     if isinstance(data.get('about'),dict) and 'name' in data['about']:data['about']['name']=native_title
     return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+'</script>'
    h=re.sub(r'<script type="application/ld\+json">(.*?)</script>',schema,h,flags=re.S)
    # Service navigation already exists in the source; only its label is language-specific.
    h=h.replace('aria-label="JAPULSE 주요 서비스"','aria-label="JAPULSE services"')
    reader=TextReader();reader.feed(h)
    if reader.rows:missing[str(Path(lang)/rel)]=list(dict.fromkeys(reader.rows))
    out=target if apply else Path('/tmp/japulse-aligned')/lang/rel
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(h);count+=1
 Path('/tmp/japulse-alignment-pending.json').write_text(json.dumps(missing,ensure_ascii=False,indent=2))
 unique=list(dict.fromkeys(x for values in missing.values() for x in values))
 Path('/tmp/japulse-alignment-pending-unique.json').write_text(json.dumps(unique,ensure_ascii=False,indent=2))
 print(json.dumps({'generated':count,'pagesWithUntranslatedVisibleText':len(missing),'uniquePendingVisibleStrings':len(unique),'applied':apply}))
if __name__=='__main__':build('--apply' in sys.argv)
