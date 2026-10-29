"""Validate the four-language search contract for every indexed page."""
from html import unescape
import json
from pathlib import Path
import re
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]


def walk(value):
    if isinstance(value,dict):
        yield value
        for child in value.values():yield from walk(child)
    elif isinstance(value,list):
        for child in value:yield from walk(child)


def main():
    rows=json.loads((ROOT/'content/search-intent-metadata.json').read_text())
    urls=re.findall(r'<loc>(.*?)</loc>',(ROOT/'sitemap.xml').read_text())
    assert set(urls)=={r['url'] for r in rows},'Search inventory must cover the sitemap exactly'
    groups=defaultdict(list);titles=defaultdict(set)
    for row in rows:
        source=(ROOT/row['url'].removeprefix('https://japulse.com/')/'index.html').read_text()
        head=source.split('</head>')[0]
        title=unescape(re.search(r'<title>(.*?)</title>',head,re.S)[1])
        desc=unescape(re.search(r'<meta name="description" content="([^"]+)"',head)[1])
        assert (title,desc)==(row['title'],row['description']),row['url']+' metadata drift'
        assert title not in titles[row['language']],row['url']+' duplicate title within language'
        titles[row['language']].add(title)
        for prop,expected in [('og:title',title),('og:description',desc)]:
            found=re.search(r'<meta\b(?=[^>]*property="'+prop+r'")[^>]*content="([^"]*)"',head)
            assert found and unescape(found[1])==expected,row['url']+' '+prop+' missing or mismatched'
        pages=[]
        for raw in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',head,re.S):
            pages += [x for x in walk(json.loads(raw)) if x.get('@type') in ('WebPage','CollectionPage','Article') and x.get('url')==row['url']]
        assert len(pages)==1,(row['url'],'expected one page entity',len(pages))
        page=pages[0]
        code='zh-CN' if row['language']=='zh-cn' else row['language']
        assert (page.get('name'),page.get('description'),page.get('inLanguage'),page.get('@type'))==(title,desc,code,row['page_type']),row['url']+' schema drift'
        groups[row['source']].append(row)
    for route,items in groups.items():
        assert {x['language'] for x in items}=={'ko','en','ja','zh-cn'},route+' missing counterpart'
        assert len({x['page_type'] for x in items})==1,route+' page role differs by language'
    print(f'PASS search metadata parity: {len(groups)} four-language groups, {len(rows)} pages, unique titles within each language and matching page/OG/schema metadata.')
    print('This validates metadata contracts, not translation completeness, query demand, indexing, traffic or AI citations.')


if __name__=='__main__':main()
