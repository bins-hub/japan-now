"""Ensure FAQ structured data is backed by readable page content."""
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Content(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ignored = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'template'):
            self.ignored += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'template'):
            self.ignored -= 1

    def handle_data(self, data):
        if not self.ignored:
            self.parts.append(data)


def normalize(value):
    parser = Content()
    parser.feed(str(value))
    return re.sub(r'\s+', '', unescape(' '.join(parser.parts)))


def faq_nodes(value):
    if isinstance(value, dict):
        types = value.get('@type', [])
        types = types if isinstance(types, list) else [types]
        if 'FAQPage' in types:
            yield value
        for child in value.values():
            yield from faq_nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from faq_nodes(child)


def main():
    pages = ET.parse(ROOT / 'sitemap.xml').findall('{*}url/{*}loc')
    questions = 0
    errors = []
    for loc in pages:
        route = loc.text.removeprefix('https://japulse.com/')
        source = (ROOT / route / 'index.html').read_text()
        visible = normalize(source)
        for raw in re.findall(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', source, re.S | re.I):
            for faq in faq_nodes(json.loads(raw)):
                entities = faq.get('mainEntity', [])
                entities = entities if isinstance(entities, list) else [entities]
                if not entities:
                    errors.append(f'{route}: FAQPage has no mainEntity')
                for question in entities:
                    questions += 1
                    answers = question.get('acceptedAnswer', [])
                    answers = answers if isinstance(answers, list) else [answers]
                    for label, text in [('question', question.get('name', ''))] + [('answer', answer.get('text', '')) for answer in answers]:
                        if not normalize(text) or normalize(text) not in visible:
                            errors.append(f'{route}: {label} absent from readable HTML: {text}')
                    if not answers:
                        errors.append(f'{route}: acceptedAnswer missing')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS FAQ visibility: {len(pages)} indexed pages; {questions} questions and answers match readable HTML.')
    print('Checks content presence, not browser CSS visibility, rich-result eligibility or actual AI citations.')


if __name__ == '__main__':
    main()
