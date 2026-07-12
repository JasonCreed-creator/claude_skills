---
name: mice-proposal
version: "v3.0.1"
description: "MICE 행사 제안서(프레젠테이션)를 자동 생성하는 스킬. RFP, 비딩 공고, 입찰 안내서 등을 입력하면 전시회·박람회·컨퍼런스·포럼·기업행사 등 MICE 행사 유형에 맞는 PPTX 제안서를 자동 구성한다. 다음 상황에서 반드시 이 스킬을 사용할 것: 사용자가 '제안서', '비딩', 'RFP', '입찰', '수주', 'PT 자료', '프레젠테이션 제안', 'MICE 제안' 등을 언급할 때, 행사 기획 제안서를 요청할 때, 비딩 문서를 업로드하며 제안서 작성을 요청할 때, 또는 행사 운영 제안을 PPTX로 만들어달라고 할 때. PCO/PEO/MICE 기획사 실무자의 제안서 작성 워크플로우에 최적화되어 있다. 실행형 지시는 실행 전 jc-prompt-builder 브리프를 거친다."
---

# MICE 제안서 자동 생성 스킬 (v3.0)

## 1. 목표

**이기는 제안서는 평가위원의 채점을 돕는 문서다.** 이 스킬의 산출물은 예쁜 슬라이드 묶음이 아니라, RFP 배점표의 모든 항목에서 점수를 가져오도록 역설계된 설득 문서(PPTX)다. 모든 구성 판단은 이 목표에 종속된다.

## 2. 입력 감지 — 3단계 컨텍스트 분기 (재분석 금지)

작업 시작 시 입력 수준을 판별하고 그에 맞게 출발한다:

- **Full Context** — mice-rfp-analyzer 체이닝 패키지(분석 보고서·평가 매트릭스·GO 판정)가 있음: **RFP를 재분석하지 않는다.** ChainPayload/v1 페이로드의 `requirements`(mandatory/optional/bonus)를 요건 태깅(MANDATORY/WEIGHTED/NICE)으로, `evaluation_focus`(category·weight·our_strength)를 배점 역설계(§3-1)의 가중치 소스로, `differentiation_points`를 승부 메시지·차별화 주장의 근거로, `proposal_structure_hint.page_allocation`을 목차 분량 배분 초안으로 그대로 승계해 §3 설득 설계로 직행한다. `risk_notes_for_negotiation`은 본문 노출 금지(협상 전용)를 유지한다.
- **Partial Context** — RFP 원문만 있거나, mice-rfp-analyzer의 GO 판정 없이 mice-meeting-minutes발 Discovery 5데이터(`discovery_data`: pain_points/expected_outcomes/budget/timeline/decision_makers/competition)만 있음: 배점표·확정 요건이 아직 없으므로 이 경로로 분기한다. RFP 원문이면 핵심 정보(행사명·발주처·유형·일시/장소·규모·예산·**배점표**·필수 요구·제출 조건)를, Discovery 데이터면 `project_context`·`discovery_data`·`strategic_notes.recommended_proposal_focus`를 추출해 분석 요약을 기획자에게 1회 확인받는다. 응찰 판단이 아직이면 mice-rfp-analyzer 선행을 권유하되 강제하지 않는다.
- **Zero Context** — 구두 요청만 있음: 위 핵심 정보 중 제안서 골격을 좌우하는 것(행사 유형·규모·평가 방식·마감)만 최소 질문으로 확보한 후 진행한다. 모르는 항목은 추측하지 말고 [확인 필요]로 슬라이드에 표기한다.

## 3. 설득 설계 (구성 판단의 핵심 — 슬라이드 생성 전 완료)

