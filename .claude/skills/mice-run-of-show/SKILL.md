---
name: mice-run-of-show
version: "v1.0.0"
description: MICE 행사 운영 큐시트(run of show)와 진행 시나리오를 버전드 XLSX로 생성하는 스킬. Cue#·시간·세그먼트·무대/발표·Audio·Video·Light·연출 cue·Owner·비고 10컬럼 그리드 + 변경이력 시트로, 쇼콜러가 리허설·본행사에서 바로 쓰는 운영 문서를 만든다. 다음 상황에서 반드시 이 스킬을 사용할 것 사용자가 '큐시트', '런오브쇼', 'run of show', 'run-of-show', '진행표', '진행 순서표', '진행 시나리오', '연출 큐시트', '행사 진행 큐', '쇼콜', 'show calling', 'AV 큐시트', '타임테이블 운영표', '큐 시트 만들어줘'를 언급할 때. 행사 프로그램·세그먼트별 시간·연출/AV/조명 cue·담당자를 운영 문서로 정리해달라고 요청할 때. mice-proposal·pt-script의 산출(프로그램·발표 시간)을 체이닝 입력으로 받아 큐시트를 자동 구성할 수 있다. 단 '발표 대본·MC 멘트 원고'는 pt-script, '회의록'은 mice-meeting-minutes, '행사 결과 KPI 대시보드'는 mice-dashboard, '제안서'는 mice-proposal 영역이므로 사용하지 말 것. 공급자·발주처·담당자 등 식별 정보는 외부 주입 변수로 처리한다.
dependencies:
  - openpyxl
---

# mice-run-of-show — 행사 운영 큐시트 생성

행사 당일의 분 단위 운영 큐시트(run of show / production cue sheet)와 진행 시나리오를 **버전 관리되는 XLSX**로 생성한다. 쇼콜러·무대감독·AV/조명 오퍼레이터가 리허설과 본행사에서 그대로 보고 콜하는 현장 문서다.

## 1. 본 스킬이 다루는 것 / 다루지 않는 것

### 다루는 것 (DO)
- 세그먼트별 분 단위 큐시트 (10컬럼 그리드, `references/cuesheet-columns.md`)
- 연출·AV·조명 cue의 **표준 표기**(`references/cue-notation.md`) — 쇼콜러 즉시 판독
- 소요시간 자동 검증(세그먼트 합 = 총 행사시간) + 클록 자동 산출
- **변경 버전 관리** — 버전 넘버 + 변경이력 시트(개정 누적)
- 진행 시나리오(deep 모드 — 큐별 연출 의도·예비 cue·리스크)

### 다루지 않는 것 (DON'T)
- 발표 대본·MC 멘트 **원고** → **pt-script** (큐시트는 "언제 무엇을", 대본은 "무슨 말을")
- 회의록·Action Items → **mice-meeting-minutes**
- 행사 결과 KPI·실적 시각화 → **mice-dashboard**
- 제안서·견적·스폰서 데크 → mice-proposal / mice-estimate / mice-sponsor-deck

> **pt-script와의 경계**: pt-script는 발표자가 *할 말*(원고·Q&A)을 쓴다. 본 스킬은 행사 전체의 *진행 순서·연출 콜*(누가·언제·어떤 cue)을 만든다. 둘은 체이닝된다 — pt-script의 세그먼트 시간을 큐시트가 흡수한다(§7).

## 2. 호출 시점 판단 가이드

| 사용자 입력 | 본 스킬 | 사용 스킬 |
|------------|:------:|----------|
| "이 행사 큐시트 만들어줘" | ✅ | mice-run-of-show |
| "런오브쇼 / 진행 순서표 짜줘" | ✅ | mice-run-of-show |
| "AV·조명 cue까지 넣은 진행표" | ✅ | mice-run-of-show |
| "발표 대본 / MC 멘트 써줘" | ❌ | pt-script |
| "회의 내용 정리해줘" | ❌ | mice-meeting-minutes |
| "행사 끝났는데 결과 대시보드" | ❌ | mice-dashboard |

## 3. 핵심 작동 원칙

1. **시간 무결성 우선** — 큐시트의 생명은 시간이 맞는 것. 세그먼트 소요시간 합이 총 행사시간과 어긋나면 빌드가 경고한다(`build_runsheet.py` 자동 검증).
2. **클록 자동 산출** — 시작 시각 + 누적 소요로 각 cue의 클록(HH:MM)을 자동 계산한다. 수기 클록 입력 오류를 차단한다.
3. **표준 표기 강제** — 연출/AV/조명 cue는 자유 서술이 아니라 표준 약어(`LX`/`SQ`/`VT`/`MIC`…)로. 쇼콜러가 현장에서 즉시 판독해야 한다.
4. **버전 불변** — 큐시트는 리허설마다 바뀐다. 모든 산출은 버전 넘버를 달고, 변경이력 시트에 개정을 누적한다.
5. **식별정보 외부 주입** — 행사명·베뉴·담당자·발주처는 모두 사용자가 매번 주입(RULE-NO-COMPANY).

