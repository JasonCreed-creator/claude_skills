---
name: mice-dashboard
version: "v2.0.0"
license: Complete terms in LICENSE.txt
description: "분석 보고서용 인터랙티브 대시보드를 생성하는 스킬. Excel/CSV 파일, 대화 입력, 또는 다른 MICE 스킬(mice-meeting-minutes 시리즈·mice-estimate 예산실적)의 체이닝 JSON 입력을 받아 KPI 카드·차트·인포그래픽이 포함된 단일 HTML 대시보드 + PDF 보고서를 자동 생성한다. v2부터 jc-design-system 시맨틱 토큰 매핑, 라이트/다크 모드 5종 변형, 인포그래픽 3종(퍼널·매트릭스·레이더)을 지원한다. 반드시 이 스킬을 사용해야 하는 상황: '대시보드', 'dashboard', 'KPI 대시보드', '분석 대시보드', '실적 대시보드', '데이터 시각화 보고서', '인터랙티브 보고서', '성과 분석 리포트'를 언급할 때. 데이터를 업로드하며 '시각화해줘', '차트로 만들어줘', '대시보드로 보여줘'라고 요청할 때. 행사 실적·매출·KPI·참가자 통계를 대시보드로 정리해달라는 요청. MICE 행사 결과보고서를 대시보드로 만들어달라는 요청. 다크 모드 토글·클라이언트 오버레이는 외부 주입 변수로 처리 — 스킬 내 어떤 회사·개인 식별 정보도 하드코딩하지 않는다."
dependencies:
  - pandas
  - openpyxl
  - playwright
---

# 분석 대시보드 생성 스킬

## 버전 히스토리

### v2.0 — 2026-05-25

**핵심 변화**: jc-design-system 시맨틱 매핑 + 라이트/다크 5종 변형 + 인포그래픽 3종 + 체이닝 명시 + 외부 변수화.

#### 신규 추가
- ⭐ **다크 모드 5종 변형**: KPI 카드·차트·테이블·콜아웃·헤더 (라이트/다크 토글 + localStorage)
- ⭐ **인포그래픽 3종**: 퍼널 (전환 분석)·매트릭스 (4분면 분류)·레이더 (다축 평가) — HTML/CSS 기반
- **jc-design-system 시맨틱 토큰 매핑**: 4종 자체 팔레트 → JC 토큰 + 클라이언트 오버레이 (mc·remember·darktrace·confex)
- **체이닝 JSON 스키마**: mice-meeting-minutes 시리즈·mice-estimate 예산실적 입력 + dashboard 출력 정의
- 신규 references 4종:
  - `dark-mode-patterns.md` — 5 컴포넌트 다크 변형 + 토글 스크립트 + 인쇄 호환 + 접근성
  - `infographic-patterns.md` — 3종 HTML/CSS 패턴 + 자동 감지 헬퍼
  - `jc-design-mapping.md` — 자체 팔레트 → JC 토큰 매핑표 + 차트 시리즈 6 슬롯
  - `chaining-schema.md` — 입출력 JSON 3종 + 트리거 자동 라우팅
- 신규 assets 2종:
  - `dashboard-template-light.html` — 라이트 모드 기본 템플릿
  - `dashboard-template-dark.html` — 다크 모드 기본 템플릿

#### 변경
- **frontmatter**: `name + description` → `name + version + description + dependencies`
- description 확장 (체이닝·다크 모드·인포그래픽·외부 변수화 명시)
- 4종 디자인 톤 → **JC 시맨틱 토큰 + 라이트/다크 모드 조합으로 재현** (v1 호환 유지)
- 차트 컬러 시퀀스를 `COLOR_CHART_SERIES_1~6` 토큰화

#### 유지 (변경 없음)
- `chart-guide.md` — 6 차트 유형 가이드 (v1 그대로)
- `kpi-patterns.md` — KPI 자동 감지 패턴 (v1 그대로)
- 자동 KPI 감지 + 차트 자동 선택 로직
- HTML + Playwright PDF 생성 흐름
- 반응형 브레이크포인트
- 엣지 케이스 처리