1. **배점 역설계**: RFP 배점표가 목차의 상위 규칙이다. 배점이 큰 항목에 페이지와 순서를 배분하고, **커버리지 매핑표(배점 항목 × 대응 슬라이드)** 를 내부 산출물로 만든다 — §8 완료 게이트의 검증 대상. 표준 7섹션(§5)은 출발점일 뿐, 배점 구조와 충돌하면 배점이 이긴다.
2. **원 메시지 관통**: 이 제안이 이기는 이유를 한 문장(승부 메시지)으로 정의하고 — Full Context면 rfp-analyzer 승계 — 표지 부제, 각 섹션 도입부, Thank You까지 같은 메시지의 변주로 관통시킨다. 슬라이드마다 다른 자랑을 하는 제안서는 아무것도 각인시키지 못한다.
3. **차별화는 비교에서만 성립**: 예상 경쟁 구도 대비 자사 강약점을 내부 배틀카드로 정리하고, **근거(실적·수치·방법론)를 댈 수 있는 STRONG 항목만** 본문에서 주장한다. 근거 없는 "풍부한 경험" 류 수식어는 금지 — 쓸 거면 숫자로 쓴다(예: "동일 규모 전시회 N회, 누적 참관객 N만 명").
4. **발주처 언어 미러링**: RFP가 쓰는 용어·우선순위 표현(예: "내실 있는", "안전관리 강화")을 섹션 헤드라인에 재사용한다. 평가위원은 자기 문서의 언어로 쓰인 제안서를 채점하기 쉽다.
5. **리스크 선제 응답**: RFP의 독소 조항·까다로운 요구는 숨기지 말고 "리스크 관리" 항목에서 대응 방안과 함께 정면으로 다룬다 — 다뤘다는 사실 자체가 신뢰 점수다.

## 4. 모드 결정 (기획자 합의 게이트 — 슬라이드 생성 전 1회)

목차(구성안)와 함께 아래 4결정을 한 번에 묻는다. 이후 전 슬라이드에 일관 적용:

| 결정 | 선택지 (기본 권장) |
|---|---|
| 컬러 모드 | [A] RFP 컬러(발주처 CI 명시·공공) / **[B] JC 시그니처** / [C] JC+클라이언트 오버레이(협업 행사) |
| 이미지 자리 | [A] 회색 박스 / [B] 마스터(네이티브 자리표시자) / **[A+B] 혼합**(표지·섹션구분·Thank You=마스터, 본문=박스) |
| 다크 모드 | **[A] 최소**(표지·섹션구분·Thank You 8장) / [B] 강조(+KPI 2장) / [C] 없음 |
| 아이콘 | **[A] Heroicons** / [B] Font Awesome / [C] 없음 |

이미지 에셋은 RULE-VISUAL-ROUTING(사진·영상=Higgsfield / 표·차트·다이어그램=Claude 코드) 준수.

## 5. 구조와 자원

**표준 7섹션 (50p 이내, 배점 역설계로 비중 조정)**: ①표지·목차 ②행사 개요·컨셉 ③운영 계획 ④크리에이티브 ⑤KPI/성과관리 ⑥회사 소개·레퍼런스 ⑦예산/부록. 슬라이드별 패턴 매핑: `references/slide-structure.md`.

**행사 유형별 강조**: 전시회·박람회=공간·동선·크리에이티브(부스 배치·바이어 매칭) / 컨퍼런스·포럼=컨셉·프로그램(연사·세션·통역) / 기업행사=크리에이티브·KPI(브랜드 가이드·임원 동선) / 인센티브=프로그램·연출(참가자 경험·F&B).

**생성 자원 (모드에 따라 필요분만 읽기)**: `references/visual-patterns.md`(기본 17패턴) · `dark-mode-patterns.md` · `icon-library.md` · `infographic-patterns.md`(퍼널·매트릭스·레이더) · `slide-masters.md`. PPTX 생성은 `/mnt/skills/public/pptx/SKILL.md`·`pptxgenjs.md` 가이드, JC 토큰은 `/mnt/skills/user/jc-design-system/references/signature-tokens.md`(+모드 C면 `client-overlays.md`) 준수.

## 6. 디자인 원칙 (요지 — 상세는 references)

