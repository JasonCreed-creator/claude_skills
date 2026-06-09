---
name: mice-sponsor-deck
description: MICE 행사의 스폰서·협찬사·후원사·파트너 유치용 영업 데크를 자동 생성하는 스킬. 발주처용 비딩 제안서가 아니라, 잠재 스폰서 기업의 마케팅 의사결정자에게 "당신 브랜드가 이 행사에서 얻을 노출·리드·ROI"를 제시하는 B2B 영업 자료다. 다음 상황에서 반드시 이 스킬을 사용할 것 사용자가 '스폰서십', '스폰서 유치', '스폰서 데크', '협찬', '협찬사 유치', '협찬 패키지', '협찬 제안서', '후원', '후원사 유치', '후원 제안', '파트너십 제안', '파트너 유치', 'sponsorship', 'sponsor deck', '스폰서 등급', 'Tier 구조', '협찬 등급'을 언급할 때. 행사 정보를 입력하며 '스폰서 데크 만들어줘', '협찬 패키지 만들어줘', '후원사 유치 자료 만들어줘'를 요청할 때. Tier별 혜택 매트릭스나 스폰서 ROI 케이스를 요청할 때. 본 스킬의 1차 산출물은 단일 파일 HTML 슬라이드 데크이며, 동일 콘텐츠를 변환한 PPTX(2차 산출물)와 Tier×혜택 매트릭스 XLSX(옵션)를 제공한다. jc-design-system 시그니처 토큰을 자동 적용하고 클라이언트 오버레이를 지원한다. 단, 다음 경우에는 사용하지 말 것 청중이 발주처(행사 의뢰자)인 일반 비딩·수주 제안서는 mice-proposal 영역. '제안서'·'PT 자료'·'비딩' 키워드만으로는 트리거하지 말 것 — 반드시 '스폰서/협찬/후원/파트너십' 키워드와 결합되어야 한다. 견적서는 mice-estimate, 발표 대본은 pt-script, 행사 결과 KPI 대시보드는 mice-dashboard 영역.
version: "v2.0.0"
---

# MICE 스폰서 데크 자동 생성 스킬

## 버전 히스토리

| 버전 | 일자 | 주요 변경점 |
|------|------|------------|
| v1.0 | 2026-05 | 초안. 6축 분석·Tier 5단·7카테고리·HTML+PPTX 2단 산출 모델. v1 references 7종. |
| **v2.0** | **2026-05-27** | **(1) 비주얼 패턴 7종 신규 정의 (`visual-patterns.md`)** — SVP-1 Tier 카드 / SVP-2 매트릭스 / SVP-3 ROI 3단 / SVP-4 KPI 콜아웃 / SVP-5 산업 분포 가로 바 / SVP-6 퍼널 / SVP-7 2×2 매트릭스. (2) **다크 모드 5종 신규 정의 (`dark-mode-patterns.md`)** — DARK-TIER / DARK-MATRIX / DARK-ROI / DARK-KPI / DARK-COVER + 슬라이드별 라이트/다크 컨텍스트 매트릭스. (3) **체이닝 명시 (`chaining-schema.md`)** — mice-meeting-minutes 스폰서 후보 추출 → sponsor-deck 입력 JSON 스키마. (4) **HTML 템플릿 2종 신규** — `assets/sponsor-deck-template-light.html`·`assets/sponsor-deck-template-dark.html` 자족형 단일 파일. (5) **샘플 생성기 (`scripts/sample_generator.py`)** — 가상 시나리오 콘텐츠 JSON 출력 (UTF-8 stdout 표준). v1 references 7종은 그대로 유지. |

---

## 개요

MICE 행사의 잠재 스폰서·협찬사·후원사·파트너 유치를 위한 B2B 영업 데크를 자동 생성한다.

**본 스킬의 본질은 "행사를 파는 것"이 아니라 "행사 위의 노출 자산을 파는 것"이다.** 청중은 행사 발주처가 아니라, 행사에 협찬·후원으로 참여할 가능성이 있는 기업의 마케팅 의사결정자다.

---

## 산출물 정책

본 스킬은 **HTML을 1차 산출물로 빌드하고, 동일 콘텐츠를 PPTX로 변환**하는 2단계 산출 모델을 따른다. HTML이 콘텐츠 의사결정의 단일 source이며, PPTX는 HTML 확정 후 변환된 결과물이다.

