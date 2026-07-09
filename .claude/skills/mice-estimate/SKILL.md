---
name: mice-estimate
version: "v2.2.1"
description: "MICE 행사 견적서를 엑셀(.xlsx)로 생성·수정하는 스킬. 두 가지 양식을 지원한다: (1) M&C 견적서 — 국가계약법 기반 산출내역서 양식 + calcEstimate 자동 산출 엔진, (2) 리멤버 견적서 — 패키지 할인 구조의 견적서 양식. 반드시 이 스킬을 사용해야 하는 상황: 사용자가 '견적서', '견적', 'estimate', '산출내역서'를 언급할 때. 특히 'M&C 견적서', '리멤버 견적서' 양식 명칭이 명시될 때. 기존 견적서 파일을 수정하거나 항목을 추가/삭제/변경할 때도 이 스킬을 사용한다. 견적 항목을 대화로 전달받아 새로 생성하거나, 기존 파일을 업로드받아 수정하거나, 행사 규모·옵션만 받아 자동 산출하는 세 가지 입력 방식을 모두 지원한다. mice-proposal·mice-rfp-analyzer 체이닝 입력을 받아 자동 견적 생성 가능. 공급자·고객사 정보는 모두 외부 주입 변수로 처리 — 스킬 내 어떤 회사·개인 식별 정보도 하드코딩하지 않는다. 실행형 지시는 실행 전 jc-prompt-builder 브리프를 거친다."
dependencies:
  - openpyxl
---

# MICE 견적서 생성 스킬

## 버전 히스토리

### v2.2.1 — 2026-07-03

CP1 GO-1 후속 조치 — ChainPayload 출력 봉투에 필수 필드 `generatedAt` 추가(chaining-schema.md §4·§7), 참조 링크 무결성 2건 정정(venue-db-realdata.md §6 파일명, venue-db.md §5 외부 문서 링크 평문화).

### v2.2.0 — 2026-07-03

**Fable 5 재설계 패스 + Sprint 8 반영.**

#### 신규 추가
- Step 6.5 **완료 게이트** — 증거주의 6항(엔진 자가검증·3중 금액 일치·재오픈 무결성·입력 전수성·식별정보·가격 산식 연동). 통과 전 전달 금지.
- `references/venue-db-realdata.{json,md}` — 베뉴파인더 견적이력 100건→25개 베뉴×홀 실데이터 (대관료 단독가 없음, 수용인원 검증·후보 제시용 — §0 경고 필독).

#### 수리
- calc 엔진 `target` 키 누락 시 KeyError → 명시적 한국어 ValueError (BL-S8-01). 회귀: golden 33케이스 + 신규 회귀 3케이스 PASS (개발 워크스페이스 `mice-skills-work/sprint-08/golden-tests/` 스위트 — 스킬 패키지 외부 자산).

### v2.1.0 — 2026-06-04

**전략 프라이싱 레이어 추가** (forge 인테이크). 원가 산출(pricing-engine)을 넘어 *제안가·할인·패키지 가격*을 전략적으로 정하는 가격 결정 논리.

#### 신규 추가
- `references/pricing-strategy.md` — 4대 가격 레버(가치기반·Van Westendorp PSM·티어/패키지·앵커링) + MICE 입찰/스폰서 맥락. 출처 패턴 maigentic/stratarts(MIT), 방법만 흡수.
- SKILL.md "전략 프라이싱(선택)" 절 — 원가↔제안가 경계 + 체이닝(`mice-market-intel`·`jc-strategy-canvas`) 명시.

### v2.0 — 2026-05-25

**핵심 변화**: 자동 가격 산출 엔진 + 체이닝 + 외부 변수화 + 디자인 시맨틱 매핑.

