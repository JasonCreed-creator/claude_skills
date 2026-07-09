# JC MICE 스킬 라이브러리

> **⚡ 2026-07-04 — Drive 정본 풀 업그레이드 동기화 (확정판)**
> 이 브랜치는 Google Drive `Skills/library/`(정본)를 반영한다. 3라운드 누적: **Phase 4(CP1 GO-1~4)** + **CP-N5(브리프 게이트 역참조)** + **CP2(Deep Audit Major 수정, Critical 0)**.
> - **22종 업그레이드** — 최신 버전·범프 사유는 [`docs/CHANGELOG-2026-07-04.md`](docs/CHANGELOG-2026-07-04.md). 각 `SKILL.md` frontmatter의 `version`이 버전 정본.
> - **신규 +1: `jc-prompt-builder` v1.0.0** — 실행 직전 러프 지시를 '업그레이드 브리프'로 증강하는 default-on 선행 게이트(라우팅 대상 아님; 22종 중 19종 description 말미에 역참조 삽입, 예외 3종).
> - **보존: `mice-run-of-show`·`mice-aftermath`** — 6월 forge 신규, Drive 미포함이나 삭제 없이 유지.
> - 카탈로그 **24 → 25종**. 아래 표의 버전 셀은 6월 스냅숏 — 현행 최신은 본 배너·CHANGELOG·각 `SKILL.md`가 정본이다.

개인 MICE 전략가용 Claude 스킬의 **단일 진실 공급원(Source of Truth)** 레포입니다.
claude.ai 웹 설치본에서 추출한 9종 + 파생 2종(jc-artifact-builder·jc-landing-page) + **기본 프리셋 개조 8종** + 라이브러리 관리 1종 + 외부 인테이크 신규 2종 + 운영 신규 2종(mice-run-of-show·mice-aftermath) + **선행 게이트 1종(jc-prompt-builder)**, 총 **25종**을 git으로 버전 관리하며, 앞으로 이 레포에서
스킬을 **업그레이드 · 통합 · 폐합**합니다. 기본 프리셋 개조 프로그램은 `docs/preset-optimization-roadmap.md`(진행) · `docs/preset-adaptation-playbook.md`(방법) 참조.

## 스킬 카탈로그 (24종)

| 스킬 | 버전 | 역할 | 주요 산출물 |
|------|------|------|------------|
| `jc-design-system` | v1.2.0 | 디자인 토큰 시스템 (다른 스킬이 참조하는 reference 자산, 인포그래픽 스케일 포함) | 토큰·컴포넌트 패턴 |
| `jc-redteam` | v1.1.0 | 결론·완성 산출물 적대적 재검증 (+ LP 마케팅 패널 모드) | Quick Strike / Deep Audit / LP 패널 |
| `jc-artifact-builder` | v1.0.0 | jc 테마가 기본 적용된 claude.ai 인터랙티브 아티팩트(React+shadcn) 빌더 | 단일 HTML 아티팩트 |
| `jc-landing-page` | v1.1.0 | jc 테마 B2B 모바일 랜딩페이지(고정스케일·GAS 폼). 검증은 jc-redteam LP 패널 | 단일 HTML LP |
| `mice-rfp-analyzer` | v1.0.1 | RFP·비딩 공고를 7축으로 분석 | .docx 보고서 + .xlsx 평가 매트릭스 |
| `mice-proposal` | v2.1.1 | RFP 기반 MICE 제안서 자동 구성 | .pptx 제안서 |
| `mice-estimate` | v2.1.0 | 견적서 생성 (M&C 산출내역서 / 리멤버 양식) + 전략 프라이싱 | .xlsx 견적서 |
| `mice-sponsor-deck` | v2.0.0 | 스폰서·협찬·후원사 유치 영업 데크 | HTML 데크 (+ PPTX / 매트릭스 XLSX) |
| `pt-script` | v2.0.0 | 발표 대본·MC 멘트 생성 | .docx 스크립트 |
| `mice-run-of-show` | v1.0.0 | 행사 운영 큐시트(run of show)·진행 시나리오. 시간 무결성 자동검증 | 버전드 XLSX(10컬럼) + 변경이력 |
| `mice-dashboard` | v2.0.0 | KPI·차트·인포그래픽 대시보드 | 단일 HTML + PDF |
| `mice-meeting-minutes` | v2.1.0 | 회의록 transcript를 8축으로 구조화 | 인터랙티브 HTML 대시보드 |
| `mice-aftermath` | v1.0.0 | 행사 사후 종합 결과보고서 + 재사용 레퍼런스 케이스(영업 재활용) | 결과보고서(HTML/md) + ChainPayload(→proposal/sponsor-deck) |

### 기본 프리셋 개조 8종 (preset → jc)

원본 프리셋 스킬을 jc 생태계(jc-design-system SoT)에 맞춰 개조. 관통 원칙: **jc는 홈베이스(기본값), 자유는 명시적 opt-in.**

