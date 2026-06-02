# 다크 모드 패턴 (v1.0)

이 문서는 다크 배경 슬라이드(섹션 구분, Thank You, 임팩트 강조 슬라이드)에서 사용하는 표·차트·콜아웃·카드의 다크 변형 패턴을 정의한다. `visual-patterns.md`의 라이트 모드 패턴과 1:1 대응한다.

---

## 0. 다크 모드 컬러 매핑

> ✅ R1 정합 완료 — jc-design-system 정본 참조. 다크 모드 토큰값은 `jc-design-system/references/mode-mapping.md §3`(다크 패밀리)·`§3.2`(차트 다크) 정본이며, 본 문서의 `DARK_*` 상수는 그 SoT 미러다. SoT 다크 페이지 배경은 `#0A1220` 패밀리(헤더/표지/로고용 `#0A2540`과 구분).

### 0-1. 색상 변수 (다크 모드)

아래 `DARK_*` 상수는 SoT(`mode-mapping.md §3`)의 다크 토큰을 pptxgenjs용(`#` 없는 6자리)으로 미러한 것이다. 값은 `mode-mapping.md §3` 정본을 따른다.

```javascript
// 다크 모드 컬러 변수 — SoT 미러 (mode-mapping.md §3 정본)
const DARK_BG = "0A1220";              // 다크 페이지 배경 (SoT 미러: --jc-bg 다크 #0A1220)
const DARK_BG_ALT = "152134";          // 카드·시트 배경 (SoT 미러: --jc-surface 다크 #152134)
const DARK_BG_PLACEHOLDER = "1F2C42";  // 이미지 placeholder (SoT 미러: --jc-surface-alt 다크 #1F2C42)
const DARK_SURFACE = "1F2C42";         // 보조 서피스 (SoT 미러: --jc-surface-alt 다크 #1F2C42)

const DARK_TEXT = "E8ECF2";            // 본문 (SoT 미러: --jc-text 다크 #E8ECF2)
const DARK_TEXT_MUTED = "A0A8B4";      // 보조 글자 (SoT 미러: --jc-text-muted 다크 #A0A8B4)
const DARK_TEXT_DISABLED = "5A6270";   // 비활성 (SoT 미러: --jc-text-disabled 다크 #5A6270)

const DARK_BORDER = "2A3650";          // 테두리 (SoT 미러: --jc-border 다크 #2A3650)
const DARK_BORDER_STRONG = "3D4A66";   // 강조 테두리 (SoT 미러: --jc-border-strong 다크 #3D4A66)

const DARK_ACCENT = "5B8DEF";          // 다크 액센트 (SoT 미러: --jc-accent 다크 #5B8DEF)
const DARK_ACCENT_SOFT = "7BA3F2";     // 다크 액센트 호버 (SoT 미러: accent-hover 다크 #7BA3F2)
```

### 0-2. 라이트 → 다크 매핑 표

라이트값은 `signature-tokens.md §6`, 다크값은 `mode-mapping.md §3` 정본 미러.

| 라이트 요소 | 라이트 컬러 (SoT 토큰) | 다크 컬러 (SoT 미러) |
|------------|------------------------|----------------------|
| 페이지 배경 | `#FFFFFF`(`--jc-surface`) / `#F8F9FB`(`--jc-bg`) | `0A1220` (다크 `--jc-bg`) |
| 카드 배경 | `#FFFFFF` (`--jc-surface`) | `152134` (다크 `--jc-surface`) |
| 보조 서피스 | `#F1F3F7` (`--jc-surface-alt`) | `1F2C42` (다크 `--jc-surface-alt`) |
| 짝수행 배경 | `#F1F3F7` (`--jc-surface-alt`) | `1F2C42` (다크 `--jc-surface-alt`) |
| 본문 글자 | `#1A1D24` (`--jc-text`) | `E8ECF2` (다크 `--jc-text`) |
| 보조 글자 | `#5A6270` (`--jc-text-muted`) | `A0A8B4` (다크 `--jc-text-muted`) |
| 테두리 | `#E5E8ED` (`--jc-border`) | `2A3650` (다크 `--jc-border`) |
| 이미지 placeholder | `#E5E8ED` (`--jc-border`) | `1F2C42` (다크 `--jc-surface-alt`) |

### 0-3. 적용 컨텍스트

| 슬라이드 유형 | 다크 모드 사용 여부 |
|--------------|-------------------|
| 표지 (1-1) | ✅ HERO 이미지 + 다크 오버레이 |
| 섹션 구분 (2-1, 3-1, 4-1, 5-1, 6-1, 7-1) | ✅ 풀 다크 배경 |
| 본문 슬라이드 | ❌ 라이트 권장 (가독성) |
| 임팩트 슬라이드 (기대 효과, KPI 일부) | ⚠️ 선택적 — 분량 5장 이내 |
| Thank You (7-5) | ✅ 풀 다크 배경 |

---

## 1. DARK-TBL 패턴 (다크 표)

### 1-1. 다크 표 헬퍼 함수

