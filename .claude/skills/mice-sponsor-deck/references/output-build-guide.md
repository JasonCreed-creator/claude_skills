# Output Build Guide — HTML 1차 빌드 + PPTX 변환

본 스킬의 산출물 빌드 워크플로우. **HTML이 1차 산출물이며, PPTX는 HTML 콘텐츠를 변환한 2차 산출물**이다.

---

## 1. 빌드 워크플로우 전체

```
┌──────────────────────────────────────┐
│ Phase 1~6: 콘텐츠 분석·확정          │
│ - 6축 분석 / Tier / 매트릭스 / ROI    │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│ Phase 7: 콘텐츠 JSON 생성            │
│ - 슬라이드별 콘텐츠 데이터 객체화     │
│ - HTML/PPTX 공통 single source       │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│ Phase 8: HTML 빌드 (1차 산출물)      │
│ - 단일 파일 HTML 슬라이드 데크        │
│ - 키보드 네비, 인쇄 페이지 분리       │
│ - 사용자 검토 → 확정                  │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│ Phase 9: PPTX 변환 (2차 산출물)      │
│ - HTML 콘텐츠 JSON → pptxgenjs       │
│ - 슬라이드 1:1 매핑                  │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│ Phase 10 (옵션): XLSX 매트릭스       │
└──────────────────────────────────────┘
```

**HTML 검토·확정 이후에만 PPTX 빌드 진입.** 콘텐츠가 두 산출물 사이에서 일치해야 한다.

---

## 2. 콘텐츠 JSON 스키마

HTML/PPTX 공통 single source. 빌드 진입 전 다음 스키마로 콘텐츠를 객체화한다.

### 2.1 최상위 구조

```json
{
  "meta": {
    "event_name": "...",
    "event_subtitle": "...",
    "event_date": "...",
    "event_venue": "...",
    "client_id": null,
    "naming_mode": "ko_first",
    "price_mode": "on_request",
    "deck_version": "v1.0",
    "is_provisional": false
  },
  "audience": {
    "kpis": [...],
    "industry_distribution": [...],
    "title_distribution": [...],
    "decision_maker_ratio": {...}
  },
  "assets": {
    "offline": [...],
    "digital": [...],
    "vip_content": [...]
  },
  "tiers": [
    { "id": "T1", "name_ko": "타이틀", "name_en": "Title", "slots": 1, "price": null, "benefits": [...] },
    ...
  ],
  "matrix": {
    "categories": [...],
    "rows": [...]
  },
  "roi_cases": [
    { "industry": "tech", "premise": "...", "formula": "...", "estimate": "..." },
    ...
  ],
  "section_8": {
    "type": "past_sponsors|reference_cases|skip",
    "data": [...]
  },
  "contact": {
    "name": "...",
    "email": "...",
    "phone": "...",
    "deadline": null
  }
}
```

### 2.2 변환 룰

이 JSON 객체로부터:
- **HTML 빌더**: 슬라이드 카드 시리즈 생성
- **PPTX 빌더**: pptxgenjs 슬라이드 생성

두 빌더는 같은 JSON을 입력으로 받아 동일 콘텐츠를 생성한다.

---

## 3. HTML 빌드 가이드 (1차 산출물)

### 3.1 파일 구조

단일 HTML 파일. 외부 의존성은 Pretendard 웹폰트 CDN 1개로 한정.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>[행사명] Sponsorship Deck</title>
  <link rel="stylesheet" 
        href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.min.css">
  <style>/* 인라인 CSS, jc-design-system 토큰 적용 */</style>
</head>
<body>
  <nav class="deck-nav">...</nav>
  <main class="deck">
    <section class="slide" data-slide="1">...</section>
    <section class="slide" data-slide="2">...</section>
    <!-- 12~18 슬라이드 -->
  </main>
  <script>/* 키보드 네비, 슬라이드 전환, 인쇄 핸들러 */</script>
</body>
</html>
```

### 3.2 슬라이드 카드 표준

각 슬라이드는 16:9 비율 카드. 화면 표시 시 한 화면에 한 슬라이드, 인쇄 시 페이지당 한 슬라이드.

```css
.slide {
  width: 100vw;
  height: 100vh;
  aspect-ratio: 16 / 9;
  padding: var(--jc-space-7);
  background: var(--jc-bg);
  display: flex;
  flex-direction: column;
  scroll-snap-align: start;
  page-break-after: always;
}

