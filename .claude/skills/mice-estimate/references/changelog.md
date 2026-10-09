# 변경 이력 (mice-estimate)

SKILL.md `## 버전 히스토리`(v3.3.0 ~ v1.0)를 v3.3.1에서 원문 그대로 옮긴 파일이다. 최신 항목(v3.3.1~)은 SKILL.md `## 변경 이력`에 두고, 다음 버전업 때 이 파일로 내려보낸다. 아래 본문에 나오는 폐합 스킬명·삭제된 파일명은 당시 사실의 기록이다(이력 문맥).

---

### v3.3.0 — 2026-10-01 (양식 단일화 — 회사 계정 반입판)

**전 직장 양식 전면 제거, 리멤버 양식으로 통일**(기획자님 지시 2026-10-01: "전 직장의 견적양식은 현 직장의 견적양식으로 전면 교체"). 회사 계정 이관 패키지에서 수정한 판본 — 정본(library) 재빌드 시 같은 변경을 적용할 것.

#### 삭제
- `mnc_template.xlsx`(구 산출내역서 공공형 템플릿), `mnc_template.md`, `pricing-engine.md`, `option-catalog.md`, `calc_estimate.py`, `export_estimate.py` — 공공형 양식 전용 자산·엔진 6종.
- 체이닝 `format` 분기(`mnc`/`remember`) 제거 — 항상 리멤버 양식. 공공·관 발주(국가계약법 산출내역서)도 리멤버 양식으로 작성하되 발주 서식이 요구하는 항목명·합계 구조만 맞춘다.

#### 유지
- 리멤버 양식 자동 산출(`calc_estimate_remember.py` + `export_estimate_remember.py`, 데이터셋 `remember_pricing_dataset_v1.json`), 수동 입력(방식 B/C), 앵커 객체 보존 규칙, 전략 프라이싱, 베뉴 DB.

### v3.2.0 — 2026-09-21 (앵커 객체 보존 규칙)

**로고·직인 소실 사고 재발 방지.** 양식 변환 작업 중 시트 삭제로 로고가 소실된 사례에서 도출.

#### 신규 추가
- **"앵커 객체(로고·직인) 보존 규칙"** 절 — 이미지가 워크북이 아니라 **시트**에 앵커된다는 사실, 소실이 일어나는 4개 경로, 앵커 좌표(EMU) 추출·재삽입 코드, 저장 전 assert 게이트.
- Step 6.5 완료 게이트 **7번 항목(앵커 객체 보존)** — 시트별 이미지 수 + 저장본 `xl/media/` 존재 + recalc 후 재확인 3단 검사.

#### 정정
- 방식 B/C 코드 블록 하단 "템플릿을 복사하면 로고 이미지, 병합셀, 서식이 모두 보존된다" → **"복사한 시트를 그대로 쓸 때만 보존된다"** 로 단서 명기. 시트를 지우거나 새로 만들면 이미지는 따라오지 않는다.
- 코드 작성 원칙 4번 "서식 보존" → 앵커 객체를 서식과 분리해 명시.
- (jc-redteam 감수 반영) 앵커 좌표 추출 정규식 — 명세 원문은 `xdr:` 접두사·oneCellAnchor만 가정해 **Excel 저장본(기본 네임스페이스·twoCellAnchor, 구 공공형 템플릿 포함)에서 매치 실패→크래시**. 접두사 유무·`<a:ext>` 폴백까지 대응하도록 보정, 실파일 3종 실측 통과.

### v3.1.0 — 2026-08-20 (Sprint 1.6 백로그 해소 — 리멤버 양식 자동 산출)

**컨피규레이터 산출 엔진 0원 이식.** 단일 출처: `src/lib/calcEstimate.js`(커밋 b210ce3) → `assets/remember_pricing_dataset_v1.json` 스냅샷.

#### 신규 추가
- `scripts/calc_estimate_remember.py` — 리멤버 양식 자동 산출 엔진(방식 A). 단가·산식은 데이터셋 JSON 로드(하드코딩 0). 베뉴 택1·스케일러 이중 규칙(≥100 & LED→s2 / <100→옵션)·화면중계 LED 게이트·PCO 만원 절사·참관객(genManage)·조정 델타·KPI 인정선 라벨 구현. CLI 자가검증: **golden 14 + adjustment 1 + headcount_grid 47행 = 0원 일치** 통과 전 사용 금지.
- `scripts/export_estimate_remember.py` — 산출 결과 → 리멤버 견적서 xlsx 자동 작성 브리지. 컨피규레이터 `exportEstimate.js` 출력 레이아웃 실측 재현(다크 타이틀·오렌지 라벨·7섹션·옵션 O/X 자동 재계산·PCO FLOOR 수식·상단 D10/D11 합계). recalc 후 `verify()`로 D10↔pk·D11↔pk_excluding_options 무결성 게이트.
- `assets/remember_pricing_dataset_v1.json` — 단가 상수·산식 원문·골든 벡터 SSOT 스냅샷. 컨피규레이터 엔진 변경 시 `exportPricingDataset.mjs`로 재생성해 교체(버전 필드 동기화).

#### 정정 (SSOT 대조)
- 리멤버 PCO 산식 서술 정정: **opCost = s1+s2+s3+s4+ot+rsvpPkg+genManage** — 쇼업 보장(showup)·leadPkg 조정 델타만 제외, `floor(opCost×0.25/10000)×10000` 만원 미만 절사. 구 v3.0.0의 "직접비 = 섹션2~5 합, 모객비용 제외" 서술은 부정확(베뉴 s1·옵션 ot·사전신청 관리 rsvpPkg·참관객 genManage 포함).
- 한글 금액: Excel 네이티브는 NUMBERSTRING 연동(원 스펙)이나 검증 파이프라인(LibreOffice) 미지원 → 기본은 정적 한글 + TEXT 동적 숫자 하이브리드, `use_numberstring=True`로 원 스펙 출력 가능.

