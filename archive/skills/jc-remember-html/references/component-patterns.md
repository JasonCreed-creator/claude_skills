# component-patterns.md — 대시보드·문서·커뮤니케이션 패턴

모든 값은 tokens.md 정본 참조. HTML 산출물은 인라인 스타일 기준.

## 버튼
- Primary: bg `#EB6F2A` / 텍스트 white / r6~8 / hover bg `#B8431A`
- Secondary: 1.5px `#4A463F` 아웃라인 / 텍스트 brown / hover 반전(bg brown, 텍스트 paper)
- Ghost: 텍스트 `#B8431A` / hover bg `#FFF1E6`
- 패딩 10~13px × 20~24px, 600 weight

## 배지 (pill)
| 상태 | 배경 | 텍스트 |
|------|------|--------|
| 진행중 | `#FFF1E6` | `#B8431A` |
| 검토 | `#E8EEF3` | `#476580` |
| 완료 | `#E7EFE8` | `#196B24` |
| 지연·경고 | `#FBE9E9` | `#D93636` |

## KPI 카드
- surface + border 1px + r10~12 + 그림자 1단계, 패딩 18~24px
- 구조: 라벨(13~14px, ink-sub 600) → 수치(31~49px 700, tabular-nums, 단위는 warm-gray 400 분리) → 증감(positive/negative 600 + 비교기준 warm-gray)
- 다크 변형: surface `#2A2620` / border `#3E3931` / 수치 `#F4F0E9` / 실시간 강조 `#F08A4C`

## 테이블
- 헤더: bg `#F4F1EA`, 텍스트 brown 600 12px, letter-spacing 0.5px
- 행 구분: `#EFEBE2` 1px, 수치 우정렬 tabular-nums(목표는 ink-sub, 실적은 700)
- 카드형: surface + border + r10~12 + overflow hidden

## 수평 바 (채널·구성비)
- 트랙 `#F4F1EA` pill, 채움은 차트 시리즈 순서, 라벨 좌 / 수치 우(600)

## 문서 헤더 (제안서·리포트)
- 모노 킥커(10~11px, letter-spacing 2px, orange 600) + 우측 날짜(모노, warm-gray)
- 제목 25px 700 → 오렌지 룰(3~4px × 44~56px) → 리드 문단(14px, brown, line-height 1.7)

## 회의록 · Action Items
- 카드 헤더: 제목 + 진행중 배지(우측)
- 행: 항목 / 담당(warm-gray) / 기한(모노 — 임박 `#B8431A`, 여유 `#6E6E6E`)

## 링크
- `a { color: #B8431A }` · `a:hover { color: #EB6F2A }`

## 레이아웃 공통
- 페이지: paper 배경, 콘텐츠 max-width 1100~1240px
- 섹션 넘버링: 모노 01/02… orange + 섹션명 h2, 라이트/화이트 밴드 교차로 리듬
- 다크 밴드(운영·관제 맥락)는 페이지당 1개 이하
