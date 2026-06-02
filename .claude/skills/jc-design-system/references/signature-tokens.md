# Signature Tokens — JC 시그니처 (변경 금지)

이 파일의 토큰은 기획자님 개인 정체성이다. 클라이언트별 차별화는 `client-overlays.md` 에서 처리한다.

---

## 1. 컬러 팔레트

### 1.1 시그니처 베이스 (고정)

| 토큰 | HEX | RGB | 용도 |
|------|------|-----|------|
| `--jc-primary` | `#0A2540` | 10, 37, 64 | Deep Navy. 헤더·로고·신뢰 톤 |
| `--jc-primary-soft` | `#1A3556` | 26, 53, 86 | Primary 보조 변주 |
| `--jc-text` | `#1A1D24` | 26, 29, 36 | 본문 텍스트 (Charcoal) |
| `--jc-text-muted` | `#5A6270` | 90, 98, 112 | 보조 텍스트·캡션 |
| `--jc-text-disabled` | `#A0A6B0` | 160, 166, 176 | 비활성 텍스트 |
| `--jc-surface` | `#FFFFFF` | 255, 255, 255 | 카드·시트 배경 |
| `--jc-surface-alt` | `#F1F3F7` | 241, 243, 247 | 보조 서피스 |
| `--jc-bg` | `#F8F9FB` | 248, 249, 251 | 페이지 배경 |
| `--jc-border` | `#E5E8ED` | 229, 232, 237 | 구분선·테두리 |
| `--jc-border-strong` | `#C9CFD8` | 201, 207, 216 | 강조 테두리 |

### 1.2 시그니처 액센트 (메인)

| 토큰 | HEX | 용도 |
|------|------|------|
| `--jc-accent` | `#2962FF` | **Electric Blue. 메인 시그니처 액센트 — KPI 강조·CTA·링크·차트 메인 시리즈** |
| `--jc-accent-soft` | `#E8EFFF` | Accent 배경 톤 (배지·하이라이트) |
| `--jc-accent-strong` | `#1E4DCC` | Accent 호버·프레스드 상태 |

### 1.3 포인트 컬러 풀 (4종)

차트 보조 시리즈·카테고리 구분·핫스팟 강조에 사용.

| 토큰 | HEX | 용도 | 폴백 |
|------|------|------|------|
| `--jc-point-orange` | `#FF5722` | Vivid Orange. 핫 데이터·우선순위·경고 | — |
| `--jc-point-magenta` | `#E91E63` | Magenta. 차별화·브랜드 포인트·Track B 강조 | — |
| `--jc-point-neon` | `#00E676` | Neon Green. 성장·긍정·라이브 데이터 | `#00C853` (인쇄·구형 모니터) |
| `--jc-point-blue` | `#2962FF` | Electric Blue (액센트와 동일) | — |

### 1.4 차트 데이터 시리즈 (5단계 + 확장 data-6)

| 시리즈 | 토큰 | HEX |
|--------|------|------|
| `data-1` | `--jc-data-1` | `#2962FF` (Electric Blue) |
| `data-2` | `--jc-data-2` | `#E91E63` (Magenta) |
| `data-3` | `--jc-data-3` | `#FF5722` (Vivid Orange) |
| `data-4` | `--jc-data-4` | `#00E676` (Neon Green) |
| `data-5` | `--jc-data-5` | `#0A2540` (Deep Navy) |
| `data-6` | `--jc-data-6` | `#7C3AED` (Violet) |

> `data-1`~`data-5`가 기본 5색 정본. **`data-6`(`#7C3AED`)는 6카테고리 이상 차트 전용 확장 슬롯**으로, 5색으로 부족한 경우에만 사용한다(예: mice-dashboard 6시리즈). 다크 모드 보정값은 `mode-mapping.md §3.2` 참조.

### 1.5 시맨틱 컬러

| 토큰 | HEX | 용도 |
|------|------|------|
| `--jc-success` | `#00C853` | 성공·확정·목표 달성 |
| `--jc-warning` | `#FFA000` | 주의·검토 필요 |
| `--jc-danger` | `#D32F2F` | 위험·실패·취소 |
| `--jc-info` | `#2962FF` | 정보 (액센트 재사용) |

### 1.6 컬러 사용 규칙

- **Primary Accent (Electric Blue)** — 면적 제한 없음. KPI·CTA·링크·메인 차트 시리즈
- **Point Pool 4종** — 한 화면 동시 사용 최대 3종. 카테고리 구분·차트 보조 시리즈에만
- **Neon Green** — 면적 5% 이내. 인쇄물에서는 폴백 `#00C853` 자동 적용
- **Magenta** — Track B(독립 전략가) 퍼스널 브랜드 포인트 후보. 클라이언트 오버레이 시 우선순위 높음
- **Deep Navy** — 헤더·로고·핵심 강조 영역에 한정

### 1.7 확장 Variant 토큰 (v1.1.0 추가)

Sprint 1~6 누적 백로그(BL-S3-1, BL-S3-2, BL-S4-1) 반영. 시그니처 베이스의 light·soft·softest·strong variant.

