"""Diagnostic candidates, not proof of translation completeness: compare headings, media, controls and stated fares."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parent.parent
LANGS=['en','ja','zh-cn']
def metrics(h):
 body=re.sub(r'<script\b[^>]*>.*?</script>','',h,flags=re.S)
 text=re.sub('<[^>]+>',' ',body)
 number=r'\d+(?:,\d{3})*'
 prices={a or b for a,b in re.findall(r'(?:¥|￥)\s*('+number+r')|('+number+r')\s*(?:엔|円|yen|日元)',text)}
 for a,b in re.findall(r'(?:¥|￥)\s*('+number+r')[~–-]('+number+r')',text):prices.update([a,b])
 return dict(h2=len(re.findall(r'<h2\b',body)),images=len(re.findall(r'<img\b',body)),details=len(re.findall(r'<details\b',body)),selects=len(re.findall(r'<select\b',body)),buttons=len(re.findall(r'<button\b',body)),prices=sorted(prices))
rows=[]
for p in ROOT.rglob('index.html'):
 rel=p.relative_to(ROOT)
 if rel.parts[0] in LANGS or '.git' in rel.parts:continue
 source=metrics(p.read_text())
 for lang in LANGS:
  target=ROOT/lang/rel;dest=metrics(target.read_text())
  differences={k:{'ko':source[k],'localized':dest[k]} for k in ['h2','images','details','selects','buttons'] if dest[k]<source[k]}
  missing=sorted(set(source['prices'])-set(dest['prices']))
  if missing:differences['fareValuesMissing']=missing
  rows.append(dict(page=str(Path(lang)/rel),source=str(rel),candidates=differences))
out=ROOT/'audit/2026-10-28/content-gap-candidates.json'
out.write_text(json.dumps({'warning':'Counts and currency tokens are diagnostic candidates only. Semantic translation, runtime controls and full layout equivalence require direct review. Passing heading counts does not certify parity.','pages':rows},ensure_ascii=False,indent=2))
print(json.dumps({'compared':len(rows),'pagesWithCandidates':sum(bool(r['candidates']) for r in rows),'fareGapPages':sum('fareValuesMissing' in r['candidates'] for r in rows)}))
