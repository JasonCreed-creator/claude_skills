#!/usr/bin/env python3
"""description-registry.md 재생성 스크립트 (jc-prompt-builder)

스킬 라이브러리 디렉터리에서 각 스킬의 SKILL.md frontmatter(name·version·description)를
실측 수집해 references/description-registry.md 스냅숏을 생성한다.
routing-map.md의 큐레이션 매핑 테이블은 사람이 유지한다 — 이 스크립트는 그 근거가 되는
실측 원본만 만든다. 재생성 후 registry diff를 보고 routing-map §2·§3 행을 갱신할 것.

사용:
    python scripts/build_routing_map.py --skills-dir <스킬 라이브러리 루트> [--draft] [--label <기준 설명>]

RULE-NO-COMPANY / 이식성: 경로를 하드코딩하지 않는다 — 디렉터리는 인자로만 받는다.
stdlib only.
"""

import argparse
import datetime
import re
import sys
from pathlib import Path

# 공용 스킬(라우팅 대상 아님) + 라우터 자신(상시 레이어 — 라우팅 대상 아님)
EXCLUDE = {
    "consolidate-memory", "docx", "pdf", "pptx", "xlsx", "schedule", "setup-cowork",
    "jc-prompt-builder",
}

# EXCLUDE 차감 후 이보다 적게 수집되면 루트 오지정으로 간주 (현행 라우팅 대상 22종)
MIN_EXPECTED = 10

BLOCK_SCALAR = ("|", ">", "|-", ">-", "|+", ">+")


def _unquote(value: str) -> str:
    """값 전체가 동일 따옴표 쌍으로 감싸져 있을 때만 양끝 1글자씩 제거한다."""
    v = value.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
        return v[1:-1]
    return v


def parse_frontmatter(text: str) -> dict:
    """SKILL.md 앞머리의 YAML frontmatter에서 name/version/description만 뽑는다.

    외부 YAML 파서 없이 처리한다(stdlib only). 지원: 단일 물리 줄 값(하우스 표준),
    들여쓰기 연속 줄, 블록 스칼라 지시자(>·| 계열), 따옴표 값, 주석 줄 무시.
    """
    text = text.lstrip("﻿")  # BOM 방어 (utf-8-sig 읽기와 이중 안전망)
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.DOTALL)
    if not m:
        return {}
    raw = {}
    current_key = None
    block_mode = False  # 현재 키가 블록 스칼라(>·|)인지 — 블록 안에서는 #·- 줄도 콘텐츠다
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if km:
            current_key = km.group(1)
            val = km.group(2).strip()
            # 블록 스칼라 지시자는 값이 아니다 — 연속 줄만 조립
            block_mode = val in BLOCK_SCALAR
            raw[current_key] = "" if block_mode else val
        elif current_key and line[:1] in (" ", "\t") and line.strip():
            # 들여쓰기로 시작하는 줄만 연속 줄로 인정
            stripped = line.strip()
            if not block_mode and (stripped.startswith("#") or stripped.startswith("- ")):
                # 일반 값에서 들여쓰기 주석·리스트 항목은 값으로 삼키지 않는다
                continue
            raw[current_key] = (raw[current_key] + " " + stripped).strip()
        elif line.lstrip().startswith("#"):
            continue  # 최상위 주석 줄
    return {k: _unquote(v) for k, v in raw.items()}


def collect(skills_dir: Path) -> list:
    rows = []
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        # Windows에서는 glob 결과가 패턴의 리터럴 표기("SKILL.md")를 그대로 쓰므로
        # resolve()로 디스크 실명을 얻어 대소문자 이형(skill.md 등)을 걸러낸다
        if skill_md.resolve().name != "SKILL.md":
            print(f"경고: 파일명 대소문자 이형 제외 - {skill_md.resolve()}", file=sys.stderr)
            continue
        name = skill_md.parent.name
        if name in EXCLUDE:
            continue
        fm = parse_frontmatter(skill_md.read_text(encoding="utf-8-sig"))
        if not fm:
            print(f"경고: frontmatter 미검출 - {skill_md}", file=sys.stderr)
        rows.append({
            "dir": name,
            "name": fm.get("name", "(누락)"),
            "version": fm.get("version", ""),
            "description": fm.get("description", "(누락)"),
        })
    return rows


