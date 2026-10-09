# 스킬 라이브러리 전수 점검(Full Stocktake) · 교통정리 집행 리포트

- **일자**: 2026-10-09 · **모드**: jc-skill-forge D 점검(Full Stocktake) → 사용자 지시("스킬 파일도 수정, 통폐합하면서 계승·업그레이드")로 **집행까지** · **브랜치** `claude/lucid-franklin-37n8cu` · 드래프트 PR #23
- **대조 소스 3종**: ① 의도된 상태 = `jc-skill-forge` `scripts/lint_skills.py`의 `LIVE`(19종)·`ARCHIVED`(20종) 목록(2026-10-05) ② claude.ai 실제 업로드본 = `~/.claude/skills/synced/`(manifest 2026-10-09, 48종) ③ git 정본 = 본 레포 `.claude/skills/`(점검 시점 29종)
- **검증 방법**: 결정론 검사(forge lint·check_drift·트리거 키워드 교차·교차 언급 그래프·manifest 일자) + 워크플로우(경계검증 6클러스터 → 폐합 20종 흡수감사 4배치 → 비평가 2명 반박) + 각 적용 에이전트의 사실 재확인
- **복구 지점**: 커밋 `8e47432`(라이브 19 + 폐합 20종이 전부 존재하는 마지막 상태; 로컬 태그 `pre-reorg-2026-10-09` — 원격 태그 push는 세션 권한상 거부됨)

---

## 0. 핵심 결론

"중복돼 보인다"의 정체는 **세 층**이었고, 그중 두 층은 이미 내려진 결정(2026-09-21 "커스텀 30→14종 재편" → 10-05 라이브 19종 확정)이 **집행되지 않은 것**이었다.

| 층 | 현상(점검 시점) | 원인 | 이번 처리 |
|---|---|---|---|
| A. claude.ai | 폐합 20종 중 **19종이 그대로 업로드**돼 계속 발동·노출 (manifest: 전부 10-02 08:41 일괄 재업로드, 10-05 라이브 갱신 때 삭제 누락) | 삭제는 사용자만 가능한 ③ 채널 작업 | **사용자 작업** — §6 카드 A |
| B. Claude Code 목록 | 같은 스킬이 `/jc-xxx`(레포 프로젝트 스킬)와 `/anthropic-skills:jc-xxx`(synced) 둘로 노출 | 레포 루트에서 Code를 열면 `.claude/skills/`와 synced가 동시 로드되는 구조 | 구조상 불가피 — 실무 세션은 행사 폴더에서 열기(§6 카드 G) |
| C. git 정본 | 9/21 재편 **이전** 상태 — 라이브 7종 없음·11종 구버전·폐합 17종 잔존, `mice-meeting-minutes`는 거꾸로 claude.ai에 없음 | 9/21~10/05 작업이 업로드본에서만 진행 | **집행 완료** — 라이브 19종 정본화, 폐합 20종 `archive/skills/` 이동(삭제 아님) |

그 위에서 **라이브 19종 안의 중복**을 워크플로우로 다시 뒤졌다. 경계검증 6클러스터가 90건을 찾았고(Critical 6·Major 44·Minor 40), 적용 에이전트 4개가 레포 파일로 사실 확인 후 **17종을 개정**했다(미적용 1건 = 오탐, mice-estimate 7건 = 사용자 관리 스킬이라 패치 목록으로). 흡수감사는 폐합 20종 중 **계승 가치 high 2·medium 4**를 적발했고, 그중 high 2(스폰서 덱·제안서 문체 정본)와 medium 4(네이밍·슬로건, HTML 리스킨, 커뮤니케이션 양식, 드라이브 운영 표준)를 라이브 후속에 이관했다.

**결과**: `.claude/skills/` = 라이브 19종(전부 하우스 규약 v2.1, lint ERROR 0) · `archive/skills/` = 폐합 20종 · CI(drift-guard)에 forge 린트 추가 · README·CHANGELOG·PROGRESS 갱신. **claude.ai 반영은 아직 0**(소스 반영 ≠ 배포) — §6.

---
## 1. 세 집합 대조표 (스킬 × 의도 / claude.ai / git)

판정 기준: LIVE인데 어느 채널에 없거나 버전이 다르면 ⚠, ARCHIVED인데 어느 채널에 남아 있으면 ⚠.

