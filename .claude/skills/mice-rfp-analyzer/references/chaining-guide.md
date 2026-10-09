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
    └── ChainPayload/v1 JSON         (후속 스킬 입력)
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
| 6축 / 입찰가 권고 | 제안서 / 가격 섹션 (mice-estimate 연동) |
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
    "event_name": "{{event_name}}",
    "event_date": "YYYY-MM-DD",
    "event_venue": "{{venue}}",
    "event_scale": "[규모]",
    "budget_announced": 0,
    "submission_deadline": "YYYY-MM-DD"
  },
  "analysis_result": {
    "judgment": "GO",
    "total_score": 4.2,
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
  "estimate_hint": {
    "budget_announced": 0, "estimated_cost": 0, "recommended_bid": 0,
    "vat": "별도", "risk_premium": 0.05
  }
}
```

- `clientId`: 발주처 슬롯 등록 ID(`client-overlays.md`) — 없으면 `null`(리멤버 기본 룩).
- 저장: `.chaining/[event_name]_[YYYYMMDD]_to_[target].json` (chaining-protocol §6-4).
- 수신 측은 `$schema`가 없으면 체이닝 입력으로 취급하지 않는다(§6-1) — 본 스킬은 항상 봉투를 채워 내보낸다. 구 `mice-proposal` 표기 페이로드는 수신 측이 `jc-pptx`로 별칭 치환한다(§3-1).

## 2-3. 매핑 시 주의 사항

- **리스크 상 등급은 제안서 본문에 노출 금지**: 협상 카드는 협상 단계에서. 제안서에 노출 시 발주처 경계 강화.
- **우리 약점은 제안서 미포함**: 4축 SWOT의 "약점·위협"은 내부 전략 자료. jc-pptx 입력에서 제외.
- **승률은 자원 투입 강도 판단용**: 제안서 본문에 노출 금지.
- **입찰가는 mice-estimate에 별도 전달**(`estimate_hint`): jc-pptx에는 가격 정책 방향만 전달.

---

## 3. mice-estimate 입력 매핑

견적서 작성 시 analyzer의 6축 데이터 활용 (페이로드 `estimate_hint`, `target: "mice-estimate"`로 별도 봉투를 내도 된다):

| analyzer 산출 데이터 | estimate 활용 |
|---------------------|--------------|
| 6축 / 발주가 (총사업비) | 견적 상한선 |
| 6축 / 추정 원가 | 견적 항목별 단가 결정 |
| 6축 / 입찰가 권고 | 견적 총액 |
| 6축 / 부가세 별도 여부 | 견적서 부가세 표기 방식 |
| 3축 / 리스크 프리미엄 | 견적 마진 가산율 |
| 1축 / 운영 범위 | 견적 항목 분류 |

→ mice-estimate 호출 시 추가 정보:
- 발주처 양식 지정 여부 ([표준 양식 A] vs [표준 양식 B] vs 자유 양식)
- 패키지 할인 적용 여부

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

결과 보고 단계에서 analyzer의 추정을 실제 결과와 비교해 분석 정확도를 축적한다.

| analyzer 분석 | 비교 대상 |
|--------------|---------------|
| 추정 승률 vs 실제 수주 | 분석 정확도 |
| 입찰가 권고 vs 실제 입찰가 | 가격 전략 검증 |
| 평가 가중치 vs 실제 평가 결과 | 평가 추정 정확도 |
| 핵심 메시지 vs 실제 평가 코멘트 | 메시지 효과성 |

---

## 6. 체이닝 호출 트리거

| 사용자 발언 | 체이닝 |
|------------|-------|
| "분석 완료. 이제 제안서 만들어줘" | analyzer → jc-pptx |
| "GO. 다음 단계 진행" | analyzer → jc-pptx |
| "이 분석 결과로 견적 뽑아줘" | analyzer → mice-estimate |
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
