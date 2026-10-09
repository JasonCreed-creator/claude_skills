# Upstream Machinery — 상위 skill-creator 기계 활용 포인터

스킬 제작의 *범용 기계*는 상위 skill-creator(`/mnt/skills/examples/skill-creator`)에 이미 있다. 복제하지 말고 필요할 때 호출한다. 본 문서는 "언제 어떤 것을 쓰는지"의 포인터다(스크립트 인자 상세는 그 스킬의 SKILL.md 정본).

## 무엇이 거기 있나

| 자원 | 경로 | 용도 |
|------|------|------|
| eval-viewer | `eval-viewer/generate_review.py` | 테스트 결과를 정성 리뷰용 HTML로(헤드리스면 `--static`) |
| 벤치마크 집계 | `scripts/aggregate_benchmark.py` | with-skill vs baseline pass_rate·시간·토큰 집계 |
| description 최적화 | `scripts/improve_description.py` | 트리거 정확도 최적화 루프(claude CLI 필요) |
| 패키징 | `scripts/package_skill.py` | `.skill` 파일 산출 |
| 채점/분석 에이전트 | `agents/grader.md`·`analyzer.md`·`comparator.md` | assertion 채점·결과 분석·블라인드 비교 |
| 스키마 | `references/schemas.md` | evals.json·grading.json 구조 |

## 언제 쓰나 (jc 판단 기준)

### 객관적 산출 스킬 → 상위 기계로 정량 평가
파일 변환·데이터 추출·고정 워크플로우처럼 **정답이 검증 가능**하면 상위 기계를 쓴다:
1. `evals/evals.json`에 현실적 테스트 prompt 2~3개.
2. with-skill / baseline 동시 실행 → 결과를 워크스페이스에 저장.
3. `aggregate_benchmark.py`로 집계, `generate_review.py`로 뷰어(헤드리스 환경은 `--static`).
4. 사용자 피드백 반영 → 반복.

### 주관적 산출 스킬 → jc-redteam 정성 검증으로 대체
디자인·글쓰기·아트처럼 **사람 판단이 필요**하면 억지 assertion을 만들지 말고, 이 레포 관행대로 `jc-redteam`(3축: 내용·오탈자·대안)으로 정성 검증한다. 기존 jc 스킬들(jc-landing-page 등)이 이 방식을 따른다.

### 트리거가 약하면 → description 최적화
스킬이 덜/잘못 트리거되면 `improve_description.py`로 최적화. eval 쿼리는 **현실적 한국어**(should-trigger 8~10 + 형제 스킬과 겹치는 near-miss should-not-trigger 8~10). claude CLI(`claude -p`)가 있어야 동작.

### 납품/배포 → 패키징
`package_skill.py <skill-dir>`로 `.skill` 생성 후 claude.ai에 업로드(README §사용법 참조).

## 헤드리스/원격 주의

- 브라우저·디스플레이가 없으면 `generate_review.py --static <out.html>`로 정적 리포트를 만들고 링크를 제시한다.
- 서브에이전트가 없는 환경(claude.ai)에서는 baseline 비교를 건너뛰고 정성 피드백 중심으로.

## jc 하우스와의 접점

상위 기계로 *무엇이든* 만들든, 최종 산출 스킬은 본 스킬의 **하우스 불변식**(`house-conventions.md`)과 **마감 절차**(SKILL.md)를 통과해야 한다. 기계는 품질 측정을, 하우스 규칙은 jc 정체성을 책임진다.