| 스킬 | 버전 | 원본 프리셋 | 역할 | 주요 산출물 |
|------|------|------------|------|------------|
| `jc-theme-factory` | v1.0.0 | theme-factory | 시그니처+오버레이 쇼케이스·선택·발행·적용 (테마 프론트엔드) | 쇼케이스 HTML + 검증 스크립트 |
| `jc-brand-styling` | v1.0.0 | brand-guidelines | 기존 PPTX/HTML에 jc 시그니처 입히는 후처리 엔진 | `style_pptx.py` |
| `jc-comms` | v1.0.0 | internal-comms | 한국 B2B·MICE 내부/대외 커뮤니케이션 글쓰기 | 3P·뉴스레터·FAQ·보고 |
| `jc-doc-coauthor` | v1.0.0 | doc-coauthoring | MICE 문서 3단계 공동작성 (검증=jc-redteam) | 산문 문서 |
| `jc-visual-philosophy` | v1.0.0 | canvas-design | 미학 선언→정적 캔버스 아트 (홈베이스/자유모드) | .md + .pdf/.png |
| `jc-generative-art` | v1.0.0 | algorithmic-art | p5.js 제너러티브 아트 (뷰어 jc 리브랜딩) | 단일 HTML 아티팩트 |
| `jc-mcp-builder` | v1.0.0 | mcp-builder | MICE 도구 커넥터용 MCP 서버 개발 가이드 | MCP 서버 |
| `jc-skill-creator` | v1.0.0 | skill-creator | jc 하우스 규칙 메타 층 (스킬 제작·개조 표준) | 스킬 |

### 라이브러리 관리 (신규)

| 스킬 / 커맨드 | 종류 | 역할 |
|------|------|------|
| `jc-skill-forge` | 스킬 | 외부 스킬 생태계 대조 → 내 라이브러리 업그레이드·통폐합·신규보강. 읽기전용 스캔 → 승인 게이트 → 승인분만 적용 |
| `/skillupgrade` | 슬래시 커맨드 | 위 워크플로우의 커맨드 버전 (`.claude/commands/`, `$ARGUMENTS`로 범위 한정) |

> `jc-skill-forge`는 *외부 대조를 통한 라이브러리 진화*, `jc-skill-creator`는 *하우스 표준 스킬 제작*. 둘은 자매 관계다. 두 형태(스킬+커맨드)는 같은 인테이크 워크플로우를 자동 트리거/명시 호출로 각각 제공한다.

### 외부 인테이크 신규 (forge)

`jc-skill-forge` / `/skillupgrade` 워크플로우로 외부 생태계 패턴을 흡수해 신규 보강한 스킬 (파일 복사 없이 패턴만 흡수, jc 네이티브 재구성).

| 스킬 | 버전 | 흡수 패턴(출처) | 역할 | 주요 산출물 |
|------|------|----------------|------|------------|
| `jc-strategy-canvas` | v1.0.0 | 전략 프레임워크 (maigentic/stratarts, MIT) | 6대 프레임워크(BMC·5 Forces·SWOT/TOWS·JTBD·포지셔닝·TAM/SAM/SOM)로 전략 구조화, 검증=jc-redteam | 전략 캔버스 HTML + ChainPayload(→proposal/rfp) |
| `mice-market-intel` | v1.0.0 | 2단계 구조화 리서치 (Weizhena/Deep-Research, MIT) | MICE 시장·경쟁·동향·스폰서·벤치마크 데스크 리서치(출처 티어링·HITL) | 리서치 리포트(md/HTML) + ChainPayload(→strategy-canvas/rfp/proposal/sponsor) |

### 체이닝 흐름 (참고)

```
mice-rfp-analyzer ──► mice-proposal ──► pt-script
mice-proposal · pt-script ──► mice-run-of-show (행사 운영 큐시트)
mice-market-intel ──► jc-strategy-canvas / mice-rfp-analyzer / mice-proposal (시장·경쟁 근거)
jc-strategy-canvas ──► mice-proposal / mice-rfp-analyzer (전략 논거)
mice-meeting-minutes ──► mice-proposal / mice-estimate
mice-estimate · mice-meeting-minutes ──► mice-dashboard
mice-dashboard · mice-estimate · mice-meeting-minutes · mice-run-of-show ──► mice-aftermath ──► mice-proposal / mice-sponsor-deck (사후 결과·재사용 케이스)
jc-design-system ──► (모든 산출물 스킬이 디자인 일관성 위해 참조)
모든 산출물 ──► jc-redteam (최종 검증)
```

## 디렉터리 구조

```
.claude/skills/<스킬명>/
  ├─ SKILL.md          # 스킬 정의 (frontmatter: name/version/description)
  ├─ references/       # 참조 문서 (.md)
  ├─ scripts/          # 실행 스크립트 (.py)
  └─ assets/           # 템플릿 (.html / .xlsx)
```

## 사용법

1. 이 레포를 클론한 뒤 **레포 루트에서 Claude Code를 실행**하면 `.claude/skills/` 가 자동 인식됩니다.
2. 또는 개별 스킬 폴더를 `~/.claude/skills/` 로 심볼릭 링크/복사해 전역 사용할 수 있습니다.
3. 작업 후 변경된 스킬을 각각 zip으로 묶어 **claude.ai 웹 → Settings → Features** 에 재업로드하면 웹에도 반영됩니다.

### 의존성

일부 스킬의 스크립트는 다음 패키지를 사용합니다 (각 SKILL.md frontmatter의 `dependencies` 참조).

- `pandas`, `openpyxl` — 데이터·엑셀 처리 (mice-estimate, mice-dashboard 등)
- `playwright` — HTML → PDF 렌더링 (mice-dashboard)

## 업그레이드 · 통합 워크플로우 가이드

이 레포를 스킬 관리의 베이스로 쓰기 위한 권장 규칙:

- **버전**: 스킬을 수정하면 해당 `SKILL.md` frontmatter의 `version` 을 올립니다 (SemVer 권장).
- **브랜치**: 변경은 작업 브랜치에서 진행하고 PR로 병합합니다.
- **커밋 메시지**: `<스킬명>: <변경 요약>` (예: `mice-estimate: 리멤버 양식 할인 로직 보강`).
- **통합/폐합**: 스킬을 합치거나 없앨 때는 커밋 메시지·PR 본문에 사유와 대체 스킬을 남깁니다.
- **검증**: 산출물 품질은 `jc-redteam` 으로 최종 점검합니다.