@media print {
  .slide {
    width: 100%;
    height: 100vh;
    page-break-after: always;
  }
  .deck-nav { display: none; }
}
```

### 3.3 키보드 네비게이션

```javascript
document.addEventListener('keydown', (e) => {
  const slides = document.querySelectorAll('.slide');
  const current = getCurrentSlideIndex();
  if (e.key === 'ArrowRight' || e.key === ' ') {
    slides[Math.min(current + 1, slides.length - 1)].scrollIntoView({ behavior: 'smooth' });
  }
  if (e.key === 'ArrowLeft') {
    slides[Math.max(current - 1, 0)].scrollIntoView({ behavior: 'smooth' });
  }
  if (e.key === 'Home') {
    slides[0].scrollIntoView({ behavior: 'smooth' });
  }
  if (e.key === 'End') {
    slides[slides.length - 1].scrollIntoView({ behavior: 'smooth' });
  }
  if (e.key === 'Escape') {
    document.querySelector('.deck-overview').classList.toggle('show');
  }
});
```

### 3.4 인쇄 페이지 분리

```css
@media print {
  @page { 
    size: A4 landscape;
    margin: 0;
  }
  body { margin: 0; }
  .slide { 
    page-break-after: always; 
    page-break-inside: avoid;
  }
}
```

### 3.5 인터랙티브 요소 (HTML 한정)

PPTX는 인터랙티브 미지원. HTML에서만 다음 인터랙션 추가:

| 요소 | 인터랙션 |
|------|---------|
| Tier 카드 | 호버 시 그림자 + 약간 확대 |
| 매트릭스 셀 | 호버 시 해당 행·열 하이라이트 |
| ROI 카드 | 호버 시 산출 공식 단계별 강조 |
| 산업 분포 차트 | 호버 시 산업 비율 툴팁 |
| 슬라이드 네비게이션 | 우측 사이드 미니 점프 인덱스 |

PPTX 변환 시 위 인터랙티브 요소는 정적 표현으로 대체.

### 3.6 차트 구현

CSS만으로 구현 가능한 차트 우선. 복잡한 차트는 SVG 인라인.

```html
<!-- 산업 분포 가로 바 차트 (CSS 기반) -->
<div class="bar-chart">
  <div class="bar-row">
    <span class="bar-label">IT·소프트웨어</span>
    <div class="bar" style="--width: 42%; --color: var(--jc-data-1)"></div>
    <span class="bar-value">42%</span>
  </div>
  <!-- ... -->
</div>

<style>
.bar { 
  width: var(--width); 
  background: var(--color); 
  height: 24px; 
  border-radius: var(--jc-radius-sm); 
}
</style>
```

도넛 차트는 SVG circle 사용 (외부 라이브러리 불필요).

---

## 4. PPTX 변환 가이드 (2차 산출물)

### 4.1 변환 원칙

- **콘텐츠는 HTML과 1:1 일치**
- 슬라이드 수 동일
- 슬라이드 순서 동일
- 텍스트·숫자 동일
- 차트·매트릭스 동일

### 4.2 기술 스택

`/mnt/skills/public/pptx/SKILL.md` 의 pptxgenjs 방식 사용. 본 스킬은 별도 스크립트 없이 SKILL.md + references 만으로 동작 (mice-proposal 패턴).

### 4.3 슬라이드 사이즈

```javascript
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';  // 13.33 x 7.5 inch
```

### 4.4 색상·폰트 설정

`design-tokens-mapping.md` 룰을 그대로 적용:

```javascript
const TOKENS = {
  primary: '0A2540',         // # 제외
  accent: '2962FF',
  text: '1A1D24',
  textMuted: '5A6270',
  surface: 'FFFFFF',
  bg: 'F8F9FB',
  // ... (모든 토큰)
};

