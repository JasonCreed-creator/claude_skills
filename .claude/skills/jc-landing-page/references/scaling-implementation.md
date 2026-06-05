# 고정 비율 스케일링 구현 (jc-landing-page 핵심)

375px 기준 **단일 비율 스케일링**(반응형 미디어쿼리 아님)의 표준 코드·안티패턴 정본 — 루트 폰트 스크립트·CSS 안전망·rem 단위·컨테이너·Sticky CTA·검증. SKILL.md §5가 이 문서를 가리킨다.

**이 섹션은 본 스킬의 가장 중요한 기술 표준이다.** 화면이 작아지든 커지든 디자인 기준 폭에서 잡힌 **폰트·여백·이미지·버튼의 비율이 그대로 유지**되어, 모든 요소가 함께 작아지거나 함께 커진다. iPhone SE에서 보든 갤럭시 노트에서 보든 폴더블 펼친 상태에서 보든 데스크톱에서 보든, **눈에 보이는 비율은 100% 동일**해야 한다.

### 5.0 작동 원리 (먼저 이해할 것)

핵심 트릭은 **`html`의 `font-size`(=1rem 기준값)를 화면 폭에 비례해서 실시간으로 바꾸는 것**이다.

- 기준 폭(375px)에서 → `html { font-size: 16px }` → `1rem = 16px`
- 화면이 320px이 되면 → `html { font-size: 13.65px }` → `1rem = 13.65px` (자동으로 모든 rem 값이 줄어듦)
- 화면이 414px이 되면 → `html { font-size: 17.66px }` → `1rem = 17.66px` (자동으로 모든 rem 값이 커짐)

즉 **rem으로 잡힌 모든 값은 화면 폭에 정확히 비례**한다. 폰트 18px → 1.125rem으로 적은 순간, 화면 폭과 함께 자동으로 스케일된다.

이게 작동하려면 다음 3개가 **모두** 만족되어야 한다:
1. viewport 메타태그가 `maximum-scale=1.0`으로 잠겨 있어야 (사용자 핀치줌으로 인한 깨짐 방지)
2. **모든 크기 단위가 rem** (px 섞이면 그 부분만 안 줄어들어 비율이 깨짐)
3. 루트 폰트 사이즈 스크립트가 `resize`·`orientationchange`에 모두 반응해야

### 5.1 viewport 메타태그 (반드시 이대로)
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
```

- `maximum-scale=1.0` + `user-scalable=no` → 사용자가 핀치줌해도 비율이 깨지지 않음 (스크립트로 폭 추적 중이므로 줌이 들어오면 계산이 어그러진다)
- `viewport-fit=cover` → 노치/펀치홀 영역까지 활용 (안전영역은 `env(safe-area-inset-*)`로 따로 처리)

### 5.2 루트 폰트 사이즈 스크립트 (표준 코드, 이대로 사용)

```html
<script>
  (function() {
    // ============ 비례 스케일링 설정 ============
    const BASE_WIDTH = 375;   // 디자인 기준 폭 (이 폭에서 1rem = 16px)
    const BASE_FONT = 16;     // 기준 폭에서의 1rem 값 (px)
    const MAX_WIDTH = 500;    // 이 폭 이상은 모바일 폭으로 고정 (데스크톱에서 가운데 정렬)
    const MIN_WIDTH = 280;    // 이 폭 이하로는 더 줄이지 않음 (구형 폴더블 접힘 상태 보호)
    // ===========================================

    function setRootFontSize() {
      // documentElement.clientWidth 사용 — window.innerWidth는 스크롤바 폭을 포함해 데스크톱에서 1~17px 오차 발생
      let width = document.documentElement.clientWidth || window.innerWidth;

      // 클램프: MIN ~ MAX 사이로 제한
      if (width > MAX_WIDTH) width = MAX_WIDTH;
      if (width < MIN_WIDTH) width = MIN_WIDTH;

      // 1rem = (현재 폭 / 기준 폭) * 기준 폰트
      // 예: 화면 폭 414 → (414 / 375) * 16 = 17.66px → 1rem = 17.66px
      const fontSize = (width / BASE_WIDTH) * BASE_FONT;
      document.documentElement.style.fontSize = fontSize + 'px';
    }

    // 최초 1회 실행 — DOM 파싱 직후 즉시 적용되어야 FOUC(스타일 깜빡임) 없음
    setRootFontSize();

    // 화면 회전·창 크기 변경·DPI 변경 모두 대응
    window.addEventListener('resize', setRootFontSize);
    window.addEventListener('orientationchange', setRootFontSize);

    // iOS Safari 주소창 표시/숨김으로 인한 viewport 변화 대응
    window.addEventListener('pageshow', setRootFontSize);
  })();
</script>
```

**스크립트 배치 위치 — 반드시 `<head>` 안, CSS 다음, 다른 모든 JS 앞.** body 안에 두면 FOUC가 생긴다.

### 5.3 CSS 안전망 (px 실수를 자동으로 잡아주는 보조 장치)

스킬 표준은 **모든 값을 rem으로 작성하는 것**이지만, 작업 중 px이 끼어들 수 있다. 다음 CSS를 항상 깔아두어 px 실수가 들어와도 비례가 무너지지 않게 한다.

```css
/* 1. 박스 모델 통일 */
*, *::before, *::after {
  box-sizing: border-box;
}

