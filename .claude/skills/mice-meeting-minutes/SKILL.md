---
name: mice-meeting-minutes
description: MICE 행사 기획·운영 과정의 미팅 메모·텍스트 transcript·구술 정리를 입력받아 8축 프레임(안건·발언요지·결정사항·Action Items·리스크·미결사항·후속일정·전략메모)으로 구조화한 인터랙티브 HTML 대시보드를 생성하는 스킬. 대시보드는 KPI 카드·Action 칸반·시리즈 누적 차트·전략 메모 5W1H 카드를 단일 파일로 통합하며, Slack 페이스트·PDF 저장·JSON 백업 옵션을 제공한다. 다음 상황에서 반드시 이 스킬을 사용할 것 사용자가 '회의록', '미팅록', '미팅 노트', '회의 정리', '회의 요약', '미팅 정리', 'Action Items', '액션 아이템', '후속 조치', '팔로업', 'follow-up', 'Discovery Meeting 정리', '킥오프 미팅 정리', '정기 미팅 정리', '발주처 협의 기록', '사전답사 기록', '협력사 미팅 정리'를 언급할 때. 클로바노트·Otter·Whisper·Zoom·Google Meet·Microsoft Teams 등에서 추출한 transcript 텍스트를 업로드하며 '정리해줘', '구조화해줘', '회의록으로 만들어줘', 'Action 뽑아줘', '대시보드로 만들어줘'를 요청할 때. 외부 클라이언트 송부용/내부 보관용 톤 분기 지원. 정기 미팅 시리즈 모드로 회차 누적 추적 가능 (window.storage 영속화). 본 스킬의 산출물은 mice-proposal 스킬의 입력으로 체이닝 가능 (Discovery 회의록에서 고객 니즈·예산·일정 자동 추출). 단, '발표 스크립트', '발표 대본', 'PT 멘트', 'MC 멘트'는 pt-script 영역이므로 사용하지 말 것. '제안서'는 mice-proposal, '견적서'는 mice-estimate, '행사 결과 KPI 대시보드'는 mice-dashboard 영역. 음성 파일 자체 STT는 본 스킬 범위 밖 — 클로바노트·Otter·Whisper 등 외부 도구로 텍스트 변환 후 입력.
version: "v2.1.0"
---

# mice-meeting-minutes (v2.1.0)

MICE 행사 기획·운영 미팅을 18년 경력 전략가 시각의 8축 프레임으로 구조화하여 **인터랙티브 HTML 대시보드**로 즉시 시각화·추적·공유하는 스킬.

## 버전 히스토리

| 버전 | 일자 | 변경 사항 |
|------|------|----------|
| v1 | ~2026-04 | .docx 회의록 + .xlsx Action 트래커 (정적 산출물) |
| v2 | 2026-05 | HTML 단일 파일 대시보드 (인터랙티브) + External/Internal 토글 + window.storage 시리즈 영속화 |
| **v2.1.0** | **2026-05-27** | **라이트/다크 모드 토글 추가** + **JSON 자동 백업 옵션 강화** + jc-design-system DARK_* 토큰 매핑 (mice-proposal v2.1.1 / mice-sponsor-deck v2.1.0 / mice-dashboard v2.0 일관) |

### v2 → v2.1.0 변경 요약 (5줄)
1. 대시보드 우상단에 **테마 토글** (라이트/다크) 추가. External/Internal 토글과 독립 동시 작동
2. `[data-theme="dark"]` CSS 변수 셀렉터로 8축 KPI 카드·Action 칸반·차트·전략 메모·헤더·테이블 일괄 다크 매핑
3. **localStorage 영속화** (`mm-theme`) + `prefers-color-scheme` 시스템 설정 자동 감지 (첫 방문)
4. **인쇄 시 라이트 강제** (`@media print`) + 토글 버튼 숨김 처리
5. 우상단 **"JSON 백업 다운로드"** 버튼이 시리즈 데이터를 `mm-series-backup-YYYYMMDD.json` 파일로 자동 저장 (window.storage 외부 영속화 보강)

