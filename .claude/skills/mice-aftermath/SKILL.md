---
name: mice-aftermath
version: "v1.0.0"
license: Complete terms in LICENSE.txt
description: MICE 행사 종료 후 결과 데이터를 종합해 ① 사후 종합 결과보고서와 ② 차기 비딩·영업에 재활용하는 레퍼런스 케이스(case study)를 산출하는 스킬. mice-dashboard(KPI)·mice-estimate(예산 실적)·mice-meeting-minutes(교훈)·mice-run-of-show(계획 대비 실제) 산출을 체이닝 입력으로 받아 목표 대비 성과·예산 실적·운영 하이라이트·이슈/교훈·차기 권고를 8축 프레임으로 구성하고, jc 스타일 결과보고서(HTML/md) + ChainPayload(→mice-proposal·mice-sponsor-deck)로 낸다. 다음 상황에서 반드시 이 스킬을 사용할 것 사용자가 '결과보고서', '사후보고', '행사 결과보고', '종합 결과보고', 'post-event report', '행사 결산 보고', '사후 평가', 'wrap-up 리포트', '디브리프', 'debrief', '레퍼런스 케이스', '케이스 스터디', 'case study', '행사 사례화', '실적 레퍼런스', '수행 실적 정리'를 언급할 때. 행사가 끝났고 그 결과를 발주처/내부 보고 + 차기 영업 재활용으로 정리해달라고 할 때. 단, 결과 데이터를 차트·KPI 대시보드로 시각화하는 것은 mice-dashboard(본 스킬은 그 수치를 서사·케이스로 종합), 산문형 문서를 백지에서 함께 써 나가는 공동작성은 jc-doc-coauthor, 발주처 제출 제안서는 mice-proposal, 스폰서 유치 데크는 mice-sponsor-deck, 회의록 구조화는 mice-meeting-minutes, 완성 보고서의 적대적 검증은 jc-redteam 영역이므로 그쪽을 쓸 것. 행사·발주처·실적 식별정보는 외부 주입 변수로 처리.
---

# mice-aftermath — 행사 사후 결과보고 + 재사용 케이스

행사가 끝난 뒤, 산재한 결과(KPI·예산 실적·교훈·계획 대비 실제 진행)를 종합해 **① 사후 종합 결과보고서**(발주처/내부 보고)와 **② 차기 비딩·영업에 그대로 인용하는 레퍼런스 케이스**(case study)를 만든다. 워크플로우의 **사후 단계**에 위치하며, 한 행사의 결과를 *다음 수주의 자산*으로 전환하는 선순환 고리다.

외부 패턴(proposal-skills의 case study 구조, Association Event Management의 post-event metrics)을 **패턴만 흡수**해 MICE 네이티브로 재구성했다(파일·코드 복사 없음).

## 1. 본 스킬이 다루는 것 / 다루지 않는 것

### 다루는 것 (DO)
- 행사 종료 후 **8축 사후 결과보고서**: 요약·개요·목표 대비 성과·예산 실적·운영 하이라이트·이슈/교훈·이해관계자 피드백·차기 권고. (`references/report-structure.md`)
- **재사용 레퍼런스 케이스 빌더**: challenge→approach→result(수치)→proof 구조 + 익명화 + 재사용 등급. (`references/case-builder.md`)
- 체이닝 입력 흡수: mice-dashboard(KPI)·mice-estimate(예산 vs 실적)·mice-meeting-minutes(교훈/Action)·mice-run-of-show(계획 대비 실제). 또는 직접 입력.
- 산출: jc 스타일 결과보고서(HTML/md) + `ChainPayload`(→mice-proposal 차기 비딩 레퍼런스, →mice-sponsor-deck ROI 케이스).

### 다루지 않는 것 (DON'T)
- 결과 데이터를 **차트·KPI 대시보드로 시각화** → **mice-dashboard** (본 스킬은 그 수치를 *서사·판단·케이스*로 종합)
- 산문형 문서를 백지에서 **함께 써 나가는 공동작성** → **jc-doc-coauthor**
- 발주처 제출 **제안서** → mice-proposal (본 스킬의 케이스는 proposal의 *입력 레퍼런스*)
- 스폰서 유치 데크 → mice-sponsor-deck (본 스킬의 ROI 케이스는 그 *입력*)
- 회의록 구조화 → mice-meeting-minutes / 결론·문서 적대 검증 → jc-redteam

