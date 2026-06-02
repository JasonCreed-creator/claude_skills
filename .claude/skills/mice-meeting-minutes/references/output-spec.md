# Output Spec v2 — 산출물 사양

본 스킬은 한 번의 입력으로 **인터랙티브 HTML 대시보드 1개**를 메인 산출물로 생성하며, 대시보드 내 버튼으로 Slack 페이스트·PDF 저장·JSON 백업의 부가 기능을 제공한다.

---

## 1. 메인 산출물: HTML 대시보드 (.html)

### 파일명 규칙
```
dashboard_[프로젝트]_[YYYYMMDD].html
```

예시:
- `dashboard_darktrace-discovery_20260509.html`
- `dashboard_rmb-rebuild26_20260509.html`
- `dashboard_internal-weekly_20260509.html`

### 단일 파일 자체 완결성
- HTML/CSS/JS 모두 포함
- React + Recharts CDN 호출 (인터넷 환경 필요)
- 다운로드·로컬 실행 가능
- 시리즈 누적은 `window.storage` 또는 `localStorage` 자동 활용

### 분량
- 파일 크기: 50~80KB (템플릿 + 주입 JSON 데이터)
- 화면 영역: 데스크톱 1280px 최적, 모바일 자동 반응형

### 구조 (4영역)
1. Header (sticky top) — 프로젝트 메타·시리즈·모드 토글
2. KPI Cards — 결정·Action·미결·완료율 4카드
3. Tabs Body — 본 미팅·Action 트래커·시리즈·전략 메모
4. Toolbar Footer (sticky bottom) — Slack·PDF·JSON·시리즈 저장 버튼

상세는 `references/dashboard-spec.md` 참조.

---

## 2. 부가 기능 1: Slack 페이스트 (대시보드 내 버튼)

### 동작
- "💬 Slack 페이스트" 버튼 클릭
- 200~600자 마크다운 요약 자동 생성
- 클립보드 복사 (navigator.clipboard 또는 fallback)
- Toast 알림 ("Slack 페이스트 복사 완료")

### 출력 포맷
```markdown
**[프로젝트명] 미팅 요약 (YYYY-MM-DD)**
_시리즈 series_id / N차_

**참석:** [참석자]

**결정사항**
- [최대 3건]

**Action**
- (Owner) Action — Due

**다음:** 다음 미팅 (...)

_(미결 N건 / 리스크 N건)_

**전략 코멘트:** [Internal 모드 한 줄]

---
_[Internal] 외부 공유 금지_  또는  _본 요약은 양측 공유용입니다._
```

### 활용 시나리오
- Slack 팀 채널 페이스트
- Email 보고용
- 카카오톡·텔레그램 그룹 공유
- Notion 회의록 페이지 헤더

---

## 3. 부가 기능 2: PDF 저장 (대시보드 내 버튼)

### 동작
- "📄 PDF 저장" 버튼 클릭
- 안내 토스트 표시 ("인쇄 대화상자에서 PDF로 저장 선택")
- `window.print()` 호출
- 사용자가 인쇄 대화상자에서 PDF 저장 옵션 선택

### @media print 자동 적용
- 헤더·툴바·탭·필터 숨김
- 패널 페이지 브레이크 회피
- Kanban 4컬럼 → 2컬럼 (인쇄 가독성)
- 컬러 → 흑백 친화 변환

### 활용 시나리오
- **Type C 발주처 공식 송부** (워드 .docx 대체)
- 임원 종이 보고
- 인쇄·보관 의무 미팅
- 클라이언트 이메일 첨부 (PDF 표준 친숙도 ↑)

---

## 4. 부가 기능 3: JSON 백업 (대시보드 내 버튼)

### 동작
- "💾 JSON 백업" 버튼 클릭
- 전체 대시보드 데이터 + 시리즈 누적 데이터 통합 JSON 다운로드
- 파일명: `mice-mtg_[프로젝트]_[YYYY-MM-DD].json`

