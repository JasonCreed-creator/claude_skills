#!/usr/bin/env python3
"""jc_tokens 로더 테스트 v2 (stdlib만).

실행: python .claude/skills/jc-design-system/scripts/test_jc_tokens.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jc_tokens import load_tokens, color, dark, asset, find_sot  # noqa: E402

SOT = Path(__file__).resolve().parents[1]  # jc-design-system 폴더


def run() -> int:
    tok = load_tokens(SOT)
    checks = [
        ("SoT 로드 성공", bool(tok)),
        ("brand == remember", tok.get("brand") == "remember"),
        ("accent == #EB6F2A", color(tok, "accent") == "#EB6F2A"),
        ("accentStrong == #B8431A", color(tok, "accentStrong") == "#B8431A"),
        ("bg == #FBFAF6", color(tok, "bg") == "#FBFAF6"),
        ("text == #1A1A1A", color(tok, "text") == "#1A1A1A"),
        ("border-strong == #CFC8BC", color(tok, "borderStrong") == "#CFC8BC"),
        ("point.steel == #476580", color(tok, "steel") == "#476580"),
        ("semantic.danger == #D93636", color(tok, "danger") == "#D93636"),
        ("dark.bg == #141210", dark(tok, "bg") == "#141210"),
        ("dark.accentText == #F08A4C", dark(tok, "accentText") == "#F08A4C"),
        ("data 6색, S1 오렌지", len(tok["color"]["data"]) == 6 and tok["color"]["data"][0] == "#EB6F2A"),
        ("scales.orange 5단계", len(tok["color"]["scales"]["orange"]) == 5),
        ("deckPt.headline == 32", tok["deckPt"]["headline"] == 32),
        ("gradient 문자열 보존", color(tok, "gradient").startswith("linear-gradient")),
        ("미지정 키 → fallback", color(tok, "no_such_key", "ABCDEF") == "#ABCDEF"),
        ("hash_prefix=False", color(tok, "accent", hash_prefix=False) == "EB6F2A"),
        ("로드 실패 시 {} → fallback", color(load_tokens("/nonexistent"), "accent", "EB6F2A") == "#EB6F2A"),
        ("find_sot 가 이 폴더를 찾음", find_sot() == SOT),
        ("로고 에셋 존재", (asset(tok, "logoLight", SOT) or Path("x")).is_file()),
        ("오브제 7점 존재", all((SOT / p).is_file() for p in tok["assets"]["objet"])),
    ]
    ok = True
    for name, passed in checks:
        print(f"  {'OK ' if passed else 'FAIL'} {name}")
        ok = ok and passed
    print("test_jc_tokens", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(run())
