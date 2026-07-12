---
name: mice-market-intel
version: "v1.0.4"
description: MICE 도메인 특화 시장·경쟁 인텔리전스 스킬. 2단계 구조화 리서치(아웃라인 설계 → 항목별 병렬 웹 조사 → 근거 종합 리포트)로 시장 규모·경쟁 구도·산업 동향·발주처/정책·스폰서 풀·벤치마크 행사를 출처 표기와 함께 조사하고, jc 스타일 리서치 리포트 + ChainPayload(→jc-strategy-canvas/mice-rfp-analyzer/mice-proposal)로 산출한다. 다음 상황에서 반드시 이 스킬을 사용할 것 사용자가 '시장 조사', '시장 리서치', '마켓 리서치', '시장 규모', '시장 동향', '산업 동향', '경쟁사 조사', '경쟁사 분석', '경쟁 조사', '경쟁사 찾아줘', '벤치마크 행사', '벤치마킹', '레퍼런스 행사', '스폰서 후보 조사', '발주처 조사', '업계 트렌드', '시장 인텔', '마켓 인텔리전스', '데스크 리서치', 'desk research', '사전 조사', '환경 분석'을 언급할 때. 신사업·신규 행사·비딩을 앞두고 '이 시장 좀 조사해줘', '경쟁사 누구 있는지 찾아줘', '비슷한 행사 사례 모아줘', '시장 규모 자료 찾아줘', '스폰서 될 만한 기업 리스트업'을 요청할 때. 2단계 사이에 사용자 확인(human-in-the-loop)을 둔다. 단, 모은 데이터를 전략 프레임워크로 *판단·구조화*하는 것은 jc-strategy-canvas(본 스킬은 데이터를 *수집*하는 상류), 주어진 RFP·공고 자체를 7축 분석하는 것은 mice-rfp-analyzer(입력 종속), 이미 가진 데이터를 차트·KPI로 시각화하는 것은 mice-dashboard, 범용(비-MICE) 주제의 심층 리서치는 built-in deep-research 영역이므로 그쪽을 쓸 것. 실행형 지시는 실행 전 jc-prompt-builder 브리프를 거친다.
license: Complete terms in LICENSE.txt
---

# mice-market-intel

MICE 전략가의 **데스크 리서치를 구조화**하는 스킬이다. "이 시장/경쟁/사례 좀 조사해줘"를 받아, **아웃라인을 먼저 설계**하고(무엇을·어떤 필드로 조사할지), 항목별로 **병렬 웹 조사**를 돌리고, **출처를 단 근거 리포트**로 종합한다. 산출은 jc 스타일 리포트 + `ChainPayload`로 `jc-strategy-canvas`(프레임워크 근거)·`mice-rfp-analyzer`(경쟁 축)·`mice-proposal`(시장 논거)에 흘러든다.

외부 생태계(`Weizhena/Deep-Research-skills`, MIT + `Anjos2/recursive-research` 패턴)의 *2단계 구조화 리서치 방법론*을 흡수해 MICE 네이티브로 재구성한 것이다. 파일·코드 복사 없이 *방법(아웃라인→병렬조사→리포트 + human-in-the-loop)* 만 차용했고, 세 가지를 바꿨다:
1. **MICE 도메인 아웃라인** — 조사 대상·필드를 MICE(시장 규모·기획사/앵커 전시 경쟁·발주처/정책·스폰서 풀·벤치마크 행사)에 맞춘 템플릿으로 시작. `references/research-outline-templates.md`.
2. **출처 티어링 + MICE 화이트리스트** — 통계·협회·공신력 우선의 근거 등급. `references/source-tiering.md`. 추정 금지·출처 필수.
3. **체이닝 산출** — 범용 리서치와 달리 `ChainPayload`로 다운스트림 스킬에 *구조화된 근거*를 배출(§7).

## 1. 본 스킬이 다루는 것 / 다루지 않는 것

### 다루는 것 (DO)
- MICE 시장·경쟁·동향·정책·스폰서·벤치마크를 **2단계 구조화 리서치**로 조사.
- 조사 **아웃라인(항목 × 데이터 필드) 설계** → 사용자 확인 → 항목별 병렬 웹 조사.
- 모든 사실에 **출처(URL·발행처·일자)** 표기, 근거 등급(티어) 부여.
- jc 스타일 **리서치 리포트**(HTML/md) + 다운스트림용 `ChainPayload` 산출.

