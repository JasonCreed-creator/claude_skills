# Build Kit — 시네마틱 캠페인 룩 (정본)

HTML 산출물(발표덱·랜딩·대시보드·아티팩트)에 시네마틱 캠페인 룩을 재현하기 위한 실행형 레시피. 본 문서가 룩의 정본(SoT)이다. jc-design-system/references/cinematic-campaign-html.md 는 본 문서로의 포인터다.

> 지위: 시그니처(딥네이비·일렉트릭블루)의 **파생 변형 테마**다. 시그니처 토큰을 수정하지 않으며, 산출물 단위로 `:root` 오버라이드 레이어로만 적용한다. 유래: 2026-08 웨비나 캠페인 발표덱 v4.2에서 실측 추출 (검증일 2026-07-25).
> 적용 예외: 본 룩은 **스크린 전용**(발표·웹). 인쇄/PDF 배포 산출물에는 `shared-rules.md#RULE-PRINT-LIGHT`에 따라 라이트 강제가 우선한다.

---

## 1. 룩 정의 (한 문장)

**"지금 촬영 중인 프리미엄 광고"** — 웜 블랙 스테이지 + 단일 오렌지 광원 + 미니어처 디오라마 시네마틱 포토(히어로) + 필름 레코딩 크롬(뷰파인더·REC·타임코드). 어둠이 기본값이고 오렌지 빛은 화면당 하나만 허락된다.

## 2. 토큰 오버라이드 (:root 복붙 블록)

기존 산출물 CSS 최하단에 삽입 — 캐스케이드로 시그니처 토큰을 덮는다.

```css
:root{
  --jc-accent:#FF4A11; --jc-accent-strong:#E03E0C; --jc-accent-light:#FFA37A;
  --st-bg-deep:#0B0805; --st-bg:#171009;
  --st-text:#F4F7FB; --st-muted:rgba(224,232,244,.64); --st-faint:rgba(224,232,244,.38);
  --st-surface:linear-gradient(180deg,rgba(255,255,255,.055),rgba(255,255,255,.02));
  --st-border:rgba(255,190,150,.13); --st-border-soft:rgba(255,190,150,.07);
  --st-glow:rgba(255,74,17,.30);
  --ease-out:cubic-bezier(.16,1,.3,1);
}
```

- 텍스트는 **쿨화이트 고정** (웜 배경 × 쿨 텍스트 긴장감이 의도) — 텍스트를 웜톤으로 바꾸지 말 것.
- 하드코딩 블루 잔존 스캔 필수: `rgba(41,98,255` · `#2962FF` · `#5B9BD5` 전량 치환 (v4 빌드에서 48건 발견된 전례).
- 대비: `#FF4A11` 위 흰 텍스트는 CTA·큰 텍스트 전용, 본문 금지. 검증은 `mode-mapping.md §9` 표준(WebAIM)으로 수행.

## 3. 레이어 아키텍처 (z-order)

```
z0  히어로 이미지/영상 (디오라마 컷, opacity .9~.92)
z1  보호 그라디언트 (.hfshade — 텍스트 존 확보)
z2  콘텐츠 (.wrap)
fixed  필름 크롬 (뷰파인더·REC·타임코드)
```

디바이더/히어로 좌측 텍스트 보호 그라디언트 (우측 2/3 이미지 구도 기준):
```css
background:linear-gradient(90deg,rgba(11,8,5,.94) 0%,rgba(11,8,5,.55) 42%,rgba(11,8,5,.10) 78%,rgba(11,8,5,.28) 100%)
```

## 4. 필름 크롬 (전문 스니펫)

```html
<div class="vf" aria-hidden="true"><i class="tl"></i><i class="tr"></i><i class="bl"></i><i class="br"></i></div>
<p id="reclive" aria-hidden="true"><i></i>REC — LIVE</p>
<p id="timecode" aria-hidden="true">00:00:00:00</p>
```
```css
.vf i{position:fixed;width:30px;height:30px;border:2px solid rgba(255,255,255,.20);z-index:52;pointer-events:none}
.vf .tl{top:20px;left:20px;border-right:0;border-bottom:0}
.vf .tr{top:20px;right:20px;border-left:0;border-bottom:0}
.vf .bl{bottom:20px;left:20px;border-right:0;border-top:0}
.vf .br{bottom:20px;right:20px;border-left:0;border-top:0}
#reclive{position:fixed;left:44px;bottom:40px;z-index:52;display:flex;align-items:center;gap:12px;font-size:17px;font-weight:800;letter-spacing:.30em;color:rgba(255,255,255,.60)}
#reclive i{width:11px;height:11px;border-radius:50%;background:var(--jc-accent);box-shadow:0 0 12px var(--st-glow);animation:recblink 1.6s steps(1) infinite}
@keyframes recblink{50%{opacity:.2}}
#timecode{position:fixed;right:44px;top:34px;z-index:52;font-size:17px;font-weight:700;letter-spacing:.20em;color:rgba(255,255,255,.55);font-variant-numeric:tabular-nums}
```
```js
(function(){var el=document.getElementById('timecode');if(!el)return;var t0=Date.now();
setInterval(function(){var ms=Date.now()-t0,f=Math.floor(ms/40)%25,s=Math.floor(ms/1000),
h=Math.floor(s/3600),m=Math.floor(s/60)%60;s=s%60;function p(n){return(n<10?'0':'')+n}
el.textContent=p(h)+':'+p(m)+':'+p(s)+':'+p(f);},120);})();
```