| 스킬 | 의도(10-05) | claude.ai 업로드 | git 정본 | 판정 |
|---|---|---|---|---|
| jc-design-system | LIVE | v2.1.0 | v1.4.0 | ⚠ git 구버전 |
| jc-doc-coauthor | LIVE | v1.1.0 | v1.0.1 | ⚠ git 구버전 |
| jc-kv-guide | LIVE | v1.1.0 | 없음 | ⚠ git에 없음 |
| jc-pptx | LIVE | v2.1.0 | 없음 | ⚠ git에 없음 |
| jc-redteam | LIVE | v1.3.0 | v1.2.2 | ⚠ git 구버전 |
| jc-session-protocol | LIVE | v1.1.0 | 없음 | ⚠ git에 없음 |
| jc-skill-forge | LIVE | v2.1.0 | v1.0.3 | ⚠ git 구버전 |
| jc-slack-relay | LIVE | v1.0.0 | 없음 | ⚠ git에 없음 |
| jc-strategy-canvas | LIVE | v1.1.0 | v1.0.2 | ⚠ git 구버전 |
| mice-aftermath | LIVE | v1.1.0 | v1.0.0 | ⚠ git 구버전 |
| mice-estimate | LIVE | v3.3.0 | v3.0.0 | ⚠ git 구버전 (사용자 직접 관리) |
| mice-market-intel | LIVE | v1.1.0 | v1.0.4 | ⚠ git 구버전 |
| mice-meeting-minutes | LIVE | **없음** | v2.1.2 | ⚠ **claude.ai에 없음** + git 사본은 구 규약(lint ERROR 47) |
| mice-ops-docs | LIVE | v1.0.0 | 없음 | ⚠ git에 없음 |
| mice-rfp-analyzer | LIVE | v2.1.0 | v2.0.1 | ⚠ git 구버전 |
| mice-run-of-show | LIVE | v1.1.0 | v1.0.0 | ⚠ git 구버전 |
| mice-slack-ops | LIVE | v1.1.0 | 없음 | ⚠ git에 없음 |
| mice-team-board | LIVE | v1.0.0 | 없음 | ⚠ git에 없음 |
| pt-script | LIVE | v2.2.0 | v2.0.0 | ⚠ git 구버전 |
| jc-artifact-builder | ARCHIVED | 잔존(버전 없음) | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| jc-asana-html | ARCHIVED | 잔존 v1.0.0 | 없음 | ⚠ claude.ai 삭제 |
| jc-brand-discovery | ARCHIVED | 잔존 v1.0.0 | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| jc-brand-styling | ARCHIVED | 잔존 v1.0.1 | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| jc-cinematic-html | ARCHIVED | 잔존 v1.0.0 | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| jc-comms | ARCHIVED | 잔존 v1.0.0 | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| jc-generative-art | ARCHIVED | 잔존 v1.0.2 | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| jc-landing-page | ARCHIVED | 잔존(버전 없음) | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| jc-mcp-builder | ARCHIVED | 잔존 v1.0.1 | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| jc-orchestrator | ARCHIVED | 잔존 v1.1.2 | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| jc-prompt-builder | ARCHIVED | 잔존 v1.0.1 | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| jc-remember-html | ARCHIVED | 잔존 v1.0.0 | 없음 | ⚠ claude.ai 삭제 |
| jc-skill-creator | ARCHIVED | 잔존 v1.0.1 | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| jc-theme-factory | ARCHIVED | 잔존 v1.1.0 | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| jc-visual-philosophy | ARCHIVED | 잔존 v1.0.1 | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| jc-workspace-ops | ARCHIVED | 잔존 v1.1.0 | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| mice-dashboard | ARCHIVED | 잔존 v2.0.3 | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| mice-proposal | ARCHIVED | 잔존 v3.1.2 | 잔존 | ⚠ claude.ai 삭제 · git 정리 |
| mice-sponsor-deck | ARCHIVED | 없음 | 잔존 v2.0.1 | ⚠ git 정리 |
| mice-weekly-performance | ARCHIVED | 잔존(버전 없음) | 없음 | ⚠ claude.ai 삭제 |

**집계** — 폐합 잔존: claude.ai 19종 / git 17종 · 라이브 결손: git 7종 없음 + 11종 구버전, claude.ai 1종 없음(`mice-meeting-minutes`) · 의도 목록 밖의 스킬: 0종.

업로드 일자(manifest `updatedAt`)가 이를 뒷받침한다: 폐합 19종은 전부 **2026-10-02 08:41~08:42**에 일괄 재업로드됐고, 라이브 18종은 **2026-10-05 13:44~13:45**에 올라갔다. 즉 10-02 일괄 업로드 뒤 10-05 라이브 갱신 때 폐합분 삭제가 빠졌다.

### 1-1. lint 결과 (forge v2.1.0 `lint_skills.py`, 자가 테스트 PASS)

| 대상 | 스킬 수 | ERROR | WARN | 비고 |
|---|---|---|---|---|
| claude.ai 업로드본 전체 | 48 | 432 | 70 | ERROR의 **97%가 폐합 19종**에서 발생 |
| 〃 라이브 19종만 | 18 | 14 | 17 | ERROR 14건 전부 `mice-estimate`(폐지 게이트 문구·`mice-proposal` 참조·`/mnt` 경로). `mice-slack-ops` WARN 3건은 채널명 `#mice-biz-team`을 스킬명으로 오인한 오탐 |
| git 레포 전체 | 29 | 869 | 56 | 라이브 사본 12종이 모두 구 규약(구 시그니처 HEX·폐합 참조·브리프 게이트) |

폐합 스킬별 ERROR(업로드본): jc-prompt-builder 84 · mice-dashboard 50 · jc-generative-art 40 · mice-proposal 36 · jc-brand-styling 30 · jc-orchestrator 30 · jc-theme-factory 26 · jc-artifact-builder 23 · jc-brand-discovery 19 · jc-asana-html 15 · jc-visual-philosophy 13 · jc-workspace-ops 12 · jc-cinematic-html 10 · jc-mcp-builder 9 · jc-comms 7 · jc-remember-html 5 · jc-skill-creator 5 · jc-landing-page 3 · mice-weekly-performance 0.

