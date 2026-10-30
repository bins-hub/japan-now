# 콘텐츠 가치 개선 2차 — 공항 교통 선택 (미배포)

기준 main `83b9ec4`는 그대로다. 1차 원격 커밋 `9ba46b60c0f6a4e83d66cc2ce6075ecf96ef7f34`와 로컬 1차 `aefeb66`은 동일 tree임을 확인한 후 원격 1차에서 새 작업 브랜치 `content/airport-value-phase2-20261030`를 만들었다. 1차 나리타를 재개발하지 않았다. 복구 지점은 원격 1차 커밋이며 백업 이름은 `backup/pre-airport-value-phase2-20261030`.

## 이번 변경: 20페이지

하네다→시나가와 / 하마마쓰초, 간사이→난바, 신치토세→삿포로 상세 4경로 × 4언어 = 16페이지. MOVE 목록 4언어도 함께 갱신했다.

| 경로 | 이전 | 개선 후 |
|---|---|---|
| 하네다→시나가와 | 운임은 공식 검색에서 확인 | 게이큐 종이표 330엔, 모노레일 520엔+JR 비교. 시나가와 숙소에 게이큐를 우선할 근거, T3 도쿄 방면 개찰구 위치와 JR 연결 승차권 설명 |
| 하네다→하마마쓰초 | 승차역·운임 공식 조회 | 종이표 520엔·IC 519엔·어린이 260/259엔. 약 20분 안내 기준, 숙소 도보와 JR 추가 구간 구분 |
| 간사이→난바 | 추가 특급권 700엔만 제시 | 공항급행 970엔 / 라피트 레귤러 총 1,670엔 / 공식 티켓리스 레귤러 총 1,520엔 비교. 기본권·특급권 구분과 차내 구매 300엔 추가. 급행 비용과 좌석 지정의 선택 근거 |
| 신치토세→삿포로 | 자유석 1,230엔·지정석 2,230엔, 범용 FAQ | 기존 금액 재확인, 에키넷 티켓리스 지정 800엔+기본 1,230엔=2,030엔 추가. 지정석 4호차/IC 입장, 33·37·43분 열차 종류 구분, B1F 역 위치 |

목록 카드의 상세 펼침에도 같은 가격을 반영해 목록과 상세가 모순되지 않게 했다. 요금 외 열차 대기·도보가 실제 일정에 미치는 영향은 추천 근거로 설명했다. 날짜별 정확한 첫차·막차는 해당 항목만 미확인으로 표시했다.

## 출처와 날짜

2026-10-30 조회. 원문 게시일·자료 기준일과 조회일은 다르다.

- [게이큐 운임 예시](https://www.keikyu.co.jp/ride/ticket/): 시나가와~T3 330엔. T1/2도 330엔은 [ANA의 게이큐 승차권 안내](https://www.ana.co.jp/ja/jp/shoppingandlife/airport/tameru_keikyu_ticket/)와 대조. IC 327엔은 이번 표에 새로 제시하지 않았다.
- [게이큐 소요시간·JR 연결](https://www.haneda-tokyo-access.com/en/ride/fares.html)
- [하네다공항 개찰구·소요시간](https://www.tokyo-haneda.com/en/access/train/index.html)
- [모노레일 운임표](https://www.tokyo-monorail.co.jp/english/guidance/train_info.html)
- [난카이 현재 특급 요금](https://www.nankai.co.jp/en_railway/traffic/express/rapit.html): 700엔, 공식 티켓리스 150엔 할인, 차내 300엔 가산.
- [난카이 시간 안내](https://www.nankai.co.jp/en_railway/access-fromkix): 라피트 최단34분·공항급행 약45분.
- [공항 직영 면세점 교통 자료](https://www.kixdutyfree.jp/en/kansai_airport_access_guide_info.html): 기본970엔 참고. **이 문서는 2024-10-28 기준**이며 라피트 총1,490엔은 현재 특급요금과 달라 채택하지 않았다. 기본970엔은 난카이 공식 검색 결과 및 2026-10-29/30 교통검색 결과와 일치한다. 조회를 최신 운임 개정 공지라고 쓰지 않는다.
- [JR 홋카이도 일반 운임](https://www.jrhokkaido.co.jp/global/english/ticket/regular/index.html)
- [JR 에어포트 탑승·편성](https://www.jrhokkaido.co.jp/global/english/travel/airport.html)
- [JR 2026 지정석 요금 개정](https://www.jrhokkaido.co.jp/CM/Info/press/pdf/20251212_KO_reservedseatfee.pdf): 2026-03-14 탑승부터 종이1,000엔·에키넷 티켓리스800엔. 2,030엔은 기본운임과의 합산값이며 모든 예약 채널의 공통 가격이 아니다.
- [신치토세 JR역 위치](https://www.hokkaido-airports.com/en/new-chitose/access/jr/)

원문을 그대로 옮기지 않고 비용·환승·좌석·숙소 위치에 따른 선택을 편집했다. 현장 체험으로 표현하지 않았다.

## 검증·보존

- 기존 자동검사14개 모두 통과: `phase2-tests.json`.
- 20페이지 script/schema·H1·canonical/hreflang 보존과 목록 카드별 해당 가격 확인: `phase2-preservation.json`. 기존 지도 링크·검색·필터·플레이어 수정 없음.
- 4언어 표 행·금액·합계·조건을 한국어 기준 동일하게 작성. ONSEN/MOVE 구조 검사102페이지 통과.
- `content/airport-decision-guides.json`이 이번 편집 데이터. `tools/improve_airport_decisions.py`를 기존 생성·현지화 도구 뒤에 실행한다. 두 번째 실행 변경0. 나리타 편집기는 별도로 유지.
- 새 공통 CSS는 표 셀 줄바꿈·표 내부 스크롤·키보드 초점 지원. 실제 좁은 화면 렌더링·터치·외부 구매 흐름은 미검증이다. 이전에 확인된 브라우저 실행 파일 부재를 해소하지 못했으며 정적 반응형 검사 통과만 기록한다.
- sitemap의 해당20개 lastmod만 갱신. main 병합·공개 배포 없음. 원격 tree가 로컬 tree와 일치하는지 확인해 보존한다.

## 다음 미완료

1. 간사이→교토·신오사카: 11월1일 HARUKA 할인권 가격 변경의 구매일/이용일 적용, 여권·체류자격·좌석 조건을 원문에서 확인하고 목록에 반영. 기존 날짜별 가격 문구만으로 모든 조건이 확인됐다고 보지 않는다.
2. 긴잔 온천: 시로가네유의 실제 이용조건을 FAQ의 직접 답변으로 연결하고 버스·주차·야간 방문을 조사.
3. SEASON 삿포로: 무료 공원과 유료 모이와산, 영업시간·비용·이동을 구분.
4. RUN/EAT 및 LIVE/NOW: 1차 보고서의 미완료 계획 유지.

누적 고유 개선 페이지는 **28개**: 나리타 상세8 + 이번 상세16 + 공통 목록4. 작업량12+20=32를 고유 페이지 수로 보고하지 않는다. 사이트 전체252페이지의 사실 검증 완료도 아니다. 승인 없이 배포하지 않는다.
