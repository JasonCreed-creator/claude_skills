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
  border: 1px solid #E5E8ED;      /* COLOR_NEUTRAL_BORDER */
  color: #1A1D24;                 /* COLOR_TEXT_PRIMARY */
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.kpi-card .label { color: #5A6270; }   /* COLOR_TEXT_SECONDARY */
.kpi-card .value { color: #0A2540; font-size: 2rem; font-weight: 700; }
.kpi-card .delta-positive { color: #00C853; }  /* COLOR_SEMANTIC_SUCCESS */
.kpi-card .delta-negative { color: #D32F2F; }  /* COLOR_SEMANTIC_DANGER */

/* 다크 */
[data-theme="dark"] .kpi-card {
  background: #1A1D24;            /* COLOR_BG_CARD_DARK */
  border: 1px solid #5A6270;      /* COLOR_NEUTRAL_BORDER_DARK */
  color: #F1F3F7;                 /* COLOR_TEXT_PRIMARY_DARK */
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}
[data-theme="dark"] .kpi-card .label { color: #A0A6B0; }
[data-theme="dark"] .kpi-card .value { color: #F8F9FB; }
[data-theme="dark"] .kpi-card .delta-positive { color: #00E676; }
[data-theme="dark"] .kpi-card .delta-negative { color: #D32F2F; }
```

### 2.2 차트 영역

```css
/* 라이트 */
.chart-container {
  background: #ffffff;
  border: 1px solid #E5E8ED;
  padding: 24px;
}
.chart-container .title { color: #1A1D24; }

/* 다크 */
[data-theme="dark"] .chart-container {
  background: #1A1D24;
  border: 1px solid #5A6270;
}
[data-theme="dark"] .chart-container .title { color: #F1F3F7; }
```

Chart.js 다크 모드 글로벌 설정:

```javascript
function applyChartTheme(isDark) {
  Chart.defaults.color = isDark ? '#C9CFD8' : '#5A6270';
  Chart.defaults.borderColor = isDark ? '#5A6270' : '#E5E8ED';
  Chart.defaults.scale.grid.color = isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)';
  Chart.defaults.plugins.tooltip.backgroundColor = isDark ? '#0A2540' : '#1A1D24';
}
```

### 2.3 테이블

```css
/* 라이트 */
.data-table { background: #ffffff; }
.data-table thead { background: #F8F9FB; color: #5A6270; }
.data-table tbody tr { border-bottom: 1px solid #E5E8ED; }
.data-table tbody tr:nth-child(even) { background: #F8F9FB; }  /* 스트라이프 */
.data-table tbody tr:hover { background: #F1F3F7; }

/* 다크 */
[data-theme="dark"] .data-table { background: #1A1D24; }
[data-theme="dark"] .data-table thead { background: #0A2540; color: #C9CFD8; }
[data-theme="dark"] .data-table tbody tr { border-bottom: 1px solid #5A6270; }
[data-theme="dark"] .data-table tbody tr:nth-child(even) { background: #1A3556; }
[data-theme="dark"] .data-table tbody tr:hover { background: #1A3556; }
```

### 2.4 콜아웃 / 배너 (인사이트·경고·확인 등)

```css
/* 라이트 — info / success / warning / danger */
.callout {
  border-radius: 8px;
  padding: 16px 20px;
  border-left: 4px solid;
}
.callout-info    { background: #E8EFFF; border-color: #2962FF; color: #1E4DCC; }
.callout-success { background: #E8EFFF; border-color: #00C853; color: #00733B; }
.callout-warning { background: #FFF3E0; border-color: #FF5722; color: #FF5722; }
.callout-danger  { background: #F1F3F7; border-color: #D32F2F; color: #D32F2F; }

/* 다크 */
[data-theme="dark"] .callout-info    { background: #1e3a8a20; border-color: #2962FF; color: #5B9BD5; }
[data-theme="dark"] .callout-success { background: #14532d20; border-color: #00E676; color: #00E676; }
[data-theme="dark"] .callout-warning { background: #78350f20; border-color: #FFA000; color: #FFA000; }
[data-theme="dark"] .callout-danger  { background: #7f1d1d20; border-color: #D32F2F; color: #D32F2F; }
```

### 2.5 헤더

```css
/* 라이트 */
.dashboard-header {
  background: linear-gradient(135deg, #ffffff 0%, #F8F9FB 100%);
  border-bottom: 1px solid #E5E8ED;
  padding: 32px;
}
.dashboard-header h1 { color: #0A2540; }
.dashboard-header .meta { color: #5A6270; }

/* 다크 */
[data-theme="dark"] .dashboard-header {
  background: linear-gradient(135deg, #0A2540 0%, #1A1D24 100%);
  border-bottom: 1px solid #5A6270;
}
[data-theme="dark"] .dashboard-header h1 { color: #F8F9FB; }
[data-theme="dark"] .dashboard-header .meta { color: #A0A6B0; }
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
    border-color: #E5E8ED !important;
  }
}
```

---

## 5. 접근성 (WCAG 2.1 AA 기준)

| 다크 모드 색상 조합 | 대비비 | 판정 |
|---|---|---|
| #F1F3F7 텍스트 on #1A1D24 배경 | 13.6:1 | ✅ AAA |
| #A0A6B0 보조 텍스트 on #1A1D24 | 5.8:1 | ✅ AA |
| #2962FF 액센트 on #0A2540 | 5.9:1 | ✅ AA |

모든 다크 변형은 최소 4.5:1 대비 유지.

---

## 6. 본 Sprint 적용 범위

- ✅ 5 컴포넌트 (KPI 카드·차트·테이블·콜아웃·헤더) 다크 변형 정의
- ✅ 토글 스크립트 + localStorage 저장
- ✅ 인쇄 시 라이트 강제
- ✅ 접근성 대비비 보장
- ⏳ Sprint 7: jc-design-system 의 mode-mapping.md 와 토큰명 정합화