### 다루지 않는 것 (DON'T)
- 모은 데이터를 **전략 프레임워크로 판단·구조화**(BMC·5 Forces·SWOT) → `jc-strategy-canvas` (본 스킬은 *수집* 상류)
- 주어진 **RFP·공고의 7축 분석** → `mice-rfp-analyzer` (입력 종속)
- 이미 가진 데이터를 **차트·KPI 대시보드로 시각화** → `mice-dashboard`
- 범용(비-MICE) 주제의 **심층 리서치** → built-in `deep-research` (범용 하니스)
- 외부 스킬·스크립트를 그대로 실행 → 금지(가드레일). 웹 조사는 안전한 검색·페치 도구로만.

> **built-in deep-research와의 경계**: deep-research는 *어떤 주제든* 받는 범용 리서치 하니스다. 본 스킬은 **MICE 도메인 아웃라인 템플릿 + 출처 티어링 + ChainPayload 체이닝**을 얹은 특화판이다. 비-MICE 일반 주제(기술 동향·학술·일반 due diligence)는 deep-research로 보낸다. 본 스킬은 *MICE 시장/경쟁/사례*에만 트리거.
>
> **jc-strategy-canvas와의 경계**: market-intel은 *데이터를 모은다*. strategy-canvas는 *프레임워크로 판단한다*. 순서는 market-intel → strategy-canvas(§7). "경쟁사 누구 있나"는 본 스킬, "그래서 우리가 이길 수 있나(5 Forces/SWOT)"는 strategy-canvas.

## 2. 호출 시점 판단 가이드

| 사용자 입력 | 본 스킬 호출 | 사용 스킬 |
|------------|:-----------:|----------|
| "이 전시 시장 규모·경쟁사 조사해줘" | ✅ | mice-market-intel |
| "비슷한 컨퍼런스 벤치마크 사례 모아줘" | ✅ | mice-market-intel |
| "스폰서 될 만한 기업 리스트업해줘" | ✅ | mice-market-intel |
| "이 시장 우리가 들어갈 만한지 판단(5 Forces)" | ❌ | jc-strategy-canvas |
| "이 RFP 평가기준 분석" + 공고 | ❌ | mice-rfp-analyzer |
| "이 실적 데이터 차트로" | ❌ | mice-dashboard |
| "양자컴퓨팅 기술 동향 리서치" (비-MICE) | ❌ | deep-research |

## 3. 2단계 리서치 방법론

```
[조사 의뢰]
    ↓
Phase 0  스코프 합의   조사 목적·결정용도·범위·기한 (무엇에 쓸 리서치인가)
    ↓
Phase 1  아웃라인 설계  조사 항목(items) × 데이터 필드(fields) 초안 → 사용자 확인 ★HITL
    ↓                  (템플릿: references/research-outline-templates.md)
Phase 2  병렬 심층 조사  항목별 웹 조사, 항목당 다중 출처 교차확인 + 티어 부여
    ↓                  (출처 등급: references/source-tiering.md)
Phase 3  종합·검증     교차모순 해소·공백 표시 → 근거 리포트 (출처 표기 필수)
    ↓                  (선택) jc-redteam으로 결론·추정 적대 검증
Phase 4  산출          jc 리포트(HTML/md) + ChainPayload(→strategy-canvas/rfp/proposal)
```

> **★ Human-in-the-loop (필수 정지점)**: Phase 1 아웃라인을 **사용자가 확인/가감**하기 전에 Phase 2 조사를 시작하지 않는다. 잘못된 아웃라인으로 조사하면 비용만 늘고 결론이 헛다리다. 조사 도중 새 항목 필요가 보이면 아웃라인에 추가 제안 후 진행.

### Phase 0 — 스코프 합의
무엇에 쓸 리서치인지부터 묻는다(신사업 사업성 / 비딩 경쟁 분석 / 스폰서 영업 / 벤치마킹). 결정 용도가 정해지면 깊이·범위·기한을 합의. 용도가 명확하면 다운스트림(strategy-canvas·rfp·sponsor-deck) 체이닝을 미리 알린다.

### Phase 1 — 아웃라인 설계 (HITL)
조사 유형에 맞는 **항목 × 필드 표**를 `research-outline-templates.md`에서 가져와 초안. 예(시장 규모): 항목=세그먼트들, 필드=규모·성장률·출처·신뢰도. 사용자가 항목/필드를 가감·확정. 모호하면 1회 확인.