### 1-2. 키워드 충돌 실측 (description 인용 트리거 기준, 라이브+폐합 39종)

동일 트리거가 2개 이상 description에 존재: 25개. 그중 **폐합 스킬이 끼지 않은 라이브↔라이브 충돌은 7개뿐**이다.

| 트리거 | 라이브 스킬 | 상태 |
|---|---|---|
| '운영계획서' | jc-doc-coauthor ↔ mice-ops-docs | §2에서 판정 |
| 'KPI 대시보드' | mice-ops-docs ↔ (폐합 mice-dashboard) | 폐합 삭제로 해소 |
| '시장 규모' | jc-strategy-canvas ↔ mice-market-intel | §2에서 판정 |
| '보드에 등록' | mice-slack-ops ↔ mice-team-board | §2에서 판정 |
| '제안서' · 'PT 자료' | jc-pptx ↔ (폐합 mice-proposal·mice-sponsor-deck) · mice-meeting-minutes | 폐합 삭제로 대부분 해소, minutes는 §2 |
| '견적서' | mice-estimate ↔ mice-meeting-minutes | §2에서 판정 |
| '주간 업데이트' | mice-slack-ops ↔ (폐합 jc-comms) | 폐합 삭제로 해소 |

나머지 18개 충돌('체크인'·'체크아웃'·'세션 이어서'·'스킬 만들어줘'·'리멤버 룩' 등)은 모두 **폐합 스킬이 한쪽**이다 — 즉 claude.ai에서 폐합분을 지우는 순간 사라진다.

## 2. 라이브 19종 경계 교차검증 — 발견 90건과 처리

워크플로우 경계검증(클러스터 6개, 각 에이전트가 SKILL.md 전체 + 체이닝 reference를 읽고 상대 스킬 description과 대조). 발견 전문(파일:줄 근거 포함)은 세션 산출물이며, 아래는 처리 결과 요약이다. ID는 `C<클러스터>-<번호>`.

| 클러스터 | 발견 | 적용 스킬(버전) | 핵심 처리 |
|---|---|---|---|
| 1 문서·보고 | 16 | jc-doc-coauthor v1.2.0 · mice-ops-docs v1.1.0 · mice-aftermath v1.2.0 · jc-kv-guide v1.2.0 · (mice-meeting-minutes v2.2.0) | **C1-1 Critical** '운영계획서' 트리거 충돌 → doc-coauthor가 양보, '같이 쓰자' 신호일 때만 / C1-6 결과보고 유형을 aftermath로 일원화 / C1-7 네이밍·슬로건 공백 → doc-coauthor 메시지 기획 문서 신설 / C1-5·C1-13 운영계획서 골격·Ground Rule 문체 정본을 ops-docs로 / C1-10 HTML 리스킨 주인 없음 → ops-docs / C1-2·C1-3·C1-8 meeting-minutes 구 규약 → v2.2.0 |
| 2 덱·대본·RFP·견적 | 19 | jc-pptx v2.2.0 · pt-script v2.3.0 · mice-run-of-show v1.2.0 · mice-rfp-analyzer v2.2.0 | **C2-1 Critical** rfp→견적 봉투 키 불일치 → rfp-analyzer §3-1 견적 전용 봉투(송신 측 해소) / **C2-2 Critical** jc-pptx→견적 estimate_hint 중첩·옵션 키 불일치 → 평탄 스키마로 / C2-9·C5-5 스폰서 덱 공백 → jc-pptx sponsor-deck.md 계승 / C2-7·C2-10·C4-5 죽은 target 4건 → playbook §1 수신 표 / C2-8·C3-7 pt-script↔run-of-show 순환 → run-of-show 상류 = jc-pptx+대화 / C2-14·C2-15 트리거 한정 |
| 3 운영·Slack·보드·큐시트 | 14 | mice-slack-ops v1.2.0 · mice-team-board v1.1.0 · jc-slack-relay v1.1.0 | C3-1 '보드에 등록' 충돌 → '계약완료 보드 등록' + 상태 보드/팀 보드 경계 / C3-2 relay 트리거 분리 / **C3-4 상태 역행 버그**(갱신 시 '준비'→'계약' 역행) → status_hint + board_rows.py 수정·self-test / C3-5·C3-6 contract notes 의미·시트 열 정본 일원화 / **C3-10 미적용(오탐)** — 세 description 모두 1,024자 이내 |
| 4 전략·리서치 | 22 | jc-strategy-canvas v1.2.0 · mice-market-intel v1.2.0 · mice-rfp-analyzer v2.2.0 | C4-1·C4-2·C4-10·C4-12·C4-13 bare 트리거('전략'·'시장 규모'·'경쟁 구도'·'환경 분석'·'GO/NO-GO') 한정·대칭 경계 / C4-3·C4-4 market-intel 경쟁분석 산출을 후보 수로 격하 + 봉투 스키마 / **C4-8** xlsx 종합 판정이 가중합산만으로 GO를 찍던 불일치 → 강제 조건 우선 수식 + rule_judgment() / C4-19 존재하지 않는 `deep-research` 라우팅 정정 |
| 5 메타·세션·디자인·검증 | 19 | jc-skill-forge v2.2.0 · jc-session-protocol v1.2.0 · jc-design-system v2.2.0 · jc-redteam v1.4.0 | C5-2·C5-3 진행 규약·모델 라우팅 3중 복제 → session-protocol 단일 정본 + 복제 위치 체크리스트 / **C5-8** forge의 ARCHIVE 정의가 gitignore된 `_archive/`를 가리켜 "삭제 아닌 아카이브" 원칙이 실제로 안 지켜짐 → `archive/skills/` 정의 / C5-6 체이닝 enum이 라이브 19종과 불일치 → 전수 분류 + lint 대조 / C5-4 redteam이 4종의 출구를 안 받음 → 4절 신설 / C5-18 '체크인·체크아웃·킥오프'가 현장 어휘와 충돌 → 한정 |
| 6 프리셋·공용 | (아래 §4) | — | 프리셋 11종 유지/비활성화 판정 |

