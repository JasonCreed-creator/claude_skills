---
name: mice-rfp-analyzer
version: "v2.1.0"
description: "RFP·비딩 공고·입찰 안내서·제안요청서를 7축(요건·평가·리스크·경쟁·일정·예산·전략권고)으로 해체해 GO/HOLD/NO-GO 판정과 근거를 담은 .docx 분석 보고서와 .xlsx 평가 매트릭스를 리멤버 웜 페이퍼 룩으로 함께 만드는 스킬. 다음 상황에서 반드시 이 스킬을 사용할 것 — 사용자가 'RFP 분석', 'RFP 해체', 'RFP 요약', '비딩 분석', '비딩 검토', '입찰 분석', '공고 분석', '요건 분석', '평가 기준 분석', '배점 분석', '수주 가능성', '응찰 여부', 'GO/NO-GO 판단', '독소 조항 찾아줘', '평가 기준 뽑아줘'를 말할 때, RFP 파일(PDF/DOCX/HWP/HWPX)을 올리며 '분석해줘', '핵심 정리해줘'를 요청할 때, 발주처 요구사항을 매트릭스로 정리해 달라고 할 때. 산출 데이터는 ChainPayload/v1로 jc-pptx(제안서)·mice-estimate(견적)에 그대로 넘어간다. 형제 경계 — 제안서·비딩 PPT 작성은 jc-pptx, 견적서는 mice-estimate, 발표 대본은 pt-script, 자사 신사업·포지셔닝 전략 프레임워크는 jc-strategy-canvas, 외부 시장·경쟁 데이터 수집은 mice-market-intel, 완성 산출물 적대 검증은 jc-redteam."
---

# mice-rfp-analyzer

MICE 행사 RFP·비딩 공고를 18년 경력 전략가의 시각으로 해체해, **응찰 의사결정을 실제로 바꿀 수 있는** 분석 보고서(.docx)와 평가 매트릭스(.xlsx)를 생성한다.

## 1. 목표와 경계

**목표**: 기획자가 이 산출물만 읽고 ①응찰 여부를 결정하고 ②응찰 시 무엇으로 이길지 알 수 있게 하는 것. 정보의 나열이 아니라 **판정과 그 근거**가 산출물의 가치다.

**경계**: 제안서·비딩 PPT → jc-pptx / 견적 → mice-estimate / 발표 대본 → pt-script(jc-pptx 덱 경유) / 자사 전략 프레임워크 → jc-strategy-canvas / 외부 시장·경쟁 리서치 → mice-market-intel / 산출물 적대 검증 → jc-redteam. GO 판정 시 체이닝으로 넘긴다(§7).

**진행 방식**: 분석·초안·파일 생성은 되돌릴 수 있는 작업이므로 묻지 않고 바로 진행하고, 고른 기본값(Full/Quick 모드, 자사 역량 가정 등)을 한 줄로 밝힌다. 판정을 좌우하는 정보가 원문에 없으면 멈추지 말고 HOLD + "발주처 질의 필요"로 처리한다. 외부 발송(발주처 질의 메일 등)만 사용자 승인 후.

## 2. 분석의 질 기준 (모든 판단에 우선 적용)

1. **원문 근거주의**: 모든 요건·배점·일정·금액은 RFP 원문 조항(페이지·항 번호)을 인용한다. 원문에 없는 것은 쓰지 않는다 — 추정이 필요한 영역(경쟁사·승률·발주처 의도)은 "추정"을 명시하고 추정의 근거를 한 줄 단다.
2. **의사결정 우선순위**: 판정을 바꿀 수 있는 정보(실격 요건, 치명 독소 조항, 원가-발주가 역전, 물리적 일정 불가)를 먼저 찾고 가장 앞에 배치한다. 사소한 발견을 아무리 쌓아도 치명 항목 하나를 놓치면 분석은 실패다.
3. **모호성은 자산**: RFP가 불명확한 지점은 약점이 아니라 **발주처 질의 기회**다. 해석이 갈리는 조항은 임의 해석하지 말고 보고서의 "발주처 질의 필요" 섹션에 모아 질의문 초안까지 제시한다.