### Phase 2 — 병렬 심층 조사
확정 아웃라인의 **각 항목을 웹 조사**한다(WebSearch/WebFetch). 규약:
- 항목당 **다중 출처 교차확인** — 단일 출처 숫자는 `[단일출처]`로 표식.
- 각 사실에 **출처(URL·발행처·일자) + 티어**(`source-tiering.md`). 1차 통계·협회 > 전문지 > 일반기사 > 블로그.
- **추정 금지** — 데이터 없으면 빈칸 + `[미확인]`. 숫자를 지어내지 않는다.
- 대량 항목은 병렬 처리(필요 시 서브에이전트/배치). 진행 상황을 사용자에게 짧게 보고.
- **경쟁 조사가 주축이면** `competitive-analysis-method.md`의 3단 방법론(포지셔닝 브리프 우선 티어링 → 9차원 가중 스코어링(긴장축 분리) → 의사결정형 리포트)으로 벼린다. 단일 상대 정면 분석은 `research-outline-templates.md` T7(타깃 주체 심층 프로파일).

### Phase 3 — 종합·검증
- **교차 모순 해소**: 출처 간 상충 수치는 범위로 제시 + 더 높은 티어 우선, 차이 명시.
- **공백 표시**: 못 찾은 항목은 `[미확인]`으로 남기고 후속 조사 경로 제안.
- (선택) **jc-redteam 검증**: 리서치 *결론/시사점*(단순 사실 나열이 아니라 "그래서 시장이 매력적" 같은 판단)이 있으면 jc-redteam Quick Strike로 낙관·표본편향을 친다.

### Phase 4 — 산출
- **리서치 리포트** — jc 스타일(HTML/md), 항목별 발견 + 출처 각주 + 신뢰도. 스펙 `references/report-spec.md`.
- **ChainPayload** — `source: mice-market-intel`, 구조화 데이터(시장규모·경쟁사·동향·스폰서후보)를 다운스트림으로. 스키마 `references/chaining-schema.md`.
- **사용자 최종 책임 고지** — 출처를 직접 확인하고, `[단일출처]`/`[미확인]` 항목은 의사결정 전 보강하라고 알린다.

## 4. 산출물 — 디자인 (SoT 앵커링)

- **토큰 값 하드코딩 금지.** SoT 런타임 참조: `jc-design-system/references/signature-tokens.md §6 JSON`. 다크/인쇄 `mode-mapping.md`.
- 핵심 값(식별용): primary `#0A2540`·accent `#2962FF`·폰트 Pretendard/Inter/JetBrains Mono(숫자·수치) — 정본은 SoT.
- 차트가 필요하면 `mice-dashboard/references/chart-guide.md` 토큰 매핑 차용(재발명 금지).
- 공통 룰: `RULE-WCAG`·`RULE-PRINT-LIGHT`. 정본 `jc-design-system/references/shared-rules.md`. 본 스킬은 디자인 소비 스킬이므로 `jc-design-system/references/shared-rules.md`·`signature-tokens.md` 정본 대조 준수.

## 5. RULE-NO-COMPANY (회사·실명 외부 주입)

리포트·페이로드에 **자사명·개인 실명·부서명을 하드코딩하지 않는다.** 단, *조사 대상*인 외부 경쟁사·발주처·스폰서 후보의 **공개된 회사명은 리서치 사실로서 출처와 함께 기재 가능**하다(공개 정보). 자사·발행자 식별만 변수 처리.
- 자사 슬롯: `{{company_name}}`·`{{personal_brand}}`·`{{author_name}}`·`{{author_title}}`. 정본 `shared-rules.md#RULE-NO-COMPANY`.
- 조사 대상 기업명은 사실·출처 기반으로만(추측성 평판·미검증 내부정보 금지).

## 6. 표준 워크플로우 (요약)

```
[조사 의뢰] → Phase 0 스코프 → Phase 1 아웃라인(★사용자 확인) → Phase 2 병렬 조사(출처·티어)
        → Phase 3 종합·검증(모순해소·공백표시·선택 jc-redteam) → Phase 4 리포트 + ChainPayload
[사용자 최종 출처 확인]
```

## 7. 생태계 연결

