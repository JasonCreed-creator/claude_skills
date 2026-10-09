#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""install_local — 정본 레포의 라이브 스킬을 ~/.claude/skills/<name>에 설치(정션) 또는 해제.

Claude Code는 ~/.claude/skills/<name>을 동명 synced 스킬보다 우선 로드한다. Cowork에는 영향 없음(claude.ai만).
사용: python install_local.py [--only a,b] [--exclude x] [--include-estimate] [--copy] [--uninstall]
      python install_local.py --self-test   # 임시 폴더에 복사 설치·해제 검증
정션(mklink /J)은 관리자 권한 없이 만들어지며 레포 편집이 즉시 반영된다. 실패 시 --copy.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
SKILLS = REPO / ".claude" / "skills"
DEST = Path.home() / ".claude" / "skills"
DEFAULT_EXCLUDE = {"mice-estimate"}


def is_link(p: Path) -> bool:
    try:
        return p.is_symlink() or (p.exists() and os.stat(p, follow_symlinks=False).st_file_attributes & 0x400 != 0)
    except Exception:
        return p.is_symlink()


def remove(p: Path) -> None:
    if not p.exists() and not p.is_symlink():
        return
    if is_link(p):
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "rmdir", str(p)], check=False, capture_output=True)
        else:
            p.unlink()
    else:
        shutil.rmtree(p)


def junction(src: Path, dst: Path) -> bool:
    if os.name != "nt":
        dst.symlink_to(src, target_is_directory=True); return True
    r = subprocess.run(["cmd", "/c", "mklink", "/J", str(dst), str(src)], capture_output=True)
    return r.returncode == 0 and dst.exists()


def install(d: Path, dest_root: Path, copy: bool) -> str:
    dst = dest_root / d.name
    remove(dst)
    if not copy and junction(d, dst):
        return "junction"
    shutil.copytree(d, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return "copied"


def self_test() -> int:
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "src" / "jc-demo"
        (src / "__pycache__").mkdir(parents=True)
        (src / "SKILL.md").write_text("---\nname: jc-demo\n---\n", encoding="utf-8")
        (src / "__pycache__" / "x.pyc").write_bytes(b"x")
        dest = Path(tmp) / "dest"; dest.mkdir()
        mode = install(src, dest, copy=True)
        cases = [
            ("복사 설치", mode == "copied" and (dest / "jc-demo" / "SKILL.md").is_file()),
            ("__pycache__ 제외", not (dest / "jc-demo" / "__pycache__").exists()),
            ("재설치 덮어쓰기", install(src, dest, copy=True) == "copied"),
        ]
        remove(dest / "jc-demo")
        cases.append(("해제", not (dest / "jc-demo").exists()))
        try:
            jm = install(src, dest, copy=False)
            cases.append((f"링크 설치({jm})", (dest / "jc-demo" / "SKILL.md").is_file()))
            remove(dest / "jc-demo")
            cases.append(("링크 해제 시 원본 보존", (src / "SKILL.md").is_file() and not (dest / "jc-demo").exists()))
        except OSError as e:
            print(f"  SKIP 링크 설치 (권한: {e})")
        for label, passed in cases:
            print(f"  {'OK ' if passed else 'FAIL'} {label}")
            ok = ok and passed
    print("install_local self-test", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--only"); ap.add_argument("--exclude", default=""); ap.add_argument("--include-estimate", action="store_true")
    ap.add_argument("--copy", action="store_true"); ap.add_argument("--uninstall", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    only = set(a.only.split(",")) if a.only else None
    excl = set(x for x in a.exclude.split(",") if x) | (set() if a.include_estimate else DEFAULT_EXCLUDE)
    dirs = [d for d in sorted(SKILLS.iterdir()) if d.is_dir() and not d.name.startswith(("_", ".")) and (d / "SKILL.md").is_file()]
    dirs = [d for d in dirs if (only is None or d.name in only) and d.name not in excl]
    DEST.mkdir(parents=True, exist_ok=True)
    for d in dirs:
        dst = DEST / d.name
        if a.uninstall:
            remove(dst); print(f"  removed {dst}"); continue
        mode = install(d, DEST, a.copy)
        print(f"  {mode:8} {dst}" + (f" -> {d}" if mode == "junction" else ""))
    print(f"{'해제' if a.uninstall else '설치'} 완료 — {len(dirs)} skills · {DEST}")
    if not a.uninstall:
        print("새 Code 세션부터 로드됩니다. synced 동명 스킬은 '/anthropic-skills:<name>'로 남아 있으니 claude.ai에서 정리하세요.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
