---
name: mice-team-board
description: 리멤버 MICE비즈팀 팀 프로젝트 보드(구글시트 + Apps Script 웹 대시보드)를 다루는 스킬. 프로젝트·배정·마일스톤·정산 탭의 행 등록과 갱신, 상태 7단계(견적·계약·준비·진행·완료·정산완료·드롭) 전이, 표준 마일스톤 생성, 인력 M/D 배정과 가동률 확인, 계약완료 메시지 파싱 결과를 보드 행으로 입력, Apps Script 코드·styles.css 수정과 배포, Chrome 확장으로 시트 조작하는 레시피를 담는다. 다음 상황에서 반드시 이 스킬을 사용할 것 — 사용자가 '팀 보드', '프로젝트 보드', '보드에 등록', '보드 업데이트', '시트에 넣어줘', '프로젝트 행', '프로젝트ID', '상태 바꿔줘', '드롭 처리', '마일스톤', '표준 마일스톤', 'M/D 배정', 'M/D', '가동률', '정산 탭', 'Apps Script', '보드 대시보드', 'styles.css', '보드 배포', 'clasp'를 언급할 때. mice-slack-ops의 contract ChainPayload를 받아 행을 넣을 때. 형제 경계 — 계약완료 메시지 파싱과 신규·갱신 판단은 mice-slack-ops(본 스킬은 그 값을 시트에 반영), Slack 스레드 첫 댓글(상태 보드)·PM 배정 댓글·[S5 시작] 단계 전환은 mice-slack-ops, 견적 산출은 mice-estimate, 운영계획서·KPI 대시보드는 mice-ops-docs, 디자인 토큰 값은 jc-design-system, 세션 규약은 jc-session-protocol. 시트 쓰기·코드 배포는 사용자 승인 후에만 한다.
version: "v1.1.0"
license: Complete terms in LICENSE.txt
---

# MICE Team Board — 팀 프로젝트 보드 운영

MICE비즈팀의 프로젝트·인력·일정·정산을 한 장에 모은 구글시트와, 그 시트를 읽어 그리는 Apps Script 웹 대시보드. 2026-09-10~16 보드 프로젝트에서 만들고 계약완료 등록(9/13·9/16)으로 검증한 운영 방식을 담는다. 보드 프로젝트 폴더 자체가 `jc-session-protocol` 규약(CLAUDE.md·PROGRESS.md)으로 운영된다.

## 0. 가드레일

- **시트 쓰기·코드 교체·배포는 승인 후.** 먼저 입력할 행 값 표를 보여주고 사용자가 "넣어"라고 한 뒤에 실행한다. 팀 공용 데이터라 되돌리기 어렵다.
- **삭제는 하지 않는다.** 행 삭제·셀 비우기는 사용자 몫(자동화도 막혀 있음). 끝난 건은 상태 `드롭`·`정산완료`로만 바꾼다.
- **신규 vs 갱신 판단이 먼저.** 같은 발주처 + 행사일(또는 행사명) 행이 있으면 갱신. 마일스톤·배정·정산 행을 중복 생성하지 않는다(`mice-slack-ops/references/contract-message.md §4`).
- 클라우드 세션은 시트를 읽기만 가능하다. 쓰기는 PC의 Claude Code + Chrome 확장 또는 사용자 직접 입력(`jc-session-protocol/references/windows-env.md §5`).
- 입력 기록은 보드 프로젝트 폴더 `data/프로젝트_등록_YYYY-MM-DD.tsv` / `프로젝트_갱신_YYYY-MM-DD.tsv`로 남긴다.
- 예시·기록에 넣는 고객사명은 실제 보드 값 그대로, 스킬 문서 안 예시는 가명.

## 1. 작업 유형별 진입

| 요청 | 절차 | 참조 |
|------|------|------|
| 계약완료 → 보드 등록 | `mice-slack-ops`가 만든 `contract` 페이로드 수신 → `scripts/board_rows.py`로 행 값 표(갱신 시 상태는 `status_hint`가 `계약`·`준비`일 때만) → 승인 → 입력(Chrome 확장 또는 사용자) → 메뉴 "표준 마일스톤 생성"(신규만) → TSV 기록 | `sheet-schema.md` · `operations.md §1` |
| 상태 변경·드롭 | 대상 행 확인 → 전이 규칙 점검 → 승인 → E열 변경 + 비고에 사유·날짜 | `operations.md §2` |
| 마일스톤·배정 | 표준 마일스톤 세트 / 역할별 M/D 기본값 → 행 값 표 → 승인 | `operations.md §3·§4` |
| 현황 질문(이번 달 행사, 가동률, 미정산) | 시트 읽기 → 표 요약. 쓰기 없음 | `operations.md §5` |
| 대시보드 디자인·코드 수정 | 변경 범위 확인 → 로컬 수정 → 미리보기 → 승인 → 코드 교체·배포 | `apps-script.md` |
| Chrome 확장으로 시트 조작 | 셀 입력·메뉴 실행·코드 교체 레시피 | `chrome-ext-recipes.md` |

