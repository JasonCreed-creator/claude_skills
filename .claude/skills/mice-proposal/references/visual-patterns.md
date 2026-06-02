# 비주얼 패턴 라이브러리 (v1.1)

이 문서는 MICE 제안서 PPTX 생성에 사용하는 표준 비주얼 패턴 라이브러리이다. 이미지 placeholder 6종, 표 4종, 차트 3종, 다이어그램 4종 — 총 17개 패턴의 사양과 pptxgenjs 코드 스니펫을 정의한다.

**v1.1 변경점 (2026-05-25)**:
- jc-design-system 토큰 연동 (`COLOR_*` 변수를 JC 시그니처 컬러로 갱신)
- 폰트 표준을 Pretendard(한글) + Inter(영문)로 변경
- 컬러 모드 시스템 도입 (RFP / JC / JC+오버레이)

---

## 0. 공통 규약

### 0-1. 좌표 시스템
- **레이아웃**: `LAYOUT_WIDE` 고정 (13.333" × 7.5")
- **본문 영역 권장**: x=0.5 ~ 12.83, y=0.7 ~ 7.0 (제목/푸터 제외)
- **여백**: 최소 0.5"

### 0-2. 컬러 모드 시스템 (v1.1 신규)

세 가지 모드를 지원한다. 사용자 선택 또는 RFP 분석 결과에 따라 자동 결정.

#### 모드 1: RFP 컬러 모드
RFP에 명시된 발주처 CI 컬러를 추출해 적용. 공공/정부 발주처가 CI 컬러를 강하게 요구할 때 사용.

```javascript
// 예: 환경/ESG 발주처 → Forest & Moss 팔레트
const COLOR_PRIMARY = "2C5F2D";
const COLOR_SECONDARY = "97BC62";
const COLOR_ACCENT = "F5F5F5";
```

#### 모드 2: JC 시그니처 모드 (기본 권장)
jc-design-system의 시그니처 토큰을 그대로 적용. 일관된 개인 브랜드 표현.

```javascript
// JC 시그니처 컬러 (Pretendard·Inter 폰트 패밀리)
const COLOR_PRIMARY = "0A2540";        // Deep Navy
const COLOR_PRIMARY_SOFT = "1A3556";   // Primary Soft
const COLOR_SECONDARY = "1A3556";      // Primary Soft (보조)
const COLOR_ACCENT = "2962FF";         // Electric Blue
const COLOR_ACCENT_SOFT = "E8EFFF";    // Accent Soft (배경)
const COLOR_ACCENT_STRONG = "1E4DCC";  // Accent Strong (호버)

const COLOR_TEXT = "1A1D24";           // Charcoal
const COLOR_TEXT_MUTED = "5A6270";     // Muted
const COLOR_TEXT_DISABLED = "A0A6B0";  // Disabled

const COLOR_SURFACE = "FFFFFF";        // 카드 배경
const COLOR_SURFACE_ALT = "F1F3F7";    // 보조 서피스
const COLOR_BG = "F8F9FB";             // 페이지 배경
const COLOR_BG_LIGHT = "F8F9FB";       // 줄무늬 행, 카드 배경
const COLOR_BG_PLACEHOLDER = "E5E8ED"; // 이미지 placeholder
const COLOR_BORDER = "E5E8ED";         // 기본 보더
const COLOR_BORDER_STRONG = "C9CFD8";  // 강조 보더

// 포인트 컬러 풀 (한 화면 최대 3종)
const COLOR_POINT_ORANGE = "FF5722";   // Vivid Orange (핫·우선순위)
const COLOR_POINT_MAGENTA = "E91E63";  // Magenta (차별화·Track B)
const COLOR_POINT_NEON = "00E676";     // Neon Green (성장·긍정, 면적 5% 이내)
const COLOR_POINT_NEON_PRINT = "00C853"; // 인쇄용 폴백

// 차트 데이터 시리즈 (5단계)
const CHART_SERIES = ["2962FF", "E91E63", "FF5722", "00E676", "0A2540"];

// 시맨틱 컬러
const COLOR_SUCCESS = "00C853";
const COLOR_WARNING = "FFA000";
const COLOR_DANGER = "D32F2F";
const COLOR_INFO = "2962FF";
```