## 5. 컴포넌트 규격

| 컴포넌트 | 규격 |
|---|---|
| 웜 글래스 카드 | radius 20px · bg `--st-surface` · border 1px `--st-border` · 강조 시 `box-shadow:0 0 24px var(--st-glow)` |
| 아이브로 | weight 600 · UPPERCASE · letter-spacing .34em · `--jc-accent` · 뒤에 9px 오렌지 도트(글로우) |
| STEP 라벨 | 내러티브가 있으면 `STEP 01 — BEFORE / 02 — DURING / 03 — AFTER` 챕터 구조 |
| 헤드라인 | weight 700–800 · ls -0.02em · lh 1.2 · **주장형 문장** ("~입니다" 클레임) |
| 숫자 | weight 650 · ls -0.03em · tabular-nums · H2의 ~1.3배 |
| CTA | 솔리드 `--jc-accent` · radius 6–8px · hover `--jc-accent-strong` |
| 프로그레스 | 3px · `linear-gradient(90deg,var(--jc-accent),var(--jc-accent-light))` + 글로우 |
| 타입 스케일 | 1920 스테이지: 110/88/64/44/30/26/22 · 웹 반응형: 1.25 스케일, 본문 16–18px |

## 6. 모션 표준 — "1회 재생 · 마지막 프레임 정지"

루핑 금지 (동작 끊김 체감 — 2026-07-25 기획자님 확정). 섹션/슬라이드 진입 시 처음부터 1회 재생, 종료 후 마지막 프레임 유지:

```js
function onActive(sl){var vids=sl.querySelectorAll('video');
  Array.prototype.forEach.call(vids,function(v){try{
    if(sl.classList.contains('active')){v.currentTime=0;var p=v.play();if(p&&p.catch)p.catch(function(){});}
    else{v.pause();}}catch(e){}});}
var mo=new MutationObserver(function(ms){Array.prototype.forEach.call(ms,function(m){onActive(m.target)})});
Array.prototype.forEach.call(document.querySelectorAll('.slide'),function(sl){
  if(sl.querySelector('video'))mo.observe(sl,{attributes:true,attributeFilter:['class']});});
```

- 영상 태그: `muted playsinline preload="auto"` (autoplay·loop 없음).
- claude.ai 아티팩트/CSP 제약 환경에서 base64 영상은 data: URI 직결 금지 → `<script type="application/octet-stream" id="xxx-data">` 블록에 저장 후 Blob URL 변환 로더 사용. 로드 실패 시 정지 컷(webp)이 포스터 폴백.
- 최적화: 무음 · H.264 CRF 26 · faststart · 클립당 ~200–350KB 목표.

## 7. 히어로 이미지 파이프라인 (RULE-VISUAL-ROUTING: 사진·영상 = Higgsfield)

**정지 컷** (nano_banana_pro · 16:9):
"Cinematic macro photograph, tilt-shift miniature diorama in premium Korean advertising style: [장면 — tiny hyper-realistic Korean business figurines + one warm orange glowing focal element], deep warm near-black background, dramatic rim lighting, shallow depth of field, subject composed on the right two-thirds leaving dark space on the left for text, photorealistic macro photography, no text, no letters, no logos, 16:9"

**모션** (kling3_0_turbo · 5s · start_image=정지 컷 job id):
"Subtle cinematic ambient loop: the miniature diorama scene stays almost perfectly still, warm orange glow gently breathes, faint dust particles drift in the light, extremely slow camera drift, figurines remain static, premium advertising motion, no text"

- 후처리: PNG → WebP(q78–84) → base64 임베드. 텍스트/로고 포함 이미지 금지 (생성 후 육안 검수).
- 실물 신뢰가 헤드라인인 슬롯("실물입니다" 류)은 디오라마 대신 실제 캡처 교체를 권장 주석으로 남긴다.

## 8. 클라이언트 전개 규칙

- 본 룩의 캠페인 액센트는 산출물 단위 주입 변수다. 타 클라이언트 재사용 시 §2 블록에서 `--jc-accent` 3종만 해당 브랜드 컬러로 치환 — 웜 블랙 스테이지·크롬·타이포는 유지.
- `client-overlays.md`의 3토큰 원칙과 충돌하지 않는다: 오버레이는 (primary/accent/logo)를 공급하고, 본 문서는 그 값을 소비하는 **테마 레이어**다.
- RULE-NO-COMPANY: 본 문서에 클라이언트 실명·전용 컬러를 추가 하드코딩하지 말 것.

## 9. Do / Don't

**Do**: 어둠 유지 · 화면당 광원 1개 · 헤드라인은 주장형 · 크롬은 얇고 은은하게 · 여백 크게(섹션 간 96px+).
**Don't**: 블루·쿨톤 액센트 금지 · 라운드 남발한 SaaS 룩 금지 · 실사 인물 스톡 금지(히어로는 디오라마만) · 이미지 내 텍스트 금지 · 글로우 2개 이상 금지 · 셰이드 없는 이미지 위 본문 금지.

---
출처: 2026-08 웨비나 캠페인 발표덱 v4.2 실측 (랜딩 캠페인 룩 이식판) · 등재일 2026-07-25