## 1. 본 스킬이 다루는 것 / 다루지 않는 것

### 다루는 것 (DO)
- 미팅 transcript의 8축 추출 + 인터랙티브 대시보드 빌드
- 5종 회의 유형(외부 클라이언트 / 내부 팀 / 발주처 공식 / 사전답사 / 협력사) 톤·구조 자동 분기
- 외부 송부용(`--external`) / 내부 보관용(`--internal`) 모드 전환
- **라이트/다크 테마 토글** (v2.1.0 신규) — External/Internal과 독립
- Action Items 칸반 보드 (TODO·DOING·BLOCKED·DONE) + 우선순위·Due 자동 표시
- 정기 미팅 시리즈 누적 추적 (회차별 완료율 차트 + carry-over 자동 처리)
- 민감 발언 redaction 룰 자동 적용 (External 모드)
- Discovery Meeting 회의록 → mice-proposal 체이닝 JSON 자동 생성
- 4채널 입력(클로바노트 / Otter·Whisper·Zoom·Meet·Teams / 메모형 / 구두 보고) 자동 인식
- Slack 페이스트(클립보드) / PDF 저장(브라우저 인쇄) / **JSON 백업 다운로드** (v2.1.0 강화)

### 다루지 않는 것 (DON'T)
- 발표 사전 스크립트 작성 (→ pt-script)
- **음성 파일 자체 STT** — Claude는 오디오 처리 불가. 클로바노트·Otter·Whisper 등 외부 도구로 텍스트 변환 후 입력
- 손글씨 사진 OCR (→ 별도 OCR 도구 활용 후 텍스트로 입력)
- 제안서 본문 작성 (→ mice-proposal)
- 견적서 작성 (→ mice-estimate)
- **행사 결과 KPI 대시보드** (→ mice-dashboard) — 본 스킬은 사전·운영 미팅 추적, mice-dashboard는 사후 결과 분석

## 2. 호출 시점 판단 가이드

| 사용자 입력 | 본 스킬 호출 | 사용 스킬 |
|------------|------------|----------|
| "이 미팅 정리해줘" + 메모 | ✅ | mice-meeting-minutes |
| "회의록 만들어줘" + 클로바노트 transcript | ✅ | mice-meeting-minutes |
| "미팅 대시보드로 만들어줘" | ✅ | mice-meeting-minutes |
| "Action Items 칸반으로 보여줘" | ✅ | mice-meeting-minutes |
| "Discovery Meeting 정리" | ✅ | mice-meeting-minutes |
| "사전답사 기록 작성" | ✅ | mice-meeting-minutes |
| "발표 멘트 만들어줘" | ❌ | pt-script |
| "제안서 만들어줘" | ❌ | mice-proposal |
| "견적 뽑아줘" | ❌ | mice-estimate |
| "행사 결과 분석 대시보드" | ❌ | mice-dashboard |
| 음성 파일(.m4a/.mp3) 단독 업로드 | ❌ 처리 불가 | (외부 STT 안내) |

## 3. 표준 워크플로우

