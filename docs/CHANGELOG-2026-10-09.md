# CHANGELOG — 스킬 라이브러리 교통정리 (2026-10-09)

> 브랜치 `claude/lucid-franklin-37n8cu` · 드래프트 PR #23 · 복구 지점 커밋 `8e47432`(로컬 태그 `pre-reorg-2026-10-09`) · 점검 리포트 `docs/stocktake-2026-10-09.md`
> 원칙: 2026-09-21 재편(라이브 19종 / 폐합 20종, 10-05 lint 목록) 결정은 유지. 집행 + 경계 수정 + 역량 계승 + 업그레이드. mice-estimate는 사용자 관리 스킬이라 내용 무수정(업로드본 동기만).

## 1. 구조 변경

- 폐합 3종(jc-asana-html·jc-remember-html·mice-weekly-performance) 히스토리 보존 → 라이브 18종 업로드본 동기 → 폐합 20종 `archive/skills/` 이동(git mv) + 레거시 3파일 `archive/legacy/` + `archive/README.md`
- `scripts/check_drift.py` 동적 탐색(SoT·메타 스킬 제외) · `.github/workflows/drift-guard.yml`에 forge 린트(`--exclude mice-estimate`)·`test_jc_tokens.py`
- README 재작성(라이브 19종 카탈로그·체이닝·아카이브·작업 규칙) · `docs/skill-intake-log.md` 머리말(forge 모드 A 단일 트래커)

## 2. 스킬 버전 대조표 (git 이전 → 현행)