#### 모드 3: JC + 클라이언트 오버레이 모드
JC 시그니처 베이스 + 클라이언트별 `primary`·`accent`·`logo` 오버레이.

```javascript
// 예: Darktrace Korea 행사 (jc-design-system/client-overlays.md 참조)
const COLOR_PRIMARY = "0A2540";        // JC Deep Navy (유지)
const COLOR_ACCENT = "E91E63";         // Magenta (Darktrace 오버레이)
// 나머지는 JC 시그니처 그대로
```

### 0-3. 폰트 표준 (v1.1 신규 - Pretendard 우선)

```javascript
// 한글 본문/제목 — Pretendard 우선, 시스템 폰트 폴백
const FONT_KO = "Pretendard";  // 또는 "Apple SD Gothic Neo" (Mac), "Malgun Gothic" (Win)
const FONT_EN = "Inter";       // 영문 본문 — 또는 "Helvetica Neue", Arial
const FONT_MONO = "JetBrains Mono";  // 숫자·데이터 — 또는 "D2Coding", Consolas
const FONT_HEADING = "Pretendard";   // 한·영 혼용 헤딩

// 사용 시:
slide.addText("제목", { fontFace: FONT_HEADING, bold: true, fontSize: 36 });
slide.addText("612", { fontFace: FONT_HEADING, bold: true, fontSize: 60 });  // 숫자 강조
```

**폰트 폴백 정책**: PPTX는 클라이언트 PC의 설치 폰트에 의존하므로, Pretendard가 없으면 PowerPoint가 자동으로 가장 가까운 시스템 폰트로 렌더한다. 사용자에게 Pretendard 설치 안내를 슬라이드 노트에 자동 삽입 권장.

### 0-4. 사이즈·간격 스케일 (jc-design-system 호환)

```javascript
// 폰트 사이즈 (단위: pt — pptxgenjs는 pt 사용)
const SIZE_XS = 9;        // 캡션·각주
const SIZE_SM = 11;       // 보조 텍스트·테이블
const SIZE_BASE = 14;     // 본문 (기본)
const SIZE_LG = 16;       // 강조 본문
const SIZE_XL = 20;       // H4·소제목
const SIZE_2XL = 24;      // H3·섹션 타이틀
const SIZE_3XL = 32;      // H2·KPI 숫자
const SIZE_4XL = 40;      // H1·페이지 타이틀
const SIZE_5XL = 56;      // 표지·임팩트

// 간격 (인치 — pptxgenjs는 인치 사용)
const SPACE_1 = 0.04;     // 4px ≈ 0.04"
const SPACE_2 = 0.08;     // 8px
const SPACE_3 = 0.12;     // 12px
const SPACE_4 = 0.16;     // 16px (카드 패딩 기본)
const SPACE_5 = 0.25;     // 24px (섹션 내 그룹)
const SPACE_6 = 0.33;     // 32px (섹션 간격)
const SPACE_7 = 0.5;      // 48px (페이지 섹션 분리)
const SPACE_8 = 0.67;     // 64px (챕터 분리)

// 모서리 라운드 (pptxgenjs rectRadius — 0~1 비율, 도형 크기 대비)
const RADIUS_SM = 0.04;   // 4px
const RADIUS_MD = 0.06;   // 8px (버튼·인풋)
const RADIUS_LG = 0.08;   // 12px (카드 기본)
const RADIUS_XL = 0.12;   // 16px (큰 컨테이너)
```

### 0-5. pptxgenjs 주의사항 (반복 강조)
1. hex 컬러는 `#` 없이 6자리만 (`"0A2540"` ✅, `"#0A2540"` ❌)
2. 옵션 객체는 호출마다 새로 생성 (재사용 금지 — pptxgenjs가 in-place 변경함)
3. `bullet: true` 사용. 유니코드 `•` 사용 금지
4. `breakLine: true`로 줄바꿈
5. `ROUNDED_RECTANGLE` + 사각 보더 조합 금지 → 둥근 모서리에 빈틈 발생
6. 제목 아래 장식선(accent line) 절대 금지

---

## 1. 이미지 Placeholder 시스템 (6종)

### 1-0. 공통 함수 — Placeholder 생성기

