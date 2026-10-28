"""Repair crawlable locale navigation and reciprocal indexing signals, without runtime redirects."""
from pathlib import Path
from urllib.parse import urlsplit
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = 'https://japulse.com'
LOCALES = {'ko': '', 'en': 'en/', 'ja': 'ja/', 'zh-CN': 'zh-cn/'}
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
XHTML = 'http://www.w3.org/1999/xhtml'

def run():
    tree = ET.parse(ROOT / 'sitemap.xml')
    changed_links = 0
    for entry in tree.getroot().findall(f'{{{NS}}}url'):
        url = entry.find(f'{{{NS}}}loc').text
        route = urlsplit(url).path.lstrip('/')
        file = ROOT / (route + 'index.html' if route.endswith('/') or not route else route)
        html = file.read_text()
        prefix = next((p for p in LOCALES.values() if p and route.startswith(p)), '')
        base = route[len(prefix):]
        if base:
            html = re.sub(r'<nav\b(?=[^>]*(?:class="(?:jp-lang|langs)"|aria-label="Language[^\"]*"|id="jp-language-route-switch"))[^>]*>.*?</nav>', '', html, flags=re.S)
        # Language links remain visible on the homepage only.
        held = []
        def hold(m):
            held.append(m[0])
            return f'<!--LOCALE_NAV_{len(held)-1}-->'
        if prefix:
            if base == '':
                html = re.sub(r'<nav\b[^>]*class="jp-lang"[^>]*>.*?</nav>', hold, html, flags=re.S)
            def localize(m):
                nonlocal changed_links
                before, href, after = m.groups()
                parsed = urlsplit(href)
                if parsed.netloc not in ('', 'japulse.com') or not parsed.path.startswith('/'):
                    return m[0]
                path = parsed.path.lstrip('/')
                if any(p and path.startswith(p) for p in LOCALES.values()):
                    return m[0]
                target = ROOT / prefix / (path + 'index.html' if not path or path.endswith('/') else path)
                if target.is_file() and target.suffix == '.html':
                    changed_links += 1
                    href = (ORIGIN if parsed.netloc else '') + '/' + prefix + path
                    if parsed.query: href += '?' + parsed.query
                    if parsed.fragment: href += '#' + parsed.fragment
                    return before + href + after
                return m[0]
            html = re.sub(r'(<a\b[^>]*\bhref=")([^"]+)(")', localize, html)
            for i, nav in enumerate(held): html = html.replace(f'<!--LOCALE_NAV_{i}-->', nav)
        # Every translated counterpart exists; expose all five reciprocal signals.
        html = re.sub(r'<link\b(?=[^>]*\brel="alternate")(?=[^>]*\bhreflang=)[^>]*>', '', html)
        alternates = {lang: ORIGIN + '/' + p + base for lang, p in LOCALES.items()}
        alternates['x-default'] = ORIGIN + '/' + base
        html = html.replace('</head>', ''.join(f'<link rel="alternate" hreflang="{lang}" href="{href}">' for lang, href in alternates.items()) + '</head>')
        for item in list(entry):
            if item.tag == f'{{{XHTML}}}link': entry.remove(item)
        for lang, href in alternates.items():
            ET.SubElement(entry, f'{{{XHTML}}}link', {'rel': 'alternate', 'hreflang': lang, 'href': href})
        if prefix and base == '':
            html = html.replace('8H3nRCFVR6Y', 'dfVK7ld38Ys').replace('i2PpmC1IeKk', '6OgYfTMOmhY')
            html = re.sub(r'home-live\.(js|css)\?v=[^"\s]+', r'home-live.\1?v=20261028-audit', html)
            html = re.sub(r'(<nav class="jp-menu"[^>]*>)(.*?)(</nav>)', lambda m: m[1] + m[2] + ''.join(f'<a href="/{prefix}{section}/">{section.upper()}</a>' for section in ['season', 'onsen', 'move']) + m[3] if '/season/' not in m[2] else m[0], html, flags=re.S)
        html = re.sub(r'weather\.js\?v=[^"\s]+', 'weather.js?v=20261028-timeout', html)
        file.write_text(html)
    ET.register_namespace('', NS)
    ET.register_namespace('xhtml', XHTML)
    tree.write(ROOT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    print(f'Repaired {changed_links} locale-preserving anchors; reciprocal hreflang on every sitemap page.')

if __name__ == '__main__': run()
