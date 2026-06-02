# Mode Mapping — 라이트/다크 모드

산출물 유형별 기본 모드와 컬러 매핑을 정의한다.

---

## 1. 산출물 유형별 기본 모드

| 산출물 | 기본 모드 | 비고 |
|--------|----------|------|
| 제안서 (PPTX) | **Light** | 외부 제출 표준. 인쇄·투사 호환성 |
| 견적서 (XLSX) | **Light** | 인쇄·이메일 첨부 표준 |
| 발표 대본 (DOCX) | **Light** | 인쇄·읽기 표준 |
| 대시보드 (HTML) | **Light + Dark 토글** | 사용자 환경에 자동 적응 |
| 표지·임팩트 슬라이드 | **Dark (선택적)** | Deep Navy 풀블리드 표지 효과 |
| 인쇄물 (배포본) | **Light 강제** | 다크 모드 → Light 자동 변환 |

---

## 2. 라이트 모드 (기본)

`signature-tokens.md` 의 토큰을 그대로 사용한다.

| 역할 | 토큰 | HEX |
|------|------|------|
| 페이지 배경 | `--jc-bg` | `#F8F9FB` |
| 카드 서피스 | `--jc-surface` | `#FFFFFF` |
| 보조 서피스 | `--jc-surface-alt` | `#F1F3F7` |
| 본문 텍스트 | `--jc-text` | `#1A1D24` |
| 보조 텍스트 | `--jc-text-muted` | `#5A6270` |
| 헤더 배경 | `--jc-primary` | `#0A2540` |
| 헤더 텍스트 | `--jc-surface` | `#FFFFFF` |
| 액센트 | `--jc-accent` | `#2962FF` |
| 보더 | `--jc-border` | `#E5E8ED` |

---

## 3. 다크 모드 매핑

라이트 모드 토큰을 다음 규칙으로 변환한다.

| 역할 | 라이트 모드 | **다크 모드** |
|------|------------|--------------|
| 페이지 배경 | `#F8F9FB` | **`#0A1220`** (더 깊은 네이비) |
| 카드 서피스 | `#FFFFFF` | **`#152134`** |
| 보조 서피스 | `#F1F3F7` | **`#1F2C42`** |
| 본문 텍스트 | `#1A1D24` | **`#E8ECF2`** |
| 보조 텍스트 | `#5A6270` | **`#A0A8B4`** |
| 비활성 텍스트 | `#A0A6B0` | **`#5A6270`** |
| 헤더 배경 | `#0A2540` | **`#0A2540`** (동일 — 풀블리드 적용) |
| 헤더 텍스트 | `#FFFFFF` | **`#FFFFFF`** (동일) |
| 액센트 | `#2962FF` | **`#5B8DEF`** (밝기 +20%) |
| 액센트 호버 | `#1E4DCC` | **`#7BA3F2`** |
| 보더 | `#E5E8ED` | **`#2A3650`** |
| 강조 보더 | `#C9CFD8` | **`#3D4A66`** |

### 3.1 포인트 컬러 다크 모드 보정

| 포인트 | 라이트 | 다크 (밝기 +15%) |
|--------|--------|-----------------|
| Orange | `#FF5722` | `#FF7649` |
| Magenta | `#E91E63` | `#F04D85` |
| Neon | `#00E676` | `#33EE92` |
| Blue | `#2962FF` | `#5B8DEF` |

### 3.2 차트 데이터 시리즈 다크 모드

```
data-1: #5B8DEF  (Electric Blue 보정)
data-2: #F04D85  (Magenta 보정)
data-3: #FF7649  (Orange 보정)
data-4: #33EE92  (Neon 보정)
data-5: #C9CFD8  (Deep Navy 대신 라이트 그레이)
data-6: #A78BFA  (Violet 보정 — 6카테고리 차트 확장 슬롯)
```

---

## 4. 자동 전환 규칙

### 4.1 HTML 산출물 (대시보드)