```
[미팅 진행]
    ↓
외부 STT 도구 (클로바노트 / Otter / Whisper / Zoom·Meet·Teams)
    ↓
[transcript 텍스트 export]
    ↓
Claude에 텍스트 입력 + 호출 + 화자 매핑
    ↓
[scripts/parse_input.py]
    ├─ 4채널 입력 형식 자동 인식
    ├─ 화자 라벨 정규화 + 매핑 적용
    ├─ 30분 단위 청크 분할 (긴 transcript)
    └─ Redaction 사전 힌트 부착
    ↓
[references/meeting-types.md] 5종 유형 자동 추정 (수동 지정 우선)
    ↓
[references/analysis-framework.md] 8축 추출 (Claude 본체)
    ↓
[references/redaction-rules.md] 모드별 민감 발언 처리
    ↓
[references/action-items-schema.md] Action 5열 표준화 + Priority/Due 자동 추정
    ↓
[scripts/build_dashboard.py] ⭐ HTML 대시보드 생성
    ├─ assets/dashboard-template.html에 JSON 데이터 주입
    ├─ jc-design-system 시그니처 토큰 인라인 (라이트 + 다크 변수)
    └─ React + Recharts CDN 호출 단일 파일
    ↓
[--series 모드] .series-data/[series_id].json 동기화 (carry-over 처리)
    ↓
[Discovery 유형 + GO 흐름] mice-proposal 체이닝 JSON 자동 생성
    ↓
present_files: dashboard_[프로젝트]_[YYYYMMDD].html (메인 산출물 1개)
```

## 4. 입력 채널 4종 (input-formats.md 상세)

| 채널 | 입력원 | 정확도 | 권장도 |
|------|--------|--------|--------|
| **Ch1** | 클로바노트 export (화자+타임스탬프) | 최고 | ★★★★★ |
| **Ch2** | Otter·Whisper·Zoom·Meet·Teams export | 높음 | ★★★★☆ |
| **Ch3** | 메모형 자유 텍스트 | 중간 (발화자 추정) | ★★★☆☆ |
| **Ch4** | 채팅창 직접 구두 보고 | 중간 | ★★★☆☆ |

→ 6종 export 포맷별 파서 사양은 `references/input-formats.md`.

## 5. 산출물 사양 — 단일 HTML 대시보드

### 파일명 규칙
```
dashboard_[프로젝트]_[YYYYMMDD].html
```

예시:
- `dashboard_darktrace-discovery_20260509.html`
- `dashboard_rmb-rebuild26_20260509.html`
- `dashboard_internal-weekly_20260509.html`

### 대시보드 구조 (v2.1.0)

```
┌────────────────────────────────────────────────────────────┐
│  [Header] Deep Navy Band — 다크 모드 시 #0A2540              │
│  프로젝트명 · 미팅일 · 시리즈 N차                            │
│  우상단 컨트롤: [Internal | External] [☀ | ☾]               │
├────────────────────────────────────────────────────────────┤
│  [KPI Cards 4] (다크 모드 시 #1A3556 배경)                   │
│  결정사항 / Action 총개 / 미결 사항 / 완료율 (%)             │
├────────────────────────────────────────────────────────────┤
│  [Tabs]                                                     │
│  본 미팅 · Action 트래커 · 시리즈 누적 · 전략 메모          │
│                                                             │
│  [본 미팅 탭] (디폴트)                                       │
│    안건·발언 요지·결정사항·리스크·미결·후속 일정 6패널       │
│                                                             │
│  [Action 트래커 탭]                                          │
│    Status 분포 도넛 + Owner별 Bar 차트 (다크 자동 매핑)      │
│    필터: 검색·Priority·Owner                                │
│    Kanban 4컬럼 (TODO/DOING/BLOCKED/DONE)                  │
│    Status 변경 (드롭다운) — window.storage 자동 저장        │
│                                                             │
│  [시리즈 누적 탭] (--series 모드만)                          │
│    회차별 완료율 LineChart + Action 분포 BarChart            │
│    회차 누적 통계 표 + 본 회차 시리즈 저장 버튼              │
│                                                             │
│  [전략 메모 탭] (Internal 모드만)                            │
│    5W1H 6질문 카드 (Who·What·When·Where·Why·How)           │
├────────────────────────────────────────────────────────────┤
│  [Toolbar Footer] (다크 모드 시 동일 Deep Navy 유지)         │
│  💬 Slack 페이스트  📄 PDF 저장  💾 JSON 백업  ↻ 시리즈 저장│
└────────────────────────────────────────────────────────────┘
```

