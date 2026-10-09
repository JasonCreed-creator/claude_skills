# claude.ai 삭제·업로드 체크리스트 (2026-10-09)

기준: Code 동기화본 `~/.claude/skills/synced/<bucket>/manifest.json` 2026-10-09 13:55Z 실측(= 현재 claude.ai 업로드 상태 49종) × 번들 `jc-skills-live19-2026-10-09.zip`.
화면: claude.ai → Settings → Capabilities → Skills. 총 **삭제 38 · 업로드 19 · 끄기 1**.

## 1. 폐합 19종 — 삭제만 (재업로드 없음)

전부 10-02~10-03 업로드본으로 현재 남아 있음을 확인.

- [ ] jc-artifact-builder
- [ ] jc-asana-html
- [ ] jc-brand-discovery
- [ ] jc-brand-styling
- [ ] jc-cinematic-html
- [ ] jc-comms
- [ ] jc-generative-art
- [ ] jc-landing-page
- [ ] jc-mcp-builder
- [ ] jc-orchestrator
- [ ] jc-prompt-builder
- [ ] jc-remember-html
- [ ] jc-skill-creator
- [ ] jc-theme-factory
- [ ] jc-visual-philosophy
- [ ] jc-workspace-ops
- [ ] mice-dashboard
- [ ] mice-proposal
- [ ] mice-weekly-performance

## 2. 라이브 19종 — 동명 구버전 삭제 → 번들의 `.skill` 업로드

| 순서 | 삭제할 구버전(현재 업로드본) | 업로드할 파일 | 새 버전 |
|---|---|---|---|
| 1 | jc-design-system (10-05) | `jc-design-system.skill` | v2.2.0 |
| 2 | jc-skill-forge (10-05) | `jc-skill-forge.skill` | v2.2.0 |
| 3 | jc-session-protocol (10-05) | `jc-session-protocol.skill` | v1.2.0 |
| 4 | jc-redteam (10-05) | `jc-redteam.skill` | v1.4.0 |
| 5 | jc-pptx (10-05) | `jc-pptx.skill` | v2.3.0 |
| 6 | jc-kv-guide (10-05) | `jc-kv-guide.skill` | v1.2.0 |
| 7 | jc-doc-coauthor (10-05) | `jc-doc-coauthor.skill` | v1.2.0 |
| 8 | pt-script (10-05) | `pt-script.skill` | v2.3.0 |
| 9 | mice-rfp-analyzer (10-05) | `mice-rfp-analyzer.skill` | v2.2.0 |
| 10 | jc-strategy-canvas (10-05) | `jc-strategy-canvas.skill` | v1.2.0 |
| 11 | mice-market-intel (10-05) | `mice-market-intel.skill` | v1.2.0 |
| 12 | mice-run-of-show (10-05) | `mice-run-of-show.skill` | v1.2.0 |
| 13 | mice-aftermath (10-05) | `mice-aftermath.skill` | v1.2.0 |
| 14 | mice-slack-ops (10-05) | `mice-slack-ops.skill` | v1.3.0 |
| 15 | mice-ops-docs (10-05) | `mice-ops-docs.skill` | v1.2.0 |
| 16 | mice-team-board (10-05) | `mice-team-board.skill` | v1.1.0 |
| 17 | jc-slack-relay (10-05) | `jc-slack-relay.skill` | v1.1.0 |
| 18 | mice-estimate (10-02, v3.3.0) | `mice-estimate.skill` | v3.3.1 |
| 19 | (없음 — 신규) | `mice-meeting-minutes.skill` | v2.2.0 |

jc-design-system을 1번으로 올리면 나머지가 참조하는 토큰 정본이 먼저 자리를 잡는다. 삭제 → 업로드를 한 쌍씩 처리하면 같은 이름이 두 개 뜨는 상태를 피할 수 있다.

## 3. 끄기 1건 (삭제 아님)

- [ ] doc-coauthoring (Anthropic 기본 스킬) — 토글 OFF. jc-doc-coauthor와 'decision doc·RFC·spec'에서 동시 발동 방지.

## 4. 손대지 않는 것 (삭제 금지)

Anthropic 기본 스킬 10종: docs · docx · xlsx · pdf · pptx · skill-creator · web-artifacts-builder · learn · import-memory · setup-writing-style.

## 5. 끝난 뒤 확인 (약 10분 후)

`%USERPROFILE%\.claude\skills\synced\<bucket>\manifest.json` 에 §1의 19개 이름이 없고, §2의 19개가 새 버전으로 있으면 완료. 확인되면 Claude Code에 "업로드 완료"라고만 알려 주시면 deploy-pipeline.md의 "37종 업로드" 팩트를 현행으로 고친다.