#### 신규 추가
- ⭐ **자동 산출 엔진** `scripts/calc_estimate.py` — SSOT §5 calcEstimate Python 포팅 (CLI 자가검증 포함, SSOT §9 11/11 PASS)
- ⭐ **xlsx 본문 자동 작성** `scripts/export_estimate.py` — 7섹션 자동 펼침 + 무결성 검증
- **방식 A (자동 산출)** 워크플로우 — `calc_estimate({target, options})` 한 번 호출로 견적서 완성
- **Step 2.5 체이닝 입력 감지** — mice-proposal / mice-rfp-analyzer 의 ChainPayload JSON 자동 처리
- **Step 3.5 공급자·고객사 슬롯 명세** — M&C 13 슬롯 + 리멤버 6 슬롯 (외부 주입 변수)
- 신규 references 5종:
  - `pricing-engine.md` — 가격 엔진 공식·14상수
  - `option-catalog.md` — 9종 옵션 + 상호배제 규칙 (media·photowall·scaler4k 자동)
  - `venue-db.md` — 베뉴 DB 스키마 + 20 슬롯 (실데이터 보류)
  - `jc-design-mapping.md` — Excel HEX → JC 시맨틱 토큰 매핑
  - `chaining-schema.md` — 입출력 JSON 스키마 (3종)

#### 변경
- **frontmatter**: `name + description` → `name + version + description + dependencies`
- **공급자 정보 외부 변수화** (CLAUDE.md §10 준수):
  - SKILL.md 본문 — 회사 정보 하드코딩 제거
  - `references/mnc_template.md` — 공급자 기본값 → 13 슬롯 명세표
  - `references/remember_template.md` — 공급자 기본값 → 6 슬롯 명세표
  - `assets/mnc_template.xlsx` 셀 — `(외부 주입 - ...)` placeholder 교체
  - `assets/remember_template.xlsx` 셀 — placeholder 교체

#### 유지 (변경 없음)
- `scripts/korean_amount.py` — 한글 금액 변환 (v1 그대로)
- 양식 시각 디자인 (색상·병합·로고) — 모두 보존

#### 검증
- ✅ SSOT §9 0원 일치 11/11 (pk = 83,750,000원, pkVat = 92,125,000원)
- ✅ Summit 2026 hand-trace 10/10 (target=120, pk = 89,810,000원)
- ✅ 9개 엣지 케이스 (target=40~501) PASS
- ✅ 트리거 충돌 0건 / 회사 종속 표현 0건
- ✅ jc-design 일관성 점수 100/100

### v1.0 — (이전)

- 두 양식(M&C / 리멤버) 템플릿 복사 + 수동 항목 입력 방식
- `scripts/korean_amount.py` 한글 금액 변환
- 공급자 정보 하드코딩
- 자동 산출·체이닝·jc-design 매핑 없음

## 개요

본 스킬은 두 가지 양식("M&C 견적서", "리멤버 견적서" — 양식 식별자)의 MICE 행사 견적서를 엑셀로 생성·수정한다. **v2부터 M&C 양식은 calcEstimate 자동 산출 엔진**을 통해 행사 규모(target)·옵션만 받아 견적 자동 생성이 가능하다.

**자산 정의 원칙**: 본 스킬은 어떤 회사·개인의 식별 정보도 하드코딩하지 않는다. 양식 명칭('M&C', '리멤버')만 식별자로 보존되며, 공급자·고객사·담당자·연락처 등 모든 식별 정보는 **외부 주입 변수**로 처리된다. 산출물 본문에는 사용자가 매번 주입하는 변수만 들어간다. (정본: `jc-design-system/references/shared-rules.md#RULE-NO-COMPANY` — 양식 식별자 보존은 정본의 '허용' 항목)

## 워크플로우

### Step 1: 양식 판별

사용자의 요청에서 어떤 양식인지 판별한다:
- **"M&C"** → M&C 양식 (국가계약법 기반 산출내역서)
- **"리멤버", "remember"** → 리멤버 양식 (패키지 할인 구조)
- 불명확하면 반드시 먼저 물어본다.

### Step 2: 입력 방식 판별 (3가지)

