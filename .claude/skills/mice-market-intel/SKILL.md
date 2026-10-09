---
name: mice-market-intel
version: "v1.2.0"
description: "MICE 도메인 특화 시장·경쟁 인텔리전스 스킬. 조사 범위와 아웃라인(항목×필드)을 밝히고 바로 항목별 웹 조사 → 다중 출처 교차확인·티어 부여 → 출처·기준일을 단 근거 리포트로 종합해, 시장 규모·경쟁 구도·산업 동향·발주처/정책·스폰서 풀·벤치마크 행사를 리멤버 웜 페이퍼 리포트와 ChainPayload/v1(→jc-strategy-canvas·mice-rfp-analyzer·jc-pptx)로 산출한다. 다음 상황에서 반드시 이 스킬을 사용할 것 — 사용자가 '시장 조사', '시장 리서치', '마켓 리서치', '시장 규모', '시장 규모 자료', '시장 동향', '산업 동향', '경쟁 구도', '경쟁사 조사·프로파일링', '경쟁사 찾아줘', '벤치마크 행사', '벤치마킹', '외부 벤치마크 행사', '타사 레퍼런스 행사', '스폰서 후보 조사', '발주처 조사', '업계 트렌드', '마켓 인텔리전스', '데스크 리서치', '사전 조사', '거시환경 자료 조사'를 말할 때, 신사업·신규 행사·비딩을 앞두고 '이 시장 좀 조사해줘', '비슷한 행사 사례 모아줘', '시장 규모 자료 찾아줘', '스폰서 될 만한 기업 리스트업'을 요청할 때. 형제 경계 — 모은 데이터로 전략을 판단·구조화하는 것은 jc-strategy-canvas(본 스킬은 수집 상류 — 시장 규모가 얼마인지 찾기, 경쟁사 누구·강약 정리, 거시환경 자료는 본 스킬, 규모 추산 구조(TAM/SAM/SOM)·들어갈 만한가·포지셔닝·PESTLE 구조화는 그쪽), 주어진 RFP·공고 자체의 7축 분석은 mice-rfp-analyzer, 자사 수행실적 레퍼런스 케이스는 mice-aftermath, 행사 KPI 대시보드는 mice-ops-docs, 비-MICE 범용 심층 리서치는 claude.ai 기본 리서치(웹 리서치) 기능."
license: Complete terms in LICENSE.txt
---

# mice-market-intel

MICE 전략가의 **데스크 리서치를 구조화**하는 스킬이다. "이 시장/경쟁/사례 좀 조사해줘"를 받아, **아웃라인을 먼저 설계**하고(무엇을·어떤 필드로 조사할지), 항목별로 **병렬 웹 조사**를 돌리고, **출처·기준일을 단 근거 리포트**로 종합한다. 산출은 리멤버 웜 페이퍼 리포트 + `ChainPayload/v1`로 `jc-strategy-canvas`(프레임워크 근거)·`mice-rfp-analyzer`(경쟁 축)·`jc-pptx`(제안서·소개서 시장 논거)에 흘러든다.

외부 생태계(`Weizhena/Deep-Research-skills`, MIT + `Anjos2/recursive-research` 패턴)의 *2단계 구조화 리서치 방법론*을 흡수해 MICE 맥락으로 재구성한 것이다. 파일·코드 복사 없이 *방법(아웃라인→병렬조사→리포트)* 만 차용했고, 세 가지를 바꿨다:
1. **MICE 도메인 아웃라인** — 조사 대상·필드를 MICE(시장 규모·기획사/앵커 전시 경쟁·발주처/정책·스폰서 풀·벤치마크 행사)에 맞춘 템플릿으로 시작. `references/research-outline-templates.md`.
2. **출처 티어링 + MICE 화이트리스트** — 통계·협회·공신력 우선의 근거 등급. `references/source-tiering.md`. 추정 금지·출처 필수.
3. **체이닝 산출** — 범용 리서치와 달리 `ChainPayload`로 다운스트림 스킬에 *구조화된 근거*를 배출(§6).

## 1. 본 스킬이 다루는 것 / 다루지 않는 것

### 다루는 것 (DO)
- MICE 시장·경쟁·동향·정책·스폰서·벤치마크를 **2단계 구조화 리서치**로 조사.
- 조사 **아웃라인(항목 × 데이터 필드) 설계** → 범위를 밝히고 바로 항목별 웹 조사(대규모만 1회 확인, §2).
- 모든 사실에 **출처(URL·발행처·일자) + 데이터 기준일** 표기, 근거 등급(티어) 부여. 시점에 따라 변하는 수치는 반드시 웹 검색으로 확인한다.
- 리멤버 웜 페이퍼 **리서치 리포트**(Claude Docs 기본 / HTML / md) + 다운스트림용 `ChainPayload/v1` 산출.

