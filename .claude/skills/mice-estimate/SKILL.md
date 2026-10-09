---
name: mice-estimate
version: "v3.3.2"
description: "MICE 행사 견적서를 엑셀(.xlsx)로 생성·수정하는 스킬. 양식은 리멤버 견적서 하나 — 패키지 할인 구조 + PCO 기획료(운영비 25%) 별도 계상, 컨피규레이터 가격 엔진(데이터셋 JSON) 기반 자동 산출 지원. 공공·관 발주의 산출내역서 요청도 같은 양식으로 작성한다. 반드시 이 스킬을 사용해야 하는 상황: 사용자가 '견적서', '견적', 'estimate', '산출내역서', '빠른견적', '견적 뽑아줘', '견적 계산해줘'를 언급할 때. 특히 '리멤버 견적서' 양식 명칭이 명시될 때. 기존 견적서 파일을 수정하거나 항목을 추가/삭제/변경할 때도 이 스킬을 사용한다. 견적 항목을 대화로 전달받아 새로 생성하거나, 기존 파일을 업로드받아 수정하거나, 행사 규모·옵션만 받아 자동 산출하는 세 가지 입력 방식을 모두 지원한다. jc-pptx·mice-rfp-analyzer 체이닝 입력(ChainPayload/v1)을 받아 자동 견적 생성 가능. 공급자·고객사 정보는 모두 외부 주입 변수로 처리 — 스킬 내 어떤 회사·개인 식별 정보도 하드코딩하지 않는다. 형제 경계 — 제안서·견적 요약 슬라이드는 jc-pptx, RFP 분석·입찰가 권고는 mice-rfp-analyzer, 가격 포지션 판단은 jc-strategy-canvas, 경쟁가·지불의향 조사는 mice-market-intel, 견적 숫자 검산·저가수주 리스크는 jc-redteam."
dependencies: openpyxl
---

# MICE 견적서 생성 스킬

## 변경 이력

- v3.3.2 (2026-10-09): 템플릿 자산 정정(`assets/remember_template.xlsx`) — 실명·샘플 헤더(B11·B13·B14·B15·B24·C24, Opt2 G24) → `(외부 주입 - …)` 자리표시자, 섹션 6을 25% 단일 라인 수식(D61·E61·F61·F64·F59)으로, 요약 B17·B19 수식화, 패키지 메타(docProps creator·lastModifiedBy) 인명 제거.
  문서 동기: 셀 위치 맵·방식 B/C 코드 주석·Assets 설명·remember_template.md §2·§3·§5.
- v3.3.1 (2026-10-09): 폐합 스킬 라우팅을 jc-pptx(구 mice-proposal 별칭)·mice-ops-docs·mice-aftermath로 교체, 폐지된 브리프 게이트 문구 삭제, 형제 경계 추가. mice-rfp-analyzer §3-1 전용 봉투(`estimate_hint`) 수용 → 완료 게이트 6 연동.
  샌드박스 고정 경로 → `recalc()` 헬퍼·`outputs/`, 색상은 jc-design-system v2 토큰 런타임 로드(`scripts/estimate_tokens.py`), 긴 버전 히스토리는 `references/changelog.md`로 이관.
- 이전 이력(v3.3.0 ~ v1.0): [references/changelog.md](references/changelog.md)

## 개요

본 스킬은 **리멤버 견적서** 양식(단일 양식, v3.3.0)의 MICE 행사 견적서를 엑셀로 생성·수정한다. 컨피규레이터 가격 엔진 포팅(`calc_estimate_remember`)으로 행사 규모·옵션만 받아 자동 산출(방식 A)이 가능하고, 항목을 직접 받아 작성(방식 B)하거나 기존 파일을 수정(방식 C)할 수도 있다. 공공·관 발주의 "산출내역서" 요청도 같은 양식으로 작성한다.

**자산 정의 원칙**: 본 스킬은 어떤 회사·개인의 식별 정보도 하드코딩하지 않는다. 양식 명칭('리멤버 견적서')만 식별자로 보존되며, 공급자·고객사·담당자·연락처 등 모든 식별 정보는 **외부 주입 변수**로 처리된다. 산출물 본문에는 사용자가 매번 주입하는 변수만 들어간다. (정본: `jc-design-system/references/shared-rules.md#RULE-NO-COMPANY` — 양식 식별자 보존은 정본의 '허용' 항목)


## 워크플로우

### Step 1: 양식 확인

양식은 **리멤버 견적서** 하나다(패키지 할인 구조 + PCO 기획료 25%). "산출내역서"·"공공"·"국가계약법" 요청도 같은 양식으로 작성하되, 발주 서식이 요구하는 항목명(예: 기업이윤·인건비 분리 표기)·합계 구조가 있으면 섹션 안에서 항목명과 비고로 맞춘다. 구 양식(다른 템플릿) 파일을 수정해 달라는 요청(방식 C)은 원 파일 구조를 존중한다.

