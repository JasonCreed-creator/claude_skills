# 아이콘 라이브러리 (v1.0)

이 문서는 MICE 제안서에서 사용하는 아이콘 라이브러리(react-icons) 활용 패턴을 정의한다. 텍스트 "+" 대신 실제 아이콘을 적용하면 비주얼 완성도가 크게 향상된다.

---

## 0. 설치 및 기본 사용법

### 0-1. 의존성 설치

```bash
npm install -g react-icons react react-dom sharp
```

### 0-2. 공통 헬퍼 함수 (필수)

`visual-patterns.md`의 컬러 변수와 함께 사용한다.

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");

/**
 * react-icons 컴포넌트를 SVG 문자열로 변환
 */
function renderIconSvg(IconComponent, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

/**
 * 아이콘을 base64 PNG로 변환 (pptxgenjs addImage에 직접 사용 가능)
 * @param {Component} IconComponent - react-icons 컴포넌트
 * @param {string} color - hex 컬러 (# 포함, 예: "#2962FF")
 * @param {number} size - 래스터화 해상도 (256 권장)
 */
async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

/**
 * 슬라이드에 아이콘을 추가하는 헬퍼 (원형 배경 옵션)
 */
async function addIcon(slide, opts) {
  const { IconComponent, x, y, size = 0.5, color = "#FFFFFF", bgColor = null, bgShape = "circle" } = opts;

  // 배경 (원형 또는 사각 — 선택적)
  if (bgColor) {
    const bgSize = size * 1.8;
    const bgX = x - (bgSize - size) / 2;
    const bgY = y - (bgSize - size) / 2;
    const shapeType = bgShape === "circle" ? pres.shapes.OVAL : pres.shapes.ROUNDED_RECTANGLE;

    slide.addShape(shapeType, {
      x: bgX, y: bgY, w: bgSize, h: bgSize,
      fill: { color: bgColor },
      line: { type: "none" },
      ...(bgShape === "rect" ? { rectRadius: 0.06 } : {})
    });
  }

  const iconData = await iconToBase64Png(IconComponent, color, 256);
  slide.addImage({
    data: iconData,
    x, y, w: size, h: size
  });
}
```

---

## 1. 아이콘 세트 (react-icons 라이브러리)

react-icons는 여러 세트를 제공한다. 본 스킬은 **Heroicons(`hi`)** 와 **Font Awesome(`fa`)** 두 세트를 표준으로 사용한다.

### 1-1. 표준 세트

```javascript
// Heroicons 2 (HI2) — 모던하고 깔끔. 일관성 있는 라인 스타일
const {
  HiOutlineUsers, HiOutlineCalendar, HiOutlineLocation,
  HiOutlineClock, HiOutlineCurrencyDollar, HiOutlineChartBar,
  HiOutlineLightBulb, HiOutlineShieldCheck, HiOutlineCog,
  HiOutlinePresentationChartLine, HiOutlineGlobe, HiOutlineSparkles
} = require("react-icons/hi");

// Font Awesome 5 (FA) — MICE 업계 특화 아이콘 풍부
const {
  FaMicrophone, FaTrophy, FaHandshake, FaPalette,
  FaCameraRetro, FaUserTie, FaBuilding, FaBullseye,
  FaRocket, FaCheckCircle, FaStar, FaQuoteRight
} = require("react-icons/fa");
```

---

## 2. 슬라이드 유형별 아이콘 매핑

| 슬라이드 | 컨텍스트 | 추천 아이콘 | 임포트 |
|---------|---------|------------|--------|
| **2-2 행사 목적** | 비전·미션 카드 | `FaBullseye`, `FaRocket`, `HiOutlineLightBulb`, `HiOutlineSparkles` | `react-icons/fa`, `hi` |
| **2-3 핵심 컨셉** | 키워드 3개 | `HiOutlineSparkles`, `FaStar`, `HiOutlineGlobe` | |
| **2-5 기대 효과** | KPI 빅넘버 옆 | `HiOutlineUsers`(참가자), `HiOutlineChartBar`(매출), `FaTrophy`(성과) | |
| **3-2 운영 체계도** | 조직 박스 | (텍스트 위주, 아이콘 불필요) | |
| **3-8 프로그램 구성** | 카드별 | `FaMicrophone`(연사), `FaHandshake`(네트워킹), `HiOutlinePresentationChartLine`(세션), `FaCameraRetro`(포토) | |
| **3-10 참가자 관리** | 프로세스 단계 | `HiOutlineCalendar`(등록), `HiOutlineLocation`(현장), `FaCheckCircle`(입장), `FaQuoteRight`(설문) | |
| **3-11 안전 대응** | 카드 | `HiOutlineShieldCheck`(보안), `FaUserTie`(인력), `HiOutlineClock`(대응시간) | |
| **4-4 연출 포인트** | 카드 | `FaPalette`(디자인), `HiOutlineSparkles`(특수효과) | |
| **5-2 KPI 대시보드** | 콜아웃 옆 | `HiOutlineUsers`, `HiOutlineChartBar`, `HiOutlineCurrencyDollar` | |
| **6-2 회사 개요** | 핵심 수치 | `HiOutlineCalendar`(설립), `FaTrophy`(실적), `HiOutlineUsers`(누적 참가자) | |
| **6-3 핵심 역량** | 4개 카드 | `HiOutlineLightBulb`(기획), `HiOutlineCog`(운영), `FaHandshake`(네트워크), `HiOutlineSparkles`(기술) | |
| **7-1 섹션 구분** (예산) | 상단 강조 | `HiOutlineCurrencyDollar` | |

---

## 3. 패턴별 아이콘 적용 예시

### 3-1. 빅넘버 콜아웃 + 아이콘 (CHART-C3 강화)

```javascript
async function addBigNumberCalloutWithIcon(slide, opts) {
  const { x, y, w, h, value, unit, label, IconComponent, iconColor = "#2962FF" } = opts;

  // 아이콘 (상단 중앙, 원형 배경)
  const iconSize = 0.7;
  const iconX = x + (w - iconSize) / 2;
  await addIcon(slide, {
    IconComponent,
    x: iconX, y, size: iconSize,
    color: "#FFFFFF",
    bgColor: iconColor, bgShape: "circle"
  });

  // 큰 숫자
  slide.addText(String(value), {
    x, y: y + 1.2, w, h: h * 0.4,
    fontSize: 56, bold: true, color: iconColor,
    fontFace: "Arial Black",
    align: "center", valign: "bottom", margin: 0
  });

  // 단위
  if (unit) {
    slide.addText(unit, {
      x, y: y + 1.2 + h * 0.4, w, h: 0.3,
      fontSize: 18, color: COLOR_TEXT, bold: true,
      align: "center", valign: "top", margin: 0
    });
  }

  // 설명
  slide.addText(label, {
    x, y: y + 1.2 + h * 0.4 + 0.3, w, h: 0.5,
    fontSize: 12, color: COLOR_TEXT_MUTED,
    align: "center", valign: "top", margin: 0
  });
}

// 사용
const { HiOutlineUsers, HiOutlineChartBar, HiOutlineCurrencyDollar } = require("react-icons/hi");

const items = [
  { value: 612, unit: "명", label: "예상 참가자", icon: HiOutlineUsers },
  { value: 93, unit: "%", label: "만족도 목표", icon: HiOutlineChartBar },
  { value: 67, unit: "건", label: "미디어 노출", icon: HiOutlineCurrencyDollar }
];

const w = 3.5, h = 4.0;
const startX = (13.33 - (w * 3 + 0.5 * 2)) / 2;

for (let i = 0; i < items.length; i++) {
  await addBigNumberCalloutWithIcon(slide, {
    x: startX + i * (w + 0.5),
    y: 2.0, w, h,
    value: items[i].value,
    unit: items[i].unit,
    label: items[i].label,
    IconComponent: items[i].icon,
    iconColor: "#2962FF"
  });
}
```

### 3-2. 카드 그리드 + 아이콘 (DIAG-D4 강화)

```javascript
async function addIconCard(slide, opts) {
  const { x, y, w, h, IconComponent, title, desc, accentColor = "#2962FF" } = opts;

  // 카드 배경
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: "FFFFFF" },
    line: { color: "E5E7EB", width: 0.5 },
    shadow: { type: "outer", color: "000000", opacity: 0.08, blur: 4, offset: 1, angle: 135 }
  });

  // 좌측 Accent 보더
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.08, h,
    fill: { color: accentColor },
    line: { type: "none" }
  });

  // 아이콘 (좌측 상단, 원형 배경)
  await addIcon(slide, {
    IconComponent,
    x: x + 0.4, y: y + 0.3,
    size: 0.5, color: "#FFFFFF",
    bgColor: accentColor, bgShape: "circle"
  });

  // 제목
  slide.addText(title, {
    x: x + 1.5, y: y + 0.3, w: w - 1.8, h: 0.7,
    fontSize: 18, bold: true, color: accentColor,
    align: "left", valign: "middle", margin: 0
  });

  // 본문
  slide.addText(desc, {
    x: x + 0.4, y: y + 1.2, w: w - 0.6, h: h - 1.4,
    fontSize: 12, color: COLOR_TEXT,
    align: "left", valign: "top", margin: 0
  });
}

