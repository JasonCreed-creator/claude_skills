#!/usr/bin/env python3
"""jc-skill lint — jc 하우스 표준 결정적 자동 채점기.

스킬 디렉터리 하나를 받아 `references/scoring-rubric.md` 정본의 8개 기준으로
0~100점을 매기고 GO / CONDITIONAL / NO-GO 판정을 낸다. 결정적(동일 입력 → 동일
점수)이며 stdlib만 쓴다. CI·체이닝용 `--json`, 자가검증 `--self-test` 지원.

사용:
    python3 lint_skill.py <skill_dir>
    python3 lint_skill.py <skill_dir> --json
    python3 lint_skill.py --self-test

채점 정본은 references/scoring-rubric.md. 본 스크립트와 그 문서는 항상 일치해야 한다.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile

# ── RULE-NO-COMPANY 금칙 리터럴(정본: jc-design-system/references/shared-rules.md#RULE-NO-COMPANY)
#    회사 상호·부서명만. 'M&C' 단독은 'M&C 견적서'(양식 식별자, §120 허용)와 충돌하므로 제외.
FORBIDDEN_LITERALS = ["엠앤씨", "M&C커뮤니케이션즈", "리멤버앤컴퍼니", "신사업실"]
#    아래 마커가 있는 줄은 sanitizer/정의/금칙리스트이므로 금칙 검사에서 면제한다.
SANITIZER_MARKERS = [
    "FORBIDDEN", "forbidden", "금칙", "sanitize", "RULE-NO-COMPANY",
    "re.sub", "scan_forbidden", "차단 리스트", "0건",
]
#    예시/플레이스홀더로 허용되는 이메일 도메인(실제 PII 아님).
ALLOWED_EMAIL_HINTS = ["example.com", "example.org", "{{", "your-", "user@", "name@"]

VERDICT_GO = 90
VERDICT_COND = 70


def _read(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except (OSError, UnicodeDecodeError):
        return ""


def parse_frontmatter(text: str) -> dict:
    """--- 펜스 사이의 단순 key: value frontmatter 파싱(PyYAML 없이)."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip("\n")
    out: dict = {}
    for line in block.splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, _, val = line.partition(":")
            out[key.strip()] = val.strip().strip('"').strip("'")
    return out


def _has_korean(s: str) -> bool:
    return any("가" <= ch <= "힣" for ch in s)


def _md_text_files(skill_dir: str) -> list[str]:
    """SKILL.md + references/*.md 본문(금칙·식별정보 검사 대상)."""
    files = []
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if os.path.isfile(skill_md):
        files.append(skill_md)
    refs = os.path.join(skill_dir, "references")
    if os.path.isdir(refs):
        for name in sorted(os.listdir(refs)):
            if name.endswith(".md"):
                files.append(os.path.join(refs, name))
    return files


def _exempt_lineset(lines: list[str], window: int = 3) -> set:
    """sanitizer/정의/금칙리스트 마커가 든 줄 ±window 줄을 면제 집합으로 반환.

    정의부(RULE-NO-COMPANY)·블록리스트(FORBIDDEN_TERMS=[...])는 마커가 헤더·선언
    줄에만 있고 리터럴은 다음 줄에 오므로, 같은 줄만 보면 오탐난다. 윈도우로 해소.
    실제 누출(템플릿 footer 등)은 주변 ±3줄에 마커가 없어 그대로 검출된다.
    """
    marked = [i for i, l in enumerate(lines) if any(m in l for m in SANITIZER_MARKERS)]
    exempt = set()
    for i in marked:
        exempt.update(range(max(0, i - window), min(len(lines), i + window + 1)))
    return exempt


def _scan_company_violations(skill_dir: str) -> list[str]:
    """sanitizer/정의 맥락(±3줄)을 제외하고 금칙 회사 리터럴이 박힌 줄을 찾는다."""
    hits = []
    for path in _md_text_files(skill_dir):
        lines = _read(path).splitlines()
        exempt = _exempt_lineset(lines)
        for idx, line in enumerate(lines):
            if idx in exempt:
                continue
            for lit in FORBIDDEN_LITERALS:
                if lit in line:
                    hits.append(f"{os.path.basename(path)}:{idx + 1} `{lit}`")
    return hits


