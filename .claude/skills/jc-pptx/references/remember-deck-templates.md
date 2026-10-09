# Remember Deck Templates — T1~T12 문법 + DS 슬라이드 01~10 레시피

16:9 기준. 모티프 어휘 2계열: ① 링·아크·그라디언트 카드(오렌지 계열) ② 포토 풀블리드·다크 패널·캡슐 프로필(차콜 `#332F29`). 그라디언트·다크 패널은 슬라이드당 1회. 값은 `jc-design-system` 토큰, 구현은 `scripts/deck_kit.py`.

## A. DS 슬라이드 10종 (Claude Design 정본, 1920×1080)

| # | 이름 | 레시피 | deck_kit |
|---|------|--------|----------|
| 01 | 표지(다크) | 배경 `#141210`, 우측 오브제 03 폭 620 + `linear-gradient(90deg,#141210,transparent)` 페이드, y122·y972 화이트 60% 1.5px 룰, 좌상단 발주처 로고 슬롯(h72), 우상단 `PROPOSAL · 날짜`(20px 자간 .2em `#F5A05A`), 아이브로우 `행사 기획·운영 제안서`(28px `#F08A4C`), 제목 88px `#F4F0E9` 폭 1200, 슬로건 32px `#CFC8BC`, 하단 발행 명의 20px + 우하단 로고 offwhite h26 | `cover(dark=True)` |
| 02 | 목차 | 라이트. 모노 번호 orange + 항목 30px, 행 구분 `#EFEBE2`. 우측 여백에 그라디언트 도트 1개 | `contents()` |
| 03 | 섹션(다크) | 배경 `#141210`, 고스트 넘버 200pt+ 저대비(`#F4F0E9` 12%), `SECTION NN` 22px `#F08A4C`, 섹션명 64px, 한 줄 요약 30px `#CFC8BC`. 오브제 선택 | `section_divider(style="dark")` |
| 04 | 요약 카드 | 3열 카드(흰·1px 보더·r10·패딩 36/40), 카드 상단 모노 킥커 orange + 제목 44px + 본문 26px. 핵심 1개는 상단 그라디언트 룰 9px | `numbered_cards(highlight=i)` |
| 05 | 본문 + 표 | 좌 텍스트 520px(헤드 44 + 본문 26) + 우 표(헤더 캡션색 20px + 1.5px 잉크 하단선, 행 1px `#DCD6C8`, 셀 24px, 첫 열 600) | `table()` |
| 06 | 타임테이블 | 시간 열 모노 tabular, 세그먼트·내용·담당 열. 핵심 세션 행 배경 `#FFF1E6`. 우측 `◎ 권장` 표기 | `table(highlight_rows=[…])` |
| 07 | KPI | 솔리드 KPI 1개(그라디언트, 흰 96px) + 카드 KPI 2~3개(orange 96px, 라벨 22px 캡션색, 하단 설명 22px brown) | `kpi(solid=True)` + `kpi()` |
| 08 | 인력 | 4열 프로필: 원형 사진(또는 이니셜 원) + 이름 30px + 역할 22px `#B8431A` + 담당 26px. 다크 변형은 charcoal 캡슐 | `profile_capsules()` |
| 09 | 견적 요약 | 좌 KPI(총액, VAT 별도 캡션) + 우 섹션별 표. 권장 옵션 열 orange | `kpi()` + `table()` |
| 10 | 클로징(다크) | 배경 `#141210`, 우측 오브제 06 코일(`background-position 78% center`, 좌측 96%→35% 페이드), 상단 화이트 50% 룰, "감사합니다" 60px, 연락처 22px `#A89F92`, 로고 offwhite | `closing()` |

## B. T1~T12 HTML 문법 (구 jc-remember-html v1.0.0 흡수 — 현 정본 jc-design-system)

> HTML 원문은 역사 참조, 빌드는 deck_kit — CSS 스니펫은 모티프 설명용이며 PPTX는 각 항목의 `→ deck_kit` 메서드(없으면 `box()`·`grad()`·`ring()` 조합)로 만든다.

### T1 · TITLE — 링 모티프 (라이트, 소개서 표지)
- surface 배경, 우하단 화면 밖으로 잘리는 그라디언트 링(테두리만) + 작은 도트 1개
- 링: `border-radius:50%; border:26px solid transparent; background: linear-gradient(#FFF,#FFF) padding-box, linear-gradient(135deg,#EB6F2A,#F5A05A) border-box`
- 로고(black) 좌상단 → 타이틀 30~34pt 700(핵심어만 orange) → 메타 캡션 → `cover(dark=False)`

