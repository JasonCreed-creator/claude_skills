# Design Tokens Mapping — jc-design-system → HTML/PPTX 매핑

본 스킬은 디자인 토큰을 직접 정의하지 않는다. **jc-design-system** 시그니처 토큰을 HTML/PPTX 산출물 영역별로 매핑하는 룰만 정의한다.

---

## 1. 의존성

본 매핑 룰은 다음 jc-design-system 파일을 의존한다:

- `jc-design-system/references/signature-tokens.md` — 시그니처 토큰 (변경 금지)
- `jc-design-system/references/client-overlays.md` — 클라이언트 오버레이 룰
- `jc-design-system/references/component-patterns.md` — 컴포넌트 패턴

빌드 시 해당 파일을 먼저 로드하고 본 매핑 룰을 적용한다.

---

## 2. 컬러 매핑 룰

### 2.1 영역별 토큰 매핑

| 영역 | 토큰 | HEX (시그니처) | 비고 |
|------|------|---------------|------|
| 표지 배경 | `--jc-primary` | `#0A2540` | Deep Navy |
| 표지 텍스트 | `--jc-surface` | `#FFFFFF` | 흰색 본문 |
| 일반 슬라이드 배경 | `--jc-bg` | `#F8F9FB` | 페이지 배경 |
| 일반 슬라이드 카드 | `--jc-surface` | `#FFFFFF` | 카드 배경 |
| 본문 텍스트 | `--jc-text` | `#1A1D24` | Charcoal |
| 보조 텍스트 | `--jc-text-muted` | `#5A6270` | 캡션·각주 |
| 메인 액센트·CTA | `--jc-accent` | `#2962FF` | Electric Blue |
| 섹션 헤더 강조 | `--jc-accent` | `#2962FF` | 좌측 액센트 막대 |
| KPI 숫자 강조 | `--jc-accent` | `#2962FF` | 큰 숫자 |
| 차트 메인 시리즈 | `--jc-data-1` | `#2962FF` | Electric Blue |
| 차트 보조 시리즈 | `--jc-data-2` ~ `--jc-data-5` | (시리즈 5색) | |
| 구분선·테두리 | `--jc-border` | `#E5E8ED` | 기본 보더 |

### 2.2 Tier 색상 매핑 (특별 룰)

각 Tier는 시각적으로 구분되어야 한다. 다음 매핑 사용:

| Tier | 토큰 | HEX |
|------|------|-----|
| T1 Title | `--jc-point-magenta` | `#E91E63` |
| T2 Platinum | `--jc-accent` | `#2962FF` |
| T3 Gold | `--jc-point-orange` | `#FF5722` |
| T4 Silver | `--jc-text-muted` | `#5A6270` |
| T5 Bronze | `--jc-border-strong` | `#C9CFD8` |
| T6 In-kind | `--jc-point-neon` | `#00E676` |

**T1에 Magenta를 매핑하는 이유:** 시그니처 토큰의 Track B(독립 전략가) 강조 컬러로 정의된 Magenta는 차별화·최상위 강조 컬러다. Title Sponsor의 격에 부합.

**T5에 Border-strong을 매핑하는 이유:** Bronze는 절제된 톤이 적합. 진한 회색(border-strong)이 Bronze의 격조와 진입 장벽 낮은 느낌을 동시에 표현.

### 2.3 시맨틱 컬러 사용

| 영역 | 토큰 | 용도 |
|------|------|------|
| 매트릭스 ✓ 셀 | `--jc-success` (`#00C853`) | 제공 표시 |
| 매트릭스 — 셀 | `--jc-text-disabled` (`#A0A6B0`) | 미제공 표시 |
| TBD/잠정 표시 | `--jc-warning` (`#FFA000`) | 미확정 강조 |
| 마감 임박 표시 | `--jc-danger` (`#D32F2F`) | CTA 긴급성 |

---

## 3. 타이포그래피 매핑

### 3.1 HTML 환경

```css
:root {
  --jc-font-ko: 'Pretendard', 'Pretendard Variable', -apple-system, 
                BlinkMacSystemFont, 'Apple SD Gothic Neo', 
                'Malgun Gothic', sans-serif;
  --jc-font-en: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --jc-font-mono: 'JetBrains Mono', 'D2Coding', 
                  'Consolas', 'Monaco', monospace;
  --jc-font-heading: 'Pretendard', 'Inter', -apple-system, sans-serif;
}
```

Pretendard 웹폰트는 CDN 임포트 권장:

```html
<link rel="stylesheet" 
  href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.min.css">
```

### 3.2 PPTX 환경

