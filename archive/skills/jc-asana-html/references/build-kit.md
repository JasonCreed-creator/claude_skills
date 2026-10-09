# jc-asana-html Build Kit — 룩의 정본

라이트 SaaS 프로덕티비티 룩의 실행형 빌드 킷. 값 표기 규약: **검증값**(공개 브랜드 가이드, 검증일 병기) / **≈ 근사치**(공개 미기재 — 재현용 정의값. "공식 값"으로 서술 금지).

---

## §1. 룩 정의

- **무드**: 밝고 정돈된 협업툴 화면. 화이트 캔버스 위에 낮은 채도의 회색 구조물, 파스텔 태그가 정보를 분류하고, 코랄은 행동 유도 지점에만 등장한다.
- **위계 원리**: 색이 아니라 **여백·보더·타이포 웨이트**로 위계를 만든다. 배경색 블록 남발 금지.
- **밀도**: 행 높이 넉넉(리스트 행 44px≈), 카드 패딩 16–20px, 섹션 간 32–40px.
- **코랄 예산**: 화면당 코랄 사용처는 주 CTA·활성 탭 인디케이터·핵심 강조 수치 등 2–3곳 이내.

## §2. 토큰 블록 (`:root` 오버라이드 레이어)

산출물 CSS **최하단**에 삽입한다(리스킨 시 캐스케이드 승리 목적). 시그니처 토큰(`--jc-*`)은 건드리지 않는다.

```css
:root {
  /* ── 중립 (≈ 근사) ─────────────────────────── */
  --al-canvas: #FFFFFF;        /* 메인 캔버스 */
  --al-surface: #F9F8F8;       /* 보드/사이드 영역 배경 ≈ */
  --al-surface-2: #F5F3F3;     /* hover·zebra ≈ */
  --al-border: #EDEAE9;        /* 기본 보더 ≈ */
  --al-border-strong: #CFCBCA; /* 구분 강조 보더 ≈ */
  --al-ink: #1E1F21;           /* 본문 잉크 ≈ */
  --al-ink-sub: #6D6E6F;       /* 보조 텍스트 ≈ */
  --al-ink-faint: #9CA0A2;     /* 플레이스홀더·비활성 전용 ≈ — 본문 금지(캔버스 대비 2.64:1 실측) */

  /* ── 사이드바 (≈ 근사) ─────────────────────── */
  --al-sidebar-bg: #2E2E30;
  --al-sidebar-ink: #F5F3F3;
  --al-sidebar-ink-sub: #A2A0A2;

  /* ── 액센트 ────────────────────────────────── */
  --al-accent: #F06A6A;        /* 코랄 — 검증값 (공개 브랜드 가이드, 2026-07-31) */
  --al-accent-strong: #DC5A5A; /* hover ≈ */
  --al-accent-tint: #FDEDED;   /* 코랄 틴트 배경 ≈ — 용례: 활성 필터 칩·선택 행 배경 */
  --al-link: #4573D2;          /* 링크 블루 ≈ */

  /* ── 상태 (≈ 근사) ─────────────────────────── */
  --al-on-track: #5DA283;      /* 순항 */
  --al-at-risk: #F1BD6C;       /* 주의 */
  --al-off-track: #DE5F73;     /* 이탈 */
  --al-on-hold: #9CA6AF;       /* 보류 */

  /* ── 형태·타이포 ───────────────────────────── */
  --al-radius-card: 8px;
  --al-radius-btn: 6px;
  --al-radius-pill: 999px;
  --al-shadow-card: 0 1px 3px rgba(0,0,0,.05);
  --al-shadow-pop: 0 4px 12px rgba(0,0,0,.08);
  --al-font: 'Pretendard', 'Pretendard Variable', -apple-system, sans-serif;
}
body { background: var(--al-canvas); color: var(--al-ink); font-family: var(--al-font); }
```

**타입 스케일** (Pretendard 고정 — 하우스 표준·한국어 산출물·전용 폰트 라이선스 회피):