## 3. 7축 분석 프레임

| 축 | 핵심 질문 | 판단 기준 (시니어 휴리스틱) |
|----|----------|--------------------------|
| 1. 요건 | 무엇을 해야 하는가? | 요건을 **MANDATORY(실격성)/WEIGHTED(배점 연동)/NICE(가점·인상)** 렌즈로 분류하고, 각각에 자사 적합성 **STRONG/PARTIAL/GAP** 을 판정한다. 산출물 기입은 기존 스키마 열에 1:1 매핑한다 — 분류는 요건 시트의 `필수/선택/가산` 열(MANDATORY=필수, WEIGHTED=선택 중 배점 연동, NICE=가산), 적합성은 `우리 측 대응` 열(STRONG=가능, PARTIAL=조건부, GAP=불가). MANDATORY×GAP(=필수×불가) 1건 = NO-GO 후보. |
| 2. 평가 | 어떻게 점수가 매겨지는가? | 배점표를 전수 옮기고 합계를 원문과 대조. 정성 배점(기획력 등)의 실질 변별력과 가격 점수 산식의 역전 가능성을 해석한다. |
| 3. 리스크 | 어디에 함정이 있는가? | `references/risk-patterns.md` 독소 조항 매칭 + 심각도 판정: **치명**(수용 시 손실·법적 위험, 협상 불가 시 NO-GO 사유) / **중대**(마진·운영 압박, 가격에 반영) / **경미**(인지만). 패턴에 없는 신종 조항도 "발주처에 유리하게 기울어진 비대칭"이 보이면 잡는다. |
| 4. 경쟁 | 누가 응찰할 것인가? | 발주처 최근 계약 이력·업계 구도 기반 추정. 자사 차별 포인트는 요건 태깅의 STRONG 항목에서 도출한다 — 근거 없는 "우리가 잘함" 금지. |
| 5. 일정 | 시간이 충분한가? | 제안 준비 기간과 행사 준비 기간을 분리 판정. 역산 일정표에서 물리적 불가능(예: 계약 후 행사까지 필수 리드타임 미달)이 나오면 치명 리스크로 승격. |
| 6. 예산 | 가격 전략은? | 발주가 대비 개산 원가(과업 범위 기준)로 마진 밴드를 추정. 원가>발주가면 치명. 가격 점수 산식이 있으면 최적 입찰가 구간을 계산한다. |
| 7. 전략 권고 | 응찰할 것인가? | §4 판정 규칙 적용. GO면 핵심 승부 메시지 3개 이내 + 승률 추정(근거 병기). |

→ 축별 상세 추출 가이드: `references/analysis-framework.md`

## 4. GO / HOLD / NO-GO 판정 규칙

- **NO-GO 강제 조건** (하나라도 해당 시, 다른 매력과 무관하게): ①MANDATORY 요건 중 충족 불가 항목 존재 ②치명 독소 조항 + 협상 여지 없음 ③합리적 원가가 발주가 초과 ④물리적 일정 불가.
- **HOLD**: 판정을 좌우할 정보가 원문에 없고 질의로 해소 가능할 때. 반드시 "무엇이 확인되면 GO인지"를 조건문으로 명시한다.
- **GO**: 강제 조건 무저촉 + 승부 메시지가 실재할 때. 승률은 배점 구조×자사 STRONG 항목의 커버리지로 근거를 대고, 낙관 편향을 경계한다(불리 요인도 반드시 병기).
- 판정이 경계선이면 판정을 억지로 내리지 말고 HOLD + 결정 조건 제시가 정직한 산출이다.

## 5. 산출물

도구: `scripts/parse_rfp.py`(텍스트 추출) → 분석 → `scripts/build_report.py`(.docx) + `scripts/build_matrix.py`(.xlsx). 도구가 실패하면 원인을 보고하고 대체 경로(수동 추출 등)를 시도한다.

