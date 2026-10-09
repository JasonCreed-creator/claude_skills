# 인포그래픽 패턴 (infographic-patterns)

**참조**: master-plan §4-2-2 (인포그래픽 3종 추가 — 퍼널·매트릭스·레이더 HTML)
**관련**: [dark-mode-patterns.md](dark-mode-patterns.md), [jc-design-mapping.md](jc-design-mapping.md)

v1 mice-dashboard 는 Chart.js 기반 표준 차트 6종(바·라인·도넛·레이더·스택드바·혼합)만 지원. v2 는 **MICE 행사 결과 분석에 특화된 인포그래픽 3종**을 HTML/CSS 기반으로 추가.

---

## 1. 퍼널 (Funnel) — 전환 분석

**적합 데이터**: 단계별 인원 감소 (방문→등록→입장→세션참여→설문응답)

### 1.1 HTML 구조

```html
<div class="infographic funnel">
  <h3 class="ig-title">참가 전환 퍼널</h3>
  <ul class="funnel-steps">
    <li class="funnel-step" style="--width: 100%; --color: var(--series-1);">
      <span class="step-label">관심 (웹 방문)</span>
      <span class="step-value">5,000명</span>
      <span class="step-pct">100%</span>
    </li>
    <li class="funnel-step" style="--width: 60%; --color: var(--series-2);">
      <span class="step-label">등록 완료</span>
      <span class="step-value">3,000명</span>
      <span class="step-pct">60%</span>
      <span class="step-drop">▼ 40% 이탈</span>
    </li>
    <li class="funnel-step" style="--width: 50%; --color: var(--series-3);">
      <span class="step-label">현장 입장</span>
      <span class="step-value">2,500명</span>
      <span class="step-pct">50%</span>
      <span class="step-drop">▼ 17% 이탈</span>
    </li>
    <li class="funnel-step" style="--width: 36%; --color: var(--series-4);">
      <span class="step-label">세션 참여</span>
      <span class="step-value">1,800명</span>
      <span class="step-pct">36%</span>
      <span class="step-drop">▼ 28% 이탈</span>
    </li>
    <li class="funnel-step" style="--width: 24%; --color: var(--series-5);">
      <span class="step-label">설문 응답</span>
      <span class="step-value">1,200명</span>
      <span class="step-pct">24%</span>
      <span class="step-drop">▼ 33% 이탈</span>
    </li>
  </ul>
</div>
```

### 1.2 CSS

```css
.infographic.funnel { padding: 24px; }
.funnel-steps { list-style: none; padding: 0; margin: 0; }
.funnel-step {
  display: grid;
  grid-template-columns: 200px 1fr auto auto;
  gap: 16px;
  align-items: center;
  margin: 8px 0;
  padding: 16px 20px;
  width: var(--width);
  background: var(--color);
  color: white;
  border-radius: 0 8px 8px 0;
  transition: width 0.4s ease;
  position: relative;
}
.step-label { font-weight: 600; }
.step-value { font-size: 1.25rem; font-weight: 700; }
.step-pct { font-size: 0.875rem; opacity: 0.9; }
.step-drop {
  position: absolute;
  right: -120px;
  color: #D32F2F;
  font-size: 0.875rem;
  font-weight: 600;
}
[data-theme="dark"] .step-drop { color: #D32F2F; }
```

### 1.3 자동 생성 입력 (Python 측)

```python
def render_funnel(steps: list[dict]) -> str:
    """steps = [{'label': '...', 'value': int, 'color_idx': 1}, ...]"""
    total = steps[0]['value']
    html = ['<ul class="funnel-steps">']
    prev = None
    for i, s in enumerate(steps):
        pct = s['value'] / total * 100
        drop = f"▼ {(prev - s['value']) / prev * 100:.0f}% 이탈" if prev else ''
        html.append(f'''
          <li class="funnel-step" style="--width: {pct}%; --color: var(--series-{s.get('color_idx', i+1)});">
            <span class="step-label">{s['label']}</span>
            <span class="step-value">{s['value']:,}명</span>
            <span class="step-pct">{pct:.0f}%</span>
            {f'<span class="step-drop">{drop}</span>' if drop else ''}
          </li>''')
        prev = s['value']
    html.append('</ul>')
    return '\n'.join(html)
```

