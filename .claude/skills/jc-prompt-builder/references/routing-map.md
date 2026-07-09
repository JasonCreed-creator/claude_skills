# Routing Map — 산출물 → 매핑 스킬 라우팅 맵

> 상태: **확정본 (DRAFT 해제 2026-07-04, CP2 Major 수정 후 재생성)** — PROGRESS.md "[MAIN] Phase 4 완료" 신호(2026-07-03 23:14) 확인 후 확정. CP2 Deep Audit Major 수정에 따라 재실행.
> 근거: [`description-registry.md`](description-registry.md) — 정본 소스 `Skills/library/`(22종) 실측 재생성(확정본, 2026-07-04, "Phase 4 확정본 + CP-N5 역참조 + CP2 Major 수정"). 누적 registry 변경: 버전 범프(jc-redteam v1.2.1·jc-strategy-canvas **v1.0.2**·mice-market-intel **v1.0.3**·mice-meeting-minutes **v2.1.2**) + 브리프 게이트 역참조 19종 삽입. §2·§3 매핑 트리거/경계는 변동 없음(역참조·버전범프·CP2 수정 모두 산출물→스킬 매핑 불변; CP2 수정은 references/specs/scripts 대상, description 무변경).
> **역참조 레이어**: 22종 중 19종 description 말미에 "실행형 지시는 실행 전 jc-prompt-builder 브리프를 거친다." 삽입. 3종 예외는 §6 참조.
> **재해제 조건(챗 CP-N5 게이트)**: Phase 5(CP2) Deep Audit에서 description이 변경되면 재실행. CP2 Major 수정은 description을 건드리지 않았으나(references/specs/scripts만) 버전 범프 3건 반영 위해 재생성·재해제 완료(2026-07-04).
> **2026-07-10 증분**: 신규 스킬 `jc-orchestrator` v1.1.0 편입 — §2 '멀티 에이전트 팀 구성' 행을 '없음(직접 수행)' → 매핑=jc-orchestrator로 갱신(배포 지시서 §1-4, 계류 v1.1.0 개정 부재로 직접 최소 갱신). registry는 22종 스냅숏 유지 — 차기 재생성 시 본 스킬 포함 확인.

브리프 6필드 중 **'산출물' 필드의 매핑 스킬**을 결정하는 참조표. 지시의 의도·산출물 형태에서 스킬을 찾고, 겹침 구간(§3)은 판별 규칙 또는 승인 카드 내 가정으로 처리한다.

## 1. 사용법

1. 지시에서 산출물 형태(무엇이 나와야 하는가)를 식별한다.
2. §2에서 해당 행을 찾는다. 판별 키가 지시와 맞는지 확인한다.
3. 두 개 이상 걸리면 §3의 겹침 판별을 적용한다. 그래도 모호하면 **가정 필드에 후보와 선택 근거를 명시**하고 승인 시 확정받는다.
4. 매핑 스킬이 없는 작업(예: 일반 코드 수정)은 "없음(직접 수행)"으로 표기한다.

## 2. 산출물 → 스킬 매핑 (실측 description 기준)