- **분석 보고서** `rfp-analysis-report_[발주처]_[행사명]_[YYYYMMDD].docx` — 8~15p, 구조는 `references/report-structure.md`. 첫 페이지에 판정·핵심 근거 3줄·치명 항목을 배치(임원이 1페이지만 읽어도 되게). "발주처 질의 필요" 섹션 포함.
- **평가 매트릭스** `rfp-evaluation-matrix_[발주처]_[행사명]_[YYYYMMDD].xlsx` — 7시트, 스키마는 `references/evaluation-matrix-spec.md` **그대로 준수**(스키마 변경 금지). §3 태깅 렌즈는 기존 열로 표현한다: 분류→`필수/선택/가산`, 적합성→`우리 측 대응`(가능/조건부/불가). 전용 태그 열 신설은 차기 스펙 개정 백로그(BL 등재)로 하고, 그 전까지 본 매핑이 정본이다.
- 디자인: jc-design-system v2 리멤버 웜 페이퍼(§6). 발행 명의는 리멤버 MICE비즈팀 기본, 발주처명은 입력 데이터(`client`)로만 주입(`RULE-NO-COMPANY`). 출력 폴더 기본 `outputs/`.

**Quick 모드(--quick)**: 사용자가 마감 임박·"핵심만"을 표명하면 핵심 3축(요건·리스크·전략)+판정만 .docx 4~6p로 압축. 생략한 축을 문서에 명시한다.

## 6. jc-design-system 연동 (토큰 런타임 로드)

색 값은 스크립트·문서에 미러하지 않는다. `scripts/rfp_tokens.py`가 하우스 규약 §2 순서(형제 `parents[2]/jc-design-system` → `~/.claude/skills/jc-design-system` → `~/.claude/skills/synced/*/jc-design-system`)로 SoT를 찾아 `jc_tokens.load_tokens`로 `signature-tokens.md §6 JSON`을 읽는다. 로드 실패 시에만 출처 주석이 달린 폴백 상수를 쓴다. 빌드 로그 첫 줄 `토큰 출처:`로 어느 쪽인지 확인한다.

| 적용 영역 | 토큰 역할 |
|----------|----------|
| 제목·본문 | `text`(잉크) · 보조 `textSecondary` · 메타 `textMuted` |
| 표 헤더 · 짝수 행 | `surfaceAlt` 면 + 잉크 Semibold · `bg` |
| 강조 박스 · 타이틀 룰 | `accentSoft` 면 + `accent` 4pt 좌측 룰 · 작은 강조 텍스트는 `accentStrong` |
| GO / GO 조건부 / HOLD / NO-GO | `success`+흰 글자 / `successBg`+`success` / `warning`+잉크(앰버 단독 텍스트 금지) / `danger`+흰 글자 |
| 리스크·압박 상/중/하 | `dangerBg`+`danger` / `warningBg`+잉크 / `successBg`+`success` |
| 로고 슬롯 | 표지(.docx)·0_종합 시트(.xlsx)에 `jc-design-system/assets/remember-black.png`. 없으면 발행 명의 텍스트 |

- 서체 Pretendard(미설치 폴백 Malgun Gothic). 공통 룰: `RULE-WCAG`·`RULE-NO-COMPANY` — 정본 `jc-design-system/references/shared-rules.md`.
- 구 네이비·네온 시그니처는 사용자가 "jc 시그니처"를 명시 요청할 때만 `legacy-jc` 오버레이(`client-overlays.md §3.3`)로 적용한다.

## 7. 체이닝 (GO 시)

분석 결과를 `references/chaining-guide.md`의 **ChainPayload/v1** 봉투(`$schema`·`source`·`version`·`generatedAt`·`target`·`clientId`·`projectTitle` + 평탄 페이로드 `rfp_meta`·`requirements`·`evaluation_focus`·`differentiation_points`·`proposal_structure_hint`)로 내보낸다. 봉투 정본은 `jc-design-system/references/chaining-protocol.md`.

