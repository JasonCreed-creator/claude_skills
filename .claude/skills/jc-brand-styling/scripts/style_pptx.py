#!/usr/bin/env python3
"""
jc-brand-styling — 이미 존재하는 PPTX에 jc 시그니처(+선택적 클라이언트 오버레이)를
입히는 후처리 적용 엔진.

원본 brand-guidelines가 Anthropic 브랜드(오렌지 #d97757 · Poppins/Lora)를 입혔다면,
이건 jc 브랜드(Deep Navy · Electric Blue · Pretendard)를 입힌다. "어떤 오버레이인지"는
jc-theme-factory가 결정하고, 이 스크립트는 "그걸 대상 .pptx에 찍는" 짝꿍이다.

무엇을 하나
  - 헤딩(기본 24pt+)·본문 폰트를 시그니처 폰트(Pretendard, 폴백 Apple SD Gothic Neo /
    Malgun Gothic / Arial)로 교체.
  - 텍스트 색은 도형 배경 대비로 자동 선택(밝은 배경→Deep Navy, 어두운 배경→흰색).
  - 비텍스트 도형(텍스트 없는 채워진 셰이프) 채움색은 accent → Point Pool → data 시리즈
    순서로 순환 적용.

SoT(단일 진실 공급원)
  - 토큰 값은 절대 하드코딩하지 않는다. 실행 시 형제 경로의 jc-design-system을 읽는다:
        Path(__file__).resolve().parents[2] / "jc-design-system"
    (jc_tokens.py의 load_tokens/color). 로드 실패 시에만 §6 미러 상수로 폴백.
  - --client <id> 지정 시 client-overlays.md의 해당 블록에서 primary/accent 오버레이를
    적용한다(null/플레이스홀더는 시그니처 유지, 3토큰 한정).

규칙
  - RULE-PPTX-HEX: python-pptx RGBColor 에는 '#' 없는 6자리(RRGGBB)만 전달.
    (HTML/CSS 는 '#' 포함. 같은 색이라도 매체에 따라 표기가 다르다.)
    정본: jc-design-system/references/shared-rules.md#RULE-PPTX-HEX
  - RULE-WCAG: 텍스트/배경 대비는 본문 4.5:1, 큰 텍스트 3:1 목표.
    배경 대비 자동 텍스트색 선택이 이를 지원한다.
    정본: jc-design-system/references/mode-mapping.md §9
  - RULE-NO-COMPANY: 회사·실명·로고 경로는 하드코딩하지 않는다. 본 스크립트는
    텍스트 콘텐츠를 생성하지 않고 기존 슬라이드 서식만 바꾼다(식별정보 무주입).

python-pptx 미설치 시: 친절한 안내(설치법)를 출력하고 비-0으로 종료한다.

사용:
    python3 style_pptx.py 입력.pptx                         # 제자리 옆에 *_jc.pptx 생성
    python3 style_pptx.py 입력.pptx -o 출력.pptx
    python3 style_pptx.py 입력.pptx --client remember       # 오버레이 적용
    python3 style_pptx.py 입력.pptx --heading-min 28        # 헤딩 임계치 조정
    python3 style_pptx.py --self-test                       # 샘플 생성→적용 자가검증
종료코드: 0 성공 / 1 python-pptx 미설치 / 2 입력 오류.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ── SoT 토큰 로드 (형제 경로, 실패 시 §6 미러 폴백) ─────────────────────────
_SOT = Path(__file__).resolve().parents[2] / "jc-design-system"

# 폴백 미러. 정본: signature-tokens.md §6 JSON / §1. SoT 로드 성공 시 사용되지 않는다.
# (주석 출처 명시 — 플레이북 §3, check_drift.py FORBIDDEN 값은 한 건도 쓰지 않는다.)
_FALLBACK = {
    "primary": "#0A2540",        # Deep Navy
    "accent": "#2962FF",         # Electric Blue
    "surface": "#FFFFFF",
    "text": "#1A1D24",
    "point": ["#FF5722", "#E91E63", "#00E676", "#2962FF"],  # orange/magenta/neon/blue
    "data": ["#2962FF", "#E91E63", "#FF5722", "#00E676", "#0A2540", "#7C3AED"],
    "font_heading": "Pretendard",
    "font_body": "Pretendard",
    # PPTX 폴백 체인 (signature-tokens.md §2.3). python-pptx는 단일 폰트명만 받으므로
    # 첫 항목을 쓰되, 적용 후 폴백 체인을 안내한다.
    "font_fallbacks": ["Apple SD Gothic Neo", "Malgun Gothic", "Arial"],
}


def load_signature() -> dict:
    """jc-design-system §6 JSON을 런타임 로드. 실패 시 _FALLBACK."""
    sig = dict(_FALLBACK)
    try:
        sys.path.insert(0, str(_SOT / "scripts"))
        from jc_tokens import load_tokens, color  # type: ignore

        tok = load_tokens(_SOT)
        if tok:
            c = tok.get("color", {})
            sig["primary"] = color(tok, "primary", _FALLBACK["primary"])
            sig["accent"] = color(tok, "accent", _FALLBACK["accent"])
            sig["surface"] = color(tok, "surface", _FALLBACK["surface"])
            sig["text"] = color(tok, "text", _FALLBACK["text"])
            pt = c.get("point", {})
            sig["point"] = [pt.get(k) for k in ("orange", "magenta", "neon", "blue")
                            if pt.get(k)] or _FALLBACK["point"]
            sig["data"] = c.get("data") or _FALLBACK["data"]
            f = tok.get("font", {})
            # 폰트 스택의 첫 토큰을 헤딩/본문 단일 폰트로 사용(시그니처 고정 — 오버레이 대상 아님).
            sig["font_heading"] = _first_font(f.get("heading"), _FALLBACK["font_heading"])
            sig["font_body"] = _first_font(f.get("ko"), _FALLBACK["font_body"])
    except Exception:
        pass
    return sig


def _first_font(stack: str | None, fallback: str) -> str:
    """'Pretendard, Inter, ...' → 'Pretendard'. 따옴표 제거."""
    if not stack:
        return fallback
    first = stack.split(",")[0].strip().strip("'\"")
    return first or fallback


# ── 오버레이 파싱 (client-overlays.md, 3토큰 한정) ──────────────────────────
_SLUG = re.compile(r"^[a-z][a-z0-9-]*$")
_JSON_FENCE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


def _valid_hex(v) -> bool:
    return isinstance(v, str) and bool(re.fullmatch(r"#?[0-9A-Fa-f]{6}", v.strip()))


def load_overlay(client_id: str) -> dict | None:
    """client-overlays.md에서 client_id 블록을 찾아 반환. 없으면 None."""
    md = _SOT / "references" / "client-overlays.md"
    if not md.is_file():
        return None
    for block in _JSON_FENCE.findall(md.read_text(encoding="utf-8")):
        try:
            d = json.loads(block)
        except Exception:
            continue
        if not (isinstance(d, dict) and "overrides" in d):
            continue
        if d.get("client_id") == client_id and _SLUG.match(client_id or ""):
            return d
    return None


def apply_overlay(sig: dict, overlay: dict | None) -> dict:
    """null이 아닌 유효 hex일 때만 primary/accent를 덮어쓴다(3토큰 한정, 폰트 불변)."""
    if not overlay:
        return sig
    o = overlay.get("overrides", {})
    out = dict(sig)
    if _valid_hex(o.get("primary")):
        out["primary"] = o["primary"]
    if _valid_hex(o.get("accent")):
        out["accent"] = o["accent"]
    return out


# ── 색 수학 (대비 자동 텍스트색 — RULE-WCAG / mode-mapping §9.1) ─────────────
def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"잘못된 hex: {h!r}")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def to_pptx_hex(h: str) -> str:
    """RULE-PPTX-HEX: '#' 없는 대문자 6자리. RGBColor.from_string에 그대로 전달 가능."""
    return h.strip().lstrip("#").upper()


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


def text_on(bg_hex: str, light_hex: str, dark_hex: str) -> str:
    """배경 대비로 더 읽기 쉬운 텍스트색 선택(흰 vs Deep Navy). 동률이면 어두운색."""
    return dark_hex if contrast(bg_hex, dark_hex) >= contrast(bg_hex, light_hex) else light_hex


# ── PPTX 스타일링 (python-pptx) ────────────────────────────────────────────
def _missing_pptx_msg() -> str:
    return (
        "오류: 'python-pptx'가 설치되어 있지 않습니다. 이 스크립트는 PPTX 후처리에\n"
        "python-pptx가 필요합니다. 다음 중 하나로 설치한 뒤 다시 실행하세요:\n\n"
        "    pip install python-pptx\n"
        "    python3 -m pip install python-pptx\n\n"
        "설치 권한이 없는 환경이라면, 토큰 값(아래)을 참고해 수동으로 서식을 적용하거나\n"
        "python-pptx가 설치된 환경에서 본 스크립트를 실행하세요.\n"
        "  · 헤딩/본문 폰트: Pretendard (폴백 Apple SD Gothic Neo / Malgun Gothic / Arial)\n"
        "  · 텍스트색: 배경 대비 자동 (밝은 배경→Deep Navy, 어두운 배경→흰색)\n"
        "  · 비텍스트 도형: accent → Point Pool → data 시리즈 순환\n"
        "토큰 정본: jc-design-system/references/signature-tokens.md §6"
    )


def style_presentation(in_path: Path, out_path: Path, sig: dict,
                       heading_min_pt: float = 24.0) -> dict:
    """기존 PPTX를 열어 폰트·텍스트색·도형 채움을 jc 시그니처로 재서식. 통계 dict 반환."""
    from pptx import Presentation
    from pptx.dml.color import RGBColor

    def rgb(h: str) -> "RGBColor":
        # RULE-PPTX-HEX: '#' 제거한 6자리만 RGBColor로.
        return RGBColor.from_string(to_pptx_hex(h))

    prs = Presentation(str(in_path))
    surface = sig["surface"]      # 기본 배경 가정(밝음) — 대비 자동 선택 기준
    light, dark = surface, sig["text"]
    # 비텍스트 도형 채움 순환 풀: accent → Point Pool → data (중복 제거, 순서 유지).
    cycle: list[str] = []
    for h in [sig["accent"], *sig["point"], *sig["data"]]:
        if _valid_hex(h):
            up = h.upper()
            if up not in {c.upper() for c in cycle}:
                cycle.append(h)
    stats = {"runs_restyled": 0, "shapes_filled": 0, "slides": 0,
             "fonts": {"heading": sig["font_heading"], "body": sig["font_body"]},
             "cycle": cycle}

    def shape_bg_hex(shape) -> str:
        """도형 채움이 단색이면 그 hex, 아니면 슬라이드 surface 가정."""
        try:
            fill = shape.fill
            if fill.type is not None and fill.fore_color and fill.fore_color.type is not None:
                return "#" + str(fill.fore_color.rgb)
        except Exception:
            pass
        return surface

    def restyle_text_frame(tf, bg_hex: str) -> None:
        for para in tf.paragraphs:
            for run in para.runs:
                font = run.font
                size_pt = font.size.pt if font.size is not None else None
                is_heading = (size_pt is not None and size_pt >= heading_min_pt) or bool(font.bold)
                font.name = sig["font_heading"] if is_heading else sig["font_body"]
                font.color.rgb = rgb(text_on(bg_hex, light, dark))
                stats["runs_restyled"] += 1

    def is_nontext_shape(shape) -> bool:
        """텍스트 없는, 채울 수 있는 도형인가(텍스트는 위에서 처리)."""
        if shape.shape_type is not None and str(shape.shape_type) == "PICTURE":
            return False
        if shape.has_text_frame and shape.text_frame.text.strip():
            return False
        return hasattr(shape, "fill")

    def walk(shapes, depth=0):
        for shape in shapes:
            # 그룹 재귀
            if shape.shape_type is not None and str(shape.shape_type) == "GROUP":
                try:
                    walk(shape.shapes, depth + 1)
                except Exception:
                    pass
                continue
            # 텍스트가 있으면 텍스트 재서식
            if shape.has_text_frame and shape.text_frame.text.strip():
                restyle_text_frame(shape.text_frame, shape_bg_hex(shape))
            elif is_nontext_shape(shape):
                col = cycle[stats["shapes_filled"] % len(cycle)] if cycle else sig["accent"]
                try:
                    shape.fill.solid()
                    shape.fill.fore_color.rgb = rgb(col)
                    stats["shapes_filled"] += 1
                except Exception:
                    pass
            # 표 셀 텍스트
            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        restyle_text_frame(cell.text_frame, shape_bg_hex(shape))

    for slide in prs.slides:
        stats["slides"] += 1
        walk(slide.shapes)

    prs.save(str(out_path))
    return stats


# ── 자가검증: 샘플 PPTX를 코드로 생성 → 스타일 적용 ─────────────────────────
def _build_sample(path: Path) -> None:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE

    prs = Presentation()  # 기본 16:9 아님(4:3) — 검증용이라 무관
    # 슬라이드 1: 제목+본문 (헤딩/본문 폰트 분기 확인)
    s1 = prs.slides.add_slide(prs.slide_layouts[1])
    s1.shapes.title.text = "JC 브랜드 스타일링 샘플"
    body = s1.placeholders[1].text_frame
    body.text = "이 본문은 Pretendard 본문 폰트로 바뀌어야 한다."
    body.add_paragraph().text = "두 번째 줄 — 색은 배경 대비로 자동 선택."
    # 헤딩 크기 강제(임계치 검증 — 32pt > 기본 24pt)
    for p in s1.shapes.title.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(32)
    # 슬라이드 2: 비텍스트 도형 3개 (채움 순환 확인)
    s2 = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    for i in range(3):
        s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                            Inches(0.5 + i * 2.2), Inches(1.0), Inches(2.0), Inches(1.2))
    prs.save(str(path))


def self_test() -> int:
    import tempfile

    sig = load_signature()
    src = "SoT" if sig["primary"] == "#0A2540" and (_SOT / "references").exists() else "폴백"
    print(f"[self-test] 시그니처 로드: {src}")
    print(f"            primary={sig['primary']} accent={sig['accent']} "
          f"heading-font={sig['font_heading']}")
    with tempfile.TemporaryDirectory() as d:
        sample = Path(d) / "sample.pptx"
        styled = Path(d) / "sample_jc.pptx"
        _build_sample(sample)
        print(f"[self-test] 샘플 PPTX 생성: {sample.name} ({sample.stat().st_size} bytes)")
        stats = style_presentation(sample, styled, sig)
        ok = styled.is_file() and styled.stat().st_size > 0
        print(f"[self-test] 스타일 적용 → {styled.name} "
              f"({styled.stat().st_size} bytes)" if ok else "[self-test] 출력 생성 실패")
        print(f"            슬라이드 {stats['slides']} · 텍스트 런 {stats['runs_restyled']}개 "
              f"재서식 · 비텍스트 도형 {stats['shapes_filled']}개 채움")
        print(f"            채움 순환 풀: {', '.join(stats['cycle'][:6])}{' …' if len(stats['cycle'])>6 else ''}")
        # 적용 결과 재검증: 폰트·채움이 실제로 들어갔는지 다시 열어 확인
        from pptx import Presentation
        prs = Presentation(str(styled))
        fonts, fills = set(), []
        for sl in prs.slides:
            for sh in sl.shapes:
                if sh.has_text_frame:
                    for p in sh.text_frame.paragraphs:
                        for r in p.runs:
                            if r.font.name:
                                fonts.add(r.font.name)
                try:
                    if sh.fill.type is not None and sh.fill.fore_color.type is not None and not (
                            sh.has_text_frame and sh.text_frame.text.strip()):
                        fills.append("#" + str(sh.fill.fore_color.rgb))
                except Exception:
                    pass
        print(f"[self-test] 검증: 적용된 폰트 {sorted(fonts)} · 도형 채움색 {fills}")
        expect_font = sig["font_heading"] in fonts or sig["font_body"] in fonts
        passed = ok and stats["runs_restyled"] > 0 and stats["shapes_filled"] > 0 and expect_font
        print("[self-test] 결과:", "✅ PASS" if passed else "❌ FAIL")
        return 0 if passed else 1


# ── CLI ─────────────────────────────────────────────────────────────────
def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="기존 PPTX에 jc 시그니처(+선택 클라이언트 오버레이)를 입히는 후처리 엔진")
    p.add_argument("input", nargs="?", help="대상 .pptx 경로")
    p.add_argument("-o", "--output", help="출력 .pptx 경로 (기본: <입력>_jc.pptx)")
    p.add_argument("--client", help="client-overlays.md의 client_id (primary/accent 오버레이)")
    p.add_argument("--heading-min", type=float, default=24.0,
                   help="헤딩으로 간주할 최소 pt (기본 24)")
    p.add_argument("--self-test", action="store_true",
                   help="샘플 PPTX 생성→적용으로 엔진 동작 자가검증")
    a = p.parse_args(argv)

    # python-pptx 가용성 확인 (RULE: 미설치 시 친절한 안내 후 비-0 종료)
    try:
        import pptx  # noqa: F401
    except Exception:
        print(_missing_pptx_msg(), file=sys.stderr)
        return 1

    if a.self_test:
        return self_test()

    if not a.input:
        p.error("입력 .pptx 경로가 필요합니다 (또는 --self-test).")
    in_path = Path(a.input)
    if not in_path.is_file():
        print(f"입력 오류: 파일을 찾을 수 없음 — {in_path}", file=sys.stderr)
        return 2
    if in_path.suffix.lower() != ".pptx":
        print(f"입력 오류: .pptx 파일이 아님 — {in_path}", file=sys.stderr)
        return 2
    out_path = Path(a.output) if a.output else in_path.with_name(in_path.stem + "_jc.pptx")

    sig = load_signature()
    overlay = None
    if a.client:
        overlay = load_overlay(a.client)
        if overlay is None:
            print(f"경고: client_id '{a.client}' 오버레이를 client-overlays.md에서 찾지 못함 "
                  f"— 시그니처로 진행.", file=sys.stderr)
        sig = apply_overlay(sig, overlay)

    src = "SoT(jc-design-system)" if (_SOT / "references").exists() else "폴백 미러"
    print(f"토큰 출처: {src}")
    print(f"적용: primary={sig['primary']} accent={sig['accent']} "
          f"폰트(헤딩/본문)={sig['font_heading']}/{sig['font_body']}"
          + (f" · 오버레이={a.client}" if overlay else ""))

    try:
        stats = style_presentation(in_path, out_path, sig, a.heading_min)
    except Exception as e:
        print(f"스타일 적용 실패: {e}", file=sys.stderr)
        return 2

    print(f"완료 → {out_path}")
    print(f"  슬라이드 {stats['slides']} · 텍스트 런 {stats['runs_restyled']}개 재서식 · "
          f"비텍스트 도형 {stats['shapes_filled']}개 채움")
    print(f"  폰트 폴백 체인(미설치 시): {sig['font_heading']} → "
          + " → ".join(_FALLBACK["font_fallbacks"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
