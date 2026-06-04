---
name: jc-brand-styling
description: 이미 존재하는 산출물(PPTX 슬라이드·HTML 아티팩트)에 jc 시그니처(Deep Navy·Electric Blue·Pretendard) + 선택적 클라이언트 오버레이를 입히는 후처리 적용 엔진. 헤딩/본문 폰트 교체·배경 대비 자동 텍스트색·비텍스트 도형 accent 순환 채움을 python-pptx로 찍는다. 다음 상황에서 반드시 이 스킬을 사용할 것 사용자가 '브랜드 입혀줘', '스타일 적용', '리테마', '우리 톤으로 바꿔줘', 'PPTX에 색 입혀줘', '이 슬라이드 브랜딩 입혀줘', '폰트 우리 걸로 바꿔줘', '기존 파일에 시그니처 적용', '아티팩트 색 바꿔줘'를 언급할 때. 완성된 .pptx나 HTML 파일을 주며 '여기에 우리 브랜드로 입혀줘', '리테마해줘'라고 할 때. 단, 형제 경계 — 어떤 테마/오버레이를 쓸지 결정·쇼케이스·신규 오버레이 발행은 jc-theme-factory, 토큰 값 자체의 정의·수정은 jc-design-system, 새 제안서/데크/대시보드를 *생성*하는 것은 mice-proposal·mice-sponsor-deck·mice-dashboard 영역이다. 이 스킬은 그 결과로 *이미 만들어진 파일에 색·폰트를 입히는* 후처리 엔진이며, 임의 팔레트·임의 폰트쌍은 만들지 않는다(시그니처 고정).
version: "v1.0.0"
license: Complete terms in LICENSE.txt
---

# JC Brand Styling

원본 `brand-guidelines`(Anthropic 브랜드 적용기)를 **jc 생태계 후처리 적용 엔진**으로 개조한 버전이다. 원본이 임의의 아티팩트에 Anthropic 브랜드(오렌지 `#d97757` · Poppins/Lora)를 입혔다면, 이건 **jc 시그니처(Deep Navy · Electric Blue · Pretendard)**를 입힌다.

핵심 역할은 **짝꿍 분업**이다:

> **jc-theme-factory** = "어떤 오버레이인지" 결정(쇼케이스·선택·발행) · **jc-brand-styling**(이 스킬) = "그걸 대상 파일에 찍는" 엔진.

새 산출물을 *생성*하지 않는다. 이미 존재하는 **PPTX 슬라이드**나 **HTML 아티팩트**에 시그니처(+선택적 클라이언트 오버레이 primary/accent/logo 3토큰)를 입히는 **후처리(post-processing)**만 한다.

## 무엇을 입히나 (원본 기능의 jc 번안)

| 원본(brand-guidelines) | → jc-brand-styling |
|------------------------|--------------------|
| Poppins(헤딩)/Lora(본문) | **Pretendard**(헤딩·본문, 폴백 Apple SD Gothic Neo→Malgun Gothic→Arial) |
| 오렌지/블루/그린 accent 순환 | **accent(Electric Blue) → Point Pool → data 시리즈** 순환 |
| 배경 대비 텍스트색 자동 | (유지) 밝은 배경→Deep Navy, 어두운 배경→흰색 (`RULE-WCAG`) |
| RGBColor(python-pptx) | (유지) 단, hex는 `#` 없는 6자리 (`RULE-PPTX-HEX`) |

폰트는 시그니처 **고정** — 오버레이로도 못 바꾼다(`signature-tokens.md §2`). 오버레이가 바꾸는 건 primary·accent **색**뿐이다.

## 핵심: `scripts/style_pptx.py` (PPTX 후처리 번들)

이미 만들어진 `.pptx`에 시그니처를 입히는 결정적 엔진. **매 호출마다 헬퍼를 새로 짜지 않도록 번들**한다(플레이북 §7).

