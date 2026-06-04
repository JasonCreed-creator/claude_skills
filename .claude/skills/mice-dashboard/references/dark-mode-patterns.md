# 다크 모드 패턴 (dark-mode-patterns)

**참조**: master-plan §4-2-2 (다크 모드 5종 변형 — mice-proposal v2.1 다크 패턴 포팅)
**관련**: [jc-design-mapping.md](jc-design-mapping.md) §5

v1 mice-dashboard 는 "기업/공식" 톤 하나만 다크였음. v2 는 **5개 컴포넌트별 다크 모드 변형**을 체계적 라이브러리로 정리. 사용자가 `theme=dark` 토글 시 자동 적용.

---

## 1. 다크 모드 활성화 전략

```html
<!-- 방식 1: data 속성 (권장) -->
<html data-theme="dark">

<!-- 방식 2: 클래스 -->
<html class="theme-dark">

<!-- 방식 3: 시스템 prefers-color-scheme 자동 감지 -->
@media (prefers-color-scheme: dark) { ... }
```

→ assets HTML 템플릿은 방식 1 + 방식 3 폴백 모두 지원.

---

## 2. 5개 컴포넌트 다크 변형

> **정본 출처**: 아래 CSS·JS 의 모든 hex 는 jc-design-system 정본을 미러한다. 라이트 = `signature-tokens.md` §1·§1.5·§6, 다크 = `mode-mapping.md` §3·§3.2. CSS 구조는 보존하되 값은 정본만 사용한다. (역할 주의: 같은 v1 slate hex 라도 라이트모드 텍스트는 `--jc-text`/`--jc-text-muted` 로, 다크모드 배경/보더는 다크 패밀리로 분기.)

### 2.1 KPI 카드

```css
/* 라이트 */
.kpi-card {
  background: #FFFFFF;            /* SoT 미러: --jc-surface */
  border: 1px solid #E5E8ED;      /* SoT 미러: --jc-border */
  color: #1A1D24;                 /* SoT 미러: --jc-text */
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.kpi-card .label { color: #5A6270; }   /* SoT 미러: --jc-text-muted */
.kpi-card .value { color: #1A1D24; font-size: 2rem; font-weight: 700; }  /* SoT 미러: --jc-text */
.kpi-card .delta-positive { color: #00C853; }  /* SoT 미러: --jc-success */
.kpi-card .delta-negative { color: #D32F2F; }  /* SoT 미러: --jc-danger */

/* 다크 */
[data-theme="dark"] .kpi-card {
  background: #152134;            /* SoT 미러: 다크 카드 서피스 */
  border: 1px solid #2A3650;      /* SoT 미러: 다크 보더 */
  color: #E8ECF2;                 /* SoT 미러: 다크 본문 텍스트 */
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}
[data-theme="dark"] .kpi-card .label { color: #A0A8B4; }   /* SoT 미러: 다크 보조 텍스트 */
[data-theme="dark"] .kpi-card .value { color: #E8ECF2; }   /* SoT 미러: 다크 본문 텍스트 */
[data-theme="dark"] .kpi-card .delta-positive { color: #00C853; }  /* SoT 미러: --jc-success */
[data-theme="dark"] .kpi-card .delta-negative { color: #D32F2F; }  /* SoT 미러: --jc-danger */
```

### 2.2 차트 영역

```css
/* 라이트 */
.chart-container {
  background: #FFFFFF;             /* SoT 미러: --jc-surface */
  border: 1px solid #E5E8ED;      /* SoT 미러: --jc-border */
  padding: 24px;
}
.chart-container .title { color: #1A1D24; }  /* SoT 미러: --jc-text */

/* 다크 */
[data-theme="dark"] .chart-container {
  background: #152134;            /* SoT 미러: 다크 카드 서피스 */
  border: 1px solid #2A3650;      /* SoT 미러: 다크 보더 */
}
[data-theme="dark"] .chart-container .title { color: #E8ECF2; }  /* SoT 미러: 다크 본문 텍스트 */
```

Chart.js 다크 모드 글로벌 설정:

