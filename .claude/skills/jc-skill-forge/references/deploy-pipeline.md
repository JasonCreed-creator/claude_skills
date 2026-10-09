# 배포 파이프라인 — 정본 레포 → claude.ai → Claude Code

검증일 2026-10-05 (Claude Code 공식 문서 + 이 PC 실측 + 2026-10-03 전수 점검) · 업로드 상태 2026-10-09 갱신.

---

## 0. 세 채널은 서로 다르다 — 소스 반영 ≠ 배포

| 채널 | 무엇 | 누가 | 반영 범위 |
|------|------|------|-----------|
| ① 소스 반영 | 정본 레포 `C:\.Claude\Code\claude_skills\.claude\skills\<name>\` 편집 + 린트 + `.skill` 빌드 | 스킬(forge) | 레포에만. **아직 아무 서피스에도 안 뜬다** |
| ② Code 로컬 설치 | `~/.claude/skills/<name>`(정션/복사) | 스킬, 승인 후 | 이 PC의 Claude Code만 |
| ③ claude.ai 업로드 | Settings > Capabilities(Skills)에서 `.skill` 업로드·구버전 삭제 | **기획자님(사용자)** | claude.ai 채팅 · Cowork · synced 동기화본 |

- 보고할 때는 스킬마다 ①②③ 상태를 따로 적는다. "수정 완료"를 "배포 완료"로 쓰지 않는다.
- ③은 CLI·API로 할 수 없다. forge는 업로드할 파일 경로와 화면 경로만 안내하고, 업로드했다고 가정하지 않는다.
- 버전 번호를 올리지 않고 내용을 고치면 ①과 ③이 같은 번호로 어긋난다(2026-09-21 jc-redteam·jc-doc-coauthor·jc-strategy-canvas 사례). 수정하면 반드시 범프.
- 반대로 claude.ai 업로드본에만 고친 내용이 있으면(2026-10-01 pt-script·jc-design-system 사례) 레포로 **수정만 골라** 이식한다. 파일째 덮지 않는다.

## 1. 동기화 사실 (바뀌면 여기부터 갱신)

| 사실 | 함의 |
|------|------|
| `~/.claude/skills/synced/<bucket>/`는 claude.ai에서 **약 10분마다 자동 갱신** | 그 폴더 편집은 덮어써짐. 읽기 전용 |
| `~/.claude/skills/<이름>/` 개인 스킬은 동명 synced보다 **우선** (`/이름` = 로컬, `/anthropic-skills:이름` = synced) | Code 즉시 반영은 여기에 설치. 단 목록에 둘 다 노출 |
| **Cowork는 claude.ai에 등록된 스킬만 로드** | claude.ai 업로드가 필수. `~/.claude/skills`는 Cowork에 안 보임 |
| claude.ai에 폐합 스킬이 남아 있으면 계속 발동한다 | 2026-10-09 기준 30종 = 자작 라이브 19종(교통정리 재업로드본) + Anthropic 프리셋 11종(doc-coauthoring은 OFF). 폐합 19종은 2026-10-09 삭제 완료. 폐합 스킬은 사용자가 삭제해야 사라진다 — 화면 조작은 Claude in Chrome 지시문으로 대행 가능(레포 `docs/claude-ai-sync-runbook-2026-10-09.md` §1), 업로드는 파일 선택창 때문에 수동 |
| 업로드 형식은 **ZIP(.skill) 하나** | 내부 구조 `<name>/SKILL.md`. **tar.gz·7z·폴더째 업로드 금지** — 받지 않거나 구조가 깨진다 |
| 업로드 프론트매터 허용 필드 제한 | `house-conventions.md §1` |
| `mice-estimate`는 사용자가 직접 업로드 관리 | 빌드·설치 대상에서 기본 제외(`--include-estimate`로만 포함) |

## 2. 편집 (① 소스 반영)

- 정본: `C:\.Claude\Code\claude_skills\.claude\skills\<name>\`. 브랜치는 사용자 방식(기본 `main` 또는 작업 브랜치).
- 변경 전 `_archive\<YYYYMMDD>\<name>\`(로컬 롤백 백업 — gitignore, 커밋 안 됨)에 원본 복사 후 바로 수정한다(되돌릴 수 있는 작업 — 단계별 확인 없음).
- 폐합(ARCHIVE)은 `_archive`가 아니라 git 보관소로: `git mv .claude/skills/<name> archive/skills/<name>` + `lint_skills.py` LIVE/ARCHIVED 갱신 + `archive/README.md` 후속 매핑 행 + `jc-design-system/references/chaining-protocol.md` §3 enum·§3-1 별칭·§7 ALIASES(같은 커밋, 커밋은 사용자).
- `version` 범프 + SKILL.md `## 변경 이력` 1항(3줄 이내).