**mice-estimate(사용자 직접 관리 — 내용 미수정)** 관련 발견 7건(C2-3·C2-4·C2-5·C2-6·C2-13·C2-17·C5-7)은 §6 카드 C의 패치 목록으로 넘겼다. 핵심은 description의 폐합 스킬명·폐지 게이트 문구(claude.ai에 jc-prompt-builder가 남아 있어 견적 요청마다 브리프 게이트가 실제 발동)와 `/mnt` 절대경로(Windows Code·Cowork에서 recalc 단계 실패)다.

### 2-1. 비평가 반박 결과

비평가(경계발견)가 Major 이상 71건의 근거 파일을 **적용 후 레포 상태로 다시 읽어** 판정했다.

| 판정 | 건수 | 내용 |
|---|---|---|
| 반박 → drop(이미 반영) | 51 | 적용 에이전트의 수정이 파일에 실재함을 파일:줄로 재확인(= 적용 검증) |
| 유지 Critical | 2 | F1-3 mice-meeting-minutes claude.ai 미업로드 · F6-1 폐합 19종 잔존 — 둘 다 ③ 채널 사용자 작업(§6 A·B) |
| 유지 Major | 5 | F2-2(1)·F2-3·F2-5·F2-6·F6-14 — 전부 mice-estimate(사용자 관리) 패치 항목(§6 C) |
| 유지 Minor | 4 | F2-4 mice-estimate 경계 · F6-12 mice-estimate 실명·구 파일명 · F6-16 doc-coauthoring 비활성화 권고 · F5-4 잔여 없음 |
| 반박 → Minor | 1 | F6-17 pptx 프리셋 비활성화는 손실이 더 큼 → 유지하되 jc-pptx description의 "빌드 기계로만 참조" 문구를 "외부 .pptx 읽기·편집·OOXML 작업용"으로 정정(**적용**) |
| 유지 drop | 8 | 프리셋 유지 판정 타당(조치 없음) |
| 오탐 확정 | 1 | C3-10 description 1,024자 초과 — 바이트(wc -m) 계산 오류, lint는 문자 수 |

비평가가 추가로 찾은 누락 3건: ① claude.ai 동기화본이 git보다 한 버전 뒤(배포 공백 — §6 A·B) ② deploy-pipeline.md:27의 "37종 업로드" 시점 팩트는 업로드 완료 후 갱신(지금 고치면 또 틀림) ③ mice-estimate chaining-schema·jc-design-mapping의 폐합 참조 추가 줄 → §6 카드 C에 포함.

### 2-2. 적용하면서 발견과 다르게 판단한 것(에이전트 보고)

- C2-2: mice-estimate 입력 스키마 정본은 chaining-schema §2(§3은 rfp 입력) — 봉투는 `estimate_hint` 중첩이 아니라 최상위 평탄 키로(mice-estimate가 최상위만 읽음).
- C4-16: `recommended_bid`는 rfp 페이로드의 `analysis_result`가 아니라 `estimate_hint`(→ v2.2.0에서 견적 전용 봉투 §3-1) 아래 — 정확한 경로로 기재.
- C4-18: 7축 점수표는 삭제 대신 "참고 지표"로 강등(승률 추정에 쓰임).
- C5-6: jc-doc-coauthor는 '수신 전용'이 아니라 메시지 기획 문서 봉투를 산출하게 됐으므로 '선택 산출'로 등록.
- C1-6: 스크립트 없는 스킬이라 `--interactive` 플래그 대신 "축별 확인 옵션" 절차로.

## 3. 폐합 20종 흡수 감사 — 역량이 라이브로 갔는가

4배치 에이전트가 각 폐합 스킬의 고유 역량(3~8개)을 뽑고 라이브 19종 전체를 grep·열람해 존재 여부를 판정했다. `recovery` = 리멤버 MICE비즈팀 팀장 업무(견적·제안서·운영계획·현장·결과보고·Slack·팀 보드) 관점의 복구 가치.

