# 결과보고서 레이아웃 스펙 (HTML/md)

사후 결과보고서 산출물의 레이아웃·디자인 규약. 값의 정본은 항상 **jc-design-system SoT**(`signature-tokens.md §6 JSON`). 본 문서는 *배치·구성*만 정의한다.

---

## 1. 산출 형식

| 형식 | 용도 | 비고 |
|------|------|------|
| **HTML(단일 파일)** | 발주처 송부·화면 공유·PDF 인쇄 | 기본. CSS 변수로 SoT 토큰, 자가완결 |
| **Markdown** | 내부 위키·빠른 공유·추가 가공 | 경량. 표 중심 |

기본은 HTML. 사용자가 "간단히/md로"면 Markdown.

---

## 2. HTML 레이아웃 (8축 1:1 매핑)

```
┌ 헤더 (primary 배경) ─ 행사명 · 일자 · "사후 결과보고서" · 버전/생성일 ┐
├ 1. Executive Summary  (강조 박스 + 핵심 KPI 3 카드)
├ 2. 행사 개요          (정보 표)
├ 3. 목표 대비 성과     (KPI 표: 목표/실적/달성률/판정 + 달성률 배지)
├ 4. 예산 대비 실적     (섹션별 표: 계획/실집행/증감/사유)
├ 5. 운영 하이라이트    (불릿 + 캡션)
├ 6. 이슈 & 교훈        (상황→영향→원인→개선 카드)
├ 7. 이해관계자 피드백  (정량 + 정성 인용, n수)
└ 8. 차기 권고 / Next   (권고 + 우선순위 3)
```

- 차트가 필요하면 **mice-dashboard 산출을 인용/임베드**(재발명 금지). 본 보고서는 표·서사 중심.
- 케이스 카드(`case-builder.md`)는 부록 또는 별지로 첨부 가능.

---

## 3. SoT 토큰 매핑 (CSS 변수)

HTML은 CSS 변수로 SoT 참조. **hex 하드코딩 금지** — 빌드 시 `signature-tokens.md §6 JSON`에서 주입.

| 역할 | 토큰 | 식별용 값 |
|------|------|----------|
| 헤더·타이틀 | `--jc-primary` | `#0A2540` |
| 강조·링크·달성 배지 | `--jc-accent` | `#2962FF` |
| 달성(✅) | `--jc-success-strong` | (SoT §1.7) |
| 미달(⚠️) | `--jc-point-orange` | `#FF5722` |
| 본문 | `--jc-text` + Pretendard | `#1A1D24` |
| 수치(KPI·금액) | JetBrains Mono | — |

- 다크/인쇄 매핑·WCAG는 `jc-design-system/references/mode-mapping.md`.
- 클라이언트 오버레이(`clientId`) 있으면 primary/accent 교체(`client-overlays.md`). 발주처 송부 시 발주처 오버레이 적용 가능.

---

## 4. 인쇄 (RULE-PRINT-LIGHT)

결과보고서는 인쇄·PDF 첨부 빈도가 높다. **인쇄 시 라이트 강제**(다크 화면 상태여도). 정본 `shared-rules.md#RULE-PRINT-LIGHT` + `mode-mapping.md §4.2`.

```css
@media print {
  :root, [data-theme="dark"] {
    --jc-bg:#FFFFFF !important; --jc-surface:#FFFFFF !important; --jc-text:#1A1D24 !important;
  }
}
```

---

## 5. KPI 표 작성 규칙 (3축)

```
| KPI | 목표 | 실적 | 달성률 | 판정 |
```
- 달성률 = 실적÷목표, % 표기. 100%↑ ✅, 미달 ⚠️(색=point-orange).
- 미달 행은 6축(교훈)으로 앵커 링크.
- 목표 미확보 KPI는 `[목표 미설정]`으로 표기하고 실적만 — 단 "성과"로 주장하지 않는다.

---

## 6. 자가 점검 (마감)

- [ ] 8축 모두 존재(데이터 없으면 `[미확보]` 명시, 누락 아님)
- [ ] 모든 성과가 *목표 대비*로 표기
- [ ] 토큰 하드코딩 0(SoT CSS 변수), `check_drift.py` FORBIDDEN 0
- [ ] 회사·발주처 식별정보 외부 주입/익명화
- [ ] 인쇄 라이트 강제 CSS
- [ ] 차트는 dashboard 인용(재발명 0)
- [ ] (영업 재사용 케이스) 익명화·동의 확인
