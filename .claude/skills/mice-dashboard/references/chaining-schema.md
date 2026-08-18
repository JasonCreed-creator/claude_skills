# 체이닝 스키마 (chaining-schema)

**참조**: master-plan §5-1 (풀 워크플로우 체이닝)
**적용 범위 (Sprint 2)**: 입출력 JSON 스키마 정의. 실제 호출 코드 통합은 Phase 4 통합 검증 시.

mice-dashboard 가 다른 MICE 스킬과 데이터를 주고받기 위한 JSON 스키마. 풀 워크플로우상 **마지막 단계** (행사 종료 후 결과 분석).

---

## 1. 풀 워크플로우상의 위치

```
[RFP 원문]
     ↓
mice-rfp-analyzer ──→ 분석 보고서 + 평가 매트릭스
     ↓
mice-proposal ──────→ 제안서 PPTX
     ↓
mice-estimate ──────→ 견적서 XLSX
     ↓
pt-script ──────────→ 발표 대본 DOCX
     ↓ (행사 종료 후)
mice-dashboard ─────→ 결과 대시보드 HTML + PDF        ⭐ 본 스킬
     ↑ (시리즈 누적 데이터)
mice-meeting-minutes (시리즈)
```

본 스킬은 **풀 워크플로우의 마지막 단계** + **mice-meeting-minutes 시리즈 데이터 수신** 가능.

---

## 2. 입력 스키마

### 2.1 입력 1: 직접 데이터 (Excel/CSV)

기본 입력. v1과 동일.

```python
# Python 측
import pandas as pd
df = pd.read_excel('/mnt/user-data/uploads/event_results.xlsx')
# 또는
df = pd.read_csv('/mnt/user-data/uploads/event_results.csv')
```

→ 컬럼명 + 데이터 분석으로 KPI/차트 자동 생성 (kpi-patterns.md 참조).

### 2.2 입력 2: mice-meeting-minutes 시리즈 데이터

회의 시리즈 누적 데이터 → 대시보드:

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-meeting-minutes",
  "version": "v2.x.x",
  "seriesType": "kickoff_to_postmortem",
  "seriesName": "REMEMBER SUMMIT 2026 정기 미팅",
  "rounds": [
    {
      "round": 1,
      "date": "2026-03-01",
      "actionItemsTotal": 12,
      "actionItemsClosed": 12,
      "decisionsCount": 5,
      "risksOpen": 3
    },
    {
      "round": 2,
      "date": "2026-04-01",
      "actionItemsTotal": 18,
      "actionItemsClosed": 16,
      "decisionsCount": 7,
      "risksOpen": 2
    }
    // ...
  ],
  "metadata": {
    "projectTitle": "REMEMBER SUMMIT 2026",
    "client": "(외부 주입)"
  }
}
```

→ Action 종결률 추이, 결정 사항 누적, 리스크 해소 추이를 자동 시각화.

### 2.3 입력 3: mice-estimate 출력 (예산 대비 실적)

`mice-estimate` 의 견적 산출 결과 + 실제 행사 비용:

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-estimate",
  "version": "v2.0",
  "projectTitle": "REMEMBER SUMMIT 2026",
  "totalAmount": 83750000,
  "sections": {
    "s1_venue": 18000000,
    "s2_system": 10700000,
    "s3_design": 4500000,
    "s4_operations": 1800000,
    "s5_pco": 9750000,
    "ot_options": 0,
    "rsvpPkg": 4000000,
    "showup": 35000000
  },
  // 행사 종료 후 추가 주입:
  "actualSpending": {
    "s1_venue": 18500000,
    "s2_system": 10200000,
    "s3_design": 4500000,
    "s4_operations": 2100000,
    "s5_pco": 9750000,
    "ot_options": 1500000,
    "rsvpPkg": 4000000,
    "showup": 35000000
  }
}
```