const FONTS = {
  ko: 'Pretendard',         // 폴백: 맑은 고딕
  en: 'Inter',              // 폴백: Helvetica Neue
  mono: 'JetBrains Mono'    // 폴백: Consolas
};
```

### 4.5 폰트 폴백

PPTX는 수신자 환경 폰트가 없으면 깨짐. 다음 룰:

- 한글 본문: `Pretendard` 우선, 없으면 `맑은 고딕` (Windows 표준)
- 영문 본문: `Inter` 우선, 없으면 `Calibri` (Office 표준)
- 모노스페이스: `JetBrains Mono` 우선, 없으면 `Consolas`

### 4.6 슬라이드 사이즈 변환 룰

HTML px 단위 → PPTX inch 단위:

```javascript
const PX_TO_INCH = 1 / 96;  // 96 DPI 가정

function pxToInch(px) {
  return px * PX_TO_INCH;
}

// 예시:
// HTML space-7 (48px) → 0.5 inch
// HTML text-3xl (36px) → 약 24pt
```

### 4.7 매트릭스 표 구현

pptxgenjs `addTable` 사용:

```javascript
slide.addTable(matrix.rows, {
  x: 0.5, y: 1.5, w: 12.33, h: 5,
  fontFace: FONTS.ko,
  fontSize: 11,
  colW: [3, 1.85, 1.85, 1.85, 1.85, 1.85],
  border: { type: 'solid', color: TOKENS.border, pt: 0.5 },
  fill: { color: TOKENS.surface }
});
```

### 4.8 차트 구현

산업 분포·직급 분포 차트는 pptxgenjs `addChart` 사용:

```javascript
slide.addChart(pptx.ChartType.bar, [{
  name: '산업 분포',
  labels: ['IT', '금융', '제조', '헬스케어', '기타'],
  values: [42, 24, 18, 10, 6]
}], {
  x: 0.5, y: 1.5, w: 6, h: 4.5,
  chartColors: [TOKENS.dataColors[0], TOKENS.dataColors[1], 
                TOKENS.dataColors[2], TOKENS.dataColors[3], 
                TOKENS.dataColors[4]],
  showLegend: false,
  catAxisLabelFontSize: 10,
  valAxisLabelFontSize: 10
});
```

### 4.9 Tier 카드 구현

pptxgenjs `addShape` (roundedRect) + `addText` 조합:

```javascript
// Tier 카드 배경
slide.addShape(pptx.ShapeType.roundRect, {
  x: 0.5, y: 1.5, w: 2.5, h: 3.5,
  fill: { color: TOKENS.surface },
  line: { color: TOKENS.border, width: 0.5 },
  rectRadius: 0.1
});

// 좌측 액센트 막대
slide.addShape(pptx.ShapeType.rect, {
  x: 0.5, y: 1.5, w: 0.05, h: 3.5,
  fill: { color: TIER_COLORS.T1 },  // Magenta for T1
  line: { color: 'transparent' }
});

// Tier 명칭
slide.addText('T1 타이틀 (Title)', {
  x: 0.7, y: 1.6, w: 2.2, h: 0.4,
  fontFace: FONTS.ko,
  fontSize: 16,
  bold: true,
  color: TOKENS.text
});

// 슬롯·가격
slide.addText('한정 1석\n가격 별도 협의', {
  x: 0.7, y: 2.1, w: 2.2, h: 0.6,
  fontFace: FONTS.ko,
  fontSize: 12,
  color: TOKENS.textMuted
});

