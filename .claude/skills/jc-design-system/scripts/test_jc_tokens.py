#!/usr/bin/env python3
"""jc_tokens 로더 테스트 (stdlib만 — 어디서나 실행 가능).

실행: python3 .claude/skills/jc-design-system/scripts/test_jc_tokens.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jc_tokens import load_tokens, color  # noqa: E402

SOT = Path(__file__).resolve().parents[1]  # jc-design-system 폴더


def run() -> int:
    tok = load_tokens(SOT)
    checks = [
        ("SoT 로드 성공", bool(tok)),
        ("accent == #2962FF", color(tok, "accent") == "#2962FF"),
        ("primary == #0A2540", color(tok, "primary") == "#0A2540"),
        ("border-strong == #C9CFD8", color(tok, "borderStrong") == "#C9CFD8"),
        ("semantic.danger == #D32F2F", color(tok, "danger") == "#D32F2F"),
        ("point.orange == #FF5722", color(tok, "orange") == "#FF5722"),
        ("data 6색", len(tok.get("color", {}).get("data", [])) == 6),
        ("data-6 == #7C3AED", tok.get("color", {}).get("data", [None] * 6)[5] == "#7C3AED"),
        ("미지정 키 → fallback", color(tok, "no_such_key", "ABCDEF") == "#ABCDEF"),
        ("hash_prefix=False", color(tok, "accent", hash_prefix=False) == "2962FF"),
        ("로드 실패 시 {} → fallback", color(load_tokens("/nonexistent"), "accent", "0A2540") == "#0A2540"),
    ]
    ok = True
    for name, passed in checks:
        print(f"  {'OK ' if passed else 'FAIL'} {name}")
        ok = ok and passed
    print("test_jc_tokens", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(run())
