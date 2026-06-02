# Component Patterns — 컴포넌트 패턴

산출물에 자주 등장하는 시각 컴포넌트 패턴을 정의한다.

---

## 1. KPI 카드

### 1.1 표준형

```html
<div style="
  background: var(--jc-surface);
  border: 0.5px solid var(--jc-border);
  border-radius: var(--jc-radius-lg);
  padding: 16px 20px;
">
  <div style="
    font-family: var(--jc-font-ko);
    font-size: 12px;
    color: var(--jc-text-muted);
  ">2026 매출 목표</div>
  
  <div style="
    font-family: var(--jc-font-mono);
    font-size: 28px;
    font-weight: 600;
    color: var(--jc-primary);
    margin-top: 4px;
  ">5.0억</div>
  
  <div style="
    font-family: var(--jc-font-ko);
    font-size: 12px;
    color: var(--jc-accent);
    margin-top: 4px;
  ">▲ 전년比 +25%</div>
</div>
```

### 1.2 강조형 (좌측 액센트 라인)

```html
<div style="
  background: var(--jc-surface);
  border: 0.5px solid var(--jc-border);
  border-left: 3px solid var(--jc-point-orange);
  border-radius: var(--jc-radius-lg);
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  padding: 16px 20px;
">
  <!-- KPI 내용 -->
</div>
```

### 1.3 KPI 카드 사용 규칙

- 한 행 최대 4개. 5개 이상은 2행으로 분리
- 숫자는 항상 `--jc-font-mono` 적용
- 트렌드 표시는 `▲ ▼ ●` 기호 + 컬러로 의미 전달
  - 상승·긍정 → `--jc-accent` 또는 `--jc-success`
  - 하락·부정 → `--jc-danger`
  - 핫스팟 → `--jc-point-orange`
  - 라이브·실시간 → `--jc-point-neon`

---

## 2. 차트 컨테이너

### 2.1 기본 구조

```html
<div style="
  background: var(--jc-surface);
  border: 0.5px solid var(--jc-border);
  border-radius: var(--jc-radius-lg);
  padding: 20px 24px;
">
  <!-- 차트 헤더 -->
  <div style="margin-bottom: 16px;">
    <div style="
      font-size: 16px;
      font-weight: 600;
      color: var(--jc-text);
    ">월별 매출 추이</div>
    <div style="
      font-size: 12px;
      color: var(--jc-text-muted);
      margin-top: 4px;
    ">2026년 1월 ~ 12월 (단위: 억원)</div>
  </div>
  
  <!-- 차트 영역 -->
  <div style="height: 280px;"><!-- 차트 라이브러리 렌더링 --></div>
  
  <!-- 범례 -->
  <div style="
    display: flex;
    gap: 16px;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 0.5px solid var(--jc-border);
    font-size: 12px;
    color: var(--jc-text-muted);
  ">
    <span><span style="color: var(--jc-data-1);">●</span> 실적</span>
    <span><span style="color: var(--jc-data-2);">●</span> 목표</span>
  </div>
</div>
```

### 2.2 차트 시리즈 운용 규칙

- 한 차트 동시 사용 시리즈 **최대 3종**
- 시리즈 우선순위: data-1 → data-2 → data-3 → data-4 → data-5
- Neon Green(data-4)은 강조 시리즈에 한정. 면적 5% 이내
- 그리드 라인: `var(--jc-border)` 0.5px solid
- 축 텍스트: `var(--jc-text-muted)` 12px

---

## 3. 섹션 구분

### 3.1 섹션 타이틀

```html
<div style="margin: 48px 0 24px;">
  <div style="
    font-size: 12px;
    font-weight: 600;
    color: var(--jc-accent);
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 8px;
  ">SECTION 01</div>
  
  <div style="
    font-size: 28px;
    font-weight: 600;
    color: var(--jc-primary);
    line-height: 1.2;
  ">사업 개요</div>
  
  <div style="
    width: 32px;
    height: 3px;
    background: var(--jc-accent);
    margin-top: 12px;
  "></div>
</div>
```

### 3.2 섹션 구분선

```html
<!-- 약한 구분 -->
<hr style="
  border: none;
  border-top: 0.5px solid var(--jc-border);
  margin: 32px 0;
">

<!-- 강한 구분 -->
<hr style="
  border: none;
  border-top: 1px solid var(--jc-border-strong);
  margin: 48px 0;
">
```

---

## 4. 테이블

### 4.1 표준 테이블

```html
<table style="
  width: 100%;
  border-collapse: collapse;
  font-family: var(--jc-font-ko);
  font-size: 14px;
">
  <thead>
    <tr style="
      background: var(--jc-surface-alt);
      border-bottom: 1px solid var(--jc-border-strong);
    ">
      <th style="
        text-align: left;
        padding: 12px 16px;
        font-weight: 600;
        color: var(--jc-text);
      ">항목</th>
      <th style="
        text-align: right;
        padding: 12px 16px;
        font-weight: 600;
        color: var(--jc-text);
      ">금액</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom: 0.5px solid var(--jc-border);">
      <td style="padding: 12px 16px; color: var(--jc-text);">기획비</td>
      <td style="
        padding: 12px 16px;
        text-align: right;
        font-family: var(--jc-font-mono);
        color: var(--jc-text);
      ">15,000,000</td>
    </tr>
  </tbody>
  <tfoot>
    <tr style="background: var(--jc-primary); color: var(--jc-surface);">
      <td style="padding: 14px 16px; font-weight: 600;">합계</td>
      <td style="
        padding: 14px 16px;
        text-align: right;
        font-family: var(--jc-font-mono);
        font-weight: 600;
      ">50,000,000</td>
    </tr>
  </tfoot>
</table>
```

