#!/usr/bin/env python3
"""Configure canonical URLs + XML sitemap for a publicly deployed JAPAN NOW site.
Usage: python3 tools/configure_domain.py https://your.real.site/path
Run from inside the unzipped site. No dependencies beyond Python 3.
"""
import json, re, sys, xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit
from datetime import date

SITE=Path(__file__).resolve().parent.parent
if len(sys.argv)!=2:sys.exit('Usage: python3 tools/configure_domain.py https://your-real-domain/optional-path')
base=sys.argv[1].rstrip('/')
parts=urlsplit(base)
if parts.scheme!='https' or not parts.netloc or parts.query or parts.fragment or any(c in base for c in '<>'):
    sys.exit('Please specify the final real HTTPS site URL, including a project subpath if any.')

allpages=sorted(SITE.rglob('index.html'))
for file in allpages:
    rel=file.relative_to(SITE).parent.as_posix()
    if rel=='.':rel=''
    canonical=base+'/'+(rel+'/' if rel else '')
    raw=file.read_text(encoding='utf-8')
    raw=re.sub(r'\s*<link rel="canonical" href="[^"]*">','',raw)
    raw=re.sub(r'\s*<meta property="og:url" content="[^"]*">','',raw)
    raw=raw.replace('</head>',f'<link rel="canonical" href="{canonical}"><meta property="og:url" content="{canonical}"></head>',1)
    def fill_jsonld(match):
        obj=json.loads(match.group(1))
        entries=obj.get('@graph', [obj])
        for item in entries:
            t=item.get('@type')
            if t=='WebSite':item['url']=base+'/'
            elif t in ('CollectionPage','WebPage'):item['url']=canonical
            elif t=='Article':item['mainEntityOfPage']=canonical
            if t=='CollectionPage' and not rel and isinstance(item.get('mainEntity'),dict):
                for li in item['mainEntity'].get('itemListElement',[]):
                    # camera items are listed in the original catalogue order
                    li.pop('url',None)
        if not rel:
            ids=['shibuya','kabukicho','sensoji','dotonbori','osaka-sky','arashiyama','fuji','sapporo','hakata','okinawa','iki']
            for item in entries:
                if item.get('@type')=='CollectionPage':
                    for li,cid in zip(item.get('mainEntity',{}).get('itemListElement',[]),ids):li['url']=base+'/cameras/'+cid+'/'
        return '<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False).replace('</','<\\/')+'</script>'
    raw=re.sub(r'<script type="application/ld\+json">(.*?)</script>',fill_jsonld,raw,flags=re.S)
    file.write_text(raw,encoding='utf-8')

ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
root=ET.Element('{%s}urlset'%ns)
for file in allpages:
    rel=file.relative_to(SITE).parent.as_posix()
    if rel=='.':rel=''
    item=ET.SubElement(root,'{%s}url'%ns)
    ET.SubElement(item,'{%s}loc'%ns).text=base+'/'+(rel+'/' if rel else '')
    ET.SubElement(item,'{%s}lastmod'%ns).text=date.today().isoformat()
ET.ElementTree(root).write(SITE/'sitemap.xml',encoding='utf-8',xml_declaration=True)
rob=(SITE/'robots.txt').read_text(encoding='utf-8')
rob=re.sub(r'\nSitemap:.*', '', rob)
(SITE/'robots.txt').write_text(rob.rstrip()+'\n\nSitemap: '+base+'/sitemap.xml\n',encoding='utf-8')
print(f'Configured {len(allpages)} canonical URLs, structured data, sitemap.xml and robots.txt for {base}')