| 산출물 / 의도 | 매핑 스킬 | 판별 키 (트리거 요지) | 산출 형태 |
|--------------|----------|---------------------|----------|
| RFP·공고·입찰 안내서 분석, GO/NO-GO | mice-rfp-analyzer | 'RFP 분석'·'비딩 분석'·'요건/평가 기준 분석' — *입력 문서* 해체 | .docx 보고서 + .xlsx 매트릭스 |
| 발주처 제출 제안서 | mice-proposal | '제안서'·'비딩'·'PT 자료' — 청중=발주처 | PPTX |
| 스폰서·협찬·후원 유치 데크 | mice-sponsor-deck | '스폰서/협찬/후원/파트너십' 키워드 **결합 필수** — 청중=잠재 스폰서 | HTML 데크(1차)→PPTX·XLSX |
| 견적서 | mice-estimate | '견적'·'산출내역서' (양식 2종: M&C/리멤버 — 양식 식별자) | XLSX |
| 발표 대본·MC 멘트 | pt-script | '대본'·'스크립트'·'발표 멘트'·'MC 멘트' | DOCX |
| 행사 결과·KPI 대시보드 | mice-dashboard | '대시보드'·'실적/성과 시각화' — MICE 데이터 전제. 비-MICE 범용은 description 자체가 data 계열로 배제(2026-07-03 실측 반영) | 단일 HTML (+PDF) |
| 회의록 구조화 | mice-meeting-minutes | '회의록'·'Action Items'·transcript 업로드 — 8축 프레임 | 단일 HTML 대시보드 |
| 시장·경쟁 인텔리전스 | mice-market-intel | '시장 조사'·'경쟁사 조사'·'벤치마크 행사' — 데이터 *수집* 상류 | 리서치 리포트 + ChainPayload |
| 전략 프레임워크 구조화 | jc-strategy-canvas | 'BMC'·'SWOT'·'Porter'·'JTBD'·'TAM/SAM/SOM'·'신사업' — 수집된 데이터의 *판단* | HTML 캔버스 + ChainPayload |
| 산문형 문서 공동작성 | jc-doc-coauthor | '같이 쓰자'·'기획서/운영계획서/Decision Doc/RFC' — N턴 프로세스 | .md 문서 |
| 커뮤니케이션 글 | jc-comms | '3P'·'주간 보고'·'뉴스레터'·'FAQ'·'공지'·'발주처 송부 메일' — 짧은 글 | 텍스트/메일 초안 |
| B2B 랜딩페이지 | jc-landing-page | 'LP'·'랜딩'·'신청/웨비나 페이지'·'사전등록 페이지'·'이벤트 신청서'·'뉴스레터 구독 페이지' — **산출 직후 jc-redteam LP 패널 검증 의무** | 단일 HTML |
| 인터랙티브 React 앱 | jc-artifact-builder | '아티팩트'·'웹앱'·'탭/모달/필터' — 상태관리·라우팅 필요 복합물 | 단일 HTML(React 번들) |
| 키비주얼·포스터·정적 아트 | jc-visual-philosophy | '키비주얼'·'포스터'·'표지/커버 아트'·'무드보드' — 정적 이미지 | .pdf/.png |
| p5.js 제너러티브 아트 | jc-generative-art | 'generative art'·'p5.js'·'플로우 필드'·'모션 배경' — 코드 아트 | 단일 HTML |
| 테마 선택·신규 오버레이 발행 | jc-theme-factory | '테마'·'팔레트'·'쇼케이스'·'어떤 테마 있어'·'신규 클라이언트 컬러' — *무엇을 입힐지 결정·발행·적용* | 오버레이 등록 + 산출물 적용 (PPTX 후처리 엔진은 styling 위임) |
| 기존 파일 리테마(후처리 실행) | jc-brand-styling | 완성 .pptx/HTML 제공 + 확정된 시그니처/기존 오버레이 '입혀줘'·'리테마' — *적용 엔진, 신규 팔레트 발행 불가* | 수정된 원본 형식 |
| 멀티 에이전트 팀 구성·오케스트레이션 | jc-orchestrator | '팀 짜줘'·'에이전트 팩토리'·'멀티 에이전트'·'Project Instructions'·복합 작업(이질 역량 3+) 실행 체계 요청 — 지침 §8 팩토리의 실행체. 승인된 브리프 필드는 팩토리 프로토콜 1단계 기입력으로 승계 | 구성안 + Project Instructions |
| 디자인 토큰 정의·수정 | jc-design-system | '디자인 토큰'·'스타일 가이드' — 값의 SoT 직접 작업 | reference 갱신 |
| MCP 서버 설계·구현 | jc-mcp-builder | 'MCP'·'커넥터'·'외부 API 연동 서버' — 재사용 도구 서버 | 서버 코드 |
| 스킬 신규 제작·개조·개선 | jc-skill-creator | '스킬 만들어줘'·'프리셋 개조' — 메타 작업 | 스킬 폴더 |
| 스킬 라이브러리 점검·외부 대조 | jc-skill-forge | '스킬 업그레이드'·'스킬 스캔'·'외부 스킬 찾아줘' | 스캔·제안 리포트 |
| 완성물 적대적 검증·최종 감수 | jc-redteam | '레드팀'·'검증해줘'·'감수해줘'·'허점 찾아줘' — *완성물* 공격 | 인라인 비평/감수 리포트 |

