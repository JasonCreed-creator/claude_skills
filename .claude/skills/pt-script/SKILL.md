---
name: pt-script
description: "프레젠테이션 스크립트(대본)를 자동 생성하는 스킬. PPTX 파일을 업로드하면 슬라이드 내용을 분석하여 슬라이드별 발표 멘트, 예상 소요시간, 전환 멘트, Q&A 예상 질의응답이 포함된 Word 문서(.docx)를 생성한다. 다음 상황에서 반드시 이 스킬을 사용할 것: 사용자가 '스크립트', '대본', '발표 멘트', '발표문', 'PT 대본', '발표 원고', '스피치 원고', '발표 준비', '프레젠테이션 스크립트', '멘트 작성' 등을 언급할 때, PPTX를 업로드하며 대본 작성을 요청할 때, 행사 MC 멘트·진행 대본·사회자 스크립트를 요청할 때, 또는 발표 연습용 원고를 요청할 때. MICE 행사(비딩 PT, 컨퍼런스, 포럼, 기업행사) 및 일반 비즈니스 프레젠테이션 모두 지원한다."
version: "v2.0.0"
---

# 프레젠테이션 스크립트(대본) 자동 생성 스킬

## 개요

업로드된 PPTX 파일의 슬라이드 내용을 분석하여, 슬라이드별 발표 대본을 Word 문서(.docx)로 자동 생성한다. MICE 비딩 PT, 컨퍼런스 발표, 포럼 기조연설, 기업행사 진행 대본 등 다양한 발표 유형에 대응한다.

v2.0부터는 jc-design-system 디자인 토큰을 docx 출력에 매핑하고, mice-proposal v2.1.1 산출물(PPTX)에서 speaker notes를 자동 추출하여 발표 베이스로 활용하는 체이닝 워크플로우를 정식 지원한다.

---

## 버전 히스토리

| 버전 | 일자 | 주요 변경 |
|------|------|---------|
| v1.0 | 2026-04 | 초기 릴리스. PPTX 분석 → docx 발표 대본 생성 워크플로우 5 Phase 확립 |
| v2.0 | 2026-05-27 | (1) jc-design-system 디자인 토큰 연동 (docx 헤더·강조·표 스타일). (2) mice-proposal v2.1.1 PPTX speaker notes 자동 추출 (extract_notes.py). (3) python-docx 기반 build_script.py 도입. (4) mice-proposal → pt-script 체이닝 JSON 스키마 명시. (5) 메타 노트 필터링 룰 추가. |

---

## 디자인 시스템 연동

본 스킬은 docx 산출물에 **jc-design-system 시그니처 토큰**을 매핑한다. HEX 컬러·폰트·사이즈·간격이 다른 7개 스킬과 일관된 룰을 따른다.

- 상세 매핑 룰: `references/jc-design-mapping.md`
- 의존성: `jc-design-system/references/signature-tokens.md` 로드 후 본 매핑 적용
- 핵심 매핑 요약:
  - 표지 배경 → `--jc-primary` (0A2540) — Section Header Shading
  - Heading2 슬라이드 번호+제목 → `--jc-accent` (2962FF)
  - "발표 멘트" 레이블 → `--jc-accent` Strong
  - 발표 팁 → `--jc-text-muted` (5A6270) Italic
  - 시간 배분표 헤더 → `--jc-primary` 배경 + 흰색 텍스트
  - 시간 배분표 짝수 행 → `--jc-surface-alt` (F1F3F7)
  - 시간 초과 알림 → `--jc-warning` (FFA000)
  - Q&A 답변 강조 → `--jc-success` (00C853)
- 폰트: 한글 Pretendard (없으면 맑은 고딕 폴백), 영문 Inter, 숫자 JetBrains Mono
- 클라이언트 오버레이: `client_id` 외부 주입 시 표지·헤딩 컬러 토글

---

## mice-proposal 출력 연동