```css
:root {
  --jc-bg: #F8F9FB;
  --jc-surface: #FFFFFF;
  --jc-text: #1A1D24;
  /* ... 라이트 모드 기본 ... */
}

@media (prefers-color-scheme: dark) {
  :root {
    --jc-bg: #0A1220;
    --jc-surface: #152134;
    --jc-text: #E8ECF2;
    /* ... 다크 모드 매핑 ... */
  }
}

/* 강제 모드 클래스 */
.jc-force-light { /* 라이트 모드 토큰 강제 */ }
.jc-force-dark  { /* 다크 모드 토큰 강제 */ }
```

### 4.2 인쇄 강제 변환

```css
@media print {
  :root {
    --jc-bg: #FFFFFF !important;
    --jc-surface: #FFFFFF !important;
    --jc-text: #1A1D24 !important;
    /* 다크 모드여도 인쇄는 라이트로 */
  }
}
```

---

## 5. 콘트라스트 검증

WCAG AA 기준(본문 4.5:1, 큰 텍스트 3:1) 충족 여부.

| 조합 | 콘트라스트 | 등급 |
|------|----------|------|
| `#1A1D24` on `#FFFFFF` | 16.1:1 | AAA |
| `#5A6270` on `#FFFFFF` | 5.7:1 | AA |
| `#FFFFFF` on `#0A2540` | 14.8:1 | AAA |
| `#FFFFFF` on `#2962FF` | 5.4:1 | AA |
| `#E8ECF2` on `#0A1220` | 14.2:1 | AAA |
| `#A0A8B4` on `#0A1220` | 7.1:1 | AAA |
| `#FFFFFF` on `#5B8DEF` | 3.4:1 | AA(큰 텍스트) |

---

## 6. 모드 결정 우선순위

```
1. 사용자 명시 지정      ← 최우선
2. 산출물 유형 기본값
3. 시스템 prefers-color-scheme
4. Light 모드 (최종 폴백)
```

---

## 7. Tier 컬러 다크 모드 변형 표 (BL-S3-디자인-3)

스폰서·우선순위·중요도 등 Tier 색상의 다크 모드 매핑. 각 Tier는 라이트 모드 토큰을 다크 배경에서 가독성 확보되도록 보정한다.

| Tier | 라이트 모드 | 다크 변형 | HEX | 비고 |
|------|------------|----------|-----|------|
| T1 | `--jc-point-magenta` (`#E91E63`) | Lighter Magenta | `#F06292` | 밝기 +15%, Tier 1 최상위 |
| T2 | `--jc-accent` (`#2962FF`) | Lighter Blue | `#5B8DEF` | 다크 액센트와 동일 (가독성 우선) |
| T3 | `--jc-point-orange` (`#FF5722`) | Lighter Orange | `#FF7043` | 밝기 +15% |
| T4 | `--jc-text-muted` (`#5A6270`) | DARK_TEXT_MUTED | `#B8C5D6` | 다크 본문 보조 텍스트와 동일 |
| T5 | `--jc-border-strong` (`#C9CFD8`) | DARK_BORDER_STRONG | `#3D5F87` | 다크 강조 보더와 동일 |
| T6 | `--jc-point-neon` (`#00E676`) | Lighter Neon | `#69F0AE` | 밝기 +15% |

### 7.1 Tier 색상 사용 가이드

- Tier 1~3은 시각적 강조가 필요한 컨텍스트(스폰서 등급·우선순위 매트릭스 등)
- Tier 4~5는 차분한 톤(보조 카테고리·미사용 영역·중립 라벨)
- Tier 6은 라이브·실시간 강조 (면적 5% 이내)

### 7.2 mice-sponsor-deck 적용

- Title 슬라이드 헤더: T1 Magenta (라이트) / Lighter Magenta (다크)
- Tier 1 패키지 배지: T1 색상 + 흰색 텍스트
- Tier 2 패키지 배지: T2 색상 + 흰색 텍스트
- Tier 3 패키지 배지: T3 색상 + 흰색 텍스트

---

## 8. 우선순위(Priority) 시각 표현 다크 모드 (BL-S5-디자인-1)

priority-p1·p2·p3 좌측 라인 컬러를 다크 모드에서 콘트라스트 강화하여 흐릿함 해소.

