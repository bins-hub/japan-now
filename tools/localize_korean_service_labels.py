"""Apply Korean service labels without changing destinations or other locales.

Run after HTML generators when rebuilding Korean pages.
"""
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
LABELS = {'LIVE': '실시간 카메라', 'NOW': '현지 날씨·상황',
          'RUN': '러닝 코스', 'EAT': '맛집', 'SEASON': '계절 여행',
          'ONSEN': '온천', 'MOVE': '교통·이동'}
PHRASES = {
    '일본 NOW 보기': '일본 현지 상황 보기',
    'NOW 날씨': '현지 날씨·상황', 'NOW 현지 날씨': '현지 날씨·상황',
    'NOW 지역 날씨': '현지 날씨·상황',
    'LIVE 카메라': '실시간 카메라', 'LIVE CAM': '실시간 카메라',
    '현지 LIVE 카메라': '현지 실시간 카메라',
    'LIVE 현지 카메라': '현지 실시간 카메라',
    'LIVE 현장 카메라': '현장 실시간 카메라',
    'LIVE 현지 화면': '실시간 현지 화면',
    'LIVE 현지 분위기': '실시간 현지 분위기',
    'EAT 맛집': '맛집', 'SEASON 계절 여행': '계절 여행',
    'MOVE 교통편': '교통·이동', 'MOVE 이동 방법': '교통·이동',
    'MOVE 경로 검색': '교통 경로 검색', 'MOVE 길찾기': '교통 길찾기',
    'MOVE 전체 보기': '교통·이동 전체 보기',
    'MOVE 전체 경로': '전체 교통 경로',
    '공항·관광지 교통 MOVE': '공항·관광지 교통·이동',
}
SERVICES = ('live/', 'now/', 'run-eat/', 'local-food/', 'season/', 'onsen/', 'move/')
ANCHOR = re.compile(r'<a\b[^>]*>.*?</a>', re.S | re.I)
TOKEN = re.compile(r'\b(' + '|'.join(LABELS) + r')\b')


def localize(source):
    if not re.search(r'<html\b[^>]*\blang=["\']ko["\']', source, re.I):
        return source

    def anchor(match):
        value = match.group()
        href = re.search(r'\bhref=["\']([^"\']+)', value)
        if not href:
            return value
        url = urlparse(urljoin('https://japulse.com/', href[1]))
        if url.netloc != 'japulse.com' or not any(url.path.startswith('/' + s) for s in SERVICES):
            return value
        opening, content = value.split('>', 1)
        def text_part(m):
            text = m.group()
            for old, new in sorted(PHRASES.items(), key=lambda item: -len(item[0])):
                text = text.replace(old, new)
            return TOKEN.sub(lambda token: LABELS[token[1]], text)
        content = re.sub(r'[^<>]+(?=<)', text_part, content)
        return opening + '>' + content

    result = ANCHOR.sub(anchor, source)
    result = result.replace('NOW · 일본 현지 상황 한눈에', '일본 현지 날씨·상황 한눈에')
    return result


if __name__ == '__main__':
    changed = []
    for path in ROOT.rglob('*.html'):
        if any(part in ('.git', 'audit', 'en', 'ja', 'zh-cn') for part in path.relative_to(ROOT).parts):
            continue
        before = path.read_text()
        after = localize(before)
        if after != before:
            path.write_text(after)
            changed.append(str(path.relative_to(ROOT)))
    print(f'Updated {len(changed)} Korean pages')
