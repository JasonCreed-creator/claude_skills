# Signature Tokens — 리멤버 웜 페이퍼 (정본)

이 파일의 값이 모든 산출물 디자인의 단일 진실 공급원이다. 기계 파싱은 §6 JSON(`scripts/jc_tokens.py`).
출처: `remember-proposal-ds/packages/tokens/css/*.css`(Claude Design DS, 2026 고객 행사 제안서 51장 실측) + 구 리멤버 HTML 스킬 v1.0.0(본 스킬로 흡수) + 팀 보드·플레이북 HTML 실전 CSS. 같은 역할의 값이 소스마다 미세하게 달랐던 경우 DS 값을 정본으로 택하고 나머지는 별칭으로 기록했다.

---

## 1. 컬러

### 1.1 캔버스·서피스 (웜 페이퍼)

| 토큰 | HEX | 용도 |
|------|-----|------|
| `--rm-canvas` | `#FBFAF6` | 페이지·슬라이드 배경 |
| `--rm-card` | `#FFFFFF` | 카드·패널·표 본문 |
| `--rm-surface-2` | `#F4F1EA` | 표 헤더·인풋·바 트랙·서브 밴드 (별칭 surface-warm) |
| `--rm-surface-3` | `#EFEBE2` | 표 행 구분·아주 옅은 면 (별칭 line-soft) |
| `--rm-border` | `#DCD6C8` | 카드 경계·표 행 보더 |
| `--rm-border-strong` | `#CFC8BC` | 강조 보더·hover 보더 |
| `--rm-line` | `#C9C9C0` | 차트 보조 그리드·시계열 과거 톤 |

### 1.2 잉크

| 토큰 | HEX | 용도 |
|------|-----|------|
| `--rm-ink` | `#1A1A1A` | 본문·헤드라인·표 첫 열 |
| `--rm-ink-2` | `#4A463F` | 보조 본문·표 값·서브 잉크 (별칭 brown) |
| `--rm-ink-3` | `#6E6E6E` | 뮤트 텍스트·서브 헤드라인 (별칭 ink-sub) |
| `--rm-caption` | `#8C867A` | 캡션·단위·푸터·플레이스홀더 (별칭 warm-gray). 본문 금지(3.6:1) |

### 1.3 액센트 (리멤버 오렌지)

| 토큰 | HEX | 용도 |
|------|-----|------|
| `--rm-accent` | `#EB6F2A` | 주 액센트. 면 채움·큰 텍스트 강조·아이브로우·차트 S1 |
| `--rm-accent-deep` | `#B8431A` | 작은 강조 텍스트·링크·hover·배지 텍스트 (AA 5.45:1) |
| `--rm-accent-light` | `#F5A05A` | 그라디언트 종점·다크 위 라벨 |
| `--rm-accent-soft` | `#F3B48A` | 차트 S5·타임라인 룰·옅은 강조 (별칭 orange-pale) |
| `--rm-accent-tint` | `#FFF1E6` | 하이라이트 면·배지 배경·테이크어웨이 바 |
| `--rm-accent-on-dark` | `#F08A4C` | 다크 배경 위 오렌지 텍스트 |
| `--rm-gradient` | `linear-gradient(135deg, #EB6F2A 0%, #F5A05A 100%)` | 슬라이드·화면당 1회 |
| `--rm-gradient-deep` | `linear-gradient(135deg, #E8641F, #F5A05A)` | 섹션 디바이더 풀블리드 변형 |

### 1.4 보조·상태

| 토큰 | HEX | 용도 |
|------|-----|------|
| `--rm-steel` | `#476580` | 보조 액센트·정보·차트 S2 |
| `--rm-steel-tint` | `#E8EEF3` | 스틸 배지 배경 |
| `--rm-positive` | `#196B24` | 긍정 지표·완료 (배경 `#E7EFE8`) |
| `--rm-negative` | `#D93636` | 부정 지표·경고·지연 (배경 `#FBE9E9`) |
| `--rm-amber` | `#D39A1F` | 주의·검토 (배경 `#FBF2DF`). 단독 텍스트 금지(2.5:1) — 배지 배경+잉크 텍스트로만 |

### 1.5 다크

표지·섹션 구분·클로징 슬라이드와 대시보드 다크 토글에만 쓴다. 매핑 규칙은 `mode-mapping.md §3`.

