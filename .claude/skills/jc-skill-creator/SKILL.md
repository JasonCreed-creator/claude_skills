---
name: jc-skill-creator
description: jc 스킬 라이브러리에서 스킬을 신규 제작·프리셋 개조·기존 개선할 때 따르는 하우스 표준. 일반 스킬 제작 기계(테스트 평가·벤치마크·eval-viewer·description 최적화)는 상위 skill-creator에 위임하고, 그 위에 jc 하우스 규칙(jc-* 명명·한국어 푸시형 description·jc-design-system SoT 앵커·shared-rules·RULE-NO-COMPANY·버전/커밋/드래프트 PR/로드맵 갱신·생태계 연결·결정적 품질 lint)을 얹어 생성물이 처음부터 jc 네이티브가 되게 한다. 다음 상황에서 반드시 이 스킬을 사용할 것 사용자가 '스킬 만들어줘', '새 스킬', '스킬 제작', '스킬 개조', '프리셋 최적화', '기본 스킬 업그레이드', '스킬 개선', 'skill 만들기', '이 스킬 나에 맞게'를 언급할 때. 기본 제공(프리셋) 스킬을 jc 생태계로 바꿔달라고 할 때. 단, 디자인 토큰 자체의 정의·수정은 jc-design-system, 완성 산출물의 적대적 검증은 jc-redteam 영역이다. 이 스킬은 '스킬을 만드는 메타 작업' 전용.
version: "v1.1.0"
license: Complete terms in LICENSE.txt
---

# JC Skill Creator

원본 skill-creator를 **jc 레포 하우스 표준에 맞춰 개조**한 메타 스킬이다. 핵심 설계 결정:

> **기계는 위임, 규칙만 얹는다.** 스킬 제작의 *범용 기계*(테스트 prompt 실행·벤치마크 집계·eval-viewer·description 최적화 루프)는 잘 작동하는 상위 skill-creator(`/mnt/skills/examples/skill-creator`)에 그대로 위임한다. 본 스킬은 그 위에 **jc 하우스 규칙**(이 레포에서 만드는 모든 스킬이 처음부터 지켜야 할 불변식)만 얹는다. 500줄짜리 평가 절차를 복제하지 않는다.

## 3가지 모드

작업 시작 시 어느 모드인지 먼저 판별한다.

| 모드 | 트리거 | 절차 |
|------|--------|------|
| **A. 프리셋 개조** | 기본 제공 스킬을 jc로 | [`docs/preset-adaptation-playbook.md`](../../../docs/preset-adaptation-playbook.md) 정본을 따른다 + [`docs/preset-optimization-roadmap.md`](../../../docs/preset-optimization-roadmap.md) 상태 갱신 |
| **B. 신규 jc 스킬** | 없던 기능을 새로 | 아래 하우스 불변식으로 골격 작성 → (필요 시) 상위 기계로 평가 |
| **C. 기존 개선** | jc 스킬 수정·버전업 | 변경 + `version` 범프 + 커밋/PR |

세 모드 모두 아래 **하우스 불변식**과 **마감 절차**를 공유한다.

## 작업 깊이 — quick / std / deep

모드와 별개로 작업 분량에 맞춰 깊이를 고른다(mice-* 스킬의 quick/std/deep과 동일 철학).

| 깊이 | 언제 | 산출 범위 |
|------|------|-----------|
| **quick** | 한 줄 수정·오타·version 범프·description 미세조정 | 변경 + lint GO + 커밋. references 미접촉 |
| **std** | 신규 단일 스킬·프리셋 1종 개조 | 골격 + references 1~3종 + lint GO + jc-redteam 권고 |
| **deep** | 스크립트·체이닝·평가까지 풀세트 | std + scripts/self-test + ChainPayload 배선 + (객관식 산출이면) 상위 기계 벤치마크 |

quick이라도 **lint는 항상** 돌린다(규약 회귀 방지). 상위 평가 기계는 **deep**에서만 호출한다(`references/upstream-machinery.md`).

## 하우스 불변식 (모든 jc 스킬이 지킨다)

상세·근거는 [`references/house-conventions.md`](references/house-conventions.md). 요지:

1. **명명·구조** — 디렉터리=frontmatter `name`=`jc-<도메인>`. SKILL.md(<500줄) + references/ + scripts/ + assets/.
2. **description** — 한국어 우선·푸시형. 무엇을 + 언제 트리거(키워드·맥락) + 형제 스킬 경계(언제 쓰지 말지)를 모두 description에. Claude의 undertrigger 경향을 이긴다.
3. **SoT 앵커** — 디자인 토큰 값 하드코딩 금지. `jc-design-system`에서 런타임 로드(`jc_tokens.py`). 라이트/다크는 `mode-mapping.md`.
4. **홈베이스 원칙** — jc 시그니처가 기본값, 임의 팔레트·대체 브랜드·아트 자유는 명시적 opt-in.
5. **공통 룰 참조** — 값 재정의 말고 `shared-rules.md#RULE-WCAG/PRINT-LIGHT/NO-COMPANY/PPTX-HEX` 링크.
6. **회사·개인정보 금지** — 외부 주입 변수만(`{{client_company}}` 등).
7. **생태계 연결** — 검증=`jc-redteam`, 데이터=`ChainPayload/v1`, 디자인=`jc-design-system`. 재발명 금지.
8. **진행형 디스클로저 + 스크립트 번들** — 반복 작업은 `scripts/`로 한 번 만든다.

## 결정적 품질 루브릭 (lint — 하우스 게이트)

규약 준수를 사람이 매번 눈으로 보지 않는다. `scripts/lint_skill.py`가 8기준 100점으로 **결정적**(동일 입력→동일 점수) 채점한다. 정본 [`references/scoring-rubric.md`](references/scoring-rubric.md) · 안티패턴 [`references/anti-patterns.md`](references/anti-patterns.md) · 완주 예시 [`references/worked-example.md`](references/worked-example.md).

```
python3 .claude/skills/jc-skill-creator/scripts/lint_skill.py <skill-dir>
# C1~C8 → GO(≥90) / CONDITIONAL(70–89) / NO-GO(<70). NO-GO는 종료코드 1(CI 게이트).
python3 .claude/skills/jc-skill-creator/scripts/lint_skill.py --self-test   # good=100 GO / bad=NO-GO
```

- **잰다(규약)**: 명명·frontmatter·SemVer·description 트리거/경계·분량·LICENSE·RULE-NO-COMPANY·구조.
- **안 잰다(품질)**: 논리·설득력·디자인 완성도 → `jc-redteam`(정성) 몫. **lint=규약 게이트, redteam=품질 게이트, 둘 다 통과**가 마감 조건(보완재, 대체 아님).

## 평가가 필요할 때 (상위 기계 위임)

스킬의 객관적 품질 검증이 필요하면 상위 skill-creator의 기계를 쓴다. 무엇을 언제 쓰는지의 포인터는 [`references/upstream-machinery.md`](references/upstream-machinery.md). 요약:

- **객관적 산출**(파일 변환·데이터 추출·고정 워크플로우): 상위 `eval-viewer/generate_review.py` + `scripts/aggregate_benchmark.py`로 테스트.
- **주관적 산출**(디자인·글쓰기·아트): 이 레포 관행대로 **`jc-redteam` 정성 검증**으로 대체 가능(억지 assertion 금지).
- **description 트리거 최적화**: 상위 `scripts/improve_description.py`(claude CLI 필요). 한국어·푸시형 + 형제 경계 eval로.
- **패키징**: 상위 `scripts/package_skill.py`로 `.skill` 산출.

## 마감 절차 (jc 하우스 워크플로우)

1. **결정적 lint** `python3 jc-skill-creator/scripts/lint_skill.py <skill-dir>` → **GO(≥90)** 확인(NO-GO면 `anti-patterns.md`로 교정 후 재채점). + 플레이북 §8 체크리스트 + (디자인/소비 스킬이면) `python3 scripts/check_drift.py` 정합.
2. `version` 설정/범프(SemVer).
3. 커밋 `<스킬명>: <요약>`, 작업 브랜치 → **드래프트 PR**.
4. 프리셋 개조면 `docs/preset-optimization-roadmap.md` 상태 갱신, 신규/주요 변경이면 `README.md` 카탈로그 갱신.
5. 최종 산출물 품질은 `jc-redteam`로 점검 가능.

## 파일 구조

```
jc-skill-creator/
├── SKILL.md                          # 본 파일 — 모드 판별 + 하우스 불변식 진입점
├── references/
│   ├── house-conventions.md          # 불변식 상세 + 디렉터리/frontmatter 템플릿
│   ├── scoring-rubric.md             # 결정적 8기준 루브릭 정본(lint와 1:1)
│   ├── anti-patterns.md              # 제작 안티패턴 라이브러리(루브릭 연결)
│   ├── worked-example.md             # 신규 스킬 end-to-end 워크드 예시
│   └── upstream-machinery.md         # 상위 skill-creator 기계를 언제 어떤 스크립트로 쓰는지
└── scripts/
    └── lint_skill.py                 # 결정적 품질 채점기(--self-test 내장)
```
