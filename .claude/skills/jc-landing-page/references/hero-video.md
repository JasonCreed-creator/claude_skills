# Hero 배경 영상 통합 표준 (jc-landing-page)

9:16 Hero 배경 영상의 사양(Pre-production)·FFmpeg 후처리·표준 HTML/CSS·안티패턴·Fallback·검증 정본. SKILL.md §9가 이 문서를 가리킨다. 영상 유무는 §0.6 인풋 체크에서 확정.

작업자가 Hero에 영상을 넣겠다고 답한 순간, **무조건 이 섹션의 표준 그대로 통합한다.** 영상을 별도 박스에 넣거나, 컨테이너 안에 카드처럼 떡 박는 방식은 사용하지 않는다. **풀블리드(full-bleed) 배경 + 그라데이션 페이드** 방식만 사용한다.

### 9.1 작업자에게 먼저 알려줄 영상 사양 (Pre-production 가이드)

영상을 만들기 전에 작업자가 알아야 하는 것. 이미 만들어진 영상을 가져왔어도 이 사양을 충족해야 풀블리드 배경으로 깔린다.

**필수 사양:**

| 항목 | 사양 | 이유 |
|---|---|---|
| **종횡비** | **9:16 (세로형) 필수** | 모바일 풀스크린(세로) hero에 풀블리드로 깔리려면 세로 영상이어야 함. 16:9 가로 영상을 풀블리드로 깔면 양옆이 잘리거나 위아래에 빈 공간 생김. |
| **해상도** | 720×1280 또는 1080×1920 | 720p가 모바일에서 충분. 더 키우면 용량만 늘어남 |
| **길이** | 5~15초 (10초 권장) | 짧으면 임팩트 부족, 길면 로딩 부담 + 다시 보고 싶지 않게 됨 |
| **루프 친화** | 첫 프레임과 마지막 프레임이 시각적으로 유사 | 무한 반복 시 점프컷이 보이지 않게 |
| **오디오** | **불필요 (제거)** | 모바일 자동재생은 muted 필수. 오디오 트랙은 용량만 차지 |
| **용량** | 1MB 이하 권장 | 모바일 LTE에서 즉시 로딩되어야 함 (3G 환경 고려) |
| **코덱** | H.264 (Constrained Baseline + yuv420p) | 모든 브라우저에서 100% 호환. High profile은 일부 환경에서 재생 안 됨 |

**콘텐츠 구성 가이드 (작업자에게 영상 만들기 전 전달):**

```
영상 안에 보여줄 핵심 시각 요소는 영상 세로 35~70% 구간에 배치하세요.
이유: hero 페이지 상단(0~35%)에는 카피가 얹히고
     하단(70~100%)에는 CTA·Trust 요소가 얹히기 때문에
     그 영역은 그라데이션으로 가려집니다.
     실제로 사용자에게 보이는 영상 영역은 가운데 35%뿐입니다.

또한 모바일 화면이 좁기 때문에 좌우 양 끝의 요소는 잘릴 수 있습니다.
중요한 시각 요소는 화면 중앙에 배치하세요.
```

**AI 영상 생성 도구(헉스필드 등) 사용 시 프롬프트 명시 사항:**

```
Aspect ratio: 9:16 VERTICAL (mobile portrait, 720x1280)
Composition: Key visual elements positioned in the CENTER VERTICAL 35-70%
of the frame. Top 35% and bottom 30% will be obscured by page gradient
overlay. Do not place critical content in those zones.
No audio track required.
```

### 9.2 영상 후처리 표준 (FFmpeg)

작업자가 영상 파일을 가져오면 작업 시작 전에 다음 명령으로 후처리한다:

```bash
ffmpeg -i input.mp4 \
  -an \
  -c:v libx264 \
  -profile:v baseline \
  -level 3.0 \
  -pix_fmt yuv420p \
  -crf 28 \
  -preset slow \
  -movflags +faststart \
  -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black" \
  rejected.mp4
```

