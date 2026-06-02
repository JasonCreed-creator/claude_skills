# 인포그래픽 패턴 (v1.0)

이 문서는 MICE 제안서에서 사용하는 인포그래픽 패턴 3종(퍼널·매트릭스·레이더)을 정의한다. `visual-patterns.md`의 차트·다이어그램 패턴과 보완 관계다.

---

## 0. 적용 컨텍스트

| 패턴 코드 | 용도 | 추천 적용 슬라이드 |
|----------|------|------------------|
| **INFO-I1** | 퍼널 (Funnel) | 참가자 모객 깔때기, 전환율 흐름, 영업 파이프라인 |
| **INFO-I2** | 매트릭스 (2×2) | 경쟁 포지셔닝, BCG 매트릭스, 우선순위 매트릭스, SWOT |
| **INFO-I3** | 레이더 (Radar) | 역량 비교, 평가 기준 비교, 다차원 KPI |

slide-structure.md 기존 슬라이드 중 다음 위치에 적용 권장:
- **슬라이드 2-4 행사 포지셔닝** → `INFO-I2` (매트릭스)
- **슬라이드 3-10 참가자 관리** → `INFO-I1` (퍼널, 모객 단계별 전환율)
- **슬라이드 6-3 핵심 역량** → `INFO-I3` (레이더, 경쟁사 대비 역량)

---

## 1. INFO-I1 — 퍼널 (Funnel)

### 1-1. 사양

| 항목 | 값 |
|------|-----|
| 용도 | 모객 깔때기, 전환율 시각화 |
| 형태 | 사다리꼴 N개를 위에서 아래로 점진적으로 좁아지게 적층 |
| 색상 위계 | 상단 Accent(가장 밝게) → 하단 Primary(가장 진하게), 또는 단일 컬러 채도 변화 |

### 1-2. pptxgenjs 코드

pptxgenjs에는 사다리꼴(`TRAPEZOID`) 도형이 있지만 회전이 까다로워, **수직 좌우 양쪽으로 좁아지는 사각형 N개**로 구현한다.

```javascript
/**
 * 퍼널 인포그래픽을 그린다.
 * @param {Slide} slide
 * @param {object} opts - { x, y, w, h, stages, colors }
 *   stages: [{ label, value, rate }, ...] — rate는 0~1 (해당 단계 너비 비율)
 *   colors: 단계별 색상 배열 (없으면 Accent → Primary 그라데이션 자동 생성)
 */
function addFunnel(slide, opts) {
  const { x, y, w, h, stages, colors } = opts;
  const stageH = h / stages.length;
  const defaultColors = ["#5B9BD5", "#2962FF", "#1E4DCC", "#0A2540"];

  stages.forEach((stage, idx) => {
    const stageW = w * stage.rate;
    const stageX = x + (w - stageW) / 2;
    const stageY = y + idx * stageH;
    const color = (colors && colors[idx]) || defaultColors[idx % defaultColors.length];

    // 사다리꼴 효과: 사각형으로 단순화 (각 단계가 점점 좁아짐)
    slide.addShape(pres.shapes.RECTANGLE, {
      x: stageX, y: stageY, w: stageW, h: stageH * 0.85,
      fill: { color: color.replace("#", "") },
      line: { color: "FFFFFF", width: 2 }
    });

    // 단계 라벨 (사각형 내부)
    slide.addText([
      { text: stage.label, options: { bold: true, fontSize: 14, breakLine: true } },
      { text: String(stage.value), options: { fontSize: 18, bold: true } }
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
        x: x + w + 0.2, y: stageY + stageH * 0.4,
        w: 1.5, h: 0.4,
        fontSize: 12, color: "5A6270", bold: true,
        align: "left", valign: "middle", margin: 0
      });
    }
  });
}

// 사용 예시: 참가자 모객 퍼널
const funnelStages = [
  { label: "리멤버 DB 노출", value: 50000, rate: 1.0 },
  { label: "이메일 오픈", value: 12500, rate: 0.7 },
  { label: "랜딩페이지 방문", value: 3000, rate: 0.45 },
  { label: "등록 완료", value: 800, rate: 0.25 },
  { label: "현장 참석", value: 612, rate: 0.18 }
];

addFunnel(slide, {
  x: 2.5, y: 1.0, w: 7.0, h: 5.5,
  stages: funnelStages
});

// 우측 보조 메트릭 (KPI 콜아웃)
slide.addText("최종 전환율", {
  x: 10.5, y: 2.5, w: 2.5, h: 0.5,
  fontSize: 14, color: "5A6270", align: "left", margin: 0
});
slide.addText("1.22%", {
  x: 10.5, y: 3.0, w: 2.5, h: 1.0,
  fontSize: 48, bold: true, color: "#2962FF",
  fontFace: "Arial Black",
  align: "left", valign: "top", margin: 0
});
slide.addText("업계 평균 0.8% 대비\n+52% 높은 전환", {
  x: 10.5, y: 4.2, w: 2.5, h: 1.0,
  fontSize: 11, color: "1A1D24",
  align: "left", valign: "top", margin: 0
});
```

