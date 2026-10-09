# Chaining Schema (v2.2.0) — jc-pptx → pt-script

pt-script가 `jc-pptx` 덱을 받아 발표 대본을 만드는 체이닝 워크플로우와 입력 JSON 스키마다.

> **봉투 정본**: 공통 `ChainPayload/v1` 구조(`source`·`version`·`generatedAt` 등)와 스킬별 키 목록은 `jc-design-system/references/chaining-protocol.md`. jc-pptx 쪽 페이로드 정의는 `jc-pptx/references/proposal-playbook.md` §6. 이 문서는 pt-script가 **읽는 키**와 하위호환 입력만 정한다.

---

## 1. 워크플로우

```
jc-pptx (제안서·소개서·발표덱 빌드)
  ↓ deck.pptx  (+ ChainPayload/v1 JSON — presentation 키 포함)
pt-script
  ├ extract_notes.py  → notes-extraction.json (슬라이드·speaker notes·메타 노트 분류)
  ├ build_script.py --meta <payload.json>  → presentation 키에서 시간·톤·발표 주체 주입
  ↓
발표대본.docx (현장 사용 종착점)
```

---

## 2. 입력 형태

| 형태 | 내용 | 확인 질문 |
|------|------|----------|
| **A. PPTX 단독** | 덱 파일만 | 발표 시간만 묻는다(나머지는 기본값 — SKILL.md Phase 2) |
| **B. PPTX + ChainPayload (권장)** | 덱 + jc-pptx 봉투 JSON | `presentation.minutes`가 있으면 묻지 않고 진행 |
| **C. PPTX + 구 proposal-meta.json** | 하위호환 | 위와 같음 |

---

## 3. 읽는 키 — jc-pptx `ChainPayload/v1`

```json
{
  "$schema": "ChainPayload/v1",
  "source": "jc-pptx",
  "version": "<jc-pptx SKILL.md version>",
  "projectTitle": "[행사명] 운영 제안",
  "clientName": "{{client_company}}",
  "deck_meta": { "purpose": "proposal", "slides": 24 },
  "presentation": {
    "minutes": 15,
    "tone": "formal",
    "type": "bidding_pt",
    "presenter": "리멤버앤컴퍼니",
    "presenter_role": "발표자",
    "audience": "발주처 심사위원"
  }
}
```

| 키 | → build_script meta | 필수 | 비고 |
|----|--------------------|------|------|
| `presentation.minutes` | `presentation_minutes` | 권장 | 없으면 사용자에게 1회 확인 |
| `presentation.tone` | `tone` | — | `formal`(기본) · `semi_formal` · `casual` |
| `presentation.type` | `presentation_type` | — | 없고 `deck_meta.purpose == "proposal"`이면 `bidding_pt` |
| `presentation.presenter` | `presenter` | — | 발표 주체. 기본 `리멤버앤컴퍼니` |
| `presentation.presenter_role` | `presenter_role` | — | 기본 "발표자" |
| `presentation.audience` | `audience_type` | — | 기본 "심사위원" |
| `projectTitle` | `rfp_title` | — | 표지 제목 |
| `clientName` | `client_name` | — | 발주처 슬롯. 없으면 `[발주처명]` |

`source`가 구 `mice-proposal`인 봉투도 같은 규칙으로 읽는다(하위호환 별칭). CLI 인자(`--minutes`·`--presenter`)가 봉투 값보다 우선한다.

---

## 4. 하위호환 — 구 `proposal-meta.json`

```json
{
  "$schema": "pt-script/v2.0",
  "proposal_meta": {
    "client_name": "[발주처명]",
    "rfp_title": "[행사명] 운영 용역",
    "presentation_minutes": 20,
    "presentation_type": "bidding_pt",
    "presenter_role": "발표자",
    "presenter_name": null,
    "audience_type": "발주처 심사위원",
    "tone": "formal",
    "qna_included": true,
    "qna_minutes": 4
  },
  "extracted_from": "jc-pptx",
  "pptx_source": "deck.pptx"
}
```

