# Chaining Guide — mice-proposal 입력 매핑

Type A 외부 클라이언트 미팅(Discovery / 정기 협의)의 회의록에서 추출한 5개 데이터를 mice-proposal 스킬 입력 JSON 패키지로 자동 변환하는 룰.

> **봉투 정본**: 공통 `ChainPayload/v1` 봉투 구조(`$schema`·`source`·`version`·`generatedAt`)·전체 워크플로우·표준 규약은 [jc-design-system/references/chaining-protocol.md](../../jc-design-system/references/chaining-protocol.md) 참조.
> 요약: 출력 JSON 봉투는 `"source": "mice-meeting-minutes"` 를 둔다(아래 §3 예시는 본 스킬 페이로드 관례를 보존). 본 스킬은 proposal·estimate·dashboard·sponsor-deck 으로 분기 체이닝하며, 본 문서는 그 **고유 페이로드 매핑**(Discovery 5데이터 추출·변환)만 정의한다.

---

## 1. 체이닝 트리거 조건

다음 조건을 **모두 만족**할 때 체이닝 입력 패키지 자동 생성:

| 조건 | 판정 |
|------|------|
| 미팅 유형 | Type A (외부 클라이언트) — 단, Discovery·킥오프 단계 |
| GO 시그널 | 결정사항에 "행사 진행 합의" 또는 "제안서 작성 합의" 포함 |
| 데이터 충족도 | 5개 데이터 카테고리 중 3개 이상 추출 가능 |
| 클라이언트 명시 | `--client` 또는 transcript 내 클라이언트명 명확 |

→ 조건 미충족 시 체이닝 패키지 생성 안 함. 사용자가 명시적 `--chain-to=mice-proposal` 호출 시만 강제 생성.

---

## 2. Discovery 5데이터 추출 카테고리

### 데이터 1: 고객 니즈 (Pain Points + 기대 효과)

#### Pain Point 추출 시그널
- "어려워요", "문제는", "고민이", "막혀 있는 게"
- "지난번에는 ~ 안 됐어요"
- "[기존 방식]으로는 한계가 있어서…"
- "ROI가 안 나와요"

#### 기대 효과 추출 시그널
- "이번엔 ~을 원해요"
- "목표는 ~"
- "성공한다고 하면 ~"
- "최소한 ~까지는"

#### 출력 형식
```json
{
  "pain_points": [
    "기존 방식으로는 타겟 고객 도달 어려움",
    "이전 행사에서 ROI 측정 불가",
    "한국 시장 인지도 낮음"
  ],
  "expected_outcomes": [
    "한국 보안 의사결정자 250명 도달",
    "ROI 측정 가능한 1:1 미팅 30건",
    "본사 보고용 한국 시장 진출 케이스 확보"
  ]
}
```

---

### 데이터 2: 예산 단서 (명시 + 추정)

#### 명시 예산 추출 시그널
- "예산은 ~억 정도", "[금액] 책정했습니다"
- "[금액] 안에서 가능할까요?"

#### 추정 예산 추출 시그널 (간접)
- 비공식 발언 ("[금액]밖에 없어서…")
- 이전 행사 규모 언급 ("작년에 [금액] 정도 썼는데")
- 결재선 언급 ("[금액] 이상은 본사 결재")

#### 출력 형식
```json
{
  "budget": {
    "explicit": null,
    "estimated_min": 80000000,
    "estimated_max": 150000000,
    "evidence": "이전 행사 규모 1억 언급 + 본사 결재 1.5억 라인 언급",
    "confidence": "medium"
  }
}
```

→ 명시 안 된 경우 `explicit: null`, 추정 범위만 제공. mice-proposal에서 견적 가이드 활용.

---

### 데이터 3: 일정 단서

#### 추출 카테고리
- 행사일 (확정 / 추정)
- 의사결정 마감 (제안서 마감·계약 마감)
- 의사결정자 일정 (본사 결재 시점·이사회 일정)
- 우리 측 답변 기한

