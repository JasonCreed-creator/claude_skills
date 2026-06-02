# Dashboard Spec — HTML 대시보드 사양

본 스킬의 메인 산출물인 단일 HTML 대시보드의 구조·인터랙션·영속화 룰을 정의한다.

---

## 1. 파일 구조

### 산출물
```
dashboard_[프로젝트]_[YYYYMMDD].html  (단일 파일, 메인)
.series-data/[series_id].json         (시리즈 모드 시 동기화)
```

### 외부 의존 (CDN)
- React 18 (UMD)
- ReactDOM 18 (UMD)
- Recharts 2.12 (UMD)
- Babel Standalone (런타임 JSX 트랜스파일)
- Pretendard (한글) / Inter (영문) / JetBrains Mono (모노스페이스)

### 오프라인 동작
- CDN 의존으로 인터넷 환경 필수
- 향후 v2.1 확장 후보: 라이브러리 인라인 임베드 옵션 (`--offline`)

---

## 2. UI 구조 — 4개 핵심 영역

### 영역 1: Header (sticky top)
- Deep Navy 배경 + Electric Blue/Orange 그라데이션 띠
- 좌측: 프로젝트명·미팅일·유형·시리즈 정보
- 우측: Internal/External 모드 토글
- 알림: 지연 Action 카운트 자동 표시

### 영역 2: KPI Cards (4개)
- 결정사항 / Action 총개 / 미결 사항 / 완료율
- 카드 상단 색상 라인으로 영역 구분 (Accent / Magenta / Orange / Neon)
- 모바일: 2단 그리드 자동 전환

### 영역 3: Tabs (4개)
- 본 미팅 (디폴트)
- Action 트래커
- 시리즈 누적 (`--series` 모드만 활성)
- 전략 메모 (Internal 모드만 활성)

### 영역 4: Toolbar Footer (sticky bottom)
- Internal/External 모드 표시
- Slack 페이스트 / PDF 저장 / JSON 백업 / 시리즈 저장 버튼

---

## 3. 인터랙션 룰

### 모드 토글 (Internal ↔ External)
- 헤더 우상단 토글 클릭 시 즉시 전환
- 전략 메모 탭 활성화/비활성화 자동 반영
- 익명화: External 시 자동 적용 (이름 → 직함·역할명)
- Redaction: External 시 표시
- Slack 페이스트 결과물에도 반영

### Action Status 변경
- 칸반 카드 내 Status 드롭다운으로 변경
- TODO → DOING → BLOCKED → DONE 자유 전환
- 변경 즉시 KPI 카드 (완료율) 자동 갱신
- window.storage 자동 저장 (시리즈 모드)

### 필터링
- 검색: 제목·Owner·ID 부분 매칭
- Priority: P0/P1/P2/P3 단일 선택
- Owner: 드롭다운 단일 선택
- 다중 필터 AND 조합

### Due 자동 표시
- 오늘 ~ +3일: Orange 굵은 글자 (`due-soon`)
- 오늘 이전 + DONE 아닌 경우: Magenta 굵은 글자 (`due-overdue`)

### Carry-over 시각 표시
- Action 카드 배경 Orange 약색
- ID 앞 ↻ 마커
- 미결 사항도 동일 처리 (왼쪽 외곽선 점선)

---

## 4. 차트 사양 (Recharts)

### Status 분포 도넛 (Action 트래커 탭)
```
PieChart
- innerRadius=50, outerRadius=80
- Colors: TODO=Grey, DOING=Accent, BLOCKED=Magenta, DONE=Neon
- 라벨: "{name} {value}"
- 0건 카테고리 자동 제외
```

### Owner별 Bar 차트 (Action 트래커 탭)
```
BarChart
- X: Owner (이름)
- Y: 건수
- 2 시리즈: 총 Action (Accent) / 완료 (Neon)
- 폰트 10pt (모바일 가독성)
```

### 시리즈 완료율 LineChart (시리즈 누적 탭)
```
LineChart
- X: "1차", "2차", "N차"
- Y: 완료율 0~100%
- Stroke: Neon, Width 3
- 추이 시각화 핵심 차트
```

### 시리즈 Action 분포 BarChart (시리즈 누적 탭)
```
BarChart (Stacked)
- X: 회차
- Y: Action 건수
- 2 시리즈 stack: 신규 (Accent) / Carry-over (Orange)
```

---

## 5. 영속화 룰

### Storage Adapter 우선순위
```
1. window.storage (Claude 환경)
   ├─ 비동기 API
   ├─ 5MB per key 제한
   └─ 사용자별 격리

2. localStorage (일반 브라우저)
   ├─ 동기 API (await Promise.resolve(...) 래핑)
   ├─ 도메인별 격리
   └─ 5~10MB 한계
```

### 키 구조
```
mice-mtg:[series_id]                    # 시리즈 회차 누적 데이터
mice-mtg:settings:[user]                # (옵션) 사용자 설정
```

### 저장 데이터 스키마
```json
{
  "series_id": "darktrace-discovery",
  "sessions": [
    {
      "session_no": 1,
      "date": "2026-04-15",
      "new_actions": 8,
      "carry_over_actions": 0,
      "done": 6, "doing": 0, "blocked": 1, "todo": 1,
      "completion_rate": 0.75,
      "data_snapshot": { /* 전체 회차 데이터 */ }
    }
  ]
}
```

### 영속화 트리거
- "시리즈 저장" 버튼 명시 클릭 (사용자 의도 보존)
- 자동 저장 안 함 (의도치 않은 덮어쓰기 방지)