### 다루지 않는 것 (DON'T)
- 모은 데이터를 **전략 프레임워크로 판단·구조화**(BMC·5 Forces·SWOT·PESTLE, 규모 추산 구조 TAM/SAM/SOM, 진입 여부·포지셔닝 결정) → `jc-strategy-canvas` (본 스킬은 *수집* 상류)
- 주어진 **RFP·공고의 7축 분석** → `mice-rfp-analyzer` (입력 종속 — 단, 그 `open_questions` 재조사 의뢰는 받는다, §6)
- **자사 수행실적 레퍼런스 케이스** 정리·사례화 → `mice-aftermath` (본 스킬의 벤치마크·레퍼런스 행사는 *외부·타사* 행사)
- 행사 실적 데이터의 **KPI 대시보드·결과 시각화** → `mice-ops-docs` (리서치 수치의 차트는 본 리포트 안에서 직접)
- 범용(비-MICE) 주제의 **심층 리서치** → claude.ai 기본 리서치(웹 리서치) 기능 (본 스킬 미발동)
- 외부 스킬·스크립트를 그대로 실행 → 금지(가드레일). 웹 조사는 안전한 검색·페치 도구로만.

> **claude.ai 기본 리서치 기능과의 경계**: claude.ai 기본 리서치(웹 리서치) 기능은 *어떤 주제든* 받는 범용 리서치다. 본 스킬은 **MICE 도메인 아웃라인 템플릿 + 출처 티어링 + ChainPayload 체이닝**을 얹은 특화판이다. 비-MICE 일반 주제(기술 동향·학술·일반 due diligence)에는 본 스킬을 발동하지 않고 일반 응답·기본 리서치 기능으로 처리한다. 본 스킬은 *MICE 시장/경쟁/사례*에만 트리거.
>
> **jc-strategy-canvas와의 경계**: market-intel은 *데이터를 모은다*. strategy-canvas는 *프레임워크로 판단한다*. 순서는 market-intel → strategy-canvas(§6). 대칭 기준 — "시장 규모 얼마야·찾아줘"는 본 스킬, 규모 추산 구조(TAM/SAM/SOM)는 strategy-canvas / 경쟁사 누구·강약 정리(경쟁 구도·프로파일링)는 본 스킬, 그래서 들어갈 만한가·어디로 포지셔닝하나(5 Forces/SWOT/F5)는 strategy-canvas / 거시환경 자료 조사는 본 스킬, PESTLE 구조화는 strategy-canvas.
>
> **mice-aftermath와의 경계**: 본 스킬의 '벤치마크·레퍼런스 행사'는 *외부·타사* 행사 조사다. 자사가 수행한 행사의 실적 레퍼런스 케이스는 mice-aftermath가 만든다.

## 2. 2단계 리서치 방법론

```
[조사 의뢰]
    ↓
Phase 0  스코프        조사 목적·결정 용도·범위·기준일을 메시지에서 읽고, 없으면 합리적 기본값
    ↓
Phase 1  아웃라인      조사 항목(items) × 데이터 필드(fields) — 범위와 함께 한 블록으로 밝히고 바로 진행
    ↓                  (대규모일 때만 ★1회 확인 / 템플릿: references/research-outline-templates.md)
Phase 2  병렬 심층 조사  항목별 웹 조사, 항목당 다중 출처 교차확인 + 티어·기준일 부여
    ↓                  (출처 등급: references/source-tiering.md)
Phase 3  종합·검증     교차모순 해소·공백 표시 → 근거 리포트 (출처·기준일 필수)
    ↓                  (판단·시사점이 있으면) jc-redteam으로 결론 적대 검증
Phase 4  산출          리포트 + ChainPayload/v1(→strategy-canvas/rfp-analyzer/jc-pptx)
```

> **범위를 밝히고 바로 조사**: 아웃라인을 만들 때마다 멈춰 묻지 않는다. "조사 범위: ○○ 시장 T1+T2, 항목 6 × 필드 5, 기준일 2026-10-05"처럼 범위·아웃라인·고른 기본값을 한 블록으로 밝히고 곧바로 Phase 2에 들어간다. 사용자는 진행 중에도 가감할 수 있고, 조사 중 새 항목 필요가 보이면 추가했다고 알리고 계속한다.
>
> **★ 대규모만 1회 확인**: 다음 중 하나면 착수 전에 아웃라인을 한 번 보여주고 확인받는다 — ① 조사 항목 10개 초과 ② 경쟁사·주체 6곳 이상 심층 프로파일(T7) ③ 서브에이전트 병렬 투입이 필요한 규모 ④ 경쟁사 발굴 진입점에서 후보를 경쟁셋으로 확정할 때. 그 외에는 확인 없이 진행한다.

