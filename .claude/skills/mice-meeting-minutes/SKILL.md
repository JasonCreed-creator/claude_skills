---
name: mice-meeting-minutes
description: "MICE 행사 기획·운영 미팅의 transcript·메모·구두 보고를 8축(안건·발언 요지·결정사항·Action Items·리스크·미결·후속 일정·전략 메모)으로 구조화해, 리멤버 웜 페이퍼 룩의 단일 HTML 회의록 대시보드(KPI 카드·Action 칸반·시리즈 누적 차트·라이트/다크·Slack 페이스트·PDF·JSON 백업)로 만드는 스킬. 외부 송부용/내부 보관용 톤 분기, 정기 미팅 회차 누적과 미완료 Action 이월 추적을 지원한다. 다음 상황에서 반드시 이 스킬을 사용할 것 — 사용자가 '회의록', '미팅록', '미팅 노트', '회의 정리', '회의 요약', '미팅 정리', 'Action Items', '액션 아이템', '후속 조치', '팔로업', 'follow-up', 'Discovery 미팅 정리', '킥오프 미팅 정리', '정기 미팅 정리', '발주처 협의 기록', '사전답사 기록', '협력사 미팅 정리'를 말할 때, 클로바노트·Otter·Whisper·Zoom·Meet·Teams transcript를 올리며 '정리해줘', '회의록으로 만들어줘', 'Action 뽑아줘', '대시보드로 만들어줘'를 요청할 때. Discovery·킥오프 회의록은 ChainPayload로 제안서 덱(jc-pptx)·전략 캔버스(jc-strategy-canvas)·운영계획서(mice-ops-docs)·결과보고(mice-aftermath)에 이어진다. 형제 경계 — 덱은 jc-pptx, 행사 KPI 대시보드·운영계획서는 mice-ops-docs, 결과보고서·교훈 종합은 mice-aftermath, 산문 문서 공동작성은 jc-doc-coauthor, Slack 요약·공지는 mice-slack-ops, 발표 대본·MC 멘트는 pt-script, 완성본 검증은 jc-redteam. 음성 파일 STT는 범위 밖(외부 도구로 텍스트 변환 후 입력)."
version: "v2.2.0"
dependencies: Pillow (선택 — 로고 축소용, 없으면 원본 크기로 임베드)
---

# mice-meeting-minutes — 회의록 대시보드 (v2.2.0)

MICE 행사 기획·운영 미팅을 18년 경력 전략가 시각의 8축 프레임으로 구조화해 **단일 HTML 회의록 대시보드**로 시각화·추적·공유한다. 룩은 리멤버 웜 페이퍼 하나(`jc-design-system` 토큰 런타임 로드), 발행 명의 기본은 **리멤버 MICE비즈팀**.

## 0. 진행 원칙

- 기본 흐름은 **기획안 1회 확인 → 빌드 → 검수(jc-redteam)**. 회의록은 입력(transcript)이 내용을 정하므로 기획안 확인 없이 기본값으로 바로 빌드한다. 되돌릴 수 있는 작업은 기본값으로 바로 진행하고, 고른 기본값은 응답 첫머리에 한 줄씩 밝힌다. 사용자가 바꾸면 재빌드.
- 되돌릴 수 없는 작업(발주처 메일 송부·Slack 게시)은 하지 않는다. 산출물은 파일까지, 송부는 승인 후 사용자 몫.
- 비어 있는 값은 지어내지 않는다. 추정은 `(추정)`, 미확인은 `[확인 필요]`로 두고 응답 끝 "확인 필요" 목록에 모은다.

| 비어 있는 입력 | 기본값 |
|---------------|--------|
| 회의 유형 | 시그널 점수 1위. 동점·근소하면 더 공식적인 유형(C > A > E > D > B) |
| 모드 | 유형 기본값 — Type A·C `external`, B·D·E `internal` |
| 화자 매핑 | 발화 내용·호칭으로 추정 + `(추정)` 표기 |
| Owner / Due | 호스트 / 미팅일+7일 + `(재확인)` 플래그 |
| Redaction 의심 발화 | External 모드에서 보수적으로 마스킹, 의심 목록을 함께 제시 |
| 테마 | 라이트 |
| 발주처 | `client_company` 슬롯(`{{client_company}}`), 예시는 가명(A사) |

