---
name: jc-design-system
description: 리멤버 MICE비즈팀 산출물(제안서·소개서 PPTX, 문서·대시보드·캔버스 HTML, 견적·큐시트 xlsx, 대본 docx)의 디자인 토큰 정본이자 스킬 간 데이터 봉투(ChainPayload/v1) 정본. 룩은 '리멤버 웜 페이퍼'(웜 아이보리 캔버스 · 잉크 블랙 · 리멤버 오렌지 액센트 · Pretendard 단일 서체) 하나이며, 다른 스킬(jc-pptx·mice-ops-docs·pt-script·mice-meeting-minutes·mice-run-of-show·mice-aftermath 등)이 런타임으로 읽는 reference 자산이다. 다음 상황에서 반드시 이 스킬을 사용할 것 — 사용자가 '디자인 토큰', '디자인 시스템', '리멤버 룩', '리멤버 디자인', '웜 페이퍼', '스타일 가이드', '컬러 팔레트', '오렌지 액센트', '다크 슬라이드', '발주처 로고 오버레이', '대비비', 'WCAG', 'ChainPayload', '체이닝 봉투'를 언급할 때. HTML·PPTX·XLSX·DOCX 산출물의 색·서체·간격·컴포넌트 패턴을 정할 때(다른 스킬이 자동 참조). 발주처별 로고·표지·푸터 슬롯을 바꿀 때. 형제 경계 — PPTX 빌드는 jc-pptx, 문서·대시보드 HTML 생성은 각 산출 스킬, 산출물 검증은 jc-redteam이며 본 스킬은 값·규칙·봉투 규약만 제공한다. 구 jc 시그니처(네이비·일렉트릭블루)는 legacy-jc 오버레이로만 남아 있으며 명시 요청 시에만 쓴다.
version: "v2.1.0"
---

# JC Design System v2 — 리멤버 웜 페이퍼

리멤버 MICE비즈팀이 내는 모든 산출물의 디자인 정본. 값은 이 스킬에만 살고, 다른 스킬은 읽기만 한다.

## 핵심 원칙

1. **룩은 하나** — 웜 아이보리 캔버스 위 잉크 블랙 타이포, 오렌지 한 점. 쿨 그레이·퓨어 블랙 금지.
2. **오렌지는 주인공 1회** — 그라디언트·다크 패널은 슬라이드(화면)당 1회. 오렌지 텍스트는 큰 글자 전용(§대비비).
3. **Pretendard 단일 서체** — 한글·영문 모두. 숫자는 tabular-nums, 토큰값·코드 표기만 JetBrains Mono.
4. **발주처는 슬롯으로만** — 로고·표지 이미지·푸터 문구 3곳만 바뀐다. 오렌지는 바꾸지 않는다.
5. **값 미러 금지** — 소비 스킬은 `references/signature-tokens.md §6 JSON`을 `scripts/jc_tokens.py`로 런타임 로드한다.
6. **토큰 정본과의 정합** — 이 문서의 값은 Claude Design 프로젝트 "리멤버 제안서 디자인 시스템"(`remember-proposal-ds` 레포 `packages/tokens/css`)과 같다. 값이 바뀌면 양쪽을 같이 고친다.

## 호출 흐름

```
1. signature-tokens.md §6 JSON 로드 (jc_tokens.load_tokens)
2. 발주처 지정 시 client-overlays.md 슬롯 적용 (로고·표지·푸터만)
3. 모드 결정 — 기본 라이트. 다크는 표지·섹션 구분·클로징 3종 + 대시보드 토글 (mode-mapping.md)
4. 산출물 유형별 컴포넌트 패턴 적용 (component-patterns.md)
5. 소비 스킬이 빌드 → 대비비·인쇄·HEX 규칙 점검 (shared-rules.md)
```

상세 절차와 코드 예시는 `references/usage-guide.md`.

## 빠른 참조

| 항목 | 값 |
|------|-----|
| 캔버스 / 카드 / 웜 서피스 | `#FBFAF6` / `#FFFFFF` / `#F4F1EA` |
| 잉크 / 보조 / 뮤트 / 캡션 | `#1A1A1A` / `#4A463F` / `#6E6E6E` / `#8C867A` |
| 보더 / 강조 보더 | `#DCD6C8` / `#CFC8BC` |
| 액센트 / 딥 / 라이트 / 틴트 | `#EB6F2A` / `#B8431A` / `#F5A05A` / `#FFF1E6` |
| 그라디언트 | `135deg #EB6F2A → #F5A05A` (1회) |
| 다크 스테이지 / 패널 / 차콜 | `#141210` / `#211E1A` / `#332F29` |
| 보조 Steel / 긍정 / 부정 | `#476580` / `#196B24` / `#D93636` |
| 차트 시리즈 | S1 `#EB6F2A` → S2 `#476580` → S3 `#4A463F` → S4 `#8C867A` → S5 `#F3B48A` |
| 서체 | Pretendard (Variable) · 모노 JetBrains Mono |
| 문서 스케일 | 12 / 14 / 16 / 20 / 25 / 31 / 39 / 49 px (1.250) |
| 덱 스케일 (1920×1080) | cover 88 · kpi 96 · headline 64 · title 44 · sub 30 · body 26 · caption 18 px |
| 간격 · 라운드 | base 4px · r6(버튼) / r10~12(카드) / pill |
| 로고 | 라이트 `assets/remember-black.png` · 다크 `assets/remember-offwhite.png` |

