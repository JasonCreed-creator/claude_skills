# House Conventions v2.2 — jc·mice 스킬 불변식

모든 라이브 스킬이 지키는 규칙. `scripts/lint_skills.py`가 기계 검사 가능한 항목을 검사한다.

---

## 1. 디렉터리 · 프론트매터

```
<name>/
├─ SKILL.md          # 진입점. <300줄 권장, 500 상한. 워크플로우·판단·경계
├─ references/       # 상세 문서(.md). 300줄 넘으면 목차
├─ scripts/          # 결정적·반복 작업(.py). stdlib 우선. 자가 테스트 필수
├─ assets/           # 템플릿·이미지 등 산출에 직접 쓰는 파일
└─ LICENSE.txt       # 있으면 frontmatter license 라인과 짝
```

```yaml
---
name: mice-<도메인>            # 디렉터리명과 정확히 일치. 소문자·하이픈
description: <한국어·푸시형>  # 무엇을 + 언제(키워드·맥락) + 형제 경계. 1,024자 이하
version: "v1.0.0"           # SemVer. 수정 시 범프
license: Complete terms in LICENSE.txt
---
```

- claude.ai 업로드 허용 필드: `name` `description` `license` `compatibility` `metadata` `allowed-tools`(+ 실측상 `version`·`dependencies` 통과). Code 전용 필드(`user-invocable`·`disable-model-invocation`·`context`·`agent`)는 업로드 실패 → 쓰지 않는다.
- description 규칙: "다음 상황에서 반드시 이 스킬을 사용할 것 — …" 패턴, 사용자가 실제 칠 법한 한국어 표현을 폭넓게, 인접 스킬과의 경계를 명시. **금지 문구**: 폐지된 게이트 문구("실행 전 … 브리프", [A]/[B]/[C] 범위, "N턴 분할"), 폐합 스킬 이름(`lint_skills.py` ARCHIVED 집합 = `archive/skills/`).
- 본문에 "when to use"를 넣지 않는다 — 전부 description에.

## 2. SoT 앵커 (값 미러 금지)

- 색·서체·간격·컴포넌트 값은 `jc-design-system` v2(리멤버 웜 페이퍼)에서 런타임 로드. 코드: `jc_tokens.find_sot()` → `load_tokens` → `color`/`dark`.
- 탐색 순서: 형제 경로(`parents[2]/jc-design-system`) → `~/.claude/skills/jc-design-system` → `~/.claude/skills/synced/*/jc-design-system`. `/mnt/skills`·`/sessions/*` 경로 금지.
- 부득이한 폴백 상수는 출처(`signature-tokens.md §6`) 주석 + 로드 실패 시에만 사용. 레포 루트 `check_drift.py`의 FORBIDDEN 값(구 시그니처 #0A2540·#2962FF 등) 금지.

## 3. 홈베이스 = 리멤버

- 기본 룩은 리멤버 웜 페이퍼 하나. 구 jc 시그니처는 `legacy-jc` 오버레이로 명시 요청 시만. 임의 팔레트·대체 브랜드·"자유 모드"는 만들지 않는다.
- 서체 Pretendard 고정.

## 4. 명의 · 식별정보 (RULE-NO-COMPANY v2)

- 발행 명의는 리멤버 MICE비즈팀 기본. 발주처·고객사·담당자·연락처는 주입 슬롯(`{{client_company}}` 등).
- 구 소속사(M&C) 명칭·프로젝트명·누적 건수는 리멤버 명의 문서에 넣지 않는다. 개인 휴대전화·사설 메일 금지.
- 내부 운영 레퍼런스(채널 ID·팀원 역할)는 `mice-slack-ops/references/channels.md` 한 곳에만.

## 5. 공통 룰 링크 (값 재정의 금지)

인라인 리마인더 + `jc-design-system/references/shared-rules.md#<RULE-ID>`: `RULE-WCAG` · `RULE-PRINT-LIGHT` · `RULE-PPTX-HEX` · `RULE-NO-COMPANY` · `RULE-VISUAL-ROUTING` · `RULE-VERSION-FACTS`.

## 6. 생태계 연결 (재발명 금지)

- 검증 → `jc-redteam`. 세션·턴·서브에이전트 → `jc-session-protocol`. 데이터 봉투 → `ChainPayload/v1`. 디자인 → `jc-design-system`. Slack → `mice-slack-ops`.
- 새 스킬이 다른 스킬 기능을 반복하면 MERGE 검토가 먼저.

## 6.1 진행 방식 — 정본 포인터

- `jc-session-protocol/SKILL.md` §3 준수(정본 — 여기서는 재기재하지 않는다).
- 폐지 게이트 문구는 description·본문 모두 금지(§1, 린트 검사).

## 6.2 표기

- 호칭: 사용자 "기획자님", 조직 직함 "팀장"("리더"·"팀리드" 금지).
- 모델: 정본 `jc-session-protocol/SKILL.md` §5(계열명·ID), 재기재 금지. 구 모델명·ID는 린트 ERROR.
- 이미지·영상 생성은 Higgsfield(연결돼 있을 때). 문서 기본 산출은 Claude Docs.

## 7. 스크립트

- `python`(Windows 3.14)에서 실행 검증. 경로는 `pathlib`, `os.path` — 문자열 `/` split 금지. 한글 출력은 `PYTHONIOENCODING=utf-8` 전제.
- 자가 테스트: `--self-test` 플래그 또는 `test_*.py`. 외부 패키지(python-pptx·openpyxl·Pillow) 의존은 frontmatter `dependencies`에 적고 미설치 시 친절한 안내 후 비-0 종료.
- 실증 스크립트(세션에서 만든 빌더)는 `scripts/examples/`로 회수해 레시피로 남긴다.

## 8. 저작 검증 루프 (RED → GREEN → REFACTOR)

1. RED — 스킬이 막아야 할 구체적 실패를 먼저 적고, 스킬 없이 같은 요청을 던지면 실제로 재현되는지 본다. 재현되지 않는 규칙은 넣지 않는다.
2. GREEN — 그 실패를 막는 최소 분량만 쓴다.
3. REFACTOR — 압박 상황의 우회("이번만", "그냥 빨리")를 반례 표(패턴 → 올바른 대응)로 명시.

## 9. 자가점검 (마감)

- [ ] name = 디렉터리, version, license
- [ ] description 한국어·푸시형·형제 경계·≤1,024자·금지 문구 0
- [ ] 값 미러 0, `/mnt` 0, 폐합 스킬 참조 0
- [ ] 리멤버 명의·주입 슬롯, M&C 0
- [ ] 생태계 연결 명시(검증·세션·봉투·디자인)
- [ ] SKILL.md 500줄 미만, 반복 작업은 scripts/, 자가 테스트 통과
- [ ] 진행 규약: jc-session-protocol §3 준수 · 호칭(사용자 '기획자님', 직함 '팀장') · 모델명은 jc-session-protocol §5 기준
- [ ] `python scripts/lint_skills.py <스킬폴더>` ERROR 0 · 변경 이력 1항 · README 카탈로그 갱신
- [ ] 배포 보고는 ①소스 반영 ②Code 설치 ③claude.ai 업로드를 따로(③은 사용자 몫, `.skill` ZIP만)
