# Shared Rules — 공통 룰 정본 (Single Source of Truth)

여러 소비자 스킬(mice-proposal·mice-sponsor-deck·mice-dashboard·mice-estimate·pt-script·mice-rfp-analyzer·mice-meeting-minutes)에 반복 등장하는 **공통 규칙의 권위 정의**다. 각 스킬은 짧은 인라인 리마인더를 유지하되, 규칙의 근거·예시·전체 정의는 이 문서를 정본으로 참조한다.

> **참조 표기 규약**: 소비자 문서에서 본 정본을 가리킬 때는
> `정본: jc-design-system/references/shared-rules.md#<RULE-ID>` 형식을 사용한다.
> (예: `정본: jc-design-system/references/shared-rules.md#RULE-PPTX-HEX`)

> **이 문서의 범위**: 디자인 토큰 *값*의 정본은 `signature-tokens.md`(라이트·시그니처)와 `mode-mapping.md`(다크·대비비)다. 본 문서는 그 위에서 작동하는 **교차 스킬 공통 정책 4종**만 정의하며, 색상 값은 정본 파일로 위임한다.

---

## 규칙 인덱스

| ID | 규칙 | 적용 산출물 | 정본 보강 |
|----|------|------------|----------|
| `RULE-PPTX-HEX` | pptxgenjs hex 는 `#` 없이 6자리 | PPTX (proposal·sponsor-deck) | — |
| `RULE-WCAG` | WCAG AA 대비 목표 | 전 산출물 | `mode-mapping.md §9` (계산 표준)·§5, `signature-tokens.md §1.7.2` |
| `RULE-PRINT-LIGHT` | 다크 산출물도 인쇄 시 라이트 강제 | HTML (dashboard·sponsor-deck) | `mode-mapping.md §4.2` |
| `RULE-NO-COMPANY` | 회사·개인 식별정보 하드코딩 금지 | 전 산출물 | 구현 예: pt-script·sponsor-deck 스크립트 |

---

## RULE-PPTX-HEX — pptxgenjs hex 표기

**정의**: pptxgenjs 에 전달하는 모든 hex 컬러 문자열은 `#` 접두사 없이 6자리(`RRGGBB`)로 표기한다.

```
"0A2540"   ✅  (pptxgenjs 가 요구하는 형식)
"#0A2540"  ❌  (앞의 # 때문에 색이 적용되지 않거나 무시됨)
```

**근거**: pptxgenjs 의 `color`/`fill`/`background`/차트 시리즈 색상 옵션은 6자리 hex 리터럴만 파싱한다. `#` 가 붙으면 색상이 적용되지 않는다(무음 실패). 동일 토큰을 HTML/CSS 에서 쓸 때는 `#0A2540` 처럼 `#` 를 붙여야 하므로, **같은 색이라도 산출물 종류에 따라 표기가 다르다**는 점에 주의한다.

**적용 범위**:
- PPTX 를 생성하는 스킬에만 해당: `mice-proposal`, `mice-sponsor-deck`(2차 산출물).
- HTML 산출물(`mice-dashboard`, sponsor-deck 1차 HTML)·DOCX 산출물에는 적용되지 않는다(CSS 는 `#` 사용).

**구현 예 / 적용 위치**:
- `mice-proposal/references/visual-patterns.md` — `COLOR_*`·`CHART_SERIES` 상수가 `#` 없는 6자리(`signature-tokens.md §6` 미러).
- `mice-sponsor-deck/references/visual-patterns.md`·`output-build-guide.md`·`design-tokens-mapping.md` — PPTX 변환 시 `#` 제외.
- 값의 SoT 는 항상 `signature-tokens.md §6`(라이트)·`mode-mapping.md §3`(다크). 본 규칙은 *표기 형식*만 규정한다.

**체크 항목**: PPTX 빌드 후 hex 문자열에 `#` 가 0건인지 확인.

---

## RULE-WCAG — WCAG AA 대비 목표

