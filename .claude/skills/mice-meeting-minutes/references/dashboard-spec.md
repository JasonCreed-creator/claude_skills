# Dashboard Spec — HTML 회의록 대시보드 사양

메인 산출물인 단일 HTML 대시보드의 구조·인터랙션·토큰·영속화 규칙. 디자인 값의 정본은 `jc-design-system`(v2 리멤버 웜 페이퍼)이며, 여기서는 CSS 변수 이름과 역할만 쓴다.

---

## 1. 파일 · 의존

```
dashboard_[프로젝트]_[YYYYMMDD].html   (단일 파일, 메인)
.series-data/[series_id].json          (시리즈 모드 시 동기화)
```

CDN(버전 고정, 인터넷 필요) — React 18.3.1 · ReactDOM 18.3.1 · prop-types 15.8.1(Recharts UMD가 전역 `PropTypes`를 요구) · Recharts 2.12.7 · Babel standalone 7.29.8(버전 미지정 시 8.x로 풀려 JSX 런타임이 바뀐다). 서체 Pretendard Variable + JetBrains Mono(ID·기한·킥커).

오프라인 동작 옵션(`--offline` 라이브러리 인라인)은 미구현 후보.

---

## 2. 토큰 주입

- 템플릿 `<style id="design-tokens">` 안의 `@design-tokens:start ~ end` 블록이 라이트(`:root`)·다크(`:root[data-theme="dark"]`)·인쇄(`@media print`, 라이트 강제) 변수 세트다. 이 블록은 미러이며, `build_dashboard.py`가 빌드 때 `jc_tokens.py`로 SoT(`signature-tokens.md §6`)를 읽어 통째로 교체한다.
- 컴포넌트 CSS와 JS는 변수만 참조한다. HEX 직접 기입 금지. 차트 색은 JS가 `getComputedStyle`로 변수를 읽어 칠하고, 테마 전환 때 다시 읽는다(`jc-design-system/references/usage-guide.md` §3.5).
- 변수 이름은 팀 보드·플레이북 HTML과 같다(`--paper` `--surface` `--surface-warm` `--ink` `--brown` `--ink-sub` `--warm-gray` `--orange` `--orange-deep` `--orange-tint` `--steel` `--positive` `--negative` `--amber` `--s1`~`--s5` …). 역할→SoT 키 표는 SKILL.md §8.

---

## 3. UI 구조

### 헤더 (component-patterns §7 문서 헤더)
- 좌: 모노 킥커(`Meeting Minutes · Type A · 시리즈 N차`, 딥 오렌지) → 제목 25px 700 → 오렌지 룰 4×48px → 리드(일시·장소·유형·발주처, brown). 지연 Action이 있으면 부정색 "지연 Action N건".
- 우: 리멤버 로고 슬롯(라이트 `remember-black.png` / 다크 `remember-offwhite.png`, 높이 20px) → [Internal | External] · [라이트 | 다크] 세그먼트 토글.
- 로고 데이터가 없으면 발행 명의 텍스트("리멤버 MICE비즈팀").

### KPI 카드 4장 (§3)
결정사항 · Action(완료 N건) · 미결 사항(Action 차단 N건) · **Action 완료율**(강조 카드 — 오렌지 1.25px 보더 + 상단 그라디언트 룰, 화면당 1장). 수치 31px 700 tabular-nums, 단위는 캡션색. 반응형 4열 → 2열(≤900px).

### 탭
본 미팅(기본) · Action 트래커 · 시리즈 누적(`series_id` 있을 때) · 전략 메모(Internal). 활성 탭은 잉크 면 + 페이퍼 글자.

### 본 미팅 탭 — 상태 카드는 좌측 4px 바 (§4)
| 패널 | 카드 |
|------|------|
| 안건 | 웜 서피스 행 + 모노 번호(01·02, 딥 오렌지) |
| 결정사항 | 틴트(`--orange-tint` 면 + `--orange-soft` 바) |
| 발언 요지 | 안건 라벨(딥 오렌지) + 화자/발화 2열, 행 구분 `--line-soft` |
| 리스크·이슈 | 부정(`--negative-bg` 면 + `--negative` 바) |
| 미결 사항 | 앰버(`--amber-bg` 면 + `--amber` 바), carry-over는 점선 바 + `↻` |
| 후속 일정 | 노트(`--surface-warm` 면 + `--steel` 바) |

