# Dark Mode Patterns (v2.0) — Sponsor Deck 다크 모드 패턴

mice-proposal v2.1.1 `dark-mode-patterns.md` 를 sponsor-deck 컨텍스트로 포팅한 **5종 다크 패턴 + 슬라이드별 라이트/다크 컨텍스트 매트릭스**다. 표지·섹션 구분·Thank You·ROI 임팩트 강조 슬라이드에 적용된다.

---

## 0. 다크 모드 컬러 매핑

### 0-1. 다크 색상 변수 (JC 시그니처 기준)

```javascript
// 다크 모드 컬러 변수 (mice-proposal v2.1.1 dark-mode-patterns 동일)
const DARK_BG = "0A2540";              // 메인 배경 (Deep Navy)
const DARK_BG_ALT = "1A3556";          // 카드·시트 배경 (Primary Soft)
const DARK_BG_PLACEHOLDER = "1F4068";  // 이미지 placeholder
const DARK_SURFACE = "12304D";         // 보조 서피스

const DARK_TEXT = "FFFFFF";            // 본문 흰색
const DARK_TEXT_MUTED = "B8C5D6";      // 보조 글자
const DARK_TEXT_DISABLED = "6B7B92";   // 비활성

const DARK_BORDER = "2A4A6E";          // 테두리
const DARK_BORDER_STRONG = "3D5F87";   // 강조 테두리

const DARK_ACCENT = "2962FF";          // Electric Blue (라이트와 동일)
const DARK_ACCENT_SOFT = "1E4DCC";     // 호버 상태

// 차트 데이터 시리즈는 라이트와 동일 (가독성 검증 완료)
const DARK_CHART_SERIES = ["2962FF", "E91E63", "FF5722", "00E676", "B8C5D6"];

// Tier 색상은 라이트와 동일 (브랜드 일관성)
const DARK_TIER_COLORS = {
  T1: "E91E63",  // Magenta — 다크에서 더 강한 임팩트
  T2: "2962FF",  // Electric Blue
  T3: "FF5722",  // Vivid Orange
  T4: "B8C5D6",  // Muted (라이트의 5A6270 → 다크에서는 B8C5D6 으로 가독성 확보)
  T5: "6B7B92",  // 다크 환경의 Border Strong 대응
  T6: "00E676"   // Neon Green
};
```

```css
/* HTML CSS 변수 (다크 모드) */
[data-theme="dark"] {
  --jc-bg: #0A2540;
  --jc-surface: #1A3556;
  --jc-surface-alt: #12304D;
  --jc-text: #FFFFFF;
  --jc-text-muted: #B8C5D6;
  --jc-text-disabled: #6B7B92;
  --jc-border: #2A4A6E;
  --jc-border-strong: #3D5F87;
  --jc-accent: #2962FF;
  --jc-accent-soft: #1E4DCC;
  /* Tier 색상은 동일 유지 */
}
```

### 0-2. 라이트 → 다크 매핑 표

| 라이트 요소 | 라이트 컬러 | 다크 컬러 |
|------------|------------|----------|
| 페이지 배경 | `#F8F9FB` | `#0A2540` |
| 카드 배경 | `#FFFFFF` | `#1A3556` |
| 보조 서피스 | `#F1F3F7` | `#12304D` |
| 짝수 행 배경 | `#F8F9FB` | `#12304D` |
| 본문 글자 | `#1A1D24` | `#FFFFFF` |
| 보조 글자 | `#5A6270` | `#B8C5D6` |
| 테두리 | `#E5E8ED` | `#2A4A6E` |
| 강조 테두리 | `#C9CFD8` | `#3D5F87` |
| 이미지 placeholder | `#E5E8ED` | `#1F4068` |

### 0-3. 적용 컨텍스트 — 슬라이드별 라이트/다크 권장 매트릭스 (sponsor-deck 핵심)

| 슬라이드 | 라이트 권장 | 다크 권장 | 비고 |
|----------|-------------|-----------|------|
| **S1 표지** | ⚠️ | **✅** | HERO 이미지 + 다크 오버레이 (영업용 임팩트). DARK-COVER 적용 |
| **S2 Why This Event** | ✅ | ⚠️ | 다크 변형 가능 (섹션 구분 강조). 1장만 다크 권장 |
| **S3 Who Attends** | **✅** | ❌ | 차트·KPI 가독성 절대 우선. 라이트 유지 |
| **S4 What We Offer** | **✅** | ❌ | 리스트·인벤토리 가독성 우선. 라이트 유지 |
| **S5 Sponsor Tiers** | ✅ | ⚠️ | T1 강조 단일 슬라이드는 다크 가능 (DARK-TIER) |
| **S6 Benefits Matrix** | **✅** | ❌ | 매트릭스 가독성 절대 우선. 라이트 강제 |
| **S7 ROI Snapshot** | ⚠️ | **✅** | KPI 임팩트 (DARK-KPI·DARK-ROI). 영업용 결정타 |
| **S8 Past Sponsors** | **✅** | ❌ | 로고 그리드 — 라이트 유지 |
| **S9 Contact** | ⚠️ | **✅** | Thank You 톤 (DARK-COVER). 영업 마무리 |

