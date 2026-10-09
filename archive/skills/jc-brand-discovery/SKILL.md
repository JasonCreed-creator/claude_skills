---
name: jc-brand-discovery
description: MICE 행사·개인(Track B)·클라이언트의 브랜드 정체성을 구조화된 다중세션 인터뷰로 발굴하는 스킬. 래더링·5 Whys·투사기법으로 존재이유(Why)·포지셔닝·타깃·성격/아키타입·보이스·내러티브·주최자↔행사 브랜드 경계 8모듈을 파고들어, 행사명·슬로건·비주얼 방향의 상류 전략을 담은 브랜드 정체성 브리프(.md)를 산출한다. 세션 간 state.json 체크포인트로 재개 가능. 다음 상황에서 반드시 이 스킬을 사용할 것 — 사용자가 '브랜드 발굴', '브랜드 정체성', '브랜드 인터뷰', '행사명 짓기', '행사 네이밍', '네이밍', '슬로건', '태그라인', '브랜드 컨셉', '브랜드 방향', '브랜드 브리프', '아이덴티티', '브랜드 성격', '브랜드 보이스', '브랜드 스토리', '브랜드 아키타입', '개인 브랜드', '퍼스널 브랜드', 'Track B 브랜드', 'brand discovery'를 언급할 때. 새 MICE 행사의 이름·슬로건·비주얼 톤을 정하기 전 '브랜드부터 잡자', '정체성 발굴해줘', '인터뷰로 파보자'를 요청할 때, 또는 클라이언트 브랜드를 인터뷰로 정리해달라 할 때. 형제 경계 — 디자인 토큰 값의 정의·수정은 jc-design-system, 결정된 톤/오버레이를 산출물에 입히는 것은 jc-theme-factory, 키비주얼·포스터 아트 제작은 jc-visual-philosophy, BMC·Porter·SWOT 같은 전략 프레임워크로 경쟁 구도·사업성을 분석하는 것은 jc-strategy-canvas(본 스킬은 인터뷰로 브랜드 *정체성을 발굴*하는 상류 발견 작업이 본령), 랜딩페이지 제작은 jc-landing-page 영역이다. 본 스킬의 산출물(브랜드 정체성 브리프)은 이들 스킬의 입력으로 체이닝된다. 실행형 지시는 실행 전 jc-prompt-builder 브리프를 거친다.
version: "v1.0.0"
license: Complete terms in LICENSE.txt
---

# jc-brand-discovery

**구조화된 다중세션 인터뷰로 브랜드의 정체성을 발굴한다.** 원본 ECC `brand-discovery`(8모듈 laddering·5 Whys·projective 인터뷰)의 방법론을 계승하되, **MICE/행사 브랜딩 문맥**으로 번안하고 jc 생태계에 앵커한 버전이다.

> 본 스킬은 *상류 발견 작업*이다. 행사명·슬로건·비주얼 방향 같은 **정체성**을 먼저 인터뷰로 세우면, 하류의 키비주얼(jc-visual-philosophy)·토큰(jc-design-system)·테마(jc-theme-factory)·랜딩(jc-landing-page)·제안서(mice-proposal)가 같은 언어를 공유한다. 산출물은 **브랜드 정체성 브리프**이며, 그것이 이들 스킬의 입력이 된다.

## STEP 0 — 대상 모드 결정

인터뷰 시작 전 어느 대상을 발굴하는지 확정한다. **미지정이면 사용자에게 한 줄로 확인**한다.

| 모드 | 대상 | 대표 상황 | 참여자 |
|------|------|-----------|--------|
| **event** | MICE 행사 브랜드 | 신규 행사의 이름·슬로건·비주얼 톤을 잡기 전 상류 전략 | 발주처·사무국·주최자 |
| **personal** | 개인/Track B 브랜드 | 독립 활동가·전략가 개인 브랜드 정립 | 본인 1인 |
| **client** | 클라이언트 브랜드 | 클라이언트 조직 브랜드를 인터뷰로 정리 | 클라이언트 이해관계자 |

모드는 `state.json`의 `subjectMode`에 기록한다. 모듈 질문·투사기법 예시는 모드에 맞춰 렌즈만 바꾼다(구조는 동일).

