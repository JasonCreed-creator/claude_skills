# Chaining Schema (v2.0) — mice-proposal → pt-script

본 문서는 pt-script v2.0 가 mice-proposal 의 산출물을 자동으로 받아 발표 대본을 생성하는 체이닝 워크플로우와 입력 JSON 스키마를 정의한다.

---

## 1. 체이닝 워크플로우 전체

```
┌──────────────────────────────────────────────────────────────┐
│ Step 1: mice-proposal (v2.1.1)                               │
│ - RFP 분석 결과 또는 사용자 직접 입력 기반                    │
│ - 12~22 슬라이드 PPTX 생성                                    │
│ - 슬라이드 노트에 메타 안내 자동 삽입 (이미지·폰트)            │
│ - (선택) proposal-meta.json 함께 생성                         │
└─────────────────────────┬────────────────────────────────────┘
                          ↓ proposal.pptx (+ proposal-meta.json)
┌──────────────────────────────────────────────────────────────┐
│ Step 2: pt-script (본 스킬)                                  │
│ - extract_notes.py 로 PPTX 분석 → notes-extraction.json       │
│ - 메타 노트 필터링 + speaker notes 우선순위 적용              │
│ - proposal-meta.json (있으면) → 발표 컨텍스트 자동 주입       │
│ - 슬라이드 유형 자동 추론 → 시간 배분 + 멘트 패턴 적용         │
│ - build_script.py 로 docx 생성 (jc-design 토큰 적용)          │
└─────────────────────────┬────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ Step 3: 최종 산출물                                          │
│ - 발표대본.docx (현장 사용 종착점)                            │
│ - (옵션) notes-extraction.json 동봉 (백업)                    │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. 입력 형태

### 2-1. 단독 PPTX 입력 (최소 케이스)

```
사용자: "proposal.pptx 첨부합니다. 20분 발표 대본 만들어주세요."
```

본 스킬 동작:
1. `extract_notes.py proposal.pptx --out /tmp/notes.json`
2. Phase 2 사용자 확인 (발표 유형·시간·톤·청중)
3. `build_script.py --notes /tmp/notes.json --minutes 20 ...`

### 2-2. PPTX + 메타 JSON 페어 (권장 케이스)

```
사용자: "proposal.pptx + proposal-meta.json 첨부합니다."
```

본 스킬 동작:
1. `proposal-meta.json` 파싱 → 발표 시간·발표자 역할·청중 등 자동 주입
2. `extract_notes.py proposal.pptx --out /tmp/notes.json`
3. Phase 2 사용자 확인 **생략 가능** (메타 JSON 에 모든 정보 있을 시)
4. `build_script.py --notes /tmp/notes.json --meta /tmp/proposal-meta.json ...`

---

## 3. 입력 JSON 스키마 — `proposal-meta.json` (선택)

### 3-1. 표준 스키마

```json
{
  "$schema": "pt-script/v2.0",
  "proposal_meta": {
    "client_name": "[발주처명]",
    "rfp_title": "TOBESOFT TECH FORUM 2026 운영 용역",
    "rfp_id": "TOBESOFT-2026-PT-001",
    "presentation_minutes": 20,
    "presentation_type": "bidding_pt",
    "presenter_role": "발표자",
    "presenter_name": null,
    "audience_type": "발주처 심사위원",
    "audience_size": 7,
    "tone": "formal",
    "qna_included": true,
    "qna_minutes": 4,
    "client_id": null
  },
  "extracted_from": "mice-proposal",
  "mice_proposal_version": "v2.1.1",
  "pptx_source": "proposal.pptx",
  "generated_at": "2026-05-27T10:00:00"
}
```

### 3-2. 필드 정의

#### proposal_meta (필수 컨테이너)

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `client_name` | string | ✅ | 발주처명 (표지·인사말에 활용). **자기 회사명 금지 — 외부 주입 변수만** |
| `rfp_title` | string | ✅ | 비딩 제안 제목 (표지에 활용) |
| `rfp_id` | string | optional | RFP 식별자 (메타데이터) |
| `presentation_minutes` | number | ✅ | 전체 발표 시간 (분). 1 이상 정수 |
| `presentation_type` | enum | ✅ | `bidding_pt` \| `conference` \| `forum` \| `corporate_event` \| `mc` \| `general_business` |
| `presenter_role` | string | optional | 발표자 직책 (예: "프로젝트 매니저", "발표자"). **실명·소속사명 금지** |
| `presenter_name` | string | optional | 발표자 이름. **회사 종속 표현 금지 — 사용자 직접 입력만** |
| `audience_type` | string | ✅ | 청중 분류 (예: "발주처 심사위원", "업계 전문가", "임직원") |
| `audience_size` | number | optional | 청중 규모 (Q&A 작성 시 활용) |
| `tone` | enum | ✅ | `formal` (격식체) \| `semi_formal` (반격식체) \| `casual` (캐주얼) |
| `qna_included` | boolean | ✅ | Q&A 섹션 포함 여부 |
| `qna_minutes` | number | optional | Q&A 시간 (분). 기본값: `presentation_minutes * 0.2` |
| `client_id` | string | optional | 클라이언트 오버레이 ID (예: "darktrace_korea"). null 이면 JC 시그니처 기본 |

#### 메타 필드

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `$schema` | string | ✅ | 항상 `"pt-script/v2.0"` |
| `extracted_from` | string | ✅ | 항상 `"mice-proposal"` (체이닝 검증용) |
| `mice_proposal_version` | string | optional | 업스트림 버전 (예: "v2.1.1") |
| `pptx_source` | string | ✅ | 동봉된 PPTX 파일명 |
| `generated_at` | ISO 8601 | optional | 메타 JSON 생성 시각 |

### 3-3. enum 값 검증

```python
VALID_PRESENTATION_TYPES = ["bidding_pt", "conference", "forum", "corporate_event", "mc", "general_business"]
VALID_TONES = ["formal", "semi_formal", "casual"]