**옵션 의미:**
- `-an`: 오디오 트랙 완전 제거
- `-profile:v baseline + -pix_fmt yuv420p`: 모든 브라우저 호환성 100%
- `-crf 28`: 모바일에 충분한 화질, 용량 최소화
- `-movflags +faststart`: 메타데이터 앞으로 이동 → 스트리밍 즉시 시작
- `scale + pad`: 9:16이 아닌 영상이 들어와도 강제로 9:16에 맞춤 (검정 패딩)

### 9.3 표준 HTML 구조 (Hero 섹션)

```html
<section id="hero">
  <!-- Z0: 영상 - 풀블리드(전체 inset:0) -->
  <div class="hero-bg-wrap">
    <video class="hero-bgvid" autoplay muted loop playsinline preload="auto" disablepictureinpicture aria-hidden="true">
      <source src="video.mp4" type="video/mp4">
    </video>
  </div>

  <!-- Z1: 그라데이션 페이드 - 상단·하단을 가려서 카피·CTA 가독성 확보 -->
  <div class="hero-bg-fade"></div>

  <!-- Z2: 컬러 액센트 (선택) -->
  <div class="hero-color"></div>

  <!-- Z3: 상단 카피 -->
  <div class="hero-body">
    <div class="hero-kicker">...</div>
    <h1 class="hero-h1">...</h1>
    <div class="hero-sub">...</div>
  </div>

  <!-- Z3: 하단 CTA + Trust -->
  <div class="hero-bottom">
    <button class="cta">CTA 문구</button>
    <div class="hero-trust">...</div>
  </div>
</section>
```

### 9.4 표준 CSS (그대로 사용)

```css
/* Hero 컨테이너 - 모바일 풀스크린 */
#hero{
  position:relative;
  min-height:100svh;
  display:flex;
  flex-direction:column;
  justify-content:flex-start;
  padding:96px 20px 220px;
  background:#0A1220;        /* 영상 로딩 전 배경 */
  overflow:hidden;
}

/* 영상 컨테이너 - 풀블리드 (hero 전체 채움) */
.hero-bg-wrap{
  position:absolute;
  inset:0;                    /* hero 전체 영역 */
  z-index:0;
  overflow:hidden;
  background:#0A1220;
}

/* 영상 - 컨테이너 가득 채우고 느린 줌인 */
.hero-bgvid{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:cover;
  object-position:center 50%;  /* 영상 중앙이 hero 중앙에 오게 (콘텐츠에 따라 조정 가능) */
  transform-origin:50% 50%;
  transform:scale(1);
  animation:heroZoom 10s ease-out forwards;
}
@keyframes heroZoom{
  from{transform:scale(1)}
  to{transform:scale(1.15)}
}

/* 그라데이션 페이드 - 상단(카피) + 하단(CTA) 영역 가림 */
.hero-bg-fade{
  position:absolute;
  inset:0;
  z-index:1;
  pointer-events:none;
  background:linear-gradient(
    180deg,
    #0A1220 0%,
    #0A1220 calc(38% - 20px),                   /* 상단 38%까지 솔리드 */
    rgba(10,18,32,0.75) calc(50% - 20px),
    rgba(10,18,32,0.35) calc(68% - 20px),
    rgba(10,18,32,0) calc(82% - 20px),            /* 50~82%는 영상 노출 */
    rgba(10,18,32,0.4) 92%,
    rgba(10,18,32,0.9) 100%                       /* 하단 다시 짙게 */
  );
}

/* 컬러 액센트 - 좌상단 부드러운 빛 (선택) */
.hero-color{
  position:absolute;
  inset:0;
  z-index:2;
  background:radial-gradient(ellipse 70% 45% at 90% 5%, rgba(41,98,255,.18) 0%, transparent 60%);
  pointer-events:none;
}

/* 상단 카피 영역 - 영상 위로 */
.hero-body{
  position:relative;
  z-index:3;
  max-width:480px;
  width:100%;
}

/* 하단 CTA 영역 - 영상 위로 + 자체 검정 페이드 */
.hero-bottom{
  position:absolute;
  left:0;
  right:0;
  bottom:0;
  z-index:3;
  padding:0 20px 48px;
  background:linear-gradient(to top, #0A1220 0%, #0A1220 50%, rgba(10,18,32,.85) 100%);
}
```

