---
name: pt-script
description: "프레젠테이션 스크립트(대본)를 자동 생성하는 스킬. PPTX를 받으면 슬라이드 내용과 speaker notes를 분석해 슬라이드별 발표 멘트, 예상 소요시간, 전환 멘트, Q&A 예상 질의응답, 발표 체크리스트가 담긴 Word 문서(.docx)를 리멤버 웜 페이퍼 룩으로 만든다. jc-pptx 덱의 체이닝 봉투(presentation 키)를 읽어 발표 시간·톤·발표 주체를 자동으로 채운다. 발표 주체 기본값은 리멤버앤컴퍼니. 다음 상황에서 반드시 이 스킬을 사용할 것 — 사용자가 '스크립트', '대본', '발표 멘트', '발표문', 'PT 대본', '발표 원고', '스피치 원고', '발표 준비', '프레젠테이션 스크립트', '멘트 작성'을 언급할 때, PPTX를 올리며 대본 작성을 요청할 때, 행사 MC 멘트·진행 대본·사회자 스크립트를 요청할 때, 발표 연습용 원고를 요청할 때. 비딩 PT·컨퍼런스·포럼·기업행사와 일반 비즈니스 발표 모두 지원. 형제 경계 — 덱 자체를 만들거나 고치는 것은 jc-pptx(상류), 행사 큐시트·운영 진행표는 mice-run-of-show, 대본·제안 논리의 적대 검증은 jc-redteam, 디자인 토큰은 jc-design-system 영역이므로 그 작업에는 사용하지 말 것."
version: "v2.2.0"
dependencies: python-pptx, python-docx
---

# 프레젠테이션 스크립트(대본) 자동 생성 스킬

## 개요

PPTX의 슬라이드 내용과 speaker notes를 분석해 슬라이드별 발표 대본을 Word 문서(.docx)로 만든다. MICE 비딩 PT, 컨퍼런스 발표, 포럼 기조연설, 기업행사 진행 대본, MC 멘트에 대응한다.

- 기본 업스트림은 `jc-pptx` 덱이다. 덱과 함께 오는 `ChainPayload/v1` 봉투의 **`presentation` 키**(시간·톤·유형·발표 주체·청중)를 읽어 확인 질문 없이 채운다.
- docx 룩은 **리멤버 웜 페이퍼**(`jc-design-system` v2 토큰 런타임 로드). 인쇄물이라 라이트 고정.
- 발표 주체 기본값은 **리멤버앤컴퍼니**(부서 표기 = 마이스 비즈 팀). `--presenter`로 바꾼다.

---

## 워크플로우 (기본값 진행 → 빌드 → 검수)

되돌릴 수 있는 작업(분석·초안·docx 생성)은 합리적 기본값으로 바로 진행하고, 고른 기본값을 한 줄로 밝힌다. 단계마다 확인받지 않는다.

### Phase 1: PPTX 분석

```bash
python scripts/extract_notes.py "C:\work\deck.pptx" --out "C:\work\notes.json"
```

산출 JSON: 전체 슬라이드 수, 슬라이드별 제목·본문·speaker notes·차트/이미지/표 유무, `notes_type`(`speaker`/`meta`/`empty`). 메타 노트(■ 이미지 교체 안내 / ■ 폰트 안내 등)는 발표 베이스에서 제외한다(`references/notes-extraction.md`).

분석: 섹션 구분(표지·목차·본문·마무리), 슬라이드 유형(표지 / 목차 / 배경·현황 / 핵심제안 / 데이터차트 / 프로세스 / 실적레퍼런스 / 마무리), 전체 스토리라인.

멘트 우선순위: ① speaker notes → ② 슬라이드 본문 → ③ 제목만.

### Phase 2: 발표 조건 — 기본값으로 채우고 한 줄로 밝힌다

| 항목 | 출처 우선순위 | 기본값 |
|------|-------------|--------|
| 전체 발표 시간 | CLI → 봉투 `presentation.minutes` → 사용자 | **없으면 이것만 1회 묻는다** |
| 발표 유형 | 봉투 `presentation.type` → 덱 목적(`proposal`→비딩 PT) → 제목 키워드 추론 | `bidding_pt` |
| 톤 | 봉투 `presentation.tone` | 격식체(`formal`) |
| 발표 주체 | `--presenter` → 봉투 `presentation.presenter` | 리멤버앤컴퍼니 |
| 발표자 역할 | 봉투 `presentation.presenter_role` | "발표자" |
| 청중 | 봉투 `presentation.audience` | 발주처 심사위원 |
| Q&A | — | 포함, 전체 시간의 20% |

예: "15분 비딩 PT · 격식체 · 발표 주체 리멤버앤컴퍼니 · Q&A 3분으로 작성합니다(바꿀 항목만 말씀 주세요)."

