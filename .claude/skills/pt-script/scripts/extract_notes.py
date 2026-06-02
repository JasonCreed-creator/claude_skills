#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_notes.py — PPTX speaker notes 자동 추출 (pt-script v2.0)

python-pptx 를 사용하여 .pptx 파일에서 슬라이드별 제목·본문 텍스트·
speaker notes·메타데이터를 추출하여 JSON 으로 출력한다.

mice-proposal v2.1.1 의 메타 노트 (■ 이미지 교체 안내 / ■ 폰트 안내)
는 자동 필터링하여 발표 베이스에서 제외한다.

Usage:
    python extract_notes.py input.pptx --out notes.json
    python extract_notes.py input.pptx --out notes.json --verbose

Output schema: references/notes-extraction.md §6 참조
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# UTF-8 stdout 표준 (jc-design-system 글로벌 룰)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


# ============================================================
# 메타 노트 필터링 패턴
# ============================================================

META_NOTE_PATTERNS = [
    r"^■\s*이미지\s*교체\s*안내",
    r"^■\s*폰트\s*안내",
    r"^■\s*PPTX\s*제작\s*안내",
    r"^\[META\]",
    r"^TODO[:：]",
    r"^FIXME[:：]",
]


def classify_notes(notes_text: str) -> str:
    """노트 텍스트를 speaker / meta / empty 로 분류."""
    if not notes_text or not notes_text.strip():
        return "empty"

    # 메타 패턴 매칭 시 메타 블록만 제거 후 재평가
    cleaned = remove_meta_blocks(notes_text)
    if cleaned.strip():
        return "speaker"
    return "meta"


def remove_meta_blocks(notes_text: str) -> str:
    """노트에서 메타 블록만 제거. 발표 노트 부분 반환.

    메타 블록 = '■ ...' 로 시작하는 줄부터 다음 빈 줄 또는 다음 '■' 까지.
    """
    if not notes_text:
        return ""

    lines = notes_text.split("\n")
    out: list[str] = []
    skip_block = False

    for line in lines:
        stripped = line.strip()
        # 메타 패턴 매칭 — 새 메타 블록 시작
        is_meta_header = any(re.match(p, stripped) for p in META_NOTE_PATTERNS)
        if is_meta_header:
            skip_block = True
            continue
        # 빈 줄 — 메타 블록 종료
        if skip_block and stripped == "":
            skip_block = False
            continue
        if not skip_block:
            out.append(line)

    return "\n".join(out).strip()


# ============================================================
# 슬라이드 유형 자동 추론
# ============================================================

def infer_slide_type(
    index: int, title: str, body_text: str, has_chart: bool, total_slides: int
) -> str:
    """슬라이드 유형 자동 추론. notes-extraction.md §6-3 룰."""
    # 위치 기반
    if index == 1:
        return "cover"
    if index == total_slides:
        return "thanks"

    # 제목 기반
    title_lower = (title or "").lower()
    if any(kw in title_lower for kw in ["목차", "agenda", "contents", "차례"]):
        return "agenda"
    if any(kw in title_lower for kw in ["감사", "thank", "마무리", "끝"]):
        return "thanks"
    if any(kw in title_lower for kw in ["배경", "현황", "이해", "분석", "context"]):
        return "background"
    if any(kw in title_lower for kw in ["전략", "제안", "솔루션", "어프로치", "approach"]):
        return "core_proposal"
    if any(kw in title_lower for kw in ["일정", "타임라인", "프로세스", "단계", "timeline", "process"]):
        return "process_timeline"
    if any(kw in title_lower for kw in ["실적", "사례", "레퍼런스", "포트폴리오", "reference", "portfolio"]):
        return "reference_case"

    # 차트 존재 시
    if has_chart:
        return "data_chart"

    return "generic"


# ============================================================
# PPTX 추출 메인 로직
# ============================================================

