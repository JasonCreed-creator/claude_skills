# Worked Example — 신규 jc 스킬을 end-to-end로 만들기

가상의 신규 스킬 **`jc-checklist`**(행사 운영 체크리스트 생성기)를 0에서 만들어 마감까지 가는 전 과정. 모드 판별 → 골격 → references → lint 채점 → redteam → PR 순서를 실제 산출물과 함께 보인다.

> 목적: "하우스 불변식"이 추상적으로 안 읽히도록, 한 번의 완주를 따라가며 각 단계에서 *무엇을 산출하는지* 못 박는다.

---

## Step 0 — 모드 판별

요청: "행사 운영 체크리스트 자동 생성 스킬 새로 만들어줘." → 없던 기능 신규 = **모드 B(신규 jc 스킬)**. (개조면 A, 기존 수정이면 C.)

깊이: 새 도메인이지만 산출은 단순 문서형 → **std**(quick/std/deep 중). deep까지 갈 필요 없음(§ SKILL.md 모드 깊이).

## Step 1 — 골격 + frontmatter

디렉터리 `jc-checklist/`, frontmatter는 4필드 템플릿(house-conventions):

```yaml
---
name: jc-checklist            # 디렉터리명과 정확히 일치 (C2)
description: MICE 행사 운영 체크리스트를 단계별(D-7~당일~철수)로 생성하는 스킬. 다음
  상황에서 반드시 이 스킬을 사용할 것 — 사용자가 '체크리스트', '운영 체크', '준비물
  리스트', 'D-day 체크'를 언급할 때. 단, 시간축 큐시트는 mice-run-of-show, 회의
  Action 추적은 mice-meeting-minutes 영역이므로 그쪽을 쓸 것.   # 무엇을+언제+경계 (C4)
version: "v1.0.0"             # 신규는 v1.0.0 (C3)
license: Complete terms in LICENSE.txt   # LICENSE.txt 동반 (C1·C6)
---
```

`LICENSE.txt`(Apache 2.0) 동반. SKILL.md 본문은 워크플로우·판단만, <500줄(C5).

## Step 2 — references 분리 (진행형 디스클로저)

상세는 SKILL.md에서 빼 `references/`로:

```
jc-checklist/
├─ SKILL.md                    # 모드·워크플로우 (<500줄)
├─ LICENSE.txt
├─ references/
│  ├─ checklist-templates.md   # 행사유형별 항목 라이브러리
│  └─ chaining-schema.md       # ChainPayload(→mice-run-of-show) (D-5)
└─ scripts/
   └─ build_checklist.py       # XLSX 산출 + --self-test (D-4)
```

식별정보는 전부 외부 주입 변수(C-1): `{{client_company}}`·`{{author_name}}`. 색·폰트는 SoT 런타임 로드, 미러 금지(C-2).

## Step 3 — 결정적 lint 채점

마감 전 `scripts/lint_skill.py`로 규약 준수를 기계 채점한다:

```
$ python3 .claude/skills/jc-skill-creator/scripts/lint_skill.py .claude/skills/jc-checklist
[lint] jc-checklist — 100/100  ✅ GO
------------------------------------------------------------
  ✓ C1 frontmatter 완전성                        20/20  누락: 없음
  ✓ C2 명명 일치(name==dir)                       10/10  OK
  ✓ C3 version SemVer                         10/10  OK
  ✓ C4 description 품질(길이·트리거·경계·한국어)          20/20  길이 168자
  ✓ C5 SKILL.md 분량(<500줄)                     10/10  142줄
  ✓ C6 LICENSE.txt 존재                          5/5   OK
  ✓ C7 RULE-NO-COMPANY(식별정보 0건)               15/15  위반 0
  ✓ C8 구조 위생(references/·scripts 자가검증)        10/10  references OK
```

**GO(≥90)** 가 아니면 해당 기준을 고치고 재채점. 예컨대 description을 한 줄로 줄였다면:

```
  · C4 description 품질(길이·트리거·경계·한국어)           4/20  길이 24자   → CONDITIONAL
```

→ `anti-patterns.md B-1`(너무 짧음)·`B-2`(경계 없음)로 돌아가 보강 후 다시 GO 확인.

## Step 4 — jc-redteam 정성 검증 (보완 게이트)

lint는 *규약*만 본다. 산출물이 *실제로 쓸 만한가*(항목 누락·논리·실무 적합성)는 `jc-redteam`으로 적대 검증한다. lint GO + redteam Critical 0 = 진짜 통과. (둘은 보완재 — `scoring-rubric.md` 한계 참조.)

## Step 5 — 마감

1. 플레이북 체크리스트 + (디자인/소비면) `check_drift.py`.
2. version 확정(`v1.0.0`).
3. 커밋 `jc-checklist: 행사 운영 체크리스트 스킬 신규 (v1.0.0)`, 작업 브랜치 → **드래프트 PR**.
4. README 카탈로그 +1 갱신.
5. (선택) `package_skill.py`로 `.skill` 패키징.

---

## 루브릭 자기 채점 (표본)

> 본 스킬(jc-skill-creator U1) 자체의 lint 결과 — 자가 적용 검증:

```
[lint] jc-skill-creator — 100/100  ✅ GO
```

채점자: `lint_skill.py`(결정적) + 최종 `jc-redteam` 권고. lint는 **규약 게이트**, redteam은 **품질 게이트** — 마감은 둘 다 통과를 요구한다.
