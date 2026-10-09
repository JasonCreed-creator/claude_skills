#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lint_skills — 스킬 라이브러리 정합 검사 (stdlib).

검사
  프론트매터 : SKILL.md 존재 · name=디렉터리 · description ≤1024자 · version · 업로드 비허용 필드 · YAML 절단 함정
  금지 문구  : 폐지 게이트("실행 전 … 브리프"·[A]/[B]/[C] 범위 게이트) · /mnt 샌드박스 경로
  폐합 참조  : 폐합 스킬 이름 (description은 ERROR, 본문은 이력 문맥이 아니면 ERROR)
  없는 스킬  : jc-*/mice-* 이름 중 라이브·폐합 어느 쪽에도 없는 것 (WARN)
  턴 분할    : "N턴" 표기 (폐지된 3턴 분할 잔재, 이력 문맥 제외 ERROR)
  구 모델 ID : Opus 4.x · Sonnet 4.x · claude-opus-4… · claude-sonnet-4… · claude-3… (ERROR)
  호칭       : "리더"·"팀리드" → "팀장" (리더십 제외, ERROR)
  구 시그니처: #0A2540 · #2962FF 하드코딩 (legacy 문맥 제외 ERROR)
  깨진 경로  : md 링크·백틱 경로(references/·scripts/·assets/·<스킬>/…)가 실재하지 않음 (WARN)
  스크립트   : .py 컴파일 · SKILL.md 500줄 상한
이력 문맥: '변경 이력'·'legacy'·'아카이브' 제목 아래, 또는 줄에 이력 표지(흡수·구 ·폐지·금지·legacy·→ 등)가 있으면 면제.

사용
  python lint_skills.py <스킬폴더|스킬 모음 폴더> [...]   # 경로 지정
  python lint_skills.py [--only a,b] [--exclude x]           # 정본 레포 .claude/skills 전체
  python lint_skills.py --self-test                          # 자가 테스트
  옵션 --strict : WARN도 실패 처리
