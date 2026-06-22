# PROGRESS — 스킬 인테이크 로그

jc-skill-forge 인테이크 적용 기록 (날짜·소스·결정·근거).

---

## 2026-06-05 — mice-run-of-show 신규 (forge N1)

- **소스**: `jcskillforge_______20260605.md` (Chat 산출 실행패키지) Wave 2 = N1
- **브랜치**: `claude/epic-fermat-YmIvr` → `main`
- **결정**: 행사 운영 큐시트(run of show) 신규. 카탈로그 22→**23종**.

### 산출
- `mice-run-of-show` v1.0.0 — SKILL.md + references 6종(cuesheet-columns·cue-notation·chaining-schema·jc-design-mapping·anti-patterns·worked-example) + scripts/build_runsheet.py
- 10컬럼 버전드 큐시트 XLSX(Cue#/시간/세그먼트/무대·발표/Audio/Video/Light/연출cue/Owner/비고) + 변경이력 시트
- **시간 무결성 자동검증**(소요 합=총 행사시간) + 클록 자동산출 + 연출 표기 표준 + quick/std/deep + ChainPayload 입출력(mice-proposal·pt-script)
- 흡수(패턴만): Association Event Management, production cue sheet → jc 재구성. mice-estimate xlsx(openpyxl + jc-design SoT 런타임 로드) 패턴 재사용.
- 회귀 리스크 0 (기존 스킬 미접촉).

### 검증
- `build_runsheet.py` self-test: 반일 컨퍼런스 11 cue/210분(09:00~12:30) 생성·재오픈 무결성 **PASS** + 시간 불일치 차단(ValueError).
- jc-design SoT 토큰 실제 로드 확인(JSON 파싱).
- jc-redteam 인테이크 감수 — 3건 적발·교정(단일 타임라인 한계 §10 명시 / worked-example 채점 정정 / 체이닝 enum 후속 표기).

### 후속 권고
- F-1 `chaining-protocol.md`에 `mice-run-of-show` source enum 등록 — jc-design-system 변경이라 본 PR 범위 밖(N1은 소비자로 동작). 별도 승인 시 추가.

---

## 2026-06-05 — mice-aftermath 신규 (forge N3)

- **소스**: `jcskillforge_______20260605.md` Wave 4 = N3 (다음 스텝으로 사용자 선택)
- **브랜치**: `claude/epic-fermat-YmIvr` → `main` (run-of-show 머지 후 최신 main 위)
- **결정**: 행사 사후 결과보고 + 재사용 케이스 빌더 신규. 카탈로그 23→**24종**.

### 산출
- `mice-aftermath` v1.0.0 — SKILL.md + references 4종(report-structure·case-builder·chaining-schema·report-spec). **reference-driven**(스크립트 없음 — 최신 exemplar `mice-market-intel` 패턴).
- 8축 사후 결과보고 프레임(요약·개요·목표 대비 성과·예산 실적·운영 하이라이트·이슈/교훈·피드백·차기 권고) + 재사용 케이스 빌더(challenge→approach→result→proof·익명화·재사용 등급 R0~R3).
- Phase 0~4(목표 대비 원칙·과장/추정 금지). 입력 체이닝(dashboard/estimate/minutes/run-of-show), 출력 ChainPayload(→proposal/sponsor-deck) — 한 행사 결과를 다음 수주 자산으로 잇는 선순환.
- 흡수(패턴만): proposal-skills(case study)·Association(post-event metrics) → jc 재구성.
- 회귀 리스크 0 (기존 스킬 미접촉).

### 검증
- description 874자(≤1024), 금칙 토큰 0(SoT canonical만), drift-guard PASS.
- jc-redteam 인테이크 감수 — 주요 1건: **mice-dashboard와 '결과보고서' 트리거 소프트 오버랩** → §1 경계 문구로 완화(dashboard=차트/시각화, aftermath=서사 종합+재사용 케이스). 잔여 소프트 오버랩으로 인지·문서화.
- 8축↔case 4요소↔chaining 페이로드 상호 정합 확인.

### 후속 권고
- F-1' `chaining-protocol.md`에 `mice-aftermath` source enum 등록(run-of-show와 동일 — jc-design-system 변경, 별도 승인).
- (선택) 사후보고 HTML 샘플 아티팩트 생성(reference-driven이라 요청 시).

---

## 2026-06-05 — F-1 ChainPayload source enum 등록 (run-of-show · aftermath)

- **결정**: 두 신규 스킬을 봉투 정본에 등록해 체이닝 정합 완성(사용자 선택 "#8 머지 + F-1").
- **변경**: `jc-design-system/references/chaining-protocol.md` — §1 적용 대상 · §3 source enum · §4 페이로드 매핑표(2행) · §5-5 엣지표(4행)에 `mice-run-of-show`·`mice-aftermath` **추가**(additive). 두 스킬의 `chaining-schema.md` 등록 노트를 "완료"로 갱신.
- **버전**: jc-design-system 버전 범프 없음 — strategy-canvas·market-intel가 v1.2.0에서 무범프 등록된 **선례 일치**(순수 additive enum 등록).
- **검증**: drift-guard PASS(jc-design-system은 CONSUMERS 비대상, 텍스트 additive·JSON 무변경), 금칙 토큰 0.
- F-1/F-1' 후속 권고 **해소 완료**.

---

## 부속 발견 — 병렬 포지 작업과의 정합 (별도 보고)

이번 N1은 **옛 11종 스냅샷** 기반으로 착수했으나, 작업 중 `main`이 PR #1~#6으로 **22종 동기화**돼 있음을 확인. 그 과정에서:

- 본래 Wave 1(키스톤 `jc-skill-creator` 신규)을 별도 빌드했으나, **main에 이미 `jc-skill-creator`가 존재**(병렬 작업) → 사용자 결정으로 **내 키스톤은 폐기**, main 것 유지. 본 PR은 **mice-run-of-show만** 반영.
- **관찰(권고)**: main의 `jc-skill-creator`는 상위 skill-creator에 평가 기계를 위임하는 얇은 층이며, forge 문서 **U1이 의무화한 4대 요소(worked example·anti-pattern 라이브러리·결정적 스코어링 루브릭·quick/std/deep)와 자동 채점기(lint)를 갖추지 않았다.** U1 완성을 원하면 별도 사이클에서 main 키스톤에 4대 요소·lint를 보강 권고(폐기한 키스톤 작업물 재활용 가능).

---

## 2026-06-05 — 보안: 공개 레포 PII 스크럽 (RULE-NO-COMPANY 정합)

- **결정**: 공개 레포에 하드코딩돼 있던 실명·회사 이메일·사명·부서를 `RULE-NO-COMPANY` 외부 주입 변수로 치환(사용자 선택). PR #1·#2가 반복 플래그한 잔여 이슈 해소.
- **스크럽(실제 노출 → 변수화)**:
  - `mice-proposal/references/slide-masters.md` (3곳: 푸터 198 · 담당자 마스터 301 · Thank You 376) — `M&C커뮤니케이션즈 신사업실 / 이진철 실장 / leejc@mnccomm.com / 010-...` → `{{company_name}} {{author_dept}} {{author_name}} {{author_title}} {{author_email}} {{author_phone}}`.
  - `.claude/commands/skillupgrade.md` 페르소나 — 실명/사명/직함 제거, 기능 맥락("MICE 18년 전략가")만 유지.
  - `jc-skill-forge/SKILL.md` description — "기획자님(이진철)" → "기획자님". version v1.0.0→**v1.0.1**.
- **SoT 등록**: `shared-rules.md#RULE-NO-COMPANY` §허용 슬롯에 연락처 3종(`{{author_dept}}`·`{{author_email}}`·`{{author_phone}}`) additive 등록(무범프 — chaining enum 선례 일치).
- **보존(의도)**: `pt-script`·`mice-sponsor-deck`의 sanitizer 차단 리스트(`FORBIDDEN_TERMS`·`forbidden`·`re.sub`)와 `shared-rules.md`의 RULE 정의부는 *회사명을 출력에서 검출·제거하기 위해 보유*하는 항목이라 그대로 둠. `mice-estimate`의 `M&C 견적서`는 §120 양식 식별자로 허용.
- **검증**: 실명·이메일(`이진철`·`leejc`·`mnccomm`) 전수 **0건**. 잔존 `M&C커뮤니케이션즈`/`신사업실`은 전부 sanitizer/정의부(8곳, 의도된 보유). 디자인 토큰 무변경이라 drift-guard 영향 없음.
- **주의**: 현재 파일은 정리됐으나 **git 히스토리에는 PII가 잔존**. 완전 제거를 원하면 히스토리 재작성(filter-repo) 또는 레포 private 전환을 별도 결정해야 함.

---

## 2026-06-05 — jc-skill-creator U1 완성 (4대 의무요소 + lint)

- **결정**: PR #7이 관찰·권고했던 **U1 미충족**(main 키스톤이 worked example·anti-pattern·결정적 루브릭·quick/std/deep·자동채점기 부재)을 해소(사용자 선택). `jc-skill-creator` v1.0.0 → **v1.1.0**.
- **산출**:
  - `scripts/lint_skill.py` — **결정적 자동 채점기**(stdlib only). 8기준 100점 → GO(≥90)/CONDITIONAL/NO-GO. `--json`(CI·체이닝)·`--self-test`. NO-GO 종료코드 1 = CI 게이트.
  - `references/scoring-rubric.md` — 8기준 루브릭 **정본**(lint와 1:1, 둘이 항상 일치).
  - `references/anti-patterns.md` — 제작 안티패턴 라이브러리(A 메타데이터·B description·C 디자인/식별·D 구조/생태계), 각 항목 루브릭 연결.
  - `references/worked-example.md` — 신규 스킬(`jc-checklist`) end-to-end 완주 + lint 채점 표본.
  - `SKILL.md` — **quick/std/deep** 작업 깊이 + **결정적 품질 루브릭(lint)** 섹션 + 마감 절차에 lint GO 게이트 추가 + 파일 구조·description 갱신.
- **설계 원칙**: lint=**규약 게이트**(명명·메타·SemVer·description·분량·LICENSE·RULE-NO-COMPANY·구조), jc-redteam=**품질 게이트**(논리·설득력·디자인). 둘은 보완재, 마감은 둘 다 통과 요구. 상위 skill-creator 평가 기계와 별개(그건 deep 모드에서만 호출).
- **검증**:
  - `lint_skill.py --self-test` **PASS**(good=100 GO / bad=33 NO-GO, C2 명명·C3 SemVer·C7 PII 감점 단위검증).
  - 라이브러리 회귀 스캔: jc-skill-creator 100 / jc-strategy-canvas 100 / mice-run-of-show 90 — **GO**, 오탐 0. (mice-proposal 86 CONDITIONAL = version 미기재 실제 신호, 본 PR 범위 밖.)
  - **lint→교정→재채점 루프 실증**: anti-patterns.md가 금칙어를 *교육 목적 인용*해 C7 플래그 → "금칙" 프레이밍으로 정정 → **100 GO**.
- **후속(선택)**: ① CI 워크플로에 lint NO-GO 게이트 추가(현재는 수동/마감 절차). ② CONDITIONAL 스킬 잔여 보강.

---

## 2026-06-05 — lint 라이브러리 1차 적용 (LICENSE 12종 + C7 견고화)

- **결정**: 방금 만든 `lint_skill.py`를 전 스킬에 적용해 결정적 위반을 스윕(사용자 "다음 스텝 계속 진행").
- **스코어카드 개선**: **CONDITIONAL 7종 → 1종**, GO 16→23/24.
- **LICENSE 보강(12종)**: PR #10이 신규 스킬에만 넣어 누락됐던 코어 스킬에 Apache 2.0 `LICENSE.txt`(기존 12종과 동일 해시) 복사 + frontmatter `license:` 필드 추가 — jc-design-system·jc-landing-page·jc-redteam·mice-aftermath·mice-dashboard·mice-estimate·mice-meeting-minutes·mice-proposal·mice-rfp-analyzer·mice-run-of-show·mice-sponsor-deck·pt-script. (C1·C6 각 +5)
- **lint C7 견고화**: 정의부(`shared-rules.md#RULE-NO-COMPANY`)·블록리스트(`FORBIDDEN_TERMS=[...]`)가 마커는 선언 줄에만 두고 리터럴은 다음 줄에 둬서 발생한 **오탐 2건**(jc-design-system·pt-script) 해소 → 마커 면제를 **±3줄 윈도우**로 확장. 실제 누출은 주변 마커가 없어 그대로 검출(self-test PASS 유지). 루브릭 정본 동기화.
- **남은 CONDITIONAL 1종**: `jc-landing-page` 80 — SKILL.md 738줄(C5)·references 없음(C8). **실제 구조 신호** → SKILL.md를 references로 분할하는 별도 리팩터 권고(본 스윕 범위 밖).
- **검증**: `lint_skill.py --self-test` PASS, 전 스킬 재채점 23 GO/1 COND, drift-guard 통과.

---

## 2026-06-05 — jc-landing-page 리팩터 + CI lint 게이트 (라이브러리 24/24 GO)

- **결정**: 사용자 선택(① LP 리팩터 → ② CI 게이트 → ③ 마무리).
- **① jc-landing-page 리팩터 (v1.1.0 → v1.1.1)**: 738줄 SKILL.md(루브릭 C5 위반)를 references 3종으로 분할 → **267줄**. `form-standard.md`(폼)·`scaling-implementation.md`(고정비율 스케일링 핵심)·`hero-video.md`(Hero 영상) 추출, SKILL.md엔 포인터만. 동작 변경 0(순수 구조 분할). description에 형제 경계(jc-artifact-builder·mice-proposal·mice-sponsor-deck) 추가(C4). → **80 CONDITIONAL → 100 GO**. 안티패턴 D-1 자가 교정 사례.
- **② CI lint 게이트**: `lint_skill.py`에 `--all <root>` 모드 추가(전 스킬 일괄 채점, NO-GO 있으면 exit 1, CONDITIONAL은 경고). 신규 워크플로 `.github/workflows/skill-lint.yml` — PR마다 self-test + `--all .claude/skills`. drift-guard와 별개 체크. 최악 회귀(frontmatter·명명·PII·SemVer)만 차단, 경미한 결함은 비차단.
- **결과**: 라이브러리 **24/24 GO** (이번 세션 시작 시 7 CONDITIONAL → 0). 
- **검증**: `--all` 24 GO exit 0, `--self-test` PASS, drift-guard 통과. 본 PR에서 skill-lint 워크플로 자체가 첫 게이트 통과를 시연.
- **남은 후속(선택)**: 미검증 신규 2종(strategy-canvas·market-intel) 실사용 스모크, mice-aftermath HTML 샘플(둘 다 사용자 미선택).