| 폐합 | 선언된 후속 | 판정 | 가치 | 남은 공백(요지) | 이번 조치 |
|---|---|---|---|---|---|
| mice-sponsor-deck | jc-pptx | partial | **high** | Tier 표준·혜택 7범주·ROI 3단·청중 데이터·진입 트리거 전부 없음 | **계승** — jc-pptx v2.2.0 `references/sponsor-deck.md` + 트리거 4종 + aftermath R2 수신 |
| mice-proposal | jc-pptx | partial | **high** | 흡수 기준이 v3.0.1이라 **proposal-voice v1.1.0**(9/25 코퍼스 증류, 블라인드 통과, 우선권 승격) 미계승 + 규칙 충돌 3건(헤드라인 어투·7섹션 순서·모객 개런티) + 게이트 7~10 | **계승** — jc-pptx v2.3.0 `references/proposal-voice.md`(206줄, 원문 보존) + 충돌 3건 정리(제안서=명사형 종결 카피 / 발주처 목차 우선·없으면 회사소개 앞단 / 모객 개런티는 모객형만) + 제안서 게이트 10항 + `check_deck.py --voice proposal`(기존 A4 명사구 검사가 deck_kit 덱에서 작동하지 않던 버그도 수정) |
| jc-brand-discovery | (없음) | partial | medium | 행사명·슬로건·보이스 발굴 역량 0, kv-guide가 미루는 곳 공백 | **계승** — jc-doc-coauthor v1.2.0 `message-planning.md`(인터뷰 규율·state.json·Track B는 의도적 제외) |
| jc-brand-styling · jc-cinematic-html · jc-asana-html · jc-remember-html | jc-pptx(PPTX 리스킨) / design-system | partial·absorbed | low | **기존 HTML 리스킨** 절차의 라이브 주인 없음(룩 자체는 의도적 폐기) | **계승** — mice-ops-docs v1.1.0 `html-reskin.md` + 트리거 'HTML 리스킨' |
| jc-comms | mice-slack-ops | partial | medium | 뉴스레터·프로젝트 업데이트 6항·리더십 업데이트 골격·트리거 어휘 12종 | **계승** — mice-slack-ops v1.3.0 `comms-templates.md` 94→210줄(양식 고르기 표 9종, 뉴스레터, 프로젝트 업데이트 6항, 리더십/경영진 업데이트, 3P 세부 규칙, 인시던트 1보) + 트리거 9종(1,002자) |
| jc-workspace-ops | jc-session-protocol | partial | medium | 행사 폴더 위계·파일명 규약·공유 권한 위생 P1~P6·트래커·청소 루틴(세션 층만 이관됨) | **계승** — mice-ops-docs v1.2.0 `drive-standards.md` `drive-standards.md` 151줄 — mice-slack-ops protocol §4 폴더 구조(01~06)에 맞춰 재작성, 배치 매트릭스 20행, 파일명 규약, 권한 점검 P1~P6, 행사 체크리스트 시트(팀 보드와 역할 구분), 정리 루틴(권한 변경·삭제·이동은 안내만) + 트리거 6종(1,005자). 보조 폴더 3개(07_발주처공유·99_archive·00_공통)는 사용자 결정(§6 카드 H) |
| mice-dashboard | mice-ops-docs | partial | medium | xlsx/csv 입력·KPI 자동 감지·Chart.js 6종 자동 선택·레이더/매트릭스·다크 5변형·HTML 템플릿·PDF 생성 | **백로그**(§6 카드 F) — ops-docs는 SVG 우선 경량 설계가 사용자 결정(10-05) |
| mice-weekly-performance | mice-slack-ops | absorbed | — | 없음 | — |
| jc-skill-creator | jc-skill-forge | absorbed | low | 프리셋 개조 플레이북 링크만 | — |
| jc-prompt-builder · jc-orchestrator | jc-session-protocol | partial | low | 라우팅 맵·registry 생성기·effort 등급표·Chat 킥오프·아키타입 계약 — 게이트 자체는 의도적 폐지 | — (백로그: effort 등급표) |
| jc-theme-factory | design-system | partial | low | 쇼케이스·오버레이 검증기 — 오버레이 발행 자체가 설계상 폐기(슬롯 3종) | — |
| jc-visual-philosophy · jc-generative-art · jc-landing-page · jc-artifact-builder · jc-mcp-builder | (없음) | none·partial | low | 정적 아트·p5.js·랜딩페이지(GAS 폼)·React 아티팩트·MCP 서버 개발 — 의도적 폐기(이미지는 Higgsfield, 룩은 하나, React는 프리셋) | — 필요 시 `archive/skills/`에서 복구(`archive/README.md` 절차) |

라이브 19종에 남아 있던 폐합 스킬 비이력 참조는 **mice-estimate 9곳**(§6 카드 C)뿐이며 나머지는 lint ERROR 0으로 확인했다.

### 3-1. 역량 공백 비평가 검증

비평가(역량공백)가 공백 주장 17건을 라이브 19종·플랫폼 기능(프리셋·Higgsfield·Claude Docs)과 대조했다. **16건 반박**(이미 이번 PR에서 계승됐거나 의도적 폐기·플랫폼이 대체), **1건 유지(Major)** = G2 proposal-voice가 작업 트리에 들어왔으나 배선 0 → E1(jc-pptx v2.3.0)에서 SKILL·playbook·design-language·check_deck 배선 완료. 추가 발견 9건 중 처리: proposal-voice 배선(완료) · README 깨진 링크(본 커밋에서 문서 생성) · archive/README jc-comms 행(수정) · mice-meeting-minutes chaining-guide stale 키(수정) · design-language 대응형 순서 상충(E1 정리) · lint에 트리거 중복 검사 부재(**추가** — forge lint `check_trigger_collisions`, 잔여 충돌 2건 해소) · code-conductor README의 html-pt 잔재(수정) / 사용자 몫: 배포 공백(§6 A·B), mice-estimate pricing-strategy 포인터(§6 C).

