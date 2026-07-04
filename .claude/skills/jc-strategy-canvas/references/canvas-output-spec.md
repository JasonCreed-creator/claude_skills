# 전략 캔버스 HTML 산출 스펙

`jc-strategy-canvas` SKILL §5·⑥의 산출물 정본. 검증(⑤) 통과 후 **단일 파일 HTML 전략 캔버스**를 생성한다. 모든 색·타이포·간격은 **jc-design-system SoT 런타임 참조** — 값 하드코딩 금지.

## 0. SoT 토큰 로딩 (값 미러링 금지)

- 색·타이포·사이즈·간격: `jc-design-system/references/signature-tokens.md §6 JSON` (구현체 `jc-design-system/scripts/jc_tokens.py`의 `load_tokens`/`color`).
- 라이트/다크·인쇄: `jc-design-system/references/mode-mapping.md` (§3 매핑, §4.2 인쇄 라이트 강제, §9 WCAG 계산).
- 클라이언트 차별화: `client-overlays.md` (primary/accent/logo 3토큰만, 충돌 회피 §6) — 페이로드 `clientId`가 있을 때만.
- 형제 경로 탐색: `Path(__file__).resolve().parents[2] / "jc-design-system"`.
- **FORBIDDEN 값 금지**: `jc-design-system/references/signature-tokens.md`에 정의되지 않은 비-canon 색값(예: 임의 navy/blue 변형)을 본문/스타일에 쓰지 않는다 — 산출 전 signature-tokens.md 대조로 수동 확인한다.

핵심 값(식별용 — 정본은 위 SoT):
- primary `#0A2540` (Deep Navy) · accent `#2962FF` (Electric Blue) · 데이터 시리즈는 `signature-tokens.md §1.4`.
- 폰트: Pretendard(한) / Inter(영) / JetBrains Mono(숫자·KPI).

## 1. 레이아웃 골격

```
┌────────────────────────────────────────────┐
│ 헤더: 전략 질문 · 결정 · 일자 · clientId 로고  │  ← navy 바, accent 액센트
├────────────────────────────────────────────┤
│ 1줄 핵심 결론 (전략 권고) — 가장 크게         │
├────────────────────────────────────────────┤
│ [프레임워크 블록들 — 채운 것만, 순서대로]      │
│   F1 BMC(9그리드) / F2 5Forces(방사형/막대)   │
│   F3 SWOT(2×2) / F4 JTBD(카드) ...            │
├────────────────────────────────────────────┤
│ 교차 종합: 모순·시너지 · 전략 옵션 2~3 표      │
├────────────────────────────────────────────┤
│ jc-redteam 검증 배지 + 잔여 가설·추정 목록     │
└────────────────────────────────────────────┘
```

- **채운 프레임워크만** 렌더(②에서 고른 것). 빈 프레임워크 자리표시 금지.
- 근거 표식 시각화: `[검증]`=accent 점, `[가설]`=중립 회색, `[추정]`=점선 테두리. 한눈에 "어디가 단단하고 어디가 무른지" 보이게.

## 2. 프레임워크별 렌더 패턴

| 프레임워크 | 권장 시각형 | 비고 |
|-----------|------------|------|
| F1 BMC | 9칸 그리드(전통 BMC 배치: 좌 KP/KA/KR, 중 VP, 우 CR/CH/CS, 하단 C$/R$) | 3면 시장이면 CS·VP 색 구분 |
| F2 Five Forces | 중앙 사각 + 5방향 화살표, 힘 세기=막대/채도 | 가장 센 힘 강조 |
| F3 SWOT/TOWS | 2×2 매트릭스 + TOWS 전략 문장 캡션 | SO 사분면 accent 강조 |
| F4 JTBD | 고객별 카드(기능/감정/pain/gain/대안) | 3면이면 3카드 |
| F5 Positioning | 5스텝 세로 흐름 또는 포지셔닝 2×2 맵 | 타깃 세그먼트 강조 |
| F6 TAM/SAM/SOM | 동심원 또는 3단 깔때기 + 숫자(JetBrains Mono) | 출처 각주 필수 |

- 차트가 필요하면 `mice-dashboard/references/chart-guide.md`의 토큰 매핑·시리즈 컬러 규약을 따른다(재발명 금지).
- 인포그래픽(퍼널·매트릭스·레이더)은 `jc-design-system` 인포그래픽 스케일 + `mice-dashboard/references/infographic-patterns.md` 패턴 차용.

## 3. 모드 / 인쇄 / 접근성

- 기본 라이트. 다크 토글 제공 시 `mode-mapping.md §3` DARK_* 매핑.
- **`RULE-PRINT-LIGHT`**: 다크로 보더라도 인쇄(@media print)는 라이트 강제 — 전략 캔버스는 출력·배포되는 의사결정 문서다.
- **`RULE-WCAG`**: 본문 대비 4.5:1↑ (`mode-mapping.md §9` 계산).
- 단일 파일·오프라인 동작(폰트는 CDN 또는 시스템 폴백). 로컬 저장·PDF 인쇄 가능.

## 4. 산출 방식

- 본 스킬의 본령은 *사고 구조화*이므로, 캔버스 HTML은 워크플로우 산물로 **인라인 생성**(별도 무거운 빌더 스크립트 없이 SKILL이 직접 작성)한다.
- 복합 인터랙티브(필터·드릴다운·상태)가 필요하면 `jc-artifact-builder`로 위임, 단순 테마/오버레이 재적용은 `jc-theme-factory`로 위임.
- 파일명: `strategy-canvas_[project_or_topic]_[YYYYMMDD].html` (회사·실명 미포함 — `RULE-NO-COMPANY`).