```bash
# 시그니처 그대로 입히기 (개인 브랜드 = personal 기본값)
python3 scripts/style_pptx.py 제안서.pptx                  # → 제안서_jc.pptx

# 출력 경로 지정
python3 scripts/style_pptx.py 제안서.pptx -o 최종.pptx

# 클라이언트 오버레이 적용 (primary/accent를 client-overlays.md에서 로드)
python3 scripts/style_pptx.py 제안서.pptx --client darktrace

# 헤딩 임계치 조정 (기본 24pt 이상을 헤딩으로 간주)
python3 scripts/style_pptx.py 제안서.pptx --heading-min 28

# 엔진 동작 자가검증 (샘플 PPTX 생성 → 적용 → 결과 재검증)
python3 scripts/style_pptx.py --self-test
```

동작 요지(상세는 [`references/style-pptx-guide.md`](references/style-pptx-guide.md)):

- **토큰은 SoT 런타임 로드.** `jc-design-system/scripts/jc_tokens.py`(형제 경로 `parents[2]`)의 `load_tokens`/`color`로 `signature-tokens.md §6 JSON`을 읽는다. 값 미러링 금지 — 로드 실패 시에만 출처 주석을 단 폴백 상수 사용.
- **`--client <id>`**: `client-overlays.md`에서 그 블록을 파싱해 `primary`/`accent`만 덮어쓴다(null/플레이스홀더는 시그니처 유지, 3토큰 한정). 못 찾으면 경고 후 시그니처로 진행.
- **헤딩/본문 분기**: run 크기가 `--heading-min`(기본 24pt) 이상이거나 bold면 헤딩 폰트, 아니면 본문 폰트.
- **텍스트색 자동**: 각 도형의 채움 배경을 보고 대비가 큰 쪽(흰 vs Deep Navy)을 선택(`RULE-WCAG`).
- **비텍스트 도형**: 텍스트 없는 채울 수 있는 도형에 accent → Point Pool(orange/magenta/neon/blue) → data 순으로 순환 채움. 그룹·표 셀도 재귀 처리.
- **`RULE-PPTX-HEX`**: `RGBColor.from_string()`에 `#` 없는 6자리만 전달. (HTML/CSS는 `#` 포함 — 같은 색이라도 매체에 따라 표기가 다르다.)
- **python-pptx 미설치 시**: 설치법 + 토큰값을 담은 친절한 안내를 출력하고 비-0 종료(무음 실패 방지).

## HTML 아티팩트 리테마

이미 만들어진 HTML 아티팩트는 PPTX와 달리 **CSS 변수 치환**으로 리테마한다. `:root` 토큰 주입 + 다크 `@media` + 인쇄 라이트 강제. 절차·스니펫의 정본은 [`references/html-retheme-guide.md`](references/html-retheme-guide.md). 요지:

```css
:root{ --jc-primary:<primary>; --jc-accent:<accent>; /* 나머지는 signature-tokens §6 그대로 */ }
@media (prefers-color-scheme: dark){ :root{ /* mode-mapping §3 다크값 */ } }
@media print{ :root{ --jc-bg:#FFFFFF!important; --jc-surface:#FFFFFF!important; --jc-text:#1A1D24!important; } } /* RULE-PRINT-LIGHT */
```

오버레이가 바꾸는 건 `--jc-primary`·`--jc-accent`(및 다크 보정값)뿐, 나머지는 시그니처 그대로다.

## 모드 (라이트/다크)

`mode-mapping.md §1` 산출물 유형 기본값을 따르되 **사용자 지정 우선**:

- PPTX(제안서·데크)·DOCX·XLSX → **Light** 기본. (PPTX는 기본 라이트라 인쇄 라이트 강제 불필요 — 표지 등 다크 슬라이드는 그 디자인 자체가 의도된 것이므로 예외.)
- HTML(대시보드·아티팩트) → **Light + Dark 토글**. **다크 상태여도 인쇄(PDF)는 라이트 강제**(`RULE-PRINT-LIGHT`, 정본 `mode-mapping.md §4.2`).

## 절대 가드레일