def render(rows: list, source: str, draft: bool, label: str) -> str:
    today = datetime.date.today().isoformat()
    status = "**DRAFT** — 확정 description 반영 전 임시본. 재생성 필요." if draft else "확정본"
    out = [
        "# Description Registry — 스킬 description 실측 스냅숏",
        "",
        f"> 생성: {today} · 상태: {status}",
        f"> 기준: {label}",
        f"> 소스: `{source}` ({len(rows)}종)",
        "> 생성기: `scripts/build_routing_map.py` — 손으로 수정하지 말 것. description 변경 시 재실행.",
        "",
        "본 문서는 `routing-map.md` 매핑 테이블의 실측 근거다. 재생성 후 이전 버전과 diff하여",
        "트리거·경계가 바뀐 스킬이 있으면 routing-map의 해당 행을 갱신한다.",
        "",
        "---",
        "",
    ]
    for r in rows:
        flags = []
        if r["dir"] != r["name"]:
            flags.append(f"⚠ 디렉터리명({r['dir']})≠name({r['name']})")
        if not r["version"]:
            flags.append("⚠ version frontmatter 누락")
        head = f"## {r['dir']} ({r['version']})" if r["version"] else f"## {r['dir']}"
        flag_str = " · ".join(flags)
        out.append(head + (f" — {flag_str}" if flag_str else ""))
        out.append("")
        out.append(r["description"])
        out.append("")
    return "\n".join(out)


def main() -> int:
    # cp949 콘솔에서 한글·특수문자 메시지 모지바케 방어
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser(description="스킬 description 실측 수집 → description-registry.md 생성")
    ap.add_argument("--skills-dir", required=True, help="스킬 라이브러리 루트 (각 스킬이 직속 하위 폴더)")
    ap.add_argument("--out", default=None, help="출력 경로 (기본: 이 스킬의 references/description-registry.md)")
    ap.add_argument("--draft", action="store_true", help="DRAFT 표기 (확정 description 반영 전)")
    ap.add_argument("--label", default="frontmatter 실측", help="기준 설명 한 줄 (예: 'Phase 4 확정본 기준')")
    ap.add_argument("--source-label", default=None,
                    help="문서에 기록할 소스 표기 (기본: --skills-dir 경로). 미러 복사본으로 측정할 때 원 출처를 명기하는 용도")
    ap.add_argument("--min-expected", type=int, default=MIN_EXPECTED,
                    help=f"수집 하한 가드 — 이보다 적으면 루트 오지정으로 보고 중단 (기본 {MIN_EXPECTED}, 0=해제)")
    args = ap.parse_args()

    skills_dir = Path(args.skills_dir)
    if not skills_dir.is_dir():
        print(f"오류: 디렉터리 아님 - {skills_dir}", file=sys.stderr)
        return 1

    rows = collect(skills_dir)
    if not rows:
        print(f"오류: {skills_dir} 아래에서 SKILL.md를 찾지 못함", file=sys.stderr)
        return 1
    if args.min_expected and len(rows) < args.min_expected:
        print(
            f"오류: 수집 {len(rows)}종 < 하한 {args.min_expected}종 - 스킬 라이브러리 루트가 맞는지 확인하라"
            f" (각 스킬이 직속 하위 폴더여야 함). 의도된 소량 실행이면 --min-expected 0",
            file=sys.stderr,
        )
        return 1

    out_path = Path(args.out) if args.out else Path(__file__).resolve().parents[1] / "references" / "description-registry.md"
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"오류: 출력 경로 생성 불가 - {out_path} ({e})", file=sys.stderr)
        return 1
    source = args.source_label if args.source_label else str(skills_dir)
    out_path.write_text(render(rows, source, args.draft, args.label), encoding="utf-8")
    print(f"생성: {out_path} ({len(rows)}종, draft={args.draft})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
