# Visual Patterns (v2.0) — Sponsor Deck 비주얼 패턴 라이브러리

mice-proposal v2.1.1 visual-patterns.md + infographic-patterns.md 패턴을 **sponsor-deck 컨텍스트로 포팅한 7종 표준 비주얼 패턴**이다. HTML 1차 산출물과 PPTX 2차 산출물 양쪽에서 동일하게 적용된다.

---

## 0. 공통 규약

### 0-1. 좌표·사이즈 시스템

| 항목 | HTML | PPTX (pptxgenjs) |
|------|------|-----------------|
| 슬라이드 크기 | 100vw × 100vh (16:9 비율) | LAYOUT_WIDE (13.33" × 7.5") |
| 본문 영역 | padding `--jc-space-7` (48px) | x=0.5~12.83, y=0.7~7.0 |
| 변환 비율 | 1 inch = 96px | px ÷ 96 = inch |
| 폰트 사이즈 변환 | px | pt (px × 0.75) |

### 0-2. 컬러 변수 (jc-design-system 시그니처 토큰)

```javascript
// PPTX용 변수 (hex 컬러 # 없이)
const COLOR_PRIMARY = "0A2540";        // Deep Navy
const COLOR_PRIMARY_SOFT = "1A3556";   // Primary Soft
const COLOR_ACCENT = "2962FF";         // Electric Blue
const COLOR_ACCENT_SOFT = "E8EFFF";    // Accent Soft (배경)
const COLOR_TEXT = "1A1D24";           // Charcoal
const COLOR_TEXT_MUTED = "5A6270";     // Muted
const COLOR_TEXT_DISABLED = "A0A6B0";  // Disabled
const COLOR_SURFACE = "FFFFFF";        // 카드 배경
const COLOR_SURFACE_ALT = "F1F3F7";    // 보조 서피스
const COLOR_BG = "F8F9FB";             // 페이지 배경
const COLOR_BORDER = "E5E8ED";         // 기본 보더
const COLOR_BORDER_STRONG = "C9CFD8";  // 강조 보더

// Tier 색상 (design-tokens-mapping.md §2.2 일치)
const TIER_COLORS = {
  T1: "E91E63",  // Magenta (Title)
  T2: "2962FF",  // Electric Blue (Platinum)
  T3: "FF5722",  // Vivid Orange (Gold)
  T4: "5A6270",  // Muted (Silver)
  T5: "C9CFD8",  // Border Strong (Bronze)
  T6: "00E676"   // Neon Green (In-kind)
};

// 시맨틱 컬러
const COLOR_SUCCESS = "00C853";
const COLOR_WARNING = "FFA000";
const COLOR_DANGER = "D32F2F";

// 차트 데이터 시리즈 5색
const CHART_SERIES = ["2962FF", "E91E63", "FF5722", "00E676", "0A2540"];
```

```css
/* HTML CSS 변수 (jc-design-system) */
:root {
  --jc-primary: #0A2540;
  --jc-primary-soft: #1A3556;
  --jc-accent: #2962FF;
  --jc-accent-soft: #E8EFFF;
  --jc-text: #1A1D24;
  --jc-text-muted: #5A6270;
  --jc-text-disabled: #A0A6B0;
  --jc-surface: #FFFFFF;
  --jc-surface-alt: #F1F3F7;
  --jc-bg: #F8F9FB;
  --jc-border: #E5E8ED;
  --jc-border-strong: #C9CFD8;
  --jc-point-magenta: #E91E63;
  --jc-point-orange: #FF5722;
  --jc-point-neon: #00E676;
  --jc-success: #00C853;
  --jc-warning: #FFA000;
  --jc-danger: #D32F2F;

  /* Tier 색상 */
  --tier-t1: var(--jc-point-magenta);
  --tier-t2: var(--jc-accent);
  --tier-t3: var(--jc-point-orange);
  --tier-t4: var(--jc-text-muted);
  --tier-t5: var(--jc-border-strong);
  --tier-t6: var(--jc-point-neon);
}
```

### 0-3. 폰트 표준

```javascript
const FONT_KO = "Pretendard";       // 한글 본문/제목
const FONT_EN = "Inter";            // 영문 본문
const FONT_MONO = "JetBrains Mono"; // 숫자·데이터
const FONT_HEADING = "Pretendard";  // 한·영 혼용 헤딩
```

### 0-4. pptxgenjs 주의사항

1. hex 컬러는 `#` 없이 6자리만 (`"0A2540"` ✅, `"#0A2540"` ❌) — 정본: `jc-design-system/references/shared-rules.md#RULE-PPTX-HEX`
2. 옵션 객체는 호출마다 새로 생성 (재사용 금지)
3. `bullet: true` 사용. 유니코드 `•` 직접 사용 금지
4. `breakLine: true`로 줄바꿈
5. 모든 텍스트에 `fontFace` 명시 (FONT_KO/FONT_HEADING/FONT_MONO 중 하나)

---

## 1. SVP-1 — Tier 카드 (좌측 액센트 막대 + Tier 색상)

### 1-1. 사양

| 항목 | 값 |
|------|-----|
| 용도 | Sponsor Tiers 슬라이드 (S5). Tier별 카드 가로 배치 |
| 형태 | 카드 N개 가로 또는 그리드 배치. 좌측 4~6px 액센트 막대로 Tier 식별 |
| 컬러 위계 | 좌측 막대 = Tier 색상, 카드 배경 = surface, 텍스트 = text |
| 적용 슬라이드 | S5 Sponsor Tiers (1~2 슬라이드) |

### 1-2. HTML 코드 (jc-design-system CSS 변수)

```html
<div class="tier-grid">
  <article class="tier-card" data-tier="T1" style="--tier-color: var(--tier-t1);">
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
        <li>메인 사이니지 8회</li>
        <li>VIP 만찬 단독 호스트</li>
        <li>부스 54㎡ 메인 동선</li>
      </ul>
    </div>
  </article>
  <!-- T2~T5 동일 구조, data-tier 만 변경 -->
</div>

<style>
.tier-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: var(--jc-space-4, 16px);
  width: 100%;
}
.tier-card {
  position: relative;
  display: flex;
  background: var(--jc-surface);
  border: 0.5px solid var(--jc-border);
  border-radius: 12px;
  overflow: hidden;
  transition: transform 160ms ease, box-shadow 160ms ease;
}
.tier-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(10, 37, 64, 0.08);
}
.tier-accent {
  width: 6px;
  background: var(--tier-color);
  flex-shrink: 0;
}
.tier-body {
  padding: 20px 18px;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.tier-header { margin-bottom: 12px; }
.tier-id {
  display: inline-block;
  font-family: var(--jc-font-mono, 'JetBrains Mono', monospace);
  font-size: 12px;
  color: var(--tier-color);
  font-weight: 600;
  letter-spacing: 0.05em;
}
.tier-name {
  font-size: 20px;
  font-weight: 700;
  color: var(--jc-text);
  margin: 4px 0 0;
  line-height: 1.2;
}
.tier-meta {
  margin: 8px 0 14px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--jc-border);
}
.tier-slots {
  font-size: 13px;
  color: var(--jc-text-muted);
  margin: 0;
}
.tier-price {
  font-size: 14px;
  color: var(--jc-text);
  font-weight: 600;
  margin: 4px 0 0;
}
.tier-benefits {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 13px;
  color: var(--jc-text);
  line-height: 1.6;
}
.tier-benefits li {
  padding-left: 14px;
  position: relative;
}
.tier-benefits li::before {
  content: "·";
  position: absolute;
  left: 4px;
  color: var(--tier-color);
  font-weight: 700;
}
</style>
```

### 1-3. PPTX 코드 (pptxgenjs)