### 0-4. 핵심 원칙

1. **다크 슬라이드 ≤ 30%**: 전체 슬라이드 15장이면 다크 슬라이드 최대 4~5장
2. **데이터·표 슬라이드는 라이트 강제**: S3·S4·S6 다크 금지
3. **표지·임팩트·종결 슬라이드는 다크 권장**: S1·S7·S9
4. **WCAG AA 대비비 (4.5:1) 검증 의무**: 흰색 텍스트 + Deep Navy 배경 = 13.1:1 (충분)
5. **인쇄 시 라이트 강제 토글 지원**: `@media print` + 다크 토글 스크립트

---

## 1. DARK-TIER 패턴 (다크 배경 Tier 카드, SVP-1 대응)

### 1-1. 사양

| 항목 | 값 |
|------|-----|
| 용도 | T1 강조 단일 슬라이드 (S5 보조) — Title Sponsor의 격을 다크로 시각화 |
| 형태 | 다크 카드 N개. 좌측 액센트 막대 = Tier 색상 (밝게 유지) |
| 컬러 위계 | 카드 배경 = DARK_BG_ALT, 텍스트 = DARK_TEXT, 좌측 막대 = TIER_COLORS |

### 1-2. HTML 코드

```html
<section class="slide slide-dark" data-theme="dark">
  <div class="tier-grid">
    <article class="tier-card dark" data-tier="T1" style="--tier-color: #E91E63;">
      <div class="tier-accent"></div>
      <div class="tier-body">
        <header class="tier-header">
          <span class="tier-id">T1</span>
          <h3 class="tier-name">타이틀 (Title)</h3>
        </header>
        <div class="tier-meta">
          <p class="tier-slots">한정 1석</p>
          <p class="tier-price">가격 별도 협의</p>
        </div>
        <ul class="tier-benefits">
          <li>행사명 결합권</li>
          <li>키노트 발표 30분</li>
          <li>VIP 만찬 단독 호스트</li>
        </ul>
      </div>
    </article>
  </div>
</section>

<style>
.slide-dark {
  background: #0A2540;
  color: #FFFFFF;
}
.tier-card.dark {
  background: #1A3556;
  border: 0.5px solid #2A4A6E;
}
.tier-card.dark .tier-name {
  color: #FFFFFF;
}
.tier-card.dark .tier-slots {
  color: #B8C5D6;
}
.tier-card.dark .tier-price {
  color: #FFFFFF;
}
.tier-card.dark .tier-benefits {
  color: #FFFFFF;
}
.tier-card.dark .tier-meta {
  border-bottom-color: #2A4A6E;
}
</style>
```

### 1-3. PPTX 코드

```javascript
function addDarkTierCard(slide, opts) {
  const { x, y, w, h, tierId, tierName, slots, price, benefits } = opts;
  const tierColor = DARK_TIER_COLORS[tierId];

  // 다크 슬라이드 배경
  slide.background = { color: DARK_BG };

  // 다크 카드 배경
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: DARK_BG_ALT },
    line: { color: DARK_BORDER, width: 0.5 },
    rectRadius: 0.08
  });

  // 좌측 액센트 막대 (Tier 색상, 다크에서도 동일)
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.1, h,
    fill: { color: tierColor },
    line: { type: "none" }
  });

  // Tier ID (Tier 색상)
  slide.addText(tierId, {
    x: x + 0.25, y: y + 0.2, w: w - 0.35, h: 0.25,
    fontSize: 11, bold: true,
    fontFace: FONT_MONO,
    color: tierColor,
    align: "left", valign: "middle", margin: 0
  });

  // Tier 이름 (흰색)
  slide.addText(tierName, {
    x: x + 0.25, y: y + 0.45, w: w - 0.35, h: 0.4,
    fontSize: 20, bold: true,
    fontFace: FONT_HEADING,
    color: DARK_TEXT,
    align: "left", valign: "middle", margin: 0
  });

  // 슬롯 + 가격
  slide.addText([
    { text: slots, options: { fontSize: 11, fontFace: FONT_KO, color: DARK_TEXT_MUTED, breakLine: true } },
    { text: price, options: { fontSize: 13, bold: true, fontFace: FONT_KO, color: DARK_TEXT } }
  ], {
    x: x + 0.25, y: y + 0.95, w: w - 0.35, h: 0.65,
    align: "left", valign: "top", margin: 0
  });

  // 구분선
  slide.addShape(pres.shapes.LINE, {
    x: x + 0.25, y: y + 1.65, w: w - 0.5, h: 0,
    line: { color: DARK_BORDER, width: 0.5 }
  });

  // 핵심 혜택 bullet (흰색)
  const benefitItems = benefits.map(b => ({
    text: b,
    options: { bullet: true, fontSize: 11, fontFace: FONT_KO, color: DARK_TEXT, paraSpaceAfter: 4 }
  }));
  slide.addText(benefitItems, {
    x: x + 0.25, y: y + 1.8, w: w - 0.35, h: h - 1.95,
    align: "left", valign: "top", margin: 0
  });
}
```

---

## 2. DARK-MATRIX 패턴 (다크 Benefits 매트릭스, SVP-2 대응)

### 2-1. 사양