mice-proposal v2.1.1 가 생성한 PPTX의 슬라이드별 speaker notes 를 자동 추출하여 발표 스크립트 베이스로 활용한다. 사용자가 동일 PPTX 파일 하나만 업로드해도 자동 체이닝이 동작한다.

- 상세 추출 룰: `references/notes-extraction.md`
- 추출 스크립트: `scripts/extract_notes.py`
- 메타 노트 필터링: mice-proposal v2.1.1 가 자동 삽입하는 "■ 이미지 교체 안내" / "■ 폰트 안내" 노트는 메타로 분류하여 발표 베이스에서 제외
- 우선순위 룰:
  1. speaker notes 있음 → 그대로 발표 베이스로 활용
  2. speaker notes 없음 → 슬라이드 본문 텍스트 기반 자동 생성
  3. 슬라이드 본문도 비어있음 → 제목만으로 자동 생성

---

## 체이닝

본 스킬은 mice-proposal 의 다운스트림이다. 풀 워크플로우는 다음과 같다.

```
mice-proposal (RFP 기반 PPTX 생성)
  ↓ proposal.pptx (+ proposal-meta.json 선택)
pt-script (본 스킬)
  ↓ extract_notes.py
notes-extraction.json
  ↓ build_script.py
발표대본.docx
```

- 상세 입력 스키마: `references/chaining-schema.md`
- 입력 형태:
  - **A 단독 PPTX 입력** — `proposal.pptx` 만 업로드. 본 스킬이 모든 정보 추출.
  - **B PPTX + 메타 JSON 페어** — `proposal.pptx` + `proposal-meta.json`. mice-proposal 산출 시 메타 JSON을 함께 제공하면 발표 시간·발표자 역할·청중 등 컨텍스트가 자동 주입됨.
- 본 스킬의 출력 .docx 는 **현장 사용 종착점**. 다른 스킬의 입력으로 들어가지 않는다.

---

## 워크플로우

### Phase 1: PPTX 분석

업로드된 PPTX 파일에서 슬라이드 내용과 speaker notes를 추출한다.

```bash
# 권장 (v2.0) — python-pptx 기반 추출 스크립트
python scripts/extract_notes.py /mnt/user-data/uploads/[파일명].pptx --out /tmp/notes.json

# 보조 (v1 호환) — 텍스트 추출
python -m markitdown /mnt/user-data/uploads/[파일명].pptx
```

`extract_notes.py` 산출 JSON에는 다음 정보가 담긴다:

- 전체 슬라이드 수
- 슬라이드별 제목·본문 텍스트·speaker notes·차트/이미지 유무
- notes_type 분류 (`speaker` / `meta` / `empty`)

추출 후 다음을 분석한다:
- 섹션 구분 (표지·목차·본문·마무리)
- 각 슬라이드 유형 (표지 / 목차 / 배경·현황 / 핵심제안 / 데이터차트 / 프로세스 / 실적레퍼런스 / 마무리)
- 프레젠테이션 전체 맥락과 스토리라인

### Phase 2: 사용자 확인

분석 결과를 요약하여 사용자에게 제시하고, 아래 항목을 확인받는다. `proposal-meta.json` 입력 시 해당 항목은 자동 채워진다.

| 확인 항목 | 설명 | 기본값 |
|-----------|------|--------|
| 발표 유형 | 비딩 PT / 컨퍼런스 발표 / 포럼 / 기업행사 / MC 진행 / 일반 비즈니스 | 자동 추론 |
| 발표자 역할 | 실장, 대표이사, PM, MC/사회자 등 | "발표자" (회사 종속 표현 금지) |
| 청중 대상 | 발주처 심사위원, 업계 전문가, 일반 참가자, 임직원 등 | 자동 추론 |
| 전체 발표 시간 | 분 단위 (예: 20분, 30분, 45분) | 사용자 입력 필수 |
| 톤 & 매너 | 격식체 / 반격식체 / 캐주얼 | 격식체 |
| Q&A 포함 여부 | 예상 질의응답 생성 여부 | 포함 |
| Q&A 시간 | 분 단위 | 전체 시간의 20% |
| client_id (선택) | 클라이언트 오버레이 컬러 적용 시 | null (JC 시그니처 기본) |

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

