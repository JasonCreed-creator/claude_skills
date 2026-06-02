# JC Design System → docx 디자인 토큰 매핑 (v2.0)

본 문서는 pt-script v2.0 가 생성하는 .docx 발표 대본의 색상·폰트·사이즈·간격을 jc-design-system 시그니처 토큰과 1:1 매핑하는 룰을 정의한다. python-docx 기반 `build_script.py` 가 본 매핑을 자동 적용한다.

---

## 1. 의존성

- **선행**: `jc-design-system/references/signature-tokens.md` 가 정의하는 시그니처 컬러·폰트·사이즈 스케일을 본 매핑이 그대로 따른다.
- **호환**: mice-proposal v2.1.1 `visual-patterns.md` §0-2 (컬러) / §0-3 (폰트) / §0-4 (사이즈) 와 동일 토큰을 docx 컨텍스트에 적용.
- **로드 순서**: pt-script Phase 4 시작 시 본 매핑 → python-docx 스타일 객체 생성.

---

## 2. 컬러 매핑 룰

### 2-1. 문서 영역별 토큰 매핑 표

> **컬러 값은 jc-design-system `signature-tokens.md` §6 JSON 정본을 따른다.** 아래 표는 docx 영역 → SoT 토큰명 매핑만 정의하며, HEX 리터럴을 본 문서에 중복 기재하지 않는다. (docx는 CSS 변수를 못 쓰므로 실제 빌드 시 `build_script.py` 가 SoT 정본값을 RGBColor 리터럴로 미러링한다 — 해당 상수의 `SoT 미러` 주석 참조.)

| docx 영역 | SoT 토큰 (값=signature-tokens.md §6 JSON) | 적용 방식 |
|----------|------------------------------------------|---------|
| 표지 배경 | `--jc-primary` | Section Header Shading (paragraph_format.shading 또는 Run highlight) |
| 표지 제목 텍스트 | `--jc-surface` | 흰색 폰트 (Deep Navy 배경 위) |
| 메인 본문 텍스트 | `--jc-text` | Run.font.color.rgb |
| Heading2 슬라이드 번호+제목 | `--jc-accent` | 헤딩 컬러 |
| "발표 멘트" 레이블 | `--jc-accent-strong` | Bold + 색상 |
| 발표 팁 (Italic) | `--jc-text-muted` | 이탤릭 + 회색 |
| 시간 배분표 헤더 배경 | `--jc-primary` | 셀 음영 (cell shading) |
| 시간 배분표 헤더 텍스트 | `--jc-surface` | 흰색 |
| 시간 배분표 짝수 행 배경 | `--jc-surface-alt` | 줄무늬 |
| 시간 배분표 홀수 행 배경 | `--jc-surface` | 기본 |
| 표 보더 | `--jc-border` | 1pt 솔리드 |
| Q&A 질문 | `--jc-text` (Bold) | Bold |
| Q&A 답변 핵심 키워드 | `--jc-success` | 강조 색상 (선택적) |
| 시간 초과 알림 | `--jc-warning` | 경고 음영 (시간 배분 ±10% 초과 시) |
| 일반 보더 강조 | `--jc-border-strong` | 표지·섹션 구분선 |

### 2-2. 시맨틱 컬러

> 값은 jc-design-system `signature-tokens.md` §1.5 / §6 JSON `semantic` 정본 참조.

| 토큰 | docx 용도 |
|------|---------|
| `--jc-success` | Q&A 답변 강조, 발표 체크리스트 ✓ |
| `--jc-warning` | 시간 초과 알림, ±10% 오차 경고 |
| `--jc-danger` | 회사 종속 표현 검출 시 경고 (제거 권고) |
| `--jc-info` | 일반 메모·노트 |

### 2-3. python-docx 적용 코드 예시

docx는 CSS 변수를 못 쓰므로 RGBColor 리터럴은 "매체 불가피"로 남되, 값은 jc-design-system `signature-tokens.md` §6 JSON 라이트 정본과 일치시킨다 (`SoT 미러` 주석).