| 항목 | 값 |
|------|-----|
| 용도 | S6 다크 변형 (선택 — 일반적으로 라이트 권장이지만 다크 데크 전체 톤 유지 시 사용) |
| 형태 | 다크 표. 헤더 = DARK_ACCENT, 본문 zebra = DARK_BG_ALT/DARK_SURFACE |
| 주의 | **다크 매트릭스는 가독성 위험 큼. 5개 Tier × 3카테고리 이하 최소화 권장** |

### 2-2. HTML 코드

```html
<section class="slide slide-dark" data-theme="dark">
  <table class="benefits-matrix dark">
    <thead>
      <tr>
        <th class="cat-col">카테고리</th>
        <th class="tier-col">T1 타이틀</th>
        <th class="tier-col">T2 플래티넘</th>
        <th class="tier-col">T3 골드</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th class="cat-row">메인 사이니지</th>
        <td class="quant">8회</td>
        <td class="quant">6회</td>
        <td class="quant">4회</td>
      </tr>
      <tr>
        <th class="cat-row">키노트·세션</th>
        <td class="quant">키노트 30분</td>
        <td class="quant">메인 45분</td>
        <td class="quant">트랙 30분</td>
      </tr>
      <tr>
        <th class="cat-row">VIP 만찬</th>
        <td class="quant">단독 10석</td>
        <td class="quant">6석</td>
        <td class="dash">—</td>
      </tr>
    </tbody>
  </table>
</section>

<style>
.benefits-matrix.dark {
  background: #0A2540;
  color: #FFFFFF;
  border: 1px solid #2A4A6E;
}
.benefits-matrix.dark thead th {
  background: #2962FF;
  color: #FFFFFF;
  border-bottom: 2px solid #1E4DCC;
}
.benefits-matrix.dark tbody th.cat-row {
  background: #12304D;
  color: #B8C5D6;
}
.benefits-matrix.dark tbody td {
  border-bottom: 1px solid #2A4A6E;
  color: #FFFFFF;
}
.benefits-matrix.dark tbody tr:nth-child(even) td,
.benefits-matrix.dark tbody tr:nth-child(even) th.cat-row {
  background: #1A3556;
}
.benefits-matrix.dark .dash {
  color: #6B7B92;
}
</style>
```

### 2-3. PPTX 코드

```javascript
function makeDarkMatrixHeader(tierLabels) {
  return [
    {
      text: "카테고리",
      options: {
        fill: { color: DARK_ACCENT }, color: "FFFFFF", bold: true,
        fontSize: 11, fontFace: FONT_KO,
        align: "left", valign: "middle",
        margin: [0.05, 0.08, 0.05, 0.08]
      }
    },
    ...tierLabels.map(label => ({
      text: label,
      options: {
        fill: { color: DARK_ACCENT }, color: "FFFFFF", bold: true,
        fontSize: 11, fontFace: FONT_KO,
        align: "center", valign: "middle",
        margin: [0.05, 0.08, 0.05, 0.08]
      }
    }))
  ];
}

function makeDarkMatrixBodyRow(catName, cellValues, rowIndex) {
  const bgColor = rowIndex % 2 === 0 ? DARK_BG_ALT : DARK_SURFACE;
  const cells = [
    {
      text: catName,
      options: {
        fill: { color: DARK_SURFACE },
        color: DARK_TEXT_MUTED, bold: false,
        fontSize: 10, fontFace: FONT_KO,
        align: "left", valign: "middle",
        margin: [0.05, 0.08, 0.05, 0.08]
      }
    }
  ];
  cellValues.forEach(val => {
    let cellColor, cellBold;
    if (val === "✓") {
      cellColor = "00E676";  // Neon Green (다크에서 더 잘 보임)
      cellBold = true;
    } else if (val === "—") {
      cellColor = DARK_TEXT_DISABLED;
      cellBold = false;
    } else {
      cellColor = DARK_TEXT;
      cellBold = false;
    }
    cells.push({
      text: String(val),
      options: {
        fill: { color: bgColor },
        color: cellColor, bold: cellBold,
        fontSize: 10, fontFace: FONT_KO,
        align: "center", valign: "middle",
        margin: [0.05, 0.08, 0.05, 0.08]
      }
    });
  });
  return cells;
}

// 사용 예시
slide.background = { color: DARK_BG };

const tierLabels = ["T1 타이틀", "T2 플래티넘", "T3 골드"];
const matrixRows = [
  makeDarkMatrixHeader(tierLabels),
  makeDarkMatrixBodyRow("메인 사이니지", ["8회", "6회", "4회"], 0),
  makeDarkMatrixBodyRow("키노트·세션", ["키노트 30분", "메인 45분", "트랙 30분"], 1),
  makeDarkMatrixBodyRow("VIP 만찬 좌석", ["단독 10석", "6석", "—"], 2)
];

slide.addTable(matrixRows, {
  x: 0.5, y: 1.5, w: 12.33,
  colW: [3.0, 3.11, 3.11, 3.11],
  border: { pt: 0.5, color: DARK_BORDER }
});
```

---

## 3. DARK-ROI 패턴 (다크 ROI 3단 카드, SVP-3 대응)

### 3-1. 사양