## 4. 워크플로우

### Step 1: 입력 방식 판별

| 방식 | 트리거 | 동작 |
|------|--------|------|
| **A. 대화 입력** | 사용자가 프로그램·세그먼트·시간을 직접 제공 | cues 리스트 구성 → 빌드 |
| **B. 체이닝 입력** | `ChainPayload`(source=mice-proposal/pt-script) JSON | 프로그램·발표 시간 자동 흡수 → 큐 스켈레톤 (`references/chaining-schema.md`) |
| **C. 개정** | 기존 큐시트 + 변경사항 | 버전 +1, 변경이력 누적 |

### Step 2: 필수 정보 수집

| 항목 | 설명 | 필수 |
|------|------|------|
| 행사명 (title) | 시트·파일명 (외부 주입) | ✅ |
| 일자 (date) | 행사일 | ✅ |
| 베뉴 (venue) | 장소 (외부 주입) | ✅ |
| 시작 시각 (start_time) | "09:00" | ✅ |
| 세그먼트 리스트 | 각: 세그먼트명·소요(분)·무대/발표·A/V/L·연출cue·Owner·비고 | ✅ |
| 총 행사시간 (end_time/총분) | 무결성 검증 기준 | 권장 |
| client_id | jc-design 오버레이 (없으면 시그니처) | 선택 |

### Step 3: 레퍼런스 로드 (빌드 전 필수)

| 작업 | 읽을 reference |
|------|---------------|
| 컬럼 작성 규약 | `references/cuesheet-columns.md` |
| 연출/AV/조명 표기 | `references/cue-notation.md` |
| 체이닝 입력 처리 | `references/chaining-schema.md` |
| 색상 토큰 | `references/jc-design-mapping.md` |

### Step 4: 빌드

```python
import sys; sys.path.insert(0, '/path/to/skill/scripts')
from build_runsheet import build_runsheet

event = {
    'title': '(외부 주입 - 행사명)', 'date': '2026-06-20',
    'venue': '(외부 주입 - 베뉴)', 'start_time': '09:00',
    'end_time': '12:30',           # 무결성 검증 기준 (선택)
    'version': 1, 'client_id': None,
}
cues = [
    # segment, duration_min, stage, audio, video, light, cue, owner, note
    {'segment': '등록·입장', 'duration_min': 30, 'stage': '-', 'audio': 'BGM',
     'video': '로비 루프', 'light': '하우스', 'cue': 'LX:하우스 100%', 'owner': '운영', 'note': '정시 개문'},
    # ...
]
out = build_runsheet(event, cues, '/home/claude/런오브쇼_행사명_v1_YYMMDD.xlsx')
```

### Step 5: 검증 + 출력

- 빌드가 **소요시간 합 = 총 행사시간** 자동 검증(불일치 시 경고). 재오픈 무결성 확인.
- 완성 파일을 `/mnt/user-data/outputs/`로 복사하고 사용자에게 전달.
- 큐시트 품질 루브릭(§6)으로 자가 점검 후, jc-redteam 최종 감수 권고.

## 5. 실행 모드

| 모드 | 발동 | 산출 |
|------|------|------|
| **quick** | "스켈레톤만", 세그먼트·시간만 있음 | 큐시트 그리드(시간·세그먼트·Owner 중심), A/V/L·연출 cue는 빈칸 골격 |
| **standard** (기본) | 일반 행사 | 10컬럼 풀 그리드 + 변경이력 시트 + 시간 무결성 검증 |
| **deep** | "연출까지", 리허설/생방/하이브리드 | 풀 그리드 + **진행 시나리오**(큐별 연출 의도·전환·예비 cue) + 리스크/컨틴전시 cue + 큐콜 약어 범례 |

모호하면 standard로 시작하고 한 번 확인한다.

## 6. 큐시트 품질 루브릭 (결정적)

산출 직후 자가 점검. 통과 못 하면 빌드로 회귀. (게이트: ≥85 GO)

| 카테고리 | 배점 | 자동 | 기준 |
|---------|:---:|:---:|------|
| 시간 무결성 | 30 | ✅ | 소요 합 = 총 행사시간, 클록 단조 증가, 음수/0 소요 없음 |
| 컬럼 완전성 | 20 | ✅ | 10컬럼 존재, Cue# 연속, 필수칸(시간·세그먼트·Owner) 채움 |
| 표기 표준 | 20 | ⛏ | 연출/AV/조명 cue가 `cue-notation.md` 약어 준수 |
| 버전·이력 | 10 | ✅ | 버전 넘버 + 변경이력 시트 존재 |
| 디자인·식별 | 10 | ⛏ | jc 토큰 적용 + 회사 식별정보 0건 |
| 현장 사용성 | 10 | ⛏ | 쇼콜러가 즉시 콜 가능(Owner 명확·비고 충분) |