```javascript
function addTierCard(slide, opts) {
  const { x, y, w, h, tierId, tierName, slots, price, benefits } = opts;
  const tierColor = TIER_COLORS[tierId];

  // 카드 배경 (roundRect)
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: COLOR_SURFACE },
    line: { color: COLOR_BORDER, width: 0.5 },
    rectRadius: 0.08
  });

  // 좌측 액센트 막대 (Tier 색상)
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.08, h,
    fill: { color: tierColor },
    line: { type: "none" }
  });

  // Tier ID (작은 라벨, Tier 색상)
  slide.addText(tierId, {
    x: x + 0.2, y: y + 0.2, w: w - 0.3, h: 0.25,
    fontSize: 11, bold: true,
    fontFace: FONT_MONO,
    color: tierColor,
    align: "left", valign: "middle", margin: 0
  });

  // Tier 이름 (메인 타이틀)
  slide.addText(tierName, {
    x: x + 0.2, y: y + 0.45, w: w - 0.3, h: 0.4,
    fontSize: 18, bold: true,
    fontFace: FONT_HEADING,
    color: COLOR_TEXT,
    align: "left", valign: "middle", margin: 0
  });

  // 슬롯 + 가격
  slide.addText(`${slots}\n${price}`, {
    x: x + 0.2, y: y + 0.9, w: w - 0.3, h: 0.6,
    fontSize: 11,
    fontFace: FONT_KO,
    color: COLOR_TEXT_MUTED,
    align: "left", valign: "top", margin: 0,
    breakLine: true
  });

  // 구분선
  slide.addShape(pres.shapes.LINE, {
    x: x + 0.2, y: y + 1.55, w: w - 0.4, h: 0,
    line: { color: COLOR_BORDER, width: 0.5 }
  });

  // 핵심 혜택 bullet
  const benefitItems = benefits.map(b => ({
    text: b,
    options: { bullet: true, fontSize: 10, fontFace: FONT_KO, color: COLOR_TEXT, paraSpaceAfter: 4 }
  }));
  slide.addText(benefitItems, {
    x: x + 0.2, y: y + 1.7, w: w - 0.3, h: h - 1.85,
    align: "left", valign: "top", margin: 0
  });
}

// 사용 예시: 5개 Tier 카드 가로 배치
const tiers = [
  { id: "T1", name: "타이틀 (Title)", slots: "한정 1석", price: "가격 별도 협의",
    benefits: ["행사명 결합권", "키노트 발표 30분", "메인 사이니지 8회", "VIP 만찬 단독", "부스 54㎡"] },
  { id: "T2", name: "플래티넘 (Platinum)", slots: "한정 3석", price: "가격 별도 협의",
    benefits: ["메인 무대 노출", "프리미엄 부스 36㎡", "VIP 만찬 6석", "보도자료 공동 명시", "SNS 2회"] },
  // T3, T4, T5 동일
];

const cardW = 2.4;
const cardH = 4.5;
const startX = 0.5;
const startY = 1.5;
tiers.forEach((tier, idx) => {
  addTierCard(slide, {
    x: startX + idx * (cardW + 0.15),
    y: startY,
    w: cardW, h: cardH,
    tierId: tier.id,
    tierName: tier.name,
    slots: tier.slots,
    price: tier.price,
    benefits: tier.benefits
  });
});
```

### 1-4. 검증 체크리스트

- [ ] 좌측 액센트 막대 색상이 `TIER_COLORS[tierId]` 와 일치
- [ ] Tier 카드 호버 시(HTML) 그림자 + 상승 인터랙션
- [ ] 카드 안에 핵심 혜택 3~5개만 표기 (과밀 금지)
- [ ] 가격 표기가 `price_mode` 설정과 일치 (`on_request` 시 "별도 협의")
- [ ] Tier 5단 카드가 한 슬라이드에 가로 배치 가능 (모바일 시 그리드 wrap 허용)

---

## 2. SVP-2 — Benefits 매트릭스 표 (7카테고리 × Tier)

### 2-1. 사양

| 항목 | 값 |
|------|-----|
| 용도 | Benefits Matrix 슬라이드 (S6). Tier × 카테고리 매핑 |
| 형태 | 표 (헤더 행 = Tier 색상 배경 또는 Primary, 본문 = 셀별 정량/✓/—) |
| 컬러 위계 | 헤더 = Primary, ✓ 셀 = success, — 셀 = text-disabled, 정량 셀 = text |
| 적용 슬라이드 | S6 Benefits Matrix (2~3 슬라이드, 카테고리 분할) |

### 2-2. HTML 코드

```html
<table class="benefits-matrix">
  <thead>
    <tr>
      <th class="cat-col">카테고리</th>
      <th class="tier-col" data-tier="T1"><span class="tier-badge">T1</span> 타이틀</th>
      <th class="tier-col" data-tier="T2"><span class="tier-badge">T2</span> 플래티넘</th>
      <th class="tier-col" data-tier="T3"><span class="tier-badge">T3</span> 골드</th>
      <th class="tier-col" data-tier="T4"><span class="tier-badge">T4</span> 실버</th>
      <th class="tier-col" data-tier="T5"><span class="tier-badge">T5</span> 브론즈</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th class="cat-row">메인 사이니지</th>
      <td class="quant">8회</td>
      <td class="quant">6회</td>
      <td class="quant">4회</td>
      <td class="quant">2회</td>
      <td class="check">✓</td>
    </tr>
    <tr>
      <th class="cat-row">보도자료 명시</th>
      <td class="quant">메인</td>
      <td class="quant">공동</td>
      <td class="quant">본문</td>
      <td class="quant">부록</td>
      <td class="dash">—</td>
    </tr>
    <tr>
      <th class="cat-row">VIP 만찬 좌석</th>
      <td class="quant">단독 10석</td>
      <td class="quant">6석</td>
      <td class="dash">—</td>
      <td class="dash">—</td>
      <td class="dash">—</td>
    </tr>
    <tr class="slot-row">
      <th class="cat-row">한정 슬롯</th>
      <td class="quant">1석</td>
      <td class="quant">3석</td>
      <td class="quant">6석</td>
      <td class="quant">10석</td>
      <td class="quant">무제한</td>
    </tr>
  </tbody>
</table>

<style>
.benefits-matrix {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--jc-font-ko, Pretendard);
  font-size: 13px;
  border: 1px solid var(--jc-border);
}
.benefits-matrix thead th {
  background: var(--jc-primary);
  color: var(--jc-surface);
  font-weight: 600;
  padding: 12px 10px;
  text-align: center;
  border-bottom: 2px solid var(--jc-accent);
}
.benefits-matrix .cat-col {
  text-align: left;
  min-width: 160px;
}
.tier-badge {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: var(--jc-font-mono, 'JetBrains Mono');
  font-size: 11px;
  margin-right: 4px;
  background: rgba(255, 255, 255, 0.18);
}
.benefits-matrix tbody th.cat-row {
  background: var(--jc-surface-alt);
  text-align: left;
  font-weight: 500;
  padding: 10px 12px;
  color: var(--jc-text);
}
.benefits-matrix tbody td {
  text-align: center;
  padding: 10px 8px;
  border-bottom: 1px solid var(--jc-border);
}
.benefits-matrix tbody tr:nth-child(even) td,
.benefits-matrix tbody tr:nth-child(even) th.cat-row {
  background: var(--jc-bg);
}
.benefits-matrix .quant {
  color: var(--jc-text);
  font-weight: 500;
}
.benefits-matrix .check {
  color: var(--jc-success);
  font-weight: 700;
  font-size: 16px;
}
.benefits-matrix .dash {
  color: var(--jc-text-disabled);
}
.benefits-matrix .slot-row td,
.benefits-matrix .slot-row th {
  background: var(--jc-accent-soft) !important;
  font-weight: 700;
  border-top: 2px solid var(--jc-accent);
}

/* 호버: 해당 행·열 하이라이트 */
.benefits-matrix tbody tr:hover td,
.benefits-matrix tbody tr:hover th {
  background: var(--jc-accent-soft);
}
</style>
```

### 2-3. PPTX 코드