| 항목 | 값 |
|------|-----|
| 용도 | S7 ROI Snapshot 다크 임팩트 버전 — 영업 결정타 |
| 형태 | 다크 3단 카드. ③ 추정값 단을 DARK_ACCENT 배경으로 임팩트 강화 |
| 컬러 위계 | 헤더 = DARK_ACCENT, 본문 = DARK_BG_ALT, ③ 추정값 = DARK_ACCENT 배경 + 흰 글자 |

### 3-2. HTML 코드

```html
<section class="slide slide-dark" data-theme="dark">
  <div class="roi-grid">
    <article class="roi-card dark">
      <header class="roi-header">
        <span class="roi-industry-badge">Tech 산업 스폰서 ROI</span>
      </header>
      <section class="roi-stage stage-premise dark">
        <h4>① 전제 조건</h4>
        <ul>
          <li>IT 참가자 약 2,184명</li>
          <li>IT 의사결정권자 약 655명</li>
        </ul>
      </section>
      <section class="roi-stage stage-formula dark">
        <h4>② 산출 공식</h4>
        <ul>
          <li>부스 전환율 12% × 의사결정권자</li>
          <li>리드 전환율 35% 적용</li>
        </ul>
      </section>
      <section class="roi-stage stage-estimate dark">
        <h4>③ 보수적 추정값</h4>
        <p class="roi-estimate-headline">리드 약 <strong>25~30건</strong></p>
        <p class="roi-estimate-secondary">PR 가치 약 KRW 25M</p>
      </section>
      <footer class="roi-caption dark">
        ⓘ 본 수치는 산업 벤치마크 기반 추정치입니다.
      </footer>
    </article>
  </div>
</section>

<style>
.roi-card.dark {
  background: #1A3556;
  border: 0.5px solid #2A4A6E;
}
.roi-card.dark .roi-header {
  background: #2962FF;
}
.roi-card.dark .roi-stage {
  border-bottom: 1px solid #2A4A6E;
}
.roi-card.dark .roi-stage h4 {
  color: #00E676;  /* Neon Green — 다크에서 강한 식별 */
}
.roi-card.dark .roi-stage ul,
.roi-card.dark .roi-stage p {
  color: #FFFFFF;
}
.roi-card.dark .stage-estimate {
  background: #2962FF;  /* Electric Blue 풀 배경 — 임팩트 강화 */
  border-bottom: none;
}
.roi-card.dark .stage-estimate h4 {
  color: #FFFFFF;
}
.roi-card.dark .roi-estimate-headline strong {
  color: #FFFFFF;
  font-size: 26px;
}
.roi-card.dark .roi-estimate-secondary {
  color: #E8EFFF;
}
.roi-card.dark .roi-caption.dark {
  background: #12304D;
  color: #B8C5D6;
}
</style>
```

### 3-3. PPTX 코드

```javascript
function addDarkRoiCard(slide, opts) {
  const { x, y, w, h, industry, premise, formula, estimate, caption } = opts;

  slide.background = { color: DARK_BG };

  // 다크 카드 배경
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: DARK_BG_ALT },
    line: { color: DARK_BORDER, width: 0.5 },
    rectRadius: 0.08
  });

  // 상단 헤더 (Electric Blue)
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h: 0.55,
    fill: { color: DARK_ACCENT },
    line: { type: "none" }
  });
  slide.addText(industry, {
    x: x + 0.2, y: y + 0.05, w: w - 0.4, h: 0.45,
    fontSize: 13, bold: true,
    fontFace: FONT_HEADING,
    color: "FFFFFF",
    align: "left", valign: "middle", margin: 0
  });

  // 1단: 전제 조건 — Neon Green 헤더
  let stageY = y + 0.65;
  slide.addText("① 전제 조건", {
    x: x + 0.2, y: stageY, w: w - 0.4, h: 0.25,
    fontSize: 11, bold: true,
    fontFace: FONT_KO,
    color: "00E676",
    align: "left", valign: "middle", margin: 0
  });
  const premiseItems = premise.map(p => ({
    text: p,
    options: { bullet: true, fontSize: 10, fontFace: FONT_KO, color: DARK_TEXT, paraSpaceAfter: 2 }
  }));
  slide.addText(premiseItems, {
    x: x + 0.2, y: stageY + 0.25, w: w - 0.4, h: 0.6,
    align: "left", valign: "top", margin: 0
  });

  // 2단: 산출 공식
  stageY = y + 1.55;
  slide.addText("② 산출 공식", {
    x: x + 0.2, y: stageY, w: w - 0.4, h: 0.25,
    fontSize: 11, bold: true,
    fontFace: FONT_KO,
    color: "00E676",
    align: "left", valign: "middle", margin: 0
  });
  const formulaItems = formula.map(f => ({
    text: f,
    options: { bullet: true, fontSize: 10, fontFace: FONT_KO, color: DARK_TEXT, paraSpaceAfter: 2 }
  }));
  slide.addText(formulaItems, {
    x: x + 0.2, y: stageY + 0.25, w: w - 0.4, h: 0.6,
    align: "left", valign: "top", margin: 0
  });

  // 3단: 추정값 (Electric Blue 풀 배경 — 임팩트)
  stageY = y + 2.45;
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y: stageY, w, h: 1.0,
    fill: { color: DARK_ACCENT },
    line: { type: "none" }
  });
  slide.addText("③ 보수적 추정값", {
    x: x + 0.2, y: stageY + 0.05, w: w - 0.4, h: 0.25,
    fontSize: 11, bold: true,
    fontFace: FONT_KO,
    color: "FFFFFF",
    align: "left", valign: "middle", margin: 0
  });
  slide.addText(estimate.headline, {
    x: x + 0.2, y: stageY + 0.3, w: w - 0.4, h: 0.4,
    fontSize: 16, bold: true,
    fontFace: FONT_HEADING,
    color: "FFFFFF",
    align: "left", valign: "middle", margin: 0
  });
  if (estimate.secondary) {
    slide.addText(estimate.secondary, {
      x: x + 0.2, y: stageY + 0.7, w: w - 0.4, h: 0.25,
      fontSize: 10,
      fontFace: FONT_KO,
      color: "E8EFFF",
      align: "left", valign: "middle", margin: 0
    });
  }

  // 캡션
  stageY = y + h - 0.5;
  slide.addText(caption || "ⓘ 본 수치는 산업 벤치마크 기반 추정치입니다.", {
    x: x + 0.2, y: stageY, w: w - 0.4, h: 0.45,
    fontSize: 9,
    fontFace: FONT_KO,
    color: DARK_TEXT_MUTED,
    italic: true,
    align: "left", valign: "top", margin: 0
  });
}
```

