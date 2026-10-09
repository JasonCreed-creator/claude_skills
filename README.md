# JC MICE 스킬 라이브러리 — 정본 레포

리멤버 MICE비즈팀이 쓰는 Claude 스킬(`jc-*`·`mice-*`·`pt-script`)의 **단일 진실 공급원(Source of Truth)**. 스킬은 `.claude/skills/`에서 편집하고, `.skill`(ZIP)로 묶어 claude.ai에 올리며, 폐합된 스킬은 `archive/`에 보관한다.

> **2026-10-09 — 교통정리(Full Stocktake) 집행.** 9/21 리멤버 전환 재편(커스텀 30 → 라이브 19종)을 git 정본에 반영했다. 라이브 11종 갱신 + 7종 추가, 폐합 20종 `archive/skills/` 이동, 레거시 파일 보관, CI에 forge 린트 추가. 점검 리포트: [`docs/stocktake-2026-10-09.md`](docs/stocktake-2026-10-09.md) · 변경 상세: [`docs/CHANGELOG-2026-10-09.md`](docs/CHANGELOG-2026-10-09.md) · 복구 지점 태그 `pre-reorg-2026-10-09`.

## 라이브 스킬 카탈로그 (19종)

버전 정본은 각 `SKILL.md` frontmatter. 룩은 **리멤버 웜 페이퍼**(`jc-design-system` v2) 하나, 명의는 리멤버 MICE비즈팀 기본·발주처는 주입 슬롯(RULE-NO-COMPANY v2).

### 리서치 · 전략 · 입력 분석

| 스킬 | 버전 | 역할 | 산출물 |
|------|------|------|--------|
| `mice-market-intel` | v1.2.0 | 시장·경쟁·동향·스폰서 풀·벤치마크 데스크 리서치(출처 티어링) | 리서치 리포트 + ChainPayload |
| `jc-strategy-canvas` | v1.2.0 | 6대 프레임워크(BMC·5 Forces·SWOT/TOWS·JTBD·포지셔닝·TAM/SAM/SOM)로 전략 구조화·권고 | 전략 캔버스 HTML + ChainPayload |
| `mice-rfp-analyzer` | v2.2.0 | RFP·공고 7축 해체, GO/HOLD/NO-GO(강제 조건 우선 판정) · 견적 전용 봉투 | .docx 보고서 + .xlsx 매트릭스 |
| `mice-meeting-minutes` | v2.2.0 | 회의 transcript를 8축으로 구조화, Action 칸반·시리즈 추적 | 인터랙티브 HTML 대시보드 |

### 제안 · 견적 · 발표

| 스킬 | 버전 | 역할 | 산출물 |
|------|------|------|--------|
| `jc-pptx` | v2.3.0 | 제안서(proposal-voice 문체 정본 우선)·스폰서/협찬 제안 덱·소개서·발표덱·결과보고 덱 — 16종 타입·설득 설계·deck_kit 빌드·check_deck 검수 | PPTX (+PDF) |
| `mice-estimate` | v3.3.0 | 리멤버 견적서(패키지 할인 + 기획료) — 컨피규레이터 가격 엔진. **사용자 직접 관리** | XLSX |
| `pt-script` | v2.3.0 | 슬라이드·speaker notes → 발표 대본·전환 멘트·Q&A | DOCX |

### 운영 · 현장 · 사후

| 스킬 | 버전 | 역할 | 산출물 |
|------|------|------|--------|
| `mice-run-of-show` | v1.2.0 | 큐시트(10컬럼 버전드) + 시간 무결성 검증 | XLSX |
| `mice-ops-docs` | v1.2.0 | 운영계획서·팀 지침/그라운드룰·KPI 대시보드·계획 대비 실적 · 기존 HTML 리멤버 룩 리스킨 · 행사 드라이브 운영 표준(폴더·파일명·권한 점검·정리) | Claude Docs / HTML |
| `mice-aftermath` | v1.2.0 | 사후 종합 결과보고서 + 재사용 레퍼런스 케이스 | 결과보고서 + ChainPayload |
| `jc-kv-guide` | v1.2.0 | 디자이너 전달용 키비주얼 제작 가이드(규칙·제약만, 디자인 제안 0) | HTML + MD |

### 팀 운영 · 커뮤니케이션

| 스킬 | 버전 | 역할 | 산출물 |
|------|------|------|--------|
| `mice-slack-ops` | v1.3.0 | 단일 채널·1행사=1스레드 프로토콜, 봇·상태 보드, 월요일/위클리 브리프, 공지·3P·상태/인시던트/리더십 보고·프로젝트 업데이트·뉴스레터·발주처 메일·FAQ 양식 | 복사용 초안 |
| `mice-team-board` | v1.1.0 | 팀 프로젝트 보드(구글시트 + Apps Script) 행 등록·상태 전이·배정·정산 | 행 값 표 / TSV |
| `jc-slack-relay` | v1.1.0 | Code가 읽은 Slack을 md로 저장 → Cowork·채팅이 읽는 중계 경로 | md 파일 |
| `jc-doc-coauthor` | v1.2.0 | 산문형 문서(기획서·전략 메모·Decision Doc·RFC·메시지 기획=행사명·슬로건) 단계별 공동 작성 | Claude Docs / .md |

### 정본 · 메타 · 검증