### Step 2: 입력 방식 판별 (3가지)

| 방식 | 트리거 | 동작 |
|---|---|---|
| **A. 자동 산출** | "빠른견적", "자동 산출", "100명 규모 견적 계산해줘" 등 | `calc_estimate_remember()` + `export_estimate_remember()` |
| **B. 대화 입력 (v1 방식)** | 사용자가 항목·단가를 직접 지정 | 템플릿 복사 후 데이터 채우기 |
| **C. 파일 수정** | 사용자가 기존 견적서 xlsx 업로드 | 해당 파일 로드하여 수정 |

방식 A 실행 순서: ① 엔진 자가검증(`python calc_estimate_remember.py` → ALL PASS 확인) ② `calc_estimate_remember(cfg)` ③ `export_estimate_remember.export_remember_estimate(result, meta, path)` ④ `recalc(path)` ⑤ `verify(path, result)` 0원 일치 확인.

### Step 2.5: 체이닝 입력 감지

`$schema: "ChainPayload/v1"` 봉투가 입력되면(`target`은 힌트 — 없거나 다른 값이어도 `source`가 `jc-pptx`·`mice-rfp-analyzer`이고 `eventScale` 키가 있으면) 별도 정보 수집 없이 방식 A로 진입한다. `source` 판별은 jc-design-system chaining-protocol §7(`detect_input_source`, 별칭 자동 치환) 규칙을 따른다.

| source | estimatedFrom | 읽는 키 (봉투 최상위, 평탄) |
|---|---|---|
| `jc-pptx` (구 `mice-proposal`은 별칭 — 수신 시 `jc-pptx`로 치환) | `proposal_chain` | `client` `eventDate` `eventScale{target,guarantee}` `venue{type,region,name,rental}` `options{9키 불리언}` `displayType`(`led`·`projector`) `boothCount` `format`. 같은 봉투의 `deck_meta`·`sections`·`coverage_map`·`presentation`은 견적과 무관 — 무시 |
| `mice-rfp-analyzer` (§3-1 전용 봉투) | `rfp_default` | `client` `rfpId` `eventDate` `budgetRange{min,max,currency,vatIncluded}` `evaluationCriteria[{name,weight}]` `eventScale` `venue`(null 가능) `options`(null 가능) `boothCount` `format` `notes` + **`estimate_hint{budget_announced, estimated_cost, recommended_bid, vat, risk_premium}`** |

- `estimate_hint`는 calc 입력이 아니다. 산출 후 제안가(`pk`·`pkVat`)를 `budget_announced`·`recommended_bid`와 대비해 어디에 있는지 한 줄로 명시한다 → Step 6.5 완료 게이트 6(가격 산식 연동)의 입력.
- `venue: null` → 대관료 자동 산출, `options: null` → 옵션 전부 미적용, `guarantee: null` → target, `displayType` 없으면 `led`.

봉투 예시·필드 매핑표는 [references/chaining-schema.md](references/chaining-schema.md) §2(jc-pptx)·§3(mice-rfp-analyzer) 참조.

### Step 3: 필수 정보 수집

#### 방식 A (자동 산출) — 최소 입력

| 항목 | 설명 | 필수 |
|------|------|------|
| 행사명 (project_title) | 시트명·파일명에 사용 | ✅ |
| target | 총 참석인원 (40~500) | ✅ |
| guarantee | 모객 게런티 | 선택 (None이면 target) |
| 옵션 | 데이터셋 옵션(`assets/remember_pricing_dataset_v1.json`의 options) 중 활성화 | 선택 |
| venueName | 베뉴명 (참조용) | 선택 |
| displayType | `led`(기본) 또는 `projector` — 스케일러·화면중계 과금 게이트 | 선택 |
| boothCount | 부스 수 | 선택 (default 0) |
| **공급자 정보 슬롯** (Step 3.5) | 외부 주입 변수 | 사용자가 매번 제공 |
| **고객사 정보 슬롯** (Step 3.5) | 외부 주입 변수 | 사용자가 매번 제공 |

→ `calc_estimate_remember(cfg)` 호출 → `export_remember_estimate(result, meta, path)` 로 리멤버 견적서 자동 작성 → recalc → `verify()`.

#### 방식 B/C (수동) — v1과 동일

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

#### 리멤버 양식 슬롯

같은 슬롯이 방식에 따라 다른 곳에 들어간다 — **방식 A**는 `export_remember_estimate()`가 5~9행에 자체 레이아웃을 만들며 `meta` dict의 아래 키만 읽는다. **방식 B/C**는 템플릿(`assets/remember_template.xlsx`)의 G11~G16 셀에 직접 쓴다.

