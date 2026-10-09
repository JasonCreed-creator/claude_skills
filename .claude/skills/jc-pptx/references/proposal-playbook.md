# Proposal Playbook — 발주처 제안서 설득 설계 (구 mice-proposal v3.0.1 흡수)

> **이기는 제안서는 평가위원의 채점을 돕는 문서다.** 예쁜 슬라이드 묶음이 아니라 RFP 배점표의 모든 항목에서 점수를 가져오도록 역설계된 설득 문서. 모든 구성 판단은 이 목표에 종속된다.

---

## 1. 입력 감지 — 3단계 분기 + 상류 보강 (재분석 금지)

| 수준 | 상태 | 출발점 |
|------|------|--------|
| **Full** | `mice-rfp-analyzer` ChainPayload(분석 보고서·평가 매트릭스·GO) 있음 | RFP 재분석 금지. `requirements`→요건 태깅(MANDATORY/WEIGHTED/NICE), `evaluation_focus`→배점 가중치, `differentiation_points`→승부 메시지 근거, `proposal_structure_hint.page_allocation`→분량 초안. `risk_notes_for_negotiation`은 본문 노출 금지 |
| **Partial** | RFP 원문만, 또는 `mice-meeting-minutes` Discovery 데이터만 | 핵심 정보(행사명·발주처·유형·일시/장소·규모·예산·**배점표**·필수 요구·제출 조건)를 추출해 분석 요약을 1회 확인. GO 판단이 필요하면 rfp-analyzer 선행 권유(강제 아님) |
| **Zero** | 구두 요청만 | 골격을 좌우하는 것(행사 유형·규모·평가 방식·마감)만 최소 질문. 모르는 항목은 슬라이드에 `[확인 필요]` |
| **보강** | `mice-estimate` 봉투(`totalAmount`·`totalAmountVat`·`sections`) 있음 | ⑦ 예산(T09)·DS 09 견적 요약 자동 채움 — 총액은 `kpi()`(VAT 별도/포함 캡션), `sections` 키별 금액은 표 행. 금액은 봉투 값 그대로 옮긴다(§5-3 숫자 정합). 없으면 ⑦은 `[견적 확정 후 반영]` |
| **보강** | `jc-strategy-canvas` 봉투(`recommendation`·`key_messages`·`differentiation_axes`) 있음 | `recommendation.headline`·`key_messages` → 원 메시지(§2-2) 후보, `differentiation_axes` → 차별화(§2-3) 근거 축. `evidence_flags`의 가설·추정 비중이 높으면 단정 표현을 피한다 |
| **보강** | `mice-market-intel` 봉투(`market_size`·`competitors`·`trends`) 있음 | ② 배경·시장 슬라이드(T05·T10) — 수치마다 출처·기준일(`scope.as_of`·`sources[].date`) 캡션 병기. `competitors`는 내부 배틀카드(§2-3)로만, `gaps` 항목은 `[확인 필요]`. `sponsor_candidates`는 스폰서 덱(`sponsor-deck.md §1`) |
| **보강** | `mice-aftermath` 봉투(`cases`·`performance`) 있음 | ⑥ 유사 실적·수행실적(T11·T05) — `reuse_tier`에 R1이 있는 케이스, `anonymize` 플래그 존중(동의 없으면 가명). R2 케이스는 스폰서 덱(`sponsor-deck.md §5`), 결과보고 덱은 `performance.kpis` → KPI(T05) |

보강 행은 Full·Partial·Zero 어느 수준에도 겹쳐 적용한다. 봉투 판별·무변경 승계는 `jc-design-system/references/chaining-protocol.md §6~§7`.

## 2. 설득 설계 (슬라이드 생성 전 완료)