| 방식 | 트리거 | 동작 |
|---|---|---|
| **A. 자동 산출 (M&C 전용, v2 신규)** | "빠른견적", "자동 산출", "100명 규모 견적 계산해줘" 등 | `calc_estimate()` 호출 → 결과로 템플릿 채움 |
| **B. 대화 입력 (v1 방식)** | 사용자가 항목·단가를 직접 지정 | 템플릿 복사 후 데이터 채우기 |
| **C. 파일 수정** | 사용자가 기존 견적서 xlsx 업로드 | 해당 파일 로드하여 수정 |

리멤버 양식은 **B / C만 지원** (calcEstimate는 단가 다를 가능성 — 별도 사이클 분리).

### Step 2.5: 체이닝 입력 감지 (v2 신규)

다음 ChainPayload JSON이 입력되었으면 자동으로 방식 A 진입:

- `source: "mice-proposal"` → estimatedFrom: `proposal_chain`
- `source: "mice-rfp-analyzer"` → estimatedFrom: `rfp_default`

ChainPayload 스키마 상세는 [references/chaining-schema.md](references/chaining-schema.md) 참조.

### Step 3: 필수 정보 수집

#### 방식 A (자동 산출) — 최소 입력

| 항목 | 설명 | 필수 |
|------|------|------|
| 행사명 (project_title) | 시트명·파일명에 사용 | ✅ |
| target | 총 참석인원 (40~500) | ✅ |
| guarantee | 모객 게런티 | 선택 (None이면 target) |
| 옵션 | 9종 중 활성화 ([option-catalog.md](references/option-catalog.md)) | 선택 |
| venueName | 베뉴명 (참조용) | 선택 |
| boothCount | 부스 수 | 선택 (default 0) |
| **공급자 정보 슬롯** (Step 3.5) | 외부 주입 변수 | 사용자가 매번 제공 |
| **고객사 정보 슬롯** (Step 3.5) | 외부 주입 변수 | 사용자가 매번 제공 |

→ `calc_estimate(cfg)` 호출 → 결과를 템플릿에 자동 채움 → `export_estimate()` 로 본문 자동 작성.

#### 방식 B/C (수동) — v1과 동일

##### M&C 양식 필수 정보

| 항목 | 설명 | 필수 |
|------|------|------|
| 행사명 | 예: "2026 ABC 박람회" | ✅ |
| 고객명 | 외부 주입 변수 | ✅ |
| 일시 | 예: "계약체결일~'26.12.16" | ✅ |
| 장소 | 외부 주입 변수 | ✅ |
| 세부 항목 | 섹션별 항목·단가·수량·기간 | ✅ |
| 인건비 | 인원·직급·참여율·기간 | 선택 |
| 절사/할인 | 금액 조정 | 선택 |

##### 리멤버 양식 필수 정보

| 항목 | 설명 | 필수 |
|------|------|------|
| Project Title | 행사명 | ✅ |
| Package Type | 예: Premium Package | ✅ |
| Venue | 장소 (외부 주입) | ✅ |
| 비고 | 일시, 규모 등 | ✅ |
| 세부 항목 | 섹션별 항목·정가·할인가 | ✅ |
| 모객 조건 | 타겟 직급·산업·직무, 인당 단가 | 선택 |
| 최종 할인가 | 전체 추가 할인 | 선택 |

### Step 3.5: 공급자·고객사 정보 슬롯 (외부 주입 변수, v2 신규)

본 스킬은 **공급자(견적 발행 측)·고객사(견적 수신 측) 모든 식별 정보를 사용자가 매번 주입**한다. 스킬 자체에는 회사·개인 식별 정보가 하드코딩되어 있지 않다.

#### M&C 양식 슬롯

| 슬롯 키 | 설명 | Excel 셀 위치 |
|---|---|---|
| `customer_name` | 고객명 | B4 |
| `event_period` | 일시 | B5 |
| `event_venue` | 장소 | B6 |
| `supplier_company` | 공급자 상호 | I3 |
| `supplier_biz_reg_no` | 사업자등록번호 | I4 |
| `supplier_representative` | 대표자 | K4 |
| `supplier_address` | 주소 | I5 |
| `supplier_biz_type` | 업태 | I6 |
| `supplier_biz_item` | 종목 | K6 |
| `supplier_manager` | 담당자 | I7 |
| `supplier_email` | 이메일 | K7 |
| `supplier_phone` | 전화 | I8 |
| `supplier_fax` | 팩스 | K8 |