- → `jc-pptx`(제안서): 요건 태깅·배점 가중치·승부 메시지·분량 힌트. `risk_notes_for_negotiation`은 본문 노출 금지.
- → `mice-estimate`(견적): 발주가·추정 원가·입찰가 권고·리스크 프리미엄.
- → `pt-script`: 직접 입력이 아니다. jc-pptx 덱이 확정된 뒤 그 덱을 받아 대본을 쓴다.
- ← `jc-strategy-canvas`: 자사 전략 캔버스 페이로드가 있으면 7축 중 경쟁·전략권고 축의 사전 입력으로 흡수.
- ← `mice-market-intel`: 발주처·경쟁사 리서치 페이로드가 있으면 4축(경쟁) 근거로 흡수(기준일 병기).

§3 태깅은 `requirements.mandatory/optional/bonus`·`our_capability` 필드와 의미가 1:1이므로 손실 없이 전달된다.

## 8. 완료 게이트 (증거주의 — 통과 전 완료 보고 금지)

산출물 제출 직전 자가 검증한다. 하나라도 미통과면 수정 후 재검증하고, 확인 불가능한 항목은 산출물에 "미확인"으로 표기한다:

1. **배점 전수성**: 매트릭스의 배점 합계 = RFP 원문 배점 합계 (숫자 재대조).
2. **실격 전수성**: 원문 grep 재확인 — "실격", "무효", "제외", "필수" 조항이 전부 요건 시트의 `필수` 분류(=MANDATORY)로 매핑됐는가.
3. **근거 링크**: 치명·중대 판정 전 항목에 원문 조항 인용이 붙어 있는가.
4. **숫자 정합**: 보고서와 매트릭스의 금액·일자·배점이 서로 일치하는가.
5. **판정 일관성**: §4 강제 조건 해당 항목이 있는데 GO로 판정하지 않았는가.
6. **룩·명의**: 빌드 로그 `토큰 출처`가 `sot:`인가(폴백이면 보고에 명시), 산출물에 구 소속사 명칭·개인 연락처 0건.

통과 후 판정이 GO이거나 대외 공유 예정이면 `jc-redteam`(Quick Strike: 판정 1장 / Deep Audit: 보고서 전체)으로 넘긴다.

## 9. 파일 구조

```
mice-rfp-analyzer/
├── SKILL.md
├── references/   analysis-framework.md · evaluation-matrix-spec.md · report-structure.md · risk-patterns.md · chaining-guide.md
└── scripts/      parse_rfp.py · build_report.py · build_matrix.py · rfp_tokens.py(토큰 어댑터)
```

자가 테스트: `python scripts/parse_rfp.py --self-test` · `python scripts/build_report.py --self-test` · `python scripts/build_matrix.py --self-test` (python-docx·openpyxl 필요).

## 10. 버전 히스토리

| 버전 | 일자 | 주요 변경 |
|------|------|---------|
| v1.0.0 | 2026 초기 | 7축 프레임·산출물 2종·체이닝 초안 |
| v1.0.1 | 2026-05-27 | 검증 사이클·UTF-8 stdout·회사 종속 표현 일반화 |
| v2.0.0 | 2026-07-03 | **지시문 재설계 (Fable 5 패스)**: 판정 규칙(GO/HOLD/NO-GO 강제 조건) 명문화, 요건 태깅(MANDATORY/WEIGHTED/NICE)×적합성(STRONG/PARTIAL/GAP) 도입, 독소 조항 심각도 3등급, 증거주의 완료 게이트 신설, 모호성→발주처 질의 프로토콜, 호출표·고정 파이프라인 등 과잉처방 제거 |
| v2.0.1 | 2026-07-03 | 용어 통일: SKILL.md §5 "빠른 분석 모드" → "Quick 모드(--quick)" (analysis-framework.md §8과 일치) |

## 변경 이력

- v2.1.0 (2026-10-05): 보고서·매트릭스의 구 네이비·네온 하드코딩 → jc-design-system 웜 페이퍼 토큰 런타임 로드(`rfp_tokens.py`) + 로고 슬롯·리멤버 발행 명의, 3개 스크립트 `--self-test`. 체이닝을 ChainPayload/v1 봉투로 정합하고 폐합 스킬 라우팅을 jc-pptx·mice-estimate·pt-script·jc-strategy-canvas로 교체. 실행 전 브리프 게이트 문구 삭제, 출력 경로 `outputs/`.
