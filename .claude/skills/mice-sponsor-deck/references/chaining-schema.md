# Chaining Schema (v2.0) — mice-meeting-minutes → mice-sponsor-deck

본 문서는 sponsor-deck이 다른 스킬과 어떻게 체이닝되는지 명시한다. 1차 입력은 mice-meeting-minutes Discovery 미팅 정리에서 추출한 **스폰서 후보 JSON**이다.

> **봉투 정본**: 공통 `ChainPayload/v1` 봉투 구조(`source`·`version`·`generatedAt` 등 공통 메타)·전체 워크플로우·표준 규약은 [jc-design-system/references/chaining-protocol.md](../../jc-design-system/references/chaining-protocol.md) 참조.
> 요약: 본 스킬은 입력 검증에 자기 전용 식별자 `"$schema": "mice-sponsor-deck/v2.0"` + `extracted_from` 을 쓴다(아래 스키마·검증 룰은 본 스킬 고유 — 그대로 보존). 공통 라우팅은 `source`(`mice-meeting-minutes`)로 수렴한다. 본 문서는 sponsor-deck **고유 입출력 페이로드 스키마**(event_meta·sponsor_candidates·deck-content 변환)만 정의한다.

---

## 1. 체이닝 워크플로우 전체

```
┌──────────────────────────────────────────────────────────────┐
│ Step 1: mice-meeting-minutes 스킬                            │
│ - Discovery 미팅·킥오프 미팅 transcript 분석                  │
│ - 8축 프레임 구조화                                          │
│ - "스폰서 후보" 또는 "협찬 가능성" 발언 추출                  │
└─────────────────────────┬────────────────────────────────────┘
                          ↓ sponsor-candidates.json
┌──────────────────────────────────────────────────────────────┐
│ Step 2: mice-sponsor-deck 스킬 (본 스킬)                     │
│ - sponsor-candidates.json 로드                               │
│ - event_meta 추출 → S1 표지 · S2 Why This Event 반영          │
│ - sponsor_candidates[] 배열 → S5 Tier 매핑 · S7 ROI 산업 선정 │
│ - 6축 분석 + Tier 5단 + 7카테고리 매트릭스 + ROI 3단 케이스    │
└─────────────────────────┬────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ Step 3: 최종 산출물                                          │
│ - HTML 1차 (assets/sponsor-deck-template-*.html 베이스)       │
│ - PPTX 2차 (pptxgenjs + visual-patterns/dark-mode-patterns)   │
│ - (옵션) XLSX 매트릭스                                       │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. 입력 JSON 스키마 (mice-meeting-minutes → sponsor-deck)

### 2-1. 표준 스키마 (`sponsor-candidates.json`)

```json
{
  "$schema": "mice-sponsor-deck/v2.0",
  "event_meta": {
    "event_name": "TOBESOFT TECH FORUM 2026",
    "event_subtitle": "AI·Cloud·Enterprise Tech의 다음 10년",
    "event_date": "2026-09-15",
    "event_venue": "코엑스 컨벤션홀",
    "event_type": "conference",
    "organizer": "[주최사명]",
    "expected_attendees": 5200,
    "is_provisional_slots": false
  },
  "sponsor_candidates": [
    {
      "name": "[기업명1]",
      "industry": "tech",
      "tier_target": "T1",
      "priority": "high",
      "decision_maker": "[직급 또는 부서]",
      "expected_budget_krw": null,
      "notes": "AI 솔루션 핵심 메시지 매칭. 작년 유사 행사 협찬 이력 있음."
    },
    {
      "name": "[기업명2]",
      "industry": "finance",
      "tier_target": "T2",
      "priority": "high",
      "decision_maker": "마케팅 임원",
      "expected_budget_krw": null,
      "notes": "VIP 만찬 좌석 6석 강조 필요. 금융 산업 ROI 케이스 강조."
    },
    {
      "name": "[기업명3]",
      "industry": "tech",
      "tier_target": "T3",
      "priority": "med",
      "decision_maker": null,
      "expected_budget_krw": null,
      "notes": "트랙 세션 스폰서 관심 표명. 부스 18~27㎡ 충분."
    }
  ],
  "audience_hints": {
    "industry_distribution": {
      "tech": 42,
      "finance": 24,
      "manufacturing": 18,
      "healthcare": 10,
      "others": 6
    },
    "decision_maker_ratio": 32,
    "c_level_plus_executive_ratio": 23,
    "b2b_ratio": 87,
    "data_source": "2024년 회차 등록 데이터 + 자기 응답"
  },
  "extracted_from": "mice-meeting-minutes",
  "extraction_date": "2026-05-27",
  "meeting_minutes_ref": {
    "meeting_id": "discovery-tobesoft-2026-04-10",
    "section": "Action Items + 전략 메모"
  }
}
```

### 2-2. 필드 정의

#### event_meta (필수)

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `event_name` | string | ✅ | 행사명 (S1 표지·S2 본문) |
| `event_subtitle` | string | optional | 부제 (S1 표지 보조) |
| `event_date` | ISO 8601 string | ✅ | YYYY-MM-DD 또는 YYYY-MM-DD/YYYY-MM-DD (다일) |
| `event_venue` | string | ✅ | 행사장 (S1 표지) |
| `event_type` | enum | ✅ | `conference` \| `exhibition` \| `forum` \| `corporate` \| `festival` \| `gala` |
| `organizer` | string | ✅ | 주최사 (S2 본문). **자기 회사 표기 금지** — 클라이언트 토큰으로 외부 주입 |
| `expected_attendees` | number | optional | 예상 참가자 수 (S3 SVP-4 KPI 입력) |
| `is_provisional_slots` | boolean | ✅ | Tier 슬롯 수 미확정 여부 (true 시 "잠정안" 캡션 자동 삽입) |

#### sponsor_candidates[] (필수, 최소 3개 이상 권장)

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `name` | string | ✅ | 기업명 (Past Sponsors 슬라이드 또는 영업 우선순위 목록) |
| `industry` | enum | ✅ | `tech` \| `finance` \| `cpg` \| `b2b` \| `public` (roi-case-templates.md §2.1 매핑) |
| `tier_target` | enum | ✅ | `T1` \| `T2` \| `T3` \| `T4` \| `T5` \| `T6` |
| `priority` | enum | ✅ | `high` \| `med` \| `low` (영업 우선순위) |
| `decision_maker` | string | optional | 의사결정자 직급/부서 |
| `expected_budget_krw` | number | optional | 예상 예산 (KRW, price_mode=explicit 시 활용) |
| `notes` | string | optional | 미팅에서 추출한 핵심 메모 (영업 포인트, 우려사항 등) |

#### audience_hints (선택)

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `industry_distribution` | object | optional | 산업별 비율 (%), 합계 100%. **5개 산업 5% 이상만** |
| `decision_maker_ratio` | number | optional | 의사결정권자 비율 (%). 0~100 |
| `c_level_plus_executive_ratio` | number | optional | C-Level + 임원 비율 (%) |
| `b2b_ratio` | number | optional | B2B 비율 (%) |
| `data_source` | string | optional | 데이터 출처 (`audience-profile.md` §2 출처 4분류) |

#### 메타 필드

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `extracted_from` | string | ✅ | 항상 `"mice-meeting-minutes"` (체이닝 검증용) |
| `extraction_date` | ISO date | ✅ | 추출 일자 |
| `meeting_minutes_ref.meeting_id` | string | optional | 원본 미팅록 식별자 |
| `meeting_minutes_ref.section` | string | optional | 추출 위치 (예: "Action Items + 전략 메모") |

---

## 3. 출력 데이터 스키마 (`deck-content.json`)

sponsor-deck이 내부적으로 생성하는 콘텐츠 JSON. HTML 1차 + PPTX 2차의 single source. (`output-build-guide.md` §2 그대로 — 본 신규 파일은 입력 명시 위주, 출력은 기존 가이드 활용)

```json
{
  "meta": {
    "event_name": "TOBESOFT TECH FORUM 2026",
    "event_subtitle": "AI·Cloud·Enterprise Tech의 다음 10년",
    "event_date": "2026-09-15",
    "event_venue": "코엑스 컨벤션홀",
    "client_id": null,
    "naming_mode": "ko_first",
    "price_mode": "on_request",
    "color_mode": "dark_mixed",
    "deck_version": "v1.0",
    "is_provisional": false
  },
  "audience": {
    "kpis": [
      { "value": 5200, "unit": "명", "label": "예상 참가자", "source": "2024년 회차 + 14% 성장" },
      { "value": 32, "unit": "%", "label": "의사결정권자", "source": "자기 응답 데이터" },
      { "value": 23, "unit": "%", "label": "C-Level + 임원", "source": "직급 기반 분류" },
      { "value": 87, "unit": "%", "label": "B2B 비율", "source": "자기 응답" }
    ],
    "industry_distribution": [
      { "name": "IT·소프트웨어", "ratio": 42, "color": "2962FF" },
      { "name": "금융·보험", "ratio": 24, "color": "E91E63" },
      { "name": "제조·산업재", "ratio": 18, "color": "FF5722" },
      { "name": "헬스케어·바이오", "ratio": 10, "color": "00E676" },
      { "name": "기타", "ratio": 6, "color": "5A6270" }
    ],
    "decision_maker_ratio": 32,
    "data_source": "2024년 회차 등록 데이터 + 자기 응답"
  },
  "tiers": [
    {
      "id": "T1",
      "name_ko": "타이틀",
      "name_en": "Title",
      "slots": 1,
      "price": null,
      "price_display": "가격 별도 협의",
      "color_token": "--jc-point-magenta",
      "color_hex": "E91E63",
      "benefits_summary": [
        "행사명 결합권",
        "키노트 발표 30분",
        "메인 사이니지 8회",
        "VIP 만찬 단독 호스트",
        "부스 54㎡ 메인 동선"
      ]
    }
  ],
  "matrix": {
    "categories": [
      { "id": 1, "ko": "브랜딩 노출" },
      { "id": 5, "ko": "연사·세션 권리" },
      { "id": 7, "ko": "VIP·네트워킹" }
    ],
    "rows": [
      { "item": "메인 사이니지", "category_id": 1, "T1": "8회", "T2": "6회", "T3": "4회", "T4": "2회", "T5": "✓" },
      { "item": "키노트·세션", "category_id": 5, "T1": "키노트 30분", "T2": "메인 45분", "T3": "트랙 30분", "T4": "—", "T5": "—" },
      { "item": "VIP 만찬 좌석", "category_id": 7, "T1": "단독 10석", "T2": "6석", "T3": "—", "T4": "—", "T5": "—" }
    ],
    "slot_row": { "T1": "1석", "T2": "3석", "T3": "6석", "T4": "10석", "T5": "무제한" }
  },
  "roi_cases": [
    {
      "industry": "tech",
      "industry_label": "Tech 산업 스폰서 ROI",
      "premise": ["IT 참가자 약 2,184명", "IT 의사결정권자 약 655명"],
      "formula": ["부스 전환율 12% × 의사결정권자", "리드 전환율 35% 적용"],
      "estimate": {
        "headline": "리드 약 25~30건",
        "secondary": "PR 가치 약 KRW 25M"
      },
      "caption": "ⓘ 본 수치는 산업 벤치마크 기반 추정치이며, 실제 결과는 노출 환경·콘텐츠 품질에 따라 변동됩니다."
    },
    {
      "industry": "finance",
      "industry_label": "Finance 산업 스폰서 ROI",
      "premise": ["금융 참가자 약 1,248명", "C-Level + 임원 약 287명"],
      "formula": ["VIP 만찬 단독 직접 접점 8~10명", "1:1 미팅 평균 LTV × 5% 전환"],
      "estimate": {
        "headline": "직접 접점 약 8~10명",
        "secondary": "잠재 영업 가치 산업 벤치마크 기반"
      },
      "caption": "ⓘ 본 수치는 산업 벤치마크 기반 추정치이며, 실제 결과는 노출 환경·콘텐츠 품질에 따라 변동됩니다."
    }
  ],
  "section_8": {
    "type": "reference_cases",
    "data": [
      { "event_name": "[유사 행사명 1]", "year": 2023, "attendees": 4200, "sponsors": 12 },
      { "event_name": "[유사 행사명 2]", "year": 2024, "attendees": 5800, "sponsors": 15 }
    ]
  },
  "contact": {
    "headline": "지금 함께하실 수 있는 13개 슬롯이 남아있습니다",
    "next_steps": [
      "1. 견적 협의 — 본 사무국 담당자 연락",
      "2. Tier 선정 — 산업·예산 매칭 1:1 컨설팅",
      "3. 계약서 송부 — 2주 이내 신청 시 우선 배정"
    ],
    "manager_name": "[담당자 이름]",
    "manager_title": "[직급]",
    "manager_email": "[이메일]",
    "manager_phone": "[연락처]",
    "deadline": "2026-08-15"
  },
  "_sponsor_candidates_carried_over": [
    {
      "name": "[기업명1]",
      "industry": "tech",
      "tier_target": "T1",
      "priority": "high"
    }
  ]
}
```

### 3-1. 데이터 변환 룰 (sponsor-candidates.json → deck-content.json)

| 입력 필드 | 출력 위치 | 변환 룰 |
|----------|----------|---------|
| `event_meta.event_name` | `meta.event_name` | 그대로 |
| `event_meta.expected_attendees` | `audience.kpis[0].value` | 그대로. 1번째 KPI 자동 생성 |
| `event_meta.is_provisional_slots` | `meta.is_provisional` | 그대로. true 시 표지 푸터에 "잠정안" 자동 캡션 |
| `audience_hints.industry_distribution` | `audience.industry_distribution[]` | 한국명 매핑 + CHART_SERIES 색상 자동 할당 |
| `audience_hints.decision_maker_ratio` | `audience.kpis[1]` | "의사결정권자" 라벨로 KPI 생성 |
| `sponsor_candidates[]` | `_sponsor_candidates_carried_over` | 영업 우선순위 메타데이터로 보존 (S8 또는 내부용) |
| `sponsor_candidates[].industry` 빈도 분석 | `roi_cases[]` 산업 선택 | 상위 2~3개 산업 자동 선정 (roi-case-templates.md §8.1) |

---

## 4. 다른 스킬과의 인터페이스

### 4-1. 입력 (선택)

| 업스트림 스킬 | 산출물 | 본 스킬 활용 |
|-------------|--------|------------|
| `mice-meeting-minutes` | `sponsor-candidates.json` | 1차 입력 (선택 — 없으면 사용자 직접 대화 입력) |

### 4-2. 출력

본 스킬은 **영업 채널 종착점**이므로 다른 스킬의 입력으로 들어가지 않는다.

| 산출물 | 형식 | 용도 |
|--------|------|------|
| HTML 1차 슬라이드 데크 | 단일 .html 파일 | 영업 미팅 발표, 이메일 첨부, 인쇄 |
| PPTX 2차 영업 데크 | .pptx | 일반 영업 자료 |
| XLSX 매트릭스 (옵션) | .xlsx | 매트릭스 단독 첨부, 가격표 |

### 4-3. 다른 스킬과의 경계 명확화

| 스킬 | 청중 | 본 스킬과의 관계 |
|------|------|----------------|
| `mice-proposal` | 발주처 (행사 의뢰자) | **다른 청중 — 침범 금지**. 결합어("협찬 제안서") 시 본 스킬 우선 |
| `mice-meeting-minutes` | 내부 / 클라이언트 송부 | **업스트림** (sponsor-candidates 추출원) |
| `mice-rfp-analyzer` | RFP 분석 보고서 | 무관 |
| `mice-estimate` | 견적서 | 무관 — sponsor-deck은 영업 데크, 견적서는 별도 |
| `mice-dashboard` | 행사 결과 KPI | 무관 — sponsor-deck은 사전 영업, dashboard는 사후 |
| `pt-script` | PT 발표자 | 본 스킬 산출물 PPTX를 입력으로 받을 수 있음 (체이닝 가능) |
| `jc-design-system` | 디자인 토큰 | **참조 의존** (signature-tokens·client-overlays 로드) |

---

## 5. CLI 사용 예시

### 5-1. 입력 JSON 파일 활용

```bash
# 사용자 메시지 예시
"sponsor-candidates.json 첨부합니다. 이 데이터로 TOBESOFT TECH FORUM 2026 스폰서 데크 만들어주세요. color_mode는 dark_mixed로."
```

본 스킬은 다음 절차를 따른다:
1. `sponsor-candidates.json` 로드 → 스키마 검증 (`$schema` 필드 확인)
2. `event_meta` 추출 → S1 표지·S2 본문 자동 구성
3. `audience_hints` 추출 → S3 SVP-4 KPI + SVP-5 산업 분포 자동 생성
4. `sponsor_candidates[]` 산업 빈도 분석 → 상위 2~3개 산업 ROI 케이스 자동 선정 (S7)
5. `roi-case-templates.md` 의 해당 산업 템플릿 로드 → SVP-3 ROI 3단 카드 생성
6. 사용자에게 6축 분석 요약 제시 → 승인 후 HTML 빌드

### 5-2. 대화 기반 입력

`sponsor-candidates.json` 없이 직접 대화로 정보 수집한 경우, 본 스킬이 내부적으로 동일 구조의 콘텐츠 JSON을 생성한다.

```
사용자: "스폰서 데크 만들어줘. 행사는 TOBESOFT TECH FORUM 2026, 9월 15일 코엑스. 5,200명 예상."
↓
본 스킬: event_meta 수집 → audience_hints 수집 → sponsor_candidates 수집 →
        sponsor-candidates.json 구조와 동일한 내부 객체 생성 →
        deck-content.json 변환 → HTML/PPTX 빌드
