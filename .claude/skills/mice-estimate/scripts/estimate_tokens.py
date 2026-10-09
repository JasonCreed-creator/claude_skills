#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
estimate_tokens.py — mice-estimate 견적서(.xlsx)용 디자인 토큰 어댑터.

값을 미러하지 않고 jc-design-system v2(리멤버 웜 페이퍼) `references/signature-tokens.md §6 JSON`을
런타임 로드한다(하우스 규약). 탐색 순서:
  ① 형제 경로  <skills>/mice-estimate/scripts/ → parents[2]/jc-design-system
  ② ~/.claude/skills/jc-design-system
  ③ ~/.claude/skills/synced/*/jc-design-system
찾은 폴더의 scripts/jc_tokens.py 를 importlib 로 읽어 load_tokens/color 를 쓴다.
로드 실패 시에만 아래 _FALLBACK 상수(§6 v2.1.0 값)를 쓴다.

사용:
    from estimate_tokens import palette
    P = palette()          # {"ink": "1A1A1A", "accent": "EB6F2A", ...}  ('#' 없는 6자리 HEX)
    P["_source"]           # "sot:<경로>" 또는 "fallback"

역할 키 ↔ §6 키 (export_estimate_remember.ST 에서 쓰는 곳):
    ink          color.primary             title.fill · sec_amt.fill
    inkSoft      color.primarySoft         col_hdr.fill
    paper        color.surface             title/label_o/sec_amt/col_hdr 글자색
    surfaceAlt   color.surfaceAlt          label_g.fill
    surfaceSoft  color.surfaceSoft         sub.fill · sub_amt.fill
    accent       color.accent              label_o.fill · tot_val 글자색
    accentSoft   color.accentSoft          tot_kor/tot_val/tot_sub/tot_vat.fill
    accentStrong color.accentStrong        warn 글자색
    warningBg    color.semantic.warningBg  warn.fill
    amberTint    color.point.amberTint     sec_hdr.fill
    steel        color.point.steel         note_blue 글자색
    steelTint    color.point.steelTint     note_blue.fill
    danger       color.semantic.danger     footer 글자색

자가 테스트: python3 estimate_tokens.py --self-test  (SoT 경로·폴백 경로 모두 6자리 HEX 반환 확인)
"""
from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
from pathlib import Path

# 역할 → (§6 키 경로, 폴백 HEX).
# 폴백 출처: jc-design-system/references/signature-tokens.md §6 JSON (v2.1.0, 리멤버 웜 페이퍼).
# SoT 로드 실패 시에만 사용. 값을 바꾸려면 SoT를 고치고 여기서는 손대지 않는다.
ROLES: dict[str, tuple[str, str]] = {
    "ink":          ("color.primary",            "1A1A1A"),
    "inkSoft":      ("color.primarySoft",        "332F29"),
    "paper":        ("color.surface",            "FFFFFF"),
    "surfaceAlt":   ("color.surfaceAlt",         "F4F1EA"),
    "surfaceSoft":  ("color.surfaceSoft",        "EFEBE2"),
    "accent":       ("color.accent",             "EB6F2A"),
    "accentSoft":   ("color.accentSoft",         "FFF1E6"),
    "accentStrong": ("color.accentStrong",       "B8431A"),
    "warningBg":    ("color.semantic.warningBg", "FBF2DF"),
    "amberTint":    ("color.point.amberTint",    "FBF2DF"),
    "steel":        ("color.point.steel",        "476580"),
    "steelTint":    ("color.point.steelTint",    "E8EEF3"),
    "danger":       ("color.semantic.danger",    "D93636"),
}
_FALLBACK: dict[str, str] = {role: fb for role, (_key, fb) in ROLES.items()}
SOT_KEY: dict[str, str] = {role: key for role, (key, _fb) in ROLES.items()}

_HEX6 = re.compile(r"^[0-9A-Fa-f]{6}$")


def find_design_system(start: Path | None = None) -> Path | None:
    """하우스 규약 탐색 순서로 jc-design-system 폴더를 찾는다. 샌드박스 절대경로는 보지 않는다."""
    here = Path(start) if start else Path(__file__).resolve()
    cands: list[Path] = []
    if len(here.parents) >= 3:
        cands.append(here.parents[2] / "jc-design-system")
    home = Path.home()
    cands.append(home / ".claude" / "skills" / "jc-design-system")
    cands.extend(sorted(home.glob(".claude/skills/synced/*/jc-design-system")))
    for c in cands:
        if (c / "references" / "signature-tokens.md").is_file():
            return c
    return None