## 3. 겹침 구간 판별 (동일 키워드 다중 후보)

### 3-1. "대시보드"
- 행사 결과·KPI **정적 보고 1장** → mice-dashboard
- **회의록** 기반 → mice-meeting-minutes
- 상태관리·라우팅 있는 **인터랙티브 앱** → jc-artifact-builder
- **비-MICE 일반 데이터** → 플랫폼 내장 data 계열 스킬(data:build-dashboard·data:create-viz) — mice-dashboard description 자체가 이를 배제하도록 스코핑됨(2026-07-03 library 실측, §4 참조)

### 3-2. "제안서 · PT · 비딩 · RFP · 입찰"
- 청중 = **발주처**(비딩·수주) → mice-proposal
- 청중 = **잠재 스폰서**(협찬·후원·파트너십 키워드 결합) → mice-sponsor-deck
- 제안서는 이미 있고 **발표 대본**이 필요 → pt-script
- '비딩'·'RFP'·'입찰' 단독은 **의도로 분기** (두 스킬 트리거에 동시 실재): 문서 해체·GO/NO-GO·평가 기준 도출 = mice-rfp-analyzer / 제출물(PPTX) 생성 = mice-proposal. 의도 불명이면 가정 필드로.
- 청중 불명이면 가정 필드로: "A) 발주처 대상으로 가정".

### 3-3. "테마 · 브랜드 · 색"
- 판별 축은 파일 유무가 아니라 **작업 성격**이다 (factory는 파일 첨부 케이스도 명시 트리거로 보유):
  - 테마 **선택·쇼케이스·신규 오버레이 발행**이 필요하면(파일 유무 무관) → jc-theme-factory
  - 이미 확정된 시그니처·등록 오버레이를 기존 파일에 **후처리 실행만** 하면 → jc-brand-styling
  - 토큰 **값 자체의 정의·수정** → jc-design-system
- 실측상 '우리 톤으로 바꿔줘'가 factory·styling 양쪽 트리거에 존재(§4 참조) — 신규 팔레트/오버레이 결정이 필요한지로 가른다. 모호하면 가정 필드로.

### 3-4. "문서 · 초안"
- 긴 산문을 **N턴 함께 작성** → jc-doc-coauthor
- 메일·공지·업데이트 등 **짧은 커뮤니케이션 글** → jc-comms
- '초안 잡아줘'는 양쪽 트리거에 실재 — 분량·독자·문서 유형으로 판별(기획서·Decision Doc=coauthor / 송부 메일·공지=comms).

### 3-5. "아트 · 비주얼"
- **정적** 이미지(.pdf/.png) → jc-visual-philosophy · **코드 생성**(p5.js) → jc-generative-art
- 사진·영상 실사 에셋은 스킬이 아니라 이미지·영상 생성 도구 라우팅 (정본: `jc-design-system/references/shared-rules.md#RULE-VISUAL-ROUTING`).

### 3-6. "리서치 · 분석"
- 외부 데이터 **수집** → mice-market-intel / 수집된 데이터의 **프레임워크 판단** → jc-strategy-canvas
- **입력 문서(RFP) 해체** → mice-rfp-analyzer / **비-MICE 범용 심층 리서치** → 플랫폼 내장 deep-research

### 3-7. "검증 · 감수"
- 완성물·결론 공격 → jc-redteam 단독. 'RFP 검토'는 검증이 아니라 분석 — mice-rfp-analyzer.

## 4. Phase 4 반영 플래그 (CP1 매트릭스 GO 항목 — "[MAIN] Phase 4 완료" 신호 후 최종 확인)

