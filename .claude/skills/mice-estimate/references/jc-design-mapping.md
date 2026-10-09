# jc-design-system 매핑

**대상 스킬**: jc-design-system (SoT — Single Source of Truth, v2 리멤버 웜 페이퍼)
**참조**: `jc-design-system/references/signature-tokens.md` (§6 JSON 정본), `jc-design-system/references/mode-mapping.md`, `jc-design-system/scripts/jc_tokens.py`(로더)
**상태**: v3.3.1 — 값 미러 폐지, 런타임 로드(`scripts/estimate_tokens.py`)

mice-estimate v1은 Excel 자체 색상 hex를 직접 사용 → 디자인 일관성 깨짐. v2/R1은 각 색상의 **시맨틱 역할**을 jc-design-system 토큰에 매핑했고, v3.3.1부터는 값을 문서·코드에 미러하지 않고 **실행 시점에 SoT JSON을 읽는다**. 모든 색상 값의 정본은 jc-design-system `signature-tokens.md §6 JSON`이며, 본 문서는 "Excel 셀 역할 → §6 키" 참조표다(값 열 없음).

> **매체 제약**: Excel(xlsx)은 CSS 변수를 쓸 수 없어 렌더링 단계에서는 hex 리터럴이 셀 스타일에 들어간다. 그 리터럴은 `estimate_tokens.palette()`가 실행 시점에 §6 JSON에서 꺼내 온 값이며, 로드 실패 시에만 §6 값을 출처 주석과 함께 둔 폴백 상수를 쓴다. 값을 바꾸려면 SoT를 고친다 — 본 스킬 쪽 문서·코드에서 값을 손대지 않는다.

---

## 1. 매핑 원칙

1. **시맨틱(역할) 우선**: hex 코드를 직접 외우지 않고 "이 셀의 *역할*은 무엇인가"로 식별한 뒤 §6 키에 매핑.
2. **클라이언트 오버레이**: 소속사 기본 오버레이는 `remember`. 기본(시그니처)은 SoT 정본, 오버레이는 jc-design-system `client-overlays.md` 책임.
3. **유니버설 vs 클라이언트별**:
   - 시맨틱(danger·warning 등)·중립(잉크·서피스) 역할 → 유니버설 (SoT 시그니처 그대로)
   - 브랜드(primary·accent) 역할 → 시그니처는 SoT, 클라이언트별 차별화는 오버레이
4. **값 미러 금지**: 문서·코드 어디에도 §6 값을 복제해 두지 않는다. 유일한 예외는 로더의 폴백 상수(§6 값 + 출처 주석, 로드 실패 시에만).

---

## 2. 런타임 로드 — `scripts/estimate_tokens.py`

`mice-rfp-analyzer/scripts/rfp_tokens.py`와 같은 패턴. importlib로 `jc-design-system/scripts/jc_tokens.py`(`find_sot`/`load_tokens`/`color`/`dark`)를 불러 §6 JSON을 파싱한다.

- **탐색 순서**: 형제 경로(`scripts/estimate_tokens.py` 파일 기준 parents[2] = `<skills>` 루트 → `jc-design-system`) → `~/.claude/skills/jc-design-system` → `~/.claude/skills/synced/*/jc-design-system`. 샌드박스 고정 경로는 보지 않는다.
- **API**: `palette() -> dict` — 역할명 → `'#'` 없는 6자리 HEX. `P["_source"]`는 `"sot:<경로>"` 또는 `"fallback"`.
- **소비처**: `export_estimate_remember.py`의 `ST` 스타일 사전이 `palette()` 값으로 fill·font 색을 채운다. `export_estimate_remember.py --self-test`가 `_source`를 출력하므로 SoT를 읽었는지 폴백인지 바로 확인할 수 있다.

---

## 3. 리멤버 양식 매핑 (Excel 셀 역할 → §6 키)

