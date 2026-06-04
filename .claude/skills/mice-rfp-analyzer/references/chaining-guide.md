# Chaining Guide — mice-proposal 입력 매핑 + 풀 워크플로우 체이닝

mice-rfp-analyzer 산출물을 다른 스킬로 전달할 때의 데이터 매핑 규칙.

> **봉투 정본**: 공통 `ChainPayload/v1` 봉투 구조(`$schema`·`source`·`version`·`generatedAt`)·전체 워크플로우 다이어그램·표준 규약은 [jc-design-system/references/chaining-protocol.md](../../jc-design-system/references/chaining-protocol.md) 참조.
> 요약: 본 스킬은 워크플로우의 **시작점**으로, 출력 JSON은 봉투에 `"source": "mice-rfp-analyzer"` 를 둔다. 본 문서는 mice-rfp-analyzer **고유 입출력 페이로드 매핑**(7축 분석 결과 → 각 후속 스킬 활용)만 정의한다.

---

## 1. 풀 워크플로우상의 위치 (요약)

```
[RFP 원문] → mice-rfp-analyzer(본 스킬, 시작점) → mice-proposal → mice-estimate → pt-script → (행사 후) mice-dashboard
```

→ 본 스킬은 후속 스킬에 양질의 입력을 전달하는 것이 핵심 기능. **전체 체이닝 흐름도(회의록 발원·영업 분기·jc-redteam 게이트 포함)는 봉투 정본 §5 참조.**

---

## 2. mice-proposal 입력 매핑 (가장 중요)

GO 판정 시, 분석 결과를 다음 구조로 변환하여 mice-proposal 호출 시 함께 전달:

### 2-1. 매핑 테이블

| analyzer 산출 데이터 | proposal 활용 영역 |
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

### 2-2. 입력 패키지 표준 형식

mice-proposal에 전달하는 표준 JSON 구조:

```json
{
  "source": "mice-rfp-analyzer",
  "rfp_meta": {
    "client": "[발주처명]",
    "event_name": "[행사명]",
    "event_date": "YYYY-MM-DD",
    "event_venue": "[장소]",
    "event_scale": "[규모]",
    "budget_announced": [발주가],
    "submission_deadline": "YYYY-MM-DD"
  },
  "analysis_result": {
    "judgment": "GO",
    "total_score": 4.2,
    "estimated_winrate": 0.45,
    "core_messages": [
      "메시지 1",
      "메시지 2",
      "메시지 3"
    ]
  },
  "requirements": {
    "mandatory": [
      {"item": "...", "source": "p.X 조항 Y", "our_capability": "가능"}
    ],
    "optional": [...],
    "bonus": [...]
  },
  "evaluation_focus": [
    {"category": "...", "weight": 0.30, "our_strength": true},
    {"category": "...", "weight": 0.25, "our_strength": true}
  ],
  "differentiation_points": [
    "차별 포인트 1",
    "차별 포인트 2"
  ],
  "proposal_structure_hint": {
    "page_allocation": {
      "executive_summary": 1,
      "requirement_response": 8,
      "operation_plan": 12,
      "differentiation": 4,
      "team_qualification": 3,
      "budget": 2
    },
    "emphasis_sections": ["operation_plan", "differentiation"]
  },
  "risk_notes_for_negotiation": [
    "리스크 상 등급 항목 1 (제안서 미포함, 협상 포인트)",
    "리스크 상 등급 항목 2"
  ]
}
```

### 2-3. 매핑 시 주의 사항

- **리스크 상 등급은 제안서 본문에 노출 금지**: 협상 카드는 협상 단계에서. 제안서에 노출 시 발주처 경계 강화.
- **우리 약점은 제안서 미포함**: 4축 SWOT의 "약점·위협"은 내부 전략 자료. proposal 입력에서 제외.
- **승률은 자원 투입 강도 판단용**: 제안서 본문에 노출 금지.
- **입찰가는 mice-estimate에 별도 전달**: proposal에는 가격 정책 방향만 전달.

---

## 3. mice-estimate 입력 매핑

견적서 작성 시 analyzer의 6축 데이터 활용:

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

## 4. pt-script 입력 매핑

발표 대본 작성 시 analyzer의 7축 데이터 활용:

| analyzer 산출 데이터 | pt-script 활용 |
|---------------------|---------------|
| 7축 / 핵심 메시지 Top 3 | 대본 도입부·결론 메시지 |
| 2축 / 평가 기준 가중치 | 대본 시간 배분 |
| 2축 / 우리 강점 영역 | 대본 강조 부분 |
| 4축 / 차별화 포인트 | 대본 차별화 섹션 |
| 발표 시간 (RFP 명시) | 대본 분량 조정 |
| 발주처 정보 | 대본 호칭·인사말 |

---

## 5. mice-dashboard 입력 매핑 (행사 종료 후)

행사 결과 보고 시 analyzer의 7축 분석 vs 실제 결과 비교:

| analyzer 분석 | dashboard 비교 |
|--------------|---------------|
| 추정 승률 vs 실제 수주 | 분석 정확도 |
| 입찰가 권고 vs 실제 입찰가 | 가격 전략 검증 |
| 평가 가중치 vs 실제 평가 결과 | 평가 추정 정확도 |
| 핵심 메시지 vs 실제 평가 코멘트 | 메시지 효과성 |

→ 분석 정확도 데이터는 향후 analyzer 개선 자료로 축적.

---

## 6. 체이닝 호출 트리거

사용자가 다음 표현을 사용할 때 체이닝 자동 진행:

| 사용자 발언 | 체이닝 |
|------------|-------|
| "분석 완료. 이제 제안서 만들어줘" | analyzer → proposal |
| "GO. 다음 단계 진행" | analyzer → proposal |
| "이 분석 결과로 견적 뽑아줘" | analyzer → estimate |
| "분석 결과 가지고 발표 대본 만들어줘" | analyzer → pt-script |
| "전체 워크플로우 자동 실행" | analyzer → proposal → estimate → pt-script (순차) |

---

## 7. 데이터 무결성 원칙

공통 무결성 규약(단일 진실 소스·변경 추적·버전 표기)은 **봉투 정본** [chaining-protocol.md §6-2](../../jc-design-system/references/chaining-protocol.md) 참조.

→ 본 스킬 특수: **RFP 원문이 모든 데이터의 출처**이며, analyzer 결과는 워크플로우 전체의 단일 진실 소스로 기능한다. 후속 스킬이 받아 임의 변경하지 않는다.

---

## 8. 한 챗 체이닝 vs 챗 전환

| 시나리오 | 권장 |
|---------|------|
| analyzer만 단독 사용 | 본 챗 |
| analyzer → proposal 즉시 체이닝 | 본 챗 (소형 RFP) / 새 챗 (대형 RFP, 컨텍스트 보호) |
| 풀 워크플로우 (analyzer→proposal→estimate→pt-script) | 새 챗 권장 (한 챗 = 한 스킬 원칙) |

→ 풀 워크플로우는 마스터 챗에서 각 스킬을 순차 호출하는 방식이 컨텍스트 안정성 우위.