카드 메타 글자는 `--brown`(틴트 면 위 대비 확보).

### Action 트래커 탭 (§9)
- 차트 2개: 상태 도넛(TODO `--s4` · DOING `--s2` · BLOCKED `--negative` · DONE `--positive`, 라벨 병기) · Owner별 바(전체 `--s4` · 완료 `--positive`).
- 필터: 검색(제목·Owner·ID) · Priority 칩(P0~P3) · Owner 선택. AND 조합.
- 칸반 4열: 열 헤더 = 상태 배지(TODO 중립 · DOING 스틸 · BLOCKED 부정 Bold 14px · DONE 긍정) + 건수.
- Action 카드: 좌측 4px 우선순위 바(P0 부정 · P1 오렌지 소프트 · P2 스틸 · P3 보더) · 모노 ID · 제목 600 · Priority 배지 · Owner · 기한(모노 — 임박 `--orange-deep`, 지연 `--negative` Bold + "지연") · 상태 드롭다운. carry-over는 앰버 면 + `↻`.

### 시리즈 누적 탭
회차별 완료율 라인(`--s1`, 3px) · 회차별 Action 구성 누적 바(신규 `--s2` · Carry-over `--s5`) · 누적 통계 표(가로선만, 헤더 1.5px 잉크 하단선, 숫자 우측 정렬 tabular, BLOCKED>0은 부정색) · "본 회차 시리즈 저장" Primary 버튼.

### 전략 메모 탭 (Internal 전용)
5W1H 카드 6장(웜 서피스, 모노 질문 라벨 딥 오렌지 + 힌트 + 본문).

### 하단 툴바 (sticky)
좌: 발행 명의 · 모드 표기(`[Internal] 외부 공유 금지` / `[External] 송부용`). 우: Slack 페이스트(Primary — `--btn-primary` 딥 오렌지 면 + 흰 글자 5.45:1) · PDF 저장 · JSON 백업 · ↻ 시리즈 저장(Secondary — brown 1.5px 아웃라인).

### 아이콘·문체
이모지 없음. 기호는 유니코드(`↻` `·` `—`)만. 토스트는 fade 240ms, 바운스 없음.

---

## 4. 인터랙션

- **모드 토글**: Internal ↔ External 즉시 전환. External이면 전략 메모 탭 비활성, Slack 페이스트 푸터 문구 전환. 발화 익명화·마스킹 자체는 8축 추출 단계에서 데이터에 반영한다(redaction-rules.md).
- **테마 토글**: 첫 렌더는 `BRAND.theme`(기본 라이트). 사용자가 토글하면 `localStorage` `mm-theme`에 저장하고 다음 방문 때 복원. 전환 시 차트 재색칠.
- **Action 상태 변경**: 카드 드롭다운 → KPI 완료율 즉시 갱신. 저장은 "시리즈 저장" 클릭 때만(의도치 않은 덮어쓰기 방지).
- **기한 표시**: 오늘~+3일 임박(딥 오렌지 600), 지연(부정 700 + "지연"), DONE은 표시 없음.

---

## 5. 영속화

| 순위 | 저장소 | 비고 |
|------|--------|------|
| 1 | `window.storage` | Claude 아티팩트 환경, 비동기 |
| 2 | `localStorage` | 일반 브라우저, 도메인별 격리 |

키: `mice-mtg:[series_id]`(회차 배열) · `mm-theme`(테마). 회차 레코드: `session_no` `date` `new_actions` `carry_over_actions` `done` `doing` `blocked` `todo` `completion_rate` `data_snapshot`. 서버 측 백업은 `build_dashboard.py`의 `.series-data/[series_id].json`.

---

## 6. Slack 페이스트