### T2 · TITLE — 오브제 풀블리드 (다크) = DS 01

### T3 · CONTENTS — 서클 포토
- 좌 42%: 화면 밖으로 잘리는 원형 사진 + 그라디언트 도트 + tint 링 / 우: 목차 리스트(모노 번호 orange, line-soft 언더라인)

### T4 · 다크 패널 오버 포토
- 사진 풀블리드 위 중앙 charcoal 96% 패널(r12, 큰 그림자), 우측 화이트 clip-path 사선. 패널 내부: 모노 킥커(`#F5A05A`) → 제목 → 본문(`#CFC8BC`)

### T5 · SECTION DIVIDER — 그라디언트
- `linear-gradient(135deg,#E8641F,#F5A05A)` 풀블리드, 우상단 화이트 25% 링, 로고 offwhite / 섹션 번호(화이트 55%) / 섹션명 화이트 700 / 하단 요약 → `section_divider(style="gradient")`

### T6 · STAT CARDS
- 센터 타이틀 + 3열 카드: 그라디언트 헤더(태그 캡션 + 큰 수치) / 화이트 바디(항목명 + 설명)

### T7 · TIMELINE
- 5단계 그리드. 일반 단계 `#F3B48A` 상단 룰 + 모노 번호 orange. 현재 단계 1개만 그라디언트 카드

### T8 · 캡슐 프로필
- 2열 캡슐(pill, charcoal): 원형 사진 + 이름·역할(`#F5A05A`)·설명(`#CFC8BC`) → `profile_capsules(dark=True)`

### T9 · 팀 포토 그리드
- 3열: 사진 + charcoal 캡션 바(이름 화이트 / 역할 `#F5A05A`)

### T10 · CHART + INSIGHT
- 좌 60% 바 차트(시계열 점증 `#C9C9C0`→`#8C867A`→`#4A463F`→`#EB6F2A`) / 우 인사이트 2건 `border-left:3px solid`(주요 orange / 보조 line) + 큰 수치 + 한 줄

### T11 · PROCESS
- 4단계 아이콘 박스(r10) 라인 연결. 일반 charcoal, 핵심 1개만 그라디언트 → `step_cards()`

### T12 · CLOSING — 오브제 (다크) = DS 10

## C. 슬라이드 매핑 지침

| 콘텐츠 | 템플릿 |
|--------|--------|
| 표지 | DS 01(제안서) / T1(소개서·라이트 톤) |
| 목차 | DS 02 / T3(사진 있을 때) |
| 행사·사업 개요 | DS 05 / T4 |
| 챕터 전환 | DS 03 (덱당 2~4회) / T5 |
| KPI·핵심 수치 | DS 07 / T6 |
| 로드맵·일정 | DS 06 / T7 |
| 조직·팀 | DS 08 / T8(내부) / T9(연사·외부) |
| 데이터·성과 | T10 |
| 방법론·프로세스 | T11 |
| 견적 요약 | DS 09 |
| 클로징 | DS 10 |

다크 슬라이드(DS 01·03·10, T2·T4·T5·T12)는 덱 전체 30% 이하.

## D. 실증 레시피 포인터 (`scripts/examples/build_deck2.py`)

| 함수 | 슬라이드 | 재사용 포인트 |
|------|---------|---------------|
| `s_quote` | 문제 정의(인용 + KPI 3) | 솔리드 KPI 1 + 카드 KPI 2, 출처 캡션, 테이크어웨이 |
| `s_funnel` | 쇼업 절벽·타깃 공백 | 수평 바 트랙 + 우측 카드 인사이트 |
| `s_links` | 3고리 구조 | 강조 카드 3 + 셰브론 + 하단 웜 서피스 밴드 |
| `s_data` / `s_target` | 데이터 풀·타깃 4단계 | KPI 4열 + 조건 pill, 단계 카드 + charcoal DROP 바 |
| `s_compare` | Before/After | 좌 뮤트 카드 / 우 강조 카드(상단 그라디언트 룰) |
| `s_timeline` `s_scope` `s_formats` | 운영 범위 | 타임라인 카드, 범위 표 |
| `s_org` `s_leader` `s_members` `s_dataleaders` | 팀 | 프로필 카드·캡슐, 팀장 강조 |
| `s_venue` `s_collage` `s_reftable` | 레퍼런스 | 사진 그리드 + 표(실명 동의 확인) |
| `s_closing` | 클로징 | 오브제 + 연락처 + 로고 |