#### 출력 형식
```json
{
  "timeline": {
    "event_date": "2026-06-18",
    "event_date_confidence": "high",
    "proposal_deadline": "2026-05-22",
    "decision_deadline": "2026-05-30",
    "decision_maker_schedule": "Darktrace 본사 시니어 5/16 미팅 참석 예정",
    "our_response_due": "2026-05-12 (베뉴 후보)"
  }
}
```

---

### 데이터 4: 의사결정자 / 영향력자

#### 추출 시그널
- 발화 빈도·길이 분석 (높은 비율 = 영향력자 후보)
- "결재", "승인", "사인" 결합 인물
- 호칭 분석 (직급 높은 인물)
- 외부 언급 ("[직책] 통해 결재")

#### 출력 형식
```json
{
  "decision_makers": [
    {
      "name": "Darktrace 김부장",
      "role": "한국 지사 영업 총괄",
      "influence": "high",
      "decision_authority": "한국 단독 결재 가능 — 1.5억 미만",
      "preference_signals": [
        "1:1 미팅룸 비중 강조",
        "ROI 측정 강조"
      ]
    },
    {
      "name": "Darktrace 본사 시니어 (미정)",
      "role": "글로벌 본사 마케팅 시니어",
      "influence": "high",
      "decision_authority": "1.5억 이상 결재 + 글로벌 일관성 검토",
      "preference_signals": [
        "5/16 미팅 참석 예정 — 직접 파악 필요"
      ]
    }
  ]
}
```

---

### 데이터 5: 경쟁사 / 대안 언급

#### 추출 시그널
- 경쟁 PCO 명 직접 언급
- "다른 곳도 견적 받고 있어요"
- "[경쟁사]랑 비교해보니까…"
- "이전에 [회사명]이랑 했는데"
- "직접 운영 vs 외주" 발화

#### 출력 형식
```json
{
  "competition": [
    {
      "type": "competing_pco",
      "name": "[경쟁 PCO 명]",
      "evidence": "사용자 28분 발화: '다른 PCO 견적도 받고 있어요'",
      "threat_level": "medium"
    },
    {
      "type": "in_house_alternative",
      "name": "Darktrace 본사 마케팅팀 직접 운영",
      "evidence": "본사 시니어 결재 시 '직접 운영 카드'도 검토 중 시사",
      "threat_level": "low"
    }
  ]
}
```

---

## 3. 통합 JSON 패키지 (mice-proposal 입력 형식)

```json
{
  "source_skill": "mice-meeting-minutes",
  "source_session_id": "darktrace-discovery-001",
  "source_minutes_file": "meeting-minutes_darktrace-discovery_20260509_A.docx",
  "generated_at": "2026-05-09T16:30:00+09:00",
  "client": {
    "id": "darktrace",
    "name": "Darktrace Korea",
    "industry": "Cybersecurity",
    "region": "Korea (Global HQ: UK)"
  },
  "project_context": {
    "project_name": "Darktrace Korea Discovery",
    "event_type_estimate": "Conference + 1:1 Business Matching",
    "scale_estimate": {
      "participants": 250,
      "duration_days": 1,
      "venue_grade": "5-star hotel"
    }
  },
  "discovery_data": {
    "pain_points": ["..."],
    "expected_outcomes": ["..."],
    "budget": {
      "explicit": null,
      "estimated_min": 80000000,
      "estimated_max": 150000000,
      "evidence": "...",
      "confidence": "medium"
    },
    "timeline": {
      "event_date": "2026-06-18",
      "proposal_deadline": "2026-05-22",
      "decision_deadline": "2026-05-30"
    },
    "decision_makers": [...],
    "competition": [...]
  },
  "strategic_notes": {
    "win_probability_estimate": "60-70%",
    "key_differentiators_to_emphasize": [
      "리멤버 명함 데이터 기반 타겟 모집",
      "1:1 미팅 ROI 측정 시스템",
      "한국 보안 시장 인사이트 패널"
    ],
    "key_risks": [
      "본사 시니어 5/16 미팅에서 직접 검증 통과 필요",
      "본사 결재 1.5억 라인 — 견적 1.4억 이내 권고"
    ],
    "recommended_proposal_focus": [
      "ROI 측정 방법론 별도 섹션",
      "한국 시장 인사이트 (본사 보고 가치)",
      "베뉴 2곳 비교 옵션 제시"
    ]
  }
}
```