| 토큰 | HEX | 용도 |
|------|-----|------|
| `--rm-dark-bg` | `#141210` | 다크 슬라이드 스테이지·오브제 배경 |
| `--rm-dark-panel` | `#211E1A` | 본문 슬라이드 안의 다크 패널·대시보드 다크 캔버스 |
| `--rm-charcoal` | `#332F29` | 사진 위 패널·캡슐 프로필·DROP 바 |
| `--rm-dark-surface` | `#2A2620` | 다크 카드 |
| `--rm-dark-border` | `#3E3931` | 다크 카드 보더 |
| `--rm-dark-ink` | `#F4F0E9` | 다크 위 본문 |
| `--rm-dark-muted` | `#CFC8BC` | 다크 위 보조 |
| `--rm-dark-sub` | `#A89F92` | 다크 위 뮤트 |
| `--rm-dark-dim` | `#6E655A` | 다크 위 캡션·푸터 |
| `--rm-dark-line` | `rgba(255,255,255,0.6)` | 표지 프레임 룰 (1.5px) |
| `--rm-dark-line-soft` | `rgba(255,255,255,0.14)` | 다크 구분선 |

### 1.6 차트 시리즈 (순서 고정)

| 시리즈 | HEX | 역할 |
|--------|-----|------|
| S1 | `#EB6F2A` | 주인공 (오렌지는 하나만) |
| S2 | `#476580` | 비교군 1 |
| S3 | `#4A463F` | 비교군 2 |
| S4 | `#8C867A` | 비교군 3 |
| S5 | `#F3B48A` | 옅은 보조 |
| S6 (확장) | `#D39A1F` | 6카테고리 이상일 때만 |

시계열 강조: 과거 `#C9C9C0` → `#8C867A` → `#4A463F` → 현재 `#EB6F2A`. 증감은 positive/negative. 축·기준선 잉크 2px, 트랙 `#F4F1EA` r4. 3D·그림자·그라디언트 차트 금지.

### 1.7 단계 스케일 (히트맵·매트릭스·퍼널)

연속 단계 표현에만 쓴다. 카테고리 구분은 §1.6 시리즈가 우선.

| 스케일 | deep → bg |
|--------|-----------|
| orange | `#B8431A` · `#EB6F2A` · `#F5A05A` · `#F3B48A` · `#FFF1E6` |
| steel | `#476580` · `#8FAEC7` · `#E8EEF3` |
| green | `#196B24` · `#6FBF7C` · `#E7EFE8` |
| red | `#D93636` · `#F07A7A` · `#FBE9E9` |
| amber | `#D39A1F` · `#E2B558` · `#FBF2DF` |
| gray(시계열) | `#C9C9C0` · `#8C867A` · `#4A463F` · `#EB6F2A` |

---

## 2. 타이포그래피

- 서체: `'Pretendard Variable', Pretendard, -apple-system, 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif` — 한글·영문 공용. CDN `cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9`. PPTX·DOCX 미설치 폴백 Malgun Gothic.
- 모노(토큰값·타임코드·코드): `'JetBrains Mono', 'D2Coding', Consolas, monospace`.
- 웨이트: Regular 400 · Semibold 600(표 첫 열·단위·라벨) · Bold 700(헤드라인·KPI). Medium 500은 UI 라벨.
- 헤드라인 자간 -0.01em, 아이브로우·영문 라벨 +0.18em 대문자, 태그 +0.10em.
- 숫자는 항상 `font-variant-numeric: tabular-nums`, 단위는 캡션색으로 분리(`12,480` + ` 명`).

### 2.1 문서·대시보드 스케일 (1.250 Major Third)

| 토큰 | px | 용도 |
|------|----|------|
| xs | 12 | 캡션·각주 |
| sm | 14 | 보조·표 |
| base | 16 | 본문 (line-height 1.6~1.7) |
| lg | 20 | H4 |
| xl | 25 | H3·문서 제목 |
| 2xl | 31 | H2·KPI 소 |
| 3xl | 39 | H1 |
| 4xl | 49 | 디스플레이·KPI 대 |

### 2.2 덱 스케일 (1920×1080 px ↔ 13.33×7.5 in pt)

1920px 캔버스 1px = 0.5pt. python-pptx 좌표는 pt 열을 쓴다.

| 역할 | px | pt |
|------|----|----|
| cover | 88 | 44 |
| kpi | 96 | 48 |
| headline | 64 | 32 |
| title | 44 | 22 |
| subtitle | 30 | 15 |
| body | 26 | 13 |
| small | 22 | 11 |
| eyebrow | 22 | 11 |
| caption | 18 | 9 |

최소 18px(9pt). 본문 26px는 "읽기용 밀도와 발표용 크기의 절충"(DS 브랜드 가이드).

