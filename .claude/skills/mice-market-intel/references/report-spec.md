# 리서치 리포트 산출 스펙

`mice-market-intel` SKILL Phase 4의 정본. 종합·검증(Phase 3) 통과 후 **출처·기준일을 단 리서치 리포트**를 낸다. 기본 Claude Docs 문서(또는 Markdown), 시각본은 리멤버 웜 페이퍼 HTML.

## 0. SoT 토큰 (값 미러링 금지)

- 색·타이포·간격: `jc-design-system/references/signature-tokens.md §6 JSON`(구현체 `jc-design-system/scripts/jc_tokens.py`, 탐색 순서는 하우스 규약 §2: 형제 → `~/.claude/skills` → `~/.claude/skills/synced/*`). 다크/인쇄 `mode-mapping.md`.
- 룩(식별용 — 값은 SoT에서 읽는다): 웜 페이퍼 캔버스(`bg`)·잉크 본문(`text`)·리멤버 오렌지 액센트(`accent`, 작은 강조 텍스트 `accentStrong`)·서체 Pretendard 단일(수치 `tabular-nums`). 헤더 리멤버 로고 슬롯. 구 네이비 룩은 `legacy-jc` 오버레이 명시 요청 시만.
- `RULE-WCAG`·`RULE-PRINT-LIGHT` 준수. FORBIDDEN 비-canon 색값 금지 — `jc-design-system/references/shared-rules.md`·`signature-tokens.md` 정본 대조로 준수 확인.
- 차트·표·배지는 `jc-design-system/references/component-patterns.md` + `signature-tokens.md §1.6` 시리즈 순서(재발명 금지).

## 1. 리포트 구조

```
1. 조사 개요      목적·결정용도·범위·조사 기준일·아웃라인 요약
2. 핵심 발견(TL;DR)  3~5개 불릿, 각 출처·티어
3. 항목별 발견    아웃라인 항목 순서로. 표/수치 + 출처 각주 + 신뢰도 표식
4. 교차·모순      출처 간 상충 → 범위·차이·티어 우선 판단
5. 공백·한계      [미확인]/[단일출처]/[접근불가] 목록 + 후속 조사 경로
6. 시사점(선택)   "그래서 무엇" — 단, 전략 판단은 jc-strategy-canvas로 위임 명시
                 (경쟁 조사면 후보 수 whitespace_candidates까지만 — 우선순위·판단은 jc-strategy-canvas)
7. 출처 목록      전체 인용 출처 (발행처·일자·URL·티어)
```

- **사실과 해석 분리**: 3=사실(출처 필수), 6=해석(가설로 명시). 둘을 섞지 않는다.
- **신뢰도 가시화**: 표 셀에 티어 배지(`[T1]`~`[T4]`), `[단일출처]`/`[미확인]`은 눈에 띄게(중립 회색·점선).
- 핵심 수치는 Pretendard `tabular-nums` + 데이터 기준 연도 병기(예: `1.2조 원 (2025, [T1])`). 출처 없는 숫자 0건(없으면 `[미확인]`).

## 2. 중립성·윤리

- **공개 정보만** 인용. 비공개·미검증 내부정보·추측성 평판 배제.
- 경쟁사·발주처·스폰서 후보는 **사실 + 출처**로만 기술. 폄훼·근거 없는 단정 금지.
- 발행 명의 리멤버 MICE비즈팀 기본, 의뢰 고객사·작성자는 변수 슬롯(`RULE-NO-COMPANY`). 조사 대상 기업 공개명은 사실로서 기재 가능.

## 3. 산출 방식

- 본령은 *조사·종합*이므로 리포트는 워크플로우 산물로 **인라인 생성**(Claude Docs 기본, 요청 시 Markdown·HTML).
- 필터·정렬되는 경쟁사 표 같은 인터랙션이 필요하면 같은 단일 HTML 안에 바닐라 JS로 직접 구현한다.
- 파일명: `market-intel_[topic]_[YYYYMMDD].md` / `.html` (자사·실명 미포함).
- 동시 산출 `ChainPayload`(`chaining-schema.md`)로 다운스트림 자동 연결.