> **mice-dashboard와의 경계**: dashboard는 "숫자가 무엇인가"(차트·KPI 카드)를 그린다. aftermath는 "그래서 무슨 의미이고 다음에 어떻게 쓰나"(목표 대비 해석·교훈·차기 권고·재사용 케이스)를 *서술*한다. 차트가 필요하면 dashboard 산출을 인용/임베드하고 재발명하지 않는다.
>
> **jc-doc-coauthor와의 경계**: doc-coauthor는 *백지 산문을 단계적으로 함께 쓰는 범용 프로세스*다(개요부터 같이 잡음). aftermath는 *행사 결과 데이터를 고정 8축 프레임으로 종합하고 재사용 케이스까지 체이닝*하는 사후 전용 산출 스킬이다. "결과보고를 같이 써 나가자"면 doc-coauthor, "행사 끝났으니 결과 종합 보고서+케이스로 내줘"면 본 스킬.

## 2. 호출 시점 판단 가이드

| 사용자 입력 | 본 스킬 | 사용 스킬 |
|------------|:------:|----------|
| "행사 끝났는데 결과보고서 정리해줘" | ✅ | mice-aftermath |
| "이 행사 사례로 만들어 차기 비딩에 쓰게" | ✅ | mice-aftermath |
| "성과·교훈·차기 권고 종합 보고" | ✅ | mice-aftermath |
| "행사 실적을 차트·KPI로 시각화" | ❌ | mice-dashboard |
| "결과보고 초안 같이 써 나가자" | ❌ | jc-doc-coauthor |
| "이 케이스로 발주처 제안서 만들어" | ❌ | mice-proposal |

## 3. 워크플로우 (Phase)

```
[행사 종료]
   ↓
Phase 0  스코프      보고 대상(발주처/내부/영업재활용)·행사 정보·입력 데이터 소스 확인
   ↓
Phase 1  데이터 정합  체이닝 입력(dashboard/estimate/minutes/run-of-show) 또는 직접 입력 흡수
   ↓                + 목표(KPI 타깃·예산 계획) 확보 → 성과는 '목표 대비'로만 의미가 생김
Phase 2  보고서 구성  8축 프레임으로 종합 (references/report-structure.md)
   ↓                ★ 추정·과장 금지: 수치는 입력 출처에 근거, 미확보는 [미확보] 표기
Phase 3  케이스 빌드  재사용 레퍼런스 케이스 추출 (references/case-builder.md)
   ↓                challenge→approach→result→proof + 익명화 + 재사용 등급
Phase 4  산출        결과보고서(HTML/md) + ChainPayload(→proposal/sponsor-deck)
                    (선택) jc-redteam — 성과 과장·생존자 편향·인과 비약 적대 검증
```

### Phase 0 — 스코프
보고 **대상**을 먼저 정한다: 발주처 송부용(격식·성과 강조), 내부 보관용(솔직한 교훈), 영업 재활용용(케이스 중심). 대상에 따라 톤·익명화·강조점이 달라진다. 행사명·일자·규모·발주처(외부 주입)를 수집.

### Phase 1 — 데이터 정합 (목표 대비 원칙)
입력 데이터를 모은다. **성과는 항상 *목표 대비*로 표현**한다(참가자 1,200명 = 목표 1,000명의 120%). 목표(KPI 타깃·예산 계획)가 없으면 먼저 확보한다 — 목표 없는 실적 숫자는 자랑일 뿐 보고가 아니다. 체이닝 입력 매핑은 `references/chaining-schema.md`.

### Phase 2 — 보고서 구성 (8축)
`report-structure.md`의 8축으로 종합. **수치는 입력 출처에 근거**하고, 없으면 `[미확보]`로 남긴다(지어내지 않음). 실패·이슈를 숨기지 않고 *교훈*으로 전환한다(내부용은 특히).

### Phase 3 — 케이스 빌드
보고서에서 **재사용 가능한 케이스**를 추출한다. challenge(과제)→approach(해법)→result(정량 성과)→proof(증빙). 발주처명은 재사용 맥락에 따라 익명화(`T社`·`[공공기관]`) 옵션. 재사용 등급(어느 다운스트림에 쓸지) 부여. `case-builder.md`.

### Phase 4 — 산출
- **결과보고서** — jc 스타일 HTML/md. 레이아웃·SoT 토큰 `references/report-spec.md`.
- **ChainPayload** — `source: mice-aftermath`. 케이스·성과를 mice-proposal(차기 비딩 실적 레퍼런스)·mice-sponsor-deck(ROI 케이스)로. 스키마 `references/chaining-schema.md`.
- (선택) **jc-redteam** — "성공했다"류 결론의 과장·생존자 편향·인과 비약을 친다.