```javascript
function applyChartTheme(isDark) {
  Chart.defaults.color = isDark ? '#A0A8B4' : '#5A6270';        // SoT 미러: 다크/라이트 보조 텍스트
  Chart.defaults.borderColor = isDark ? '#2A3650' : '#E5E8ED';  // SoT 미러: 다크/라이트 보더
  Chart.defaults.scale.grid.color = isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)';
  Chart.defaults.plugins.tooltip.backgroundColor = isDark ? '#0A1220' : '#152134';  // SoT 미러: 다크 페이지 배경 / 다크 카드 서피스
}
```

### 2.3 테이블

```css
/* 라이트 */
.data-table { background: #FFFFFF; }                                /* SoT 미러: --jc-surface */
.data-table thead { background: #F1F3F7; color: #5A6270; }          /* SoT 미러: --jc-surface-alt / --jc-text-muted */
.data-table tbody tr { border-bottom: 1px solid #E5E8ED; }          /* SoT 미러: --jc-border */
.data-table tbody tr:nth-child(even) { background: #F1F3F7; }       /* SoT 미러: --jc-surface-alt (스트라이프) */
.data-table tbody tr:hover { background: #F1F3F7; }                 /* SoT 미러: --jc-surface-alt */

/* 다크 */
[data-theme="dark"] .data-table { background: #152134; }                              /* SoT 미러: 다크 카드 서피스 */
[data-theme="dark"] .data-table thead { background: #0A1220; color: #A0A8B4; }        /* SoT 미러: 다크 페이지 배경 / 다크 보조 텍스트 */
[data-theme="dark"] .data-table tbody tr { border-bottom: 1px solid #2A3650; }        /* SoT 미러: 다크 보더 */
[data-theme="dark"] .data-table tbody tr:nth-child(even) { background: #1F2C42; }     /* SoT 미러: 다크 보조 서피스 */
[data-theme="dark"] .data-table tbody tr:hover { background: #1F2C42; }               /* SoT 미러: 다크 보조 서피스 */
```

### 2.4 콜아웃 / 배너 (인사이트·경고·확인 등)

```css
/* 라이트 — info / success / warning / danger */
.callout {
  border-radius: 8px;
  padding: 16px 20px;
  border-left: 4px solid;
}
/* SoT 미러: bg=시맨틱/액센트 @ ~9% 또는 --jc-accent-soft, border=시맨틱, text=AA 가독 변형 */
.callout-info    { background: #E8EFFF;    border-color: #2962FF; color: #2962FF; }  /* SoT 미러: --jc-accent-soft / --jc-accent */
.callout-success { background: #00C85316;  border-color: #00C853; color: #00733B; }  /* SoT 미러: --jc-success / 텍스트 --jc-success-strong(WCAG AA) */
.callout-warning { background: #FFA00016;  border-color: #FFA000; color: #FFA000; }  /* SoT 미러: --jc-warning */
.callout-danger  { background: #D32F2F16;  border-color: #D32F2F; color: #D32F2F; }  /* SoT 미러: --jc-danger */

/* 다크 — SoT 미러: bg=시맨틱/액센트 @ ~20% 알파, border·text=다크 보정 시맨틱 (mode-mapping §3.1·§3.2·§8) */
[data-theme="dark"] .callout-info    { background: #2962FF33; border-color: #5B8DEF; color: #5B8DEF; }  /* SoT 미러: 다크 액센트 */
[data-theme="dark"] .callout-success { background: #00C85333; border-color: #33EE92; color: #33EE92; }  /* SoT 미러: 다크 Neon(= 다크 data-4) */
[data-theme="dark"] .callout-warning { background: #FFA00033; border-color: #FFB74D; color: #FFB74D; }  /* SoT 미러: DARK_WARNING (mode-mapping §8) */
[data-theme="dark"] .callout-danger  { background: #D32F2F33; border-color: #F44336; color: #F44336; }  /* SoT 미러: DARK_DANGER (mode-mapping §8) */
```

### 2.5 헤더

