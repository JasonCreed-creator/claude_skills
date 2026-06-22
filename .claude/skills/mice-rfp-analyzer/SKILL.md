---
name: mice-rfp-analyzer
version: "v1.0.1"
license: Complete terms in LICENSE.txt
description: RFP, 비딩 공고, 입찰 안내서, 제안요청서를 7축 프레임(요건·평가·리스크·경쟁·일정·예산·전략권고)으로 분석하여 .docx 분석 보고서와 .xlsx 평가 매트릭스를 동시 생성하는 스킬. 다음 상황에서 반드시 이 스킬을 사용할 것 사용자가 'RFP 분석', 'RFP 해체', 'RFP 요약', '비딩 분석', '비딩 검토', '입찰 분석', '공고 분석', '요건 분석', '평가 기준 분석', '수주 가능성 분석', '제안 전략 도출', 'GO/NO-GO 판단'을 언급할 때. RFP 파일(PDF/DOCX/HWP/HWPX)을 업로드하며 '분석해줘', '핵심 정리해줘', '평가 기준 뽑아줘', '독소 조항 찾아줘'를 요청할 때. 발주처 요구사항을 매트릭스로 정리해달라고 요청할 때. 응찰 여부 판단을 요청할 때. 본 스킬의 산출물은 mice-proposal 스킬의 입력으로 그대로 체이닝 가능. 단, '제안서 작성', '비딩 자료 만들기', 'PT 자료'는 mice-proposal 영역이므로 사용하지 말 것. '견적서'는 mice-estimate, '대본/스크립트'는 pt-script, '대시보드'는 mice-dashboard 영역.
---

# mice-rfp-analyzer

MICE 행사 RFP·비딩 공고·입찰 안내서를 18년 경력 전략가 시각의 **7축 프레임**으로 분석하여 의사결정용 산출물 2종을 생성하는 스킬.

## 1. 본 스킬이 다루는 것 / 다루지 않는 것

### 다루는 것 (DO)
- RFP·비딩 공고·입찰 안내서·제안요청서·과업지시서의 **분석·해체·요약**
- 평가 기준 매트릭스화, 독소 조항 식별, 경쟁 환경 추정, 예산 적정성 검토
- GO/NO-GO 응찰 판단 권고
- 분석 결과를 mice-proposal 입력으로 전달하는 체이닝

### 다루지 않는 것 (DON'T)
- 제안서 본문 작성 (→ mice-proposal)
- 견적서 작성 (→ mice-estimate)
- 발표 대본 작성 (→ pt-script)
- 대시보드 시각화 (→ mice-dashboard)

## 2. 호출 시점 판단 가이드

| 사용자 입력 | 본 스킬 호출 | 사용 스킬 |
|------------|-------------|----------|
| "이 RFP 분석해줘" + 파일 | ✅ | mice-rfp-analyzer |
| "비딩 검토해줘" + 파일 | ✅ | mice-rfp-analyzer |
| "응찰할지 판단해줘" | ✅ | mice-rfp-analyzer |
| "독소 조항 있나 봐줘" | ✅ | mice-rfp-analyzer |
| "이 RFP로 제안서 만들어줘" | ❌ | mice-proposal |
| "비딩 PT 자료 만들어줘" | ❌ | mice-proposal |
| "견적 뽑아줘" | ❌ | mice-estimate |

## 3. 표준 워크플로우

```
[RFP 파일 입력]
    ↓
[scripts/parse_rfp.py] 텍스트 추출 (PDF/DOCX/HWP/HWPX)
    ↓
[references/analysis-framework.md] 7축 분석 수행
    ↓
[references/risk-patterns.md] 독소 조항 매칭
    ↓
[scripts/build_report.py] .docx 분석 보고서 생성
[scripts/build_matrix.py] .xlsx 평가 매트릭스 생성
    ↓
[GO인 경우] references/chaining-guide.md → mice-proposal 입력 패키지 생성
```

## 4. 7축 분석 프레임 (요약)