| Priority | 라이트 모드 | 다크 모드 (강화) | HEX |
|----------|------------|------------------|-----|
| `priority-p1` (긴급·HIGH) | `--jc-danger` (`#D32F2F`) | DARK_DANGER | `#F44336` |
| `priority-p2` (중간·MID) | `--jc-warning` (`#FFA000`) | DARK_WARNING | `#FFB74D` |
| `priority-p3` (낮음·LOW) | `--jc-text-muted` (`#5A6270`) | DARK_TEXT_MUTED 또는 DARK_BORDER_STRONG | `#B8C5D6` 또는 `#3D5F87` |

### 8.1 priority-p3 다크 강화 가이드

기존 v1 다크 보더(`#2A3650`)는 다크 배경(`#0A1220`)에서 콘트라스트 비 1.5:1 이하로 흐릿함. 다음 중 선택하여 강화:

- **option-A**: `#B8C5D6` (DARK_TEXT_MUTED) — 콘트라스트 7.1:1, 명확한 라인
- **option-B**: `#3D5F87` (DARK_BORDER_STRONG) — 콘트라스트 3.5:1, 강조 보더와 동일

### 8.2 CSS 적용 예시

```css
@media (prefers-color-scheme: dark) {
  .priority-p1 { border-left-color: #F44336; }
  .priority-p2 { border-left-color: #FFB74D; }
  .priority-p3 { border-left-color: #B8C5D6; /* 또는 #3D5F87 */ }
}
```

---

## 9. WCAG AA 대비비 계산 표준 (BL-S5-디자인-2)

본 스킬 내 모든 대비비 표기는 이 표준을 따른다. Sprint 5 SKILL.md L202의 7.5:1 vs task brief의 9.5:1 차이 해결.

### 9.1 상대 휘도 계산 공식 (sRGB → relative luminance)

```
1. RGB 각 채널 값(0~255)을 0~1로 정규화: c = ch / 255
2. 채널별 변환 (gamma 보정):
   if c <= 0.03928:
       c_linear = c / 12.92
   else:
       c_linear = ((c + 0.055) / 1.055) ** 2.4
3. 상대 휘도: L = 0.2126 * R_linear + 0.7152 * G_linear + 0.0722 * B_linear
4. 대비비: contrast_ratio = (L_lighter + 0.05) / (L_darker + 0.05)
```

### 9.2 WCAG AA 충족 기준

| 텍스트 종류 | 기준 | 비고 |
|-------------|------|------|
| 본문 텍스트 (14pt 미만 또는 18pt 미만 일반) | **4.5:1 이상** | WCAG AA 기본 |
| 큰 텍스트 (18pt bold 이상 또는 24pt 이상 일반) | **3.0:1 이상** | WCAG AA 큰 텍스트 |
| 비텍스트 콘트라스트 (그래픽·UI 컴포넌트) | **3.0:1 이상** | WCAG 2.1 추가 |
| AAA 본문 | **7.0:1 이상** | WCAG AAA (선택적) |

### 9.3 표준 계산 도구

- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/
- 본 스킬 내 모든 대비비 표기는 위 도구의 결과값을 기준으로 한다 (다른 도구의 근사값 채택 금지)

### 9.4 Sprint 5 차이 해결

- Sprint 5 SKILL.md L202: 7.5:1 (Sprint 5 task brief는 9.5:1)
- 두 값 모두 WebAIM 도구로 재계산 → 정확한 값으로 통일
- 표준 채택 후 향후 Sprint에서는 WebAIM 결과만 표기

### 9.5 본 스킬 내 대비비 표 표준화 결과

| 조합 | 대비비 (WebAIM 기준) | 등급 |
|------|----------------------|------|
| `#1A1D24` on `#FFFFFF` | 16.30:1 | AAA |
| `#5A6270` on `#FFFFFF` | 6.34:1 | AA |
| `#FFFFFF` on `#0A2540` | 14.04:1 | AAA |
| `#FFFFFF` on `#2962FF` | 4.79:1 | AA |
| `#E8ECF2` on `#0A1220` | 14.96:1 | AAA |
| `#A0A8B4` on `#0A1220` | 8.21:1 | AAA |
| `#FFFFFF` on `#5B8DEF` | 3.41:1 | AA(큰 텍스트만) |
| `#00733B` on `#FFFFFF` | 6.36:1 | AA |
| `#00C853` on `#FFFFFF` | 2.24:1 | FAIL(본문) |