| 슬롯 | 방식 A — `meta` 키 (기입 셀) | 방식 B/C — 템플릿 셀 |
|---|---|---|
| 제안일자 | `proposal_date` (G5) | G11 |
| 유효기간 | `validity` (G6, 기본 "제안일자로 부터 30일") | G12 |
| 공급자 상호 | `supplier_company` (G7) | G13 |
| 주소 | `supplier_address` (G8) | G14 |
| 담당자 | `supplier_manager` (G9) | G15 |
| 연락처 | **행 없음** — 필요하면 `supplier_manager` 값에 병기 | G16 |
| 행사·고객사 | `project_title`(B5, 필수) · `venue_text`(B7 + 섹션 1 장소 사용료 행 C16) · `venue_type`(B16 '내용', 기본 "5성급 호텔") · `remark`(B8) · `quote_date`(B9) · `targeting`(모객 C열) · `sheet_name` · `booth_count`/`booth_premium_count`(부스 단가×수량 분해, 선택) | B11 행사명 · B12 패키지 · B13 베뉴 · B14 비고 · B15 견적일 |

방식 A `meta`에 `venue`·`note`·`validity_period`·`package_type`·`supplier_contact` 같은 다른 이름을 쓰면 **조용히 무시되어 기본값이 기입**된다(베뉴 공란·비고 "1일 full day 기준"·유효기간 기본값) — 위 키 이름 그대로 쓴다.

#### 수집 방식 권장 순서

1. 사용자가 첫 견적 요청 시 공급자 정보 일괄 수집 → 사용자 메모리에 저장 권장 (스킬 자체와 별도)
2. 이후 견적 생성 시 메모리에서 자동 채움 + 변경분만 추가 입력
3. 한 번도 입력되지 않은 경우 명시적으로 묻기 — 추정·임의값 사용 금지

### Step 4: 견적서 생성/수정

#### 레퍼런스 파일 읽기 (필수)

작업 전 반드시 해당 양식의 레퍼런스를 읽는다:

| 양식·방식 | 읽을 reference |
|---|---|
| 방식 B/C (수동) | `references/remember_template.md` |
| 방식 A (자동 산출) | `references/remember_template.md` + `assets/remember_pricing_dataset_v1.json`(단가·산식·골든 벡터) |
| 방식 A + 베뉴 룩업 시 | `references/venue-db.md` |
| 체이닝 입력 처리 | `references/chaining-schema.md` |

#### 방식 A: 컨피규레이터 엔진 자동 산출 (리멤버 견적서)

```python
import sys, subprocess
from datetime import date
from pathlib import Path
SKILL = Path('<이 스킬 폴더>')              # 예: Path.home()/'.claude/skills/synced/<bucket>/mice-estimate'
sys.path.insert(0, str(SKILL / 'scripts'))
from calc_estimate_remember import calc_estimate_remember
from export_estimate_remember import export_remember_estimate, recalc, verify
YYMMDD = date.today().strftime('%y%m%d')

subprocess.run([sys.executable, str(SKILL / 'scripts' / 'calc_estimate_remember.py')], check=True)  # ① ALL PASS 아니면 사용 금지

cfg = {
    'target': 100,            # 총 참석 인원
    'guarantee': 100,         # 모객 게런티(없으면 target)
    'venueName': '(외부 주입)',
    'displayType': 'led',     # 'led' | 'projector'
    'options': {},            # 데이터셋 options 키 중 활성화할 것만 True
    'boothCount': 0,
}
result = calc_estimate_remember(cfg)                                              # ② 산출

meta = {                                   # 공급자·고객사 정보는 매번 주입(Step 3.5) — 키 이름은 export_remember_estimate()가 읽는 그대로
    'project_title': '(외부 주입)',                                     # 필수 — B5·파일명
    'venue_text': '(외부 주입)', 'venue_type': '5성급 호텔',             # B7·C16 / B16(섹션 1 '내용')
    'remark': '(일시·규모 등)', 'quote_date': '(외부 주입)',             # B8 / B9
    'proposal_date': '(외부 주입)', 'validity': '제안일자로 부터 30일',   # G5 / G6
    'supplier_company': '(외부 주입)', 'supplier_address': '(외부 주입)', 'supplier_manager': '(외부 주입)',  # G7~G9 (연락처 행 없음)
    'targeting': '(모객 C열 텍스트, 선택)', 'sheet_name': '리멤버MICE솔루션',
    # 체이닝 봉투용(§7 to_chain_payload가 읽음) — 상류 봉투가 있으면 clientId·projectTitle 무변경 승계
    'projectTitle': '(외부 주입)', 'clientId': None, 'venueName': cfg['venueName'],
    'createdAt': date.today().isoformat(), 'estimatedFrom': 'auto_calc',   # 체이닝 입력이면 'proposal_chain' | 'rfp_default'
}
if cfg['boothCount']:
    meta['booth_count'] = cfg['boothCount']                                       # 섹션 5 부스 행 단가×수량 분해
out = Path('outputs') / f'리멤버견적서_{meta["project_title"]}_{YYMMDD}.xlsx'; out.parent.mkdir(exist_ok=True)
export_remember_estimate(result, meta, str(out))                                  # ③ xlsx 작성(7섹션·옵션 O/X·PCO 수식·상단 합계)
recalc(str(out))                                                                  # ④ xlsx 스킬 recalc.py → 없으면 LibreOffice headless
verify(str(out), result)                                                          # ⑤ D10↔pk · D11↔pk_excluding_options 0원 일치 게이트
meta['estimateFile'] = str(out)                                                   # §7 봉투 estimateFile
```

