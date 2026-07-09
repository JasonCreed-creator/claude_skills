# Usage Guide — 다른 스킬에서 호출하는 방법

`mice-proposal`, `mice-estimate`, `pt-script`, `mice-dashboard` 등 다른 스킬이 본 디자인 시스템을 참조하는 표준 절차를 정의한다.

---

## 1. 호출 표준 절차 (4단계)

### Step 1. 시그니처 토큰 로드

```
references/signature-tokens.md 의 §6 JSON 추출 블록을 읽어
토큰 객체로 메모리에 보관
```

### Step 2. 클라이언트 오버레이 적용

```
사용자 또는 호출 스킬이 client_id 를 지정한 경우:
    references/client-overlays.md 에서 해당 항목 조회
    overrides 의 null 이 아닌 값만 토큰 객체에 덮어쓰기

client_id 미지정 시:
    "personal" 오버레이 적용 (시그니처 그대로)
```

### Step 3. 모드 결정

```
산출물 유형별 기본 모드 (references/mode-mapping.md §1):
    PPTX 제안서 → Light
    XLSX 견적서 → Light
    DOCX 대본   → Light
    HTML 대시보드 → Light + Dark 토글
    표지 슬라이드 → Dark (선택적)

다크 모드인 경우:
    references/mode-mapping.md §3 매핑 테이블로 토큰 변환
```

### Step 4. 컴포넌트 패턴 적용

```
산출물에 필요한 컴포넌트를 references/component-patterns.md 에서 참조:
    KPI 카드 → §1
    차트 컨테이너 → §2
    섹션 구분 → §3
    테이블 → §4
    헤더/표지/푸터 → §5
    배지·콜아웃 → §6, §7

§8 동시 사용 규칙 준수
```

---

## 2. 스킬별 적용 가이드

### 2.1 mice-proposal (제안서)

**적용 우선순위**: 표지 → 헤더/푸터 → 섹션 타이틀 → 차트 → KPI 카드 → 테이블

**필수 적용**:
- 표지: `component-patterns.md §5.2` (Dark 풀블리드)
- 본문 페이지: Light 모드 + 상단 헤더 (§5.1)
- 섹션 타이틀: §3.1 (액센트 라인 + 번호)
- 폰트: 한글 Pretendard, 영문 Inter, 숫자 JetBrains Mono

**클라이언트 처리**:
- 표지 우상단에 `client_name` 표기
- 표지 좌하단에 클라이언트 로고 (있을 시)

### 2.2 mice-estimate (견적서)

**적용 우선순위**: 헤더 → 테이블 → 합계 행

**필수 적용**:
- 상단 헤더: `--jc-primary` 풀블리드 + 흰색 텍스트
- 테이블: §4.1 표준 테이블
- 합계 행: `--jc-primary` 배경 + 흰색 텍스트
- 금액 컬럼: `--jc-font-mono` + 우측 정렬 + 천단위 콤마

**클라이언트 처리**:
- 헤더 좌측에 클라이언트 로고
- 헤더 우측에 발행일·견적번호

### 2.3 pt-script (발표 대본)

**적용 우선순위**: 문서 헤더 → 슬라이드 라벨 → 본문 → 강조

**필수 적용**:
- 문서 헤더: §5.1 압축형
- 슬라이드 번호 라벨: 배지 형태 (§6.1)
- 본문: `--jc-text` + `--jc-leading-relaxed` (1.7)
- 강조 멘트: 콜아웃 (§7)
- 시간 표시: `--jc-font-mono`

**컬러 운용**:
- 액센트(파란색) — 강조 멘트
- Orange — 주의·강조 표시
- 단조로움 회피 위해 페이지당 강조 1~2회 한정

### 2.4 mice-dashboard (대시보드)

**적용 우선순위**: KPI 카드 → 차트 → 테이블 → 필터/컨트롤

**필수 적용**:
- 라이트/다크 자동 토글 (§4.1 mode-mapping)
- KPI 카드: §1.1 표준형 또는 §1.2 강조형
- 차트: §2.1 컨테이너 + 데이터 시리즈 5단계
- 인터랙티브 호버: `--jc-accent-soft` 배경

**컬러 운용**:
- data-1 (Electric Blue) → 메인 지표
- data-2 (Magenta) → 비교 지표
- data-3 (Orange) → 핫스팟
- data-4 (Neon) → 라이브·실시간만
- data-5 (Deep Navy) → 누적·합계

---

## 3. 코드 호출 패턴

### 3.1 Python (PPTX·DOCX·XLSX 생성)

