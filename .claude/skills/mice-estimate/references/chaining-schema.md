# 체이닝 가이드 (chaining-guide)

**참조**: master-plan-2026-05-25.md §5-1 (풀 워크플로우 체이닝)
**적용 범위 (Sprint 1)**: 입출력 JSON 스키마 정의. 실제 호출 코드 통합은 Phase 4 통합 검증 시.

mice-estimate가 다른 MICE 스킬과 데이터를 주고받기 위한 JSON 스키마와 워크플로우상의 위치를 정의한다.

> **봉투 정본**: 공통 `ChainPayload/v1` 봉투 구조(`$schema`·`source`·`version`·`generatedAt` 등 공통 메타)와 전체 워크플로우·표준 규약은 [jc-design-system/references/chaining-protocol.md](../../jc-design-system/references/chaining-protocol.md) 참조.
> 요약: 모든 체이닝 JSON은 최상위에 `"$schema": "ChainPayload/v1"` + `source`(생산 스킬) + `version` 을 두고, 그 아래에 아래 정의된 mice-estimate 고유 페이로드를 평탄하게 담는다. 본 문서는 mice-estimate **고유 입출력 페이로드 매핑**만 정의한다.

---

## 1. 풀 워크플로우상의 위치

```
[RFP 원문]
     ↓
mice-rfp-analyzer ──→ analysis-report.docx + evaluation-matrix.xlsx
                     ↓ GO 판정 시
                  (ChainPayload JSON)
                     ↓
mice-proposal ──────→ proposal.pptx
                     ↓ 제안 확정 시
                  (ChainPayload JSON: eventScale + venue + options)
                     ↓
mice-estimate ──────→ estimate.xlsx       ⭐ 본 스킬
                     ↓
                  (ChainPayload JSON: totalAmount + sections)
                     ↓
pt-script ──────────→ presentation-script.docx
mice-dashboard ─────→ result-dashboard.html
```

본 스킬은 **3번째 단계** (rfp-analyzer/proposal로부터 입력 받음, pt-script·dashboard로 출력 전달).

---

## 2. 입력 스키마 — `mice-proposal` 에서 받기

mice-proposal이 제안서 PPTX 작성 후, 견적 단계로 전환할 때 생성하는 JSON.

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-proposal",
  "version": "v2.x.x",
  "projectTitle": "2026 관광공모전 및 박람회",
  "client": "한국관광공사",
  "eventDate": "2026-12-16",
  "eventScale": {
    "target": 100,
    "guarantee": 90
  },
  "venue": {
    "type": "5star",
    "region": "서울 강남",
    "name": "조선팰리스 강남",
    "rental": null
  },
  "options": {
    "video": false,
    "emcee": true,
    "souvenir": true,
    "scaler4k": false,
    "survey": false,
    "photowall_basic": false,
    "photowall_premium": false,
    "photo": false,
    "aving": false
  },
  "boothCount": 0,
  "format": "mnc"
}
```

### 필드 매핑 (input JSON → calc_estimate input)

| ChainPayload 필드 | → calc_estimate.c 키 | 변환 |
|---|---|---|
| `eventScale.target` | `target` | 그대로 |
| `eventScale.guarantee` | `guarantee` | None이면 target |
| `venue.rental` | `venueRental` | None이면 자동 산출 |
| `venue.name` | `venueName` | 그대로 |
| `options` | `options` | 그대로 (9개 옵션 키) |
| `boothCount` | `boothCount` | 그대로 |
| `format` | (양식 선택) | `mnc` / `remember` 분기 |
| `projectTitle`, `client`, `eventDate` | (Excel 헤더 채우기) | M&C: A3·B3 등에 사용 |

---

## 3. 입력 스키마 — `mice-rfp-analyzer` 에서 받기

RFP 분석 단계 — 베뉴·옵션이 미정일 수 있어 일부 필드 옵셔널.

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-rfp-analyzer",
  "version": "v1.x.x",
  "projectTitle": "제목",
  "client": "발주처명",
  "rfpId": "공고번호",
  "budgetRange": {
    "min": 50000000,
    "max": 120000000,
    "currency": "KRW",
    "vatIncluded": true
  },
  "evaluationCriteria": [
    {"name": "가격", "weight": 30},
    {"name": "기술/실적", "weight": 70}
  ],
  "eventScale": {
    "target": 100,
    "guarantee": 80
  },
  "venue": null,
  "options": null,
  "boothCount": 0,
  "format": "mnc",
  "notes": "RFP 단계 — 베뉴·옵션 TBD. 표준값 추정."
}
```

### 처리 규칙

- `venue=null` → `venueRental=None` → target × 180,000 자동 산출
- `options=null` → 모든 옵션 False
- 출력 JSON의 `metadata.estimatedFrom = "rfp_default"` 플래그 추가
- `budgetRange`는 견적 산출 후 비교용 (calc_estimate의 입력은 아님)