### 4.2 테이블 사용 규칙

- 헤더 배경: `--jc-surface-alt`
- 합계 행 배경: `--jc-primary` + 흰색 텍스트
- 숫자 컬럼: `--jc-font-mono` + 우측 정렬
- 행 구분선: `0.5px solid --jc-border`
- 호버 행 배경: `--jc-accent-soft` (인터랙티브 산출물에서만)

---

## 5. 헤더 / 표지 / 푸터

### 5.1 문서 헤더 (상단 풀블리드)

```html
<div style="
  background: var(--jc-primary);
  color: var(--jc-surface);
  padding: 24px 48px;
  display: flex;
  justify-content: space-between;
  align-items: center;
">
  <div>
    <div style="font-size: 12px; opacity: 0.7;">2026 / Q1</div>
    <div style="font-size: 20px; font-weight: 600;">제안서 타이틀</div>
  </div>
  <div style="font-size: 12px; opacity: 0.7;">{{client_name}}</div>
</div>
```

### 5.2 표지 (Dark 모드 풀블리드)

```html
<div style="
  background: var(--jc-primary);
  color: var(--jc-surface);
  padding: 80px 64px;
  min-height: 540px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
">
  <!-- 상단: 클라이언트 -->
  <div>
    <div style="
      font-size: 12px;
      letter-spacing: 0.1em;
      opacity: 0.6;
    ">FOR {{client_name}}</div>
  </div>
  
  <!-- 중앙: 타이틀 -->
  <div>
    <div style="
      font-size: 14px;
      color: var(--jc-accent);
      letter-spacing: 0.05em;
      margin-bottom: 16px;
    ">PROPOSAL</div>
    <div style="
      font-size: 56px;
      font-weight: 700;
      line-height: 1.1;
    ">{{document_title}}</div>
    <div style="
      width: 48px;
      height: 4px;
      background: var(--jc-accent);
      margin-top: 24px;
    "></div>
  </div>
  
  <!-- 하단: 메타 -->
  <div style="
    font-size: 12px;
    opacity: 0.6;
    display: flex;
    justify-content: space-between;
  ">
    <span>{{author_name}} / {{author_title}}</span>
    <span>{{date}}</span>
  </div>
</div>
```

### 5.3 푸터

```html
<div style="
  border-top: 0.5px solid var(--jc-border);
  padding: 16px 48px;
  font-size: 11px;
  color: var(--jc-text-muted);
  display: flex;
  justify-content: space-between;
">
  <span>© 2026. All rights reserved.</span>
  <span>Page {{page_num}} / {{total_pages}}</span>
</div>
```

---

## 6. 배지·태그·라벨

### 6.1 상태 배지

```html
<!-- 진행중 -->
<span style="
  display: inline-block;
  background: var(--jc-accent-soft);
  color: var(--jc-accent-strong);
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: var(--jc-radius-pill);
">진행중</span>

<!-- 핫 (Orange) -->
<span style="
  background: #FFF0EC;
  color: #C7401A;
  /* 나머지 동일 */
">우선순위 핫</span>

<!-- 완료 -->
<span style="
  background: #E8F8EE;
  color: #00873D;
">완료</span>
```

---

## 7. 인용·콜아웃

```html
<div style="
  border-left: 3px solid var(--jc-accent);
  background: var(--jc-accent-soft);
  padding: 16px 20px;
  border-radius: 0 var(--jc-radius-md) var(--jc-radius-md) 0;
  margin: 24px 0;
">
  <div style="
    font-size: 11px;
    font-weight: 600;
    color: var(--jc-accent-strong);
    letter-spacing: 0.05em;
    margin-bottom: 8px;
  ">KEY POINT</div>
  <div style="
    font-size: 15px;
    color: var(--jc-text);
    line-height: 1.6;
  ">핵심 메시지 본문 영역</div>
</div>
```

---

## 8. 컴포넌트 동시 사용 규칙

| 규칙 | 한도 |
|------|------|
| 한 화면 KPI 카드 동시 노출 | 최대 4개 (한 행) |
| 차트 시리즈 동시 사용 | 최대 3종 |
| 포인트 컬러 동시 사용 | 최대 3종 |
| 페이지당 강조 컴포넌트 (콜아웃·배지) | 최대 2개 |
| 페이지당 헤딩 레벨 | H1=1, H2=무제한, H3=H2당 5개 권장 |

원칙: 시각 노이즈 최소화. 한 화면에 강조 요소가 너무 많으면 모두 평준화된다.