**정의**: 모든 산출물의 텍스트·UI 색상 대비는 WCAG 2.1 AA 를 충족한다.

| 텍스트 종류 | 대비 목표 |
|-------------|----------|
| 본문 텍스트 (18pt 미만 일반 / 14pt 미만 bold) | **4.5:1 이상** |
| 큰 텍스트 (18pt bold 이상 / 24pt 이상 일반) | **3.0:1 이상** |
| 비텍스트(그래픽·UI 컴포넌트) | **3.0:1 이상** |
| AAA 본문 (선택적 상향) | 7.0:1 이상 |

**근거 / 계산 표준**: 대비비 산출 공식(sRGB 상대 휘도)·판정 기준·검증 도구는 본 문서에서 재정의하지 않는다. **구체 대비표·계산 공식·도구의 정본은 다음이다**:

- **`jc-design-system/references/mode-mapping.md §9`** — WCAG AA 대비비 계산 표준(sRGB→상대 휘도 공식, WebAIM Contrast Checker 기준). 본 스킬 군의 모든 대비비 표기는 WebAIM 결과값을 기준으로 하며 다른 도구의 근사값은 채택하지 않는다.
- **`jc-design-system/references/mode-mapping.md §5`** — 라이트/다크 표준 조합별 대비비 표.
- **`jc-design-system/references/signature-tokens.md §1.7.2`** — 확장 variant 토큰(`--jc-success-strong` 등)의 대비비.

**자주 쓰는 결론(요약, 정본 수치는 위 §9 표 참조)**:
- 본문에 녹색이 필요하면 `--jc-success`(`#00C853`, 본문 2.24:1 FAIL) 대신 `--jc-success-strong`(`#00733B`, 6.36:1 AA) 사용.
- 다크 액센트 `#5B8DEF` 위 흰 텍스트는 큰 텍스트(3:1)에서만 AA — 본문 라벨에 쓰지 않는다.

**구현 예 / 적용 위치**:
- `mice-dashboard/references/dark-mode-patterns.md §5` — 다크 조합 대비비 표(§9 미러).

---

## RULE-PRINT-LIGHT — 인쇄 시 라이트 강제

**정의**: 다크 모드로 표시되는 산출물(HTML 대시보드·HTML 데크)도 **인쇄(PDF 출력) 시에는 항상 라이트 모드로 강제 전환**한다. `always-dark`/사용자 토글로 다크 상태여도 인쇄 출력은 라이트여야 한다.

**근거**:
- 다크 배경 풀블리드는 잉크/토너 과다 소모 + 대비 저하로 인쇄 가독성이 떨어진다.
- 배포본(인쇄·PDF 첨부)은 라이트가 표준(`mode-mapping.md §1`: "인쇄물(배포본) = Light 강제").
- 인쇄 강제는 화면 상태를 **영구 변경하지 않는다** — 인쇄 컨텍스트에서만 라이트 토큰을 덮어쓰고, 인쇄 종료 후 원래(다크) 상태로 복귀한다.

**구현 패턴(요지)** — 산출물별 CSS/JS 는 각 스킬이 소유하되, 동작 규약은 동일하다:

```css
@media print {
  /* 다크 토글 상태여도 인쇄는 라이트 토큰으로 덮어쓴다 */
  :root, [data-theme="dark"] {
    --jc-bg: #FFFFFF !important;
    --jc-surface: #FFFFFF !important;
    --jc-text: #1A1D24 !important;
    /* 보더·차트 영역 등도 라이트 토큰으로 */
  }
}
```

라이트 강제 시 사용하는 토큰 값의 정본은 `jc-design-system/references/mode-mapping.md §4.2`(인쇄 강제 변환).

**적용 범위**: 다크 모드를 지원하는 HTML 산출물 — `mice-dashboard`, `mice-sponsor-deck`(1차 HTML 데크). PPTX/DOCX 는 기본 라이트라 별도 처리 불필요(표지 등 다크 슬라이드는 산출물 자체가 그 디자인이므로 예외).