---

## 2. 매트릭스 (Matrix) — 2축 분류

**적합 데이터**: 4분면 분류 (예: 우선순위 매트릭스, 만족도×참여도, 비용×효과)

### 2.1 HTML 구조

```html
<div class="infographic matrix">
  <h3 class="ig-title">세션 효과성 매트릭스 (만족도 × 참여도)</h3>
  <div class="matrix-grid">
    <div class="matrix-axis-y">만족도 (높음 →)</div>
    <div class="matrix-axis-x">참여도 (높음 →)</div>

    <div class="quadrant q-tl" data-tone="warning">
      <span class="q-label">개선 필요</span>
      <span class="q-desc">만족 高·참여 低 — 콘텐츠 노출 강화</span>
      <ul class="q-items"><li>키노트 A</li><li>세션 B</li></ul>
    </div>
    <div class="quadrant q-tr" data-tone="success">
      <span class="q-label">핵심 강점</span>
      <span class="q-desc">만족 高·참여 高 — 차기 확대</span>
      <ul class="q-items"><li>세션 C</li><li>워크숍 D</li></ul>
    </div>
    <div class="quadrant q-bl" data-tone="danger">
      <span class="q-label">재검토</span>
      <span class="q-desc">만족 低·참여 低 — 폐지 또는 리뉴얼</span>
      <ul class="q-items"><li>세션 E</li></ul>
    </div>
    <div class="quadrant q-br" data-tone="info">
      <span class="q-label">품질 개선</span>
      <span class="q-desc">만족 低·참여 高 — 콘텐츠 보강</span>
      <ul class="q-items"><li>패널 F</li><li>세션 G</li></ul>
    </div>
  </div>
</div>
```

### 2.2 CSS

```css
.matrix-grid {
  display: grid;
  grid-template-columns: 40px 1fr 1fr;
  grid-template-rows: 1fr 1fr 40px;
  gap: 4px;
  aspect-ratio: 1.4;
  position: relative;
}
.matrix-axis-y {
  grid-column: 1; grid-row: 1 / 3;
  writing-mode: vertical-rl; transform: rotate(180deg);
  display: flex; align-items: center; justify-content: center;
  font-weight: 600; color: var(--text-secondary);
}
.matrix-axis-x {
  grid-column: 2 / 4; grid-row: 3;
  display: flex; align-items: center; justify-content: center;
  font-weight: 600; color: var(--text-secondary);
}
.quadrant {
  padding: 20px;
  border-radius: 8px;
  display: flex; flex-direction: column; gap: 8px;
  border: 2px solid;
}
.q-tl { grid-column: 2; grid-row: 1; }
.q-tr { grid-column: 3; grid-row: 1; }
.q-bl { grid-column: 2; grid-row: 2; }
.q-br { grid-column: 3; grid-row: 2; }
.q-label { font-weight: 700; font-size: 1.125rem; }
.q-desc { font-size: 0.875rem; opacity: 0.85; }
.q-items { list-style: '· '; padding-left: 20px; margin: 0; font-size: 0.875rem; }

[data-tone="success"] { background: #E8EFFF; border-color: #00E676; color: #00733B; }
[data-tone="info"]    { background: #E8EFFF; border-color: #2962FF; color: #1E4DCC; }
[data-tone="warning"] { background: #FFF3E0; border-color: #FFA000; color: #FF5722; }
[data-tone="danger"]  { background: #F1F3F7; border-color: #D32F2F; color: #D32F2F; }

[data-theme="dark"] [data-tone="success"] { background: #14532d40; color: #00E676; }
[data-theme="dark"] [data-tone="info"]    { background: #1e3a8a40; color: #5B9BD5; }
[data-theme="dark"] [data-tone="warning"] { background: #78350f40; color: #FFA000; }
[data-theme="dark"] [data-tone="danger"]  { background: #7f1d1d40; color: #D32F2F; }
```

---

## 3. 레이더 (Radar) — 다축 평가 (인포그래픽 강조 버전)

**v1 의 Chart.js radar 차트와 차별점**: 본 인포그래픽은 **점수 + 평가 카드 결합**. 차트 옆에 항목별 평가 코멘트 자동 배치.

