# R1 — JC Design SoT 정합화 검증 리포트

- **일자:** 2026-06-02
- **브랜치:** `claude/relaxed-fermat-M5h5C` (PR #1)
- **범위:** 스킬 9종 유지(병합·삭제 없음). consumer 6종이 하드코딩으로 보유한 디자인 토큰을 `jc-design-system`(SoT)에 정합화.

## 확정 결정 (Phase 0 게이트)

| 항목 | 결정 |
|------|------|
| **D1 다크 배경 패밀리** | **SoT `#0A1220` 계열 정본 채택** (덱 다크 톤이 약간 깊어지는 의도적 시각 변화 수용). `mode-mapping §3` 무변경. |
| **작업 범위** | **문서 + 템플릿 + 스크립트 전체** (reference 정규화 + assets/scripts의 drift hex 정본 교정). |
| **D2 라이트 차트** | SoT 5색 정본 유지. 6-series 차트(dashboard)가 깨지지 않도록 **`--jc-data-6 = #7C3AED` 확장 슬롯 신설**(다크 보정 `#A78BFA`). |
| **D3 다크 차트 / D4 Tier 다크** | SoT `§3.2` / `§7` 정본 유지, consumer를 여기에 정합. |

## Phase별 산출

- **Phase 0 — SoT 정본:** `signature-tokens.md`(§1.4 표·§6 JSON)·`mode-mapping.md`(§3.2)에 `--jc-data-6` 추가. (commit `R1 Phase 0`)
- **Phase 1 — consumer 와이어링 (스킬당 1 서브에이전트, 자기 폴더만 수정):**
  | 스킬 | 핵심 교정 |
  |------|----------|
  | `mice-estimate` | Excel drift(`#003366`·`#FF6D01`·`#434343`) → SoT 시그니처 토큰 역할 매핑 + 미러 주석. 산출 로직 무변경. |
  | `pt-script` | `FFE5DD` → `--jc-point-orange-softest #FFF3E0`. WCAG 대비비 → SoT `§9.5` 정본. 금칙어 sanitize 보존. |
  | `mice-proposal` | 다크 `DARK_*`(`#0A2540→#0A1220` 등) → `§3` 미러, 다크 accent `#2962FF→#5B8DEF`. |
  | `mice-dashboard` | slate 3종 → SoT 다크(역할 분기: `#1e293b` 라이트텍스트=`#1A1D24` / 다크카드=`#152134`). 6색 Tailwind 차트 → SoT data-1..6. 콜아웃 다크값 `§8`. |
  | `mice-sponsor-deck` | 덱 다크(`#0A2540`/`#1A3556`/`#12304D`) → SoT(`#0A2540`은 primary/data-5/표지 용도만 유지). 다크 Tier `§7`(`E91E63→F06292` 등). |

## Phase 2 — 검증 결과

| 체크 | 결과 |
|------|------|
| in-scope consumer의 **비-canon LIVE drift** 잔존 | **0건** (주석/교정이력 제외 grep) |
| 다크 정본 일치 (`mode-mapping §3`) | ✅ consumer 6종 일치 |
| 차트 시리즈 (라이트 `§1.4`+data-6 / 다크 `§3.2` / Tier `§7`) | ✅ 일치 |
| SoT `§6` JSON 유효성 (Phase 0 편집) | ✅ 파싱 OK, `data` 6색 |
| 수정 스크립트 구문 (`export_estimate`·`build_script`·`sample_generator`) | ✅ `ast.parse` 통과 |
| WCAG | ✅ SoT `§3`/`§9.5` 정본(다크 본문 AAA, `#E8ECF2` on `#0A1220` ≈ 14.96:1) 채택 |
| 회귀 | ✅ D1 의도적 변화(덱 다크 bg `#0A2540→#0A1220`)만, 사용자 승인 |
| 빌드 스모크 | ⚠️ 스크립트 구문·HTML 정적 구조 확인. 실제 렌더 스모크는 `openpyxl`/`playwright` 미설치로 본 환경 미수행 |

## 잔존 / 후속 권고 (R1 범위 밖)

1. **`infographic-patterns.md` (매체별 구현, 명세상 보존 대상)** — `mice-dashboard`에 Tailwind 팔레트 22색(`#F59E0B`·`#EF4444`·`#3B82F6` 등) off-canon, `mice-proposal`에 `#94A3B8`(slate) 1색. 인포그래픽 정합은 별도 패스로 권고.
2. **체이닝 정의 중복(R2) / 공통 룰 블록 통합(R3 일부)** — 본 R1 범위 밖, 분리 진행 권고.
3. **`mice-proposal/references/slide-masters.md` 개인정보** — R1과 무관한 별도 사안. 레포가 public이므로 필요 시 플레이스홀더 치환/비공개 전환 권고.