## 세션 시작 프로토콜

매 활성화 시, **질문을 던지기 전에** 먼저:

1. **이전 진행 확인.** 프로젝트 brand-identity 디렉터리에서 모듈 파일과 `state.json` 체크포인트를 찾는다. 없으면 신규 시작 — 대상 모드·브랜드/행사명·참여자·저장 경로를 확정하고 첫 모듈부터.
2. **진행 중 모듈 파일을 읽고** Raw 섹션에서 기존 수집 답변을 스캔한다.
3. **사용자에게 2~3문장 보고**: 현재 모듈·상태·남은 것. 그리고 "이어서 진행할까요, 모듈 전환할까요?"

## 인터뷰 규율 (전 모듈 공통)

1. **한 번에 한 질문.** 질문 리스트를 나열하지 않는다.
2. **답변 후:** 짧은 패러프레이즈 → 딥닝 프로브 1개, 또는 포화 시 스레드 종료. 절대 말없이 넘어가지 않는다.
3. **래더링:** 모든 "무엇" 답변에 "그게 왜 중요한가요?"를 붙여 핵심 가치가 드러날 때까지(보통 2~4회).
4. **5 Whys:** 신념·포지셔닝 주장은 표면 선언이 아닌 근본 이유가 나올 때까지 파고든다.
5. **얇은 답변 감지:** 일반론·전문용어·모호함이면 구체 사례·행사 일화·숫자를 하나 요청한다.
6. **투사기법**(모듈당 1회, 정체 돌파용) — MICE 렌즈로 번안:
   - "이 행사가 사람이라면 개막식장에 어떻게 걸어 들어올까요?"
   - 브랜드 부고: "이 행사가 5년 뒤 폐지된다면 참가자들이 그리워할 것은? 못다 한 말은?"
   - 경쟁 대조: "존경하지만 절대 닮고 싶지 않은 경쟁 행사 하나. 무엇이 정확히 잘못된 모델인가요?"
7. **포화 신호:** 연속 2개 프로브가 새 정보를 내지 못하면 요약하고 모듈을 닫는다.
8. **모듈 종료 시** `## Raw`(발언 원문·일화) + `## Synthesis`(해석·후보 3안·미결 질문·참여자 간 모순) 2섹션 모듈 파일을 쓰고 `state.json`을 갱신한다.

## 8모듈 시퀀스 (MICE 번안)

순서대로 진행하되 사용자의 모듈 점프 요청은 존중하고 `state.json`에 스킵을 기록한다. 각 모듈의 프레임워크·Raw 질문·Synthesis 산출은 **[`references/module-guide.md`](references/module-guide.md)** 가 정본.

| 파일 | 모듈 | 프레임워크 | MICE 초점 |
|------|------|-----------|-----------|
| `10_purpose-why.md` | 존재이유 / Why | Sinek Golden Circle · Lencioni | 이 행사/브랜드가 존재하는 이유(창설 신념) |
| `20_positioning.md` | 포지셔닝 | Dunford · Moore | 경쟁 행사·대안 대비 카테고리·차별점 |
| `30_audience-niche.md` | 타깃 & 니치 | Baker · ICP | 참가자·발주처·스폰서·연사의 이상적 프로필 |
| `40_personality-archetype.md` | 성격 & 아키타입 | Mark & Pearson 12원형 · J. Aaker 5차원 | 행사가 사람이라면의 성격·무드 |
| `50_voice-tone.md` | 보이스 & 톤 | 보이스 스펙트럼 · 톤 매트릭스 | 초청장·현장 안내·SNS의 언어 register |
| `60_narrative-story.md` | 내러티브 / 스토리 | Neumeier 트루라인 · 스토리 아크 | 창설 스토리·행사가 여는 변화·초대 |
| `70_owner-tension.md` | 주최자 ↔ 행사 브랜드 경계 | Enns · 개인↔조직 브랜드 스펙트럼 | 주최자/개인 명성과 행사 브랜드의 관계·이양 |
| `90_brand-brief.md` | 브랜드 정체성 브리프(종합) | Kapferer 프리즘 · Aaker 시스템 | 7모듈 종합 → 네이밍·슬로건·비주얼 방향 |

## 상태 관리 프로토콜