> ✅ **구현체 제공:** `jc-design-system/scripts/jc_tokens.py` (`load_tokens`/`color`, 테스트 `test_jc_tokens.py`). mice-estimate·pt-script·mice-sponsor-deck 스크립트가 형제 경로의 SoT §6 JSON 을 **런타임 로딩**하며, 실패 시 미러값으로 폴백한다. (구 'Sprint 7 런타임 fetch' 목표 완결.)

```python
import json
import re
from pathlib import Path

def load_jc_tokens(skill_path: Path, client_id: str = "personal") -> dict:
    """JC 디자인 시스템 토큰을 로드하고 클라이언트 오버레이 적용"""
    
    # 1. 시그니처 토큰 로드
    sig_md = (skill_path / "references" / "signature-tokens.md").read_text(encoding="utf-8")
    sig_json = re.search(r'```json\n(.*?)\n```', sig_md, re.DOTALL)
    tokens = json.loads(sig_json.group(1))
    
    # 2. 클라이언트 오버레이 적용
    overlay_md = (skill_path / "references" / "client-overlays.md").read_text(encoding="utf-8")
    # client_id 매칭 블록 파싱 후 overrides 적용
    # (null 항목은 시그니처 유지)
    
    return tokens

# 사용 예시
tokens = load_jc_tokens(Path("/path/to/jc-design-system"), client_id="remember")
primary_color = tokens["color"]["primary"]      # "#0A2540"
accent_color  = tokens["color"]["accent"]       # "#2962FF"
data_series   = tokens["color"]["data"]         # 5색 리스트
```

### 3.2 PPTX 색상 적용 (python-pptx)

```python
from pptx.dml.color import RGBColor

def hex_to_rgb(hex_str: str) -> RGBColor:
    h = hex_str.lstrip('#')
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

# 표지 배경
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = hex_to_rgb(tokens["color"]["primary"])

# 액센트 라인
shape.fill.solid()
shape.fill.fore_color.rgb = hex_to_rgb(tokens["color"]["accent"])
```

### 3.3 XLSX 색상 적용 (openpyxl)

```python
from openpyxl.styles import PatternFill, Font

# 헤더 행
header_fill = PatternFill("solid", fgColor=tokens["color"]["primary"].lstrip("#"))
header_font = Font(name="Pretendard", size=14, bold=True, color="FFFFFF")

# 합계 행 강조
total_fill = PatternFill("solid", fgColor=tokens["color"]["accent"].lstrip("#"))
```

### 3.4 HTML/CSS 적용

```html
<style>
:root {
  --jc-primary: #0A2540;
  --jc-accent: #2962FF;
  --jc-text: #1A1D24;
  /* signature-tokens.md §6 JSON 을 CSS 변수로 변환 */
}

@media (prefers-color-scheme: dark) {
  :root {
    --jc-primary: #0A2540;
    --jc-bg: #0A1220;
    /* mode-mapping.md §3 매핑 적용 */
  }
}
</style>
```

---

## 4. 자동 호출 트리거 (다른 스킬 SKILL.md 작성 시 권장)

> ※ 이하는 스킬 저작자를 위한 메타 안내이며 실행 시 참조 불필요.

다른 스킬 작성 시 SKILL.md 본문에 다음 문장 포함을 권장:

```markdown
## 디자인 적용
산출물 생성 직전 jc-design-system 스킬의 references/ 를 로드하여
시그니처 토큰을 적용한다. 클라이언트가 지정된 경우 오버레이를 함께 적용한다.
```

---

## 5. 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| 한글 깨짐 | Pretendard 미설치 환경 | 폴백 `Apple SD Gothic Neo` / `Malgun Gothic` 적용 (signature-tokens.md §2.3) |
| 네온 그린이 인쇄에서 칙칙함 | 형광 컬러 인쇄 한계 | `#00C853` 폴백 자동 적용 |
| 다크 모드에서 액센트가 너무 어두움 | 라이트 모드 토큰 그대로 사용 | mode-mapping.md §3 매핑으로 `#5B8DEF` 사용 |
| 차트 시리즈가 너무 많아 구분 안 됨 | 시리즈 4종 이상 사용 | 최대 3종으로 제한, 나머지는 그레이 톤 처리 |
| 클라이언트 컬러가 시그니처와 충돌 | CI 컬러가 Deep Navy와 유사 | client-overlays.md §6 충돌 회피 규칙 적용 |

---

## 6. 우선순위 매트릭스

산출물 빌드 시 디자인 토큰 적용 우선순위:

```
1. 사용자 명시 지정          ← 최우선 (절대값)
2. 클라이언트 오버레이
3. 시그니처 토큰
4. 폴백 (시스템 기본)        ← 최종 안전망
```

상위 단계 값이 있으면 하위 단계는 무시한다.

---

## 7. 실제 사용 사례 (Sprint 1~6 결과 기반)

