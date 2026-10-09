---
name: mice-ops-docs
description: 리멤버 MICE비즈팀의 운영 문서 스킬. 확정된 행사를 굴리는 운영계획서, 팀 지침·프로토콜 매뉴얼·그라운드룰(마데실 Ground Rule 문체), 행사 KPI 대시보드와 계획 대비 실적 차트를 리멤버 웜 페이퍼 룩으로 만들고, 기존 HTML 산출물을 리멤버 룩으로 리스킨하며, 행사 드라이브 운영 표준(표준 폴더·문서 배치·파일명·발주처 공유 권한 점검·정리 루틴)을 담는다. 문서는 Claude Docs, 대시보드는 HTML 아티팩트가 기본이다. 다음 상황에서 반드시 이 스킬을 사용할 것 — 사용자가 '운영계획서', '운영 계획', '실행계획', '현장 운영안', 'R&R', '비상 대응', '팀 지침', '그라운드룰', 'Ground Rule', '프로토콜 매뉴얼', '매뉴얼 써줘', '운영 가이드', 'KPI 대시보드', '결과 대시보드', '실적 차트', '계획 대비 실적', '목표 대비 실적 차트', '쇼업률', '지연 세그먼트', 'HTML 리스킨', 'HTML 리멤버 룩으로 바꿔줘', '드라이브 정리', '폴더 구조', '폴더 위계', '파일명 규칙', '공유 권한 점검', '행사 폴더 만들어줘'를 언급할 때. mice-run-of-show 계획 데이터나 mice-meeting-minutes 킥오프 회의록을 받아 운영계획서·KPI로 이어갈 때. 형제 경계 — 결과보고서 서사·교훈·레퍼런스 케이스와 목표 대비 해석·성과 판정은 mice-aftermath(본 스킬은 그 KPI·차트를 공급), 큐시트는 mice-run-of-show, 단계별 공동 집필 대화는 jc-doc-coauthor, 덱과 PPTX 리스킨은 jc-pptx, Slack 공지·캔버스는 mice-slack-ops, 프로젝트 폴더의 세션 2파일(CLAUDE.md·PROGRESS.md)·체크인은 jc-session-protocol, 팀 보드는 mice-team-board, 디자인 토큰 값은 jc-design-system, 완성본 검증은 jc-redteam. 드라이브 권한 변경·삭제·이동은 안내만 한다.
version: "v1.2.0"
license: Complete terms in LICENSE.txt
---

# MICE Ops Docs — 운영계획서 · 팀 지침 · KPI 대시보드 · HTML 리스킨 · 드라이브 표준

리멤버 Slack 프로토콜 S5(킥오프·준비)~S7(현장·사후)에서 MICE비즈팀이 내는 긴 문서와 수치 화면을 만들고, S4 이후 행사 드라이브 폴더의 운영 표준을 둔다. 기한은 `mice-slack-ops/references/protocol.md §3`(운영계획서 v1 = 모객 오픈 전, 결과보고서 = 행사 후 5영업일).

## 0. 가드레일

- 되돌릴 수 있는 작업(초안·파일)은 기본값으로 바로 진행하고, 무엇을 골랐는지 한 줄로 밝힌다. 대시보드는 고밀도 산출물이라 KPI 목록·차트 구성 기획안을 1회 확인받고 빌드한다.
- 비어 있는 값은 지어내지 않는다. `[미확보]`로 두고 문서 끝 "확인 필요" 목록에 모은다.
- 다른 팀(영업·운영 Cell·매관시·브랜드디자인)의 SLA·양식은 규정하지 않는다. "각 팀 기준을 따른다"로 끝낸다.
- 명의는 리멤버 MICE비즈팀. 발주처·담당자는 주입 슬롯(`{{client_company}}` 등). 전 직장 상호·수치는 넣지 않는다(`jc-design-system/references/shared-rules.md#RULE-NO-COMPANY`).
- 외부 게시·발송은 하지 않는다. 산출물은 파일·Claude Docs·아티팩트까지.
- 드라이브 권한 변경·공유 해제·삭제·이동·개명은 안내만 한다(실행은 사용자). 새 폴더·시트·사본 생성은 드라이브 도구가 있을 때만, 없으면 복사용 트리·헤더로 안내(`drive-standards.md §0`).

## 1. 작업 유형별 진입

