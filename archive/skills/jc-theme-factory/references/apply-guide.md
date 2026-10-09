# Apply Guide — 선택/발행한 오버레이를 산출물에 적용

원본 Theme Factory의 "Apply the theme" 단계에 대응한다. 본 스킬은 "어떤 테마(오버레이)인지"를 결정하고, 실제로 산출물에 찍는 일은 매체에 따라 직접 하거나 `jc-brand-styling`에 위임한다.

## 0. 적용 원칙

- **토큰 값은 SoT 런타임 로드.** 미러 금지. `jc-design-system/scripts/jc_tokens.py`의 `load_tokens`/`color` + 본 스킬의 오버레이 파서로 최종 토큰 객체를 만든다.
- **우선순위**(`usage-guide.md §6`): ① 사용자 명시 지정 → ② 클라이언트 오버레이 → ③ 시그니처 → ④ 폴백.
- **모드 결정**(`mode-mapping.md §1`): 산출물 유형 기본값을 따르되 사용자 지정 우선.

```python
# 형제 경로로 SoT 로드 + 오버레이 적용 (개념 코드)
import sys, re, json
from pathlib import Path
SOT = Path(__file__).resolve().parents[2] / "jc-design-system"
sys.path.insert(0, str(SOT / "scripts"))
from jc_tokens import load_tokens, color            # SoT 토큰

tok = load_tokens(SOT)                               # 시그니처
ov  = parse_overlay(SOT, client_id)                  # client-overlays.md의 해당 블록
for k in ("primary", "accent"):                      # null 아닌 값만 덮어쓰기
    if ov["overrides"].get(k):
        tok["color"][k] = ov["overrides"][k]
```

## 1. 매체별 적용

| 산출물 | 기본 모드 | 적용 경로 | 핵심 |
|--------|----------|----------|------|
| **PPTX**(제안서·데크) | Light | **`jc-brand-styling`에 위임 권장** | python-pptx. hex는 `#` 없는 6자리(`RULE-PPTX-HEX`) |
| **HTML**(대시보드·아티팩트·LP) | Light + Dark 토글 | CSS 변수 주입 | `:root` 토큰 + `@media (prefers-color-scheme: dark)` + 인쇄 라이트 강제 |
| **DOCX**(대본·보고서) | Light | python-docx | 헤더 풀블리드 primary + 흰 텍스트, 강조 accent |
| **XLSX**(견적) | Light | openpyxl | 헤더 primary·합계 accent (`usage-guide.md §3.3`) |

### HTML 토큰 주입 (요지)

```css
:root{ --jc-primary:<primary>; --jc-accent:<accent>; /* 나머지는 signature-tokens §6 */ }
@media (prefers-color-scheme: dark){ :root{ /* mode-mapping §3 다크값 */ } }
@media print{ :root{ --jc-bg:#fff!important; --jc-surface:#fff!important; --jc-text:#1A1D24!important; } } /* RULE-PRINT-LIGHT */
```

오버레이가 바꾸는 건 `--jc-primary`·`--jc-accent`(및 다크 보정값)뿐이고, 나머지는 시그니처 그대로다.

## 2. jc-brand-styling 위임 (PPTX/기존 아티팩트 후처리)

이미 존재하는 PPTX나 아티팩트에 테마를 "입히는" 후처리는 `jc-brand-styling`이 전담한다. 본 스킬은 결정한 `client_id`(또는 오버레이 토큰 객체)를 넘기고, jc-brand-styling이 매체 후처리를 수행한다.

```
jc-theme-factory: 쇼케이스 → 선택/발행 → (client_id 결정)
        │  client_id / 토큰 객체 전달
        ▼
jc-brand-styling: 대상 파일(.pptx/.html)에 jc 시그니처+오버레이 스탬프
```

새로 *생성*하는 산출물(제안서·데크·대시보드 등)은 각 mice-* 스킬이 자체적으로 jc-design-system을 호출해 적용하므로, 본 스킬은 주로 (a) 쇼케이스/선택/발행과 (b) 기존 산출물 리테마(jc-brand-styling 경유)에 쓰인다.

## 3. 적용 후 점검

- [ ] 토큰 값 하드코딩 0건(SoT 참조), `check_drift.py` FORBIDDEN 0건
- [ ] 폰트 시그니처(Pretendard/Inter/JetBrains Mono) 유지
- [ ] 라이트/다크 모드 규칙 준수, 다크 HTML은 인쇄 라이트 강제
- [ ] 흰 텍스트 대비 WCAG AA↑(`RULE-WCAG`)
- [ ] (PPTX) hex `#` 없는 6자리(`RULE-PPTX-HEX`)
- [ ] 회사·개인정보 외부 주입 변수 처리(`RULE-NO-COMPANY`)
- [ ] 최종 카피·수치·대비는 `jc-redteam`으로 점검 가능
