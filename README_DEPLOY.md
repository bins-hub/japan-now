# JAPAN NOW — GitHub Pages 배포 준비본

대상 GitHub 계정: `bins-hub`  / 제안하는 **새 공개 저장소 이름**: `japan-now`

## 사용자가 GitHub에서 해야 할 일

1. <https://github.com/new>에서 `japan-now` 이름의 새 저장소를 **Public**으로 생성하세요. 기존 비공개 `youtube-trend-radar` 저장소는 사용하지 마세요.
2. 생성된 저장소의 **Add file → Upload files**에서 이 ZIP을 해제한 **폴더 안의 내용물**을 모두 업로드 후 Commit changes를 누르세요. ZIP 파일 자체를 업로드해서는 사이트가 뜨지 않습니다.
3. 저장소의 **Settings → Pages → Build and deployment → Deploy from a branch → main / (root) → Save**를 설정하세요.
4. 배포가 성공하면, **예상 주소**는 `https://japulse.com/` 입니다. 도메인 소유권과 배포 확인 전에는 실제 작동한다고 보장할 수 없습니다.
5. 최신 디자인 홈페이지는 `/`, 기존 카메라 목록 UI는 `/classic.html`, 데모 페이지는 `/preview.html` 입니다.

## SEO·GEO 설정

`https://japulse.com/` 를 기준으로 24개 canonical URL 및 `sitemap.xml`을 미리 설정했습니다. **저장소 이름을 다르게 만들면** 업로드 전에 `python3 tools/configure_domain.py https://bins-hub.github.io/새저장소이름` 을 다시 실행해야 합니다.

배포 후 Google Search Console에 `https://japulse.com/sitemap.xml` 을 등록하세요. AI 검색에 반드시 노출되는 것은 아닙니다.

## 공개 전 확인 사항

- 카메라 원본 링크는 방송 종료, 소유자 외부 삽입 제한, 지역제한으로 재생 실패할 수 있습니다.
- 주변 관광명소/먹거리 정보는 안내용으로, 공식 영업시간 및 실제 운영 정보를 직접 확인해야 합니다.
- 개인 정보 처리방침 및 문의 정보는 운영자 정보가 입력되기 전까지 초안입니다.
- 사이트를 상업적으로 사용하기 전 이미지·영상 이용 약관을 확인하세요.
