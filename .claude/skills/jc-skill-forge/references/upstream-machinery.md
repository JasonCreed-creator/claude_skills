# Upstream Machinery — 상위 skill-creator 평가 기계 포인터

Anthropic 공식 `skill-creator`(claude.ai 예제 스킬 / anthropics/skills 레포)에는 스킬 평가 기계가 있다. 복제하지 말고 찾은 위치에서 호출한다. 스킬 제작·개선 자체는 `jc-skill-forge`가 맡고 skill-creator는 평가 기계로만 쓴다.

현재 claude.ai 동기화본 `~/.claude/skills/synced/*/skill-creator/`에 있다(2026-10-09 확인 — 약 10분마다 갱신, 편집 금지).

**탐색 순서**: ① `~/.claude/skills/skill-creator`(개인 설치, 우선) → ② `~/.claude/skills/synced/*/skill-creator/`(claude.ai 동기화본) → ③ 둘 다 없으면 anthropics/skills에서 받아 ①에 둔다.

## 무엇이 있나

아래 경로는 위 탐색 순서로 찾은 `skill-creator/` 폴더 기준이다.

| 자원 | 용도 |
|------|------|
| `skill-creator/eval-viewer/generate_review.py` | 테스트 결과를 정성 리뷰 HTML로(헤드리스 `--static`) |
| `skill-creator/scripts/aggregate_benchmark.py` | with-skill vs baseline 집계 |
| `skill-creator/scripts/improve_description.py` | 트리거 정확도 최적화 루프(claude CLI 필요 — 이 PC는 `~/.local/bin/claude.exe` 전체 경로) |
| `skill-creator/scripts/package_skill.py` | `.skill` 패키징(우리는 `build_skills.py`로 대체 — ZIP만) |
| `agents/grader.md` 등 | 채점·분석·비교 에이전트 |

## 언제 쓰나

- **객관적 산출 스킬**(변환·추출·고정 워크플로우): evals.json 2~3개 → with/without 실행 → 집계.
- **주관적 산출 스킬**(디자인·글쓰기): 억지 assertion 대신 `jc-redteam` 정성 검증.
- **트리거가 약하면**: 현실적 한국어 should-trigger 8~10 + 형제 near-miss should-not-trigger 8~10으로 description 최적화. 결과는 1,024자 상한 안에서.

## 접점

기계는 품질 측정, `house-conventions.md`는 정체성. 어느 기계로 만들든 마감은 하우스 자가점검을 통과해야 한다.
