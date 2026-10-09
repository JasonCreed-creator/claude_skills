# Themes — 토큰 매핑 · 프리셋 · 주입 규칙

> 값의 정본은 `jc-design-system/references/signature-tokens.md §6`. 본 문서는 그 값을 덱 토큰 8종(+확장)에 어떻게 매핑하는지만 정의한다. deck_kit `load_remember()`가 구현체.

## 덱 토큰

| 토큰 | 역할 | remember 매핑 (§6 JSON 키) |
|---|---|---|
| `bg_base` | 슬라이드 배경 | `color.bg` `#FBFAF6` |
| `bg_card` | 카드·박스 | `color.surface` `#FFFFFF` |
| `surface_alt` | 표 헤더·바 트랙·서브 밴드 | `color.surfaceAlt` `#F4F1EA` |
| `text_primary` | 헤드라인·첫 열 | `color.text` `#1A1A1A` |
| `text_body` | 본문 | `color.textSecondary` `#4A463F` |
| `text_muted` | 캡션·푸터 | `color.textCaption` `#8C867A` |
| `text_sub` | 서브 헤드라인 | `color.textMuted` `#6E6E6E` |
| `accent` | 강조어·아이브로우·면 채움 | `color.accent` `#EB6F2A` |
| `accent_deep` | 작은 강조 텍스트·링크 | `color.accentStrong` `#B8431A` |
| `accent_light` | 그라디언트 종점·다크 라벨 | `color.accentLight` `#F5A05A` |
| `accent_pale` | 차트 S5·타임라인 룰 | `color.accentSoftLine` `#F3B48A` |
| `accent_tint` | 테이크어웨이·배지 배경 | `color.accentSoft` `#FFF1E6` |
| `accent_sub` | 보조 강조 | `color.point.steel` `#476580` |
| `line` | 보더·구분선 | `color.border` `#DCD6C8` |
| `line_soft` | 표 행 구분 | `color.surfaceSoft` `#EFEBE2` |
| `charcoal` | 사진 위 패널·캡슐·DROP 바 | `color.primarySoft` `#332F29` |
| `d_bg` / `d_panel` / `d_surface` / `d_border` | 다크 슬라이드 | `color.dark.bg/panel/surface/border` |
| `d_ink` / `d_muted` / `d_sub` / `d_dim` | 다크 텍스트 | `color.dark.text/textMuted/textSub/textDim` |
| `d_accent_text` | 다크 위 오렌지 텍스트 | `color.dark.accentText` `#F08A4C` |
| `positive` / `negative` | 증감 | `semantic.success` / `semantic.danger` |
| `series` | 차트 | `color.data` (S1~S6) |
| 서체 | 헤드/본문 | Pretendard (미설치 폴백 Malgun Gothic) |

타이포 pt 스케일은 `deckPt`(cover 44 · kpi 48 · headline 32 · title 22 · sub 15 · body 13 · small/eyebrow 11 · caption 9).

## 프리셋

### remember (기본 — 지정 없으면 항상 이것)
위 매핑 그대로. 다크 슬라이드(표지·섹션·클로징)는 `d_*` 토큰. 그라디언트 `135° accent → accent_light` 슬라이드당 1회. 로고·오브제는 `jc-design-system/assets`.

### legacy-jc (명시 요청 시만)
구 개인 시그니처(Deep Navy·Electric Blue). 값은 `jc-design-system/references/client-overlays.md §3.3 deck_theme` 블록에서 로드. "jc 시그니처로", "네이비 톤으로"라고 말할 때만.

### dark-premium · light-vivid (명명 프리셋, 외부 브랜드 톤 실험용)
v1의 실측 프리셋. 리멤버 명의 산출물에는 쓰지 않는다. 값은 deck_kit `PRESETS`에 보존(텍스처 `assets/texture-*.png`).

## 주입 규칙

1. **기본 = remember.** 사용자가 프리셋을 말하지 않으면 묻지 않고 remember.
2. **발주처 슬롯 3종만 주입** — `client-overlays.md §1`: `logo_path`(표지·클로징 좌상단), `cover_image`(표지 우측, 기본 오브제 03), `footer_text`(행사명). 발주처 컬러는 팔레트에 넣지 않는다.
3. 발주처가 "우리 색으로"를 요구하면: 로고 원색 노출 + 표지 이미지로 대응하고, 팔레트 변경은 하지 않는다고 설명한다. 그래도 필요하면 별도 프리셋을 `jc-design-system`에 등록하는 결정으로 넘긴다(본 스킬이 임의 생성하지 않음).

## 색 사용 계율

- 토큰 외 색 금지(검수 실패). 오렌지 텍스트는 24px+/18px+Bold에서만, 작은 글자는 `accent_deep`.
- 그라디언트 면 / 솔리드 KPI / 다크 패널 중 슬라이드당 1개. 다크 슬라이드 덱 30% 이하.
- python-pptx는 `RGBColor.from_string("EB6F2A")` — `#` 없이 (RULE-PPTX-HEX). deck_kit `C()`가 처리.
- 인쇄·PDF 배포본은 다크 슬라이드 그대로 두되(표지·섹션·클로징은 디자인 자체), 본문 다크 패널은 최소화.
