---
name: jc-session-protocol
description: 여러 세션·여러 서피스(Claude Code 데스크톱·Cowork·클라우드 세션)에 걸치는 프로젝트를 "폴더=세션 · 요청 하나=스레드 하나" 규약으로 굴리는 운영·오케스트레이션 정본. 프로젝트 폴더의 CLAUDE.md(불변 컨텍스트)·PROGRESS.md(가변 상태) 2파일, 체크인 3줄 복명·체크아웃 7항목, 체크리스트 진행과 고밀도 산출물만 기획안 1회 확인 → 빌드 → 검수 흐름, 착수 지시문(code-brief) 양식, 서브에이전트 병렬 분할·쓰기 경계·핸드오프·모델 라우팅, 이 PC(Windows 11) 환경 제약을 담는다. 다음 상황에서 반드시 이 스킬을 사용할 것 — 사용자가 '세션 체크인', '체크인 복명', '세션 체크아웃', 'PROGRESS', '이어서 작업', '이어서 진행', '세션 이어서', '새 세션에서 계속', '컨텍스트 꽉 찼어', '폴더에서 이어서', '착수 지시문', 'code brief', '기획안 확인', '진행 규약', '오케스트레이션', '서브에이전트 병렬', '모델 라우팅', '서브에이전트 킥오프', '에이전트 킥오프', '킥오프 블록', '핸드오프', '쓰기 경계', '에이전트 팀', '새 프로젝트 세팅', '프로젝트 폴더 만들어줘'를 언급할 때. 새 프로젝트의 실행 체계를 잡아달라고 할 때. 프로젝트 폴더에 CLAUDE.md·PROGRESS.md가 있으면 체크인부터 시작한다. 형제 경계 — 개별 산출물 생성은 각 전용 스킬(jc-pptx·mice-ops-docs·mice-estimate 등), 완성물 검증은 jc-redteam, Slack 채널 운영과 행사 킥오프 댓글·회의록 공유는 mice-slack-ops, 회의 킥오프 정리는 mice-meeting-minutes, 행사 참가자 체크인·현장 운영은 mice-ops-docs·mice-run-of-show, 팀 보드 조작은 mice-team-board, 행사 드라이브 폴더 세팅·권한 점검은 mice-ops-docs, 스킬 제작·배포는 jc-skill-forge.
version: "v1.2.0"
license: Complete terms in LICENSE.txt
---

# JC Session Protocol — 폴더=세션 운영 규약

세션(머신·서피스)은 무상태 클라이언트다. 상태는 **프로젝트 폴더의 2파일**에만 산다. 대화는 휘발, 파일이 정본. 2026-09 플레이북·팀 보드 프로젝트에서 실증한 방식을 정본화했다.

## 1. 2파일 표준

| 파일 | 성격 | 개정 주체 | 내용 |
|------|------|-----------|------|
| `CLAUDE.md` | 불변·저빈도 | 사용자(기획자님)만 | 프로젝트 정의 · 확정 결정(D1~Dn) · 작업 규칙 · 폴더 구조 · 권장 모델 · 쓰기 경계 · 금지 |
| `PROGRESS.md` | 가변 | 에이전트(체크아웃 시) | 현재 상태 · 완료 · 미결·질문 · 다음 스텝 · 결정 로그 · 턴/세션 로그 · 세션 잠금 · 환경 메모 |

템플릿: `assets/templates/CLAUDE.md.template` · `PROGRESS.md.template`. 세부 규칙: `references/checkin-checkout.md`.

## 2. 리추얼

**체크인(세션 시작)** — ① `CLAUDE.md` + `PROGRESS.md` 로드 → ② 3줄 복명(현재 상태 / 이번 세션 목표 / 열린 질문) → ③ 바로 개시(승인 대기 없음). `PROGRESS.md` 세션 잠금이 다른 머신으로 기록돼 있을 때만 개시 전 확인. 사용자가 "OO 폴더에서 이어서. PROGRESS의 '체크아웃 — 날짜' 절부터"라고 하면 그 절부터 읽는다.

**체크아웃(세션 종료·컨텍스트 한도)** — `PROGRESS.md` 7항목 갱신(상태 요약 · 완료 · 미결 · 다음 스텝 · 결정 로그 · 세션 로그 · 잠금 해제) + **다음 세션 시작 순서** 1~N번을 적고, 채팅에 체크아웃 보고 블록을 그대로 출력한다. git 저장소면 커밋까지(push는 사용자).

한 폴더 = 동시 1세션. 체크인 없는 작업 금지. 컨텍스트가 차면 새 세션을 열고 체크아웃 절부터 인계한다.

## 3. 진행 규약 — 요청 하나 = 스레드 하나 · 체크리스트 · 기획안 1회 확인

