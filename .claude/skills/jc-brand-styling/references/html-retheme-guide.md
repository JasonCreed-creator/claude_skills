# HTML 아티팩트 리테마 가이드

이미 존재하는 **HTML 아티팩트**(대시보드·랜딩·단일 페이지 산출물)에 jc 시그니처(+선택적 클라이언트 오버레이)를 입히는 방법. PPTX는 `style_pptx.py`가 바이너리를 직접 후처리하지만, HTML은 **CSS 변수(custom property) 치환**으로 리테마한다.

> 토큰 값 정본: 라이트=`jc-design-system/references/signature-tokens.md §6 JSON`, 다크=`mode-mapping.md §3`, 인쇄=`mode-mapping.md §4.2`. 이 문서의 hex는 정본 미러이며 **새 값을 만들지 않는다**(`check_drift.py` FORBIDDEN 0건). 오버레이가 바꾸는 건 `--jc-primary`·`--jc-accent`(+다크 보정)뿐이다.

## 0. 리테마 절차 (4단계)

1. **토큰 블록 식별** — 대상 HTML의 `<style>` 또는 `:root`에서 색·폰트를 정의한 부분을 찾는다. 인라인 `style="color:#..."` 하드코딩이 있으면 변수 참조로 바꾼다.
2. **`:root` 시그니처 주입** — 아래 §1 블록으로 교체(오버레이 지정 시 primary/accent만 그 값으로).
3. **다크 `@media` 추가/교체** — §2 블록. 이미 다크 블록이 있으면 정본 매핑값으로 교정한다.
4. **인쇄 라이트 강제 추가** — §3 블록(`RULE-PRINT-LIGHT`). 다크를 지원하면 **필수**.

치환 후 `check_drift.py` 관점에서 FORBIDDEN 값(구 slate/tailwind 계열)이 남지 않았는지 확인한다.

## 1. `:root` — 라이트 시그니처 (기본)

`signature-tokens.md §6` 미러. `<primary>`·`<accent>`는 오버레이 지정 시 그 값으로, 미지정 시 시그니처(`#0A2540`·`#2962FF`).

```css
:root{
  /* base */
  --jc-primary:        #0A2540;   /* ← 오버레이 primary 가능 */
  --jc-primary-soft:   #1A3556;
  --jc-text:           #1A1D24;
  --jc-text-muted:     #5A6270;
  --jc-surface:        #FFFFFF;
  --jc-surface-alt:    #F1F3F7;
  --jc-bg:             #F8F9FB;
  --jc-border:         #E5E8ED;
  --jc-border-strong:  #C9CFD8;
  /* accent (오버레이 accent 가능) */
  --jc-accent:         #2962FF;   /* ← 오버레이 accent 가능 */
  --jc-accent-soft:    #E8EFFF;
  --jc-accent-strong:  #1E4DCC;
  /* point pool */
  --jc-point-orange:   #FF5722;
  --jc-point-magenta:  #E91E63;
  --jc-point-neon:     #00E676;   /* 면적 5% 이내, 인쇄 폴백 #00C853 */
  --jc-point-blue:     #2962FF;
  /* data series 1..6 (6번째는 6+카테고리 확장 슬롯) */
  --jc-data-1:#2962FF; --jc-data-2:#E91E63; --jc-data-3:#FF5722;
  --jc-data-4:#00E676; --jc-data-5:#0A2540; --jc-data-6:#7C3AED;
  /* semantic */
  --jc-success:#00C853; --jc-success-strong:#00733B;  /* 본문 녹색은 strong 사용(WCAG) */
  --jc-warning:#FFA000; --jc-danger:#D32F2F; --jc-info:#2962FF;
  /* type — 시그니처 고정(오버레이 불가) */
  --jc-font-ko:'Pretendard','Pretendard Variable',-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  --jc-font-en:'Inter','Helvetica Neue',Helvetica,Arial,sans-serif;
  --jc-font-mono:'JetBrains Mono','IBM Plex Mono','D2Coding','Consolas','Monaco',monospace;
  --jc-font-heading:'Pretendard','Inter',-apple-system,sans-serif;
}
```

폰트는 **시그니처 고정** — 오버레이로 못 바꾼다(`signature-tokens.md §2`). 사이즈·간격·라운드도 시그니처 고정(필요 시 §6 JSON의 `size`/`space`/`radius`를 그대로 미러).

## 2. 다크 모드 (`@media (prefers-color-scheme: dark)`)

`mode-mapping.md §3` 미러. 헤더 배경/텍스트는 라이트와 동일(풀블리드 Deep Navy + 흰 텍스트). 토글 방식(`[data-theme="dark"]`)을 쓰는 산출물이면 그 셀렉터에도 같은 값을 건다.

