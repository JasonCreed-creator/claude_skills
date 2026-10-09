# claude.ai 스킬 동기화 런북 — 삭제·끄기(확장프로그램) + 업로드(수동)

작성 2026-10-09. 대상: 리포트 `docs/stocktake-2026-10-09.md` §6 카드 **A**(폐합 19종 삭제) · **D**(프리셋 doc-coauthoring 끄기) · **B**(라이브 19종 업로드).

세 채널 중 **③ claude.ai 업로드본**만 다룬다(①git 정본은 PR #23에 반영 완료, ②Code 로컬 설치는 하지 않음 — 리포트 §6 카드 G).

| 작업 | 수단 | 되돌리기 |
|---|---|---|
| 1. 폐합 19종 삭제 | Claude in Chrome(확장프로그램) — 아래 지시문 붙여넣기 | 불가(필요 시 `archive/skills/`에서 `.skill` 재빌드 후 재업로드) |
| 2. 프리셋 `doc-coauthoring` 끄기 | 같은 지시문 안에 포함 | 토글 다시 켜면 됨 |
| 3. 라이브 19종 업로드 | **기획자님 수동**(확장프로그램은 파일 선택창을 못 다룸) | 구버전 삭제 후 재업로드 |
| 4. 반영 확인 | PC에서 manifest.json 확인 | — |

## 0. 시작 전 확인 3가지

1. 브라우저(Chrome)에 **Claude in Chrome** 확장프로그램이 설치·로그인돼 있고, claude.ai 회사 계정(리멤버)으로 로그인된 상태인지.
2. 열려 있는 claude.ai 탭에서 **Settings → Capabilities**(설정 → 기능)로 들어가면 **Skills** 목록이 보이는지. 안 보이면 조직 관리자 권한 문제이므로 중단.
3. 아래 "삭제 금지" 목록을 한 번 읽는다 — 확장프로그램이 실수해도 기획자님이 확인창에서 막을 수 있다.

**삭제 금지(절대)**: `mice-estimate` · 라이브 18종(jc-design-system jc-skill-forge jc-session-protocol jc-redteam jc-pptx jc-kv-guide jc-doc-coauthor pt-script mice-rfp-analyzer jc-strategy-canvas mice-market-intel mice-meeting-minutes mice-run-of-show mice-aftermath mice-slack-ops mice-ops-docs mice-team-board jc-slack-relay) · Anthropic 프리셋 전부(docs docx xlsx pdf pptx skill-creator web-artifacts-builder learn import-memory setup-writing-style doc-coauthoring — doc-coauthoring은 **끄기만**).

## 1. 확장프로그램 지시문 (그대로 붙여넣기)

Claude in Chrome 사이드 패널을 열고 아래 블록 전체를 붙여넣는다. 실행 중 삭제 확인창이 뜨면 **이름이 목록에 있는지 보고** 확인을 누른다.

```
지금 열린 claude.ai 탭에서 아래 작업만 정확히 수행해줘. 목록 밖의 어떤 스킬도 삭제·수정·끄지 마.

[작업 1] Settings → Capabilities 화면의 Skills 목록에서 다음 19개를 하나씩 삭제(Delete/Remove). 이름이 정확히 일치하는 것만:
jc-artifact-builder, jc-asana-html, jc-brand-discovery, jc-brand-styling, jc-cinematic-html, jc-comms, jc-generative-art, jc-landing-page, jc-mcp-builder, jc-orchestrator, jc-prompt-builder, jc-remember-html, jc-skill-creator, jc-theme-factory, jc-visual-philosophy, jc-workspace-ops, mice-dashboard, mice-proposal, mice-weekly-performance

[작업 2] 같은 화면에서 Anthropic 기본 스킬 doc-coauthoring 의 토글을 끈다(비활성화). 삭제가 아니라 끄기. 다른 기본 스킬(docs, docx, xlsx, pdf, pptx, skill-creator, web-artifacts-builder, learn, import-memory, setup-writing-style)은 손대지 않는다.

[규칙]
- 시작 전에 현재 Skills 목록 전체(이름·버전·켜짐 여부)를 그대로 적어서 먼저 보고하고, 그다음 작업을 시작해.
- mice-estimate 와 다음 18개는 절대 삭제·끄기 금지: jc-design-system, jc-skill-forge, jc-session-protocol, jc-redteam, jc-pptx, jc-kv-guide, jc-doc-coauthor, pt-script, mice-rfp-analyzer, jc-strategy-canvas, mice-market-intel, mice-meeting-minutes, mice-run-of-show, mice-aftermath, mice-slack-ops, mice-ops-docs, mice-team-board, jc-slack-relay
- 이름이 비슷해도(예: jc-doc-coauthor 와 doc-coauthoring, mice-ops-docs 와 mice-dashboard) 목록과 글자 단위로 같을 때만 처리해.
- 목록의 이름이 화면에 없으면 건너뛰고 "없음"으로 보고해. 새로 업로드하거나 파일을 올리는 작업은 하지 마.
- 삭제 확인창이 뜨면 창에 적힌 이름이 [작업 1] 목록에 있을 때만 확인을 눌러.
- 끝나면 결과를 표로 보고해: 이름 | 처리(삭제됨 / 없음 / 꺼짐) | 비고. 마지막에 남아 있는 Skills 목록 전체를 다시 적어줘.
```

예상 결과: 삭제 19 · 꺼짐 1 · 남는 목록 = 라이브 18종(구버전) + mice-estimate + Anthropic 프리셋.

## 2. 업로드 (수동, 10분)

파일: 이 세션이 첨부한 `jc-skills-live19-2026-10-09.zip`을 PC에 풀면 `.skill` 19개가 나온다(mice-estimate v3.3.1 포함).

1. 같은 Settings → Capabilities → Skills 화면에서 **동명 구스킬을 먼저 삭제**한다(예: jc-pptx v2.1.x 삭제 → 새 jc-pptx.skill 업로드). 같은 이름이 두 개 뜨는 상태를 만들지 않는다.
2. "Upload skill"(스킬 업로드) 버튼 → 풀어 둔 폴더에서 `.skill` 파일 하나 선택 → 업로드. 19개를 반복한다. 순서는 상관없지만 **jc-design-system을 먼저** 올리면 나머지가 참조할 토큰 정본이 먼저 자리를 잡는다.
3. `mice-meeting-minutes`는 현재 claude.ai에 없는 **신규**라 삭제 단계 없이 바로 업로드한다.
4. `mice-estimate`는 v3.3.0(현재) 삭제 → `mice-estimate.skill`(v3.3.1) 업로드.
5. 업로드 형식은 `.skill`(ZIP)만 받는다. 폴더째·tar.gz는 올리지 않는다.

## 3. 반영 확인 (업로드 약 10분 후)

PC에서 파일 탐색기 주소창에 `%USERPROFILE%\.claude\skills\synced` 를 입력해 들어가면 긴 영문 ID 폴더가 하나 있다. 그 안의 `manifest.json`을 메모장으로 열어:

- 폐합 19종 이름이 **없고**, 라이브 19종이 **있으며**, 버전이 아래와 같은지 본다.

| 스킬 | 기대 버전 |
|---|---|
| jc-design-system | v2.2.0 |
| jc-skill-forge | v2.2.0 |
| jc-session-protocol | v1.2.0 |
| jc-redteam | v1.4.0 |
| jc-pptx | v2.3.0 |
| jc-kv-guide | v1.2.0 |
| jc-doc-coauthor | v1.2.0 |
| pt-script | v2.3.0 |
| mice-rfp-analyzer | v2.2.0 |
| jc-strategy-canvas | v1.2.0 |
| mice-market-intel | v1.2.0 |
| mice-meeting-minutes | v2.2.0 |
| mice-run-of-show | v1.2.0 |
| mice-aftermath | v1.2.0 |
| mice-slack-ops | v1.3.0 |
| mice-estimate | v3.3.1 |
| mice-ops-docs | v1.2.0 |
| mice-team-board | v1.1.0 |
| jc-slack-relay | v1.1.0 |

- 꺼둔 `doc-coauthoring`이 manifest에 남아 있어도 무방하다(끄기는 발동 차단이 목적). 만약 삭제한 19종이 10분 뒤에도 manifest에 남아 있으면 claude.ai 화면에서 삭제가 실제로 됐는지 다시 본다.

확인이 끝나면 Claude Code에 "업로드 완료"라고만 알려 주시면 `jc-skill-forge/references/deploy-pipeline.md §1`의 "37종 업로드" 팩트를 현행(라이브 19 + 프리셋)으로 고친다.

## 4. 왜 확장프로그램으로 업로드를 못 하나

Claude in Chrome은 웹 페이지 안의 버튼·토글·텍스트는 조작하지만, 운영체제의 **파일 선택창**(업로드 대화상자)은 브라우저 밖이라 다루지 못한다. 삭제·끄기는 전부 페이지 안의 조작이라 가능하다.