### Phase 3: 스크립트 생성

`references/script-guide.md` 를 반드시 읽고 스크립트를 구성한다.

#### 시간 배분 로직

전체 발표 시간에서 Q&A 시간을 제외한 순수 발표 시간을 슬라이드에 배분한다.

```
순수 발표 시간 = 전체 시간 - Q&A 시간
슬라이드당 평균 시간 = 순수 발표 시간 / 슬라이드 수
```

슬라이드 유형별 가중치:
- **표지/목차/감사 슬라이드**: 0.3배 (간단히 넘기는 슬라이드)
- **핵심 내용 슬라이드**: 1.5배 (데이터, 전략, 핵심 제안)
- **일반 내용 슬라이드**: 1.0배 (기본 설명)
- **시각 중심 슬라이드**: 0.7배 (이미지, 영상, 도식 위주)

#### 멘트 분량 기준

1분당 약 250자(한국어 기준)를 기본으로 산출한다.

| 슬라이드 배정 시간 | 멘트 분량 |
|-------------------|-----------|
| 30초 | 약 125자 (2~3문장) |
| 1분 | 약 250자 (4~5문장) |
| 1분 30초 | 약 375자 (6~8문장) |
| 2분 | 약 500자 (8~10문장) |
| 3분 | 약 750자 (12~15문장) |

### Phase 4: Word 문서 생성

```bash
python scripts/build_script.py --notes "C:\work\notes.json" --meta "C:\work\deck-payload.json" --out "C:\work\발표대본.docx"
# 봉투 없이: --minutes 20 --presentation-type bidding_pt --tone formal [--presenter "리멤버 MICE비즈팀"]
```

`--meta`는 jc-pptx `ChainPayload/v1`(`presentation` 키)과 구 `proposal-meta.json`(`proposal_meta` 컨테이너)을 모두 받는다 — `references/chaining-schema.md`.

#### 문서 구조

```
[표지]           제목(28pt, 웜 서피스 배경) · 발표 대상 · 발표 주체 · 발표자 · 시간 · 일자 · 발주처
[발표 개요]      시간 배분표 (슬라이드 | 제목 | 배정 시간 | 누적 시간) — 헤더 차콜 + 흰 글자, 짝수 행 웜 서피스
[슬라이드별]     슬라이드 N: 제목(20pt 오렌지) · 배정 시간 · 내용 요약 · 【발표 멘트】(accent-deep) · 발표 팁(뮤트 이탤릭)
[Q&A]           질문(Bold) · 예상 답변(PREP) — 5~10개
[체크리스트]     발표 전 / 중 / 후
```

#### 디자인 매핑 (요약 — 상세 `references/jc-design-mapping.md`)

| 요소 | 토큰 (`signature-tokens.md` §6) |
|------|------|
| 표지 배경 | `surfaceAlt`(MC·기업행사는 `accentSoft`) + 잉크 텍스트 |
| 섹션 제목·본문 | `text` (잉크) |
| 슬라이드 제목 | `accent`(20pt 큰 글자 전용) · 컨퍼런스·포럼은 `text` |
| "발표 멘트" 레이블·체크리스트 분류 | `accentStrong`(accent-deep, 작은 오렌지 글자) |
| 팁·메타 | `textMuted` |
| 시간 배분표 헤더 / 짝수 행 | `primarySoft`(차콜) + 흰 글자 / `surfaceAlt` |
| 예상 답변 레이블 | `semantic.success` |
| 시간 초과 알림 | `semantic.warningBg` 배경 |

서체 Pretendard(한·영 동시 지정, 없으면 맑은 고딕). 구 네이비 시그니처는 쓰지 않는다(`legacy-jc` 오버레이는 명시 요청 시 jc-design-system에서). 발주처 컬러는 받지 않고 발주처명·행사명 텍스트만 넣는다.

### Phase 5: 검수 및 전달

1. 멘트 글자 수 합산 → 예상 소요시간(250자/분), 지정 시간 대비 ±10% 확인. 초과 시 문서 끝에 경고 단락.
2. build_script 출력의 `former_company_leaks`가 비어 있는지 확인 — 전 직장 상호가 보이면 해당 문장을 고친다(자동 치환하지 않음).
3. docx 무결성(python-docx로 다시 열림).
4. 비딩 PT는 필요 시 `jc-redteam` Quick Strike로 Q&A·논리 검수.
5. 작업 폴더에 저장해 전달(외부 발송은 사용자가 결정).

---

## 콘텐츠 작성 원칙

### 멘트 작성 규칙