1. **배점 역설계** — 배점표가 목차의 상위 규칙. 배점 큰 항목에 페이지·순서 배분. **커버리지 매핑표(배점 항목 × 대응 슬라이드)** 를 내부 산출물로 만든다(§5 게이트 검증 대상). §3 표준 7섹션은 출발점일 뿐, 충돌하면 배점이 이긴다.
2. **원 메시지 관통** — 이기는 이유 한 문장(승부 메시지)을 표지 부제 → 각 섹션 도입 → 클로징까지 변주로 관통. 슬라이드마다 다른 자랑을 하면 아무것도 각인되지 않는다.
3. **차별화는 비교에서만** — 예상 경쟁 구도 대비 강약점을 내부 배틀카드로 정리하고, **근거(실적·수치·방법론)를 댈 수 있는 항목만** 본문에서 주장. "풍부한 경험" 류 수식어 금지 — 쓸 거면 숫자로("동일 규모 컨퍼런스 N회, 누적 참석 N명").
4. **발주처 언어 미러링** — RFP의 용어·우선순위 표현("내실 있는", "안전관리 강화")을 섹션 헤드라인에 재사용. 평가위원은 자기 문서의 언어로 쓰인 제안서를 채점하기 쉽다.
5. **리스크 선제 응답** — 독소 조항·까다로운 요구는 숨기지 말고 "리스크 관리" 항목에서 대응 방안과 함께 정면으로. 다뤘다는 사실이 신뢰 점수다.
6. **리멤버 고유 자산을 구조에 심기** — 모객 개런티·타깃 데이터(310 산업 × 145 직무)·쇼업 설계·세일즈 연결은 "운영 계획" 안에 별도 슬라이드로(소개서 문법 `examples/build_deck2.py` `s_target`·`s_showup` 참조). 발주처 요구가 운영만이면(베뉴 대납형 등) 축소.

## 3. 표준 7섹션 골격 → 타입 매핑

50p 이내(SIMPLE 15~35 / CUSTOM 50~80). 배점 역설계로 비중 조정.

| 섹션 | 슬라이드 | 타입 | DS 템플릿 |
|------|---------|------|-----------|
| ① 표지·목차 | 표지 / 목차 | T01 / T02 | 01(다크) / 02 |
| ② 행사 이해·콘셉트 | 섹션 구분 / 배경·목적 / 콘셉트·슬로건 / 포지셔닝 / 기대효과 / RFP 요구 대응표 | T03 / T08 / T12 / T06 / T05 / T09 | 03(다크) / 04 / — / — / 07 / 05 |
| ③ 운영 계획 | 운영 체계도 / 마스터 타임라인 / 당일 타임테이블 / 공간·동선 / 프로그램 / 참가자 관리(모객 퍼널) / 안전·비상 | T13 / T13 / T13 / T14 / T08 / T07 / T08 | 08 / 06 / 06 / — / 04 / — / 04 |
| ④ 크리에이티브 | 디자인 콘셉트 / 공간 디자인 / 연출 포인트 | T11 / T14 / T08 | — |
| ⑤ KPI·성과 관리 | KPI 대시보드 / 측정 체계 / 사후 보고 | T05 / T07 / T13 | 07 / — / — |
| ⑥ 회사·레퍼런스 | 회사 개요 / 핵심 역량 / 유사 실적 / 투입 인력 | T04 / T08 / T11 / T13 | 05 / 04 / — / 08 |
| ⑦ 예산·부록 | 총괄 예산 / 상세 내역 / 마일스톤 / 클로징 | T09 / T09 / T13 / T16 | 09 / 09 / 06 / 10(다크) |

### 3.1 행사 유형별 강조

| 유형 | 강조 섹션 |
|------|-----------|
| 전시회·박람회 | 공간·동선·크리에이티브(부스 배치·바이어 매칭) |
| 컨퍼런스·포럼 | 콘셉트·프로그램(연사·세션·통역) + 타깃 모객 |
| 기업행사(고객 초청·어프리시에이션) | 크리에이티브·KPI(브랜드 가이드·임원 동선·관계 시간) |
| 인센티브·워크숍 | 프로그램·연출(참가자 경험·F&B) |
| 공공 위탁(국가계약) | 대응형 목차 그대로 + 안전·정산·산출내역서(`mice-estimate` 리멤버 양식 — 발주 서식 항목명·합계 구조만 맞춤) |

### 3.2 다크 슬라이드 배분
표지 · 섹션 구분(2~4회) · 클로징. 그 외 다크는 KPI 강조 1장까지. 전체 30% 이하.

## 4. 이미지·자원

- 사진: 발주처·베뉴 제공 원본 → 오브제(다크 슬라이드) → 플레이스홀더 + 이미지 브리프. 임의 스톡 금지(RULE-VISUAL-ROUTING).
- 표·차트·도해·타임라인: deck_kit 컴포넌트로 직접 렌더. 24px(12pt) 미만 표 금지 → 차트 1 + 핵심 수치 1로 재구성.
- 아이콘 없음(유니코드 기호만). 구 mice-proposal의 react-icons·슬라이드 마스터·pptxgenjs 패턴은 폐기(레포 `_archive/20260921/mice-proposal` 참조만).

