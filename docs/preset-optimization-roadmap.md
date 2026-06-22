# 기본 프리셋 스킬 → jc 생태계 최적화 로드맵

Claude 기본 제공(프리셋) 스킬 세트를 **개인 MICE 전략가용 jc 생태계**(= `jc-design-system` 정본)에 맞게 개조하는 프로그램의 단일 트래커다. 작업이 여러 세션·여러 PR에 걸쳐도 이 문서가 진행 상태의 기준점이 된다.

> 개조 *방법*의 정본은 [`preset-adaptation-playbook.md`](preset-adaptation-playbook.md). 본 문서는 *무엇을·어디까지* 했는지만 추적한다.

## 관통 원칙

1. **jc는 홈베이스(기본값), 자유는 명시적 옵션** — 임의 팔레트·대체 브랜드·아트 모드는 silent default가 아니라 이름 붙은 opt-in으로만 노출한다. (`jc-design-system` 1원칙 "시그니처 고정 + 오버레이 차별화"를 전 스킬로 일반화.)
2. **토큰 값은 미러링 금지, SoT 런타임 참조** — `jc-design-system/references/signature-tokens.md §6 JSON` + `mode-mapping.md` + `client-overlays.md`. 구현체 `jc-design-system/scripts/jc_tokens.py`.
3. **생태계와 연결, 재발명 금지** — 검증=`jc-redteam`, 데이터 입출력=`ChainPayload/v1`(`chaining-protocol.md`), 디자인=`jc-design-system`.
4. **회사·개인 식별정보 하드코딩 금지** — `shared-rules.md#RULE-NO-COMPANY`, 외부 주입 변수만.
5. **하우스 워크플로우** — `jc-*` 명명, 한국어 우선·푸시형 description, SemVer, 커밋 `<스킬명>: <요약>`, 작업 브랜치 + 드래프트 PR, 최종 `jc-redteam` 점검.

## 로스터 & 상태

범례: ⬜ 미착수 · 🟦 진행중 · ✅ 완료(커밋) · ⏸ 보류

| # | 기본 프리셋 | jc 타깃 | 처분 | 상태 | 핵심 개조 |
|---|---|---|---|---|---|
| 1 | Theme Factory | `jc-theme-factory` | 개조 | ✅ | 10개 임의테마 택1 → 시그니처+클라이언트 오버레이 *쇼케이스·선택·발행(3토큰·색충돌·WCAG 검증)·적용*. 쇼케이스/검증 스크립트 번들 |
| 2 | Anthropic Brand Styling | `jc-brand-styling` | 개조 | ✅ | Anthropic 브랜드(오렌지·Poppins/Lora) → jc 시그니처(네이비·일렉트릭블루·Pretendard) PPTX·아티팩트 *적용 엔진* |
| 3 | Internal Comms | `jc-comms` | 개조 | ✅ | 3P·뉴스레터·FAQ·상태/인시던트 보고 → 한국어 B2B·MICE 프로젝트 맥락 + jc 비주얼 + jc-redteam 검증 |
| 4 | Doc Co-Authoring | `jc-doc-coauthor` | 개조 | ✅ | 3단계 공동작성 → MICE 문서(기획서·전략메모·의사결정문). Reader Testing을 `jc-redteam`으로 대체 |
| 5 | Visual Philosophy (캔버스 아트) | `jc-visual-philosophy` | 개조 | ✅ | 미학선언→캔버스(.md+.pdf/.png). 크롬·기본 팔레트 jc, '자유 아트 모드' 명시. 행사 키비주얼·데크 표지아트 |
| 6 | Algorithmic Art (p5.js) | `jc-generative-art` | 개조 | ✅ | 제너러티브 아트(.md+.html+.js). 뷰어 템플릿 Anthropic→jc 브랜딩, 기본 팔레트 jc 데이터컬러. 행사 모션배경·데이터아트 |
| 7 | MCP Server Dev Guide | `jc-mcp-builder` | 경량개조 | ✅ | 기술 내용 유지 + 용례를 MICE 도구 커넥터(견적/대시보드 데이터·Slack·Google) 중심으로 프레이밍 |
| 8 | Skill Creator | `jc-skill-creator` | 메타개조 | ✅ | 플레이북 내장 — 생성되는 모든 스킬이 하우스 스타일을 자동 준수. **v1.1.0 U1 완성**: 결정적 루브릭·anti-pattern·worked-example·quick/std/deep + `lint_skill.py` 자동채점기 |

> 추가 프리셋이 더 올라오면 이 표에 행을 덧붙인다(프로그램은 확장형).

## 의존 순서

```
preset-adaptation-playbook (방법 정본)
        │
        ├─ jc-theme-factory (선택·발행) ──┐
        │                                 ├─ 상호 참조 (선택 ↔ 적용)
        └─ jc-brand-styling (적용 엔진) ──┘
jc-comms / jc-doc-coauthor ──► 산출물 검증 jc-redteam
jc-visual-philosophy / jc-generative-art (아트, jc 기본값)
jc-mcp-builder (커넥터)
jc-skill-creator (플레이북을 코드/문서로 형식화 — 마지막)
```

## 변경 이력

- **jc-skill-creator U1 완성 (v1.1.0).** forge U1 의무 4대 요소(결정적 스코어링 루브릭·anti-pattern 라이브러리·worked-example·quick/std/deep) + 자동채점기 `scripts/lint_skill.py`(8기준 100점·GO/CONDITIONAL/NO-GO·`--self-test` PASS) 보강. lint=규약 게이트 / jc-redteam=품질 게이트 보완 구조 확립. PR #7 관찰 권고 해소.
- **1차 프로그램 완료 — 8종 전부 개조·커밋.** jc-theme-factory(쇼케이스·검증 스크립트) · jc-brand-styling(style_pptx self-test PASS) · jc-comms · jc-doc-coauthor(검증=jc-redteam) · jc-visual-philosophy · jc-generative-art(뷰어 Anthropic 잔재 0) · jc-mcp-builder(경량) · jc-skill-creator(메타). 전 스킬 FORBIDDEN 0건, 공유파일 오염 0건. 드리프트 가드 CONSUMERS에 디자인 소비 4종 등록.
- 프로그램 개시. 플레이북 + 로드맵 수립.
