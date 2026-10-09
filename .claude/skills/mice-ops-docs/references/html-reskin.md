# HTML 리스킨 — 기존 HTML을 리멤버 웜 페이퍼로

이미 있는 HTML 산출물(대시보드·리포트·단일 페이지)을 **구조·문구는 그대로 두고 색·서체만** 리멤버 웜 페이퍼로 바꾸는 절차. PPTX 리스킨은 `jc-pptx`.

이 문서는 값을 적지 않는다. 키만 적고 값은 `jc-design-system/references/signature-tokens.md` §6 JSON에서 읽는다(코드는 `jc-design-system/scripts/jc_tokens.py`의 `load_tokens`·`color`·`dark`). 다크 매핑 `mode-mapping.md §3`, 인쇄 `mode-mapping.md §4.2`, 변수 이름 `usage-guide.md §3.4`(팀 보드·플레이북과 같은 이름).

---

## 0. 범위 (묻지 않고 기본값)

- 색·서체·라운드·그림자만 바꾼다. 레이아웃·문구·데이터는 손대지 않는다 — 원본과 텍스트 diff 0.
- 원본에 다크가 있으면 `data-theme="dark"` 토글로 유지, 없으면 라이트 단일 + 인쇄 블록만.
- 리멤버 로고 슬롯 추가(§6 `assets.logoLight`·`assets.logoDark`). 발주처 로고는 원색 그대로 병기하고 발주처 브랜드 색은 팔레트에 넣지 않는다(`client-overlays.md §1`).

## 1. 토큰 블록 식별

| 위치 | 찾을 것 |
|------|---------|
| `:root`·`body` 변수 블록 | `--primary`·`--bg` 같은 원본 변수 |
| 다크 블록 | `@media (prefers-color-scheme: dark)` · `[data-theme="dark"]` · `.dark` |
| 인라인 스타일 | `style="color:…"`·`background:…` |
| SVG 속성 | `fill=` · `stroke=` · `stop-color=` |
| 스크립트 | Chart.js `backgroundColor` 배열, 색 상수 |
| 유틸리티 CSS 클래스 | `bg-*`·`text-*` — 클래스 대신 변수 참조 규칙으로 덮는다 |
| 서체 | 웹폰트 `<link>`, `font-family` |

## 2. 토큰 오버라이드 — 리멤버 변수 주입

`:root`에 아래 변수를 넣는다. 값은 §6 키에서 생성하고, 스크립트를 못 돌리는 환경이면 `usage-guide.md §3.4` 블록을 그대로 복사한다(그 블록이 HTML용 미러 정본).

| 변수 | 역할 | §6 라이트 키 | §6 다크 키 |
|------|------|--------------|------------|
| `--paper` | 페이지 배경 | `color.bg` | `color.dark.panel` |
| `--surface` | 카드·표 | `color.surface` | `color.dark.surface` |
| `--surface-warm` | 표 헤더·바 트랙 | `color.surfaceAlt` | `color.dark.surfaceAlt` |
| `--ink` | 본문·헤드라인 | `color.text` | `color.dark.text` |
| `--brown` | 보조 본문 | `color.textSecondary` | `color.dark.brownText` |
| `--ink-sub` | 뮤트 | `color.textMuted` | `color.dark.textSub` |
| `--warm-gray` | 캡션·단위(본문 금지) | `color.textCaption` | `color.dark.textDim` |
| `--border` · `--line` | 보더 · 구분선 | `color.border` · `color.line` | `color.dark.border` · `color.dark.line` |
| `--orange` | 면·큰 글자 강조 | `color.accent` | `color.dark.accent` |
| `--orange-deep` | 작은 강조·링크 | `color.accentStrong` | `color.dark.accentText` |
| `--orange-tint` | 하이라이트 면 | `color.accentSoft` | `color.dark.accentTint` |
| `--steel` · `--steel-tint` | 보조·정보 | `color.point.steel` · `color.point.steelTint` | `color.dark.steelText` · `color.dark.steelTint` |
| `--positive`·`--negative`·`--amber` (+`-bg`) | 상태 | `color.semantic.success`·`danger`·`warning` (+`…Bg`) | `color.dark.success`·`danger`·`warning` (+`…Bg`) |
| `--s1`~`--s5` | 차트 시리즈 | `color.data[0]`~`[4]` | 동일 |
| `--font` | 서체 | `font.ko` | 동일 |
| `--shadow` | 카드 그림자 | `shadow.card` | `mode-mapping.md §3` 그림자 행 |

