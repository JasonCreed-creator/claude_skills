# Chaining Guide — ChainPayload/v1 출력 매핑 + 워크플로우 체이닝

mice-rfp-analyzer 산출물을 다른 스킬로 전달할 때의 데이터 매핑 규칙. 봉투 정본은 `jc-design-system/references/chaining-protocol.md`(ChainPayload/v1), 본 문서는 **본 스킬 고유 페이로드**만 정의한다.

---

## 1. 워크플로우 체인 (전체 그림)

```
[RFP 원문 파일]   ← (선택) jc-strategy-canvas 전략 캔버스 · mice-market-intel 발주처/경쟁 리서치
    ↓ 분석
[mice-rfp-analyzer]
    ├── rfp-analysis-report.docx     (의사결정용)
    ├── rfp-evaluation-matrix.xlsx   (실무용)
    ├── ChainPayload/v1 JSON         (후속 스킬 입력 — target별 봉투)
    └── open_questions ──→ mice-market-intel (T4 발주처 · T7 맞수 재조사, §3-2)
    ↓ GO 판정 시
[jc-pptx]          제안서 PPTX
    ↓ 제안 확정 시
[mice-estimate]    견적서 xlsx
    ↓ 발표 준비 (jc-pptx 덱을 입력으로)
[pt-script]        발표 대본
    ↓ 행사 종료 후
[mice-aftermath]   결과 보고 (분석 정확도 회고)
모든 산출물 ──→ jc-redteam (적대 검증)
```

→ 본 스킬은 워크플로우의 **시작점**. 후속 스킬에 양질의 입력을 전달하는 것이 핵심 기능.

---

## 2. jc-pptx 입력 매핑 (가장 중요)

GO 판정 시, 분석 결과를 다음 구조로 변환해 jc-pptx(제안서 모드)에 전달한다. jc-pptx는 이 페이로드가 있으면 RFP를 재분석하지 않는다(`jc-pptx/references/proposal-playbook.md` Full 모드).

### 2-1. 매핑 테이블

| analyzer 산출 데이터 | 제안서 활용 영역 |
|---------------------|-------------------|
| 1축 / 필수 요건 리스트 | 제안서 본문 / 운영 계획 섹션 |
| 1축 / 가산 요건 | 제안서 / 차별화 부록 |
| 2축 / 평가 기준 + 가중치 | 제안서 / 섹션 분량 비율 결정 |
| 2축 / 우리 강점 영역 | 제안서 / 표지·도입부·결론 강조 메시지 |
| 3축 / 리스크 상 등급 | 제안서 / 협상 포인트 (본문에 명시 X) |
| 4축 / 차별화 포인트 | 제안서 / 핵심 메시지 |
| 6축 / 입찰가 권고 | 제안서 / 가격 섹션 (금액은 mice-estimate 전용 봉투로, §3-1) |
| 7축 / 판정·판정 근거 | 제안서 방향 설정 (내부용, 제안서 미포함) |
| 7축 / 핵심 메시지 Top 3 | 제안서 표지 / Executive Summary |
| 7축 / 승률 추정 | 자원 투입 강도 결정 (내부용, 제안서 미포함) |

### 2-2. ChainPayload/v1 표준 형식

