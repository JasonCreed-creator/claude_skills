#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""jc-pptx check_deck v3 — 안티패턴 + 제안서 어투 자동 검수 CLI.

사용:
  python check_deck.py <deck.pptx> [--theme remember|legacy-jc|dark-premium|light-vivid] [--no-theme]
                       [--voice deck|proposal]
  python check_deck.py --self-test
검수 항목 (references/design-language.md §7):
  A2 테마 토큰 외 색 / A3 이미지·텍스처 0장 / A4 명사구 제목 / A5 동일 위계 /
  A6 깨알 표(<9pt) / A7 네비게이션 누락 / A8 CTA 없는 클로징 / A9 다크 슬라이드 30% 초과
  (A1 '박스 나열'은 A5 위계 검사가 근사 탐지)
--voice proposal — 발주처 제안서 (references/proposal-voice.md §3-4 · §6):
  A4를 끈다(명사형 종결 주장 카피 '~제공'·'~구축'·'~설계'가 정상). 대신 헤드라인 어투를 검사한다.
  V1 주어 시작 / V2 피동 직역 / V3 '통해·통한·통하여' 슬라이드당 2회+ / V4 콜론·세미콜론·대시
  (D-/W-/D+ 상대 일정·시각·수치 범위는 예외) / V5 30자 초과(공백·{{변수}} 제외) /
  V6 한 주장(쉼표·가운뎃점 2개+, 천 단위 콤마 제외) / V7 질문형 헤드라인
  + 금칙 수식어(§6) 후보 출력 — 근거 동반 여부는 사람 판정, 실패 처리 안 함.