### v3.0.0 — 2026-08-18 (리멤버 전환 — D1)

**소속 전환에 따른 양식 체계 재편** (변경명세서 v1.0 §2.1, D1 확정). 기본 양식과 명칭 체계가 바뀌는 major 변경.

#### 변경 (breaking)
- **기본 양식 전환**: 리멤버 견적서를 1차(기본) 양식으로 승격. 체이닝 `format` 기본값 `mnc` → `remember` (chaining-schema.md §4·§7). description·본문의 양식 서열을 리멤버 우선으로 재기술.
- **양식 리네임 보존**: 기존 전 직장 양식을 **"산출내역서(공공·국가계약법형)"** 으로 일반화 리네임(v3.3.0에서 제거) — 공공·관 발주 대응 시 재사용 가치가 있어 삭제하지 않고 보존. 사용자 대면 명칭에서 회사 상호를 제거.
  - `mnc_template.xlsx`의 법인 직인 이미지 → 중립 **외부 주입 슬롯**(공급자 직인/로고) placeholder로 치환. xlsx 셀 내 회사 상호 텍스트 0건(기존부터 외부 주입 구조).
  - 파일명 패턴 `[구 양식]_{고객명}_{행사명}_견적서.xlsx` → `[{공급자}]_{고객명}_{행사명}_산출내역서.xlsx` (일반 패턴).
  - **코드 식별자는 하위호환 위해 유지**: `format` 값 `mnc`, 함수 `export_mnc_estimate()`, 파일 `mnc_template.xlsx`는 그대로 두고 리네임 사실을 주석/문서로 명기(참조 무결성 보존).
- **리멤버 양식 실무 반영** (D1-③):
  - PCO 이윤 계산을 **PCO 기획료 = 직접비(섹션2~5 합)의 25% 별도 계상** 방식으로 명문화(remember_template.md §5).
  - "질문이 필요 없는 견적서" 규칙 명문화 — 평이한 한국어 항목명 사용(2026-08-03 확정 preference).

#### 범위 외 (백로그 유지)
- calcEstimate 자동 산출 엔진의 리멤버 양식 연결은 본 전환 범위 외 — Sprint 1.6 백로그 유지. 자동 산출(방식 A)은 계속 산출내역서(공공형) 엔진만 사용.

### v2.2.1 — 2026-07-03

CP1 GO-1 후속 조치 — ChainPayload 출력 봉투에 필수 필드 `generatedAt` 추가(chaining-schema.md §4·§7), 참조 링크 무결성 2건 정정(venue-db-realdata.md §6 파일명, venue-db.md §5 외부 문서 링크 평문화).

### v2.2.0 — 2026-07-03

**Fable 5 재설계 패스 + Sprint 8 반영.**

#### 신규 추가
- Step 6.5 **완료 게이트** — 증거주의 7항(엔진 자가검증·3중 금액 일치·재오픈 무결성·입력 전수성·식별정보·가격 산식 연동·앵커 객체 보존). 통과 전 전달 금지.
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
- ⭐ **자동 산출 엔진** `calc_estimate.py` — SSOT §5 calcEstimate Python 포팅 (CLI 자가검증 포함, SSOT §9 11/11 PASS)
- ⭐ **xlsx 본문 자동 작성** `export_estimate.py` — 7섹션 자동 펼침 + 무결성 검증
- **방식 A (자동 산출)** 워크플로우 — `calc_estimate({target, options})` 한 번 호출로 견적서 완성
- **Step 2.5 체이닝 입력 감지** — mice-proposal(현 jc-pptx 별칭) / mice-rfp-analyzer 의 ChainPayload JSON 자동 처리
- **Step 3.5 공급자·고객사 슬롯 명세** — 구 양식 13 슬롯 + 리멤버 6 슬롯 (외부 주입 변수; v3.3.0부터 리멤버 6 슬롯만)
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
  - `mnc_template.md` — 공급자 기본값 → 13 슬롯 명세표
  - `references/remember_template.md` — 공급자 기본값 → 6 슬롯 명세표
  - `mnc_template.xlsx` 셀 — `(외부 주입 - ...)` placeholder 교체
  - `assets/remember_template.xlsx` 셀 — placeholder 교체

#### 유지 (변경 없음)
- `scripts/korean_amount.py` — 한글 금액 변환 (v1 그대로)
- 양식 시각 디자인 (색상·병합·로고) — 모두 보존

#### 검증
- ✅ SSOT §9 0원 일치 11/11 (pk = 83,750,000원, pkVat = 92,125,000원)
- ✅ Summit 2026 hand-trace 10/10 (target=120, pk = 89,810,000원)
- ✅ 9개 엣지 케이스 (target=40~501) PASS
- ✅ 트리거 충돌 0건 / 회사 종속 표현 0건
- ✅ jc-design-system 일관성 점수 100/100

### v1.0 — (이전)

- 두 양식(구 양식 / 리멤버) 템플릿 복사 + 수동 항목 입력 방식
- `scripts/korean_amount.py` 한글 금액 변환
- 공급자 정보 하드코딩
- 자동 산출·체이닝·jc-design-system 매핑 없음