def validate_meta(meta_json):
    errors = []
    pm = meta_json.get("proposal_meta", {})

    # 필수 필드
    required = ["client_name", "rfp_title", "presentation_minutes",
                "presentation_type", "audience_type", "tone", "qna_included"]
    for f in required:
        if pm.get(f) is None:
            errors.append(f"Missing required field: proposal_meta.{f}")

    # enum 검증
    if pm.get("presentation_type") not in VALID_PRESENTATION_TYPES:
        errors.append(f"presentation_type must be one of: {VALID_PRESENTATION_TYPES}")
    if pm.get("tone") not in VALID_TONES:
        errors.append(f"tone must be one of: {VALID_TONES}")

    # 숫자 검증
    if pm.get("presentation_minutes") is not None and pm["presentation_minutes"] < 1:
        errors.append("presentation_minutes must be >= 1")

    # 체이닝 검증
    if meta_json.get("extracted_from") != "mice-proposal":
        errors.append("extracted_from must be 'mice-proposal'")

    return errors
```

---

## 4. PPTX 입력 — 단독 사용

`proposal-meta.json` 없이 PPTX 만 받은 경우:

1. `extract_notes.py` 가 슬라이드 분석
2. 메타 정보를 Phase 2 사용자 확인으로 수집:
   - 발표 시간 → 사용자 입력 필수
   - 발표 유형 → 슬라이드 제목 키워드 기반 자동 추론 (`bidding_pt` 기본)
   - 톤 → 격식체 기본 (`formal`)
   - 청중 → 사용자 입력 (기본 "심사위원")
3. 수집한 정보로 내부 `proposal_meta` 객체 생성 → build_script.py 호출

### 4-1. 발표 유형 자동 추론 룰 (PPTX 단독 입력 시)

```python
def infer_presentation_type(pptx_titles):
    """슬라이드 제목들에서 발표 유형 추론."""
    titles = " ".join(pptx_titles).lower()

    # 비딩/제안 키워드
    if any(kw in titles for kw in ["제안", "비딩", "rfp", "수주", "proposal"]):
        return "bidding_pt"
    # 포럼/기조
    if any(kw in titles for kw in ["기조", "keynote", "포럼", "forum"]):
        return "forum"
    # MC/사회
    if any(kw in titles for kw in ["환영", "사회자", "mc", "프로그램 안내", "큐시트"]):
        return "mc"
    # 컨퍼런스
    if any(kw in titles for kw in ["발표", "presentation", "session", "session", "콘퍼런스"]):
        return "conference"
    # 기본
    return "general_business"
