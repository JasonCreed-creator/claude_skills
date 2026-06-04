# 스킬 인테이크 로그 (forge)

`jc-skill-forge` / `/skillupgrade` 워크플로우의 단일 트래커. 외부 생태계 대조 → 판정 → 적용 결과를 날짜·소스·결정·근거로 누적한다. (프리셋 개조 프로그램은 `preset-optimization-roadmap.md` 별도.)

범례: 🆕 NEW · ⬆️ UPGRADE · 🔀 MERGE · ♻️ REPLACE · ⛔ SKIP

---

## 2026-06-04 — 1차 인테이크 (전체 라이브러리 스캔)

**스캔 소스(화이트리스트, 읽기전용 대조)**: maigentic/stratarts(MIT) · Weizhena/Deep-Research-skills(MIT) · obra/superpowers(MIT) · anthropics/skills · ComposioHQ/awesome-claude-skills · VoltAgent/awesome-agent-skills.

**핵심 판정**: 현 라이브러리는 "산출 스킬"은 촘촘하나 전략가의 "사고 스킬"(전략 프레임워크·시장 인텔) 부재구간. 승인(GO): NEW 2 + UPGRADE 1.

| 결정 | 스킬 | 흡수 패턴 (출처·라이선스) | 근거 | 상태 |
|------|------|--------------------------|------|------|
| 🆕 | `jc-strategy-canvas` | 전략 프레임워크 6종 (maigentic/stratarts, MIT) | 전략가인데 자사 전략수립 프레임워크 부재. mice-rfp는 RFP-입력 종속이라 별개 | ✅ 빌드·검수 완료 |
| 🆕 | `mice-market-intel` | 2단계 구조화 리서치 (Weizhena/Deep-Research, MIT + Anjos2/recursive-research) | 시장·경쟁 인텔 부재. built-in deep-research는 범용·비-MICE·비-체이닝 | ✅ 빌드·검수 완료 |
| ⬆️ | `mice-estimate` | 전략 프라이싱(Van Westendorp·티어 논리) (stratarts/pricing-strategy-architect, MIT) | 원가기반 산출만, 전략적 가격결정 논리 부재 | ✅ 빌드·검수 완료 (v2.1.0) |
| ⏸ | `mice-sponsor-deck` | 영업 실행층(반론대응·아웃리치·리드자격) (coreyhaines31, Composio/lead-research) | 데크 생성만, 영업 실행층 부재 | ⏸ 보류 (이번 미승인) |
| ⛔ | (다수) | 마케팅 그로스·CRM 자동화·dev-process·공식 문서엔진·resume/invoice | MICE 전략 코어와 무관·중복·이미커버 | — |

**가드레일 준수**: 외부 파일 복사 0 (패턴=방법론만 흡수, jc 네이티브 재구성) · 외부 스크립트 실행 0 · 출처 URL 보존 · 변경 전 원본 `_archive/<날짜>/` 보존(해당 시).

### jc-strategy-canvas 빌드 노트 (v1.0.0)
- 구조: SKILL.md(176줄) + references 3종(framework-catalog·canvas-output-spec·chaining-schema) + LICENSE.
- 하우스 규약: jc-* 명명 · 한국어 푸시형 description · SoT 토큰 런타임 참조(값 하드코딩 0) · `RULE-NO-COMPANY`(회사·실명 0건) · ChainPayload(→proposal/rfp) · jc-redteam 검증 끼움.
- check_drift `CONSUMERS`에 등록(전략 캔버스 HTML = 디자인 소비). drift-guard ✅.
- 검수(jc-redteam 렌즈): 트리거·형제경계 명확, mice-rfp-analyzer("경쟁") 경계는 description에서 "RFP 입력 종속 vs 자사 전략"으로 분리 명시. 오탈자 0, 보안(외부 스크립트·시크릿) 해당 없음.

### mice-market-intel 빌드 노트 (v1.0.0)
- 구조: SKILL.md(148줄) + references 4종(research-outline-templates·source-tiering·report-spec·chaining-schema) + LICENSE.
- 방법론: 2단계 리서치(아웃라인→병렬조사→리포트) + Phase 1 HITL 정지점. 출처 티어링(T1~T4)·교차확인·추정금지.
- 형제경계: built-in deep-research(범용) vs 본 스킬(MICE 도메인+체이닝)을 description·§1에 분리 명시. jc-strategy-canvas(판단)와 수집-판단 분리.
- 하우스 규약: SoT 토큰 런타임 참조·RULE-NO-COMPANY(자사 식별 변수화, *조사 대상* 공개 기업명은 사실·출처로 허용)·check_drift CONSUMERS 등록·drift-guard ✅.
- 배선: 두 신규 스킬을 `chaining-protocol.md`(ChainPayload/v1 SoT) 적용대상·source enum·페이로드 매핑표에 등록.

### mice-estimate 강화 노트 (v2.0.0 → v2.1.0)
- `references/pricing-strategy.md` 추가 — 4대 가격 레버(가치기반·Van Westendorp PSM·티어/패키지·앵커링) + MICE 입찰/스폰서 맥락. SKILL.md "전략 프라이싱(선택)" 절 + References + 버전 히스토리 연결.
- 원본 `_archive/20260604/mice-estimate/` 백업(롤백용). 기존 원가 산출(pricing-engine·calc_estimate) **무변경** — 가법적 레이어.
- 경계 명시: 조사=mice-market-intel, 포지션 판단=jc-strategy-canvas, 원가=pricing-engine, 저가수주 검증=jc-redteam.