```javascript
function makeDarkHeaderRow(labels) {
  return labels.map(label => ({
    text: label,
    options: {
      fill: { color: DARK_ACCENT },  // Electric Blue 헤더
      color: "FFFFFF",
      bold: true,
      fontSize: 12,
      align: "center",
      valign: "middle"
    }
  }));
}

function makeDarkBodyRow(values, rowIndex, options = {}) {
  const bgColor = rowIndex % 2 === 0 ? DARK_BG_ALT : DARK_SURFACE;
  return values.map((val, colIdx) => ({
    text: String(val),
    options: {
      fill: { color: bgColor },
      color: DARK_TEXT,
      fontSize: 11,
      align: options.aligns?.[colIdx] || "left",
      valign: "middle",
      margin: [0.05, 0.08, 0.05, 0.08]
    }
  }));
}
```

### 1-2. 사용 예시

```javascript
slide.background = { color: DARK_BG };

const darkHeader = makeDarkHeaderRow(["항목", "Q1", "Q2", "Q3"]);
const darkBody = [
  ["매출", "120M", "145M", "168M"],
  ["행사 건수", "5건", "7건", "9건"],
  ["참가자 수", "850", "1,200", "1,580"]
].map((row, idx) => makeDarkBodyRow(row, idx, { aligns: ["left", "right", "right", "right"] }));

slide.addTable([darkHeader, ...darkBody], {
  x: 0.5, y: 1.5, w: 12.33,
  colW: [3.0, 3.11, 3.11, 3.11],
  border: { pt: 0.5, color: DARK_BORDER }
});
```

---

## 2. DARK-CHART 패턴 (다크 차트)

차트 데이터 시리즈는 다크 배경 가독성을 위해 **다크 보정 시리즈**(`mode-mapping.md §3.2` 정본: `#5B8DEF`, `#F04D85`, `#FF7649`, `#33EE92`, `#C9CFD8`, `#A78BFA`)를 사용한다. 라이트 시리즈는 `signature-tokens.md §1.4` 참조. 배경·라벨·그리드 색상도 다크 변형 적용.

### 2-1. 다크 도넛 차트

```javascript
slide.background = { color: DARK_BG };

slide.addChart(pres.charts.DOUGHNUT, [{
  name: "예산 구성",
  labels: ["기획·운영", "공간·시설", "디자인·제작", "F&B"],
  values: [25, 30, 20, 25]
}], {
  x: 0.5, y: 1.5, w: 6.0, h: 5.0,
  chartColors: ["5B8DEF", "F04D85", "FF7649", "33EE92"],  // 다크 보정 시리즈 (SoT 미러: mode-mapping.md §3.2)
  chartArea: { fill: { color: DARK_BG } },               // 차트 배경 다크
  plotArea: { fill: { color: DARK_BG } },
  showLegend: true,
  legendPos: "r",
  legendFontSize: 11,
  legendColor: DARK_TEXT,                                 // 범례 글자 흰색
  showPercent: true,
  dataLabelColor: "FFFFFF",
  dataLabelFontSize: 10,
  dataLabelFontBold: true,
  holeSize: 60,
  showTitle: false
});
```

### 2-2. 다크 바·컬럼 차트

```javascript
slide.background = { color: DARK_BG };

slide.addChart(pres.charts.BAR, [{
  name: "연간 행사 건수",
  labels: ["2021", "2022", "2023", "2024", "2025"],
  values: [12, 15, 18, 22, 27]
}], {
  x: 0.5, y: 1.5, w: 12.33, h: 5.0,
  barDir: "col",
  chartColors: ["5B8DEF"],  // 다크 보정 data-1 (SoT 미러: mode-mapping.md §3.2)
  chartArea: { fill: { color: DARK_BG } },
  plotArea: { fill: { color: DARK_BG } },
  catAxisLabelColor: DARK_TEXT_MUTED,                    // 카테고리 라벨
  catAxisLabelFontSize: 11,
  valAxisLabelColor: DARK_TEXT_MUTED,                    // 값축 라벨
  valAxisLabelFontSize: 10,
  valGridLine: { color: DARK_BORDER, size: 0.5 },        // 그리드선 어둡게
  catGridLine: { style: "none" },
  showValue: true,
  dataLabelPosition: "outEnd",
  dataLabelColor: DARK_TEXT,                              // 값 라벨 흰색
  dataLabelFontSize: 11,
  dataLabelFontBold: true,
  showLegend: false
});
```

---

## 3. DARK-C3 패턴 (다크 빅넘버 콜아웃)