### 기술 스택
- **단일 HTML 파일** — 다운로드·로컬 실행 가능
- **React 18 + Recharts 2.12** — CDN 호출 (인터넷 환경 필요)
- **Babel Standalone** — 브라우저 내 JSX 트랜스파일
- **window.storage / localStorage** — 시리즈 데이터 영속화
- **Pretendard / Inter / JetBrains Mono** — 한글·영문·코드 폰트
- **CSS 변수 + `[data-theme]` 셀렉터** (v2.1.0 신규) — 라이트/다크 동시 정의

### 영속화 룰
- 시리즈 모드 활성 시 `mice-mtg:[series_id]` 키로 회차별 데이터 자동 저장
- 챗 환경 리셋 대비 JSON 다운로드 버튼으로 외부 백업 권장
- `.series-data/[series_id].json` 파일도 동시 생성 (서버 사이드 백업)
- **테마 선호도** `mm-theme` 키로 localStorage 영속화 (v2.1.0)

## 6. 모드 분기

### 6-1. External / Internal 모드 (콘텐츠 톤)

| 모드 | 톤 | Redaction | 전략 메모 탭 | 토글 위치 |
|------|----|-----------| -----------|----------|
| `--external` | 정중·사실 위주 | 자동 적용 | 비활성화 | 헤더 우상단 |
| `--internal` (기본) | 솔직한 평가 | 미적용 | 활성화 (5W1H) | 헤더 우상단 |

→ **모드는 대시보드 우상단 토글로 실시간 전환 가능**. 빌드 직후 사용자가 토글하면 전략 메모 탭 표시·익명화 자동 반영.

### 6-2. 라이트 / 다크 테마 토글 (v2.1.0 신규)

| 테마 | 페이지 배경 | 카드 배경 | 본문 | 보조 | 액센트 |
|------|------------|----------|------|------|--------|
| **라이트** (기본) | #F5F7FA | #FFFFFF | #1A1A1A | #808080 | #2962FF |
| **다크** | #0A2540 | #1A3556 | #FFFFFF | #B8C5D6 | #2962FF |

**작동 원리**:
- 우상단 토글 버튼 (☀ ↔ ☾) 클릭으로 즉시 전환
- 첫 방문 시 `prefers-color-scheme: dark` 시스템 설정 자동 감지
- localStorage `mm-theme` 키로 선호도 영속화 (다음 방문 시 자동 복원)
- **인쇄 시 라이트 강제** (`@media print`) — PDF 저장은 항상 라이트 톤 유지
- External/Internal 모드와 **독립적**으로 작동 (4개 조합 모두 가능)

