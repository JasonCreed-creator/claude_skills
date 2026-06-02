# PPTX Speaker Notes 자동 추출 (v2.0)

본 문서는 pt-script v2.0 의 핵심 신규 기능 — PPTX 파일에서 슬라이드별 speaker notes·본문 텍스트·메타데이터를 자동 추출하여 발표 대본 베이스로 활용하는 워크플로우를 정의한다. mice-proposal v2.1.1 산출물과의 무결한 체이닝을 보장한다.

---

## 1. 추출 워크플로우

```
proposal.pptx (mice-proposal v2.1.1 산출물)
    ↓
extract_notes.py (python-pptx 기반)
    ↓
notes-extraction.json (슬라이드별 구조화 데이터)
    ↓
build_script.py 입력
    ↓
발표대본.docx
```

### 1-1. extract_notes.py 의 동작 순서

1. `python-pptx` 로 .pptx 파일 열기
2. 슬라이드 순회 (index 1부터)
3. 각 슬라이드에서 다음 추출:
   - **제목**: `slide.shapes.title.text` (있으면)
   - **본문 텍스트**: 모든 텍스트 도형의 텍스트 수집 (제목 제외)
   - **speaker notes**: `slide.notes_slide.notes_text_frame.text`
   - **도형/차트 메타데이터**: `slide.shapes` 순회 → has_chart / has_image / has_table 플래그
4. 노트 텍스트를 `notes_type` 으로 분류 (§4 필터링 패턴 적용)
5. JSON 출력

### 1-2. 출력 JSON 위치

기본: `/tmp/notes-extraction.json` 또는 `--out` 옵션 경로
- 권장 경로: `/mnt/user-data/outputs/notes-extraction.json` (사용자 다운로드용)
- 임시 경로: `/tmp/notes.json` (build_script.py 만 입력으로 사용 시)

---

## 2. mice-proposal v2.1.1 슬라이드 노트 표준

mice-proposal v2.1.1 은 PPTX 생성 시 슬라이드별로 다음 두 종류의 노트를 자동 삽입한다.

### 2-1. 메타 노트 (필터링 대상)

mice-proposal 의 `visual-patterns.md` §1-7 표준 텍스트:

```
■ 이미지 교체 안내 (회색 박스 모드)
회색 점선 박스로 표시된 영역에 실제 이미지를 삽입해주세요.
PowerPoint에서: 박스 클릭 → Delete → 동일 위치에 [삽입 → 사진]
캡션 텍스트도 함께 삭제하면 됩니다.

■ 폰트 안내
본 PPTX는 Pretendard·Inter 폰트를 사용합니다.
설치 없을 시 시스템 폰트로 자동 폴백됩니다.
권장 설치: https://github.com/orioncactus/pretendard
```

이런 메타 노트는 **이미지 교체·폰트 설치 안내**가 목적이지 발표 멘트가 아니다. pt-script는 이를 자동 필터링한다.

### 2-2. Speaker Notes (정상 발표 베이스)

기획자가 mice-proposal Phase 5 이후 수동 추가하거나, mice-proposal v2.1.1 의 메시지 추출 기능이 자동 생성한 노트. 예시:

```
이 슬라이드에서는 우리의 핵심 제안 3가지를 강조한다.
첫 번째는 운영 안정성으로, 작년 5,000명 규모 운영 경험을 부각.
두 번째는 디지털 확장으로, AI 기반 매칭 시스템을 데모로 보여줄 예정.
세 번째는 사후 관리로, 행사 후 3개월간 KPI 트래킹을 약속.
```

pt-script 는 이런 정상 노트를 **우선순위 1** 로 채택하여 발표 멘트 베이스로 활용한다.

---

## 3. 노트 → 스크립트 베이스 변환 룰

### 3-1. 우선순위 (3단)

| 우선순위 | 조건 | 변환 룰 |
|--------|------|--------|
| 1 (높음) | `notes_type == "speaker"` (정상 발표 노트 존재) | 그대로 발표 베이스로 활용. 톤 조정만 추가. |
| 2 (중) | `notes_type == "meta"` 또는 `notes == ""` 이고 본문 텍스트 존재 | 슬라이드 본문 + 제목 기반 자동 멘트 생성 (script-guide.md 패턴 적용) |
| 3 (낮음) | 본문 텍스트도 비어있고 제목만 존재 | 제목만으로 짧은 멘트 자동 생성 (표지·섹션 구분 슬라이드 등) |

### 3-2. 우선순위 1 — speaker notes 직접 활용

```python
# 노트 텍스트를 발표 톤으로 다듬기
def adapt_speaker_notes(notes_text, tone="formal"):
    """
    speaker notes는 보통 짧은 메모 형식.
    톤에 맞춰 완전한 발표 문장으로 다듬는다.
    """
    if tone == "formal":
        # "강조한다" → "강조하겠습니다"
        # "보여줄 예정" → "보여드리겠습니다"
        # ... LLM 호출 또는 규칙 기반 변환
        pass
    return adapted
```