전체 토큰과 JSON은 `references/signature-tokens.md`.

## 대비비 요약 (WCAG AA, 실측)

- 오렌지 `#EB6F2A` 텍스트: 카드 위 3.07:1 · 캔버스 위 2.94:1 → **큰 텍스트(24px+ 또는 18px+ Bold) 전용**. 작은 강조 텍스트·링크는 딥 오렌지 `#B8431A`(5.45:1).
- 캡션 `#8C867A`: 3.6:1 → 캡션·단위·푸터 등 보조 정보에만. 본문에 쓰지 않는다.
- 앰버 `#D39A1F`: 2.5:1 → 단독 텍스트 금지. 배지는 배경 `#FBF2DF` + 잉크 텍스트.
- 다크 위 오렌지 텍스트는 `#F08A4C`(6.7:1 이상). 면 채움은 `#EB6F2A` 유지.
- 전체 표는 `references/mode-mapping.md §5`.

## 금지

- 쿨 그레이(`#E5E7EB`·Tailwind slate 계열)·퓨어 블랙 `#000` · 오렌지 다중 그라디언트 · 3D·그림자 차트
- 라이트 캔버스 위 오브제 PNG · 로고 재염색·비율 왜곡 · 슬라이드 좌측 컬러 보더 카드
- 이모지·느낌표·과장 수사(제안서 문체 규칙은 `component-patterns.md §0`)

## legacy-jc (구 시그니처)

Deep Navy `#0A2540` · Electric Blue `#2962FF` 체계는 `client-overlays.md §3.3 legacy-jc`에 보존한다. 사용자가 "jc 시그니처로", "네이비 톤으로"를 명시할 때만 쓴다. 기본값이 아니다.

## 파일 구조

```
jc-design-system/
├── SKILL.md
├── references/
│   ├── signature-tokens.md     # 토큰 정본 + §6 JSON (기계 파싱)
│   ├── mode-mapping.md         # 라이트/다크 매핑 · 인쇄 강제 · 대비비 표 · WCAG 계산 표준
│   ├── client-overlays.md      # 발주처 슬롯 3종 · legacy-jc · 아카이브
│   ├── component-patterns.md   # 문체 규칙 + KPI·카드·표·배지·헤더·대시보드 패턴
│   ├── usage-guide.md          # 소비 스킬 호출 절차 · Python/CSS 코드 패턴
│   ├── shared-rules.md         # RULE-WCAG · PRINT-LIGHT · PPTX-HEX · NO-COMPANY · VISUAL-ROUTING · VERSION-FACTS
│   └── chaining-protocol.md    # ChainPayload/v1 봉투 규약 · 라이브 source enum · 판별 함수
├── scripts/
│   ├── jc_tokens.py            # §6 JSON 로더 (stdlib)
│   └── test_jc_tokens.py
└── assets/
    ├── remember-black.png · remember-offwhite.png   # 로고타입 2종
    └── objet-01~07-*.png                           # 다크 슬라이드 히어로 오브제 7점
```

## 변경 이력

- v2.1.0 (2026-10-05): 체이닝 정본 enum을 라이브 스킬 기준으로 재작성(run-of-show·aftermath 라이브 복구, strategy-canvas·market-intel·mice-ops-docs·mice-team-board 등록, 폐합 source는 별칭), §6 절 번호·§7 판별 함수 명시.
  구 소속사 오버레이(`mc`·`darktrace`) 행 삭제, 예시 고객사 실명 → A사, 흡수된 구 HTML 스킬 참조 정리, §6 JSON version 2.1.0, 없는 LICENSE.txt 참조 삭제.

### v2.0.0 (2026-09-21) — 리멤버 베이스 전환
- 기본 룩을 jc 시그니처(네이비·블루)에서 **리멤버 웜 페이퍼**로 교체. 값 출처: `jc-remember-html` v1.0.0 토큰 + `remember-proposal-ds`(2026 고객 행사 제안서 51장 실측) + 팀 보드·플레이북 HTML 실전 CSS.
- `jc-remember-html` 스킬을 본 스킬로 흡수(토큰·컴포넌트·로고·오브제). 덱 템플릿 문법은 `jc-pptx/references/remember-deck-templates.md`로 이관.
- 클라이언트 오버레이를 컬러 주입에서 **슬롯 3종(로고·표지·푸터)**으로 축소. 구 시그니처는 `legacy-jc` 오버레이로 보존.
- 대비비 표를 리멤버 팔레트로 재계산(37조합). 오렌지 텍스트 큰 글자 전용 규칙 신설.
- `RULE-NO-COMPANY`를 "리멤버 명의 기본, 발주처·담당자만 주입"으로 재정의. `mice-sponsor-deck` 등 폐지 스킬 참조 제거.
- 삭제: `cinematic-campaign-html.md` 포인터, Tier/priority 다크 변형(구 sponsor-deck 전용).

### v1.4.0 이전
구 jc 시그니처 체계의 이력은 git 히스토리(2026-04 ~ 2026-08-18)에 보존.