```python
from docx.shared import RGBColor

# 토큰 상수 — 값은 jc-design-system signature-tokens.md §6 JSON 정본 미러
JC_PRIMARY = RGBColor(0x0A, 0x25, 0x40)        # SoT 미러: --jc-primary (#0A2540)
JC_ACCENT = RGBColor(0x29, 0x62, 0xFF)         # SoT 미러: --jc-accent (#2962FF)
JC_ACCENT_STRONG = RGBColor(0x1E, 0x4D, 0xCC)  # SoT 미러: --jc-accent-strong (#1E4DCC)
JC_TEXT = RGBColor(0x1A, 0x1D, 0x24)           # SoT 미러: --jc-text (#1A1D24)
JC_TEXT_MUTED = RGBColor(0x5A, 0x62, 0x70)     # SoT 미러: --jc-text-muted (#5A6270)
JC_SURFACE = RGBColor(0xFF, 0xFF, 0xFF)        # SoT 미러: --jc-surface (#FFFFFF)
JC_SURFACE_ALT = RGBColor(0xF1, 0xF3, 0xF7)    # SoT 미러: --jc-surface-alt (#F1F3F7)
JC_BORDER = RGBColor(0xE5, 0xE8, 0xED)         # SoT 미러: --jc-border (#E5E8ED)
JC_BORDER_STRONG = RGBColor(0xC9, 0xCF, 0xD8)  # SoT 미러: --jc-border-strong (#C9CFD8)
JC_SUCCESS = RGBColor(0x00, 0xC8, 0x53)        # SoT 미러: --jc-success (#00C853)
JC_WARNING = RGBColor(0xFF, 0xA0, 0x00)        # SoT 미러: --jc-warning (#FFA000)

# 사용 예
heading2.runs[0].font.color.rgb = JC_ACCENT
mute_run.font.color.rgb = JC_TEXT_MUTED
mute_run.italic = True
```

### 2-4. 셀 음영 (Cell Shading) 적용

python-docx 는 셀 음영을 직접 API로 제공하지 않으므로 OXML 직접 조작.

```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_cell_shading(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)  # 6자리 hex 문자열 형식 (예: --jc-primary = "0A2540", SoT 미러)
    tc_pr.append(shd)
```

---

## 3. 타이포그래피 매핑

### 3-1. 폰트 패밀리

| 토큰 | 1순위 | 폴백 | docx 용도 |
|------|-------|------|---------|
| `--jc-font-ko` | Pretendard | 맑은 고딕 (Win), Apple SD Gothic Neo (Mac) | 한글 본문·제목 |
| `--jc-font-en` | Inter | Helvetica Neue, Arial | 영문 본문 |
| `--jc-font-mono` | JetBrains Mono | D2Coding, Consolas | 숫자·코드 |
| `--jc-font-heading` | Pretendard | 동일 | 모든 헤딩 |

### 3-2. python-docx 폰트 설정

```python
from docx.oxml.ns import qn

def set_run_font(run, font_name="Pretendard"):
    """한글·영문 모두 동일 폰트 적용 (CJK 폴백 포함)."""
    run.font.name = font_name
    # 한글 처리를 위한 EastAsia 폰트 명시
    r_pr = run._element.get_or_add_rPr()
    r_fonts = r_pr.find(qn('w:rFonts'))
    if r_fonts is None:
        r_fonts = OxmlElement('w:rFonts')
        r_pr.append(r_fonts)
    r_fonts.set(qn('w:eastAsia'), font_name)
    r_fonts.set(qn('w:ascii'), font_name)
    r_fonts.set(qn('w:hAnsi'), font_name)
```

### 3-3. 사이즈 매핑 (jc-design-system 스케일 → docx pt)

| JC 스케일 토큰 | docx pt | 용도 |
|-------------|--------|------|
| `--jc-size-xs` (SIZE_XS = 9) | 9pt | 캡션·각주 |
| `--jc-size-sm` (SIZE_SM = 11) | 11pt | 발표 팁·시간 배분표 본문 |
| `--jc-size-base` (SIZE_BASE = 14) | 14pt | 본문 멘트 (기본) |
| `--jc-size-lg` (SIZE_LG = 16) | 16pt | 강조 본문 |
| `--jc-size-xl` (SIZE_XL = 20) | 20pt | Heading2 슬라이드 번호+제목 |
| `--jc-size-2xl` (SIZE_2XL = 24) | 24pt | Heading1 섹션 (발표 개요·Q&A 등) |
| `--jc-size-3xl` (SIZE_3XL = 32) | 32pt | 표지 보조 |
| `--jc-size-4xl` (SIZE_4XL = 40) | 28pt (docx 축소) | 문서 제목 (표지) |

**참고**: docx는 PPTX 표지처럼 56pt~40pt 큰 폰트를 거의 안 쓴다. 표지 제목은 28pt로 축소 매핑.