| 영역 | 권장 폰트 | 폴백 |
|------|----------|------|
| 한글 본문 | `Pretendard` | `맑은 고딕` (Windows) / `Apple SD Gothic Neo` (Mac) |
| 영문 본문 | `Inter` | `Helvetica Neue` / `Arial` |
| KPI 숫자 | `JetBrains Mono` | `Consolas` / `Courier New` |

**중요:** PPTX는 폰트가 임베드되지 않으면 수신자 환경에서 깨질 수 있음. pptxgenjs로 생성 시 다음 룰 적용:

- 표준 환경에서 가장 안전한 한글 폰트는 `맑은 고딕` 또는 `Pretendard`
- Pretendard 미설치 환경 대응을 위해 폴백 명시
- 시스템 폰트 우선 옵션 제공 (사용자 선택)

### 3.3 사이즈 매핑 (HTML/PPTX 공통)

| 슬라이드 영역 | 토큰 | px (HTML) | pt (PPTX) |
|-------------|------|-----------|-----------|
| 표지 메인 타이틀 | `--jc-text-5xl` | 56px | 44pt |
| 슬라이드 타이틀 | `--jc-text-4xl` | 44px | 32pt |
| 섹션 헤더 | `--jc-text-3xl` | 36px | 24pt |
| 서브타이틀 | `--jc-text-2xl` | 28px | 20pt |
| 본문 (큰) | `--jc-text-xl` | 22px | 16pt |
| 본문 (기본) | `--jc-text-lg` | 18px | 14pt |
| 본문 (작은) | `--jc-text-base` | 16px | 12pt |
| 캡션·각주 | `--jc-text-sm` | 14px | 10pt |
| 메타·미니 | `--jc-text-xs` | 12px | 9pt |

**HTML→PPTX 사이즈 변환 비율:** 대략 0.75배 (16px ≈ 12pt)

### 3.4 KPI 숫자 강조

KPI 숫자(예: "5,200명", "32%")는 다음 스타일 적용:

```css
.kpi-number {
  font-family: var(--jc-font-mono);  /* JetBrains Mono */
  font-size: var(--jc-text-3xl);     /* 36px */
  font-weight: 600;                  /* semibold */
  color: var(--jc-accent);           /* Electric Blue */
  line-height: 1.2;
}
```

---

## 4. 간격 매핑

jc-design-system 4px base 8단계 사용.

### 4.1 슬라이드 영역별 간격

| 영역 | 간격 | 값 |
|------|------|-----|
| 슬라이드 외부 마진 | `--jc-space-7` | 48px |
| 슬라이드 내부 패딩 | `--jc-space-6` | 32px |
| 섹션 간 분리 | `--jc-space-6` | 32px |
| 섹션 내 그룹 | `--jc-space-5` | 24px |
| 카드 패딩 | `--jc-space-4` | 16px |
| 카드 내 요소 | `--jc-space-3` | 12px |
| 인라인 미세 | `--jc-space-2` | 8px |

### 4.2 PPTX 변환 룰

PPTX는 px이 아니라 inch 단위. 다음 변환:

- 1 inch = 96 px (표준)
- 슬라이드 외부 마진 48px → 약 0.5 inch
- 슬라이드 내부 패딩 32px → 약 0.33 inch

---

## 5. 모서리·그림자 매핑

### 5.1 모서리 (radius)

| 영역 | 토큰 | 값 |
|------|------|-----|
| 배지·태그 | `--jc-radius-sm` | 4px |
| 버튼·작은 카드 | `--jc-radius-md` | 8px |
| 카드 (기본) | `--jc-radius-lg` | 12px |
| 큰 컨테이너 | `--jc-radius-xl` | 16px |

PPTX는 모서리 둥글기 표현이 제한적. 카드는 `roundedRect` 도형 사용.

### 5.2 그림자

평면 디자인 우선. 그림자는 카드 호버에만 사용 (HTML 한정). PPTX에서는 그림자 사용 안 함.

```css
.card:hover {
  box-shadow: var(--jc-shadow-sm);  /* 0 1px 2px rgba(10, 37, 64, 0.06) */
}
```

---

## 6. 컴포넌트 패턴 적용

다음 컴포넌트는 jc-design-system 의 component-patterns.md 패턴을 그대로 적용한다.

### 6.1 KPI 카드

```
┌─────────────────────────┐
│ 라벨 (xs muted)          │
│ 5,200명 (3xl mono accent)│
│ 캡션 (xs muted)          │
└─────────────────────────┘
배경: surface
보더: 0.5px border
패딩: space-4 (16px)
```

