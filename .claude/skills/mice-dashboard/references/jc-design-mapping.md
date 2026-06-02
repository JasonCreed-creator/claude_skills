# jc-design-system 매핑 (jc-design-mapping)

**대상 스킬**: jc-design-system v1 (별도 스킬)
**참조**: master-plan §2-1 (표준 강화 체크리스트 jc 연동)
**적용 범위 (Sprint 2)**: 정적 매핑 문서. 런타임 토큰 fetch는 Sprint 7 통합 검증 시.

mice-dashboard v1 은 4종 자체 컬러 팔레트(slate/blue 계열 등)를 직접 사용 → 디자인 일관성 깨짐. v2 는 각 팔레트를 **jc-design-system(SoT) 시그니처 토큰**으로 매핑하여 정합성을 확보한다.

> **정본 단일 출처(SoT)**: 모든 색상 값은 jc-design-system 정본을 미러한다. 라이트 베이스·차트 data-1..6·시맨틱 = `signature-tokens.md` §1·§1.4·§1.5·§6, 다크 패밀리·차트 다크 = `mode-mapping.md` §3·§3.2. 본 문서는 **토큰명 매핑만** 보유하고 hex 리터럴은 정본 파일을 참조한다. 클라이언트별 오버레이(mc·remember·confex 등) hex 는 본 문서에 하드코딩하지 않고 jc-design-system 의 `client-overlays.md` 가 단일 소유한다.

---

## 1. 매핑 원칙

1. **시맨틱 우선**: hex 대신 의미 토큰. 어떤 카드·차트도 토큰명으로 식별.
2. **클라이언트 오버레이**: 동일 시맨틱이라도 클라이언트(`mc`, `remember`, `darktrace`, `confex`)별로 다른 hex.
3. **모드 분리**: 라이트·다크는 동일 시맨틱 토큰의 모드 변형.

---

## 2. 4종 자체 팔레트 → JC(SoT) 토큰 매핑

> 모든 v1 자체 hex 는 폐기하고 아래 **SoT 정본 토큰**으로 흡수한다. hex 값은 `signature-tokens.md` §1·§1.5·§6(라이트·시맨틱) / `mode-mapping.md` §3(다크) 정본. 클라이언트 오버레이 hex 는 `client-overlays.md` 단일 소유 — 본 표에 직접 기입하지 않는다.

### 2.1 v1 "기업/공식" 톤 (다크) → JC 다크 모드

| 영역 | SoT 정본 토큰 (라이트) | SoT 정본 토큰 (다크) |
|---|---|---|
| 페이지 배경 | `--jc-bg` | 다크 페이지 배경 (mode-mapping §3) |
| 카드 배경 | `--jc-surface` | 다크 카드 서피스 (mode-mapping §3) |
| 액센트 | `--jc-accent` | 다크 액센트 (mode-mapping §3) |
| 강조/하이라이트 | `--jc-danger` | `--jc-danger` (시맨틱 단일값) |

### 2.2 v1 "성과/실적" 톤 (라이트) → JC 라이트 모드 기본

| 영역 | SoT 정본 토큰 |
|---|---|
| 페이지 배경 | `--jc-bg` |
| 카드 배경 | `--jc-surface` |
| 액센트 | `--jc-accent` |
| 긍정 | `--jc-success` |

### 2.3 v1 "마케팅/이벤트" 톤 → Point 풀 강조

| 영역 | SoT 정본 토큰 |
|---|---|
| 액센트 1 | `--jc-accent` (= `--jc-data-1`) |
| 액센트 2 | `--jc-point-orange` (= `--jc-data-3`) |
| 액센트 3 | `--jc-point-magenta` (= `--jc-data-2`) |

### 2.4 v1 "재무/회계" 톤 → 보수적 라이트 변형

| 영역 | SoT 정본 토큰 |
|---|---|
| 액센트 | `--jc-primary` (Deep Navy `--jc-data-5`) |
| 긍정 | `--jc-success-strong` (WCAG AA 본문 그린) |

---

## 3. 차트 컬러 시퀀스 (시리즈 색상)

차트의 데이터 시리즈별 색상은 SoT 의 `--jc-data-1..6` 시퀀스에 1:1 대응한다. 값은 `signature-tokens.md` §1.4(라이트) / `mode-mapping.md` §3.2(다크) 정본:

| 슬롯 | SoT 토큰 | 라이트 hex (정본) | 다크 hex (정본) |
|---|---|---|---|
| series-1 | `--jc-data-1` | `#2962FF` | `#5B8DEF` |
| series-2 | `--jc-data-2` | `#E91E63` | `#F04D85` |
| series-3 | `--jc-data-3` | `#FF5722` | `#FF7649` |
| series-4 | `--jc-data-4` | `#00E676` | `#33EE92` |
| series-5 | `--jc-data-5` | `#0A2540` | `#C9CFD8` |
| series-6 | `--jc-data-6` | `#7C3AED` | `#A78BFA` |

→ Chart.js 글로벌 설정에 위 SoT 정본 hex 주입. (값은 signature-tokens.md §1.4 / mode-mapping.md §3.2 정본)

---

## 4. 4종 자체 팔레트 호환 매핑

기획자님이 v1 의 4종 톤(기업/공식·성과/실적·마케팅·재무)을 그대로 사용하고 싶을 때:

| v1 톤 | SoT 토큰 묶음 (모드) | 호출 |
|---|---|---|
| 기업/공식 (다크) | `--jc-bg`+`--jc-accent` (다크 모드 변형) | `applyTone('corporate-dark')` |
| 성과/실적 (라이트) | `--jc-bg`+`--jc-accent` (라이트) | `applyTone('business-light')` |
| 마케팅/이벤트 | `--jc-bg`+`--jc-point-magenta`/`--jc-point-orange` (라이트) | `applyTone('event-light')` |
| 재무/회계 | `--jc-bg`+`--jc-primary` (라이트) | `applyTone('finance-light')` |

→ v1 의 4종 톤을 SoT 토큰 + 라이트/다크 모드 조합으로 재현 가능 (회귀 없음). 클라이언트별 hex 치환은 `client-overlays.md` 가 처리.

---

## 5. 다크 모드 매핑 (5종 변형)

상세는 [dark-mode-patterns.md](dark-mode-patterns.md) 참조.

값은 `mode-mapping.md` §3·§3.2 정본을 따른다.

| 컴포넌트 | 라이트 SoT 토큰 | 다크 SoT 매핑 (mode-mapping §3) |
|---|---|---|
| KPI 카드 배경 | `--jc-surface` | 다크 카드 서피스 |
| 차트 영역 배경 | `--jc-bg` | 다크 페이지 배경 |
| 테이블 행 호버 | `--jc-surface-alt` | 다크 보조 서피스 |
| 콜아웃/배너 | `--jc-accent-soft` | 다크 액센트 기반 틴트 |
| 헤더 배경 | `--jc-surface`→`--jc-surface-alt` | 다크 bg→surface |

---

## 6. 클라이언트 오버레이 토글 (개념)

```javascript
// 향후 구현 (Sprint 7)
import { setOverlay, getToken } from 'jc-design-system';
setOverlay('<client-id>');                  // 클라이언트 오버레이 선택 (client-overlays.md 정의)
const primary = getToken('--jc-accent');    // 오버레이별 치환값 반환 (hex 는 client-overlays.md 단일 소유)
```

> 기본(오버레이 미적용) `--jc-accent` 정본값은 `signature-tokens.md` §1.2(`#2962FF`). 클라이언트별 치환 hex 는 본 문서에 하드코딩하지 않는다 — `client-overlays.md` 가 단일 소유.

현재: HTML 템플릿에 SoT 정본 hex 직접 명시 + `SoT 미러: <토큰명>` 주석. 본 문서의 SoT 토큰명과 1:1 매핑 보장.

---

## 7. 본 Sprint 의 적용 범위

| 항목 | 적용 |
|---|---|
| 매핑 문서 (본 문서) | ✅ |
| HTML 템플릿에 hex 직접 명시 + 토큰명 주석 | ✅ |
| 런타임 jc-design-system 토큰 fetch | ❌ Sprint 7 |
| 클라이언트 오버레이 자동 토글 | ❌ Sprint 7 |
| Pretendard 폰트 보장 | CDN 로드 (assets HTML 의 head) |

---

## 8. 결정 사항

- ✅ 4종 자체 팔레트의 시맨틱 토큰 매핑 동결
- ✅ 라이트·다크 모드 분리 토큰
- ✅ 차트 시리즈 색상 6 슬롯 시퀀스
- ✅ HTML 템플릿의 hex 는 v1 호환 유지 + 토큰명 주석
