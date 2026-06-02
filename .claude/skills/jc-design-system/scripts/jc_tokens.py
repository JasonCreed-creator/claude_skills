#!/usr/bin/env python3
"""
jc-design-system 토큰 로더 (SoT 런타임 로딩의 정식 구현).

consumer 스킬이 디자인 토큰값을 하드코딩(미러)하지 않고, 실행 시
`signature-tokens.md §6 JSON`을 단일 진실 공급원(SoT)으로 읽도록 한다.
stdlib만 사용(json·re·pathlib) — 어떤 환경에서도 의존성 없이 동작.

사용:
    from jc_tokens import load_tokens, color
    tok = load_tokens(sot_dir)                 # sot_dir = jc-design-system 폴더
    accent = color(tok, "accent")              # "#2962FF"
    data   = tok["color"]["data"]              # 6색 리스트

consumer 스크립트는 보통 형제 경로로 SoT를 찾는다:
    sot = Path(__file__).resolve().parents[2] / "jc-design-system"

견고성: SoT 파일을 못 찾거나 파싱 실패 시 예외 대신 빈 dict({}) 반환 →
호출부는 `color(tok, key, fallback=...)`로 안전하게 폴백한다.
(클라이언트 오버레이 적용은 client-overlays.md 포맷 확정 후 확장 예정.)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

_JSON_FENCE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


def _find_signature_md(sot_dir: Path | None) -> Path | None:
    """signature-tokens.md 경로 탐색. sot_dir 미지정 시 이 파일 기준 자동 추정."""
    candidates = []
    if sot_dir is not None:
        sot_dir = Path(sot_dir)
        candidates += [sot_dir / "references" / "signature-tokens.md",
                       sot_dir / "signature-tokens.md"]
    else:
        here = Path(__file__).resolve()
        # 이 파일이 jc-design-system/scripts/ 에 있다고 가정
        candidates += [here.parents[1] / "references" / "signature-tokens.md"]
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


def color(tokens: dict, key: str, fallback: str = "", *, hash_prefix: bool = True) -> str:
    """color.<key> 또는 color.point.<key>/color.semantic.<key> 조회. 없으면 fallback.

    fallback 은 '#' 유무 무관하게 받아 hash_prefix 설정에 맞춰 정규화한다.
    """
    c = (tokens or {}).get("color", {})
    val = c.get(key)
    if val is None:
        val = c.get("point", {}).get(key)
    if val is None:
        val = c.get("semantic", {}).get(key)
    if val is None:
        val = fallback
    if not val:
        return val
    val = val.lstrip("#")
    return ("#" + val) if hash_prefix else val


if __name__ == "__main__":  # 간이 데모/점검
    tok = load_tokens()
    if not tok:
        print("SoT 로드 실패 — signature-tokens.md 를 찾을 수 없음")
    else:
        print("accent  :", color(tok, "accent"))
        print("primary :", color(tok, "primary"))
        print("danger  :", color(tok, "danger"))
        print("data    :", tok["color"]["data"])