- `proposal_meta` 컨테이너가 있으면 그대로 쓴다. `extracted_from`은 `jc-pptx`(또는 구 별칭)이며 검증용 정보일 뿐 빌드를 막지 않는다.
- 필드: `client_name` · `rfp_title` · `presentation_minutes`(≥1) · `presentation_type`(enum) · `presenter`(선택) · `presenter_role` · `presenter_name` · `audience_type` · `tone`(enum) · `qna_included` · `qna_minutes`(기본 = 시간×0.2).
- enum — `presentation_type`: `bidding_pt` | `conference` | `forum` | `corporate_event` | `mc` | `general_business` / `tone`: `formal` | `semi_formal` | `casual`.

---

## 5. 발표 유형 자동 추론 (PPTX 단독 입력)

```python
def infer_presentation_type(pptx_titles):
    titles = " ".join(pptx_titles).lower()
    if any(kw in titles for kw in ["제안", "비딩", "rfp", "수주", "proposal"]):
        return "bidding_pt"
    if any(kw in titles for kw in ["기조", "keynote", "포럼", "forum"]):
        return "forum"
    if any(kw in titles for kw in ["환영", "사회자", "mc", "프로그램 안내", "큐시트"]):
        return "mc"
    if any(kw in titles for kw in ["발표", "presentation", "session", "콘퍼런스"]):
        return "conference"
    return "general_business"
```

---

## 6. 다른 스킬과의 경계

| 스킬 | 관계 |
|------|------|
| `jc-pptx` | **업스트림** — 덱 + `presentation` 키 제공 |
| `mice-run-of-show` | 행사 큐시트·MC 진행 흐름. MC 대본의 순서 근거로 참고 가능 |
| `mice-rfp-analyzer` · `mice-estimate` · `mice-aftermath` | 무관 — 분석·견적·결과보고는 대본 입력이 아님 |
| `jc-design-system` | **참조 의존** — `references/jc-design-mapping.md`가 토큰 매핑 |
| `jc-redteam` | 비딩 PT 대본의 Q&A·논리 검수(선택) |

출력 `.docx`는 현장 사용 종착점이다. 다른 스킬의 입력으로 들어가지 않는다.

---

## 7. CLI 예시 (Windows 경로 표기)

```bash
python scripts/extract_notes.py "C:\work\deck.pptx" --out "C:\work\notes.json"

# B. jc-pptx 봉투와 함께
python scripts/build_script.py --notes "C:\work\notes.json" --meta "C:\work\deck-payload.json" --out "C:\work\발표대본.docx"

# A. 단독 — 기본값 + 시간만 지정
python scripts/build_script.py --notes "C:\work\notes.json" --minutes 20 --presentation-type bidding_pt --out "C:\work\발표대본.docx"

# 발표 주체 바꾸기
python scripts/build_script.py --notes "C:\work\notes.json" --minutes 15 --presenter "리멤버 MICE비즈팀" --out "C:\work\발표대본.docx"
```

---

## 8. 검증 체크리스트

- [ ] 덱이 python-pptx로 정상 파싱된다
- [ ] 발표 시간이 정해졌다(봉투·CLI·사용자 답 중 하나)
- [ ] `presentation_type`·`tone`이 유효 enum
- [ ] 산출물에 미치환 자리표시자(`[발표 주체]`·`[부서명]`) 0건 — `sanitize_text`가 발표 주체·부서로 채운다
- [ ] 전 직장 상호 0건 — 검출 시 build_script가 `[WARN] 전 직장 상호 유출 의심`을 낸다(치환하지 않고 사람이 고친다)
- [ ] `python scripts/build_script.py --self-test` PASS

---

## 9. 함께 보는 문서

| 파일 | 내용 |
|------|------|
| `references/script-guide.md` | 슬라이드 유형 8종별 멘트 패턴 |
| `references/jc-design-mapping.md` | docx 토큰 매핑 |
| `references/notes-extraction.md` | speaker notes 추출 + 메타 노트 필터링 |
| `jc-pptx/references/proposal-playbook.md` | 업스트림 봉투(§6) |
