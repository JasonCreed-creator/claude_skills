---
name: jc-strategy-canvas
version: "v1.0.0"
description: MICE 전략가의 전략적 사고를 검증된 프레임워크로 구조화하는 스킬. 신사업 아이템·행사 콘셉트 전략·경쟁 포지셔닝·비즈니스 모델·시장 진입을 6대 프레임워크(비즈니스 모델 캔버스·Porter 5 Forces·SWOT/TOWS·JTBD·포지셔닝·TAM/SAM/SOM)로 펼쳐 채우고, 교차 종합해 전략 권고를 도출하며, jc-redteam 적대 검증을 거쳐 jc 스타일 전략 캔버스(HTML)와 ChainPayload(→mice-proposal/mice-rfp-analyzer)로 산출한다. 다음 상황에서 반드시 이 스킬을 사용할 것 사용자가 '전략', '전략 수립', '비즈니스 모델', 'BM', '비즈니스 모델 캔버스', 'BMC', 'SWOT', 'TOWS', 'Porter', '5 Forces', '다섯 가지 힘', '경쟁 분석', '경쟁 구도', '경쟁 포지셔닝', '포지셔닝', 'JTBD', 'Jobs to be Done', '고객 과업', '시장 규모', 'TAM', 'SAM', 'SOM', '신사업', '신규 사업', '사업 아이템', '사업성 검토', '시장 진입', '시장 매력도', 'GTM 전략', '전략 캔버스', '전략 프레임워크'를 언급할 때. 새 행사·신규 BM·신사업을 구상하며 '전략 짜줘', '프레임워크로 정리해줘', '경쟁 구도 분석해줘', '우리 포지셔닝 잡아줘', '사업성 따져줘', '시장 매력도 봐줘'를 요청할 때. 단, 주어진 RFP·공고를 7축으로 분석하는 것은 mice-rfp-analyzer(입력 종속) 영역, 산문형 전략 메모·기획서를 함께 써 나가는 것은 jc-doc-coauthor, 발주처 제출용 제안서 슬라이드는 mice-proposal, 외부 시장·경쟁 데이터를 리서치로 수집하는 것은 mice-market-intel(본 스킬은 그 데이터를 프레임워크로 구조화·판단하는 상류 사고 도구), 견적은 mice-estimate, 이미 내려진 결론의 적대적 검증만 단독으로 원하면 jc-redteam 영역이므로 그쪽을 쓸 것.
license: Complete terms in LICENSE.txt
---

# jc-strategy-canvas

MICE 전략가의 **전략적 사고를 검증된 프레임워크로 구조화**하는 스킬이다. "막연한 아이디어/상황"을 받아 적합한 프레임워크를 골라 **빈칸을 함께 채우고**, 프레임워크 간 교차 종합으로 **전략 권고**를 뽑고, `jc-redteam` 적대 검증으로 낙관 편향을 친 뒤, jc 스타일 **전략 캔버스(HTML)** + `ChainPayload`로 산출한다.

외부 생태계(`maigentic/stratarts`, MIT)의 전략 프레임워크 *패턴(방법론)*을 흡수해 jc 네이티브로 재구성한 것이다. 파일·코드 복사 없이 프레임워크의 *구조와 질문 세트*만 차용했고, 세 가지를 바꿨다:
1. **MICE 렌즈** — 모든 프레임워크의 예시·질문·함정을 MICE(행사 기획사 신사업·전시/컨퍼런스 BM·발주처 수주 전략·스폰서 시장) 맥락으로 번안. 골격은 `references/framework-catalog.md`.
2. **검증을 `jc-redteam`으로** — stratarts는 "스코어링"으로 자기 검증을 흉내 낸다. jc 생태계엔 18년 경력 외부 감사관 시각의 레드팀이 있으므로 그 자리에 jc-redteam을 끼운다(§4 ⑤). 전략 결론을 *우호적 채점*이 아니라 *적대적 공격*으로 검증한다.
3. **상류 사고 도구로 체이닝** — 산출 `ChainPayload`가 `mice-proposal`·`mice-rfp-analyzer`의 전략 논거로 흘러든다. 입력은 `mice-market-intel`(시장 데이터)·`mice-meeting-minutes`(Discovery)에서 받는다(§7).