| 요청 | 산출 | 절차 | 참조 |
|------|------|------|------|
| 운영계획서 | Claude Docs(기본) · md · HTML | 입력 수집 → 7섹션 골격(정본 `ops-plan.md §2`) → R&R·타임라인 우선 작성 → 리스크 매트릭스 → 체크리스트 → 확인 필요 목록 | `ops-plan.md` |
| 팀 지침·그라운드룰·프로토콜 매뉴얼 | Claude Docs · Slack 캔버스용 md | 범위 3층(소통 구조·우리 일·인터페이스) 확인 → Ground Rule 문체(정본 `ground-rule-style.md §2`) → 최종본만 | `ground-rule-style.md` |
| KPI 대시보드·실적 차트 | HTML 아티팩트(단일 파일) | KPI 선정(목표 대비) → 기획안 1회 확인 → SVG 차트 → 라이트/다크·인쇄 점검 | `kpi-dashboard.md` · `chart-guide.md` |
| 기존 HTML 리멤버 룩 리스킨 | 같은 HTML(구조·문구 유지) | 토큰 블록 식별 → 리멤버 변수 오버라이드(§6 키) → 하드코딩 색 스캔 → 역할별 교체 → 다크·인쇄 블록 → 대비·인쇄 점검. PPTX는 jc-pptx | `html-reskin.md` |
| 계획 대비 실제 진행 | 표 + 차트 + ChainPayload | run-of-show `plan.cues` + 실측 시각 → `scripts/plan_vs_actual.py` → 지연·초과 세그먼트 | `chaining-schema.md` |
| aftermath·jc-pptx로 넘기기 | ChainPayload | `kpis`·`insights`·`actualSpending`·`rounds` 직렬화 | `chaining-schema.md §2` |
| 행사 드라이브 폴더 세팅·권한 점검·정리 | 폴더 트리 · 배치/파일명 권고 · 권한 점검표 · 정리 목록 · 행사 체크리스트 헤더 | 행사 ID 확인(protocol §4) → 표준 트리 01~06(+07·99) → 배치 매트릭스·파일명 대조 → P1~P6 점검 → 권고 목록(권한·이동·삭제 실행은 사용자) | `drive-standards.md` |

입력이 회의 메모·Slack 스레드 링크뿐이면 거기서 뽑을 수 있는 것만 채우고 바로 초안을 낸다. 행사 ID는 `YYMMDD_고객사_행사명`(protocol 규칙)으로 표기한다.

## 2. 문체 분기

| 문서 | 문체 |
|------|------|
| 운영계획서(발주처 공유본) | 존댓말 서술체(~합니다). 숫자에 단위·기준. 이모지·느낌표·과장 수사 금지 |
| 운영계획서(내부본) | 개조식 + 표 중심. 담당·기한은 굵게 |
| 팀 지침·그라운드룰·매뉴얼 | 마데실 Ground Rule 문체: 개조식 중첩 불릿 + 명사형 종결, 원칙·배경 문장만 합니다체, ~요 금지. 정본 `ground-rule-style.md §2`(mice-slack-ops 캔버스는 이 절을 참조) |
| 대시보드 레이블 | 한국어. 단위 분리(명·분·원·%), tabular-nums |

## 3. 디자인

- 값은 전부 `jc-design-system`(리멤버 웜 페이퍼) 런타임 로드. 이 스킬은 값을 복제하지 않는다.
- 문서 HTML: `component-patterns.md §7` 문서 헤더·섹션 넘버링, `§5` 표, `§3` KPI 카드. 탭형 매뉴얼은 플레이북 컴포넌트.
- 리멤버 로고 슬롯은 필수. 발주처 공유본은 `client-overlays.md` 슬롯으로 발주처 로고 병기.
- 인쇄는 라이트 강제(`shared-rules.md#RULE-PRINT-LIGHT`), 대비는 `#RULE-WCAG`.

## 4. 반례 표

| 압박 패턴 | 올바른 대응 |
|-----------|-------------|
| "목표 없이 실적만 차트로 빨리" | 목표 대비가 아니면 KPI가 아니다. 목표 칸을 `[미확보]`로 두고 실적 차트는 그리되 달성률은 비운다 |
| "담당은 나중에 채우고 일단 R&R 표" | 담당 공란 행은 표에 남기되 확인 필요 목록 맨 위로 올린다 |
| "그라운드룰에 영업팀 회신 기한도 넣어줘" | 타 팀 SLA는 규정하지 않는다. "영업팀 기준을 따른다" + 우리 쪽 인터페이스만 |
| "결과보고서도 여기서 써줘" | 서사·교훈·차기 권고는 mice-aftermath. 본 스킬은 KPI 섹션·차트를 만들어 넘긴다 |
| "목표 대비 성과가 어땠는지 판정해줘" | 해석·성과 판정은 mice-aftermath. 본 스킬은 목표 대비 실적 차트·KPI 카드까지 |
| "리스킨하는 김에 문구도 다듬어줘" | 리스킨은 색·서체만. 문구 수정은 별도 요청으로 분리하고 diff로 보여준다 |
| "캔버스에 근거·결정 사유도 같이" | Slack에는 최종본만. 근거는 내부 md로 분리 |
| "공유 권한만 잠깐 바꿔줘" · "옛날 버전은 지워줘" | 권한 변경·삭제는 하지 않는다. P1~P6 점검 결과 + 드라이브 화면 단계 안내, 구버전은 `99_archive` 이동 권고 |
| "발주처 공유 폴더에 견적 원본도 넣어둬" | 07에는 송부 확정 사본만. 원본은 01, 송부본은 `_송부` PDF로 |