### 3.1 HTML 구조

```html
<div class="infographic radar">
  <h3 class="ig-title">행사 평가 다축 분석</h3>
  <div class="radar-grid">
    <div class="radar-chart-wrap">
      <canvas id="radar-canvas"></canvas>  <!-- Chart.js radar -->
    </div>
    <div class="radar-evaluations">
      <div class="eval-item" data-tone="success">
        <span class="eval-axis">콘텐츠 품질</span>
        <span class="eval-score">4.6 / 5.0</span>
        <span class="eval-comment">예년 대비 ▲0.4 — 키노트 만족도 견인</span>
      </div>
      <div class="eval-item" data-tone="success">
        <span class="eval-axis">운영 매끄러움</span>
        <span class="eval-score">4.4 / 5.0</span>
        <span class="eval-comment">현장 동선 개선 효과</span>
      </div>
      <div class="eval-item" data-tone="warning">
        <span class="eval-axis">네트워킹 기회</span>
        <span class="eval-score">3.2 / 5.0</span>
        <span class="eval-comment">자유 시간 부족 의견 다수</span>
      </div>
      <div class="eval-item" data-tone="info">
        <span class="eval-axis">베뉴 접근성</span>
        <span class="eval-score">4.1 / 5.0</span>
        <span class="eval-comment">교통 안내 강화 권장</span>
      </div>
      <div class="eval-item" data-tone="success">
        <span class="eval-axis">F&B 품질</span>
        <span class="eval-score">4.5 / 5.0</span>
        <span class="eval-comment">신규 케이터링 호평</span>
      </div>
    </div>
  </div>
</div>
```

### 3.2 CSS

```css
.radar-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  align-items: center;
}
.radar-chart-wrap {
  position: relative;
  aspect-ratio: 1;
}
.radar-evaluations {
  display: flex; flex-direction: column; gap: 12px;
}
.eval-item {
  display: grid;
  grid-template-columns: 140px 80px 1fr;
  gap: 12px;
  align-items: center;
  padding: 12px 16px;
  border-radius: 8px;
  border-left: 4px solid;
}
.eval-axis { font-weight: 600; }
.eval-score { font-weight: 700; font-variant-numeric: tabular-nums; }
.eval-comment { font-size: 0.875rem; opacity: 0.85; }
```

(tone 색상은 §2 매트릭스의 .q-* 와 동일 — 재사용)

---

## 4. 다크 모드 호환

3종 인포그래픽 모두 `[data-theme="dark"]` 셀렉터로 다크 변형 정의됨. [dark-mode-patterns.md §2.4](dark-mode-patterns.md) 의 콜아웃 다크 변형이 매트릭스·레이더 의 tone 색상에 적용.

---

## 5. 자동 생성 헬퍼 (Python build_dashboard.py 측)

```python
INFOGRAPHIC_TRIGGERS = {
    'funnel':  ['전환', '단계', '퍼널', 'funnel', '이탈', '드롭'],
    'matrix':  ['매트릭스', '4분면', '분류', '우선순위', '평가표'],
    'radar':   ['다축', '평가', '역량', '항목별 점수', '레이더'],
}

def detect_infographics(data_summary: dict) -> list[str]:
    """데이터 컬럼·키워드에서 인포그래픽 후보 자동 감지."""
    candidates = []
    text = ' '.join(data_summary.get('columns', []) + [data_summary.get('title', '')])
    for ig_type, keywords in INFOGRAPHIC_TRIGGERS.items():
        if any(k in text.lower() for k in keywords):
            candidates.append(ig_type)
    return candidates
```

→ 자동 감지된 인포그래픽은 표준 차트 영역 다음에 배치.

---

## 6. 본 Sprint 적용 범위

- ✅ 퍼널·매트릭스·레이더 3종 HTML/CSS 패턴 정의
- ✅ 라이트/다크 모드 양쪽 호환
- ✅ Chart.js radar 와 연동 (레이더 인포그래픽)
- ✅ Python 자동 감지 헬퍼 시안
- ✅ 검증 샘플 1종 (output_infographic.html) 에서 실제 렌더링