---

## 4. mice-proposal 측 활용 매핑

mice-proposal이 본 패키지를 받으면 제안서 1차 초안의 70%가 자동 채워지는 구조:

| 제안서 섹션 | 활용 데이터 |
|------------|-------------|
| 제안 요약 | pain_points + expected_outcomes |
| 행사 컨셉 | event_type_estimate + recommended_proposal_focus |
| 행사 규모 | scale_estimate |
| 차별화 포인트 | key_differentiators_to_emphasize |
| 일정 | timeline |
| 견적 가이드 | budget |
| 리스크 대응 | key_risks |
| 의사결정자 매핑 (내부 메모) | decision_makers |
| 경쟁 대응 (내부 메모) | competition |

---

## 5. 체이닝 패키지 저장 위치

```
.chaining/[client_id]_[YYYYMMDD]_to_proposal.json
```

예시:
```
.chaining/darktrace_20260509_to_proposal.json
```

→ mice-proposal 호출 시 본 경로 우선 검색.

---

## 6. 사용자에게 제시되는 체이닝 안내

회의록 생성 직후 본 스킬 출력에 다음 안내 포함:

```
[체이닝 가능 안내]

본 회의록은 mice-proposal 입력 패키지로 변환되었습니다.

저장 위치: .chaining/darktrace_20260509_to_proposal.json
추출 데이터:
- 고객 Pain Point 3건 / 기대 효과 3건
- 예산 추정: 8천만 ~ 1.5억 (신뢰도 중)
- 일정: 행사 6/18, 제안 마감 5/22
- 의사결정자: 김부장 (한국 단독) + 본사 시니어 (글로벌)
- 경쟁 추정: 타 PCO 1곳 + 직접 운영 옵션 (낮음)

다음 단계 권장: mice-proposal 호출 ("Darktrace 제안서 작성")
```

---

## 7. 체이닝 검증 체크리스트

생성 후 자동 검증:

| 체크 | 기준 | 미달 시 |
|------|------|--------|
| 5개 카테고리 추출 수 | 3개 이상 | "데이터 부족 — 추가 미팅 권장" 경고 |
| 의사결정자 신뢰도 | high 1명 이상 | "의사결정자 미확정 — 별도 확인 필요" |
| 예산 추정 범위 | 신뢰도 medium 이상 | "예산 단서 부족 — 견적 사전 협의 권장" |
| 행사일 추정 | 명시 또는 신뢰도 high | "행사일 미확정 — 일정 협의 우선" |
| 경쟁사 시그널 | 1개 이상 식별 | "경쟁 환경 미파악 — 시장 조사 권장" |

→ 미달 항목은 mice-proposal 측에서 "Discovery 보강 필요" 표시로 표출.

---

## 8. 풀 워크플로우 체인 (참고)

본 스킬의 발원 위치(요약):

```
mice-rfp-analyzer → [GO] → Discovery Meeting → mice-meeting-minutes(본 스킬, Type A) → mice-proposal → mice-estimate → pt-script → 비딩 PT → mice-meeting-minutes(Type C 사후) → 시리즈 누적
```

→ 전체 체이닝 흐름도(회의록 발원 분기·시리즈→dashboard·jc-redteam 게이트 포함)는 **봉투 정본** [chaining-protocol.md §5](../../jc-design-system/references/chaining-protocol.md) 참조.