---

## 4. 출력 스키마 — pt-script·mice-dashboard 로 전달

mice-estimate가 견적 산출 + Excel 생성 후, 후속 스킬에 전달하는 JSON.

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-estimate",
  "version": "v2.0",
  "projectTitle": "행사명",
  "format": "mnc",
  "isCustom": false,
  "totalAmount": 83750000,
  "totalAmountVat": 92125000,
  "sections": {
    "s1_venue":      18000000,
    "s2_system":     10700000,
    "s3_design":      4500000,
    "s4_operations":  1800000,
    "s5_pco":         9750000,
    "ot_options":           0,
    "rsvpPkg":        4000000,
    "showup":        35000000
  },
  "breakdown": {
    "sys": {"video": 2000000, "scaler4k": 2500000, "audio": 2000000,
            "engineer": 1000000, "presentation": 1200000,
            "registration": 1000000, "misc": 1000000},
    "des": {"env": 2500000, "web": 1000000, "kv": 1000000},
    "ops": {"desk": 500000, "ops": 900000, "insurance": 400000},
    "ot":  {}
  },
  "optionsApplied": {
    "video": false, "emcee": false, "souvenir": false,
    "scaler4k": false, "survey": false,
    "photowall_basic": false, "photowall_premium": false,
    "photo": false, "aving": false
  },
  "metadata": {
    "target": 100,
    "guarantee": 100,
    "venueName": "조선팰리스 강남",
    "createdAt": "2026-05-25",
    "estimatedFrom": "user_input"
  },
  "estimateFile": "C:/path/to/MC견적서_xxx_260525.xlsx"
}
```

### `estimatedFrom` 가능 값

| 값 | 의미 |
|---|---|
| `user_input` | 사용자가 채팅으로 직접 항목·단가 입력 (v1 방식) |
| `auto_calc` | calc_estimate 자동 산출 |
| `rfp_default` | mice-rfp-analyzer 입력 + 베뉴·옵션 표준값 추정 |
| `proposal_chain` | mice-proposal 입력 + 자동 산출 |

---

## 5. 후속 스킬에서의 활용

### pt-script (발표 대본)
- `sections.s1_venue` 등을 발표 시 "비용 구조 슬라이드"에 인용
- `totalAmount`, `totalAmountVat` 를 견적 총액 멘트로 사용

### mice-dashboard (결과 대시보드)
- 행사 종료 후 실제 비용과 비교 → 예산 대비 실적 KPI 카드
- `sections` 키별 누적 차트

---

## 6. 본 Sprint의 적용 범위

| 항목 | 적용 여부 |
|---|---|
| 입출력 JSON 스키마 정의 (본 문서) | ✅ |
| ChainPayload 직렬화 함수 (mice-estimate 측) | ⏳ Phase 4 통합 검증 시 |
| mice-proposal·mice-rfp-analyzer 측에서 출력 함수 | 각 스킬 강화 Sprint에서 |
| 풀 워크플로우 end-to-end 검증 | Phase 4 통합 검증 |

본 Sprint는 **계약 정의**까지. 실제 호출 코드는 모든 스킬이 v2 강화 완료 후 Phase 4 통합에서 작성.

---

## 7. 직렬화 헬퍼 (선택)

calc_estimate 결과를 그대로 ChainPayload 형식으로 변환하는 헬퍼:

```python
def to_chain_payload(result: dict, meta: dict) -> dict:
    """calc_estimate 결과 → ChainPayload/v1 출력."""
    return {
        '$schema': 'ChainPayload/v1',
        'source': 'mice-estimate',
        'version': 'v2.0',
        'projectTitle': meta.get('projectTitle', ''),
        'format': meta.get('format', 'mnc'),
        'isCustom': result['isCustom'],
        'totalAmount': result['pk'],
        'totalAmountVat': result['pkVat'],
        'sections': {
            's1_venue':      result['s1'],
            's2_system':     result['s2'],
            's3_design':     result['s3'],
            's4_operations': result['s4'],
            's5_pco':        result['s5'],
            'ot_options':    result['ot'],
            'rsvpPkg':       result['rsvpPkg'],
            'showup':        result['showup'],
        },
        'breakdown': {
            'sys': result['sysBreakdown'],
            'des': result['desBreakdown'],
            'ops': result['opsBreakdown'],
            'ot':  result['otBreakdown'],
        },
        'optionsApplied': result['optionsApplied'],
        'metadata': {
            'target':         result['t'],
            'guarantee':      result['g'],
            'venueName':      meta.get('venueName', ''),
            'createdAt':      meta.get('createdAt', ''),
            'estimatedFrom':  meta.get('estimatedFrom', 'user_input'),
        },
        'estimateFile': meta.get('estimateFile', ''),
    }
```

본 헬퍼는 Phase 4 통합 시 `calc_estimate.py` 또는 별도 `chain_payload.py`로 분리 예정.
