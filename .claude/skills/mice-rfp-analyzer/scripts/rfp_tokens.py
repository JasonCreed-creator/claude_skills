#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
rfp_tokens.py — mice-rfp-analyzer 산출물(.docx/.xlsx)용 디자인 토큰 어댑터.

값을 미러하지 않고 jc-design-system v2(리멤버 웜 페이퍼) `signature-tokens.md §6 JSON`을
런타임 로드한다(하우스 규약 §2). 탐색 순서:
  ① 형제 경로  <skills>/mice-rfp-analyzer/scripts/ → parents[2]/jc-design-system
  ② ~/.claude/skills/jc-design-system
  ③ ~/.claude/skills/synced/*/jc-design-system
찾은 폴더의 scripts/jc_tokens.py 를 import 해 load_tokens/color/dark 를 쓴다.
로드 실패 시에만 아래 _FALLBACK 상수를 쓴다.

사용:
    from rfp_tokens import palette, logo_path
    P = palette()          # {"ink": "1A1A1A", "accent": "EB6F2A", ...}  ('#' 없는 6자리)
    P["_source"]           # "sot:<경로>" 또는 "fallback"
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

# 폴백 상수 — 출처: jc-design-system/references/signature-tokens.md §6 (v2.0.0, 리멤버 웜 페이퍼).
# SoT 로드 실패 시에만 사용. 값을 바꾸려면 SoT를 고치고 여기서는 손대지 않는다.
_FALLBACK = {
    "bg": "FBFAF6", "surface": "FFFFFF", "surfaceAlt": "F4F1EA", "surfaceSoft": "EFEBE2",
    "border": "DCD6C8", "borderStrong": "CFC8BC",
    "text": "1A1A1A", "textSecondary": "4A463F", "textMuted": "6E6E6E", "textCaption": "8C867A",
    "accent": "EB6F2A", "accentStrong": "B8431A", "accentSoft": "FFF1E6",
    "steel": "476580", "steelTint": "E8EEF3",
    "success": "196B24", "successBg": "E7EFE8",
    "warning": "D39A1F", "warningBg": "FBF2DF",
    "danger": "D93636", "dangerBg": "FBE9E9",
    "darkPanel": "211E1A",
}


def find_design_system(start: Path | None = None) -> Path | None:
    """하우스 규약 §2 탐색 순서로 jc-design-system 폴더를 찾는다. /mnt·/sessions 경로는 보지 않는다."""
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
    mod_path = sot / "scripts" / "jc_tokens.py"
    if not mod_path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("jc_tokens", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def palette(sot: Path | None = None) -> dict:
    """역할명 → '#' 없는 HEX 6자리. SoT 로드 실패 시 _FALLBACK."""
    out = dict(_FALLBACK)
    out["_source"] = "fallback"
    try:
        sot = sot or find_design_system()
        if sot is None:
            return out
        jt = _import_jc_tokens(sot)
        if jt is None:
            return out
        tok = jt.load_tokens(sot)
        if not tok:
            return out
        for key, fb in _FALLBACK.items():
            if key == "darkPanel":
                out[key] = jt.dark(tok, "panel", fb, hash_prefix=False).upper()
            else:
                out[key] = jt.color(tok, key, fb, hash_prefix=False).upper()
        out["_source"] = f"sot:{sot}"
        out["_sot_dir"] = str(sot)
    except Exception:
        pass
    return out


def logo_path(P: dict | None = None) -> Path | None:
    """라이트 배경용 리멤버 로고(assets/remember-black.png). 없으면 None → 로고 슬롯은 텍스트로 대체."""
    try:
        sot = Path(P["_sot_dir"]) if P and P.get("_sot_dir") else find_design_system()
        if sot is None:
            return None
        p = sot / "assets" / "remember-black.png"
        return p if p.is_file() else None
    except Exception:
        return None


ISSUER = "리멤버 MICE비즈팀"  # 발행 명의 기본(RULE-NO-COMPANY v2). 발주처는 입력 데이터로 주입.


if __name__ == "__main__":
    P = palette()
    print("source :", P["_source"])
    print("accent :", P["accent"], "/ ink", P["text"], "/ bg", P["bg"])
    print("logo   :", logo_path(P))
