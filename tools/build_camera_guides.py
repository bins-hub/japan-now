#!/usr/bin/env python3
"""Render reviewed, localized editorial guides as static HTML for all cameras.

Edit content/camera-guides.json, then run this script from any directory.
Existing players, metadata and source attribution are preserved.
"""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content/camera-guides.json').read_text())
LABELS = {
    'ko': ['화면을 읽는 방법', '방문 동선 계획', '공식 장소·교통 안내', '자료 확인', 'JAPULSE 편집 · 공식 장소 안내와 영상 활용 팁을 구분해 정리했습니다.'],
    'en': ['How to read the view', 'Plan your visit', 'Official place and transport information', 'Sources reviewed', 'Edited by JAPULSE · Official place information and camera-use tips are presented separately.'],
    'ja': ['映像の見方', '訪問ルートを考える', '場所・交通の公式案内', '資料確認日', 'JAPULSE編集 · 公式の場所案内と映像の活用方法を分けて整理しています。'],
    'zh-cn': ['如何看懂画面', '规划到访路线', '地点与交通官方信息', '资料核对日期', 'JAPULSE编辑 · 区分官方地点信息与画面使用建议。'],
}
START = '<!-- JAPULSE PLACE GUIDE START -->'
END = '<!-- JAPULSE PLACE GUIDE END -->'
CSS = 'https://japulse.com/assets/place-guide.css?v=20261026'


def render(place, lang):
    title, observation, route, question, answer = place[lang]
    read, visit, official, reviewed, credit = LABELS[lang]
    source_name, source_url = place['source']
    e = escape
    steps = ''.join('<li>' + e(step) + '</li>' for step in route)
    return (START + '<section class="jp-place-guide" aria-labelledby="jp-place-title">'
            '<h2 id="jp-place-title">' + e(title) + '</h2>'
            '<h3>' + read + '</h3><p>' + e(observation) + '</p>'
            '<h3>' + visit + '</h3><ol>' + steps + '</ol>'
            '<h3>' + e(question) + '</h3><p>' + e(answer) + '</p>'
            '<div class="jp-place-sources"><strong>' + official + '</strong><p><a href="'
            + e(source_url, quote=True) + '" target="_blank" rel="noopener noreferrer">'
            + e(source_name) + ' ↗</a></p><p>' + reviewed + ': <time datetime="'
            + DATA['reviewed'] + '">' + DATA['reviewed'] + '</time></p>'
            '<p>' + credit + '</p></div></section>' + END)


def main():
    changed = []
    for slug, place in DATA['places'].items():
        for lang in LABELS:
            path = ROOT / ('' if lang == 'ko' else lang) / 'cameras' / slug / 'index.html'
            old = path.read_text()
            section = render(place, lang)
            if START in old:
                new, count = re.subn(re.escape(START) + r'.*?' + re.escape(END), lambda _: section, old, flags=re.S)
            elif slug == 'haneda':
                anchor = '<p class="jp-camera-disclaimer">'
                assert old.count(anchor) == 1, path
                new = old.replace(anchor, section + anchor, 1)
                count = 1
            elif lang == 'ko':
                # Replace the two older travel cards (before FAQ) as one guide.
                articles = list(re.finditer(r'<article>.*?</article>', old, re.S))
                assert len(articles) >= 5 and '여행 전 참고하기' in articles[1].group(), path
                assert '자주 하는 질문' in articles[3].group(), path
                new = old[:articles[1].start()] + section + old[articles[2].end():]
                count = 1
            else:
                # The old Travel ideas card repeats broad region lists on each camera.
                pattern = r'<div class="article"><h2>[^<]+</h2>(?:(?!<div).)*?<h3>.*?</div>'
                new, count = re.subn(pattern, lambda _: section, old, flags=re.S)
            assert count == 1, (path, count)
            if CSS not in new:
                new = new.replace('</head>', '<link rel="stylesheet" href="' + CSS + '"></head>', 1)
            if new != old:
                path.write_text(new)
                changed.append(str(path.relative_to(ROOT)))
    # Advance lastmod only for the pages whose body changed.
    sitemap = ROOT / 'sitemap.xml'
    old = sitemap.read_text()
    new = old
    for path in changed:
        url = 'https://japulse.com/' + path.removesuffix('index.html')
        pattern = r'(<loc>' + re.escape(url) + r'</loc><lastmod>)[^<]+</lastmod>'
        new, count = re.subn(pattern, lambda m: m.group(1) + DATA['reviewed'] + '</lastmod>', new)
        assert count == 1, url
    if new != old:
        sitemap.write_text(new)
    print(json.dumps({'updated_camera_pages': len(changed)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