## 5. 완료 게이트 (증거주의 — 통과 전 완료 보고 금지)

1. **커버리지** — §2-1 매핑표 기준 RFP 배점 전 항목에 대응 슬라이드 실재(누락 0).
2. **제출 조건** — 페이지 제한·목차 양식·필수 서식 재대조.
3. **숫자 정합** — 금액·일정·규모가 RFP 원문 및 견적(`mice-estimate`)과 상호 일치.
4. **원 메시지** — 표지→섹션 도입→클로징 관통 확인.
5. **주장-근거 짝** — 차별화 주장 전 건에 근거. 없는 주장은 삭제.
6. **명의·식별정보** — 리멤버 명의, 발주처·담당자 슬롯 주입, 구 소속사 언급 0건, 고객사 실명 레퍼런스는 동의 확인.

미통과는 수정 후 재검증. 확인 불가 항목(자사 실적 데이터 부재 등)은 `[확인 필요]`로 명시 보고. 이후 `jc-redteam` Deep Audit.

## 6. 체이닝 (ChainPayload/v1, source `jc-pptx`)

```json
{
  "$schema": "ChainPayload/v1", "source": "jc-pptx", "version": "<SKILL.md version>",
  "generatedAt": "…", "target": "mice-estimate", "clientId": "…", "projectTitle": "…",
  "deck_meta": { "purpose": "proposal|sponsor|intro|report", "slides": 51, "storyline": "response", "density": "CUSTOM" },
  "sections": [ { "id": "03", "title": "운영 계획", "slides": [12, 24] } ],
  "coverage_map": [ { "rfp_item": "운영 계획(30점)", "slides": [12, 13, 18] } ],
  "client": "{{client_company}}", "eventDate": "2026-06-18",
  "eventScale": { "target": 250, "guarantee": 225 },
  "venue": { "type": "5star", "region": "{{region}}", "name": "{{venue}}", "rental": null },
  "options": { "video": false, "emcee": true, "souvenir": false, "scaler4k": false, "survey": false,
               "photowall_basic": true, "photowall_premium": false, "photo": false, "aving": false },
  "displayType": "led", "boothCount": 0, "format": "remember",
  "presentation": { "minutes": 15, "tone": "formal" }
}
```

- **견적 입력 키(`estimate_hint`로 불러 온 묶음)** — `eventScale`·`venue`·`options`·`displayType`·`boothCount`·`eventDate`·`client`를 봉투 최상위에 평탄하게 싣는다. 중첩 객체(`"estimate_hint": {…}`)로 감싸지 않는다 — `mice-estimate`는 최상위 키만 읽는다(정본 `mice-estimate/references/chaining-schema.md §2` 입력 스키마).
  - `eventScale.guarantee`는 모객 개런티 인원(없으면 `null` → target과 같게 처리). `venue.rental`은 확정 대관료(원), 미정이면 `null`(자동 산출).
  - `options`는 불리언 맵 — 위 9키만 쓴다. 문자열 배열(`["led", …]`) 금지. LED·프로젝터는 옵션이 아니라 `displayType`(`led`|`projector`), 포토월은 `photowall_basic`/`photowall_premium`.
  - `format`은 항상 `remember`(양식 단일). 미정 값은 `null` — `venue: null`이면 대관료 자동 산출, `options: null`이면 옵션 전부 미적용으로 처리된다.
  - mice-estimate가 `source: "jc-pptx"`를 아직 자동 감지하지 못하면 봉투 파일을 주며 "이 봉투로 견적 산출"을 명시 요청한다(키 구조는 같다).
- `presentation`(`minutes`·`tone`·선택 `type`·`presenter`·`audience`) → `pt-script`가 읽어 발표 시간·톤을 채운다. `presentation.minutes`·`sections`는 `mice-run-of-show`가 발표 블록 시간·순서 참고로 읽는다(프로그램 세그먼트 배열은 내지 않는다).
- 수신 측은 `source: "mice-proposal"`을 본 스킬 별칭으로 취급한다(하위호환).
