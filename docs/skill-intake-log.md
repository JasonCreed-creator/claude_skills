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
| 🆕 | `mice-market-intel` | 2단계 구조화 리서치 (Weizhena/Deep-Research, MIT + Anjos2/recursive-research) | 시장·경쟁 인텔 부재. built-in deep-research는 범용·비-MICE·비-체이닝 | ⬜ 빌드 예정 |
| ⬆️ | `mice-estimate` | 전략 프라이싱(Van Westendorp·티어 논리) (stratarts/pricing-strategy-architect, MIT) | 원가기반 산출만, 전략적 가격결정 논리 부재 | ⬜ 빌드 예정 |
| ⏸ | `mice-sponsor-deck` | 영업 실행층(반론대응·아웃리치·리드자격) (coreyhaines31, Composio/lead-research) | 데크 생성만, 영업 실행층 부재 | ⏸ 보류 (이번 미승인) |
| ⛔ | (다수) | 마케팅 그로스·CRM 자동화·dev-process·공식 문서엔진·resume/invoice | MICE 전략 코어와 무관·중복·이미커버 | — |

**가드레일 준수**: 외부 파일 복사 0 (패턴=방법론만 흡수, jc 네이티브 재구성) · 외부 스크립트 실행 0 · 출처 URL 보존 · 변경 전 원본 `_archive/<날짜>/` 보존(해당 시).

### jc-strategy-canvas 빌드 노트 (v1.0.0)
- 구조: SKILL.md(176줄) + references 3종(framework-catalog·canvas-output-spec·chaining-schema) + LICENSE.
- 하우스 규약: jc-* 명명 · 한국어 푸시형 description · SoT 토큰 런타임 참조(값 하드코딩 0) · `RULE-NO-COMPANY`(회사·실명 0건) · ChainPayload(→proposal/rfp) · jc-redteam 검증 끼움.
- check_drift `CONSUMERS`에 등록(전략 캔버스 HTML = 디자인 소비). drift-guard ✅.
- 검수(jc-redteam 렌즈): 트리거·형제경계 명확, mice-rfp-analyzer("경쟁") 경계는 description에서 "RFP 입력 종속 vs 자사 전략"으로 분리 명시. 오탈자 0, 보안(외부 스크립트·시크릿) 해당 없음.