**구현 예 / 적용 위치**:
- `mice-dashboard/references/dark-mode-patterns.md §4` — `@media print` 라이트 강제 CSS.
- `mice-sponsor-deck/references/dark-mode-patterns.md` — `beforeprint`/`afterprint` 토글 + `@media print` 라이트 강제(복귀 보장).

---

## RULE-NO-COMPANY — 회사·개인 식별정보 하드코딩 금지

**정의**: 어떤 스킬도 산출물·문서·스크립트에 **특정 회사명·개인 실명·부서명 등 식별 정보를 하드코딩하지 않는다.** 발주처·공급자·고객사·발행자·발표자 등 모든 식별 정보는 **외부 주입 변수**로만 처리하며, 사용자가 매 산출 시 직접 제공한다.

**근거**: 본 스킬 군은 특정 소속사가 아닌 **개인(MICE 전략가) 자산**이다(`jc-design-system/SKILL.md` 핵심 원칙 3 "회사 종속 표현 배제"). 회사 종속 표현이 박히면 Track A/B 양쪽 재사용이 깨지고, 산출물이 특정 고용주에 묶인다. CLAUDE.md §10(외부 주입 변수 원칙)과 동일 정책.

**금칙(하드코딩 금지) 예시**:
- 회사 상호: `엠앤씨`, `M&C`(및 `M&C커뮤니케이션즈`), `리멤버앤컴퍼니` 등 구체 상호
- 부서·조직: `신사업실` 등 내부 조직명
- 개인 실명·직함을 식별 가능한 형태로 고정

**허용**:
- 일반화 표현: "MICE 전문가", "행사 기획팀", "본 행사 사무국", "발표자", "본 PCO", "발주처"(또는 `T社`)
- **양식 식별자**로서의 명칭: mice-estimate 의 `M&C 견적서`·`리멤버 견적서`는 *양식 종류*를 가리키는 식별자이므로 보존된다(회사 상호를 산출물 본문에 쓰는 것과 구분).
- 외부 주입 변수 슬롯: `{{client_company}}`, `{{author_name}}`, `{{personal_brand}}`, `{{author_title}}`, `{{company_name}}` 등(`jc-design-system/SKILL.md` v1.1.0 표준 5종) + 연락처 슬롯 `{{author_dept}}`·`{{author_email}}`·`{{author_phone}}`(담당자 푸터용, additive 등록), 및 각 스킬의 공급자/고객사 슬롯.

**구현 예 (실제 sanitize 코드)** — 문서 규칙의 코드 레벨 구현은 다음 스크립트가 정본이다(로직 자체는 본 문서로 옮기지 않는다):
- `pt-script/scripts/build_script.py` — `sanitize_text()`: 금칙 상호/부서명을 `[발표 주체]`·`[부서명]` 등 placeholder 로 치환하고, meta 슬롯 전반에 적용.
- `mice-sponsor-deck/scripts/sample_generator.py` — `FORBIDDEN_TERMS` + `scan_forbidden_terms()`: 후보 JSON·데크 콘텐츠에서 금칙어를 검출해 검증 단계에서 차단.

**체크 항목**: 산출물·후보 JSON 에 금칙어 0건인지 검증(스킬별 QA 체크리스트의 "회사 종속 표현 0건" 항목).

---

## 변경 이력

### v1.0.0 (2026-06-02) — R3 공통 룰 통합

- 4개 공통 규칙(`RULE-PPTX-HEX`·`RULE-WCAG`·`RULE-PRINT-LIGHT`·`RULE-NO-COMPANY`)을 ID 부여하여 단일 정본화.
- 색상 *값*은 `signature-tokens.md`·`mode-mapping.md` 로 위임, 본 문서는 *정책*만 정의.
- 소비자 스킬은 짧은 인라인 리마인더를 유지하고 본 문서를 `#<RULE-ID>` 로 참조.