---

## 3. 간격 · 라운드 · 그림자 · 프레임

- 간격 base 4px: 4 / 8 / 12 / 16 / 20 / 24 / 32 / 40 / 48 / 64 / 80 / 96
- 라운드: 버튼 r6 · 카드 r10~12 · 배지 pill(999)
- 그림자: 대시보드 카드 `0 2px 12px rgba(74,70,63,0.08)` 한 단계. DS 카드 hairline `0 1px 2px rgba(74,70,63,0.08)`. 다크 패널 강조 `0 12px 32px rgba(33,30,26,0.35)`. 슬라이드는 플랫.
- 문서 그리드: 12col · gutter 24 · content 1100~1240. 패딩 상하 32 / 좌우 36.
- 덱 프레임(1920×1080): 좌우 마진 90 · eyebrow y72 · headline y130 · sub y236 · 콘텐츠 y340~1000 · 푸터 y1017 · 카드 간격 28. 푸터 = 좌 행사명 · 중앙 페이지 · 우 로고.

---

## 4. 로고 · 오브제

- 로고타입 2종(재염색·왜곡 금지, 최소 높이 16px, 클리어스페이스 R 높이의 1/2): `assets/remember-black.png`(라이트) · `assets/remember-offwhite.png`(다크).
- 오브제 7점 — 다크 슬라이드 히어로 전용, 슬라이드당 1점, 텍스트는 반대편 여백:

| ID | 파일 | 용도 |
|----|------|------|
| OBJ-01 | objet-01-bulb.png | 아이디어·인사이트 타이틀 |
| OBJ-02 | objet-02-torn.png | 전환·대비 디바이더 |
| OBJ-03 | objet-03-slit.png | 표지 배경 (DS 01-cover 정본) |
| OBJ-04 | objet-04-glow.png | 클로징·배경 그라디언트 |
| OBJ-05 | objet-05-ribbed.png | 데이터 섹션 텍스처 |
| OBJ-06 | objet-06-coil.png | 구조·프로세스·클로징(DS 10-closing) |
| OBJ-07 | objet-07-sphere.png | 데이터·네트워크 |

배경 레시피: `linear-gradient(90deg, rgba(20,18,16,0.72), rgba(20,18,16,0.25)), url(objet)` — 텍스트 쪽 오버레이를 더 진하게.

---

## 5. 컬러 사용 규칙

- 오렌지 면(그라디언트·솔리드 KPI·다크 패널)은 슬라이드당 1회. 나머지 강조는 딥 오렌지 텍스트·틴트 배경·오렌지 룰(3~4px)로.
- 오렌지 텍스트는 24px+ 또는 18px+ Bold에서만(카드 위 3.07:1, 캔버스 위 2.94:1). 작은 글자는 `#B8431A`.
- Steel은 정보성·비교군에만. 상태색은 표 셀·배지 안에서만.
- 다크 슬라이드는 덱 전체의 30% 이하.
- 발주처 색을 받아도 오렌지를 바꾸지 않는다(`client-overlays.md`).

---

## 6. JSON 추출 (기계 파싱 정본)