```javascript
function makeMatrixHeader(tierLabels) {
  // tierLabels: ["T1 타이틀", "T2 플래티넘", ...]
  return [
    {
      text: "카테고리",
      options: {
        fill: { color: COLOR_PRIMARY }, color: "FFFFFF", bold: true,
        fontSize: 11, fontFace: FONT_KO,
        align: "left", valign: "middle",
        margin: [0.05, 0.08, 0.05, 0.08]
      }
    },
    ...tierLabels.map(label => ({
      text: label,
      options: {
        fill: { color: COLOR_PRIMARY }, color: "FFFFFF", bold: true,
        fontSize: 11, fontFace: FONT_KO,
        align: "center", valign: "middle",
        margin: [0.05, 0.08, 0.05, 0.08]
      }
    }))
  ];
}

function makeMatrixBodyRow(catName, cellValues, rowIndex) {
  const bgColor = rowIndex % 2 === 0 ? COLOR_SURFACE : COLOR_BG;
  const cells = [
    {
      text: catName,
      options: {
        fill: { color: COLOR_SURFACE_ALT },
        color: COLOR_TEXT, bold: false,
        fontSize: 10, fontFace: FONT_KO,
        align: "left", valign: "middle",
        margin: [0.05, 0.08, 0.05, 0.08]
      }
    }
  ];
  cellValues.forEach(val => {
    let cellColor, cellBold;
    if (val === "✓") {
      cellColor = COLOR_SUCCESS;
      cellBold = true;
    } else if (val === "—") {
      cellColor = COLOR_TEXT_DISABLED;
      cellBold = false;
    } else {
      cellColor = COLOR_TEXT;
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

function makeMatrixSlotRow(slotValues) {
  // 슬롯 행은 강조: accent_soft 배경 + bold
  const cells = [
    {
      text: "한정 슬롯",
      options: {
        fill: { color: COLOR_ACCENT_SOFT },
        color: COLOR_ACCENT, bold: true,
        fontSize: 11, fontFace: FONT_KO,
        align: "left", valign: "middle",
        margin: [0.05, 0.08, 0.05, 0.08]
      }
    }
  ];
  slotValues.forEach(val => {
    cells.push({
      text: String(val),
      options: {
        fill: { color: COLOR_ACCENT_SOFT },
        color: COLOR_ACCENT, bold: true,
        fontSize: 11, fontFace: FONT_KO,
        align: "center", valign: "middle",
        margin: [0.05, 0.08, 0.05, 0.08]
      }
    });
  });
  return cells;
}

// 사용 예시
const tierLabels = ["T1 타이틀", "T2 플래티넘", "T3 골드", "T4 실버", "T5 브론즈"];
const matrixRows = [
  makeMatrixHeader(tierLabels),
  makeMatrixBodyRow("메인 사이니지", ["8회", "6회", "4회", "2회", "✓"], 0),
  makeMatrixBodyRow("보도자료 명시", ["메인", "공동", "본문", "부록", "—"], 1),
  makeMatrixBodyRow("공식 SNS 포스트", ["3회", "2회", "1회", "—", "—"], 2),
  makeMatrixBodyRow("부스 면적", ["54㎡", "36㎡", "27㎡", "15㎡", "—"], 3),
  makeMatrixBodyRow("키노트·세션", ["키노트 30분", "메인 45분", "트랙 30분", "—", "—"], 4),
  makeMatrixBodyRow("리드 데이터", ["1,000건+", "600건", "400건", "200건", "—"], 5),
  makeMatrixBodyRow("VIP 만찬 좌석", ["단독 10석", "6석", "—", "—", "—"], 6),
  makeMatrixSlotRow(["1석", "3석", "6석", "10석", "무제한"])
];

slide.addTable(matrixRows, {
  x: 0.5, y: 1.3, w: 12.33,
  colW: [2.83, 1.9, 1.9, 1.9, 1.9, 1.9],
  border: { type: "solid", color: COLOR_BORDER, pt: 0.5 }
});
```

### 2-4. 검증 체크리스트