```css
/* 라이트 */
.dashboard-header {
  background: linear-gradient(135deg, #FFFFFF 0%, #F1F3F7 100%);  /* SoT 미러: --jc-surface → --jc-surface-alt */
  border-bottom: 1px solid #E5E8ED;                               /* SoT 미러: --jc-border */
  padding: 32px;
}
.dashboard-header h1 { color: #1A1D24; }     /* SoT 미러: --jc-text */
.dashboard-header .meta { color: #5A6270; }  /* SoT 미러: --jc-text-muted */

/* 다크 */
[data-theme="dark"] .dashboard-header {
  background: linear-gradient(135deg, #0A1220 0%, #152134 100%);  /* SoT 미러: 다크 bg → surface */
  border-bottom: 1px solid #2A3650;                               /* SoT 미러: 다크 보더 */
}
[data-theme="dark"] .dashboard-header h1 { color: #E8ECF2; }     /* SoT 미러: 다크 본문 텍스트 */
[data-theme="dark"] .dashboard-header .meta { color: #A0A8B4; }  /* SoT 미러: 다크 보조 텍스트 */
```

---

## 3. 다크 모드 토글 스크립트

```html
<button id="theme-toggle" aria-label="테마 전환">🌙</button>

<script>
(function() {
  const toggle = document.getElementById('theme-toggle');
  const html = document.documentElement;

  // 초기값: localStorage > prefers-color-scheme > light
  const saved = localStorage.getItem('dashboard-theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const initial = saved || (prefersDark ? 'dark' : 'light');
  html.setAttribute('data-theme', initial);
  toggle.textContent = initial === 'dark' ? '☀️' : '🌙';

  toggle.addEventListener('click', () => {
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('dashboard-theme', next);
    toggle.textContent = next === 'dark' ? '☀️' : '🌙';
    if (typeof applyChartTheme === 'function') {
      applyChartTheme(next === 'dark');
      Chart.helpers.each(Chart.instances, (chart) => chart.update());
    }
  });
})();
</script>
```

---

## 4. 인쇄 시 라이트 강제 (PDF 출력 호환)

> 정본: `jc-design-system/references/shared-rules.md#RULE-PRINT-LIGHT` (라이트 강제 토큰 값은 `mode-mapping.md §4.2`). 아래는 본 스킬의 구현 예.

```css
@media print {
  /* 다크 모드라도 인쇄는 항상 라이트로 */
  html[data-theme="dark"] {
    --force-light: 1;
  }
  /* 모든 다크 변형 무효화 */
  [data-theme="dark"] .kpi-card,
  [data-theme="dark"] .chart-container,
  [data-theme="dark"] .data-table {
    background: white !important;
    color: black !important;
    border-color: #E5E8ED !important;   /* SoT 미러: --jc-border */
  }
}
```

---

## 5. 접근성 (WCAG 2.1 AA 기준)

> 대비 목표·정책 정본: `jc-design-system/references/shared-rules.md#RULE-WCAG`. 대비비 수치·계산 표준은 `mode-mapping.md` §9(WebAIM 표준)·§5 정본을 미러한다. 색상은 SoT 다크 패밀리.

| 다크 모드 색상 조합 | 대비비 (WebAIM 기준) | 판정 |
|---|---|---|
| `#E8ECF2` 본문 텍스트 on `#0A1220` 배경 | 14.96:1 | ✅ AAA |
| `#A0A8B4` 보조 텍스트 on `#0A1220` | 8.21:1 | ✅ AAA |
| `#FFFFFF` on `#5B8DEF` (다크 액센트) | 3.41:1 | ✅ AA(큰 텍스트만) |

모든 다크 변형은 본문 4.5:1 / 큰 텍스트 3:1 (WCAG AA) 이상 유지. 수치 산출 공식·도구는 `mode-mapping.md` §9.1·§9.3 표준.

---

## 6. 본 Sprint 적용 범위

- ✅ 5 컴포넌트 (KPI 카드·차트·테이블·콜아웃·헤더) 다크 변형 정의
- ✅ 토글 스크립트 + localStorage 저장
- ✅ 인쇄 시 라이트 강제
- ✅ 접근성 대비비 보장
- ✅ jc-design-system 의 mode-mapping.md(§3·§3.2) 와 토큰명·값 정합화 완료 (R1 SoT 정합화 — 모든 hex 를 SoT 다크 패밀리/시맨틱으로 교정, slate 계열 제거)