---

## 4. DARK-KPI 패턴 (다크 KPI 콜아웃, SVP-4 대응)

### 4-1. 사양

| 항목 | 값 |
|------|-----|
| 용도 | S7 ROI Snapshot 추가 강조 또는 임팩트 슬라이드 |
| 형태 | 큰 숫자 (72pt) + 단위 + 라벨. Electric Blue 또는 Neon Green 강조 |
| 컬러 위계 | 숫자 = DARK_ACCENT (Electric Blue) 또는 Neon Green (선택), 라벨 = DARK_TEXT_MUTED |

### 4-2. HTML 코드

```html
<section class="slide slide-dark" data-theme="dark">
  <div class="kpi-callout-grid dark">
    <div class="kpi-callout dark">
      <div class="kpi-number neon">1,196</div>
      <div class="kpi-unit">명</div>
      <div class="kpi-label">의사결정권자 직접 노출</div>
      <div class="kpi-source">C-Level + 임원 23% × 5,200명</div>
    </div>
    <div class="kpi-callout dark">
      <div class="kpi-number">87</div>
      <div class="kpi-unit">%</div>
      <div class="kpi-label">B2B 비율</div>
    </div>
    <div class="kpi-callout dark">
      <div class="kpi-number">25</div>
      <div class="kpi-unit">M</div>
      <div class="kpi-label">PR 가치 (KRW)</div>
    </div>
  </div>
</section>

<style>
.kpi-callout.dark {
  background: #1A3556;
  border: 0.5px solid #2A4A6E;
  border-left: 6px solid #2962FF;
}
.kpi-callout.dark .kpi-number {
  color: #2962FF;
  font-size: 72px;
}
.kpi-callout.dark .kpi-number.neon {
  color: #00E676;  /* 강조용 — 1순위 KPI에만 사용 */
}
.kpi-callout.dark .kpi-unit {
  color: #2962FF;
}
.kpi-callout.dark .kpi-number.neon + .kpi-unit {
  color: #00E676;
}
.kpi-callout.dark .kpi-label {
  color: #FFFFFF;
}
.kpi-callout.dark .kpi-source {
  color: #B8C5D6;
}
</style>
```

### 4-3. PPTX 코드 (mice-proposal DARK-C3 포팅)