```javascript
function addImagePlaceholder(slide, opts) {
  const { x, y, w, h, caption, shape = "rect" } = opts;
  const shapeType = shape === "circle" ? pres.shapes.OVAL : pres.shapes.RECTANGLE;

  // 배경 박스 (점선 테두리)
  slide.addShape(shapeType, {
    x, y, w, h,
    fill: { color: COLOR_BG_PLACEHOLDER },
    line: { color: COLOR_BORDER_STRONG, width: 1, dashType: "dash" }
  });

  // 중앙 아이콘 (+ 기호)
  slide.addText("+", {
    x, y, w, h,
    fontSize: Math.min(w, h) * 24,
    color: COLOR_TEXT_MUTED, bold: true,
    fontFace: FONT_HEADING,
    align: "center", valign: "middle", margin: 0
  });

  // 하단 캡션
  slide.addText(caption || "[이미지]", {
    x, y: y + h - 0.35, w, h: 0.3,
    fontSize: SIZE_SM, fontFace: FONT_KO,
    color: COLOR_TEXT_MUTED,
    align: "center", valign: "middle", margin: 0
  });
}
```

### 1-1. IMG-HERO — 풀블리드 히어로 (13.33 × 7.5, 16:9, 사각)
표지·섹션 구분·Thank You. Primary 컬러 40~60% 투명도 오버레이 권장.

### 1-2. IMG-WIDE — 본문 메인 시각자료 (5.5~6.0 × 3.3~3.6, 5:3, 사각)
컨셉·디자인 컨셉·공간 디자인 슬라이드의 메인 비주얼.

### 1-3. IMG-CARD — 카드 그리드 내부 이미지 (2.5 × 1.5, 5:3, 사각)
프로그램 구성·유사 실적 카드 내부 상단.

### 1-4. IMG-PORTRAIT — 인물 사각 사진 (1.5 × 2.0, 3:4, 사각)
투입 인력 프로필 (사각 형태).

### 1-5. IMG-AVATAR — 인물 원형 사진 (1.2 × 1.2, 1:1, 원형)
투입 인력 프로필 컴팩트 버전. `shape: "circle"` 옵션 사용.

### 1-6. IMG-MOOD — 무드보드 그리드 (셀당 2.5 × 2.5, 1:1, 사각, 4/6/9분할)
디자인 컨셉 슬라이드의 무드보드.

### 1-7. 슬라이드 노트 자동 삽입 표준 텍스트

```javascript
slide.addNotes(
  "■ 이미지 교체 안내 (회색 박스 모드)\n" +
  "회색 점선 박스로 표시된 영역에 실제 이미지를 삽입해주세요.\n" +
  "PowerPoint에서: 박스 클릭 → Delete → 동일 위치에 [삽입 → 사진]\n" +
  "캡션 텍스트도 함께 삭제하면 됩니다.\n\n" +
  "■ 폰트 안내\n" +
  "이 제안서는 Pretendard 폰트를 권장합니다.\n" +
  "미설치 시 https://github.com/orioncactus/pretendard 에서 다운로드.\n" +
  "(미설치 시 시스템 기본 한글 폰트로 자동 대체됩니다)"
);
```

---

## 2. 표(Table) 패턴 (4종)

### 2-0. 공통 규격

| 항목 | 값 |
|------|-----|
| 헤더 배경 | `COLOR_PRIMARY` (Deep Navy) |
| 헤더 글자 | 흰색, Bold, `SIZE_SM`(11pt), Pretendard |
| 본문 폰트 | Pretendard, 10~11pt |
| 짝수행 배경 | `COLOR_SURFACE_ALT` (zebra) |
| 홀수행 배경 | 흰색 |
| 외곽선 | 0.5pt `COLOR_BORDER` |
| 셀 패딩 | 0.08" × 0.05" |

### 2-0-1. 공통 헬퍼 함수

```javascript
function makeHeaderRow(labels) {
  return labels.map(label => ({
    text: label,
    options: {
      fill: { color: COLOR_PRIMARY },
      color: "FFFFFF", bold: true,
      fontSize: SIZE_SM, fontFace: FONT_KO,
      align: "center", valign: "middle"
    }
  }));
}

function makeBodyRow(values, rowIndex, options = {}) {
  const bgColor = rowIndex % 2 === 0 ? "FFFFFF" : COLOR_SURFACE_ALT;
  return values.map((val, colIdx) => ({
    text: String(val),
    options: {
      fill: { color: bgColor },
      color: COLOR_TEXT,
      fontSize: SIZE_SM, fontFace: FONT_KO,
      align: options.aligns?.[colIdx] || "left",
      valign: "middle",
      margin: [0.05, 0.08, 0.05, 0.08]
    }
  }));
}
```