def _scan_email_violations(skill_dir: str) -> list[str]:
    """example/플레이스홀더가 아닌 실제 이메일 주소를 찾는다(±3줄 마커 면제)."""
    pat = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
    hits = []
    for path in _md_text_files(skill_dir):
        lines = _read(path).splitlines()
        exempt = _exempt_lineset(lines)
        for idx, line in enumerate(lines):
            if idx in exempt:
                continue
            for m in pat.findall(line):
                if not any(h in m or h in line for h in ALLOWED_EMAIL_HINTS):
                    hits.append(f"{os.path.basename(path)}:{idx + 1} `{m}`")
    return hits


def lint(skill_dir: str) -> dict:
    """스킬 디렉터리를 채점해 결과 dict 반환."""
    skill_dir = os.path.abspath(skill_dir.rstrip("/"))
    dir_name = os.path.basename(skill_dir)
    skill_md_path = os.path.join(skill_dir, "SKILL.md")
    skill_md = _read(skill_md_path)
    fm = parse_frontmatter(skill_md)
    criteria: list[dict] = []

    def add(cid, label, got, mx, notes=""):
        criteria.append({"id": cid, "label": label, "score": got,
                         "max": mx, "notes": notes})

    # C1 frontmatter 완전성 (20) — name/description/version/license 각 5
    have = {k: bool(fm.get(k)) for k in ("name", "description", "version", "license")}
    c1 = sum(5 for k in have if have[k])
    add("C1", "frontmatter 완전성", c1, 20,
        "누락: " + (", ".join(k for k in have if not have[k]) or "없음"))

    # C2 명명 일치 (10) — frontmatter name == 디렉터리명
    c2 = 10 if fm.get("name") == dir_name else 0
    add("C2", "명명 일치(name==dir)", c2, 10,
        "OK" if c2 else f"name={fm.get('name')!r} != dir={dir_name!r}")

    # C3 version SemVer (10)
    ver = fm.get("version", "")
    c3 = 10 if re.match(r"^v?\d+\.\d+\.\d+$", ver) else 0
    add("C3", "version SemVer", c3, 10, "OK" if c3 else f"비정상 version={ver!r}")

    # C4 description 품질 (20) — 길이8 + 트리거4 + 경계4 + 한국어4
    desc = fm.get("description", "")
    dlen = len(desc)
    c4 = 0
    c4 += 8 if 200 <= dlen <= 1024 else (4 if 120 <= dlen < 200 else 0)
    c4 += 4 if any(k in desc for k in ("사용할 것", "언제", "트리거", "상황에서", "요청할 때")) else 0
    c4 += 4 if any(k in desc for k in ("단,", "영역", "경계", "말 것", "쓰지 말", "아니다")) else 0
    c4 += 4 if _has_korean(desc) else 0
    add("C4", "description 품질(길이·트리거·경계·한국어)", c4, 20, f"길이 {dlen}자")

    # C5 SKILL.md 분량 (10) — <500 만점, 500~600 절반, 초과 0
    n_lines = skill_md.count("\n") + 1 if skill_md else 0
    c5 = 10 if n_lines and n_lines < 500 else (5 if n_lines <= 600 else 0)
    if not skill_md:
        c5 = 0
    add("C5", "SKILL.md 분량(<500줄)", c5, 10, f"{n_lines}줄")

    # C6 LICENSE 존재 (5)
    c6 = 5 if os.path.isfile(os.path.join(skill_dir, "LICENSE.txt")) else 0
    add("C6", "LICENSE.txt 존재", c6, 5, "OK" if c6 else "없음")

    # C7 RULE-NO-COMPANY (15) — 금칙 회사 리터럴 + 실제 이메일 0건
    comp = _scan_company_violations(skill_dir)
    mail = _scan_email_violations(skill_dir)
    viol = comp + mail
    c7 = 15 if not viol else max(0, 15 - 5 * len(viol))
    add("C7", "RULE-NO-COMPANY(식별정보 0건)", c7, 15,
        "위반 0" if not viol else "; ".join(viol[:5]))

    # C8 구조 위생 (10) — references/ ≥1 .md (6) + scripts 자가검증 표지(4)
    refs = os.path.join(skill_dir, "references")
    has_refs = os.path.isdir(refs) and any(f.endswith(".md") for f in os.listdir(refs)) \
        if os.path.isdir(refs) else False
    c8 = 6 if has_refs else 0
    scripts = os.path.join(skill_dir, "scripts")
    if os.path.isdir(scripts):
        blob = "".join(_read(os.path.join(scripts, f))
                       for f in os.listdir(scripts) if f.endswith(".py"))
        c8 += 4 if ("--self-test" in blob or "self_test" in blob
                    or '__main__' in blob) else 0
    else:
        c8 += 4  # 스크립트 불요 스킬(reference-driven)은 감점하지 않음
    add("C8", "구조 위생(references/·scripts 자가검증)", c8, 10,
        ("references OK" if has_refs else "references 없음"))

    total = sum(c["score"] for c in criteria)
    verdict = "GO" if total >= VERDICT_GO else ("CONDITIONAL" if total >= VERDICT_COND else "NO-GO")
    return {"skill": dir_name, "path": skill_dir, "score": total,
            "max": 100, "verdict": verdict, "criteria": criteria}