## 1. 본 스킬이 다루는 것 / 다루지 않는 것

### 다루는 것 (DO)
- 자사·신사업·신규 행사의 **전략을 0→1로 프레임워크화** — 무엇을 분석할지부터 함께 정한다.
- 6대 프레임워크의 **빈칸을 가이드 질문으로 채우기** (한 번에 다 채우지 않고 미지가 큰 칸부터).
- 프레임워크 **교차 종합** — 예: 5 Forces(시장 매력도) × SWOT(자사 역량) → 진입/회피 판단.
- 전략 결론의 **jc-redteam 적대 검증**(짧은 결론=Quick Strike, 캔버스 전체=Deep Audit).
- jc-design-system 토큰을 입힌 **전략 캔버스 HTML** + 다운스트림용 `ChainPayload` 산출.

### 다루지 않는 것 (DON'T)
- 주어진 **RFP·공고의 7축 분석**(요건·평가·리스크·경쟁·일정·예산·전략권고) → `mice-rfp-analyzer` (입력 종속)
- 산문형 **전략 메모·기획서·의사결정 문서**를 함께 집필 → `jc-doc-coauthor`
- 발주처 제출용 **제안서 슬라이드(PPTX)** → `mice-proposal`
- 외부 **시장·경쟁 데이터를 리서치로 수집** → `mice-market-intel` (본 스킬은 그 데이터를 *구조화·판단*하는 상류)
- **견적·가격 산출** → `mice-estimate` · 발표 대본 → `pt-script`
- 이미 내려진 결론의 **검증만** 단독 요청 → `jc-redteam` 직접

> **mice-rfp-analyzer와의 경계**: rfp-analyzer는 *발주처가 준 RFP*를 분석한다(입력이 외부 문서). 본 스킬은 *자사가 세우는 전략*을 프레임워크로 구조화한다(입력이 자사 상황·질문). 전자는 "이 비딩 어떻게 이길까", 후자는 "이 사업/행사 자체가 맞나·어떻게 포지셔닝하나"다.
>
> **mice-market-intel과의 경계**: market-intel은 *데이터를 모은다*(시장 규모·경쟁사·트렌드를 리서치). 본 스킬은 *데이터로 판단한다*(모인 데이터를 프레임워크에 꽂아 전략을 도출). market-intel → strategy-canvas 순서가 자연스럽다(§7).

## 2. 호출 시점 판단 가이드

| 사용자 입력 | 본 스킬 호출 | 사용 스킬 |
|------------|:-----------:|----------|
| "이 신사업 아이템 사업성 따져줘" | ✅ | jc-strategy-canvas |
| "우리 전시회 BM 캔버스로 정리해줘" | ✅ | jc-strategy-canvas |
| "이 시장 경쟁 구도(5 Forces) 분석" | ✅ | jc-strategy-canvas |
| "우리 행사 포지셔닝 어떻게 잡지" | ✅ | jc-strategy-canvas |
| "이 RFP 평가기준·독소조항 분석" + 공고 | ❌ | mice-rfp-analyzer |
| "이 시장 규모·경쟁사 좀 찾아봐줘" | ❌ | mice-market-intel |
| "전략 메모 산문으로 같이 써줘" | ❌ | jc-doc-coauthor |
| "이 전략 결론 허점 때려줘" | ❌ | jc-redteam |
| "발주처 제안서 PPTX 만들어줘" | ❌ | mice-proposal |

## 3. 6대 프레임워크 — 언제 무엇을

전략 질문의 *유형*에 따라 프레임워크를 고른다. 상세 구조·질문 세트·MICE 렌즈·흔한 함정은 `references/framework-catalog.md`.

