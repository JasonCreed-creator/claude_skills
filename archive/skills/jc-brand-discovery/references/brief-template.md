# Brief Template — 브랜드 정체성 브리프 (`90_brand-brief.md`)

종합 모듈이 산출하는 최종 문서 템플릿. 7모듈을 조정해 **네이밍·슬로건·비주얼 방향**까지 커밋한다. 하류 스킬(jc-visual-philosophy·jc-design-system·jc-theme-factory·jc-landing-page·mice-proposal)이 이 브리프를 브랜드 근거로 브리핑받는다.

> 회사명·실명 하드코딩 금지 — 식별정보는 `{{event_name}}`·`{{client_company}}`·`{{personal_brand}}`·`{{author_name}}` 주입 변수로(`#RULE-NO-COMPANY`). 비주얼은 *방향*까지만, 토큰 hex·폰트 값 금지.

---

## `90_brand-brief.md` 구조

```markdown
# {{event_name}} — 브랜드 정체성 브리프
> 대상 모드: event | 종합일: {ISO-8601} | 참여자: [비식별 슬러그]

## 1. Why (M10)
- 핵심 신념:
- 행동으로서의 How:
- 거부하는 것:

## 2. 포지셔닝 (M20)
> [타깃]이 [상황]할 때, {{event_name}}은 [카테고리]로서 [유니크 가치].
> [대안]과 달리 우리는 [차별점].
- 소유하는 화이트스페이스:

## 3. 타깃 (M30)
- ICP 한 단락 초상:
- 지향 니치:
- 레드플래그/부적합:

## 4. Kapferer 브랜드 아이덴티티 프리즘
| 면 | 내용 |
|---|---|
| Physique (가시·유형 속성) | |
| Personality (사람이라면의 캐릭터) | |
| Culture (배경 가치·원칙) | |
| Relationship (대상과의 관계 방식) | |
| Reflection (대상이 보는 자기 이미지) | |
| Self-image (사용 시 내면 감정) | |

## 4b. 아키타입 & Aaker (M40)
- 주 아키타입 / 그림자:
- 브랜드 연상 3~5:
- 사라지면 잃는 것(브랜드 에쿼티):

## 5. 보이스 & 톤 (M50)
- 보이스 문장 1단락:
- 모든 초안 통과 체크 3:

## 6. 내러티브 (M60)
- 트루라인:
- 스토리 아크 1단락(About/개막사 초안 가능):

## 7. 주최자 ↔ 행사 브랜드 경계 (M70)
- 주최자/개인이 소유:
- 행사/조직이 독립 소유:

## 8. 브랜드 표현 커밋 (상류 → 하류 전달물)
### 8a. 네이밍 후보 (3안, 근거·리스크 병기)
1. · 근거: · 리스크(발음·중의·상표 충돌 의심):
2.
3.
### 8b. 슬로건/태그라인 후보 (3안, register 변주)
1. 2. 3.
### 8c. 비주얼 방향 큐 (방향만 — 값 금지)
- 무드 키워드(3~5):
- 색온도/명도 방향(예: 차갑고 신뢰감 / 따뜻하고 활기): 
- 톤 레퍼런스(느낌의 형용사, 특정 작품 모사 아님):
- 하류 핸드오프: 키비주얼→jc-visual-philosophy · 토큰→jc-design-system · 오버레이→jc-theme-factory

## 9. 긴장 해소 로그
| 긴장 | 모듈 A | 모듈 B | 해소 |
|---|---|---|---|

## 10. 실행 다음 단계 (3~5)
1. 2. 3.
```

---

## ChainPayload/v1 봉투 (선택 — 후속 스킬 체이닝 시)

브리프를 기계 소비(하류 스킬 자동 흡수)하려면 봉투로 감싼다. 봉투 필드 정본은 `jc-design-system/references/chaining-protocol.md` §2~3. 본 스킬은 8종 필수 대상이 아닌 **자율 채택** 생산자다(1차 산출은 사람이 읽는 .md, 봉투는 선택).

```json
{
  "$schema": "ChainPayload/v1",
  "source": "jc-brand-discovery",
  "version": "v1.0.0",
  "generatedAt": "2026-07-12T10:00:00+09:00",
  "target": "jc-visual-philosophy",
  "subjectMode": "event",
  "brandBrief": {
    "why": { "coreBelief": "", "behaviouralHow": "", "refuses": "" },
    "positioning": { "statement": "", "whitespace": "" },
    "icp": { "portrait": "", "niche": "", "redFlag": "" },
    "archetype": { "primary": "", "shadow": "", "associations": [] },
    "voice": { "statement": "", "checks": ["", "", ""] },
    "narrative": { "trueline": "", "storyArc": "" },
    "namingCandidates": [ { "name": "", "rationale": "", "risk": "" } ],
    "sloganCandidates": ["", "", ""],
    "visualDirection": { "moodKeywords": [], "colorTemperature": "", "toneReference": "" }
  }
}
```

- 봉투 필드는 **camelCase**·평탄 구조(페이로드를 별도 `payload` 키로 감싸지 않는다).
- `visualDirection`은 **방향 키워드만** — 구체 hex·폰트 파일명을 넣지 않는다(하류 jc-design-system이 토큰으로 해석).
- 식별정보(`brandName`)가 필요하면 주입 변수 참조로 두고 실명을 봉투에 박지 않는다.
- 최종 브리프는 납품 전 `jc-redteam`으로 슬로건 오탈자·네이밍 리스크·논리 일관성을 점검한다.