- [ ] 헤더 행 배경이 `COLOR_PRIMARY` (Deep Navy), 글자 흰색
- [ ] ✓ 셀은 `COLOR_SUCCESS` (#00C853) 굵은 글자
- [ ] — 셀은 `COLOR_TEXT_DISABLED` (#A0A6B0) 일반 글자
- [ ] 슬롯 행이 `COLOR_ACCENT_SOFT` 배경 + Accent 글자로 강조
- [ ] 짝수 행은 `COLOR_BG`, 홀수 행은 `COLOR_SURFACE` (zebra)
- [ ] 7카테고리 중 행사 유형별 우선 3~4개만 표시 (`benefit-catalog.md` §행사 유형별 카테고리 우선순위 참조)

---

## 3. SVP-3 — ROI 3단 카드 (전제·공식·추정값)

### 3-1. 사양

| 항목 | 값 |
|------|-----|
| 용도 | ROI Snapshot 슬라이드 (S7). 산업별 ROI 시뮬레이션 |
| 형태 | 3단 수직 카드. 상단 배지(산업명+Tier 색상) → ①전제→②공식→③추정값 → ⓘ 캡션 |
| 컬러 위계 | 상단 배지 = 산업 매칭 Tier 색상, 본문 = text, 캡션 = text-muted |
| 적용 슬라이드 | S7 ROI Snapshot (1~2 슬라이드, 산업 2~3종 가로 배치) |

### 3-2. HTML 코드

```html
<div class="roi-grid">
  <article class="roi-card" data-industry="tech">
    <header class="roi-header">
      <span class="roi-industry-badge">Tech 산업 스폰서 ROI</span>
    </header>
    <section class="roi-stage stage-premise">
      <h4>① 전제 조건</h4>
      <ul>
        <li>IT 참가자 약 2,184명</li>
        <li>IT 의사결정권자 약 655명</li>
      </ul>
    </section>
    <section class="roi-stage stage-formula">
      <h4>② 산출 공식</h4>
      <ul>
        <li>부스 전환율 12% × 의사결정권자</li>
        <li>리드 전환율 35% 적용</li>
      </ul>
    </section>
    <section class="roi-stage stage-estimate">
      <h4>③ 보수적 추정값</h4>
      <p class="roi-estimate-headline">리드 약 <strong>25~30건</strong></p>
      <p class="roi-estimate-secondary">PR 가치 약 KRW 25M</p>
    </section>
    <footer class="roi-caption">
      ⓘ 본 수치는 산업 벤치마크 기반 추정치이며, 실제 결과는 노출 환경·콘텐츠 품질에 따라 변동됩니다.
    </footer>
  </article>
  <!-- 두 번째 산업 카드: data-industry="finance" 등 -->
</div>

<style>
.roi-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  width: 100%;
}
.roi-card {
  background: var(--jc-surface);
  border: 0.5px solid var(--jc-border);
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.roi-header {
  background: var(--jc-primary);
  padding: 12px 16px;
}
.roi-industry-badge {
  color: var(--jc-surface);
  font-size: 14px;
  font-weight: 600;
}
.roi-stage {
  padding: 14px 18px;
  border-bottom: 1px solid var(--jc-border);
}
.roi-stage h4 {
  font-size: 13px;
  font-weight: 600;
  color: var(--jc-accent);
  margin: 0 0 6px;
  letter-spacing: 0.02em;
}
.roi-stage ul {
  margin: 0;
  padding-left: 18px;
  font-size: 13px;
  color: var(--jc-text);
  line-height: 1.55;
}
.roi-stage.stage-estimate {
  background: var(--jc-accent-soft);
  border-bottom: none;
}
.roi-estimate-headline {
  font-size: 16px;
  color: var(--jc-text);
  margin: 4px 0;
}
.roi-estimate-headline strong {
  font-family: var(--jc-font-mono, 'JetBrains Mono');
  font-size: 22px;
  color: var(--jc-accent);
  font-weight: 700;
}
.roi-estimate-secondary {
  font-size: 12px;
  color: var(--jc-text-muted);
  margin: 4px 0 0;
}
.roi-caption {
  padding: 10px 18px;
  font-size: 11px;
  color: var(--jc-text-muted);
  background: var(--jc-bg);
  line-height: 1.5;
}
</style>
```

### 3-3. PPTX 코드

```javascript
function addRoiCard(slide, opts) {
  const { x, y, w, h, industry, premise, formula, estimate, caption } = opts;

  // 카드 배경
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: COLOR_SURFACE },
    line: { color: COLOR_BORDER, width: 0.5 },
    rectRadius: 0.08
  });

  // 상단 헤더 (산업명 배지)
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h: 0.55,
    fill: { color: COLOR_PRIMARY },
    line: { type: "none" }
  });
  slide.addText(industry, {
    x: x + 0.2, y: y + 0.05, w: w - 0.4, h: 0.45,
    fontSize: 13, bold: true,
    fontFace: FONT_HEADING,
    color: "FFFFFF",
    align: "left", valign: "middle", margin: 0
  });

  // 1단: 전제 조건
  let stageY = y + 0.65;
  slide.addText("① 전제 조건", {
    x: x + 0.2, y: stageY, w: w - 0.4, h: 0.25,
    fontSize: 11, bold: true,
    fontFace: FONT_KO,
    color: COLOR_ACCENT,
    align: "left", valign: "middle", margin: 0
  });
  const premiseItems = premise.map(p => ({
    text: p,
    options: { bullet: true, fontSize: 10, fontFace: FONT_KO, color: COLOR_TEXT, paraSpaceAfter: 2 }
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
    color: COLOR_ACCENT,
    align: "left", valign: "middle", margin: 0
  });
  const formulaItems = formula.map(f => ({
    text: f,
    options: { bullet: true, fontSize: 10, fontFace: FONT_KO, color: COLOR_TEXT, paraSpaceAfter: 2 }
  }));
  slide.addText(formulaItems, {
    x: x + 0.2, y: stageY + 0.25, w: w - 0.4, h: 0.6,
    align: "left", valign: "top", margin: 0
  });

  // 3단: 보수적 추정값 (강조 영역)
  stageY = y + 2.45;
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y: stageY, w, h: 0.9,
    fill: { color: COLOR_ACCENT_SOFT },
    line: { type: "none" }
  });
  slide.addText("③ 보수적 추정값", {
    x: x + 0.2, y: stageY + 0.05, w: w - 0.4, h: 0.25,
    fontSize: 11, bold: true,
    fontFace: FONT_KO,
    color: COLOR_ACCENT,
    align: "left", valign: "middle", margin: 0
  });
  slide.addText(estimate.headline, {
    x: x + 0.2, y: stageY + 0.3, w: w - 0.4, h: 0.35,
    fontSize: 14, bold: true,
    fontFace: FONT_HEADING,
    color: COLOR_TEXT,
    align: "left", valign: "middle", margin: 0
  });
  if (estimate.secondary) {
    slide.addText(estimate.secondary, {
      x: x + 0.2, y: stageY + 0.62, w: w - 0.4, h: 0.25,
      fontSize: 10,
      fontFace: FONT_KO,
      color: COLOR_TEXT_MUTED,
      align: "left", valign: "middle", margin: 0
    });
  }

  // 캡션
  stageY = y + h - 0.45;
  slide.addText(caption || "ⓘ 본 수치는 산업 벤치마크 기반 추정치이며, 실제 결과는 노출 환경·콘텐츠 품질에 따라 변동됩니다.", {
    x: x + 0.2, y: stageY, w: w - 0.4, h: 0.4,
    fontSize: 8,
    fontFace: FONT_KO,
    color: COLOR_TEXT_MUTED,
    italic: true,
    align: "left", valign: "top", margin: 0
  });
}

// 사용 예시: 2개 산업 ROI 카드 가로 배치
const roiCases = [
  {
    industry: "Tech 산업 스폰서 ROI",
    premise: ["IT 참가자 약 2,184명", "IT 의사결정권자 약 655명"],
    formula: ["부스 전환율 12% × 의사결정권자", "리드 전환율 35% 적용"],
    estimate: { headline: "리드 약 25~30건", secondary: "PR 가치 약 KRW 25M" }
  },
  {
    industry: "Finance 산업 스폰서 ROI",
    premise: ["금융 참가자 약 1,248명", "C-Level + 임원 약 287명"],
    formula: ["VIP 만찬 단독 직접 접점 8~10명", "1:1 미팅 평균 LTV × 5% 전환"],
    estimate: { headline: "직접 접점 약 8~10명", secondary: "잠재 영업 가치 산업 벤치마크 기반" }
  }
];

const cardW = 5.9;
const cardH = 5.3;
const gap = 0.4;
const startX = (13.33 - (cardW * 2 + gap)) / 2;
roiCases.forEach((roi, idx) => {
  addRoiCard(slide, {
    x: startX + idx * (cardW + gap),
    y: 1.5,
    w: cardW, h: cardH,
    industry: roi.industry,
    premise: roi.premise,
    formula: roi.formula,
    estimate: roi.estimate
  });
});
```

### 3-4. 검증 체크리스트

- [ ] 3단 구조 강제: ① 전제 → ② 공식 → ③ 추정값. 누락 시 빌드 실패
- [ ] ③ 추정값 단은 `COLOR_ACCENT_SOFT` 배경으로 강조
- [ ] 하단에 "ⓘ 본 수치는 산업 벤치마크 기반 추정치" 캡션 의무 (`roi-case-templates.md` §1.1)
- [ ] 산업명 배지 상단 헤더가 `COLOR_PRIMARY` (Deep Navy)
- [ ] "수억원", "확실한", "압도적" 등 절대 회피 표현 0건 (`roi-case-templates.md` §9)

---

## 4. SVP-4 — KPI 콜아웃 (큰 숫자 + 캡션)

### 4-1. 사양

| 항목 | 값 |
|------|-----|
| 용도 | Who Attends 슬라이드 (S3). 청중 규모·의사결정권자·B2B 비율 등 강조 |
| 형태 | 큰 숫자 (mono 폰트) + 단위 + 라벨 + 출처 캡션. 카드 N개 가로 배치 |
| 컬러 위계 | 숫자 = Accent (Electric Blue), 단위 = Accent, 라벨 = text, 캡션 = text-muted |
| 적용 슬라이드 | S3-1 (KPI 3~4개), S7 ROI 추가 강조 (선택) |
| 베이스 | mice-proposal CHART-C3 빅넘버 콜아웃 포팅 |

### 4-2. HTML 코드

```html
<div class="kpi-callout-grid">
  <div class="kpi-callout">
    <div class="kpi-number">5,200</div>
    <div class="kpi-unit">명</div>
    <div class="kpi-label">예상 참가자</div>
    <div class="kpi-source">2024년 회차 4,800명 + 14% 성장 가정</div>
  </div>
  <div class="kpi-callout">
    <div class="kpi-number">32</div>
    <div class="kpi-unit">%</div>
    <div class="kpi-label">의사결정권자</div>
    <div class="kpi-source">자기 응답 데이터</div>
  </div>
  <div class="kpi-callout">
    <div class="kpi-number">23</div>
    <div class="kpi-unit">%</div>
    <div class="kpi-label">C-Level + 임원</div>
    <div class="kpi-source">직급 기반 분류</div>
  </div>
  <div class="kpi-callout">
    <div class="kpi-number">87</div>
    <div class="kpi-unit">%</div>
    <div class="kpi-label">B2B 비율</div>
    <div class="kpi-source">자기 응답</div>
  </div>
</div>

<style>
.kpi-callout-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  width: 100%;
}
.kpi-callout {
  background: var(--jc-surface);
  border: 0.5px solid var(--jc-border);
  border-left: 4px solid var(--jc-accent);
  border-radius: 12px;
  padding: 20px 18px;
  text-align: center;
}
.kpi-number {
  font-family: var(--jc-font-mono, 'JetBrains Mono', monospace);
  font-size: 56px;
  font-weight: 700;
  color: var(--jc-accent);
  line-height: 1;
  display: inline-block;
}
.kpi-unit {
  display: inline-block;
  font-family: var(--jc-font-ko, Pretendard);
  font-size: 20px;
  font-weight: 600;
  color: var(--jc-accent);
  margin-left: 4px;
  vertical-align: top;
  padding-top: 4px;
}
.kpi-label {
  font-size: 14px;
  color: var(--jc-text);
  font-weight: 500;
  margin-top: 8px;
}
.kpi-source {
  font-size: 11px;
  color: var(--jc-text-muted);
  margin-top: 6px;
  line-height: 1.4;
}
</style>
```

### 4-3. PPTX 코드 (mice-proposal CHART-C3 포팅)

```javascript
function addKpiCallout(slide, opts) {
  const { x, y, w, h, value, unit, label, source } = opts;

  // 카드 배경 + 좌측 Accent 보더
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: COLOR_SURFACE },
    line: { color: COLOR_BORDER, width: 0.5 },
    rectRadius: 0.08
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.06, h,
    fill: { color: COLOR_ACCENT },
    line: { type: "none" }
  });

  // 숫자 자동 천단위 콤마 (mice-proposal v1.1 패치 적용)
  const valueStr = typeof value === "number"
    ? value.toLocaleString("ko-KR")
    : String(value);

  // 큰 숫자
  slide.addText(valueStr, {
    x: x + 0.1, y: y + 0.3, w: w - 0.2, h: h * 0.48,
    fontSize: 48, bold: true,
    fontFace: FONT_MONO,
    color: COLOR_ACCENT,
    align: "center", valign: "middle", margin: 0
  });

  // 단위 (큰 숫자 옆 또는 아래)
  if (unit) {
    slide.addText(unit, {
      x: x + 0.1, y: y + 0.3 + h * 0.48, w: w - 0.2, h: 0.3,
      fontSize: 16, bold: true,
      fontFace: FONT_KO,
      color: COLOR_ACCENT,
      align: "center", valign: "top", margin: 0
    });
  }

  // 라벨
  slide.addText(label, {
    x: x + 0.1, y: y + h * 0.72, w: w - 0.2, h: 0.3,
    fontSize: 12, bold: false,
    fontFace: FONT_KO,
    color: COLOR_TEXT,
    align: "center", valign: "middle", margin: 0
  });

  // 출처 캡션
  if (source) {
    slide.addText(source, {
      x: x + 0.1, y: y + h * 0.85, w: w - 0.2, h: 0.3,
      fontSize: 9,
      fontFace: FONT_KO,
      color: COLOR_TEXT_MUTED,
      align: "center", valign: "top", margin: 0
    });
  }
}

// 사용 예시: 4개 KPI 콜아웃 가로 배치
const kpis = [
  { value: 5200, unit: "명", label: "예상 참가자", source: "2024년 회차 4,800명 + 14% 성장 가정" },
  { value: 32, unit: "%", label: "의사결정권자", source: "자기 응답 데이터" },
  { value: 23, unit: "%", label: "C-Level + 임원", source: "직급 기반 분류" },
  { value: 87, unit: "%", label: "B2B 비율", source: "자기 응답" }
];

const cardW = 2.8;
const cardH = 2.6;
const gap = 0.25;
const startX = (13.33 - (cardW * 4 + gap * 3)) / 2;
kpis.forEach((kpi, idx) => {
  addKpiCallout(slide, {
    x: startX + idx * (cardW + gap),
    y: 2.2,
    w: cardW, h: cardH,
    value: kpi.value,
    unit: kpi.unit,
    label: kpi.label,
    source: kpi.source
  });
});
```

### 4-4. 검증 체크리스트

- [ ] 숫자 폰트가 `FONT_MONO` (JetBrains Mono) — 시각 정렬·임팩트
- [ ] 숫자 색상이 `COLOR_ACCENT` (Electric Blue)
- [ ] number 타입은 `toLocaleString("ko-KR")` 으로 천단위 콤마 자동 (`5200` → `5,200`)
- [ ] 출처 캡션 의무 (`audience-profile.md` §2 데이터 출처 표기)
- [ ] 좌측 4~6px Accent 보더 (식별성)
- [ ] KPI 3~4개 한 슬라이드에 균등 배치

---

## 5. SVP-5 — 산업 분포 가로 바 차트

### 5-1. 사양

| 항목 | 값 |
|------|-----|
| 용도 | Who Attends 슬라이드 (S3-2). 청중 산업 분포 |
| 형태 | 가로 바 차트. 라벨 + 막대 + 비율(%) 가로 배치 |
| 컬러 위계 | 상위 산업 = CHART_SERIES 1~5, 기타 = text-muted |
| 적용 슬라이드 | S3-2 산업 분포 |
| 베이스 | mice-proposal CHART-C2 포팅 |

### 5-2. HTML 코드 (CSS-only)

```html
<div class="industry-bar-chart">
  <h3 class="chart-title">산업 분포 (Top 5)</h3>
  <div class="bar-row">
    <span class="bar-label">IT·소프트웨어</span>
    <div class="bar-track">
      <div class="bar-fill" style="--width: 42%; --color: var(--jc-data-1, #2962FF);"></div>
    </div>
    <span class="bar-value">42%</span>
  </div>
  <div class="bar-row">
    <span class="bar-label">금융·보험</span>
    <div class="bar-track">
      <div class="bar-fill" style="--width: 24%; --color: var(--jc-data-2, #E91E63);"></div>
    </div>
    <span class="bar-value">24%</span>
  </div>
  <div class="bar-row">
    <span class="bar-label">제조·산업재</span>
    <div class="bar-track">
      <div class="bar-fill" style="--width: 18%; --color: var(--jc-data-3, #FF5722);"></div>
    </div>
    <span class="bar-value">18%</span>
  </div>
  <div class="bar-row">
    <span class="bar-label">헬스케어·바이오</span>
    <div class="bar-track">
      <div class="bar-fill" style="--width: 10%; --color: var(--jc-data-4, #00E676);"></div>
    </div>
    <span class="bar-value">10%</span>
  </div>
  <div class="bar-row">
    <span class="bar-label">기타</span>
    <div class="bar-track">
      <div class="bar-fill" style="--width: 6%; --color: var(--jc-text-muted, #5A6270);"></div>
    </div>
    <span class="bar-value">6%</span>
  </div>
  <p class="chart-source">출처: 2024년 회차 등록 산업 분류</p>
</div>

<style>
.industry-bar-chart {
  width: 100%;
  font-family: var(--jc-font-ko, Pretendard);
}
.chart-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--jc-text);
  margin: 0 0 16px;
}
.bar-row {
  display: grid;
  grid-template-columns: 160px 1fr 60px;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
}
.bar-label {
  font-size: 13px;
  color: var(--jc-text);
  text-align: right;
}
.bar-track {
  width: 100%;
  height: 24px;
  background: var(--jc-bg);
  border-radius: 4px;
  overflow: hidden;
}
.bar-fill {
  width: var(--width);
  height: 100%;
  background: var(--color);
  border-radius: 4px;
  transition: width 320ms ease;
}
.bar-value {
  font-family: var(--jc-font-mono, 'JetBrains Mono');
  font-size: 14px;
  font-weight: 600;
  color: var(--jc-text);
  text-align: right;
}
.chart-source {
  font-size: 11px;
  color: var(--jc-text-muted);
  margin: 16px 0 0;
  font-style: italic;
}
</style>
```

### 5-3. PPTX 코드 (pptxgenjs BAR 차트 + 데이터 시리즈 5색)

```javascript
// 산업 분포 가로 바 차트 (수평 바)
slide.addChart(pres.charts.BAR, [{
  name: "산업 분포",
  labels: ["IT·소프트웨어", "금융·보험", "제조·산업재", "헬스케어·바이오", "기타"],
  values: [42, 24, 18, 10, 6]
}], {
  x: 0.5, y: 1.5, w: 9.0, h: 5.0,
  barDir: "bar",  // 가로 바
  chartColors: CHART_SERIES,  // 데이터 시리즈 5색
  chartArea: { fill: { color: COLOR_SURFACE } },
  plotArea: { fill: { color: COLOR_SURFACE } },
  catAxisLabelColor: COLOR_TEXT,
  catAxisLabelFontSize: 11,
  catAxisLabelFontFace: FONT_KO,
  valAxisLabelColor: COLOR_TEXT_MUTED,
  valAxisLabelFontSize: 9,
  valGridLine: { color: COLOR_BORDER, size: 0.5 },
  catGridLine: { style: "none" },
  showValue: true,
  dataLabelPosition: "outEnd",
  dataLabelColor: COLOR_TEXT,
  dataLabelFontSize: 11,
  dataLabelFontBold: true,
  dataLabelFontFace: FONT_HEADING,
  dataLabelFormatCode: '0"%"',
  showLegend: false,
  valAxisMaxVal: 50,
  valAxisMinVal: 0
});

// 우측 출처 캡션
slide.addText("출처: 2024년 회차 등록 산업 분류", {
  x: 10.0, y: 6.2, w: 2.8, h: 0.3,
  fontSize: 9, italic: true,
  fontFace: FONT_KO,
  color: COLOR_TEXT_MUTED,
  align: "left", valign: "middle", margin: 0
});

// 우측 인사이트 박스 (선택)
slide.addText("상위 3개 산업 (IT·금융·제조) 비중 합계 84%", {
  x: 10.0, y: 2.0, w: 2.8, h: 0.6,
  fontSize: 12, bold: true,
  fontFace: FONT_KO,
  color: COLOR_ACCENT,
  align: "left", valign: "top", margin: 0
});
slide.addText("스폰서 영업 1순위 타겟 산업", {
  x: 10.0, y: 2.65, w: 2.8, h: 0.4,
  fontSize: 10,
  fontFace: FONT_KO,
  color: COLOR_TEXT_MUTED,
  align: "left", valign: "top", margin: 0
});
```

### 5-4. 검증 체크리스트

- [ ] 차트 색상이 `CHART_SERIES` 5색 (`#2962FF`, `#E91E63`, `#FF5722`, `#00E676`, `#0A2540`)
- [ ] 비율(%) 합계가 100%인지 검증 (`audience-profile.md` §4.2)
- [ ] "기타" 5% 이상이면 통합 처리
- [ ] 출처 캡션 의무
- [ ] HTML은 CSS-only (외부 라이브러리 의존 0)
- [ ] PPTX `dataLabelFormatCode: '0"%"'` 로 % 단위 자동 표시

---

## 6. SVP-6 — 모객·전환 퍼널

### 6-1. 사양

| 항목 | 값 |
|------|-----|
| 용도 | Who Attends 슬라이드 (S3 선택). 모객 깔때기 또는 청중 ≥ IT 비중 ≥ 의사결정권자 단계 |
| 형태 | 사다리꼴 N개 (3~5단계), 단계별 점진적 좁아짐. 우측에 전환율 % 표시 |
| 컬러 위계 | 상단 Accent (밝게) → 하단 Primary (진하게) |
| 적용 슬라이드 | S3 Who Attends (선택, 청중 깔때기 시각화) |
| 베이스 | mice-proposal INFO-I1 퍼널 포팅 |

### 6-2. HTML 코드 (SVG)

```html
<div class="funnel-chart">
  <h3 class="chart-title">청중 깔때기 — 전체 → 타겟 의사결정권자</h3>
  <div class="funnel-wrapper">
    <svg class="funnel-svg" viewBox="0 0 600 400" preserveAspectRatio="xMidYMid meet">
      <!-- Stage 1: 전체 참가자 (rate 100%) -->
      <polygon points="50,20 550,20 510,90 90,90"
               fill="#5B9BD5" stroke="#FFFFFF" stroke-width="2"/>
      <text x="300" y="50" text-anchor="middle" fill="#FFFFFF" font-size="14" font-weight="700">전체 참가자</text>
      <text x="300" y="72" text-anchor="middle" fill="#FFFFFF" font-size="18" font-weight="700">5,200명</text>
      <!-- Stage 2: IT 산업 (rate 42%) -->
      <polygon points="90,100 510,100 470,170 130,170"
               fill="#2962FF" stroke="#FFFFFF" stroke-width="2"/>
      <text x="300" y="130" text-anchor="middle" fill="#FFFFFF" font-size="14" font-weight="700">IT 산업</text>
      <text x="300" y="152" text-anchor="middle" fill="#FFFFFF" font-size="18" font-weight="700">2,184명</text>
      <!-- Stage 3: IT 의사결정권자 (rate 30%) -->
      <polygon points="130,180 470,180 430,250 170,250"
               fill="#1E4DCC" stroke="#FFFFFF" stroke-width="2"/>
      <text x="300" y="210" text-anchor="middle" fill="#FFFFFF" font-size="14" font-weight="700">IT 의사결정권자</text>
      <text x="300" y="232" text-anchor="middle" fill="#FFFFFF" font-size="18" font-weight="700">655명</text>
      <!-- Stage 4: 부스 방문 추정 (rate 12%) -->
      <polygon points="170,260 430,260 390,330 210,330"
               fill="#0A2540" stroke="#FFFFFF" stroke-width="2"/>
      <text x="300" y="290" text-anchor="middle" fill="#FFFFFF" font-size="14" font-weight="700">부스 방문 추정</text>
      <text x="300" y="312" text-anchor="middle" fill="#FFFFFF" font-size="18" font-weight="700">78명</text>
    </svg>
    <div class="funnel-rates">
      <span class="rate-step">↓ 42%</span>
      <span class="rate-step">↓ 30%</span>
      <span class="rate-step">↓ 12%</span>
    </div>
  </div>
  <p class="chart-source">출처: 2024년 회차 데이터 + 부스 평균 전환율 12% (Tech 산업 벤치마크)</p>
</div>

<style>
.funnel-chart {
  width: 100%;
  font-family: var(--jc-font-ko, Pretendard);
}
.funnel-wrapper {
  display: grid;
  grid-template-columns: 1fr 80px;
  gap: 16px;
  align-items: stretch;
}
.funnel-svg {
  width: 100%;
  max-height: 360px;
}
.funnel-rates {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  padding: 60px 0;
}
.rate-step {
  font-family: var(--jc-font-mono, 'JetBrains Mono');
  font-size: 14px;
  font-weight: 600;
  color: var(--jc-accent);
}
</style>
```

### 6-3. PPTX 코드 (mice-proposal INFO-I1 포팅, sponsor-deck 컨텍스트)

```javascript
function addSponsorFunnel(slide, opts) {
  const { x, y, w, h, stages } = opts;
  const stageH = h / stages.length;
  const defaultColors = ["5B9BD5", "2962FF", "1E4DCC", "0A2540"];

  stages.forEach((stage, idx) => {
    const stageW = w * stage.rate;
    const stageX = x + (w - stageW) / 2;
    const stageY = y + idx * stageH;
    const color = (stage.color || defaultColors[idx % defaultColors.length]);

    slide.addShape(pres.shapes.RECTANGLE, {
      x: stageX, y: stageY, w: stageW, h: stageH * 0.85,
      fill: { color },
      line: { color: COLOR_SURFACE, width: 2 }
    });

    // 단계 라벨 (사각형 내부)
    slide.addText([
      { text: stage.label, options: { bold: true, fontSize: 12, fontFace: FONT_KO, breakLine: true } },
      { text: stage.value.toLocaleString("ko-KR") + (stage.unit || "명"),
        options: { fontSize: 18, bold: true, fontFace: FONT_HEADING } }
    ], {
      x: stageX, y: stageY, w: stageW, h: stageH * 0.85,
      color: "FFFFFF",
      align: "center", valign: "middle", margin: 0
    });

    // 우측 부가 설명 (전환율 화살표)
    if (idx < stages.length - 1) {
      const nextRate = stages[idx + 1].value / stage.value;
      const ratePct = Math.round(nextRate * 100);
      slide.addText(`↓ ${ratePct}%`, {
        x: x + w + 0.2, y: stageY + stageH * 0.35,
        w: 1.0, h: 0.4,
        fontSize: 12, color: COLOR_ACCENT, bold: true,
        fontFace: FONT_MONO,
        align: "left", valign: "middle", margin: 0
      });
    }
  });
}

// 사용 예시: 청중 깔때기
const funnelStages = [
  { label: "전체 참가자", value: 5200, rate: 1.0 },
  { label: "IT 산업", value: 2184, rate: 0.7 },
  { label: "IT 의사결정권자", value: 655, rate: 0.45 },
  { label: "부스 방문 추정", value: 78, rate: 0.22 }
];

addSponsorFunnel(slide, {
  x: 1.5, y: 1.5, w: 8.5, h: 5.0,
  stages: funnelStages
});

// 우측 인사이트 (CHART-C3 KPI 활용)
slide.addText("최종 전환율", {
  x: 10.5, y: 2.5, w: 2.5, h: 0.4,
  fontSize: 13, color: COLOR_TEXT_MUTED,
  fontFace: FONT_KO,
  align: "left", margin: 0
});
slide.addText("1.5%", {
  x: 10.5, y: 3.0, w: 2.5, h: 1.0,
  fontSize: 48, bold: true, color: COLOR_ACCENT,
  fontFace: FONT_MONO,
  align: "left", valign: "top", margin: 0
});
slide.addText("부스 방문 → 의사결정권자\n5,200명 중 78명 도달", {
  x: 10.5, y: 4.2, w: 2.5, h: 1.0,
  fontSize: 11, color: COLOR_TEXT,
  fontFace: FONT_KO,
  align: "left", valign: "top", margin: 0
});
```

### 6-4. 검증 체크리스트

- [ ] 단계가 점진적으로 좁아짐 (인접 단계 너비 차이 최소 10%)
- [ ] 우측 전환율 화살표 자동 계산 (`nextRate = next.value / current.value`)
- [ ] 색상 진행: 상단 Accent → 하단 Primary (시간·전환 흐름 표현)
- [ ] 우측 인사이트 KPI 콜아웃 (SVP-4) 함께 배치 권장
- [ ] 출처 캡션 의무

---

## 7. SVP-7 — 2×2 매트릭스 (Tier 차별화·산업 우선순위)

### 7-1. 사양

| 항목 | 값 |
|------|-----|
| 용도 | Tier 차별화 매트릭스 (S5 보조) 또는 산업 우선순위 매핑 (S2 또는 S7 보조) |
| 형태 | X·Y 축 + 4사분면 + 점 또는 산업·Tier 라벨 플로팅 |
| 컬러 위계 | Q1 (이상적) = Accent Soft, 본 행사·우선 산업 = Accent, 비교 = text-muted |
| 적용 슬라이드 | S2 Why This Event (행사 포지셔닝) 또는 S5/S7 보조 |
| 베이스 | mice-proposal INFO-I2 포팅 |

### 7-2. HTML 코드 (SVG)

```html
<div class="matrix-2x2-chart">
  <h3 class="chart-title">산업 우선순위 매트릭스 — 비중 × 의사결정권자 비율</h3>
  <div class="matrix-wrapper">
    <svg class="matrix-svg" viewBox="0 0 600 480" preserveAspectRatio="xMidYMid meet">
      <!-- Y축 라벨 -->
      <text x="20" y="20" font-size="12" font-weight="700" fill="#1A1D24">↑ 의사결정권자 비율</text>
      <!-- X축 라벨 -->
      <text x="560" y="470" font-size="12" font-weight="700" fill="#1A1D24" text-anchor="end">산업 비중 →</text>

      <!-- 4사분면 배경 -->
      <rect x="300" y="50" width="250" height="200" fill="#E8EFFF"/>       <!-- Q1 우상: 이상적 -->
      <rect x="50" y="50" width="250" height="200" fill="#F1F3F7"/>        <!-- Q2 좌상 -->
      <rect x="50" y="250" width="250" height="200" fill="#F8F9FB"/>       <!-- Q3 좌하 -->
      <rect x="300" y="250" width="250" height="200" fill="#FFF3E0"/>      <!-- Q4 우하 -->

      <!-- 사분면 라벨 -->
      <text x="320" y="80" font-size="11" font-style="italic" fill="#5A6270">⭐ Tier 1 영업 대상</text>
      <text x="60" y="80" font-size="11" font-style="italic" fill="#5A6270">Tier 2~3 영업 가능</text>
      <text x="60" y="430" font-size="11" font-style="italic" fill="#5A6270">우선순위 낮음</text>
      <text x="320" y="430" font-size="11" font-style="italic" fill="#5A6270">대량 노출 Tier 4~5</text>

      <!-- X축 (가로선) -->
      <line x1="50" y1="250" x2="550" y2="250" stroke="#5A6270" stroke-width="1.5"
            marker-end="url(#arrow)"/>
      <!-- Y축 (세로선) -->
      <line x1="300" y1="450" x2="300" y2="50" stroke="#5A6270" stroke-width="1.5"
            marker-end="url(#arrow)"/>

      <!-- 화살표 마커 정의 -->
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
          <path d="M0,0 L0,10 L10,5 z" fill="#5A6270"/>
        </marker>
      </defs>

      <!-- 산업 데이터 점 -->
      <!-- IT (x=42%, y=30%) -->
      <circle cx="466" cy="200" r="14" fill="#2962FF" stroke="#FFFFFF" stroke-width="2"/>
      <text x="488" y="200" font-size="13" font-weight="700" fill="#1A1D24" dominant-baseline="middle">IT (42% / 30%)</text>
      <!-- Finance (x=24%, y=70%) -->
      <circle cx="370" cy="116" r="14" fill="#E91E63" stroke="#FFFFFF" stroke-width="2"/>
      <text x="392" y="116" font-size="13" font-weight="700" fill="#1A1D24" dominant-baseline="middle">Finance (24% / 70%)</text>
      <!-- 제조 (x=18%, y=20%) -->
      <circle cx="346" cy="290" r="11" fill="#FF5722" stroke="#FFFFFF" stroke-width="2"/>
      <text x="364" y="290" font-size="12" fill="#1A1D24" dominant-baseline="middle">제조 (18% / 20%)</text>
      <!-- 헬스케어 (x=10%, y=40%) -->
      <circle cx="190" cy="170" r="10" fill="#00E676" stroke="#FFFFFF" stroke-width="2"/>
      <text x="207" y="170" font-size="12" fill="#1A1D24" dominant-baseline="middle">헬스케어 (10% / 40%)</text>
    </svg>
  </div>
  <p class="chart-source">출처: 2024년 회차 등록 + 의사결정권자 자기 응답</p>
</div>

<style>
.matrix-2x2-chart {
  width: 100%;
  font-family: var(--jc-font-ko, Pretendard);
}
.matrix-wrapper {
  width: 100%;
  max-width: 720px;
  margin: 0 auto;
}
.matrix-svg {
  width: 100%;
  max-height: 480px;
}
</style>
```

### 7-3. PPTX 코드 (mice-proposal INFO-I2 포팅)

```javascript
function addSponsorMatrix(slide, opts) {
  const { x, y, w, h, xLabel, yLabel, quadrants, dots } = opts;
  const halfW = w / 2;
  const halfH = h / 2;

  // 4사분면 배경
  const quadColors = ["E8EFFF", "F1F3F7", "F8F9FB", "FFF3E0"];
  // 우상 Q1
  slide.addShape(pres.shapes.RECTANGLE, {
    x: x + halfW, y, w: halfW, h: halfH,
    fill: { color: quadColors[0] }, line: { type: "none" }
  });
  // 좌상 Q2
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w: halfW, h: halfH,
    fill: { color: quadColors[1] }, line: { type: "none" }
  });
  // 좌하 Q3
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y: y + halfH, w: halfW, h: halfH,
    fill: { color: quadColors[2] }, line: { type: "none" }
  });
  // 우하 Q4
  slide.addShape(pres.shapes.RECTANGLE, {
    x: x + halfW, y: y + halfH, w: halfW, h: halfH,
    fill: { color: quadColors[3] }, line: { type: "none" }
  });

  // 사분면 라벨 (코너에서 0.3" 안쪽 — v1.1 패치)
  if (quadrants) {
    const corners = [
      { x: x + halfW + 0.3, y: y + 0.3, text: quadrants[0] },
      { x: x + 0.3, y: y + 0.3, text: quadrants[1] },
      { x: x + 0.3, y: y + halfH + 0.2, text: quadrants[2] },
      { x: x + halfW + 0.3, y: y + halfH + 0.2, text: quadrants[3] }
    ];
    corners.forEach(c => {
      slide.addText(c.text, {
        x: c.x, y: c.y, w: halfW - 0.5, h: 0.35,
        fontSize: 10, italic: true,
        fontFace: FONT_KO,
        color: COLOR_TEXT_MUTED,
        align: "left", valign: "top", margin: 0
      });
    });
  }

  // X축
  slide.addShape(pres.shapes.LINE, {
    x, y: y + halfH, w, h: 0,
    line: { color: COLOR_TEXT_MUTED, width: 1.5, endArrowType: "triangle" }
  });
  // Y축
  slide.addShape(pres.shapes.LINE, {
    x: x + halfW, y: y + h, w: 0, h: -h,
    line: { color: COLOR_TEXT_MUTED, width: 1.5, endArrowType: "triangle" }
  });

  // 축 라벨 (매트릭스 바깥 — v1.1 패치)
  if (xLabel) {
    slide.addText(xLabel, {
      x: x + w + 0.1, y: y + halfH - 0.2, w: 1.3, h: 0.4,
      fontSize: 11, bold: true,
      fontFace: FONT_KO,
      color: COLOR_TEXT,
      align: "left", valign: "middle", margin: 0
    });
  }
  if (yLabel) {
    slide.addText(yLabel, {
      x: x + halfW - 0.7, y: y - 0.5, w: 1.6, h: 0.4,
      fontSize: 11, bold: true,
      fontFace: FONT_KO,
      color: COLOR_TEXT,
      align: "center", valign: "middle", margin: 0
    });
  }

  // 데이터 점
  if (dots) {
    dots.forEach(dot => {
      const dotX = x + dot.x * w;
      const dotY = y + (1 - dot.y) * h;
      const dotSize = dot.isPrimary ? 0.4 : 0.3;
      const dotColor = dot.color || (dot.isPrimary ? COLOR_ACCENT : COLOR_TEXT_MUTED);

      slide.addShape(pres.shapes.OVAL, {
        x: dotX - dotSize / 2, y: dotY - dotSize / 2,
        w: dotSize, h: dotSize,
        fill: { color: dotColor },
        line: { color: "FFFFFF", width: 2 }
      });

      slide.addText(dot.name, {
        x: dotX + dotSize / 2 + 0.05, y: dotY - 0.15,
        w: 2.0, h: 0.3,
        fontSize: 10, bold: dot.isPrimary,
        fontFace: FONT_KO,
        color: COLOR_TEXT,
        align: "left", valign: "middle", margin: 0
      });
    });
  }
}

// 사용 예시: 산업 우선순위 매트릭스
addSponsorMatrix(slide, {
  x: 2.0, y: 1.5, w: 8.5, h: 5.5,
  xLabel: "비중 →",
  yLabel: "↑ 의사결정권자 비율",
  quadrants: ["⭐ Tier 1 영업 대상", "Tier 2~3 영업 가능", "우선순위 낮음", "대량 노출 Tier 4~5"],
  dots: [
    { name: "IT (42%, 30%)", x: 0.84, y: 0.3, isPrimary: true, color: "2962FF" },
    { name: "Finance (24%, 70%)", x: 0.48, y: 0.7, isPrimary: true, color: "E91E63" },
    { name: "제조 (18%, 20%)", x: 0.36, y: 0.2, color: "FF5722" },
    { name: "헬스케어 (10%, 40%)", x: 0.2, y: 0.4, color: "00E676" }
  ]
});
```

### 7-4. 검증 체크리스트

- [ ] 사분면 라벨이 코너에서 0.3" 안쪽 (v1.1 패치 — 축 라벨 충돌 방지)
- [ ] X축 라벨이 매트릭스 우측 바깥 (`x + w + 0.1`)
- [ ] Y축 라벨이 매트릭스 상단 바깥 (`y - 0.5`)
- [ ] 본 행사 우선 점은 `isPrimary: true` → 크기 +33%, 굵은 글씨
- [ ] 점·라벨이 다른 점과 겹치지 않음 (좌표 검증)
- [ ] Q1 (우상) 배경이 `E8EFFF` (Accent Soft) — 이상적 영역 강조

---

## 8. HTML → PPTX 매핑 룰표

| HTML 요소 (SVP 패턴) | PPTX 변환 메서드 | 비고 |
|---------------------|----------------|------|
| `.tier-card` (SVP-1) | `addShape(ROUNDED_RECTANGLE)` + 좌측 `addShape(RECTANGLE)` + `addText` | 좌측 Tier 색상 막대 유지 |
| `.benefits-matrix` (SVP-2) | `addTable` + 헤더 `COLOR_PRIMARY` + 슬롯 행 `COLOR_ACCENT_SOFT` | zebra·hover 인터랙션은 정적 제거 |
| `.roi-card` (SVP-3) | `addShape(ROUNDED_RECTANGLE)` + 헤더 `addShape(RECTANGLE)` + 3단 `addText` | 3단 영역 `accent_soft` 배경 |
| `.kpi-callout` (SVP-4) | `addShape(ROUNDED_RECTANGLE)` + 좌측 보더 `addShape(RECTANGLE)` + 큰 숫자 `addText(FONT_MONO)` | toLocaleString("ko-KR") 자동 |
| `.industry-bar-chart` (SVP-5) | `addChart(BAR)` + `barDir: "bar"` + `CHART_SERIES` | dataLabelFormatCode: `'0"%"'` |
| `.funnel-svg` (SVP-6) | `addShape(RECTANGLE)` N개 점진적 너비 변화 + 우측 전환율 `addText` | 사다리꼴 → 사각형 적층 |
| `.matrix-svg` (SVP-7) | 4 `addShape(RECTANGLE)` + 2 `addShape(LINE)` 화살표 + N `addShape(OVAL)` 점 + `addText` 라벨 | 축 라벨은 매트릭스 바깥 |

### 8-1. 공통 변환 룰

- HTML CSS 변수 `var(--jc-*)` → PPTX 상수 `COLOR_*` (값 일치)
- HTML 호버·인터랙션 → PPTX 정적 표현 (제거)
- HTML px → PPTX inch (×1/96)
- HTML font-size px → PPTX fontSize pt (×0.75)
- HTML CSS class 선택자 → PPTX 옵션 객체 (호출마다 새로 생성)

---

## 9. 슬라이드별 SVP 패턴 매핑 (sponsor-deck 표준 구조 기준)

| 슬라이드 | 1순위 SVP | 2순위 SVP (선택) | 비고 |
|---------|----------|----------------|------|
| S1 표지 | — | — | DARK-COVER 또는 라이트 표지. SVP 미적용 |
| S2 Why This Event | SVP-7 (포지셔닝 매트릭스) | — | 행사 차별화 시각 강화 |
| S3 Who Attends | SVP-4 KPI · SVP-5 산업 분포 | SVP-6 퍼널 | 청중 데이터 핵심 |
| S4 What We Offer | — | — | 리스트 표 (SVP 미적용) |
| S5 Sponsor Tiers | SVP-1 Tier 카드 | SVP-7 Tier 차별화 매트릭스 | 5개 Tier 카드 가로 배치 |
| S6 Benefits Matrix | SVP-2 매트릭스 | — | 카테고리 분할 시 SVP-2 × 2~3 슬라이드 |
| S7 ROI Snapshot | SVP-3 ROI 3단 | SVP-4 KPI 임팩트 | 산업 2~3종 ROI |
| S8 Past Sponsors | — | — | 로고 그리드 (SVP 미적용) |
| S9 Contact | — | — | CTA + 담당자 (SVP 미적용) |

---

## 10. 색상 위계 표준 규칙 (sponsor-deck v2.0)

| 요소 | 컬러 사용 |
|------|----------|
| 최상위 강조 (매트릭스 헤더, ROI 상단 배지) | `COLOR_PRIMARY` (Deep Navy) |
| 액센트·CTA·KPI 숫자·차트 메인 시리즈 | `COLOR_ACCENT` (Electric Blue) |
| Tier 식별 막대 (T1~T6) | `TIER_COLORS[tierId]` (Magenta/Electric Blue/Orange/Muted/Border Strong/Neon) |
| ROI 3단 ③ 추정값 배경 | `COLOR_ACCENT_SOFT` (Accent Soft) |
| 매트릭스 슬롯 행 배경 | `COLOR_ACCENT_SOFT` |
| 매트릭스 ✓ 셀 | `COLOR_SUCCESS` (Success) |
| 매트릭스 — 셀 | `COLOR_TEXT_DISABLED` |
| 본문 글자 | `COLOR_TEXT` (Charcoal) |
| 보조 글자 (캡션, 출처) | `COLOR_TEXT_MUTED` |
| 짝수 행·보조 영역 | `COLOR_BG` 또는 `COLOR_SURFACE_ALT` |
| 차트 데이터 시리즈 5색 | `CHART_SERIES` (Electric Blue, Magenta, Orange, Neon, Deep Navy) |

---

## 11. 검증 체크리스트 (전체 패턴 공통)

### 콘텐츠 검증
- [ ] 모든 SVP 패턴에 데이터 출처 캡션 명시 (`audience-profile.md` §2)
- [ ] 추측·과장 표현 0건 (`roi-case-templates.md` §9 절대 회피 룰)
- [ ] 정량화 가능한 모든 숫자가 정량화 (예: "많은" 금지)
- [ ] 회사 종속 표현 0건

### 시각 검증
- [ ] 텍스트 오버플로우 없음
- [ ] 동일 패턴 3장 연속 없음 (변화감)
- [ ] Tier 색상이 `TIER_COLORS` 매핑과 일치
- [ ] HTML/PPTX 모두 폰트가 명시 (FONT_KO/FONT_HEADING/FONT_MONO)

### 코드 품질
- [ ] PPTX hex 컬러 `#` 없음
- [ ] PPTX 옵션 객체 재사용 없음 (호출마다 새 객체)
- [ ] PPTX `bullet: true` 사용 (유니코드 `•` 직접 사용 금지)
- [ ] HTML 외부 의존성 Pretendard CDN 1개만

### v2.0 신규
- [ ] SVP-1~SVP-7 중 행사 유형에 맞는 패턴 선택됨
- [ ] HTML→PPTX 매핑 룰표 §8 준수
- [ ] jc-design-system 토큰 0 하드코딩 (변수 사용 강제)
- [ ] (color_mode=dark_mixed) `dark-mode-patterns.md` 와 함께 사용

---

## 12. 함께 보는 문서

| 파일 | 내용 |
|------|------|
| `dark-mode-patterns.md` | 다크 5종 (DARK-TIER/DARK-MATRIX/DARK-ROI/DARK-KPI/DARK-COVER) |
| `chaining-schema.md` | mice-meeting-minutes → sponsor-deck 입력 스키마 |
| `tier-framework.md` | Tier 5단 + 1트랙 구조 (SVP-1 입력 데이터) |
| `benefit-catalog.md` | 7카테고리 표준 혜택 (SVP-2 입력 데이터) |
| `roi-case-templates.md` | 산업 5종 ROI 템플릿 (SVP-3 입력 데이터) |
| `audience-profile.md` | 청중 데이터 (SVP-4·SVP-5·SVP-6 입력 데이터) |
| `design-tokens-mapping.md` | jc-design-system 토큰 매핑 (전체 SVP 색상 베이스) |
| `output-build-guide.md` | HTML 1차 빌드 + PPTX 변환 워크플로우 |
| `slide-structure.md` | 표준 12~18 슬라이드 콘텐츠 구조 |
