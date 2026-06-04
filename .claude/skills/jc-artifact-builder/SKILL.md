---
name: jc-artifact-builder
description: jc-design-system 시그니처 테마가 기본 적용된 claude.ai 인터랙티브 아티팩트(React + TypeScript + Tailwind + shadcn/ui) 빌더. 상태관리·라우팅·다중 컴포넌트가 필요한 복합 아티팩트를 단일 HTML로 번들한다. 폰트(Pretendard)·컬러(accent #2962FF·navy #0A2540)·라이트/다크·차트 시리즈·인포그래픽 스케일이 jc-design-system 정본에서 자동 매핑된다. 다음 상황에서 반드시 이 스킬을 사용할 것 사용자가 '아티팩트', 'artifact', 'React 아티팩트', '인터랙티브 앱', '웹앱', 'claude.ai 아티팩트', 'shadcn', '컴포넌트 앱', '상태관리 UI', '라우팅 있는 화면', '인터랙티브 대시보드 앱'을 언급할 때. MICE 데이터(견적·회의록·실적)를 입력하며 '클릭 가능한 앱으로', '필터 되는 대시보드로', '탭/모달 있는 화면으로 만들어줘'를 요청할 때. 단, 단순 단일 HTML/JSX 한 장은 본 스킬을 쓰지 말 것(과함). 정적 결과보고 KPI 대시보드 1장은 mice-dashboard, 회의록 대시보드는 mice-meeting-minutes, 발주처 제안서(PPTX)는 mice-proposal, 스폰서 데크(HTML)는 mice-sponsor-deck 영역. 본 스킬은 그 산출물의 ChainPayload/v1 JSON을 입력으로 받아 인터랙티브 React 아티팩트로 확장할 수 있다.
license: Complete terms in LICENSE.txt
---

# JC Artifact Builder

원본 web-artifacts-builder를 **jc-design-system(SoT) 환경에 맞춰 개조**한 버전이다.
스캐폴딩 시 jc 시그니처 테마(폰트·컬러·라이트/다크·차트·스케일)가 **자동 적용**되므로,
산출 아티팩트가 사용자님의 다른 MICE 산출물(대시보드·데크·제안서)과 동일한 룩앤필을 갖는다.

빌드 절차:
1. `scripts/init-artifact.sh <project-name>` 로 프로젝트 초기화 (jc 테마 자동 주입)
2. 생성된 코드를 편집해 아티팩트 개발
3. `scripts/bundle-artifact.sh` 로 단일 HTML(`bundle.html`)로 번들
4. 사용자에게 아티팩트 표시
5. (선택) 아티팩트 테스트

**Stack**: React 18 + TypeScript + Vite + Parcel(번들) + Tailwind CSS + shadcn/ui + **jc-design-system 테마**

## Design & Style Guidelines (jc-design-system)

**VERY IMPORTANT — "AI slop" 회피 + jc 시그니처 준수:**
- ❌ 금지: 과도한 중앙정렬, 보라색 그라데이션, 균일한 둥근 모서리 남발, **Inter 폰트**.
- ✅ jc 시그니처: **Pretendard**(한국어 우선, 자동 주입) · 액센트 **Electric Blue `#2962FF`** · 헤더/표지 **Deep Navy `#0A2540`**(`navy` 또는 `bg-card`+텍스트) · 절제된 그림자 · 라디우스 스케일(sm4/md8/lg12) · 비대칭 그리드/충분한 여백.
- **다크 모드**: `<html class="dark">` 또는 `next-themes`. 토큰이 `#0A1220` 계열로 자동 전환된다.
- **차트**: `bg-chart-1`~`bg-chart-6` 또는 `hsl(var(--chart-N))` (라이트/다크 자동 보정). 6시리즈까지.
- **연속/히트맵/매트릭스**: 인포그래픽 스케일 `bg-scaleBlue-1..5`, `scaleGreen/Red/Amber`.
- 토큰·사용법 전체는 [`references/jc-theme.md`](references/jc-theme.md) 참조.

### 공통 룰 (shared-rules 정본)
- **RULE-WCAG**: 본문 대비 4.5:1 이상 (jc 토큰은 라이트/다크 모두 AAA 충족). 정본: `jc-design-system/references/shared-rules.md#RULE-WCAG`.
- **RULE-PRINT-LIGHT**: 다크 아티팩트도 인쇄 시 라이트 강제(`@media print`). 정본: `shared-rules.md#RULE-PRINT-LIGHT`.
- **RULE-NO-COMPANY**: 회사·개인 식별정보(엠앤씨/M&C/실명/이메일) 하드코딩 금지 — 모두 props/외부 주입 변수로. 정본: `shared-rules.md#RULE-NO-COMPANY`.

## Quick Start

### Step 1: Initialize Project
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```
생성물: React+TS(Vite), Tailwind 3.4.1 + shadcn 테마, `@/` 별칭, 40+ shadcn 컴포넌트, Radix 의존성, Parcel 번들 설정, **jc-design-system 테마(`tailwind.config.js`·`src/index.css`)와 Pretendard 폰트 링크가 사전 주입됨**.

### Step 2: Develop Your Artifact
생성된 파일을 편집한다. jc 토큰은 일반 Tailwind 클래스처럼 쓴다:
`bg-primary`(Electric Blue)·`text-foreground`·`bg-card`·`bg-muted`·`text-muted-foreground`·`bg-chart-1`·`bg-scaleGreen-2`·`font-mono`.

### Step 3: Bundle to Single HTML File
```bash
bash scripts/bundle-artifact.sh
```
모든 JS/CSS/의존성을 인라인한 자가완결 `bundle.html` 생성(루트에 `index.html` 필요). claude.ai 아티팩트로 바로 공유 가능.

### Step 4: Share Artifact with User
번들된 HTML을 대화에서 아티팩트로 공유한다.

### Step 5: Testing/Visualizing (Optional)
필요/요청 시에만. Playwright/Puppeteer 등으로 사후 확인(선제 테스트는 지연만 늘리므로 지양).

## MICE 체이닝 (입력 연동)
mice-estimate·mice-meeting-minutes·mice-dashboard 등이 내보낸 `ChainPayload/v1` JSON을
아티팩트의 데이터 소스로 받아 인터랙티브(필터·탭·드릴다운)로 확장할 수 있다.
봉투 구조·source 판별은 `jc-design-system/references/chaining-protocol.md` 참조,
데이터→컴포넌트 매핑 패턴은 [`references/jc-theme.md`](references/jc-theme.md) §체이닝 참조.

## Reference
- jc 토큰 매핑·사용법: `references/jc-theme.md`
- 디자인 토큰 정본: `jc-design-system/references/signature-tokens.md` · `mode-mapping.md`
- shadcn/ui 컴포넌트: https://ui.shadcn.com/docs/components