| 단계 | 산출물 | 형식 | 필수/옵션 | 빌드 방법 |
|------|--------|------|-----------|-----------|
| 1차 | HTML 슬라이드 데크 | 단일 HTML 파일 | **필수** | 자체 슬라이드 카드 시스템 + 키보드 네비 + 인쇄 페이지 분리. `assets/sponsor-deck-template-light.html` 또는 `assets/sponsor-deck-template-dark.html` 베이스 |
| 2차 | PPTX 영업 데크 | .pptx | **필수** | HTML 확정 콘텐츠 → pptxgenjs 변환. `references/visual-patterns.md`·`references/dark-mode-patterns.md` 패턴 적용 |
| 옵션 | 혜택 매트릭스 | .xlsx | 사용자 요청 시 | xlsx skill |

### 워크플로우 원칙

```
콘텐츠 JSON 추출 → HTML 빌드 → 사용자 검토 → HTML 확정
                                                    ↓
                                              동일 콘텐츠로 PPTX 변환
                                                    ↓
                                              (옵션) XLSX 매트릭스
```

**반드시 HTML 검토·확정 이후에 PPTX를 빌드한다.** HTML과 PPTX의 콘텐츠가 일치해야 하며, 슬라이드 1:1 매핑을 유지한다.

---

## 다른 스킬과의 경계 (필독)

| 산출물 청중 | 스킬 | 핵심 메시지 |
|---|---|---|
| 발주처(행사 의뢰자) | `mice-proposal` | "우리가 이 행사를 잘 만든다" |
| **잠재 스폰서·후원사·파트너** | **`mice-sponsor-deck` (본 스킬)** | **"당신 브랜드가 얻을 노출·리드·ROI는 이만큼이다"** |

### 라우팅 우선순위

1. 사용자 요청에 **"스폰서/협찬/후원/파트너십"** 키워드가 있으면 본 스킬
2. **"제안서"·"PT 자료"·"비딩"** 키워드만 있으면 `mice-proposal`
3. **결합어("협찬 제안서", "스폰서십 PT", "후원 비딩")** 인 경우 본 스킬 우선
4. 모호한 경우 사용자에게 청중 명시적 확인: "이 자료의 청중이 행사 발주처입니까, 스폰서·후원사 유치 대상입니까?"

---

## 비주얼 패턴 라이브러리 (v2.0 신규)

> 이미지 에셋은 jc-design-system의 RULE-VISUAL-ROUTING을 따른다 (사진/래스터=Higgsfield, 표·다이어그램·차트=Claude 자체).

`references/visual-patterns.md` 참조. 본 스킬은 HTML과 PPTX 양쪽에서 사용할 수 있는 7종 표준 비주얼 패턴을 정의한다.

| 코드 | 패턴 | 적용 슬라이드 | 산출물 |
|------|------|---------------|--------|
| **SVP-1** | Tier 카드 (좌측 액센트 막대 + Tier 색상) | S5 Sponsor Tiers | HTML 카드 + PPTX `addShape` |
| **SVP-2** | Benefits 매트릭스 표 (7카테고리×Tier) | S6 Benefits Matrix | HTML 표 + PPTX `addTable` |
| **SVP-3** | ROI 3단 카드 (전제·공식·추정값) | S7 ROI Snapshot | HTML 카드 + PPTX `roundRect` |
| **SVP-4** | KPI 콜아웃 (큰 숫자 + 캡션) | S3 Who Attends | HTML 카드 + PPTX `addText` |
| **SVP-5** | 산업 분포 가로 바 차트 | S3 Who Attends | HTML CSS 차트 + PPTX `addChart` |
| **SVP-6** | 모객·전환 퍼널 | S3 Who Attends (선택) | HTML SVG + PPTX 사각형 적층 |
| **SVP-7** | 2×2 매트릭스 (Tier 차별화·산업 우선순위) | S2 또는 S5 (선택) | HTML SVG + PPTX `addShape` |

각 패턴은 다음 구조를 갖는다:
- **사양 표** (용도, 형태, 컬러 위계, 적용 슬라이드)
- **HTML 코드 스니펫** (jc-design-system CSS 변수 사용)
- **PPTX 코드 스니펫** (pptxgenjs, hex 컬러 `#` 없이)
- **검증 체크리스트 항목**

HTML→PPTX 1:1 변환 룰표는 `references/visual-patterns.md` §8 참조.