### 데이터 스키마
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
  "_seriesHistory": [...]
}
```

### 활용 시나리오
- 챗 환경 리셋 대비 외부 백업 (Google Drive·Notion)
- 다른 환경에서 대시보드 복원
- 시리즈 데이터 영속화 보강

---

## 5. 부가 기능 4: 시리즈 저장 (대시보드 내 버튼)

### 동작
- 시리즈 모드 활성화 시에만 표시
- "↻ 시리즈 저장" 버튼 클릭
- 본 회차 데이터를 `window.storage`에 저장 (`mice-mtg:[series_id]` 키)
- 누적 통계 자동 갱신

### 저장 데이터
- 본 회차 8축 데이터 전체 (data_snapshot)
- 회차 통계 (신규·carry-over·DONE·BLOCKED·완료율)

### 다음 회차 활용
- 동일 series_id로 다음 회차 빌드 시
- `load_series_carry_over()` 함수가 미완료 Action 자동 carry-over
- 차트에 회차 추가 표시

---

## 6. 자동 동기화 산출물

### `.series-data/[series_id].json` (서버 사이드 백업)
- 시리즈 모드 활성 시 빌드 직후 자동 생성
- `build_dashboard.py`의 `sync_series_data()` 함수
- window.storage와 별개로 서버 측 영속화

### `.chaining/[client_id]_[YYYYMMDD]_to_proposal.json` (체이닝 패키지)
- Type A 외부 클라이언트 + Discovery·킥오프 시
- mice-proposal 입력으로 자동 변환
- 상세는 `references/chaining-guide.md`

---

## 7. 산출물 생성 순서

```
1. parse_input.py                    → 정규화 transcript + 화자 매핑
   ↓
2. (8축 추출 — Claude 본체)
   ↓
3. build_dashboard.py                → HTML 대시보드 (메인)
   ├─ assets/dashboard-template.html 로드
   ├─ JSON 데이터 주입 (INITIAL_DATA)
   ├─ 페이지 제목 주입 (TITLE)
   └─ 단일 .html 파일 생성
   ↓
4. sync_series_data()                → .series-data/*.json (시리즈 모드)
   ↓
5. (Type A·Discovery 시) chaining JSON → .chaining/*.json
   ↓
6. validate_dashboard_html()         → 자동 검증
   ↓
7. present_files                     → dashboard.html 1개만 노출
```

→ **사용자에게 노출되는 메인 산출물은 .html 1개**. .json 파일들은 백엔드 동기화로 자동 처리.

---

## 8. 산출물 검증 체크리스트

생성 직후 자동 검증:

| 체크 항목 | 통과 기준 |
|-----------|----------|
| HTML 파일 존재 | 정상 생성 |
| 파일 크기 | 50KB 이상 |
| 플레이스홀더 치환 | `{{TITLE}}`·`{{INITIAL_DATA}}` 잔존 없음 |
| React 라이브러리 연결 | `react@18` 또는 `React` 매칭 |
| Recharts 라이브러리 연결 | `recharts` 매칭 |
| jc-design-system 토큰 | 5색 시그니처 모두 적용 (#0A2540·#2962FF·#FF5722·#E91E63·#00E676) |
| Action Items 수 | 1개 이상 (0개면 "Action 미식별" 경고) |
| 결정사항 수 | 1개 이상 (0개면 "결정사항 미식별" 경고) |
| Owner 미정 비율 | 30% 이하 (초과 시 재확인 권장) |
| Due 미정 비율 | 30% 이하 |
| External 모드 Redaction | 적용 여부 확인 |
| 시리즈 carry-over | `--series` 모드 시 누적 표시 확인 |

→ 검증 실패 시 사용자에게 경고 출력 후 산출물은 생성하되 "검토 권장" 플래그 부착.

---

## 9. v1 → v2 산출물 변경 매트릭스

| v1 산출물 | v2 처리 | 사용자 영향 |
|----------|---------|------------|
| .docx 회의록 | ❌ 폐기 | PDF 저장 버튼으로 대체 |
| .xlsx Action Items 트래커 | ❌ 폐기 | 대시보드 내 칸반 + JSON 백업으로 대체 |
| .md 공유 요약 | ❌ 파일 폐기 | 대시보드 내 Slack 페이스트 버튼으로 대체 |
| .internal-backup | ❌ 폐기 | 대시보드 내 모드 토글로 대체 (실시간 전환) |
| .next-agenda | (v2.1 후보) | 대시보드 내 자동 생성 기능으로 통합 예정 |

→ v2 사용자는 산출물이 1개로 통합되어 다운로드·관리·공유 모두 단일 파일로 가능.