---

## 2. INFO-I2 — 매트릭스 (2×2)

### 2-1. 사양

| 항목 | 값 |
|------|-----|
| 용도 | 경쟁 포지셔닝, 우선순위 매트릭스, BCG, SWOT |
| 형태 | X·Y축 + 4사분면 + 점(또는 라벨) 플로팅 |
| 4사분면 컬러 | 옅은 4색 (각 사분면 의미별) 또는 단일 옅은 배경 |

### 2-2. pptxgenjs 코드

```javascript
/**
 * 2x2 매트릭스를 그린다.
 * @param {object} opts - { x, y, w, h, xLabel, yLabel, quadrants, dots }
 *   quadrants: [Q1, Q2, Q3, Q4] — 4사분면 라벨 ([우상, 좌상, 좌하, 우하] 순)
 *   dots: [{ name, x, y, color, isOurs }] — x, y는 0~1 비율
 */
function addMatrix(slide, opts) {
  const { x, y, w, h, xLabel, yLabel, quadrants, dots } = opts;
  const halfW = w / 2;
  const halfH = h / 2;

  // 4사분면 배경 (옅은 색)
  const quadColors = [
    "#E8EFFF",  // Q1 (우상): 액센트 옅게 (이상적 영역)
    "#F1F3F7",  // Q2 (좌상)
    "#F8F9FB",  // Q3 (좌하)
    "#FFF3E0"   // Q4 (우하): 옅은 오렌지
  ];

  // 우상 (Q1)
  slide.addShape(pres.shapes.RECTANGLE, {
    x: x + halfW, y, w: halfW, h: halfH,
    fill: { color: quadColors[0].replace("#", "") },
    line: { type: "none" }
  });
  // 좌상 (Q2)
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w: halfW, h: halfH,
    fill: { color: quadColors[1].replace("#", "") },
    line: { type: "none" }
  });
  // 좌하 (Q3)
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y: y + halfH, w: halfW, h: halfH,
    fill: { color: quadColors[2].replace("#", "") },
    line: { type: "none" }
  });
  // 우하 (Q4)
  slide.addShape(pres.shapes.RECTANGLE, {
    x: x + halfW, y: y + halfH, w: halfW, h: halfH,
    fill: { color: quadColors[3].replace("#", "") },
    line: { type: "none" }
  });

  // 사분면 라벨 — 코너에서 안쪽으로 이동 (축 라벨과 겹치지 않게)
  // v1.1 패치: y를 +0.3 내려서 Y축 라벨과 충돌 방지
  if (quadrants) {
    const corners = [
      { x: x + halfW + 0.3, y: y + 0.5, text: quadrants[0], align: "left" },
      { x: x + 0.3, y: y + 0.5, text: quadrants[1], align: "left" },
      { x: x + 0.3, y: y + halfH + 0.2, text: quadrants[2], align: "left" },
      { x: x + halfW + 0.3, y: y + halfH + 0.2, text: quadrants[3], align: "left" }
    ];
    corners.forEach(c => {
      slide.addText(c.text, {
        x: c.x, y: c.y, w: halfW - 0.5, h: 0.4,
        fontSize: 11, italic: true, color: "5A6270",
        align: c.align, valign: "top", margin: 0
      });
    });
  }

  // X축
  slide.addShape(pres.shapes.LINE, {
    x, y: y + halfH, w, h: 0,
    line: { color: "5A6270", width: 1.5, endArrowType: "triangle" }
  });
  // Y축
  slide.addShape(pres.shapes.LINE, {
    x: x + halfW, y: y + h, w: 0, h: -h,
    line: { color: "5A6270", width: 1.5, endArrowType: "triangle" }
  });

  // 축 라벨 — v1.1 패치: 매트릭스 바깥에 배치하여 사분면 라벨과 충돌 회피
  if (xLabel) {
    slide.addText(xLabel, {
      x: x + w + 0.1, y: y + halfH - 0.2, w: 1.2, h: 0.4,
      fontSize: 12, bold: true, color: "1A1D24",
      align: "left", valign: "middle", margin: 0
    });
  }
  if (yLabel) {
    slide.addText(yLabel, {
      x: x + halfW - 0.6, y: y - 0.5, w: 1.5, h: 0.4,
      fontSize: 12, bold: true, color: "1A1D24",
      align: "center", valign: "middle", margin: 0
    });
  }

  // 데이터 점(dot) 플로팅
  if (dots) {
    dots.forEach(dot => {
      const dotX = x + dot.x * w;
      const dotY = y + (1 - dot.y) * h;  // y축은 위쪽이 1
      const dotSize = dot.isOurs ? 0.4 : 0.3;
      const dotColor = (dot.color || (dot.isOurs ? "#2962FF" : "#5A6270")).replace("#", "");

      slide.addShape(pres.shapes.OVAL, {
        x: dotX - dotSize / 2, y: dotY - dotSize / 2,
        w: dotSize, h: dotSize,
        fill: { color: dotColor },
        line: { color: "FFFFFF", width: 2 }
      });

      // 라벨
      slide.addText(dot.name, {
        x: dotX + dotSize / 2 + 0.05, y: dotY - 0.15,
        w: 1.5, h: 0.3,
        fontSize: 10, bold: dot.isOurs, color: "1A1D24",
        align: "left", valign: "middle", margin: 0
      });
    });
  }
}

// 사용 예시: 경쟁 포지셔닝 매트릭스
// 주의 (v1.1): yLabel이 매트릭스 위쪽 바깥에 배치되므로, y 시작 좌표에 0.5" 여유 필요
addMatrix(slide, {
  x: 2.5, y: 1.3, w: 8.0, h: 5.7,  // y를 1.0이 아닌 1.3으로 시작
  xLabel: "규모 →",
  yLabel: "↑ 전문성",
  quadrants: ["프리미엄 리더", "니치 전문가", "범용 저가", "대량 표준화"],
  dots: [
    { name: "본 행사", x: 0.7, y: 0.85, isOurs: true, color: "#2962FF" },
    { name: "경쟁사 A", x: 0.85, y: 0.45, color: "#5A6270" },
    { name: "경쟁사 B", x: 0.3, y: 0.6, color: "#5A6270" },
    { name: "경쟁사 C", x: 0.5, y: 0.25, color: "#5A6270" }
  ]
});
```

