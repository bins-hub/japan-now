"""Remove header service links already shown in the seven-item service menu."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
PAGE = re.compile(r"<header\b[^>]*>.*?</header>", re.S | re.I)
NAV = re.compile(r"<nav\b[^>]*>.*?</nav>", re.S | re.I)
ANCHOR = re.compile(r"<a\b[^>]*>.*?</a>", re.S | re.I)
HREF = re.compile(r'\bhref=["\']([^"\']+)["\']', re.I)
SERVICES = ('live/', 'now/', 'run-eat/', 'local-food/', 'season/', 'onsen/', 'move/')


class Navigation(HTMLParser):
    def __init__(self):
        super().__init__()
        self.global_menu = False

    def handle_starttag(self, tag, attrs):
        if tag == 'nav' and 'jp-global-services' in dict(attrs).get('class', '').split():
            self.global_menu = True


def route(href, base):
    url = urlparse(urljoin('https://japulse.com' + base, href))
    return url.path if url.netloc == 'japulse.com' and not url.fragment else None


def update(path):
    original = path.read_text()
    parsed = Navigation()
    parsed.feed(original)
    if not parsed.global_menu:
        return 0
    base = '/' + str(path.relative_to(ROOT).parent).replace('\\', '/') + '/'
    if base == '/./':
        base = '/'
    locale = next((x for x in ('en/', 'ja/', 'zh-cn/') if base.startswith('/' + x)), '')
    destinations = {'/' + locale + x for x in SERVICES}
    count = 0

    def header_change(match):
        def nav_change(nav):
            nonlocal count
            def anchor_change(anchor):
                nonlocal count
                found = HREF.search(anchor.group())
                if found and route(found.group(1), base) in destinations:
                    count += 1
                    return ''
                return anchor.group()
            return ANCHOR.sub(anchor_change, nav.group())
        return NAV.sub(nav_change, match.group())

    result = PAGE.sub(header_change, original, count=1)
    if path.relative_to(ROOT).as_posix() in ('onsen/index.html', 'en/onsen/index.html', 'ja/onsen/index.html', 'zh-cn/onsen/index.html'):
        # The price shortcut should focus the existing price control, not repeat day-use.
        pattern = re.compile(r'(<div class="visitor-shortcuts">.*?<a href=")#facility-finder("[^>]*>[^<]*(?:가격|price|料金|价格)[^<]*</a>)', re.S | re.I)
        result, n = pattern.subn(r'\1#facility-price\2', result, count=1)
        if n != 1 and 'href="#facility-price"' not in result.split('<div class="visitor-shortcuts">', 1)[1].split('</div>', 1)[0]:
            raise ValueError(f'Price shortcut not found: {path}')
        count += n
    if result != original:
        path.write_text(result)
    return count


if __name__ == '__main__':
    changed = Counter()
    for item in ROOT.rglob('index.html'):
        if 'audit' in item.relative_to(ROOT).parts:
            continue
        n = update(item)
        if n:
            changed['pages'] += 1
            changed['links'] += n
    print(dict(changed))