- **출력 체이닝(핵심)**:
  - → `jc-strategy-canvas` — 시장규모·경쟁사·동향을 F2/F5/F6의 `[검증]` 근거로.
  - → `mice-rfp-analyzer` — 경쟁사·시장 데이터를 7축 중 경쟁·전략권고 축 사전 근거로.
  - → `mice-proposal` — 시장 논거·트렌드를 제안서 배경 슬라이드로.
  - → `mice-sponsor-deck` — 스폰서 후보 리스트·산업 분포를.
  - 봉투 `ChainPayload/v1`(`jc-design-system/references/chaining-protocol.md`).
- **검증(선택)**: `jc-redteam` — 리서치 *결론/시사점*의 낙관·표본편향(Phase 3).
- **범용 위임**: 비-MICE 주제는 built-in `deep-research`. 본 스킬은 그 위에 MICE 구조를 얹는다(재발명 금지 — 일반 리서치 엔진을 다시 만들지 않는다).
- **디자인**: 리포트 시각화는 `jc-design-system` SoT, 차트는 `mice-dashboard` 패턴.

## 8. 파일 구조

```
mice-market-intel/
├── SKILL.md                       # 본 파일 — 진입점
├── LICENSE.txt
└── references/
    ├── research-outline-templates.md  # MICE 조사 유형별 항목×필드 템플릿(T1~T7 + 진입점)
    ├── competitive-analysis-method.md # 경쟁 조사 3단 방법론(티어링→9차원 스코어링→의사결정 리포트)
    ├── source-tiering.md              # 출처 신뢰도 등급 + MICE 화이트리스트
    ├── report-spec.md                 # 리서치 리포트 레이아웃·인용·SoT 토큰
    └── chaining-schema.md             # ChainPayload out(→strategy-canvas/rfp/proposal/sponsor)
```

## 9. 운영 원칙 / 한계

- **아웃라인 먼저, 조사 나중**: HITL 정지점(Phase 1)을 건너뛰지 않는다.
- **추정 금지·출처 필수**: 모든 수치에 출처·티어. 없으면 `[미확인]`. 단일 출처는 표식.
- **수집과 판단 분리**: 전략적 판단(매력도·진입여부)은 `jc-strategy-canvas`로. 본 스킬은 근거를 *댄다*.
- **공개 정보만**: 비공개·미검증 내부정보·추측성 평판은 다루지 않는다.
- **범용 리서치 재발명 금지**: 비-MICE는 deep-research 위임.
- **본령은 MICE 데스크 리서치**: 차트 시각화가 주가 되면 mice-dashboard, 프레임워크 판단이 주가 되면 jc-strategy-canvas로 — 잘못 트리거.

## 10. 버전 히스토리

| 버전 | 일자 | 변경 |
|------|------|------|
| v1.0.0 | 2026-06-04 | 신규 — `Weizhena/Deep-Research-skills`(MIT)·`Anjos2/recursive-research` 2단계 구조화 리서치 패턴 흡수, MICE 네이티브 재구성. Phase 0~4 + HITL 정지점. 출처 티어링·추정금지. 산출=jc 리포트 + ChainPayload(→strategy-canvas/rfp/proposal/sponsor). references 4종. 한국어·푸시형. |
| v1.0.1 | (미상) | 중간 버전 — 세부 변경 기록 부재(frontmatter만 존재). CP2에서 이력 계보 완결 위해 행 백필. |
| v1.0.2 | 2026-07-03 | Fable-정합 감사 후속 조치 — `chaining-schema.md` ChainPayload 예시 버전 표기를 SKILL.md와 정합화(v1.0.0→v1.0.2). T2 경쟁 구도 템플릿에 "미방어 세그먼트 탐지" 분석 렌즈 보강(경쟁사 포지셔닝 벤치마크 패턴 흡수). + description 말미 jc-prompt-builder 브리프 게이트 역참조 삽입(CP-N5). |
| v1.0.3 | 2026-07-04 | CP2 조치 — v1.0.1 이력 행 백필(계보 완결), v1.0.2 변경 서술에 back-ref 반영 명시. |
| v1.0.4 | 2026-07-12 | CP3 인테이크 — CP1 GO-4 잔여(company-intel 7렌즈+4진입점) 흡수 + ECC 경쟁분석 3종 패턴(티어링·9차원 스코어링·의사결정 리포트) 보강. `research-outline-templates.md`에 T7 타깃 주체 심층 프로파일 + 진입점 4종(단일주체/산업·세그먼트/지정경쟁셋/경쟁사발굴) 신설, `competitive-analysis-method.md` 신규 reference 추가. |
