---
name: jc-theme-factory
description: jc-design-system 정본을 사람이 쓰는 인터페이스로 감싼 테마 프론트엔드. 시그니처+등록된 클라이언트 오버레이를 시각 쇼케이스로 보여주고, 적용할 오버레이를 고르거나(미지정=개인 시그니처), 맞는 게 없으면 신규 오버레이를 발행(primary/accent/logo 3토큰 한정·색충돌·WCAG 자동 검증)해 client-overlays.md에 등록한 뒤, 산출물(HTML/PPTX/DOCX)에 적용한다. 다음 상황에서 반드시 이 스킬을 사용할 것 사용자가 '테마', 'theme', '테마 적용', '테마 입혀줘', '팔레트', '컬러 입혀줘', '스타일 입히기', '오버레이', '클라이언트 컬러', '브랜드 컬러 적용', '쇼케이스', '시그니처 보여줘', '어떤 테마 있어', '이 산출물에 우리 톤 적용', '신규 클라이언트 컬러 만들어줘'를 언급할 때. 특정 산출물을 가리키며 '여기에 OO 테마/컬러로 입혀줘'라고 할 때. 단, 토큰 값 자체의 정의·수정·확장(시그니처 변경)은 jc-design-system 직접 영역이고, 임의 팔레트·임의 폰트쌍 생성은 하지 않는다(시그니처 고정). 미학 무드의 캔버스 아트는 jc-visual-philosophy, 제너러티브 아트는 jc-generative-art, 실제 PPTX 후처리 적용 엔진은 jc-brand-styling 영역.
version: "v1.0.0"
license: Complete terms in LICENSE.txt
---

# JC Theme Factory

원본 Theme Factory(10개 임의 테마 중 택1 + 임의 커스텀 테마 생성)를 **jc-design-system(SoT) 환경에 맞춰 개조**한 버전이다.

원본은 서로 무관한 10개 팔레트·폰트쌍 중 하나를 고르게 했다. 그런데 그 전제는 jc-design-system 1원칙과 정면충돌한다:

> "시그니처는 고정 자산 — 컬러·폰트는 변경 금지. **클라이언트는 오버레이(primary/accent/logo 3토큰)로만 차별화.**"

그래서 본 스킬은 "테마"를 **"오버레이"로 재해석**한다. 원본의 *쇼케이스 → 선택 → 적용 → 커스텀 생성* 4박자는 그대로 살리되, 알맹이를 jc 오버레이 체계로 치환했다. jc-design-system은 *읽기 전용 참조 자산*이라 인터랙티브 UX가 없는데, 본 스킬이 그 빠진 "프론트오피스"(쇼케이스·선택·발행 워크플로우)를 채운다.

## 핵심 워크플로우 (4박자)

### 1. 쇼케이스 (원본 theme-showcase.pdf 대응)

`scripts/build_showcase.py`로 **시그니처 + 등록된 모든 클라이언트 오버레이**를 라이트/다크 카드로 렌더한 단일 HTML을 생성해 사용자에게 보여준다. 임의 테마 10종을 나열하는 게 아니라, 실제 등록된 오버레이(personal·mc·remember·darktrace·confex…)를 보여준다.

```bash
python3 scripts/build_showcase.py            # 전체 오버레이 쇼케이스 → theme-showcase.html
python3 scripts/build_showcase.py --overlay remember   # 특정 오버레이만
```

각 카드는 primary/accent 스와치 + KPI 카드·버튼·차트 범례 미니 프리뷰를 포함하고, 인쇄 시 라이트 강제(`RULE-PRINT-LIGHT`)가 걸려 PDF로도 뽑을 수 있다. 쇼케이스 파일은 **읽기용으로만 표시**하고 임의 수정하지 않는다. 카탈로그 요약은 [`references/overlay-catalog.md`](references/overlay-catalog.md).

### 2. 선택

어떤 오버레이를 산출물에 적용할지 사용자에게 확인한다. **미지정 = `personal` = 시그니처 그대로**(개인 브랜드 기본값). 등록된 오버레이 목록·정체성은 카탈로그 참조.

### 3. 발행 (원본 "create your own theme" 대응)

맞는 오버레이가 없으면 **신규 클라이언트 오버레이를 발행**한다. 임의 테마를 새로 만드는 게 아니라, 시그니처 위에 얹는 3토큰 오버레이를 만드는 것이다. 절차·검증의 정본은 [`references/mint-overlay.md`](references/mint-overlay.md). 요지:

- 주입 가능 토큰은 **`primary` / `accent` / `logo_path` 3개뿐.** 폰트·사이즈·간격·텍스트/배경은 시그니처 고정 → 건드리지 않는다.
- `scripts/validate_overlay.py`로 **자동 검증**: WCAG 대비비(`RULE-WCAG`), 색충돌 회피(`client-overlays.md §6` — Deep Navy 채도 근접·Point Pool ΔE<5·인쇄 형광), 3토큰 한정.
- 검증 통과안을 사용자에게 **리뷰**시킨 뒤, `jc-design-system/references/client-overlays.md`(SoT)에 `§3.X` 형식으로 등록한다.

```bash
python3 scripts/validate_overlay.py --primary "#0A2540" --accent "#7C3AED" --print
```

### 4. 적용

선택/발행된 오버레이를 대상 산출물에 적용한다.

- **토큰 값은 항상 jc-design-system을 SoT로 런타임 참조**(미러 금지). `jc_tokens.py`의 `load_tokens`/`color` + 본 스킬의 오버레이 파서.
- 모드(라이트/다크)는 `mode-mapping.md §1` 산출물 기본값 → 사용자 지정 우선.
- 실제 매체별 적용(특히 PPTX 후처리)은 **`jc-brand-styling`에 위임**할 수 있다. 본 스킬은 "어떤 테마"를 결정하고, jc-brand-styling은 "그걸 산출물에 찍는" 엔진이다. 매체별 적용 가이드는 [`references/apply-guide.md`](references/apply-guide.md).

## 절대 가드레일

- **폰트 불변** — Pretendard(한)/Inter(영)/JetBrains Mono(숫자). 오버레이로도 못 바꾼다. 원본의 "폰트쌍 고르기"는 jc에서 폐기.
- **3토큰 한정** — 오버레이는 primary/accent/logo만. text/bg/surface/size/space/radius 전부 시그니처 고정.
- **값 미러링 금지** — 토큰 값을 본문/코드에 박지 말고 SoT에서 읽는다. `check_drift.py` FORBIDDEN 값 0건.
- **임의 팔레트 생성 금지** — "Sunset Boulevard" 같은 자유 팔레트는 만들지 않는다. 색 자유가 필요한 *아트 오브젝트*는 jc-visual-philosophy / jc-generative-art로 보낸다.
- 공통 룰: `RULE-WCAG` · `RULE-PRINT-LIGHT` · `RULE-NO-COMPANY` · (PPTX 적용 시)`RULE-PPTX-HEX`. 정본 `jc-design-system/references/shared-rules.md`.

## 생태계 연결

- **디자인 SoT**: `jc-design-system/references/` (signature-tokens·mode-mapping·client-overlays). 본 스킬은 그 프론트엔드.
- **적용 엔진**: `jc-brand-styling`(PPTX/아티팩트 후처리). 선택↔적용으로 짝.
- **검증**: 발행한 오버레이·적용 결과의 대비·카피·일관성은 `jc-redteam`으로 최종 점검 가능.
- **데이터**: 다른 mice-* 산출물에 테마를 입힐 때 입력은 `ChainPayload/v1`(`chaining-protocol.md`)로 받을 수 있다.

## 파일 구조

```
jc-theme-factory/
├── SKILL.md                      # 본 파일 — 진입점
├── references/
│   ├── overlay-catalog.md        # "Themes Available" 대응 — 시그니처+등록 오버레이 카탈로그
│   ├── mint-overlay.md           # 신규 오버레이 발행 절차 + 검증 규칙 + 등록 포맷
│   └── apply-guide.md            # 매체별(HTML/PPTX/DOCX) 적용 + jc-brand-styling 연동 + 모드 결정
└── scripts/
    ├── build_showcase.py         # SoT+오버레이 → 쇼케이스 HTML(라이트/다크·인쇄 라이트)
    └── validate_overlay.py       # 신규 오버레이 WCAG·색충돌·3토큰 검증 (재사용 헬퍼)
```

## 빠른 체크리스트

- [ ] 쇼케이스는 임의 10테마가 아니라 **시그니처+등록 오버레이**를 보여줬다
- [ ] 선택 미지정 시 `personal`(시그니처) 폴백
- [ ] 신규 발행은 3토큰 한정 + `validate_overlay.py` 통과(WCAG·충돌) 후 SoT 등록
- [ ] 적용 시 토큰 값은 SoT 런타임 참조(하드코딩 0건), 모드 규칙 준수
- [ ] 폰트 불변·임의 팔레트 0건, 회사·개인정보 하드코딩 0건
