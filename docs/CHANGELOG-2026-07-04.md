# CHANGELOG — 스킬 라이브러리 풀 업그레이드 (2026-07-04 확정판)

> 소스: `Skills/library/` (정본) · 산출: `dist/2026-07-04/`
> 누적 3라운드: **Phase 4(CP1 GO-1~4)** + **CP-N5(브리프 게이트 역참조)** + **CP2(Deep Audit Major 수정)**

---

## 버전 범프 대조표

| 스킬 | 이전 | 현행 | 사유 (라운드) |
|------|------|------|--------------|
| mice-dashboard | v2.0.1 | **v2.0.2** | GO-1: 범용 트리거 스코핑(data 계열 충돌 방지) · +역참조 |
| mice-estimate | v2.2.0 | **v2.2.1** | GO-1: ChainPayload `generatedAt` 필드 + 정본 §8 표 정합 · +역참조 |
| mice-meeting-minutes | v2.1.0 | **v2.1.2** | GO-1: 레거시 .docx/.xlsx 서술 정리(v2.1.1) · **CP2: 크기 게이트 100→50KB 정합, RULE-NO-COMPANY 예시 전량 변수/가명화, 레거시 .docx→.html(v2.1.2)** · +역참조 |
| jc-brand-styling | v1.0.0 | **v1.0.1** | GO-2: jc-theme-factory 트리거 중첩 인라인 판별 · +역참조 |
| jc-design-system | v1.3.0 | **v1.3.1** | GO-2: 호출절차 일원화 · GO-3: chaining-protocol §8 표 정합화 (역참조 예외 — reference 자산) |
| jc-generative-art | v1.0.1 | **v1.0.2** | GO-2: 죽은 교차참조 3곳 정정 · +역참조 |
| jc-strategy-canvas | v1.0.0 | **v1.0.2** | GO-2: check_drift.py 죽은 참조 제거 · GO-4: PESTLE 확장 프레임워크(v1.0.1) · **CP2: 추적성 보강 — 자율채택 등재·GO-4 몫 명문화(v1.0.2)** (역참조 예외 — 한도초과) |
| mice-market-intel | v1.0.1 | **v1.0.3** | GO-2: chaining 예시버전 정합 · GO-4: 미방어 세그먼트 렌즈(v1.0.2) · **CP2: v1.0.1 이력 행 백필·back-ref 명기(v1.0.3)** · +역참조 |
| mice-proposal | v3.0.0 | **v3.0.1** | GO-2: ChainPayload 봉투 소비 문서화 · +역참조 |
| mice-rfp-analyzer | v2.0.0 | **v2.0.1** | GO-2: 모드 용어 통일 · +역참조 |
| mice-sponsor-deck | v2.0 | **v2.0.1** | GO-3: sample_generator.py `icejc` 하드코딩 경로→상대경로 · +역참조 |
| jc-skill-forge | v1.0.1 | **v1.0.2** | GO-4: writing-skills 검증 루프 흡수 · +역참조 |
| jc-skill-creator | v1.0.0 | **v1.0.1** | GO-4: writing-skills 검증 루프 · +역참조 |
| jc-visual-philosophy | v1.0.0 | **v1.0.1** | GO-4: frontend-design 패턴("AI스러운 기본값 회피") · +역참조 |
| jc-theme-factory | v1.0.1 | **v1.0.2** | GO-4: frontend-design 2-pass 비평 루프 · +역참조 |
| jc-redteam | v1.2.0 | **v1.2.1** | GO-4: verification-before-completion 이식 (역참조 예외 — 게이트 직행 카브아웃) |
| jc-artifact-builder | (없음) | (없음) | GO-2: 버전핀 검증일 주석 · +역참조 (version frontmatter 원래 없음 — 가드레일상 신설 금지) |
| jc-landing-page | (없음) | (없음) | GO-2: CDN 검증일·트리거 동의어 · +역참조 (동상) |
| jc-comms · jc-doc-coauthor · jc-mcp-builder · pt-script | (무변경 버전) | 동일 | Phase 4 미대상, **+역참조만** (description 말미) |
| **jc-prompt-builder** | — | **v1.0.0** | N5 신규 빌드(브리프 게이트 상시 레이어). CP2에서 `library/`로 이동(라우팅 EXCLUDE 유지) |

## 역참조 레이어 (CP-N5)
22종 중 **19종** description 말미에 `실행형 지시는 실행 전 jc-prompt-builder 브리프를 거친다.` 삽입. 예외 3종: jc-strategy-canvas(한도초과)·jc-design-system(reference 자산)·jc-redteam(게이트 직행 예외). 상세: `library/jc-prompt-builder/references/routing-map.md` §6.

## CP2 Deep Audit 결과
18종 감사 → **Critical 0**. Major 6건(3종) 전량 해소(위 CP2 표). Minor 14건은 백로그(대부분 기존·스타일 티어).

## claude.ai 교체 업로드 대상
`dist/2026-07-04/*.zip` — 22 라우팅 스킬 전량(Phase4/역참조/CP2로 모두 변경됨). jc-prompt-builder.zip은 N5서 이미 업로드된 v1.0.0과 내용 동일(위치만 이동) — 재업로드 선택.