## 4. 산출물 — 디자인 (SoT 앵커링)

- **토큰 값 하드코딩 금지.** SoT 런타임 참조: `jc-design-system/references/signature-tokens.md §6 JSON`. 다크/인쇄 `mode-mapping.md`.
- 식별용 핵심값: primary `#0A2540`·accent `#2962FF`·폰트 Pretendard/Inter/JetBrains Mono(수치) — 정본은 SoT.
- 차트가 필요하면 재발명 말고 `mice-dashboard` 산출을 인용/임베드하거나 `mice-dashboard/references/chart-guide.md` 토큰 매핑 차용.
- 공통 룰: `RULE-WCAG`·`RULE-PRINT-LIGHT`(배포본 인쇄=라이트). 정본 `jc-design-system/references/shared-rules.md`.

## 5. RULE-NO-COMPANY (식별정보 외부 주입)

- 자사명·개인 실명·부서명을 **하드코딩하지 않는다**. 슬롯: `{{company_name}}`·`{{author_name}}`·`{{personal_brand}}`·`{{author_title}}`. 정본 `shared-rules.md#RULE-NO-COMPANY`.
- 발주처·협력사·실적 수치는 **외부 주입**. 케이스를 *공개 영업자료*로 재사용할 때는 발주처명을 익명화(`T社`·`[공공기관]`)하거나 사용 동의를 전제로 한다(`case-builder.md` 익명화 규칙).

## 6. 생태계 연결

- **입력(체이닝)**: mice-dashboard(KPI)·mice-estimate(예산 vs 실적)·mice-meeting-minutes(교훈·Action)·mice-run-of-show(계획 대비 실제 진행). 봉투 `ChainPayload/v1`(`chaining-protocol.md`).
- **출력(체이닝)**: → mice-proposal(차기 비딩 *실적 레퍼런스*) · → mice-sponsor-deck(스폰서 *ROI 케이스*). 선순환: 한 행사의 결과가 다음 수주 자산이 된다.
- **검증(선택)**: jc-redteam — 성과 해석의 과장·편향.
- **디자인**: jc-design-system SoT, 차트는 mice-dashboard 패턴.

## 7. 파일 구조

```
mice-aftermath/
├── SKILL.md                    # 본 파일 — 진입점
└── references/
    ├── report-structure.md     # 8축 사후 결과보고 프레임 + 축별 지침 + 워크드 예시
    ├── case-builder.md         # 재사용 케이스(challenge→approach→result→proof) + 익명화·재사용 등급
    ├── chaining-schema.md      # ChainPayload in(dashboard/estimate/minutes/run-of-show) / out(proposal/sponsor-deck)
    └── report-spec.md          # HTML/md 리포트 레이아웃 + SoT 토큰 + 인쇄
```

## 8. 운영 원칙 / 한계

- **목표 대비가 본질**: 목표 없는 실적은 보고가 아니다. Phase 1에서 목표를 먼저 확보한다.
- **과장·추정 금지**: 수치는 입력 출처 근거. 미확보는 `[미확보]`. "성공" 결론은 jc-redteam로 친다(생존자 편향·인과 비약 경계).
- **교훈을 숨기지 않는다**: 내부용 보고는 실패·이슈를 *개선 자산*으로 기록한다. 발주처용은 톤을 조절하되 사실을 왜곡하지 않는다.
- **시각화는 dashboard에 위임**: 차트가 주가 되면 잘못 트리거 — mice-dashboard로. 본 스킬은 *서사 종합 + 재사용 케이스*가 본령.
- **케이스 재사용은 동의·익명화 전제**: 발주처 실명·실적의 외부 영업 재사용은 익명화하거나 사용 동의를 확인.

## 9. 버전 히스토리

| 버전 | 일자 | 변경 |
|------|------|------|
| v1.0.0 | 2026-06-05 | 신규. proposal-skills(case study)·Association(post-event metrics) 패턴 흡수·MICE 재구성. 8축 사후 결과보고 프레임 + 재사용 케이스 빌더(challenge→approach→result→proof) + Phase 0~4(목표 대비 원칙·과장 금지). 입력 체이닝(dashboard/estimate/minutes/run-of-show), 출력 ChainPayload(→proposal/sponsor-deck). reference-driven(스크립트 없음), jc-design SoT 앵커. jc-skill-creator 하우스 표준 준수. |