- **요청 하나 = 스레드 하나.** 한 스레드(세션)에 다른 요청을 섞지 않는다. 새 요청은 새 스레드로, 맥락은 PROGRESS.md·파일로 넘긴다.
- **체크리스트로 진행.** 첫 응답에 단계 목록(✓ 완료 · ✱ 진행 · ○ 대기)을 내고 단계가 끝날 때마다 갱신한다. 단계마다 묻지 않는다.
- **되돌릴 수 있는 작업**(초안·파일·분석·코드 수정)은 합리적 기본값으로 바로 진행하고 고른 기본값을 한 줄로 밝힌다.
- **고밀도 산출물**(덱·장문 문서·대시보드·여러 파일 빌드)만 기획안(구성·핵심 메시지) **1회 확인 → 빌드 → 검수(jc-redteam)**. 확인 양식은 `references/brief-card.md`. "바로 해줘"면 생략.
- **되돌릴 수 없는 작업**(외부 발송·게시·삭제·배포·결제)만 그 직전에 승인.
- 폐지(2026-10-05): 3턴 분할, [A]/[B]/[C] 범위 게이트, "실행 전 브리프" 게이트.

Cowork 기획 → Code 빌드 분업은 서피스가 바뀔 때만 쓴다. 착수 지시문 양식(세션 설정 · 0 체크인 · 1 목표 · 2 산출물과 경로 · 3 계약 동결 · 4 실행 구조 · 5~7 규격 · 8 품질 게이트 · 9 체크아웃 · 10 금지)은 `assets/templates/code-brief.md.template`, 규약 상세와 판정 형식은 `references/turn-protocol.md`.

**패치 후 재검증** — 검증 이후 코드를 고쳤으면 영향 경로는 미검증으로 되돌리고 게이트를 다시 돌린다. 재검증 없는 패치는 발행하지 않는다.

## 4. 서브에이전트 · 병렬 · 핸드오프 (요지)

- 에이전트 사이를 흐르는 것은 대화가 아니라 **파일**이다. 호출 시 읽을 파일 경로 열거("앞 단계 참고" 금지), 산출 경로·형식 사전 계약, 완료 보고 = 산출 경로 + 핵심 결정 3줄 + 미해결 이슈.
- 병렬은 ⓐ 같은 파일을 쓰지 않고 ⓑ 서로의 출력을 입력으로 삼지 않는 노드에만. 확신 없으면 순차. 공통 기반(계약·스키마·토큰) 먼저, 그 위에 독립 구현 병렬.
- 쓰기 경계는 킥오프 블록에서 겹침 0으로 선언, 변경은 킥오프 블록 개정으로만. 메인이 계약 기준으로 병합·검수.
- 실패 시 조용한 스펙 축소 금지 — 중단 보고(사유 + 시도 + 대안 1개).
- 백그라운드 에이전트는 PC 절전·앱 종료 시 스톨로 죽는다 → 파일 단위로 범위를 잘라 새로 띄우는 편이 안전(2026-09-11 실증).
- 킥오프 블록·Task 표준 지시문·아키타입 8종·라운드 동기화는 `references/subagent-handoff.md`.

## 5. 모델 라우팅 (서브에이전트 · 세션)

| 용도 | 모델 | ID |
|------|------|----|
| 기본(메인·판단·구현) | Opus 5.5 | `claude-opus-5-5` |
| 정리·가공(문서·데이터 정리, 요약) | Sonnet 5.5 | `claude-sonnet-5-5` |
| 단순 추출·변환(명령 실행·조회·포맷 변환) | Haiku 4.5 | `claude-haiku-4-5-20251001` |
| 최고난도·장시간(설계 분기·근본원인·긴 자율 작업) | Fable 5.1 | `claude-fable-5-1` |

킥오프 블록의 '위임 모델' 줄과 `assets/code-conductor/`(지휘-실행 분리 훅 프리셋, 설치본 기준 `claude-opus-5-5`)가 이 표를 따른다. 모델 ID는 시점 팩트 — 바뀌면 검증일과 함께 이 표부터 고친다(RULE-VERSION-FACTS). 이 표가 라이브러리 전체의 모델 정본이다(다른 스킬은 재기재하지 않고 여기를 가리킨다).

**복제 위치 체크리스트** — 라인업·ID를 바꾸면 같은 커밋에서 아래를 함께 고친다(agents·env.sh에 구 ID가 남으면 서브에이전트 호출이 404).

- [ ] `references/subagent-handoff.md` §4 킥오프 블록 '위임 모델' 줄 · §7 code-conductor 요지
- [ ] `assets/code-conductor/` — README.md · INSTALL.md · agents/deep-reasoner.md · agents/runner.md(`model:` 줄) · env.sh(리매핑 ID) · fable.md(라우팅 계층)
- [ ] 템플릿 2종 — `assets/templates/CLAUDE.md.template` · `assets/templates/code-brief.md.template`(권장 모델 줄)
- [ ] `jc-skill-forge/scripts/lint_skills.py`의 `CURRENT_MODELS` 상수(구 모델 경고 메시지) — 구 ID 정규식도 함께 검토

## 6. 환경 메모 (이 PC)

