# 리서치 리포트 산출 스펙

`mice-market-intel` SKILL Phase 4의 정본. 종합·검증(Phase 3) 통과 후 **출처를 단 리서치 리포트**를 낸다. 기본 Markdown, 시각본은 jc 스타일 HTML.

## 0. SoT 토큰 (값 미러링 금지)

- 색·타이포·간격: `jc-design-system/references/signature-tokens.md §6 JSON`(구현체 `jc_tokens.py`). 다크/인쇄 `mode-mapping.md`.
- 식별용: primary `#0A2540`·accent `#2962FF`·폰트 Pretendard/Inter/JetBrains Mono(수치). 정본은 SoT.
- `RULE-WCAG`·`RULE-PRINT-LIGHT` 준수. FORBIDDEN 비-canon 색값 금지(`check_drift.py`). 본 스킬은 CONSUMERS 등록.
- 차트가 필요하면 `mice-dashboard/references/chart-guide.md`·인포그래픽 패턴 차용(재발명 금지).

## 1. 리포트 구조

```
1. 조사 개요      목적·결정용도·범위·조사일·아웃라인 요약
2. 핵심 발견(TL;DR)  3~5개 불릿, 각 출처·티어
3. 항목별 발견    아웃라인 항목 순서로. 표/수치 + 출처 각주 + 신뢰도 표식
4. 교차·모순      출처 간 상충 → 범위·차이·티어 우선 판단
5. 공백·한계      [미확인]/[단일출처]/[접근불가] 목록 + 후속 조사 경로
6. 시사점(선택)   "그래서 무엇" — 단, 전략 판단은 jc-strategy-canvas로 위임 명시
7. 출처 목록      전체 인용 출처 (발행처·일자·URL·티어)
```

- **사실과 해석 분리**: 3=사실(출처 필수), 6=해석(가설로 명시). 둘을 섞지 않는다.
- **신뢰도 가시화**: 표 셀에 티어 배지(`[T1]`~`[T4]`), `[단일출처]`/`[미확인]`은 눈에 띄게(중립 회색·점선).
- 핵심 수치는 JetBrains Mono. 출처 없는 숫자 0건(없으면 `[미확인]`).

## 2. 중립성·윤리

- **공개 정보만** 인용. 비공개·미검증 내부정보·추측성 평판 배제.
- 경쟁사·발주처·스폰서 후보는 **사실 + 출처**로만 기술. 폄훼·근거 없는 단정 금지.
- 자사·개인 식별은 변수 슬롯(`RULE-NO-COMPANY`). 조사 대상 기업 공개명은 사실로서 기재 가능.

## 3. 산출 방식

- 본령은 *조사·종합*이므로 리포트는 워크플로우 산물로 **인라인 생성**(Markdown 우선, 요청 시 jc HTML).
- 복합 인터랙티브(필터·정렬되는 경쟁사 표)는 `jc-artifact-builder`, 차트 KPI 시각화는 `mice-dashboard`로 위임.
- 파일명: `market-intel_[topic]_[YYYYMMDD].md` / `.html` (자사·실명 미포함).
- 동시 산출 `ChainPayload`(`chaining-schema.md`)로 다운스트림 자동 연결.