### 백업 전략
- JSON 다운로드 버튼: 사용자 명시 클릭으로 즉시 다운로드
- 외부 영속화: Google Drive·Notion 등에 사용자가 수기 백업
- 챗 환경 리셋 시 window.storage 손실 가능 → JSON 백업 운영 권장

---

## 6. Slack 페이스트 포맷

### 출력 마크다운 구조 (`buildSlackMd`)
```markdown
**[프로젝트명] 미팅 요약 (YYYY-MM-DD)**
_시리즈 series_id / N차_

**참석:** [참석자 목록]

**결정사항**
- [최대 3건]
- (외 N건은 본 회의록 참조)

**Action**
- (Owner) Action — Due
- [최대 3건]
- (외 Action N건은 본 회의록 참조)

**다음:** 다음 미팅 (YYYY-MM-DD HH:MM)

_(미결 N건 / 리스크 N건 — 회의록 본문 참조)_

**전략 코멘트:** [Internal 모드 strategy_oneliner 한 줄]

---
_[Internal] 외부 공유 금지_  또는  _본 요약은 양측 공유용입니다._
```

### 클립보드 복사 메커니즘
```
1. navigator.clipboard.writeText() 우선 시도
   └─ 실패 시 (HTTPS 미환경) ↓
2. textarea + execCommand('copy') fallback
   └─ 모든 환경에서 동작 보장
```

### 분량 가이드
- 200~600자 (Slack/Email 1스크롤 내)
- 모바일 가독성 우선

---

## 7. PDF Export 메커니즘

### 동작 원리
```javascript
window.print()  → 브라우저 인쇄 대화상자 →
사용자가 "PDF로 저장" 선택 → 다운로드
```

### @media print 스타일 적용
```css
@media print {
  .header, .toolbar, .tabs, .input-area, .filter-bar { display: none; }
  .panel { page-break-inside: avoid; border: 1px solid #999; }
  body { background: white; }
  .kanban { grid-template-columns: repeat(2, 1fr); }
}
```

→ 인쇄 시 다음 자동 처리:
- 헤더·푸터 툴바·탭 숨김
- 패널 페이지 브레이크 회피
- 칸반 4컬럼 → 2컬럼 (인쇄 가독성)
- 컬러 → 흑백 친화 변환

### PDF 활용 시나리오
- Type C 발주처 공식 송부 (워드 대체)
- 임원 종이 보고
- 인쇄·보관 의무 미팅
- 클라이언트 이메일 첨부

---

## 8. JSON 백업 메커니즘

### 다운로드 데이터 스키마
```json
{
  "project_name": "...",
  "meeting_date": "...",
  "agenda": [...],
  "decisions": [...],
  "actions": [...],
  "risks": [...],
  "pending": [...],
  "next_steps": [...],
  "strategy_note": {...},
  "series_id": "...",
  "_seriesHistory": [...]   // 시리즈 누적 데이터 동시 백업
}
```

### 파일명 규칙
```
mice-mtg_[프로젝트]_[YYYY-MM-DD].json
```

### 복원 가능성
- JSON을 다시 본 스킬에 입력하면 동일 대시보드 재생성
- 시리즈 모드 복원 시 `_seriesHistory` 자동 인식

---

## 9. 접근성 / 반응형

### 키보드 인터랙션
- Tab: 포커스 이동
- Enter/Space: 버튼 활성화
- Esc: 모달 닫기 (향후 v2.1)

### 화면 크기 반응
| 너비 | 레이아웃 |
|------|---------|
| ≥ 900px | KPI 4단 / Kanban 4컬럼 |
| 720~900px | KPI 4단 / Kanban 2컬럼 |
| < 720px | KPI 2단 / Kanban 1컬럼 / 헤더 축소 |

### 인쇄
- A4 세로 기준
- 패널 페이지 브레이크 회피
- 컬러 → 회색조 친화

---

## 10. 보안·프라이버시

### Internal/External 토글 보안
- External 모드 전환 시 즉시 익명화 적용
- 전략 메모 탭 비활성화 (DOM에서도 제거)
- Redaction 표시 활성화

### 클립보드 데이터 처리
- Slack 페이스트 시 모드별 마스킹 자동 적용
- 사용자 의도 명시적 클릭 후에만 동작

### 영속화 데이터 보호
- window.storage / localStorage 모두 사용자 디바이스 한정
- 서버 전송 없음
- 외부 백업은 사용자 책임 (JSON 다운로드)

---

## 11. 검증 체크리스트

생성 직후 자동 검증 (`validate_dashboard_html`):

| 체크 | 통과 기준 |
|------|----------|
| 플레이스홀더 치환 | `{{TITLE}}`·`{{INITIAL_DATA}}` 잔존 없음 |
| 라이브러리 연결 | React + Recharts 확인 |
| 시그니처 토큰 | 5색 (#0A2540·#2962FF·#FF5722·#E91E63·#00E676) 모두 적용 |
| 파일 크기 | 100KB 이상 (정상 빌드 시 50~80KB 템플릿 + JSON 데이터) |

---

## 12. v2.1 확장 후보 (참고)

| 기능 | 설명 | 우선순위 |
|------|------|---------|
| `--offline` | 라이브러리 인라인 임베드 (오프라인 동작) | 중 |
| `--client=<id>` 오버레이 | 클라이언트별 컬러 자동 적용 | 중 |
| 통합 미팅 대시보드 | 다중 series_id 통합 조회 | 낮 |
| 다음 어젠다 자동 생성 | 미결+후속 일정 → 어젠다 .md | 중 |
| Action 마감 알림 | window.Notification API | 낮 |
| 음성 메모 임베드 | Web Audio API (대시보드 내 재생) | 낮 |
| 다국어 지원 | i18n (영문 모드) | 중 |