### 2-1. TBL-T1 (비교표)

용도: 경쟁사·옵션·안 비교. 추천안 컬럼 전체를 `COLOR_PRIMARY` 배경 + 흰 글자로 강조.

### 2-2. TBL-T2 (매트릭스 표)

용도: RFP 평가 대응표, 위험 매트릭스. 합계 행은 `COLOR_PRIMARY` 배경 강조.

### 2-3. TBL-T3 (일정/타임테이블)

용도: 행사 당일 진행표. 시간 컬럼 Bold, 핵심 프로그램 행에 `COLOR_ACCENT` 좌측 보더 (3pt).

### 2-4. TBL-T4 (예산표)

용도: 산출내역서. 숫자 컬럼 우측 정렬·천단위 콤마, 합계 행 `COLOR_PRIMARY` 배경.

```javascript
// TBL-T4 합계 행 예시 (v1.1 토큰 적용)
const t4Sum = [
  { text: "합계", options: { 
      fill: { color: COLOR_PRIMARY }, color: "FFFFFF", 
      bold: true, fontSize: SIZE_BASE, fontFace: FONT_KO,
      align: "left", valign: "middle", colspan: 4,
      margin: [0.05, 0.08, 0.05, 0.08] 
  }},
  { text: fmt(t4Total), options: { 
      fill: { color: COLOR_PRIMARY }, color: "FFFFFF", 
      bold: true, fontSize: SIZE_BASE, fontFace: FONT_MONO,  // 숫자는 mono 권장
      align: "right", valign: "middle",
      margin: [0.05, 0.08, 0.05, 0.08] 
  }},
  { text: "VAT 별도", options: { 
      fill: { color: COLOR_PRIMARY }, color: "FFFFFF", 
      fontSize: SIZE_XS, fontFace: FONT_KO,
      align: "left", valign: "middle",
      margin: [0.05, 0.08, 0.05, 0.08] 
  }}
];
```

> 표 패턴(TBL-T1~T4)의 전체 코드 스니펫은 mice-proposal v2.0(이전 버전)의 `visual-patterns.md`와 동일하며, 컬러 변수만 v1.1 토큰으로 치환한다. 자세한 코드 예시는 `slide-structure.md` 슬라이드별 매핑 참조.

---

## 3. 차트(Chart) 패턴 (3종)

### 3-1. CHART-C1 (도넛 차트)

```javascript
slide.addChart(pres.charts.DOUGHNUT, [{
  name: "예산 항목",
  labels: ["기획·운영", "공간·시설", "디자인·제작", "홍보·마케팅", "F&B", "예비비"],
  values: [21, 13, 12, 9, 39, 6]
}], {
  x: 0.5, y: 1.5, w: 6.0, h: 5.0,
  chartColors: CHART_SERIES,  // v1.1: JC 데이터 시리즈 5색
  chartArea: { fill: { color: "FFFFFF" } },
  showLegend: true,
  legendPos: "r",
  legendFontSize: SIZE_SM,
  legendColor: COLOR_TEXT,
  legendFontFace: FONT_KO,
  showPercent: true,
  dataLabelColor: "FFFFFF",
  dataLabelFontSize: SIZE_XS,
  dataLabelFontBold: true,
  dataLabelFontFace: FONT_HEADING,
  holeSize: 60,
  showTitle: false
});
```

### 3-2. CHART-C2 (바·컬럼 차트)

```javascript
// 단일 시리즈
slide.addChart(pres.charts.BAR, [{
  name: "연간 행사 건수",
  labels: ["2021", "2022", "2023", "2024", "2025"],
  values: [12, 15, 18, 22, 27]
}], {
  x: 0.5, y: 1.5, w: 12.33, h: 5.0,
  barDir: "col",
  chartColors: [COLOR_ACCENT],
  chartArea: { fill: { color: "FFFFFF" } },
  catAxisLabelColor: COLOR_TEXT_MUTED,
  catAxisLabelFontSize: SIZE_SM,
  catAxisLabelFontFace: FONT_KO,
  valAxisLabelColor: COLOR_TEXT_MUTED,
  valAxisLabelFontSize: SIZE_XS,
  valGridLine: { color: COLOR_BORDER, size: 0.5 },
  catGridLine: { style: "none" },
  showValue: true,
  dataLabelPosition: "outEnd",
  dataLabelColor: COLOR_TEXT,
  dataLabelFontSize: SIZE_SM,
  dataLabelFontBold: true,
  dataLabelFontFace: FONT_HEADING,
  showLegend: false
});

// 비교 시리즈 — chartColors: [COLOR_TEXT_DISABLED, COLOR_ACCENT]
```