```

---

## 6. 스키마 검증 룰

본 스킬은 입력 `sponsor-candidates.json` 을 다음 룰로 검증한다.

### 6-1. 필수 필드 누락 검증

```javascript
const requiredFields = [
  "event_meta.event_name",
  "event_meta.event_date",
  "event_meta.event_venue",
  "event_meta.event_type",
  "event_meta.organizer",
  "event_meta.is_provisional_slots",
  "sponsor_candidates",
  "extracted_from",
  "extraction_date"
];

function validateInput(json) {
  const errors = [];
  for (const field of requiredFields) {
    const value = field.split(".").reduce((obj, key) => obj?.[key], json);
    if (value === undefined || value === null) {
      errors.push(`Missing required field: ${field}`);
    }
  }
  if (!Array.isArray(json.sponsor_candidates) || json.sponsor_candidates.length === 0) {
    errors.push("sponsor_candidates must be non-empty array");
  }
  if (json.extracted_from !== "mice-meeting-minutes") {
    errors.push("extracted_from must be 'mice-meeting-minutes' (chaining contract)");
  }
  return errors;
}
```

### 6-2. enum 값 검증

```javascript
const validEventTypes = ["conference", "exhibition", "forum", "corporate", "festival", "gala"];
const validIndustries = ["tech", "finance", "cpg", "b2b", "public"];
const validTiers = ["T1", "T2", "T3", "T4", "T5", "T6"];
const validPriorities = ["high", "med", "low"];

