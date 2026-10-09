# Output Spec — 산출물 사양

한 번의 입력으로 **HTML 회의록 대시보드 1개**를 만든다. Slack 페이스트·PDF 저장·JSON 백업·시리즈 저장은 대시보드 안의 버튼이다.

---

## 1. 메인 산출물 — HTML 대시보드

```
dashboard_[프로젝트]_[YYYYMMDD].html
```

예: `dashboard_a사-discovery_20260509.html` · `dashboard_b사-regular26_20260509.html` · `dashboard_team-weekly_20260509.html`

- HTML/CSS/JS 한 파일. React·Recharts는 CDN(버전 고정), 로고 2종은 data URI로 내장.
- 크기 약 95KB(템플릿 + 로고 + 데이터). 데스크톱 1280px 최적, 모바일 반응형.
- 구조: 헤더(킥커·제목·로고 슬롯·토글) → KPI 4장 → 탭 → 하단 툴바. 상세 `dashboard-spec.md`.

---

## 2. 부가 기능 (대시보드 버튼)

| 버튼 | 동작 | 활용 |
|------|------|------|
| Slack 페이스트 | 200~600자 마크다운 요약을 클립보드로 | 팀 채널·메일 본문 붙여넣기 (게시는 사용자) |
| PDF 저장 | `window.print()` — 인쇄는 라이트 강제 | Type C 발주처 공식 송부, 종이 보고 |
| JSON 백업 | 회차 데이터 + 시리즈 누적 다운로드 | 세션 리셋 대비, 다른 환경에서 재빌드 |
| ↻ 시리즈 저장 | `mice-mtg:[series_id]`에 본 회차 저장 | 회차별 완료율 추이 누적 |

Slack 페이스트 포맷:

```markdown
**[프로젝트명] 미팅 요약 (YYYY-MM-DD)**
_시리즈 series_id / N차_

**참석:** [참석자]

**결정사항**
- [최대 3건]

**Action**
- (Owner) Action — Due

**다음:** 다음 미팅 (...)

_(미결 N건 / 리스크 N건 — 회의록 본문 참조)_

**전략 코멘트:** [Internal 모드 한 줄]

---
_[Internal] 외부 공유 금지_  또는  _본 요약은 양측 공유용입니다._
```

---

## 3. 자동 동기화 산출물

| 파일 | 조건 | 생성 |
|------|------|------|
| `.series-data/[series_id].json` | `--series` | `build_dashboard.py` `sync_series_data()` |
| `.chaining/[project]_[YYYYMMDD]_to_[target].json` | Discovery·킥오프·회고 + 조건 충족 | ChainPayload/v1 (`chaining-guide.md`) |

---

## 4. 생성 순서

```
1. python scripts/parse_input.py transcript.txt --mapping "..."    → 정규화 transcript
2. (Claude) 유형·모드 판정 + 8축 추출                               → minutes.json (DashboardData 필드)
3. python scripts/build_dashboard.py --input minutes.json --out <폴더>
   ├─ SoT 토큰 로드(jc_tokens.py) → @design-tokens 블록 교체
   ├─ BRAND(발행 명의·발주처 슬롯·로고) · INITIAL_DATA 주입
   ├─ .series-data 동기화 (시리즈 모드)
   └─ validate_dashboard_html() 자동 검증
4. (조건 충족 시) .chaining/*.json
5. 사용자에게 HTML 경로 1개 + 고른 기본값 + 확인 필요 목록 전달
```

입력 JSON 예시는 `python scripts/build_dashboard.py --dump-sample sample.json`.

---

## 5. 검증 체크리스트

| 항목 | 기준 |
|------|------|
| HTML 생성 · 크기 | 40KB 이상 |
| 플레이스홀더 | `{{TITLE}}` · `{{INITIAL_DATA}}` · `{{BRAND}}` 잔존 0 |
| 라이브러리 | React · Recharts 연결 |
| 디자인 토큰 | SoT 라이트·다크 값 주입, 인쇄 라이트 블록, legacy 색 0 |
| Action Items | 1개 이상 (0개면 "Action 미식별" 경고) |
| 결정사항 | 1개 이상 (0개면 "결정사항 미식별" 경고) |
| Owner · Due 미정 비율 | 각 30% 이하 |
| External 모드 | Redaction 적용 여부 |
| 시리즈 | `--series` 시 carry-over 표시 |
| 식별정보 | 발주처 실명은 슬롯, 개인 연락처 0 (RULE-NO-COMPANY) |

검증 실패여도 산출물은 남기고 "검토 필요"로 보고한다. 발주처 송부본은 jc-redteam Quick 검수 권장.
