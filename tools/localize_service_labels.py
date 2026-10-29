"""Localize service-link labels after HTML generation; preserve URLs and markup."""
from html import escape, unescape
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content/service-labels.json').read_text())
SERVICES = ('live', 'now', 'run-eat', 'local-food', 'season', 'onsen', 'move')
TOKEN = re.compile(r'\b(?:LIVE|NOW|RUN|EAT|SEASON|ONSEN|MOVE)\b')
ANCHOR = re.compile(r'<a\b[^>]*>.*?</a>', re.S | re.I)
HOME_CSS = '.jp-bar-inner{flex-wrap:wrap}.jp-menu{flex-wrap:wrap;max-width:100%}@media(max-width:900px){.jp-menu{flex-basis:100%;margin-left:0}}'


def localize(source, locale, route):
    data = DATA[locale]
    def change(match):
        value = match.group()
        href = re.search(r'\bhref=["\']([^"\']+)', value)
        if not href:
            return value
        url = urlparse(urljoin('https://japulse.com/' + route, unescape(href[1])))
        service = any(url.path.startswith('/' + locale + '/' + s + '/') for s in SERVICES)
        home_camera = url.path == '/' + locale + '/' and url.fragment in ('live', 'cameras')
        if url.netloc != 'japulse.com' or not (service or home_camera):
            return value
        opening, content = value.split('>', 1)
        def text_part(m):
            text = unescape(m.group())
            text = text.replace('LIVE CAM', data['labels']['LIVE'])
            for old, new in sorted(data['phrases'].items(), key=lambda item: -len(item[0])):
                text = text.replace(old, new)
            text = TOKEN.sub(lambda token: data['labels'][token[0]], text)
            return escape(text, quote=False)
        content = re.sub(r'[^<>]+(?=<)', text_part, content)
        return opening + '>' + content
    result = ANCHOR.sub(change, source)
    old, new = data['teaser']
    result = result.replace('<h2>' + old + '</h2>', '<h2>' + escape(new, quote=False) + '</h2>')
    if route == locale + '/' and HOME_CSS not in result:
        result = result.replace('<style id="jp-home-seven-tabs">', '<style id="jp-home-seven-tabs">' + HOME_CSS, 1)
    return result


if __name__ == '__main__':
    for locale in DATA:
        changed = 0
        for path in (ROOT / locale).rglob('index.html'):
            before = path.read_text()
            route = path.relative_to(ROOT).as_posix().removesuffix('index.html')
            after = localize(before, locale, route)
            if after != before:
                path.write_text(after)
                changed += 1
        print(f'{locale}: {changed} pages updated')