```css
@media (prefers-color-scheme: dark){
  :root{
    --jc-bg:            #0A1220;   /* 더 깊은 네이비 */
    --jc-surface:       #152134;
    --jc-surface-alt:   #1F2C42;
    --jc-text:          #E8ECF2;
    --jc-text-muted:    #A0A8B4;
    --jc-border:        #2A3650;
    --jc-border-strong: #3D4A66;
    /* accent 다크 보정 (밝기 +20%) — 오버레이 시 그 색의 보정값으로 */
    --jc-accent:        #5B8DEF;
    --jc-accent-strong: #7BA3F2;
    /* point pool 다크 보정 (밝기 +15%) */
    --jc-point-orange:  #FF7649;
    --jc-point-magenta: #F04D85;
    --jc-point-neon:    #33EE92;
    --jc-point-blue:    #5B8DEF;
    /* data series 다크 */
    --jc-data-1:#5B8DEF; --jc-data-2:#F04D85; --jc-data-3:#FF7649;
    --jc-data-4:#33EE92; --jc-data-5:#C9CFD8; --jc-data-6:#A78BFA;
  }
}
```

> 헤더는 라이트·다크 공통으로 `background:var(--jc-primary); color:#FFFFFF;`. Deep Navy(`#0A2540`) 위 흰 텍스트는 14.04:1(AAA)로 양쪽 모드에서 안전(`mode-mapping.md §9.5`).

**오버레이 + 다크 동시 적용**: 오버레이 accent가 시그니처 밖이면, 다크 보정값은 그 색의 HSL 명도를 +20% 올린 값을 쓴다(`validate_overlay.py`의 `lighten()`이 산출하는 값과 동일 규칙). 단순 케이스는 `jc-theme-factory`가 발행 시 함께 산출해 넘긴다.

## 3. 인쇄 라이트 강제 (`RULE-PRINT-LIGHT`)

다크 모드를 지원하는 HTML은 **인쇄(PDF 출력) 시 라이트로 강제**한다. 다크 토글 상태여도 인쇄 출력은 라이트여야 한다(잉크/토너·대비). 정본 토큰: `mode-mapping.md §4.2`, 규칙: `shared-rules.md#RULE-PRINT-LIGHT`.

```css
@media print{
  :root, [data-theme="dark"]{
    --jc-bg:           #FFFFFF !important;
    --jc-surface:      #FFFFFF !important;
    --jc-surface-alt:  #F1F3F7 !important;
    --jc-text:         #1A1D24 !important;
    --jc-text-muted:   #5A6270 !important;
    --jc-border:       #E5E8ED !important;
    --jc-accent:       #2962FF !important;   /* 오버레이 시 그 라이트 accent */
  }
}
```

인쇄 강제는 **화면 상태를 영구 변경하지 않는다** — 인쇄 컨텍스트에서만 라이트 토큰을 덮어쓰고, 인쇄 종료 후 원래(다크) 상태로 복귀한다. JS 토글(`beforeprint`/`afterprint`)을 쓰는 산출물도 동일 규약을 따른다.

## 4. 적용 예시 (요지)

리테마는 보통 대상 파일의 `<style>` 안 토큰 정의부만 위 3블록으로 교체하면 끝난다. 컴포넌트 규칙은 변수를 참조하므로 자동 반영된다:

```css
.kpi-card   { background:var(--jc-surface); border:0.5px solid var(--jc-border); border-radius:12px; }
.kpi-value  { color:var(--jc-accent); font-family:var(--jc-font-heading); }
.header     { background:var(--jc-primary); color:#FFFFFF; }
.btn-cta    { background:var(--jc-accent); color:#FFFFFF; }   /* 4.79:1 AA */
.series-1   { color:var(--jc-data-1); }
```

하드코딩된 색(원본 Anthropic 오렌지 같은 대체 브랜드 잔재나 tailwind slate/blue 계열 리터럴)이 보이면 대응하는 `var(--jc-*)`로 치환한다. 그래야 다크·인쇄 모드가 한 번에 따라온다. (구체 금칙값 목록은 `scripts/check_drift.py`의 FORBIDDEN 참조 — 본 문서엔 리터럴로 적지 않는다.)

## 5. 점검 체크리스트 (HTML 리테마 후)

- [ ] `:root` 시그니처 주입, 인라인 하드코딩 색 → `var(--jc-*)` 치환
- [ ] 토큰 값 정본 미러(`signature-tokens §6`), `check_drift.py` FORBIDDEN 0건(구 slate/tailwind 잔재 없음)
- [ ] 폰트 시그니처(Pretendard/Inter/JetBrains Mono) 유지, 오버레이로 폰트 안 바뀜
- [ ] 다크 `@media` 정본 매핑값(`mode-mapping §3`), 헤더는 양 모드 공통 Deep Navy+흰
- [ ] **인쇄 라이트 강제**(`@media print`) 존재 — 다크 지원 시 필수(`RULE-PRINT-LIGHT`)
- [ ] 본문 텍스트 대비 WCAG AA↑(`RULE-WCAG`), 본문 녹색은 `--jc-success-strong`
- [ ] 오버레이는 `--jc-primary`·`--jc-accent`만, 나머지 시그니처 고정
- [ ] 회사·개인정보 외부 주입 변수(`RULE-NO-COMPANY`), 최종 대비·카피는 `jc-redteam` 점검 가능