`scripts/build_script.py` (python-docx 기반)로 docx 문서를 생성한다.

```bash
python scripts/build_script.py \
  --notes /tmp/notes.json \
  --meta /tmp/proposal-meta.json \   # 선택
  --minutes 20 \
  --tone formal \
  --presentation-type bidding_pt \
  --out /mnt/user-data/outputs/발표대본.docx
```

빌드 스크립트는 `references/jc-design-mapping.md` 의 컬러·폰트·사이즈 매핑을 자동 적용한다.

#### 문서 구조

```
[표지 페이지]
  프레젠테이션 제목 (28pt, --jc-primary 배경 강조)
  발표자 / 발표일 / 발표 시간 / 대상

[발표 개요]
  전체 시간 배분표 (표 형식)
  - 슬라이드 번호 | 제목 | 배정 시간 | 누적 시간
  - 헤더: --jc-primary 배경 + 흰색
  - 짝수 행: --jc-surface-alt

[슬라이드별 스크립트]
  각 슬라이드마다:
  ┌─────────────────────────────┐
  │ 슬라이드 N: [제목] (--jc-accent) │
  │ 배정 시간: X분 Y초            │
  ├─────────────────────────────┤
  │ [슬라이드 내용 요약]          │
  │ (슬라이드에 있는 핵심 텍스트)  │
  ├─────────────────────────────┤
  │ 【발표 멘트】 (--jc-accent Strong) │
  │ (실제 발표할 대본 내용)       │
  ├─────────────────────────────┤
  │ 💡 발표 팁 (--jc-text-muted Italic) │
  │ (강조 포인트, 제스처, 시선 등) │
  └─────────────────────────────┘

[Q&A 예상 질의응답]
  질문 1: ... (Bold)
  예상 답변: ... (--jc-success 강조)
  (5~10개)

[발표 체크리스트]
  발표 전 / 발표 중 / 발표 후 체크항목
```

#### docx 스타일 가이드

| 요소 | 스타일 | 토큰 매핑 |
|------|--------|---------|
| 문서 제목 | Heading1, 28pt, Bold | `--jc-primary` 배경 + 흰색 |
| 슬라이드 번호+제목 | Heading2, 20pt, Bold | `--jc-accent` (2962FF) |
| "발표 멘트" 레이블 | Bold, 강조 | `--jc-accent` Strong (1E4DCC) |
| 멘트 본문 | 본문 14pt, 행간 1.5 | `--jc-text` (1A1D24) |
| 발표 팁 | 이탤릭, 회색 | `--jc-text-muted` (5A6270) |
| Q&A 질문 | Bold | `--jc-text` |
| Q&A 답변 | 일반 본문 | `--jc-text` (핵심 키워드 `--jc-success`) |
| 시간 배분표 헤더 | 음영 | `--jc-primary` (0A2540) + 흰색 |
| 시간 배분표 짝수 행 | 음영 | `--jc-surface-alt` (F1F3F7) |
| 시간 초과 알림 | 강조 | `--jc-warning` (FFA000) |

### Phase 5: QA 및 전달

1. 전체 멘트 글자 수 합산 → 예상 총 소요시간 계산 (250자/분)
2. 사용자 지정 발표 시간과의 오차 확인 (±10% 이내 목표). 초과 시 표지·시간 배분표에 `--jc-warning` 강조 표시
3. python-docx 산출물 무결성 검증 (XML 파싱 가능, 페이지 수 1 이상)
4. 최종 파일을 `/mnt/user-data/outputs/` 에 저장하여 전달

---

## 발표 유형별 톤 가이드