def format_report(result: dict) -> str:
    icon = {"GO": "✅", "CONDITIONAL": "⚠️", "NO-GO": "❌"}[result["verdict"]]
    lines = [f"[lint] {result['skill']} — {result['score']}/100  {icon} {result['verdict']}",
             "-" * 60]
    for c in result["criteria"]:
        mark = "✓" if c["score"] == c["max"] else ("·" if c["score"] else "✗")
        lines.append(f"  {mark} {c['id']} {c['label']:<38} {c['score']:>2}/{c['max']:<2}  {c['notes']}")
    lines.append("-" * 60)
    band = ">=90 GO · 70-89 CONDITIONAL · <70 NO-GO"
    lines.append(f"  판정 밴드: {band}")
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────── self-test
_GOOD_DESC = (
    "테스트용 jc 스킬을 만드는 메타 작업을 검증하는 더미 스킬이다. 다음 상황에서 "
    "반드시 이 스킬을 사용할 것 — 사용자가 '테스트', '더미', '검증'을 언급할 때, "
    "샘플 산출을 요청할 때. 단, 실제 디자인 토큰 정의는 jc-design-system 영역이고, "
    "완성물의 적대적 검증은 jc-redteam 영역이므로 그쪽을 쓸 것. 이 스킬은 lint "
    "자가검증 픽스처 전용이며 다른 용도로는 트리거하지 않는다."
)


def _write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def _make_good(root: str) -> str:
    d = os.path.join(root, "jc-good")
    _write(os.path.join(d, "SKILL.md"),
           f"---\nname: jc-good\ndescription: {_GOOD_DESC}\n"
           f"version: \"v1.0.0\"\nlicense: Complete terms in LICENSE.txt\n---\n\n"
           f"# JC Good\n\n본문. 외부 주입 변수 {{{{company_name}}}}만 쓴다.\n")
    _write(os.path.join(d, "LICENSE.txt"), "Apache 2.0 ...\n")
    _write(os.path.join(d, "references", "guide.md"), "# Guide\n예시 email@example.com.\n")
    _write(os.path.join(d, "scripts", "build.py"),
           "def main():\n    pass\nif __name__ == '__main__':\n    # --self-test\n    main()\n")
    return d


def _make_bad(root: str) -> str:
    d = os.path.join(root, "jc-bad-named")  # 디렉터리명 != frontmatter name
    _write(os.path.join(d, "SKILL.md"),
           "---\nname: wrongname\ndescription: 너무 짧음\nversion: 1.0\n---\n\n"
           "# Bad\n\n작성자 이진철 / M&C커뮤니케이션즈 신사업실 leejc@mnccomm.com\n")
    return d