### Phase 0 — 스코프
무엇에 쓸 리서치인지(신사업 사업성 / 비딩 경쟁 분석 / 스폰서 영업 / 벤치마킹)를 메시지에서 읽는다. 불분명하면 묻지 않고 가장 그럴듯한 용도를 가정해 한 줄로 밝힌다. 기준일 기본값 = 오늘. 용도가 명확하면 다운스트림(jc-strategy-canvas·mice-rfp-analyzer·jc-pptx) 체이닝을 미리 알린다.

### Phase 1 — 아웃라인 설계
조사 유형에 맞는 **항목 × 필드 표**를 `research-outline-templates.md`에서 가져와 짠다. 예(시장 규모): 항목=세그먼트들, 필드=규모·성장률·기준연도·출처·신뢰도. 결정 용도에 필요한 최소 항목만. 대규모 조건(위 ★)에 해당할 때만 확인받는다.

### Phase 2 — 병렬 심층 조사
아웃라인의 **각 항목을 웹 조사**한다(WebSearch/WebFetch). 규약:
- 항목당 **다중 출처 교차확인** — 단일 출처 숫자는 `[단일출처]`로 표식.
- 각 사실에 **출처(URL·발행처·일자) + 티어**(`source-tiering.md`). 1차 통계·협회 > 전문지 > 일반기사 > 블로그.
- **실시간 데이터는 웹 검색 + 기준일 병기**: 시장 규모·성장률·점유율·환율·정책·행사 일정·기업 현황처럼 시점에 따라 바뀌는 값은 학습 지식으로 채우지 않고 반드시 검색으로 확인하며, 데이터 기준 연도와 조사일을 함께 적는다(`RULE-VERSION-FACTS`).
- **추정 금지** — 데이터 없으면 빈칸 + `[미확인]`. 숫자를 지어내지 않는다.
- 대량 항목은 병렬 처리(필요 시 서브에이전트/배치 — 분할·핸드오프는 `jc-session-protocol`, 단순 수집·추출 서브에이전트는 Haiku 4.5, 정리·가공은 Sonnet 5.5). 진행 상황은 짧게 보고하고 확인을 기다리지 않는다.
- **경쟁 조사가 주축이면** `competitive-analysis-method.md`의 3단 방법론(포지셔닝 브리프 우선 티어링 → 9차원 가중 스코어링(긴장축 분리) → 의사결정 지원형 리포트 — 후보 수까지, 우선순위·판단은 jc-strategy-canvas)으로 벼린다. 단일 상대 정면 분석은 `research-outline-templates.md` T7(타깃 주체 심층 프로파일).

### Phase 3 — 종합·검증
- **교차 모순 해소**: 출처 간 상충 수치는 범위로 제시 + 더 높은 티어 우선, 차이 명시.
- **공백 표시**: 못 찾은 항목은 `[미확인]`으로 남기고 후속 조사 경로 제안.
- **jc-redteam 검증**: 리서치 *결론/시사점*(단순 사실 나열이 아니라 "그래서 시장이 매력적" 같은 판단)이 있으면 jc-redteam Quick Strike로 낙관·표본편향을 친다. 사실 나열만이면 생략 가능.

### Phase 4 — 산출
- **리서치 리포트** — 기본 Claude Docs 문서(요청 시 리멤버 웜 페이퍼 HTML 또는 md), 항목별 발견 + 출처 각주 + 신뢰도 + 기준일. 스펙 `references/report-spec.md`.
- **ChainPayload/v1** — `source: mice-market-intel`, 구조화 데이터(시장규모·경쟁사·동향·스폰서후보)를 다운스트림으로. 스키마 `references/chaining-schema.md`.
- **사용자 최종 책임 고지** — 출처를 직접 확인하고, `[단일출처]`/`[미확인]` 항목은 의사결정 전 보강하라고 알린다.

## 3. 산출물 — 디자인 (리멤버 웜 페이퍼, SoT 앵커링)