| 레벨 | 크기/웨이트 | 용도 |
|---|---|---|
| 페이지 타이틀 | 24px / 700 | 문서 제목 (탭 헤더 좌측) |
| 섹션 헤더 | 18px / 600 | 8축·지표 그룹 제목 |
| 카드 타이틀 | 15px / 600 | 카드·칸반 카드 제목 |
| 본문 | 14px / 400 / lh 1.6 | 일반 텍스트 |
| 메타 | 12px / 400, `--al-ink-sub` | 날짜·담당·캡션 |

## §3. 레이어 아키텍처 (페이지 골격)

```
┌────────────┬──────────────────────────────────────┐
│  사이드바   │  탭 헤더 (56px≈): 타이틀 · 탭 · 메타   │
│  (240px≈)  ├──────────────────────────────────────┤
│  도트 내비  │  콘텐츠 (max-width 1200 · pad 24–32) │
│            │   └ 카드 / 리스트 / 칸반 / KPI 그리드  │
└────────────┴──────────────────────────────────────┘
```

- 사이드바: `--al-sidebar-bg`, 섹션 앵커 내비. 900px 이하에서 숨김(상단 드롭 내비로 대체):
  ```css
  @media (max-width:900px){ .al-side{display:none;} .al-topnav{display:flex;} }
  ```
- 탭 헤더: 하단 1px 보더. 활성 탭은 텍스트 `--al-ink` + 하단 2px `--al-accent` 인디케이터.
- 콘텐츠 배경은 `--al-canvas` 기본, 칸반 영역만 `--al-surface`.

## §4. 컴포넌트 규격

### 4.1 사이드바 도트 내비 (문서 목차 전용)
```html
<nav class="al-side">
  <div class="al-side-title">{{doc_title}}</div>
  <a class="al-side-item is-active"><i class="al-dot" style="--dot:#5DA283"></i>결정사항</a>
  <a class="al-side-item"><i class="al-dot" style="--dot:#F1BD6C"></i>Action Items</a>
</nav>
```
```css
.al-side{background:var(--al-sidebar-bg);color:var(--al-sidebar-ink);width:240px;padding:20px 12px;}
.al-side-item{display:flex;align-items:center;gap:10px;padding:8px 12px;border-radius:6px;
  color:var(--al-sidebar-ink-sub);font-size:14px;text-decoration:none;}
.al-side-item.is-active,.al-side-item:hover{background:rgba(255,255,255,.08);color:var(--al-sidebar-ink);}
.al-dot{width:10px;height:10px;border-radius:50%;background:var(--dot);flex:none;}
```

### 4.2 태스크 리스트 행 (Action Items 전용)
```html
<div class="al-row">
  <span class="al-check" data-done="false"></span>
  <span class="al-row-title">{{task}}</span>
  <span class="al-avatar">{{initial}}</span>
  <span class="al-due">{{due}}</span>
  <span class="al-pill" data-pair="purple">{{tag}}</span>
</div>
```
```css
.al-row{display:flex;align-items:center;gap:12px;min-height:44px;padding:0 12px;
  border-bottom:1px solid var(--al-border);}
.al-row:hover{background:var(--al-surface-2);}
.al-check{width:18px;height:18px;border:1.5px solid var(--al-ink-faint);border-radius:50%;
  flex:none;display:inline-grid;place-items:center;}
.al-check[data-done="true"]{background:var(--al-on-track);border-color:var(--al-on-track);}
.al-check[data-done="true"]::after{content:'✓';color:#fff;font-size:11px;line-height:1;}
.al-due{font-size:12px;color:var(--al-ink-sub);margin-left:auto;}
```
완료 행은 타이틀에 `color:var(--al-ink-faint); text-decoration:line-through`.

### 4.3 필 태그 (분류·담당·우선순위)
```css
.al-pill{border-radius:var(--al-radius-pill);padding:2px 10px;font-size:12px;font-weight:500;
  background:var(--pill-bg);color:var(--pill-ink);}
```
색은 **반드시 §6 페어 표**의 `data-pair` 조합만 사용.

