# Usage Guide — 다른 스킬에서 호출하는 방법

---

## 1. 호출 표준 절차

```
Step 1  토큰 로드      scripts/jc_tokens.py → load_tokens()  (§6 JSON)
Step 2  발주처 슬롯     client-overlays.md → logo_path / cover_image / footer_text
Step 3  모드 결정      mode-mapping.md §1 (기본 라이트, 다크는 표지·섹션·클로징·토글)
Step 4  패턴 적용      component-patterns.md (산출물 유형별)
Step 5  규칙 점검      shared-rules.md (WCAG · PRINT-LIGHT · PPTX-HEX · NO-COMPANY)
```

SoT 경로 탐색 순서(소비 스크립트 공통):
1. 형제 경로 `Path(__file__).resolve().parents[2] / "jc-design-system"` (레포·claude.ai 설치본)
2. `~/.claude/skills/jc-design-system` (Claude Code 개인 스킬)
3. `~/.claude/skills/synced/*/jc-design-system` (claude.ai 동기화본)
4. 실패 시 각 스크립트의 폴백 상수(출처 주석 필수)

## 2. 스킬별 적용 가이드

| 스킬 | 산출물 | 적용 요지 |
|------|--------|-----------|
| jc-pptx | PPTX | `themes.md`의 `remember` 프리셋이 §6 JSON을 매핑. 다크는 표지·섹션·클로징만. 발주처 슬롯 3종 |
| mice-ops-docs | HTML·md·xlsx | 문서 헤더·섹션 넘버링·카드·표 패턴. 탭형 문서는 플레이북 컴포넌트 |
| mice-meeting-minutes | 단일 HTML 대시보드 | §3 KPI 카드·§4 칸반·§6 차트 S1~S5, 로고 슬롯, 인쇄 라이트 강제(v2.2.0 jc_tokens 런타임 로드) |
| pt-script | DOCX | 헤더 잉크 밴드 + 오렌지 룰, 본문 Pretendard 11pt, 강조 `#B8431A` |
| mice-rfp-analyzer | DOCX·XLSX | 헤더 잉크 배경 + 오렌지 라벨, 평가 매트릭스 셀 배지색(§2 배지) |
| mice-run-of-show | XLSX 큐시트 | 헤더 잉크 밴드 + 웜 서피스 행, 큐 유형 배지색(§2 배지). 인쇄 라이트 |
| mice-aftermath | HTML·DOCX 결과보고 | 문서 헤더·KPI 카드(목표 대비)·표 패턴. 리멤버 명의 기본 |
| jc-strategy-canvas | HTML 캔버스 | 잉크 헤더 + 웜 카드 그리드, `[검증]/[가설]/[추정]` 배지 |
| mice-market-intel | HTML·md 리포트 | 문서 헤더·출처 티어 배지·표 패턴, 차트 시리즈 S1~S5 |
| jc-redteam | md·HTML 감수 리포트 | 심각도 배지(부정·앰버 배지·캡션), 헤더 잉크 + 오렌지 룰 |
| jc-kv-guide | HTML + MD 가이드 | 발행 명의 리멤버 MICE비즈팀, 오렌지 큰 글자 전용(작은 강조는 딥 오렌지), 템플릿 CSS는 §6 미러(출처 주석) |
| mice-team-board | Apps Script HTML | 팀 보드 `styles.css`가 곧 구현체 — 토큰 변경 시 그 파일도 동기화 |
| mice-slack-ops | 캔버스·메시지 | 색 없음. 구조 규칙만(`mice-slack-ops/references/canvas-rules.md`) |

## 3. 코드 패턴

### 3.1 Python 토큰 로드

```python
import sys
from pathlib import Path

def find_sot():
    here = Path(__file__).resolve()
    for c in [here.parents[2] / "jc-design-system",
              Path.home() / ".claude/skills/jc-design-system",
              *Path.home().glob(".claude/skills/synced/*/jc-design-system")]:
        if (c / "references/signature-tokens.md").is_file():
            return c
    return None

SOT = find_sot()
sys.path.insert(0, str(SOT / "scripts"))
from jc_tokens import load_tokens, color, dark

tok = load_tokens(SOT)
ACCENT = color(tok, "accent", "#EB6F2A")        # "#EB6F2A"
INK    = color(tok, "text", "#1A1A1A")
DARK_BG = dark(tok, "bg", "#141210")
SERIES = tok["color"]["data"]
```

### 3.2 python-pptx (RULE-PPTX-HEX — `#` 없이)

