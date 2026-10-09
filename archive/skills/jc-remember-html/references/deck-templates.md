# deck-templates.md — 덱 템플릿 T1~T12 문법

16:9 기준. 모티프 어휘 2계열: ① 링·아크·그라디언트 카드(오렌지 계열 레퍼런스), ② 포토 풀블리드·다크 패널·캡슐 프로필(차콜 계열 레퍼런스 → charcoal `#332F29`로 이식). 그라디언트·다크 패널은 슬라이드당 1회.

## T1 · TITLE — 링 모티프 (라이트)
- surface 배경, 우하단에 화면 밖으로 잘리는 그라디언트 링(테두리만) + 작은 도트 1개
- 링 레시피: `border-radius:50%; border:26px solid transparent; background: linear-gradient(#FFF,#FFF) padding-box, linear-gradient(135deg,#EB6F2A,#F5A05A) border-box`
- 로고(black) 좌상단 → 타이틀 30~34px 700(핵심어만 orange) → 메타 캡션

## T2 · TITLE — 오브제 풀블리드 (다크)
- OBJ-03(라이트 슬릿) 등 오브제 배경 + `linear-gradient(90deg, rgba(20,18,16,0.72), rgba(20,18,16,0.25))` 오버레이
- 상하 1.5px 화이트 60% 룰 사이에 로고(offwhite)+타이틀, 우측에 모노 캡션(#F5A05A)

## T3 · CONTENTS — 서클 포토
- 좌 42%: 화면 밖으로 잘리는 원형 사진 + 그라디언트 도트 + tint 링
- 우: 목차 리스트(모노 번호 orange + 항목, line-soft 언더라인)

## T4 · 다크 패널 오버 포토
- 사진 풀블리드 위 중앙 charcoal 96% 패널(r12, 큰 그림자), 우측에 화이트 clip-path 사선
- 패널 내부: 모노 킥커(#F5A05A) → 제목 → 본문(#CFC8BC)

## T5 · SECTION DIVIDER — 그라디언트
- `linear-gradient(135deg,#E8641F,#F5A05A)` 풀블리드, 우상단 화이트 25% 링
- 로고(offwhite) / 섹션 번호(모노, 화이트 55%) / 섹션명 화이트 700 / 하단 요약 한 줄

## T6 · STAT CARDS
- 센터 타이틀 + 3열 카드: 그라디언트 헤더(태그 캡션+큰 수치) / 화이트 바디(항목명+설명)

## T7 · TIMELINE
- 5단계 그리드. 일반 단계: `#F3B48A` 상단 룰 + 모노 번호 orange. 현재 단계 1개만 그라디언트 카드(hero)

## T8 · 캡슐 프로필
- 2열 캡슐(pill, charcoal): 원형 사진 + 이름·역할(#F5A05A)·설명(#CFC8BC)

## T9 · 팀 포토 그리드
- 3열: 사진 영역 + charcoal 캡션 바(이름 화이트 / 역할 #F5A05A)

## T10 · CHART + INSIGHT
- 좌 60%: 바 차트(시계열 점증 — 과거 `#C9C9C0`→`#8C867A`→`#4A463F`→현재 `#EB6F2A`)
- 우: 인사이트 2건, `border-left: 3px solid` (주요 orange / 보조 line) + 큰 수치 + 한 줄 설명

## T11 · PROCESS
- 4단계 아이콘 박스(r10) 라인 연결. 일반 단계 charcoal, 핵심 단계 1개만 그라디언트

## T12 · CLOSING — 오브제 (다크)
- OBJ-06(코일) 우측 배치: `linear-gradient(90deg, rgba(20,18,16,0.96) 42%, rgba(20,18,16,0.35)), url(objet-06-coil.png); background-position: 78% center`
- 상단 화이트 50% 룰 → "감사합니다" 30px 700 → 연락처(#A89F92) → 로고(offwhite)

## 슬라이드 매핑 지침

| 콘텐츠 | 템플릿 |
|--------|--------|
| 표지 | T1(라이트 톤 덱) 또는 T2(임팩트·다크 오프닝) |
| 목차 | T3 |
| 행사/사업 개요 | T4 |
| 챕터 전환 | T5 (덱당 2~4회) |
| KPI·핵심 수치 | T6 |
| 로드맵·일정 | T7 |
| 조직·팀 | T8(내부 조직) / T9(연사·외부 인물) |
| 데이터·성과 | T10 |
| 방법론·프로세스 | T11 |
| 클로징 | T12 |

전체 덱에서 다크 슬라이드(T2·T4·T5·T12)는 30% 이하로 유지 — 웜 페이퍼가 기본 톤.
