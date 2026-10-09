#!/usr/bin/env python
"""
render_guide.py — jc-kv-guide 렌더러

guide.json(정본 1개) → <slug>.md + <slug>.html 을 동시에 만든다.
같은 데이터에서 두 산출물이 나오므로 HTML·MD 간 드리프트가 없다.

사용법:
    python scripts/render_guide.py --input guide.json --out-dir out/ [--strict] [--template assets/guide-template.html]
    python scripts/render_guide.py --self-test      # 샘플 렌더 자가 검증

동작:
  1. 구조 검증 — 8섹션 존재, source 태그 4종, quote→ref 필수, tbd→question 필수·value 비움,
     standard는 섹션 06·08에만 허용
  2. NO-DESIGN 게이트 — quote가 아닌 텍스트에서 금칙어 스캔. --strict면 검출 시 종료 코드 2
     (variable은 경고만 — 사용자가 준 값이므로 삭제 대상이 아니라 확인 대상)
  3. 질문 집계 — tbd 항목의 question을 섹션 순서대로 모아 두 산출물 말미와 stdout에 출력
  4. 렌더 — MD 직접 생성, HTML은 템플릿 셸의 {{...}} 슬롯을 채움

stdlib만 사용한다. 외부 패키지 없음.
룩 토큰의 정본은 jc-design-system/references/signature-tokens.md — 값은 템플릿 CSS에만 있다(이 파일에는 색 값 없음).
발행 주체(issuer)가 비었거나 미치환 슬롯이면 DEFAULT_ISSUER(리멤버 MICE비즈팀)를 넣는다.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# 상수
# ---------------------------------------------------------------------------

DEFAULT_ISSUER = "리멤버 MICE비즈팀"  # RULE-NO-COMPANY v2 — 리멤버 명의 기본

SECTION_IDS = ["01", "02", "03", "04", "05", "06", "07", "08"]
SOURCES = {"quote", "variable", "tbd", "standard"}
STANDARD_ALLOWED_SECTIONS = {"06", "08"}

SOURCE_LABEL = {
    "quote": "원문",
    "variable": "주입값",
    "tbd": "확인 필요",
    "standard": "표준",
}

# 섹션별 한 줄 안내 — 템플릿 고정 문장(콘텐츠가 아니라 문서 안내). 디자인 방향 서술 없음.
SECTION_LEAD = {
    "01": "행사의 사실 정보와 발주처가 정한 핵심 메시지. 문장은 원문 그대로입니다.",
    "02": "키비주얼이 쓰이는 지면과 보는 사람.",
    "03": "빠지면 안 되는 텍스트·로고와 그 표기 순서. 순서는 발주처가 정합니다.",
    "04": "브랜드 가이드에 적힌 값. 어떤 색을 어디에 쓸지는 이 문서가 정하지 않습니다.",
    "05": "발주처 자료에 실제로 적힌 표현만 인용합니다. 없으면 확인 요청으로 남깁니다.",
    "06": "발주처가 지정한 금지 + 표준 안전 항목([표준] 표시). 표준 항목은 발주처·디자이너가 삭제할 수 있습니다.",
    "07": "크기·비율·해상도·안전영역·파일 형식. 숫자는 추정하지 않습니다.",
    "08": "납품물·마감·검수 기준. 검수는 사실 확인 항목만 봅니다.",
}

# NO-DESIGN 게이트 금칙어 — quote가 아닌 텍스트에서 검출되면 삭제 대상
FORBIDDEN_PATTERNS = [
    r"컨셉", r"시안", r"목업", r"무드보드", r"레이아웃", r"구도", r"조합",
    r"추천", r"느낌", r"분위기", r"레퍼런스", r"참고\s*이미지", r"톤앤매너", r"톤\s*&\s*매너",
]
FORBIDDEN_RE = re.compile("|".join(FORBIDDEN_PATTERNS))

# ---------------------------------------------------------------------------
# 검증
# ---------------------------------------------------------------------------


class GuideError(Exception):
    pass


def validate(doc: dict) -> list[str]:
    """구조 오류를 모아 반환한다. 비어 있으면 통과."""
    errors: list[str] = []
    if doc.get("$schema") != "ChainPayload/v1":
        errors.append("$schema 는 'ChainPayload/v1' 이어야 합니다")
    if doc.get("source") != "jc-kv-guide":
        errors.append("source 는 'jc-kv-guide' 이어야 합니다")
    g = doc.get("guide")
    if not isinstance(g, dict):
        errors.append("guide 객체가 없습니다")
        return errors
    for key in ("eventName", "docVersion", "issuedAt", "slug", "inputDocs", "sections"):
        if key not in g:
            errors.append(f"guide.{key} 누락")
    if "slug" in g and not re.fullmatch(r"[a-z0-9-]+", g["slug"]):
        errors.append("guide.slug 는 소문자·숫자·하이픈만")

    doc_ids = {d.get("id") for d in g.get("inputDocs", []) if isinstance(d, dict)}
    sections = g.get("sections", [])
    got_ids = [s.get("id") for s in sections]
    if got_ids != SECTION_IDS:
        errors.append(f"섹션 id 순서는 {SECTION_IDS} 이어야 합니다 (현재 {got_ids})")

    for s in sections:
        sid = s.get("id", "?")
        for i, it in enumerate(s.get("items", [])):
            where = f"섹션 {sid} 항목#{i+1} '{it.get('label', '')}'"
            src = it.get("source")
            if src not in SOURCES:
                errors.append(f"{where}: source 가 {sorted(SOURCES)} 중 하나가 아닙니다")
                continue
            val = it.get("value", "")
            if src == "quote":
                ref = it.get("ref", "")
                if not ref:
                    errors.append(f"{where}: quote 는 ref(출처)가 필수입니다")
                elif doc_ids and ref.split()[0] not in doc_ids:
                    errors.append(f"{where}: ref '{ref}' 의 문서 ID가 inputDocs 에 없습니다")
                if not val:
                    errors.append(f"{where}: quote 인데 value 가 비어 있습니다")
            elif src == "tbd":
                if val:
                    errors.append(f"{where}: tbd 는 value 를 비워야 합니다 (채우면 추측)")
                if not it.get("question"):
                    errors.append(f"{where}: tbd 는 question(발주처 질문)이 필수입니다")
            elif src == "standard" and sid not in STANDARD_ALLOWED_SECTIONS:
                errors.append(f"{where}: standard 는 섹션 06·08 에서만 허용됩니다")
            elif src == "variable" and not val:
                errors.append(f"{where}: variable 인데 value 가 비어 있습니다 — 값이 없으면 tbd 로")
        for sw in s.get("swatches", []) or []:
            if not re.fullmatch(r"#[0-9A-Fa-f]{6}", sw.get("hex", "")):
                errors.append(f"섹션 {sid} 스와치 '{sw.get('name')}': hex 형식 오류")
            if sw.get("source") not in {"quote", "variable"}:
                errors.append(f"섹션 {sid} 스와치 '{sw.get('name')}': source 는 quote/variable 만")
    return errors


def scan_forbidden(doc: dict) -> tuple[list[str], list[str]]:
    """(실패 목록, 경고 목록). quote 는 스캔 제외, variable 은 경고, 나머지는 실패."""
    fails: list[str] = []
    warns: list[str] = []
    g = doc["guide"]
    for s in g.get("sections", []):
        sid = s["id"]
        for it in s.get("items", []):
            src = it.get("source")
            if src == "quote":
                continue
            text = f"{it.get('label', '')} {it.get('value', '')} {it.get('question', '')}"
            m = FORBIDDEN_RE.search(text)
            if not m:
                continue
            msg = f"섹션 {sid} '{it.get('label')}' — 금칙어 '{m.group(0)}' 검출"
            (warns if src == "variable" else fails).append(msg)
    for c in g.get("sourceCorrections", []) or []:
        m = FORBIDDEN_RE.search(f"{c.get('suggested', '')} {c.get('reason', '')}")
        if m:
            fails.append(f"원문 수정 제안 '{c.get('ref')}' — 금칙어 '{m.group(0)}' 검출")
    return fails, warns


def collect_questions(doc: dict) -> list[dict]:
    out = []
    for s in doc["guide"]["sections"]:
        for it in s.get("items", []):
            if it.get("source") == "tbd":
                out.append({"section": f"{s['id']} {s['title']}", "label": it["label"], "question": it["question"]})
    return out


# ---------------------------------------------------------------------------
# MD 렌더
# ---------------------------------------------------------------------------


def _md_cell(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ")


def render_md(doc: dict, questions: list[dict]) -> str:
    g = doc["guide"]
    L: list[str] = []
    L.append(f"# {g['eventName']} — 키비주얼(KV) 제작 가이드")
    L.append("")
    meta = [f"문서 버전 {g['docVersion']}", f"발행일 {g['issuedAt']}"]
    if g.get("issuer"):
        meta.append(f"발행 {g['issuer']}")
    L.append(" · ".join(meta))
    L.append("")
    L.append("> 이 문서는 규칙·제약·필수 요소·규격·검수 기준만 담습니다. 디자인 결정은 디자이너의 몫입니다.")
    L.append("> 출처 표시 — **원문**: 발주처 자료 그대로 / **주입값**: 이번 건에 전달받은 값 / **확인 필요**: 발주처 확인 대기 / **표준**: 공통 안전 항목(삭제 가능)")
    L.append("")
    L.append("## 입력 문서")
    for d in g.get("inputDocs", []):
        L.append(f"- **{d['id']}** {d['name']}")
    L.append("")

    for s in g["sections"]:
        L.append(f"## {s['id']}. {s['title']}")
        L.append("")
        L.append(SECTION_LEAD.get(s["id"], ""))
        L.append("")
        L.append("| 항목 | 내용 | 출처 |")
        L.append("|---|---|---|")
        for it in s.get("items", []):
            src = it["source"]
            if src == "tbd":
                val, srccol = "**[확인 필요]**", "확인 필요"
            elif src == "quote":
                val, srccol = _md_cell(it.get("value", "")), f"원문 · {it.get('ref', '')}"
            elif src == "standard":
                val, srccol = _md_cell(it.get("value", "")), "[표준]"
            else:
                val, srccol = _md_cell(it.get("value", "")), "주입값"
            L.append(f"| {_md_cell(it['label'])} | {val} | {srccol} |")
        if s.get("swatches"):
            L.append("")
            L.append("**색상 값** (표시만 — 용도·조합은 이 문서가 정하지 않음)")
            L.append("")
            L.append("| 이름 | 색상 코드 | 출처 |")
            L.append("|---|---|---|")
            for sw in s["swatches"]:
                srccol = f"원문 · {sw.get('ref', '')}" if sw["source"] == "quote" else "주입값"
                L.append(f"| {_md_cell(sw['name'])} | `{sw['hex']}` | {srccol} |")
        L.append("")

    if g.get("sourceCorrections"):
        L.append("## 원문 수정 제안")
        L.append("")
        L.append("원문은 그대로 두었습니다. 아래는 오탈자·명백한 오류로 보이는 부분이며 발주처 확인 후 반영합니다.")
        L.append("")
        L.append("| 위치 | 원문 | 제안 | 사유 |")
        L.append("|---|---|---|---|")
        for c in g["sourceCorrections"]:
            L.append(f"| {_md_cell(c['ref'])} | {_md_cell(c['original'])} | {_md_cell(c['suggested'])} | {_md_cell(c['reason'])} |")
        L.append("")

    L.append(f"## 발주처 확인 질문 ({len(questions)}건)")
    L.append("")
    if questions:
        for i, q in enumerate(questions, 1):
            L.append(f"{i}. [{q['section']} — {q['label']}] {q['question']}")
    else:
        L.append("확인 필요 항목이 없습니다.")
    L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------------------
# HTML 렌더
# ---------------------------------------------------------------------------


def _e(s: str) -> str:
    return html.escape(s or "", quote=True)


def _badge(src: str, ref: str = "") -> str:
    label = SOURCE_LABEL.get(src, src)
    ref_html = f' <span class="ref">{_e(ref)}</span>' if ref else ""
    return f'<span class="badge badge-{src}">{label}</span>{ref_html}'


def render_html_body(doc: dict, questions: list[dict]) -> dict:
    g = doc["guide"]
    parts: list[str] = []

    # 입력 문서
    parts.append('<section class="card" id="inputs"><div class="sec-head"><span class="num">입력</span><h2>입력 문서</h2></div><ul class="docs">')
    for d in g.get("inputDocs", []):
        parts.append(f'<li><span class="doc-id">{_e(d["id"])}</span>{_e(d["name"])}</li>')
    parts.append("</ul></section>")

    for s in g["sections"]:
        sid = s["id"]
        parts.append(f'<section class="card" id="s{sid}">')
        parts.append(f'<div class="sec-head"><span class="num">{sid}</span><h2>{_e(s["title"])}</h2></div>')
        parts.append(f'<p class="lead-sm">{_e(SECTION_LEAD.get(sid, ""))}</p>')
        parts.append('<table><thead><tr><th>항목</th><th>내용</th><th>출처</th></tr></thead><tbody>')
        for it in s.get("items", []):
            src = it["source"]
            label = _e(it["label"])
            if src == "tbd":
                val = '<span class="tbd">[확인 필요]</span>'
                srccol = _badge("tbd")
            elif src == "quote":
                val = f'<span class="quote">{_e(it.get("value", ""))}</span>'
                srccol = _badge("quote", it.get("ref", ""))
            elif src == "standard":
                val = _e(it.get("value", ""))
                srccol = _badge("standard")
            else:
                val = f'<code class="var">{_e(it.get("value", ""))}</code>' if "{{" in it.get("value", "") else _e(it.get("value", ""))
                srccol = _badge("variable")
            parts.append(f"<tr><td class=\"label\">{label}</td><td>{val}</td><td class=\"src\">{srccol}</td></tr>")
        parts.append("</tbody></table>")
        if s.get("swatches"):
            parts.append('<p class="lead-sm swatch-note">색상 값 — 표시만 합니다. 용도·조합은 이 문서가 정하지 않습니다.</p><div class="swatches">')
            for sw in s["swatches"]:
                hexv = sw["hex"].upper()
                srccol = _badge(sw["source"], sw.get("ref", "") if sw["source"] == "quote" else "")
                parts.append(
                    f'<div class="swatch"><div class="chip" style="background:{_e(hexv)}"></div>'
                    f'<div class="sw-name">{_e(sw["name"])}</div><div class="sw-hex">{_e(hexv)}</div><div class="sw-src">{srccol}</div></div>'
                )
            parts.append("</div>")
        parts.append("</section>")

    if g.get("sourceCorrections"):
        parts.append('<section class="card" id="corrections"><div class="sec-head"><span class="num">부록</span><h2>원문 수정 제안</h2></div>')
        parts.append('<p class="lead-sm">원문은 그대로 두었습니다. 아래는 오탈자·명백한 오류로 보이는 부분이며 발주처 확인 후 반영합니다.</p>')
        parts.append('<table><thead><tr><th>위치</th><th>원문</th><th>제안</th><th>사유</th></tr></thead><tbody>')
        for c in g["sourceCorrections"]:
            parts.append(f"<tr><td class=\"label\">{_e(c['ref'])}</td><td>{_e(c['original'])}</td><td>{_e(c['suggested'])}</td><td>{_e(c['reason'])}</td></tr>")
        parts.append("</tbody></table></section>")

    # 질문 리스트
    q_lines = [f"{i}. [{q['section']} — {q['label']}] {q['question']}" for i, q in enumerate(questions, 1)]
    q_text = "\n".join(q_lines) if q_lines else "확인 필요 항목이 없습니다."
    parts.append(f'<section class="card questions" id="questions"><div class="sec-head"><span class="num">확인</span><h2>발주처 확인 질문 <span class="count">{len(questions)}건</span></h2></div>')
    parts.append('<p class="lead-sm">아래 항목이 확정되면 가이드의 [확인 필요]가 채워집니다. 그대로 복사해 발주처에 보낼 수 있습니다.</p>')
    parts.append(f'<pre id="qtext">{_e(q_text)}</pre><button class="btn" type="button" onclick="copyQ()">질문 복사</button></section>')

    nav = ['<a href="#inputs">입력</a>']
    nav += [f'<a href="#s{s["id"]}">{s["id"]} {_e(s["title"])}</a>' for s in g["sections"]]
    if g.get("sourceCorrections"):
        nav.append('<a href="#corrections">원문 수정 제안</a>')
    nav.append(f'<a href="#questions">확인 질문 {len(questions)}</a>')

    meta = [f"문서 버전 {_e(g['docVersion'])}", f"발행일 {_e(g['issuedAt'])}"]
    if g.get("issuer"):
        meta.append(f"발행 {_e(g['issuer'])}")

    return {
        "TITLE": _e(f"{g['eventName']} — 키비주얼 제작 가이드"),
        "EVENT": _e(g["eventName"]),
        "META_RIGHT": " · ".join(meta),
        "NAV": "".join(nav),
        "BODY": "\n".join(parts),
        "GENERATED": _e(doc.get("generatedAt", "")),
    }


def fill_template(template: str, slots: dict) -> str:
    out = template
    for k, v in slots.items():
        out = out.replace("{{" + k + "}}", v)
    leftovers = re.findall(r"\{\{[A-Z_]+\}\}", out)
    if leftovers:
        raise GuideError(f"템플릿 슬롯 미충족: {sorted(set(leftovers))}")
    return out


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="jc-kv-guide: guide.json → .md + .html")
    ap.add_argument("--input", help="guide.json 경로")
    ap.add_argument("--self-test", action="store_true", help="assets/sample 렌더 자가 검증")
    ap.add_argument("--out-dir", default="out", help="출력 디렉터리")
    ap.add_argument("--template", default=None, help="HTML 템플릿 경로 (기본: assets/guide-template.html)")
    ap.add_argument("--strict", action="store_true", help="금칙어 검출 시 실패(종료 코드 2)")
    ap.add_argument("--md-only", action="store_true")
    ap.add_argument("--html-only", action="store_true")
    args = ap.parse_args(argv)

    here = Path(__file__).resolve().parent
    if args.self_test:
        return self_test(here)
    if not args.input:
        ap.error("--input 이 필요합니다 (또는 --self-test).")
    template_path = Path(args.template) if args.template else here.parent / "assets" / "guide-template.html"

    doc = json.loads(Path(args.input).read_text(encoding="utf-8"))

    errors = validate(doc)
    if errors:
        print("구조 검증 실패:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    apply_default_issuer(doc)
    fails, warns = scan_forbidden(doc)
    for w in warns:
        print(f"[경고] {w} — 사용자 전달값이라 삭제하지 않음. 디자인 지시가 섞였는지 확인", file=sys.stderr)
    if fails:
        print("NO-DESIGN 게이트 검출:", file=sys.stderr)
        for f in fails:
            print(f"  - {f}", file=sys.stderr)
        if args.strict:
            print("→ --strict: 해당 문장을 삭제한 뒤 다시 실행하세요.", file=sys.stderr)
            return 2
    else:
        print("NO-DESIGN 게이트 통과 (금칙어 0건)")

    questions = collect_questions(doc)
    tbd_count = sum(1 for s in doc["guide"]["sections"] for it in s["items"] if it["source"] == "tbd")
    if len(questions) != tbd_count:
        print(f"질문 수({len(questions)}) ≠ tbd 항목 수({tbd_count})", file=sys.stderr)
        return 1

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = doc["guide"]["slug"]
    written = []

    if not args.html_only:
        md_path = out_dir / f"{slug}.md"
        md_path.write_text(render_md(doc, questions), encoding="utf-8")
        written.append(md_path)
    if not args.md_only:
        template = template_path.read_text(encoding="utf-8")
        html_out = fill_template(template, render_html_body(doc, questions))
        html_path = out_dir / f"{slug}.html"
        html_path.write_text(html_out, encoding="utf-8")
        written.append(html_path)

    print(f"생성 {len(written)}개: " + ", ".join(str(p) for p in written))
    print(f"발주처 확인 질문 {len(questions)}건:")
    for i, q in enumerate(questions, 1):
        print(f"  {i}. [{q['section']} — {q['label']}] {q['question']}")
    return 0


def apply_default_issuer(doc: dict) -> None:
    """issuer가 비었거나 '{{company_name}}' 같은 미치환 슬롯이면 리멤버 명의로 채운다."""
    g = doc.get("guide", {})
    iss = str(g.get("issuer") or "").strip()
    if not iss or re.fullmatch(r"\{\{.*\}\}", iss):
        g["issuer"] = DEFAULT_ISSUER


def self_test(here: Path) -> int:
    import tempfile
    sample = here.parent / "assets" / "sample" / "guide.sample.json"
    with tempfile.TemporaryDirectory() as td:
        rc = main(["--input", str(sample), "--out-dir", td, "--strict"])
        if rc != 0:
            print(f"[self-test] FAIL — 렌더 종료 코드 {rc}")
            return 1
        outs = list(Path(td).glob("*.md")) + list(Path(td).glob("*.html"))
        texts = [p.read_text(encoding="utf-8") for p in outs]
        checks = {
            "산출물 2종": len(outs) == 2,
            "발행 주체 기본값": all(DEFAULT_ISSUER in s for s in texts),
            "미치환 company_name 0": all("{{company_name}}" not in s for s in texts),
            "HTML 슬롯 잔여 0": all(not re.search(r"\{\{[A-Z_]+\}\}", s) for s in texts),
        }
    for k, v in checks.items():
        print(f"[self-test] {k}: {'OK' if v else 'FAIL'}")
    ok = all(checks.values())
    print("[self-test]", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
