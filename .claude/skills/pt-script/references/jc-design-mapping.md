# 디자인 토큰 → docx 매핑 (v2.2.0 — 리멤버 웜 페이퍼)

pt-script가 만드는 .docx 발표 대본의 색·서체·사이즈·간격을 `jc-design-system` v2(리멤버 웜 페이퍼) 토큰에 매핑하는 규칙이다. `scripts/build_script.py`가 이 매핑을 자동 적용한다.

---

## 1. 의존성 · 로드

- **정본**: `jc-design-system/references/signature-tokens.md` §6 JSON. 이 문서는 *어느 docx 영역에 어느 토큰을 쓰는지*만 정하고 값을 다시 정의하지 않는다.
- **런타임 로드**: `build_script.py`가 형제 경로 → `~/.claude/skills/jc-design-system` → `~/.claude/skills/synced/*/jc-design-system` 순으로 §6 JSON을 찾아 읽는다. 못 찾을 때만 §6 값을 옮겨 둔 폴백 상수를 쓴다(상수마다 출처 주석).
- **구 룩**: 구 네이비·일렉트릭블루 jc 시그니처는 쓰지 않는다. 필요하면 사용자가 명시 요청할 때만 `jc-design-system`의 `legacy-jc` 오버레이로 처리한다.
- **공통 룰**: `RULE-WCAG`(본문 4.5:1↑, 오렌지 글자는 큰 글자 전용)·`RULE-PRINT-LIGHT`(인쇄물은 라이트). 정본 `jc-design-system/references/shared-rules.md`.

---

## 2. 컬러 매핑

### 2-1. 문서 영역 → §6 토큰

| docx 영역 | §6 토큰 (`color.*`) | build_script 상수 | 비고 |
|----------|-------------------|------------------|------|
| 표지 제목 단락 배경 | `surfaceAlt` (유형별 `accentSoft`) | `RM_SURFACE_ALT` / `RM_ACCENT_SOFT` | 인쇄 라이트 — 다크 표지 없음 |
| 표지 제목 텍스트 | `text` | `RM_INK` | 28pt Bold |
| 섹션 제목(발표 개요·스크립트·Q&A·체크리스트) | `text` | `RM_INK` | 24pt Bold |
| 슬라이드 번호+제목 | `accent` (유형별 `text`) | `RM_ACCENT` | 20pt Bold — 큰 글자라 오렌지 허용 |
| "【발표 멘트】" 레이블 | `accentStrong` (accent-deep) | `RM_ACCENT_DEEP` | 14pt — 작은 오렌지 글자는 deep |
| 체크리스트 분류 제목 | `accentStrong` | `RM_ACCENT_DEEP` | 14pt Bold |
| 멘트·Q&A 본문 | `text` | `RM_INK` | 14pt |
| 발표 팁·배정 시간·표지 메타 | `textMuted` | `RM_MUTED` | Italic(팁·시간) |
| 시간 배분표 헤더 배경 / 텍스트 | `primarySoft` / `surface` | `RM_CHARCOAL` / `RM_SURFACE` | 차콜 위 흰 글자 |
| 시간 배분표 짝수 행 | `surfaceAlt` | `RM_SURFACE_ALT` | 웜 줄무늬 |
| "예상 답변:" 레이블 | `semantic.success` | `RM_SUCCESS` | 12pt Bold |
| 시간 초과 알림 단락 배경 | `semantic.warningBg` | `RM_WARNING_BG` | 잉크 텍스트 |
| 보조 포인트(선택) | `point.steel` | `RM_STEEL` | 데이터 캡션 등 |

### 2-2. 사용 규칙

- 오렌지(`accent`)는 18pt 이상 또는 14pt Bold 이상 큰 글자에만. 그보다 작은 강조는 `accentStrong`(accent-deep).
- 덱에서 넘어온 발주처 컬러는 받지 않는다. 발주처는 텍스트 슬롯(발주처명·행사명)으로만 들어간다.
- 테마 토큰 외 색 금지. 새 색이 필요하면 `jc-design-system`에 먼저 추가한다.

### 2-3. 셀 음영 (OXML)