> **v1.1 패치 (2026-05-25)**: 검증 결과 사분면 라벨이 축 라벨과 겹치는 결함 발견. 수정 내용:
> - 사분면 라벨 위치를 코너에서 0.5" 안쪽으로 이동 (Y축 라벨과 충돌 방지)
> - X축 라벨 `xLabel`을 매트릭스 우측 바깥에 배치 (`x + w + 0.1`)
> - Y축 라벨 `yLabel`을 매트릭스 상단 바깥에 배치 (`y - 0.5`)
> - 사용 시 매트릭스 y 시작 좌표에 0.5" 여유 필수

---

## 3. INFO-I3 — 레이더 차트 (Radar)

### 3-1. 사양

| 항목 | 값 |
|------|-----|
| 용도 | 역량 비교, 평가 기준 다차원 시각화 |
| 라이브러리 타입 | `pres.charts.RADAR` |
| 색상 규칙 | 본 행사 = Accent, 비교 대상 = 회색 또는 Point 컬러 |

### 3-2. pptxgenjs 코드

pptxgenjs는 RADAR 차트를 네이티브 지원한다.

```javascript
// INFO-I3: 레이더 차트 (역량 비교)
const radarData = [
  {
    name: "본 행사 (M&C)",
    labels: ["기획력", "운영력", "네트워크", "기술력", "디자인", "사후관리"],
    values: [9, 9, 8, 7, 8, 9]
  },
  {
    name: "경쟁사 평균",
    labels: ["기획력", "운영력", "네트워크", "기술력", "디자인", "사후관리"],
    values: [7, 7, 6, 6, 7, 5]
  }
];

slide.addChart(pres.charts.RADAR, radarData, {
  x: 0.5, y: 1.0, w: 7.5, h: 6.0,
  radarStyle: "standard",  // "standard" | "marker" | "filled"
  chartColors: ["2962FF", "94A3B8"],  // 본 행사 = Electric Blue, 경쟁 = 회색
  chartArea: { fill: { color: "FFFFFF" } },
  catAxisLabelColor: "1A1D24",
  catAxisLabelFontSize: 12,
  catAxisLabelFontBold: true,
  valAxisLabelColor: "5A6270",
  valAxisLabelFontSize: 9,
  valAxisMaxVal: 10,
  valAxisMinVal: 0,
  showLegend: true,
  legendPos: "b",
  legendFontSize: 11,
  legendColor: "1A1D24",
  showTitle: false
});

// 우측 보조 텍스트 (해석)
slide.addText("종합 우위 영역", {
  x: 8.5, y: 1.5, w: 4.3, h: 0.5,
  fontSize: 16, bold: true, color: "#0A2540",
  align: "left", margin: 0
});

const insights = [
  "✓ 사후관리: 경쟁사 대비 +4점 (가장 큰 격차)",
  "✓ 기획력·운영력: 9점으로 동급 최고 수준",
  "✓ 네트워크: 협력사 200+ 보유 강점",
  "△ 기술력·디자인: 보완 영역 (외부 협력 강화)"
];

slide.addText(insights.join("\n\n"), {
  x: 8.5, y: 2.2, w: 4.3, h: 4.0,
  fontSize: 12, color: "1A1D24",
  align: "left", valign: "top", margin: 0,
  paraSpaceAfter: 6
});
```