원본 변수 이름을 지울 이유가 없으면 **별칭**으로 잇는다 — `--primary: var(--ink); --accent: var(--orange);`. 컴포넌트 CSS를 고치지 않아도 전체가 따라온다.

**역할 대응**
- 원본 브랜드 주색(헤더·제목 배경) → `--ink`(리멤버의 primary는 잉크). 헤더는 잉크 밴드 + 오렌지 룰.
- 원본 액센트·CTA → 면은 `--orange`(화면당 오렌지 면 1회), 작은 글자·링크는 `--orange-deep`.
- 원본 차트 색 → 순서대로 `--s1`~`--s5`, 강조 시리즈 하나만 `--s1`.
- 리멤버에 없는 색(보라·청록 등) → 가장 가까운 역할로 흡수한다. 새 색을 만들지 않는다.

## 3. 하드코딩 색 스캔

변수 정의 밖에 남은 색 리터럴을 줄 번호와 함께 뽑는다(`python scan_colors.py page.html`).

```python
import re, sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
pat = re.compile(r"(--[\w-]+\s*:\s*)?(#[0-9A-Fa-f]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\))")
for no, line in enumerate(src.splitlines(), 1):
    for m in pat.finditer(line):
        if not m.group(1):          # 변수 정의(--x: 값)는 건너뜀
            print(no, m.group(2))
```

이름 색(`white`·`black`·`navy` 등), 그라디언트·그림자 안의 색, 앵커(`href="#…"`) 오탐은 눈으로 한 번 더 본다.

## 4. 교체

- 리터럴 → `var(--…)`. 판정 순서: 배경 면 → 텍스트 → 보더 → 상태 → 시리즈.
- 인라인 SVG는 `fill="var(--s1)"`처럼 변수를 받는다. `<img src="*.svg">` 외부 파일은 변수를 못 받으므로 인라인화하거나 그대로 둔다.
- Chart.js는 색 상수 대신 `getComputedStyle`로 변수를 읽고 테마 토글 때 `chart.update()`(`usage-guide.md §3.5`).
- 그라디언트는 §6 `color.gradient` 화면당 1회. 3D·그림자 차트는 플랫으로.
- 서체는 다른 웹폰트 `<link>`를 지우고 Pretendard 하나(`usage-guide.md §3.4` 링크). 숫자는 `tabular-nums`.

## 5. 다크 · 인쇄 블록

- 다크: `:root[data-theme="dark"]`에 §2 표의 다크 키. 원본이 `prefers-color-scheme`를 쓰면 같은 값으로 바꾸고, 첫 렌더는 라이트(`mode-mapping.md §4.1`).
- 인쇄: `@media print` 라이트 강제(`mode-mapping.md §4.2`, `RULE-PRINT-LIGHT`). 다크를 지원하면 필수. 화면 상태는 바꾸지 않는다.

## 6. 점검 (마감)

- [ ] §3 스캔 재실행 — 변수 정의 밖 색 리터럴 0
- [ ] 원본 팔레트·구 시그니처 값 0 (남았으면 §4로)
- [ ] 본문 대비 4.5:1 이상 — `mode-mapping.md §5` 표의 조합만 사용(`RULE-WCAG`). 캡션색 본문 금지, 앰버 단독 텍스트 금지, 18px 미만 오렌지 글자 금지(→ `--orange-deep`)
- [ ] 오렌지 면 화면당 1회, 상태색은 배지·셀 안에서만
- [ ] 다크 토글 시 흰 배경·검은 글자 하드코딩 잔재 없음
- [ ] 인쇄 미리보기 라이트(다크 밴드 포함)
- [ ] 원본 대비 텍스트 diff 0 — 리스킨은 문구를 바꾸지 않는다
- [ ] 리멤버 로고 슬롯, 발행 명의 리멤버 MICE비즈팀(`RULE-NO-COMPANY`)
- [ ] 발주처 공유본이면 `jc-redteam` Quick Strike(대비·명의·잔재)
