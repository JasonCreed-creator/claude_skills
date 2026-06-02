# jc-design-system 매핑 (jc-design-mapping)

**대상 스킬**: jc-design-system (SoT — Single Source of Truth)
**참조**: jc-design-system `references/signature-tokens.md` (§1 라이트 토큰, §6 JSON 정본), `references/mode-mapping.md`
**상태**: ✅ R1 정합 완료 — jc-design-system 정본 참조

mice-estimate v1은 Excel 자체 색상 hex(예: `#003366`, `#FF6D01`)을 직접 사용 → 디자인 일관성 깨짐. v2/R1은 각 색상의 **시맨틱 역할**을 jc-design-system 시그니처 토큰에 매핑한다. 모든 색상 값의 정본은 jc-design-system `signature-tokens.md §6 JSON 정본`이며, 본 문서는 "Excel 셀 역할 → SoT 토큰" 참조표다.

> **매체 제약**: Excel(xlsx)은 CSS 변수를 사용할 수 없으므로, 렌더링 단계의 hex 리터럴은 불가피하다. 이 리터럴은 반드시 SoT 정본값과 일치시키고 `SoT 미러: --jc-xxx` 주석을 단다(`scripts/export_estimate.py` 참조). 값 자체는 본 문서가 아니라 SoT JSON 정본을 진실의 원천으로 한다.

---

## 1. 매핑 원칙

1. **시맨틱(역할) 우선**: hex 코드를 직접 외우지 않고 "이 셀의 *역할*은 무엇인가"로 식별한 뒤 SoT 토큰에 매핑.
2. **클라이언트 오버레이**: 동일 역할이라도 클라이언트(`mc`, `remember`)별 브랜드 색이 다를 수 있다. 기본(시그니처)은 SoT 정본, 오버레이는 `jc-design-system/client-overlays.md` 책임.
3. **유니버설 vs 클라이언트별**:
   - 시맨틱(danger·success 등)·중립(텍스트·보더·서피스) 역할 → 유니버설 (SoT 시그니처 그대로)
   - 브랜드(primary·accent) 역할 → 시그니처는 SoT, 클라이언트별 차별화는 오버레이

---

## 2. M&C 양식 매핑 (Excel 셀 역할 → SoT 토큰)

값은 모두 jc-design-system `signature-tokens.md §6 JSON 정본` 기준. 아래 hex는 "SoT 정본값"으로, Excel 렌더링 시 미러링되는 참고치다.

| Excel 위치 | 시맨틱 역할 | SoT 토큰 | SoT 정본값 | 비고 |
|---|---|---|---|---|
| 세부산출내역 타이틀 (A19:K19) | 헤더·타이틀 (신뢰 톤) | `--jc-primary` | `#0A2540` | Deep Navy — 표지/헤더/로고 역할 |
| 열 헤더 행 (Row 20) | 헤더 배경 | `--jc-primary` | `#0A2540` | 동상 |
| 카테고리 행 (예: "1. 유통판로 지원") | 액센트·구분 강조 | `--jc-accent` | `#2962FF` | Electric Blue 액센트 |
| 소계 금액 강조 | 위험·금액 강조 (시맨틱) | `--jc-danger` | `#D32F2F` | 유니버설 — 모든 클라이언트 공통 |
| 소계 행 배경 | 중립 강조 보더/면 | `--jc-border-strong` | `#C9CFD8` | 유니버설 |
| 헤더 텍스트 | 카드·시트 서피스(흰색) | `--jc-surface` | `#FFFFFF` | 유니버설 |
| Row 17 (총견적) 배경 | 헤더·강조 | `--jc-primary` | `#0A2540` | 유니버설(시그니처) |
| 데이터 행 hair 테두리 | 구분선 | `--jc-border` | `#E5E8ED` | 유니버설 (hair/thin 두께는 렌더 로직) |
| 데이터 행 thin 외곽 | 강조 보더 | `--jc-border-strong` | `#C9CFD8` | 유니버설 |
| 본문 폰트 | 본문 | `--jc-font-ko` + `--jc-text-base`(16px) | Pretendard | M&C 표준 (xlsx 실제 12pt 매체값) |
| 타이틀 폰트 | 페이지 타이틀 | `--jc-font-heading` + `--jc-text-4xl`(44px) | Pretendard | Row 1 (xlsx 실제 30pt 매체값) |
| 헤더 폰트 | H4·소제목 | `--jc-font-heading` + `--jc-text-xl`(22px) + `--jc-weight-bold` | Pretendard | 행사명·고객명 등 (xlsx 실제 14pt 매체값) |

