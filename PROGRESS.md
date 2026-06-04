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

## 부속 발견 — 병렬 포지 작업과의 정합 (별도 보고)

이번 N1은 **옛 11종 스냅샷** 기반으로 착수했으나, 작업 중 `main`이 PR #1~#6으로 **22종 동기화**돼 있음을 확인. 그 과정에서:

- 본래 Wave 1(키스톤 `jc-skill-creator` 신규)을 별도 빌드했으나, **main에 이미 `jc-skill-creator`가 존재**(병렬 작업) → 사용자 결정으로 **내 키스톤은 폐기**, main 것 유지. 본 PR은 **mice-run-of-show만** 반영.
- **관찰(권고)**: main의 `jc-skill-creator`는 상위 skill-creator에 평가 기계를 위임하는 얇은 층이며, forge 문서 **U1이 의무화한 4대 요소(worked example·anti-pattern 라이브러리·결정적 스코어링 루브릭·quick/std/deep)와 자동 채점기(lint)를 갖추지 않았다.** U1 완성을 원하면 별도 사이클에서 main 키스톤에 4대 요소·lint를 보강 권고(폐기한 키스톤 작업물 재활용 가능).