| 역할(palette 키) | §6 키 | 쓰이는 곳(`ST` 스타일) | 비고 |
|---|---|---|---|
| `ink` | `color.primary` | `title.fill`, `sec_amt.fill` | 타이틀·섹션 합계 다크 면 |
| `inkSoft` | `color.primarySoft` | `col_hdr.fill` | 열 헤더 다크 면 |
| `paper` | `color.surface` | `title`·`label_o`·`sec_amt`·`col_hdr` 글자색 | 다크 면 위 글자 |
| `surfaceAlt` | `color.surfaceAlt` | `label_g.fill` | 회색 라벨 |
| `surfaceSoft` | `color.surfaceSoft` | `sub.fill`, `sub_amt.fill` | 소계 행 |
| `accent` | `color.accent` | `label_o.fill`, `tot_val` 글자색 | 리멤버 오렌지 — 섹션 라벨·총액 |
| `accentSoft` | `color.accentSoft` | `tot_kor`·`tot_val`·`tot_sub`·`tot_vat.fill` | 총액 행 |
| `accentStrong` | `color.accentStrong` | `warn` 글자색 | 경고 문구 |
| `warningBg` | `color.semantic.warningBg` | `warn.fill` | 경고 배경 |
| `amberTint` | `color.point.amberTint` | `sec_hdr.fill` | 섹션 헤더 |
| `steel` | `color.point.steel` | `note_blue` 글자색 | 안내 문구 |
| `steelTint` | `color.point.steelTint` | `note_blue.fill` | 안내 배경 |
| `danger` | `color.semantic.danger` | `footer` 글자색 | 푸터 주의 문구 |
| (서체) | `font.ko` · `size.sm` · `weight.bold` | 본문 폰트 | 매체값(10pt·굵기)은 컨피규레이터 실측 그대로 — 토큰화 대상은 색뿐 |

색 외의 레이아웃(글꼴 크기·굵기·정렬·테두리·숫자서식·열 너비·행 높이)은 컨피규레이터 실측값을 유지한다. 견적서는 라이트 전용이라 `color.dark.*`는 쓰지 않는다.

---

## 4. 사용 예 — `estimate_tokens.palette()`

```python
import sys
sys.path.insert(0, str(SKILL / 'scripts'))          # SKILL = 이 스킬 폴더
from estimate_tokens import palette

P = palette()                 # 역할명 → '#' 없는 HEX 6자리 (SoT §6 JSON 런타임 로드)
P['accent']                   # 섹션 라벨 배경·총액 글자 — color.accent
P['ink'], P['paper']          # 다크 면과 그 위 글자 — color.primary / color.surface
P['_source']                  # 'sot:<jc-design-system 경로>' 또는 'fallback'
```

클라이언트 오버레이 토글은 jc-design-system `client-overlays.md`가 관장한다 — 본 스킬은 역할 키만 묻고, 값은 SoT가 돌려준다.

---

## 5. 적용 범위

| 항목 | 적용 여부 |
|---|---|
| 역할 매핑 문서 (본 문서) | ✅ |
| Excel 생성 코드 색 → 런타임 로드 (`scripts/estimate_tokens.py` → `export_estimate_remember.py` `ST`) | ✅ v3.3.1 |
| 폴백 상수 (§6 값 + 출처 주석, 로드 실패 시에만) | ✅ `estimate_tokens.py` 안에만 둔다 |
| 클라이언트 오버레이 자동 토글 | jc-design-system `client-overlays.md` 책임 |
| Pretendard 폰트 보장 | 사용자 PC 설치 책임 |

---

## 6. jc-design-system 정본과의 정합

본 매핑의 정합성 보장 조건:

1. 색상 값의 정본은 jc-design-system `signature-tokens.md §6 JSON` — 본 문서는 키만 참조하고 값을 재정의·미러하지 않는다.
2. `client-overlays.md`에 `remember`(소속사) 오버레이 정의를 둔다. 구 `mc`는 아카이브(deprecated).
3. 견적서(xlsx)는 라이트 모드 전용 — `mode-mapping.md §1`상 xlsx 기본 모드 Light, 다크는 N/A(인쇄·이메일 첨부 표준).
4. mice-estimate 렌더 코드는 `estimate_tokens.py`로 §6를 **런타임 로드**한다. 폴백 상수는 §6 값 + 출처 주석(로드 실패 시에만). `--self-test`의 `_source`로 SoT/폴백 여부를 확인한다.

---

## 7. 결정 사항

- ✅ **색상 정본은 jc-design-system SoT(`signature-tokens.md §6`)로 단일화**. 본 문서는 역할→키 참조표 역할만 한다.
- ✅ **값 미러 폐지(v3.3.1)**: Excel 생성 코드의 색은 `estimate_tokens.py` 런타임 로드. 폴백 상수는 §6 값 + 출처 주석으로 로더 안에만 둔다.
- ✅ **소속사 오버레이는 `remember`로 단일화**. 구 `mc`는 아카이브(deprecated), 그 외는 미사용.