### 3-4. python-docx 사이즈 설정

```python
from docx.shared import Pt

run.font.size = Pt(14)  # 본문
run.font.size = Pt(20)  # Heading2
run.font.size = Pt(28)  # 표지 제목
```

---

## 4. 간격·스타일

### 4-1. 행간

| 영역 | 행간 | python-docx |
|------|------|-----------|
| 본문 멘트 | 1.5 | `paragraph.paragraph_format.line_spacing = 1.5` |
| 발표 팁 | 1.3 | `1.3` |
| 표지 제목 | 1.0 | `1.0` |
| 시간 배분표 셀 | 1.2 | `1.2` |

### 4-2. 단락 간격

| 영역 | 단락 후 | python-docx |
|------|--------|-----------|
| 슬라이드 카드 사이 | 18pt | `paragraph_format.space_after = Pt(18)` |
| 섹션 간 | 24pt | `Pt(24)` |
| 본문 단락 간 | 6pt | `Pt(6)` |

### 4-3. 슬라이드별 카드 구분

옵션 A: 페이지 단위 분리 — 슬라이드마다 페이지 브레이크
```python
from docx.enum.text import WD_BREAK
run.add_break(WD_BREAK.PAGE)
```

옵션 B (기본): 섹션 브레이크 없이 단락 간격 + 보더 박스
```python
# 슬라이드 카드 박스 (paragraph border)
```

### 4-4. 셀 패딩 (시간 배분표)

```python
# python-docx 표 셀 마진 (단위: dxa, 1pt = 20 dxa)
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement('w:tcMar')
    for side, value in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{side}')
        node.set(qn('w:w'), str(value))
        node.set(qn('w:type'), 'dxa')
        tc_mar.append(node)
    tc_pr.append(tc_mar)
```

---

## 5. 발표 유형별 톤 컬러 분기 (선택)

`build_script.py --presentation-type` 옵션에 따라 표지·헤딩의 강조 컬러를 토글한다.

| presentation_type | 표지 배경 | Heading2 강조 | 메인 강조 룰 |
|-------------------|---------|-------------|---------|
| `bidding_pt` (비딩 PT) | `--jc-primary` (0A2540) | `--jc-accent` (2962FF) | 신뢰·차별화 강조 |
| `conference` (컨퍼런스) | `--jc-primary` (0A2540) | `--jc-primary-soft` (1A3556) | 차분·전문성 |
| `forum` (포럼) | `--jc-primary` (0A2540) | `--jc-primary-soft` (1A3556) | 비전 제시 |
| `corporate_event` (기업행사) | `--jc-primary` (0A2540) | `--jc-point-orange` (FF5722) | 활기·참여 |
| `mc` (MC/사회자) | `--jc-point-orange-softest` (FFF3E0, SoT 미러) | `--jc-point-orange` (FF5722) | 활기·환영 |
| `general_business` (일반 비즈) | `--jc-primary` (0A2540) | `--jc-accent` (2962FF) | 명확·간결 |

**기본값**: `bidding_pt` (mice-proposal 출력 연동 시 가장 흔한 케이스)

---

## 6. 클라이언트 오버레이

`client_id` 외부 주입 시 표지·헤딩 컬러만 오버라이드한다. 본문·표 등 나머지는 JC 시그니처 유지.

```python
# 클라이언트 오버레이 예시
CLIENT_OVERLAYS = {
    "darktrace_korea": {
        "cover_bg": JC_PRIMARY,        # JC 유지
        "heading_accent": RGBColor(0xE9, 0x1E, 0x63),  # Magenta 오버레이
    },
    # 추가 클라이언트는 jc-design-system/client-overlays.md 참조
}

def apply_client_overlay(client_id):
    if client_id and client_id in CLIENT_OVERLAYS:
        return CLIENT_OVERLAYS[client_id]
    return {"cover_bg": JC_PRIMARY, "heading_accent": JC_ACCENT}
```

`client_id` 가 null 또는 미정의 값이면 JC 시그니처 기본 모드로 폴백.

---

## 7. JSON 스키마 (빠른 참조)