> Excel 폰트 포인트(12/14/30pt)는 xlsx 매체 고유 단위로, SoT의 px 스케일과 1:1 대응이 아니라 역할(본문/헤딩/타이틀) 기준 매핑이다.

---

## 3. 리멤버 양식 매핑 (Excel 셀 역할 → SoT 토큰)

| Excel 위치 | 시맨틱 역할 | SoT 토큰 | SoT 정본값 | 비고 |
|---|---|---|---|---|
| 섹션 라벨 배경 (A12 등) | 포인트·핫 강조 (브랜드 포인트) | `--jc-point-orange` (= `--jc-data-3`) | `#FF5722` | Vivid Orange — 리멤버 시그니처 포인트 역할 |
| 열 헤더 배경 | 본문 텍스트(Charcoal) 톤의 진한 헤더 면 | `--jc-text` | `#1A1D24` | 유니버설 (중립 다크 면) |
| 열 헤더 텍스트 | 카드·시트 서피스(흰색) | `--jc-surface` | `#FFFFFF` | 유니버설 |
| 본문 폰트 | 보조 텍스트·테이블 | `--jc-font-ko` + `--jc-text-sm`(14px) | 맑은 고딕(레거시 폴백) | 리멤버 표준 (xlsx 실제 10pt 매체값) |
| VAT 비고 강조 | 강조 본문 | `--jc-font-ko` + `--jc-weight-bold` | (유니버설) | |

> `--jc-point-orange`의 인쇄·구형 모니터 폴백은 없음(SoT §1.3). Neon 계열만 폴백 정의됨.

---

## 4. 클라이언트 오버레이 토글 (개념 설계)

본 문서는 *정적 역할 매핑*을 정의한다. 실제 런타임 토글·오버레이 주입은 jc-design-system 스킬의 `client-overlays.md`가 SoT로 관장한다.

```python
# 개념 모식 — 실제 토큰 값은 jc-design-system SoT가 반환
from jc_design_system import get_token, set_overlay

set_overlay('mc')                         # M&C 견적서 생성 시
primary = get_token('--jc-primary')       # 시그니처 정본 → '#0A2540' (오버레이 시 mc 브랜드값)

set_overlay('remember')                   # 리멤버 견적서 생성 시
point = get_token('--jc-point-orange')    # → '#FF5722' (리멤버 포인트 역할)
```

xlsx는 매체 특성상 hex를 직접 기입하되, 의미는 본 문서의 SoT 토큰과 1:1 매핑됨을 보장한다. 값의 진실의 원천은 jc-design-system `signature-tokens.md §6 JSON 정본`이다.

---

## 5. 적용 범위

| 항목 | 적용 여부 |
|---|---|
| 역할 매핑 문서 (본 문서) | ✅ |
| Excel 생성 코드 hex → SoT 정본값 정합 + `SoT 미러` 주석 | ✅ (`scripts/export_estimate.py`) |
| 런타임 jc-design-system 토큰 fetch | jc-design-system SoT 책임 (향후) |
| 클라이언트 오버레이 자동 토글 | jc-design-system `client-overlays.md` 책임 |
| Pretendard 폰트 보장 | 사용자 PC 설치 책임 |

---

## 6. jc-design-system 정본과의 정합 (R1)

본 매핑의 정합성 보장 조건:

1. 색상 값의 정본은 jc-design-system `signature-tokens.md §6 JSON 정본` — 본 문서는 토큰명 참조만 하고 값을 재정의하지 않는다.
2. `client-overlays.md`에 `mc`·`remember` 오버레이 정의(브랜드 색 차별화)를 둔다.
3. 견적서(xlsx)는 라이트 모드 전용 — `mode-mapping.md §1`상 xlsx 기본 모드 Light, 다크는 N/A(인쇄·이메일 첨부 표준).
4. mice-estimate 렌더 코드는 SoT 정본값을 미러링하고 `SoT 미러: --jc-xxx` 주석으로 추적성을 유지한다.

✅ R1 정합 완료 — jc-design-system 정본 참조

---

## 7. 결정 사항 (R1 확정)

- ✅ **색상 정본은 jc-design-system SoT(`signature-tokens.md §6`)로 단일화**. 본 문서는 역할→토큰 참조표 역할만 한다.
- ✅ **Excel 생성 코드의 hex는 SoT 정본값으로 정합**(드리프트 교정). 매체 제약상 리터럴은 유지하되 `SoT 미러` 주석 필수.
- ✅ **클라이언트 오버레이는 mc / remember 만 정의**. 그 외는 미사용.