→ 섹션별 예산 vs 실적 차이 차트 (스택드 바 또는 매트릭스 인포그래픽) 자동 생성.

---

## 3. 출력 스키마

mice-dashboard 는 풀 워크플로우의 **종착점**이지만, 외부 시스템·다음 행사 기획에 전달할 수 있는 분석 결과 JSON 을 부산물로 산출:

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-dashboard",
  "version": "v2.0",
  "projectTitle": "행사명",
  "generatedAt": "2026-XX-XX",
  "outputs": {
    "html": "/mnt/user-data/outputs/dashboard_YYYYMMDD.html",
    "pdf":  "/mnt/user-data/outputs/dashboard_YYYYMMDD.pdf"
  },
  "kpis": [
    {"name": "총 참가자 수", "value": 1850, "unit": "명", "delta": 12.5, "deltaUnit": "%", "vs": "전년"},
    {"name": "전체 만족도", "value": 4.3, "unit": "점/5", "delta": 0.3, "deltaUnit": "점"}
  ],
  "insights": [
    "전년 대비 참가자 12% 증가, 신규 등록자 비중 38%",
    "F&B 만족도가 가장 높음 (4.7/5.0), 네트워킹은 보완 필요 (3.2/5.0)",
    "예산 대비 실 집행률 102% — 추가옵션 1.5M 초과"
  ],
  "theme": {
    "mode": "light",
    "tone": "business",
    "overlay": "remember"
  },
  "chartCount": 5,
  "infographicCount": 2
}
```

→ 차기 행사 기획 시 mice-proposal·mice-rfp-analyzer 가 본 출력을 입력으로 받아 "전년 실적 기반 제안서" 작성 가능 (선순환).

---

## 4. 직렬화 헬퍼 (선택)

```python
def to_chain_payload(dashboard_meta: dict) -> dict:
    """대시보드 생성 결과를 ChainPayload 형식으로 출력."""
    return {
        '$schema': 'ChainPayload/v1',
        'source': 'mice-dashboard',
        'version': 'v2.0',
        'projectTitle': dashboard_meta.get('project_title', ''),
        'generatedAt': dashboard_meta.get('generated_at', ''),
        'outputs': {
            'html': dashboard_meta.get('html_path', ''),
            'pdf':  dashboard_meta.get('pdf_path', ''),
        },
        'kpis': dashboard_meta.get('kpis', []),
        'insights': dashboard_meta.get('insights', []),
        'theme': dashboard_meta.get('theme', {}),
        'chartCount': dashboard_meta.get('chart_count', 0),
        'infographicCount': dashboard_meta.get('infographic_count', 0),
    }
```

본 헬퍼는 Phase 4 통합 검증 시 `scripts/build_dashboard.py` 또는 별도 `scripts/chain_io.py` 로 분리.

---

## 5. 본 Sprint 의 적용 범위

| 항목 | 적용 |
|---|---|
| 입출력 JSON 스키마 정의 (본 문서) | ✅ |
| ChainPayload 직렬화 함수 (dashboard 측) | ⏳ Phase 4 |
| mice-meeting-minutes·mice-estimate 측 출력 함수 | 각 스킬 강화 Sprint |
| 풀 워크플로우 end-to-end 검증 | Phase 4 통합 검증 |

본 Sprint 는 **계약 정의**까지.

---

## 6. 트리거 동작 분기 (자동 라우팅)

```python
def detect_input_source(input_payload) -> str:
    """입력 형식으로 처리 분기 결정."""
    if isinstance(input_payload, dict) and '$schema' in input_payload:
        return input_payload.get('source')   # mice-meeting-minutes, mice-estimate
    if hasattr(input_payload, 'read'):
        # 파일 객체 (Excel/CSV)
        return 'file_upload'
    if isinstance(input_payload, (list, dict)):
        return 'inline_data'
    return 'unknown'
```

각 source 에 맞춰 데이터 파싱 + 차트·인포그래픽 자동 선택 분기.