**Critical 자동 반려**: 시간 무결성 실패(합 불일치) / 회사 식별정보 하드코딩.
자동 항목(시간·컬럼·버전)은 `build_runsheet.py`가 검증, 나머지는 사람/jc-redteam.

## 7. 체이닝

본 스킬은 **운영 단계 소비자**다. 상류(기획·발표)의 시간 구조를 받아 큐시트로 구체화한다.

```
mice-proposal (프로그램 구조)  ─┐
                                ├─→ mice-run-of-show ─→ 큐시트 XLSX (현장 종착)
pt-script (발표 세그먼트 시간)  ─┘                    └─(선택)→ mice-dashboard/mice-aftermath
```

- **입력**: `ChainPayload/v1` (source=`mice-proposal` 또는 `pt-script`). 봉투 정본은 `jc-design-system/references/chaining-protocol.md`, 본 스킬 고유 입력 매핑은 `references/chaining-schema.md`.
- **출력**: `ChainPayload/v1` (source=`mice-run-of-show`) — 계획 대비 실제 진행 비교용으로 사후 스킬에 전달 가능. 1차 용도는 현장 XLSX.

## 8. jc-design-system 연동

XLSX는 CSS 변수 불가 → `build_runsheet.py`가 SoT JSON(`signature-tokens.md §6`)을 런타임 로드하고, 실패 시 미러 hex로 폴백한다(`references/jc-design-mapping.md`). 값 정본은 항상 jc-design-system.

| 위치 | 시맨틱 역할 | SoT 토큰 |
|------|-----------|---------|
| 행사 헤더·타이틀 | 헤더 | `--jc-primary` (#0A2540) |
| 컬럼 헤더 | 액센트 | `--jc-accent` (#2962FF) |
| 섹션/시간 블록 구분 | 중립 강조면 | `--jc-border-strong` |
| 연출 cue 강조 | 포인트 | `--jc-point-orange` |

## 9. 파일 구조

```
mice-run-of-show/
├── SKILL.md
├── references/
│   ├── cuesheet-columns.md     # 10컬럼 작성 규약
│   ├── cue-notation.md         # 연출/AV/조명 표준 표기
│   ├── chaining-schema.md      # ChainPayload 입출력 (고유 페이로드)
│   ├── jc-design-mapping.md    # xlsx 색상 역할→SoT 토큰
│   ├── anti-patterns.md        # 큐시트 도메인 안티패턴
│   └── worked-example.md       # 반일 컨퍼런스 end-to-end
└── scripts/
    └── build_runsheet.py       # XLSX 생성 + 시간 검증 + 버전관리 (self-test 포함)
```

## 10. 운영 원칙 / 한계

- **시간이 진실**: 디자인보다 시간 무결성이 먼저. 합이 안 맞으면 예쁜 큐시트는 무의미하다.
- **현장 우선**: 화면 미려함보다 쇼콜러 판독성. 약어 표준·Owner 명확성을 우선한다.
- **단일 타임라인 모델**: 본 스킬은 클록을 *순차 누적*으로 산출한다 → **하나의 무대/트랙**을 전제한다. 동시 진행되는 분과(브레이크아웃·복수 홀)는 트랙별로 큐시트를 분리 생성(트랙당 1회 빌드)한다. 한 시트에 병렬 트랙을 겹쳐 넣지 않는다(시간 무결성 검증이 깨짐).
- **STT·실시간 아님**: 본 스킬은 사전 운영 문서다. 현장 실시간 콜 로그·중계는 범위 밖.
- **xlsx 한계**: openpyxl 미설치 환경은 빌드 불가 → 구문(ast) 검증만. 의존성 명시(frontmatter).

## 11. 버전 히스토리

| 버전 | 일자 | 주요 변경 |
|------|------|---------|
| v1.0.0 | 2026-06-05 | 신규. jc-skill-creator 하우스 표준 준수. 10컬럼 버전드 큐시트 XLSX + 변경이력 시트 + 시간 무결성 자동검증 + 클록 자동산출 + 연출 표기 표준 + quick/std/deep 모드 + ChainPayload 입출력(proposal/pt-script). Association Event Management·production cue sheet 패턴 흡수·jc 재구성. mice-estimate xlsx(openpyxl+SoT 토큰 로드) 패턴 재사용. |
