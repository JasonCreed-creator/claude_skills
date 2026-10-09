# -*- coding: utf-8 -*-
"""리멤버 MICE 솔루션 소개서 v2 — 섹션 순서 가변(솔루션 우선 / 팀 우선) 빌드 스크립트."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from remember_kit import *
from PIL import Image, ImageDraw, ImageOps
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

SCR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(SCR, "img")
SKILLS = r"C:\Users\Jinchul Lee\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\42d3cd4d-ae05-4e24-bd4e-cf117d75612c\e19e80d1-4484-489b-bf31-cb6d61aa52c1\skills"
ASSETS = os.path.join(SKILLS, "jc-design-system", "assets")  # 로고·오브제 정본 (구 jc-remember-html 폐합)
OUT = os.path.join(SCR, "out"); os.makedirs(OUT, exist_ok=True)

def P(sub, name): return os.path.join(IMG, sub, name)

def circle_png(src, out, size=1400, centering=(0.5, 0.45)):
    im = Image.open(src).convert("RGB")
    im = ImageOps.fit(im, (size, size), centering=centering)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    im.putalpha(mask); im.save(out); return out

def gray_png(src, out, size=(600, 800)):
    im = Image.open(src).convert("L"); im = ImageOps.fit(im, size); im = ImageOps.autocontrast(im)
    im.convert("RGB").save(out); return out

O, OD, OS, OT = T["orange"], T["orange_deep"], T["orange_soft"], T["orange_tint"]
INK, SUB, MUT, BR, CH = T["ink"], T["ink_sub"], T["warm_gray"], T["brown"], T["charcoal"]
ST = T["steel"]
DOC = "리멤버 MICE 솔루션 소개서"

# ══════════════════════════════════════════════════════════════════
# 섹션별 슬라이드 함수 — (d, eb, ft) : eyebrow 문자열 / footer 섹션명
# ══════════════════════════════════════════════════════════════════

# ── 01 문제 정의 ─────────────────────────────────────────────────
def s_quote(d, eb, ft):
    s = d.content_slide(eb, ft, [("\"행사는 잘 끝났습니다.\n그런데 ", INK), ("계약", O), ("은 어디에 있죠?\"", INK)],
        sub="행사를 열어본 기업 214곳에 물었습니다. 고민 1위는 '성과'였습니다.")
    stats = [("34%", "영업 기회로 넘어가지 않는다\nROI를 증명할 수 없다", True), ("28%", "준비 리소스가\n낭비된다", False), ("21%", "핵심 타겟 모객이 어렵다\n노쇼가 많다", False)]
    w = (CONTENT_W - GAP * 2) / 3
    for i, (num, cap, solid) in enumerate(stats):
        d.kpi(s, MARGIN + i * (w + GAP), 2.85, w, 2.55, num, top="주최사 고민 " + ["1위", "2위", "3위"][i], bottom=cap, solid=solid, num_size=54)
    d.text(s, MARGIN, 5.5, CONTENT_W, 0.3, [("출처: 리멤버 B2B 마케터 조사 · 행사 주최 경험 기업 214곳 응답, 2026", MUT)], 8.5)
    d.takeaway(s, [("행사가 안 열려서가 아니라, ", INK), ("열린 행사가 매출로 증명되지 않아서", OD), (" 고민입니다.", INK)])

def s_funnel(d, eb, ft):
    s = d.content_slide(eb, ft, [("사전등록 100명 중 ", INK), ("30명", O), ("만 오고,\n그중 만나려던 사람은 ", INK), ("10명 중 1명", O), ("입니다.", INK)],
        sub="쇼업의 절벽과 타겟의 공백. 예산의 대부분이 이 두 지점에서 사라집니다.")
    d.text(s, MARGIN, 2.7, 6.6, 0.3, [("① 쇼업의 절벽 · 사전등록 100명이 당일까지 남는 과정", INK)], 12, bold=True)
    bars = [("사전등록", 100, T["line"]), ("D-1 잔존", 55, T["orange_pale"]), ("당일 참석", 30, O)]
    maxw = 5.0
    for i, (lab, v, col) in enumerate(bars):
        y = 3.15 + i * 0.78
        d.text(s, MARGIN, y + 0.1, 1.1, 0.4, [(lab, BR)], 10.5, bold=True)
        d.box(s, MARGIN + 1.15, y, maxw, 0.52, fill=T["surface_warm"], radius=0.3)
        d.box(s, MARGIN + 1.15, y, maxw * v / 100, 0.52, fill=col, radius=0.3)
        d.text(s, MARGIN + 1.15 + maxw * v / 100 + 0.1, y + 0.08, 1.2, 0.4, [(f"{v}명", INK)], 12, bold=True)
    d.text(s, MARGIN, 5.5, 6.6, 0.6, [("등록 직후부터 당일까지 3주 동안 조용히 빠져나갑니다.\n리마인드를 N번 보내도 숫자가 움직이지 않는 이유는 횟수가 아니라 설계의 문제입니다.", SUB)], 9.5, line_spacing=1.3)
    x0 = MARGIN + 7.2; wr = CONTENT_W - 7.2
    d.text(s, x0, 2.7, wr, 0.3, [("② 타겟의 공백 · 광고 모집형 등록자 100명의 구성", INK)], 12, bold=True)
    d.card(s, x0, 3.15, wr, 2.9)
    d.box(s, x0 + 0.3, 3.45, wr - 0.6, 0.55, fill=T["surface_warm"], radius=0.3)
    d.box(s, x0 + 0.3, 3.45, (wr - 0.6) * 0.1, 0.55, fill=O, radius=0.3)
    d.text(s, x0 + 0.3, 4.1, 1.6, 0.9, [("10%", O, True, 34)], 34, bold=True)
    d.text(s, x0 + 1.9, 4.18, wr - 2.2, 0.8, [("만나려던 타겟\n", INK, True, 11), ("의사결정권자·타겟 직무", SUB)], 10, line_spacing=1.25)
    d.text(s, x0 + 0.3, 5.05, wr - 0.6, 0.9, [("나머지 90명은 예산과 좌석만 쓰고 계약으로 이어지지 않습니다.\n등록자 수는 목표를 넘겨도, 영업팀은 \"연락할 사람이 없다\"고 말합니다.", BR)], 9.5, line_spacing=1.3)
    d.takeaway(s, [("등록자 수는 KPI가 아닙니다. 등록자의 ", INK), ("'구성'", OD), ("이 매출을 결정합니다.", INK)])

def s_links(d, eb, ft):
    s = d.content_slide(eb, ft, [("매출은 ", INK), ("타겟·쇼업·세일즈", O), (" 세 고리가\n이어질 때만 나옵니다.", INK)],
        sub="한 고리라도 끊기면 좌석은 차도 계약은 비어 있습니다. 기존 시장은 각 고리를 따로 팝니다.")
    links = [("01 · TARGET", "타겟", "의사결정권자만 골라내는\n타겟 설계", "데이터·광고 플랫폼은\n'명단'만 팝니다"),
             ("02 · SHOW-UP", "쇼업", "등록자를 참석자로 바꾸는\n리마인드·현장 설계", "행사 대행사는\n'운영'만 합니다"),
             ("03 · SALES", "세일즈", "현장의 대화를 계약으로 잇는\n전환 설계", "사후 팔로업은\n고객사 영업팀 몫으로 남습니다")]
    w = (CONTENT_W - GAP * 2) / 3
    for i, (tag, big, desc, gap) in enumerate(links):
        x = MARGIN + i * (w + GAP)
        d.card(s, x, 2.9, w, 2.15, hl=True)
        d.text(s, x + 0.25, 3.05, w - 0.5, 0.3, [(tag, O)], 10.5, bold=True, spacing=1.5)
        d.text(s, x + 0.25, 3.35, w - 0.5, 0.7, [(big, INK)], 26, bold=True)
        d.text(s, x + 0.25, 4.1, w - 0.5, 0.85, [(desc, BR)], 11, line_spacing=1.3)
        d.box(s, x, 5.2, w, 0.85, fill=T["surface_warm"], radius=0.08)
        d.text(s, x + 0.25, 5.27, w - 0.5, 0.75, [("기존 시장  ", MUT, True, 9), (gap, BR)], 9.5, line_spacing=1.25)
        if i < 2: d.chevron(s, x + w + 0.03, 3.72, w=0.27, h=0.5)
    d.takeaway(s, [("세 고리를 ", INK), ("하나의 데이터", OD), ("로 잇는 구조. 그것이 리멤버 MICE 솔루션입니다.", INK)])

# ── 02 왜 리멤버인가 ─────────────────────────────────────────────
def s_data(d, eb, ft):
    s = d.content_slide(eb, ft, [("국내 최대 비즈니스 네트워크 앱의\n검증된 프로필 ", INK), ("500만", O), ("이 곧 초청 명부입니다.", INK)],
        sub="직장인이 매일 명함을 등록하고 갱신하는 앱이라, 소속·직급·직무가 '살아 있는' 데이터입니다.")
    kp = [("500만+", "DATA POOL", "검증된 비즈니스 프로필\n실명·소속·직급 확인", True),
          ("60%", "DECISION MAKERS", "의사결정권자 비중\n(리멤버 리서치 패널 기준)", False),
          ("41%", "C-LEVEL", "대표 21% + 임원 20% (패널 기준)\n최종 결재선에 직접 닿는 풀", False),
          ("310×145", "TAXONOMY", "310개 산업 × 145개 직무 분류\n표준산업분류코드 매핑", False)]
    w = (CONTENT_W - GAP * 3) / 4
    for i, (num, top, bot, solid) in enumerate(kp):
        d.kpi(s, MARGIN + i * (w + GAP), 2.85, w, 2.25, num, top=top, bottom=bot, solid=solid, num_size=40 if i < 3 else 30)
    d.text(s, MARGIN, 5.3, 2.0, 0.35, [("조합 가능한 조건", INK)], 11, bold=True)
    cx = MARGIN + 2.0
    for c in ["산업", "직무", "직급", "부서", "기업 규모", "매출", "소재지", "사업자등록번호", "최근 활동 시그널"]:
        cw = 0.32 + len(c) * 0.16
        d.pill(s, cx, 5.28, cw, 0.36, c, fill=OT, color=OD, size=9.5); cx += cw + 0.12
    d.takeaway(s, [("양이 아니라 ", INK), ("'골라낼 수 있다'", OD), ("는 것이 핵심입니다. 광고로 뿌리지 않고, 이름을 알고 초청합니다.", INK)])

def s_target(d, eb, ft):
    s = d.content_slide(eb, ft, [("'올 사람'이 아니라 ", INK), ("'와야 할 사람'", O), ("을\n네 줄의 조건으로 지목합니다.", INK)],
        sub="데이터 → 필터 → 우선순위 → 초청. 그리고 대부분의 타겟팅이 빠뜨리는 '버리는 기준'까지.")
    steps = [("01 · DATA POOL", "명함·이력서 데이터", "국내 최대 비즈니스 프로필\n재직·직급·직무 최신성\n동의 기반 컨택 채널"),
             ("02 · FILTER", "결정권자 정의", "직급: 검토자 vs 결재자\n직무: 사용 부서와 구매 부서\n산업과 규모: 계약 가능성"),
             ("03 · SCORE", "우선순위 스코어링", "타겟 기업 리스트 매칭\n기존 거래·상담 이력 가중\n유사 기업·직무로 확장"),
             ("04 · INVITE", "개인화 초청", "이름과 직무 맞춤 메시지\n'당신의 자리' 명시\n등록 현황 고객사 실시간 공유")]
    w = (CONTENT_W - GAP * 3) / 4
    for i, (tag, title, desc) in enumerate(steps):
        x = MARGIN + i * (w + GAP)
        d.card(s, x, 2.85, w, 2.05, hl=(i == 3))
        d.text(s, x + 0.2, 3.0, w - 0.4, 0.3, [(tag, O)], 10, bold=True, spacing=1.5)
        d.text(s, x + 0.2, 3.32, w - 0.4, 0.45, [(title, INK)], 14.5, bold=True)
        d.text(s, x + 0.2, 3.8, w - 0.4, 1.05, [(desc, BR)], 10, line_spacing=1.35)
        if i < 3: d.chevron(s, x + w + 0.03, 3.62, w=0.27, h=0.5)
    d.box(s, MARGIN, 5.08, CONTENT_W, 0.62, fill=CH, radius=0.08)
    d.text(s, MARGIN + 0.3, 5.08, 1.2, 0.62, [("DROP", OS)], 13, bold=True, anchor=MSO_ANCHOR.MIDDLE, spacing=2)
    d.text(s, MARGIN + 1.5, 5.08, CONTENT_W - 1.8, 0.62, [("경쟁사, 무관 직무, '머릿수 채우기'는 초청하지 않습니다. 좌석은 의사결정 그룹에게만 씁니다.", "F4F0E9")], 11.5, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, MARGIN, 5.8, CONTENT_W, 0.4, [("실물 예시 · A사 컨퍼런스 (2026.7): 임직원 500인 이상 · 정보보안/IT운영/사업전략/AI데이터 · 팀장급 이상 · 기존 고객사 제외  →  초청 후보 ", SUB), ("188,230명", OD, True)], 9.5)
    d.takeaway(s, [("타겟은 '모집'이 아니라 ", INK), ("'지목'", OD), ("이어야 합니다. 뺄 사람을 먼저 정해야 좌석이 삽니다.", INK)])

def s_compare(d, eb, ft):
    s = d.content_slide(eb, ft, [("같은 좌석인데 명단을 바꾸면,\n타겟 일치율이 ", INK), ("10%에서 75%", O), ("가 됩니다.", INK)],
        sub="왼쪽은 광고 모객의 일반적인 결과, 오른쪽은 A사 컨퍼런스 참석자 168명 전원의 직급을 열어본 실측입니다.")
    w = (CONTENT_W - 0.9) / 2; x = MARGIN
    d.card(s, x, 2.85, w, 2.85)
    d.text(s, x + 0.3, 3.0, w - 0.6, 0.3, [("BEFORE · 광고 모집형", MUT)], 10, bold=True, spacing=1.5)
    d.text(s, x + 0.3, 3.3, 2.2, 1.0, [("10%", MUT, True, 44)], 44, bold=True)
    d.text(s, x + 2.4, 3.42, w - 2.7, 0.8, [("\"많이 왔다\"\n", INK, True, 15), ("등록자 중 만나려던 타겟 비중", SUB)], 10.5, line_spacing=1.25)
    d.bullet_list(s, x + 0.3, 4.45, w - 0.6, ["등록자 수는 목표 달성, 명부를 열면 타겟은 10명 중 1명", "나머지 90%에 예산과 좌석이 소모", "행사 후 영업팀: \"연락할 사람이 없다\""], size=10, gap=0.38, bullet_color=T["line"])
    x = MARGIN + w + 0.9
    d.card(s, x, 2.85, w, 2.85, hl=True); d.grad(s, x, 2.85, w, 0.09, radius=0)
    d.text(s, x + 0.3, 3.0, w - 0.6, 0.3, [("AFTER · 리멤버 데이터 지목형", O)], 10, bold=True, spacing=1.5)
    d.text(s, x + 0.3, 3.3, 2.2, 1.0, [("75%", O, True, 44)], 44, bold=True)
    d.text(s, x + 2.4, 3.42, w - 2.7, 0.8, [("\"살 사람이 왔다\"\n", INK, True, 15), ("타겟 조건 일치 참석자 (A사 168명 실측)", SUB)], 10.5, line_spacing=1.25)
    d.bullet_list(s, x + 0.3, 4.45, w - 0.6, ["C레벨·임원 28% + 부장·팀장급 47%, 대리·사원은 5%", "대기업 참석사의 60%가 2명 이상 동반 참석 (중소기업 2.5%)", "C사 행사는 1순위 타겟 24개사를 기업명 단위로 지목해 모객"], size=10, gap=0.38)
    d.arrow(s, MARGIN + w + 0.17, 4.1, w=0.56, h=0.36)
    d.takeaway(s, [("KPI는 등록자 수가 아니라, ", INK), ("'타겟 조건에 맞는 참석자 비율'", OD), ("입니다.", INK)])

def s_showup(d, eb, ft):
    s = d.content_slide(eb, ft, [("등록이 아니라 ", INK), ("참석", O), ("을 설계합니다.\n확인을 통과한 사람은 ", INK), ("82%", O), ("가 옵니다.", INK)],
        sub="리마인드는 '발송'이 아니라 운영표입니다. 다섯 계단의 확인이 등록자를 '약속한 사람'으로 바꿉니다.")
    ladder = [("신청 직후", "문자", "접수 확인 +\n행사 가치 리마인드"), ("신청 +2~3일", "유선 콜", "참석·예비·검토\n3단계 분류"),
              ("D-7", "문자", "최종 확정 요청\n좌석·어젠다 안내"), ("D-1", "확정폼", "\"가겠다\"를\n한 번 더 누르는 절차"), ("당일 09:00", "문자 + 영접", "오시는 길·체크인\n마지막 마찰 제거")]
    lw = 7.55; n = len(ladder); cw = (lw - 0.18 * (n - 1)) / n
    for i, (when, ch, desc) in enumerate(ladder):
        x = MARGIN + i * (cw + 0.18)
        d.card(s, x, 2.85, cw, 1.75, hl=(i == 3))
        d.text(s, x + 0.12, 2.95, cw - 0.24, 0.3, [(when, O)], 9.5, bold=True)
        d.text(s, x + 0.12, 3.22, cw - 0.24, 0.4, [(ch, INK)], 13, bold=True)
        d.text(s, x + 0.12, 3.62, cw - 0.24, 0.9, [(desc, BR)], 9, line_spacing=1.25)
    d.card(s, MARGIN, 4.75, 3.65, 1.4)
    d.text(s, MARGIN + 0.2, 4.85, 3.3, 0.3, [("전체 신청자 기준 참석률", MUT)], 9.5, bold=True)
    d.text(s, MARGIN + 0.2, 5.12, 1.5, 0.9, [("35%", MUT, True, 34)], 34, bold=True)
    d.text(s, MARGIN + 1.75, 5.3, 1.8, 0.7, [("전원에게 같은\n리마인드를 보냈을 때", SUB)], 9, line_spacing=1.25)
    d.card(s, MARGIN + 3.9, 4.75, 3.65, 1.4, hl=True)
    d.text(s, MARGIN + 4.1, 4.85, 3.3, 0.3, [("D-1 확인 통과자 기준 참석률", O)], 9.5, bold=True)
    d.text(s, MARGIN + 4.1, 5.12, 1.5, 0.9, [("82%", O, True, 34)], 34, bold=True)
    d.text(s, MARGIN + 5.65, 5.3, 1.8, 0.7, [("콜 → 확정폼 → D-1 확인\n통과자 (행사별 82~107%)", SUB)], 9, line_spacing=1.25)
    gx = MARGIN + 7.95; gw = CONTENT_W - 7.95
    d.card(s, gx, 2.85, gw, 3.3); d.grad(s, gx, 2.85, gw, 0.95, radius=0.08); d.box(s, gx, 3.45, gw, 0.4, fill=OS, radius=0)
    d.text(s, gx + 0.3, 2.95, gw - 0.6, 0.3, [("SHOW-UP GUARANTEE", "FFF1E6")], 9.5, bold=True, spacing=2)
    d.text(s, gx + 0.3, 3.22, gw - 0.6, 0.5, [("참석 인원을 계약으로 보장합니다", "FFFFFF")], 15, bold=True)
    d.bullet_list(s, gx + 0.3, 4.05, gw - 0.6, ["목표 인원의 130%를 확정한 채 당일을 시작", "결정권자·실무자 트랙을 나눈 채널·타이밍·메시지", "미달 시 목표 도달까지 추가 모객 무상 지원", "좌석이 비는 리스크를 리멤버가 집니다"], size=10, gap=0.48)
    d.takeaway(s, [("리마인드 횟수가 아니라 ", INK), ("'확인'이라는 행동", OD), ("이 참석을 일정에서 약속으로 바꿉니다.", INK)])

def s_showup_results(d, eb, ft):
    s = d.content_slide(eb, ft, [("참석률은 운이 아니라 ", INK), ("운영의 결과", O), ("입니다.\n2026년 행사 4건 모두 목표를 넘겼습니다.", INK)],
        sub="목표 인원(KPI) 대비 실제 참석 인원. 같은 확인 사다리와 130% 버퍼 기준을 적용한 결과입니다.")
    data = [("A사", "AI 보안 컨퍼런스", 50, 57, 114), ("J사", "초청 컨퍼런스", 60, 81, 135), ("I사", "이커머스 대형 컨퍼런스", 100, 138, 138), ("K사", "임원 세미나", 30, 58, 193)]
    cx0 = MARGIN; cw = 7.3; base_y = 5.55; maxh = 2.45; bw = 1.05
    d.text(s, cx0, 2.72, cw, 0.3, [("KPI 대비 실참석률 (%)", INK)], 11, bold=True)
    ref_y = base_y - maxh * 100 / 200
    d.hline(s, cx0, ref_y, cw, color=T["line"], weight=0.75)
    d.text(s, cx0, ref_y - 0.27, 1.2, 0.25, [("목표 100%", MUT)], 8.5)
    for i, (co, ev, k, a, pct) in enumerate(data):
        x = cx0 + 0.5 + i * 1.75; h = maxh * pct / 200
        d.box(s, x, base_y - h, bw, h, fill=O if i == 3 else T["orange_pale"], radius=0)
        d.text(s, x - 0.2, base_y - h - 0.42, bw + 0.4, 0.4, [(f"{pct}%", INK)], 15, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, x - 0.35, base_y + 0.06, bw + 0.7, 0.55, [(f"{co} · {ev}\n", INK, True, 9.5), (f"KPI {k}명 → {a}명", SUB)], 9, align=PP_ALIGN.CENTER, line_spacing=1.2)
    d.hline(s, cx0, base_y, cw, color=INK, weight=1.25)
    rx = MARGIN + 7.75; rw = CONTENT_W - 7.75
    d.card(s, rx, 2.72, rw, 3.45, hl=True)
    d.text(s, rx + 0.25, 2.85, rw - 0.5, 0.3, [("같은 행사 1차 → 2차, 리마인드 설계 전후", O)], 10, bold=True)
    d.text(s, rx + 0.25, 3.15, 1.3, 0.8, [("30%", MUT, True, 30)], 30, bold=True)
    d.arrow(s, rx + 1.5, 3.42, w=0.45, h=0.3)
    d.text(s, rx + 2.05, 3.15, 1.4, 0.8, [("60%", O, True, 30)], 30, bold=True)
    d.text(s, rx + 0.25, 3.98, rw - 0.5, 0.3, [("사전등록자 대비 실제 참석 비율, 100명 중 30명이 더 왔습니다", SUB)], 9)
    for i, (b, a) in enumerate([("전원 동일 발송", "타겟별 시나리오 · 결정권자와 실무자의 동선 분리"), ("문자 N번 반복", "채널 믹스 + 마지막 D-1은 사람이 직접 전화"), ("'행사 안내' 공지", "'당신의 자리' · 좌석·자료·미팅, 내 것의 언어")]):
        y = 4.4 + i * 0.56
        d.text(s, rx + 0.25, y, 1.3, 0.5, [(b, MUT)], 8.8, line_spacing=1.2)
        d.chevron(s, rx + 1.55, y + 0.06, w=0.16, h=0.28)
        d.text(s, rx + 1.78, y, rw - 2.0, 0.5, [(a, INK)], 8.8, bold=True, line_spacing=1.2)
    d.takeaway(s, [("목표가 100명이면 130명을 확정해 두고 시작합니다. ", INK), ("버퍼는 비용이 아니라 좌석의 보험", OD), ("입니다.", INK)])

def s_sales(d, eb, ft):
    s = d.content_slide(eb, ft, [("명함 300장이 아니라 ", INK), ("대화의 맥락", O), ("을 남겨\n계약까지 잇습니다.", INK)],
        sub="계약은 무대가 아니라 상담 테이블에서 시작됩니다. 행사 중과 행사 후 N주를 다섯 칸으로 설계합니다.")
    cells = [("01 · MATCH", "사전 매칭", "우선 계정 추출\n담당 세일즈 배정\n대화 목표 설정"), ("02 · FLOOR", "현장 동선", "좌석·테이블 배치\n브레이크 동선 설계\n데모·부스로 계기 심기"),
             ("03 · LOG", "현장 기록", "누구와, 무엇을\n다음 약속 합의\n식기 전에 30초 기록"), ("04 · D+1~W1", "맥락 팔로업", "대화 한 줄 인용 감사\n자료 + 미팅 제안\n캘린더로 다음 스텝"),
             ("05 · W2~N", "시그널 너처링", "열람·회신·재방문 추적\nHOT 리드 우선 접촉\n경쟁사 비교·사례 공급")]
    n = 5; w = (CONTENT_W - 0.2 * (n - 1)) / n
    for i, (tag, title, desc) in enumerate(cells):
        x = MARGIN + i * (w + 0.2)
        d.card(s, x, 2.85, w, 2.1, hl=(i == 2))
        if i == 2: d.grad(s, x, 2.85, w, 0.09, radius=0)
        d.text(s, x + 0.18, 3.0, w - 0.36, 0.3, [(tag, O)], 9.5, bold=True, spacing=1.2)
        d.text(s, x + 0.18, 3.3, w - 0.36, 0.45, [(title, INK)], 14, bold=True)
        d.text(s, x + 0.18, 3.8, w - 0.36, 1.1, [(desc, BR)], 9.8, line_spacing=1.35)
    d.card(s, MARGIN, 5.15, 5.6, 1.0)
    d.text(s, MARGIN + 0.25, 5.22, 1.4, 0.9, [("ONE RULE", O)], 10, bold=True, spacing=1.5, anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, MARGIN + 1.5, 5.22, 3.9, 0.9, [("호스트 1명이 맡는 타겟은 최대 3팀. 결정권자 10팀을 부르면 우리 쪽 응대 인력이 3~4명 필요하다는 뜻입니다.", BR)], 9.5, line_spacing=1.3, anchor=MSO_ANCHOR.MIDDLE)
    bx = MARGIN + 5.85; bw2 = CONTENT_W - 5.85
    d.card(s, bx, 5.15, bw2, 1.0)
    d.text(s, bx + 0.25, 5.22, bw2 - 0.5, 0.3, [("사전 매칭 보드 (예시)  ", O, True, 9.5), ("타겟 · 전담 호스트 · 접점 장소 · 첫 대화 주제 · 성공 조건", MUT)], 9)
    d.text(s, bx + 0.25, 5.5, bw2 - 0.5, 0.6, [("A사 CFO · 대표이사 직접 · VIP 라운지 · 업계 원가 구조 리포트 · 경영진 미팅 확정\nC사 IT실장 · 프리세일즈 · 데모 존 · 라이브 데모 시연 · PoC 일정 합의", BR)], 9, line_spacing=1.3)
    d.takeaway(s, [("타겟에서 시작한 데이터가 기록과 팔로업까지 끊기지 않습니다. 이것이 ", INK), ("ONE DATA", OD), ("입니다.", INK)])

def s_unique(d, eb, ft):
    s = d.content_slide(eb, ft, [("데이터·모객·운영·세일즈를 ", INK), ("한 계약", O), ("으로.\n이 구조를 가진 사업자는 리멤버가 유일합니다.", INK)],
        sub="MICE는 온라인에서 포착되지 않는 구매 신호가 한자리에 모이는 지점입니다. 그 참석자를 식별하고, DB의 흐름까지 만드는 회사여야 합니다.")
    cols = ["", "리멤버 MICE", "행사 대행사 (PCO)", "데이터·광고 플랫폼"]
    rows = [("초청 명단", "●  자체 검증 프로필 500만", "△  외부 DB 구매·광고 모집", "●  보유 (행사 연계는 별도)"),
            ("개인화 초청 · RSVP 확정 콜", "●  트랙별 운영표로 직접", "△  단체 발송 위주", "△  발송만, 확인 단계 없음"),
            ("참석 보장 (Show-up Guarantee)", "●  계약에 명문화, 미달 시 무상 추가 모객", "✕", "✕"),
            ("베뉴·무대·현장 운영", "●  PM·스태프·제휴 호텔", "●", "✕"),
            ("사전 매칭 · 현장 기록 · 팔로업", "●  세일즈 연결 설계 포함", "✕", "△  리드 전달까지"),
            ("성과 리포트 · 명단 소유권", "●  참석 데이터·시그널, 명단은 고객사 소유", "△  결과보고서", "△  리드 리스트")]
    cx = [MARGIN, MARGIN + 3.0, MARGIN + 6.35, MARGIN + 9.05]; cwid = [3.0, 3.35, 2.7, 3.04]; hy = 2.78
    d.box(s, cx[1], hy, cwid[1], 0.42, fill=O, radius=0.08)
    for j, c in enumerate(cols):
        if j == 0: continue
        d.text(s, cx[j], hy, cwid[j], 0.42, [(c, "FFFFFF" if j == 1 else INK)], 11, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    d.box(s, cx[1], hy + 0.42, cwid[1], 0.46 * len(rows) + 0.05, fill=OT, radius=0.08)
    for i, r in enumerate(rows):
        y = hy + 0.5 + i * 0.46
        d.hline(s, MARGIN, y + 0.46, CONTENT_W, color=T["line_soft"], weight=0.75)
        for j, val in enumerate(r):
            col = INK if j == 0 else (OD if val.startswith("●") else (BR if val.startswith("△") else MUT))
            d.text(s, cx[j] + 0.15, y, cwid[j] - 0.3, 0.46, [(val, col)], 9.5 if j else 10.5, bold=(j == 0 or (j == 1)), align=PP_ALIGN.LEFT if j < 2 else PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, MARGIN, 6.08, CONTENT_W, 0.26, [("●  직접 제공   △  부분 제공 또는 외부 의존   ✕  미제공  ·  시장 일반 유형 기준의 비교이며 개별 사업자와는 다를 수 있습니다", MUT)], 8.5)
    d.takeaway(s, [("명단을 가진 회사가 ", INK), ("직접 초청하고, 운영하고, 결과를 보장", OD), ("합니다.", INK)])

# ── 03 솔루션 구조 ───────────────────────────────────────────────
def s_timeline(d, eb, ft):
    s = d.content_slide(eb, ft, [("행사 ", INK), ("8주 전", O), ("에 시작하면 됩니다.\n앞의 두 줄이 나머지 6주를 결정합니다.", INK)],
        sub="리멤버 MICE 표준 운영 일정. 각 단계의 담당이 명확해서 고객사가 준비할 것은 연사·콘텐츠와 현장 영업 응대뿐입니다.")
    phases = [("D-8주 ~ D-7주", "목표와 명단", "몇 명을, 어떤 분들로 모실지 확정\n타겟 조건 4줄 · 초청 후보 모수 · 형식·베뉴", "리멤버 + 고객사 함께", True),
              ("D-7주 ~ D-3주", "모객과 준비", "초청 발송 · 랜딩페이지 · RSVP\n프로그램 구성 · 무대·디자인 제작\n초청부터 신청까지 보통 2~4주", "리멤버 (연사·콘텐츠는 고객사)", False),
              ("D-2주 ~ 당일", "확인과 현장", "콜 → 확정폼 → D-1 확인\n130% 버퍼 확보 · 사전 매칭표\n체크인·컨시어지·현장 기록", "리멤버 (영업 응대는 고객사)", False),
              ("종료 후 1주", "성과 리포트", "참석자 데이터 · 조건 일치율\n반응 분석 · HOT/WARM/COLD\n후속 액션 제안 · 명단 인계", "리멤버 (명단은 고객사 소유)", False)]
    n = 4; w = (CONTENT_W - 0.25 * (n - 1)) / n
    for i, (when, title, desc, owner, hero) in enumerate(phases):
        x = MARGIN + i * (w + 0.25)
        if hero: d.grad(s, x, 2.85, w, 2.85, radius=0.08); tc, dc, oc, wc = "FFFFFF", "FFF1E6", "FFFFFF", "FFF1E6"
        else:
            d.card(s, x, 2.85, w, 2.85); d.box(s, x, 2.85, w, 0.08, fill=T["orange_pale"], radius=0); tc, dc, oc, wc = INK, BR, OD, O
        d.text(s, x + 0.22, 3.02, w - 0.44, 0.3, [(when, wc)], 10, bold=True, spacing=1)
        d.text(s, x + 0.22, 3.32, w - 0.44, 0.5, [(title, tc)], 17, bold=True)
        d.text(s, x + 0.22, 3.85, w - 0.44, 1.2, [(desc, dc)], 9.8, line_spacing=1.35)
        d.text(s, x + 0.22, 5.2, w - 0.44, 0.4, [("담당  ", wc, True, 8.5), (owner, oc)], 9.5, bold=True)
        if i < 3: d.chevron(s, x + w + 0.02, 4.02, w=0.21, h=0.42)
    d.text(s, MARGIN, 5.85, CONTENT_W, 0.35, [("계약 후 킥오프 미팅에서 운영정책서·WBS·커뮤니케이션 프로토콜을 공유합니다. 역할 분담, 리마인드 운영표, 현장 매뉴얼, 개인정보 처리 기준까지 문서로 합의한 뒤 시작합니다.", SUB)], 9.5)
    d.takeaway(s, [("11월 행사라면, ", INK), ("지금 시작하시면 됩니다.", OD)])

def s_scope(d, eb, ft):
    s = d.content_slide(eb, ft, [("명단부터 리포트까지, ", INK), ("한 계약", O), ("으로 끝납니다.\n나눠 발주하고 조율할 일이 없습니다.", INK)],
        sub="여섯 영역을 한 창구가 책임집니다. 고객사는 연사와 콘텐츠, 그리고 현장에서의 대화에만 집중하면 됩니다.")
    scope = [("TARGET", "명단 · 초청 · RSVP", "타겟 조건 설계 · 초청 후보 모수 산출\n개인화 초청 메시지 · 랜딩페이지 제작\n유선 확정 콜 · 확정폼 · 고객사 전용 리드 대시보드"),
             ("VENUE", "베뉴 · F&B", "서울 주요 호텔 20곳+ 제휴 (5성급 중심)\n대관·F&B 조건 협상 (F&B 상계 등)\n표준 답사 체크리스트로 동선·설비 확인"),
             ("PRODUCTION", "무대 · 기술 · 디자인", "LED 미디어월 · 스위칭 · 프롬프터 · 음향\n키비주얼 · 백월 · 배너 · 명찰 · 인쇄물\n전문 사회자 · 사진·영상 촬영"),
             ("ON-SITE", "현장 운영", "행사경험 100건+ PM + 운영 스태프\n셀프 체크인 키오스크 · 도착 10분 동선\n컨시어지 데스크 · 실시간 참석 현황"),
             ("SALES", "세일즈 연결", "사전 매칭 보드 · 영업 배치 설계\n현장 기록 템플릿 · 1:1 상담 세션 운영\nD+1 맥락 팔로업 템플릿"),
             ("REPORT", "성과 리포트 · 데이터", "참석률 · 타겟 조건 일치율 · 직급 구성\n상담 기록 · 시그널 스코어링\n참석자 명단은 고객사 소유로 인계")]
    w = (CONTENT_W - GAP * 2) / 3; h = 1.5
    for i, (tag, title, desc) in enumerate(scope):
        r, c = divmod(i, 3); x = MARGIN + c * (w + GAP); y = 2.8 + r * (h + 0.22)
        d.card(s, x, y, w, h, hl=tag in ("TARGET", "SALES"))
        d.text(s, x + 0.22, y + 0.12, w - 0.44, 0.28, [(tag, O)], 9.5, bold=True, spacing=1.5)
        d.text(s, x + 0.22, y + 0.38, w - 0.44, 0.35, [(title, INK)], 13.5, bold=True)
        d.text(s, x + 0.22, y + 0.72, w - 0.44, 0.78, [(desc, BR)], 9, line_spacing=1.28)
    d.takeaway(s, [("주황 테두리 두 칸(명단·세일즈 연결)이 ", INK), ("일반 행사 대행과 갈리는 지점", OD), ("입니다.", INK)])

def s_formats(d, eb, ft):
    s = d.content_slide(eb, ft, [("규모가 아니라 ", INK), ("대화의 깊이", O), ("가 계약을 만듭니다.\n목적에 맞는 형식을 고릅니다.", INK)],
        sub="같은 방법론으로 운영한 대형 세미나와 소수 네트워킹은 성과의 종류가 달랐습니다. 형식이 결과를 가릅니다.")
    fmt_cols = ["", "소수 라운드테이블", "초청 세미나", "컨퍼런스", "커스텀 · 국제 포럼"]
    fmt_rows = [("규모", "30~50명", "100명 내외", "200~300명", "200명 이상, 다중 세션·전시"), ("타겟", "C레벨 · 임원", "실무 결정권자 + 임원", "산업 전반 결정권자·실무자", "글로벌 VIP · 파트너"),
                ("주된 성과", "상담 · 미팅 전환", "리드 + 후속 미팅", "인지도 + 리드 수", "브랜드 · 파트너십"), ("1인당 대화 시간", "길다 (10배+)", "중간", "짧다 (소수 세션 병행 권장)", "설계에 따라"),
                ("베뉴 예시", "호텔 프라이빗룸 · 조선 팰리스", "호텔 중연회장 · 호텔나루", "대연회장 · 코엑스 · FKI타워", "컨벤션센터 · 유니크 베뉴"), ("준비 기간", "8주", "8주", "8~10주", "협의")]
    cx = [MARGIN, MARGIN + 1.75, MARGIN + 4.35, MARGIN + 6.95, MARGIN + 9.55]; cwid = [1.75, 2.6, 2.6, 2.6, 2.54]; hy = 2.75
    for j, c in enumerate(fmt_cols):
        if j == 0: continue
        d.box(s, cx[j] + 0.05, hy, cwid[j] - 0.1, 0.42, fill=O if j == 1 else T["surface_warm"], radius=0.08)
        d.text(s, cx[j], hy, cwid[j], 0.42, [(c, "FFFFFF" if j == 1 else INK)], 11, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    for i, r in enumerate(fmt_rows):
        y = hy + 0.5 + i * 0.44
        d.hline(s, MARGIN, y + 0.44, CONTENT_W, color=T["line_soft"], weight=0.75)
        for j, val in enumerate(r):
            d.text(s, cx[j] + 0.12, y, cwid[j] - 0.24, 0.44, [(val, INK if j == 0 else (OD if j == 1 else BR))], 10 if j == 0 else 9.5, bold=(j == 0), align=PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, MARGIN, 5.95, CONTENT_W, 0.32, [("견적  ", OD, True), ("4,000만원~ (VAT 별도). 규모·타겟 난이도·베뉴에 따라 산정하며, 모객·운영·Show-up Guarantee를 한 견적에 담습니다. 상세 견적서는 킥오프 전 제공합니다.", SUB)], 9.5)
    d.takeaway(s, [("인지도가 목적이면 대형, 계약이 목적이면 소수. 둘 다 필요하면 ", INK), ("대형 안에 소수 세션", OD), ("을 넣습니다.", INK)])

def s_lineup(d, eb, ft):
    s = d.content_slide(eb, ft, [("행사가 유일한 답은 아닙니다.\n목적에 따라 ", INK), ("세 가지", O), (" 중에서 고르시면 됩니다.", INK)],
        sub="리멤버 Lead Gen Total Solution. 셋 다 같은 명함 데이터에서 출발하고, '타겟 설계'가 공통 엔진입니다.")
    d.numbered_cards(s, [("01 · SURVEY", "리드젠 서베이", "지금 당장 영업할 리드가 필요할 때.\n설문으로 상담 의향이 있는 분만 걸러냅니다.\n\n소요 2~4주"),
                         ("02 · ABM", "리드마그넷 & ABM", "만나야 할 기업이 정해져 있을 때.\n그 회사 의사결정권자에게 콘텐츠로 접근합니다.\n\n소요 7~9주"),
                         ("03 · MICE", "MICE 솔루션", "만나야 풀리는 딜일 때.\n모객부터 현장 운영, 사후 리포트까지 대신 돌립니다.\n\n소요 8주")], y=2.85, h=2.45, highlight=2, body_size=10.5)
    d.box(s, MARGIN, 5.5, CONTENT_W, 0.62, fill=T["surface_warm"], radius=0.08)
    d.text(s, MARGIN + 0.3, 5.5, CONTENT_W - 0.6, 0.62, [("공통 엔진  ", OD, True), ("검증된 명함 프로필 500만 → 조건 필터 → 우선순위 → 개인화 접촉. 행사 후 COLD로 분류된 리드는 다음 행사 초청 타겟으로 이관되어, 데이터가 버려지지 않고 순환합니다.", BR)], 9.8, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.3)
    d.takeaway(s, [("세 상품은 따로 도는 게 아니라, ", INK), ("하나의 데이터 위에서 리드를 순환", OD), ("시킵니다.", INK)])

def s_report(d, eb, ft):
    s = d.content_slide(eb, ft, [("행사가 끝나면 참석자 명단이 아니라\n", INK), ("'영업 파이프라인'", O), ("이 남습니다.", INK)],
        sub="종료 후 1주 안에 리포트를 드립니다. 반응이 다음 액션을 결정하고, 안 살 사람은 쫓지 않습니다.")
    lx = MARGIN; lw = 4.9
    d.card(s, lx, 2.85, lw, 3.3)
    d.text(s, lx + 0.25, 3.0, lw - 0.5, 0.3, [("성과 리포트에 담기는 것", O)], 10.5, bold=True, spacing=1)
    d.bullet_list(s, lx + 0.25, 3.4, lw - 0.5, ["사전등록 대비 참석률 · 확정자 대비 참석률", "타겟 조건 일치율 · 직급 구성 (C레벨/부장·팀장/실무)", "세션·부스 반응, 1:1 상담 기록 (누구와·무엇을·다음 약속)",
                                               "리드별 시그널 스코어 (HOT / WARM / COLD)", "후속 액션 제안 · 다음 행사 타겟 재구성 제안", "쇼업 완료 리드 전체를 D+1 영업일에 인계 (명단은 고객사 소유)"], size=10, gap=0.4)
    d.text(s, lx + 0.25, 5.8, lw - 0.5, 0.35, [("행사 전에는 고객사 전용 리드 대시보드에서 등록 현황과 리드 스코어링을 실시간으로 확인합니다.", SUB)], 8.8, line_spacing=1.25)
    rx = MARGIN + lw + 0.35; rw = CONTENT_W - lw - 0.35
    sig = [("HOT", O, "답장 · 미팅 수락 · 자료 2개 이상 열람", "48시간 내 실무 미팅 제안. 세일즈가 직접, 전화 우선. 여기서 파이프라인이 열립니다."),
           ("WARM", ST, "메일 오픈 · 자료 1회 다운로드", "주 1회 맞춤 콘텐츠(사례·비교자료)로 온도 상승 유도. 3주 연속 오픈 시 HOT 전환 시도."),
           ("COLD", MUT, "2주 이상 무반응", "중단이 아니라 순환. 다음 행사 초청 타겟으로 이관, 행사가 다시 온도를 올리는 장치가 됩니다.")]
    for i, (lab, col, cond, act) in enumerate(sig):
        y = 2.85 + i * 1.12
        d.card(s, rx, y, rw, 1.0); d.box(s, rx, y, 0.1, 1.0, fill=col, radius=0)
        d.text(s, rx + 0.3, y + 0.1, 1.1, 0.4, [(lab, col)], 15, bold=True, spacing=1)
        d.text(s, rx + 1.4, y + 0.12, rw - 1.6, 0.35, [(cond, INK)], 10, bold=True)
        d.text(s, rx + 1.4, y + 0.45, rw - 1.6, 0.55, [(act, BR)], 9, line_spacing=1.25)
    d.takeaway(s, [("전원에게 같은 메일 3통보다, ", INK), ("HOT 5팀에 15번의 맞춤 접촉", OD), ("이 계약을 만듭니다.", INK)])

# ── 04 MICE 비즈팀 ───────────────────────────────────────────────
def s_org(d, eb, ft):
    s = d.content_slide(eb, ft, [("데이터 회사 안에 MICE 전문 조직이 있습니다.\n세 팀이 ", INK), ("하나의 데이터", O), (" 위에서 한 행사를 돌립니다.", INK)],
        sub="타겟은 리드젠팀이, 현장은 MICE 비즈팀이, 계약은 리드세일즈팀이. 고객사는 한 창구만 상대합니다.")
    d.box(s, MARGIN + 2.3, 2.8, 7.5, 0.62, fill=CH, radius=0.08)
    d.text(s, MARGIN + 2.3, 2.8, 7.5, 0.62, [("리멤버 마켓솔루션본부 · Lead Gen Total Solution", "F4F0E9", True, 13), ("   |   마켓데이터사업실 · 광고사업실", "A89F92")], 11, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    d.vline(s, MARGIN + 6.05, 3.42, 0.28, color=T["line"], weight=1)
    d.hline(s, MARGIN + 1.9, 3.7, 8.3, color=T["line"], weight=1)
    teams = [("리드젠프로젝트팀", "팀장 신주은", "TARGET", "타겟 조건 설계 · 초청 후보 모수 산출\n기업 리스트 매칭 · 개인화 초청 · RSVP", False),
             ("MICE 비즈팀", "팀장 이진철 · 4인", "SHOW-UP · ON-SITE", "행사 기획 · 베뉴·무대·디자인 프로듀싱\n리마인드 운영표 · 현장 PM · 성과 리포트", True),
             ("리드세일즈팀", "팀장 김현래", "SALES", "사전 매칭 · 영업 배치 설계\n현장 기록 · D+1 팔로업 · 시그널 너처링", False)]
    w = 3.8
    for i, (nm, lead, tag, desc, hl) in enumerate(teams):
        x = MARGIN + 0.1 + i * (w + 0.35); cxm = x + w / 2
        d.vline(s, cxm, 3.7, 0.25, color=T["line"], weight=1)
        d.card(s, x, 3.95, w, 1.55, hl=hl)
        if hl: d.grad(s, x, 3.95, w, 0.09, radius=0)
        d.text(s, x + 0.25, 4.08, w - 0.5, 0.28, [(tag, O)], 9, bold=True, spacing=1.5)
        d.text(s, x + 0.25, 4.34, w - 0.5, 0.4, [(nm, INK, True, 15), ("   " + lead, SUB, False, 10)], 15, bold=True)
        d.text(s, x + 0.25, 4.78, w - 0.5, 0.7, [(desc, BR)], 9.5, line_spacing=1.3)
    d.card(s, MARGIN, 5.65, 6.75, 0.6)
    d.text(s, MARGIN + 0.25, 5.65, 6.3, 0.6, [("현장 인력 풀  ", OD, True, 9.5), ("검증된 PM·테크니션·디자인·의전 인력 네트워크를 행사 규모에 맞춰 편성합니다", BR)], 9.5, anchor=MSO_ANCHOR.MIDDLE)
    d.card(s, MARGIN + 7.0, 5.65, CONTENT_W - 7.0, 0.6)
    d.text(s, MARGIN + 7.25, 5.65, CONTENT_W - 7.5, 0.6, [("자사 행사  ", OD, True, 9.5), ("REBUILD26 · DMS 2026 등 리멤버 주최 컨퍼런스 직접 운영", BR)], 9.5, anchor=MSO_ANCHOR.MIDDLE)
    d.takeaway(s, [("2026년 9월, MICE 사업을 더 빠르게 키우기 위해 ", INK), ("MICE 비즈팀을 신설", OD), ("했습니다.", INK)])

def s_leader(d, eb, ft):
    s = d.content_slide(eb, ft, [("정부 국제회의부터 초대형 박람회까지,\n", INK), ("18년", O), ("의 MICE 운영 전문가가 팀을 이끕니다.", INK)],
        sub="현장 실무에서 시작해 PM, 전시·컨벤션 기획, 신사업 모델 설계까지. 리멤버 MICE의 운영 표준은 이 경력에서 나왔습니다.")
    lx, ly, lw, lh = MARGIN, 2.8, 4.3, 3.35
    d.box(s, lx, ly, lw, lh, fill=CH, radius=0.12)
    d.dot(s, lx + 0.85, ly + 0.8, r=0.55, color=T["brown"])
    d.text(s, lx + 0.3, ly + 0.25, 1.1, 1.1, [("JL", OS)], 20, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=1)
    d.text(s, lx + 1.65, ly + 0.35, lw - 1.9, 0.5, [("이진철", "FFFFFF")], 24, bold=True)
    d.text(s, lx + 1.65, ly + 0.9, lw - 1.9, 0.5, [("MICE 비즈팀 팀장 · MICE 운영 총괄", OS)], 10.5, bold=True)
    facts = [("18년", "MICE 업력 · 현장 실무 → PM → 기획 → 신사업"), ("국제회의 → 박람회", "정부 국제회의부터 초대형 박람회까지 직접 운영"),
             ("2만명 규모", "단일 행사 최대 운영 규모 · 3일 · 100개+ 부스"), ("2025~", "리멤버 MICE 모객 솔루션 기획 단계부터 참여")]
    for i, (v, lab) in enumerate(facts):
        y = ly + 1.6 + i * 0.42
        d.text(s, lx + 0.3, y, 1.6, 0.4, [(v, OS)], 12.5, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        d.text(s, lx + 1.85, y, lw - 2.1, 0.4, [(lab, "CFC8BC")], 9, anchor=MSO_ANCHOR.MIDDLE)
    rx = MARGIN + lw + 0.3; rw = CONTENT_W - lw - 0.3
    d.text(s, rx, 2.78, rw, 0.3, [("운영 경험의 범위 · 유형별 규모와 역할", INK)], 11, bold=True)
    d.hline(s, rx, 3.1, rw, color=T["line"], weight=0.75)
    recs = [("정부 국제회의", "정부 주최 국제회의 · 다수 경제체 대표단 의전 · 장차관급 참석", "국제회의"),
            ("초대형 박람회 · 마켓", "2만명 규모 박람회 · 100개+ 부스 · 전시·마켓·비즈니스 미팅 통합 운영", "박람회"),
            ("국제학회 · 컨퍼런스", "50개국+ · 1,000명+ 규모 · 다중 세션 · 사전등록·현장 등록 시스템", "국제학회"),
            ("국무총리·장차관급 회의", "정부 협의체 · 의전 동선 · 보안·경호 협조 · 국빈급 세리머니", "고위급"),
            ("기업 컨퍼런스 · 세미나", "결정권자 초청 · 라운드테이블 · 1:1 상담 세션 설계 · 리드 연계", "기업행사"),
            ("B2B 상담회 · 트래블마트", "바이어·셀러 1:1 사전 매칭 · 노쇼 방지 운영 · 상담 성과 집계", "B2B 상담회"),
            ("공모전 · 해커톤 · 시상식", "연중 장기 프로젝트 · 교육·멘토링·결선·시상 통합 운영", "장기 프로젝트"),
            ("모객 솔루션 기획", "명함 데이터 기반 참가자 모객 솔루션을 리멤버와 공동 기획 · 상품화", "신사업")]
    for i, (t, desc, tag) in enumerate(recs):
        y = 3.2 + i * 0.385
        d.text(s, rx, y, 2.55, 0.36, [(t, INK)], 10, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        d.text(s, rx + 2.55, y, 3.65, 0.36, [(desc, BR)], 9, anchor=MSO_ANCHOR.MIDDLE)
        d.pill(s, rx + rw - 1.25, y + 0.04, 1.25, 0.28, tag, fill=OT, color=OD, size=9, bold=True)
        d.hline(s, rx, y + 0.385, rw, color=T["line_soft"], weight=0.5)
    d.takeaway(s, [("국빈급 의전과 2만명 규모 운영을 해본 사람이, ", INK), ("30명 라운드테이블의 디테일", OD), ("을 설계합니다.", INK)])

def s_members(d, eb, ft):
    s = d.content_slide(eb, ft, [("국제회의 · BTL · 기업회의 · B2B 컨퍼런스,\n", INK), ("네 가지 전문성", O), ("이 한 팀에 있습니다.", INK)],
        sub="행사 유형마다 운영 문법이 다릅니다. 각 유형을 직접 운영해 온 사람이 맡습니다.")
    people = [("이진철", "팀장 · MICE 운영 총괄", "JL", "18년 MICE 운영 전문가",
               "정부 국제회의부터 초대형 박람회까지 현장 실무·PM·전시컨벤션 기획·신사업 설계를 거쳤습니다.\n리멤버 MICE 모객 솔루션을 기획 단계부터 함께 만들었고, 전체 행사의 PM과 품질을 총괄합니다."),
              ("이왕희", "BTL 운영 전문가", "WL", "브랜드 체험 · 프로모션 · 현장 이벤트",
               "리멤버 마켓필드(필드마케팅) 출신으로 브랜드 체험·프로모션·로드쇼 등 BTL 현장 운영을 맡아 왔습니다.\n행사 운영 스레드와 리마인드 운영표, 현장 연출·디자인 기획, 사후 리포트를 담당합니다."),
              ("곽은지", "기업회의 · 국제회의 전문가", "EK", "컨퍼런스 · 포럼 · 국제회의",
               "기업 컨퍼런스와 포럼, 국제회의의 기획·운영 전문가입니다.\n베뉴·의전·프로그램 운영과 RSVP 확정 콜, 참가자 커뮤니케이션, 만족도 조사까지 참가자 여정 전체를 담당합니다."),
              ("조민하", "B2B 컨퍼런스 전문가", "MC", "자사 B2B 컨퍼런스 · 파트너 운영",
               "리멤버 필드마케팅 출신 B2B 컨퍼런스 기획·운영 전문가입니다.\nREBUILD26 등 자사 컨퍼런스 경험을 바탕으로 고객사 킥오프, WBS·운영정책서, 연사·파트너 커뮤니케이션을 맡습니다.")]
    w = (CONTENT_W - GAP) / 2; h = 1.6
    for i, (nm, role, ini, tagline, desc) in enumerate(people):
        r, c = divmod(i, 2); x = MARGIN + c * (w + GAP); y = 2.75 + r * (h + 0.18)
        d.box(s, x, y, w, h, fill=CH, radius=0.12)
        if i == 0: d.grad(s, x, y, 0.1, h, radius=0)
        d.dot(s, x + 0.65, y + 0.65, r=0.45, color=T["brown"])
        d.text(s, x + 0.2, y + 0.2, 0.9, 0.9, [(ini, OS)], 14, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=1)
        d.text(s, x + 1.3, y + 0.14, w - 1.5, 0.35, [(nm, "FFFFFF", True, 15), ("   " + role, OS, True, 10)], 15, bold=True)
        d.text(s, x + 1.3, y + 0.46, w - 1.5, 0.26, [(tagline, "A89F92")], 9, bold=True)
        d.text(s, x + 1.3, y + 0.72, w - 1.5, h - 0.78, [(desc, "CFC8BC")], 9, line_spacing=1.25)
    d.takeaway(s, [("고객사는 담당 PM 한 명과 이야기하고, ", INK), ("네 사람의 전문성", OD), ("이 그 뒤에서 움직입니다.", INK)])

def s_dataleaders(d, eb, ft):
    s = d.content_slide(eb, ft, [("타겟과 세일즈는 리멤버 데이터 전문가들이\n", INK), ("같은 데이터", O), (" 위에서 함께 설계합니다.", INK)],
        sub="MICE 비즈팀이 현장을 맡는 동안, 명단과 계약은 이 세 사람의 팀이 책임집니다.")
    for nm, fn in [("w019.jpg", "p_joo.jpg"), ("w020.jpg", "p_shin.jpg"), ("w021.jpg", "p_kim.jpg")]:
        gray_png(P("webinar", nm), os.path.join(IMG, fn))
    people = [("주대웅", "마켓데이터사업실장", os.path.join(IMG, "p_joo.jpg"), "데이터 · 타겟팅 · 현장 운영 총괄",
               "마켓데이터사업실 총괄. MICE 사업을 기획 단계부터 이끌어 왔고, 데이터·타겟팅·현장 운영을 총괄합니다.\n웨비나 '행사는 성공했는데, 매출은 왜 없을까' 쇼업 세션 연사."),
              ("신주은", "리드젠프로젝트팀 팀장", os.path.join(IMG, "p_shin.jpg"), "타겟 초청 · 기업 리스트 매칭",
               "프로필 500만에서 '와야 할 사람'을 고르는 타겟 설계 방법론(데이터 → 필터 → 스코어 → 초청, 버리는 기준)을 담당합니다.\n등록 현황 대시보드와 리드 납품 정책을 운영합니다."),
              ("김현래", "리드세일즈팀 팀장", os.path.join(IMG, "p_kim.jpg"), "세일즈 · 팔로업 · 전환",
               "현장 대화를 파이프라인으로 잇는 5칸 방법론(매칭 → 동선 → 기록 → D+1 인용 → 시그널 너처링)을 담당합니다.\n계약 후 고객사 킥오프와 사후 전환을 함께 설계합니다.")]
    w = (CONTENT_W - GAP * 2) / 3; h = 3.2; y = 2.8
    for i, (nm, role, photo, tagline, desc) in enumerate(people):
        x = MARGIN + i * (w + GAP)
        d.box(s, x, y, w, h, fill=CH, radius=0.12)
        cp = circle_png(photo, os.path.join(IMG, f"circ_dl_{i}.png"), size=600)
        s.shapes.add_picture(cp, Inches(x + 0.3), Inches(y + 0.3), Inches(1.1), Inches(1.1))
        d.text(s, x + 1.6, y + 0.35, w - 1.8, 0.45, [(nm, "FFFFFF")], 18, bold=True)
        d.text(s, x + 1.6, y + 0.8, w - 1.8, 0.3, [(role, OS)], 10.5, bold=True)
        d.text(s, x + 1.6, y + 1.1, w - 1.8, 0.3, [(tagline, "A89F92")], 9, bold=True)
        d.hline(s, x + 0.3, y + 1.62, w - 0.6, color=T["d_border"], weight=0.75)
        d.text(s, x + 0.3, y + 1.75, w - 0.6, h - 1.85, [(desc, "CFC8BC")], 9.2, line_spacing=1.3)
    d.takeaway(s, [("타겟은 리드젠팀, 현장은 MICE 비즈팀, 계약은 리드세일즈팀. ", INK), ("고객사는 한 창구", OD), ("만 상대합니다.", INK)])

def s_expertise(d, eb, ft):
    s = d.content_slide(eb, ft, [("운영은 ", INK), ("행사 경험 100건 이상의 PM", O), ("이 맡습니다.\n전문성은 네 가지로 증명합니다.", INK)],
        sub="국빈급 국제회의를 운영해 온 사람들의 방법론에, 리멤버의 데이터를 더했습니다.")
    d.numbered_cards(s, [("01 · CONVENTION", "국제회의·박람회 운영 경험", "정부 국제회의부터 초대형 박람회까지, 정부 국제회의·국제학회·기업 컨퍼런스·B2B 상담회를 18년간 운영한 팀장이 직접 PM을 맡습니다.\n국빈급 의전과 2만명 규모 운영을 거친 표준으로 30명 행사도 설계합니다."),
                         ("02 · VENUE", "베뉴·F&B 협상력", "서울 주요 호텔 20곳+의 최신 견적·도면·메뉴 보유.\n대관료 대비 F&B 상계, 야간 설치, VIP 동선까지 표준 답사 체크리스트로 확인하고 협상합니다."),
                         ("03 · PRODUCTION", "무대·기술 프로듀싱", "LED 미디어월·스위칭·프롬프터·음향 설계, 키비주얼부터 명찰까지 풀 디자인.\n셀프 체크인 키오스크와 컨시어지 데스크로 '도착 10분'을 설계합니다."),
                         ("04 · ONE DATA", "데이터 원팀 운영", "타겟 설계 → 리마인드 → 현장 기록 → 팔로업이 하나의 데이터로 흐릅니다.\n등록 현황 실시간 공유, 운영정책서 기반 킥오프, 종료 후 1주 리포트.")], y=2.85, h=3.05, highlight=3, body_size=9.8)
    d.takeaway(s, [("행사를 잘 운영하는 회사는 많습니다. ", INK), ("누가 왔는지까지 책임지는 회사", OD), ("는 드뭅니다.", INK)])

def s_venue(d, eb, ft):
    s = d.content_slide(eb, ft, [("서울 주요 호텔 ", INK), ("20곳", O), ("의\n최신 견적과 도면을 이미 갖고 있습니다.", INK)],
        sub="행사 목적과 규모에 맞는 베뉴를 즉시 비교 제안합니다. 대관료·F&B·설비 조건 협상까지 저희 일입니다.")
    venues = [("JW 메리어트 서울", "강남"), ("그랜드 인터컨티넨탈 서울 파르나스", "강남"), ("웨스틴 서울 파르나스", "강남"), ("조선 팰리스 서울 강남", "강남"),
              ("콘래드 서울", "여의도"), ("호텔 신라 서울", "강북"), ("포시즌스 호텔 서울", "강북"), ("롯데호텔 서울", "강북"),
              ("안다즈 서울 강남", "강남"), ("페어몬트 앰배서더 서울", "여의도"), ("소피텔 앰배서더 서울", "잠실"), ("파크 하얏트 서울", "강남"),
              ("호텔나루 서울 엠갤러리", "마포"), ("노보텔 앰배서더 강남", "강남"), ("르메르디앙 · 목시 서울 명동", "강북"), ("오크우드 프리미어 코엑스", "강남"),
              ("더 플라자", "강북"), ("반얀트리 클럽 앤 스파 서울", "강북"), ("글래드 여의도", "여의도"), ("서울드래곤시티", "용산"),
              ("코엑스 컨벤션센터", "강남"), ("FKI타워 컨퍼런스센터", "여의도"), ("GS타워 아모리스홀", "강남"), ("파이팩토리 · 유니크 베뉴", "성수")]
    w = (8.4 - 0.15 * 3) / 4; h = 0.44
    for i, (nm, reg) in enumerate(venues):
        r, c = divmod(i, 4); x = MARGIN + c * (w + 0.15); y = 2.78 + r * (h + 0.09)
        d.box(s, x, y, w, h, fill=T["surface"] if i < 20 else T["surface_warm"], line=T["border"], radius=0.25)
        d.text(s, x + 0.12, y, w - 0.62, h, [(nm, INK)], 9, bold=True, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0)
        d.text(s, x + w - 0.62, y, 0.55, h, [(reg, MUT)], 9, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    rx = MARGIN + 8.7; rw = CONTENT_W - 8.7
    d.card(s, rx, 2.8, rw, 3.3, hl=True)
    d.text(s, rx + 0.25, 2.95, rw - 0.5, 0.3, [("표준 답사 체크리스트로 확인하는 것", O)], 10, bold=True)
    d.bullet_list(s, rx + 0.25, 3.35, rw - 0.5, ["대관료 포함 항목 · 시간대별 비용 · 취소 규정", "세팅 타입별 수용 인원 · 무대·층고 · 니쥬", "LED 픽셀 · 하우스 음향 · 인터넷 회선", "VIP 룸·동선 · 주차 · 화물 엘리베이터", "커피브레이크 공간 · 특이식성 메뉴", "야간 설치·철거 가능 여부와 추가비"], size=9.5, gap=0.42)
    d.text(s, MARGIN, 5.98, 8.4, 0.3, [("5성급 중심 호텔 20곳 + 컨벤션·유니크 베뉴 4곳 · 2026년 견적서·도면·메뉴 기준 · 지방 및 신규 베뉴는 답사 후 제안", MUT)], 9)
    d.takeaway(s, [("대관료의 80%까지 F&B로 상계하는 등, ", INK), ("조건 협상까지 저희 일", OD), ("입니다.", INK)])

# ── 05 레퍼런스 ─────────────────────────────────────────────────
def s_collage(d, eb, ft):
    s = d.content_slide(eb, ft, [("2026년, 이 설계는 ", INK), ("매달 현장", O), ("에서 검증되고 있습니다.", INK)],
        sub="대기업 컨퍼런스부터 소수 정예 라운드테이블, 네트워킹 디너까지. 리멤버 MICE가 직접 운영한 현장입니다.")
    shots = [("w002.jpg", "물류 IT 컨퍼런스 세션장", "C사 물류 컨퍼런스 · 판교 · 2026.4"), ("w014.jpg", "CXO 라운드테이블", "C레벨 소수 네트워킹 · 2026.2"),
             ("w015.jpg", "리멤버 REBUILD26", "코엑스 · 2026.5 · 등록 809명, 참석 527명"), ("w016.jpg", "패션·뷰티 해외진출 세미나", "서울 호텔 · 2026.2"),
             ("w018.jpg", "1:1 비즈니스 미팅 세션", "현장 상담 설계 · 사전 매칭 보드 운영"), ("w007.jpg", "등록 데스크 · 도착 10분 동선", "C사 컨퍼런스 현장 · 2026.4")]
    w = (CONTENT_W - 0.22 * 2) / 3; ph = 1.42; ch_ = 0.5
    for i, (fn, t1, t2) in enumerate(shots):
        r, c = divmod(i, 3); x = MARGIN + c * (w + 0.22); y = 2.62 + r * (ph + ch_ + 0.16)
        d.picture(s, P("webinar", fn), x, y, w, ph)
        d.box(s, x, y + ph, w, ch_, fill=CH, radius=0)
        d.text(s, x + 0.15, y + ph + 0.04, w - 0.3, 0.25, [(t1, "FFFFFF")], 9.5, bold=True)
        d.text(s, x + 0.15, y + ph + 0.26, w - 0.3, 0.22, [(t2, OS)], 7.8)

def s_reftable(d, eb, ft):
    s = d.slide(); d.nav(s, eb, ft)
    d.headline(s, [("보안·이커머스·물류·리테일·SaaS까지,\n2026년 리멤버 MICE가 만든 ", INK), ("현장", O), ("입니다.", INK)])
    # 고객사 실명·행사명은 가명 예시(실제 덱은 고객 동의분만 실명 주입 — RULE-NO-COMPANY v2).
    refs = [("B사", "패션·뷰티 해외진출 전략 세미나", "2026.2", "서울 호텔", "초청 세미나 + 1:1 상담"),
            ("C사", "물류 컨퍼런스", "2026.4", "판교", "컨퍼런스 · 100개사 참석 보장"),
            ("D사", "고객 초청 세미나 (ABM 캠페인 병행)", "2026.4", "서울", "소수 초청 세미나"),
            ("E사", "리테일 CX 라운드테이블", "2026.4", "서울 호텔", "라운드테이블 · 40명 보장"),
            ("리멤버", "REBUILD26 컨퍼런스 · AI 시대 B2B의 RE:BUILD", "2026.5", "코엑스", "컨퍼런스 · 등록 809명 · 참석 527명"),
            ("F사", "F&B 임원 브리핑", "2026.5", "서울 호텔", "이사급 이상 임원 세미나 · RSVP"),
            ("G사", "대표이사 대상 절세 전략 세미나", "2026.6", "서울 호텔", "소수 세미나 · 40명 보장"),
            ("H사", "사이버 보안 컨퍼런스", "2026.7", "서울 호텔", "컨퍼런스 · 신규 60명 + 고객 200명+"),
            ("A사", "AI 보안 컨퍼런스", "2026.7", "서울 호텔", "보안 임원 컨퍼런스 · 180명 보장"),
            ("I사", "이커머스 컨퍼런스", "2026.7", "서울 컨벤션홀", "컨퍼런스 300명 · 리멤버 100명 모객"),
            ("J사", "제조 신규 고객 초청 세미나", "2026.8", "서울 호텔", "제조 결정권자 · 20명 보장"),
            ("L사", "보안 임원 초청 세미나", "2026.9", "서울 호텔", "보안 임원 초청 세미나 · 50명")]
    hdr = ["고객사", "행사", "일시", "장소", "형식 · 규모"]
    cx = [MARGIN, MARGIN + 1.85, MARGIN + 6.35, MARGIN + 7.3, MARGIN + 9.55]; cwid = [1.85, 4.5, 0.95, 2.25, 2.54]; hy = 2.35
    d.box(s, MARGIN, hy, CONTENT_W, 0.36, fill=T["surface_warm"], radius=0.06)
    for j, c in enumerate(hdr):
        d.text(s, cx[j] + 0.12, hy, cwid[j] - 0.24, 0.36, [(c, INK)], 9.5, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    for i, r in enumerate(refs):
        y = hy + 0.42 + i * 0.29
        d.hline(s, MARGIN, y + 0.29, CONTENT_W, color=T["line_soft"], weight=0.5)
        for j, val in enumerate(r):
            d.text(s, cx[j] + 0.12, y, cwid[j] - 0.24, 0.29, [(val, OD if j == 0 else (INK if j == 1 else BR))], 9 if j != 1 else 9.2, bold=(j in (0, 1)), anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, MARGIN, 6.28, CONTENT_W, 0.3, [("12건 모두 2026년 실집행 기준. 참석률·타겟 일치율 등 성과 수치는 고객사 요청에 따라 다음 장에서 익명으로 표기합니다. 하반기 예정 행사는 '자사 주최·예정' 장 참고.", MUT)], 8.5)
    d.text(s, MARGIN, 6.62, CONTENT_W, 0.4, [("2026년 한 해에만 ", INK), ("보안·클라우드·이커머스·물류·리테일·제조", OD), ("의 결정권자를 현장으로 모았습니다.", INK)], 13, bold=True, align=PP_ALIGN.CENTER)

def s_kpi(d, eb, ft):
    s = d.content_slide(eb, ft, [("같은 예산으로 다른 결과.\n", INK), ("숫자", O), ("로 증명합니다.", INK)],
        sub="2026년 실집행 행사의 실측값입니다. 고객사 요청으로 익명 처리했습니다.")
    kp = [("75%", "타겟 조건 일치 참석자", "A사 168명 실측\n(광고 모집형은 10%)", True), ("82%", "확인 통과자 참석률", "콜 → 확정폼 → D-1 확인 통과자\n행사별 82~107%", False),
          ("193%", "KPI 대비 최대 실참석", "K사 30명 → 58명\n4개 행사 평균 145%", False), ("1.8배", "REBUILD26 3주 회수", "실집행 1.61억 → 수주 2.89억\n2026.5.28 집계, 진행 딜 미반영", False)]
    w = (CONTENT_W - GAP * 3) / 4
    for i, (num, top, bot, solid) in enumerate(kp):
        d.kpi(s, MARGIN + i * (w + GAP), 2.85, w, 2.2, num, top=top, bottom=bot, solid=solid, num_size=40)
    d.card(s, MARGIN, 5.22, CONTENT_W, 0.95)
    d.text(s, MARGIN + 0.3, 5.28, 3.2, 0.85, [("가이드 사례 · L사 고객초청 세미나\n", INK, True, 10.5), ("직접 운영이 아니라 설계만 이식한 행사", SUB)], 9, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.3)
    for i, (v, lab) in enumerate([("9% → 41%", "등록자 중 의사결정권자 비중"), ("33% → 58%", "사전등록 대비 참석률"), ("27건", "행사 후 4주 내 후속 미팅")]):
        x = MARGIN + 3.7 + i * 2.8
        d.text(s, x, 5.3, 2.7, 0.45, [(v, OD)], 17, bold=True); d.text(s, x, 5.75, 2.7, 0.3, [(lab, SUB)], 9)
    d.takeaway(s, [("설계가 이식되면, ", INK), ("같은 예산으로 다른 결과", OD), ("가 나옵니다.", INK)])

def s_heritage(d, eb, ft):
    s = d.content_slide(eb, ft, [("정부 국제회의부터 대형 국제학회까지,\n", INK), ("18년간 직접 운영해 온 현장", O), ("입니다.", INK)],
        sub="MICE 비즈팀 팀장이 총괄·수행해 온 대표 실적. 리멤버 MICE의 운영 표준은 이 현장들에서 나왔습니다.")
    for i, (v, lab) in enumerate([("18년", "MICE 운영 업력"), ("{{n}}건", "리멤버 집행 실적(주입)"), ("{{max_pax}}명", "단일 행사 최다 동원(주입)"), ("{{max_countries}}개국", "최다 참가국(주입)")]):
        y = 2.8 + i * 0.85
        d.card(s, MARGIN, y, 2.35, 0.72)
        d.text(s, MARGIN + 0.2, y + 0.05, 2.0, 0.4, [(v, O)], 18, bold=True); d.text(s, MARGIN + 0.2, y + 0.42, 2.0, 0.28, [(lab, SUB)], 8.5)
    photos = [("s28_image69.jpeg", "대표 실적 사진 1 · {{연도}}"), ("s28_image74.jpeg", "대표 실적 사진 2 · {{연도}}"), ("s29_image86.jpeg", "대표 실적 사진 3 · {{연도}}"), ("s28_image73.jpeg", "대표 실적 사진 4 · {{연도}}")]
    px0 = MARGIN + 2.6; pw = 2.35; ph = 1.42
    for i, (fn, cap) in enumerate(photos):
        r, c = divmod(i, 2); x = px0 + c * (pw + 0.12); y = 2.8 + r * (ph + 0.32)
        d.picture(s, P("v5", fn), x, y, pw, ph); d.text(s, x, y + ph + 0.02, pw, 0.26, [(cap, MUT)], 8.5)
    lx = px0 + 2 * pw + 0.45; lw = CONTENT_W - (lx - MARGIN)
    d.text(s, lx, 2.72, lw, 0.3, [("규모·등급별 대표 실적", INK)], 10.5, bold=True)
    # 실명 실적은 리멤버 명의·고객 동의분만 주입한다(RULE-NO-COMPANY v2). 아래는 슬롯 예시.
    groups = [("정부 회의", "{{대표 실적 1}}"), ("국제회의", "{{대표 실적 2}}"),
              ("국제학회", "{{대표 실적 3}}"), ("50개국+", "{{대표 실적 4}}"),
              ("20개국+", "{{대표 실적 5}}"), ("500명+ 컨퍼런스", "{{대표 실적 6}}"),
              ("박람회 · 마켓", "{{대표 실적 7}}")]
    for i, (g, ev) in enumerate(groups):
        y = 3.08 + i * 0.44
        d.text(s, lx, y, 1.45, 0.42, [(g, OD)], 9, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        d.text(s, lx + 1.5, y, lw - 1.5, 0.42, [(ev, BR)], 9, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.15)
        d.hline(s, lx, y + 0.44, lw, color=T["line_soft"], weight=0.5)
    d.takeaway(s, [("국빈급 의전과 1,000명 규모 운영 노하우가, ", INK), ("30명 라운드테이블의 디테일", OD), ("에도 그대로 들어갑니다.", INK)])

def s_own(d, eb, ft):
    s = d.content_slide(eb, ft, [("고객사 행사만이 아닙니다.\n같은 방법론으로 ", INK), ("저희 행사", O), ("도 엽니다.", INK)],
        sub="리멤버가 직접 주최하는 컨퍼런스에 이 설계를 그대로 적용합니다. 다음은 '기업 대표만' 모십니다.")
    own = [("2026.5.7 · 코엑스", "REBUILD26", "AI 시대 B2B의 RE:BUILD", "등록 809명 · 참석 527명 · 부스 상담 184건\n당일 견적 요청 35건(28개사) · 3주 뒤 수주 2.89억"),
           ("2024.9 · 2025.4", "HR Leaders' Insight", "GS타워 아모리스홀 · 엘타워", "핵심 참석자 350+ · 연사 8인 · 2회 연속 개최\nCEO 세션 · Insight Talk · 워크숍 연계"),
           ("2026.10.15 · 코엑스 컨퍼런스홀", "Decision Makers Summit 2026", "The AI-Powered CEO", "참가 자격 기업 대표 only · 300개사 이상\n9월 중순 사전신청 460명+ · 스폰서 파트너 참여 중")]
    w = (CONTENT_W - GAP * 2) / 3
    for i, (when, nm, sub_, desc) in enumerate(own):
        x = MARGIN + i * (w + GAP); hero = (i == 2)
        if hero: d.grad(s, x, 2.8, w, 2.3, radius=0.08); c1, c2, c3, c4 = "FFF1E6", "FFFFFF", "FFF1E6", "FFFFFF"
        else: d.card(s, x, 2.8, w, 2.3); c1, c2, c3, c4 = O, INK, SUB, BR
        d.text(s, x + 0.25, 2.93, w - 0.5, 0.3, [(when, c1)], 9.5, bold=True, spacing=1)
        d.text(s, x + 0.25, 3.22, w - 0.5, 0.5, [(nm, c2)], 16.5 if len(nm) > 14 else 19, bold=True)
        d.text(s, x + 0.25, 3.7, w - 0.5, 0.35, [(sub_, c3)], 10.5, bold=True)
        d.text(s, x + 0.25, 4.1, w - 0.5, 0.95, [(desc, c4)], 9.8, line_spacing=1.35)
    d.text(s, MARGIN, 5.25, CONTENT_W, 0.3, [("2026 하반기 예정 · 고객사 행사", INK)], 10.5, bold=True)
    up = [("M사", "CXO 서밋 · 서울 호텔 · 10.20"), ("N사", "테크 데이 · 부산 호텔 · 10.29"), ("I사", "이커머스 서밋 · 코엑스 · 12.10 · 운영 총괄")]  # 가명 예시
    uw = (CONTENT_W - 0.2 * 2) / 3
    for i, (co, ev) in enumerate(up):
        x = MARGIN + i * (uw + 0.2)
        d.box(s, x, 5.58, uw, 0.6, fill=T["surface_warm"], radius=0.08)
        d.text(s, x + 0.2, 5.58, uw - 0.4, 0.6, [(co + "  ", OD, True, 10), (ev, BR)], 9.2, anchor=MSO_ANCHOR.MIDDLE)
    d.takeaway(s, [("대표님들 앞에서 이야기할 것이 있으시다면, ", INK), ("DMS 2026의 자리", OD), ("도 열려 있습니다.", INK)])

# ── 06 시작하기 ─────────────────────────────────────────────────
def s_next(d, eb, ft):
    s = d.content_slide(eb, ft, [("시작은 이메일 한 통입니다.\n조건에 맞는 ", INK), ("초청 후보가 몇 명인지", O), (" 먼저 뽑아드립니다.", INK)],
        sub="회사명과 만나고 싶은 산업·직급만 보내주세요. 계약 전에 명단의 규모와 형식을 먼저 확인하실 수 있습니다.")
    steps = [("STEP 1 · 무료", "초청 후보 모수 산출", "회사명 + 만나고 싶은 산업·직급을 보내주시면\n검증된 프로필 500만에서 조건에 맞는 초청 후보 규모와\n적합한 형식·베뉴를 제안드립니다.", "2영업일"),
             ("STEP 2 · D-8주", "킥오프", "목표 인원 · 명단 조건 · 형식 · 베뉴 확정\n운영정책서 공유: 역할 분담, 리마인드 운영표,\n현장 매뉴얼, 개인정보 처리 기준", "1회 미팅"),
             ("STEP 3 · D-7주 ~ D+1주", "실행과 리포트", "모객 → 확인 사다리 → 130% 버퍼 → 현장 운영\n사전 매칭 · 현장 기록 → 종료 후 1주 성과 리포트\nShow-up Guarantee 적용", "8주")]
    w = (CONTENT_W - GAP * 2) / 3
    for i, (tag, title, desc, dur) in enumerate(steps):
        x = MARGIN + i * (w + GAP)
        d.card(s, x, 2.85, w, 2.6, hl=(i == 0))
        if i == 0: d.grad(s, x, 2.85, w, 0.09, radius=0)
        d.text(s, x + 0.25, 3.0, w - 0.5, 0.3, [(tag, O)], 10, bold=True, spacing=1.2)
        d.text(s, x + 0.25, 3.3, w - 0.5, 0.5, [(title, INK)], 18, bold=True)
        d.text(s, x + 0.25, 3.85, w - 0.5, 1.2, [(desc, BR)], 9.8, line_spacing=1.35)
        d.pill(s, x + 0.25, 5.0, 1.3, 0.32, "소요 " + dur, fill=OT, color=OD, size=9)
        if i < 2: d.chevron(s, x + w + 0.03, 3.9, w=0.27, h=0.5)
    d.box(s, MARGIN, 5.65, CONTENT_W, 0.55, fill=CH, radius=0.08)
    d.text(s, MARGIN + 0.3, 5.65, CONTENT_W - 0.6, 0.55, [("문의  ", OS, True), ("mice_solution@remember.co.kr", "FFFFFF", True), ("     리멤버 마켓솔루션 · MICE 비즈팀 이진철 팀장", "A89F92")], 12, anchor=MSO_ANCHOR.MIDDLE)
    d.takeaway(s, [("다음 행사 전에 한 가지만 확인하십시오. ", INK), ("'우리 조건에 맞는 사람이 몇 명이나 있는가'", OD), (".", INK)])

def s_closing(d):
    s = d.slide(dark=True, bg=T["d_objet"])
    obj = os.path.join(ASSETS, "objet-06-coil.png")
    if os.path.exists(obj):
        im = Image.open(obj); iw, ih = im.size; h = SLIDE_H; w = h * iw / ih
        s.shapes.add_picture(obj, Inches(SLIDE_W - w * 0.92), Inches(0), Inches(w), Inches(h))
        ov = d.box(s, 0, 0, SLIDE_W * 0.62, SLIDE_H, fill=T["d_objet"], radius=0); d._alpha(ov, 0.92)
        ov2 = d.box(s, SLIDE_W * 0.62, 0, SLIDE_W * 0.38, SLIDE_H, fill=T["d_objet"], radius=0); d._alpha(ov2, 0.35)
    d.hline(s, MARGIN, 1.1, 5.5, color="FFFFFF", weight=1)
    d.text(s, MARGIN, 1.35, 8.0, 0.35, [("REMEMBER MICE SOLUTION", T["d_orange"])], 11.5, bold=True, spacing=3)
    d.text(s, MARGIN, 1.9, 8.2, 2.2, [("다음 행사는,\n좌석이 아니라 ", "F4F0E9"), ("계약", T["d_orange"]), ("을 채우십시오.", "F4F0E9")], 38, bold=True, line_spacing=1.12)
    d.text(s, MARGIN, 4.2, 8.0, 0.9, [("타겟부터 계약까지, 하나의 데이터로.\n리멤버 MICE가 함께합니다.", "A89F92")], 14, line_spacing=1.35)
    d.text(s, MARGIN, 5.35, 8.0, 1.1, [("문의  mice_solution@remember.co.kr\n리멤버 마켓솔루션 · MICE 비즈팀 이진철 팀장\n(주)리멤버앤컴퍼니 · 서울 강남구 테헤란로 134 포스코타워 역삼", "A89F92")], 10.5, line_spacing=1.45)
    d.logo(s, MARGIN, 6.7, h=0.3, dark=True)
    d.text(s, SLIDE_W - MARGIN - 6, FOOTER_Y, 6, 0.3, [(f"{DOC}   ·   {d.page:02d}", T["d_dim"])], SZ_FOOTER, align=PP_ALIGN.RIGHT)

# ══════════════════════════════════════════════════════════════════
# 섹션 정의 및 변형(variant)
# ══════════════════════════════════════════════════════════════════
SECTIONS = {
    "problem": dict(short="문제 정의", title="행사는 성공했는데,\n매출은 왜 없을까", toc="문제 정의", toc_desc="행사는 성공했는데, 매출은 왜 없을까",
                    summary="사전등록자의 절반은 오지 않고, 온 사람의 절반은 의사결정권자가 아닙니다.\n예산이 새는 두 지점부터 확인합니다.", photo=("webinar", "w001.jpg"),
                    slides=[s_quote, s_funnel, s_links]),
    "why": dict(short="왜 리멤버인가", title="왜 리멤버 MICE만\n가능한가", toc="왜 리멤버 MICE인가", toc_desc="명단을 가진 회사가 직접 초청하고 운영하는, 유일한 구조",
                summary="명단을 가진 회사가 직접 초청하고, 운영하고, 계약까지 잇습니다.\n데이터·모객·운영·세일즈를 한 계약에 담는 사업자는 리멤버가 유일합니다.", photo=("webinar", "w014.jpg"),
                slides=[s_data, s_target, s_compare, s_showup, s_showup_results, s_sales, s_unique]),
    "solution": dict(short="솔루션 구조", title="솔루션 구조와\n프로세스", toc="솔루션 구조와 프로세스", toc_desc="8주 표준 일정, 한 계약의 범위, 형식별 가이드",
                     summary="8주면 됩니다. 명단·초청·RSVP부터 베뉴, 무대, 현장 인력, 사후 리포트까지\n한 계약으로. 나눠 발주하고 조율할 일이 없습니다.", photo=("webinar", "w000.jpg"),
                     slides=[s_timeline, s_scope, s_formats, s_lineup, s_report]),
    "team": dict(short="MICE 비즈팀", title="리멤버\nMICE 비즈팀", toc="리멤버 MICE 비즈팀", toc_desc="국제회의부터 박람회까지, 18년 MICE 운영 전문가와 데이터 전문가들",
                 summary="데이터 회사 안에 MICE 전문 조직이 있습니다.\n국제회의부터 박람회까지 운영해 온 전문가들이 리멤버 데이터 위에서 일합니다.", photo=("webinar", "w007.jpg"),
                 slides=[s_org, s_leader, s_members, s_dataleaders, s_expertise, s_venue]),
    "refs": dict(short="레퍼런스", title="레퍼런스", toc="레퍼런스", toc_desc="2026년 실행 현장과 성과 수치, 자사 주최 컨퍼런스",
                 summary="2026년, 매달 현장에서 검증되고 있습니다.\n보안·이커머스·물류·리테일·SaaS 고객사의 행사와, 리멤버가 직접 여는 컨퍼런스.", photo=("webinar", "w013.jpg"),
                 slides=[s_collage, s_reftable, s_kpi, s_own]),
    "start": dict(short="시작하기", title=None, toc="시작하기", toc_desc="이메일 한 통으로 초청 후보 모수부터", summary=None, photo=None, slides=[s_next]),
}

VARIANTS = {
    "A_솔루션우선": dict(order=["problem", "why", "solution", "team", "refs", "start"],
                     title=[("타겟부터 ", INK), ("계약", O), ("까지,\n하나의 데이터로.", INK)],
                     sub="검증된 프로필 500만이 초청하고, 전문가가 운영하고, 데이터로 증명합니다.",
                     toc_title="성과가 남는 행사는\n어떻게 다른가"),
    "B_팀우선": dict(order=["team", "refs", "problem", "why", "solution", "start"],
                   title=[("행사를 아는 사람들이,\n", INK), ("데이터", O), ("로 초청합니다.", INK)],
                   sub="18년 MICE 운영 전문가 팀과 검증된 프로필 500만이 함께 만드는 행사.",
                   toc_title="누가 만들고,\n무엇이 다른가"),
}

def build(variant):
    v = VARIANTS[variant]
    d = RDeck(DOC, ASSETS, IMG)
    # 커버
    s = d.slide()
    d.logo(s, MARGIN, 0.62, h=0.30)
    d.text(s, MARGIN, 1.95, 7.2, 0.35, [("REMEMBER MICE SOLUTION   ·   INTRODUCTION 2026", O)], 11.5, bold=True, spacing=2.5)
    d.text(s, MARGIN, 2.4, 7.4, 2.3, v["title"], 46, bold=True, line_spacing=1.08, spacing=-1)
    d.text(s, MARGIN, 4.75, 7.0, 1.0, [("리멤버 MICE 솔루션 소개서\n", INK, True, 15), (v["sub"], SUB)], 13, line_spacing=1.35)
    d.hline(s, MARGIN, 6.45, 3.0, color=O, weight=1.5)
    d.text(s, MARGIN, 6.58, 9.0, 0.35, [("리멤버 마켓솔루션 · MICE 비즈팀   |   (주)리멤버앤컴퍼니   |   2026. 09", MUT)], 10.5)
    d.picture(s, P("webinar", "w002.jpg"), 8.05, 0.95, 4.65, 5.15)
    d.text(s, 8.05, 6.18, 3.6, 0.3, [("리멤버 MICE 운영 현장 · 고객사 컨퍼런스 (2026.4)", MUT)], 8.5)
    d.ring(s, 12.85, 7.15, 1.35, thick=0.24); d.dot(s, 11.35, 6.75, r=0.07)
    # 목차
    s = d.slide()
    circ = circle_png(P("webinar", "w018.jpg"), os.path.join(IMG, "circle_contents.png"))
    s.shapes.add_picture(circ, Inches(-1.6), Inches(1.2), Inches(5.35), Inches(5.35))
    d.ring(s, 4.05, 1.85, 0.55, thick=0.12, grad=False, color=OT); d.dot(s, 3.45, 6.35, r=0.1)
    d.nav(s, "CONTENTS", "INTRODUCTION")
    d.text(s, 5.6, 0.95, 7.2, 0.9, [(v["toc_title"], INK)], 28, bold=True, line_spacing=1.1)
    for i, key in enumerate(v["order"]):
        sec = SECTIONS[key]; y = 2.1 + i * 0.74
        d.text(s, 5.6, y, 0.7, 0.4, [(f"{i+1:02d}", O)], 14, bold=True)
        d.text(s, 6.3, y - 0.02, 6.4, 0.4, [(sec["toc"], INK)], 16, bold=True)
        d.text(s, 6.3, y + 0.33, 6.4, 0.3, [(sec["toc_desc"], SUB)], 10)
        d.hline(s, 5.6, y + 0.66, 7.1, color=T["line_soft"], weight=0.75)
    # 섹션
    for i, key in enumerate(v["order"]):
        sec = SECTIONS[key]; num = i + 1
        eb = f"{num:02d} · {sec['short']}"; ft = f"{num:02d} {sec['short']}"
        if sec["title"]:
            d.section_divider(num, sec["title"], sec["summary"], ft, photo=P(*sec["photo"]))
        for fn in sec["slides"]:
            fn(d, eb, ft)
    s_closing(d)
    out = os.path.join(OUT, f"리멤버_MICE_솔루션_소개서_2026_{variant}.pptx")
    d.save(out); print("SAVED", out, "slides:", d.page)
    return out

if __name__ == "__main__":
    for vname in VARIANTS:
        build(vname)
