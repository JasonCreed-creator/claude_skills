# Chaining Schema — mice-run-of-show 입출력

본 스킬이 상류(mice-proposal·pt-script)에서 프로그램·시간 구조를 받아 큐시트로 구체화하고, 사후 스킬로 계획 데이터를 넘기는 페이로드 매핑.

> **봉투 정본**: 공통 `ChainPayload/v1` 봉투(`$schema`·`source`·`version`·`generatedAt`)·표준 규약·자동 라우팅은 [jc-design-system/references/chaining-protocol.md](../../jc-design-system/references/chaining-protocol.md) 참조. 본 문서는 mice-run-of-show **고유 페이로드**만 정의한다. 봉투 식별은 `source`로 수렴한다.

---

## 1. 워크플로우상의 위치

```
mice-proposal (프로그램 구조) ─┐
                               ├─→ mice-run-of-show ─→ 큐시트 XLSX (현장 종착)
pt-script (발표 세그먼트 시간) ─┘                     └─(선택)→ mice-dashboard / mice-aftermath
```

운영 단계 **소비자**. 1차 용도는 현장 XLSX이며, 출력 봉투는 사후 비교(계획 vs 실제)용 선택지다.

---

## 2. 입력 — `mice-proposal` 에서 받기

제안서의 프로그램/일정 슬라이드 → 세그먼트 스켈레톤.

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-proposal",
  "version": "v2.x.x",
  "projectTitle": "T社 테크 포럼 2026",
  "eventDate": "2026-06-20",
  "venue": { "name": "[베뉴]" },
  "program": [
    { "segment": "등록·입장",   "duration_min": 30, "owner": "운영" },
    { "segment": "개회·환영사", "duration_min": 10, "stage": "사회자", "owner": "사회" },
    { "segment": "기조연설",     "duration_min": 40, "stage": "기조연사", "owner": "무대" }
  ]
}
```

### 매핑 (program[] → cue 객체)

| ChainPayload 필드 | → cue 키 | 변환 |
|---|---|---|
| `program[].segment` | `segment` | 그대로 |
| `program[].duration_min` | `duration_min` | 없으면 사용자 보완 |
| `program[].stage` | `stage` | 없으면 `-` |
| `program[].owner` | `owner` | 없으면 사용자 보완 |
| (A/V/L·연출cue) | `audio`/`video`/`light`/`cue` | 제안서엔 없음 → 빈칸(quick) 또는 사용자 작성 |
| `projectTitle`·`eventDate`·`venue.name` | event 헤더 | 그대로 |

---

## 3. 입력 — `pt-script` 에서 받기

발표 대본의 세그먼트별 소요시간 → 발표 블록 큐.

```json
{
  "$schema": "ChainPayload/v1",
  "source": "pt-script",
  "version": "v2.x.x",
  "proposal_meta": { "presentation_minutes": 20, "presentation_type": "conference" },
  "segments": [
    { "segment": "오프닝", "duration_min": 2, "stage": "발표자", "cue": "VT 인트로" },
    { "segment": "본론 1", "duration_min": 8, "stage": "발표자", "video": "발표 PPT" }
  ]
}
```

### 처리 규칙
- `segments[]`(또는 단일 `presentation_minutes`)를 발표 세그먼트 큐로 흡수.
- pt-script는 *발표 1건*의 시간 구조 → 행사 전체 큐시트의 **한 블록**으로 삽입(앞뒤에 등록·휴식·폐회 등 운영 큐를 사용자/proposal에서 보충).
- pt-script 고유 봉투(`$schema: pt-script/v2.0`)로 와도 `source`로 수렴 식별(chaining-protocol §8).

---

## 4. 출력 — 사후 스킬로 전달 (선택)

큐시트 생성 후, 계획 데이터를 사후 비교용으로 직렬화.

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-run-of-show",
  "version": "v1.0.0",
  "generatedAt": "2026-06-05T10:00:00+09:00",
  "target": "mice-dashboard",
  "projectTitle": "T社 테크 포럼 2026",
  "eventDate": "2026-06-20",
  "plan": {
    "startTime": "09:00",
    "endTime": "12:30",
    "totalMinutes": 210,
    "cueCount": 18,
    "cues": [
      { "cueNo": "C01", "clock": "09:00", "segment": "등록·입장", "durationMin": 30, "owner": "운영" }
    ]
  },
  "version_no": 1,
  "runsheetFile": "런오브쇼_T社테크포럼_v1_260620.xlsx"
}
```

### 활용
- **mice-dashboard**: 계획 타임라인 vs 실제 진행 비교 KPI(지연·초과 세그먼트).
- **mice-aftermath**(향후): 사후 결과보고의 운영 타임라인 섹션.

---

## 5. source enum 등록 (완료)

`mice-run-of-show`는 ChainPayload **신규 source**다. 봉투 정본(`jc-design-system/references/chaining-protocol.md`)의 §1 적용 대상 · §3 source enum · §4 페이로드 매핑표 · §5 엣지에 본 스킬이 **등록 완료**(F-1)되었다. 다운스트림 `detect_input_source()`가 `source` 문자열로 본 스킬을 식별한다.

---

## 6. 입력 검증 체크

- [ ] `$schema`가 `ChainPayload/v1`(또는 레거시 스킬 전용)인가
- [ ] `source`가 `mice-proposal` / `pt-script`인가
- [ ] `program[]`/`segments[]`의 각 항목에 `segment`가 있는가
- [ ] `duration_min`이 양의 정수인가(없으면 사용자 보완 플래그)
- [ ] 회사 식별정보 0건(헤더·owner·segment에서 검출 시 경고)