본 스킬이 다른 7개 스킬에서 어떻게 적용되었는지 실제 산출물 기반 정리. v1.1.0 추가 (Sprint 1~6 완료 후).

### 7.1 mice-estimate (Sprint 1) — XLSX 견적서

**적용 패턴**: Excel 셀 색상이 jc-design 토큰에 매핑

| 셀 영역 | 토큰 | HEX | 적용 방식 |
|---------|------|-----|----------|
| 헤더 행 (1~3행) | `--jc-primary` | `#0A2540` | openpyxl PatternFill |
| 항목 라벨 컬럼 | `--jc-text` | `#1A1D24` | Font color |
| 금액 컬럼 | `--jc-font-mono` | JetBrains Mono | Font name |
| 합계 행 | `--jc-accent` | `#2962FF` | PatternFill + 흰색 텍스트 |
| 부가세 행 | `--jc-text-muted` | `#5A6270` | Font color |

**견적서 양식 A / 양식 B 공통**: 헤더는 `--jc-primary`, 합계는 `--jc-accent`로 통일.

### 7.2 mice-dashboard (Sprint 2) — HTML 인터랙티브 대시보드

**적용 패턴**: 4종 자체 팔레트 → JC 시맨틱 토큰 매핑 + 다크 모드 5종 변형

| 자체 팔레트 | 매핑 JC 토큰 |
|-------------|-------------|
| KPI 카드 강조 | `--jc-accent` |
| 트렌드 상승 | `--jc-success` (또는 `--jc-success-strong` for AA) |
| 트렌드 하락 | `--jc-danger` |
| 데이터 시리즈 5종 | `--jc-data-1` ~ `--jc-data-5` |
| 다크 토글 배경 | DARK_BG (`#0A1220`) |

**Chart.js 적용**: 차트 색상은 CSS 변수로 동적 주입 (§7.8 가이드 참조)

### 7.3 mice-sponsor-deck (Sprint 3) — HTML 슬라이드 데크

**적용 패턴**: SVP-1~SVP-7 7종 비주얼 패턴 + DARK 5종 토글 + Tier 색상 6종 매핑

| 패턴 | 핵심 토큰 |
|------|-----------|
| SVP-1 (표지 임팩트) | `--jc-primary` 풀블리드 + `--jc-accent` 라인 |
| SVP-6 (퍼널 5단계) | `--jc-accent` → `--jc-accent-light` (`#5B9BD5`) 그라데이션 |
| SVP-7 (2x2 매트릭스) | Q1 Magenta / Q2 Accent / Q3 Orange / Q4 `--jc-point-orange-softest` (`#FFF3E0`) |
| Tier 1/2/3 배지 | Magenta / Accent / Orange POINT 시리즈 |

**다크 모드 토글**: §7 Tier 다크 변형 표 적용. F06292 / 5B8DEF / FF7043 / B8C5D6 / 3D5F87 / 69F0AE

### 7.4 pt-script (Sprint 4) — DOCX 발표 대본

**적용 패턴**: docx 헤더 컬러·강조 컬러·표 스타일·시간 초과 경고가 jc-design 토큰 매핑

| 영역 | 토큰 | 적용 |
|------|------|------|
| 문서 헤더 | `--jc-primary` 풀블리드 | python-docx paragraph shading |
| 슬라이드 라벨 배지 | `--jc-accent-soft` 배경 + `--jc-accent-strong` 텍스트 | Run.font.color |
| 강조 멘트 콜아웃 | `--jc-accent` 좌측 3px 라인 | Border style |
| 시간 초과 경고 | `--jc-danger` | Font.highlight_color |
| Q&A 예상 답변 레이블 | `--jc-success-strong` (`#00733B`) | WCAG AA 충족 (BL-S4-1 반영) |

### 7.5 mice-meeting-minutes (Sprint 5) — HTML 대시보드 + 다크 토글

**적용 패턴**: HTML 대시보드 다크 모드 토글 + 8축 KPI 카드 다크 변형

| 8축 카드 | 컬러 토큰 |
|----------|----------|
| 안건 (Agenda) | `--jc-primary` |
| 발언요지 (Remarks) | `--jc-text` |
| 결정사항 (Decisions) | `--jc-success-strong` |
| Action Items | `--jc-accent` |
| 리스크 (Risks) | `--jc-danger` |
| 미결사항 (Open Items) | `--jc-warning` |
| 후속일정 (Schedule) | `--jc-text-muted` |
| 전략메모 (Strategy) | `--jc-point-magenta` |

**Priority 라인 다크**: priority-p1 / p2 / p3 = DARK_DANGER / DARK_WARNING / DARK_TEXT_MUTED (BL-S5-1 반영)

### 7.6 mice-rfp-analyzer (Sprint 6) — DOCX 분석 보고서 + XLSX 평가 매트릭스