#### 방식 B/C: v1 수동 입력 (변경 없음)

```python
import shutil
from pathlib import Path
from openpyxl import load_workbook

SKILL = Path('<이 스킬 폴더>')
template = SKILL / 'assets' / 'remember_template.xlsx'
output = Path('outputs') / '리멤버견적서_{{event_name}}_{{YYMMDD}}.xlsx'; output.parent.mkdir(exist_ok=True)
shutil.copy(template, output)
wb = load_workbook(output)
# 단일 옵션 견적이면 미사용 시트는 삭제(남는 시트의 로고는 보존 — 이미지는 시트별 앵커): del wb['Opt2_350명']
for ws in wb.worksheets:   # 두 시트 모두 `(외부 주입 - …)` 자리표시자·샘플 리터럴을 갖는다 — 남기는 시트는 전부 채운다
    # 헤더·베뉴 셀(B11·B13·B14·B15·B24·C24)은 `(외부 주입 - …)` 자리표시자 — 주입값으로 교체
    ws['B11'] = '{{event_name}}'; ws['B13'] = ws['B24'] = '{{venue}}'; ws['B14'] = '{{remark}}'; ws['C24'] = '{{venue_spec}}'
    ws['B15'] = '{{quote_date}}'  # 날짜 서식 셀(yyyy"년" m"월" d"일" 유지) — 문자열·datetime 모두 주입 가능
    ws['G13'] = meta['supplier_company']  # Step 3.5 슬롯(G11~G16) — 절대 하드코딩 금지
    # ...
    # 세부 항목 행 작성
    # ...

wb.properties.creator = 'mice-estimate'; wb.properties.lastModifiedBy = None   # 파일 메타(docProps)에도 인명 미기재 — RULE-NO-COMPANY
wb.save(output)
```

**중요**: 템플릿을 복사하면 병합셀·서식은 보존되고, 로고·직인 이미지는 **복사한 시트를 그대로 쓸 때만** 보존된다. 시트를 삭제하거나 새로 만들면 이미지는 따라오지 않는다 — "앵커 객체(로고·직인) 보존 규칙" 절 참조.

### Step 5: 수식 재계산 (방식 B/C — 방식 A는 ④에서 수행)

`export_estimate_remember.recalc(path)` 헬퍼 하나로 재계산한다(방식 A·B/C 공통):

1. xlsx 스킬의 `recalc.py` 탐색 — 환경변수 `XLSX_RECALC`(파일 경로) → 형제 스킬 폴더 `xlsx/scripts/recalc.py` → `~/.claude/skills/xlsx/scripts/recalc.py` → `~/.claude/skills/synced/*/xlsx/scripts/recalc.py` 순. 찾으면 `python recalc.py <파일>`로 실행.
2. 없으면 LibreOffice headless(`soffice --headless --convert-to xlsx`)로 재계산한 결과로 원본을 교체한다.
3. 둘 다 없으면 한국어 안내를 출력하고 `False`를 돌려준다 — 이때는 **Excel에서 열어 저장**(수식 계산)한 뒤 `verify()`를 돌린다.

```python
from export_estimate_remember import recalc, verify
ok = recalc(str(output))        # True = 재계산 완료 / False = Excel 저장 후 verify 필요
```

재계산 후 합계 셀을 다시 읽어 섹션 소계·최종 견적이 맞는지 확인한다. 한글 금액 표기가 필요하면 `korean_amount.py`의 `num_to_korean()`을 쓴다(방식 A는 `export_estimate_remember`가 정적 한글 + TEXT 동적 숫자 하이브리드로 자동 기입).

### Step 6: 출력

완성 파일은 작업 폴더의 `outputs/`에 `리멤버견적서_{{event_name}}_{{YYMMDD}}.xlsx`로 저장한다. 전달은 환경에 따라 — claude.ai에서는 present_files로 파일을 첨부하고, Claude Code에서는 저장 경로를 안내한다(파일 카드가 필요하면 그 환경의 파일 전달 도구를 쓴다).

체이닝 후속 스킬(jc-pptx ⑦예산 · mice-ops-docs 예산 집행률 · mice-aftermath 계획 예산)에 전달할 ChainPayload JSON이 필요하면 [chaining-schema.md §7](references/chaining-schema.md) 의 `to_chain_payload()` 헬퍼를 쓴다 — 호출: `payload = to_chain_payload(result, meta, cfg, target='jc-pptx', skill_dir=SKILL)`. `cfg`는 ② 입력(`optionsApplied`를 여기서 만든다), `meta`는 방식 A의 meta 그대로(`estimatedFrom` 필수), `skill_dir`는 세션에 붙여넣어 쓸 때 필수(`__file__` 없음), `target`은 `'jc-pptx'`·`'mice-ops-docs'`·`'mice-aftermath'`·`None`(공통). 저장: `.chaining/{{event_name}}_{{YYYYMMDD}}_to_{{target}}.json`.