```javascript
function addDarkKpiCallout(slide, opts) {
  const { x, y, w, h, value, unit, label, source, neon = false } = opts;

  slide.background = { color: DARK_BG };

  // 다크 카드 배경
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: DARK_BG_ALT },
    line: { color: DARK_BORDER, width: 0.5 },
    rectRadius: 0.08
  });

  // 좌측 6px Accent 보더
  const borderColor = neon ? "00E676" : DARK_ACCENT;
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.08, h,
    fill: { color: borderColor },
    line: { type: "none" }
  });

  // 숫자 자동 천단위 콤마
  const valueStr = typeof value === "number"
    ? value.toLocaleString("ko-KR")
    : String(value);

  // 큰 숫자 — 72pt, Electric Blue 또는 Neon Green
  slide.addText(valueStr, {
    x: x + 0.1, y: y + 0.3, w: w - 0.2, h: h * 0.48,
    fontSize: 60, bold: true,
    fontFace: FONT_MONO,
    color: neon ? "00E676" : DARK_ACCENT,
    align: "center", valign: "middle", margin: 0
  });

  // 단위
  if (unit) {
    slide.addText(unit, {
      x: x + 0.1, y: y + 0.3 + h * 0.48, w: w - 0.2, h: 0.3,
      fontSize: 20, bold: true,
      fontFace: FONT_KO,
      color: neon ? "00E676" : DARK_ACCENT,
      align: "center", valign: "top", margin: 0
    });
  }

  // 라벨 (흰색)
  slide.addText(label, {
    x: x + 0.1, y: y + h * 0.72, w: w - 0.2, h: 0.3,
    fontSize: 13, bold: false,
    fontFace: FONT_KO,
    color: DARK_TEXT,
    align: "center", valign: "middle", margin: 0
  });

  // 출처 캡션
  if (source) {
    slide.addText(source, {
      x: x + 0.1, y: y + h * 0.85, w: w - 0.2, h: 0.3,
      fontSize: 9,
      fontFace: FONT_KO,
      color: DARK_TEXT_MUTED,
      align: "center", valign: "top", margin: 0
    });
  }
}

// 사용 예시: 3개 KPI 다크 임팩트 슬라이드 (S7 ROI 추가 강조)
slide.background = { color: DARK_BG };

const darkKpis = [
  { value: 1196, unit: "명", label: "의사결정권자 직접 노출",
    source: "C-Level + 임원 23% × 5,200명", neon: true },
  { value: 87, unit: "%", label: "B2B 비율", neon: false },
  { value: 25, unit: "M", label: "PR 가치 (KRW)", neon: false }
];

const cardW = 3.8;
const cardH = 3.0;
const gap = 0.5;
const startX = (13.33 - (cardW * 3 + gap * 2)) / 2;
darkKpis.forEach((kpi, idx) => {
  addDarkKpiCallout(slide, {
    x: startX + idx * (cardW + gap),
    y: 2.5,
    w: cardW, h: cardH,
    value: kpi.value,
    unit: kpi.unit,
    label: kpi.label,
    source: kpi.source,
    neon: kpi.neon
  });
});
```

---

## 5. DARK-COVER 패턴 (다크 표지 + "For Sponsors" 배지)

### 5-1. 사양

| 항목 | 값 |
|------|-----|
| 용도 | S1 표지 또는 S9 Contact (Thank You 톤) |
| 형태 | 풀 다크 배경 + 행사명 메인 타이틀 + "For Sponsors" 배지 + 일시·장소 |
| 컬러 위계 | 배경 = DARK_BG, 메인 = 흰색, 배지 = DARK_ACCENT, 액센트 라인 = DARK_ACCENT |

### 5-2. HTML 코드

```html
<section class="slide slide-cover-dark" data-theme="dark">
  <div class="cover-content">
    <div class="cover-badge">For Sponsors</div>
    <h1 class="cover-title">TOBESOFT TECH FORUM 2026</h1>
    <p class="cover-subtitle">AI·Cloud·Enterprise Tech의 다음 10년</p>
    <div class="cover-accent-line"></div>
    <div class="cover-meta">
      <span class="cover-date">2026.09.15 (Tue)</span>
      <span class="cover-divider">·</span>
      <span class="cover-venue">코엑스 컨벤션홀</span>
    </div>
  </div>
  <footer class="cover-footer">
    <span class="cover-version">v1.0 · 2026.05</span>
  </footer>
</section>

<style>
.slide-cover-dark {
  background: #0A2540;
  color: #FFFFFF;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding: 64px;
  position: relative;
}
.cover-content {
  max-width: 80%;
}
.cover-badge {
  display: inline-block;
  padding: 6px 14px;
  background: #2962FF;
  color: #FFFFFF;
  font-family: var(--jc-font-mono, 'JetBrains Mono');
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  border-radius: 4px;
  margin-bottom: 24px;
  text-transform: uppercase;
}
.cover-title {
  font-family: var(--jc-font-heading, Pretendard);
  font-size: 56px;
  font-weight: 700;
  color: #FFFFFF;
  margin: 0 0 12px;
  line-height: 1.1;
  letter-spacing: -0.02em;
}
.cover-subtitle {
  font-size: 22px;
  color: #B8C5D6;
  margin: 0 0 24px;
  font-weight: 400;
}
.cover-accent-line {
  width: 120px;
  height: 4px;
  background: #2962FF;
  margin: 24px 0;
}
.cover-meta {
  font-size: 16px;
  color: #FFFFFF;
}
.cover-date,
.cover-venue {
  font-weight: 500;
}
.cover-divider {
  margin: 0 12px;
  color: #B8C5D6;
}
.cover-footer {
  position: absolute;
  bottom: 24px;
  right: 64px;
}
.cover-version {
  font-family: var(--jc-font-mono, 'JetBrains Mono');
  font-size: 11px;
  color: #B8C5D6;
}
</style>
```

### 5-3. PPTX 코드 (다크 표지)