```javascript
slide.background = { color: DARK_BG };

function addDarkBigNumberCallout(slide, opts) {
  const { x, y, w, h, value, unit, label } = opts;

  // 숫자 자동 천단위 콤마 (v1.1 패치)
  const valueStr = typeof value === "number"
    ? value.toLocaleString("ko-KR")
    : String(value);

  // 큰 숫자 — Electric Blue 또는 Neon Green으로 강조
  slide.addText(valueStr, {
    x, y, w, h: h * 0.55,
    fontSize: 72, bold: true, color: DARK_ACCENT,
    fontFace: "Arial Black",
    align: "center", valign: "bottom", margin: 0
  });

  // 단위
  if (unit) {
    slide.addText(unit, {
      x, y: y + h * 0.55, w, h: 0.3,
      fontSize: 22, color: "FFFFFF", bold: true,
      align: "center", valign: "top", margin: 0
    });
  }

  // 설명
  slide.addText(label, {
    x, y: y + h * 0.55 + 0.3, w, h: h * 0.3 - 0.3,
    fontSize: 13, color: DARK_TEXT_MUTED,
    align: "center", valign: "top", margin: 0
  });
}

// 사용 예시: 기대 효과 슬라이드 (다크 임팩트 버전)
const items = [
  { value: 1200, unit: "명+", label: "예상 참가자" },
  { value: 95, unit: "%", label: "재참여 의향" },
  { value: 28, unit: "억 원", label: "경제 파급효과" }
];

const w = 3.8, h = 3.0;
const startX = (13.33 - (w * 3 + 0.5 * 2)) / 2;
items.forEach((item, idx) => {
  addDarkBigNumberCallout(slide, {
    x: startX + idx * (w + 0.5),
    y: 2.5, w, h,
    value: item.value, unit: item.unit, label: item.label
  });
});
```

---

## 4. DARK-D4 패턴 (다크 카드 그리드)

```javascript
slide.background = { color: DARK_BG };

const d4Cards = [
  { title: "기획력", desc: "18년 MICE 경력 기반\n핵심 컨셉 설계" },
  { title: "운영력", desc: "연간 25건+ 행사\n위기 대응 매뉴얼" },
  { title: "네트워크", desc: "베뉴·연사·F&B\n협력사 200+" },
  { title: "기술력", desc: "리멤버 DB 활용\n타겟 모객 시스템" }
];

const cardW = 5.5, cardH = 2.5;
const gapX = 0.3, gapY = 0.3;
const startX = (13.33 - (cardW * 2 + gapX)) / 2;
const startY = 1.8;

d4Cards.forEach((card, idx) => {
  const col = idx % 2;
  const row = Math.floor(idx / 2);
  const x = startX + col * (cardW + gapX);
  const y = startY + row * (cardH + gapY);

  // 다크 카드 배경
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w: cardW, h: cardH,
    fill: { color: DARK_BG_ALT },
    line: { color: DARK_BORDER, width: 0.5 }
  });

  // 좌측 Accent 보더 (Electric Blue)
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.08, h: cardH,
    fill: { color: DARK_ACCENT },
    line: { type: "none" }
  });

  // 제목 (Electric Blue 또는 흰색)
  slide.addText(card.title, {
    x: x + 0.3, y: y + 0.3, w: cardW - 0.6, h: 0.6,
    fontSize: 20, bold: true, color: "FFFFFF",
    align: "left", valign: "middle", margin: 0
  });

  // 본문
  slide.addText(card.desc, {
    x: x + 0.3, y: y + 1.0, w: cardW - 0.6, h: cardH - 1.2,
    fontSize: 12, color: DARK_TEXT_MUTED,
    align: "left", valign: "top", margin: 0
  });
});
```

---

## 5. DARK-IMG 패턴 (다크 이미지 placeholder)

```javascript
function addDarkImagePlaceholder(slide, opts) {
  const { x, y, w, h, caption, shape = "rect" } = opts;
  const shapeType = shape === "circle" ? pres.shapes.OVAL : pres.shapes.RECTANGLE;

  slide.addShape(shapeType, {
    x, y, w, h,
    fill: { color: DARK_BG_PLACEHOLDER },
    line: { color: DARK_BORDER_STRONG, width: 1, dashType: "dash" }
  });

  slide.addText("+", {
    x, y, w, h,
    fontSize: Math.min(w, h) * 24,
    color: DARK_TEXT_MUTED,
    bold: true,
    align: "center", valign: "middle", margin: 0
  });

  slide.addText(caption || "[이미지]", {
    x, y: y + h - 0.35, w, h: 0.3,
    fontSize: 10, fontFace: "Calibri",
    color: DARK_TEXT_MUTED,
    align: "center", valign: "middle", margin: 0
  });
}
```

---

## 6. 다크 모드 사용 체크리스트

- [ ] 슬라이드 배경 `slide.background = { color: DARK_BG }` 적용
- [ ] 모든 글자 색이 흰색 또는 `DARK_TEXT_MUTED` (회색은 금지 — 가독성 저하)
- [ ] 차트의 `chartArea.fill`, `plotArea.fill` 모두 다크 배경
- [ ] 차트 라벨·범례 색상이 다크 모드 토큰 사용
- [ ] 그리드선이 `DARK_BORDER` 컬러로 미세하게 보임
- [ ] 이미지 placeholder가 `DARK_BG_PLACEHOLDER` 배경
- [ ] 카드 좌측 보더가 Accent 컬러 (Electric Blue)로 식별성 확보
- [ ] 다크 모드 슬라이드가 전체 분량의 30% 이내 (가독성 보호)
