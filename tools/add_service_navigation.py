"""Keep every service reachable throughout the selected-language user journey."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent.parent
PREFIXES=['en/','ja/','zh-cn/']
SECTIONS={'live':'LIVE','now':'NOW','run-eat':'RUN','local-food':'EAT','season':'SEASON','onsen':'ONSEN','move':'MOVE'}
for p in ROOT.rglob('index.html'):
 if '.git' in p.parts:continue
 route=str(p.relative_to(ROOT)).removesuffix('index.html')
 prefix=next((s for s in PREFIXES if route.startswith(s)),'')
 base=route[len(prefix):]
 if not base:continue
 h=p.read_text()
 if 'class="jp-global-services"' in h:continue
 label={'en/':'JAPULSE services','ja/':'JAPULSEサービス','zh-cn/':'JAPULSE服务','':'JAPULSE 주요 서비스'}[prefix]
 current=base.split('/')[0]
 nav='<nav class="jp-global-services" aria-label="'+label+'">'+''.join('<a href="/'+prefix+slug+'/"'+(' aria-current="page"' if current==slug else '')+'>'+name+'</a>' for slug,name in SECTIONS.items())+'</nav>'
 if re.search(r'<main\b',h):h=re.sub(r'(<main\b[^>]*>)',lambda m:m[1]+nav,h,count=1)
 else:h=h.replace('</header>','</header><div class="wrap">'+nav+'</div>',1)
 if '/assets/services-nav.css' not in h:h=h.replace('</head>','<link rel="stylesheet" href="/assets/services-nav.css?v=20261028"></head>')
 p.write_text(h)
print('Added seven-service locale-preserving navigation to 300 internal pages.')