### 9.5 절대 하지 말 것 (Anti-patterns)

다음 방식은 EOS·NICE 등의 케이스에서 명백히 잘못된 것으로 확인됨. 절대 사용 금지:

❌ **영상을 hero-body 안에 카드처럼 넣기** (`<video>` 위에 border-radius + box-shadow) → "박스가 박혀있는 느낌"
❌ **영상 영역을 50~75%로 제한** (`bottom:0; height:60%`) → 풀블리드가 안 됨, 박스 느낌
❌ **mask-image로 외곽 페이드** → "박힌 박스를 가리려는 짜깁기" 티가 남
❌ **filter:blur로 흐리게** → 영상의 분위기가 죽고, 굳이 영상 넣은 의미 없어짐
❌ **16:9 가로 영상을 풀블리드 시도** → 양옆 잘리고 위아래 빈 공간
❌ **그라데이션이 과채도/밝은 색** → jc 다크(`#0A1220`) 계열 저채도 톤이 시네마틱

### 9.6 영상이 16:9 가로형으로 이미 만들어진 경우 (Fallback)

이상적으로는 9.1대로 9:16로 다시 만드는 게 맞지만, 시간/비용상 어렵다면 다음 차선책을 작업자와 합의 후 적용:

**옵션 A: 가로 영상을 풀블리드로 깔되 일부만 보이게** (가장 흔한 차선책)
- `object-fit: cover` + `object-position`으로 영상 일부만 노출
- 핵심 시각 요소가 가운데에 있다면 `object-position: center center`
- 좌측 요소가 중요하면 `object-position: 30% center`
- 양옆이 잘리는 것은 감수

**옵션 B: 가로 영상을 hero 상단 절반에 배치 (레터박스식)**
- hero 상단 50%에만 영상, 하단은 일반 카피·CTA
- 영상은 정상 비율로 보이지만 EOS 같은 풀블리드 느낌은 아님

**옵션 C: 작업자에게 9:16 재제작 권유**
- 가장 좋은 결과물을 위해서는 재제작이 정답임을 명확히 알린다
- 9.1 가이드 다시 노출

어떤 차선책이든 **작업자에게 한계를 명시**한다: "16:9 가로 영상은 EOS 같은 풀블리드 느낌을 100% 재현할 수 없습니다. 이 부분 인지하고 진행하시겠습니까?"

### 9.7 산출물 검증 (영상 통합 시)

페이지 완성 후 영상 통합 부분 추가 체크:

- [ ] 영상이 9:16 세로형인가? (아니면 9.6 차선책 적용했고 작업자가 인지했나)
- [ ] 영상 용량이 1MB 이하인가? (FFmpeg 후처리 완료)
- [ ] 오디오 트랙이 제거되었나?
- [ ] H.264 Baseline + yuv420p로 인코딩되었나? (모바일 호환성)
- [ ] `inset:0` 풀블리드로 깔렸나? (박스 아님)
- [ ] mask-image나 filter:blur 같은 안티패턴 사용 안 했나?
- [ ] 상단 카피, 하단 CTA 영역이 그라데이션으로 가려져 가독성 확보되었나?
- [ ] 영상이 `autoplay muted loop playsinline`으로 모바일 자동재생 보장되나?
- [ ] 영상 로드 전에도 hero가 깔끔하게 보이나? (배경색 fallback)
- [ ] 영상이 무한 반복 시 점프컷이 어색하지 않은가?

---
