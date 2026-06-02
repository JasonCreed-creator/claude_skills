#!/usr/bin/env python3
"""
R1 drift-guard — jc-design-system(SoT) 정합 회귀 방지.

R1 정합화에서 consumer 스킬로부터 제거한 '비-canon' 디자인 토큰값이 다시
라이브 코드값으로 유입됐는지 검사한다. 주석(/* */, //)·교정이력·문서 설명은 무시하고
실제 적용되는 값만 본다. 드리프트 발견 시 비-0 으로 종료(CI 실패).

대상: .claude/skills/<consumer>/  (infographic-patterns.md 제외 — 매체별 스케일/히트맵은 R1 범위 밖)
사용: python3 scripts/check_drift.py        (정합 검사)
      python3 scripts/check_drift.py --selftest  (탐지기 자체 검증)
"""
from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
SKILLS = REPO / ".claude" / "skills"
CONSUMERS = ["mice-estimate", "pt-script", "mice-dashboard", "mice-sponsor-deck", "mice-proposal"]
EXCLUDE_NAMES = {"infographic-patterns.md"}  # 매체별 구현(히트맵/스케일) — R1 범위 밖
SCAN_SUFFIXES = {".md", ".html", ".css", ".js", ".py"}

# R1에서 제거된 '절대 비-canon' drift 값 → 사유. (#7C3AED 는 이제 canon data-6 이므로 제외)
FORBIDDEN = {
    "0f172a": "slate-900 (dashboard 구 다크 bg)",
    "1e293b": "slate-800 (dashboard 구 다크 카드/텍스트)",
    "334155": "slate-700 (dashboard 구 다크 보더)",
    "475569": "slate-600",
    "64748b": "slate-500",
    "94a3b8": "slate-400",
    "cbd5e1": "slate-300",
    "e2e8f0": "slate-200",
    "f1f5f9": "slate-100",
    "1a1a2e": "구 dashboard 다크",
    "2563eb": "tailwind blue-600 (dashboard 구 brand/series-1)",
    "0891b2": "tailwind cyan (구 series-3)",
    "d97706": "tailwind amber (구 series-4)",
    "db2777": "tailwind pink (구 series-5)",
    "059669": "tailwind emerald (구 series-6)",
    "1f4068": "덱 구 다크 변형",
    "2a4a6e": "덱 구 다크 변형",
    "6b7b92": "덱 구 다크 muted",
    "12304d": "덱 구 다크 보조 서피스",
    "ffe5dd": "pt-script 구 drift",
    "003366": "estimate 구 Excel 네이비",
    "ff6d01": "estimate 구 Excel 오렌지",
    "434343": "estimate 구 그레이",
    "0066cc": "estimate 구 블루",
}
# 라이브가 아닌 '교정이력/문서' 라인을 한 번 더 걸러내는 방어 마커
DOC_MARKERS = ("구 ", "구#", "→", "미러", "SoT", "drift", "이력", "기존", "before", "legacy", "deprecat")

_ALT = "|".join(sorted(FORBIDDEN, key=len, reverse=True))
RE_GENERAL = re.compile(r"(?<![0-9A-Fa-f])#(" + _ALT + r")(?![0-9A-Fa-f])", re.I)
RE_PY = re.compile(r"""['"]#?(""" + _ALT + r""")['"]""", re.I)
RE_BLOCK = re.compile(r"/\*.*?\*/", re.S)
RE_LINE = re.compile(r"//[^\n]*")


def scan_text(text: str, is_py: bool):
    text = RE_BLOCK.sub(" ", text)   # /* ... */ 주석 제거(교정이력 주석 포함)
    text = RE_LINE.sub(" ", text)    # // ... 주석 제거
    pat = RE_PY if is_py else RE_GENERAL
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if any(mk in line for mk in DOC_MARKERS):
            continue
        for m in pat.finditer(line):
            hits.append((i, m.group(1).lower(), line.strip()[:120]))
    return hits


def main() -> int:
    findings = []
    for consumer in CONSUMERS:
        base = SKILLS / consumer
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in SCAN_SUFFIXES or path.name in EXCLUDE_NAMES:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for ln, val, snippet in scan_text(text, path.suffix == ".py"):
                findings.append((path.relative_to(REPO), ln, val, snippet))

    if findings:
        print("❌ drift-guard: 비-canon 토큰값이 라이브 코드에서 발견됨 (R1 회귀)")
        for rel, ln, val, snippet in findings:
            print(f"  {rel}:{ln}  #{val}  ({FORBIDDEN[val]})")
            print(f"      {snippet}")
        print(f"\n총 {len(findings)}건. jc-design-system(SoT) 정본 토큰값으로 교정하세요.")
        print("정본: signature-tokens.md §6 JSON / mode-mapping.md §3·§3.2·§7")
        return 1
    print("✅ drift-guard 통과 — consumer 스킬에 비-canon 토큰 드리프트 없음.")
    return 0


def selftest() -> int:
    """탐지기가 (a) 라이브 드리프트를 잡고 (b) 주석/이력은 무시하는지 검증."""
    bad_css = "  --jc-bg: #0f172a;\n  --series-1: #2563eb;\n"
    bad_py = '    fill = "FF6D01"\n'
    ok_comment = "  --jc-bg: #0A1220; /* 구 #0f172a D1 drift 교정 */\n"
    ok_doc = "v1은 #003366 을 직접 사용했다 → v2에서 토큰화.\n"
    ok_canon = "  --jc-accent: #2962FF;\n  --jc-data-6: #7C3AED;\n"
    checks = [
        ("라이브 CSS 드리프트 탐지", len(scan_text(bad_css, False)) == 2),
        ("라이브 .py 드리프트 탐지", len(scan_text(bad_py, True)) == 1),
        ("교정이력 주석 무시", scan_text(ok_comment, False) == []),
        ("문서 설명(→) 무시", scan_text(ok_doc, False) == []),
        ("canon 값 통과", scan_text(ok_canon, False) == []),
    ]
    ok = True
    for name, passed in checks:
        print(f"  {'✅' if passed else '❌'} {name}")
        ok = ok and passed
    print("selftest", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