`buildSlackMd` — 제목·시리즈 / 참석 / 결정 최대 3 / Action 최대 3 / 다음 일정 / 미결·리스크 건수 / 전략 코멘트(Internal) / 공유 범위 푸터. 200~600자. `navigator.clipboard` 실패 시 textarea + `execCommand('copy')` 폴백. 채널 게시는 사용자 몫(채널 운영 규칙은 mice-slack-ops).

---

## 7. PDF (RULE-PRINT-LIGHT)

`window.print()` → 인쇄 대화상자에서 "PDF로 저장". `@media print`:
- 토큰 블록이 다크 상태여도 라이트 값으로 덮어쓴다(캔버스 흰색).
- 툴바·탭·필터·헤더 토글 숨김, 헤더 제목·로고(라이트)는 인쇄.
- 패널·차트·KPI 카드 `break-inside: avoid`, 그림자 제거, 칸반 2열.
- 인쇄 전용 푸터: "발행 리멤버 MICE비즈팀 · 일자 · 송부용/내부 보관용".

---

## 8. JSON 백업

```json
{
  "_meta": {"backup_date": "...", "skill_version": "<BRAND.skillVersion>", "project_name": "...", "series_id": "...", "theme": "light", "mode": "internal"},
  "current_session": {"meeting_date": "...", "agenda": [], "decisions": [], "actions": [], "risks": [], "pending": [], "next_steps": [], "discussion": {}, "strategy_note": {}},
  "series_history": []
}
```

파일명 `mm-series-backup-[series_id]-[YYYYMMDD].json` (시리즈 없으면 `mm-backup-[프로젝트]-[YYYYMMDD].json`). 다시 입력하면 같은 대시보드로 재빌드.

---

## 9. 접근성 · 반응형

- 토글은 `aria-pressed`, 탭은 `role="tab"`·`aria-selected`, 포커스 링 2px 오렌지.
- 대비: `jc-design-system/references/shared-rules.md#RULE-WCAG` — 작은 강조 글자는 `--orange-deep`, `--orange` 글자는 큰 글자만, 캡션색은 단위·푸터에만.

| 너비 | 레이아웃 |
|------|---------|
| > 900px | KPI 4열 · 칸반 4열 |
| 600~900px | KPI 2열 · 칸반 2열 |
| < 600px | 칸반 1열 · 헤더 세로 정렬 · 발언 요지 1열 |

---

## 10. 보안 · 프라이버시

- External 전환 시 전략 메모 탭 비활성(DOM에서 렌더 안 함).
- 저장 데이터는 사용자 기기 한정, 서버 전송 없음. 외부 백업은 JSON 다운로드로 사용자가 관리.
- 빌드 산출물에는 로컬 경로를 넣지 않는다(`BRAND.tokenSource`는 `sot`/`fallback`만).

---

## 11. 자동 검증 (`validate_dashboard_html`)

| 체크 | 통과 기준 |
|------|----------|
| 플레이스홀더 | `{{TITLE}}` · `{{INITIAL_DATA}}` · `{{BRAND}}` 잔존 0 |
| 라이브러리 | React · Recharts 연결 |
| SoT 토큰 | `--orange` · `--paper` · `--s1` 라이트 값과 다크 `--paper` 값이 SoT와 일치 |
| 인쇄 | `@media print` 라이트 강제 블록 존재 |
| legacy 색 | 구 네이비·일렉트릭블루 계열 0건 |
| 크기 | 40KB 이상 (템플릿 단독 약 54KB, 로고 2종 포함 약 95KB) |

실패해도 파일은 남기고 "검토 필요"로 보고한다.

---

## 12. 확장 후보

| 기능 | 설명 |
|------|------|
| `--offline` | 라이브러리 인라인 임베드 |
| 발주처 로고 병기 | `client-overlays.md` 슬롯의 발주처 로고를 헤더 우측에 병기 (오렌지 불변) |
| 다중 시리즈 통합 뷰 | 여러 `series_id` 통합 조회 |
| 다음 어젠다 자동 생성 | 미결 + 후속 일정 → 어젠다 초안 |
