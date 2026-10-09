#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""jc-pptx check_deck v2 — 안티패턴 자동 검수 CLI.

사용: python check_deck.py <deck.pptx> [--theme remember|legacy-jc|dark-premium|light-vivid] [--no-theme]
검수 항목 (references/design-language.md §7):
  A2 테마 토큰 외 색 / A3 이미지·텍스처 0장 / A4 명사구 제목 / A5 동일 위계 /
  A6 깨알 표(<9pt) / A7 네비게이션 누락 / A8 CTA 없는 클로징 / A9 다크 슬라이드 30% 초과
(A1 '박스 나열'은 A5 위계 검사가 근사 탐지)
기본 테마는 remember. Windows·POSIX 경로 모두 동작.
"""
import argparse
import os
import re
import sys
import zipfile
from collections import Counter
from dataclasses import fields

NEUTRALS = {"FFFFFF", "000000", "E8641F"}  # 흰/검 + 섹션 디바이더 그라디언트 시작색
ASSERTIVE_END = re.compile(r"(다|니다|까|요|죠|가|로|으로|것)\s*[.?!]?\s*$|[.?!'’”]\s*$")
CTA_HINT = re.compile(r"[?？]|시작|문의|연락|제안|선택|함께|다음 단계|잔여|마감|킥오프|드립니다")
EMU_IN = 914400


def theme_tokens(name):
    """테마의 모든 색 토큰 집합. 실패 시 None(A2 스킵)."""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import deck_kit
        t = deck_kit.get_theme(name)
        vals = set()
        for f in fields(t):
            v = getattr(t, f.name)
            if isinstance(v, str) and re.fullmatch(r"[0-9A-Fa-f]{6}", v):
                vals.add(v.upper())
            elif isinstance(v, list):
                vals |= {str(x).lstrip("#").upper() for x in v if re.fullmatch(r"#?[0-9A-Fa-f]{6}", str(x))}
        return vals | NEUTRALS
    except Exception as e:  # noqa: BLE001
        print(f"(테마 로드 실패 — A2 스킵: {e})")
        return None


def is_dark_slide(xml, tokens_dark):
    m = re.search(r"<p:bg>.*?<a:srgbClr val=\"([0-9A-Fa-f]{6})\"", xml, re.S)
    return bool(m and m.group(1).upper() in tokens_dark)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck"); ap.add_argument("--theme", default="remember"); ap.add_argument("--no-theme", action="store_true")
    a = ap.parse_args()
    z = zipfile.ZipFile(a.deck)
    slides = sorted([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
                    key=lambda n: int(re.search(r"(\d+)", n).group(1)))
    media = [n for n in z.namelist() if n.startswith("ppt/media/")]
    tokens = None if a.no_theme else theme_tokens(a.theme)
    dark_bgs = {"141210", "211E1A", "16140F", "332F29"}
    issues, off_colors, dark_count = [], Counter(), 0

    for idx, sn in enumerate(slides, 1):
        xml = z.read(sn).decode("utf-8", "ignore")
        texts = re.findall(r"<a:t>([^<]*)</a:t>", xml)
        if is_dark_slide(xml, dark_bgs):
            dark_count += 1
        # A2 테마 외 색
        if tokens is not None:
            for c in set(re.findall(r'<a:srgbClr val="([0-9A-Fa-f]{6})"', xml)):
                if c.upper() not in tokens:
                    off_colors[c.upper()] += 1
        # A4 명사구 제목 — 본문 슬라이드의 최대 폰트 텍스트. 문장 종결·인용 강조어구·쉼표 리듬은 통과
        m = re.findall(r'sz="(\d{4,})"[^>]*/>.*?<a:t>([^<]+)</a:t>', xml, re.S)
        bigs = [(int(s) / 100, t.strip()) for s, t in m if int(s) >= 2400]
        if bigs and idx not in (1, len(slides)):
            title = max(bigs, key=lambda x: x[0])[1]
            if (len(title) > 12 and not ASSERTIVE_END.search(title) and "'" not in title and "," not in title
                    and not re.match(r"^\d|^SECTION|^[IVX]+\.|^목차|^CONTENTS", title)):
                issues.append(f"[A4] s{idx}: 명사구 제목 의심 → '{title[:30]}'")
        # A6 깨알 폰트
        tiny = [int(s) for s in re.findall(r'sz="(\d{3,4})"', xml) if int(s) < 900]
        if len(tiny) > 12:
            issues.append(f"[A6] s{idx}: 9pt 미만 텍스트 {len(tiny)}런 — 깨알 표 의심")
        # A7 네비게이션 — 커버(1)·클로징(마지막) 제외
        off = [int(v) for v in re.findall(r'<a:off x="\d+" y="(\d+)"', xml)]
        has_footer = any(v > int(6.9 * EMU_IN) for v in off)
        has_eyebrow = any(v < int(0.75 * EMU_IN) for v in off)
        if idx not in (1, len(slides)) and len(texts) > 4 and not (has_footer or has_eyebrow):
            issues.append(f"[A7] s{idx}: 네비게이션(아이브로우/푸터) 누락 의심")
        # A5 위계 균일
        exts = re.findall(r'<a:ext cx="(\d+)" cy="(\d+)"', xml)
        hs = [cy for _, cy in exts]
        if len(hs) >= 6 and len(set(hs)) == 1:
            issues.append(f"[A5] s{idx}: 모든 도형 동일 크기 — 위계 차등 없음")
    if not media:
        issues.append("[A3] 데크 전체 이미지·텍스처 0장")
    if tokens is not None and off_colors:
        top = ", ".join(f"#{c}({n})" for c, n in off_colors.most_common(8))
        issues.append(f"[A2] 테마 토큰 외 색 사용: {top}")
    last = z.read(slides[-1]).decode("utf-8", "ignore")
    last_text = " ".join(re.findall(r"<a:t>([^<]*)</a:t>", last))
    if not CTA_HINT.search(last_text):
        issues.append(f"[A8] 클로징에 CTA 신호 없음 → '{last_text[:40]}'")
    if len(slides) >= 10 and dark_count / len(slides) > 0.30:  # 짧은 스모크 덱은 제외
        issues.append(f"[A9] 다크 슬라이드 {dark_count}/{len(slides)} = {dark_count/len(slides):.0%} — 30% 초과")

    print(f"jc-pptx check_deck — {a.deck} ({len(slides)} slides · 다크 {dark_count} · 미디어 {len(media)})")
    if issues:
        print(f"FAIL — {len(issues)}건")
        for i in issues:
            print(" ", i)
        sys.exit(1)
    print("PASS — 안티패턴 0건")


if __name__ == "__main__":
    main()
