# Chaining Guide — 회의록 → ChainPayload/v1

Discovery·킥오프·운영 협의·사후 회고 회의록에서 뽑은 데이터를 다음 스킬이 재분석 없이 이어받도록 `ChainPayload/v1` 봉투로 내보내는 규칙. 본 문서는 **본 스킬 고유 페이로드**만 정의한다.

> **봉투 정본**: `$schema`·`source`·`version`·`generatedAt`·`target`·`clientId`·`projectTitle`과 수신 규칙은 [jc-design-system/references/chaining-protocol.md](../../jc-design-system/references/chaining-protocol.md). source는 `mice-meeting-minutes`, `version`은 SKILL.md frontmatter 값을 넣는다(예시 숫자 복사 금지). 봉투와 페이로드는 같은 최상위에 평탄하게 둔다.

---

## 1. 생성 조건 · target 선택

다음을 모두 만족하면 회의록 빌드 직후 페이로드를 함께 만든다. 사용자가 `--chain-to=<target>`을 주면 조건과 무관하게 만든다.

| 조건 | 판정 |
|------|------|
| 미팅 유형 | Type A(Discovery·킥오프) · Type C(계약·운영 협의) · 사후 회고 |
| 진행 시그널 | 결정사항에 "진행 합의"·"제안 요청"·"킥오프 확정"·"회고" 류 포함 |
| 데이터 충족도 | §2 다섯 카테고리 중 3개 이상 추출 |
| 발주처 식별 | `--client` 또는 transcript 내 발주처 명확 (실명은 `{{client_company}}` 슬롯으로만) |

| 회의 성격 | target | 수신 측 용도 (수신 스킬 정본) |
|----------|--------|------------------------------|
| Type A Discovery + 제안 진행 합의 | `jc-pptx` | 제안서 덱 Partial 입력 (`jc-pptx/references/proposal-playbook.md §1`) |
| Discovery에서 포지셔닝·사업성 판단이 필요 | `jc-strategy-canvas` | ① 인테이크 · F4 JTBD · F3 SWOT 시드 (`jc-strategy-canvas/references/chaining-schema.md §1-2`) |
| 수주 후 킥오프·운영 협의 (Type A·C) | `mice-ops-docs` | 운영계획서 1·2·7섹션 (`mice-ops-docs/references/chaining-schema.md §1`) |
| 행사 후 회고·정산 미팅 | `mice-aftermath` | 6축 교훈 · 8축 차기 권고 (`mice-aftermath/references/chaining-schema.md §1`) |

조건 미충족이면 만들지 않고, 응답 끝에 "체이닝 데이터 부족 — 추가 미팅 권장" 한 줄만 남긴다. 견적은 jc-pptx 덱의 `estimate_hint`를 거쳐 mice-estimate로 가므로 본 스킬이 직접 보내지 않는다.

---

## 2. Discovery 5데이터 추출

### 데이터 1 — 고객 니즈 (Pain Point + 기대 효과)
- Pain Point 시그널: "어려워요", "문제는", "고민이", "지난번에는 ~ 안 됐어요", "[기존 방식]으로는 한계가…", "ROI가 안 나와요"
- 기대 효과 시그널: "이번엔 ~을 원해요", "목표는 ~", "성공한다고 하면 ~", "최소한 ~까지는"

```json
{
  "pain_points": ["기존 방식으로는 타깃 고객 도달 어려움", "이전 행사에서 성과 측정 불가"],
  "expected_outcomes": ["타깃 직무 의사결정자 250명 도달", "성과 측정 가능한 1:1 미팅 30건"]
}
```

### 데이터 2 — 예산 단서 (명시 + 추정)
- 명시: "예산은 ~ 정도", "[금액] 책정했습니다", "[금액] 안에서 가능할까요?"
- 추정(간접): 비공식 발언("[금액]밖에 없어서…"), 이전 행사 규모 언급, 결재선 언급("[금액] 이상은 본사 결재")
- 비공식 예산 발언은 External 회의록에서 마스킹되지만 페이로드에는 Internal 값으로 남긴다(내부 전용 봉투).