## 3. 검증

```bash
cd /c/.Claude/Code/claude_skills
python .claude/skills/jc-skill-forge/scripts/lint_skills.py                      # 레포 전체
python .claude/skills/jc-skill-forge/scripts/lint_skills.py .claude/skills/jc-pptx  # 폴더 지정
python .claude/skills/jc-skill-forge/scripts/lint_skills.py --self-test
python scripts/check_drift.py                                                    # 디자인 값 드리프트(레포 루트)
python .claude/skills/jc-design-system/scripts/test_jc_tokens.py
python .claude/skills/jc-skill-forge/scripts/build_skills.py --self-test
python .claude/skills/jc-skill-forge/scripts/install_local.py --self-test
```

린트 검사 항목은 `lint_skills.py` 머리말(폐합·없는 스킬 참조, "N턴", 구 모델 ID, "리더", 구 시그니처 HEX, 깨진 상대경로 등). ERROR 0이 마감 조건.

## 4. 빌드 (여전히 ① — 배포 아님)

```bash
python .claude/skills/jc-skill-forge/scripts/build_skills.py            # dist/skills/<name>.skill 전부
python .claude/skills/jc-skill-forge/scripts/build_skills.py --only jc-pptx
python .claude/skills/jc-skill-forge/scripts/build_skills.py --src <스킬 모음 폴더> --out <출력 폴더>
```
- 산출은 ZIP `.skill`만. `__pycache__`·`.pyc`·`.DS_Store` 제외. `dist/`는 `.gitignore`.
- zip 명령이 없는 환경이어도 `build_skills.py`(python zipfile)로 같은 구조가 나온다. tar로 대체하지 않는다.
- 큰 자산(jc-design-system 오브제 약 4MB)은 포함. 업로드가 용량으로 실패하면 오브제를 별도 배포로 뺀다.

## 5. claude.ai 업로드 (③ — 기획자님이 직접)

forge는 아래 안내와 파일 경로만 낸다.
1. claude.ai → Settings → Capabilities(Skills) → 기존 동명 스킬 **삭제** → `dist\skills\<name>.skill` 업로드.
2. 폐합 스킬(`lint_skills.py` ARCHIVED 집합 = `archive/skills/`)도 같은 화면에서 삭제해야 synced 목록·Cowork에서 사라진다.
3. 약 10분 뒤 `~/.claude/skills/synced/…/manifest.json`에서 버전 반영을 확인. Cowork는 다음 세션부터.

## 6. Claude Code 로컬 설치 (② — 승인 후)

```bash
python .claude/skills/jc-skill-forge/scripts/install_local.py           # 라이브 스킬 전부 → ~/.claude/skills/<name> (정션)
python .claude/skills/jc-skill-forge/scripts/install_local.py --copy    # 정션 대신 복사
python .claude/skills/jc-skill-forge/scripts/install_local.py --uninstall
```
- 정션(`mklink /J`)이면 레포 편집이 즉시 반영된다. 복사면 재설치 필요.
- 2026-10-03 기준 Code 로컬 설치는 0종(synced만 있음). claude.ai 업로드가 끝나 synced가 최신이면 설치하지 않아도 된다.
- 잔존 정리(사용자): 사용자 PC에 구 `/skillupgrade` 커맨드(`.claude/commands/skillupgrade.md`·`~/.claude/commands/skillupgrade.md`)가 남아 있으면 삭제. 그 워크플로우는 forge 모드 A로 대체됐고 원본은 `archive/legacy/`에 보관.

## 7. 문서 갱신

- `README.md` 카탈로그(라이브 스킬 표) · `docs/CHANGELOG-<날짜>.md` · `PROGRESS.md`(세션 상태) · `docs/skill-intake-log.md`(모드 A 인테이크 판정의 단일 트래커).
- 사용자 메모리(`project-skill-library-reorg`·`ref-claude-skill-sync-rules`)와 어긋나면 갱신 제안.

## 8. 커밋 (사용자)

```bash
cd /c/.Claude/Code/claude_skills && git add -A && git commit -m "skills: <요약>" && git push
```
커밋 메시지 초안은 forge가 제시하고 실행은 사용자가 한다.
