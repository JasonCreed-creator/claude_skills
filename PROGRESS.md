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

## 2026-07-12 — CP3 인테이크: 5종 업그레이드 + 2종 신규 (Drive 정본 동기화)

- **소스**: Google Drive `Skills/library/`(정본). 브랜치 `claude/drive-sync-cp3-20260712`(베이스: 현행 `main` = PR #14·#16 머지 후). 결정 정본: `docs/CP3-decision-matrix.md`. 외부 소스 판정 — ECC(everything-claude-code 2.0.0, 278종)에서 후보 20건→채택 7건, superpowers/skills-main/doc-coauthoring/image-enhancer는 델타 0 또는 SKIP.
- **업그레이드 5종**:
  - mice-market-intel v1.0.3→**v1.0.4** — T7 렌즈(타깃 주체 심층 프로파일)+진입점 4종 + `references/competitive-analysis-method.md` 신규(경쟁분석 3종: 티어링→9차원 가중 스코어링→의사결정형 리포트). CP1 잔여 GO(company-intel 역참조) 완결.
  - jc-doc-coauthor v1.0.0→**v1.0.1** — 아티팩트 링크 제공 규칙·공유문서 alt-text 체크.
  - jc-skill-forge v1.0.2→**v1.0.3** — 점검 2모드(Quick Scan/Full Stocktake)·NEW 판정 전 중복 탐색 게이트.
  - jc-orchestrator v1.1.1→**v1.1.2** — 병렬 스텝 탐지·안티패턴 카탈로그 3종(컨텍스트 브리프 패턴은 jc-prompt-builder 중복으로 불채택). §6 Windows 적응 절(v1.1.1) 보존 확인.
  - jc-redteam v1.2.1→**v1.2.2** — opt-in 강도 티어 2종(이중 독립 감수 수렴·결정 카운슬), 기본 2모드 불변.
- **신규 2종**(각 LICENSE.txt 포함):
  - **jc-brand-discovery v1.0.0** — 8모듈 브랜드 정체성 인터뷰(대상 모드 3종: event/personal/client, state.json 다중세션).
  - **jc-workspace-ops v1.0.0** — MICE Drive 운영 층(폴더 위계·문서 배치·권한 위생 P1~P6·트래커 규약).
- **레거시 보존**: `mice-run-of-show`·`mice-aftermath` 유지(삭제 없음). 카탈로그 26→**28종**(자사 기준).
- **적용 방식**: 기존 스킬 폴더 위 덮어쓰기+신규 파일 추가(폴더 단위 삭제 없음). 라인엔딩 정규화(autocrlf)로 실질 변경 파일만 diff 반영 — 커밋 변경분 = SKILL.md 5종 + 신규 9파일.
- **후속**: registry/routing-map 재생성(신규 2종 description 편입) · claude.ai zip 재업로드(갱신 7종) · PROGRESS.md는 본 git 인테이크 로그로 유지(Drive `Skills/PROGRESS.md`는 별도 워킹 체크포인트 문서).

## [CP3 후속] Minor 백로그 동기화 — 2026-07-12

- **소스**: Google Drive `Skills/library/`(정본). 브랜치 `claude/drive-sync-backlog-20260712`(베이스: 현행 `main` = PR #17 머지 후). CP3 인테이크(PR #17) 이후 Drive 정본에 쌓인 Minor 백로그 3건을 동기화.
- **백로그 3건**:
  - ① jc-orchestrator SKILL.md v1.1.1 이력 행 **실명 일반화** — 레포 사본에 이미 반영됨(PR #17 세션 자체 정리), 실질 diff 0.
  - ② jc-brand-discovery **ECC 용어 정리**(70_owner-tension.md·participants/·participant-a 치환) — 레포 사본에 이미 반영됨, 실질 diff 0.
  - ③ jc-prompt-builder **registry 재생성(22→25종)** + routing-map 갱신 + SKILL.md §9 헤더 증분 — 본 동기화로 반영(레포 미반영분).
- **실반영 = ③ (jc-prompt-builder 3파일)**:
  - `references/description-registry.md` — 22→**25종** 재생성: `jc-orchestrator` 스냅숏 최초 편입 + 신규 2종 `jc-brand-discovery`·`jc-workspace-ops` 추가. 헤더 생성일 2026-07-12·소스 25종. 버전 범프 반영(jc-doc-coauthor v1.0.1·jc-redteam v1.2.2·jc-skill-forge v1.0.3·mice-market-intel v1.0.4·jc-orchestrator v1.1.2).
  - `references/routing-map.md` — 2026-07-12 증분 노트 + §2 행 **2건 추가**(brand-discovery·workspace-ops) + §3 판별 **2건**(§3-3 브랜드 정체성 발굴 분기·§3-8 "정리·파일" 신설).
  - `SKILL.md` — §9 파일 트리 주석 "현행 22종" → "현행 25종".
- **적용 방식**: 자사 26종 폴더 위 파일 단위 덮어쓰기(폴더 삭제 없음·레거시 2종·_README.txt 보존). 라인엔딩 정규화(autocrlf)로 실질 변경 파일만 diff 반영 — 커밋 변경분 = jc-prompt-builder 3파일. 나머지 25종은 정본=레포 내용 동일(diff 0) 확인.
- **후속**: claude.ai zip 재업로드(갱신분)는 별도 진행 중 · Drive `Skills/PROGRESS.md`는 별도 워킹 체크포인트 문서로 유지.

---

## 2026-08-18 — CP4 동기화: Drive 병합대기분(2026-07-25) git 반영

- **소스**: Drive `PROGRESS-병합대기_20260725_cinematic_v2.md` + library 실측(07-25 수정분). 브랜치 `claude/skill-library-phase-0-validation-ef0jsa`.
- **결정**: [리멤버 전환] Phase 0 3자 대조에서 Drive>git 병합대기 1건 발견 → 전환 착수 전 선반영(A안, 2026-08-18 기획자님 승인). registry 역행 덮어쓰기(cinematic 항목 소실) 방지 목적.

### 산출
- `jc-cinematic-html` v1.0.0 신규 — SKILL.md + references/build-kit.md (시네마틱 캠페인 룩 정본. 웜 블랙 스테이지·단일 오렌지 광원·디오라마 히어로·필름 크롬·모션 1회재생 표준)
- `jc-workspace-ops` v1.0.0 → **v1.1.0** — 세션 층 흡수('체크인/체크아웃/PROGRESS/세션 이어서' 트리거 6종, 세션 2파일 템플릿 전개, session-protocol.md 포인터)
- `jc-prompt-builder` registry(25→26종, 07-25본)·routing-map(07-25 증분 노트 포함) 동기
- `jc-design-system/references/cinematic-campaign-html.md` — 포인터로 신설(값 미보유, 드리프트 방지). SKILL.md 무범프 이력 한 줄 + 파일 구조 갱신
- 바이트 검증: cinematic SKILL.md 5,489B · build-kit.md 8,587B · wsops SKILL.md 12,178B · registry 39,713B · routing-map 16,733B — Drive 실측 크기와 전량 일치

### 잔여(병합대기 v2 기준)
- routing-map §2 cinematic 행 추가 + §3 키워드 경계 → [리멤버 전환] Phase 2에서 함께 처리
- Drive 병합대기 v1·v2 파일 삭제 → Phase 4 Drive 반영 시 처리
- CLAUDE.md·MASTER-CONTEXT 카운트(26→27) → Drive 챗 문서, 수동 이월

---

## 2026-08-18 — [리멤버 전환] 변경명세서 v1.0 집행 (D1·D2) · Phase 4 채널 상태

명세서 §5 절차 집행 완료. 변경 스킬·검증은 PR #21 본문 참조.

### 채널 4종 반영 상태 ('소스 반영 ≠ 배포')

| 채널 | 상태 | 비고 |
|---|---|---|
| ② git 정본 | **반영 완료** | 브랜치 `claude/skill-library-phase-0-validation-ef0jsa`, 드래프트 PR #21(base: `claude/relaxed-fermat-M5h5C`), CI drift-guard green |
| ③ claude.ai .skill | **반영 완료** (2026-08-18) | 변경 6종 .skill ZIP(mice-estimate·jc-design-system·jc-theme-factory·mice-dashboard·jc-workspace-ops·jc-cinematic-html) 기획자님 업로드 완료 확인 |
| ① Drive `library/` | **미반영(수동 권장)** | Drive MCP는 콘텐츠 업데이트 도구 부재(create+trash만 가능 — 파일 ID·공유링크 변경 위험) + 다중 미러 구조 모호. D1/D2 변경분(오버레이 2파일·mice-estimate 9파일·registry/routing-map 등 약 20파일)은 PR 머지 후 Drive UI에서 반영 권장. cinematic·workspace-ops는 Drive가 이미 정본(병합대기 원본) |
| ④ 전역 설치 2머신(icejc·Jason) | **미반영(수동)** | 사용자 머신 로컬 설치 — 원격 세션에서 불가. PR 머지 후 각 머신에서 pull·설치 |

### 미결 이월
- registry 전체 재생성(run-of-show·aftermath·cinematic §2 행 편입, 26→28종) — 두 미러 정합 백로그
- Drive `library/`의 jc-design-system `cinematic-campaign-html.md` 포인터 축약(병합대기 v2 잔여 task#1) — Drive 반영 시 동시 처리
- calcEstimate 리멤버 양식 연결(Sprint 1.6) · 입사 후 과제 §6(jc-comms 리멤버 양식·슬랙 채널 ID·리멤버 CI 실측)

---

## 2026-08-18 — [리멤버 전환] 후속조치: 잔여 드리프트 정리 + 템플릿 자산 정화

PR #21 머지 후 Drive `library/` 반영(채널 ①) 작업 중 발견한 잔여분 처리. 명세서 §2 D1/D2의
*의도*는 반영됐으나 실제 자산·활성 사양부에 남아 있던 누락분이다.

### A. 템플릿 자산 정화 (`mice-estimate/assets/mnc_template.xlsx`) — **중대**

Phase 1에서 교체했다고 기록한 직인 치환이 **커밋되지 않아 정본에 반영되지 않은 상태**였다. 실측 재확인 결과:

| 항목 | 발견 | 조치 |
|---|---|---|
| `xl/media/image1.png` (86,636B) | 구 소속사 **법인 직인** 원본 그대로 잔존 | 동일 픽셀 크기(162×200) 중립 placeholder(1,382B)로 치환 — 시트 레이아웃·drawing 앵커 불변 |
| `sheet1.xml.rels` 하이퍼링크 | 셀 K7 표시값은 `(외부 주입 - 이메일)`로 치환됐으나 **하이퍼링크 타깃에 구 소속사 도메인 개인 메일이 그대로 살아 있음** (클릭 시 실주소로 연결) | `<hyperlinks>` 블록 + hyperlink Relationship 제거 |

- 결과: 105,072B → **19,756B**. openpyxl 로드 정상(`A1:K121`, 이미지 1), zip 무결성 OK, 회사/PII 토큰 **0건**.
- 최초 스캔이 이를 놓친 이유: 한글 상호·`M&C` 철자만 훑고 **도메인 문자열과 rels 내부 링크 타깃을 보지 않았다.** 이후 자산 점검은 `.rels`·`media/`까지 포함한다.

### B. 활성 사양부의 아카이브 오버레이 참조 제거

D2로 `mc`·`darktrace`를 아카이브했으나, **선택지를 제시하는 활성 사양부**가 여전히 두 값을 유효한 것처럼 열거하고 있었다.

| 스킬 | 위치 | 조치 |
|---|---|---|
| `mice-dashboard` v2.0.4 | Step 4 톤 매핑표 · 오버레이 슬롯 표 · 코드 작성 원칙 | `mc` → `remember`, 슬롯 열거에서 아카이브분 제외 |
| `mice-dashboard` | `references/jc-design-mapping.md` §1·§2·§6, `references/chaining-schema.md` 출력 예시 | 동일 기준 동기 (hex 값 불변 — `remember`와 시그니처 컬러가 동일) |
| `jc-theme-factory` v1.1.1 | §1 쇼케이스 본문 등록 오버레이 예시 | 아카이브분 제거 + 쇼케이스 제외 원칙 명문화 |
| `jc-brand-styling` v1.0.2 | CLI 사용 예시 `--client darktrace` (SKILL.md + `style_pptx.py` docstring) | `--client remember`로 교체 |

**버전 히스토리(과거 이력) 기술은 원문 보존** — `mice-dashboard` v2.0 항목의 당시 오버레이 열거는 이력이므로 수정하지 않았다.

### C. registry 정비
- 버전 헤딩 동기: jc-theme-factory v1.1.1 · mice-dashboard v2.0.4 · jc-brand-styling v1.0.2
- 줄바꿈 **LF 정규화** (구 CRLF 혼재 116행) — 라이브러리 내 유일한 예외였고, Drive 왕복 시 바이트 대조를 불가능하게 만들던 원인

### 검증
- `check_drift.py` ✅ 통과 (비-canon 토큰 0건)
- 전 라이브러리 회사 도메인·이메일 스윕: 잔존 `엠앤씨`/`M&C` 히트는 **전량 RULE-NO-COMPANY 금지어 필터 목록**(명세서 §4 존치 대상) + 변경 이력 기술. 실 하드코딩 0건
- OOXML 자산 2종 전수 스캔: `mnc_template.xlsx` ✅ / `remember_template.xlsx` — 아래 결정 대기

### 기획자님 결정 필요 (미조치)
- `remember_template.xlsx`에 **리멤버 워드마크 로고 이미지 2개(각 59,001B)가 하드코딩**되어 있다. 구 소속사 직인과 *구조적으로 동일한 사안*이지만, 신 소속사 자사 양식에 자사 로고가 들어가는 것은 통상적이기도 하다. RULE-NO-COMPANY(공급자 로고=외부 주입 슬롯) 원칙을 그대로 적용할지 여부는 기획자님 판단 사항이라 **임의 변경하지 않았다.**
- `pt-script`·`mice-proposal`의 `darktrace_korea` 예시는 명세서 §4 무변경 대상(pt-script)·단순 이력 예시(mice-proposal)라 존치.