### 4.4 칸반 보드 (Action 상태·이니셔티브 보드)
```html
<div class="al-board">
  <div class="al-col"><div class="al-col-head">진행 전 <span class="al-count">3</span></div>
    <div class="al-card">…</div></div>
</div>
```
```css
.al-board{display:flex;gap:16px;background:var(--al-surface);padding:16px;border-radius:var(--al-radius-card);overflow-x:auto;}
.al-col{min-width:260px;flex:1;}
.al-col-head{font-size:13px;font-weight:600;color:var(--al-ink-sub);padding:4px 4px 10px;}
.al-card{background:var(--al-canvas);border:1px solid var(--al-border);border-radius:var(--al-radius-card);
  box-shadow:var(--al-shadow-card);padding:12px 14px;margin-bottom:10px;}
```
카드 내부: 카드 타이틀 → 필 태그 행 → 하단(아바타 + 듀데이트) 3단 고정.

### 4.5 상태 도트 + 라벨 (전략지표 신호등)
```html
<span class="al-status" data-state="on-track"><i></i>순항</span>
```
```css
.al-status{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;}
.al-status i{width:10px;height:10px;border-radius:50%;}
.al-status[data-state="on-track"] i{background:var(--al-on-track);}
.al-status[data-state="at-risk"]  i{background:var(--al-at-risk);}
.al-status[data-state="off-track"] i{background:var(--al-off-track);}
.al-status[data-state="on-hold"]  i{background:var(--al-on-hold);}
```
라벨 어휘 고정: 순항 / 주의 / 이탈 / 보류 (영문 병기 시 On track / At risk / Off track / On hold).

### 4.6 KPI 카드 + 진행률
```css
.al-kpi{background:var(--al-canvas);border:1px solid var(--al-border);border-radius:var(--al-radius-card);
  box-shadow:var(--al-shadow-card);padding:16px 20px;}
.al-kpi-value{font-size:28px;font-weight:700;letter-spacing:-.01em;}
.al-bar{height:6px;border-radius:999px;background:var(--al-surface-2);}
.al-bar>i{display:block;height:100%;border-radius:999px;background:var(--al-on-track);}
```
- 진행률 도넛(SVG): 트랙 `--al-surface-2` / 진행 `--al-on-track`(위험 시 상태색), 중앙 % 수치 700.
- 핵심 강조 수치 1–2곳만 `--al-accent` 허용(§1 코랄 예산).

### 4.7 아바타 스택
```css
.al-avatar{width:26px;height:26px;border-radius:50%;display:grid;place-items:center;
  font-size:11px;font-weight:600;color:#fff;background:var(--av,#6B3FA0);border:2px solid var(--al-canvas);}
.al-avstack .al-avatar+.al-avatar{margin-left:-8px;}
```
아바타 배경은 §6 페어 표의 **텍스트 색** 계열에서 순환 배정(파스텔 배경은 저대비라 금지). 실측 크기 = 코어 26px + 캔버스색 보더 2px(스택 겹침 경계용) = 30px.

### 4.8 차트 시리즈 팔레트 (Chart.js 등)
시리즈 순서: `#5DA283 → #4573D2 → #6B3FA0 → #F1BD6C → #DE5F73 → #17766B → #A15720 → #3D4DB7` (모두 ≈). 격자선 `--al-border`, 축 라벨 `--al-ink-sub`. 다중 시리즈 8개 초과 시 동일 순환을 흰색 40% 혼합 틴트로 반복.

## §5. 리스킨 절차 (기존 HTML)

1. §2 토큰 블록을 기존 CSS 최하단에 삽입.
2. **하드코딩 색 스캔** — 아래 목록을 정규식으로 전량 검출·치환(cinematic 리스킨 1건에서 48건 발견 전례 — 전수 스캔 필수):

| 검출 대상 | 치환 |
|---|---|
| `#2962FF` · `rgba(41,98,255…)` (일렉트릭블루) | `var(--al-accent)` 또는 `var(--al-link)` — 용도별 판단 |
| `#0B1F3B` · `#0A192F` 등 딥네이비 배경 | `var(--al-canvas)` / 사이드바면 `var(--al-sidebar-bg)` |
| `#5B9BD5` 계열 차트색 | §4.8 시리즈 팔레트 |
| `#333`·`#222` 류 잉크 | `var(--al-ink)` |
| `#666`·`#888` 류 보조 | `var(--al-ink-sub)` |
| 임의 그림자 (`0 10px 30px rgba(0,0,0,.3)` 류) | `var(--al-shadow-card)` / `var(--al-shadow-pop)` |

