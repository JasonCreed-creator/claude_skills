# jc-design-system 매핑 (jc-design-mapping)

**대상 스킬**: jc-design-system v1 (별도 스킬)
**참조**: master-plan §2-1 (표준 강화 체크리스트 jc 연동)
**적용 범위 (Sprint 2)**: 정적 매핑 문서. 런타임 토큰 fetch는 Sprint 7 통합 검증 시.

mice-dashboard v1 은 4종 자체 컬러 팔레트(`#0A2540`, `#2962FF`, `#E91E63`, `#1A3556` 등)를 직접 사용 → 디자인 일관성 깨짐. v2 는 각 팔레트를 **jc 시맨틱 토큰**으로 매핑하여 클라이언트 오버레이 토글 가능 구조 확보.

---

## 1. 매핑 원칙

1. **시맨틱 우선**: hex 대신 의미 토큰. 어떤 카드·차트도 토큰명으로 식별.
2. **클라이언트 오버레이**: 동일 시맨틱이라도 클라이언트(`remember`, `confex`, `personal`)별로 다른 hex. 구 `mc`·`darktrace`는 아카이브(deprecated) — 신규 산출물 사용 금지.
3. **모드 분리**: 라이트·다크는 동일 시맨틱 토큰의 모드 변형.

---

## 2. 4종 자체 팔레트 → JC 토큰 매핑

### 2.1 v1 "기업/공식" 톤 (다크) → JC 다크 모드

| 영역 | v1 hex | JC 시맨틱 토큰 | remember 오버레이 hex (라이트) | remember 오버레이 hex (다크) |
|---|---|---|---|---|
| 페이지 배경 | `#0A2540` | `COLOR_BG_PAGE` | `#ffffff` | `#0A2540` |
| 카드 배경 | `#1A3556` | `COLOR_BG_CARD` | `#F8F9FB` | `#1A1D24` |
| 액센트 | `#1A3556` | `COLOR_BRAND_PRIMARY` | `#0A2540` | `#1E4DCC` |
| 강조/하이라이트 | `#E91E63` | `COLOR_SEMANTIC_DANGER` | `#D32F2F` | `#D32F2F` |

### 2.2 v1 "성과/실적" 톤 (라이트) → JC 라이트 모드 기본

| 영역 | v1 hex | JC 시맨틱 토큰 | 유니버설 hex |
|---|---|---|---|
| 페이지 배경 | `#ffffff` | `COLOR_BG_PAGE` | `#ffffff` |
| 카드 배경 | `#F8F9FB` | `COLOR_BG_CARD` | `#F8F9FB` |
| 액센트 | `#2962FF` | `COLOR_BRAND_PRIMARY_BIZ` | `#2962FF` |
| 긍정 | `#00C853` | `COLOR_SEMANTIC_SUCCESS` | `#00C853` |

### 2.3 v1 "마케팅/이벤트" 톤 → confex 오버레이 후보

| 영역 | v1 hex | JC 시맨틱 토큰 | confex 오버레이 hex |
|---|---|---|---|
| 액센트 1 | `#E91E63` | `COLOR_BRAND_PRIMARY` | `#E91E63` |
| 액센트 2 | `#FFA000` | `COLOR_BRAND_ACCENT` | `#FFA000` |
| 액센트 3 | `#E91E63` | `COLOR_BRAND_HIGHLIGHT` | `#E91E63` |

### 2.4 v1 "재무/회계" 톤 → 보수적 라이트 변형

| 영역 | v1 hex | JC 시맨틱 토큰 | 유니버설 hex |
|---|---|---|---|
| 액센트 | `#1A3556` | `COLOR_BRAND_PRIMARY_FINANCE` | `#1A3556` |
| 긍정 | `#00733B` | `COLOR_SEMANTIC_SUCCESS_SUBDUED` | `#00733B` |

---

## 3. 차트 컬러 시퀀스 (시리즈 색상)

차트의 데이터 시리즈별 색상은 별도 시맨틱 토큰 시퀀스로 관리:

| 슬롯 | JC 토큰 | 라이트 hex | 다크 hex |
|---|---|---|---|
| series-1 | `COLOR_CHART_SERIES_1` | `#2962FF` | `#2962FF` |
| series-2 | `COLOR_CHART_SERIES_2` | `#E91E63` | `#E91E63` |
| series-3 | `COLOR_CHART_SERIES_3` | `#1E4DCC` | `#2962FF` |
| series-4 | `COLOR_CHART_SERIES_4` | `#FF5722` | `#FFA000` |
| series-5 | `COLOR_CHART_SERIES_5` | `#E91E63` | `#E91E63` |
| series-6 | `COLOR_CHART_SERIES_6` | `#00C853` | `#00C853` |

→ Chart.js 글로벌 설정에 토큰 매핑된 hex 주입.

---

## 4. 4종 자체 팔레트 호환 매핑

기획자님이 v1 의 4종 톤(기업/공식·성과/실적·마케팅·재무)을 그대로 사용하고 싶을 때:

| v1 톤 | JC 시맨틱 묶음 | 호출 |
|---|---|---|
| 기업/공식 (다크) | `COLOR_BG_PAGE` (다크) + `COLOR_BRAND_PRIMARY` (remember) | `applyTone('corporate-dark')` |
| 성과/실적 (라이트) | `COLOR_BG_PAGE` (라이트) + `COLOR_BRAND_PRIMARY_BIZ` | `applyTone('business-light')` |
| 마케팅/이벤트 | `COLOR_BG_PAGE` (라이트) + `COLOR_BRAND_PRIMARY` (confex) | `applyTone('event-light')` |
| 재무/회계 | `COLOR_BG_PAGE` (라이트) + `COLOR_BRAND_PRIMARY_FINANCE` | `applyTone('finance-light')` |

→ v1 의 4종 톤을 JC 토큰 + 라이트/다크 모드 조합으로 재현 가능 (회귀 없음).

---

## 5. 다크 모드 매핑 (5종 변형)

상세는 [dark-mode-patterns.md](dark-mode-patterns.md) 참조.

| 컴포넌트 | 라이트 토큰 | 다크 토큰 |
|---|---|---|
| KPI 카드 배경 | `COLOR_BG_CARD` | `COLOR_BG_CARD_DARK` |
| 차트 영역 배경 | `COLOR_BG_PAGE` | `COLOR_BG_PAGE_DARK` |
| 테이블 행 호버 | `COLOR_NEUTRAL_HOVER_LIGHT` | `COLOR_NEUTRAL_HOVER_DARK` |
| 콜아웃/배너 | `COLOR_ACCENT_SUBDUED_LIGHT` | `COLOR_ACCENT_SUBDUED_DARK` |
| 헤더 배경 | `COLOR_BG_HEADER_LIGHT` | `COLOR_BG_HEADER_DARK` |

---

## 6. 클라이언트 오버레이 토글 (개념)

```javascript
// 향후 구현 (Sprint 7)
import { setOverlay, getToken } from 'jc-design-system';
setOverlay('remember');                            // 소속사 기본 오버레이 (Track A) — 리멤버 전환(D2)
const primary = getToken('COLOR_BRAND_PRIMARY');   // → '#0A2540' (시그니처 유지)
const point   = getToken('COLOR_POINT_ORANGE');    // → '#FF5722' (리멤버 포인트 역할)
```

Sprint 2 현재: HTML 템플릿에 hex 직접 명시, 단 본 문서의 토큰명과 1:1 매핑 보장.

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
