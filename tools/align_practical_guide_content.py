"""Align guide/contact body content with Korean; preserve metadata and behavior."""
from pathlib import Path
import html,json,re

ROOT=Path(__file__).resolve().parent.parent
DATA=json.loads((ROOT/'content/guide-source-locales.json').read_text())
SLUGS=['travel-prep','where-to-watch','camera-troubleshooting']

def articles(rows):
    return ''.join('<article class="article"><h2>'+html.escape(title)+'</h2><p>'+body+'</p></article>' for title,body in rows)

def run():
    changed=[]
    for lang,copy in DATA.items():
        faq_label,camera_label,extra_label=copy['labels']
        for slug in SLUGS:
            path=ROOT/lang/'guides'/slug/'index.html'
            source=(ROOT/'guides'/slug/'index.html').read_text()
            source_directory=re.search(r'<article><h2>장소별 카메라 선택</h2>.*?</article>',source,re.S)[0]
            camera_slugs=re.findall(r'href="[^"]*/cameras/([^/]+)/"',source_directory)
            assert len(camera_slugs)==7
            camera_links=[]
            for camera in camera_slugs:
                local_camera=(ROOT/lang/'cameras'/camera/'index.html').read_text()
                title=re.sub('<[^>]+>','',re.search(r'<h1[^>]*>(.*?)</h1>',local_camera,re.S)[1])
                camera_links.append('<a class="tile" href="/'+lang+'/cameras/'+camera+'/">'+title+'</a>')
            text=path.read_text()
            start='<!-- JP SOURCE GUIDE START -->';end='<!-- JP SOURCE GUIDE END -->'
            if start in text:
                previous=re.search(re.escape(start)+r'(.*?)'+re.escape(end),text,re.S)[1]
                extras=re.search(r'<details id="jp-guide-extra-tips".*?</details>',previous,re.S)[0]
            else:
                core=re.search(r'<div class="details-layout"><div>((?:<article class="article">.*?</article>){4})',text,re.S)
                assert core,path
                # Keep existing destination/food/browser tips available without
                # presenting the old summary in place of the Korean source.
                tips=core[1].replace('<article class="article">','<div>').replace('</article>','</div>').replace('<h2>','<p><strong>').replace('</h2>','</strong></p>')
                extras='<details id="jp-guide-extra-tips" class="article"><summary>'+extra_label+'</summary>'+tips+'</details>'
            block=articles(copy[slug]['sections'])
            block+='<article class="article" id="jp-guide-source-faq"><h2>'+faq_label+'</h2>'+''.join('<div class="qa"><strong>'+html.escape(q)+'</strong><p>'+html.escape(a)+'</p></div>' for q,a in copy[slug]['faq'])+'</article>'+extras
            block+='<div class="article" id="jp-guide-source-cameras"><h2>'+camera_label+'</h2><div class="grid">'+''.join(camera_links)+'</div></div>'
            block=start+block+end
            if start in text:
                text=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda m:block,text,flags=re.S)
            else:
                # Only replace body content, ending immediately before the
                # already-localized related-guide sidebar.
                pattern=r'(<div class="details-layout"><div>).*?(</div><aside class="aside">)'
                text,n=re.subn(pattern,lambda m:m[1]+block+m[2],text,count=1,flags=re.S)
                assert n==1,path
            path.write_text(text);changed.append(str(path.relative_to(ROOT)))
        path=ROOT/lang/'contact/index.html';text=path.read_text()
        start='<!-- JP SOURCE CONTACT START -->';end='<!-- JP SOURCE CONTACT END -->'
        block=start+articles(copy['contact'])+end
        if start in text:
            text=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda m:block,text,flags=re.S)
        else:
            # Preserve the email CTA, sidebar, header and all existing scripts.
            text,n=re.subn(r'(<div class="details-layout"><div>)(?:<article class="article">.*?</article>){3}',lambda m:m[1]+block,text,count=1,flags=re.S)
            assert n==1,path
        path.write_text(text);changed.append(str(path.relative_to(ROOT)))
    print(json.dumps({'pages':len(changed),'paths':changed}))

if __name__=='__main__':run()
