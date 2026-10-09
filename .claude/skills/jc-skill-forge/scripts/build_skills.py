#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_skills — 라이브 스킬을 claude.ai 업로드용 .skill(zip)로 패키징 (zip 명령 없는 Windows 대응).

출력: <repo>/dist/skills/<name>.skill  (zip 루트에 <name>/ 폴더 포함)
사용: python build_skills.py [--only a,b] [--exclude x] [--include-estimate] [--src <스킬 모음 폴더>] [--out <출력 폴더>]
      python build_skills.py --self-test
기본 제외: _archive/, mice-estimate(사용자 직접 관리), __pycache__, *.pyc, .DS_Store
형식: ZIP 하나만(.skill, 내부 <name>/SKILL.md). tar.gz·7z 등 다른 압축은 claude.ai가 받지 않으므로 만들지 않는다.
빌드는 소스 반영일 뿐 배포가 아니다 — claude.ai 업로드는 사용자가 한다.
"""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
SKILLS = REPO / ".claude" / "skills"
OUT = REPO / "dist" / "skills"
DEFAULT_EXCLUDE = {"mice-estimate"}
SKIP_NAMES = {"__pycache__", ".DS_Store"}


def build(d: Path, out_dir: Path | None = None) -> Path:
    out_dir = out_dir or OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{d.name}.skill"
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(d.rglob("*")):
            if any(p in SKIP_NAMES for p in f.parts) or f.suffix == ".pyc":
                continue
            if f.is_file():
                z.write(f, f"{d.name}/{f.relative_to(d).as_posix()}")
    return out


def self_test() -> int:
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "src" / "jc-demo"
        (src / "scripts" / "__pycache__").mkdir(parents=True)
        (src / "SKILL.md").write_text("---\nname: jc-demo\n---\n", encoding="utf-8")
        (src / "scripts" / "a.py").write_text("print(1)\n", encoding="utf-8")
        (src / "scripts" / "__pycache__" / "a.cpython-311.pyc").write_bytes(b"x")
        (src / ".DS_Store").write_bytes(b"x")
        out = build(src, Path(tmp) / "out")
        names = zipfile.ZipFile(out).namelist() if zipfile.is_zipfile(out) else []
        cases = [
            ("확장자 .skill", out.suffix == ".skill"),
            ("ZIP 형식", zipfile.is_zipfile(out)),
            ("루트 <name>/SKILL.md", "jc-demo/SKILL.md" in names),
            ("scripts 포함", "jc-demo/scripts/a.py" in names),
            ("__pycache__·.pyc 제외", not any("__pycache__" in n or n.endswith(".pyc") for n in names)),
            (".DS_Store 제외", not any(n.endswith(".DS_Store") for n in names)),
            ("재빌드 덮어쓰기", build(src, Path(tmp) / "out") == out and zipfile.is_zipfile(out)),
        ]
        for label, passed in cases:
            print(f"  {'OK ' if passed else 'FAIL'} {label}")
            ok = ok and passed
    print("build_skills self-test", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=".skill(ZIP) 패키징 — tar.gz 등 다른 형식은 만들지 않는다")
    ap.add_argument("--only"); ap.add_argument("--exclude", default=""); ap.add_argument("--include-estimate", action="store_true")
    ap.add_argument("--src", help="스킬 모음 폴더 (기본: 정본 레포 .claude/skills)")
    ap.add_argument("--out", help="출력 폴더 (기본: 레포 dist/skills)")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    src_root = Path(a.src).resolve() if a.src else SKILLS
    out_dir = Path(a.out).resolve() if a.out else OUT
    only = set(a.only.split(",")) if a.only else None
    excl = set(x for x in a.exclude.split(",") if x) | (set() if a.include_estimate else DEFAULT_EXCLUDE)
    dirs = [d for d in sorted(src_root.iterdir()) if d.is_dir() and not d.name.startswith(("_", ".")) and (d / "SKILL.md").is_file()]
    dirs = [d for d in dirs if (only is None or d.name in only) and d.name not in excl]
    total = 0
    for d in dirs:
        out = build(d, out_dir); sz = out.stat().st_size; total += sz
        print(f"  OK {out.name:34} {sz/1024:8.1f} KB")
    print(f"완료 → {out_dir}  ({len(dirs)} skills · {total/1024/1024:.1f} MB)")
    print("빌드 = 소스 반영일 뿐 배포 아님. claude.ai 업로드는 기획자님 몫:")
    print("  claude.ai → Settings → Capabilities(Skills) → 동명 구스킬 삭제 → .skill 업로드 (ZIP만, tar.gz 금지)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