/* 2. 루트 폰트 사이즈 fallback — 스크립트가 로드되기 전에도 비례 비슷하게 작동 */
:root {
  /* 4vw → 화면 폭 400px에서 16px. 스크립트가 즉시 덮어쓰므로 거의 안 쓰이지만 보험. */
  font-size: clamp(13px, 4.2667vw, 21.33px);  /* MIN_WIDTH=280 → 13px, BASE=375 → 16px, MAX=500 → 21.33px */
}

/* 3. body는 1rem(=16px @375)을 기본 폰트로 */
body {
  font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  font-size: 1rem;              /* @375 = 16px */
  line-height: 1.5;
  color: #1A1D24;
  -webkit-text-size-adjust: 100%;   /* iOS Safari가 가로모드에서 폰트를 임의로 키우는 것 방지 */
  -webkit-font-smoothing: antialiased;
}

/* 4. 이미지·영상도 비례 스케일 — 부모 폭 100% + 자동 높이 */
img, video, svg, picture {
  max-width: 100%;
  height: auto;
  display: block;
}
```

### 5.4 모든 크기는 rem 단위로 작성 (절대 규칙)

- **px 대신 rem 사용** — 폰트, 패딩, 마진, width, height, border-radius, gap, top/left/right/bottom 좌표 등 **거의 모든 값**
- **px 허용 예외 (이것만)**:
  - `border: 1px solid` (보더 두께)
  - `box-shadow`의 blur radius 1~2px 미세값
  - `outline` 두께
- **% / vw / vh 사용 시 주의**:
  - `%`는 부모 기준이라 의도대로 비례 스케일됨 — OK
  - `vw`는 viewport 폭 기준이라 `MAX_WIDTH` 초과 시 데스크톱에서 너무 커짐 — **사용 금지** (단 5.3의 fallback에서만 예외)
  - `vh`는 hero 섹션 높이(`100vh`) 정도에만 쓰고, 내부 요소 크기에는 사용 금지
- 기준 폭 375px에서 디자인할 때 **px → rem 변환은 ÷16**

**px → rem 빠른 환산표 (디자인 자주 쓰는 값):**

| 디자인 px @375 | rem | 디자인 px @375 | rem |
|---|---|---|---|
| 8px | 0.5rem | 32px | 2rem |
| 10px | 0.625rem | 36px | 2.25rem |
| 12px | 0.75rem | 40px | 2.5rem |
| 14px | 0.875rem | 48px | 3rem |
| 16px | 1rem | 56px | 3.5rem |
| 18px | 1.125rem | 64px | 4rem |
| 20px | 1.25rem | 80px | 5rem |
| 24px | 1.5rem | 100px | 6.25rem |
| 28px | 1.75rem | 120px | 7.5rem |

### 5.5 컨테이너 구조

```css
html, body {
  margin: 0;
  padding: 0;
  background: #1A1D24;       /* 데스크톱에서 양 옆에 보이는 배경색 (캠페인 톤에 맞게 조정) */
  overflow-x: hidden;        /* 가로 스크롤 차단 */
}

.page-container {
  max-width: 31.25rem;       /* 500px → 데스크톱에서 모바일 폭으로 고정 */
  margin: 0 auto;            /* 가운데 정렬 */
  background: #ffffff;       /* 페이지 본문 배경 (캠페인에 따라 조정) */
  min-height: 100vh;
  overflow-x: hidden;
  position: relative;        /* sticky CTA 등 자식 absolute 기준점 */
}
```

### 5.6 Sticky CTA 버튼 처리

```css
.sticky-cta {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 31.25rem;          /* 500px → 페이지 컨테이너와 동일 */
  padding-bottom: env(safe-area-inset-bottom, 0);  /* iPhone 노치/홈바 영역 회피 */
  z-index: 100;
}
```

### 5.7 검증 방법 (작업 마무리 시 반드시 확인)

브라우저 개발자 도구에서 다음 3개 폭으로 토글하며 **모든 요소의 비율과 위치가 동일하게 줄어들고/커지는지** 확인:

| 검증 폭 | 확인 사항 |
|---|---|
| **320px** (iPhone SE 1세대) | 텍스트가 비례 축소되며 줄바꿈 동일. 버튼 터치 영역 충분 |
| **375px** (기준) | 디자인 그대로 |
| **414px** (iPhone Plus) | 비례 확대되어 여전히 디자인 비율 동일 |
| **500px** 이상 (데스크톱) | 모바일 폭으로 고정, 좌우 배경색 노출, 가운데 정렬 |

**비율이 깨졌다면 99% 원인은 px이 섞여 들어간 것이다.** 개발자 도구에서 의심 요소 클릭 → Computed 탭에서 단위가 px로 그대로 박혀있는지 확인.

### 5.8 흔한 실수 (Anti-patterns)

❌ **미디어 쿼리로 다른 폰트 사이즈 지정** — `@media (max-width: 360px) { font-size: 14px }` 같은 것. 본 스킬의 스케일링과 충돌한다. 미디어 쿼리는 **레이아웃 분기에 사용하지 않는다.**
❌ **`vw` 단위 남발** — 데스크톱에서 폭 고정이 풀려서 폰트가 거대해짐
❌ **`100vh` 내부 요소에 사용** — iOS Safari 주소창 변화로 깜빡거림. hero 높이 정도만 허용
❌ **`px`로 폰트 사이즈 지정** — 스케일링에서 빠짐. 그 텍스트만 비율 깨짐
❌ **`maximum-scale=1.0`을 빼고 빌드** — 사용자가 핀치줌하는 순간 모든 계산이 어그러짐
❌ **스크립트를 `<body>` 하단에 두기** — FOUC 발생, 로드 직후 큰 폰트가 0.3초쯤 보였다가 줄어듦

---
