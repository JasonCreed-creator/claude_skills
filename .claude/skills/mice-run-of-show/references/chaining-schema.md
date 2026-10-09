# Chaining Schema — mice-run-of-show 입출력

본 스킬이 대화 입력과 `jc-pptx` 봉투에서 프로그램·시간 구조를 받아 큐시트로 구체화하고, 사후 스킬로 계획 데이터를 넘기는 페이로드 매핑.

> **봉투 정본**: 공통 `ChainPayload/v1` 봉투(`$schema`·`source`·`version`·`generatedAt`)·표준 규약·자동 라우팅은 [jc-design-system/references/chaining-protocol.md](../../jc-design-system/references/chaining-protocol.md) 참조. 본 문서는 mice-run-of-show **고유 페이로드**만 정의한다. 봉투 식별은 `source`로 수렴한다(chaining-protocol §7).

---

## 1. 워크플로우상의 위치

```
대화 입력 (프로그램·세그먼트·시간·Owner)         ─┐
jc-pptx 봉투 (presentation.minutes · sections · 헤더) ─┴─→ mice-run-of-show ─→ 큐시트 XLSX (현장 종착)
                                                                  └─(선택)→ mice-ops-docs / mice-aftermath
```

운영 단계 **소비자**. 1차 용도는 현장 XLSX이며, 출력 봉투는 사후 비교(계획 vs 실제)용 선택지다. 행사 프로그램(세그먼트 배열)을 봉투로 내는 상류는 없다 — 세그먼트는 대화 입력(또는 사용자가 준 덱의 당일 타임테이블 슬라이드 내용)으로 채운다. `pt-script`는 상류가 아니다(봉투를 내지 않음). 반대로 pt-script가 완성 큐시트를 MC 대본의 순서 참고로 읽는 것은 가능하다.

---

## 2. 입력 — `jc-pptx` 봉투에서 받기

제안서·발표덱 봉투(정본 `jc-pptx/references/proposal-playbook.md` §6)에서 행사 헤더와 발표 블록 시간을 가져온다.

```json
{
  "$schema": "ChainPayload/v1",
  "source": "jc-pptx",
  "version": "<송신 스킬 버전>",
  "projectTitle": "A사 테크 포럼 2026",
  "eventDate": "2026-06-20",
  "venue": { "name": "[베뉴]" },
  "deck_meta": { "purpose": "proposal", "slides": 24 },
  "sections": [ { "id": "03", "title": "운영 계획", "slides": [12, 24] } ],
  "presentation": { "minutes": 20, "type": "conference" }
}
```

### 매핑 (봉투 → event 헤더·cue 객체)

| ChainPayload 필드 | → 큐시트 | 변환 |
|---|---|---|
| `projectTitle`·`eventDate`·`venue.name` | event `title`·`date`·`venue` | 그대로. 없으면 대화 입력 |
| `presentation.minutes` | 발표 블록 cue의 `duration_min` | 발표 1건 = 행사 전체 큐시트의 **한 블록**. 앞뒤 등록·휴식·폐회 등 운영 큐는 대화 입력으로 보충 |
| `presentation.type` | 발표 블록 `stage`·`segment` 이름 힌트 | `bidding_pt`면 "제안 발표", `conference`면 "발표" |
| `sections[]` | 참고만 | 덱의 프로그램·타임테이블 슬라이드 위치를 찾는 단서. 세그먼트로 직접 변환하지 않는다 |
| (A/V/L·연출 cue·Owner) | `audio`/`video`/`light`/`cue`/`owner` | 봉투에 없음 → 빈칸(quick) 또는 사용자 작성 |

> 봉투에 세그먼트 배열(`program[]`)은 없다. 향후 jc-pptx가 이 키를 내게 되면 `segment`·`duration_min`·`stage`·`owner`를 cue 키로 그대로 흡수한다(현재는 대화 입력 경로).

---

## 3. 입력 — 대화로 받기 (기본 경로)

세그먼트 리스트(세그먼트명·소요 분·무대/발표·A/V/L·연출 cue·Owner·비고)를 SKILL.md Step 2 표대로 받아 `cues`를 구성한다. 시작 시각·총 행사시간이 있으면 무결성 검증 기준으로 쓴다. 빠진 값은 `TBD` 기본값으로 채우고 한 줄로 밝힌다.

---

## 4. 출력 — 사후 스킬로 전달 (선택)

큐시트 생성 후, 계획 데이터를 사후 비교용으로 직렬화.

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-run-of-show",
  "version": "<스킬 버전>",
  "generatedAt": "2026-06-05T10:00:00+09:00",
  "target": "mice-ops-docs",
  "projectTitle": "A사 테크 포럼 2026",
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
  "runsheetFile": "런오브쇼_A사테크포럼_v1_260620.xlsx"
}
```

### 활용
- **mice-ops-docs**(기본 target, 구 mice-dashboard 대체): 계획 타임라인 vs 실제 진행 비교 KPI 대시보드(지연·초과 세그먼트).
- **mice-aftermath**: 사후 결과보고의 "계획 대비 실제" 운영 타임라인 섹션. `target="mice-aftermath"`로 지정.

---

## 5. source enum 등록

`mice-run-of-show`는 봉투 정본(`jc-design-system/references/chaining-protocol.md`)의 §3 source enum · §4 페이로드 정본 위치 · §5 체이닝 흐름에 등록돼 있다. 다운스트림은 §7 `detect_input_source()`로 `source` 문자열을 판별해 본 스킬을 식별한다.

---

## 6. 입력 검증 체크

- [ ] `$schema`가 `ChainPayload/v1`인가(아니면 체이닝이 아니라 파일·대화 입력으로 처리 — chaining-protocol §6-1)
- [ ] `source`가 `jc-pptx`인가(구 별칭은 chaining-protocol §3-1로 해석)
- [ ] `presentation.minutes`가 양의 정수인가(없으면 발표 블록 시간 사용자 보완 플래그)
- [ ] 대화로 받은 각 세그먼트에 `segment`·`duration_min`(양의 정수)이 있는가
- [ ] 회사 식별정보 0건(헤더·owner·segment에서 검출 시 경고)