function validateEnums(json) {
  const errors = [];
  if (!validEventTypes.includes(json.event_meta?.event_type)) {
    errors.push(`event_type must be one of: ${validEventTypes.join(", ")}`);
  }
  (json.sponsor_candidates || []).forEach((c, i) => {
    if (!validIndustries.includes(c.industry)) {
      errors.push(`sponsor_candidates[${i}].industry must be one of: ${validIndustries.join(", ")}`);
    }
    if (!validTiers.includes(c.tier_target)) {
      errors.push(`sponsor_candidates[${i}].tier_target must be one of: ${validTiers.join(", ")}`);
    }
    if (!validPriorities.includes(c.priority)) {
      errors.push(`sponsor_candidates[${i}].priority must be one of: ${validPriorities.join(", ")}`);
    }
  });
  return errors;
}
```

### 6-3. audience_hints 비율 합계 검증

```javascript
function validateIndustryRatios(json) {
  const dist = json.audience_hints?.industry_distribution;
  if (!dist) return [];
  const sum = Object.values(dist).reduce((a, b) => a + b, 0);
  if (Math.abs(sum - 100) > 1) {  // 1% 오차 허용
    return [`industry_distribution sum must be 100, got ${sum}`];
  }
  return [];
}
```

---

## 7. 회사 종속 표현 검증 (입력 단계)

입력 `sponsor-candidates.json` 에 다음 표현이 포함되면 사용자 경고 + 익명화 권고.

| 검출 패턴 | 처리 |
|----------|------|
| `event_meta.organizer` 가 자기 회사명 | 클라이언트 토큰으로 외부 주입 권고 |
| `sponsor_candidates[].notes` 에 회사 종속 표현 ("당사", "엠앤씨", "M&C") | 일반 표현으로 치환 |
| `audience_hints.data_source` 에 데이터 파트너사 실명 | "데이터 파트너사 명함 데이터 기반 분석" 으로 치환 (audience-profile.md §7) |

### 7-1. 검증 함수 예시

```javascript
function validateCompanyMentions(json) {
  const forbidden = ["엠앤씨", "M&C커뮤니케이션즈", "M&C", "리멤버앤컴퍼니"];
  const warnings = [];

  function scan(obj, path) {
    if (typeof obj === "string") {
      forbidden.forEach(term => {
        if (obj.includes(term)) {
          warnings.push(`Forbidden company mention "${term}" at ${path}`);
        }
      });
    } else if (typeof obj === "object" && obj !== null) {
      for (const [k, v] of Object.entries(obj)) {
        scan(v, `${path}.${k}`);
      }
    }
  }
  scan(json, "$");
  return warnings;
}
```

---

## 8. 통합 검증 체크리스트

본 스킬 빌드 직전 자가검증 체크리스트:

- [ ] `sponsor-candidates.json` 의 `$schema` 가 `mice-sponsor-deck/v2.0` 인가
- [ ] `extracted_from` 이 `mice-meeting-minutes` 인가
- [ ] `event_meta` 필수 6필드 (event_name, event_date, event_venue, event_type, organizer, is_provisional_slots) 모두 존재
- [ ] `sponsor_candidates` 가 비어있지 않은 배열
- [ ] 각 `sponsor_candidates[i]` 의 enum 필드 (industry, tier_target, priority) 가 유효 값
- [ ] (선택) `audience_hints.industry_distribution` 합계 100% (±1% 오차 허용)
- [ ] 회사 종속 표현 0건 (자기 회사명, 데이터 파트너 실명)

---

## 9. 다음 단계 (sponsor-deck 빌드 진입)

검증 통과 시 본 스킬의 표준 워크플로우 진입:

1. **Phase 1 정보 수집** 자동 완료 (JSON에서 모두 추출)
2. **Phase 2 6축 분석** 자동 매핑
3. **Phase 3 Tier 표준 적용** — `tier-framework.md` + `sponsor_candidates[].tier_target` 빈도 분석
4. **Phase 4 매트릭스** — `benefit-catalog.md` + 행사 유형별 우선순위
5. **Phase 5 ROI 케이스** — `roi-case-templates.md` + `sponsor_candidates[].industry` 상위 2~3종
6. **Phase 6 슬라이드 구조** — `slide-structure.md` + 행사 규모 기반 가감
7. **Phase 7 HTML 빌드** — `assets/sponsor-deck-template-light.html` 또는 `-dark.html`
8. **Phase 8 PPTX 변환** — `visual-patterns.md` + (color_mode=dark_mixed 시) `dark-mode-patterns.md`

---

## 10. 함께 보는 문서

| 파일 | 내용 |
|------|------|
| `visual-patterns.md` | 7종 비주얼 패턴 SVP-1~SVP-7 (출력 HTML/PPTX) |
| `dark-mode-patterns.md` | 다크 5종 (color_mode=dark_mixed 시) |
| `tier-framework.md` | Tier 5단 + 1트랙 (sponsor_candidates[].tier_target 매핑 베이스) |
| `roi-case-templates.md` | 산업 5종 ROI 템플릿 (sponsor_candidates[].industry 매핑 베이스) |
| `audience-profile.md` | 청중 데이터 표기 룰 (audience_hints 매핑 베이스) |
| `output-build-guide.md` | HTML 1차 + PPTX 2차 빌드 워크플로우 |
| `slide-structure.md` | 표준 12~18 슬라이드 구조 |
