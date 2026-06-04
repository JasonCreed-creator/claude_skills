# JC 아트 팔레트 — p5.js 사용 가이드

제너러티브 아트의 **기본 팔레트는 jc data 시리즈**다. 값 정본은 항상 `jc-design-system/references/signature-tokens.md`(§6 JSON)·`mode-mapping.md`(§3.2 다크). 본 문서는 그 값을 **p5.js에서 어떻게 쓰는지**만 보여주는 사용서다.

> 단일 HTML 아티팩트엔 런타임 JSON 파서가 없으므로 색을 인라인 상수로 박는다. 그 상수는 **출처(§1.4/§3.2/§1.8)를 주석으로 명시한 의도적 복제**다. 임의 색·원본 프리셋의 비-jc 색(테라코타·세이지·웜그레이 계열)은 금지(구체 금지 목록은 SKILL.md FORBIDDEN 참조).

## 1. 기본 팔레트 — data 시리즈 (signature-tokens.md §1.4)

| 시리즈 | HEX(라이트) | HEX(다크 보정 §3.2) | 성격 |
|--------|------------|---------------------|------|
| data-1 | `#2962FF` | `#5B8DEF` | Electric Blue — 메인 |
| data-2 | `#E91E63` | `#F04D85` | Magenta — 브랜드 포인트 |
| data-3 | `#FF5722` | `#FF7649` | Vivid Orange — 핫 |
| data-4 | `#00E676` | `#33EE92` | Neon Green — 라이브(면적 절제) |
| data-5 | `#0A2540` | `#C9CFD8` | Deep Navy(다크에선 라이트 그레이) |
| data-6 | `#7C3AED` | `#A78BFA` | Violet — 6번째 확장 슬롯 |

캔버스 배경 기본: **Deep Navy `#0A2540`**(§1.1 `--jc-primary`) 또는 **라이트 `#F8F9FB`**(§1.1 `--jc-bg`). 작품 톤에 맞춰 선택.

```javascript
// 라이트/다크 배경에 맞는 data 시리즈 (출처: signature-tokens.md §1.4 / mode-mapping.md §3.2)
const JC_DATA_LIGHT = ['#2962FF', '#E91E63', '#FF5722', '#00E676', '#0A2540', '#7C3AED'];
const JC_DATA_DARK  = ['#5B8DEF', '#F04D85', '#FF7649', '#33EE92', '#C9CFD8', '#A78BFA'];

// 어두운 캔버스(Deep Navy)에는 다크 보정 팔레트가 대비가 좋다.
let palette = (params.bgColor === '#0A2540') ? JC_DATA_DARK : JC_DATA_LIGHT;
```

## 2. 시드 기반 색 선택 (재현성 유지)

`randomSeed(params.seed)` 이후 `random()`은 결정적이므로, 팔레트 인덱스도 시드에 묶인다.

```javascript
// 입자/요소마다 시드 기반으로 팔레트 색 배정
function pickColor(palette) {
  const c = color(palette[floor(random(palette.length))]);
  c.setAlpha(90);            // 누적 렌더링 시 투명도로 밀도 표현
  return c;
}
```

## 3. 연속/단계 표현 — 인포그래픽 스케일 (signature-tokens.md §1.8)

밀도장·히트맵·그라데이션처럼 **단일 카테고리가 아닌 연속/단계** 표현엔 data 시리즈 대신 스케일을 쓴다(deep→bg 5단계).

```javascript
// scale-blue (전부 시그니처 토큰, 신규 색 없음) — 출처: signature-tokens.md §1.8
const JC_SCALE_BLUE  = ['#0A2540', '#1E4DCC', '#2962FF', '#5B9BD5', '#E8EFFF'];
const JC_SCALE_GREEN = ['#00733B', '#00C853', '#4CDE8A', '#9CEBC4', '#E6F8EE'];
const JC_SCALE_RED   = ['#8E1F1F', '#D32F2F', '#E57373', '#F2B8B8', '#FBEAEA'];
const JC_SCALE_AMBER = ['#8A5200', '#C77F00', '#FFA000', '#FFC24D', '#FFF3E0'];

// 값 t(0~1)를 5단계 스케일로 보간
function scaleColor(scale, t) {
  const i = constrain(floor(t * (scale.length - 1)), 0, scale.length - 2);
  const f = (t * (scale.length - 1)) - i;
  return lerpColor(color(scale[i]), color(scale[i + 1]), f);
}
```

## 4. 잔상(trail) 배경 페이드

애니메이션 잔상은 **jc 배경색**을 반투명으로 덮어 만든다(비-jc 프리셋 라이트색 금지).

```javascript
function fadeBackground(alpha) {
  const c = color(params.bgColor); // 예: '#0A2540'
  c.setAlpha(alpha);               // 2~40 권장
  noStroke();
  fill(c);
  rect(0, 0, width, height);
}
```

## 5. 자유 팔레트 모드 (opt-in)

사용자가 **"자유 팔레트"/"free art"/"이 브랜드 컬러로"**를 *명시*할 때만 jc 팔레트를 벗어난다. 명시가 없으면 위 1~4의 jc 홈베이스가 기본이다. 자유 모드에서도:

- 작품 본문/제목에 회사명·실명 하드코딩 금지(`RULE-NO-COMPANY`).
- 특정 클라이언트 톤이 목적이면 `jc-theme-factory`의 3토큰 오버레이를 먼저 고려.

## 6. 대비 메모 (뷰어 UI)

아트 캔버스 자체는 미적 자유가 있으나, **뷰어 UI 텍스트**는 WCAG AA를 지킨다(정본 `mode-mapping.md §9`). jc 토큰 조합은 충족:

| 조합 | 대비 | 등급 |
|------|------|------|
| `#FFFFFF` on `#0A2540`(헤더) | 14.04:1 | AAA |
| `#1A1D24` on `#FFFFFF`(본문) | 16.30:1 | AAA |
| `#5A6270` on `#FFFFFF`(보조) | 6.34:1 | AA |