---

## 4. 인포그래픽 패턴 사용 체크리스트

- [ ] INFO-I1 퍼널: 각 단계의 너비 비율(`rate`)이 시각적으로 의미 있게 좁아지는지 확인 (인접 단계 차이 최소 10%)
- [ ] INFO-I1 퍼널: 우측 전환율 화살표 라벨이 자동 계산 (`nextRate = next.value / current.value`)
- [ ] INFO-I2 매트릭스: "본 행사" 점이 가장 이상적 사분면(통상 우상단)에 위치
- [ ] INFO-I2 매트릭스: 점 라벨이 다른 점과 겹치지 않음
- [ ] INFO-I2 매트릭스: 사분면 의미 라벨이 코너에 옅게 배치
- [ ] INFO-I3 레이더: 본 행사 시리즈가 첫 번째 (chartColors 첫 색상)
- [ ] INFO-I3 레이더: 축 라벨이 6~8개 (너무 많으면 가독성 저하)
- [ ] INFO-I3 레이더: `valAxisMaxVal` 명시 (자동 스케일 방지)
- [ ] 모든 인포그래픽 옆에 해석 텍스트 (인사이트) 함께 배치

---

## 5. 다크 모드 적용 시 주의

인포그래픽을 다크 모드 슬라이드에 적용하는 경우:

- **INFO-I1 퍼널**: 배경이 다크일 때 사다리꼴 컬러를 채도 -20% 적용 (가독성)
- **INFO-I2 매트릭스**: 사분면 배경색을 `DARK_BG_ALT`, `DARK_SURFACE` 위주로 미세하게 차이 두기
- **INFO-I3 레이더**: `chartArea.fill`, `plotArea.fill` 모두 `DARK_BG`. 축 라벨 `DARK_TEXT`, 그리드 `DARK_BORDER`

`dark-mode-patterns.md`의 컬러 변수를 사용하면 자동 적용된다.