| # | 프레임워크 | 답하는 질문 | MICE 적용 예 |
|---|-----------|------------|-------------|
| F1 | **Business Model Canvas** (9블록) | 이 사업은 어떻게 가치를 만들고 돈을 버는가 | 신규 자체행사·유료 컨퍼런스 BM 설계 |
| F2 | **Porter's Five Forces** | 이 시장은 들어갈 만큼 매력적인가 | 신규 전시 분야·지역 진입 매력도 |
| F3 | **SWOT / TOWS** | 자사 역량 × 환경으로 어떤 전략이 나오나 | 수주 전략·신사업 GO/NO-GO 옵션화 |
| F4 | **JTBD** (Jobs-to-be-Done) | 고객(발주처·참가자·스폰서)은 무엇을 해결하려 하나 | 행사 가치제안·참가자 경험 설계 |
| F5 | **Positioning** (A. Dunford) | 경쟁 대안 대비 우리는 무엇으로 다른가 | 행사·기획사 차별화·카테고리 정의 |
| F6 | **TAM/SAM/SOM** + 시장기회 | 이 기회는 얼마나 크고 우리 몫은 얼마인가 | 신사업·신규 행사 시장 규모화 |

> **조합 권장**: 단일 프레임워크는 한쪽 눈이다. 신사업 검토 = F6(규모)→F2(매력도)→F3(역량 매칭)→F1(수익구조). 차별화 = F4(고객 과업)→F5(포지셔닝). 본 스킬은 질문을 듣고 **조합과 순서를 제안**한다.

## 4. 워크플로우

```
① 상황 인테이크   전략 질문·맥락 끌어내기 (무엇을 결정하려 하나)
        ↓         (mice-market-intel / meeting-minutes 입력 있으면 흡수 §7)
② 프레임워크 선택  질문 유형 → 프레임워크 조합·순서 제안 (사용자 확정)
        ↓
③ 가이드 채우기   프레임워크별 핵심 질문으로 빈칸 채움 (미지 큰 칸부터, 5~20 옵션 펼침)
        ↓
④ 교차 종합       프레임워크 간 모순·시너지 → 전략 권고(들) + 트레이드오프
        ↓
⑤ jc-redteam 검증  전략 결론 적대 검증 (낙관편향·숨은가정·논리비약) → 리팩터 루프
        ↓
⑥ 산출            전략 캔버스 HTML (jc 토큰) + ChainPayload(→proposal/rfp) + 사용자 최종책임
```

### ① 상황 인테이크
무엇을 *결정*하려는지부터 묻는다(신사업 GO/NO-GO / 행사 포지셔닝 / BM 설계 / 시장 진입 / 차별화). 약식·자유 덤프 허용. 메타 질문:
1. 어떤 결정을 앞두고 있나? 데드라인·이해관계자는?
2. 대상은? (자체 신규 행사 / 신사업 라인 / 특정 비딩 / 기존 행사 재포지셔닝)
3. 이미 가진 데이터·가설은? (있으면 덤프 — 시장 수치·경쟁사·고객 반응)
4. 성공/실패의 기준은 무엇으로 볼 건가?

> **연동(Integrations) 활용**: `mice-market-intel` 리서치 산출이나 `mice-meeting-minutes` Discovery 회의록이 있으면 `ChainPayload`로 직접 흡수해 ①을 건너뛴다. Slack·Drive 커넥터가 있으면 관련 자료를 끌어온다.

### ② 프레임워크 선택
질문 유형 → §3 표로 **조합·순서를 제안**한다. 사용자가 가감(예: "F2·F3만", "F1 추가"). 모호하면 1회 확인. 과적합 금지 — 결정에 필요한 최소 프레임워크만.

### ③ 가이드 채우기 (프레임워크별 반복)
각 프레임워크를 `framework-catalog.md`의 질문 세트로 채운다:
1. **미지 큰 칸부터** — BMC면 핵심 가치제안·수익원, 5 Forces면 가장 센 힘부터.
2. **브레인스토밍** — 칸마다 5~20개 후보를 *대화로* 펼쳐 빠진 각도를 발굴(캔버스엔 확정분만).
3. **큐레이션** — 남길/뺄/합칠 것을 고른다. 근거 1줄을 청해 다음 칸 우선순위 학습.
4. **증거 표식** — 각 칸 항목에 근거 강도 표식: `[검증]`(데이터 출처 있음) / `[가설]`(미검증) / `[추정]`. 가설·추정은 ⑤에서 집중 공격 대상.