3. **컴포넌트 문법 치환 매핑**:

| 기존 패턴 | 본 룩 치환 |
|---|---|
| Action 테이블 행 | §4.2 태스크 리스트 행 |
| 상태 뱃지(■ 완료/지연) | §4.5 상태 도트 + 라벨 |
| 카테고리 뱃지 | §4.3 필 태그 (§6 페어) |
| Action 칸반(기존 스타일) | §4.4 칸반 보드 규격 |
| KPI 카드 | §4.6 규격 (수치 28px/700) |
| 담당자 텍스트 | §4.7 아바타(+이름 텍스트 병기) |
| 상단 고정 헤더 | §3 탭 헤더 (활성 탭 코랄 인디케이터) |

4. 검수: §8 체크리스트.

## §6. 파스텔 대비 페어 표 (필 태그 전용 — 이 조합만 허용)

| data-pair | 배경 ≈ | 텍스트 ≈ | 권장 용도 |
|---|---|---|---|
| coral | `#FCE5E5` | `#A83232` | 긴급·차단 |
| orange | `#FDEBDD` | `#A15720` | 우선순위 高 |
| amber | `#FBF0D0` | `#876618` | 대기·검토 |
| lime | `#EEF5D8` | `#59761D` | 아이디어 |
| green | `#DCF2E4` | `#1E7A46` | 완료·승인 |
| teal | `#D8F2EF` | `#17766B` | 운영 |
| blue | `#DDEEFB` | `#1C6DAC` | 정보·문서 |
| indigo | `#E2E6FB` | `#3D4DB7` | 개발·시스템 |
| purple | `#EBE2FA` | `#6B3FA0` | 전략·기획 |
| magenta | `#F8E0F3` | `#A03287` | 마케팅 |
| pink | `#FBE2EA` | `#B0356B` | 이벤트 |
| gray | `#EFEDEC` | `#57595B` | 기타·보류 |

규칙: 배경·텍스트는 반드시 같은 행에서 페어로 사용(교차 조합 금지). 전 12페어는 WCAG 대비 4.5:1 이상 **재계산 검증 완료(2026-07-31)**. 신규 페어 추가 시 `shared-rules.md#RULE-WCAG` 재계산 검증 후 본 표에 등재.

## §7. 미차용 자산 (상표·저작권 — 절대 삽입 금지)

- Asana 로고·워드마크·**삼점(three-dot) 심볼** — 삼각 배열 3도트 모티프 자체를 장식으로 그리는 것도 금지(상표 유사). 내비 도트는 §4.1처럼 세로 리스트 단일 도트로만.
- 유니콘·예티 등 셀레브레이션 캐릭터, 완료 애니메이션 모사.
- Asana 전용 서체 — 타이포는 Pretendard 고정.
- "Asana" 명칭을 산출물 화면 텍스트에 노출하지 않는다(스킬 내부 용어로만 사용).

## §8. 검수 체크리스트

- [ ] 토큰 밖 하드코딩 색 0건 (§5 스캔 재실행)
- [ ] 코랄 사용처 화면당 2–3곳 이내 (§1 예산)
- [ ] `#F06A6A` 위 흰 텍스트는 버튼·큰 텍스트 전용 — 본문 사용 0건 (RULE-WCAG)
- [ ] 필 태그 전 건이 §6 페어 표 조합 (교차 조합 0건)
- [ ] 산출물 유형별 최소 컴포넌트 문법 적용 확인 (회의록=리스트+칸반 / 지표=상태 도트+진행률)
- [ ] 상표 자산 0건 (§7)
- [ ] 담당자·회사명이 주입 변수 처리 (RULE-NO-COMPANY)
- [ ] 인쇄 미리보기 정상 (라이트 룩 — PRINT-LIGHT 자연 부합 확인)
- [ ] 최종 감수: jc-redteam