```python
from pptx.dml.color import RGBColor
def C(h): return RGBColor.from_string(h.lstrip("#"))
shape.fill.solid(); shape.fill.fore_color.rgb = C(color(tok, "accent"))
```

한글 렌더링을 위해 run 폰트는 latin·ea·cs 세 곳에 모두 지정한다(`jc-pptx/scripts/deck_kit.py` `set_font_all`).

### 3.3 openpyxl

```python
from openpyxl.styles import PatternFill, Font
hdr = PatternFill("solid", fgColor=color(tok, "primary", hash_prefix=False))   # 1A1A1A
lab = Font(name="Pretendard", bold=True, color=color(tok, "accent", hash_prefix=False))
```

### 3.4 HTML/CSS

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css">
<style>
:root{--paper:#FBFAF6;--surface:#FFFFFF;--surface-warm:#F4F1EA;--ink:#1A1A1A;--ink-sub:#6E6E6E;--warm-gray:#8C867A;
--border:#DCD6C8;--line:#C9C9C0;--line-soft:#EFEBE2;--brown:#4A463F;--charcoal:#332F29;--orange:#EB6F2A;--orange-deep:#B8431A;
--orange-soft:#F5A05A;--orange-tint:#FFF1E6;--orange-pale:#F3B48A;--steel:#476580;--steel-tint:#E8EEF3;--positive:#196B24;
--positive-bg:#E7EFE8;--negative:#D93636;--negative-bg:#FBE9E9;--amber:#D39A1F;--amber-bg:#FBF2DF;
--s1:#EB6F2A;--s2:#476580;--s3:#4A463F;--s4:#8C867A;--s5:#F3B48A;--shadow:0 2px 12px rgba(74,70,63,.08);
--r-card:12px;--r-btn:6px;--font:"Pretendard Variable",Pretendard,"Apple SD Gothic Neo","Malgun Gothic",sans-serif}
:root[data-theme="dark"]{--paper:#211E1A;--surface:#2A2620;--surface-warm:#322D26;--ink:#F4F0E9;--ink-sub:#A89F92;--warm-gray:#6E655A;
--border:#3E3931;--line:#4A443B;--line-soft:#383229;--brown:#C9C0B2;--charcoal:#171512;--orange-deep:#F08A4C;--orange-tint:#3A2A1E;
--steel:#8FAEC7;--steel-tint:#26313A;--positive:#6FBF7C;--positive-bg:#22301F;--negative:#F07A7A;--negative-bg:#3A2323;
--amber:#E2B558;--amber-bg:#3A3021;--shadow:0 2px 12px rgba(0,0,0,.32)}
body{background:var(--paper);color:var(--ink);font-family:var(--font)}
.num{font-variant-numeric:tabular-nums}
</style>
```

이 변수 이름은 팀 보드·플레이북 HTML과 같다. 새 HTML 산출물도 같은 이름을 쓰면 컴포넌트를 그대로 옮길 수 있다. Claude Design DS와 연결할 때는 `--rm-*` 접두 토큰(`remember-proposal-ds/packages/tokens/css`)을 `@import`한다.

### 3.5 Chart.js

```js
const v = k => getComputedStyle(document.documentElement).getPropertyValue(k).trim();
const series = ['--s1','--s2','--s3','--s4','--s5'].map(v);
// 테마 토글 후: chart.data.datasets.forEach((d,i)=>d.backgroundColor=series[i]); chart.update();
```

## 4. 자동 호출 트리거 (소비 스킬 SKILL.md 권장 문구)

```
## 디자인 적용
- 정본: jc-design-system (v2 리멤버 웜 페이퍼). 값 하드코딩 금지 — scripts/jc_tokens.py 런타임 로드.
- 발주처 슬롯: client-overlays.md §1. 규칙: shared-rules.md#RULE-WCAG / #RULE-PRINT-LIGHT / #RULE-PPTX-HEX.
```

## 5. 트러블슈팅

| 증상 | 원인 → 조치 |
|------|-------------|
| PPTX 한글이 다른 서체로 보임 | `a:ea` 미지정 → `set_font_all` 사용 |
| 오렌지 글자가 흐릿함 | 작은 글자에 `#EB6F2A` → `#B8431A`로 |
| 색이 안 먹힘(python-pptx) | `#` 포함 → 6자리로 |
| 다크 인쇄가 검게 나옴 | `@media print` 라이트 강제 누락 → mode-mapping §4.2 |
| SoT 못 찾음 | 경로 탐색 §1 순서 확인, 폴백 상수 출처 주석 |