---

## 다크 모드 (v2.0 신규)

`references/dark-mode-patterns.md` 참조. 스폰서 데크의 임팩트 강화를 위해 5종 다크 패턴 + 슬라이드별 컨텍스트 매트릭스를 정의한다.

### 적용 컨텍스트 (슬라이드별 라이트/다크 권장)

| 슬라이드 | 라이트 권장 | 다크 권장 | 비고 |
|----------|-------------|-----------|------|
| S1 표지 | ⚠️ | ✅ | HERO 이미지 + 다크 오버레이 (영업용 임팩트) |
| S2 Why This Event | ✅ | ⚠️ | 다크 변형 가능 (섹션 구분 강조) |
| S3 Who Attends | ✅ | ❌ | 차트·KPI 가독성 우선 |
| S4 What We Offer | ✅ | ❌ | 리스트·인벤토리 가독성 우선 |
| S5 Sponsor Tiers | ✅ | ⚠️ | T1 강조 시 다크 단일 슬라이드 가능 |
| S6 Benefits Matrix | ✅ | ❌ | 매트릭스 가독성 절대 우선 |
| S7 ROI Snapshot | ⚠️ | ✅ | KPI 임팩트 버전 (Electric Blue 강조) |
| S8 Past Sponsors | ✅ | ❌ | 로고 그리드 — 라이트 권장 |
| S9 Contact | ⚠️ | ✅ | Thank You 톤 — 다크 강력 권장 |

**원칙: 다크 슬라이드는 전체 분량의 30% 이내로 통제** (가독성·인쇄 호환성).

### 다크 5종 패턴

| 코드 | 패턴 | 라이트 대응 |
|------|------|------------|
| **DARK-TIER** | 다크 배경 Tier 카드 (좌측 액센트 막대 유지) | SVP-1 |
| **DARK-MATRIX** | 다크 Benefits 매트릭스 표 | SVP-2 |
| **DARK-ROI** | 다크 ROI 3단 카드 (Electric Blue 임팩트) | SVP-3 |
| **DARK-KPI** | 다크 KPI 콜아웃 (큰 숫자 강조) | SVP-4 |
| **DARK-COVER** | 다크 표지 + "For Sponsors" 배지 | S1 표지 |

상세 코드 스니펫은 `references/dark-mode-patterns.md` §1~5 참조. HTML 토글 스크립트는 §6, PPTX 변환 룰은 §7, WCAG AA 대비비 체크리스트는 §8.

---

## 체이닝 명시 (v2.0 신규)

`references/chaining-schema.md` 참조. 본 스킬은 다음 체이닝 워크플로우를 명시적으로 지원한다.

```
mice-meeting-minutes (Discovery 미팅 transcript)
  ↓ 스폰서 후보 추출 (Action Items 또는 별도 섹션)
sponsor-candidates.json
  ↓
mice-sponsor-deck (본 스킬)
  ↓
HTML 1차 + PPTX 2차 + (옵션) XLSX
```

### 입력 JSON 스키마 (mice-meeting-minutes → sponsor-deck)

```json
{
  "event_meta": {
    "event_name": "TOBESOFT TECH FORUM 2026",
    "event_date": "2026-09-15",
    "event_venue": "코엑스 컨벤션홀"
  },
  "sponsor_candidates": [
    { "name": "[기업명1]", "industry": "tech", "tier_target": "T1", "priority": "high", "notes": "..." },
    { "name": "[기업명2]", "industry": "finance", "tier_target": "T2", "priority": "high", "notes": "..." }
  ],
  "extracted_from": "mice-meeting-minutes",
  "extraction_date": "2026-05-27"
}
```

`industry` 값은 `references/roi-case-templates.md` §2.1 산업 5종(tech/finance/cpg/b2b/public) 그대로 매핑한다. `tier_target` 은 `references/tier-framework.md` Tier ID(T1~T6) 사용.

### 다른 스킬과의 인터페이스

- **입력 (선택)**: `mice-meeting-minutes` Discovery 미팅에서 추출한 스폰서 후보 JSON
- **출력**: 단일 산출물 (HTML 1차 + PPTX 2차 + XLSX 옵션). sponsor-deck은 영업 채널 종착점 — 후속 스킬 없음

---

## 빌드 옵션 (외부 주입 변수)

