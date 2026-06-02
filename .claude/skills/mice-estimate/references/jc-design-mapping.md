# jc-design-system 매핑 (jc-design-mapping)

**대상 스킬**: jc-design-system v1 (별도 스킬)
**참조**: master-plan-2026-05-25.md §2-1 (jc-design-system 연동 표준)
**적용 범위 (Sprint 1)**: 정적 매핑 문서 작성만. 런타임 토큰 fetch는 Sprint 7 통합 검증 시 구현.

mice-estimate v1은 Excel 자체 색상 hex(#003366, #FF6D01 등)을 직접 사용 → 디자인 일관성 깨짐. v2는 각 색상의 **시맨틱 의미**를 jc-design-system 토큰에 매핑하여, 향후 클라이언트 오버레이 토글 가능.

---

## 1. 매핑 원칙

1. **시맨틱 우선**: Hex 코드를 직접 외우지 않고 "이 셀의 *의미*는 무엇인가"로 식별.
2. **클라이언트 오버레이**: 동일 시맨틱이라도 클라이언트(`mc`, `remember`, `darktrace`, `confex`)별로 다른 hex.
3. **유니버설 vs 클라이언트별**:
   - `COLOR_SEMANTIC_*` (danger, success, neutral 등) → 유니버설 (오버레이와 무관)
   - `COLOR_BRAND_*` (primary, accent) → 클라이언트별

---

## 2. M&C 양식 매핑

| Excel 위치 | 현재 Hex (v1) | JC 시맨틱 토큰 (제안) | `mc` 오버레이 hex | 비고 |
|---|---|---|---|---|
| 세부산출내역 타이틀 (A19:K19) | `#003366` | `COLOR_BRAND_PRIMARY` | `#003366` (유지) | M&C 시그니처 진남색 |
| 열 헤더 행 (Row 20) | `#003366` | `COLOR_BRAND_PRIMARY` | `#003366` | 동상 |
| 카테고리 행 (예: "1. 유통판로 지원") | `#0066CC` | `COLOR_BRAND_ACCENT` | `#0066CC` | M&C 액센트 파랑 |
| 소계 금액 빨강 | `#FF0000` | `COLOR_SEMANTIC_DANGER` | (유니버설) | 금액 강조 — 모든 클라이언트 공통 |
| 소계 행 배경 회색 | `#C0C0C0` | `COLOR_NEUTRAL_LIGHT` | (유니버설) | |
| 헤더 텍스트 흰색 | `#FFFFFF` | `COLOR_NEUTRAL_WHITE` | (유니버설) | |
| Row 17 (총견적) 배경 | `#003366` | `COLOR_BRAND_PRIMARY` | `#003366` | |
| 데이터 행 hair 테두리 | (회색) | `COLOR_NEUTRAL_BORDER_HAIR` | (유니버설) | |
| 데이터 행 thin 외곽 | (검정) | `COLOR_NEUTRAL_BORDER_THIN` | (유니버설) | |
| 본문 폰트 | Pretendard 12pt | `FONT_BODY` + `SIZE_BODY` | Pretendard | M&C 표준 |
| 타이틀 폰트 | Pretendard 30pt Bold | `FONT_DISPLAY` + `SIZE_DISPLAY` | Pretendard | Row 1 |
| 헤더 폰트 | Pretendard 14pt Bold | `FONT_HEADING_2` + `SIZE_HEADING_2` | Pretendard | 행사명·고객명 등 |

---

## 3. 리멤버 양식 매핑

| Excel 위치 | 현재 Hex (v1) | JC 시맨틱 토큰 | `remember` 오버레이 hex | 비고 |
|---|---|---|---|---|
| 섹션 라벨 배경 (A12 등) | `#FF6D01` | `COLOR_BRAND_PRIMARY` | `#FF6D01` | 리멤버 시그니처 오렌지 |
| 열 헤더 배경 | `#434343` | `COLOR_NEUTRAL_DARK` | (유니버설) | |
| 열 헤더 텍스트 흰색 | `#FFFFFF` | `COLOR_NEUTRAL_WHITE` | (유니버설) | |
| 본문 폰트 | 맑은 고딕 10pt | `FONT_BODY_KO_LEGACY` + `SIZE_BODY_SMALL` | 맑은 고딕 | 리멤버 표준 |
| VAT 비고 Bold | (검정) | `FONT_BODY` + `WEIGHT_BOLD` | (유니버설) | |

---

## 4. 클라이언트 오버레이 토글 (개념 설계)

본 Sprint에서는 *정적 매핑*만 정의. 실제 런타임 토글은 Sprint 7 통합 시.

```python
# 향후 구현 모식 (Sprint 7)
from jc_design_system import get_token, set_overlay

set_overlay('mc')                                # M&C 견적서 생성 시
primary = get_token('COLOR_BRAND_PRIMARY')       # → '#003366'

set_overlay('remember')                          # 리멤버 견적서 생성 시
primary = get_token('COLOR_BRAND_PRIMARY')       # → '#FF6D01'
```

현재(Sprint 1)는 양식별로 hex를 직접 명시하되, 의미는 본 문서의 시맨틱 토큰과 1:1 매핑됨을 보장. 향후 jc-design-system 스킬과 통합 시 본 매핑이 참조표 역할.

---

## 5. 본 Sprint의 적용 범위

| 항목 | 적용 여부 |
|---|---|
| 매핑 문서 작성 (본 문서) | ✅ |
| Excel 생성 코드에 hex 직접 명시 | ✅ 유지 (v1 동작 호환) |
| 런타임 jc-design-system 토큰 fetch | ❌ Sprint 7 |
| 클라이언트 오버레이 자동 토글 | ❌ Sprint 7 |
| Pretendard 폰트 보장 | 사용자 PC 설치 책임 (sprint1-guide §3-2) |

---

## 6. 미래 확장 (Sprint 7 통합 시)

본 매핑이 정합성을 갖춤을 보장하려면:

1. jc-design-system 스킬의 `signature-tokens.md`에 본 토큰명이 실제 정의되어야 함 (Sprint 7에서 확인·확장)
2. `client-overlays.md`에 `mc`·`remember` 오버레이 정의 완비 확인
3. `mode-mapping.md`에 견적서용 라이트/다크 매핑 정의 (xlsx는 다크 N/A — 양식 특성상)
4. mice-estimate에서 `jc_design_system` import 또는 reference fetch 메커니즘 구현

Sprint 7 종료 시 본 문서의 토큰명을 실제 jc-design-system 토큰명과 정합화.

---

## 7. 결정 사항 (이 Sprint에서 확정)

- ✅ **시맨틱 매핑은 본 문서로 동결**. 향후 토큰명 변경 시 본 문서를 진실의 원천(SoT)으로 갱신.
- ✅ **Excel 생성 코드의 hex는 v1 그대로 유지**. v2에서 hex 자체는 변경하지 않음 (호환성).
- ✅ **클라이언트 오버레이는 mc / remember 만 정의**. darktrace·confex·personal 은 미사용.