// 사용
const { HiOutlineLightBulb, HiOutlineCog, HiOutlineSparkles } = require("react-icons/hi");
const { FaHandshake } = require("react-icons/fa");

const cards = [
  { icon: HiOutlineLightBulb, title: "기획력", desc: "18년 MICE 경력 기반\n핵심 컨셉 설계" },
  { icon: HiOutlineCog, title: "운영력", desc: "연간 25건+ 행사\n위기 대응 매뉴얼" },
  { icon: FaHandshake, title: "네트워크", desc: "베뉴·연사·F&B\n협력사 200+" },
  { icon: HiOutlineSparkles, title: "기술력", desc: "리멤버 DB 활용\n타겟 모객 시스템" }
];

const cardW = 5.5, cardH = 2.5;
const gapX = 0.3, gapY = 0.3;
const startX = (13.33 - (cardW * 2 + gapX)) / 2;

for (let i = 0; i < cards.length; i++) {
  const col = i % 2;
  const row = Math.floor(i / 2);
  await addIconCard(slide, {
    x: startX + col * (cardW + gapX),
    y: 1.5 + row * (cardH + gapY),
    w: cardW, h: cardH,
    IconComponent: cards[i].icon,
    title: cards[i].title,
    desc: cards[i].desc,
    accentColor: "#2962FF"
  });
}
```

### 3-3. 프로세스 플로우 + 아이콘 (DIAG-D2 강화)

```javascript
const { HiOutlineCalendar, HiOutlineLocation, HiOutlineCheckCircle, 
        HiOutlineSparkles, HiOutlineChatBubbleLeft, HiOutlineEnvelope } = require("react-icons/hi");