본 스킬은 클라이언트별 차별화를 위한 외부 주입 변수를 지원한다. 사용자가 명시하지 않으면 기본값 사용.

| 변수명 | 값 | 기본값 | 설명 |
|--------|-----|--------|------|
| `client_id` | `null` 또는 식별자 | `null` | jc-design-system 클라이언트 오버레이 적용 |
| `naming_mode` | `ko_first` \| `en_first` | `ko_first` | Tier·카테고리 명칭 한글/영문 우선 토글 (예: `타이틀 (Title)` vs `Title (타이틀)`) |
| `price_mode` | `explicit` \| `on_request` | `on_request` | 가격을 데크에 명시할지 "별도 협의" 처리할지 |
| `output_format` | `html_only` \| `pptx_only` \| `both` | `both` | 산출물 형식 선택 |
| `include_xlsx` | `true` \| `false` | `false` | 혜택 매트릭스 XLSX 동봉 여부 |
| **`color_mode`** (v2.0) | `light` \| `dark_mixed` | `light` | 다크 슬라이드 활성화 여부. `dark_mixed`인 경우 S1·S7·S9 등 다크 권장 슬라이드에 다크 모드 적용 |

### 기본값 결정 근거

- `naming_mode = ko_first`: 한국 발주처·국내 기업 스폰서 영업이 다수
- `price_mode = on_request`: 한국 시장 관행상 가격 비공개가 안전. 민간 B2B 행사로 explicit 명시 요구 시 사용자가 토글
- `output_format = both`: 본 스킬의 핵심 가치는 HTML+PPTX 동시 제공
- `include_xlsx = false`: Tier가 5단 이상이거나 발주처가 명시적 매트릭스 요구 시에만 활성화
- `color_mode = light`: 일반 영업 데크는 라이트 우선. 임팩트 강화 요구 시 `dark_mixed` 토글

---

## 워크플로우

### Phase 1: 행사 정보 수집

사용자가 업로드한 행사 자료(제안서·기획서·운영안·과거 결과보고서) 또는 대화 입력에서 다음 정보를 수집한다. (v2.0: mice-meeting-minutes 산출 JSON을 입력으로 받을 수 있음 — `references/chaining-schema.md` 참조)

| 분류 | 항목 | 미확정 시 처리 |
|------|------|---------------|
| 행사 정의 | 행사명·부제·일시·장소·주최/주관·행사 유형 | 보완 요청 |
| 청중 자산 | 예상 참가자 수·산업 분포·직급 분포·의사결정권 | `references/audience-profile.md` fallback |
| 노출 자산 | 보유 노출 슬롯 (사이니지·홈페이지·이메일·세션·부스 등) | 표준 인벤토리 가이드 적용 |
| Tier 슬롯 수 | 각 Tier별 한정 슬롯 수 | **"협의 가능" 표기 + 사용자 경고 출력** |
| 가격 가이드 | 협찬 가격 범위 | `price_mode` 따라 처리 |
| 클라이언트 토큰 | jc-design-system 오버레이 ID | 시그니처 그대로 적용 |

**슬롯 수 미확정 경고 룰 (필수):**

발주처가 Tier 슬롯 수를 확정하지 않은 단계에서 데크를 먼저 작성하는 케이스가 빈번하다. 이 경우 본 스킬은 다음 절차를 따른다.

1. 미확정 Tier에 "협의 가능" 또는 "TBD" 표기
2. 사용자에게 명시적 경고 출력:
   ```
   ⚠ 슬롯 수가 미확정인 Tier가 있습니다. 영업 데크의 핵심은 희소성 표현입니다.
   가능한 한 빠르게 발주처와 슬롯 수를 확정하는 것을 권장합니다.
   미확정: [T1, T2, ...]
   ```
3. 사용자가 진행 의사를 표명하면 데크에 "잠정 / 확정 시 통지" 캡션 자동 삽입

### Phase 2: 6축 분석 프레임

수집한 정보를 다음 6축으로 구조화한다. 본 스킬의 핵심 분석 모델이다.

| 축 | 정의 | 산출 슬라이드 |
|---|---|---|
| ① 행사 정의 | 행사의 목적·규모·격 | 표지 + Why This Event |
| ② 청중 자산 | 참가자 프로파일 데이터 | Who Attends |
| ③ 노출 자산 인벤토리 | 행사가 보유한 모든 노출 슬롯 | What We Offer |
| ④ Tier 구조 | 협찬 등급별 가격·슬롯 수 제한 | Sponsor Tiers |
| ⑤ 혜택 매트릭스 | Tier × 7카테고리 매핑표 | Benefits Matrix |
| ⑥ ROI 케이스 | 스폰서 산업별 기대 효과 | ROI Snapshot + Next Steps |