### Step 6.5: 완료 게이트 (증거주의 — 통과 전 전달 금지)

견적서는 숫자가 곧 신뢰다. 전달 직전 아래를 실제로 실행·확인하고, 미통과면 수정 후 재검증한다:

1. **엔진 자가검증** (방식 A): `python scripts/calc_estimate_remember.py` 실행 → "ALL PASS — golden 14 + adjustment 1 + grid 47행" 확인. 실패 시 엔진·입력을 의심하고 임의 보정 금지.
2. **3중 금액 일치**: 엔진 결과(`pk`·`pk_excluding_options`) ↔ 시트 합계 셀(D10·D11) ↔ 한글 금액 표기가 동일한가 — 셀 값을 다시 읽어 대조한다(눈대중 금지).
3. **재오픈 무결성**: 산출 .xlsx를 openpyxl로 재로드해 깨짐·수식 오류(#REF! 등)가 없는가.
4. **입력 반영 전수성**: 요청·체이닝 입력의 인원·기간·옵션·특이 요구가 각각 어느 행에 반영됐는지 대응을 확인한다 — 누락 항목 0건.
5. **식별정보**: 슬롯 주입값 외 회사·개인 식별정보 하드코딩 0건 (RULE-NO-COMPANY).
6. **가격 산식 연동** (mice-rfp-analyzer 체이닝의 `estimate_hint` 또는 RFP 가격 점수 산식 존재 시): 제안가(`pk`·`pkVat`)가 `budget_announced`·`recommended_bid`(최적 입찰가 구간) 대비 어디에 있는지 한 줄 명시해 전달한다. `estimate_hint.vat`에 맞춰 비교 기준(VAT 별도/포함)을 맞춘다.
7. **앵커 객체 보존**: 로고·직인이 산출물에 실제로 들어 있는가 — ① 시트별 `ws._images` 수 ② 저장본 `xl/media/` 존재 ③ recalc 후 재확인. 시트를 새로 만들거나 삭제한 작업이면 **필수**. 금액 검증은 이 결함을 걸러내지 못한다.

확인 불가 항목(예: 발주가 미공개)은 "미확인"으로 표기하고 완료 주장하지 않는다.

---

## 전략 프라이싱 (선택 — 원가→제안가)

`calc_estimate_remember`(데이터셋 단가·산식)가 *원가·마진*을 산출한다면, 견적의 **제안가·할인폭·패키지 가격을 전략적으로** 정해야 할 때는 [pricing-strategy.md](references/pricing-strategy.md)를 참조한다. 4대 레버(가치기반·Van Westendorp 가격민감도·티어/패키지 구조·앵커링)로 "얼마에 제안할까"를 설계한다.

- 기계적 원가 산출만 필요하면 이 절을 건너뛴다(과함).
- 경쟁가·지불의향 *조사*는 `mice-market-intel`, 가격 포지션 *판단*은 `jc-strategy-canvas`, *원가*는 `calc_estimate_remember`. 본 절은 그 사이 가격 *결정 논리*.
- 데이터 없는 지불의향·경쟁가는 `[가설]` — 추정 금지. 저가수주 리스크·낙관 마진은 `jc-redteam`으로 점검.

## 리멤버 견적서 상세 규칙

### 금액 계산

- **차액**: `F열 = D열(정가) - E열(패키지할인가)`
- **섹션 소계**: total 행에 D/E/F열 각각 SUM
- **PCO 기획료 (운영비의 25% — SSOT: calcEstimate.js, v3.1.0 정정)**:
  - **opCost = s1(베뉴)+s2(시스템)+s3(디자인)+s4(운영)+ot(옵션)+rsvpPkg(사전신청 관리)+genManage(참관객)** — **쇼업 보장(showup) 비용만 제외**, leadPkg 조정 델타 미포함
  - **PCO 기획료 = floor(opCost × 0.25 / 10000) × 10000** — 만원 미만 절사(반올림 아님), 단일 라인 별도 계상(섹션 6)
  - (레거시 참고) 구 v2 방식은 인건비(운영비 15%) + 기업이윤(10%)의 2단 구조였다. v3부터 직접비 25% 단일 기획료로 대체. 기존 파일(방식 C) 수정 시에는 원 파일 구조를 존중하되 신규 생성은 25% 방식을 기본으로 한다.
- **최종 견적**: 모든 섹션 F열 합계 + 할인

### "질문이 필요 없는 견적서" 원칙 (2026-08-03 확정 preference, D1-③)

리멤버 견적서는 **평이한 한국어 항목명**을 사용한다 — 발주처·사무국이 항목만 보고 무엇인지 즉시 이해해 되묻지 않도록 한다.

- 전문 약어·영문 직역·내부 코드명 대신 일상 한국어로 풀어 쓴다 (예: "RSVP 솔루션" → "사전신청 관리", "M/M" → "투입 인월").
- 한 항목이 무엇을 포함하는지 DESCRIPTION 열에서 한 줄로 설명한다.
- 추가 설명 없이는 이해 못 할 항목명은 지양한다 — "이게 뭐냐"는 후속 질문이 나오면 항목명을 다시 손본다.

### 7개 섹션 (고정 구조)

1. 베뉴 사용료
2. 시스템 구축 비용
3. 디자인 및 브랜딩 비용
4. 운영인력 및 보험
5. 기타 운영비
6. PCO 기획료 (직접비 25% — 자동 계산)
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

### 스타일 규칙 (색은 jc-design-system v2 토큰 런타임 로드)

값(HEX)은 문서에 적지 않는다 — `scripts/estimate_tokens.py`의 `palette()`가 `jc-design-system/references/signature-tokens.md` §6 JSON에서 역할별 색을 읽어 `export_estimate_remember.py`의 `ST` 스타일에 채우고, 로드 실패 시에만 §6 값을 출처 주석과 함께 둔 폴백 상수를 쓴다(`palette()["_source"]`로 `sot:`/`fallback` 확인). 글꼴 크기·굵기·정렬·테두리·숫자서식·열 너비·행 높이는 컨피규레이터 실측 레이아웃 그대로 — 바뀌는 것은 색뿐. 매핑 정본은 [jc-design-mapping.md](references/jc-design-mapping.md) §3.

| 위치 | 역할(palette 키) | §6 키 |
|---|---|---|
| 타이틀·섹션 합계 배경 | `ink` | `color.primary` |
| 열 헤더 배경 | `inkSoft` | `color.primarySoft` |
| 다크 면 위 글자(타이틀·라벨·헤더) | `paper` | `color.surface` |
| 섹션 라벨 배경·총액 글자 (리멤버 오렌지) | `accent` | `color.accent` |
| 총액 행 배경 | `accentSoft` | `color.accentSoft` |
| 회색 라벨 / 소계 행 배경 | `surfaceAlt` / `surfaceSoft` | `color.surfaceAlt` / `color.surfaceSoft` |
| 섹션 헤더 배경 | `amberTint` | `color.point.amberTint` |
| 경고 문구 글자 / 배경 | `accentStrong` / `warningBg` | `color.accentStrong` / `color.semantic.warningBg` |
| 안내 문구 글자 / 배경 | `steel` / `steelTint` | `color.point.steel` / `color.point.steelTint` |
| 푸터 글자 | `danger` | `color.semantic.danger` |
| 본문 서체·크기·굵기 | (매체값 10pt 유지) | `font.ko` · `size.sm` · `weight.bold` |

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
| 6. PCO 기획료 | 59 | 60 | 61 (62~63 예비) | 64 |
| 7. 모객솔루션 | 66 | 67 | 68~69 | 70 |

**주의**: `insert_rows()` / `delete_rows()` 사용 시 수식 범위가 자동 조정되지 않으므로 소계 수식을 반드시 재설정한다.

**섹션 6(방식 B 템플릿 복사 시)**: 템플릿 `assets/remember_template.xlsx`의 59~64행은 25% 단일 라인 — D61 `=F25+F35+F43+F50+F57+F68`(섹션 1~5 total + F68 = 섹션 7 68행 모집리드·사전모집 = `rsvpPkg`, 쇼업 F69 제외) · E61 0.25 · F61 `=FLOOR(D61*E61,10000)` · F64 `=F61` · F59 `=F64`, 요약 B17 `=F25+F35+F43+F50+F57+F64+F70` · B19 `=B17+B18`. **값 교체만 하면 되고 행 치환은 불필요**하다.
62~63행은 섹션 6 예비(빈 행, 스타일·병합 유지). 섹션 6에 라인을 추가해 62·63행을 쓰면 F64를 `=SUM(F61:F63)`로 바꾼다. 참관객 관리 등 직접비 항목은 섹션 7(68~69행 아래 insert — 위 주의대로 F70·B17 참조 재설정)에 넣고, 그 F셀을 D61 수식에 더한다(쇼업 보장 F69는 계속 제외).

---

## 앵커 객체(로고·직인) 보존 규칙 (v3.2.0 신규)

xlsx의 로고·직인 이미지는 워크북이 아니라 **개별 시트에 앵커**된다(`xl/drawings/drawingN.xml` ↔ 시트 rels). 시트를 지우면 그 시트에 얹힌 이미지도 함께 사라진다. 금액·수식·서식은 멀쩡하므로 **금액 검증만으로는 절대 걸러지지 않는다.**

### 소실이 발생하는 경로

| 작업 경로 | 이미지 | 대응 |
|---|---|---|
| 템플릿 복사 → 기존 시트에 값만 교체 | 보존 | 조치 불필요 — **권장 경로** |
| 템플릿 복사 → `create_sheet()`로 새 시트 → 원본 시트 `del wb[name]` | **소실** | 앵커 재삽입 필수 |
| `copy_worksheet()`로 시트 복제 | **소실** (openpyxl은 이미지를 복제하지 않는다) | 앵커 재삽입 필수 |
| `load_workbook()` → `save()` 왕복 | 대체로 보존, 버전에 따라 유실 | 저장 후 게이트로 확인 |

리멤버 견적서의 "값 교체 우선 원칙"은 이 소실을 구조적으로 회피하는 장치이기도 하다. 시트를 새로 만들어야 하는 변환 작업에서만 아래 절차가 필요하다.

### 앵커 좌표 추출

눈대중 배치 금지 — 원본 `drawing1.xml`의 EMU 값을 그대로 재사용한다.

```python
import zipfile, re

with zipfile.ZipFile(SRC) as z:
    xml = z.read('xl/drawings/drawing1.xml').decode()
    open(LOGO, 'wb').write(z.read('xl/media/image1.png'))

# Excel 저장본 = 기본 네임스페이스(접두사 없음)+twoCellAnchor / openpyxl 저장본 = xdr: 접두사+oneCellAnchor → 둘 다 대응
f = re.search(r'<(?:xdr:)?from>\s*<(?:xdr:)?col>(\d+)</(?:xdr:)?col>\s*<(?:xdr:)?colOff>(\d+)</(?:xdr:)?colOff>'
              r'\s*<(?:xdr:)?row>(\d+)</(?:xdr:)?row>\s*<(?:xdr:)?rowOff>(\d+)</(?:xdr:)?rowOff>', xml)
e = re.search(r'<(?:xdr:|a:)?ext\b[^>]*\bcx="(\d+)"[^>]*\bcy="(\d+)"', xml)  # oneCellAnchor <xdr:ext> 또는 xfrm <a:ext>
COL, COL_OFF, ROW, ROW_OFF = map(int, f.groups())
CX, CY = map(int, e.groups())   # 1 px = 9,525 EMU (96 DPI)
```

### 재삽입

```python
from openpyxl.drawing.image import Image as XLImage
from openpyxl.drawing.spreadsheet_drawing import OneCellAnchor, AnchorMarker
from openpyxl.drawing.xdr import XDRPositiveSize2D

def add_anchored_image(ws, path, col, col_off, row, row_off, cx, cy):
    img = XLImage(path)
    img.anchor = OneCellAnchor(
        _from=AnchorMarker(col=col, colOff=col_off, row=row, rowOff=row_off),
        ext=XDRPositiveSize2D(cx, cy))
    ws.add_image(img)
```

새 시트를 만드는 즉시 호출한다 — 마지막에 몰아서 처리하면 시트 하나를 빠뜨리기 쉽다.

### 저장 전 게이트 (필수)

```python
for name in wb.sheetnames:
    n = len(wb[name]._images)
    assert n == EXPECTED, f'{name}: 앵커 이미지 {n}개 (기대 {EXPECTED})'
wb.save(OUT)

with zipfile.ZipFile(OUT) as z:
    assert [n for n in z.namelist() if n.startswith('xl/media/')], '저장본에 이미지 없음'
```

`recalc.py`는 LibreOffice 왕복이므로 **재계산 후에도 한 번 더 확인**한다. 동일 이미지가 여러 시트에 있으면 이 단계에서 하나로 병합되는데, 이는 정상 동작이다.

### 외부 주입 직인 슬롯

공급자 직인·로고는 Step 3.5의 `supplier_logo` 슬롯이며 외부 주입 대상이다. 템플릿 자산에 특정 법인의 직인 이미지가 embed된 채로 남아 있으면 공급자 슬롯과 무관하게 그 직인이 찍혀 나간다. 템플릿 자산을 수정하거나 동기화할 때 `xl/media/` 실물을 확인한다 — 파일 크기 급증은 이미지 잔존 신호다.

```bash
unzip -l assets/<템플릿>.xlsx | grep -E 'media|drawing'
```

---

## 코드 작성 원칙

1. **수식 사용 필수** (방식 B/C): 금액은 Python으로 계산하지 말고 반드시 Excel 수식으로 넣는다
2. **자동 산출은 Python에서** (방식 A): `calc_estimate_remember()` + `export_remember_estimate()` 결합
3. **템플릿 복사 우선**: 새 견적서는 항상 assets/의 템플릿을 복사하여 시작한다
4. **서식·앵커 객체 보존**: 폰트·색상·병합셀은 셀 스타일이라 시트를 새로 만들어도 복제할 수 있지만, 로고·직인은 **시트에 앵커된 별도 객체**라 셀 스타일 복제로 따라오지 않는다. 시트를 삭제·신규 생성하는 경로에서는 앵커 재삽입 + 저장 전 게이트를 반드시 거친다
5. **외부 주입 변수 엄수**: 공급자·고객사 정보 하드코딩 절대 금지 (정본: `jc-design-system/references/shared-rules.md#RULE-NO-COMPANY`)
6. **체이닝 입력 우선 처리** (v2): ChainPayload JSON이 있으면 별도 정보 수집 없이 자동 진행
7. **골든 벡터 인지**: 데이터셋 golden 14건·headcount grid 47행이 엔진 자가검증의 기준값이다. 자동 산출 결과가 같은 인원대의 골든 값에서 크게 벗어나면 입력값 재확인.
8. **양식 식별자 외 회사명 금지**: 본문·산출물에 구체 회사 상호를 작성하지 않는다. 양식 식별자(`리멤버 견적서`)만 양식 명칭으로 사용. 공급자·고객사 식별 정보는 모두 외부 주입 변수 (Step 3.5 슬롯). 정본: `jc-design-system/references/shared-rules.md#RULE-NO-COMPANY`.

---

## References

- [changelog.md](references/changelog.md) — 변경 이력 원문(v3.3.0 ~ v1.0). 최신 항목은 본 문서 '## 변경 이력'
- [pricing-strategy.md](references/pricing-strategy.md) — 전략 프라이싱(가치기반·Van Westendorp·티어·앵커링), 원가→제안가 결정 논리
- [venue-db.md](references/venue-db.md) — 베뉴 DB 스키마 + 슬롯 (데이터 보류)
- [venue-db-realdata.md](references/venue-db-realdata.md) — 베뉴파인더 견적이력 기반 실데이터 25건 (2026-04~05 스냅샷, Sprint 8 입수). 사용 전 주의:
  - `per_pax_rate`·대관료 단독가는 소스에 없어 **여전히 미채움** — 자동 산출 경로는 데이터셋의 베뉴 단가 규칙을 따른다.
  - 실데이터의 금액 필드(`min_rental`/`max_rental_observed`)는 **견적 총액(F&B 등 포함)이지 대관료 단독이 아니다** — 대관료 라인아이템(s1) 참고 시 반드시 [venue-db-realdata.md](references/venue-db-realdata.md) §0을 먼저 읽을 것.
  - `lookup_venue()`는 아직 실데이터 기준으로 구현되지 않음 — 현재 실질 가치는 수용인원 검증(capacity sanity check)과 지역별 베뉴 후보 제시다.
- [jc-design-mapping.md](references/jc-design-mapping.md) — Excel 셀 역할 → jc-design-system §6 키 매핑(값 없음 — `estimate_tokens.py` 런타임 로드)
- [chaining-schema.md](references/chaining-schema.md) — 입출력 JSON 스키마(입력 jc-pptx·mice-rfp-analyzer / 출력 jc-pptx·mice-ops-docs·mice-aftermath)·직렬화 헬퍼
- [remember_template.md](references/remember_template.md) — 리멤버 양식 상세 사양(템플릿 v3.3.2 실측 셀·수식·스타일)

## Scripts

- [calc_estimate_remember.py](scripts/calc_estimate_remember.py) — 리멤버 양식 자동 산출 엔진 (v3.1.0). `python calc_estimate_remember.py` 로 golden 14+adjustment 1+grid 47행 자가검증
- [export_estimate_remember.py](scripts/export_estimate_remember.py) — 리멤버 견적서 xlsx 자동 작성 브리지 + `recalc()` 재계산 헬퍼 + `verify()` 무결성 게이트. `--self-test`로 export→recalc→verify 왕복과 토큰 출처(`_source`) 확인
- [estimate_tokens.py](scripts/estimate_tokens.py) — jc-design-system v2 토큰 런타임 로더. `palette()` 역할명 → HEX, `_source`로 SoT/폴백 구분 (v3.3.1)
- [korean_amount.py](scripts/korean_amount.py) — 한글 금액 변환

## Assets

- [remember_template.xlsx](assets/remember_template.xlsx) — 리멤버 견적서 템플릿(방식 B/C 수동 입력용 — 방식 A는 export_estimate_remember가 레이아웃 자체 생성). 자리표시자만(실명 0 — 셀·docProps 메타 모두; 두 시트 B11·B13·B14·B15·B24·C24 `(외부 주입 - …)`)·섹션 6 25% 단일 라인(D61·E61·F61·F64·F59 수식)·요약 수식(B17·B19), 그 외 금액은 샘플 리터럴(방식 B가 덮어씀). 복사 직후 자리표시자를 주입값으로 교체(RULE-NO-COMPANY, Step 6.5 게이트 5)
- [remember_pricing_dataset_v1.json](assets/remember_pricing_dataset_v1.json) — 컨피규레이터 단가·산식·골든 벡터 SSOT 스냅샷 (v3.1.0)