`build_script.py` 가 내부에서 사용하는 매핑 객체. docx는 CSS 변수를 못 쓰므로 아래 HEX 리터럴은 "매체 불가피"이며, **모든 값은 jc-design-system `signature-tokens.md` §6 JSON 라이트 정본의 미러**다(권위 값은 SoT 단일 정본 참조). `cover_bg`=`--jc-primary`, `cover_text`/`table_header_text`/`table_row_odd`=`--jc-surface`, `body_text`=`--jc-text`, `heading2`=`--jc-accent`, `label_mention`=`--jc-accent-strong`, `tip_text`=`--jc-text-muted`, `table_row_even`=`--jc-surface-alt`, `table_border`=`--jc-border`, `qna_answer_keyword`=`--jc-success`, `time_overrun_warning`=`--jc-warning`, `mc.cover_bg`=`--jc-point-orange-softest`.

```json
{
  "color_mapping": {
    "cover_bg": "0A2540",
    "cover_text": "FFFFFF",
    "body_text": "1A1D24",
    "heading2": "2962FF",
    "label_mention": "1E4DCC",
    "tip_text": "5A6270",
    "table_header_bg": "0A2540",
    "table_header_text": "FFFFFF",
    "table_row_even": "F1F3F7",
    "table_row_odd": "FFFFFF",
    "table_border": "E5E8ED",
    "qna_answer_keyword": "00C853",
    "time_overrun_warning": "FFA000"
  },
  "font_mapping": {
    "ko": "Pretendard",
    "ko_fallback": "맑은 고딕",
    "en": "Inter",
    "mono": "JetBrains Mono",
    "heading": "Pretendard"
  },
  "size_mapping": {
    "caption": 9,
    "tip": 11,
    "body": 14,
    "body_strong": 16,
    "heading2": 20,
    "heading1": 24,
    "title": 28
  },
  "spacing_mapping": {
    "line_body": 1.5,
    "line_tip": 1.3,
    "line_title": 1.0,
    "line_table": 1.2,
    "para_after_slide_card": 18,
    "para_after_section": 24,
    "para_after_body": 6
  },
  "presentation_type_overrides": {
    "bidding_pt": { "heading_accent": "2962FF" },
    "conference": { "heading_accent": "1A3556" },
    "forum": { "heading_accent": "1A3556" },
    "corporate_event": { "heading_accent": "FF5722" },
    "mc": { "heading_accent": "FF5722", "cover_bg": "FFF3E0" },
    "general_business": { "heading_accent": "2962FF" }
  }
}
```

---

## 8. 검증 룰 (디자인 일관성)

본 매핑 적용 docx의 자가검증 체크리스트:

> 대비비 수치는 jc-design-system `mode-mapping.md` §9(WebAIM 표준) 정본을 따른다. 아래 값은 SoT §9.5 미러이며 근사값을 임의 채택하지 않는다.

- [ ] 모든 HEX 컬러가 본 문서 §2-1 표(=SoT 토큰) 에 존재 (외부 컬러 사용 금지)
- [ ] 표지 배경 + 텍스트 콘트라스트 WCAG AA 이상 (White FFFFFF on Deep Navy 0A2540 = 14.04:1 AAA ✅, SoT §9.5)
- [ ] Heading2 강조 콘트라스트 WCAG AA 이상 (White FFFFFF on Electric Blue 2962FF = 4.79:1 AA ✅, SoT §9.5)
- [ ] 본문 텍스트 + 배경 콘트라스트 (Charcoal 1A1D24 on White FFFFFF = 16.30:1 AAA ✅, SoT §9.5)
- [ ] 발표 팁 + 배경 콘트라스트 (Muted 5A6270 on White FFFFFF = 6.34:1 AA ✅, SoT §9.5)
- [ ] 시간 배분표 헤더 + 텍스트 (White on Deep Navy 0A2540 = 14.04:1 AAA ✅, SoT §9.5)
- [ ] 한글 폰트 EastAsia 속성 명시 (CJK 폴백 보장)
- [ ] 본문 사이즈 14pt 이상 (가독성)
- [ ] 사이즈 스케일이 jc-design-system §0-4 와 1:1 매칭

---

## 9. 함께 보는 문서

| 파일 | 내용 |
|------|------|
| `script-guide.md` | 슬라이드 유형 8종별 멘트 패턴, 전환 멘트, Q&A 구조 |
| `notes-extraction.md` | PPTX speaker notes 추출 + 메타 노트 필터링 |
| `chaining-schema.md` | mice-proposal → pt-script 입력 JSON 스키마 |
| jc-design-system/references/signature-tokens.md | 본 매핑의 베이스 토큰 |