- **토큰 값 하드코딩 금지** — SoT(`jc-design-system`) 런타임 참조. `check_drift.py` FORBIDDEN 값 0건. 폴백 미러는 출처 주석 필수.
- **폰트 불변** — Pretendard(한)/Inter(영)/JetBrains Mono(숫자). 오버레이로도 못 바꾼다. 원본의 "폰트쌍 고르기"는 jc에서 폐기.
- **3토큰 한정** — 오버레이는 primary/accent/logo만. text/bg/surface/size/space/radius 전부 시그니처 고정.
- **임의 팔레트 금지** — 시그니처+등록 오버레이 외 임의 색을 만들지 않는다. 색 자유가 필요한 아트는 jc-visual-philosophy / jc-generative-art 영역.
- **`RULE-NO-COMPANY`** — 회사·실명·부서·로고 경로는 하드코딩하지 않고 외부 주입 변수(`{{client_company}}`·`{{author_name}}`·`{{personal_brand}}`·`{{author_title}}`·`{{company_name}}`)로만. 본 엔진은 텍스트 콘텐츠를 생성하지 않고 기존 슬라이드의 서식만 바꾼다.
- 공통 룰 정본: `jc-design-system/references/shared-rules.md` (`#RULE-PPTX-HEX`·`#RULE-WCAG`·`#RULE-PRINT-LIGHT`·`#RULE-NO-COMPANY`).

## 생태계 연결

- **테마 결정 ↔ 적용**: [`jc-theme-factory`]가 쇼케이스·선택·발행으로 `client_id`(또는 오버레이 토큰)를 결정 → 이 스킬이 대상 `.pptx`/`.html`에 찍는다. (`jc-theme-factory/references/apply-guide.md §2` 위임 규약)
- **디자인 SoT**: `jc-design-system/references/`(signature-tokens·mode-mapping·client-overlays). 토큰·모드·오버레이의 단일 진실.
- **검증**: 리테마 결과의 대비·일관성·카피는 [`jc-redteam`]으로 최종 점검(결론·문서=3축). 적용 자체 동작은 `--self-test`로 회귀 확인.
- **데이터**: 다른 mice-* 산출물 파일을 입력으로 받을 때 메타는 `ChainPayload/v1`(`chaining-protocol.md`)로 받을 수 있다(이 엔진은 *파일*을 입력으로 받는 게 1차).

## 파일 구조

```
jc-brand-styling/
├── SKILL.md                       # 본 파일 — 진입점
├── LICENSE.txt
├── references/
│   ├── style-pptx-guide.md        # style_pptx.py 상세 동작·옵션·CLI·트러블슈팅
│   └── html-retheme-guide.md      # HTML 아티팩트 CSS 변수 치환(라이트/다크/인쇄 라이트)
└── scripts/
    └── style_pptx.py              # PPTX 후처리 엔진 (SoT 런타임 로드·오버레이·자가검증)
```

## 빠른 체크리스트

- [ ] 입력은 *이미 존재하는* 파일(.pptx/.html) — 새로 생성하는 게 아니다(생성은 mice-* / 결정은 theme-factory)
- [ ] 토큰 값 SoT 런타임 참조(하드코딩 0건), `check_drift.py` FORBIDDEN 0건
- [ ] 폰트 시그니처(Pretendard 등) 유지, 임의 팔레트·임의 폰트쌍 0건
- [ ] (PPTX) hex `#` 없는 6자리(`RULE-PPTX-HEX`), 흰 텍스트 대비 WCAG AA↑(`RULE-WCAG`)
- [ ] (HTML) 다크 지원 시 인쇄 라이트 강제(`RULE-PRINT-LIGHT`)
- [ ] 오버레이는 primary/accent/logo 3토큰만, null은 시그니처 유지
- [ ] 회사·개인정보 외부 주입 변수(`RULE-NO-COMPANY`), python-pptx 미설치 시 친절 안내
- [ ] 적용 결과는 `--self-test`로 회귀 확인, 최종 카피·대비는 jc-redteam 점검 가능