6축 분석 결과를 사용자에게 요약 제시 → 확인 후 다음 단계.

### Phase 3: Tier 표준 적용

`references/tier-framework.md` 를 읽어 Tier 5단 + 1트랙 구조를 확정한다. 클라이언트 명칭 오버라이드, 가격 모드, 영문 병기 모드를 적용한다.

### Phase 4: 혜택 매트릭스 작성

`references/benefit-catalog.md` 를 읽어 7카테고리 표준 혜택을 행사 자산에 매핑한다. Tier × 카테고리 매트릭스를 작성한다. (v2.0: `references/visual-patterns.md` SVP-2 매트릭스 패턴 적용)

### Phase 5: ROI 케이스 시뮬레이션

`references/roi-case-templates.md` 를 읽어 산업 2~3종의 ROI 시나리오를 작성한다.

**ROI 3단 표현 룰 (필수):**

ROI는 본질적으로 추정치다. 추측 금지·팩트 기반 원칙을 지키기 위해 모든 ROI 케이스는 다음 3단 구조로 표현한다. (v2.0: `references/visual-patterns.md` SVP-3 ROI 카드 패턴 적용)

```
[ 전제 조건 ]   예: "참가자 5,200명 중 IT 의사결정자 1,560명"
       ↓
[ 산출 공식 ]   예: "노출 횟수 × 평균 노출 시간 × 의사결정자 비율"
       ↓
[ 보수적 추정값 ] 예: "리드 약 80~120건 (산업 평균 전환율 5~7% 적용)"
```

모든 ROI 슬라이드 하단에 "본 수치는 산업 벤치마크 기반 추정치입니다" 캡션 의무 삽입.

### Phase 6: 슬라이드 구조 확정

`references/slide-structure.md` 를 읽어 표준 12~18 슬라이드 구성안을 확정한다. 행사 규모와 신규/기존 여부에 따라 슬라이드 수 가감.

**Past Sponsors 분기 룰 (필수):**

| 행사 유형 | Section 8 처리 |
|---|---|
| 기존 행사 (과거 회차 존재) | "Past Sponsors" — 과거 협찬사 로고 그리드 |
| 신규 행사 (1회차) | "Reference Cases" — 주최사 과거 실적 또는 유사 행사 레퍼런스 |
| 데이터 없음 | Section 8 생략 (총 슬라이드 12~14장으로 축소) |

### Phase 7: HTML 빌드 (1차 산출물)

`references/output-build-guide.md` 의 HTML 빌드 가이드를 따라 단일 HTML 파일을 생성한다. `references/design-tokens-mapping.md` 에서 jc-design-system 시그니처 토큰을 매핑한다.

**v2.0 베이스 템플릿 활용:**

- `color_mode = light`: `assets/sponsor-deck-template-light.html` 베이스
- `color_mode = dark_mixed`: `assets/sponsor-deck-template-dark.html` 베이스

위 템플릿은 SVP-1~SVP-7 패턴 7종을 모두 포함하며, 다크 토글 스크립트가 내장되어 있다. 콘텐츠 JSON을 치환만 하면 된다.

HTML 산출물 핵심 요건:
- 단일 자족형 HTML 파일 (외부 의존성: Pretendard CDN 1개)
- 16:9 슬라이드 카드 시스템 (12~18장)
- 키보드 네비게이션 (←/→/Space/Esc/Home/End)
- 인쇄 시 슬라이드별 페이지 분리 (`@media print` + `@page A4 landscape`)
- 인터랙티브 요소 (Tier 호버, 매트릭스 정렬·필터, 다크 토글)
- jc-design-system 시그니처 토큰 적용

HTML 빌드 후 사용자에게 검토 요청.

### Phase 8: PPTX 변환 (2차 산출물)

**HTML 검토·확정 이후에만 PPTX 빌드 진입.** HTML 콘텐츠 데이터를 그대로 사용하여 동일 슬라이드를 PPTX로 변환한다.

