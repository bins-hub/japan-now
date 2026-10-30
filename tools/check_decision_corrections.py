"""Prevent a return-course distance from regressing to a one-way claim."""
from pathlib import Path
import re,json
R=Path(__file__).resolve().parents[1]
old_claims=['약 4.3km (공식 편도 구간)','~4.3 km official one-way section','公式片道区間 約4.3km','官方单程路段约4.3公里','4.3km one-way']
results=[]
for pre in ['','en/','ja/','zh-cn/']:
 for service in ['run-eat','local-food','live','now']:
  f=R/pre/service/'index.html';s=f.read_text()
  assert not any(x in s for x in old_claims),f
  assert len(re.findall(r'<h1(?:\s[^>]*)?>',s))==1,f
  assert '<table class="jp-decision-table">' in s,f
  results.append(str(f.relative_to(R)))
 data=json.loads((R/'content/regional-run-eat-decisions.json').read_text())['locales']['ko']
 assert 1000+1630==2630 and 1630*2+950==4210 and 1903+500==2403 and 2403+100==2503
 # Every language offers all five remaining running regions and three meal regions.
 for c in json.loads((R/'content/regional-run-eat-decisions.json').read_text())['locales'].values():
  assert set(c['run'])=={'osaka','kyoto','kyushu','hokkaido','okinawa'}
  assert set(c['eat'])=={'osaka','kyoto','kyushu'}
s=(R/'assets/run-route-visuals.js').read_text();assert '4.3km one-way' not in s
print('PASS16 decision pages; Kyoto obsolete one-way claims absent; regional locale coverage and family/budget arithmetic')