종료코드: 0 통과 / 1 오류(ERROR) 있음 (--strict면 WARN도 실패)
"""
from __future__ import annotations

import argparse
import py_compile
import re
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
SKILLS = REPO / ".claude" / "skills"

ALLOWED_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools", "version", "dependencies"}
DESC_MAX = 1024
SKILL_MAX_LINES = 500

# 라이브 스킬 (2026-10-05). 새 스킬을 만들면 여기에 추가한다.
LIVE = {
    "jc-design-system", "jc-skill-forge", "jc-session-protocol", "jc-redteam", "jc-pptx", "jc-kv-guide",
    "jc-doc-coauthor", "pt-script", "mice-rfp-analyzer", "jc-strategy-canvas", "mice-market-intel",
    "mice-meeting-minutes", "mice-run-of-show", "mice-aftermath", "mice-slack-ops", "mice-estimate",
    "mice-ops-docs", "mice-team-board", "jc-slack-relay",
}
# 자가 테스트 픽스처 이름 (없는 스킬 경고에서 제외)
FIXTURES = {"jc-demo", "jc-good", "jc-bad"}
# 폐합 스킬 — `_archive` 목록
ARCHIVED = {
    "mice-sponsor-deck", "mice-proposal", "jc-prompt-builder", "jc-orchestrator", "jc-workspace-ops",
    "jc-skill-creator", "jc-theme-factory", "jc-brand-styling", "jc-remember-html", "jc-comms",
    "jc-cinematic-html", "jc-asana-html", "jc-visual-philosophy", "jc-generative-art",
    "jc-brand-discovery", "jc-landing-page", "jc-artifact-builder", "jc-mcp-builder", "mice-dashboard",
    "mice-weekly-performance",
}

# (정규식, 사유, 심각도) — 본문 줄 단위. 이력 문맥이면 면제.
LINE_RULES = [
    (re.compile(r"실행\s*전\s*\(?\s*(jc-prompt-builder)?\s*\)?\s*브리프"), "폐지된 '실행 전 브리프' 게이트", "ERROR"),
    (re.compile(r"\[A\]\s*/?\s*\[B\]|\[B\]\s*/?\s*\[C\]|범위\s*\[[ABC]\]"), "폐지된 [A]/[B]/[C] 범위 게이트", "ERROR"),
    (re.compile(r"(?<![0-9A-Za-z.])\d턴"), "폐지된 'N턴' 분할 표기 → 기획안 1회 확인 → 빌드 → 검수", "ERROR"),
    (re.compile(r"claude-(?:opus|sonnet)-4|claude-3[-.]|\b(?:Opus|Sonnet)\s*4(?:\.\d+)?\b"), "구 모델 ID/명칭 → Opus 5.5 / Sonnet 5.5 / Haiku 4.5 / Fable 5.1", "ERROR"),
    (re.compile(r"리더(?!십)|팀리드"), "호칭 '리더'·'팀리드' → '팀장'", "ERROR"),
    (re.compile(r"(?<![0-9A-Fa-f])(?:0A2540|2962FF)(?![0-9A-Fa-f])", re.I), "구 jc 시그니처 HEX 하드코딩 → 리멤버 토큰(jc-design-system)", "ERROR"),
    (re.compile(r"/mnt/skills|/mnt/user-data"), "claude.ai 샌드박스 경로 — Windows Code에서 무효", "ERROR"),
]
HISTORY_MARKERS = ("변경 이력", "변경이력", "흡수", "구 ", "폐지", "폐합", "아카이브", "이관", "legacy", "금지",
                   "금칙", "_archive", "별칭", "alias", "잔재", "교체", "→", "삭제", "정정")
HISTORY_HEADINGS = ("변경 이력", "변경이력", "이력", "legacy", "아카이브", "별칭", "하위호환", "changelog", "history")
SKILL_TOKEN = re.compile(r"(?<![A-Za-z0-9_/.-])((?:jc|mice)-[a-z][a-z0-9-]*[a-z0-9])(?![A-Za-z0-9_:-]|\.(?:md|py|json|html|css|js|xlsx|pptx|docx)\b)")
MD_LINK = re.compile(r"\]\(([^)\s]+)\)")
TICK_PATH = re.compile(r"`((?:(?:jc|mice|pt)-[a-z0-9-]+/)?(?:references|scripts|assets)/[^`\s]+?\.(?:md|py|json|png|txt|template))`")
SELF_EXEMPT = {"lint_skills.py"}
TEXT_SUFFIX = {".md", ".py", ".js", ".html", ".css", ".json", ".txt", ".template", ".sh"}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return {}, text
    fm, body = {}, text[m.end():]
    cur = None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if km:
            cur = km.group(1); fm[cur] = km.group(2).strip().strip('"').strip("'")
        elif cur and line.startswith((" ", "\t", "-")):
            fm[cur] = (fm[cur] + "\n" + line.strip()).strip()
    return fm, body


def _history_line(line: str, heading: str) -> bool:
    if any(h in heading.lower() for h in HISTORY_HEADINGS):
        return True
    return any(h in line for h in HISTORY_MARKERS)


def _check_path(target: str, f: Path, d: Path, root: Path) -> bool:
    """True = 실재(또는 검사 불가). 자리표시자·URL·앵커는 검사하지 않는다."""
    if any(c in target for c in "<>{}*|$") or target.startswith(("http", "#", "mailto:", "~", "/")):
        return True
    target = target.split("#")[0]
    if not target:
        return True
    m = re.match(r"((?:jc|mice|pt)-[a-z0-9-]+)/(.*)", target)
    if m and not target.startswith(("references/", "scripts/", "assets/")):
        sk = root / m.group(1)
        return (not sk.is_dir()) or (sk / m.group(2)).exists()
    return (f.parent / target).exists() or (d / target).exists()


def lint_skill(d: Path, issues: list, known: set | None = None) -> None:
    name = d.name
    root = d.parent
    known = set(known or set()) | LIVE | FIXTURES
    md = d / "SKILL.md"
    if not md.is_file():
        issues.append(("ERROR", name, "SKILL.md 없음")); return
    text = md.read_text(encoding="utf-8", errors="replace")
    fm, _ = parse_frontmatter(text)
    if not fm:
        issues.append(("ERROR", name, "프론트매터 없음")); return
    if fm.get("name") != name:
        issues.append(("ERROR", name, f"name '{fm.get('name')}' ≠ 디렉터리명"))
    desc = fm.get("description", "")
    if not desc:
        issues.append(("ERROR", name, "description 비어 있음"))
    elif len(desc) > DESC_MAX:
        issues.append(("ERROR", name, f"description {len(desc)}자 > {DESC_MAX}"))
    if not fm.get("version"):
        issues.append(("WARN", name, "version 없음"))
    lic = fm.get("license", "")
    if "LICENSE.txt" in lic and not (d / "LICENSE.txt").is_file():
        issues.append(("WARN", name, "license가 LICENSE.txt를 가리키나 파일 없음"))
    # YAML plain scalar 함정: ' #'는 주석 시작, ': '는 매핑으로 오인 → description 절단
    raw_desc = re.search(r"^description:\s*(.*)$", text, re.M)
    if raw_desc and not raw_desc.group(1).startswith(('"', "'")):
        if " #" in raw_desc.group(1):
            issues.append(("ERROR", name, "description에 ' #' — YAML 주석으로 절단됨 (따옴표로 감싸거나 # 제거)"))
        if ": " in raw_desc.group(1):
            issues.append(("ERROR", name, "description에 ': ' — YAML 매핑으로 오인 (따옴표로 감싸거나 제거)"))
    for k in fm:
        if k not in ALLOWED_FIELDS:
            issues.append(("WARN", name, f"업로드 비허용 프론트매터 필드 '{k}'"))
    for rx, why, _lvl in LINE_RULES:
        if rx.search(desc):
            issues.append(("ERROR", name, f"description 금지 표현 — {why}"))
    for a in sorted(ARCHIVED):
        if a != name and re.search(rf"(?<![A-Za-z0-9_-]){re.escape(a)}(?![A-Za-z0-9_-])", desc):
            issues.append(("ERROR", name, f"description이 폐합 스킬 '{a}' 참조"))
    nlines = text.count("\n") + 1
    if nlines > SKILL_MAX_LINES:
        issues.append(("WARN", name, f"SKILL.md {nlines}줄 > {SKILL_MAX_LINES}"))

    for f in sorted(d.rglob("*")):
        if not f.is_file() or "__pycache__" in f.parts or f.name in SELF_EXEMPT:
            continue
        rel = f.relative_to(d).as_posix()
        if f.suffix not in TEXT_SUFFIX or rel == "LICENSE.txt":
            continue
        try:
            t = f.read_text(encoding="utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            continue
        heading = ""
        in_fm = rel == "SKILL.md"
        for i, line in enumerate(t.splitlines(), 1):
            if in_fm:
                if i > 1 and line.strip() == "---":
                    in_fm = False
                continue
            if f.suffix == ".md" and line.startswith("#"):
                heading = line
            hist = _history_line(line, heading)
            for rx, why, lvl in LINE_RULES:
                if rx.search(line) and not hist:
                    issues.append((lvl, name, f"{rel}:{i} {why}"))
            for tok in SKILL_TOKEN.findall(line):
                if tok == name:
                    continue
                if tok in ARCHIVED:
                    if not hist:
                        issues.append(("ERROR", name, f"{rel}:{i} 폐합 스킬 '{tok}' 참조 → 라이브 스킬로 돌리거나 삭제"))
                elif tok not in known and not hist:
                    issues.append(("WARN", name, f"{rel}:{i} 없는 스킬 '{tok}' 참조"))
            if f.suffix == ".md":
                for tgt in MD_LINK.findall(line) + TICK_PATH.findall(line):
                    if not _check_path(tgt, f, d, root):
                        issues.append(("WARN", name, f"{rel}:{i} 깨진 상대경로 '{tgt}'"))
        if f.suffix == ".py":
            try:
                py_compile.compile(str(f), cfile=str(Path(tempfile.gettempdir()) / "lint_skills_tmp.pyc"), doraise=True)
            except Exception as e:  # noqa: BLE001
                issues.append(("ERROR", name, f"{rel} 컴파일 실패: {e}"))


def collect(paths: list, only: set | None, excl: set) -> list:
    dirs: list = []
    if paths:
        for p in paths:
            pp = Path(p).expanduser().resolve()
            if (pp / "SKILL.md").is_file():
                dirs.append(pp)
            elif pp.is_dir():
                dirs += [c for c in sorted(pp.iterdir()) if (c / "SKILL.md").is_file() and not c.name.startswith(("_", "."))]
    elif SKILLS.is_dir():
        dirs = [c for c in sorted(SKILLS.iterdir()) if c.is_dir() and not c.name.startswith(("_", "."))]
    return [c for c in dirs if (only is None or c.name in only) and c.name not in excl]


def run(dirs: list, strict: bool, quiet: bool = False) -> tuple:
    issues: list = []
    for d in dirs:
        siblings = {c.name for c in d.parent.iterdir() if (c / "SKILL.md").is_file()}
        lint_skill(d, issues, siblings - ARCHIVED)
    errs = [i for i in issues if i[0] == "ERROR"]; warns = [i for i in issues if i[0] == "WARN"]
    bad = bool(errs) or (strict and bool(warns))
    if not quiet:
        print(f"lint_skills — {len(dirs)} skills · ERROR {len(errs)} · WARN {len(warns)}")
        for lvl, name, msg in issues:
            print(f"  {lvl:5} {name:22} {msg}")
        print("FAIL" if bad else "PASS")
    return (1 if bad else 0), issues


def self_test() -> int:
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        good = root / "jc-good"; (good / "references").mkdir(parents=True)
        (good / "references" / "a.md").write_text("# A\n본문\n", encoding="utf-8")
        (good / "SKILL.md").write_text(
            '---\nname: jc-good\ndescription: 다음 상황에서 반드시 이 스킬을 사용할 것 — 테스트. 검증은 jc-redteam.\nversion: "v1.0.0"\n---\n'
            "# 좋은 스킬\n팀장이 확인한다. 리더십 교육은 예외. 모델은 Opus 5.5 / Sonnet 5.5 / Haiku 4.5(claude-haiku-4-5-20251001).\n"
            "상세는 `references/a.md`, 디자인은 jc-design-system.\n\n## 변경 이력\n- v1.0.0: jc-orchestrator 흡수, 3턴 분할 삭제, 리더 표기 정리.\n",
            encoding="utf-8")
        bad = root / "jc-bad"; bad.mkdir()
        (bad / "SKILL.md").write_text(
            '---\nname: jc-bad\ndescription: 제안서는 mice-proposal로. 실행 전 jc-prompt-builder 브리프를 거친다.\nversion: "v1.0.0"\n---\n'
            "# 나쁜 스킬\n작업은 3턴으로 나눈다.\n리더에게 보고한다.\n모델 claude-opus-4-8 사용, Sonnet 4.6 폴백.\n"
            "헤더 색 #0A2540, 강조 2962FF.\n대시보드는 jc-asana-html.\n보조는 jc-nonexistent-skill.\n상세 `references/missing.md`.\n",
            encoding="utf-8")
        (bad / "x.py").write_text("def broken(:\n", encoding="utf-8")
        rc_good, iss_good = run([good], strict=True, quiet=True)
        rc_bad, iss_bad = run([bad], strict=False, quiet=True)
        msgs = " | ".join(m for _, _, m in iss_bad)
        cases = [
            ("clean 스킬 strict PASS", rc_good == 0 and not iss_good),
            ("위반 스킬 FAIL", rc_bad == 1),
            ("description 폐합 스킬", "description이 폐합 스킬 'mice-proposal'" in msgs),
            ("description 브리프 게이트", "description 금지 표현" in msgs),
            ("N턴", "'N턴'" in msgs),
            ("리더", "'리더'" in msgs),
            ("구 모델 ID", "구 모델" in msgs),
            ("구 시그니처 HEX", "구 jc 시그니처 HEX" in msgs),
            ("본문 폐합 스킬", "폐합 스킬 'jc-asana-html'" in msgs),
            ("없는 스킬", "없는 스킬 'jc-nonexistent-skill'" in msgs),
            ("깨진 경로", "references/missing.md" in msgs),
            ("py 컴파일", "x.py 컴파일 실패" in msgs),
        ]
        for label, passed in cases:
            print(f"  {'OK ' if passed else 'FAIL'} {label}")
            ok = ok and passed
        if not ok:
            print("  good issues:", iss_good)
            print("  bad issues :", msgs)
    print("lint_skills self-test", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="jc·mice 스킬 라이브러리 정합 검사")
    ap.add_argument("paths", nargs="*", help="스킬 폴더 또는 스킬 모음 폴더 (생략 시 정본 레포 .claude/skills)")
    ap.add_argument("--only", help="쉼표 구분 스킬명")
    ap.add_argument("--exclude", default="", help="쉼표 구분 제외 스킬명")
    ap.add_argument("--strict", action="store_true", help="WARN도 실패 처리")
    ap.add_argument("--self-test", action="store_true", help="자가 테스트 실행")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    only = set(a.only.split(",")) if a.only else None
    excl = set(x for x in a.exclude.split(",") if x)
    dirs = collect(a.paths, only, excl)
    if not dirs:
        print("검사할 스킬 폴더가 없습니다 (경로 또는 레포 .claude/skills 확인)")
        return 1
    rc, _ = run(dirs, a.strict)
    return rc


if __name__ == "__main__":
    sys.exit(main())
