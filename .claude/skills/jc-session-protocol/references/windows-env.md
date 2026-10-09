# 환경 메모 — 이 PC (Windows 11 Pro · Claude 데스크톱 앱 Code 세션)

검증일 2026-09-21. 항목마다 마지막 확인일을 적는다(RULE-VERSION-FACTS). 프로젝트별 추가 제약은 각 PROGRESS.md 환경 메모가 우선.

---

## 1. 런타임 · 도구

| 도구 | 상태 | 비고 |
|------|------|------|
| `python` / `python3` | 3.14.7 PATH 있음 (09-21) | python-pptx 1.0.2 · Pillow · openpyxl · lxml 설치됨. `python3` 대신 `python` 권장 |
| `node` | v24 PATH 있음 (09-21) | 9/11 시점 팀 보드 메모는 "없음"이었음 — 이후 설치됨. npm 확인은 프로젝트에서 |
| `perl` | 5.42 | 플레이북 시절 텍스트 도구(`_tools/*.pl`) |
| `git` | 2.55 | `gh` 없음. 시스템 `core.autocrlf=true` → 새 저장소는 `git init -b main` + 로컬 `core.autocrlf=false` |
| `zip` · `jq` · `soffice` | 없음 | zip은 `python -m zipfile` 또는 `zipfile` 모듈로. PPTX 렌더는 PowerPoint(설치됨) 수동 확인 |
| PowerPoint | `C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE` | Pretendard 1.3.9 사용자 폰트 설치됨(09-18). 타 PC 공유는 PDF |
| `claude.exe` | `%USERPROFILE%\.local\bin\claude.exe` — PATH 미등록 | 전체 경로로 실행. 데스크톱 앱 번들 CLI는 MSIX 가상화(`%LOCALAPPDATA%\Packages\Claude_…`) — Claude가 보는 경로가 사용자에겐 없을 수 있음 |

## 2. Bash 도구 함정

- 히어독은 약 10KB 넘으면 잘리고 `\\`가 `\`로 축약 → 큰 파일·백슬래시 포함 파일은 Write 도구.
- stdin을 읽는 명령(`cat > 파일` 입력 없음, `python -`)은 영원히 대기 → `< /dev/null` 또는 `printf`. 히어독(`<<'EOF'`)은 괜찮다.
- `cd`가 포함된 복합 명령은 작업 디렉터리를 바꿔 다음 호출에 영향 → 절대경로 사용.
- Git Bash가 `/design-login` 같은 슬래시 인자를 `C:/Program Files/Git/design-login`으로 변환 → 슬래시 명령은 REPL 안에서만.
- `node --test tests/` 디렉터리 인자는 경로 변환으로 실패 → 파일 나열.
- 한글 stdout은 `PYTHONIOENCODING=utf-8` 지정(cp949 인코딩 오류).

## 3. 브라우저 · UI 자동화

- 내장 브라우저 패널은 `file://` 거부 → PowerShell HttpListener 정적 서버(`serve.ps1`, 포트 8765) 또는 `python -m http.server`. 세션 종료 시 정지.
- 패널이 숨겨지면 스크린샷 공백·`innerWidth` 0 → `resize_window 1280x800` 후 캡처, 끝나면 desktop 프리셋으로 복귀.
- Chrome 확장(claude-in-chrome): 구글 시트·Apps Script 조작 레시피는 `mice-team-board/references/chrome-ext-recipes.md`. 요지: 코드 교체는 `<input type=file>` 주입 + `file_upload` + monaco `pushEditOperations`; 삭제·붙여넣기는 안 됨(사용자 몫); 셀 입력은 Name Box → F2 → ctrl+a → 타이핑; 저장 버튼은 큰 교체 후 60초 무시될 수 있음.
- OAuth 승인 클릭·hCaptcha는 자동화 차단 → 사용자가 직접(화면 잠금 시 페이지가 활성화되지 않음).
- 자동 모드 분류기가 `git remote add`·`git push`·시트 Delete 키를 거부할 수 있음 → settings `permissions.allow`에 규칙 추가하거나 사용자가 실행.

## 4. MCP · 연동

- Slack: `plugin:productivity:slack` 도구 27종(`mcp__plugin_productivity_slack__*`). 인증은 `/mcp`에서 productivity slack 재인증(커넥터 "다시 연결"의 기업 ID 오류는 경로 문제). 세션 재시작 불필요. 상세 `mice-slack-ops/references/channels.md`.
- Google Drive MCP: 읽기·생성·복사·권한조회만. 본문 수정·삭제·이동 없음. `create_file`은 `text/markdown`으로 올려야 중첩 불릿이 살아남음(text/html은 풀림). 읽기 도구는 4바이트 이모지를 깨진 문자로 보여주지만 문서는 정상. 개인 gmail 계정(icejc1015) 소유 → 회사 계정 이전은 사용자 몫.
- DesignSync(Claude Design): `~/.local/bin/claude.exe`에서 `/design-login` 1회. 비대화형 세션도 재사용. 프로젝트 `remember-proposal-ds` `.design-sync/NOTES.md` 참조.
- 회사 Google 계정은 커넥터 연결이 차단됨 → 개인 계정으로 작업 후 소유권 이전.

## 5. 클라우드 세션(GitHub)과의 분업

| | 로컬 PC | 클라우드 세션 |
|---|---|---|
| npm·Playwright·Chromium | 프로젝트별 확인 | 있음 — 게이트 전부 실행 가능 |
| 시트·Apps Script 쓰기 | Chrome 확장으로 가능 | 불가(읽기만) |
| 배포(clasp·회사 계정) | 사용자 | CI(`deploy.yml`) 또는 사용자 |

로컬 세션은 커밋 전 `git fetch`로 클라우드 세션의 PR 병합 여부를 확인한다.

## 6. 스킬 파일 위치

- claude.ai 동기화본 `~/.claude/skills/synced/<bucket>/` — 약 10분마다 덮어씀. 편집 금지.
- 정본 레포 `C:\.Claude\Code\claude_skills` — 편집은 여기서. 배포는 `jc-skill-forge/references/deploy-pipeline.md`.
- Code 전용 즉시 반영: `~/.claude/skills/<이름>` (동명 synced보다 우선).
