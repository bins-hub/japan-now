"""Put practical localized guide content first and make duplicate descriptions page-specific."""
from pathlib import Path
from collections import Counter
from html import unescape,escape
import re
ROOT=Path(__file__).resolve().parent.parent

def take_div(html, ident):
    start=html.find('<div id="'+ident+'">')
    if start<0:return html,''
    depth=0
    for m in re.finditer(r'</?div\b[^>]*>',html[start:]):
        depth+=-1 if m[0].startswith('</') else 1
        if depth==0:
            end=start+m.end()
            return html[:start]+html[end:],html[start:end]
    raise ValueError('Unbalanced guide block '+ident)

def run():
    fixed=0
    for lang in ['en','ja','zh-cn']:
        pages=list((ROOT/lang).rglob('index.html'))
        descriptions=Counter(re.search(r'<meta name="description" content="([^"]*)"',p.read_text())[1] for p in pages)
        for p in pages:
            h=p.read_text();blocks=[]
            for ident in ['jp-onsen-context','jp-season-photos','jp-season-places','jp-tokyo-winter-details']:
                h,block=take_div(h,ident)
                if block:blocks.append(block)
            if blocks:h=re.sub(r'(<h1\b[^>]*>.*?</h1>)',lambda m:m[1]+''.join(blocks),h,count=1,flags=re.S)
            m=re.search(r'<meta name="description" content="([^"]*)"',h)
            if descriptions[m[1]]>1:
                title=unescape(re.sub('<[^>]+>','',re.search(r'<h1\b[^>]*>(.*?)</h1>',h,re.S)[1]))
                desc=title+'. '+unescape(m[1])
                h=h.replace(m[0],'<meta name="description" content="'+escape(desc,quote=True)+'">');fixed+=1
            p.write_text(h)
    print(f'Put localized practical content before directory CTAs; made {fixed} duplicate descriptions page-specific.')
if __name__=='__main__':run()