python-docx는 셀 음영 API가 없어 OXML을 직접 조작한다(`build_script.py` `set_cell_shading`). `w:fill`에는 `#` 없는 6자리 HEX를 넣는다.

---

## 3. 타이포그래피

| 용도 | 서체 | 폴백 |
|------|------|------|
| 한글·영문 본문·제목 | Pretendard (latin·eastAsia 동시 지정) | 맑은 고딕(Win) · Apple SD Gothic Neo(Mac) |
| 숫자·코드(선택) | JetBrains Mono | Consolas |

| 영역 | pt |
|------|----|
| 표지 제목 | 28 |
| 섹션 제목 | 24 |
| 슬라이드 제목 | 20 |
| 멘트·Q&A 본문 | 14 |
| 레이블 | 12~14 |
| 팁·표 본문·메타 | 11~12 |

문서 스케일 정본은 `signature-tokens.md` §2. docx는 덱보다 작은 스케일을 쓴다.

---

## 4. 간격

| 영역 | 행간 | 단락 후 |
|------|------|--------|
| 멘트 본문 | 1.5 | 10pt |
| 발표 팁 | 1.3 | 18pt |
| 체크리스트 | 1.4 | — |
| 섹션 제목 | 1.0 | 18pt |

---

## 5. 발표 유형별 강조 분기

`--presentation-type`(또는 메타 `presentation.type`)에 따라 표지 배경과 슬라이드 제목 색만 바뀐다. 본문·표는 공통.

| presentation_type | 표지 배경 | 슬라이드 제목 | 의도 |
|-------------------|----------|-------------|------|
| `bidding_pt` (기본) | `surfaceAlt` | `accent` | 신뢰·차별화 |
| `conference` | `surfaceAlt` | `text` | 차분·전문성 |
| `forum` | `surfaceAlt` | `text` | 비전 제시 |
| `corporate_event` | `accentSoft` | `accent` | 활기·참여 |
| `mc` | `accentSoft` | `accent` | 환영·진행 |
| `general_business` | `surfaceAlt` | `accent` | 명확·간결 |

---

## 6. 발주처 표기

발주처 컬러 오버레이는 쓰지 않는다. 발주처 로고·표지 이미지 같은 슬롯 규칙은 `jc-design-system/references/client-overlays.md §1`을 따르고, docx에는 발주처명·행사명 텍스트만 넣는다. `--client-id`는 하위호환용으로 받기만 하고 색을 바꾸지 않는다.

---

## 7. 검증 체크리스트

대비 수치는 WCAG 2.1 공식으로 계산한 값이다(정본 `jc-design-system/references/mode-mapping.md`).

- [ ] 모든 색이 §2-1 표의 토큰에서 왔다(외부 색 0)
- [ ] 본문 잉크 `1A1A1A` on 흰 배경 = 17.4:1 (AAA)
- [ ] 표지 잉크 on `surfaceAlt` `F4F1EA` = 15.4:1 / on `accentSoft` `FFF1E6` = 15.7:1
- [ ] 슬라이드 제목 오렌지 `EB6F2A` on 흰 배경 = 3.07:1 — 20pt Bold 큰 글자 기준(3:1)만 충족하므로 작은 글자에 쓰지 않는다
- [ ] 작은 오렌지 `B8431A` on 흰 배경 = 5.45:1 (AA)
- [ ] 팁 `6E6E6E` on 흰 배경 = 5.1:1 (AA)
- [ ] 표 헤더 흰 글자 on `332F29` = 13.3:1 (AAA)
- [ ] 한글 EastAsia 서체 속성 지정
- [ ] 본문 14pt 이상

---

## 8. 함께 보는 문서

| 파일 | 내용 |
|------|------|
| `references/script-guide.md` | 슬라이드 유형 8종별 멘트 패턴, 전환 멘트, Q&A 구조 |
| `references/notes-extraction.md` | PPTX speaker notes 추출 + 메타 노트 필터링 |
| `references/chaining-schema.md` | jc-pptx → pt-script 입력 스키마 (`presentation` 키) |
| `jc-design-system/references/signature-tokens.md` | 토큰 정본 (§6 JSON) |
