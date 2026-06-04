# JC MICE 스킬 라이브러리

개인 MICE 전략가용 Claude 스킬의 **단일 진실 공급원(Source of Truth)** 레포입니다.
claude.ai 웹 설치본에서 추출한 9종 + 파생 2종(jc-artifact-builder·jc-landing-page), 총 11종을 git으로 버전 관리하며, 앞으로 이 레포에서
스킬을 **업그레이드 · 통합 · 폐합**합니다.

## 스킬 카탈로그 (11종)

| 스킬 | 버전 | 역할 | 주요 산출물 |
|------|------|------|------------|
| `jc-design-system` | v1.2.0 | 디자인 토큰 시스템 (다른 스킬이 참조하는 reference 자산, 인포그래픽 스케일 포함) | 토큰·컴포넌트 패턴 |
| `jc-redteam` | v1.1.0 | 결론·완성 산출물 적대적 재검증 (+ LP 마케팅 패널 모드) | Quick Strike / Deep Audit / LP 패널 |
| `jc-artifact-builder` | v1.0.0 | jc 테마가 기본 적용된 claude.ai 인터랙티브 아티팩트(React+shadcn) 빌더 | 단일 HTML 아티팩트 |
| `jc-landing-page` | v1.1.0 | jc 테마 B2B 모바일 랜딩페이지(고정스케일·GAS 폼). 검증은 jc-redteam LP 패널 | 단일 HTML LP |
| `mice-rfp-analyzer` | v1.0.1 | RFP·비딩 공고를 7축으로 분석 | .docx 보고서 + .xlsx 평가 매트릭스 |
| `mice-proposal` | v2.1.1 | RFP 기반 MICE 제안서 자동 구성 | .pptx 제안서 |
| `mice-estimate` | v2.0.0 | 견적서 생성 (M&C 산출내역서 / 리멤버 양식) | .xlsx 견적서 |
| `mice-sponsor-deck` | v2.0.0 | 스폰서·협찬·후원사 유치 영업 데크 | HTML 데크 (+ PPTX / 매트릭스 XLSX) |
| `pt-script` | v2.0.0 | 발표 대본·MC 멘트 생성 | .docx 스크립트 |
| `mice-dashboard` | v2.0.0 | KPI·차트·인포그래픽 대시보드 | 단일 HTML + PDF |
| `mice-meeting-minutes` | v2.1.0 | 회의록 transcript를 8축으로 구조화 | 인터랙티브 HTML 대시보드 |

### 체이닝 흐름 (참고)

```
mice-rfp-analyzer ──► mice-proposal ──► pt-script
mice-meeting-minutes ──► mice-proposal / mice-estimate
mice-estimate · mice-meeting-minutes ──► mice-dashboard
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