- **토큰 값 하드코딩 금지.** HTML 리포트를 만들면 `jc-design-system`을 하우스 규약 §2 순서(형제 `parents[2]/jc-design-system` → `~/.claude/skills/jc-design-system` → `~/.claude/skills/synced/*/jc-design-system`)로 찾아 `jc-design-system/scripts/jc_tokens.py`로 `signature-tokens.md §6 JSON`을 읽어 CSS 변수로 주입한다. 다크/인쇄 `mode-mapping.md`.
- 룩: 웜 페이퍼 캔버스·잉크 본문·리멤버 오렌지 액센트, 서체 Pretendard 단일(수치는 `tabular-nums`). 헤더에 리멤버 로고 슬롯(`jc-design-system/assets/remember-black.png`). 구 네이비·일렉트릭블루 룩은 "jc 시그니처" 명시 요청 시 `legacy-jc` 오버레이로만.
- 차트·표·배지는 `jc-design-system/references/component-patterns.md`와 `signature-tokens.md §1.6` 시리즈 순서를 따른다(재발명 금지).
- 공통 룰: `RULE-WCAG`·`RULE-PRINT-LIGHT`·`RULE-VERSION-FACTS`. 정본 `jc-design-system/references/shared-rules.md`.

## 4. RULE-NO-COMPANY (리멤버 명의 기본 + 실명 주입)

발행 명의는 리멤버 MICE비즈팀 기본. *조사 대상*인 외부 경쟁사·발주처·스폰서 후보의 **공개된 회사명은 리서치 사실로서 출처와 함께 기재 가능**하다(공개 정보). 의뢰 고객사·담당자·작성자는 주입 슬롯으로만.
- 슬롯: `{{client_company}}`·`{{event_name}}`·`{{author_name}}`·`{{author_title}}`. 정본 `shared-rules.md#RULE-NO-COMPANY`.
- 금지: 구 소속사 명칭·프로젝트명, 개인 연락처. 조사 대상 기업명은 사실·출처 기반으로만(추측성 평판·미검증 내부정보 금지).

## 5. 표준 워크플로우 (요약)

```
[조사 의뢰] → Phase 0 스코프(기본값 한 줄) → Phase 1 아웃라인(밝히고 진행 · 대규모만 ★1회 확인)
        → Phase 2 병렬 조사(출처·티어·기준일) → Phase 3 종합·검증(모순해소·공백표시·jc-redteam)
        → Phase 4 리포트 + ChainPayload/v1
[사용자 최종 출처 확인]
```

## 6. 생태계 연결

- **출력 체이닝(핵심)**:
  - → `jc-strategy-canvas` — 시장규모·경쟁사·동향을 F2/F5/F6의 `[검증]` 근거로.
  - → `mice-rfp-analyzer` — 경쟁사·시장 데이터를 7축 중 경쟁·전략권고 축 사전 근거로.
  - → `jc-pptx` — 시장 논거·트렌드·벤치마크를 제안서 배경 슬라이드로, 스폰서 후보·산업 분포를 스폰서 제안서·소개서로.
  - 봉투 `ChainPayload/v1` — 정본 `jc-design-system/references/chaining-protocol.md`(§1 봉투 · §3 enum · §6 수신 규칙).
- **입력(재조사 의뢰)**: `mice-rfp-analyzer`의 `open_questions`(발주처 이력 → T4 발주처/정책 환경, 비딩 맞수 → T7 타깃 주체 심층 프로파일)와 `jc-strategy-canvas`의 `open_questions`(미검증 칸)를 Phase 1 아웃라인 시드로 받는다. 결과는 요청한 스킬로 회신 봉투를 낸다(`references/chaining-schema.md` §1).
- **검증**: `jc-redteam` — 리서치 *결론/시사점*의 낙관·표본편향(Phase 3).
- **세션**: 대규모 병렬 조사의 분할·서브에이전트 운용은 `jc-session-protocol`.
- **범용 위임**: 비-MICE 주제는 claude.ai 기본 리서치(웹 리서치) 기능. 본 스킬은 그 위에 MICE 구조를 얹는다(재발명 금지).
- **디자인**: `jc-design-system` SoT 런타임 참조(§3).

## 7. 파일 구조

```
mice-market-intel/
├── SKILL.md                       # 본 파일 — 진입점
├── LICENSE.txt
└── references/
    ├── research-outline-templates.md  # MICE 조사 유형별 항목×필드 템플릿(T1~T7 + 진입점)
    ├── competitive-analysis-method.md # 경쟁 조사 3단 방법론(티어링→9차원 스코어링→의사결정 지원 리포트)
    ├── source-tiering.md              # 출처 신뢰도 등급 + MICE 화이트리스트
    ├── report-spec.md                 # 리서치 리포트 레이아웃·인용·SoT 토큰
    └── chaining-schema.md             # ChainPayload/v1 in(←open_questions) / out(→strategy-canvas/rfp-analyzer/jc-pptx)
```