## 1. 다루는 것 / 다루지 않는 것

**다루는 것**
- transcript 8축 추출 + 인터랙티브 대시보드 빌드 (`references/analysis-framework.md`)
- 5종 회의 유형(외부 클라이언트·내부 팀·발주처 공식·사전답사·협력사) 톤·구조 분기 (`references/meeting-types.md`)
- External(송부용)/Internal(내부 보관용) 모드 + Redaction (`references/redaction-rules.md`)
- Action Items 5열 표준 + 칸반(TODO·DOING·BLOCKED·DONE) (`references/action-items-schema.md`)
- 정기 미팅 시리즈 누적·carry-over (`references/series-tracking.md`)
- Discovery·킥오프 회의록 → ChainPayload/v1 (`references/chaining-guide.md`)

**다루지 않는 것** — 음성 파일 STT(클로바노트·Otter·Whisper로 텍스트 변환 후 입력), 손글씨 OCR, 제안서·소개서 덱(jc-pptx), 견적(mice-estimate), 행사 KPI 대시보드·운영계획서(mice-ops-docs), 결과보고서(mice-aftermath), Slack 채널 요약·공지(mice-slack-ops), 발표 대본(pt-script). 대시보드의 Slack 페이스트 버튼은 회의 1건 요약 복사까지만 한다.

## 2. 워크플로우

```
[미팅] → 외부 STT(클로바노트·Otter·Whisper·Zoom·Meet·Teams) → transcript 텍스트
   ↓
① 파싱      python scripts/parse_input.py transcript.txt --mapping "참석자 1 = 호스트, 참석자 2 = 김부장 (A사)"
             채널 감지 · 화자 매핑 · 30분 청크 · Redaction 힌트 · 입력 검증 (references/input-formats.md)
   ↓
② 판정      유형(meeting-types.md) · 모드 · 기본값 — 응답 첫머리에 한 줄씩
   ↓
③ 8축 추출  analysis-framework.md → redaction-rules.md → action-items-schema.md  (Claude 본체)
   ↓
④ 빌드      8축 JSON 저장 → python scripts/build_dashboard.py --input minutes.json --out <출력폴더>
             SoT 토큰 런타임 로드 · 로고 슬롯 · 자동 검증 · (시리즈) .series-data 동기화
   ↓
⑤ 체이닝    Discovery·킥오프면 ChainPayload/v1 → .chaining/ (chaining-guide.md)
   ↓
⑥ 검수      발주처 송부용(External)은 jc-redteam Quick(결정·Action 정합, 마스킹 누락)
   ↓
산출: dashboard_[프로젝트]_[YYYYMMDD].html 1개 + 확인 필요 목록
```

입력 JSON 형식은 `python scripts/build_dashboard.py --dump-sample sample.json`으로 확인한다(필드 = `DashboardData`).

## 3. 입력 채널 4종

| 채널 | 입력원 | 정확도 |
|------|--------|--------|
| Ch1 | 클로바노트 export (화자+타임스탬프) | 최고 |
| Ch2 | Otter·Whisper·Zoom(VTT)·Google Meet·Teams export | 높음 |
| Ch3 | 메모형 자유 텍스트 | 중간 (화자 추정) |
| Ch4 | 채팅창 구두 보고 | 낮음 (대부분 `(추정)`) |

## 4. 산출물 — 단일 HTML 대시보드

파일명 `dashboard_[프로젝트]_[YYYYMMDD].html` (예: `dashboard_a사-discovery_20260509.html`). 구조·인터랙션 상세는 `references/dashboard-spec.md`, 산출 순서·검증은 `references/output-spec.md`.