```javascript
function addDarkCoverSlide(pres, opts) {
  const { eventName, eventSubtitle, eventDate, eventVenue, version } = opts;
  const slide = pres.addSlide();
  slide.background = { color: DARK_BG };

  // "For Sponsors" 배지
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.7, y: 1.5, w: 1.6, h: 0.35,
    fill: { color: DARK_ACCENT },
    line: { type: "none" },
    rectRadius: 0.06
  });
  slide.addText("FOR SPONSORS", {
    x: 0.7, y: 1.5, w: 1.6, h: 0.35,
    fontSize: 11, bold: true,
    fontFace: FONT_MONO,
    color: "FFFFFF",
    align: "center", valign: "middle", margin: 0,
    charSpacing: 80
  });

  // 메인 행사명
  slide.addText(eventName, {
    x: 0.7, y: 2.1, w: 12.0, h: 1.5,
    fontSize: 48, bold: true,
    fontFace: FONT_HEADING,
    color: "FFFFFF",
    align: "left", valign: "middle", margin: 0
  });

  // 부제
  if (eventSubtitle) {
    slide.addText(eventSubtitle, {
      x: 0.7, y: 3.5, w: 12.0, h: 0.5,
      fontSize: 18,
      fontFace: FONT_KO,
      color: DARK_TEXT_MUTED,
      align: "left", valign: "middle", margin: 0
    });
  }

  // 액센트 라인
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.7, y: 4.3, w: 1.5, h: 0.05,
    fill: { color: DARK_ACCENT },
    line: { type: "none" }
  });

  // 일시·장소
  slide.addText(`${eventDate}  ·  ${eventVenue}`, {
    x: 0.7, y: 4.6, w: 12.0, h: 0.45,
    fontSize: 16,
    fontFace: FONT_KO,
    color: "FFFFFF",
    align: "left", valign: "middle", margin: 0
  });

  // 버전 (우하단)
  slide.addText(version || "v1.0", {
    x: 11.5, y: 7.0, w: 1.5, h: 0.3,
    fontSize: 10,
    fontFace: FONT_MONO,
    color: DARK_TEXT_MUTED,
    align: "right", valign: "middle", margin: 0
  });

  return slide;
}

// 사용 예시
addDarkCoverSlide(pres, {
  eventName: "TOBESOFT TECH FORUM 2026",
  eventSubtitle: "AI·Cloud·Enterprise Tech의 다음 10년",
  eventDate: "2026.09.15 (Tue)",
  eventVenue: "코엑스 컨벤션홀",
  version: "v1.0 · 2026.05"
});
```

---

## 6. HTML 다크 토글 스크립트

자족형 HTML 템플릿(assets/sponsor-deck-template-dark.html)에 포함되는 다크 토글 스크립트.

```html
<button class="theme-toggle" id="themeToggle" aria-label="다크 모드 토글">
  <span class="toggle-icon-light">☀</span>
  <span class="toggle-icon-dark">☾</span>
</button>

<script>
(function() {
  const toggle = document.getElementById('themeToggle');
  const root = document.documentElement;

  // 1. 사용자 선호 우선 (localStorage > prefers-color-scheme)
  function getInitialTheme() {
    const saved = localStorage.getItem('sponsor-deck-theme');
    if (saved === 'dark' || saved === 'light') return saved;
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  }

  // 2. 적용
  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    localStorage.setItem('sponsor-deck-theme', theme);
    if (toggle) {
      toggle.setAttribute('data-theme', theme);
    }
  }

  // 3. 초기 적용
  applyTheme(getInitialTheme());

  // 4. 토글 핸들러
  if (toggle) {
    toggle.addEventListener('click', () => {
      const current = root.getAttribute('data-theme') || 'light';
      applyTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  // 5. 인쇄 시 라이트 강제 (영구 변경 없음)
  window.addEventListener('beforeprint', () => {
    root.setAttribute('data-print-theme', 'light');
  });
  window.addEventListener('afterprint', () => {
    root.removeAttribute('data-print-theme');
  });
})();
</script>

<style>
.theme-toggle {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 100;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--jc-border);
  background: var(--jc-surface);
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 200ms ease;
}
.theme-toggle:hover {
  transform: scale(1.06);
  box-shadow: 0 2px 8px rgba(10, 37, 64, 0.16);
}
[data-theme="light"] .toggle-icon-dark,
[data-theme="dark"] .toggle-icon-light {
  display: none;
}
@media print {
  .theme-toggle { display: none !important; }
  [data-print-theme="light"] {
    background: #FFFFFF !important;
    color: #1A1D24 !important;
  }
}
</style>
```

---

## 7. PPTX 다크 슬라이드 변환 룰

### 7-1. 기본 룰

1. 슬라이드 생성 직후 `slide.background = { color: DARK_BG };` 즉시 적용
2. 모든 텍스트의 `color` 를 다크 토큰으로 강제: `DARK_TEXT`, `DARK_TEXT_MUTED`
3. 차트의 `chartArea.fill`, `plotArea.fill` 모두 `DARK_BG` 또는 `DARK_BG_ALT`
4. 차트 라벨·범례 색상도 다크 토큰
5. 그리드선은 `DARK_BORDER` (미세하게 보이도록)
6. 이미지 placeholder 배경 `DARK_BG_PLACEHOLDER`

### 7-2. 다크 슬라이드 헬퍼 함수

```javascript
function applyDarkTheme(slide) {
  slide.background = { color: DARK_BG };
}

function darkTextOpts(extra = {}) {
  return {
    color: DARK_TEXT,
    fontFace: FONT_KO,
    align: "left",
    valign: "middle",
    margin: 0,
    ...extra
  };
}

function darkMutedTextOpts(extra = {}) {
  return {
    color: DARK_TEXT_MUTED,
    fontFace: FONT_KO,
    align: "left",
    valign: "middle",
    margin: 0,
    ...extra
  };
}
```