> **추정 금지 원칙**: 데이터가 없으면 숫자를 지어내지 않는다. `[가설]`로 명시하고, 검증이 필요하면 `mice-market-intel`로 보낸다(재발명 금지).

### ④ 교차 종합
채운 프레임워크를 가로질러 본다:
- **모순 탐지** — 예: 5 Forces는 "매력적"인데 SWOT는 "역량 미달" → 진입 조건/선결과제로 정리.
- **시너지** — JTBD의 미충족 과업 ↔ Positioning의 차별화 축 정렬.
- **전략 옵션화** — 단일 답이 아니라 **2~3개 전략 옵션**을 트레이드오프와 함께 제시(공격/방어/관망 등). 각 옵션에 전제·리스크·필요자원.

### ⑤ jc-redteam 적대 검증 ⭐
전략 결론(또는 권고 옵션)을 **`jc-redteam`**에 넘긴다. stratarts식 자기 채점이 아니라 외부 감사관의 적대적 공격으로 친다.
- 짧은 결론형(GO/NO-GO 한 줄, 핵심 권고) → **Quick Strike**.
- 캔버스 전체·옵션 비교 문서 → **Deep Audit**.
- 전략 유형별 집중 공격 포인트(낙관 편향·시장규모 과대·경쟁 과소·역량 자기과신)는 `jc-redteam/references/chaining-guide.md` 매핑 활용. 결함이 걸린 프레임워크 칸으로 **③ 루프 복귀**, Critical·Major부터 교정 후 재검증. `✅결론 유지` 판정까지 반복.

> jc-redteam은 재생성하지 않는다 — 결함 지적·교정·대안까지만. 실제 수정(칸 재작성)은 본 스킬이 ③ 루프로 수행한다.

### ⑥ 산출
검증 통과 후:
- **전략 캔버스 HTML** — 프레임워크별 레이아웃 + jc-design-system SoT 토큰. 스펙은 `references/canvas-output-spec.md`.
- **ChainPayload** — `source: jc-strategy-canvas`, 전략 권고·차별화 축·핵심 메시지를 `mice-proposal`/`mice-rfp-analyzer`로 전달. 스키마는 `references/chaining-schema.md`.
- **사용자 최종 책임 고지** — 전략의 소유자·실행 책임자는 사용자다. 가설·추정 칸을 다시 확인하고, 의도한 의사결정에 실제로 답하는지 검증하라고 알린다.

## 5. 산출물 — 디자인 (SoT 앵커링)

- **토큰 값을 본문/코드에 하드코딩하지 않는다.** 빌드 시 SoT 런타임 참조: `jc-design-system/references/signature-tokens.md §6 JSON`(색·타이포·사이즈·간격). 다크/인쇄는 `mode-mapping.md`.
- 핵심 값(식별용): primary `#0A2540`(Deep Navy)·accent `#2962FF`(Electric Blue)·폰트 Pretendard(한)/Inter(영)/JetBrains Mono(숫자) — **정본은 위 SoT**, 여기 적은 건 식별용일 뿐.
- 클라이언트 차별화가 필요하면 `clientId` 오버레이(`client-overlays.md`, primary/accent/logo 3토큰만).
- 공통 룰: `RULE-WCAG`(본문 4.5:1↑)·`RULE-PRINT-LIGHT`(다크 HTML도 인쇄 시 라이트 강제). 정본 `jc-design-system/references/shared-rules.md`.
- 복합 인터랙티브 캔버스(필터·드릴다운)가 필요하면 `jc-artifact-builder`, 테마/오버레이 적용은 `jc-theme-factory`로 위임.

## 6. RULE-NO-COMPANY (회사·실명 외부 주입)