- `LAYOUT_WIDE`(13.333"×7.5") 고정, 여백 최소 0.5", 제목 아래 장식선 금지.
- **모든 슬라이드에 비주얼 요소 1개 이상** (이미지 자리/표/차트/다이어그램/인포그래픽/아이콘 보강). 동일 레이아웃 연속 금지 — 패턴을 교차 배치.
- 타이포: Pretendard(제목 Bold 32~44pt·본문 Regular 14~16pt), 숫자 JetBrains Mono, 영문 Inter. 미설치 시 시스템 폴백.
- 컬러: JC 시그니처(Primary `0A2540`·Accent `2962FF`·Point `FF5722`/`E91E63`) — pptxgenjs HEX는 `#` 없이 6자리(RULE-PPTX-HEX). RFP 컬러 모드 팔레트는 `references/visual-patterns.md §0` 참조.
- 문체: 한국어 개조식, 수치·방법론 중심, 회사·개인 식별정보 하드코딩 금지(RULE-NO-COMPANY — 제안사 정보는 기획자가 주입).

## 7. 실행 흐름

입력 감지(§2) → 설득 설계(§3) → **목차+모드 합의 게이트(§4, 기획자 확인 1회)** → 자원 로드 → 슬라이드 생성 → 완료 게이트(§8) → Visual QA(`/mnt/skills/public/pptx/SKILL.md` QA 절차 — 서브에이전트 검수) → 전달(슬라이드 노트에 이미지 교체·폰트 안내 자동 삽입).

기획자 확인은 §2의 분석 요약(Partial/Zero일 때)과 §4 게이트 두 곳이면 충분하다 — 단계마다 승인을 구하지 않는다.

## 8. 완료 게이트 (증거주의 — 통과 전 완료 보고 금지)

1. **커버리지**: §3-1 매핑표 기준, RFP 배점 전 항목에 대응 슬라이드가 실재하는가 (누락 0건).
2. **제출 조건**: 페이지 제한·목차 양식·필수 서식 등 RFP 제출 조건을 재대조했는가.
3. **숫자 정합**: 본문 금액·일정·규모 수치가 RFP 원문 및 상호 간 일치하는가.
4. **원 메시지**: 표지→섹션 도입→Thank You에 승부 메시지가 실제로 관통하는가.
5. **주장-근거 짝**: 차별화 주장 전 건에 근거(실적·수치)가 붙어 있는가 — 없는 주장은 삭제.
6. **일관성·규정**: 4모드 일관 적용 + 전 슬라이드 비주얼 + 식별정보 하드코딩 0건.

미통과 항목은 수정 후 재검증. 확인 불가능한 항목(예: 자사 실적 데이터 부재)은 기획자에게 [확인 필요]로 명시 보고한다.

## 9. 모듈 파일 목록

| 파일 | 내용 |
|------|------|
| `references/slide-structure.md` | 38개 슬라이드 × 패턴 코드 매핑 |
| `references/visual-patterns.md` | 기본 17패턴 + JC 토큰 + RFP 팔레트 |
| `references/dark-mode-patterns.md` | 다크 변형 5종 |
| `references/icon-library.md` | react-icons 적용 가이드 |
| `references/infographic-patterns.md` | 퍼널·매트릭스·레이더 |
| `references/slide-masters.md` | 슬라이드 마스터 5종 + 네이티브 그림 자리표시자 |

## 10. 버전 히스토리

- **v1.0 (2026-04)**: 7섹션 표준 구조
- **v2.0 (2026-05-25)**: 비주얼 패턴 시스템 (이미지 6·표 4·차트 3·다이어그램 4)
- **v2.1 (2026-05-25)**: 인포그래픽·다크 모드·아이콘·슬라이드 마스터·JC 토큰 연동 5모듈
- **v3.0.0 (2026-07-03)**: **지시문 재설계 (Fable 5 패스)** — 설득 설계 신설(배점 역설계·원 메시지·근거 있는 차별화·언어 미러링·리스크 선제 응답), 입력 감지 3분기(체이닝 재분석 금지), 증거주의 완료 게이트, 12단계 고정 절차·단계별 승인 과잉처방 제거(합의 게이트 2곳으로 압축), frontmatter version 필드 추가
- **v3.0.1 (2026-07-03)**: 체이닝 소비 문서화(CP1 GO-2) — §2에 ChainPayload/v1 필드 소비 규칙(requirements·evaluation_focus·differentiation_points·proposal_structure_hint 등)과 mice-meeting-minutes발 Discovery 5데이터의 Partial Context 분기 귀속 명시
