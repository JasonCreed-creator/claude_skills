# archive/ — 폐합 스킬·레거시 파일 보관소

`jc-skill-forge` 원칙 "폐합은 삭제가 아니라 아카이브"를 git에서 구현한 폴더다. `.claude/skills/` 밖에 있으므로 Claude Code는 이 안의 스킬을 로드하지 않는다. `_archive/`(gitignore, 로컬 롤백 백업)와는 다른 폴더다.

| 경로 | 내용 | 기준 |
|------|------|------|
| `skills/<name>/` | 폐합 스킬 20종 — 2026-10-05 `jc-skill-forge/scripts/lint_skills.py`의 `ARCHIVED` 목록 | 마지막 업로드본(claude.ai 2026-10-02) 또는 레포 마지막 버전 그대로. 내용 수정 없음 |
| `legacy/` | 스킬이 아닌 구 운영 파일 — `/skillupgrade` 슬래시 커맨드(forge 모드 A와 중복·구 모델 ID), `build-skills.sh`(forge `build_skills.py`와 중복), 9종 시절 `_README.txt` | 2026-10-09 교통정리 |

## 복구

- 폴더째: `git mv archive/skills/<name> .claude/skills/<name>` 후 lint ERROR 0까지 개정(폐합 참조·구 룩·게이트 문구가 남아 있다) → `version` 범프 → `lint_skills.py`의 `LIVE`/`ARCHIVED` 집합 갱신.
- 역량 일부만: 해당 reference/script를 라이브 후속 스킬의 `references/`로 옮기고 출처를 변경 이력에 적는다(§계승 기록은 `docs/stocktake-2026-10-09.md`).
- 교통정리 직전 전체 상태: 태그 `pre-reorg-2026-10-09`.

## 폐합 → 후속 매핑 (2026-09-21 재편 · 10-05 확정)

| 폐합 | 후속(라이브) | 흡수 범위 |
|------|-------------|----------|
| mice-proposal · mice-sponsor-deck | jc-pptx | 설득 설계·7섹션 골격·게이트 → `proposal-playbook.md`; 스폰서 덱(청중 프로파일·Tier·혜택·ROI 케이스·골격) → `jc-pptx/references/sponsor-deck.md`(v2.2.0 계승); 체이닝 source는 별칭 자동 치환 |
| mice-dashboard | mice-ops-docs | KPI 대시보드·차트 가이드(리멤버 토큰 재작성) |
| mice-weekly-performance | mice-slack-ops | 위클리 브리프(§2-1 + `weekly-brief.md`) |
| jc-comms | mice-slack-ops | 양식 4종(3P·뉴스레터·FAQ·일반) → `comms-templates.md` |
| jc-prompt-builder · jc-orchestrator · jc-workspace-ops | jc-session-protocol | 기획안 카드·킥오프·핸드오프·code-conductor·세션 2파일 리추얼 |
| jc-skill-creator | jc-skill-forge | 하우스 규약·저작 검증 루프·상위 기계 포인터 |
| jc-remember-html | jc-design-system · jc-pptx | 토큰·컴포넌트·로고·오브제 / 덱 템플릿 T1~T12 |
| jc-theme-factory · jc-brand-styling | jc-design-system(슬롯 3종·legacy-jc) · jc-pptx(`restyle_pptx.py`) | 오버레이 체계 축소, PPTX 리스킨 |
| jc-cinematic-html · jc-asana-html · jc-visual-philosophy · jc-generative-art · jc-brand-discovery · jc-landing-page · jc-artifact-builder · jc-mcp-builder | (후속 없음) | 룩은 리멤버 하나, 이미지·영상은 Higgsfield, React 앱은 프리셋 web-artifacts-builder. 필요 시 위 복구 절차 |