PPTX 생성은 반드시 `/mnt/skills/public/pptx/SKILL.md` 의 pptxgenjs 방식을 따른다. HTML→PPTX 매핑 룰은 `references/visual-patterns.md` §8 + `references/output-build-guide.md` §5 에 정의.

### Phase 9: 옵션 산출물 — XLSX

`include_xlsx = true` 인 경우, Tier × 7카테고리 매트릭스 + 가격표(price_mode가 explicit일 때)를 별도 XLSX로 생성. `/mnt/skills/public/xlsx/SKILL.md` 가이드 따름.

### Phase 10: QA 및 전달

다음 체크리스트 통과 후 최종 전달:

- [ ] 청중 데이터에 출처가 명시되었는가 (과거 행사 / 산업 벤치마크 / 추정)
- [ ] Tier별 슬롯 수가 한정되어 희소성이 표현되었는가 (또는 미확정 경고가 처리되었는가)
- [ ] 혜택 매트릭스에서 Tier 간 차이가 명확한가
- [ ] ROI 케이스가 3단 구조(전제/공식/추정값)로 표현되고 "추정치" 캡션이 있는가
- [ ] ROI 케이스가 최소 2개 산업 이상 제시되었는가
- [ ] CTA에 담당자·연락처·마감일이 명시되었는가
- [ ] **회사 종속 표현이 0건인가** ("당사", "M&C", "엠앤씨", "리멤버앤컴퍼니" 등)
- [ ] jc-design-system 시그니처 토큰이 정확히 적용되었는가 (또는 클라이언트 오버레이)
- [ ] HTML과 PPTX의 콘텐츠가 1:1 일치하는가
- [ ] HTML 인쇄 시 슬라이드별 페이지 분리가 정상 작동하는가
- [ ] **(v2.0) 다크 슬라이드가 전체 30% 이내인가** (가독성 보호)
- [ ] **(v2.0) 비주얼 패턴 SVP-1~SVP-7 중 행사 유형에 맞는 패턴이 선택되었는가**

---

## 표준 슬라이드 구조 (12~18 슬라이드)

| # | 섹션 | 슬라이드 | 6축 매핑 | v2.0 적용 패턴 |
|---|---|---|---|---|
| 1 | 표지 + 행사 한 줄 요약 | 1 | ① | DARK-COVER (`color_mode=dark_mixed`) 또는 라이트 표지 |
| 2 | Why This Event — 시장 맥락·행사 의의 | 2~3 | ① | (선택) SVP-7 2×2 매트릭스 |
| 3 | Who Attends — 청중 데이터 | 2~3 | ② | SVP-4 KPI · SVP-5 산업 분포 · SVP-6 퍼널 (선택) |
| 4 | What We Offer — 노출 자산 인벤토리 | 2~3 | ③ | 리스트 표 (라이트 우선) |
| 5 | Sponsor Tiers — 등급·가격·슬롯 | 1~2 | ④ | SVP-1 Tier 카드 |
| 6 | Benefits Matrix — Tier × 7카테고리 | 2~3 | ⑤ | SVP-2 매트릭스 |
| 7 | ROI Snapshot — 산업별 기대 효과 | 1~2 | ⑥ | SVP-3 ROI 3단 · DARK-ROI/DARK-KPI (color_mode=dark_mixed) |
| 8 | Past Sponsors / Reference Cases (조건부) | 0~2 | — | 로고 그리드 |
| 9 | Contact & Next Steps | 1 | ⑥ | DARK-COVER 톤 (color_mode=dark_mixed) |

상세 콘텐츠 가이드는 `references/slide-structure.md` 참조.

---

## 콘텐츠 작성 원칙

### 핵심 메시지 5원칙

1. **숫자로 말한다** — "많은 참가자" 금지, "예상 5,200명 / B2B 비율 87%" 사용
2. **노출량을 정량화한다** — "로고 노출"이 아니라 "메인 사이니지 8회 × 평균 노출 시간 2.5h"
3. **ROI를 산업별로 변환한다** — 같은 청중도 산업에 따라 다른 가치 제시. ROI는 항상 3단 구조(전제/공식/추정값)
4. **Tier 차별화는 명확하게** — 상위 Tier 혜택은 하위 Tier가 받지 못함을 매트릭스로 시각화
5. **CTA는 의사결정 단위로** — 견적·미팅·계약서 송부의 명확한 다음 단계

### 회사 종속 표현 배제

