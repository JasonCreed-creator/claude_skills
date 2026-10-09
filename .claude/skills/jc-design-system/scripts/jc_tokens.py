#!/usr/bin/env python3
"""
jc-design-system 토큰 로더 (SoT 런타임 로딩의 정식 구현). v2 — 리멤버 웜 페이퍼.

소비 스킬이 디자인 토큰값을 하드코딩(미러)하지 않고, 실행 시
`references/signature-tokens.md §6 JSON`을 단일 진실 공급원(SoT)으로 읽도록 한다.
stdlib만 사용(json·re·pathlib) — 어떤 환경에서도 의존성 없이 동작.

사용:
    from jc_tokens import load_tokens, color, dark, find_sot
    tok = load_tokens(find_sot())
    accent = color(tok, "accent")                 # "#EB6F2A"
    hexno  = color(tok, "accent", hash_prefix=False)  # "EB6F2A" (python-pptx/openpyxl)
    bg     = dark(tok, "bg")                      # "#141210"
    series = tok["color"]["data"]                 # 시리즈 6색

견고성: SoT 파일을 못 찾거나 파싱 실패 시 예외 대신 빈 dict({}) 반환 →
호출부는 `color(tok, key, fallback=...)`로 안전하게 폴백한다.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

_JSON_FENCE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


def find_sot(start: Path | None = None) -> Path | None:
    """jc-design-system 폴더 탐색: 형제 경로 → ~/.claude/skills → synced. 없으면 None."""
    here = Path(start) if start else Path(__file__).resolve()
    cands = []
    # 이 파일이 jc-design-system/scripts/ 안에 있으면 그 자체
    if here.parent.name == "scripts" and here.parents[1].name == "jc-design-system":
        cands.append(here.parents[1])
    # 소비 스킬의 scripts/ 에서 호출된 경우: <skills>/<skill>/scripts/x.py → <skills>/jc-design-system
    if len(here.parents) >= 3:
        cands.append(here.parents[2] / "jc-design-system")
    home = Path.home()
    cands.append(home / ".claude" / "skills" / "jc-design-system")
    cands.extend(sorted(home.glob(".claude/skills/synced/*/jc-design-system")))
    for c in cands:
        if (c / "references" / "signature-tokens.md").is_file():
            return c
    return None


def _find_signature_md(sot_dir: Path | None) -> Path | None:
    candidates = []
    if sot_dir is not None:
        sot_dir = Path(sot_dir)
        candidates += [sot_dir / "references" / "signature-tokens.md",
                       sot_dir / "signature-tokens.md"]
    else:
        found = find_sot()
        if found:
            candidates.append(found / "references" / "signature-tokens.md")
    for c in candidates:
        if c.is_file():
            return c
    return None


def load_tokens(sot_dir: Path | str | None = None) -> dict:
    """SoT signature-tokens.md §6 JSON 을 파싱해 토큰 dict 반환. 실패 시 {}."""
    try:
        md_path = _find_signature_md(Path(sot_dir) if sot_dir is not None else None)
        if md_path is None:
            return {}
        m = _JSON_FENCE.search(md_path.read_text(encoding="utf-8"))
        if not m:
            return {}
        return json.loads(m.group(1))
    except Exception:
        return {}


def _norm(val: str, hash_prefix: bool) -> str:
    if not val:
        return val
    if val.startswith("linear-gradient") or val.startswith("rgba"):
        return val
    val = val.lstrip("#")
    return ("#" + val) if hash_prefix else val


def color(tokens: dict, key: str, fallback: str = "", *, hash_prefix: bool = True) -> str:
    """color.<key> → color.point.<key> → color.semantic.<key> 순 조회. 없으면 fallback."""
    c = (tokens or {}).get("color", {})
    val = c.get(key)
    if val is None:
        val = c.get("point", {}).get(key)
    if val is None:
        val = c.get("semantic", {}).get(key)
    if val is None or isinstance(val, (list, dict)):
        val = fallback
    return _norm(val, hash_prefix)


def dark(tokens: dict, key: str, fallback: str = "", *, hash_prefix: bool = True) -> str:
    """color.dark.<key> 조회. 없으면 fallback."""
    val = (tokens or {}).get("color", {}).get("dark", {}).get(key)
    if val is None:
        val = fallback
    return _norm(val, hash_prefix)


def asset(tokens: dict, key: str, sot_dir: Path | str | None = None) -> Path | None:
    """assets.<key> 경로를 SoT 폴더 기준 절대경로로 반환 (logoLight/logoDark)."""
    rel = (tokens or {}).get("assets", {}).get(key)
    if not rel or isinstance(rel, list):
        return None
    base = Path(sot_dir) if sot_dir else find_sot()
    return (base / rel) if base else None


if __name__ == "__main__":  # 간이 데모/점검
    sot = find_sot()
    tok = load_tokens(sot)
    if not tok:
        print("SoT 로드 실패 — signature-tokens.md 를 찾을 수 없음")
    else:
        print("sot     :", sot)
        print("brand   :", tok.get("brand"), tok.get("version"))
        print("accent  :", color(tok, "accent"), "/ deep", color(tok, "accentStrong"))
        print("bg/ink  :", color(tok, "bg"), color(tok, "text"))
        print("dark bg :", dark(tok, "bg"), "/ panel", dark(tok, "panel"))
        print("data    :", tok["color"]["data"])
        print("logo    :", asset(tok, "logoLight", sot))