```
┌ 헤더 ─ 모노 킥커(유형·시리즈) · 제목 · 오렌지 룰 · 일시·장소·발주처 ───── 리멤버 로고 슬롯 ┐
│        [Internal | External]  [라이트 | 다크]                                              │
├ KPI 4장 ─ 결정사항 · Action · 미결 사항 · Action 완료율(강조 카드 1장)                       ┤
├ 탭 ─ 본 미팅 | Action 트래커 | 시리즈 누적(--series) | 전략 메모(Internal)                   ┤
│   본 미팅: 안건 · 결정(틴트 카드) · 발언 요지 · 리스크(부정 바) · 미결(앰버 바) · 후속 일정    │
│   Action: 상태 도넛 · Owner별 바 · 필터 · 칸반 4열(상태 배지) · 상태 드롭다운                 │
│   시리즈: 회차별 완료율(S1) · 신규(S2)/carry-over(S5) 누적 바 · 누적 통계 표                  │
│   전략 메모: 5W1H 카드 6장                                                                   │
└ 하단 툴바 ─ 발행 명의 · 모드 표기 │ Slack 페이스트 · PDF 저장 · JSON 백업 · 시리즈 저장      ┘
```

- 기술: 단일 파일, React 18.3.1 + prop-types 15.8.1 + Recharts 2.12.7 + Babel standalone 7.29.8 CDN(버전 고정, 인터넷 필요), Pretendard + JetBrains Mono.
- 영속화: 시리즈 회차는 `window.storage`(없으면 `localStorage`) 키 `mice-mtg:[series_id]`, 테마 선택은 `mm-theme`. 빌드 측 백업은 `.series-data/[series_id].json`.
- JSON 백업 버튼: `mm-series-backup-[series_id]-[YYYYMMDD].json` — 다른 세션에서 이 파일을 입력하면 같은 상태로 재빌드.

## 5. 모드

| 모드 | 톤 | Redaction | 전략 메모 탭 |
|------|----|-----------|-------------|
| `external` | 정중·사실 위주 | 적용 | 숨김 |
| `internal` | 솔직한 평가 | 미적용 | 노출 (5W1H) |

- 헤더 토글로 실시간 전환. 테마(라이트/다크)와 독립.
- 라이트가 첫 화면 기본. 다크는 토글(사용자 선택은 `mm-theme`에 저장). **인쇄·PDF는 다크 상태여도 라이트**(`jc-design-system/references/shared-rules.md#RULE-PRINT-LIGHT`).

## 6. 시리즈 모드 (`--series=<id>`)

1차 빌드 → 대시보드 "시리즈 저장" → 2차 빌드 시 직전 회차 미완료 Action·미결 사항 자동 carry-over(`↻` 표시, 앰버 배경) → 3회 이상 이월 시 장기 미해결 경고. 상세 `references/series-tracking.md`.

## 7. 체이닝 (ChainPayload/v1)

봉투 정본 `jc-design-system/references/chaining-protocol.md`, source `mice-meeting-minutes`. 페이로드 키 `client` · `project_context` · `discovery_data` · `strategic_notes` (+ `actions`·`risks`·`pending`).

| target | 언제 | 수신 측 용도 |
|--------|------|-------------|
| `jc-pptx` | Type A Discovery + 제안 진행 합의 | 제안서 덱 인테이크(Partial 입력) |
| `jc-strategy-canvas` | Discovery에서 전략 판단이 필요할 때 | ① 인테이크·JTBD·SWOT 시드 |
| `mice-ops-docs` | 수주 후 킥오프·운영 협의 | 운영계획서 1·2·7섹션(결정·Action·담당) |
| `mice-aftermath` | 사후 회고·정산 미팅 | 6축 교훈·8축 차기 권고 |

저장 `.chaining/[project]_[YYYYMMDD]_to_[target].json`. 상세 매핑 `references/chaining-guide.md`.

## 8. 디자인 — jc-design-system 연동

