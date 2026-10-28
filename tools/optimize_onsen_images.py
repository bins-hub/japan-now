"""Build same-origin responsive WebP copies of existing, attributed ONSEN photos.

Input: directory containing results.json and <index>.image downloads from the
existing source URLs. Does not change/crop the photo or replace its attribution.
"""
import argparse, hashlib, html, json, re
from pathlib import Path
from PIL import Image, ImageOps

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/onsen'
MANIFEST=OUT/'photos.json'

def build(source_dir):
    OUT.mkdir(parents=True,exist_ok=True)
    rows=json.loads((source_dir/'results.json').read_text())
    source=(ROOT/'onsen/index.html').read_text()
    # Read the original mapping from the source on the first run; preserve it
    # in the manifest so regenerating cannot confuse old and optimized URLs.
    if MANIFEST.exists():
        old=json.loads(MANIFEST.read_text())['photos']
        slugs={x['sourceUrl'].split('?')[0]:x['slug'] for x in old}
    else:
        slugs={url.split('?')[0]:slug for slug,url in re.findall(r'<a class="card" href="/onsen/([^/]+)/"[^>]*><img[^>]*src="([^"]+)"',source)}
    assert len(rows)==len(slugs)==15
    photos=[]
    for row in rows:
        assert 'error' not in row, row
        slug=slugs[row['url'].split('?')[0]]
        path=source_dir/f"{row['index']}.image"
        with Image.open(path) as raw:
            im=ImageOps.exif_transpose(raw).convert('RGB')
            candidates=[]
            for width in sorted({min(w,im.width) for w in [360,650,960]}):
                size=(width,round(im.height*width/im.width))
                photo=im.resize(size,Image.Resampling.LANCZOS)
                import io
                buffer=io.BytesIO()
                photo.save(buffer,format='WEBP',quality=77,method=6)
                data=buffer.getvalue();digest=hashlib.sha256(data).hexdigest()[:10]
                name=f'{slug}-{width}-{digest}.webp'
                (OUT/name).write_bytes(data)
                candidates.append({'width':width,'height':size[1],'url':'/assets/onsen/'+name,'bytes':len(data)})
        source_page=(ROOT/'onsen'/slug/'index.html').read_text()
        caption=re.search(r'<figure class="onsen-photo">.*?(<figcaption>.*?</figcaption>)',source_page,re.S)[1]
        photos.append({'slug':slug,'sourceUrl':row['url'],'resolvedSourceUrl':row['final'],
                       'sourceBytes':row['bytes'],'sourceFetchSeconds':row['seconds'],
                       'attributionHtml':caption,'changes':'Resized and WebP encoded; no crop or content changes. Original license and credit links retained on each guide.',
                       'variants':candidates})
    MANIFEST.write_text(json.dumps({'version':1,'quality':77,'photos':photos},ensure_ascii=False,indent=2)+'\n')
    return photos

def apply(photos):
    sources={p['sourceUrl'].split('?')[0]:p for p in photos}
    local={v['url']:p for p in photos for v in p['variants']}
    count=0
    for prefix in ['', 'en/', 'ja/', 'zh-cn/']:
        for path in (ROOT/prefix/'onsen').rglob('index.html'):
            is_main=path.parent.name=='onsen'
            index=0
            def update(m):
                nonlocal index
                tag=m[0];src=re.search(r'\bsrc="([^"]+)"',tag)
                if not src:return tag
                photo=sources.get(src[1].split('?')[0]) or local.get(src[1])
                if not photo:return tag
                variants=photo['variants']
                default=next((v for v in variants if v['width']>=650),variants[-1]) if is_main else variants[-1]
                tag=re.sub(r'\bsrc="[^"]+"','src="'+default['url']+'"',tag)
                for attr in ['srcset','sizes','loading','fetchpriority']:
                    tag=re.sub(r'\s'+attr+r'="[^"]*"','',tag)
                sizes='(max-width: 600px) calc(100vw - 40px), (max-width: 1000px) 45vw, 360px' if is_main else '(max-width: 700px) calc(100vw - 40px), 1000px'
                priority='high' if index==0 else 'auto'
                loading='eager' if not is_main or index<3 else 'lazy'
                attrs=' srcset="'+', '.join(v['url']+' '+str(v['width'])+'w' for v in variants)+'" sizes="'+sizes+'" loading="'+loading+'" fetchpriority="'+priority+'"'
                index+=1
                return tag[:-1]+attrs+'>'
            before=path.read_text();after=re.sub(r'<img\b[^>]*>',update,before)
            assert index==(15 if is_main else 1), (path,index)
            path.write_text(after);count+=1
    return count

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-dir',type=Path)
    args=parser.parse_args()
    photos=build(args.source_dir) if args.source_dir else json.loads(MANIFEST.read_text())['photos']
    count=apply(photos)
    before=sum(p['sourceBytes'] for p in photos)
    card=sum(next((v['bytes'] for v in p['variants'] if v['width']>=650),p['variants'][-1]['bytes']) for p in photos)
    print(json.dumps({'pages':count,'photos':len(photos),'originalBytes':before,'cardWebpBytes':card,'reductionPercent':round((1-card/before)*100,1)}))