캔버스·페이로드 어디에도 **특정 회사명·개인 실명·부서명을 하드코딩하지 않는다.** 자사·발주처·경쟁사·파트너는 **외부 주입 변수**로 처리한다.
- 허용: "자사", "발주처", "경쟁사 A/B", `T社`, 일반화 표현 + 변수 슬롯 `{{company_name}}`·`{{client_company}}`·`{{personal_brand}}`·`{{author_name}}`·`{{author_title}}`.
- 정본: `jc-design-system/references/shared-rules.md#RULE-NO-COMPANY`. jc-redteam 검증 시 "회사 종속 표현 0건"을 점검 항목에 포함.

## 7. 생태계 연결

- **입력 체이닝**:
  - `mice-market-intel` → 시장 규모·경쟁사·트렌드 데이터를 F2/F5/F6의 `[검증]` 근거로 흡수.
  - `mice-meeting-minutes` → Discovery 회의록의 고객 니즈·예산·결정사항을 ① 인테이크·F4(JTBD)로 흡수.
  - 봉투: `ChainPayload/v1`(`jc-design-system/references/chaining-protocol.md`).
- **검증(핵심)**: `jc-redteam` — ⑤ 전체. 짧은 결론=Quick Strike, 캔버스=Deep Audit.
- **출력 체이닝**:
  - → `mice-proposal` — 전략 권고·차별화 축·핵심 메시지를 제안서 논거로.
  - → `mice-rfp-analyzer` — 자사 전략 캔버스를 비딩 전략권고(7축 중 전략축)의 사전 입력으로.
  - 스키마: `references/chaining-schema.md`.
- **디자인**: 시각 산출은 `jc-design-system` SoT 런타임 참조. 복합 인터랙티브는 `jc-artifact-builder`, 테마는 `jc-theme-factory`.

## 8. 파일 구조

```
jc-strategy-canvas/
├── SKILL.md                    # 본 파일 — 진입점(워크플로우·판단)
├── LICENSE.txt
└── references/
    ├── framework-catalog.md    # 6대 프레임워크 상세(구조·질문·MICE 렌즈·함정)
    ├── canvas-output-spec.md   # 전략 캔버스 HTML 산출 스펙(프레임워크별 레이아웃 + SoT 토큰)
    └── chaining-schema.md      # ChainPayload in(←market-intel/minutes) / out(→proposal/rfp)
```

## 9. 운영 원칙 / 한계

- **사용자 agency 우선**: 프레임워크 건너뛰기·자유 모드를 항상 허용한다. 프레임워크는 사고를 돕는 도구이지 관문이 아니다 — 건너뛰면 무엇을 잃는지 1줄로만 알린다.
- **추정 금지**: 데이터 없는 숫자는 `[가설]`/`[추정]`으로만 표식. 검증은 `mice-market-intel`에 위임(재발명 금지).
- **최소 프레임워크**: 결정에 필요한 것만. 6개를 다 채우는 건 대개 과적합 신호다.
- **전략은 옵션으로**: 단일 정답이 아니라 트레이드오프 있는 2~3 옵션 + 권고. 결정은 사용자 몫.
- **검증은 위임**: 결론의 견고성은 자체 채점하지 말고 `jc-redteam`으로(④→⑤).
- **본령은 사고 구조화**: 산문 문서가 주가 되면 jc-doc-coauthor, 슬라이드가 주가 되면 mice-proposal로 — 잘못 트리거된 것.

## 10. 버전 히스토리

| 버전 | 일자 | 변경 |
|------|------|------|
| v1.0.0 | 2026-06-04 | 신규 — `maigentic/stratarts`(MIT) 전략 프레임워크 패턴 흡수, jc 네이티브 재구성. 6대 프레임워크(BMC·5 Forces·SWOT/TOWS·JTBD·Positioning·TAM/SAM/SOM) + MICE 렌즈. 검증=jc-redteam, 산출=jc 캔버스 HTML + ChainPayload(→proposal/rfp). references 3종(framework-catalog·canvas-output-spec·chaining-schema). 한국어·푸시형. |