**적용 패턴**: docx 분석 보고서 + xlsx 평가 매트릭스 + GO/HOLD/NO-GO 판정 색상

| 판정 | STATUS 시리즈 (의미적) | POINT 시리즈 (시각적 임팩트) |
|------|---------------------|---------------------------|
| GO | `--jc-success-strong` (`#00733B`) | `--jc-point-neon` (`#00E676`) |
| HOLD | `--jc-warning` (`#FFA000`) | `--jc-point-orange` (`#FF5722`) |
| NO-GO | `--jc-danger` (`#D32F2F`) | `--jc-point-magenta` (`#E91E63`) |

**선택 가이드**: §9 component-patterns.md 시리즈 선택 가이드 참조 (BL-S6-1 반영)

### 7.7 mice-proposal v2.1.1 (기준점) — PPTX 제안서

**적용 패턴**: 17개 비주얼 패턴 + 5개 확장 모듈 (인포그래픽·다크·아이콘·마스터·jc-design 연동)

| 모듈 | 핵심 토큰 |
|------|-----------|
| 표지 풀블리드 | `--jc-primary` + `--jc-accent` 라인 |
| 섹션 타이틀 | `--jc-accent` 라인 + `--jc-primary` 헤딩 |
| KPI 카드 | `--jc-surface` 배경 + `--jc-accent` 강조 |
| 차트 시리즈 | `--jc-data-1` ~ `--jc-data-5` |
| 인포그래픽 (퍼널/매트릭스/타임라인) | POINT 시리즈 4종 + 확장 variant |
| 다크 마스터 슬라이드 | 다크 모드 매핑 표 전체 적용 |

A+ 등급 기준점. 모든 후속 스킬은 이 패턴을 따른다.

---

## 8. Chart.js CSS 변수 직접 참조 가이드 (BL-S2-3)

Chart.js v3+에서 `--jc-data-1` 등 CSS 변수를 차트 `backgroundColor`·`borderColor` 에 직접 주입하는 패턴.

### 8.1 패턴 코드 (JavaScript)

```javascript
// CSS 변수에서 토큰 값 추출
const root = document.documentElement;
const tokens = {
  primary: getComputedStyle(root).getPropertyValue('--jc-primary').trim(),
  accent: getComputedStyle(root).getPropertyValue('--jc-accent').trim(),
  data1: getComputedStyle(root).getPropertyValue('--jc-data-1').trim(),
  data2: getComputedStyle(root).getPropertyValue('--jc-data-2').trim(),
  data3: getComputedStyle(root).getPropertyValue('--jc-data-3').trim(),
  data4: getComputedStyle(root).getPropertyValue('--jc-data-4').trim(),
  data5: getComputedStyle(root).getPropertyValue('--jc-data-5').trim(),
};

// Chart.js 차트 생성
const ctx = document.getElementById('myChart').getContext('2d');
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['1월', '2월', '3월', '4월'],
    datasets: [{
      label: '매출',
      data: [12, 19, 3, 5],
      backgroundColor: tokens.data1,
      borderColor: tokens.data1,
      borderWidth: 2
    }, {
      label: '비용',
      data: [8, 12, 5, 7],
      backgroundColor: tokens.data2,
      borderColor: tokens.data2
    }]
  },
  options: {
    plugins: {
      legend: { labels: { color: tokens.primary } }
    },
    scales: {
      x: { ticks: { color: tokens.primary } },
      y: { ticks: { color: tokens.primary } }
    }
  }
});
```

### 8.2 다크 모드 자동 갱신

```javascript
// prefers-color-scheme 변경 감지 시 차트 재생성
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
  // CSS 변수는 :root + @media 로 자동 갱신됨
  // 차트 갱신은 chart.update() 호출
  chart.data.datasets[0].backgroundColor = getComputedStyle(root).getPropertyValue('--jc-data-1').trim();
  chart.update();
});
```

### 8.3 투명도 추가 (rgba 변환)

```javascript
function hexToRgba(hex, alpha) {
  const h = hex.replace('#', '');
  const r = parseInt(h.substring(0,2), 16);
  const g = parseInt(h.substring(2,4), 16);
  const b = parseInt(h.substring(4,6), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

// 사용 예: 배경 반투명
dataset.backgroundColor = hexToRgba(tokens.data1, 0.3);  // "rgba(41, 98, 255, 0.3)"
```

### 8.4 적용 스킬

mice-dashboard (Sprint 2), mice-meeting-minutes (Sprint 5) HTML 대시보드 산출물에서 본 패턴 사용. CSS 변수가 토큰과 1:1 매핑되므로 라이트/다크 모드 전환 시 차트도 자동 갱신.