#### 리멤버 양식 슬롯

| 슬롯 키 | 설명 | Excel 셀 위치 |
|---|---|---|
| `proposal_date` | 제안일자 | G11 |
| `validity_period` | 유효기간 | G12 |
| `supplier_company` | 공급자 상호 | G13 |
| `supplier_address` | 주소 | G14 |
| `supplier_manager` | 담당자 | G15 |
| `supplier_contact` | 연락처 | G16 |

#### 수집 방식 권장 순서

1. 사용자가 첫 견적 요청 시 공급자 정보 일괄 수집 → 사용자 메모리에 저장 권장 (스킬 자체와 별도)
2. 이후 견적 생성 시 메모리에서 자동 채움 + 변경분만 추가 입력
3. 한 번도 입력되지 않은 경우 명시적으로 묻기 — 추정·임의값 사용 금지

### Step 4: 견적서 생성/수정

#### 레퍼런스 파일 읽기 (필수)

작업 전 반드시 해당 양식의 레퍼런스를 읽는다:

| 양식·방식 | 읽을 reference |
|---|---|
| 방식 A (M&C 자동 산출) | `references/pricing-engine.md` + `references/option-catalog.md` + `references/mnc_template.md` |
| 방식 A + 베뉴 룩업 시 | `references/venue-db.md` |
| 방식 B/C (M&C 수동) | `references/mnc_template.md` |
| 리멤버 (B/C) | `references/remember_template.md` |
| 체이닝 입력 처리 | `references/chaining-schema.md` |

#### 방식 A: calcEstimate 자동 산출 (M&C, v2 신규)

```python
import sys
sys.path.insert(0, '/path/to/skill/scripts')
from calc_estimate import calc_estimate
from export_estimate import export_mnc_estimate

cfg = {
    'target': 100,
    'guarantee': 100,
    'venueName': '(외부 주입)',
    'options': {'video': True, 'emcee': True},
    'boothCount': 0,
}
result = calc_estimate(cfg)

# 공급자·고객사 정보는 사용자가 주입 (예시 — 실제 값은 매번 다름)
meta = {
    'project_title':         '(외부 주입)',
    'customer_name':         '(외부 주입)',
    'event_period':          '(외부 주입)',
    'event_venue':           '(외부 주입)',
    'supplier_company':      '(외부 주입)',
    'supplier_biz_reg_no':   '(외부 주입)',
    'supplier_representative':'(외부 주입)',
    'supplier_address':      '(외부 주입)',
    'supplier_biz_type':     '(외부 주입)',
    'supplier_biz_item':     '(외부 주입)',
    'supplier_manager':      '(외부 주입)',
    'supplier_email':        '(외부 주입)',
    'supplier_phone':        '(외부 주입)',
    'supplier_fax':          '(외부 주입)',
}

output_path = export_mnc_estimate(
    template_path='/path/to/skill/assets/mnc_template.xlsx',
    output_path=f'/home/claude/MC견적서_{meta["project_title"]}_{YYMMDD}.xlsx',
    result=result,
    meta=meta,
)
# → 헤더·본문(세부산출내역 7개 섹션)·B8(한글금액) 모두 자동 채움
# → 무결성 검증 포함 (재오픈 가능 여부)
```

#### 방식 B/C: v1 수동 입력 (변경 없음)

```python
from openpyxl import load_workbook
import shutil

template = "/path/to/skill/assets/{mnc|remember}_template.xlsx"
output = "/home/claude/{파일명}.xlsx"
shutil.copy(template, output)
wb = load_workbook(output)
ws = wb.active

# 외부 주입 변수로 헤더 채움
ws['B4'] = meta['customer_name']  # 절대 하드코딩 금지
# ...

# 세부 항목 행 작성
# ...

wb.save(output)
```

**중요**: 템플릿을 복사하면 로고 이미지, 병합셀, 서식이 모두 보존된다.