```json
{
  "budget": {
    "explicit": null,
    "estimated_min": 80000000,
    "estimated_max": 150000000,
    "evidence": "이전 행사 규모 언급 + 본사 결재선 언급 (예시 수치)",
    "confidence": "medium"
  }
}
```

### 데이터 3 — 일정 단서
행사일(확정/추정) · 제안·계약 마감 · 의사결정자 일정 · 우리 측 답변 기한.

```json
{
  "timeline": {
    "event_date": "2026-06-18",
    "event_date_confidence": "high",
    "proposal_deadline": "2026-05-22",
    "decision_deadline": "2026-05-30",
    "decision_maker_schedule": "A사 본사 담당 5/16 미팅 참석 예정",
    "our_response_due": "2026-05-12 (베뉴 후보)"
  }
}
```

### 데이터 4 — 의사결정자 · 영향력자
발화 빈도·길이, "결재·승인·사인" 결합 인물, 직급 호칭, 외부 언급("[직책] 통해 결재").

```json
{
  "decision_makers": [
    {"name": "김부장 (A사)", "role": "국내 사업 총괄", "influence": "high",
     "decision_authority": "국내 단독 결재 — 결재선 이하", "preference_signals": ["1:1 미팅룸 비중", "성과 측정"]},
    {"name": "A사 본사 담당 (미정)", "role": "본사 마케팅", "influence": "high",
     "decision_authority": "결재선 초과분 + 글로벌 일관성 검토", "preference_signals": ["5/16 미팅에서 직접 확인 필요"]}
  ]
}
```

### 데이터 5 — 경쟁사 · 대안
경쟁 대행사 직접 언급, "다른 곳도 견적 받고 있어요", "직접 운영 vs 외주" 발화.

```json
{
  "competition": [
    {"type": "competing_agency", "name": "[경쟁사명]", "evidence": "28분 발화: '다른 곳 견적도 받고 있어요'", "threat_level": "medium"},
    {"type": "in_house_alternative", "name": "A사 본사 직접 운영", "evidence": "본사 결재 시 직접 운영 검토 시사", "threat_level": "low"}
  ]
}
```

---