- 값은 전부 `jc-design-system`(v2 리멤버 웜 페이퍼)에서 런타임 로드한다. `build_dashboard.py`가 `jc-design-system/scripts/jc_tokens.py`를 import해 `signature-tokens.md §6 JSON`을 읽고, 템플릿의 `@design-tokens` CSS 블록(미러)을 SoT 값으로 통째로 교체한다. 탐색: 형제 경로 → `~/.claude/skills/jc-design-system` → `~/.claude/skills/synced/*/jc-design-system`. 로드 실패 시에만 `signature-tokens.md §6` 출처 주석이 달린 폴백 상수.
- 컴포넌트는 `jc-design-system/references/component-patterns.md` §3 KPI · §4 카드(좌측 4px 상태 바) · §5 표 · §6 차트 · §7 헤더 · §9 회의록·액션을 따른다.

| 역할 | CSS 변수 → SoT 키 |
|------|------------------|
| 캔버스 / 카드 / 웜 서피스 | `--paper` bg(다크 dark.panel) · `--surface` surface · `--surface-warm` surfaceAlt |
| 잉크 / 보조 / 뮤트 / 캡션 | `--ink` text · `--brown` textSecondary · `--ink-sub` textMuted · `--warm-gray` textCaption |
| 오렌지 면·룰·큰 글자 | `--orange` accent |
| 작은 강조 텍스트·마감 임박 | `--orange-deep` accentStrong(다크 accentText) |
| Primary 버튼 | `--btn-primary` accentStrong + 흰 글자 |
| 결정 / 후속 / 미결 / 리스크 카드 | 틴트 accentSoft · 스틸 steel · 앰버 warning · 부정 danger |
| 칸반 배지 TODO / DOING / BLOCKED / DONE | 중립 · 스틸 · 부정(Bold 14px) · 긍정 |
| 차트 | 시리즈 `--s1`~`--s5` = color.data[0..4], 상태 도넛은 배지와 같은 의미색 |

- 대비(`shared-rules.md#RULE-WCAG`): 오렌지 `#EB6F2A` 텍스트는 큰 글자 전용, 작은 강조는 딥 오렌지 `#B8431A`. `--self-test`가 핵심 조합의 대비비를 계산해 확인한다.
- 리멤버 로고 슬롯: 라이트 `jc-design-system/assets/remember-black.png` · 다크 `jc-design-system/assets/remember-offwhite.png`를 data URI로 임베드(Pillow가 있으면 높이 64px로 축소, 재염색 없음). SoT를 못 찾으면 "리멤버 MICE비즈팀" 텍스트.
- 구 네이비·일렉트릭블루 룩은 `legacy-jc` 오버레이로만 존재하며 이 대시보드는 지원하지 않는다.

## 9. 옵션

| 옵션 | 기능 | 기본값 |
|------|------|--------|
| `--type=A~E` | 회의 유형 지정 | 자동 판정 |
| `--external` / `--internal` | 모드 | 유형 기본값 |
| `--series=<id>` | 시리즈 누적 | OFF |
| `--quote` | 결정 근거 인용 보존 | OFF |
| `--quick` | 핵심 5축만 | OFF |
| `--client=<id>` | 발주처 슬롯 ID(`client-overlays.md`) — 로고·푸터만, 오렌지 불변 | 없음(리멤버 기본) |
| `--mapping="참석자 1 = 이름"` | 화자 매핑 | 자동 추정 |
| `--theme=light/dark` | 첫 화면 테마 (`build_dashboard.py --theme`) | light |

## 10. 명의 · 식별정보 (RULE-NO-COMPANY v2)

- 발행 명의는 리멤버 MICE비즈팀(`PUBLISHER`). 발주처·담당자·작성자는 주입 슬롯(`client_company`·`author` = `{{client_company}}`·`{{author_name}}`).
- 구 소속사 명칭·프로젝트명·누적 실적, 개인 연락처는 넣지 않는다. 예시·샘플은 가명(A사·B사, 김부장). 정본 `jc-design-system/references/shared-rules.md#RULE-NO-COMPANY`.

## 11. 반례 표