봉투 필드(`$schema`·`source`·`version`·`generatedAt`·`target`·`clientId`·`projectTitle`)와 페이로드 필드가 **같은 최상위에 평탄하게** 공존한다. `version`은 이 스킬 SKILL.md frontmatter의 현재 버전을 그대로 쓴다(예시에 고정값을 적지 않는다).

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-rfp-analyzer",
  "version": "<SKILL.md frontmatter version>",
  "generatedAt": "YYYY-MM-DDTHH:MM:SS+09:00",
  "target": "jc-pptx",
  "clientId": null,
  "projectTitle": "{{event_name}}",

  "rfp_meta": {
    "client": "{{client_company}}",
    "rfp_id": "{{공고번호 또는 null}}",
    "event_name": "{{event_name}}",
    "event_date": "YYYY-MM-DD",
    "event_venue": "{{venue}}",
    "event_scale": "[규모 — 원문 표기 그대로]",
    "budget_announced": 0,
    "submission_deadline": "YYYY-MM-DD"
  },
  "analysis_result": {
    "judgment": "GO",
    "judgment_basis": [
      "NO-GO 강제 조건 0건 — 필수×불가 0 · 치명 독소 0 · 원가<발주가 · 일정 가능",
      "승부 메시지 실재 — 배점 상위 항목(p.X)과 STRONG 요건이 겹침",
      "불리 요인 — (예) 지역 가산점 미충족"
    ],
    "go_conditions": [],
    "estimated_winrate": 0.45,
    "core_messages": ["메시지 1", "메시지 2", "메시지 3"]
  },
  "requirements": {
    "mandatory": [
      {"item": "...", "source": "p.X 조항 Y", "our_capability": "가능"}
    ],
    "optional": [],
    "bonus": []
  },
  "evaluation_focus": [
    {"category": "...", "weight": 0.30, "our_strength": true}
  ],
  "differentiation_points": ["차별 포인트 1", "차별 포인트 2"],
  "proposal_structure_hint": {
    "page_allocation": {
      "executive_summary": 1, "requirement_response": 8, "operation_plan": 12,
      "differentiation": 4, "team_qualification": 3, "budget": 2
    },
    "emphasis_sections": ["operation_plan", "differentiation"]
  },
  "risk_notes_for_negotiation": ["리스크 상 등급 항목 (제안서 미포함, 협상 포인트)"],
  "open_questions": [
    {"item": "가산점 항목 평가 방식(절대/상대)", "type": "client_query", "source": "p.7 6조"},
    {"item": "발주처 최근 3년 동일 행사 수행사", "type": "client_history", "route": "mice-market-intel T4"},
    {"item": "예상 맞수 B사의 유사 실적 규모", "type": "competitor", "route": "mice-market-intel T7"}
  ]
}
```

- `analysis_result.judgment`는 SKILL §4 3단(GO/HOLD/NO-GO)만 쓴다. 근거는 `judgment_basis` 3줄(강제 조건 점검 결과 · 승부 메시지 근거 · 불리 요인)로 남기고, HOLD면 `go_conditions`에 "무엇이 확인되면 GO인지"를 조건문으로 적는다. 가중 점수는 판정이 아니므로 봉투에 싣지 않는다.
- `open_questions`: 보고서 "발주처 질의 필요" 항목(`client_query`)과 4축에서 "추정"으로 남긴 발주처 이력(`client_history`)·경쟁사(`competitor`) 미확인 항목. 앞의 것은 발주처 질의로, 뒤의 둘은 mice-market-intel 재조사로 해소한다(본 문서 §3-2).
- 입찰가·원가 숫자(`estimate_hint`)는 이 봉투에 싣지 않는다 — mice-estimate 전용 봉투(본 문서 §3-1)로만 보낸다.
- `clientId`: 발주처 슬롯 등록 ID(`client-overlays.md`) — 없으면 `null`(리멤버 기본 룩).
- 저장: `.chaining/[event_name]_[YYYYMMDD]_to_[target].json` (chaining-protocol §6-4).
- 수신 측은 `$schema`가 없으면 체이닝 입력으로 취급하지 않는다(chaining-protocol §6-1) — 본 스킬은 항상 봉투를 채워 내보낸다. 구 `mice-proposal` 표기 페이로드는 수신 측이 `jc-pptx`로 별칭 치환한다(chaining-protocol §3-1).

## 2-3. 매핑 시 주의 사항

- **리스크 상 등급은 제안서 본문에 노출 금지**: 협상 카드는 협상 단계에서. 제안서에 노출 시 발주처 경계 강화.
- **우리 약점은 제안서 미포함**: 4축 응찰 S/W/O/T 메모의 "약점·위협"은 내부 전략 자료. jc-pptx 입력에서 제외.
- **승률은 자원 투입 강도 판단용**: 제안서 본문에 노출 금지.
- **입찰가는 mice-estimate에 별도 전달**(전용 봉투의 `estimate_hint`, 본 문서 §3-1): jc-pptx에는 가격 정책 방향만 전달.

---

## 3. 견적·재조사 봉투

### 3-1. mice-estimate 전용 봉투 (`target: "mice-estimate"`)

견적 단계로 넘길 때는 jc-pptx용 봉투를 재사용하지 않고 **mice-estimate가 실제로 읽는 키**로 별도 봉투를 낸다. 수신 측 정본은 `mice-estimate/references/chaining-schema.md` §3(rfp-analyzer 입력 스키마)이며, mice-estimate는 `source: "mice-rfp-analyzer"`를 감지하면 자동 산출(`estimatedFrom: rfp_default`)로 들어간다. 6축 금액 데이터는 같은 봉투 안의 `estimate_hint`로 함께 싣는다.

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-rfp-analyzer",
  "version": "<SKILL.md frontmatter version>",
  "generatedAt": "YYYY-MM-DDTHH:MM:SS+09:00",
  "target": "mice-estimate",
  "clientId": null,
  "projectTitle": "{{event_name}}",

  "client": "{{client_company}}",
  "rfpId": "{{공고번호 또는 null}}",
  "eventDate": "YYYY-MM-DD",
  "budgetRange": { "min": null, "max": 300000000, "currency": "KRW", "vatIncluded": false },
  "evaluationCriteria": [
    { "name": "운영 계획", "weight": 30 },
    { "name": "입찰 가격", "weight": 20 }
  ],
  "eventScale": { "target": 500, "guarantee": null },
  "venue": null,
  "options": null,
  "boothCount": 0,
  "format": "remember",
  "notes": "RFP 단계 — 베뉴·옵션 TBD. 발주처 지정 서식: (있으면 명칭·요구 항목)",

  "estimate_hint": {
    "budget_announced": 300000000,
    "estimated_cost": 238000000,
    "recommended_bid": 294880000,
    "vat": "별도",
    "risk_premium": 0.05
  }
}
```