> 정본: `jc-design-system/references/shared-rules.md#RULE-NO-COMPANY` (금칙어·허용 표현·구현 예 전체 정의). 아래는 본 스킬 고유 적용 메모.

- 본 스킬은 "MICE 전문가" 또는 "행사 기획팀" 일반 용어만 사용
- 클라이언트·발주처·소속사 정보는 외부 주입 변수로만 처리
- "당사" 같은 자기 지칭 표현 금지 → "행사 기획팀" 또는 "본 행사 사무국"으로 대체

---

## 디자인 원칙

본 스킬은 디자인 토큰을 직접 정의하지 않는다. **`jc-design-system` 시그니처 토큰을 자동 매핑**한다.

- HTML/PPTX 모두 동일한 토큰 매핑 룰 사용 (`references/design-tokens-mapping.md`)
- 클라이언트 오버레이는 `jc-design-system/references/client-overlays.md` 룰 따름
- 시그니처 베이스는 어떤 경우에도 유지
- (v2.0) 비주얼 패턴 SVP-1~SVP-7 및 다크 5종 모두 시그니처 토큰 매핑 강제

---

## 파일 구조

```
mice-sponsor-deck/
├── SKILL.md                              # 본 파일 — 진입점
├── references/
│   ├── tier-framework.md                 # Tier 5단+1트랙 + 명칭 오버라이드 + 가격 모드
│   ├── audience-profile.md               # 청중 데이터 패턴 + 신규 행사 fallback
│   ├── benefit-catalog.md                # 7카테고리 × 표준 혜택 항목
│   ├── roi-case-templates.md             # 산업 5종 ROI 시나리오 + 3단 표현 룰
│   ├── design-tokens-mapping.md          # jc-design-system → HTML/PPTX 매핑
│   ├── slide-structure.md                # 표준 12~18 슬라이드 콘텐츠 구조 + 분기 룰
│   ├── output-build-guide.md             # HTML 1차 빌드 + PPTX 변환 워크플로우
│   ├── visual-patterns.md                # (v2.0 신규) 비주얼 패턴 7종 SVP-1~SVP-7
│   ├── dark-mode-patterns.md             # (v2.0 신규) 다크 5종 + 슬라이드별 컨텍스트
│   └── chaining-schema.md                # (v2.0 신규) mice-meeting-minutes → sponsor-deck 입력
├── assets/
│   ├── sponsor-deck-template-light.html  # (v2.0 신규) 라이트 베이스 HTML 템플릿
│   └── sponsor-deck-template-dark.html   # (v2.0 신규) 다크 베이스 HTML 템플릿 (토글 내장)
└── scripts/
    └── sample_generator.py               # (v2.0 신규) 가상 시나리오 콘텐츠 JSON 생성기
```

---

## 실행 순서 요약

```
1. 행사 자료 읽기 → 6축 정보 추출
   ├─ (v2.0 선택) mice-meeting-minutes 산출 sponsor-candidates.json 활용
2. 슬롯 수 미확정 시 사용자 경고 출력
3. 사용자에게 6축 분석 요약 제시 → 확인/보완
4. references/tier-framework.md 읽기 → Tier 구조 + 명칭·가격 모드 확정
5. references/audience-profile.md 읽기 → 청중 데이터 (또는 fallback)
6. references/benefit-catalog.md 읽기 → 매트릭스 작성
7. references/roi-case-templates.md 읽기 → ROI 3단 케이스 2종+ 작성
8. references/slide-structure.md 읽기 → 슬라이드 구성안 제시 → 사용자 확인
9. references/design-tokens-mapping.md 읽기 → 토큰 매핑
10. references/visual-patterns.md 읽기 → SVP 패턴 선택 적용
11. (color_mode=dark_mixed) references/dark-mode-patterns.md 읽기 → 다크 슬라이드 매핑
12. references/output-build-guide.md 읽기 → HTML 빌드 (assets/ 템플릿 베이스)
13. HTML 사용자 검토 → 확정
14. /mnt/skills/public/pptx/SKILL.md 읽기 → PPTX 변환
15. (옵션) /mnt/skills/public/xlsx/SKILL.md 읽기 → XLSX 매트릭스
16. QA 체크리스트 수행 → 최종 파일 전달
```

중요: Phase 1(정보 수집), Phase 2(6축 분석), Phase 7(HTML 빌드) 이후 반드시 사용자 승인을 받는다.
