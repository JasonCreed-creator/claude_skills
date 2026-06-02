# Series Tracking — 시리즈 모드 데이터 구조 + Carry-over 룰

동일 프로젝트의 N회차 미팅 누적 추적을 위한 시리즈 모드 정의.

호출: `--series=<series_id>`

---

## 1. 시리즈 식별자 (`series_id`)

### 명명 규칙
```
[프로젝트 약어]-[유형]
```

### 권장 series_id 예시 (기획자님 현재 진행 프로젝트 기준)

| series_id | 프로젝트 | 유형 |
|-----------|---------|------|
| `darktrace-discovery` | Darktrace Korea | Discovery (수주 전) |
| `darktrace-execution` | Darktrace Korea | 수주 후 운영 |
| `rmb-rebuild26` | RMB REBUILD26 | 정기 협의 |
| `tobesoft-seminar26` | TOBESOFT GRAND SEMINAR 2026 | 정기 협의 |
| `confex-bidding` | ConfEx 박람회 | 입찰 단계 |
| `remember-weekly` | 리멤버 주대웅 실장 | 주간 정기 |
| `pco-internal-weekly` | 자사 내부 팀 | 주간 내부 |

→ 기획자님이 새 시리즈 시작 시 `--series=<신규 ID>`로 호출하면 자동 생성.

---

## 2. 시리즈 데이터 구조

각 시리즈는 별도 JSON 데이터 파일로 누적 관리.

### 저장 위치
```
.series-data/[series_id].json
```

(점 prefix로 일반 파일과 분리)

### 데이터 스키마

```json
{
  "series_id": "darktrace-discovery",
  "project_name": "Darktrace Korea Discovery",
  "client_id": "darktrace",
  "default_type": "A",
  "created_at": "2026-04-15",
  "last_updated": "2026-05-09",
  "sessions": [
    {
      "session_no": 1,
      "date": "2026-04-15",
      "type": "A",
      "minutes_file": "meeting-minutes_darktrace-discovery_20260415_A.docx",
      "actions_file": "action-items_darktrace-discovery_20260415.xlsx",
      "summary_file": "summary_darktrace-discovery_20260415.md",
      "decisions_count": 3,
      "actions": [
        {
          "id": "DT-DISC-001",
          "owner": "호스트",
          "due": "2026-04-22",
          "priority": "P1",
          "status": "DONE",
          "action": "베뉴 후보 3곳 비교 자료 제출",
          "linked": null
        },
        {
          "id": "DT-DISC-002",
          "owner": "Darktrace 김부장",
          "due": "2026-05-02",
          "priority": "P1",
          "status": "BLOCKED",
          "action": "본사 동시통역 결재",
          "linked": null
        }
      ],
      "pending_items": [
        {
          "id": "DT-DISC-PEND-001",
          "item": "동시통역 부스 설치 여부",
          "reason": "Darktrace 본사 결재 필요",
          "next_review": "다음 미팅"
        }
      ]
    },
    {
      "session_no": 2,
      "date": "2026-05-09",
      "type": "A",
      "minutes_file": "meeting-minutes_darktrace-discovery_20260509_A.docx",
      "carry_over_actions": ["DT-DISC-002"],
      "carry_over_pending": ["DT-DISC-PEND-001"],
      "new_actions_count": 7,
      "decisions_count": 4
    }
  ],
  "cumulative_stats": {
    "total_sessions": 2,
    "total_actions": 13,
    "done": 7,
    "doing": 2,
    "blocked": 2,
    "todo": 2,
    "completion_rate": 0.54,
    "long_pending_actions": ["DT-DISC-002"]
  }
}
```

---

## 3. Carry-over 처리 룰

### 자동 carry-over 대상

| 이전 회차 항목 | Status / 유형 | 본 회차 처리 |
|---------------|--------------|-------------|
| Action | TODO | 그대로 carry-over |
| Action | DOING | 그대로 carry-over (진척도 갱신 시도) |
| Action | BLOCKED | 그대로 carry-over (해소 시그널 매칭 시 갱신) |
| Action | DONE | carry-over 제외, 누적 시트에만 기록 |
| 미결 사항 | (모든 미결) | 그대로 carry-over (본 회차 재논의 시 해소 처리) |
| 결정사항 | (모든 결정) | carry-over 안 함 (본 회차에는 "지난 결정 참조" 표기만) |

### Status 갱신 시그널 매칭

본 회차 transcript에서 carry-over Action ID 또는 내용 매칭:

```
"베뉴 후보 자료 보내드렸습니다"          → DT-DISC-001 → DONE
"동시통역 결재 아직 못 받았어요"          → DT-DISC-002 → BLOCKED 유지
"통역 결재 받았습니다"                  → DT-DISC-002 → TODO/DOING 갱신
"통역사 1명 계약 완료"                  → DT-DISC-002 → DONE
```

매칭 신뢰도 낮은 경우 사용자 확인 요청.

---

## 4. 본 회차 회의록 내 시리즈 표시

