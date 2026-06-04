---
name: jc-design-system
description: 개인 MICE 전략가용 디자인 토큰 시스템. 다른 스킬이 산출물 생성 시 참조하는 reference 자산이다. 컬러·타이포·사이즈·간격·컴포넌트 패턴을 통합 정의하며 클라이언트별 오버레이를 토글로 지원한다. 다음 상황에서 반드시 이 스킬을 사용할 것 사용자가 '디자인 토큰', '디자인 시스템', '스타일 가이드', '비주얼 시스템', 'JC 디자인', '개인 디자인 토큰'을 언급할 때. 또한 mice-proposal / mice-estimate / pt-script / mice-dashboard 등 다른 스킬이 산출물 디자인 일관성을 위해 자동 호출할 때. 컬러 팔레트 정의·수정·확장, 클라이언트별 컬러 오버레이 적용, 라이트/다크 모드 매핑 조회, KPI 카드·차트 컨테이너·섹션 구분 등 컴포넌트 패턴 적용 시에도 사용한다.
version: "v1.2.0"
---

# JC Design System

MICE 전략가의 개인 디자인 토큰 시스템이다. 회사 종속이 아닌 개인 자산으로, Track A(행사 기획 전략 역할) / Track B(독립 전략가 퍼스널 브랜드) 양쪽에서 활용된다.

## 핵심 원칙

1. **시그니처는 고정 자산** — 컬러 베이스·텍스트·타이포·사이즈·간격은 개인 정체성으로 변경 금지
2. **클라이언트는 오버레이로만 차별화** — primary / accent / logo 3개 토큰만 외부 주입 변수로 처리
3. **회사 종속 표현 배제** — "MICE 전문가" 일반 용어 사용
4. **Single Source of Truth** — 모든 산출물 디자인은 이 스킬을 통해 일관성 유지

## 사용 시점

### 직접 호출
- 디자인 토큰 조회·수정·확장 요청
- 신규 클라이언트 오버레이 추가 요청
- 컴포넌트 패턴 확장 요청

### 자동 호출 (다른 스킬에서)
- `mice-proposal` 제안서 생성 시 → 색상·타이포·표지 적용
- `mice-estimate` 견적서 생성 시 → 헤더 컬러·강조 톤 적용
- `pt-script` 발표 대본 생성 시 → 문서 헤더·강조 스타일 적용
- `mice-dashboard` 대시보드 생성 시 → KPI 카드·차트 시리즈 적용

## 호출 흐름

```
1. references/signature-tokens.md 로드 (개인 고정 자산)
       ↓
2. references/client-overlays.md 에서 클라이언트 오버레이 적용
       (client_id 미지정 시 시그니처 그대로 사용)
       ↓
3. references/mode-mapping.md 로 라이트/다크 결정
       (산출물 유형별 기본값 따름)
       ↓
4. references/component-patterns.md 로 컴포넌트 적용
       ↓
5. 산출물 생성 (다른 스킬이 결과물 빌드)
```

## 파일 구조

```
jc-design-system/
├── SKILL.md                        # 본 파일 — 진입점
└── references/
    ├── signature-tokens.md         # 시그니처 고정 토큰 (변경 금지)
    ├── client-overlays.md          # 클라이언트 주입 스키마 + 샘플
    ├── mode-mapping.md             # 라이트/다크 모드 매핑
    ├── component-patterns.md       # KPI 카드·차트·섹션·테이블 패턴
    └── usage-guide.md              # 다른 스킬에서 호출하는 방법
```

## 빠른 참조

| 항목 | 값 / 위치 |
|------|----------|
| Primary (Deep Navy) | `#0A2540` |
| Accent (Electric Blue) | `#2962FF` |
| Point Pool | Orange `#FF5722` / Magenta `#E91E63` / Neon `#00E676` / Blue `#2962FF` |
| 한글 폰트 | Pretendard |
| 영문 폰트 | Inter |
| 숫자·데이터 폰트 | JetBrains Mono |
| 사이즈 스케일 | 1.250 (Major Third) |
| 간격 base | 4px |

전체 토큰은 `references/signature-tokens.md` 참조.

## 다른 스킬에서 호출하는 방법

다른 스킬(mice-proposal 등) 작업 중 디자인 적용이 필요하면:

```
1. references/signature-tokens.md 를 읽어 토큰 값을 추출한다
2. 클라이언트가 지정된 경우 references/client-overlays.md 에서 오버레이를 적용한다
3. 산출물 유형(PPTX/DOCX/HTML)에 맞춰 references/component-patterns.md 패턴을 적용한다
```

상세 가이드는 `references/usage-guide.md` 참조.

## 변경 정책

- 시그니처 토큰 변경: 본 스킬을 직접 수정하는 빌드 챗에서만 가능
- 클라이언트 오버레이 추가: `client-overlays.md` 의 샘플 형식 따라 추가
- 컴포넌트 패턴 확장: 기존 패턴과 충돌하지 않는 범위에서 추가

## 변경 이력

### v1.1.0 (2026-05-27) — Sprint 7 보강

Sprint 1~6 누적 백로그 8건 반영 + CLAUDE.md §10 위반 정정.

| 백로그 ID | 항목 | 반영 위치 |
|----------|------|----------|
| BL-S2-3 | Chart.js 글로벌 색상 CSS 변수 직접 참조 | `references/usage-guide.md` §8 |
| BL-S3-디자인-1 | SVP-6 퍼널 단계 `#5B9BD5` 토큰화 | `references/signature-tokens.md` §1.7 `--jc-accent-light` |
| BL-S3-디자인-2 | SVP-7 매트릭스 Q4 `#FFF3E0` 토큰화 | `references/signature-tokens.md` §1.7 `--jc-point-orange-softest` |
| BL-S3-디자인-3 | 다크 모드 Tier 가이드 표 | `references/mode-mapping.md` §7 |
| BL-S4-디자인-1 | Q&A 답변 레이블 WCAG AA 강한 녹색 | `references/signature-tokens.md` §1.7 `--jc-success-strong` |
| BL-S5-디자인-1 | 다크 priority-p3 콘트라스트 강화 | `references/mode-mapping.md` §8 |
| BL-S5-디자인-2 | WCAG AA 대비비 계산 표준화 (WebAIM) | `references/mode-mapping.md` §9 |
| BL-S6-디자인-1 | POINT vs STATUS 시리즈 선택 가이드 | `references/component-patterns.md` §9 |

**신규 자산**:
- 토큰 4종 (`--jc-accent-light`, `--jc-point-orange-softest`, `--jc-point-magenta-soft`, `--jc-success-strong`)
- usage-guide §7 실제 사용 사례 7개 (Sprint 1~6 결과 기반)
- WCAG AA 계산 표준 (sRGB 공식 + WebAIM Contrast Checker)

**§10 위반 정정**:
- description 본인명 트리거 제거 + 외부 주입 변수 5종 표준화 (`{{client_company}}`, `{{author_name}}`, `{{personal_brand}}`, `{{author_title}}`, `{{company_name}}`)

### v1.0.0 (2026-04 초안)

기본 자산 — 시그니처 토큰 + 클라이언트 오버레이 + 모드 매핑 + 컴포넌트 패턴 + 사용 가이드 5종 references.