### Step 5: 수식 재계산 + 한글 금액 반영 (M&C 전용)

**1단계: 수식 재계산** (방식 B/C, 또는 방식 A에서 합계영역 일치 확인용)

```bash
python /mnt/skills/public/xlsx/scripts/recalc.py {output_file}
```

**2단계: 한글 금액 변환 및 B8 반영**

```python
from openpyxl import load_workbook
from korean_amount import format_estimate_amount

# 방식 A: result['pkVat'] 직접 사용 (calc_estimate가 이미 정확)
# 방식 B/C: recalc 후 I17 값 읽기
wb = load_workbook(output, data_only=True)
total = wb.active['I17'].value
wb.close()

wb = load_workbook(output)
wb.active['B8'] = format_estimate_amount(total)
wb.save(output)
```

### Step 6: 출력

완성된 파일을 `/mnt/user-data/outputs/` 로 복사하고 present_files 로 전달한다.

체이닝 후속 스킬에 전달할 ChainPayload JSON이 필요하면 [chaining-schema.md §7](references/chaining-schema.md) 의 `to_chain_payload()` 헬퍼 사용.

### Step 6.5: 완료 게이트 (증거주의 — 통과 전 전달 금지)

견적서는 숫자가 곧 신뢰다. 전달 직전 아래를 실제로 실행·확인하고, 미통과면 수정 후 재검증한다:

1. **엔진 자가검증** (방식 A): `python scripts/calc_estimate.py` 실행 → "SSOT §9 검증 통과 (PASS)" 확인. 실패 시 엔진·입력을 의심하고 임의 보정 금지.
2. **3중 금액 일치**: 엔진 결과(`pkVat`) ↔ 시트 합계 셀 ↔ 한글 금액(B8)이 동일한가 — 셀 값을 다시 읽어 대조한다(눈대중 금지).
3. **재오픈 무결성**: 산출 .xlsx를 openpyxl로 재로드해 깨짐·수식 오류(#REF! 등)가 없는가.
4. **입력 반영 전수성**: 요청·체이닝 입력의 인원·기간·옵션·특이 요구가 각각 어느 행에 반영됐는지 대응을 확인한다 — 누락 항목 0건.
5. **식별정보**: 슬롯 주입값 외 회사·개인 식별정보 하드코딩 0건 (RULE-NO-COMPANY).
6. **가격 산식 연동** (rfp-analyzer 체이닝 + RFP 가격 점수 산식 존재 시): 제안가가 최적 입찰가 구간 대비 어디에 있는지 한 줄 명시해 전달한다.

확인 불가 항목(예: 발주가 미공개)은 "미확인"으로 표기하고 완료 주장하지 않는다.

---

## 전략 프라이싱 (선택 — 원가→제안가)

`calc_estimate`/`pricing-engine.md`가 *원가·마진*을 산출한다면, 견적의 **제안가·할인폭·패키지 가격을 전략적으로** 정해야 할 때는 [pricing-strategy.md](references/pricing-strategy.md)를 참조한다. 4대 레버(가치기반·Van Westendorp 가격민감도·티어/패키지 구조·앵커링)로 "얼마에 제안할까"를 설계한다.

- 기계적 원가 산출만 필요하면 이 절을 건너뛴다(과함).
- 경쟁가·지불의향 *조사*는 `mice-market-intel`, 가격 포지션 *판단*은 `jc-strategy-canvas`, *원가*는 `pricing-engine`. 본 절은 그 사이 가격 *결정 논리*.
- 데이터 없는 지불의향·경쟁가는 `[가설]` — 추정 금지. 저가수주 리스크·낙관 마진은 `jc-redteam`으로 점검.

## M&C 견적서 상세 규칙

### 자동 산출 매핑 (v2 신규)

calc_estimate 결과를 M&C 양식에 매핑하는 표준 카테고리:

| 양식 카테고리 (Row 20+ A열) | calc_estimate 키 | 비고 |
|---|---|---|
| "1. 베뉴 사용료" | `s1` | 단일 행 (venueName 명시) |
| "2. 시스템 구축" | `sysBreakdown` 7개 | video / scaler4k / audio / engineer / presentation / registration / misc |
| "3. 디자인 및 브랜딩" | `desBreakdown` 3개 | env / web / kv |
| "4. 운영 및 보험" | `opsBreakdown` 3개 | desk / ops / insurance |
| "5. 추가옵션" | `otBreakdown` (활성 옵션만) | 옵션 라벨로 펼침 |
| "6. 모객 솔루션" | `rsvpPkg` + `showup` | 2행 (RSVP / 쇼업) |
| "7. PCO 기획료" | `s5` | 단일 행 |

각 카테고리 끝에 "소계" 행 (I열 = SUM(...)) 자동 삽입. 섹션 간 빈 행 (높이 10) 삽입.

상세 구현: `scripts/export_estimate.py` 의 `export_mnc_estimate()` 함수 참조.

### 금액 계산 (v1과 동일 — 기존 호환)

- **일반 항목**: `AMOUNT = PRODUCT(D열:F열)` (단가 × 수량 × 기간)
- **인건비**: `AMOUNT = PRODUCT(D열:G열)` (단가 × 수량 × 개월 × 참여율) — 방식 B/C 전용
- **소계**: 각 섹션의 AMOUNT 합계 (`=SUM(범위)`)

### 합계 구조 (Row 12~17)

| 셀 | 항목 | 수식 (방식 B/C) | 방식 A 처리 |
|---|---|---|---|
| I12 | 1. 합계 | 모든 섹션 소계의 SUM | calc_estimate 의 (s1+s2+s3+s4+ot+rsvpPkg+showup) |
| I13 | 2. 기업이윤 | 인건비 기반 수식 | calc_estimate 의 s5 (PCO 기획료) |
| I14 | 3. 총계 | =I12+I13 | 자동 (수식 유지) |
| I15 | 4. 절사/할인 | 사용자 입력 | 0 (또는 사용자 지정) |
| I16 | 5. 부가세 | =(I14+I15)*0.1 | 자동 |
| I17 | 총 견적 | =I14+I15+I16 | calc_estimate 의 pkVat 와 일치해야 함 |

방식 A에서 무결성 보장: `export_estimate.py` 가 본문 작성 후 `result['pkVat']` 과 셀 I17 결과 일치 여부 자동 verify.

### 데이터 행 삽입 시 주의사항 (v1과 동일)

1. **행 삭제 전 병합 해제 필수**: Row 19+ 영역의 기존 병합셀을 모두 `unmerge_cells()` 로 해제한 후 행을 삭제해야 충돌 방지
2. 카테고리 구분 행 → 아이템 행 → 서브아이템 행 순서를 유지한다
3. 소계 행의 I열에 `=SUM(시작:끝)` 수식을 넣는다
4. 섹션 간 빈 행(구분선, 높이 10)을 삽입한다

### 필수 병합 규칙 (v1과 동일)

- **세부산출내역(Row 19)**: A19:K19 전체 병합
- **열 헤더 REMARKS**: J20:K20 병합
- **모든 데이터 행**: J:K 병합 (카테고리, 아이템, 소계 모두)
- **소계 행**: A:H 병합 + J:K 병합

### 동적 수식 규칙 (v1과 동일)

- **B7 (견적일시)**: `=TODAY()` + 날짜 형식 `YYYY"년 "M"월 "D"일"`
- **B8 (견적금액)**: recalc 또는 calc_estimate 후 한글 변환하여 정적 문자열 기입
- **K9 (RFP 금액)**: 사용자 입력 셀 (파란색 텍스트, 외부 주입)
- **J17 (비율)**: `=IF(K9>0,I17/K9,"")` — RFP 대비 비율, 0% 형식

### 스타일 규칙 (역할→SoT 토큰 매핑은 [jc-design-mapping.md](references/jc-design-mapping.md), 값 정본은 jc-design-system signature-tokens.md §6 JSON 정본)

| 위치 | 시맨틱 역할 | SoT 토큰 | 클라이언트 오버레이 |
|---|---|---|---|
| 세부산출내역 타이틀 (Row 19), 열 헤더 (Row 20), 총 견적 (Row 17) | 헤더·타이틀 | `--jc-primary` | `mc` |
| 카테고리 행 | 액센트·구분 강조 | `--jc-accent` | `mc` |
| 소계 금액 강조 | 위험·금액 강조 | `--jc-danger` | 유니버설 |
| 소계 배경 | 중립 강조 면 | `--jc-border-strong` | 유니버설 |
| 본문 폰트 | 본문 | `--jc-font-ko` + `--jc-text-base` | 유니버설 |

#### 행 높이
- Row 1 (타이틀): 37.5 / Row 2~10: 25.0 / 구분선: 10.0 / 데이터: 25.0

---

## 리멤버 견적서 상세 규칙 (v1과 동일)

### 금액 계산

- **차액**: `F열 = D열(정가) - E열(패키지할인가)`
- **섹션 소계**: total 행에 D/E/F열 각각 SUM
- **PCO 이윤**:
  - 인건비 = 운영비합계(섹션2~5의 F열 합) × 15%
  - 기업이윤 = (운영비합계 + 인건비) × 10%
- **최종 견적**: 모든 섹션 F열 합계 + 할인

### 7개 섹션 (고정 구조)

1. 베뉴 사용료
2. 시스템 구축 비용
3. 디자인 및 브랜딩 비용
4. 운영인력 및 보험
5. 기타 운영비
6. PCO 이윤 (자동 계산)
7. 리멤버 모객 솔루션

사용자가 항목을 제공하지 않은 섹션은 소계 0으로 유지하되 섹션 자체는 삭제하지 않는다.

### 모객 솔루션 섹션 작성 규칙

C열에 타겟팅 조건을 줄바꿈(\n)으로 기재:

```
사전모집은 쇼업 게런티 수에 비례

- 직급 : [{직급 범위}]
- 산업 : [{산업 분야}]
- 직무 : [{직무 분야}]

* KPI 확정 후 모객 규모 및 비용 별도 협의
```

### 스타일 규칙 (역할→SoT 토큰 매핑은 [jc-design-mapping.md](references/jc-design-mapping.md) §3, 값 정본은 jc-design-system signature-tokens.md §6 JSON 정본)

| 위치 | 시맨틱 역할 | SoT 토큰 | 클라이언트 오버레이 |
|---|---|---|---|
| 섹션 라벨 배경 | 포인트·핫 강조 (브랜드 포인트) | `--jc-point-orange` (= `--jc-data-3`) | `remember` |
| 열 헤더 배경 | 중립 다크 헤더 면 (Charcoal 톤) | `--jc-text` | 유니버설 |
| 본문 폰트 | 보조 텍스트·테이블 | `--jc-font-ko` + `--jc-text-sm` (맑은 고딕 레거시 폴백) | `remember` |

#### 행 높이
- 기본 15.75 / 구분선 6.75 / 섹션·열 헤더 29.25

---

## 리멤버 견적서 생성 방식 — 값 교체 우선 원칙

리멤버 견적서는 7개 섹션 고정 구조이므로, **행을 삭제/재생성하지 않고 셀 값만 교체**.

### 셀 위치 맵 (Opt1 기준)

| 섹션 | 헤더 | 열 헤더 | 데이터 시작 | total |
|------|------|---------|-------------|-------|
| 1. 베뉴 | 22 | 23 | 24 | 25 |
| 2. 시스템 | 27 | 28 | 29~34 | 35 |
| 3. 디자인 | 37 | 38 | 39~42 | 43 |
| 4. 운영인력 | 45 | 46 | 47~49 | 50 |
| 5. 기타운영비 | 52 | 53 | 54~56 | 57 |
| 6. PCO이윤 | 59 | 60 | 61~62 | 64 |
| 7. 모객솔루션 | 66 | 67 | 68~69 | 70 |

**주의**: `insert_rows()` / `delete_rows()` 사용 시 수식 범위가 자동 조정되지 않으므로 소계 수식을 반드시 재설정한다.

---

## 코드 작성 원칙

1. **수식 사용 필수** (방식 B/C): 금액은 Python으로 계산하지 말고 반드시 Excel 수식으로 넣는다
2. **자동 산출은 Python에서** (방식 A, v2 신규): `calc_estimate()` + `export_estimate()` 결합
3. **템플릿 복사 우선**: 새 견적서는 항상 assets/의 템플릿을 복사하여 시작한다
4. **서식 보존**: 템플릿의 폰트, 색상, 병합셀, 로고를 최대한 보존한다
5. **외부 주입 변수 엄수**: 공급자·고객사 정보 하드코딩 절대 금지 (CLAUDE.md §10)
6. **체이닝 입력 우선 처리** (v2): ChainPayload JSON이 있으면 별도 정보 수집 없이 자동 진행
7. **§9 검증값 인지**: 100명 표준 (옵션 없음) = 83,750,000원. 자동 산출 결과가 이 값에서 크게 벗어나면 입력값 재확인.
8. **양식 식별자 외 회사명 금지**: 본문·산출물에 구체 회사 상호를 작성하지 않는다. 양식 식별자(`M&C 견적서`·`리멤버 견적서`)만 양식 명칭으로 사용. 공급자·고객사 식별 정보는 모두 외부 주입 변수 (Step 3.5 슬롯). 정본: `jc-design-system/references/shared-rules.md#RULE-NO-COMPANY`.

---

## References

- [pricing-engine.md](references/pricing-engine.md) — calc_estimate 엔진 사용법·공식 (원가 산출)
- [pricing-strategy.md](references/pricing-strategy.md) — 전략 프라이싱(가치기반·Van Westendorp·티어·앵커링), 원가→제안가 결정 논리
- [option-catalog.md](references/option-catalog.md) — 9종 옵션·상호배제 규칙
- [venue-db.md](references/venue-db.md) — 베뉴 DB 스키마 + 슬롯 (데이터 보류)
- [venue-db-realdata.md](references/venue-db-realdata.md) — 베뉴파인더 견적이력 기반 실데이터 25건 (2026-04~05 스냅샷, Sprint 8 입수). 사용 전 주의:
  - `per_pax_rate`·대관료 단독가는 소스에 없어 **여전히 미채움** — calcEstimate 자동 산출 경로는 변경 없이 유지되며 기존 `VENUE_PER_PAX_5STAR` 폴백이 계속 적용된다.
  - 실데이터의 금액 필드(`min_rental`/`max_rental_observed`)는 **견적 총액(F&B 등 포함)이지 대관료 단독이 아니다** — 대관료 라인아이템(s1) 참고 시 반드시 [venue-db-realdata.md](references/venue-db-realdata.md) §0을 먼저 읽을 것.
  - `lookup_venue()`는 아직 실데이터 기준으로 구현되지 않음 — 현재 실질 가치는 수용인원 검증(capacity sanity check)과 지역별 베뉴 후보 제시다.
- [jc-design-mapping.md](references/jc-design-mapping.md) — Excel 색상 → JC 시맨틱 토큰
- [chaining-schema.md](references/chaining-schema.md) — 입출력 JSON 스키마·풀 워크플로우
- [mnc_template.md](references/mnc_template.md) — M&C 양식 상세 사양 (v1 유지)
- [remember_template.md](references/remember_template.md) — 리멤버 양식 상세 사양 (v1 유지)

## Scripts

- [calc_estimate.py](scripts/calc_estimate.py) — 자동 산출 엔진. `python calc_estimate.py` 로 SSOT §9 자가검증
- [export_estimate.py](scripts/export_estimate.py) — Excel 본문 자동 작성 (calc_estimate 결과 → xlsx)
- [korean_amount.py](scripts/korean_amount.py) — 한글 금액 변환

## Assets

- [mnc_template.xlsx](assets/mnc_template.xlsx) — M&C 견적서 템플릿 (양식 식별자 'M&C' 만 포함)
- [remember_template.xlsx](assets/remember_template.xlsx) — 리멤버 견적서 템플릿 (양식 식별자 '리멤버' 만 포함)