| 유형 | 톤 | 특징 | 강조 컬러 (선택) |
|------|-----|------|-----------------|
| **비딩 PT** | 격식체, 자신감 | "~하겠습니다", "~드리겠습니다". 차별화 포인트 강조, 실적 기반 신뢰 구축 | `--jc-accent` 메인 |
| **컨퍼런스 발표** | 반격식체, 전문적 | "~합니다", "~입니다". 데이터·사례 중심, 인사이트 전달 | `--jc-primary` 차분 |
| **포럼/기조연설** | 격식체, 비전 제시 | "~하고자 합니다". 큰 그림 먼저, 구체적 내용 후행 | `--jc-primary` 차분 |
| **기업행사 진행** | 반격식체, 활기 | "~하시겠습니다", "~주시기 바랍니다". 참가자 행동 유도 | `--jc-point-orange` |
| **MC/사회자** | 반격식체~캐주얼 | 환영인사, 프로그램 안내, 연사 소개, 전환 멘트 중심 | `--jc-point-orange` |
| **일반 비즈니스** | 반격식체 | "~합니다". 명확하고 간결한 전달 | `--jc-accent` 메인 |

발표 유형별 톤 컬러 분기 상세는 `references/jc-design-mapping.md` §5 참조.

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

### 회사 종속 표현 금지 (자산 정의 원칙)

본 스킬은 개인 자산이다. 회사 종속 표현은 산출물에 절대 포함하지 않는다.

> 정본: `jc-design-system/references/shared-rules.md#RULE-NO-COMPANY`. 코드 레벨 구현은 `scripts/build_script.py` 의 `sanitize_text()` (정본 문서의 '구현 예'). 아래는 본 스킬 고유 적용 메모.

- "엠앤씨", "M&C커뮤니케이션즈", "리멤버앤컴퍼니", "신사업실", 실명 등 0건
- 회사명·발표자 직함은 **외부 주입 변수**로 처리 (사용자가 Phase 2 에서 직접 입력)
- 기본 표기는 일반화된 표현 사용: "본 PCO", "당사", "발표자" 등

---

## 실행 순서 요약

```
1. extract_notes.py 로 PPTX 분석 → notes-extraction.json
2. (선택) proposal-meta.json 로드 → 발표 컨텍스트 자동 주입
3. Phase 2 사용자 확인 (발표 유형, 시간, 톤 등) — 메타 JSON 입력 시 생략 가능
4. references/script-guide.md + jc-design-mapping.md 읽기
5. 시간 배분 계산 (슬라이드 유형 가중치 적용)
6. 슬라이드별 멘트 작성 (speaker notes 우선순위 → 본문 → 제목 폴백)
7. Q&A 예상 질의응답 작성 (PREP 구조)
8. build_script.py 로 docx 생성 (jc-design 토큰 자동 적용)
9. QA 수행 (글자 수 검증 + ±10% 오차 확인 + 문서 유효성)
10. 최종 .docx 파일 전달
```

중요: Phase 2(사용자 확인) 이후에 본격 작성에 들어간다. 발표 시간은 반드시 사용자에게 확인받는다. 단, `proposal-meta.json` 입력 시 `presentation_minutes` 값을 우선 적용한다.

---

## 함께 보는 문서

| 파일 | 내용 |
|------|------|
| `references/script-guide.md` | 슬라이드 유형 8종별 멘트 패턴, 전환 멘트, Q&A 답변 구조, 발표 팁 |
| `references/jc-design-mapping.md` | docx 디자인 토큰 매핑 (컬러·폰트·사이즈·간격) |
| `references/notes-extraction.md` | PPTX speaker notes 자동 추출 + 메타 노트 필터링 룰 |
| `references/chaining-schema.md` | mice-proposal → pt-script 입력 JSON 스키마 |
| `scripts/extract_notes.py` | python-pptx 기반 노트·텍스트 추출 |
| `scripts/build_script.py` | python-docx 기반 발표 대본 빌드 |
