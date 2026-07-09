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

## 2026-07-04 — Drive 정본 풀 업그레이드 동기화 (CP2)

- **소스**: Google Drive `Skills/library/`(신규 정본, Jason 머신). 브랜치 `claude/drive-sync-20260704`.
- **반영**: 22종 overlap 스킬을 Drive 최신본으로 갱신(Phase 4 CP1 GO-1~4 + CP-N5 역참조 + CP2 Deep Audit Major 수정, Critical 0). `jc-prompt-builder` v1.0.0 신규 추가(선행 브리프 게이트, 라우팅 EXCLUDE). 상세: `docs/CHANGELOG-2026-07-04.md`.
- **보존**: `mice-run-of-show`·`mice-aftermath`(6월 forge 신규, Drive 미포함) — 삭제 없이 유지. 카탈로그 24→25종.
- **역참조 레이어**: 22종 중 19종 description에 브리프 게이트 역참조 삽입(예외 3종: jc-strategy-canvas 한도초과·jc-design-system reference 자산·jc-redteam 게이트 직행). 정본 맵: `.claude/skills/jc-prompt-builder/references/routing-map.md`.
- **주의(후속)**: Drive `library/`와 이 레포 `.claude/skills/`가 이제 두 미러 — 향후 편집 지점 일원화 필요. run-of-show/aftermath는 역으로 Drive에 미반영(백로그).

---

## 2026-07-10 — jc-orchestrator v1.1.0 신규 (에이전트 팩토리 실행체)

- **소스**: 챗 빌드(2026-07-10) → claude.ai 업로드본 캐시에서 26파일 회수(챗 ZIP 미다운로드 — 업로드 선행으로 회수 경로 대체). 배포 지시서: `docs/DEPLOY-jc-orchestrator-v1.1.0.md`. 브랜치 `feat/jc-orchestrator-v1.1.0`(베이스: `claude/drive-sync-20260704`).
- **결정**: 신규 스킬 — 운영지침 §8 에이전트 팩토리의 실행체(카탈로그 8아키타입·킥오프 3종·핸드오프 규약·구성안/PI 형식 SoT). 프리셋 2종: html-pt(8에이전트, 2026-05-07 스펙 재생성 v2) + code-conductor(비용 라우팅+강제 게이트+fable 스위치). 카탈로그 25→**26종**.
- **정합**: `jc-prompt-builder` v1.0.0→**v1.0.1** — routing-map §2 '멀티 에이전트 팀 구성' 행 '없음(직접 수행)'→매핑=jc-orchestrator + SKILL.md §6 동일 갱신. 계류 v1.1.0 개정 부재로 흡수 불가 → 직접 최소 갱신 판정(지시서 §1-4). description·registry 무변경(CP-N5 게이트 비발동, registry 22종 스냅숏 유지 — 차기 재생성 시 포함 확인).
- **배포 채널**: claude.ai 업로드 v1.1.0 ✅(2026-07-10, 사용자 수행) / Drive `Skills/library/` ✅ / git 본 브랜치 ✅ / 전역 `~/.claude/skills` — 본 배포에서 설치.
- **후속**: html-pt 원본(v1) zip 발견 시 재생성본(v2)과 diff 대조 병합 후 patch 범프 / 지침 §8 개정의 사용자 설정 UI 반영 확인(미반영 시 이중 SoT 드리프트) / code-conductor 환경 설치는 머신별 실측 로그 별도 기재.

### code-conductor 설치 로그 (머신별)

- `2026-07-10 | code-conductor 설치 | Jason(DESKTOP-26ACTQL, Windows 네이티브) | (a)차단OK/(b)통과OK`
  - §0: claude CLI 2.1.123 → **2.1.206 업데이트 후 통과**(요구 2.1.196+). 모델 문자열 2종 유효(2026-07-10).
  - Windows 적응 3건: ① 훅 커맨드 `python -X utf8 "<경로>"` 명시 — **utf8 플래그 없으면 한국어 차단 메시지 cp949 깨짐**(단위 실측으로 발견·교정) ② 심링크(ln -sfn) → 파일 복사로 대체(agents·active.md — `fable status`의 agents [--]는 정상) ③ 리매핑(env.sh) 생략 — 비용 우선(지시서 §2 선택 조항).
  - §4 실측: (a) 중첩 세션에서 c1·c2 생성 후 c3 차단 + BLOCKED 보고 / (b) 서브에이전트 d1~d3 전부 생성. 훅 단위 실측 7케이스(허용 2→차단·서브 통과·턴 리셋·Bash 리다이렉트 차단·비코드 통과) 전부 정상. 부수 증거: 설치 세션 자체의 Bash 호출이 게이트에 실차단됨(훅 즉시 적용 확인).
  - 잔여: icejc 머신 설치 미수행. INSTALL.md에 Windows 적응 절 추가 권고(→ patch 범프 후보).
- 후속(2026-07-10): INSTALL.md에 Windows 네이티브 환경 적응 절(§6) 추가 — 위 적응 3건 중 문서화 대상 3건(utf8 훅 커맨드·심링크=복사·`claude update`) 반영, env.sh 생략은 머신별 선택이라 제외. jc-orchestrator **v1.1.0→v1.1.1** patch 범프(Drive 정본 편집 → git·전역 승격, `feat/jc-orchestrator-v1.1.0` 브랜치 추가 커밋). 잔여는 icejc 머신 설치만.