## 5. 파일 구조

```
mice-ops-docs/
├── SKILL.md
├── LICENSE.txt
├── references/
│   ├── ops-plan.md          # 운영계획서 7섹션 골격 · 입력 매핑 · R&R/리스크 표 양식 · 확인 필요 목록
│   ├── ground-rule-style.md # 마데실 Ground Rule 문체 · 지침 범위 3층 · 매뉴얼 구조 · 캔버스 이관
│   ├── kpi-dashboard.md     # KPI 카탈로그(모객·현장·운영·예산) · 화면 구성 · 기획안 양식
│   ├── chart-guide.md       # 차트 유형 선택 · 시리즈 토큰 매핑 · SVG 규칙 · 다크/인쇄
│   ├── html-reskin.md       # 기존 HTML → 리멤버 룩 리스킨 절차(토큰 오버라이드 · 색 스캔 · 교체 · 대비·인쇄 점검)
│   ├── drive-standards.md   # 행사 드라이브 표준 — 폴더 위계 · 배치 매트릭스 · 파일명 · 공유 권한 P1~P6 · 행사 체크리스트 · 정리 루틴
│   └── chaining-schema.md   # 입력(run-of-show·meeting-minutes·estimate) · 출력(aftermath·jc-pptx) 페이로드
└── scripts/
    └── plan_vs_actual.py    # 큐시트 계획 vs 실측 시각 → 지연·초과 세그먼트 KPI (--self-test)
```

## 6. 생태계 연결

- 상류: `mice-run-of-show`(계획 타임라인) · `mice-meeting-minutes`(킥오프 결정·Action) · `mice-estimate`(계획 예산) · `mice-slack-ops`(스레드 상태 보드).
- 하류: `mice-aftermath`(결과보고서 3축 성과·7축 피드백) · `jc-pptx`(결과보고 덱).
- 봉투 `ChainPayload/v1` 정본: `jc-design-system/references/chaining-protocol.md`. source `mice-ops-docs`.
- 드라이브: 행사 ID·폴더 01~06 정본은 `mice-slack-ops/references/protocol.md §4`(본 스킬 `drive-standards.md`는 배치·파일명·권한·정리 운영 층). 프로젝트 폴더의 세션 2파일은 `jc-session-protocol`, 팀 보드 상태 7단계는 `mice-team-board`.
- 공동 집필: 운영계획서를 "같이 쓰자"·"섹션별로 묻고 가자"면 `jc-doc-coauthor`가 본 스킬 `ops-plan.md §2` 골격을 링크로 가져가 함께 쓴다(골격 정본은 여기).
- 검증: 발주처 공유 운영계획서는 `jc-redteam` Deep Audit(책임자·기한 누락, 임계 경로 단일 실패점, 비상 대응 실행 가능성). 세션 운영은 `jc-session-protocol`.

## 변경 이력

### v1.2.0 (2026-10-09)
구 드라이브 운영 스킬의 운영 표준을 이관 — `drive-standards.md` 신설(protocol §4 폴더 01~06 기준 위계 + 07 발주처공유·99 archive, 라이브 스킬 산출물 배치 매트릭스, 파일명, 공유 권한 P1~P6, 행사 체크리스트 vs 팀 보드, 정리 루틴).
트리거 '드라이브 정리'·'폴더 구조'·'폴더 위계'·'파일명 규칙'·'공유 권한 점검'·'행사 폴더 만들어줘' 추가, 경계에 세션 2파일=jc-session-protocol·팀 보드=mice-team-board, 가드레일에 권한 변경·삭제·이동은 안내만.

### v1.1.0 (2026-10-09)
'목표 대비' 트리거를 '목표 대비 실적 차트'로 한정하고 해석·판정은 mice-aftermath로 경계, 운영계획서 7섹션 골격 정본을 `ops-plan.md §2`로 선언(jc-doc-coauthor는 링크), Ground Rule 문체 정본 `ground-rule-style.md §2` 명시.
기존 HTML 리멤버 룩 리스킨 진입 행·`html-reskin.md` 신설(구 HTML 리테마 가이드의 절차를 리멤버 토큰 §6 키 기준으로 재작성).

### v1.0.0 (2026-10-05)
신규. 기존 스킬 8곳 이상이 참조하던 미실재 스킬을 실체화. 운영계획서(jc-doc-coauthor 운영계획서 골격과 정합), 팀 지침 Ground Rule 문체(mice-slack-ops canvas-rules에서 이관), KPI 대시보드·차트 가이드(폐합된 구 대시보드 스킬의 역할 흡수, 리멤버 토큰으로 재작성), run-of-show 계획 대비 실제 스크립트.