```

---

## 5. 다른 스킬과의 인터페이스

### 5-1. 입력 (upstream)

| 업스트림 스킬 | 산출물 | 본 스킬 활용 |
|-------------|--------|------------|
| `mice-proposal` (v2.1.1+) | `proposal.pptx` (+ 선택 `proposal-meta.json`) | **1차 입력 (권장)** |
| `mice-meeting-minutes` | transcript 정리 .docx | 2차 입력 (발표용 transcript 정리 시) — 비공식 |

### 5-2. 출력 (downstream)

본 스킬의 출력 `.docx` 는 **현장 사용 종착점**. 다른 스킬의 입력으로 들어가지 않는다.

| 산출물 | 형식 | 용도 |
|--------|------|------|
| 발표대본.docx | .docx | 발표자가 현장 인쇄·태블릿 휴대 |
| notes-extraction.json (옵션) | .json | 백업·이후 재가공 |

### 5-3. 다른 스킬과의 경계 명확화

| 스킬 | 본 스킬과의 관계 |
|------|----------------|
| `mice-proposal` | **업스트림** (PPTX + 메타 JSON 페어 제공) |
| `mice-rfp-analyzer` | 무관 — RFP 분석 보고서는 본 스킬 입력이 아님 |
| `mice-estimate` | 무관 — 견적서와 발표 대본은 별도 산출물 |
| `mice-dashboard` | 무관 — 사후 결과 KPI 와 사전 발표 대본은 다름 |
| `mice-sponsor-deck` | sponsor-deck PPTX 를 본 스킬 입력으로 활용 가능 (협찬 영업 PT 대본 생성 시) |
| `mice-meeting-minutes` | 무관 — 회의록은 발표용이 아님 |
| `jc-design-system` | **참조 의존** (`jc-design-mapping.md` 가 토큰 매핑) |

---

## 6. CLI 사용 예시

### 6-1. 풀 워크플로우 (mice-proposal → pt-script)

```bash
# Step 1: mice-proposal 산출물 받기
# (mice-proposal 스킬이 /mnt/user-data/outputs/proposal.pptx + proposal-meta.json 생성)

# Step 2: PPTX 분석
python scripts/extract_notes.py \
  /mnt/user-data/uploads/proposal.pptx \
  --out /tmp/notes-extraction.json

# Step 3: 발표 대본 빌드
python scripts/build_script.py \
  --notes /tmp/notes-extraction.json \
  --meta /mnt/user-data/uploads/proposal-meta.json \
  --out /mnt/user-data/outputs/발표대본.docx
```

### 6-2. PPTX 단독 입력

```bash
python scripts/extract_notes.py /mnt/user-data/uploads/proposal.pptx --out /tmp/notes.json

# 사용자 확인 후 수동 옵션 전달
python scripts/build_script.py \
  --notes /tmp/notes.json \
  --minutes 20 \
  --presentation-type bidding_pt \
  --tone formal \
  --presenter-role "발표자" \
  --audience-type "발주처 심사위원" \
  --client-name "[발주처명]" \
  --rfp-title "TOBESOFT TECH FORUM 2026 운영 제안" \
  --out /mnt/user-data/outputs/발표대본.docx