### 3-3. 우선순위 2 — 본문 텍스트 기반 자동 생성

```python
def generate_from_body(title, body_text, slide_type, tone="formal"):
    """
    슬라이드 본문을 발표 멘트로 자동 변환.
    script-guide.md 의 슬라이드 유형 8종 패턴 적용.
    """
    if slide_type == "cover":
        return generate_cover_script(title, tone)
    elif slide_type == "agenda":
        return generate_agenda_script(body_text, tone)
    elif slide_type == "data_chart":
        return generate_data_chart_script(title, body_text, tone)
    # ... 기타
```

### 3-4. 우선순위 3 — 제목만 활용

```python
def generate_from_title_only(title, slide_type, tone="formal"):
    """
    제목만 있는 슬라이드 (표지·섹션 구분·감사 등).
    최소 멘트 생성.
    """
    if slide_type == "section_divider":
        return f"이어서 {title} 섹션으로 넘어가겠습니다."
    elif slide_type == "thanks":
        return "경청해 주셔서 감사합니다."
    return f"{title} 에 대해 말씀드리겠습니다."
```

---

## 4. 메타 노트 필터링 패턴

### 4-1. 검출 패턴 (정규식)

```python
import re

META_NOTE_PATTERNS = [
    r"^■\s*이미지\s*교체\s*안내",     # mice-proposal 이미지 안내
    r"^■\s*폰트\s*안내",              # mice-proposal 폰트 안내
    r"^■\s*PPTX\s*제작\s*안내",       # mice-proposal 일반 제작 안내
    r"^\[META\]",                      # 명시적 META 태그
    r"^TODO[:：]",                     # TODO 메모
    r"^FIXME[:：]",                    # FIXME 메모
]

def classify_notes(notes_text):
    """
    노트 텍스트를 speaker / meta / empty 로 분류.
    """
    if not notes_text or not notes_text.strip():
        return "empty"

    # 메타 패턴 매칭
    for pattern in META_NOTE_PATTERNS:
        if re.search(pattern, notes_text, re.MULTILINE):
            # 패턴이 노트 첫 줄에 있으면 메타로 분류
            return "meta"

    # 메타 + 발표 노트 혼합인 경우 — 메타 부분만 제거
    cleaned = remove_meta_blocks(notes_text)
    if cleaned.strip():
        return "speaker"  # 메타 제거 후 남은 텍스트가 있으면 speaker
    return "meta"

def remove_meta_blocks(notes_text):
    """
    노트 텍스트에서 메타 블록만 제거하고 발표 노트 부분 반환.
    메타 블록 = '■ ...' 로 시작하는 줄부터 다음 빈 줄 또는 다음 '■' 까지.
    """
    lines = notes_text.split("\n")
    out = []
    skip_block = False

    for line in lines:
        stripped = line.strip()
        if any(re.match(p, stripped) for p in META_NOTE_PATTERNS):
            skip_block = True
            continue
        if skip_block and stripped == "":
            skip_block = False
            continue
        if not skip_block:
            out.append(line)

    return "\n".join(out).strip()
```

### 4-2. 혼합 노트 처리

mice-proposal v2.1.1 표준은 메타 노트만 자동 삽입한다. 그러나 기획자가 같은 노트 영역에 발표 멘트를 추가로 적은 경우 (혼합 노트), §4-1 `remove_meta_blocks` 함수가 메타 블록만 제거하고 발표 부분을 보존한다.

예시 입력:
```
■ 이미지 교체 안내
회색 점선 박스로 표시된 영역에...

이 슬라이드에서는 우리의 핵심 제안 3가지를 강조한다.
첫 번째는 운영 안정성...
```

`remove_meta_blocks` 결과:
```
이 슬라이드에서는 우리의 핵심 제안 3가지를 강조한다.
첫 번째는 운영 안정성...
```

분류: `notes_type = "speaker"`

---

## 5. extract_notes.py CLI 사용 예시

### 5-1. 기본 사용

```bash
python scripts/extract_notes.py /mnt/user-data/uploads/proposal.pptx \
  --out /tmp/notes-extraction.json
```

### 5-2. 상세 모드 (디버그)

```bash
python scripts/extract_notes.py proposal.pptx --out notes.json --verbose
```

verbose 모드는 다음을 추가 출력:
- 슬라이드별 텍스트 도형 개수
- 메타 노트 필터링 적용 여부
- 차트·이미지·표 검출 결과

### 5-3. Python 임포트 사용

```python
from extract_notes import extract_pptx_notes

result = extract_pptx_notes("proposal.pptx")
print(f"Total slides: {result['slide_count']}")
for slide in result["slides"]:
    print(f"  [{slide['index']}] {slide['title']} — notes_type={slide['notes_type']}")
```

---

## 6. 출력 JSON 스키마

### 6-1. 표준 스키마