헤드라인 = 표지·클로징을 뺀 슬라이드에서 가장 큰 글자(24pt+) 텍스트 도형의, 그 크기 런을 문단 순서로 이은 문자열
(숫자·단위만인 KPI 도형은 건너뜀). 기본 테마는 remember. Windows·POSIX 경로 모두 동작.
"""
import argparse
import html
import os
import re
import sys
import tempfile
import zipfile
from collections import Counter
from dataclasses import fields

NEUTRALS = {"FFFFFF", "000000", "E8641F"}  # 흰/검 + 섹션 디바이더 그라디언트 시작색
ASSERTIVE_END = re.compile(r"(다|니다|까|요|죠|가|로|으로|것)\s*[.?!]?\s*$|[.?!'’”\"]\s*$")
CTA_HINT = re.compile(r"[?？]|시작|문의|연락|제안|선택|함께|다음 단계|잔여|마감|킥오프|드립니다")
EMU_IN = 914400
DARK_BGS = {"141210", "211E1A", "16140F", "332F29"}

# 헤드라인 추출 — 런의 rPr이 자식(solidFill·latin·ea)을 가진 deck_kit 형식과 자기닫힘 형식 모두
TXBODY = re.compile(r"<p:txBody>(.*?)</p:txBody>", re.S)
PARA = re.compile(r"<a:p(?:\s[^>]*)?>(.*?)</a:p>", re.S)
RUN = re.compile(r"<a:r>\s*(?:<a:rPr\b([^>]*?)(?:/>|>.*?</a:rPr>))?\s*<a:t>([^<]*)</a:t>", re.S)
NUMERIC_ONLY = re.compile(r"[\d\s,.\-+%~×x/:원명분개회배억만천건년월일장석사곳팀위점]+")

# 제안서 어투 (proposal-voice.md §3-4 · §1-2 · §6)
V1_SUBJECT = re.compile(r"^(?:우리는|우리가|우리의|당사는|당사가|당사의|저희는|저희가|본\s*제안사는|제안사는|리멤버는)(?:\s|$)")
V2_PASSIVE = re.compile(r"되어집니다|되어지[는며고]|하도록\s*설계되었|(?:할|될)\s*수\s*있도록.{0,20}?(?:구성|연출|설계)")
V3_TONGHAE = re.compile(r"통해|통한|통하여")
V4_EXEMPT = re.compile(r"[DWdw][-+]\d+|\d{1,2}:\d{2}|\d\s*[-–~]\s*\d")
V4_PUNCT = re.compile(r"[:;：；—–]|\s-\s")
BANNED = ("다양한", "철저한", "철저히", "체계적", "적극적", "극대화", "최적의", "최적화", "혁신적", "전문적",
          "풍부한", "완벽한", "완벽히", "고품격", "검증된", "프리미엄", "정교한", "매끄러운", "확실한", "맞춤형",
          "성공적", "실행형", "압도적", "탄탄한", "절대적", "국내 최대", "대표", "최상의", "특A급", "High-Quality")


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


def headline_of(xml):
    """(pt, 텍스트) — 가장 큰 글자(24pt+) 텍스트 도형에서 그 크기 런을 문단 순서로 잇는다. 없으면 (0, '')."""
    best_sz, best_txt = 0, ""
    for body in TXBODY.findall(xml):
        paras, top = [], 0
        for p in PARA.findall(body):
            runs = []
            for attrs, txt in RUN.findall(p):
                m = re.search(r'\bsz="(\d+)"', attrs or "")
                if m:
                    runs.append((int(m.group(1)), html.unescape(txt)))
            paras.append(runs)
            if runs:
                top = max(top, max(sz for sz, _ in runs))
        if top < 2400 or top <= best_sz:
            continue
        text = " ".join("".join(t for sz, t in runs if sz == top) for runs in paras if any(sz == top for sz, _ in runs))
        text = re.sub(r"\s+", " ", text).strip()
        if not text or NUMERIC_ONLY.fullmatch(text):
            continue  # KPI 숫자·고스트 넘버
        best_sz, best_txt = top, text
    return best_sz / 100, best_txt


def voice_issues(idx, title, slide_text):
    """제안서 어투 V1~V7 — proposal-voice.md §3-4 (헤드라인 기준, V3만 슬라이드 전체)."""
    out = []
    if title:
        if V1_SUBJECT.search(title):
            out.append(("V1", idx, f"주어로 시작하는 헤드라인 → '{title[:30]}'"))
        if V2_PASSIVE.search(title):
            out.append(("V2", idx, f"피동 직역 → '{title[:30]}'"))
        if V4_PUNCT.search(V4_EXEMPT.sub("", title)):
            out.append(("V4", idx, f"콜론·세미콜론·대시 → '{title[:30]}'"))
        n = len(re.sub(r"\{\{.*?\}\}|\s", "", title))
        if n > 30:
            out.append(("V5", idx, f"헤드라인 {n}자(공백 제외) > 30 — 서브카피로 나눌 것"))
        commas = len(re.findall(r",", re.sub(r"(?<=\d),(?=\d{3})", "", title)))
        dots = title.count("·") + title.count("ㆍ")
        if commas >= 2 or dots >= 2:
            out.append(("V6", idx, f"한 헤드라인 여러 주장(쉼표 {commas} · 가운뎃점 {dots}) → '{title[:30]}'"))
        if title.rstrip().rstrip("\"'’”").endswith(("?", "？")):
            out.append(("V7", idx, f"질문형 헤드라인 → '{title[:30]}'"))
    k = len(V3_TONGHAE.findall(slide_text))
    if k >= 2:
        out.append(("V3", idx, f"'통해·통한·통하여' {k}회 — 슬라이드당 1회 이하"))
    return out


def check(path, theme="remember", no_theme=False, voice="deck"):
    """검수 실행 → (issues[(code, slide|None, msg)], candidates[(slide, [금칙어])], meta dict)."""
    z = zipfile.ZipFile(path)
    slides = sorted([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
                    key=lambda n: int(re.search(r"(\d+)", n).group(1)))
    media = [n for n in z.namelist() if n.startswith("ppt/media/")]
    tokens = None if no_theme else theme_tokens(theme)
    issues, cands, off_colors, dark_count = [], [], Counter(), 0

    for idx, sn in enumerate(slides, 1):
        xml = z.read(sn).decode("utf-8", "ignore")
        texts = [html.unescape(t) for t in re.findall(r"<a:t>([^<]*)</a:t>", xml)]
        body = " ".join(texts)
        if is_dark_slide(xml, DARK_BGS):
            dark_count += 1
        # A2 테마 외 색
        if tokens is not None:
            for c in set(re.findall(r'<a:srgbClr val="([0-9A-Fa-f]{6})"', xml)):
                if c.upper() not in tokens:
                    off_colors[c.upper()] += 1
        inner = idx not in (1, len(slides))
        _, title = headline_of(xml) if inner else (0, "")
        if voice == "proposal":
            # 제안서 — A4 대신 어투 V1~V7 + 금칙 후보 (proposal-voice.md §3-4 · §6)
            if inner:
                issues += voice_issues(idx, title, body)
            hits = [w for w in BANNED if w in body]
            if hits:
                cands.append((idx, hits))
        elif title:
            # A4 명사구 제목 — 문장 종결·인용 강조어구·쉼표 리듬은 통과
            if (len(title) > 12 and not ASSERTIVE_END.search(title) and "'" not in title and "," not in title
                    and not re.match(r"^\d|^SECTION|^[IVX]+\.|^목차|^CONTENTS", title)):
                issues.append(("A4", idx, f"명사구 제목 의심 → '{title[:30]}'"))
        # A6 깨알 폰트
        tiny = [int(s) for s in re.findall(r'sz="(\d{3,4})"', xml) if int(s) < 900]
        if len(tiny) > 12:
            issues.append(("A6", idx, f"9pt 미만 텍스트 {len(tiny)}런 — 깨알 표 의심"))
        # A7 네비게이션 — 커버(1)·클로징(마지막) 제외
        off = [int(v) for v in re.findall(r'<a:off x="\d+" y="(\d+)"', xml)]
        has_footer = any(v > int(6.9 * EMU_IN) for v in off)
        has_eyebrow = any(v < int(0.75 * EMU_IN) for v in off)
        if inner and len(texts) > 4 and not (has_footer or has_eyebrow):
            issues.append(("A7", idx, "네비게이션(아이브로우/푸터) 누락 의심"))
        # A5 위계 균일
        hs = [cy for _, cy in re.findall(r'<a:ext cx="(\d+)" cy="(\d+)"', xml)]
        if len(hs) >= 6 and len(set(hs)) == 1:
            issues.append(("A5", idx, "모든 도형 동일 크기 — 위계 차등 없음"))
    if not media:
        issues.append(("A3", None, "데크 전체 이미지·텍스처 0장"))
    if tokens is not None and off_colors:
        top = ", ".join(f"#{c}({n})" for c, n in off_colors.most_common(8))
        issues.append(("A2", None, f"테마 토큰 외 색 사용: {top}"))
    if slides:
        last = z.read(slides[-1]).decode("utf-8", "ignore")
        last_text = " ".join(html.unescape(t) for t in re.findall(r"<a:t>([^<]*)</a:t>", last))
        if not CTA_HINT.search(last_text):
            issues.append(("A8", None, f"클로징에 CTA 신호 없음 → '{last_text[:40]}'"))
    if len(slides) >= 10 and dark_count / len(slides) > 0.30:  # 짧은 스모크 덱은 제외
        issues.append(("A9", None, f"다크 슬라이드 {dark_count}/{len(slides)} = {dark_count/len(slides):.0%} — 30% 초과"))
    return issues, cands, {"slides": len(slides), "dark": dark_count, "media": len(media)}


def _fmt(code, idx, msg):
    return f"[{code}] s{idx}: {msg}" if idx else f"[{code}] {msg}"


# ── 자가 테스트 (외부 의존 없음 — 합성 PPTX) ──────────────────────
def _run(text, sz, self_closing=False):
    if self_closing:
        return f'<a:r><a:rPr lang="ko-KR" sz="{sz}" b="1"/><a:t>{html.escape(text, quote=False)}</a:t></a:r>'
    return (f'<a:r><a:rPr sz="{sz}" b="1"><a:solidFill><a:srgbClr val="1A1A1A"/></a:solidFill>'
            f'<a:latin typeface="Pretendard"/><a:ea typeface="Pretendard"/></a:rPr><a:t>{html.escape(text, quote=False)}</a:t></a:r>')


def _shape(y_in, paras, cy):
    ps = "".join(f"<a:p>{''.join(paras_)}</a:p>" for paras_ in paras)
    return (f'<p:sp><p:spPr><a:xfrm><a:off x="566928" y="{int(y_in * EMU_IN)}"/><a:ext cx="11000000" cy="{cy}"/></a:xfrm></p:spPr>'
            f"<p:txBody><a:bodyPr/>{ps}</p:txBody></p:sp>")


def _slide(headline=None, body=(), kpi=None, self_closing=False):
    """deck_kit 형식을 흉내 낸 슬라이드 XML — 아이브로우·헤드라인(32pt)·본문(13pt)·푸터."""
    sh = [_shape(0.50, [[_run("01 · 섹션", 1100)]], 300000)]
    if kpi:
        sh.append(_shape(2.8, [[_run(kpi, 4800)], [_run("명", 1500)]], 2000000))
    if headline is not None:
        heads = headline if isinstance(headline, list) else [[(headline, 3200)]]
        sh.append(_shape(0.90, [[_run(t, s, self_closing) for t, s in p] for p in heads], 1188720))
    for i, b in enumerate(body):
        sh.append(_shape(2.5 + i * 0.4, [[_run(b, 1300)]], 365760 + i))
    sh.append(_shape(7.06, [[_run("행사명 · 푸터", 900)]], 274320))
    return ('<?xml version="1.0" encoding="UTF-8"?><p:sld xmlns:a="a" xmlns:p="p"><p:cSld><p:spTree>'
            + "".join(sh) + "</p:spTree></p:cSld></p:sld>")


def _deck(path, inner_slides):
    slides = [_slide("행사 기획·운영 제안서")] + inner_slides + [_slide("킥오프 미팅을 제안드립니다")]
    with zipfile.ZipFile(path, "w") as z:
        for i, x in enumerate(slides, 1):
            z.writestr(f"ppt/slides/slide{i}.xml", x)
        z.writestr("ppt/media/image1.png", b"\x89PNG\r\n")


def self_test():
    ok = True

    def expect(label, cond):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'PASS' if cond else 'FAIL'}  {label}")

    print("[self-test] 헤드라인 추출")
    expect("분할 런(강조 런) 결합", headline_of(_slide([[("감사가 아니라, ", 3200), ("'내년의 첫 미팅'", 3200)]]))[1]
           == "감사가 아니라, '내년의 첫 미팅'")
    expect("자기닫힘 rPr 형식", headline_of(_slide("책임 PM One-Stop 서비스 제공", self_closing=True))[1]
           == "책임 PM One-Stop 서비스 제공")
    expect("KPI 숫자(48pt) 건너뛰고 헤드라인(32pt)", headline_of(_slide("250명, 한 테이블.", kpi="250"))[1] == "250명, 한 테이블.")
    expect("두 줄 헤드라인 문단 결합", headline_of(_slide([[("현장 17명,", 3200)], [("지휘선 하나.", 3200)]]))[1]
           == "현장 17명, 지휘선 하나.")

    with tempfile.TemporaryDirectory() as d:
        # 1) 명사형 종결 주장 카피 — 기본 모드는 A4, 제안서 모드는 통과
        p1 = os.path.join(d, "noun.pptx")
        _deck(p1, [_slide("책임 PM One-Stop 서비스 제공"), _slide("현장 지휘는 한 사람이 맡습니다.")])
        iss, _, _ = check(p1, no_theme=True, voice="deck")
        print("[self-test] 기본 모드(--voice deck)")
        expect("명사형 종결 헤드라인 → A4 검출", [(c, i) for c, i, _ in iss] == [("A4", 2)])
        iss, _, _ = check(p1, no_theme=True, voice="proposal")
        print("[self-test] 제안서 모드(--voice proposal)")
        expect("같은 덱 → A4 꺼짐 · 위반 0", iss == [])

        # 2) 어투 V1~V7 양성 · 예외 음성
        cases = [
            ("V1", _slide("우리는 참가자에게 최고의 경험을 제공합니다")),
            ("V2", _slide("네트워킹을 할 수 있도록 설계되었습니다")),
            ("V3", _slide("3대 전략으로 운영 안정 확보", body=["사전 점검을 통해 리스크를 줄이고", "데이터를 통한 타기팅"])),
            ("V4", _slide("1단계: 기획 확정")),
            ("V5", _slide("참가자 동선 설계와 안전 관리 체계와 수송 계획과 식음 운영까지 모두 한 번에 확정")),
            ("V6", _slide("숙소 120실, 도시락 300명분, 협찬 5사 확보")),
            ("V7", _slide("세미나의 성패는 무엇으로 결정될까요?")),
            (None, _slide("D-30 답사와 10:00~12:00 리허설로 현장 확정")),
            (None, _slide("2,000명의 러너, 2,000가지의 러닝 여정을 설계")),
            (None, _slide("리멤버 MICE는 '행사'가 아니라 '참석자'를 보장합니다")),
            (None, _slide("안전 리스크 8종을 표로 관리", body=["체계적인 안전관리"])),
        ]
        p2 = os.path.join(d, "voice.pptx")
        _deck(p2, [x for _, x in cases])
        iss, cands, _ = check(p2, no_theme=True, voice="proposal")
        got = {(c, i) for c, i, _ in iss}
        for n, (code, _) in enumerate(cases, 2):
            if code:
                expect(f"{code} 검출 (s{n})", (code, n) in got)
            else:
                expect(f"예외·정상 헤드라인 통과 (s{n})", not any(i == n for _, i in got))
        expect("검출이 해당 슬라이드에만", got == {(c, n) for n, (c, _) in enumerate(cases, 2) if c})
        last = len(cases) + 1  # '체계적' 본문 슬라이드
        expect("금칙 후보 출력 · 실패 미처리", any(i == last and "체계적" in w for i, w in cands)
               and not any(i == last for _, i in got))

        # 3) 실제 deck_kit 덱 회귀 (python-pptx·jc-design-system 있으면)
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import deck_kit
            p3 = deck_kit._smoke(os.path.join(d, "smoke.pptx"))
        except Exception as e:  # noqa: BLE001
            print(f"[self-test] deck_kit 스모크 덱 회귀 — 건너뜀({type(e).__name__}: {e})")
        else:
            print("[self-test] deck_kit 스모크 덱 회귀")
            for v in ("deck", "proposal"):
                iss, _, _ = check(p3, voice=v)
                expect(f"--voice {v} 위반 0", iss == [])

    print("[self-test] 결과:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="jc-pptx 안티패턴 + 제안서 어투 검수")
    ap.add_argument("deck", nargs="?")
    ap.add_argument("--theme", default="remember")
    ap.add_argument("--no-theme", action="store_true")
    ap.add_argument("--voice", choices=("deck", "proposal"), default="deck",
                    help="proposal = 발주처 제안서(A4 끔 · 어투 V1~V7 · 금칙 후보) — references/proposal-voice.md")
    ap.add_argument("--self-test", action="store_true", help="합성 덱으로 검출기 자가 검증")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    if not a.deck:
        ap.error("deck 경로가 필요합니다 (또는 --self-test)")
    issues, cands, meta = check(a.deck, a.theme, a.no_theme, a.voice)
    print(f"jc-pptx check_deck — {a.deck} ({meta['slides']} slides · 다크 {meta['dark']} · 미디어 {meta['media']}"
          f" · voice {a.voice})")
    if cands:
        print(f"금칙 수식어 후보 {sum(len(w) for _, w in cands)}건 — 근거(수치·사례·프로세스명) 동반 여부 사람 판정"
              " (proposal-voice.md §6)")
        for idx, words in cands:
            print(f"  [후보] s{idx}: {' · '.join(words)}")
    if issues:
        print(f"FAIL — {len(issues)}건")
        for i in issues:
            print(" ", _fmt(*i))
        sys.exit(1)
    print("PASS — 안티패턴 0건" + (" · 어투 위반 0건" if a.voice == "proposal" else ""))


if __name__ == "__main__":
    main()