세션 첫 명령 전에 `references/windows-env.md`를 본다. 요지: `python`(3.14)·`node`(24)·`git`은 PATH에 있음(`gh`·`zip`·`jq`·`soffice` 없음), Bash 히어독 10KB·백슬래시 취약(큰 파일은 Write 도구), stdin 읽는 명령은 영원히 대기, Git Bash가 `/슬래시명령`을 경로로 변환, 브라우저 패널 file:// 거부·숨김 시 캡처 공백, `claude.exe`는 PATH 미등록. 클라우드 세션(GitHub)은 npm·Chromium이 있어 게이트 전부 실행 가능하나 시트·Apps Script 쓰기 불가.

## 7. 기획안 카드 (옵트인)

기본은 즉시 실행이다. 고밀도 산출물의 기획안 1회 확인, 또는 사용자가 "브리프", "정리하고 시작", "뭘 만들지부터"라고 할 때만 `references/brief-card.md`의 카드(목표·산출물·구성·핵심 메시지·성공 기준·제약·가정)를 1회 제시하고 승인 후 끝까지 실행한다.

## 8. 파일 구조

```
jc-session-protocol/
├── SKILL.md
├── references/
│   ├── checkin-checkout.md     # 2파일 규칙 · 리추얼 · 체크아웃 보고 블록 · 세션 인계 · 잠금
│   ├── turn-protocol.md        # 진행 규약(스레드·체크리스트·기획안 1회) · 착수 지시문 · 결정 로그 · 게이트 · 판정 형식
│   ├── subagent-handoff.md     # 킥오프 블록(Code·Cowork) · Task 지시문 · 핸드오프 7칙 · 아키타입 8종
│   ├── windows-env.md          # 이 PC 환경 제약 · 도구 경로 · 우회법 (검증일 병기)
│   └── brief-card.md           # 기획안 1회 확인 카드 (구 프롬프트 빌더 요지 흡수)
└── assets/
    ├── templates/CLAUDE.md.template · PROGRESS.md.template · code-brief.md.template
    └── code-conductor/         # (선택) Code 지휘-실행 분리 훅 프리셋(구 jc-orchestrator에서 흡수) — README·INSTALL 참조
```

## 9. 생태계 연결

- 산출물: `jc-pptx` · `mice-ops-docs` · `mice-estimate` · `mice-meeting-minutes` · `mice-team-board`(보드 프로젝트 자체가 이 규약으로 운영됨). 문서 기본 산출은 Claude Docs, 이미지·영상 생성은 Higgsfield
- 스킬 제작·배포: `jc-skill-forge`
- 검증: `jc-redteam` — 검수 턴의 기본 도구. Deep Audit 판정 형식은 `turn-protocol.md §5`
- 데이터: `jc-design-system/references/chaining-protocol.md`(ChainPayload/v1)
- 흡수 이력: `jc-orchestrator` v1.1.2(오케스트레이션 — 킥오프·핸드오프·아키타입·code-conductor) + `jc-workspace-ops` v1.1.0 §5(세션 연속성) + `jc-prompt-builder` v1.0.1(카드, 게이트는 폐지) — 2026-09-21 흡수. 폐합 스킬이 호출되던 자리는 모두 이 스킬로 온다

## 변경 이력

- v1.2.0 (2026-10-09): 트리거 한정 — '체크인'·'체크아웃'·'킥오프' → '세션 체크인'·'체크인 복명'·'세션 체크아웃'·'서브에이전트/에이전트 킥오프'·'킥오프 블록', 경계에 행사 킥오프 댓글(mice-slack-ops)·회의 킥오프 정리(mice-meeting-minutes)·참가자 체크인(mice-ops-docs·mice-run-of-show) 추가.
  §5를 모델 정본으로 선언 + 복제 위치 체크리스트, description의 모델 나열 삭제. 판정 형식 참조 §4→§5 정정, turn-protocol §5 판정 라벨을 jc-redteam 3종으로 통일.
- v1.1.0 (2026-10-05): 3턴 분할·[A]/[B]/[C] 범위 게이트 삭제 → "요청 하나=스레드 하나 · 체크리스트 진행 · 고밀도만 기획안 1회 확인 → 빌드 → 검수", 체크인 승인 대기 제거, 템플릿·brief-card·turn-protocol 개정.
  모델 라우팅 표 신설(Opus 5.5 / Sonnet 5.5 / Haiku 4.5 / Fable 5.1), code-conductor를 설치본(`claude-opus-5-5`)에 맞춤, 구 오케스트레이터 흡수 표기 정리.

### v1.0.0 (2026-09-21)
신규. 플레이북(2026-09-07)·팀 보드(2026-09-10~16) 프로젝트의 CLAUDE.md/PROGRESS.md/code-brief 실전 규약을 정본화. jc-orchestrator·jc-workspace-ops 세션 층·jc-prompt-builder 카드 흡수. 멀티 에이전트 "팩토리 5단계 승인" 절차는 폐지(발동 0회) — 킥오프 블록 1장으로 대체.