#### 검증
- ✅ jc-design 일관성 (시맨틱 토큰 매핑 1:1)
- ✅ 다크 모드 5종 변형 + 접근성 WCAG 2.1 AA 대비비
- ✅ 인포그래픽 3종 HTML 렌더링 (라이트/다크 양쪽)
- ✅ 체이닝 JSON 스키마 3종 정의
- ✅ 회사 종속 표현 0건

### v1.0 — (이전)

- 자동 KPI 감지 + 차트 자동 선택 (4종 디자인 톤)
- HTML + PDF (Playwright)
- 반응형 + 엣지 케이스 처리
- jc-design·다크 모드 체계화·인포그래픽·체이닝 없음

---

## 개요

데이터를 분석하여 한국어 인터랙티브 HTML 대시보드 + PDF 보고서를 자동 생성하는 스킬. MICE 행사 실적/KPI 분석에 최적화되어 있으나 범용 데이터 분석에도 사용. v2부터 다른 MICE 스킬과의 체이닝 입력 + 다크 모드 + 인포그래픽 3종 지원.

**자산 정의 원칙**: 본 스킬은 어떤 회사·개인의 식별 정보도 하드코딩하지 않는다. 프로젝트명·고객사·발행자 등은 모두 **외부 주입 변수**로 처리. (정본: `jc-design-system/references/shared-rules.md#RULE-NO-COMPANY`)

## 워크플로우

### Step 1: 입력 데이터 확인 (3가지 경로, v2 신규 1·2 추가)

| 경로 | 트리거 | 처리 |
|---|---|---|
| **A. ChainPayload JSON (v2 신규)** | 입력에 `$schema: "ChainPayload/v1"` 포함 | source 별 자동 라우팅 (chaining-schema.md §6) |
| **B. 파일 입력 (v1)** | `/mnt/user-data/uploads/` 의 .xlsx/.csv | pandas/openpyxl 로드 |
| **C. 대화 입력 (v1)** | 채팅으로 데이터 직접 전달 | 텍스트 → 구조화 데이터 변환 |

### Step 1.5: 체이닝 입력 감지 (v2 신규)

```python
from chaining_helper import detect_input_source

source = detect_input_source(input_payload)
# 가능 값: 'mice-meeting-minutes' (시리즈) / 'mice-estimate' (예산실적) / 'file_upload' / 'inline_data'
```

ChainPayload 스키마 상세는 [chaining-schema.md](references/chaining-schema.md) 참조.

### Step 2: 데이터 분석 및 KPI 자동 감지

`references/kpi-patterns.md` 를 읽고, 컬럼명·값 패턴 분석하여 KPI 유형 자동 판별. (v1 로직 그대로)

**판별 순서**: 컬럼명 키워드 → 데이터 타입 → 값 범위 → 시계열 여부

**자동 KPI 카드**: 주요 지표 3~6개 자동 선별, 비교 기준 있으면 증감률 자동.

### Step 3: 차트 유형 자동 선택

`references/chart-guide.md` 를 읽고 적합 차트 자동 선택. (v1 로직 그대로)

| 데이터 패턴 | 차트 |
|---|---|
| 시계열 + 연속값 | 라인 |
| 카테고리 + 수치 | 바 (수직/수평) |
| 비율/구성 | 도넛 |
| 비교 (2~4 항목) | 그룹드 바 |
| 분포 | 히스토그램/박스 |
| 목표 vs 실적 | 게이지/프로그레스 |
| 다차원 비교 | 레이더 |

### Step 3.5: 인포그래픽 자동 감지 (v2 신규)

`references/infographic-patterns.md` §5 의 `INFOGRAPHIC_TRIGGERS` 사전 기반:

| 인포그래픽 | 트리거 키워드 |
|---|---|
| 퍼널 (Funnel) | 전환, 단계, 퍼널, funnel, 이탈, 드롭 |
| 매트릭스 (Matrix) | 매트릭스, 4분면, 분류, 우선순위, 평가표 |
| 레이더 (Radar 인포그래픽) | 다축, 평가, 역량, 항목별 점수, 레이더 |

→ 데이터 컬럼·제목에서 트리거 키워드 감지 시 표준 차트 영역 다음에 자동 배치.