### 7-3. 다크 차트 변환 패턴

```javascript
// 라이트 → 다크 변환 룰 (예: SVP-5 산업 분포 바 차트)
slide.addChart(pres.charts.BAR, [{
  name: "산업 분포",
  labels: [...],
  values: [...]
}], {
  x: 0.5, y: 1.5, w: 9.0, h: 5.0,
  barDir: "bar",
  chartColors: DARK_CHART_SERIES,         // 다크용 시리즈 (라이트와 거의 동일)
  chartArea: { fill: { color: DARK_BG } }, // 차트 배경 다크
  plotArea: { fill: { color: DARK_BG } },
  catAxisLabelColor: DARK_TEXT,            // 카테고리 라벨 흰색
  catAxisLabelFontSize: 11,
  catAxisLabelFontFace: FONT_KO,
  valAxisLabelColor: DARK_TEXT_MUTED,      // 값축 라벨 muted
  valAxisLabelFontSize: 9,
  valGridLine: { color: DARK_BORDER, size: 0.5 },  // 그리드 어둡게
  catGridLine: { style: "none" },
  showValue: true,
  dataLabelPosition: "outEnd",
  dataLabelColor: DARK_TEXT,               // 값 라벨 흰색
  dataLabelFontSize: 11,
  dataLabelFontBold: true,
  showLegend: false
});
```

---

## 8. 다크 모드 체크리스트

### 8-1. 색상 검증
- [ ] 슬라이드 배경 `slide.background = { color: DARK_BG }` 적용
- [ ] 모든 글자 색이 흰색·`DARK_TEXT_MUTED`·`DARK_TEXT_DISABLED` 중 하나 (회색은 가독성 저하 금지)
- [ ] 차트의 `chartArea.fill`, `plotArea.fill` 모두 다크 토큰
- [ ] 차트 라벨·범례·그리드선이 다크 토큰
- [ ] 이미지 placeholder `DARK_BG_PLACEHOLDER`
- [ ] 카드 좌측 보더가 Accent 또는 Neon (식별성)

### 8-2. WCAG AA 대비비 검증
- [ ] 흰색 (`#FFFFFF`) on Deep Navy (`#0A2540`) = **13.1:1** ✓ (목표 4.5:1 충분 초과)
- [ ] B8C5D6 on `#0A2540` = 7.5:1 ✓
- [ ] DARK_ACCENT (`#2962FF`) on `#FFFFFF` = 5.8:1 ✓
- [ ] 다크 그라데이션 사용 금지 (인쇄 호환성)

### 8-3. 분량 검증
- [ ] **다크 모드 슬라이드가 전체 분량의 30% 이내** (가독성 보호)
- [ ] 데이터 슬라이드 (S3·S4·S6) 다크 사용 안 함
- [ ] 임팩트 슬라이드 (S1·S7·S9) 다크 사용
- [ ] 연속 3장 이상 다크 슬라이드 금지 (변화감)

### 8-4. HTML 토글 검증
- [ ] localStorage 영속화 키 `sponsor-deck-theme`
- [ ] `prefers-color-scheme: dark` 미디어 쿼리 감지
- [ ] `@media print` 라이트 강제
- [ ] 토글 버튼이 슬라이드 위에 부유 (z-index: 100)

### 8-5. PPTX 변환 검증
- [ ] 다크 슬라이드의 모든 텍스트 호출에 `color: DARK_TEXT` 또는 `DARK_TEXT_MUTED` 명시
- [ ] 차트 옵션에 `chartArea.fill` / `plotArea.fill` 모두 다크 적용
- [ ] 라이트 슬라이드와 다크 슬라이드가 같은 deck 내 혼재 시 슬라이드별 `background` 명시

---

## 9. 함께 보는 문서

| 파일 | 내용 |
|------|------|
| `visual-patterns.md` | 라이트 7종 패턴 SVP-1~SVP-7 (다크 대응 매핑) |
| `design-tokens-mapping.md` | jc-design-system 토큰 베이스 |
| `slide-structure.md` | 슬라이드별 콘텐츠 구조 |
| `output-build-guide.md` | HTML 1차 + PPTX 2차 빌드 워크플로우 |

---

## 10. JSON 스키마 (다크 모드 활성화 결정 데이터)

```json
{
  "color_mode": "dark_mixed",
  "dark_slides": {
    "S1_cover": true,
    "S2_why_event": false,
    "S3_who_attends": false,
    "S4_what_we_offer": false,
    "S5_sponsor_tiers": false,
    "S5_t1_highlight": true,
    "S6_benefits_matrix": false,
    "S7_roi_snapshot": true,
    "S7_kpi_impact": true,
    "S8_past_sponsors": false,
    "S9_contact": true
  },
  "dark_pattern_mapping": {
    "DARK-TIER": "SVP-1 다크 대응",
    "DARK-MATRIX": "SVP-2 다크 대응 (사용 비권장)",
    "DARK-ROI": "SVP-3 다크 대응",
    "DARK-KPI": "SVP-4 다크 대응",
    "DARK-COVER": "S1 / S9 표지·종결"
  },
  "dark_ratio_max": 0.3,
  "print_force_light": true,
  "wcag_aa_compliance": true
}
```