### 6.2 Tier 카드 (스폰서 데크 전용)

```
┌─────────────────────────┐
│ ▌ T1 Title              │ ← 좌측 3px 액센트 (Tier 색상)
│ 한정 1석                 │
│ KRW 100,000,000          │
│ ─────                   │
│ 핵심 혜택 3~5개 bullet    │
└─────────────────────────┘
```

좌측 액센트 막대 색상은 Tier별로 다름 (위 §2.2 참조).

### 6.3 매트릭스 표

```
헤더 행: surface-alt 배경 + text-muted
데이터 행: 짝수 행 surface, 홀수 행 surface-alt
✓ 셀: success 색상
— 셀: text-disabled 색상
정량 셀: text 기본 색상
```

### 6.4 ROI 3단 카드

```
┌─────────────────────────────────────┐
│ ■ 산업명 (Tier 색상 배지)            │
├─────────────────────────────────────┤
│ ① 전제 조건                         │
│   ─ 데이터 nudge                     │
│ ② 산출 공식                         │
│   ─ 공식 표시                       │
│ ③ 보수적 추정값                     │
│   ─ 결과 (큰 텍스트)                │
├─────────────────────────────────────┤
│ ⓘ 캡션 (xs muted)                   │
└─────────────────────────────────────┘
```

---

## 7. 차트 시리즈 매핑

차트 색상은 jc-design-system 의 데이터 시리즈 5색을 사용한다. 추가 시리즈가 필요하면 포인트 풀에서 선택.

### 7.1 산업 분포 도넛/바 차트

```
시리즈 5종 사용:
1순위 산업: --jc-data-1 (#2962FF)
2순위 산업: --jc-data-2 (#E91E63)
3순위 산업: --jc-data-3 (#FF5722)
4순위 산업: --jc-data-4 (#00E676)
5순위 산업: --jc-data-5 (#0A2540)
기타: --jc-text-muted (#5A6270)
```

### 7.2 직급 분포 가로 바 차트

```
C-Level + 임원 (강조): --jc-accent (#2962FF)
시니어 매니저: --jc-accent-soft (#E8EFFF)
매니저·실무자: --jc-text-muted (#5A6270)
```

C-Level+임원만 강조하는 이유: 의사결정권자 강조가 영업 핵심 메시지.

---

## 8. 클라이언트 오버레이 적용

`client_id` 가 지정된 경우 jc-design-system 의 `client-overlays.md` 룰을 따라 다음 3개 토큰을 오버라이드한다:

- `--jc-primary` (표지 배경)
- `--jc-accent` (메인 액센트·CTA)
- 로고

**Tier 색상은 오버라이드 대상이 아니다.** Tier 색상은 본 스킬 자체의 시각 언어이므로 클라이언트 변경 시 차별성·일관성이 깨진다.

### 8.1 클라이언트 오버레이 적용 예시

```
client_id = "remember"
↓
--jc-primary 오버라이드 → REMEMBER 브랜드 컬러
--jc-accent 오버라이드 → REMEMBER 강조 컬러
Tier 색상은 시그니처 그대로 유지
```

---

## 9. 회사 종속 표현 회피 (디자인 영역)

### 9.1 로고 처리

- 본 스킬 자체에는 어떤 회사 로고도 하드코딩하지 않음
- 클라이언트 토큰으로만 로고 주입
- `client_id = null` 상태에서는 로고 영역을 placeholder 또는 텍스트만 표시

### 9.2 표지 푸터

```
✓ "본 자료는 [행사명] 스폰서십 영업용으로 제작되었습니다."
❌ "© 엠앤씨커뮤니케이션즈"
❌ "M&C Communications"
```

자기 지칭 표현은 클라이언트 토큰으로만 표시.

---

## 10. 빠른 참조 — JSON 스키마

```json
{
  "color_mapping": {
    "cover_bg": "--jc-primary",
    "cover_text": "--jc-surface",
    "slide_bg": "--jc-bg",
    "card_bg": "--jc-surface",
    "body_text": "--jc-text",
    "muted_text": "--jc-text-muted",
    "accent": "--jc-accent",
    "kpi_number": "--jc-accent"
  },
  "tier_colors": {
    "T1": "--jc-point-magenta",
    "T2": "--jc-accent",
    "T3": "--jc-point-orange",
    "T4": "--jc-text-muted",
    "T5": "--jc-border-strong",
    "T6": "--jc-point-neon"
  },
  "size_html_to_pptx_ratio": 0.75,
  "client_overlay_targets": ["primary", "accent", "logo"],
  "tier_colors_overridable": false
}
```