"[MAIN] Phase 4 완료" 신호(2026-07-03 23:14) 확인 후 **2026-07-04 확정본 registry 재생성으로 최종 확정**했다.

| 스킬 | 변경 (CP1 근거) | 확정 상태 (2026-07-04 확정본 registry) | 본 문서 반영 |
|------|---------------|------------------------------|-------------|
| mice-dashboard | 범용 트리거 스코핑 — 내장 data 계열과 충돌 방지 (Major) | ✅ **확정** ("data:build-dashboard·data:create-viz 영역" 배제 문구, v2.0.2) | §2·§3-1 갱신 완료 |
| jc-landing-page | 트리거 동의어 보강 (Minor) | ✅ **확정** ('사전등록 페이지'·'이벤트 신청서'·'뉴스레터 구독 페이지' 추가) | §2 갱신 완료 |
| jc-brand-styling | jc-theme-factory 트리거 중첩 조정 (Minor) | ✅ **확정** ('우리 톤으로 바꿔줘'에 인라인 판별 병기, v1.0.1) | §3-3 기존 판별과 정합 |
| mice-rfp-analyzer | 모드 용어 통일 (Minor) | ✅ **확정** (GO-2 적용, v2.0.1) — 라우팅 영향 없음 | 확인만 |
| jc-artifact-builder | version frontmatter 누락 정정 가능성 | ⚠ **의도된 존치** — 원래 version frontmatter 부재, 가드레일상 신설 금지(jc-landing-page 동일). registry ⚠는 결함 아님, 라우팅 영향 없음 | 재확인 완료 |

## 5. 유지보수

- description이 하나라도 바뀌면: registry 재생성 → diff 확인 → §2·§3 해당 행 갱신 → §4 플래그 정리.
- 신규 스킬 추가 시: §2에 행 추가 + 겹침 발생 시 §3에 판별 추가.
- 본 문서와 registry의 생성 기준일이 다르면 registry가 우선 — 본 문서를 registry에 맞춘다.

## 6. 브리프 게이트 역참조 레이어 (CP-N5, 2026-07-04)

챗 CP-N5 게이트 승인(2026-07-04)에 따라, 라우팅 대상 22종 중 **19종** description 말미에
`실행형 지시는 실행 전 jc-prompt-builder 브리프를 거친다.`(+41자)를 삽입했다 — jc-prompt-builder 선행 게이트의
양방향 선언(레이어 감사 축 F01 후반부). 삽입은 21종 적대 검증(케이스별 의미 충돌 점검) 통과분에 한한다.

**예외 3종 (역참조 미삽입 — 사유 로그)**

| 스킬 | 사유 | 근거 |
|------|------|------|
| jc-strategy-canvas | **한도 초과** — 현행 description 1000자, +41자 시 1041 > 1024 한도 | 실측(description 길이), 챗 Q1=삽입 생략 |
| jc-design-system | **의미 충돌** — 스스로를 "다른 스킬이 참조하는 reference 자산(자동 호출 대상)"으로 규정. 사용자 '실행형 지시'의 직접 대상이 아니므로 게이트 문구가 부정확·오라우팅 | 21종 검증 워크플로우 conflict 판정 |
| jc-redteam | **게이트 명시적 예외** — 완성 산출물 검증은 브리프 생략 '직행' 경로(jc-prompt-builder 정본 카브아웃). 범용 문구는 오독 소지, 한정 문구 삽입 여지 없음(960→한정어 추가 시 한도 근접) | 검증 워크플로우 skip 권고 + 정본 카브아웃 |

- 예외 3종의 관계는 jc-prompt-builder **전방향 선언**(SKILL.md description·§6)이 이미 커버하므로 라우팅 갭 아님.
- Phase 5(CP2) Deep Audit이 예외 재판정 시: 삽입은 append-only라 가역 — 재삽입 후 registry 재생성.
- minor 판정 14종의 개선 제안(문구를 SKILL.md 본문 배치 / '사용자의 실행형 지시' 한정 등)은 Phase 5 감수 입력으로 이월(라우팅 무해, 필수 아님).