### 3-3. CHART-C3 (빅넘버 콜아웃)

```javascript
function addBigNumberCallout(slide, opts) {
  const { x, y, w, h, value, unit, label, color = COLOR_ACCENT } = opts;

  // 숫자 자동 천단위 콤마 (number 타입일 때만)
  const valueStr = typeof value === "number"
    ? value.toLocaleString("ko-KR")
    : String(value);

  slide.addText(valueStr, {
    x, y, w, h: h * 0.55,
    fontSize: 60, bold: true, color,
    fontFace: FONT_HEADING,  // v1.1: Pretendard (한글 숫자 혼용 시) 또는 FONT_MONO
    align: "center", valign: "bottom", margin: 0
  });

  if (unit) {
    slide.addText(unit, {
      x, y: y + h * 0.55, w, h: 0.3,
      fontSize: SIZE_XL, color, bold: true,
      fontFace: FONT_KO,
      align: "center", valign: "top", margin: 0
    });
  }

  slide.addText(label, {
    x, y: y + h * 0.55 + 0.3, w, h: h * 0.3 - 0.3,
    fontSize: SIZE_SM, color: COLOR_TEXT_MUTED,
    fontFace: FONT_KO,
    align: "center", valign: "top", margin: 0
  });
}
```

> **v1.1 패치 (2026-05-25)**: 검증 결과 `String(value)`로 숫자를 그대로 출력하면 천단위 콤마가 누락된다(1200으로 표시). `typeof value === "number"` 체크 후 `toLocaleString("ko-KR")` 적용으로 수정됨. number가 아닌 string으로 들어오는 경우(예: "9.5K")는 그대로 출력.

---

## 4. 다이어그램(Diagram) 패턴 (4종)

### 4-1. DIAG-D1 (조직도)
3단 구조. 최상단 `COLOR_PRIMARY`, 2단 `COLOR_PRIMARY_SOFT`, 3단 `COLOR_SURFACE_ALT`.

### 4-2. DIAG-D2 (프로세스 플로우)
좌→우. 첫 박스 `COLOR_ACCENT` → 점진적 옅어짐. 화살표는 `LINE` + `endArrowType: "triangle"`.

### 4-3. DIAG-D3 (타임라인)
가로 라인 `COLOR_ACCENT` 2pt + 마일스톤 노드 `COLOR_POINT_ORANGE` 0.35" 직경 + 라벨 위·아래 번갈아.

> **v1.1 패치 (2026-05-25)**: 검증 결과 구간 밴드가 거의 안 보이는 결함 발견. 수정값:
> - 구간 밴드 컬러: `EBF4F9 / D5E8F3 / BFDCED / EBF4F9` (옅음) → `D5E8F3 / A7CFE5 / 7AB6D6 / D5E8F3` (점진적 진해짐)
> - 투명도: `50%` → `20%`
> - 단계가 진행될수록 컬러가 진해지므로 시각적 시간 흐름 표현 가능

### 4-4. DIAG-D4 (카드 그리드)
좌측 4pt `COLOR_ACCENT` 보더 + 카드 배경 흰색 + 미세 그림자.