| analyzer 산출 데이터 | 봉투 키 | 변환 규칙 |
|---------------------|--------|----------|
| `rfp_meta.client` | `client` | 그대로 |
| `rfp_meta.rfp_id` | `rfpId` | 그대로(없으면 `null`) |
| `rfp_meta.event_date` | `eventDate` | 그대로 |
| 6축 / 발주가 `budget_announced` | `budgetRange.max` | 숫자(원). 하한이 원문에 없으면 `min: null` |
| 6축 / 부가세 별도·포함 | `budgetRange.vatIncluded` | 포함=`true`, 별도=`false` |
| 2축 / `evaluation_focus[].category`·`weight` | `evaluationCriteria[].name`·`weight` | 비율 0.30 → 정수 30(%) |
| 1축 / 행사 규모 `event_scale` | `eventScale.target` | 원문 인원을 **정수**로 파싱(범위면 상한). 최소 보장 인원이 원문에 있으면 `guarantee`, 없으면 `null`(수신 측이 target으로 대체) |
| 1축 / 장소 지정 | `venue` | 원문이 베뉴를 지정하면 `{"name": "...", "rental": null}`, 미정이면 `null`(수신 측 자동 산출) |
| 1축 / 과업 범위의 옵션 | `options` | 원문에 명시된 것만 mice-estimate 옵션 키(`video`·`emcee`·`souvenir`·`scaler4k`·`survey`·`photowall_basic`·`photowall_premium`·`photo`·`aving`)로 `true`. 미정이면 `null` |
| 6축 / 발주가·추정 원가·입찰가 권고·VAT | `estimate_hint.budget_announced`·`estimated_cost`·`recommended_bid`·`vat` | 그대로 — 수신 측은 산출 후 비교·가격 점수 산식 연동(완료 게이트 6)에 쓴다 |
| 3축 / 리스크 프리미엄 | `estimate_hint.risk_premium` | 상 10% · 중 5% 합산(소수) |

- **양식**: 리멤버 견적서 단일(`format: "remember"`). 발주처가 지정한 서식(산출내역서 항목명·합계 구조 등)이 있으면 `notes`로 전달한다.
- 패키지 할인 적용 여부 등 견적 조건 메모도 `notes`에 적는다.
- 저장: `.chaining/[event_name]_[YYYYMMDD]_to_mice-estimate.json`.

### 3-2. mice-market-intel 재조사 의뢰 (`open_questions`)

4축(경쟁)에서 근거 자료가 없어 "추정"으로 남긴 항목은 판정을 지탱하지 못한다. `open_questions` 중 `client_history`·`competitor` 유형을 `target: "mice-market-intel"` 봉투(같은 키)로 넘기면 mice-market-intel이 Phase 1 아웃라인 시드로 흡수해 **T4 발주처/정책 환경**(발주 패턴·과거 수행사) 또는 **T7 타깃 주체 심층 프로파일**(비딩 맞수)로 조사하고, 결과 `competitors[]`·`policy_demand[]`를 다시 4축 근거로 보낸다(기준일 병기). `client_query` 유형은 발주처 질의 대상이므로 넘기지 않는다.