```json
{
  "brand": "remember",
  "version": "2.1.0",
  "color": {
    "bg": "#FBFAF6",
    "surface": "#FFFFFF",
    "surfaceAlt": "#F4F1EA",
    "surfaceSoft": "#EFEBE2",
    "border": "#DCD6C8",
    "borderStrong": "#CFC8BC",
    "line": "#C9C9C0",
    "text": "#1A1A1A",
    "textSecondary": "#4A463F",
    "textMuted": "#6E6E6E",
    "textCaption": "#8C867A",
    "textDisabled": "#8C867A",
    "primary": "#1A1A1A",
    "primarySoft": "#332F29",
    "accent": "#EB6F2A",
    "accentStrong": "#B8431A",
    "accentLight": "#F5A05A",
    "accentSoftLine": "#F3B48A",
    "accentSoft": "#FFF1E6",
    "accentOnDark": "#F08A4C",
    "gradient": "linear-gradient(135deg, #EB6F2A 0%, #F5A05A 100%)",
    "gradientDeep": "linear-gradient(135deg, #E8641F, #F5A05A)",
    "point": {
      "steel": "#476580",
      "steelTint": "#E8EEF3",
      "brown": "#4A463F",
      "amber": "#D39A1F",
      "amberTint": "#FBF2DF",
      "orangeLight": "#F5A05A",
      "orangePale": "#F3B48A"
    },
    "semantic": {
      "success": "#196B24",
      "successStrong": "#196B24",
      "successBg": "#E7EFE8",
      "warning": "#D39A1F",
      "warningBg": "#FBF2DF",
      "danger": "#D93636",
      "dangerBg": "#FBE9E9",
      "info": "#476580",
      "infoBg": "#E8EEF3"
    },
    "data": ["#EB6F2A", "#476580", "#4A463F", "#8C867A", "#F3B48A", "#D39A1F"],
    "scales": {
      "orange": ["#B8431A", "#EB6F2A", "#F5A05A", "#F3B48A", "#FFF1E6"],
      "steel": ["#476580", "#8FAEC7", "#E8EEF3"],
      "green": ["#196B24", "#6FBF7C", "#E7EFE8"],
      "red": ["#D93636", "#F07A7A", "#FBE9E9"],
      "amber": ["#D39A1F", "#E2B558", "#FBF2DF"],
      "timeline": ["#C9C9C0", "#8C867A", "#4A463F", "#EB6F2A"]
    },
    "dark": {
      "bg": "#141210",
      "panel": "#211E1A",
      "charcoal": "#332F29",
      "surface": "#2A2620",
      "surfaceAlt": "#322D26",
      "border": "#3E3931",
      "line": "#4A443B",
      "text": "#F4F0E9",
      "textMuted": "#CFC8BC",
      "textSub": "#A89F92",
      "textDim": "#6E655A",
      "brownText": "#C9C0B2",
      "accent": "#EB6F2A",
      "accentText": "#F08A4C",
      "accentLight": "#F5A05A",
      "accentTint": "#3A2A1E",
      "steelText": "#8FAEC7",
      "steelTint": "#26313A",
      "success": "#6FBF7C",
      "successBg": "#22301F",
      "danger": "#F07A7A",
      "dangerBg": "#3A2323",
      "warning": "#E2B558",
      "warningBg": "#3A3021",
      "frameLine": "rgba(255,255,255,0.6)",
      "lineSoft": "rgba(255,255,255,0.14)"
    }
  },
  "font": {
    "ko": "'Pretendard Variable', Pretendard, -apple-system, 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif",
    "en": "'Pretendard Variable', Pretendard, -apple-system, 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif",
    "mono": "'JetBrains Mono', 'D2Coding', Consolas, monospace",
    "heading": "'Pretendard Variable', Pretendard, sans-serif",
    "pptxFallback": ["Pretendard", "Malgun Gothic", "Apple SD Gothic Neo"]
  },
  "weight": { "regular": 400, "medium": 500, "semibold": 600, "bold": 700 },
  "size": { "xs": 12, "sm": 14, "base": 16, "lg": 20, "xl": 25, "2xl": 31, "3xl": 39, "4xl": 49 },
  "deckPx": { "cover": 88, "kpi": 96, "headline": 64, "title": 44, "subtitle": 30, "body": 26, "small": 22, "eyebrow": 22, "caption": 18 },
  "deckPt": { "cover": 44, "kpi": 48, "headline": 32, "title": 22, "subtitle": 15, "body": 13, "small": 11, "eyebrow": 11, "caption": 9 },
  "leading": { "tight": 1.15, "snug": 1.3, "normal": 1.5, "relaxed": 1.65 },
  "tracking": { "eyebrow": "0.18em", "tag": "0.10em", "tight": "-0.01em" },
  "space": { "1": 4, "2": 8, "3": 12, "4": 16, "5": 20, "6": 24, "8": 32, "10": 40, "12": 48, "16": 64, "20": 80, "24": 96 },
  "radius": { "sm": 6, "md": 10, "lg": 12, "pill": 999 },
  "shadow": {
    "card": "0 2px 12px rgba(74,70,63,0.08)",
    "hairline": "0 1px 2px rgba(74,70,63,0.08)",
    "darkPanel": "0 12px 32px rgba(33,30,26,0.35)"
  },
  "deckFrame": { "w": 1920, "h": 1080, "padX": 90, "padTop": 72, "headlineY": 130, "subY": 236, "contentY": 340, "contentBottom": 1000, "footerY": 1017, "gapCard": 28 },
  "assets": {
    "logoLight": "assets/remember-black.png",
    "logoDark": "assets/remember-offwhite.png",
    "objet": ["assets/objet-01-bulb.png", "assets/objet-02-torn.png", "assets/objet-03-slit.png", "assets/objet-04-glow.png", "assets/objet-05-ribbed.png", "assets/objet-06-coil.png", "assets/objet-07-sphere.png"]
  }
}
```
