#!/usr/bin/env python3
"""
오버레이 쇼케이스 생성기 (jc-theme-factory) — 원본 theme-showcase.pdf 대응.

jc-design-system(SoT)의 시그니처 토큰 + client-overlays.md의 등록 오버레이를 읽어,
각 오버레이를 라이트/다크 카드로 렌더한 단일 HTML(theme-showcase.html)을 만든다.
임의 테마 10종을 나열하는 게 아니라 "시그니처 1 + 등록 오버레이 N"을 보여준다.

토큰 값은 SoT 런타임 로드(미러 금지). 색 수학은 validate_overlay.py를 재사용.
다크 상수의 정본은 mode-mapping.md §3·§3.2.

사용:
    python3 build_showcase.py                          # 전체 → theme-showcase.html
    python3 build_showcase.py --overlay remember       # 특정 오버레이만
    python3 build_showcase.py --preview-primary "#0A2540" --preview-accent "#7C3AED"  # 발행 후보 미리보기
    python3 build_showcase.py --out /tmp/show.html
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_overlay import lighten, contrast  # 색 수학 재사용

_SOT = Path(__file__).resolve().parents[2] / "jc-design-system"

# 다크 모드 상수 — 정본: mode-mapping.md §3 / §3.2 (라이트엔 §6 JSON, 다크는 표라서 여기 미러)
DARK = {
    "bg": "#0A1220", "surface": "#152134", "surfaceAlt": "#1F2C42",
    "text": "#E8ECF2", "textMuted": "#A0A8B4", "border": "#2A3650",
    "data": ["#5B8DEF", "#F04D85", "#FF7649", "#33EE92", "#C9CFD8", "#A78BFA"],
}
LIGHT_FALLBACK = {  # SoT 로드 실패 시 폴백(출처: signature-tokens.md §6)
    "primary": "#0A2540", "accent": "#2962FF", "surface": "#FFFFFF",
    "surfaceAlt": "#F1F3F7", "bg": "#F8F9FB", "text": "#1A1D24",
    "textMuted": "#5A6270", "border": "#E5E8ED",
    "data": ["#2962FF", "#E91E63", "#FF5722", "#00E676", "#0A2540", "#7C3AED"],
}


def load_signature() -> dict:
    try:
        sys.path.insert(0, str(_SOT / "scripts"))
        from jc_tokens import load_tokens  # type: ignore
        tok = load_tokens(_SOT)
        c = (tok or {}).get("color", {})
        if c:
            return {
                "primary": c.get("primary", LIGHT_FALLBACK["primary"]),
                "accent": c.get("accent", LIGHT_FALLBACK["accent"]),
                "surface": c.get("surface", LIGHT_FALLBACK["surface"]),
                "surfaceAlt": c.get("surfaceAlt", LIGHT_FALLBACK["surfaceAlt"]),
                "bg": c.get("bg", LIGHT_FALLBACK["bg"]),
                "text": c.get("text", LIGHT_FALLBACK["text"]),
                "textMuted": c.get("textMuted", LIGHT_FALLBACK["textMuted"]),
                "border": c.get("border", LIGHT_FALLBACK["border"]),
                "data": c.get("data", LIGHT_FALLBACK["data"]),
            }
    except Exception as e:
        print(f"경고: SoT({_SOT}) 토큰 로드 실패, 폴백 값 사용 — {e}", file=sys.stderr)
    return dict(LIGHT_FALLBACK)


_SLUG = re.compile(r"[a-z0-9][a-z0-9-]*$")
_HEX = re.compile(r"#?[0-9A-Fa-f]{6}$")


def _valid_hex(v) -> bool:
    return isinstance(v, str) and bool(_HEX.match(v.strip()))


def parse_overlays() -> list[dict]:
    """client-overlays.md의 등록 오버레이만 파싱. §2 스키마 예시 블록은 슬러그·hex 검사로 거른다."""
    md = _SOT / "references" / "client-overlays.md"
    out: list[dict] = []
    if md.is_file():
        for block in re.findall(r"```json\s*\n(.*?)\n```", md.read_text(encoding="utf-8"), re.DOTALL):
            try:
                d = json.loads(block)
            except Exception:
                continue
            if not (isinstance(d, dict) and "overrides" in d):
                continue
            cid = d.get("client_id", "")
            if not _SLUG.match(cid):  # 스키마 예시("string — …")·플레이스홀더 제외
                continue
            out.append(d)
    return out


def effective(sig: dict, ov: dict) -> tuple[str, str]:
    """override가 유효한 hex일 때만 적용, 아니면(null·플레이스홀더) 시그니처 유지."""
    o = ov.get("overrides", {})
    prim = o.get("primary"); acc = o.get("accent")
    return (prim if _valid_hex(prim) else sig["primary"],
            acc if _valid_hex(acc) else sig["accent"])


# ── HTML 렌더 ────────────────────────────────────────────────────────────
def _swatch(label: str, hex_: str, on_dark: bool) -> str:
    txt = "#E8ECF2" if on_dark else "#1A1D24"
    return (f'<div class="sw"><span class="chip" style="background:{hex_}"></span>'
            f'<span class="swl" style="color:{txt}">{label}<b>{hex_}</b></span></div>')


def render_card(sig: dict, prim: str, acc: str, mode: str) -> str:
    if mode == "dark":
        bg, surf, surfAlt, text, muted, border = (DARK[k] for k in ("bg", "surface", "surfaceAlt", "text", "textMuted", "border"))
        acc_eff, data = lighten(acc, 0.16), DARK["data"]
    else:
        bg, surf, surfAlt, text, muted, border = (sig[k] for k in ("bg", "surface", "surfaceAlt", "text", "textMuted", "border"))
        acc_eff, data = acc, sig["data"]
    on_dark = mode == "dark"
    btn_txt = "#FFFFFF" if contrast("#FFFFFF", acc_eff) >= 3.0 else "#0A1220"
    dots = "".join(f'<span class="dot" style="background:{data[i]}"></span>' for i in range(5))
    return f"""
      <div class="card" style="background:{bg};border-color:{border}">
        <div class="hd" style="background:{prim}">{'다크' if on_dark else '라이트'}</div>
        <div class="body">
          <div class="sws">{_swatch('primary ', prim, on_dark)}{_swatch('accent ', acc_eff, on_dark)}</div>
          <div class="kpi" style="background:{surf};border-color:{border}">
            <div class="kn" style="color:{acc_eff}">92<span style="font-size:.5em">%</span></div>
            <div class="kl" style="color:{muted}">목표 달성률</div>
          </div>
          <button class="btn" style="background:{acc_eff};color:{btn_txt}">주요 CTA</button>
          <div class="legend" style="color:{muted}">{dots}<span>차트 시리즈</span></div>
          <div class="para"><span style="color:{text}">본문 텍스트 (Pretendard)</span>
            <span style="color:{muted}">· 보조 텍스트</span></div>
        </div>
      </div>"""


def render_row(sig: dict, ov: dict) -> str:
    prim, acc = effective(sig, ov)
    cid = ov.get("client_id", "")
    name = ov.get("client_name", cid) or cid
    if "{{" in name:  # 외부 주입 변수는 표시용으로 client_id 대체 (RULE-NO-COMPANY)
        name = cid
    track = ov.get("track", "")
    notes = ov.get("notes", "")
    o = ov.get("overrides", {})
    badge = "시그니처 그대로" if not o.get("primary") and not o.get("accent") else "오버레이 적용"
    return f"""
    <section class="row">
      <div class="meta">
        <div class="cid">{cid}</div>
        <div class="cname">{name}</div>
        <div class="tags"><span class="tag">track {track}</span><span class="tag">{badge}</span></div>
        <p class="notes">{notes}</p>
      </div>
      <div class="cards">{render_card(sig, prim, acc, 'light')}{render_card(sig, prim, acc, 'dark')}</div>
    </section>"""


def build_html(rows_html: str, sig: dict) -> str:
    return f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>JC Theme Factory — 오버레이 쇼케이스</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<style>
  :root{{--fg:{sig['text']};--muted:{sig['textMuted']};--bg:{sig['bg']};--surf:{sig['surface']};--bd:{sig['border']};--primary:{sig['primary']};--accent:{sig['accent']}}}
  *{{box-sizing:border-box}}
  body{{margin:0;font-family:'Pretendard Variable',Pretendard,-apple-system,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;background:var(--bg);color:var(--fg)}}
  .pagehd{{background:var(--primary);color:#fff;padding:32px 28px}}
  .pagehd h1{{margin:0;font-size:24px;font-weight:700;letter-spacing:-.02em}}
  .pagehd p{{margin:6px 0 0;opacity:.85;font-size:14px}}
  .wrap{{max-width:1040px;margin:0 auto;padding:24px 20px 64px}}
  .row{{display:grid;grid-template-columns:240px 1fr;gap:20px;padding:20px 0;border-bottom:.5px solid var(--bd)}}
  .meta .cid{{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--accent);font-weight:600}}
  .meta .cname{{font-size:18px;font-weight:600;margin-top:2px}}
  .tags{{margin:8px 0;display:flex;gap:6px;flex-wrap:wrap}}
  .tag{{font-size:11px;background:var(--surf);border:.5px solid var(--bd);border-radius:9999px;padding:2px 9px;color:var(--muted)}}
  .notes{{font-size:12.5px;color:var(--muted);line-height:1.5;margin:6px 0 0}}
  .cards{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
  .card{{border:.5px solid;border-radius:12px;overflow:hidden}}
  .hd{{color:#fff;font-size:11px;font-weight:600;padding:6px 12px;letter-spacing:.04em}}
  .body{{padding:14px}}
  .sws{{display:flex;gap:14px;margin-bottom:12px}}
  .sw{{display:flex;align-items:center;gap:7px}}
  .chip{{width:22px;height:22px;border-radius:6px;box-shadow:inset 0 0 0 .5px rgba(0,0,0,.15)}}
  .swl{{font-size:10px;line-height:1.25;display:flex;flex-direction:column}}
  .swl b{{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:600}}
  .kpi{{border:.5px solid;border-radius:10px;padding:10px 12px;margin-bottom:10px}}
  .kn{{font-family:'JetBrains Mono',monospace;font-size:30px;font-weight:700;line-height:1}}
  .kl{{font-size:11px;margin-top:3px}}
  .btn{{border:0;border-radius:8px;padding:8px 14px;font-family:inherit;font-size:13px;font-weight:600;cursor:pointer;width:100%}}
  .legend{{display:flex;align-items:center;gap:5px;font-size:11px;margin:11px 0 9px}}
  .dot{{width:10px;height:10px;border-radius:9999px;display:inline-block}}
  .legend span:last-child{{margin-left:4px}}
  .para{{font-size:12px;line-height:1.5}}
  .foot{{max-width:1040px;margin:0 auto;padding:0 20px 48px;font-size:12px;color:var(--muted)}}
  @media print{{.row{{break-inside:avoid}}body{{background:#fff}}}}
</style></head>
<body>
  <header class="pagehd">
    <h1>JC Theme Factory — 오버레이 쇼케이스</h1>
    <p>시그니처 1 + 등록된 클라이언트 오버레이 N. 각 항목 라이트/다크. 값 정본: jc-design-system.</p>
  </header>
  <main class="wrap">{rows_html}</main>
  <footer class="foot">오버레이는 primary·accent·logo 3토큰만 시그니처 위에 덮어쓴다. 폰트·사이즈·간격·본문색은 시그니처 고정.
  신규 발행·검증은 validate_overlay.py, 절차는 references/mint-overlay.md.</footer>
</body></html>"""


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="오버레이 쇼케이스 HTML 생성")
    p.add_argument("--overlay", help="특정 client_id만 렌더")
    p.add_argument("--preview-primary", help="발행 후보 primary (미리보기 카드)")
    p.add_argument("--preview-accent", help="발행 후보 accent (미리보기 카드)")
    p.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "theme-showcase.html"))
    a = p.parse_args(argv)

    sig = load_signature()
    # 시그니처(오버레이 없음)를 맨 앞에 합성
    overlays = [{"client_id": "(signature)", "client_name": "JC 시그니처", "track": "personal",
                 "overrides": {"primary": None, "accent": None, "logo_path": None},
                 "notes": "오버레이 없음 = 기본값. 미지정 시 항상 이 시그니처가 적용된다."}]
    overlays += parse_overlays()

    if a.preview_primary or a.preview_accent:
        overlays = [{"client_id": "(preview)", "client_name": "발행 후보 미리보기", "track": "B",
                     "overrides": {"primary": a.preview_primary, "accent": a.preview_accent, "logo_path": None},
                     "notes": "validate_overlay.py 검증과 함께 사용자 리뷰용."}]
    elif a.overlay:
        overlays = [o for o in overlays if o.get("client_id") == a.overlay]
        if not overlays:
            print(f"client_id '{a.overlay}' 오버레이를 찾지 못함.", file=sys.stderr)
            return 2

    rows = "".join(render_row(sig, o) for o in overlays)
    Path(a.out).write_text(build_html(rows, sig), encoding="utf-8")
    print(f"✅ 쇼케이스 생성: {a.out}  (오버레이 {len(overlays)}종)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