```json
{
  "source_pptx": "proposal.pptx",
  "extracted_at": "2026-05-27T11:45:00",
  "slide_count": 9,
  "slides": [
    {
      "index": 1,
      "title": "TOBESOFT TECH FORUM 2026 운영 제안",
      "body_text": "AI·Cloud·Enterprise Tech의 다음 10년 | 2026.09.15 | 코엑스",
      "notes": "",
      "notes_type": "empty",
      "has_chart": false,
      "has_image": true,
      "has_table": false,
      "slide_type_hint": "cover"
    },
    {
      "index": 2,
      "title": "목차",
      "body_text": "1. 행사 이해\n2. 핵심 전략\n3. 실행 방안\n4. 일정·예산\n5. 차별점·실적",
      "notes": "",
      "notes_type": "empty",
      "has_chart": false,
      "has_image": false,
      "has_table": false,
      "slide_type_hint": "agenda"
    },
    {
      "index": 5,
      "title": "핵심 전략",
      "body_text": "운영 안정성 + 디지털 확장 + 사후 관리",
      "notes": "이 슬라이드에서는 우리의 핵심 제안 3가지를 강조한다. 첫 번째는 운영 안정성으로, 작년 5,000명 규모 운영 경험을 부각. 두 번째는 디지털 확장으로, AI 기반 매칭 시스템을 데모로 보여줄 예정. 세 번째는 사후 관리로, 행사 후 3개월간 KPI 트래킹을 약속.",
      "notes_type": "speaker",
      "has_chart": false,
      "has_image": false,
      "has_table": false,
      "slide_type_hint": "core_proposal"
    }
  ]
}
```

### 6-2. 필드 정의

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `source_pptx` | string | ✅ | 원본 파일명 |
| `extracted_at` | ISO 8601 string | ✅ | 추출 시각 |
| `slide_count` | number | ✅ | 전체 슬라이드 수 |
| `slides[]` | array | ✅ | 슬라이드별 데이터 배열 |
| `slides[].index` | number | ✅ | 슬라이드 번호 (1부터) |
| `slides[].title` | string | ✅ | 슬라이드 제목 (없으면 "") |
| `slides[].body_text` | string | ✅ | 본문 텍스트 (제목 제외, 줄바꿈 유지) |
| `slides[].notes` | string | ✅ | 메타 노트 필터링 후 남은 텍스트 |
| `slides[].notes_type` | enum | ✅ | `speaker` \| `meta` \| `empty` |
| `slides[].has_chart` | boolean | ✅ | 차트 존재 여부 |
| `slides[].has_image` | boolean | ✅ | 이미지 존재 여부 |
| `slides[].has_table` | boolean | ✅ | 표 존재 여부 |
| `slides[].slide_type_hint` | string | optional | 자동 추론 슬라이드 유형 (`cover`/`agenda`/`section_divider`/`background`/`core_proposal`/`data_chart`/`process_timeline`/`reference_case`/`thanks`/`generic`) |

### 6-3. slide_type_hint 자동 추론 룰

```python
def infer_slide_type(index, title, body_text, has_chart, total_slides):
    """슬라이드 유형 자동 추론."""
    # 위치 기반
    if index == 1:
        return "cover"
    if index == total_slides:
        return "thanks"

    # 제목 기반
    title_lower = (title or "").lower()
    if any(kw in title_lower for kw in ["목차", "agenda", "contents", "차례"]):
        return "agenda"
    if any(kw in title_lower for kw in ["감사", "thank", "마무리"]):
        return "thanks"
    if any(kw in title_lower for kw in ["배경", "현황", "이해", "분석"]):
        return "background"
    if any(kw in title_lower for kw in ["전략", "제안", "솔루션", "어프로치"]):
        return "core_proposal"
    if any(kw in title_lower for kw in ["일정", "타임라인", "프로세스", "단계"]):
        return "process_timeline"
    if any(kw in title_lower for kw in ["실적", "사례", "레퍼런스", "포트폴리오"]):
        return "reference_case"

    # 차트 존재 시
    if has_chart:
        return "data_chart"

    return "generic"
```

---

## 7. 에러 처리

| 에러 케이스 | 처리 방식 |
|----------|---------|
| 입력 파일 없음 | `FileNotFoundError` → exit code 2 + stderr 메시지 |
| 입력이 .pptx 가 아님 | `ValueError` → exit code 3 |
| PPTX 손상 | python-pptx `PackageNotFoundError` → exit code 4 |
| 빈 PPTX (슬라이드 0개) | warning + `slide_count: 0`, exit code 0 |
| 노트 추출 실패 | 해당 슬라이드 `notes: ""` + `notes_type: "empty"` + warning |
| UTF-8 인코딩 오류 | `sys.stdout.reconfigure(encoding='utf-8')` 로 회피 |

---

## 8. 함께 보는 문서

| 파일 | 내용 |
|------|------|
| `script-guide.md` | 슬라이드 유형 8종별 멘트 패턴 (notes_type=speaker/empty 변환 시 활용) |
| `jc-design-mapping.md` | docx 디자인 토큰 매핑 |
| `chaining-schema.md` | mice-proposal → pt-script 입력 JSON 스키마 |
| `../scripts/extract_notes.py` | 본 문서의 구현체 |
