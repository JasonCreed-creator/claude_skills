# code-conductor 설치·검증 지시서

> 실설치는 Code 세션(사용자 머신) 소관 — 챗 샌드박스 설치는 무효. **2머신 체제라면 머신별로 각각 설치**하고 PROGRESS.md에 설치 완료를 로그한다.
> 전제: WSL(또는 Linux 셸) + python3 + `~/.local/bin`이 PATH에 포함 *(가정 — 머신 환경이 다르면 경로만 치환)*. **Windows 네이티브(Git Bash) 설치는 §6 적응 3건을 함께 적용한다.**

## 0. 사전 실측 (신뢰하기 전에 확인)

- [ ] `claude --version` — 훅 prompt_id 필드는 가이드 주장 기준 v2.1.196+ (미만이면 턴 카운터 리셋 불가 → 게이트 보류)
- [ ] 모델 문자열 유효 확인 — `claude-opus-4-8` / `claude-haiku-4-5-20251001` (검증 2026-07-10. 라인업 변경 시 최신 계열 ID로 교체 — RULE-VERSION-FACTS)

## 1. 본체 배치

```bash
mkdir -p ~/.claude/fable/agents ~/.claude/fable/hooks
# 본 프리셋 파일 복사:
#   fable.md → ~/.claude/fable/fable.md
#   env.sh → ~/.claude/fable/env.sh
#   agents/*.md → ~/.claude/fable/agents/
#   hooks/orchestration-gate.py → ~/.claude/fable/hooks/ (chmod +x)
#   fable-toggle.sh → ~/.local/bin/fable (chmod +x)
echo '<!-- fable off -->' > ~/.claude/fable/empty.md
ln -sfn ~/.claude/fable/fable.md ~/.claude/fable/active.md
```

## 2. 로딩 코드 4종 (각 1회)

1. `~/.claude/CLAUDE.md` 맨 끝: `@/home/<사용자명>/.claude/fable/active.md`
2. 에이전트 심링크: `ln -sfn ~/.claude/fable/agents/{deep-reasoner,runner}.md ~/.claude/agents/`
3. `~/.bashrc` 맨 끝: `[ -f "$HOME/.claude/fable/env.sh" ] && . "$HOME/.claude/fable/env.sh"` *(③리매핑 생략 시 이 줄도 생략 가능)*
4. `~/.claude/settings.json` — **기존 파일에 hooks 키만 병합**(파일 통째 교체 금지 — 기존 설정·타 훅 보존. `hooks.PreToolUse` 배열이 이미 있으면 아래 matcher 블록을 항목으로 추가):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|NotebookEdit|MultiEdit|Bash",
        "hooks": [
          { "type": "command", "command": "/home/<사용자명>/.claude/fable/hooks/orchestration-gate.py" }
        ]
      }
    ]
  }
}
```

## 3. 활성화·상태 점검

```bash
fable on && fable status   # 로딩 코드 4종 [OK] 확인
```

- 적용은 **다음 claude 세션부터**(CLAUDE.md·훅은 세션 시작 시 로드). env.sh 래퍼만 실행 시점마다 상태를 읽는다.
- ③리매핑을 생략했다면 `fable status`의 'env 래퍼 [--]'는 **정상**(선택 계층 미설치)이다 — 실패로 오독하지 말 것.
- 지휘자 모델 자체는 스위치가 건드리지 않음 — Code 안에서 `/model`로 별도 설정.

## 4. 실측 검증 (필수 — 이 두 결과가 함께 나와야 완성)

```bash
# (a) 메인 차단 확인 — 3번째 코드 파일에서 차단, c3.ts 미생성이어야 정상
claude -p "c1.ts, c2.ts, c3.ts 세 파일을 순서대로 생성해라. 차단되면 BLOCKED: 뒤에 사유를 출력하고 멈춰라."
ls *.ts   # 기대: c1.ts c2.ts 만 존재

# (b) 서브에이전트 통과 확인 — 3개 전부 생성이어야 정상(위임 경로 무손상)
claude -p "서브에이전트를 띄워서 d1.ts, d2.ts, d3.ts 세 파일을 생성하게 해라."
ls d*.ts  # 기대: d1.ts d2.ts d3.ts

# 검증 후 테스트 파일 정리
rm -f c*.ts d*.ts
```

- (a)만 성공하고 (b)가 차단되면 **게이트가 위임 경로를 죽인 것** — 즉시 `fable off` 후 agent_id 분기 확인.
- 검증 결과를 PROGRESS.md에 1줄 기록: `날짜 | code-conductor 설치 | 머신명 | (a)차단OK/(b)통과OK`

## 5. 일상 조작

| 명령 | 동작 |
|------|------|
| `fable on` | 지침 로드 + 리매핑 + 게이트 활성(다음 세션부터) |
| `fable off` | 전부 비활성 — 로딩 코드는 유지, 심링크·상태만 전환 |
| `fable status` | 상태 + 로딩 코드 4종 설치 점검 |

## 6. Windows 네이티브 환경 적응 (실측 2026-07-10, Windows 11 + Git Bash)

WSL 없이 Windows 네이티브로 설치할 때 아래 3건을 적용한다. 미적용 시 게이트는 동작하나 안내·상태 표시가 어긋난다.

1. **훅 커맨드는 `python -X utf8` 형태로 명시** — §2-④의 command를 다음처럼 기재한다:

   ```json
   { "type": "command", "command": "python -X utf8 \"C:/Users/<사용자명>/.claude/fable/hooks/orchestration-gate.py\"" }
   ```

   `-X utf8`이 없으면 한국어 차단 메시지가 cp949로 인코딩돼 모델에게 깨져 보인다 — 차단 자체는 되지만 위임 안내가 실효를 잃는다.
2. **심링크(`ln -sfn`)는 Git Bash에서 파일 복사로 동작** — 기능은 동일하나 `fable status`의 agents 심링크 체크가 `[--]`로 나오는 것은 **정상**이다(실패로 오독하지 말 것). 대신 에이전트 원본(`~/.claude/fable/agents/`)을 갱신하면 `~/.claude/agents/`에 **재복사가 필요**하다(자동 반영 안 됨).
3. **claude CLI 버전이 데스크톱 앱 번들과 다를 수 있음** — §0의 `claude --version`이 요구 버전(2.1.196+) 미만이면 `claude update`로 해결 가능하다(실측: 2.1.123 → 2.1.206).

## 알려진 한계

- 게이트 Bash 우회 감지는 대표 경로(sed -i·perl -i·리다이렉트·tee)만 — 이론상 완전 차단 아님(지침과 겹으로 운용)
- 셸 래퍼를 거치지 않는 실행 경로(IDE 확장 등)에는 ③리매핑 미적용 — 그 세션에선 위임 시 model 명시
- 다른 플러그인의 PreToolUse 훅과 병행 가능(하나라도 차단하면 차단되는 구조)