모듈이 포화/완료에 이르면 **두 파일**을 쓴다.

- **모듈 파일** `modules/{moduleFile}` — 전체 Raw·Synthesis.
- **`state.json`** — 재개용 경량 체크포인트. `completedModules`·`inProgressModule`·`nextModule`·`lastUpdated` 갱신. 스키마:

```json
{
  "session": "{brand_or_event}-brand-{YYYY-MM}",
  "subjectMode": "event",
  "outputPath": "{brand-identity 디렉터리 절대경로}",
  "completedModules": [],
  "inProgressModule": "10_purpose-why.md",
  "nextModule": "20_positioning.md",
  "participants": ["사무국"],
  "lastUpdated": "{ISO-8601}"
}
```

- **경로/입력 검증(필수):** `moduleFile`은 10~90 열거 시퀀스에만 매칭, `participant`는 영숫자·하이픈만 허용(`/`·`\`·`..`·특수문자 거부), `outputPath`는 프로젝트 내부 절대경로만 허용(상대경로·`..` 탈출 거부).
- **종단 모듈(`90_brand-brief.md`):** 브리프를 쓸 때 `inProgressModule="90_brand-brief.md"`·`nextModule=null`, 완료 후 `completedModules`에 추가하고 `inProgressModule=null`로 되돌린다(남겨두면 다음 세션이 완료본을 진행 중으로 오인). "브랜드 브리프 완료. 전 모듈 저장됨."
- 저장 후 확인: "모듈 X 저장. 상태 갱신. 다음: Y."

## 다중 참여자 모드 (event/client)

발주처·사무국·주최자 등 이해관계자가 둘 이상이면 각자 답변을 `participants/{participant}.md`에 쓰고(위 검증 규칙 적용), 전원이 한 모듈을 마친 뒤 **조정 패스**를 돈다: 수렴·발산을 모듈 파일에 요약하고 "생산적 긴장"을 정렬 워크숍용으로 표시한다. **개인 인터뷰 완료 전 집단 논의 금지**(앵커링 편향).

## 산출물 — 브랜드 정체성 브리프

종합 모듈은 **브랜드 정체성 브리프(.md)** 를 낸다: Why·포지셔닝·타깃 ICP·Kapferer 프리즘·아키타입·보이스·트루라인·주최자↔행사 경계 + **네이밍 후보·슬로건 후보·비주얼 방향 큐**(무드/색온도 키워드). 템플릿은 **[`references/brief-template.md`](references/brief-template.md)** 정본.

- 브리프는 비주얼 *방향*(무드·색온도·키워드)만 담고 **구체 토큰 hex·폰트 값은 담지 않는다** — 그 결정은 jc-design-system·jc-visual-philosophy가 소유한다.
- 후속 스킬 체이닝이 필요하면 `ChainPayload/v1` 봉투(`source: jc-brand-discovery`)로 감싼다. 봉투 정본은 `jc-design-system/references/chaining-protocol.md`. 본 스킬은 8종 필수 대상이 아닌 **자율 채택** 생산자다(브리프는 사람이 읽는 .md가 1차, 봉투는 선택).

## 형제 경계 (본령 재확인)

- **본령** — *인터뷰로 브랜드 정체성을 발굴*하고 그 결과를 브리프로 종합.
- jc-strategy-canvas — BMC·Porter·SWOT·TAM/SAM/SOM으로 **경쟁 구도·사업성**을 분석(정량 전략). 포지셔닝도 여기선 *인터뷰 언어*로 발굴, 정식 경쟁 포지셔닝 분석은 그쪽.
- jc-design-system — 색·타이포 **토큰 값**의 정의/수정. jc-theme-factory — 결정된 톤/오버레이를 산출물에 **적용**. jc-visual-philosophy — **키비주얼/포스터 아트** 제작. jc-landing-page — 랜딩페이지 제작.
- **체이닝:** 브리프 → (visual-philosophy 키비주얼 / theme-factory 오버레이 / design-system 토큰 / landing-page·mice-proposal·mice-sponsor-deck의 브랜드 근거).

## SoT 앵커링 · 공통 룰 (값 재정의 금지 · 정본 위임)

- **토큰 값 하드코딩 금지** — 브리프는 비주얼 *방향*까지만. 색·폰트 값은 `jc-design-system/references/signature-tokens.md`가 정본이며 하류 스킬이 런타임 로드한다.
- **`#RULE-NO-COMPANY`** (`jc-design-system/references/shared-rules.md`) — 회사명·개인 실명·부서명을 브리프·모듈·state에 하드코딩하지 않는다. 발주처·주최자·참여자·클라이언트는 외부 주입 변수(`{{event_name}}`·`{{client_company}}`·`{{personal_brand}}`·`{{author_name}}`)로만. 참여자 식별은 `participant-a` 같은 비식별 슬러그로.
- **`#RULE-WCAG`** — 브리프에 읽혀야 할 카피 샘플(슬로건 시안)을 색과 함께 제시하면 대비 4.5:1↑ 권장(계산 표준 `mode-mapping.md §9`). 방향 큐 자체는 장식이므로 예외.

## 생태계 연결 (재발명 금지)

- **검증** — 완성 브리프(슬로건 오탈자·네이밍 리스크·논리 일관성)의 최종 점검은 `jc-redteam`.
- **데이터 봉투** — 체이닝 시 `ChainPayload/v1`(정본 `chaining-protocol.md`).
- **상류 입력** — 시장·경쟁 데이터는 `mice-market-intel`, Discovery 회의록은 `mice-meeting-minutes`에서 받아 모듈 Raw의 재료로 흡수 가능(식별정보는 배제).

## 안티패턴

- **상태 먼저 읽지 않고 시작.** 매 세션은 모듈 파일·`state.json` 확인으로 연다. 건너뛰면 이전 세션 연속성이 소실된다.
- **한 번에 여러 질문.** 리스트는 체크리스트 답변만 유발한다 — 협상 불가.
- **포화 전 Synthesis 이동.** 마지막 두 프로브가 새 정보를 못 냈으면 종료, 냈으면 아직 아니다.
- **다중 참여자 조정 스킵.** 개인 인터뷰 완료 전 집단 논의는 앵커링 편향.
- **원샷 취급.** 다중세션 설계다. 한 대화에서 브리프까지 몰아치면 얕은 산출.
- **정체성 단계에서 토큰·아트로 침범.** 여기선 *방향*까지. 값·아트는 하류 형제 스킬 소관.

## 파일 구조

```
jc-brand-discovery/
├── SKILL.md                 # 본 파일 — 대상 모드·세션 프로토콜·인터뷰 규율·8모듈·상태·형제 경계
└── references/
    ├── module-guide.md      # 8모듈 상세(프레임워크·Raw 질문·Synthesis 산출, MICE 번안)
    └── brief-template.md    # 브랜드 정체성 브리프 템플릿 + ChainPayload/v1 봉투 예시
```

## 빠른 체크리스트

- [ ] **대상 모드 확정**(event/personal/client) → `state.json.subjectMode`
- [ ] 세션 시작 시 기존 모듈·`state.json` 먼저 읽고 상태 보고
- [ ] 한 번에 한 질문 · 래더링/5 Whys · 모듈당 투사기법 1회 · 포화 시 종료
- [ ] 모듈 종료마다 Raw/Synthesis 파일 + `state.json` 갱신(경로/참여자/모듈 검증)
- [ ] 다중 참여자면 개인 인터뷰 완료 후 조정 패스
- [ ] 브리프에 네이밍·슬로건·비주얼 *방향*까지만(토큰 hex·폰트 값 금지)
- [ ] 회사·개인 식별정보 0건(`#RULE-NO-COMPANY`, 외부 주입 변수)
- [ ] 필요 시 `ChainPayload/v1`로 봉투, 최종 점검 `jc-redteam`

## 변경이력

- v1.0.0 (2026-07-12): CP3 인테이크 — ECC brand-discovery 패턴 기반 신규 저작(8모듈 인터뷰의 MICE 번안). 대상 모드 3종(event/personal/client)·다중세션 state.json 재개·references 2종(module-guide·brief-template). SoT 앵커=jc-design-system, 검증=jc-redteam, 봉투=ChainPayload/v1 자율 채택. 한국어·푸시형 description + 형제 경계(design-system·theme-factory·visual-philosophy·strategy-canvas·landing-page).