---

## 4. pt-script 연결 (jc-pptx 경유)

pt-script는 RFP 분석 페이로드를 직접 받지 않는다(`pt-script/references/chaining-schema.md`). 아래 analyzer 데이터는 jc-pptx 덱에 먼저 반영되고, pt-script는 확정된 덱(+ jc-pptx 페이로드)을 입력으로 대본을 쓴다.

| analyzer 산출 데이터 | 덱을 거쳐 대본에 반영되는 곳 |
|---------------------|---------------|
| 7축 / 핵심 메시지 Top 3 | 대본 도입부·결론 메시지 |
| 2축 / 평가 기준 가중치 | 대본 시간 배분 |
| 4축 / 차별화 포인트 | 대본 차별화 섹션 |
| 발표 시간 (RFP 명시) | 대본 분량 조정 — `rfp_meta`에 함께 기록 |

---

## 5. 행사 종료 후 회고 (mice-aftermath)

결과 보고 단계에서 analyzer의 추정을 실제 결과와 비교해 분석 정확도를 축적한다. mice-aftermath는 `.chaining/`에 남은 두 봉투에서 아래 키를 읽는다(실제 수주 여부·계약가는 사용자 입력).

| analyzer 분석 | 봉투 키 (어느 봉투) | 비교 대상 |
|--------------|-------------------|---------------|
| 판정·추정 승률 vs 실제 수주 | `analysis_result.judgment`·`estimated_winrate` (jc-pptx 봉투, §2-2) | 분석 정확도 |
| 입찰가 권고 vs 실제 입찰가 | `estimate_hint.recommended_bid` (mice-estimate 봉투, §3-1) | 가격 전략 검증 |
| 평가 가중치 vs 실제 평가 결과 | `evaluation_focus` (jc-pptx 봉투) | 평가 추정 정확도 |
| 핵심 메시지 vs 실제 평가 코멘트 | `analysis_result.core_messages` (jc-pptx 봉투) | 메시지 효과성 |

---

## 6. 체이닝 호출 트리거

| 사용자 발언 | 체이닝 |
|------------|-------|
| "분석 완료. 이제 제안서 만들어줘" | analyzer → jc-pptx |
| "GO. 다음 단계 진행" | analyzer → jc-pptx |
| "이 분석 결과로 견적 뽑아줘" | analyzer → mice-estimate (전용 봉투, §3-1) |
| "발주처 이력·맞수 더 알아봐줘" | analyzer → mice-market-intel (`open_questions`, §3-2) |
| "발표 대본까지" | analyzer → jc-pptx → pt-script |
| "전체 워크플로우 진행" | analyzer → jc-pptx → mice-estimate → pt-script (순차, 각 단계 산출물은 기획안 1회 확인 후 빌드) |

---

## 7. 데이터 무결성 원칙

- **단일 진실 소스 (Single Source of Truth)**: RFP 원문이 모든 데이터의 출처. analyzer 결과를 다른 스킬이 받아 변경하지 않음.
- **변경 추적**: 후속 스킬에서 분석 결과를 수정해야 할 경우, 변경 사유를 명시하고 analyzer에 피드백.
- **버전 관리**: 산출물 파일명에 날짜 포함. 동일 RFP에 대한 분석을 여러 번 갱신할 경우 버전 표기.

---

## 8. 한 세션 체이닝 vs 세션 분리

| 시나리오 | 권장 |
|---------|------|
| analyzer만 단독 사용 | 현재 세션 |
| analyzer → jc-pptx 즉시 체이닝 | 현재 세션(소형 RFP) / 새 세션(대형 RFP, 컨텍스트 보호) |
| 풀 워크플로우 (analyzer→jc-pptx→mice-estimate→pt-script) | 단계별 세션 분리 권장 — 분리·핸드오프 규칙은 `jc-session-protocol` |

→ 세션을 나눌 때는 ChainPayload JSON 파일을 넘겨 다음 세션이 재분석 없이 이어받게 한다.