| 축 | 핵심 질문 | 산출 데이터 |
|----|----------|------------|
| 1. 요건 | 무엇을 해야 하는가? | 필수/선택/권장 + 실격 항목 |
| 2. 평가 | 어떻게 점수가 매겨지는가? | 평가 기준 + 배점 + 가중치 |
| 3. 리스크 | 어디에 함정이 있는가? | 독소 조항 + 책임 범위 |
| 4. 경쟁 | 누가 응찰할 것인가? | 예상 경쟁사 + 차별 포인트 |
| 5. 일정 | 시간이 충분한가? | 마감·발표·계약·행사일 + 압박 강도 |
| 6. 예산 | 가격 전략은? | 발주가 + 원가 추정 + 입찰가 권고 |
| 7. 전략 권고 | 응찰할 것인가? | GO/NO-GO + 핵심 메시지 + 승률 |

→ 상세 정의는 `references/analysis-framework.md` 참조.

## 5. 산출물 사양

### 5-1. 분석 보고서 (.docx)
- 파일명: `rfp-analysis-report_[발주처]_[행사명]_[YYYYMMDD].docx`
- 분량: 8~15페이지 (RFP 분량에 비례)
- 구조: `references/report-structure.md` 정의
- 디자인: jc-design-system / personal 베이스 적용

### 5-2. 평가 매트릭스 (.xlsx)
- 파일명: `rfp-evaluation-matrix_[발주처]_[행사명]_[YYYYMMDD].xlsx`
- 시트: 7개 (요건·평가·리스크·경쟁·일정·예산·종합)
- 구조: `references/evaluation-matrix-spec.md` 정의
- 디자인: jc-design-system / personal 베이스 적용

## 6. 빠른 분석 모드 (--quick)

마감이 24시간 이내로 임박한 경우 핵심 3축(요건·평가·전략)만 빠르게 산출하는 모드.

**호출 트리거**: 사용자가 "급해", "빨리", "마감 임박", "핵심만"이라고 언급할 때.

**산출물**: 분석 보고서(.docx) 1종만, 4~6페이지로 압축.

## 7. jc-design-system 연동

본 스킬은 jc-design-system의 signature 토큰을 참조한다.

| 적용 영역 | 호출 토큰 |
|----------|----------|
| 분석 보고서 표지·헤더 | `color.primary` (#0A2540 Deep Navy) |
| 강조 박스·차트 | `color.accent` (#2962FF Electric Blue) |
| GO 판정 | `color.point.neon` (#00E676) |
| HOLD 판정 | `color.point.orange` (#FF5722) |
| NO-GO 판정 | `color.point.magenta` (#E91E63) |
| 리스크 등급 (상/중/하) | Magenta / Orange / Neon |

→ 클라이언트 오버레이 미적용 (작업자 베이스 유지).

## 8. 체이닝 (mice-proposal로 전달)

GO 판정 시, 분석 결과를 mice-proposal의 입력 형태로 변환하는 매핑 규칙 적용.

→ 상세 매핑은 `references/chaining-guide.md` 참조.

## 9. 파일 구조

```
mice-rfp-analyzer/
├── SKILL.md                              # 본 파일
├── references/
│   ├── analysis-framework.md             # 7축 추출 가이드
│   ├── evaluation-matrix-spec.md         # .xlsx 스키마
│   ├── report-structure.md               # .docx 구조
│   ├── risk-patterns.md                  # 독소 조항 라이브러리
│   └── chaining-guide.md                 # mice-proposal 매핑
└── scripts/
    ├── parse_rfp.py                      # PDF/DOCX/HWP 추출
    ├── build_report.py                   # .docx 생성
    └── build_matrix.py                   # .xlsx 생성
```

## 10. 운영 원칙

- 추측 금지. RFP 원문에 명시된 내용만 분석 데이터로 사용.
- 추정이 필요한 영역(경쟁사·승률 등)은 명시적으로 "추정"임을 표기.
- 보고서 본문에 발주처 명을 명시하되, 작업자 베이스 디자인 유지.
- 산출물 파일명에 발주처·행사명·날짜 포함하여 버전 관리 용이성 확보.

## 11. 버전 히스토리

| 버전 | 일자 | 주요 변경 |
|------|------|---------|
| v1.0.0 | 2026 초기 | 7축 분석 프레임·.docx 보고서·.xlsx 매트릭스·체이닝 가이드 초안 |
| v1.0.1 | 2026-05-27 | 검증 사이클 수행 (가상 RFP 시나리오 1건 분석 완료) · UTF-8 stdout 패턴 추가 (3 스크립트) · 회사 종속 표현 일반화 (references/scripts 9건) · frontmatter version 필드 추가 |
