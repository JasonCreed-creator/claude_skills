# env.sh → ~/.claude/fable/env.sh — 스위치 로더 (.bashrc에서 source 됨)
# 스위치가 on이면 claude 실행 시 sonnet 등급 서브에이전트를 상위 계열로 리매핑한다.
# ③계층은 선택 사항 — 비용 우선이면 이 파일 설치를 생략한다(나머지 계층은 독립 작동).
# 리매핑 대상 모델 ID(claude-opus-4-8)는 공식 제품 정보 대조 검증(2026-07-10). 단, 이 환경변수의
# 리매핑 동작 자체는 미검증 — INSTALL.md §0·§4 실측 후 신뢰할 것 (RULE-VERSION-FACTS)

_fable_on() { [ "$(cat "$HOME/.claude/.fable-state" 2>/dev/null)" = "on" ]; }

_fable_run() {
  if _fable_on; then
    ANTHROPIC_DEFAULT_SONNET_MODEL="claude-opus-4-8" "$@"
  else
    "$@"
  fi
}

claude() { _fable_run command claude "$@"; }