```javascript
// DIAG-D4 카드 (v1.1 토큰)
slide.addShape(pres.shapes.RECTANGLE, {
  x, y, w: cardW, h: cardH,
  fill: { color: COLOR_SURFACE },
  line: { color: COLOR_BORDER, width: 0.5 },
  shadow: { type: "outer", color: "0A2540", opacity: 0.08, blur: 4, offset: 1, angle: 135 }
});

// 좌측 Accent 보더
slide.addShape(pres.shapes.RECTANGLE, {
  x, y, w: 0.08, h: cardH,
  fill: { color: COLOR_ACCENT },
  line: { type: "none" }
});

// 제목 (Electric Blue)
slide.addText(card.title, {
  x: x + 0.3, y: y + 0.3, w: cardW - 0.6, h: 0.6,
  fontSize: SIZE_XL, bold: true, color: COLOR_ACCENT,
  fontFace: FONT_HEADING,
  align: "left", valign: "middle", margin: 0
});

// 본문
slide.addText(card.desc, {
  x: x + 0.3, y: y + 1.0, w: cardW - 0.6, h: cardH - 1.2,
  fontSize: SIZE_BASE, color: COLOR_TEXT,
  fontFace: FONT_KO,
  align: "left", valign: "top", margin: 0
});
```

> 다이어그램 패턴(DIAG-D1~D4)의 전체 코드 스니펫은 mice-proposal v2.0의 `visual-patterns.md`와 동일하며, 컬러·폰트 변수만 v1.1 토큰으로 치환한다.

---

## 5. 색상 위계 표준 규칙 (v1.1 갱신)

| 요소 | 컬러 사용 |
|------|----------|
| 최상위 강조 (헤더, 합계, 추천안, 1단 조직) | `COLOR_PRIMARY` (Deep Navy) |
| 액센트·CTA·메인 차트 시리즈·KPI 강조 | `COLOR_ACCENT` (Electric Blue) |
| 보조 강조 (2단 조직, 비교 시리즈 2) | `COLOR_PRIMARY_SOFT` |
| 포인트 (마일스톤 노드, 카드 좌측 보더 옵션) | `COLOR_POINT_ORANGE` / `COLOR_POINT_MAGENTA` |
| 본문 글자 | `COLOR_TEXT` (Charcoal) |
| 보조 글자 (캡션, 비고, 축 라벨) | `COLOR_TEXT_MUTED` |
| 짝수행 배경, 보조 영역 | `COLOR_SURFACE_ALT` |
| 이미지 placeholder | `COLOR_BG_PLACEHOLDER` |
| 테두리, 보더 | `COLOR_BORDER` (기본) ~ `COLOR_BORDER_STRONG` (강조) |

---

## 6. 검증 체크리스트

### 콘텐츠 검증
- [ ] 모든 슬라이드에 비주얼 요소(이미지/표/차트/다이어그램) 최소 1개 이상 포함
- [ ] 이미지 placeholder마다 캡션 명시
- [ ] 슬라이드 노트에 교체 안내 + 폰트 안내 자동 삽입
- [ ] 표 합계 행이 Primary 배경 강조
- [ ] 차트 색상이 `CHART_SERIES` 또는 `COLOR_ACCENT` 기반

### 시각 검증
- [ ] 텍스트 박스 오버플로우 없음
- [ ] 동일 비주얼 패턴 3장 연속 없음
- [ ] 다크 배경의 글자 고대비
- [ ] ROUNDED + 사각 보더 조합으로 인한 빈틈 없음
- [ ] 폰트 페이스가 모든 텍스트에 명시 (FONT_KO/FONT_HEADING/FONT_MONO)

### 코드 품질
- [ ] hex 컬러 `#` 없음
- [ ] shadow `opacity` 분리
- [ ] 옵션 객체 재사용 없음
- [ ] `bullet: true` 사용

### 신규 (v1.1)
- [ ] 컬러 모드 결정됨 (RFP / JC / JC+오버레이)
- [ ] 사용된 컬러가 jc-design-system 토큰 표에 매핑됨
- [ ] 폰트가 Pretendard·Inter·JetBrains Mono로 명시됨
- [ ] 사이즈가 `SIZE_*` 토큰 사용

---

## 7. 함께 보는 문서

| 파일 | 내용 |
|------|------|
| `slide-structure.md` | 슬라이드별 패턴 적용 매핑 |
| `dark-mode-patterns.md` | 다크 모드 변형 (DARK-TBL, DARK-CHART, DARK-C3, DARK-D4, DARK-IMG) |
| `icon-library.md` | react-icons 활용 + 슬라이드별 아이콘 매핑 |
| `infographic-patterns.md` | 인포그래픽 3종 (INFO-I1 퍼널, INFO-I2 매트릭스, INFO-I3 레이더) |
| `slide-masters.md` | PowerPoint 네이티브 그림 자리표시자 + 5개 슬라이드 마스터 |