## 3. 통합 페이로드 (예: target jc-pptx)

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-meeting-minutes",
  "version": "<SKILL.md version>",
  "generatedAt": "2026-05-09T16:30:00+09:00",
  "target": "jc-pptx",
  "clientId": "a-corp-2026",
  "projectTitle": "A사 고객 컨퍼런스 2026",
  "dashboardFile": "dashboard_a사-discovery_20260509.html",
  "seriesId": "a-corp-discovery",
  "client": {"id": "a-corp-2026", "name": "{{client_company}}", "industry": "IT 솔루션", "region": "국내 (본사 해외)"},
  "project_context": {
    "project_name": "A사 고객 컨퍼런스 2026",
    "event_type_estimate": "컨퍼런스 + 1:1 비즈니스 매칭",
    "scale_estimate": {"participants": 250, "duration_days": 1, "venue_grade": "5성 호텔"}
  },
  "discovery_data": {
    "pain_points": ["..."], "expected_outcomes": ["..."],
    "budget": {"explicit": null, "estimated_min": 80000000, "estimated_max": 150000000, "confidence": "medium"},
    "timeline": {"event_date": "2026-06-18", "proposal_deadline": "2026-05-22"},
    "decision_makers": ["..."], "competition": ["..."]
  },
  "strategic_notes": {
    "win_probability_estimate": "60-70%",
    "key_differentiators_to_emphasize": ["리멤버 타깃 데이터 기반 모객", "1:1 미팅 성과 측정 설계"],
    "key_risks": ["본사 담당 5/16 검증 통과 필요", "결재선 이내 견적 권고"],
    "recommended_proposal_focus": ["성과 측정 방법론 별도 섹션", "베뉴 2곳 비교 옵션"]
  },
  "actions": [{"id": "AC-DISC-001", "owner": "호스트 (리멤버 MICE비즈팀)", "action": "베뉴 후보 3곳 비교 자료", "due": "2026-05-12", "status": "TODO"}],
  "risks": [{"text": "베뉴 가용일 충돌", "impact": "상"}],
  "pending": [{"text": "동시통역 부스 설치 여부", "reason": "본사 결재 필요"}]
}
```

- `clientId`는 `client-overlays.md` 발주처 슬롯 ID. 없으면 `null`(리멤버 기본). 발주처 실명은 `client.name` 슬롯으로만.
- target별로 필요한 키만 채워도 된다 — `mice-ops-docs`는 `client`·`project_context`·`strategic_notes`·`actions`, `mice-aftermath`는 `strategic_notes`·`risks`·`actions`·`pending`, `jc-strategy-canvas`는 `discovery_data`·`project_context`·`strategic_notes`.

---

## 4. 수신 측 활용 (jc-pptx 제안서 예)

| 제안서 섹션 | 활용 데이터 |
|------------|-------------|
| 제안 요약 | pain_points + expected_outcomes |
| 행사 컨셉 | event_type_estimate + recommended_proposal_focus |
| 행사 규모 | scale_estimate |
| 차별화 | key_differentiators_to_emphasize (근거 있는 항목만) |
| 일정 | timeline |
| 견적 가이드 (`estimate_hint` → mice-estimate) | budget |
| 리스크 대응 | key_risks |
| 내부 메모 (본문 노출 금지) | decision_makers · competition |

---

## 5. 저장 위치

```
.chaining/[project_or_topic]_[YYYYMMDD]_to_[target].json      # chaining-protocol §6-4
예) .chaining/a-corp-discovery_20260509_to_jc-pptx.json
```

## 6. 사용자 안내 (응답 끝에 붙이는 블록)

```
[체이닝] .chaining/a-corp-discovery_20260509_to_jc-pptx.json
- Pain Point 2 · 기대 효과 2 · 예산 추정 8천만~1.5억(신뢰도 중, 예시)
- 일정: 행사 6/18 · 제안 마감 5/22 · 의사결정자 2명 · 경쟁 신호 2건
다음 단계: jc-pptx에 이 파일을 주고 "A사 제안서 구성" 요청
```

## 7. 검증 체크리스트

| 체크 | 기준 | 미달 시 |
|------|------|--------|
| 5개 카테고리 추출 수 | 3개 이상 | "데이터 부족 — 추가 미팅 권장" |
| 의사결정자 신뢰도 | high 1명 이상 | "의사결정자 미확정 — 별도 확인 필요" |
| 예산 추정 | 신뢰도 medium 이상 | "예산 단서 부족 — 견적 사전 협의 권장" |
| 행사일 | 명시 또는 신뢰도 high | "행사일 미확정 — 일정 협의 우선" |
| 경쟁 신호 | 1개 이상 | "경쟁 환경 미파악 — mice-market-intel 조사 권장" |
| 식별정보 | 발주처 실명·개인 연락처 0 | 슬롯(`{{client_company}}`)으로 치환 |

미달 항목은 봉투에 `"warnings": [...]`로 남기고, 수신 측은 "Discovery 보강 필요"로 표시한다.

## 8. 전체 흐름

```
mice-rfp-analyzer → [GO] → Discovery 미팅 → mice-meeting-minutes(Type A)
   ├─→ jc-strategy-canvas (전략 판단) ─→ jc-pptx
   └─→ jc-pptx (제안서) → mice-estimate → pt-script → 비딩 PT
수주 → 킥오프 미팅 → mice-meeting-minutes(Type A·C) ─→ mice-ops-docs (운영계획서)
행사 후 회고 → mice-meeting-minutes ─→ mice-aftermath (결과보고·교훈)
모든 산출물 ─→ jc-redteam
```

전체 체이닝 흐름도는 봉투 정본 [chaining-protocol.md §5](../../jc-design-system/references/chaining-protocol.md).
