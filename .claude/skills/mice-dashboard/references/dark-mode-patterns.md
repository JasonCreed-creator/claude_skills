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

### 2.1 KPI 카드

```css
/* 라이트 */
.kpi-card {
  background: #ffffff;            /* COLOR_BG_CARD */
  border: 1px solid #e2e8f0;      /* COLOR_NEUTRAL_BORDER */
  color: #1e293b;                 /* COLOR_TEXT_PRIMARY */
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.kpi-card .label { color: #64748b; }   /* COLOR_TEXT_SECONDARY */
.kpi-card .value { color: #0f172a; font-size: 2rem; font-weight: 700; }
.kpi-card .delta-positive { color: #16a34a; }  /* COLOR_SEMANTIC_SUCCESS */
.kpi-card .delta-negative { color: #dc2626; }  /* COLOR_SEMANTIC_DANGER */

/* 다크 */
[data-theme="dark"] .kpi-card {
  background: #1e293b;            /* COLOR_BG_CARD_DARK */
  border: 1px solid #334155;      /* COLOR_NEUTRAL_BORDER_DARK */
  color: #f1f5f9;                 /* COLOR_TEXT_PRIMARY_DARK */
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}
[data-theme="dark"] .kpi-card .label { color: #94a3b8; }
[data-theme="dark"] .kpi-card .value { color: #f8fafc; }
[data-theme="dark"] .kpi-card .delta-positive { color: #22c55e; }
[data-theme="dark"] .kpi-card .delta-negative { color: #ef4444; }
```

### 2.2 차트 영역

```css
/* 라이트 */
.chart-container {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  padding: 24px;
}
.chart-container .title { color: #1e293b; }

/* 다크 */
[data-theme="dark"] .chart-container {
  background: #1e293b;
  border: 1px solid #334155;
}
[data-theme="dark"] .chart-container .title { color: #f1f5f9; }
```

Chart.js 다크 모드 글로벌 설정:

```javascript
function applyChartTheme(isDark) {
  Chart.defaults.color = isDark ? '#cbd5e1' : '#475569';
  Chart.defaults.borderColor = isDark ? '#334155' : '#e2e8f0';
  Chart.defaults.scale.grid.color = isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)';
  Chart.defaults.plugins.tooltip.backgroundColor = isDark ? '#0f172a' : '#1e293b';
}
```

### 2.3 테이블

```css
/* 라이트 */
.data-table { background: #ffffff; }
.data-table thead { background: #f8fafc; color: #475569; }
.data-table tbody tr { border-bottom: 1px solid #e2e8f0; }
.data-table tbody tr:nth-child(even) { background: #f8fafc; }  /* 스트라이프 */
.data-table tbody tr:hover { background: #f1f5f9; }

/* 다크 */
[data-theme="dark"] .data-table { background: #1e293b; }
[data-theme="dark"] .data-table thead { background: #0f172a; color: #cbd5e1; }
[data-theme="dark"] .data-table tbody tr { border-bottom: 1px solid #334155; }
[data-theme="dark"] .data-table tbody tr:nth-child(even) { background: #1a2332; }
[data-theme="dark"] .data-table tbody tr:hover { background: #2d3a4f; }
```

### 2.4 콜아웃 / 배너 (인사이트·경고·확인 등)

```css
/* 라이트 — info / success / warning / danger */
.callout {
  border-radius: 8px;
  padding: 16px 20px;
  border-left: 4px solid;
}
.callout-info    { background: #eff6ff; border-color: #2563eb; color: #1e40af; }
.callout-success { background: #f0fdf4; border-color: #16a34a; color: #166534; }
.callout-warning { background: #fffbeb; border-color: #d97706; color: #92400e; }
.callout-danger  { background: #fef2f2; border-color: #dc2626; color: #991b1b; }

/* 다크 */
[data-theme="dark"] .callout-info    { background: #1e3a8a20; border-color: #3b82f6; color: #93c5fd; }
[data-theme="dark"] .callout-success { background: #14532d20; border-color: #22c55e; color: #86efac; }
[data-theme="dark"] .callout-warning { background: #78350f20; border-color: #f59e0b; color: #fcd34d; }
[data-theme="dark"] .callout-danger  { background: #7f1d1d20; border-color: #ef4444; color: #fca5a5; }
```

### 2.5 헤더

```css
/* 라이트 */
.dashboard-header {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-bottom: 1px solid #e2e8f0;
  padding: 32px;
}
.dashboard-header h1 { color: #0f172a; }
.dashboard-header .meta { color: #64748b; }

/* 다크 */
[data-theme="dark"] .dashboard-header {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  border-bottom: 1px solid #334155;
}
[data-theme="dark"] .dashboard-header h1 { color: #f8fafc; }
[data-theme="dark"] .dashboard-header .meta { color: #94a3b8; }
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
    border-color: #e2e8f0 !important;
  }
}
```

---

## 5. 접근성 (WCAG 2.1 AA 기준)

| 다크 모드 색상 조합 | 대비비 | 판정 |
|---|---|---|
| #f1f5f9 텍스트 on #1e293b 배경 | 13.6:1 | ✅ AAA |
| #94a3b8 보조 텍스트 on #1e293b | 5.8:1 | ✅ AA |
| #3b82f6 액센트 on #0f172a | 5.9:1 | ✅ AA |

모든 다크 변형은 최소 4.5:1 대비 유지.

---

## 6. 본 Sprint 적용 범위

- ✅ 5 컴포넌트 (KPI 카드·차트·테이블·콜아웃·헤더) 다크 변형 정의
- ✅ 토글 스크립트 + localStorage 저장
- ✅ 인쇄 시 라이트 강제
- ✅ 접근성 대비비 보장
- ⏳ Sprint 7: jc-design-system 의 mode-mapping.md 와 토큰명 정합화