| 스킬 | git 이전 | 현행 | 변경 요지 |
|------|---------|------|----------|
| jc-design-system | v1.4.0 | **v2.2.0** | 업로드본 v2.1.0 동기 → 체이닝 enum 라이브 19종 전수 분류(가이드·문서 행·봉투 비대상), §4 정본 키(kv-guide=guide.schema.json·market-intel 신규 키·rfp 견적 전용 봉투·jc-pptx 평탄 키), §5 흐름 현행화, 체이닝 봉투 절, description에 jc-kv-guide 경계, shared-rules 소비 목록 mice-estimate·'공공형' 폐지, usage-guide §2 산출 형식 정정 |
| jc-skill-forge | v1.0.3 | **v2.2.0** | 업로드본 v2.1.0 동기 → ARCHIVE = `archive/skills/`(+LIVE/ARCHIVED·archive/README·chaining §3 같은 커밋), 진행 규약·모델은 session-protocol 포인터, lint `CURRENT_MODELS`·LIVE↔chaining enum 대조 WARN·**description 트리거 중복 WARN(재발 방지)**, 프리셋 skill-creator 대비 우선권 문장, upstream-machinery synced 위치 |
| jc-session-protocol | (없음) | **v1.2.0** | 신규 편입 v1.1.0 → '세션 체크인'·'킥오프 블록' 등 현장 어휘와 충돌 트리거 한정, 모델 라우팅 단일 정본 + 복제 위치 체크리스트, turn-protocol 판정 라벨을 redteam 3종으로 |
| jc-redteam | v1.2.2 | **v1.4.0** | 업로드본 v1.3.0 동기 → 체이닝 표에 jc-doc-coauthor(문서 유형별 공격 포인트 6종 이관)·jc-kv-guide·mice-slack-ops·jc-skill-forge(스킬 인테이크 감수) 4절, 본문 호출 표 제거 |
| jc-pptx | (없음) | **v2.3.0** | 신규 편입 v2.1.0 → v2.2.0 스폰서·협찬 제안 덱 계승(`sponsor-deck.md`, 트리거 4종, aftermath R2 수신), 상류 봉투 수신 표(estimate·strategy-canvas·market-intel·aftermath), 견적 입력 키 평탄, 경계 정정 → v2.3.0 **proposal-voice v1.1.0 계승**(우선권, 규칙 충돌 3건 정리, 제안서 게이트 10항) + check_deck.py --voice proposal·--self-test(A4 추출 버그 수정), 프리셋 pptx 역할 문구 정정(893자) |
| jc-kv-guide | (없음) | **v1.2.0** | 신규 편입 v1.1.0 → '디자인 가이드' → 'KV 디자인 가이드', 입력을 jc-doc-coauthor 메시지 기획 문서 key_message로, 봉투 정본 guide.schema.json |
| jc-doc-coauthor | v1.0.1 | **v1.2.0** | 업로드본 v1.1.0 동기 → '운영계획서' 트리거 양보(mice-ops-docs), 결과보고 유형 제거(mice-aftermath), 행사명·슬로건 **메시지 기획 문서** 유형·`message-planning.md` 계승, 골격·공격 포인트는 정본 포인터 |
| pt-script | v2.0.0 | **v2.3.0** | 업로드본 v2.2.0 동기 → 트리거 한정('발표 연습 원고'·'피티 대본'·'사회자 대본'·'진행 멘트'), 큐시트는 하류 아님(봉투 미생산 명시) |
| mice-rfp-analyzer | v2.0.1 | **v2.2.0** | 업로드본 v2.1.0 동기 → xlsx 종합 판정 강제 조건 우선 수식 + `rule_judgment()`, 견적 전용 봉투 §3-1, `open_questions`→market-intel 재조사, 트리거 '응찰 GO/NO-GO' 한정, Quick 모드 3문서 통일, LICENSE.txt |
| jc-strategy-canvas | v1.0.2 | **v1.2.0** | 업로드본 v1.1.0 동기 → bare 트리거('전략'·'시장 규모'·'경쟁 구도') 제거, market-intel/rfp-analyzer 대칭 경계, 수신 매핑(competitor_tier·whitespace·aftermath R3), §2 호출표 삭제 |
| mice-market-intel | v1.0.4 | **v1.2.0** | 업로드본 v1.1.0 동기 → 수집/판단 경계 대칭, 경쟁분석 '전략 권고' → 후보 수, 봉투 competitor_tier·scores·tension_axes·whitespace_candidates·source_tier, rfp open_questions 수신, deep-research 표기 정정 |
| mice-meeting-minutes | v2.1.2 | **v2.2.0** | 리멤버 웜 페이퍼 전환(jc_tokens 런타임 로드·로고 슬롯·인쇄 라이트·S1~S5), 폐합 참조·게이트 문구 정리(description 928자), Recharts UMD 미렌더 버그(prop-types·CDN 핀), 파서 버그 2건, `--self-test`, 예시 가명화, 체이닝 target 4종 |
| mice-run-of-show | v1.0.0 | **v1.2.0** | 업로드본 v1.1.0 동기 → 상류 = jc-pptx 봉투(presentation.minutes)+대화 입력(pt-script 상류 전제 제거), '진행 시나리오' → '연출 시나리오', chaining-protocol 절 번호 잔재 정리 |
| mice-aftermath | v1.0.0 | **v1.2.0** | 업로드본 v1.1.0 동기 → 결과보고 공동 집필을 자체 축별 확인 옵션으로, rfp-analyzer 회고 입력, R3 케이스 → jc-strategy-canvas, 경계(market-intel 벤치마크), v1.1.0 중복 이력 통합 |
| mice-ops-docs | (없음) | **v1.2.0** | 신규 편입 v1.0.0 → v1.1.0 HTML 리멤버 룩 리스킨 계승(`html-reskin.md`), '목표 대비' 한정, 운영계획서 골격·Ground Rule 문체 정본 선언(+규칙 2항 이관) → v1.2.0 행사 드라이브 운영 표준 계승(`drive-standards.md`) (151줄, 보조 폴더 3개는 사용자 결정) |
| mice-slack-ops | (없음) | **v1.3.0** | 신규 편입 v1.1.0 → v1.2.0 team-board 경계 대칭('계약완료 보드 등록'), relay 트리거 분리, contract status_hint·notes 의미, 시트 열·문체·경로 정본 포인터화 → v1.3.0 커뮤니케이션 양식 계승(뉴스레터·프로젝트/리더십 업데이트·3P 세부) (comms-templates 94→210줄, description 1,002자) |
| mice-team-board | (없음) | **v1.1.0** | 신규 편입 v1.0.0 → 갱신 시 상태 역행 버그 수정(status_hint), notes 이중 기재 제거, 시트 열 정의 정본(sheet-schema §2), slack-ops 상태 보드와 경계 |
| jc-slack-relay | (없음) | **v1.1.0** | 신규 편입 v1.0.0 → relay 전용 트리거, 경로 정본 선언, 요약 절 위임 |
| mice-estimate | v3.0.0 | v3.3.0 | 업로드본 동기만(사용자 관리). 패치 목록은 리포트 §6 카드 C |

## 3. 폐합 20종 → `archive/skills/`

mice-proposal · mice-sponsor-deck · mice-dashboard · mice-weekly-performance · jc-comms · jc-prompt-builder · jc-orchestrator · jc-workspace-ops · jc-skill-creator · jc-remember-html · jc-theme-factory · jc-brand-styling · jc-cinematic-html · jc-asana-html · jc-visual-philosophy · jc-generative-art · jc-brand-discovery · jc-landing-page · jc-artifact-builder · jc-mcp-builder — 후속·흡수 범위·복구 절차는 `archive/README.md`.

## 4. 배포 (③ claude.ai — 사용자)

`python3 .claude/skills/jc-skill-forge/scripts/build_skills.py` → `dist/skills/*.skill` 18종(ZIP). claude.ai Settings → Capabilities에서 **폐합 19종 삭제 → 동명 구스킬 삭제 → 18종 업로드**(mice-meeting-minutes는 신규). 약 10분 후 synced manifest에서 버전 확인. 상세: `jc-skill-forge/references/deploy-pipeline.md` §5.