def _import_jc_tokens(sot: Path):
    mod_path = Path(sot) / "scripts" / "jc_tokens.py"
    if not mod_path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("jc_tokens", mod_path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _walk(tok: dict, dotted: str):
    """'color.point.amberTint' 같은 §6 키 경로를 토큰 dict에서 직접 꺼낸다. 없으면 None."""
    cur = tok
    for part in dotted.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur if isinstance(cur, str) else None


def _norm(val) -> str:
    return str(val).strip().lstrip("#").upper() if isinstance(val, str) else ""


def is_hex6(val) -> bool:
    return isinstance(val, str) and bool(_HEX6.match(val))


def palette(sot: Path | None = None) -> dict:
    """역할명 → '#' 없는 HEX 6자리. SoT 로드 실패 시 _FALLBACK (P['_source'] == 'fallback')."""
    out: dict = dict(_FALLBACK)
    out["_source"] = "fallback"
    try:
        sot = sot or find_design_system()
        if sot is None:
            return out
        jt = _import_jc_tokens(sot)
        if jt is None:
            return out
        tok = jt.load_tokens(sot)           # §6 JSON 파싱은 jc_tokens 정식 구현에 맡긴다
        if not tok:
            return out
        for role, (key, fb) in ROLES.items():
            # ① §6 키 경로 직접 조회(중첩 color.point.* / color.semantic.* 포함)
            val = _norm(_walk(tok, key))
            if not is_hex6(val):
                # ② jc_tokens.color(): color.<k> → color.point.<k> → color.semantic.<k> 순 조회
                val = _norm(jt.color(tok, key.split(".")[-1], "", hash_prefix=False))
            out[role] = val if is_hex6(val) else fb
        out["_source"] = f"sot:{sot}"
        out["_sot_dir"] = str(sot)
    except Exception:  # noqa: BLE001 — 어떤 실패도 폴백으로 흡수
        pass
    return out


def _check_palette(label: str, P: dict) -> list[str]:
    errs: list[str] = []
    for role in ROLES:
        v = P.get(role)
        if not is_hex6(v):
            errs.append(f"{label}: {role} = {v!r} (6자리 HEX 아님)")
    return errs


def _self_test() -> int:
    errs: list[str] = []
    # 경로 1 — 실제 탐색 (SoT가 있으면 sot:, 없으면 fallback)
    P1 = palette()
    print(f"[1] palette()        source = {P1['_source']}")
    errs += _check_palette("sot", P1)
    # 경로 2 — SoT 없는 빈 폴더를 넘겨 강제 폴백
    with tempfile.TemporaryDirectory(prefix="estimate-tokens-nosot-") as tmp:
        P2 = palette(Path(tmp))
    print(f"[2] palette(no-SoT)  source = {P2['_source']}")
    if P2["_source"] != "fallback":
        errs.append(f"fallback 경로가 'fallback'이 아님: {P2['_source']}")
    errs += _check_palette("fallback", P2)
    for role in ROLES:
        print(f"    {role:13} {SOT_KEY[role]:26} sot={P1[role]}  fallback={P2[role]}")
    if P1["_source"].startswith("sot:"):
        drift = [r for r in ROLES if P1[r] != P2[r]]
        if drift:
            print("    WARN 폴백 상수가 SoT 현재값과 다름(폴백 갱신 검토):", ", ".join(drift))
    for e in errs:
        print("    FAIL", e)
    print("estimate_tokens self-test", "FAIL" if errs else "PASS")
    return 1 if errs else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv[1:]:
        raise SystemExit(_self_test())
    P = palette()
    print("source :", P["_source"])
    print("accent :", P["accent"], "/ ink", P["ink"], "/ paper", P["paper"])