## 4. Anthropic 프리셋 11종 — 라이브와의 중복 판정

| 프리셋 | 판정 | 근거 |
|---|---|---|
| doc-coauthoring | **비활성화 권고** | jc-doc-coauthor가 런타임 의존 없이 완전 포크(검증 단계·기본값 진행·MICE 유형). 'decision doc·RFC·spec'에 두 스킬이 함께 뜨고 프리셋의 'proposals'는 jc-pptx와도 겹침 |
| pptx | 유지(단 역할 명시) | jc-pptx description이 "빌드 기계로만 참조"라 적었지만 실제 deck_kit은 프리셋 자산을 쓰지 않음. 외부 .pptx 읽기·OOXML 편집용으로 남기되 jc-pptx가 우선 |
| skill-creator | 유지 | jc-skill-forge가 평가 기계로 의존(upstream-machinery.md). v2.2.0 description에 우선권 문장 추가 완료 |
| docs · docx · xlsx · pdf | 유지 | 라이브 스킬의 산출 기계(Claude Docs 기본 산출·.docx 변환·xlsx 재계산·PDF 처리) |
| web-artifacts-builder | 유지 | 라이브 HTML은 단일 파일이라 발동 조건(React+shadcn)과 겹치지 않음. 구 jc-artifact-builder의 범용 기능은 여기 있음 |
| learn · import-memory · setup-writing-style | 유지 | 무관 |

## 5. 집행 결과 (git 정본, 브랜치 `claude/lucid-franklin-37n8cu`)

| 단계 | 커밋 | 내용 |
|---|---|---|
| 보존 | `8e47432` | claude.ai에만 있던 폐합 3종(jc-asana-html·jc-remember-html·mice-weekly-performance)을 히스토리에 보존 → **복구 지점** |
| 동기 | `d487f78` | 라이브 18종 git 정본 재동기화(claude.ai 10-05 업로드본 그대로: 11종 갱신 + 7종 신규) |
| 아카이브 | `fe213c1` `8b23499` | 폐합 20종 `archive/skills/` 이동(git mv, 삭제 아님) · 레거시 3파일(`/skillupgrade` 커맨드·`build-skills.sh`·9종 시절 `_README.txt`) `archive/legacy/` · `archive/README.md`(복구 절차·흡수 매핑) |
| 가드 | `fe213c1` | `check_drift.py` CONSUMERS 하드코딩(폐합 포함) → 라이브 동적 탐색 · CI에 forge 린트(`--exclude mice-estimate`)·토큰 로더 테스트 추가 |
| 개정 | `5ccc2d3` | mice-meeting-minutes v2.2.0 — 유일하게 재편을 거치지 않았던 라이브 스킬(ERROR 47)을 리멤버 규약으로; Recharts UMD 미렌더 버그·파서 버그 2건 수정 |
| 업그레이드 | 17커밋 | §2 발견 적용 — 17종 개정(표: `docs/CHANGELOG-2026-10-09.md` §2) |
| 계승 | (위에 포함) | 스폰서 덱 → jc-pptx · 제안서 문체 정본(proposal-voice) → jc-pptx · 네이밍·슬로건 → jc-doc-coauthor · HTML 리스킨 → mice-ops-docs · 커뮤니케이션 양식 → mice-slack-ops · 드라이브 운영 표준 → mice-ops-docs |
| 문서 | `e737685` + 마감 커밋 | README(라이브 19종 카탈로그·체이닝·아카이브·작업 규칙), CHANGELOG, PROGRESS, 본 리포트 |

**마감 검증(최종 커밋 기준)**: `lint_skills.py --exclude mice-estimate` ERROR 0(WARN 3 = mice-slack-ops 채널명 `#mice-biz-team`·멘션 `@U…` 오탐) · `check_drift.py` PASS · `test_jc_tokens.py` PASS · 스크립트 self-test PASS(meeting-minutes 2종·rfp-analyzer 3종·team-board·run-of-show·pt-script·kv-guide·ops-docs·lint·build) · `build_skills.py` 18종 `.skill` ZIP 구조 OK · README 카탈로그 버전 = SKILL.md frontmatter(불일치 0) · CI drift-guard 녹색.

**추가 마감(카드 C 적용 후)**: `lint_skills.py`(제외 없음, 라이브 19종) ERROR 0 · WARN 3(동일 오탐) · `check_drift.py` PASS · `test_jc_tokens.py` PASS · mice-estimate self-test 3종(calc ALL PASS · export `--self-test` recalc→verify 0원 일치 · estimate_tokens `--self-test`) PASS · CI `--exclude mice-estimate` 제거 · `build_skills.py --include-estimate` 19종 `.skill` ZIP OK. 적대 검증 3렌즈(패치 완전성·체이닝 정합·스크립트 실행) 발견 21건 중 Critical 2(§7 헬퍼 KeyError·방식 A meta 키 불일치)·Major 6 전부 적용, 다른 스킬 측 2건(jc-pptx playbook:111 거짓 문장·chaining-protocol §4/§5 `displayType`·`totalAmountVat`)은 마감 커밋에서 정합 보정(범프 없음, 미배포).