### Step 4: 디자인 톤 + 모드 자동 선택 (v2 강화)

#### v1 호환 — 4종 톤 자동 결정 (chart-guide.md §디자인 톤)

| 데이터 키워드 | 톤 | JC 토큰 매핑 |
|---|---|---|
| 보고·결과·실적·report | 기업/공식 (다크) | `COLOR_BG_PAGE_DARK` + `COLOR_BRAND_PRIMARY` (mc) |
| 매출·비용·예산·수익 | 재무/회계 (라이트) | `COLOR_BG_PAGE` + `COLOR_BRAND_PRIMARY_FINANCE` |
| 이벤트·페스티벌·캠페인 | 마케팅 (컬러풀) | `COLOR_BG_PAGE` + `COLOR_BRAND_PRIMARY` (confex) |
| 기본 | 성과/실적 (라이트) | `COLOR_BG_PAGE` + `COLOR_BRAND_PRIMARY_BIZ` |

#### v2 신규 — 라이트/다크 모드 명시

사용자가 `theme=dark` 명시 시 → 자동으로 `data-theme="dark"` 적용. localStorage 에 저장하여 재방문 시 유지.

#### v2 신규 — 클라이언트 오버레이 슬롯

| 슬롯 | 설명 |
|---|---|
| `overlay` | `mc` / `remember` / `darktrace` / `confex` / null (외부 주입) |

→ Sprint 7 통합 시 jc-design-system 의 토큰 fetch + hex 자동 적용.

### Step 5: HTML 대시보드 생성

`assets/dashboard-template-light.html` 또는 `assets/dashboard-template-dark.html` 을 베이스로 사용. 데이터·KPI·차트·인포그래픽을 주입.

#### 기술 스택 (v1과 동일)

- **차트**: Chart.js 4.x (CDN)
- **폰트**: Pretendard (CDN)
- **레이아웃**: CSS Grid + Flexbox
- **반응형**: 미디어 쿼리 (1200px / 768px 브레이크포인트)

#### HTML 구조 (v2 강화)

```
┌──────────────────────────────────────────────┐
│ 헤더: 제목 + 생성일시 + 데이터 출처 + 🌙토글  │  ← v2: 다크 모드 토글 추가
├──────────────────────────────────────────────┤
│ KPI 카드 영역 (3~6개)                         │  ← v2: 다크 변형 5종 적용
├──────────────────────────────────────────────┤
│ 메인 차트 영역 (2~6개)                        │  ← v2: 차트 시리즈 6 슬롯 토큰
├──────────────────────────────────────────────┤
│ 인포그래픽 영역 (퍼널·매트릭스·레이더, v2)    │  ← v2 신규
├──────────────────────────────────────────────┤
│ 데이터 테이블                                 │  ← v2: 다크 변형
├──────────────────────────────────────────────┤
│ 푸터: 생성 도구 + 면책 + 외부 주입 발행자     │
└──────────────────────────────────────────────┘
```

#### 코딩 규칙 (v1 유지 + v2 추가)

1. **단일 HTML 파일**: CSS·JS 모두 인라인. 외부 의존성은 CDN만.
2. **한국어 고정**: 모든 레이블·제목·툴팁·범례 한국어.
3. **숫자 포맷**: 한국식 — 천 단위 콤마, 원화(₩), 퍼센트(%) (`chart-guide.md` `formatKR()`)
4. **Chart.js 기본**: `responsive: true`, `maintainAspectRatio: false`, 한국어 툴팁, 범례 하단
5. **KPI 카드 증감**: ▲(긍정)/▼(부정), 색상 시맨틱 토큰 (`COLOR_SEMANTIC_SUCCESS/DANGER`)
6. **테이블**: 정렬·호버·스트라이프, 다크 변형 자동 적용
7. **인쇄 최적화**: `@media print` 다크→라이트 강제 (PDF 호환)
8. **접근성**: `aria-label`, WCAG AA 대비비, 키보드 토글
9. **(v2 신규) 다크 토글**: 헤더 우측 버튼 + localStorage 저장 + Chart.js 글로벌 색상 갱신
10. **(v2 신규) 외부 주입 슬롯**: `projectTitle` / `client` / `publisher` / `publishDate` 등은 hardcoding 금지