**컬러 매핑 출처**: mice-proposal v2.1.1 `dark-mode-patterns.md` DARK_* 토큰 (DARK_BG = #0A2540 / DARK_BG_ALT = #1A3556 / DARK_TEXT = #FFFFFF / DARK_TEXT_MUTED = #B8C5D6 / DARK_BORDER = #2A4A6E / DARK_ACCENT = #2962FF). mice-sponsor-deck v2.1.0 / mice-dashboard v2.0과 1:1 일관.

**WCAG AA 대비비 검증**:
- 흰색 (`#FFFFFF`) on Deep Navy (`#0A2540`) = **17.4:1** ✓ (목표 4.5:1 충분 초과)
- B8C5D6 on `#0A2540` = 7.5:1 ✓
- 다크 모드 본문 텍스트 가독성 보장

## 7. 시리즈 모드 (`--series`)

```
--series=darktrace-discovery
```

→ 이전 회차 미해결 Action 자동 carry-over + 차회 빌드 시 누적 시트 갱신. 상세는 `references/series-tracking.md`.

### v2.1.0 시리즈 영속화 흐름 (강화)
```
1차 회차 빌드 → 대시보드에서 "시리즈 저장" 클릭 → window.storage 저장
                                                     ↓
[v2.1.0 신규] "JSON 백업 다운로드" 클릭 → 외부 파일로 영구 백업
                                                     ↓
2차 회차 빌드 → 자동 carry-over (이전 회차 미완료 Action) → 대시보드 차트에 누적 표시
                                                     ↓
3차 회차 → carry-over 횟수 3회 도달 시 "장기 미해결" 경고 표시
                                                     ↓
[v2.1.0 신규] JSON 백업 자동 다운로드 옵션 활성 시 매 회차 저장 후 즉시 외부 백업
```

## 8. 시리즈 누적 백업 (v2.1.0 강화)

### 8-1. JSON 백업 다운로드 버튼

대시보드 우상단·하단 툴바 양쪽에 "💾 JSON 백업" 버튼 배치. 클릭 시:

1. 현재 시리즈 데이터(window.storage 또는 localStorage) 전체 추출
2. 파일명: `mm-series-backup-{project}-{YYYYMMDD}.json` (날짜 자동 포함)
3. 브라우저 다운로드 트리거 (Blob + URL.createObjectURL 활용)
4. Toast 알림: "JSON 백업 다운로드 완료"

### 8-2. JSON 백업 파일 구조

```json
{
  "_meta": {
    "backup_date": "2026-05-27T10:30:00+09:00",
    "skill_version": "v2.1.0",
    "project_name": "TOBESOFT TECH FORUM 2026 Discovery",
    "series_id": "ttf2026-discovery"
  },
  "current_session": {
    "meeting_date": "2026-05-09",
    "actions": [...],
    "decisions": [...],
    "pending": [...]
  },
  "series_history": [
    {
      "session_no": 1,
      "date": "2026-05-09",
      "new_actions": 8,
      "carry_over_actions": 0,
      "done": 3,
      "completion_rate": 0.375
    }
  ]
}
```

### 8-3. JSON 복원 워크플로우

1. 다른 챗 세션에서 JSON 파일 업로드
2. Claude에 "이 시리즈 데이터로 N차 회차 대시보드 빌드해줘" 요청
3. `build_dashboard.py`가 `series_history` 로드 + 차트 자동 복원
4. 동일 상태에서 작업 재개 가능

→ 본 영속화 강화로 챗 환경 리셋·다중 디바이스 작업·장기 시리즈 유실 리스크 0건 보장

## 9. 체이닝 (mice-proposal로 전달)

Type A 외부 클라이언트 미팅(Discovery / 정기 협의)에서 추출한 5개 데이터를 mice-proposal 입력 JSON 패키지로 자동 변환. 상세는 `references/chaining-guide.md`.

## 10. jc-design-system 연동

### 10-1. 라이트 모드 토큰

| 적용 영역 | 토큰 |
|----------|------|
| 헤더 띠 | `color.primary` (#0A2540 Deep Navy) |
| KPI 카드 강조 | `color.accent` (#2962FF Electric Blue) |
| Action P0 (블로커) | `color.point.magenta` (#E91E63) |
| Action P1 (금주) | `color.point.orange` (#FF5722) |
| 미결 사항 | `color.point.orange` |
| 리스크 마커 | `color.point.magenta` |
| Status DONE | `color.point.neon` (#00E676) |
| Status BLOCKED | `color.point.magenta` |
| Carry-over 외곽선 | `color.point.orange` |
| 시리즈 차트 라인 | `color.point.neon` (완료율) / `color.accent` (신규) / `color.point.orange` (carry-over) |

### 10-2. 다크 모드 토큰 (v2.1.0 신규)

| 적용 영역 | 토큰 (CSS 변수) | HEX |
|----------|---------------|-----|
| 페이지 배경 | `--bg` | #0A2540 (DARK_BG) |
| 카드 배경 | `--surface` | #1A3556 (DARK_BG_ALT) |
| 보조 서피스 | `--surface-alt` | #12304D (DARK_SURFACE) |
| 본문 글자 | `--text` | #FFFFFF (DARK_TEXT) |
| 보조 글자 | `--text-muted` | #B8C5D6 (DARK_TEXT_MUTED) |
| 비활성 글자 | `--text-disabled` | #6B7B92 (DARK_TEXT_DISABLED) |
| 테두리 | `--border` | #2A4A6E (DARK_BORDER) |
| 강조 테두리 | `--border-strong` | #3D5F87 (DARK_BORDER_STRONG) |
| Accent | `--accent` | #2962FF (DARK_ACCENT, 라이트와 동일) |
| Accent soft (호버) | `--accent-soft` | #1E4DCC |
| 포인트 색상 (P0·DONE·BLOCKED 등) | 동일 유지 | E91E63 / FF5722 / 00E676 |

→ 폰트: Pretendard (KR) / Inter (EN) / JetBrains Mono (코드·ID·숫자) — 양 테마 동일

## 11. 옵션 플래그

| 플래그 | 기능 | 기본값 |
|--------|------|--------|
| `--type=A/B/C/D/E` | 회의 유형 수동 지정 | 자동 추정 |
| `--external` / `--internal` | 모드 지정 | Type A·C → external / B·D·E → internal |
| `--series=<id>` | 시리즈 누적 모드 | OFF |
| `--quote` | 결정 근거 인용 보존 | OFF |
| `--quick` | 핵심 5축만 빠르게 | OFF |
| `--client=<id>` | 클라이언트 오버레이 지정 | personal |
| `--mapping="참석자 1 = 이름"` | 화자 매핑 명시 | 자동 추정 |
| `--theme=light/dark/auto` (v2.1.0) | 초기 테마 지정 | auto (시스템 설정 따름) |

## 12. 산출물 활용 패턴

### 패턴 1: 미팅 직후 즉시 공유 (가장 흔함)
1. 클로바노트 transcript 입력 → 본 스킬 호출
2. 대시보드 다운로드 → 브라우저 열기
3. 모드·테마 확인 → "Slack 페이스트" 클릭 → 팀 채널 즉시 공유

### 패턴 2: 발주처 공식 송부
1. External 모드 + 라이트 테마 빌드
2. 대시보드 → "PDF 저장" → 인쇄 대화상자 "PDF로 저장" (인쇄 시 다크라도 라이트 강제)
3. PDF 발주처 송부 (워드 대체)

### 패턴 3: 시리즈 누적 추적
1. 1차 미팅: `--series=darktrace-discovery` 빌드 → "시리즈 저장" 클릭
2. **"JSON 백업 다운로드"** 클릭 → 외부 폴더(Google Drive)에 영구 보관 (v2.1.0)
3. 2차 미팅: 동일 series_id로 빌드 → carry-over 자동 적용
4. N차 미팅: 회차별 완료율 차트로 진척 시각화

### 패턴 4: 야간·심야 작업 (v2.1.0 신규 활용)
1. 다크 테마 토글 → 눈 피로 감소
2. 동일 작업 흐름. localStorage 영속화로 다음 세션에서 자동 다크 복원
3. 외부 송부 시 자동 라이트 강제 (인쇄)

### 패턴 5: 외부 백업·복원 (v2.1.0 강화)
1. 빌드 직후 "JSON 백업" 클릭 → 외부 폴더(Google Drive)에 저장
2. 다른 환경에서 작업 시 JSON 데이터를 본 스킬에 다시 입력 → 동일 대시보드 복원
3. 시리즈 누적 + 테마 선호도 모두 보존

## 13. 검증 자산 (v2.1.0)

- `_samples/sample_transcript.txt` — TOBESOFT TECH FORUM 2026 Discovery 미팅 가상 transcript (Sprint 3·4 시나리오 연속성)
- v2.1.0 강화 후 본 transcript로 샘플 HTML 대시보드 생성·검수
- 회사 종속 표현 0건 (발주처는 "T社"로 일반화) — 정본: `jc-design-system/references/shared-rules.md#RULE-NO-COMPANY`
