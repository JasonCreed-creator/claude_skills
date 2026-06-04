# Chaining Protocol — 체이닝 봉투 정본 (ChainPayload/v1)

> **정본(Single Source of Truth)**: MICE 스킬 간 데이터 교환에 쓰이는 공통 "봉투(envelope)" 구조를 한 곳에서 권위 정의한다.
> 각 스킬의 reference 문서(`chaining-guide.md` / `chaining-schema.md`)는 **자기 고유의 input/output 페이로드 매핑**만 정의하고, 봉투 구조는 본 문서를 참조한다.
>
> 적용 대상 스킬: `mice-rfp-analyzer` · `mice-proposal` · `mice-estimate` · `pt-script` · `mice-dashboard` · `mice-meeting-minutes` · `mice-sponsor-deck` · `jc-redteam` · `jc-strategy-canvas` · `mice-market-intel`.

---

## 목차

- [1. 봉투란 무엇인가](#1-봉투란-무엇인가)
- [2. ChainPayload/v1 봉투 구조](#2-chainpayloadv1-봉투-구조)
- [3. 공통 메타 필드 정의](#3-공통-메타-필드-정의)
- [4. 페이로드(payload) — 스킬 고유 영역](#4-페이로드payload--스킬-고유-영역)
- [5. 스킬 간 체이닝 흐름](#5-스킬-간-체이닝-흐름)
- [6. 표준 규약](#6-표준-규약)
- [7. 자동 라우팅 (입력 source 판별)](#7-자동-라우팅-입력-source-판별)
- [8. 마이그레이션 노트 (기존 변형 통합)](#8-마이그레이션-노트-기존-변형-통합)

---

## 1. 봉투란 무엇인가

체이닝 봉투는 **"누가, 어떤 버전으로, 언제 만든 데이터인가"** 를 식별하는 공통 헤더다.
봉투 안에 담기는 **실제 데이터(페이로드)** 는 스킬마다 다르지만, 봉투(헤더) 구조는 모든 스킬이 동일하게 따른다.

```
┌─ ChainPayload/v1 봉투 (공통 — 본 문서가 정의) ─────────────┐
│  $schema, source, version, generatedAt, (target)          │
│  ┌─ payload (스킬 고유 — 각 스킬 reference가 정의) ──────┐ │
│  │  rfp_meta / discovery_data / sections / sponsor_…     │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

이 분리 원칙 덕분에:
- **봉투 규약 변경**은 본 문서 한 곳만 고치면 된다.
- **스킬 고유 데이터 모델**은 각 스킬이 독립적으로 진화시킨다.

---

## 2. ChainPayload/v1 봉투 구조

모든 체이닝 JSON은 다음 봉투 필드를 **최상위(top-level)** 에 둔다.

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-estimate",
  "version": "v2.0",
  "generatedAt": "2026-05-25T16:30:00+09:00",
  "target": "mice-dashboard",

  "// 이하 스킬 고유 페이로드 (각 스킬 reference 문서가 정의)": "...",
  "projectTitle": "REMEMBER SUMMIT 2026",
  "sections": { "...": "..." }
}
```

- 봉투 필드와 페이로드 필드는 **같은 최상위 객체에 평탄(flat)하게 공존**한다 (페이로드를 별도 `payload` 키로 감싸지 않는다 — 기존 모든 스킬이 평탄 구조를 쓴다).
- 봉투 필드는 **예약어**다. 페이로드가 `source` / `version` 등의 이름을 재사용하지 않는다.

---

## 3. 공통 메타 필드 정의

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `$schema` | string | ✅ | 봉투 버전 식별자. **항상 `"ChainPayload/v1"`**. 입력 라우팅의 1차 판별 키. |
| `source` | string | ✅ | 생산 스킬 ID. `mice-rfp-analyzer` \| `mice-proposal` \| `mice-estimate` \| `pt-script` \| `mice-dashboard` \| `mice-meeting-minutes` \| `mice-sponsor-deck` \| `jc-strategy-canvas` \| `mice-market-intel` 중 하나. |
| `version` | string | ✅ | 생산 스킬의 시맨틱 버전 (예: `"v2.0"`, `"v2.1.1"`). 다운스트림 호환성 판단용. |
| `generatedAt` | ISO 8601 string | ✅ | 생성 시각 (예: `"2026-05-27T10:00:00+09:00"`). |
| `target` | string | optional | 의도된 수신 스킬 ID. 다대다 체이닝에서 라우팅 힌트. 생략 가능. |
| `clientId` | string \| null | optional | 클라이언트 오버레이 ID (jc-design-system `client-overlays.md` 참조). null = personal 시그니처. 디자인 산출물 스킬 간 전달 시 사용. |

### 3-1. 명명 규약 (camelCase 정본)

봉투 필드는 **camelCase** 를 정본으로 한다: `generatedAt`, `projectTitle`, `clientId`.

> 과거 일부 스킬이 `generated_at`(snake_case), `source_skill`, `extracted_from` 등 변형을 썼다. 이는 **각 스킬 내부 페이로드 관례**일 뿐 봉투 표준이 아니다. 신규/갱신 시 봉투 헤더는 camelCase + 위 표의 필드명을 사용한다. 기존 페이로드 내부 필드명은 호환을 위해 그대로 두되, 봉투 레벨 식별은 `$schema`/`source` 우선으로 처리한다. (§8 참조)

---

## 4. 페이로드(payload) — 스킬 고유 영역

봉투 아래의 실제 데이터 구조는 **각 스킬의 reference 문서가 권위 정의**한다. 본 문서는 봉투까지만 정의하고 페이로드 필드는 정의하지 않는다.

| 스킬 | 페이로드 정본 문서 | 페이로드 핵심 키 (예시) |
|------|-------------------|----------------------|
| mice-rfp-analyzer | `mice-rfp-analyzer/references/chaining-guide.md` | `rfp_meta`, `analysis_result`, `requirements`, `evaluation_focus`, `differentiation_points` |
| mice-meeting-minutes | `mice-meeting-minutes/references/chaining-guide.md` | `client`, `project_context`, `discovery_data`, `strategic_notes` |
| mice-estimate | `mice-estimate/references/chaining-schema.md` | `eventScale`, `venue`, `options`, `sections`, `breakdown`, `totalAmount` |
| mice-dashboard | `mice-dashboard/references/chaining-schema.md` | `rounds`, `kpis`, `insights`, `actualSpending`, `outputs` |
| mice-sponsor-deck | `mice-sponsor-deck/references/chaining-schema.md` | `event_meta`, `sponsor_candidates`, `audience_hints` |
| pt-script | `pt-script/references/chaining-schema.md` | `proposal_meta` (client_name, presentation_minutes, tone, …) |
| jc-redteam | `jc-redteam/references/chaining-guide.md` | 페이로드 스키마 없음 — 임의 산출물/텍스트 수용 |
| jc-strategy-canvas | `jc-strategy-canvas/references/chaining-schema.md` | `topic`, `decision`, `recommendation`, `differentiation_axes`, `key_messages`, `evidence_flags` |
| mice-market-intel | `mice-market-intel/references/chaining-schema.md` | `market_size`, `competitors`, `trends`, `sponsor_candidates`, `benchmarks`, `sources` |

> **이 페이로드 매핑들은 "중복"이 아니다.** 각 스킬만의 고유 필드·예시·변환 룰이므로 해당 스킬 문서에 그대로 보존한다.

---

## 5. 스킬 간 체이닝 흐름

### 5-1. 풀 워크플로우 (수주 → 운영 → 결과)

```
[RFP 원문]
     ↓
mice-rfp-analyzer ──→ 분석 보고서(.docx) + 평가 매트릭스(.xlsx)
     │                  └─ ChainPayload(source=mice-rfp-analyzer) ─┐
     ↓ GO 판정                                                     │
mice-proposal ───────→ 제안서(.pptx)  ←──────────────────────────┘
     │                  └─ ChainPayload(source=mice-proposal) ─┬─┐
     ↓ 제안 확정                                                │ │
mice-estimate ───────→ 견적서(.xlsx)  ←──────────────────────┘ │
     │                  └─ ChainPayload(source=mice-estimate) ──┼─┐
     ↓ 발표 준비                                                 │ │
pt-script ───────────→ 발표 대본(.docx)  ←───────────────────────┘ │
     ↓ (행사 종료 후)                                                │
mice-dashboard ──────→ 결과 대시보드(.html/.pdf)  ←─────────────────┘
     ↑ (시리즈 누적)
mice-meeting-minutes (시리즈)
```

### 5-2. 회의록 발원 체인

```
Discovery / 정기 / 사후 협의
     ↓
mice-meeting-minutes (8축 구조화)
     ├──→ ChainPayload(source=mice-meeting-minutes, target=mice-proposal)   [Discovery 5데이터]
     ├──→ ChainPayload(source=mice-meeting-minutes, target=mice-estimate)   [규모·예산 단서]
     ├──→ ChainPayload(source=mice-meeting-minutes, target=mice-dashboard)  [시리즈 누적 rounds]
     └──→ ChainPayload(source=mice-meeting-minutes, target=mice-sponsor-deck) [스폰서 후보]
```

### 5-3. 영업 분기 (스폰서)

```
mice-meeting-minutes ──→ sponsor_candidates ──→ mice-sponsor-deck ──→ HTML/PPTX 데크
                                                       └──→ (PPTX) ──→ pt-script (영업 PT 대본)
```

### 5-4. 최하류 품질 게이트 (jc-redteam)

```
mice-proposal / mice-estimate / mice-sponsor-deck / mice-dashboard / mice-rfp-analyzer / mice-meeting-minutes
        모든 산출물 (PPTX/XLSX/DOCX/HTML/JSON 또는 결론 텍스트)
                                  ↓
                            jc-redteam  ← 최종 검증 (재생성 안 함, 결함 지적·교정·대안만)
```

### 5-5. 체이닝 엣지 요약표

| From | To | 봉투 source | 전달 핵심 |
|------|----|-----------|----------|
| mice-rfp-analyzer | mice-proposal | `mice-rfp-analyzer` | 요건·평가·차별화·핵심 메시지 |
| mice-rfp-analyzer | mice-estimate | `mice-rfp-analyzer` | 발주가·예산 범위 (베뉴·옵션 TBD) |
| mice-meeting-minutes | mice-proposal | `mice-meeting-minutes` | Discovery 5데이터 |
| mice-meeting-minutes | mice-estimate | `mice-meeting-minutes` | 규모·예산 단서 |
| mice-proposal | mice-estimate | `mice-proposal` | eventScale·venue·options |
| mice-proposal | pt-script | `mice-proposal` | 발표 메타 (시간·톤·청중) |
| mice-estimate | pt-script | `mice-estimate` | sections·총액 (비용 슬라이드 멘트) |
| mice-estimate | mice-dashboard | `mice-estimate` | 예산 vs 실적 |
| mice-meeting-minutes | mice-dashboard | `mice-meeting-minutes` | 시리즈 rounds 누적 |
| mice-meeting-minutes | mice-sponsor-deck | `mice-meeting-minutes` | sponsor_candidates |
| mice-sponsor-deck | pt-script | `mice-sponsor-deck` | 영업 데크 PPTX |
| (모든 스킬) | jc-redteam | (각 source) | 최종 산출물 검증 |
| mice-dashboard | mice-proposal/rfp-analyzer | `mice-dashboard` | 차기 행사 기획용 전년 실적 (선순환) |

---

## 6. 표준 규약

### 6-1. 입력 수용 원칙

1. 다운스트림 스킬은 입력 봉투의 `$schema == "ChainPayload/v1"` 를 먼저 확인한다.
2. `$schema` 가 없거나 봉투가 아니면 → 파일/텍스트/대화 입력으로 처리 (봉투 강제 아님).
3. `source` 로 페이로드 파싱 분기를 결정한다 (§7).
4. `jc-redteam` 은 봉투 유무와 무관하게 모든 산출물·텍스트를 수용한다 (엄격 스키마 없음).

### 6-2. 데이터 무결성

- **단일 진실 소스**: 원천 데이터(RFP 원문·회의 transcript 등)가 진실. 다운스트림은 받은 페이로드를 임의 변경하지 않는다.
- **변경 추적**: 수정이 불가피하면 사유를 명시하고 업스트림에 피드백.
- **버전 표기**: 산출물 파일명에 날짜 포함, `version` 필드로 갱신 추적.

### 6-3. 회사·개인 식별 정보 금지

- 봉투·페이로드 어디에도 자기 회사명·데이터 파트너 실명을 **하드코딩하지 않는다.**
- 발주처/클라이언트/공급자 정보는 **외부 주입 변수**(`clientId` 오버레이 등)로 처리한다.
- 검출 시 일반 표현으로 치환하거나 사용자에게 경고한다. (각 스킬의 회사 종속 표현 검증 룰은 해당 스킬 문서에 보존.)

### 6-4. 저장 위치 관례

```
.chaining/[client_or_project]_[YYYYMMDD]_to_[target].json
```

다운스트림 스킬 호출 시 본 경로를 우선 탐색한다. (스킬별 파일명 세부는 각 문서 참조.)

### 6-5. 디자인 토큰 일관성

체이닝으로 생성되는 시각 산출물(PPTX/XLSX/DOCX/HTML)은 jc-design-system 시그니처 토큰을 적용한다. `clientId` 봉투 필드가 있으면 해당 오버레이를 적용한다. 토큰 로드·오버레이·모드 매핑 절차는 `usage-guide.md` 참조.

---

## 7. 자동 라우팅 (입력 source 판별)

다운스트림 스킬의 표준 입력 분기 로직:

```python
def detect_input_source(input_payload) -> str:
    """입력 형식으로 처리 분기 결정 (ChainPayload/v1 봉투 우선)."""
    if isinstance(input_payload, dict) and input_payload.get("$schema") == "ChainPayload/v1":
        return input_payload.get("source")     # mice-estimate, mice-meeting-minutes, ...
    if isinstance(input_payload, dict) and "$schema" in input_payload:
        return input_payload["$schema"]         # 레거시 스킬 전용 스키마 (마이그레이션 중)
    if hasattr(input_payload, "read"):
        return "file_upload"                     # Excel/CSV/PPTX 등 파일 객체
    if isinstance(input_payload, (list, dict)):
        return "inline_data"                     # 대화/인라인 데이터
    return "unknown"
```

판별된 `source` 에 맞춰 해당 스킬 reference 문서의 페이로드 파싱 룰을 적용한다.

---

## 8. 마이그레이션 노트 (기존 변형 통합)

본 정본 수립 이전, 스킬마다 봉투 관례가 갈라져 있었다. 정본은 이를 **`ChainPayload/v1` + camelCase 메타** 로 수렴시킨다.

| 스킬 | 기존 봉투 관례 | 정본 대비 차이 | 호환 처리 |
|------|---------------|---------------|----------|
| mice-estimate | `$schema: ChainPayload/v1` + `source` + `version` | ✅ 정본과 일치 | 그대로 |
| mice-dashboard | `$schema: ChainPayload/v1` + `source` + `version` + `generatedAt` | ✅ 정본과 일치 | 그대로 |
| mice-rfp-analyzer | `source` 만 (`$schema`·`version` 없음) | 봉투 헤더 미흡 | 신규 출력 시 `$schema`/`version`/`generatedAt` 추가 권장 |
| mice-meeting-minutes | `source_skill` + `generated_at` (snake) | 필드명 변형 | `source`/`generatedAt` 로 수렴 권장. 기존 페이로드는 유지 |
| mice-sponsor-deck | `$schema: mice-sponsor-deck/v2.0` + `extracted_from` | 봉투에 스킬 전용 스키마 사용 | 입력 검증은 기존 유지. 봉투 식별은 `source`로 수렴 권장 |
| pt-script | `$schema: pt-script/v2.0` + `extracted_from` | 봉투에 스킬 전용 스키마 사용 | 입력 검증은 기존 유지. 봉투 식별은 `source`로 수렴 권장 |
| jc-redteam | 봉투 없음 (임의 입력) | 해당 없음 | 변경 없음 — 모든 입력 수용 유지 |

> **호환성 원칙**: `detect_input_source()`(§7)는 `ChainPayload/v1` 과 레거시 스킬 전용 스키마(`pt-script/v2.0` 등)를 **모두** 받아낸다. 따라서 기존 페이로드를 깨지 않고 점진 수렴이 가능하다. 각 스킬의 enum·필드 검증 룰은 해당 스킬 문서가 계속 권위를 가진다.
