"""Inventory visible editorial blocks; flags are review candidates, not policy verdicts."""
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict
import re,json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1]
class Blocks(HTMLParser):
 def __init__(self):
  super().__init__();self.skip=0;self.active=None;self.text=[];self.blocks=[]
 def handle_starttag(self,t,a):
  if t in ('script','style','nav','header','footer'):self.skip+=1
  if not self.skip and t in ('p','li','h2','h3','td'):self.active=t;self.text=[]
 def handle_data(self,d):
  if self.active and not self.skip:self.text.append(d)
 def handle_endtag(self,t):
  if t==self.active:
   s=' '.join(''.join(self.text).split())
   if s:self.blocks.append((t,s))
   self.active=None
  if t in ('script','style','nav','header','footer'):self.skip=max(0,self.skip-1)
patterns={
 'referral_or_caveat':r'공식.{0,35}확인|확인.{0,20}(하세요|필요)|달라질 수|보장하지|미확인|check.{0,40}official|consult.{0,30}official|公式.{0,30}確認|公式.{0,30}確認|请.{0,25}(确认|查询)|以.{0,20}为准',
 'missing_specific_value':r'운행편별 공식 확인|요금.{0,12}미확인|운영시간.{0,12}미확인|not verified|unverified|未確認|未核实'
}
def run(label):
 rows=[]; repeated=defaultdict(list)
 for p in sorted(ROOT.rglob('index.html')):
  rel=p.relative_to(ROOT);parts=rel.parts;lang=parts[0] if parts[0] in ('en','ja','zh-cn') else 'ko';family=parts[1] if lang!='ko' else parts[0]
  if family not in ('live','cameras','now','season','onsen','move','run-eat','local-food'):continue
  h=p.read_text();parser=Blocks();parser.feed(h)
  flags=[dict(kind=k,text=s) for t,s in parser.blocks for k,pat in patterns.items() if re.search(pat,s,re.I)]
  for t,s in parser.blocks:
   if t in ('p','li') and len(s)>=45:repeated[(lang,s)].append(str(rel))
  rows.append(dict(path=str(rel),language=lang,family=family,visibleCharacters=sum(len(s) for _,s in parser.blocks),tables=len(re.findall(r'<table\b',h)),flags=flags,sha256=hashlib.sha256(h.encode()).hexdigest()))
 duplicates=[dict(language=l,text=s,pages=sorted(set(ps))) for (l,s),ps in repeated.items() if len(set(ps))>=3]
 result=dict(baseline='83b9ec4',scope='All index.html under seven services, including camera detail pages; shared region/guides require separate review.',warning='Regex and exact repetition are review candidates. Short text is not proof of low value. Manual factual/semantic review remains required.',pages=rows,repeatedBlocks=duplicates)
 out=ROOT/'audit/2026-10-30'/('content-value-'+label+'.json');out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(dict(snapshot=label,pages=len(rows),flaggedPages=sum(bool(r['flags']) for r in rows),repeatedBlocks=len(duplicates),families={f:sum(r['family']==f for r in rows) for f in sorted({r['family'] for r in rows})})))
if __name__=='__main__':
 import sys;run(sys.argv[1] if len(sys.argv)>1 else 'current')