## 8. 운영 원칙 / 한계

- **아웃라인 먼저, 조사 바로**: 아웃라인은 항상 짜되, 밝히고 곧장 조사한다. 확인은 대규모일 때 1회뿐.
- **실시간 데이터는 검색으로**: 시점 민감 수치는 웹 검색으로 확인하고 기준일을 병기한다. 학습 지식으로 최신 수치를 대신하지 않는다.
- **추정 금지·출처 필수**: 모든 수치에 출처·티어. 없으면 `[미확인]`. 단일 출처는 표식.
- **수집과 판단 분리**: 전략적 판단(매력도·진입여부)은 `jc-strategy-canvas`로. 본 스킬은 근거를 *댄다*.
- **공개 정보만**: 비공개·미검증 내부정보·추측성 평판은 다루지 않는다.
- **범용 리서치 재발명 금지**: 비-MICE는 claude.ai 기본 리서치(웹 리서치) 기능 몫.
- **본령은 MICE 데스크 리서치**: 행사 KPI 대시보드가 주가 되면 mice-ops-docs, 프레임워크 판단이 주가 되면 jc-strategy-canvas로 — 잘못 트리거.

## 9. 버전 히스토리

| 버전 | 일자 | 변경 |
|------|------|------|
| v1.0.0 | 2026-06-04 | 신규 — `Weizhena/Deep-Research-skills`(MIT)·`Anjos2/recursive-research` 2단계 구조화 리서치 패턴 흡수, MICE 네이티브 재구성. Phase 0~4 + HITL 정지점. 출처 티어링·추정금지. 산출=jc 리포트 + ChainPayload(→strategy-canvas/rfp/proposal/sponsor). references 4종. 한국어·푸시형. |
| v1.0.1 | (미상) | 중간 버전 — 세부 변경 기록 부재(frontmatter만 존재). CP2에서 이력 계보 완결 위해 행 백필. |
| v1.0.2 | 2026-07-03 | Fable-정합 감사 후속 조치 — `chaining-schema.md` ChainPayload 예시 버전 표기를 SKILL.md와 정합화(v1.0.0→v1.0.2). T2 경쟁 구도 템플릿에 "미방어 세그먼트 탐지" 분석 렌즈 보강(경쟁사 포지셔닝 벤치마크 패턴 흡수). + description 말미 jc-prompt-builder 브리프 게이트 역참조 삽입(CP-N5). |
| v1.0.3 | 2026-07-04 | CP2 조치 — v1.0.1 이력 행 백필(계보 완결), v1.0.2 변경 서술에 back-ref 반영 명시. |
| v1.0.4 | 2026-07-12 | CP3 인테이크 — CP1 GO-4 잔여(company-intel 7렌즈+4진입점) 흡수 + ECC 경쟁분석 3종 패턴(티어링·9차원 스코어링·의사결정 리포트) 보강. `research-outline-templates.md`에 T7 타깃 주체 심층 프로파일 + 진입점 4종(단일주체/산업·세그먼트/지정경쟁셋/경쟁사발굴) 신설, `competitive-analysis-method.md` 신규 reference 추가. |

## 변경 이력

- v1.2.0 (2026-10-09): 트리거 정리 — '경쟁 구도'·'경쟁사 조사·프로파일링'·'거시환경 자료 조사'·'외부 벤치마크/타사 레퍼런스 행사'로 한정, jc-strategy-canvas(규모·경쟁·PESTLE)·mice-aftermath(자사 실적 케이스)와 대칭 경계, `deep-research` 표기를 claude.ai 기본 리서치 기능으로. §2 호출표 삭제·§ 번호 재정렬.
  경쟁 방법론 '전략 권고'를 후보 수(`whitespace_candidates`)로 격하, 페이로드에 `competitor_tier`·`scores`·`tension_axes`·`whitespace_candidates` 추가·출처 티어 `source_tier`로 개명, rfp-analyzer `open_questions` 재조사 입력 정의.
- v1.1.0 (2026-10-05): 아웃라인마다 멈추던 확인(HITL) → "범위를 밝히고 바로 조사, 대규모(항목 10개 초과·6곳 이상 심층·병렬 투입·경쟁셋 확정)만 1회 확인". 실시간 데이터는 웹 검색·기준일 병기 원칙 명문화. 룩을 리멤버 웜 페이퍼·Pretendard로, 폐합 스킬 라우팅을 jc-pptx·mice-ops-docs로 정리하고 실행 전 브리프 게이트 문구 삭제.