**채널별 반영 상태(소스 반영 ≠ 배포)**

| 채널 | 상태 |
|---|---|
| ① git 정본 | **반영 완료**(본 브랜치, PR #23 드래프트) |
| ② Code 로컬 설치(`~/.claude/skills`) | 미반영 — 현재 0종 설치 상태 유지(synced만 사용) |
| ③ claude.ai 업로드 | **반영 완료(2026-10-09 14:05Z, 기획자님)** — 폐합 19종 삭제·라이브 19종 재업로드(mice-meeting-minutes 신규·mice-estimate v3.3.1)·프리셋 doc-coauthoring OFF. 확인: claude.ai 화면 "내가 만듦 19". jc-skill-forge v2.2.1(배포 팩트 갱신)도 14:1xZ 재업로드 완료 — ①=③ 전 스킬 일치 |

## 6. 남은 결정·사용자 작업 — 한 단어로 답하실 수 있게

번호로 GO/NO를 주시면 됩니다. ★ = 추천.

| 카드 | 내용 | 누가 | 추천 |
|---|---|---|---|
| **A** | ✅ **완료(2026-10-09, 기획자님)** — claude.ai Settings → Capabilities에서 **폐합 19종 삭제**: jc-artifact-builder · jc-asana-html · jc-brand-discovery · jc-brand-styling · jc-cinematic-html · jc-comms · jc-generative-art · jc-landing-page · jc-mcp-builder · jc-orchestrator · jc-prompt-builder · jc-remember-html · jc-skill-creator · jc-theme-factory · jc-visual-philosophy · jc-workspace-ops · mice-dashboard · mice-proposal · mice-weekly-performance | 기획자님 | ★ 즉시 — 층 A와 키워드 충돌 18개가 한 번에 사라짐(약 10분 후 synced 반영) |
| **B** | ✅ **완료(2026-10-09, 기획자님)** — 같은 화면에서 **동명 구스킬 삭제 → `.skill` 업로드 18종**(`dist/skills/`, 이 세션이 파일로 첨부). mice-meeting-minutes는 **신규 업로드**(현재 claude.ai에 없음) | 기획자님 | ★ A 직후 |
| **C** | ✅ **적용 완료(v3.3.1, 사용자 GO)** — 원 패치 목록: `mice-estimate` 패치(사용자 관리 스킬 — 1차 마감까지 내용 무수정). ① description: `mice-proposal·mice-rfp-analyzer 체이닝 입력` → `jc-pptx·mice-rfp-analyzer 체이닝 입력`, 말미 "실행형 지시는 실행 전 jc-prompt-builder 브리프를 거친다." 삭제, 형제 경계 추가(제안서·견적 슬라이드=jc-pptx / 입찰가 권고=mice-rfp-analyzer / 가격 포지션=jc-strategy-canvas / 경쟁가 조사=mice-market-intel / 검산=jc-redteam) ② Step 2.5 체이닝 감지에 `source: "jc-pptx"`(mice-proposal은 별칭) + rfp 견적 전용 봉투(§3-1 키) 수용 ③ `chaining-schema.md` §1 도식·§2 제목·§4·§5 수신 목록(jc-pptx ⑦예산 추가·pt-script 삭제·mice-dashboard→mice-ops-docs/aftermath), 예시 version 플레이스홀더·generatedAt·clientId ④ `pricing-strategy.md:32` → `jc-pptx/references/sponsor-deck.md §3` ⑤ `/mnt/skills`·`/mnt/user-data` 3곳 → xlsx 스킬 recalc 상대 탐색 또는 soffice, 출력 `outputs/` ⑥ `jc-design-mapping.md`·SKILL 스타일 표의 구 토큰 → §6 키, `export_estimate_remember.py` 색을 jc_tokens 런타임 로드 ⑦ 완료 후 v3.3.1 범프·lint 통과·재업로드 | Claude Code(적용됨) → 업로드는 기획자님(카드 B에 포함) | 완료 — 남은 자산 건은 C-2 |
| **C-2** | ✅ **적용 완료(v3.3.2, 2026-10-09, 사용자 위임 "알아서 처리")** — 두 시트 B11·B13·B14·B15·B24·C24·Opt2 G24 자리표시자, 59~64행 25% 단일 라인 수식(D61·E61·F61·F64·F59)·B17·B19 수식, 파일 메타 인명(creator·lastModifiedBy) 제거, 로고 앵커·병합·스타일·B15 날짜 서식 무변경 게이트 통과. **③ 재업로드는 기획자님(`.skill` 1개)**. 원 발견: `mice-estimate/assets/remember_template.xlsx` 자산 정정(검증에서 발견, 자산은 이번 미수정): ① 두 시트 B11·B13·B24·G24에 샘플 행사명·베뉴명 실문구 잔존 → `{{event_name}}`·`{{venue}}`·일반 문구(RULE-NO-COMPANY, 레포 public) ② 59~64행이 구 v2 PCO 2단(인건비·기업이윤) 구조 → 61행 단일 PCO 기획료 25%(SKILL.md 산식)로 정정. 로고·직인 앵커 보존 게이트 적용 후 v3.3.2 범프·재업로드. 그 전까지 SKILL.md가 복사 직후 수동 교체(B11·B13·B24·G24, PCO 행 치환)를 필수로 지시 | Claude Code(적용됨) → 재업로드 기획자님 | 완료 |
| **D** | ✅ **완료(2026-10-09, 기획자님)** — 프리셋 `doc-coauthoring` 비활성화(§4). `pptx`는 유지 | 기획자님 | ★ GO |
| **E** | 브랜치 — `main`(7/25 정지)을 `claude/relaxed-fermat-M5h5C`까지 fast-forward 후 본 PR base=main으로 변경(E-1) / 또는 relaxed-fermat을 기본 브랜치로 지정(E-2) | 기획자님 승인 → Code | ★ E-1 |
| **F** | 백로그(이번 미적용): ⓐ mice-ops-docs에 구 대시보드 역량(xlsx/csv 입력·Chart.js 자동 선택·레이더/매트릭스·PDF) 선택 계승 ⓑ jc-pptx 봉투 `program[]`(run-of-show 자동 흡수)·`deck_kit.cover()` "PROPOSAL" 라벨 인자화·레이더/2×2 타입 ⓒ jc-kv-guide 템플릿 토큰 런타임 로드 ⓓ jc-design-system §6에 `--line-soft`·`--charcoal` 키 ⓔ jc-session-protocol '브리프' 어휘 → '기획안 카드' ⓕ lint 허용 목록(채널명 오탐) ⓖ 폐합 jc-prompt-builder의 effort 등급표 | — | 다음 점검 사이클 |
| **H** | 행사 드라이브 표준(mice-ops-docs v1.2.0 `drive-standards.md`)이 공표 프로토콜 매뉴얼(구글독 정본)의 01~06 폴더에 **보조 폴더 3개**(`07_발주처공유`·`99_archive`·`00_공통`)를 덧붙였다 — 팀 표준으로 쓸지, 쓴다면 매뉴얼 정본에 반영할지 | 기획자님 | **기본값 채택 — 보조 폴더 유지**(2026-10-09 회신 "C드라이브 외 드라이브 없음"은 PC 디스크로 이해하신 것으로 보여 구글 드라이브 폴더 구조 건임을 재안내. 이의 없으면 유지, 매뉴얼 정본 반영은 다음 개정 때) |
| **G** | 층 B 완화 — 실무 세션은 행사 프로젝트 폴더에서 Code를 열고(synced 19종만 노출), 레포 루트는 스킬 편집 세션 전용. `~/.claude/skills` 개인 설치는 하지 않음(세 번째 사본 방지) | 기획자님 | 운영 원칙 |

## 7. 리스크 · 주의

- **(해소) claude.ai 구 상태**: 2026-10-09 14:05Z 카드 A·B·D 완료로 해소 — 폐합 19종 삭제(브리프 게이트 발동 원인 제거), 라이브 19종 재업로드(mice-meeting-minutes 신규). Code 동기화본(synced)도 14:12Z 스냅숏에서 19종 새 버전·폐합 0으로 일치 확인(29종 = 자작 19 + 프리셋 10 — **끈 프리셋(doc-coauthoring)은 synced에서 빠진다**, 다음 forge 개정 때 deploy-pipeline §1 사실 표에 추가).
- **업로드 순서**: 폐합 삭제(A) → 라이브 업로드(B). 반대로 하면 synced에 구·신 두 벌이 잠시 공존한다.
- **mice-estimate**: 카드 C 적용 완료(v3.3.1) — lint ERROR 14 → 0, CI `--exclude mice-estimate` 제거. 견적 xlsx의 색이 컨피규레이터 실측 리터럴(순오렌지·검정)에서 리멤버 웜 페이퍼 토큰(accent·ink 계열)으로 바뀐다(레이아웃·수식·금액 무변경). 템플릿 자산의 샘플 실문구·구 PCO 2단 구조·파일 메타 인명은 카드 C-2로 정정 완료(v3.3.2) — claude.ai 재업로드만 남음.
- **개정 스킬의 동작 변화**: mice-meeting-minutes는 시스템 다크 자동 감지를 없앴고(첫 렌더 라이트, mode-mapping §4.1) JSON 버튼을 하단 툴바로 옮겼다. mice-rfp-analyzer xlsx 0_종합 시트는 셀 배치가 바뀌었다(B9~B15 판정, B25~ 참고 점수). mice-team-board 갱신 TSV는 상태 열이 기본 빈칸(유지)이다.
- **원격 태그 없음**: 복구 지점은 커밋 SHA `8e47432`로 기억(로컬 태그는 이 세션에만 존재).
- **동시 편집 흔적**: 적용 에이전트 4개가 병렬로 돌았고 쓰기 범위를 폴더 단위로 분리했다. 교차 요청(체이닝 enum·정본 키·문체 규칙)은 마감 커밋에서 정합 보정했으며 lint 대조(LIVE ⊆ chaining §3)가 WARN 0이다.