### Step 6: PDF 보고서 생성

v1 그대로 — Playwright 우선, wkhtmltopdf 폴백, 브라우저 인쇄 최후.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{html_path}")
    page.wait_for_timeout(2000)
    page.pdf(path=pdf_path, format="A4", landscape=True, print_background=True)
    browser.close()
```

⚠️ 다크 모드 활성 상태에서도 인쇄는 라이트 강제 (CSS `@media print`).

### Step 7: 파일 출력 + ChainPayload (v2 신규)

1. HTML → `/mnt/user-data/outputs/{주제}_대시보드_{YYYYMMDD}.html`
2. PDF → `/mnt/user-data/outputs/{주제}_대시보드_{YYYYMMDD}.pdf`
3. `present_files` 도구로 사용자에게 두 파일 전달
4. **ChainPayload JSON 생성** (chaining-schema.md §3·4): 차기 행사 기획·외부 시스템 전달용 — 선택적 산출

---

## 엣지 케이스 처리 (v1과 동일)

| 상황 | 대응 |
|---|---|
| 데이터 너무 적음 (3행 미만) | KPI + 단순 테이블만 |
| 숫자 컬럼 없음 | 카테고리 빈도수 + 워드클라우드 |
| 컬럼명 영문 | 한국어 자동 매핑 시도 |
| 결측치 다수 | 결측 비율 KPI 카드에 경고 |
| 시트 여러 개 | 사용자에게 선택 요청 |
| 1만 행 초과 | 1000행 샘플링 + 전체 통계 별도 |

---

## 품질 체크리스트

대시보드 생성 후:
- [ ] 모든 차트 정상 렌더링 (빈 차트 0)
- [ ] 숫자 포맷 한국식 적용
- [ ] KPI 카드 수치 원본과 일치
- [ ] 반응형 레이아웃 정상
- [ ] 한국어 깨짐 없음
- [ ] 인쇄 시 레이아웃 유지
- **[v2 추가] 다크 모드 토글 정상 동작**
- **[v2 추가] 인포그래픽 (감지된 경우) 정상 렌더링**
- **[v2 추가] 외부 주입 슬롯 모두 채움 (또는 placeholder)**

---

## 코드 작성 원칙

1. **단일 HTML 파일**: 외부 의존 CDN만
2. **한국어 표시**: 모든 사용자 직면 텍스트
3. **시맨틱 토큰 우선**: hex 직접 사용 시 토큰명 주석 필수 (`/* COLOR_BRAND_PRIMARY (mc) */`)
4. **다크 모드 기본 지원**: 5 컴포넌트 변형 모두 적용
5. **인포그래픽 자동 감지**: 데이터 키워드 기반 (`INFOGRAPHIC_TRIGGERS`)
6. **체이닝 입력 우선**: ChainPayload 감지 시 자동 진행 (별도 정보 수집 없음)
7. **외부 주입 변수 엄수**: 회사·개인 식별 정보 0건 (CLAUDE.md §10)

---

## References

- [chart-guide.md](references/chart-guide.md) — 6 차트 유형 + 컬러 팔레트 + Chart.js 글로벌 설정 (v1 유지)
- [kpi-patterns.md](references/kpi-patterns.md) — KPI 자동 감지 패턴 5 카테고리 (v1 유지)
- [jc-design-mapping.md](references/jc-design-mapping.md) — 시맨틱 토큰 매핑 + 차트 시리즈 6 슬롯 (v2 신규)
- [dark-mode-patterns.md](references/dark-mode-patterns.md) — 5 컴포넌트 다크 변형 + 토글 (v2 신규)
- [infographic-patterns.md](references/infographic-patterns.md) — 퍼널·매트릭스·레이더 3종 (v2 신규)
- [chaining-schema.md](references/chaining-schema.md) — 입출력 JSON 3종 (v2 신규)

## Assets

- [dashboard-template-light.html](assets/dashboard-template-light.html) — 라이트 모드 베이스 (v2 신규)
- [dashboard-template-dark.html](assets/dashboard-template-dark.html) — 다크 모드 베이스 (v2 신규)