1. **자연스러운 구어체**: 문어체가 아닌, 실제 말하는 듯한 자연스러운 문장
2. **슬라이드 내용 반복 금지**: 슬라이드에 적힌 텍스트를 그대로 읽지 않고, 보충 설명·맥락·스토리를 제공
3. **핵심 메시지 먼저**: 각 슬라이드에서 가장 중요한 포인트를 먼저 언급
4. **구체적 수치 활용**: 슬라이드의 데이터를 멘트에서 해석하고 의미를 부여
5. **청중 시선 유도**: "화면을 보시면~", "여기서 주목할 점은~" 등 시각 자료 연결
6. **전환 자연스럽게**: 슬라이드 간 논리적 연결 ("이어서~", "그렇다면~", "이를 바탕으로~")

### Q&A 작성 규칙

1. 프레젠테이션 내용에서 논쟁적이거나 추가 설명이 필요한 부분 중심
2. 청중 특성에 맞는 질문 수준 설정
3. 답변은 간결하되 핵심 근거 포함 (PREP 구조: Point → Reason → Example → Point)
4. 비딩 PT의 경우 심사위원 관점의 날카로운 질문 포함
5. 기본 5개, 핵심 내용이 많으면 최대 10개

### 발표 주체 표기 (RULE-NO-COMPANY v2)

- 발표 주체 기본값 **리멤버앤컴퍼니**, 부서 표기 **마이스 비즈 팀**. 구 양식 자리표시자 `[발표 주체]`·`[부서명]`은 `sanitize_text()`가 이 값(또는 `--presenter`)으로 채운다.
- 전 직장 상호·전 부서명은 산출물에 쓰지 않는다. 치환하지 않고 **유출 경고**(`[WARN] 전 직장 상호 유출 의심`)만 낸다 — 사람이 문장을 고친다.
- 발주처·담당자는 주입 슬롯(`client_name` 등). 비딩 PT에서 발주처가 주체 표기를 제한하면 "당사"·"본 PCO"로 일반화한다.
- 정본: `jc-design-system/references/shared-rules.md#RULE-NO-COMPANY`.

---

## 실행 순서 요약

```
1. extract_notes.py 로 PPTX 분석 → notes.json
2. 봉투(presentation 키)·CLI·기본값으로 발표 조건 확정 — 시간이 없을 때만 1회 질문, 고른 기본값 한 줄 명시
3. references/script-guide.md 읽고 시간 배분 + 슬라이드별 멘트 + Q&A(PREP) 작성
4. build_script.py 로 docx 생성 (리멤버 토큰 자동 적용)
5. 검수 (±10% 시간 · 유출 경고 0 · docx 유효성) → 전달
```

## 생태계 연결

- 상류: `jc-pptx`(덱 + `ChainPayload/v1` `presentation` 키) — 봉투 정본 `jc-design-system/references/chaining-protocol.md`
- 디자인: `jc-design-system` v2 토큰 런타임 로드
- 검증: `jc-redteam`(선택 — 비딩 PT Q&A·논리)
- 행사 진행 순서 참고: `mice-run-of-show`(MC 대본)

## 함께 보는 문서

| 파일 | 내용 |
|------|------|
| `references/script-guide.md` | 슬라이드 유형 8종별 멘트 패턴, 전환 멘트, Q&A 답변 구조, 발표 팁 |
| `references/jc-design-mapping.md` | docx 토큰 매핑 (리멤버 웜 페이퍼) |
| `references/notes-extraction.md` | speaker notes 추출 + 메타 노트 필터링 |
| `references/chaining-schema.md` | jc-pptx → pt-script 입력 스키마 (`presentation` 키) |
| `scripts/extract_notes.py` | python-pptx 기반 노트·텍스트 추출 |
| `scripts/build_script.py` | python-docx 기반 대본 빌드 · `--self-test` |

## 변경 이력

- v2.2.0 (2026-10-05): 디자인 매핑을 구 네이비 → 리멤버 웜 페이퍼 토큰(§6 런타임 로드, 폴백 출처 주석)으로 재작성. jc-pptx 체이닝 봉투 `presentation` 키 읽기, `--presenter` 인자·전 직장 상호 유출 경고·`--self-test` 추가.
  상류를 폐합 mice-proposal → jc-pptx로, Phase 2 확인 → 기본값 진행(시간만 질문), 브리프 게이트 문구·샌드박스 경로 삭제. v2.1.0의 발표 주체(리멤버앤컴퍼니) 수정은 유지.
- v2.1.0 (2026-10-01): 전 직장 명칭 치환 규칙(`sanitize_text`) 삭제 → 리멤버앤컴퍼니를 기본 발표 주체로.
- v2.0 (2026-05-27): 디자인 토큰 연동, PPTX speaker notes 자동 추출(extract_notes.py), python-docx build_script.py, 체이닝 스키마, 메타 노트 필터링.
- v1.0 (2026-04): 초기 릴리스.