```

### 6-3. 대화 기반 입력

`proposal-meta.json` 없이 직접 대화로 정보 수집한 경우, 본 스킬이 내부적으로 동일 구조의 메타 객체를 생성 후 build_script.py 에 전달.

---

## 7. 스키마 검증 룰

### 7-1. 입력 검증 체크리스트

본 스킬 빌드 직전 자가검증:

- [ ] `proposal-meta.json` 의 `$schema` 가 `pt-script/v2.0` 인가 (메타 JSON 입력 시)
- [ ] `extracted_from` 이 `mice-proposal` 인가 (메타 JSON 입력 시)
- [ ] `proposal.pptx` 가 python-pptx 로 정상 파싱되는가
- [ ] `proposal_meta` 필수 7필드 (client_name, rfp_title, presentation_minutes, presentation_type, audience_type, tone, qna_included) 모두 존재 (메타 JSON 입력 시)
- [ ] `presentation_type` 이 유효 enum 값인가
- [ ] `tone` 이 유효 enum 값인가
- [ ] `presentation_minutes` >= 1
- [ ] 회사 종속 표현 0건 (`client_name`, `presenter_role`, `presenter_name` 에서 검출 시 경고)

### 7-2. 회사 종속 표현 검증

```python
FORBIDDEN_COMPANY_TERMS = [
    "엠앤씨", "M&C커뮤니케이션즈", "M&C",
    "리멤버앤컴퍼니", "신사업실",
]

def validate_company_mentions(meta_json):
    warnings = []
    pm = meta_json.get("proposal_meta", {})

    check_fields = ["client_name", "presenter_role", "presenter_name", "rfp_title"]
    for field in check_fields:
        value = pm.get(field, "")
        if not value:
            continue
        for term in FORBIDDEN_COMPANY_TERMS:
            if term in str(value):
                warnings.append(
                    f"Forbidden company mention '{term}' at proposal_meta.{field}. "
                    f"Replace with generic term or external client token."
                )
    return warnings
```

---

## 8. proposal-meta.json 생성 가이드 (mice-proposal 측)

mice-proposal v2.1.1 가 본 메타 JSON을 자동 생성하려면 Phase 5 마지막에 다음 로직 추가 (참고용 — pt-script 빌드 범위 외):

```python
def export_pt_script_meta(rfp_data, user_inputs):
    """mice-proposal 빌드 완료 후 pt-script 용 메타 JSON 생성."""
    meta = {
        "$schema": "pt-script/v2.0",
        "proposal_meta": {
            "client_name": rfp_data.get("client_name"),
            "rfp_title": rfp_data.get("rfp_title"),
            "rfp_id": rfp_data.get("rfp_id"),
            "presentation_minutes": user_inputs.get("pt_minutes", 20),
            "presentation_type": "bidding_pt",
            "presenter_role": user_inputs.get("presenter_role", "발표자"),
            "audience_type": user_inputs.get("audience_type", "발주처 심사위원"),
            "tone": "formal",
            "qna_included": True,
            "qna_minutes": user_inputs.get("qna_minutes", 4),
            "client_id": user_inputs.get("client_id"),
        },
        "extracted_from": "mice-proposal",
        "mice_proposal_version": "v2.1.1",
        "pptx_source": "proposal.pptx",
        "generated_at": datetime.now().isoformat()
    }
    return meta
```

본 가이드는 참고용이며, pt-script 는 메타 JSON 없이도 PPTX 단독으로 동작한다.

---

## 9. 함께 보는 문서

| 파일 | 내용 |
|------|------|
| `script-guide.md` | 슬라이드 유형 8종별 멘트 패턴 |
| `jc-design-mapping.md` | docx 디자인 토큰 매핑 (client_id 오버레이 포함) |
| `notes-extraction.md` | PPTX speaker notes 추출 + 메타 노트 필터링 |
| `../scripts/extract_notes.py` | PPTX 분석 구현체 |
| `../scripts/build_script.py` | docx 빌드 구현체 |
| mice-proposal/references (별도 스킬) | 업스트림 산출물 가이드 |