| 토큰 | HEX | RGB | 용도 | 백로그 ID |
|------|------|-----|------|-----------|
| `--jc-accent-light` | `#5B9BD5` | 91, 155, 213 | Accent의 light variant. 퍼널 단계 컬러·옅은 차트 시리즈·SVP-6 패턴 | BL-S3-디자인-1 |
| `--jc-point-orange-softest` | `#FFF3E0` | 255, 243, 224 | Point Orange의 softest variant. 옅은 배경·매트릭스 4사분면·SVP-7 Q4 | BL-S3-디자인-2 |
| `--jc-point-magenta-soft` | `#FCE4EC` | 252, 228, 236 | Point Magenta의 softest variant. 배지·하이라이트 배경 | (Sprint 3 보조) |
| `--jc-success-strong` | `#00733B` | 0, 115, 59 | Success의 진한 variant. WCAG AA 본문 컬러 4.5:1+ 충족. Q&A 답변 레이블 | BL-S4-디자인-1 |

#### 1.7.1 사용 컨텍스트

- **`--jc-accent-light`**: 차트 보조 시리즈(메인 액센트와 구분 필요), 퍼널 단계 색상의 옅은 톤(예: 5단계 퍼널의 2~4단계), SVP-6 인포그래픽 패턴
- **`--jc-point-orange-softest`**: 매트릭스 사분면 배경 색상(BCG/SVP-7 Q4 영역), Orange 시맨틱이지만 텍스트 가독성을 위한 옅은 배경
- **`--jc-point-magenta-soft`**: Magenta 배지·하이라이트 영역의 배경 컬러. 텍스트는 `--jc-point-magenta` 또는 `--jc-text` 사용
- **`--jc-success-strong`**: 흰색 배경 위 본문 텍스트로 사용 시 WCAG AA 본문 4.5:1+ 충족. Q&A 예상 답변 레이블·검증 통과 표시·체크리스트 항목 등

#### 1.7.2 WCAG AA 대비비

| 조합 | 대비비 | 등급 |
|------|--------|------|
| `#00733B` on `#FFFFFF` | 6.36:1 | AA(본문) / AAA(큰 텍스트) |
| `#00C853` on `#FFFFFF` | 2.24:1 | FAIL(본문) — `--jc-success-strong` 사용 권장 |
| `#5B9BD5` on `#FFFFFF` | 3.04:1 | AA(큰 텍스트만) |
| `#FFF3E0` on `#1A1D24` | 14.8:1 | AAA (배경+짙은 텍스트 조합) |

#### 1.7.3 다크 모드 매핑

| Light | Dark 변형 | 비고 |
|-------|----------|------|
| `--jc-accent-light` `#5B9BD5` | `#7EB6E8` | 밝기 +15% |
| `--jc-point-orange-softest` `#FFF3E0` | `#3D2E1A` | 짙은 오렌지 톤 배경 |
| `--jc-point-magenta-soft` `#FCE4EC` | `#3D1F2A` | 짙은 마젠타 톤 배경 |
| `--jc-success-strong` `#00733B` | `#33C272` | 다크에서는 밝은 그린으로 |

---

## 2. 타이포그래피

### 2.1 폰트 스택 (폴백 체인 포함)

```css
/* 한글 본문 */
--jc-font-ko: 'Pretendard', 'Pretendard Variable', -apple-system, 
              BlinkMacSystemFont, 'Apple SD Gothic Neo', 
              'Malgun Gothic', sans-serif;

/* 영문 본문 */
--jc-font-en: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;

/* 숫자·데이터 (모노스페이스) */
--jc-font-mono: 'JetBrains Mono', 'IBM Plex Mono', 'D2Coding', 
                'Consolas', 'Monaco', monospace;

/* 통합 헤딩 (한글·영문 혼용) */
--jc-font-heading: 'Pretendard', 'Inter', -apple-system, sans-serif;
```

### 2.2 폰트 굵기

| 토큰 | 값 | 용도 |
|------|-----|------|
| `--jc-weight-regular` | 400 | 본문 |
| `--jc-weight-medium` | 500 | 라벨·강조 본문 |
| `--jc-weight-semibold` | 600 | 헤딩·KPI 숫자 |
| `--jc-weight-bold` | 700 | 페이지 타이틀·표지 |

### 2.3 폰트 미설치 시 폴백 정책

- PPTX·DOCX 환경에서 Pretendard 미설치 → `Apple SD Gothic Neo`(Mac) / `Malgun Gothic`(Windows)
- JetBrains Mono 미설치 → `D2Coding` → `Consolas` → 시스템 monospace

---

## 3. 사이즈 스케일

**Major Third (1.250) 비율 적용. base 16px 기준.**