### 회의록 .docx 상단 표시
```
[프로젝트명] (시리즈 N차 / 누적 액션 X건 중 Y건 완료, 완료율 Z%)
```

### Carry-over Action 표시
- Action Items 표에서 carry-over 행은 외곽선 표시 (`color.point.orange`)
- ID 옆에 (carried) 마커
- "처음 등록 회차: N차" 메타 표시

### 미결 사항 carry-over 표시
- 미결 사항 섹션 상단에 "(지난 회차 미결)" 그룹화
- 신규 미결 사항은 그 아래 "(본 회차 신규)" 그룹화

---

## 5. Action Items 트래커 .xlsx 시리즈 시트

`series-tracking.md` 시리즈 모드 활성화 시 .xlsx에 추가되는 시트:

### 시트명: "시리즈 누적"

| 회차 | 일자 | 신규 Action | 완료 (DONE) | 진행 (DOING) | 차단 (BLOCKED) | 미시작 (TODO) | 완료율 |
|------|------|-------------|-------------|--------------|----------------|---------------|--------|
| 1 | 2026-04-15 | 8 | 6 | 0 | 1 | 1 | 75% |
| 2 | 2026-05-09 | 12 (신규 7+carry 5) | 9 | 1 | 1 | 1 | 75% |

### 시트명: "장기 미해결"

3회차 이상 carry-over된 Action 별도 추적:

| ID | 최초 등록 | 회차 횟수 | 현재 Status | Owner | Due | Action |
|----|----------|----------|-------------|-------|-----|--------|
| DT-DISC-002 | 2026-04-15 | 3 | BLOCKED | Darktrace 김부장 | 2026-05-02 (지연) | 본사 동시통역 결재 |

→ 장기 미해결 자동 감지 → 회의록 전략 메모에 "장기 미해결 N건 처리 시급" 자동 권고.

---

## 6. 시리즈 종료 처리

### 종료 시그널
- 사용자 명시: `--series-close=<series_id>`
- 또는 회의록에 "프로젝트 종료" 명시 발화 매칭

### 종료 시 산출물
- 시리즈 종합 보고서 .docx 자동 생성
- 누적 통계 + 모든 결정사항 통합 + 모든 Action 최종 상태 + 학습 메모

### 시리즈 종합 보고서 구조

```
1. 시리즈 개요 (프로젝트명·기간·총 회차)
2. 누적 결정사항 (회차별 결정 모음)
3. Action 최종 상태 (완료율·미완료 Action 사유)
4. 미결 사항 처리 결과
5. 일정 변동 추이
6. 시리즈 학습 메모 (전략 메모 통합)
7. 다음 시리즈 권고 (있는 경우)
```

---

## 7. 시리즈 모드 호출 예시

### 신규 시리즈 시작 (1차 미팅)
```
사용자: "Darktrace Discovery 1차 미팅 정리해줘. transcript는 [붙여넣기]. --series=darktrace-discovery"
```

→ 본 스킬:
- `.series-data/darktrace-discovery.json` 신규 생성
- session_no=1로 기록
- 일반 회의록 + Action + 요약 산출

### 2차 미팅 (carry-over 자동 적용)
```
사용자: "Darktrace Discovery 2차 미팅 정리해줘. transcript는 [붙여넣기]. --series=darktrace-discovery"
```

→ 본 스킬:
- 기존 JSON 로드 → session 1의 미완료 Action·미결 사항 추출
- 본 회차 transcript에서 갱신 시그널 매칭 → Status 갱신
- 본 회차 신규 Action 추가
- session_no=2로 기록
- 회의록에 carry-over 표시 + 누적 통계 + 시리즈 시트

### 시리즈 조회
```
사용자: "darktrace-discovery 시리즈 현황 보여줘"
```

→ 본 스킬:
- JSON 로드 → 누적 통계 + 장기 미해결 Action 보고서 생성

### 시리즈 종료
```
사용자: "darktrace-discovery 시리즈 종료 처리해줘"
```

→ 본 스킬:
- 시리즈 종합 보고서 .docx 산출
- JSON에 closed_at 타임스탬프 추가

---

## 8. 시리즈 데이터 백업 권장

JSON 데이터 파일은 챗 환경 리셋 시 손실될 수 있으므로 외부 백업 권장:

| 백업 방식 | 비고 |
|-----------|------|
| Google Drive 동기화 | 권장 — 자동 백업 + 다중 디바이스 |
| 로컬 PC 폴더 | 보안 강한 시리즈는 로컬만 |
| Notion DB | 시리즈 데이터를 Notion으로 마이그레이션 (수기) |

→ 본 스킬은 산출물을 환경 내에 생성하지만, 시리즈 데이터 영속성은 사용자가 외부로 가져가서 관리.

---

## 9. 시리즈 모드 미적용 시 동작

`--series` 플래그 없이 호출 시:
- 단일 회의 회의록만 생성
- carry-over 처리 없음
- 시리즈 누적 시트 없음
- 추후 시리즈 모드 추가 시 수기로 JSON에 추가 가능