## 2. 상태 7단계

`견적 → 계약 → 준비 → 진행 → 완료 → 정산완료`, 어느 단계에서든 `드롭`.

- 견적 단계에서 선등록된 행은 계약완료 시 같은 행을 `계약`으로 갱신. 이미 `준비` 이후인 행은 상태 유지(`status_hint: keep` — 역행 금지).
- `준비`는 MICE PM 배정·킥오프 착수 시. `진행`은 행사 주간. `완료`는 행사 종료 다음 날. `정산완료`는 정산 탭 마감 후.
- 칩 색은 `jc-design-system/references/component-patterns.md §2`(6종 + 드롭 = 중립 취소선).

## 3. 반례 표

| 압박 패턴 | 올바른 대응 |
|-----------|-------------|
| "계약완료 떴으니 바로 새 행으로 넣어" | 기존 견적·계약 행 대조가 먼저. 있으면 갱신 |
| "끝난 건 행 지워줘" | 삭제 금지. `드롭` 또는 `정산완료` + 비고 |
| "값은 알아서 넣고 결과만 알려줘" | 행 값 표를 먼저 보여주고 승인 후 입력 |
| "styles.css 색 하나만 바꿔" | 값은 jc-design-system 토큰과 같아야 한다. 토큰이 바뀐 게 아니면 바꾸지 않고, 바뀌었으면 양쪽 동기화 |
| "클라우드에서 그냥 시트에 써" | 클라우드는 읽기만. PC 세션 또는 사용자 입력으로 넘긴다 |

## 4. 파일 구조

```
mice-team-board/
├── SKILL.md
├── LICENSE.txt
├── references/
│   ├── sheet-schema.md        # 탭 구성 · 프로젝트 탭 A~P 열(정본) · 배정/마일스톤/정산 탭 · 커스텀 메뉴
│   ├── operations.md          # 등록·갱신 · 상태 전이 · 표준 마일스톤 · 배정 M/D · 현황 질의
│   ├── apps-script.md         # 웹 대시보드 구조 · styles.css 토큰 동기화 · 배포 경로
│   └── chrome-ext-recipes.md  # Chrome 확장 셀 입력 · 메뉴 실행 · 코드 교체 · 막히는 동작
└── scripts/
    └── board_rows.py          # contract ChainPayload → 프로젝트 탭 행(TSV) (--self-test)
```

## 5. 생태계 연결

- 상류: `mice-slack-ops`(계약완료 파싱 · `contract` 페이로드 · 트래커 알림 채널) · `mice-estimate`(견적 단계 선등록 금액).
- 하류: 읽기 질의 결과(현황 표)를 `mice-ops-docs`·주간 퍼포먼스 리포트(`mice-slack-ops` §2-1)가 참고한다(봉투 없음 — 본 스킬은 수신 전용).
- 디자인: `jc-design-system` — 보드 `styles.css`가 리멤버 웜 페이퍼의 대시보드 구현체(`usage-guide.md §2`).
- 세션·환경: `jc-session-protocol`(폴더=세션, Windows 실행 환경). 검증: 대규모 구조 변경 전 `jc-redteam`.

## 변경 이력

### v1.1.0 (2026-10-09)
경계 정리 — 트리거 '배정'→'M/D 배정', 상태 보드·PM 배정 댓글·단계 전환은 mice-slack-ops로 명시. 시트 열(A~P) 정의 정본을 `sheet-schema.md`로 이관(트래커 용어 1줄), 하류는 현황 표 참고(봉투 없음)로 정정.
`board_rows.py`: 갱신 시 상태 열은 빈칸(유지) 기본·`status_hint`가 `계약`/`준비`일 때만 채움, 비고는 payload `notes` 그대로(중복 조립 제거), 자가 테스트에 갱신·힌트 케이스 추가.

### v1.0.0 (2026-10-05)
신규. 기존 스킬 여러 곳(mice-slack-ops·jc-design-system·jc-session-protocol)이 참조하던 미실재 스킬을 실체화. 2026-09 보드 프로젝트의 시트 구조·상태 체계·계약완료 등록 절차·Chrome 확장 레시피를 정본화. 보드 원본에서 확인하지 못한 열·메뉴는 문서에 "실측 필요"로 표시.