| 스킬 | 버전 | 역할 | 산출물 |
|------|------|------|--------|
| `jc-design-system` | v2.2.0 | 디자인 토큰 정본(리멤버 웜 페이퍼) + 공통 룰 + ChainPayload/v1 봉투 규약 | reference 자산 (`scripts/jc_tokens.py` 런타임 로드) |
| `jc-session-protocol` | v1.2.0 | 폴더=세션 · 요청 하나=스레드 하나 규약, 체크인/체크아웃, 서브에이전트 병렬·모델 라우팅 | 규약·템플릿 |
| `jc-skill-forge` | v2.2.0 | 스킬 제작·개선·인테이크·점검·배포(린트·빌드·설치 스크립트) | 스킬·.skill |
| `jc-redteam` | v1.4.0 | 완성 산출물 적대적 재검증(Quick Strike / Deep Audit) — 최하류 품질 게이트 | 비평 / 감수 리포트 |

### 체이닝 흐름 (ChainPayload/v1 — 정본 `jc-design-system/references/chaining-protocol.md` §3)

```
mice-market-intel ──► jc-strategy-canvas ──► jc-pptx · mice-rfp-analyzer
mice-rfp-analyzer ──► jc-pptx ──► pt-script ──► mice-run-of-show
mice-rfp-analyzer · jc-pptx ──► mice-estimate
mice-meeting-minutes ──► jc-pptx · mice-estimate · mice-ops-docs · jc-strategy-canvas
mice-run-of-show · mice-meeting-minutes · mice-estimate ──► mice-ops-docs ──► mice-aftermath ──► jc-pptx
mice-slack-ops(contract) ──► mice-team-board ──► mice-ops-docs
jc-design-system ──► (모든 산출 스킬이 토큰·룰·봉투를 런타임 참조)
모든 산출물 ──► jc-redteam
```
구 source(`mice-proposal`·`mice-sponsor-deck` → `jc-pptx`, `mice-dashboard` → `mice-ops-docs`)는 수신 측이 별칭으로 자동 치환한다.

## 폐합 스킬 (20종) — `archive/skills/`

2026-09-21 재편으로 라이브에서 내린 스킬. 삭제하지 않고 마지막 버전 그대로 보관한다. 후속 스킬·흡수 범위·복구 절차는 [`archive/README.md`](archive/README.md).

`mice-proposal` `mice-sponsor-deck` `mice-dashboard` `mice-weekly-performance` `jc-comms` `jc-prompt-builder` `jc-orchestrator` `jc-workspace-ops` `jc-skill-creator` `jc-remember-html` `jc-theme-factory` `jc-brand-styling` `jc-cinematic-html` `jc-asana-html` `jc-visual-philosophy` `jc-generative-art` `jc-brand-discovery` `jc-landing-page` `jc-artifact-builder` `jc-mcp-builder`

> claude.ai에 아직 올라가 있는 폐합 스킬은 Settings → Capabilities에서 **사용자가 삭제**해야 synced 목록·Cowork에서 사라진다(`jc-skill-forge/references/deploy-pipeline.md` §5).

## 디렉터리 구조

```
.claude/skills/<스킬명>/     # 라이브 스킬 19종 (SKILL.md + references/ scripts/ assets/)
archive/skills/<스킬명>/     # 폐합 스킬 20종 (로드되지 않음)
archive/legacy/              # 구 커맨드·스크립트·안내문
scripts/check_drift.py       # SoT 디자인 토큰 드리프트 가드 (라이브 스킬 동적 탐색)
docs/                        # 점검 리포트 · CHANGELOG · 결정 매트릭스
PROGRESS.md                  # 인테이크·점검 로그
```

## 작업 규칙

- **편집 → 검증 → 빌드 → 배포** 순서와 채널 구분(①소스 반영 ②Code 설치 ③claude.ai 업로드)은 `jc-skill-forge/references/deploy-pipeline.md`가 정본. "소스 반영 ≠ 배포".
- **검증(마감 조건)**: 아래 넷이 모두 통과해야 한다. CI(`.github/workflows/drift-guard.yml`)가 PR마다 같은 검사를 돌린다.
  ```bash
  python3 .claude/skills/jc-skill-forge/scripts/lint_skills.py --exclude mice-estimate   # 하우스 규약 · 폐합 참조 · 구 룩
  python3 scripts/check_drift.py                                                         # 디자인 토큰 드리프트
  python3 .claude/skills/jc-design-system/scripts/test_jc_tokens.py
  python3 .claude/skills/jc-skill-forge/scripts/build_skills.py --self-test
  ```
- **빌드**: `python3 .claude/skills/jc-skill-forge/scripts/build_skills.py` → `dist/skills/<name>.skill`(ZIP만, `dist/`는 gitignore). 업로드는 사용자가 claude.ai에서.
- **버전**: 수정하면 `version` 범프(SemVer) + `## 변경 이력` 1항. 커밋 메시지 `<스킬명>: <요약>`.
- **의존성**: `python-pptx`·`Pillow`(jc-pptx) · `openpyxl`(mice-estimate·mice-run-of-show) · `python-docx`(pt-script·mice-rfp-analyzer). 각 스킬 frontmatter `dependencies`와 스크립트의 미설치 안내가 정본.

## 이력 문서

`docs/CHANGELOG-2026-10-09.md`(교통정리) · `docs/stocktake-2026-10-09.md`(전수 점검 리포트) · `docs/CHANGELOG-2026-07-04.md` · `docs/CP3-decision-matrix.md` · `docs/skill-intake-log.md` · `docs/preset-optimization-roadmap.md`(프리셋 개조 프로그램 — 2026-09 재편으로 종료) · `PROGRESS.md`
