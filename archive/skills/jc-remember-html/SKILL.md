---
name: jc-remember-html
description: "HTML/덱 산출물(발표덱·KPI 대시보드·문서·회의록 커뮤니케이션)을 '리멤버 웜 페이퍼 룩'(웜 아이보리 캔버스 · 잉크 블랙 · 오렌지 액센트 #EB6F2A · Pretendard · 링/아크·그라디언트 카드·다크 패널 모티프)으로 신규 빌드하거나 기존 산출물을 리스킨하는 클라이언트 룩 엔진. 다음 상황에서 반드시 이 스킬을 사용할 것 — 사용자가 '리멤버', 'REMEMBER', '리멤버 룩', '리멤버 디자인', '리멤버 톤', '웜 페이퍼 룩', 'REMEMBER Design Guide'를 언급하며 덱·대시보드·문서·랜딩 등 산출물 제작이나 리스킨을 요청할 때. 리멤버 MICE 사업 관련 제안서·리포트·데이터 사업 자료를 만들 때. 형제 경계 — jc 시그니처(Deep Navy·Electric Blue) 기본 산출물은 jc-design-system 직접 참조, 오버레이 선택·발행은 jc-theme-factory, PPTX 빌드 기계는 jc-pptx(본 스킬은 그 위에 리멤버 룩 문법을 주입), 시네마틱 룩은 jc-cinematic-html, 라이트 SaaS 룩은 jc-asana-html 영역. 본 스킬은 '리멤버 웜 페이퍼 룩' 한 가족의 토큰·템플릿 문법·오브제 운용만 담당한다. 실행형 지시는 실행 전 jc-prompt-builder 브리프를 거친다."
version: "v1.0.0"
---

# jc-remember-html

리멤버(REMEMBER) 클라이언트 전용 룩 엔진. 실측 레퍼런스 2종(MICE Business v70 54p · 데이터사업해부와 상품설계 v1 44p)에서 추출·정규화한 팔레트와, 외부 레퍼런스 2계열(오렌지 링/아크·차콜 포토 패널)을 이식한 덱 템플릿 문법을 내장한다.

**홈베이스 원칙과의 관계**: jc 시그니처가 기본값이라는 홈베이스 원칙의 **명시적 opt-in 예외**다. 사용자가 리멤버 맥락을 언급할 때만 이 룩으로 전환한다.

## 핵심 원칙

1. **웜 페이퍼 캔버스** — 배경은 `#FBFAF6`, 순백 카드(`#FFFFFF`)와 1px 웜 보더(`#DCD6C8`)로 층위. 쿨 그레이 금지.
2. **오렌지는 주인공 1회** — 그라디언트(`#EB6F2A→#F5A05A`)와 다크 패널은 슬라이드당 1회. 나머지는 플랫 토큰.
3. **잉크 위계** — 본문 `#1A1A1A` / 보조 `#6E6E6E` / 캡션 `#8C867A`. 웜 브라운 `#4A463F`는 서브 잉크·다크 면 겸용.
4. **Pretendard 단일 서체** — 숫자는 `font-variant-numeric: tabular-nums`. 토큰값·코드 표기만 JetBrains Mono.
5. **오브제는 다크 전용** — assets/objet-*.png 7점은 다크 슬라이드 히어로로만, 슬라이드당 1점, 텍스트는 반대편 여백에.

## 호출 흐름

```
1. references/tokens.md 로드 → 팔레트·타이포·간격 적용
2. 덱이면 references/deck-templates.md 의 T1~T12 문법으로 슬라이드 매핑
3. 대시보드·문서면 references/component-patterns.md 패턴 적용
4. 다크 슬라이드에 assets/objet-*.png 배치 (운용 규칙: tokens.md §6)
5. 로고: 라이트 배경 = remember-black.png / 다크 배경 = remember-offwhite.png
```

## 빠른 참조

| 항목 | 값 |
|------|-----|
| Canvas | `#FBFAF6` (다크 `#211E1A`, 오브제 배경 `#141210`) |
| Ink | `#1A1A1A` (다크 `#F4F0E9`) |
| Accent | `#EB6F2A` / Deep `#B8431A` / Tint `#FFF1E6` / 다크 텍스트용 `#F08A4C` |
| Gradient | `linear-gradient(135deg, #EB6F2A, #F5A05A)` — 슬라이드당 1회 |
| 보조 | Steel `#476580` · Brown `#4A463F` · Charcoal 패널 `#332F29` |
| 상태 | Positive `#196B24` · Negative `#D93636` |
| 서체 | Pretendard (스케일 1.250: 12/14/16/20/25/31/39/49) |
| 간격 | base 4px · 라운드 r6(버튼)/r10~12(카드)/pill(배지) |
| 그림자 | `rgba(74,70,63,0.08)` 한 단계만 |
| 차트 시리즈 | S1 `#EB6F2A` → S2 `#476580` → S3 `#4A463F` → S4 `#8C867A` → S5 `#F3B48A` |

## 금지 사항

- 로고 재염색·비율 왜곡 (BLACK/OFF WHITE 2종 외 변형 금지)
- 쿨 그레이·퓨어 블랙(#000) 사용, 오렌지 다중 그라디언트 남발
- 라이트 캔버스 위 오브제 이미지 사용
- 슬라이드 내 배경색 3종 이상 혼용

## 공통 룰 (정본 참조)

- 검증: 고부담 산출물은 `jc-redteam` 게이트
- WCAG·인쇄·PPTX 헥스 규칙: `jc-design-system/references/shared-rules.md`
- 다크 매핑 상세: `references/tokens.md` §5

## 파일 구조

```
jc-remember-html/
├── SKILL.md
├── references/
│   ├── tokens.md               # 팔레트(라이트/다크)·타이포·간격·차트·오브제 운용
│   ├── deck-templates.md       # 덱 템플릿 T1~T12 문법 + CSS 레시피
│   └── component-patterns.md   # 버튼·배지·KPI 카드·테이블·차트 패턴
└── assets/
    ├── remember-black.png      # 로고타입 (라이트 배경용)
    ├── remember-offwhite.png   # 로고타입 (다크 배경용)
    └── objet-01~07.png         # 다크 히어로 오브제 7점
```

## 변경 이력

### v1.0.0 (2026-08-18)

신규 빌드. 실측 레퍼런스 2종에서 팔레트 정규화(오렌지 #E97132/#EB6F2A → #EB6F2A 단일화), 외부 레퍼런스 2계열 이식(링/아크·그라디언트 카드 + 포토 풀블리드·다크 패널·캡슐 프로필), 덱 템플릿 12종 문법화, 오브제 라이브러리 7점 운용 규칙 수록. 원본 라이브 가이드: 디자인 프리셋 설계 프로젝트 `REMEMBER Design Guide.dc.html` · `REMEMBER Deck Templates.dc.html`.