const steps = [
  { icon: HiOutlineCalendar, title: "사전등록", desc: "온라인" },
  { icon: HiOutlineLocation, title: "현장등록", desc: "QR 인증" },
  { icon: HiOutlineCheckCircle, title: "입장", desc: "네임택" },
  { icon: HiOutlineSparkles, title: "참관", desc: "세션 참여" },
  { icon: HiOutlineChatBubbleLeft, title: "설문", desc: "디지털" },
  { icon: HiOutlineEnvelope, title: "사후관리", desc: "CRM" }
];

const stepW = 1.8, stepH = 1.6;
const gap = 0.3;
const totalW = stepW * 6 + gap * 5;
const startX = (13.33 - totalW) / 2;
const stepY = 3.0;

for (let i = 0; i < steps.length; i++) {
  const x = startX + i * (stepW + gap);

  // 박스 배경
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y: stepY, w: stepW, h: stepH,
    fill: { color: "FFFFFF" },
    line: { color: "#2962FF", width: 1 },
    rectRadius: 0.08
  });

  // 아이콘 (상단 중앙)
  await addIcon(slide, {
    IconComponent: steps[i].icon,
    x: x + (stepW - 0.55) / 2,
    y: stepY + 0.2,
    size: 0.55, color: "#2962FF"
  });

  // 제목 + 설명
  slide.addText([
    { text: steps[i].title, options: { bold: true, fontSize: 13, breakLine: true } },
    { text: steps[i].desc, options: { fontSize: 10, color: "5A6270" } }
  ], {
    x, y: stepY + 0.9, w: stepW, h: 0.6,
    color: "#1A1D24",
    align: "center", valign: "middle", margin: 0
  });

  // 화살표 (마지막 제외)
  if (i < steps.length - 1) {
    slide.addShape(pres.shapes.LINE, {
      x: x + stepW + 0.05, y: stepY + stepH / 2, w: gap - 0.1, h: 0,
      line: { color: "94A3B8", width: 2, endArrowType: "triangle" }
    });
  }
}
```

---

## 4. 폴백 정책 (아이콘 미사용 시)

react-icons + sharp 의존성이 없는 환경에서는 텍스트 또는 도형으로 폴백한다:

```javascript
async function safeAddIcon(slide, opts) {
  try {
    await addIcon(slide, opts);
  } catch (e) {
    // 폴백 1: 원형 배경 + 첫 글자
    const { x, y, size = 0.5, color = "#FFFFFF", bgColor = "#2962FF", fallbackChar = "•" } = opts;
    slide.addShape(pres.shapes.OVAL, {
      x, y, w: size, h: size,
      fill: { color: bgColor },
      line: { type: "none" }
    });
    slide.addText(fallbackChar, {
      x, y, w: size, h: size,
      fontSize: size * 36, bold: true, color,
      align: "center", valign: "middle", margin: 0
    });
  }
}
```

---

## 5. 아이콘 사용 가이드라인

### 5-1. 일관성 원칙
- 한 슬라이드 내에서는 **하나의 아이콘 세트만 사용** (Heroicons 또는 Font Awesome — 혼용 금지)
- 한 제안서 전체에서 메인 아이콘 세트 1개 + 보조 1개 이내
- 아이콘 컬러는 jc-design-system 데이터 시리즈 또는 Primary/Accent에서 선택

### 5-2. 사이즈 표준
| 컨텍스트 | 권장 사이즈 (인치) |
|---------|------------------|
| 카드 좌측 상단 아이콘 (배경 원형) | 0.5 |
| 빅넘버 콜아웃 상단 아이콘 (배경 원형) | 0.7 |
| 프로세스 플로우 박스 내부 | 0.55 |
| 다이어그램 노드 라벨 옆 | 0.35 |
| 본문 인라인 강조 | 0.25 |

### 5-3. 컬러 사용 규칙
- **단색 아이콘 우선** — Filled 스타일보다 Outline 스타일이 모던
- 원형 배경 사용 시 — 배경 = Accent, 아이콘 = 흰색
- 배경 없이 사용 시 — 아이콘 = Accent 또는 Primary

---

## 6. 검증 체크리스트

- [ ] react-icons + sharp 의존성 설치 확인 (`npm list -g | grep -E "react-icons|sharp"`)
- [ ] 아이콘 사이즈 파라미터(`size: 256`)가 표시 사이즈가 아닌 래스터화 해상도임을 확인
- [ ] 한 슬라이드 내 아이콘 세트 혼용 없음 (Heroicons OR Font Awesome)
- [ ] 아이콘 컬러가 jc-design-system 토큰 기반
- [ ] 폴백 처리(safeAddIcon)가 의존성 없는 환경에서 동작
- [ ] async/await 처리 누락 없음 (아이콘 렌더링은 비동기)