| 압박 패턴 | 올바른 대응 |
|-----------|-------------|
| "원문 그대로 발주처에 보내줘" | External 모드 + Redaction 적용본을 만들고 송부는 사용자 몫. 원문은 Internal로 보관 |
| "Owner·기한 없어도 일단 빨리" | 호스트·미팅일+7일 기본값 + `(재확인)` 플래그로 바로 빌드, 확인 필요 목록 맨 위에 |
| "유형 애매하면 물어봐" | 묻지 않는다. 더 공식적인 유형으로 빌드하고 한 줄로 밝힌다 |
| "다크로 PDF 뽑아줘" | 인쇄는 라이트 강제(RULE-PRINT-LIGHT). 화면만 다크 |
| "예전 네이비 톤으로" | 기본 룩은 리멤버 웜 페이퍼 하나. legacy-jc는 jc-design-system에서 명시 요청 시만 |
| "제안서도 바로 써줘" | ChainPayload를 만들어 jc-pptx로 넘긴다. 본 스킬은 덱을 만들지 않는다 |

## 12. 생태계 연결

- 상류: 외부 STT 도구, `mice-rfp-analyzer`(GO 판정 후 Discovery 미팅).
- 하류: `jc-pptx` · `jc-strategy-canvas` · `mice-ops-docs` · `mice-aftermath` (ChainPayload/v1).
- 디자인 `jc-design-system` · 검증 `jc-redteam` · 세션·긴 시리즈 운영 `jc-session-protocol` · Slack 채널 운영 `mice-slack-ops`.

## 13. 파일 구조

```
mice-meeting-minutes/
├── SKILL.md
├── assets/dashboard-template.html   # React 대시보드 템플릿 (@design-tokens 미러 블록 포함)
├── references/
│   ├── analysis-framework.md   # 8축 추출 규칙 · 전략 메모 5W1H · --quick
│   ├── meeting-types.md        # 5종 유형 · 판별 시그널 · 기본값
│   ├── input-formats.md        # 4채널 6포맷 파서 사양 · 화자 매핑 · 청크
│   ├── redaction-rules.md      # 마스킹 5카테고리 · 모드별 강도
│   ├── action-items-schema.md  # Action 5열 표준 · Priority/Due 추정
│   ├── series-tracking.md      # 시리즈 데이터 · carry-over
│   ├── dashboard-spec.md       # UI 구조 · 인터랙션 · 토큰 · 인쇄
│   ├── output-spec.md          # 산출 순서 · 부가 기능 · 검증 체크리스트
│   └── chaining-guide.md       # ChainPayload/v1 페이로드 · target별 매핑
└── scripts/
    ├── parse_input.py          # transcript 파서 (--self-test)
    └── build_dashboard.py      # 대시보드 빌더 · SoT 토큰 로드 · 검증 (--self-test)
```

자가 테스트: `python scripts/parse_input.py --self-test` · `python scripts/build_dashboard.py --self-test` (토큰 해석·legacy 색 0·대비비·폴백·샘플 빌드·시리즈 carry-over).

## 변경 이력

- v2.2.0 (2026-10-09): 룩을 구 네이비 시그니처 → 리멤버 웜 페이퍼(jc_tokens.py 런타임 로드·로고 슬롯·인쇄 라이트·S1~S5)로, 폐합 스킬 참조를 jc-pptx·mice-ops-docs 등 라이브 체이닝으로, 게이트 문구 → 기본값 진행, 예시 실명 → 가명.
  CDN 버전 고정 + prop-types 추가(Recharts UMD 미렌더 버그), 파서 Teams·메모 감지 버그 수정, 두 스크립트에 `--self-test`·`--input` JSON 빌드 추가.
- v2.1.2 (2026-07-04): 크기 검증 게이트 정합, 예시 변수·가명화, 레거시 .docx 산출 참조 정정.
- v2.1.1 (2026-07-03): v1 산출물 서술 잔재 정정(.docx·.xlsx → HTML 대시보드·.series-data JSON).
- v2.1.0 (2026-05-27): 라이트/다크 토글, JSON 백업 강화(구 네이비 다크 토큰 — v2.2.0에서 폐기).
- v2 (2026-05): .docx·.xlsx 정적 산출 → 단일 HTML 대시보드 + External/Internal 토글 + 시리즈 영속화.