// 핵심 혜택 bullet
slide.addText([
  { text: '• 행사명 결합권', options: { bullet: false } },
  { text: '• 키노트 발표 30분', options: { bullet: false } },
  // ...
], {
  x: 0.7, y: 2.8, w: 2.2, h: 2,
  fontFace: FONTS.ko,
  fontSize: 11,
  color: TOKENS.text,
  paraSpaceAfter: 4
});
```

---

## 5. HTML→PPTX 매핑 룰 (요소별)

| HTML 요소 | PPTX 변환 |
|----------|----------|
| `<section class="slide">` | `pptx.addSlide()` |
| `<h1 class="slide-title">` | `slide.addText({fontSize: 32pt, bold: true})` |
| `<div class="kpi-card">` | `roundRect 도형 + addText` 조합 |
| `<div class="bar-chart">` | `slide.addChart(bar)` |
| `<table class="matrix">` | `slide.addTable()` |
| `<div class="tier-card">` | `roundRect + 좌측 rect 액센트 + addText` |
| `<div class="roi-card">` | `roundRect + 3단 텍스트 블록` |
| 호버·인터랙션 | **정적 표현으로 대체** (PPTX 미지원) |
| 차트 호버 툴팁 | **데이터 라벨로 대체** (`showValue: true`) |

---

## 6. 옵션 산출물 — XLSX 매트릭스

`include_xlsx = true` 인 경우 별도 XLSX 생성. `/mnt/skills/public/xlsx/SKILL.md` 가이드 따름.

### 6.1 XLSX 시트 구조

| 시트 | 내용 |
|------|------|
| `Tiers` | Tier 5단 + 가격(또는 협의)·슬롯·요약 혜택 |
| `Benefits Matrix` | 7카테고리 × 5 Tier 매트릭스 (정량값 포함) |
| `Audience` | 청중 데이터 (산업·직급·KPI) |
| `ROI` | 산업별 ROI 시나리오 (3단 표시) |

### 6.2 XLSX 디자인

- 헤더: jc-design-system primary 배경 + 흰색 텍스트
- Tier 색상: 매트릭스 헤더 행에 Tier 색상 적용
- 폰트: 시스템 기본 (Calibri 11pt) — XLSX는 Pretendard 미지원 환경 대응

---

## 7. QA 체크리스트 (HTML/PPTX 공통)

### 7.1 콘텐츠 일치 검증

- [ ] 슬라이드 수가 HTML과 PPTX에서 동일한가
- [ ] 슬라이드 순서가 동일한가
- [ ] 모든 텍스트·숫자가 일치하는가
- [ ] 차트 데이터가 일치하는가
- [ ] 매트릭스 셀 값이 일치하는가
- [ ] Tier 색상이 일치하는가

### 7.2 HTML 자체 QA

- [ ] 키보드 네비게이션 정상 작동 (←/→/Space/Esc)
- [ ] 인쇄 시 슬라이드별 페이지 분리 정상
- [ ] Pretendard 미설치 환경 폴백 정상
- [ ] 모바일 화면 (선택) 가독성 확인
- [ ] 단일 파일 자족형 (외부 의존성: Pretendard CDN만)

### 7.3 PPTX 자체 QA

- [ ] `/mnt/skills/public/pptx/SKILL.md` QA 절차 수행
- [ ] 폰트 폴백 정상 동작
- [ ] 16:9 비율 슬라이드
- [ ] 차트 정상 렌더링
- [ ] 표 셀 병합 정상

---

## 8. 빌드 실행 순서

```
1. 콘텐츠 JSON 생성 (Phase 7)
   └─ 6축 분석 결과 → JSON 객체화

2. HTML 빌드 (Phase 8)
   ├─ jc-design-system signature-tokens.md 로드
   ├─ design-tokens-mapping.md 적용
   ├─ 단일 HTML 파일 생성
   └─ 사용자 검토 요청 → 확정

3. PPTX 변환 (Phase 9)
   ├─ /mnt/skills/public/pptx/SKILL.md 로드
   ├─ 동일 콘텐츠 JSON 입력
   ├─ pptxgenjs 슬라이드 생성
   └─ QA 수행

4. (옵션) XLSX 매트릭스 (Phase 10)
   ├─ /mnt/skills/public/xlsx/SKILL.md 로드
   └─ 4시트 XLSX 생성

5. present_files 호출 → 사용자 전달
```

---

## 9. JSON 스키마 (요약)

```json
{
  "build_workflow": {
    "primary_output": "html",
    "secondary_output": "pptx",
    "optional_output": "xlsx",
    "html_review_required_before_pptx": true,
    "content_source": "json_single_source"
  },
  "html_requirements": {
    "single_file": true,
    "external_deps": ["pretendard_cdn"],
    "keyboard_nav": true,
    "print_pagebreak": true,
    "interactive_elements": true
  },
  "pptx_requirements": {
    "library": "pptxgenjs",
    "layout": "16:9",
    "content_match_html": true
  }
}
```
