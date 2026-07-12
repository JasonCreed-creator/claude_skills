# CP3 — 스킬 인테이크 결정 매트릭스 (외부 소스 5종)

> 작성: 2026-07-12 (Claude Code, Fable 5 오케스트레이션 + Sonnet 5 스캔 에이전트 4기)
> 소스: ① superpowers-main.zip(v6.1.1) ② ECC-main.zip(everything-claude-code 2.0.0) ③ skills-main.zip(→기클론 레포로 대체) ④ doc-coauthoring SKILL.md 단품 ⑤ image-enhancer SKILL.md 단품
> 브리프: jc-prompt-builder 게이트 승인(2026-07-12) — 가정 A1~A4 확정. 확신도 高·저위험 = 즉시 적용, 구조 변경 = 별도 GO
> 스캔 리포트 원본: 세션 스크래치패드 `intake\reports\` (cp1-audit / superpowers-scan / ecc-scan / anthropic-delta)

---

## 0. 요약

- **CP1(7/3) GO 22건 중 21건 적용 확인, 잔여 1건 발견** — mice-market-intel의 company-intel 패턴 흡수 누락. 본 CP3의 U1으로 편입.
- superpowers·anthropics/skills 모두 **CP1 이후 델타 0건** (스냅숏/업스트림이 7월 초 이전 상태).
- 신규 소스 ECC(278종 스킬)에서 **즉시 적용 2건 + GO 대기 4건** 채택, 나머지 전량 SKIP.
- doc-coauthoring 원본 대조에서 jc-doc-coauthor **경미 누락 2건** 발견 — 즉시 적용.
- image-enhancer 단품 **SKIP**.

---

## A. 즉시 적용 — 3건 (브리프 A3: 확신도 高·저위험, 서브에이전트 적용)

| # | 대상 스킬 | 흡수 내용 | 소스 | 확신도 / 공수 |
|---|---|---|---|---|
| **U1** | mice-market-intel | ① CP1 GO-4 잔여: company-intel "7렌즈+4진입점+후속체이닝"(T7 렌즈 보강) ② ECC 경쟁분석 3종 요지 — 경쟁사 티어링, 9차원 가중 스코어링(긴장축 분리), 의사결정형 리포트 구조 | deanpeters/Product-Manager-Skills(웹) + ECC competitive-platform-analysis·benchmark-methodology·competitive-report-structure | 高 / 中 |
| **U2** | jc-doc-coauthor | 원본 doc-coauthoring 누락 2건 — ① 아티팩트 편집/초안 후 링크 제공 규칙 ② 기존 공유문서 편집 시 이미지 alt-text 체크(무맥락 독자 대비). ※ Stage3 가독성 축은 의도적 설계로 판단해 불채택, frustration 대응·엔티티 검색 확인은 低확신 보류 | doc-coauthoring SKILL.md(입수본=레포본 동일 확인) | 高 / 低 |
| **U3** | jc-skill-forge | ① skill-scout: 설치·제작 전 중복 검색 순서(로컬→마켓플레이스→GitHub→웹) ② skill-stocktake: Quick Scan/Full Stocktake 2모드 품질 감사 | ECC skill-scout·skill-stocktake | 高 / 低 |

## B. GO 대기 — 4건 (구조 변경 or 확신도 中, 별도 승인 카드)

| # | 제안 | 내용 | 확신도 / 공수 | 리스크 |
|---|---|---|---|---|
| **N1** | NEW: 브랜드 디스커버리(가칭 jc-brand-discovery) | 8모듈 브랜드 정체성 인터뷰(다중세션) — 라이브러리 실공백(jc-design-system은 토큰, 이건 브랜드 전략 발굴). MICE 행사 아이덴티티·Track B 개인 브랜드에 적용 | 高 / 中(신규 저작) | 신규 스킬 = jc-skill-creator 하우스 표준 전체 사이클 필요 |
| **N2** | NEW: 구글 워크스페이스 운영(가칭 jc-workspace-ops) | Drive/Docs/Sheets/Slides 통합 운영 워크플로 — 워크스페이스가 실제로 Google Drive 기반이라 접점 있음 | 中-高 / 中 | 기보유 Drive MCP·플랫폼 내장 기능과 중복 가능성 검증 필요 |
| **U4** | UPGRADE: jc-orchestrator ← ECC blueprint | 안티패턴 카탈로그·병렬 스텝 탐지·자기완결 컨텍스트 브리프 | 中 / 中 | v1.1.0(7/10) 직후라 비대화 위험, jc-prompt-builder와 브리프 역할 중첩 소지 |
| **U5** | UPGRADE: jc-redteam ← ECC santa-method(+council) | 독립 이중 리뷰어 수렴 루프("둘 다 통과해야 출하") + 4보이스 결정 프레임 | 中 / 低-中 | CP1 감사 '조치불요' 스킬 — 검증 강도 향상 vs 프로세스 비대화 트레이드오프 |

## C. SKIP — 대표 항목과 사유

| 항목 | 사유 |
|---|---|
| image-enhancer(단품) | 스크립트·기법 전무한 프롬프트 껍데기. Higgsfield MCP(upscale_image·remove_background)와 완전 중복. 저작 품질 기준(RED→GREEN·반례) 미달 |
| superpowers 전체(13종) | CP1 이후 델타 0. 기흡수 2종(writing-skills·verification-before-completion) 확장 없음. 나머지는 순수 SW 개발 도구(CP1 판정 유지) |
| anthropics/skills 레포 | 업스트림 7/1 이후 커밋 0 — 델타 없음 |
| ECC prompt-optimizer·token-budget-advisor | jc-prompt-builder 프로토콜 v1 자구 동결(§8 재증류 게이트) — 다음 재증류 시 참고 후보로만 기록 |
| ECC plan-orchestrate | jc-orchestrator 킥오프·핸드오프 설계와 중복 |
| ECC agent-self-evaluation | jc-redteam 3축 감수와 중복(5축 자가채점은 자기평가라 적대 검증보다 약함) |
| ECC rules-distill | jc-skill-creator의 상위 skill-creator 위임 구조와 상충 |
| ECC product-lens | jc-prompt-builder 브리프 게이트("왜" 검증)와 중복 |
| ECC frontend-slides | mice-proposal·pptx·jc-theme-factory 경계에 걸침 — 후순위 보류(차기 인테이크 재평가) |
| ECC make-interfaces-feel-better | jc-design-system 컴포넌트 패턴과 중복, 참고만 |
| ECC nutrient / visa-doc-translate / lead-intelligence·social-graph-ranker | 유료 API 종속 / macOS 종속·니치 / B2B SaaS 전제(低-中) |
| ECC 나머지 ~240종 | 언어·프레임워크 코딩, 테스트/CI/DB, 크립토, 헬스케어, 홈랩 등 도메인 불일치(상세: ecc-scan.md) |

## D. 참고 기록 (인테이크 대상 외)

- ECC `agents/chief-of-staff.md` — 다채널(이메일·Slack 등) 4단계 트리아지+답장 초안 에이전트. jc-comms(작성)와 다른 축(분류·팔로우스루) — 향후 에이전트 팩토리(jc-orchestrator) 아키타입 참고.
- CP1 이월 검토 항목 재상기: stakeholder-mapping류 NEW 후보(deanpeters, CP1 §B-2) — 여전히 미결. N1 GO 판단 시 함께 고려 가치.
- jc-prompt-builder 차기 재증류(§8) 참고 후보: ECC prompt-optimizer 6단계 파이프라인, token-budget-advisor.

---

## 처리 상태 (2026-07-12 종결)

- [x] U1~U3 적용 (서브에이전트, _archive 백업 선행)
- [x] N1·N2·U4·U5 GO 카드 회신 — **4건 전부 GO** → 적용 완료 (N2는 중복 검증 통과 후 범위 축소 저작)
- [x] 적용분 jc-redteam 스팟 검증 — Critical 0 · Major 2(신규 2종 LICENSE.txt 누락 → 즉시 해소) · Minor 5 백로그
- [x] PROGRESS.md 인테이크 로그 기재 ([CP3] 섹션)

**최종 결과**: UPGRADE 5건(mice-market-intel v1.0.4 · jc-doc-coauthor v1.0.1 · jc-skill-forge v1.0.3 · jc-orchestrator v1.1.2 · jc-redteam v1.2.2) + NEW 2건(jc-brand-discovery v1.0.0 · jc-workspace-ops v1.0.0) — 라이브러리 자사 24→26종. 백업: `library/_archive/20260712/`. 배포본(~/.claude/skills) 동기화 완료, claude.ai zip·git은 수동 동기화 대기.