def self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        good = lint(_make_good(tmp))
        bad = lint(_make_bad(tmp))

    fails = []
    # 좋은 스킬: GO + 만점에 가깝다
    if good["verdict"] != "GO" or good["score"] < 90:
        fails.append(f"good 기대 GO>=90, 실제 {good['score']} {good['verdict']}")
    # 나쁜 스킬: NO-GO
    if bad["verdict"] != "NO-GO" or bad["score"] >= VERDICT_COND:
        fails.append(f"bad 기대 NO-GO<70, 실제 {bad['score']} {bad['verdict']}")
    # 개별 기준 검증
    by = {c["id"]: c for c in bad["criteria"]}
    if by["C2"]["score"] != 0:
        fails.append("bad C2(명명 불일치) 감점 실패")
    if by["C3"]["score"] != 0:
        fails.append("bad C3(version 비-SemVer) 감점 실패")
    if by["C7"]["score"] >= 15:
        fails.append("bad C7(회사·이메일 노출) 감점 실패")
    gby = {c["id"]: c for c in good["criteria"]}
    if gby["C7"]["score"] != 15:
        fails.append("good C7(위반 0) 만점 실패")
    if gby["C1"]["score"] != 20:
        fails.append("good C1(frontmatter 완전) 만점 실패")

    print(format_report(good))
    print()
    print(format_report(bad))
    print()
    if fails:
        print("SELF-TEST: FAIL")
        for f in fails:
            print("  -", f)
        return 1
    print(f"SELF-TEST: PASS (good={good['score']} GO, bad={bad['score']} NO-GO)")
    return 0


def lint_all(root: str) -> int:
    """root 아래 모든 스킬(SKILL.md 보유 디렉터리)을 채점. NO-GO 있으면 exit 1.

    CONDITIONAL은 경고(통과). CI 게이트용 — 최악 회귀(frontmatter 누락·명명 불일치·
    PII 누출·비-SemVer)만 차단하고 경미한 결함은 막지 않는다.
    """
    if not os.path.isdir(root):
        print(f"디렉터리 없음: {root}", file=sys.stderr)
        return 2
    dirs = sorted(
        os.path.join(root, n) for n in os.listdir(root)
        if os.path.isfile(os.path.join(root, n, "SKILL.md"))
    )
    if not dirs:
        print(f"스킬 없음: {root}", file=sys.stderr)
        return 2
    results = [lint(d) for d in dirs]
    icon = {"GO": "✅", "CONDITIONAL": "⚠️", "NO-GO": "❌"}
    for r in sorted(results, key=lambda x: x["score"]):
        print(f"{r['score']:>3}/100  {icon[r['verdict']]} {r['verdict']:<12} {r['skill']}")
    counts: dict = {}
    for r in results:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    print("-" * 56)
    print(f"합계 {len(results)}종 — " + " · ".join(f"{k} {counts[k]}" for k in sorted(counts)))
    nogo = [r["skill"] for r in results if r["verdict"] == "NO-GO"]
    if nogo:
        print(f"❌ NO-GO 차단: {', '.join(nogo)}", file=sys.stderr)
        return 1
    print("✅ NO-GO 없음 — 게이트 통과(CONDITIONAL은 경고).")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="jc-skill 결정적 lint 채점기")
    ap.add_argument("skill_dir", nargs="?", help="채점할 스킬 디렉터리")
    ap.add_argument("--json", action="store_true", help="JSON으로 출력(CI·체이닝)")
    ap.add_argument("--self-test", action="store_true", help="내장 픽스처로 자가검증")
    ap.add_argument("--all", action="store_true",
                    help="skill_dir를 루트로 전 스킬 일괄 채점(NO-GO 있으면 exit 1)")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()
    if args.all:
        if not args.skill_dir:
            ap.error("--all 에는 스킬 루트 경로가 필요합니다 (예: .claude/skills)")
        return lint_all(args.skill_dir)
    if not args.skill_dir:
        ap.error("skill_dir / --all / --self-test 중 하나가 필요합니다")
    if not os.path.isdir(args.skill_dir):
        print(f"디렉터리 없음: {args.skill_dir}", file=sys.stderr)
        return 2

    result = lint(args.skill_dir)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(result))
    # CONDITIONAL은 0(경고), NO-GO는 1(실패)로 종료코드 분기 → CI 게이트
    return 1 if result["verdict"] == "NO-GO" else 0


if __name__ == "__main__":
    raise SystemExit(main())