| 토큰 | 값 | 용도 |
|------|-----|------|
| `--jc-text-xs` | 12px | 캡션·각주·메타 |
| `--jc-text-sm` | 14px | 보조 텍스트·테이블 |
| `--jc-text-base` | 16px | 본문 (기본) |
| `--jc-text-lg` | 18px | 강조 본문·서브타이틀 |
| `--jc-text-xl` | 22px | H4·소제목 |
| `--jc-text-2xl` | 28px | H3·섹션 타이틀 |
| `--jc-text-3xl` | 36px | H2·KPI 숫자 |
| `--jc-text-4xl` | 44px | H1·페이지 타이틀 |
| `--jc-text-5xl` | 56px | 표지·임팩트 (선택적) |

### 3.1 라인 하이트

| 토큰 | 값 | 용도 |
|------|-----|------|
| `--jc-leading-tight` | 1.2 | 헤딩·KPI 숫자 |
| `--jc-leading-normal` | 1.5 | 본문 (기본) |
| `--jc-leading-relaxed` | 1.7 | 긴 본문·아티클 |

---

## 4. 간격 규칙

**4px base. 8 단계.**

| 토큰 | 값 | 용도 |
|------|-----|------|
| `--jc-space-1` | 4px | 인라인 미세 간격 |
| `--jc-space-2` | 8px | 컴포넌트 내부 |
| `--jc-space-3` | 12px | 카드 내부 요소 간격 |
| `--jc-space-4` | 16px | 카드 패딩 (기본) |
| `--jc-space-5` | 24px | 섹션 내 그룹 간격 |
| `--jc-space-6` | 32px | 섹션 간격 |
| `--jc-space-7` | 48px | 페이지 섹션 분리 |
| `--jc-space-8` | 64px | 챕터 분리·표지 마진 |

---

## 5. 보더·라운드·그림자

### 5.1 모서리

| 토큰 | 값 | 용도 |
|------|-----|------|
| `--jc-radius-sm` | 4px | 배지·태그 |
| `--jc-radius-md` | 8px | 버튼·인풋·작은 카드 |
| `--jc-radius-lg` | 12px | 카드 (기본) |
| `--jc-radius-xl` | 16px | 큰 컨테이너·모달 |
| `--jc-radius-pill` | 9999px | 필 형태 배지 |

### 5.2 보더 두께

- 기본: `0.5px solid var(--jc-border)`
- 강조: `1px solid var(--jc-border-strong)`
- 액센트 라인 (좌측 강조 막대): `3px solid var(--jc-accent)` 또는 포인트 컬러

### 5.3 그림자 (최소 사용)

```css
--jc-shadow-none: none;
--jc-shadow-sm: 0 1px 2px rgba(10, 37, 64, 0.06);   /* 호버·플로팅 */
--jc-shadow-md: 0 2px 8px rgba(10, 37, 64, 0.08);   /* 모달·드롭다운 */
```

원칙: 평면 디자인 우선. 그림자는 인터랙션 피드백 한정.

---

## 6. JSON 추출 (다른 스킬용)

다른 스킬이 기계 파싱할 수 있도록 토큰 JSON 표현을 동봉한다.

```json
{
  "color": {
    "primary": "#0A2540",
    "primarySoft": "#1A3556",
    "text": "#1A1D24",
    "textMuted": "#5A6270",
    "textDisabled": "#A0A6B0",
    "surface": "#FFFFFF",
    "surfaceAlt": "#F1F3F7",
    "bg": "#F8F9FB",
    "border": "#E5E8ED",
    "borderStrong": "#C9CFD8",
    "accent": "#2962FF",
    "accentSoft": "#E8EFFF",
    "accentStrong": "#1E4DCC",
    "accentLight": "#5B9BD5",
    "point": {
      "orange": "#FF5722",
      "orangeSoftest": "#FFF3E0",
      "magenta": "#E91E63",
      "magentaSoft": "#FCE4EC",
      "neon": "#00E676",
      "neonFallback": "#00C853",
      "blue": "#2962FF"
    },
    "data": ["#2962FF", "#E91E63", "#FF5722", "#00E676", "#0A2540", "#7C3AED"],
    "semantic": {
      "success": "#00C853",
      "successStrong": "#00733B",
      "warning": "#FFA000",
      "danger": "#D32F2F",
      "info": "#2962FF"
    }
  },
  "font": {
    "ko": "Pretendard, -apple-system, 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif",
    "en": "Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif",
    "mono": "'JetBrains Mono', 'D2Coding', Consolas, monospace",
    "heading": "Pretendard, Inter, -apple-system, sans-serif"
  },
  "weight": { "regular": 400, "medium": 500, "semibold": 600, "bold": 700 },
  "size": {
    "xs": 12, "sm": 14, "base": 16, "lg": 18,
    "xl": 22, "2xl": 28, "3xl": 36, "4xl": 44, "5xl": 56
  },
  "leading": { "tight": 1.2, "normal": 1.5, "relaxed": 1.7 },
  "space": { "1": 4, "2": 8, "3": 12, "4": 16, "5": 24, "6": 32, "7": 48, "8": 64 },
  "radius": { "sm": 4, "md": 8, "lg": 12, "xl": 16, "pill": 9999 }
}
```
