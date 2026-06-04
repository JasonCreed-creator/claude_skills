#!/usr/bin/env python3
"""
신규 클라이언트 오버레이 검증기 (jc-theme-factory).

3토큰(primary/accent/logo) 오버레이 후보가 jc 가드레일을 지키는지 자동 점검한다:
  1) WCAG 대비비        (RULE-WCAG / mode-mapping.md §9.1 공식)
  2) 색충돌 회피         (client-overlays.md §6 — Deep Navy 채도 근접·Point Pool ΔE<5)
  3) 인쇄 형광/네온 점검  (§6 — 인쇄 시 채도 -20% 권고)
  4) 다크 모드 가독성     (mode-mapping.md §3 — 밝힌 accent가 다크 배경에서 충분한지)

토큰 값은 jc-design-system(SoT)을 런타임 로드하고, 실패 시 시그니처 상수로 폴백한다.
색 수학(hex/rgb/luminance/contrast/hsl/hsv/lab/ΔE)은 build_showcase.py가 재사용한다.

사용:
    python3 validate_overlay.py --accent "#7C3AED"
    python3 validate_overlay.py --primary "#101820" --accent "#E91E63" --print
    python3 validate_overlay.py --accent "#00E676" --json
종료코드: WCAG 하드 실패 시 1(Critical=차단), 그 외 0(경고는 통과).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

# ── SoT 토큰 로드 (실패 시 시그니처 폴백) ────────────────────────────────
_SOT = Path(__file__).resolve().parents[2] / "jc-design-system"
_FALLBACK = {  # 정본: signature-tokens.md §1 / §6. 폴백용 미러(주석으로 출처 명시).
    "primary": "#0A2540", "accent": "#2962FF",
    "orange": "#FF5722", "magenta": "#E91E63", "neon": "#00E676", "blue": "#2962FF",
}


def load_signature() -> dict:
    try:
        sys.path.insert(0, str(_SOT / "scripts"))
        from jc_tokens import load_tokens, color  # type: ignore
        tok = load_tokens(_SOT)
        if tok:
            return {k: color(tok, k, _FALLBACK[k]) for k in _FALLBACK}
    except Exception:
        pass
    return dict(_FALLBACK)


# ── 색 수학 ──────────────────────────────────────────────────────────────
def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"잘못된 hex: {h!r}")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(rgb: tuple[float, float, float]) -> str:
    return "#" + "".join(f"{max(0, min(255, round(c))):02X}" for c in rgb)


def _lin(ch: float) -> float:
    c = ch / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def rel_luminance(h: str) -> float:
    r, g, b = hex_to_rgb(h)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(h1: str, h2: str) -> float:
    l1, l2 = rel_luminance(h1), rel_luminance(h2)
    lo, hi = sorted((l1, l2))
    return (hi + 0.05) / (lo + 0.05)


def rgb_to_hsv(h: str) -> tuple[float, float, float]:
    r, g, b = (c / 255.0 for c in hex_to_rgb(h))
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d == 0:
        hue = 0.0
    elif mx == r:
        hue = ((g - b) / d) % 6
    elif mx == g:
        hue = (b - r) / d + 2
    else:
        hue = (r - g) / d + 4
    return hue * 60.0, (0.0 if mx == 0 else d / mx), mx


def saturation_hsl(h: str) -> float:
    r, g, b = (c / 255.0 for c in hex_to_rgb(h))
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    d = mx - mn
    if d == 0:
        return 0.0
    return d / (1 - abs(2 * l - 1)) if l not in (0, 1) else 0.0


def _to_lab(h: str) -> tuple[float, float, float]:
    r, g, b = (_lin(c) for c in hex_to_rgb(h))
    x = 0.4124 * r + 0.3576 * g + 0.1805 * b
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = 0.0193 * r + 0.1192 * g + 0.9505 * b
    xn, yn, zn = 0.95047, 1.0, 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x / xn), f(y / yn), f(z / zn)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e76(h1: str, h2: str) -> float:
    l1, a1, b1 = _to_lab(h1)
    l2, a2, b2 = _to_lab(h2)
    return math.sqrt((l1 - l2) ** 2 + (a1 - a2) ** 2 + (b1 - b2) ** 2)


def lighten(h: str, amount: float = 0.16) -> str:
    """다크 모드 accent 근사 — HSL 명도를 amount만큼 올린다(정본 근사: mode-mapping §3·§3.1)."""
    r, g, b = (c / 255.0 for c in hex_to_rgb(h))
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    nl = min(1.0, l + amount)
    if mx == mn:
        v = nl * 255
        return rgb_to_hex((v, v, v))
    scale = (nl - l) / (1 - l) if nl > l and l < 1 else 0
    return rgb_to_hex(tuple(255 * (c + (1 - c) * scale) for c in (r, g, b)))


# ── 검증 ────────────────────────────────────────────────────────────────
def validate(primary: str, accent: str, check_print: bool = False) -> dict:
    sig = load_signature()
    findings: list[dict] = []

    def add(sev: str, rule: str, msg: str):
        findings.append({"severity": sev, "rule": rule, "message": msg})

    # 1) WCAG — 헤더 풀블리드에 흰 텍스트가 얹힘
    c_prim = contrast("#FFFFFF", primary)
    if c_prim < 4.5:
        add("Critical", "RULE-WCAG", f"흰 텍스트 on primary 대비 {c_prim:.2f}:1 < 4.5:1 (본문 실패). primary를 더 어둡게.")
    c_acc = contrast("#FFFFFF", accent)
    if c_acc < 3.0:
        add("Critical", "RULE-WCAG", f"흰 텍스트 on accent 대비 {c_acc:.2f}:1 < 3.0:1 (큰 텍스트도 실패). accent를 더 어둡게.")
    elif c_acc < 4.5:
        add("Minor", "RULE-WCAG", f"흰 텍스트 on accent 대비 {c_acc:.2f}:1 — 버튼/큰 텍스트는 OK, 본문 라벨엔 부적합.")

    # 2) 색충돌 — primary가 Deep Navy와 근접
    ds = abs(saturation_hsl(primary) - saturation_hsl(sig["primary"]))
    de_prim = delta_e76(primary, sig["primary"])
    if de_prim < 8 or ds < 0.30 * 1.0 and de_prim < 20:
        if primary.upper() != sig["primary"].upper():
            add("Minor", "overlay§6", f"primary가 시그니처 Deep Navy와 근접(ΔE {de_prim:.1f}). 차이가 미미하면 primary=null(시그니처 유지) 권고.")

    # 2) 색충돌 — accent가 Point Pool과 근접 → 통합 권고
    pool = {"orange": sig["orange"], "magenta": sig["magenta"], "neon": sig["neon"], "blue": sig["blue"]}
    nearest = min(pool, key=lambda k: delta_e76(accent, pool[k]))
    de_acc = delta_e76(accent, pool[nearest])
    if de_acc < 5 and accent.upper() != pool[nearest].upper():
        add("Major", "overlay§6", f"accent가 Point Pool '{nearest}'({pool[nearest]})와 ΔE {de_acc:.1f}<5. 그 포인트 색으로 통합 권고(가족 일관성).")
    elif de_acc >= 5 and accent.upper() not in {v.upper() for v in pool.values()} and accent.upper() != sig["accent"].upper():
        add("Minor", "overlay§6", f"accent가 Point Pool 밖(가장 가까운 '{nearest}' ΔE {de_acc:.1f}). CI 확정색이 아니면 풀 색 사용 권장.")

    # 3) 인쇄 형광/네온
    if check_print:
        _, s, v = rgb_to_hsv(accent)
        if s > 0.85 and v > 0.85:
            add("Minor", "overlay§6", f"accent 고채도(S {s:.2f}·V {v:.2f}) — 형광/네온 가능. 인쇄용은 채도 -20% 권고(네온그린은 폴백 #00C853).")

    # 4) 다크 모드 가독성 — 밝힌 accent가 다크 배경에서 충분한지
    dark_accent = lighten(accent, 0.16)
    c_dark = contrast(dark_accent, "#0A1220")  # 다크 bg 정본: mode-mapping §3
    if c_dark < 3.0:
        add("Minor", "mode-mapping§3", f"다크 보정 accent({dark_accent}) on 다크배경 대비 {c_dark:.2f}:1 < 3.0 — 다크에서 더 밝게 보정 필요.")

    has_critical = any(f["severity"] == "Critical" for f in findings)
    return {
        "input": {"primary": primary, "accent": accent},
        "computed": {
            "white_on_primary": round(c_prim, 2),
            "white_on_accent": round(c_acc, 2),
            "nearest_point": nearest, "delta_e_to_nearest": round(de_acc, 1),
            "dark_accent": dark_accent, "dark_accent_on_dark_bg": round(c_dark, 2),
        },
        "findings": findings,
        "passed": not has_critical,
    }


def _report(res: dict) -> str:
    sev_icon = {"Critical": "🛑", "Major": "🟠", "Minor": "🟡"}
    lines = [
        "── jc 오버레이 검증 ──",
        f"  primary {res['input']['primary']}  ·  accent {res['input']['accent']}",
        f"  흰 텍스트 대비: on primary {res['computed']['white_on_primary']}:1 · on accent {res['computed']['white_on_accent']}:1",
        f"  가장 가까운 Point: {res['computed']['nearest_point']} (ΔE {res['computed']['delta_e_to_nearest']})",
        f"  다크 보정 accent: {res['computed']['dark_accent']} (다크배경 {res['computed']['dark_accent_on_dark_bg']}:1)",
        "",
    ]
    if not res["findings"]:
        lines.append("  ✅ 지적 없음 — 가드레일 통과.")
    else:
        for f in res["findings"]:
            lines.append(f"  {sev_icon.get(f['severity'],'•')} [{f['severity']}/{f['rule']}] {f['message']}")
    lines.append("")
    lines.append("  판정: " + ("✅ 통과(발행 가능)" if res["passed"] else "🛑 차단(Critical 해소 필요)"))
    return "\n".join(lines)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="신규 클라이언트 오버레이 검증 (3토큰·WCAG·색충돌)")
    p.add_argument("--primary", default=None, help="헤더/표지 색 (생략 시 시그니처 Deep Navy)")
    p.add_argument("--accent", default=None, help="강조/CTA 색 (생략 시 시그니처 Electric Blue)")
    p.add_argument("--print", dest="check_print", action="store_true", help="인쇄 형광/네온 점검 포함")
    p.add_argument("--json", action="store_true", help="JSON 출력")
    a = p.parse_args(argv)

    sig = load_signature()
    primary = a.primary or sig["primary"]
    accent = a.accent or sig["accent"]
    try:
        res = validate(primary, accent, a.check_print)
    except ValueError as e:
        print(f"입력 오류: {e}", file=sys.stderr)
        return 2

    print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else _report(res))
    return 0 if res["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
