# jc-theme — jc-design-system 토큰 ↔ 아티팩트 매핑

`init-artifact.sh`가 주입하는 테마의 토큰 매핑·사용법·MICE 체이닝 가이드.
**값 정본은 항상 `jc-design-system/references/signature-tokens.md`(§6 JSON)와 `mode-mapping.md`(§3·§3.2)** 다. 본 문서는 그 값을 shadcn/Tailwind에 어떻게 연결했는지만 설명한다.

## 1. 시맨틱 토큰 매핑 (shadcn CSS 변수 = jc 토큰)

| Tailwind 클래스 | CSS 변수 | 라이트(jc) | 다크(jc) | 용도 |
|----------------|----------|-----------|----------|------|
| `bg-background` `text-foreground` | `--background`/`--foreground` | `#F8F9FB`/`#1A1D24` | `#0A1220`/`#E8ECF2` | 페이지 |
| `bg-card` | `--card` | `#FFFFFF` | `#152134` | 카드·패널 |
| `bg-primary` `text-primary-foreground` | `--primary` | `#2962FF` | `#5B8DEF` | **CTA·버튼·강조** |
| `bg-secondary` | `--secondary` | `#F1F3F7` | `#1F2C42` | 보조 면 |
| `bg-muted` `text-muted-foreground` | `--muted`/`--muted-foreground` | `#F1F3F7`/`#5A6270` | `#1F2C42`/`#A0A8B4` | 약한 배경·캡션 |
| `bg-accent` `text-accent-foreground` | `--accent` | `#E8EFFF`/`#1E4DCC` | `#1F2C42`/`#E8ECF2` | 호버·하이라이트 |
| `bg-destructive` | `--destructive` | `#D32F2F` | `#F44336` | 위험·삭제 |
| `border-border` | `--border` | `#E5E8ED` | `#2A3650` | 보더 |
| `ring-ring` | `--ring` | `#2962FF` | `#5B8DEF` | 포커스 링 |

> shadcn `primary`는 **액센트(Electric Blue)** 에 매핑돼 버튼/CTA가 jc 시그니처를 따른다. **헤더·표지의 Deep Navy**는 별도 유틸 `bg-navy`(`#0A2540`) 또는 `text-navy` 사용.

## 2. jc 확장 유틸 (init 주입)

- **헤더/표지 네이비**: `bg-navy` `text-navy` = `#0A2540`
- **시맨틱**: `text-success`(#00C853) `text-warning`(#FFA000) `text-info`(#2962FF) — 단, 위험은 `destructive`
- **차트 시리즈(라이트/다크 자동)**: `bg-chart-1`…`bg-chart-6`, 또는 CSS `hsl(var(--chart-N))`
  - 라이트: `#2962FF #E91E63 #FF5722 #00E676 #0A2540 #7C3AED`
  - 다크: `#5B8DEF #F04D85 #FF7649 #33EE92 #C9CFD8 #A78BFA`
- **인포그래픽 스케일(히트맵·매트릭스·퍼널, 5단계 deep→bg)**:
  `bg-scaleBlue-1..5` · `bg-scaleGreen-1..5` · `bg-scaleRed-1..5` · `bg-scaleAmber-1..5`

## 3. 다크 모드

`darkMode: ["class"]`. 토글:
```tsx
// 단순 토글
document.documentElement.classList.toggle("dark");
// 또는 next-themes(설치됨): <ThemeProvider attribute="class"> + useTheme()
```
모든 토큰이 `mode-mapping §3` 다크값으로 자동 전환된다. 별도 다크 색 하드코딩 금지.

## 4. 차트 (recharts/chart.js 등)

CSS 변수를 그대로 색으로 넘긴다(라이트/다크 자동):
```tsx
const SERIES = Array.from({length:6},(_,i)=>`hsl(var(--chart-${i+1}))`);
// recharts: <Bar fill="hsl(var(--chart-1))" /> · <Line stroke="hsl(var(--chart-2))" />
```
6개 초과 카테고리는 스케일(scaleBlue 등)로 단계 표현하거나 그룹화한다.

## 5. 공통 룰 (정본: jc-design-system/references/shared-rules.md)

- **WCAG**: jc 토큰 조합은 라이트/다크 본문 4.5:1↑(대부분 AAA). 임의 색 추가 시 `mode-mapping §9`로 재검증. → `#RULE-WCAG`
- **인쇄 라이트 강제**: 다크 아티팩트는 인쇄 시 라이트로. → `#RULE-PRINT-LIGHT`
  ```css
  @media print { :root { color-scheme: light; } .dark { /* 라이트 토큰 강제 */ } }
  ```
- **회사 종속 금지**: 회사명·실명·이메일·로고 URL을 코드에 하드코딩하지 말고 props/설정 객체로 주입. → `#RULE-NO-COMPANY`

## 6. MICE 체이닝 (ChainPayload/v1 입력)

mice-* 스킬 산출 JSON을 아티팩트 데이터로 소비한다(봉투 구조는 `chaining-protocol.md`).
```tsx
// payload.json = { "$schema":"ChainPayload/v1", "source":"mice-estimate", "data": {...} }
import payload from "./payload.json";
// source별 분기 → 컴포넌트 매핑
const view = {
  "mice-estimate":        EstimateExplorer,   // 견적 항목 필터·합계 드릴다운
  "mice-meeting-minutes": ActionKanban,       // Action Items 칸반·시리즈 추적
  "mice-dashboard":       KpiBoard,           // KPI·차트 인터랙티브
}[payload.source] ?? RawView;
```
- 입력 데이터는 그대로 두고, 색/폰트만 jc 테마로 렌더 → 다른 산출물과 일관.
- `jc-redteam`으로 최종 산출 아티팩트의 카피/수치/대비를 점검할 수 있다.

## 7. 빠른 체크리스트
- [ ] Inter 미사용(Pretendard 적용) · 보라 그라데이션·과도 중앙정렬 없음
- [ ] 액센트=Electric Blue, 헤더=Deep Navy, 다크 토글 동작
- [ ] 차트는 `--chart-N`/스케일 사용(임의 hex 금지)
- [ ] 회사·개인정보 하드코딩 0건(props 주입)
- [ ] 본문 대비 4.5:1↑, 인쇄 라이트 강제