def extract_pptx_notes(pptx_path: str, verbose: bool = False) -> dict:
    """PPTX 파일에서 슬라이드별 데이터 추출.

    Returns:
        dict — notes-extraction.md §6 스키마 준수
    """
    try:
        from pptx import Presentation
        from pptx.util import Pt  # noqa: F401 (인지용)
    except ImportError as exc:
        raise RuntimeError(
            "python-pptx 가 설치되지 않았습니다. `pip install python-pptx` 실행."
        ) from exc

    path = Path(pptx_path)
    if not path.exists():
        raise FileNotFoundError(f"PPTX 파일을 찾을 수 없음: {pptx_path}")
    if path.suffix.lower() != ".pptx":
        raise ValueError(f"입력 파일이 .pptx 확장자가 아님: {pptx_path}")

    try:
        prs = Presentation(str(path))
    except Exception as exc:
        raise RuntimeError(f"PPTX 파싱 실패 (손상 가능성): {exc}") from exc

    slides_data: list[dict] = []
    total = len(prs.slides)

    for idx, slide in enumerate(prs.slides, start=1):
        title = ""
        body_parts: list[str] = []
        has_chart = False
        has_image = False
        has_table = False

        # 제목 추출
        try:
            if slide.shapes.title is not None and slide.shapes.title.has_text_frame:
                title = (slide.shapes.title.text or "").strip()
        except Exception:
            title = ""

        # 본문 텍스트 + 메타데이터 수집
        for shape in slide.shapes:
            try:
                # 차트
                if getattr(shape, "has_chart", False):
                    has_chart = True
                    continue
                # 표
                if getattr(shape, "has_table", False):
                    has_table = True
                    # 표 셀 텍스트도 수집
                    try:
                        for row in shape.table.rows:
                            for cell in row.cells:
                                cell_text = (cell.text or "").strip()
                                if cell_text and cell_text != title:
                                    body_parts.append(cell_text)
                    except Exception:
                        pass
                    continue
                # 이미지 (shape_type 13 = PICTURE)
                if hasattr(shape, "shape_type") and shape.shape_type == 13:
                    has_image = True
                    continue
                # 텍스트 도형 (제목 제외)
                if shape.has_text_frame:
                    text = (shape.text_frame.text or "").strip()
                    if text and text != title:
                        body_parts.append(text)
            except Exception:
                continue

        body_text = "\n".join(body_parts).strip()

        # speaker notes 추출
        raw_notes = ""
        try:
            if slide.has_notes_slide and slide.notes_slide.notes_text_frame is not None:
                raw_notes = (slide.notes_slide.notes_text_frame.text or "").strip()
        except Exception:
            raw_notes = ""

        # 메타 노트 필터링 + 분류
        notes_type = classify_notes(raw_notes)
        if notes_type == "speaker":
            cleaned_notes = remove_meta_blocks(raw_notes)
        elif notes_type == "meta":
            cleaned_notes = ""
        else:  # empty
            cleaned_notes = ""

        slide_type_hint = infer_slide_type(idx, title, body_text, has_chart, total)

        slide_data = {
            "index": idx,
            "title": title,
            "body_text": body_text,
            "notes": cleaned_notes,
            "notes_type": notes_type,
            "has_chart": has_chart,
            "has_image": has_image,
            "has_table": has_table,
            "slide_type_hint": slide_type_hint,
        }
        slides_data.append(slide_data)

        if verbose:
            print(
                f"  [{idx:02d}] type={slide_type_hint:<18s} notes={notes_type:<7s} "
                f"chart={has_chart} image={has_image} table={has_table} "
                f"title={title[:30]!r}",
                file=sys.stderr,
            )

    return {
        "source_pptx": path.name,
        "extracted_at": datetime.now().isoformat(),
        "slide_count": total,
        "slides": slides_data,
    }


# ============================================================
# CLI 진입점
# ============================================================

def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="PPTX speaker notes 자동 추출 (pt-script v2.0)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("pptx", help="입력 PPTX 파일 경로")
    parser.add_argument(
        "--out", "-o",
        default=None,
        help="출력 JSON 파일 경로 (미지정 시 stdout)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="상세 모드 (슬라이드별 메타데이터 stderr 출력)",
    )

    args = parser.parse_args(argv)

    try:
        result = extract_pptx_notes(args.pptx, verbose=args.verbose)
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 3
    except RuntimeError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 4

    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_json, encoding="utf-8")
        if args.verbose:
            print(f"[OK] 출력 완료 — {out_path} ({result['slide_count']} slides)", file=sys.stderr)
    else:
        print(output_json)

    return 0


if __name__ == "__main__":
    sys.exit(main())
