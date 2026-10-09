#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build_dashboard.py — mice-meeting-minutes 회의록 대시보드 빌더 (v2.2.0)

assets/dashboard-template.html 에 8축 추출 데이터(JSON)·발행 명의·로고 슬롯·디자인 토큰을
주입해 단일 HTML 대시보드를 만든다. 룩은 jc-design-system v2(리멤버 웜 페이퍼) 하나.

디자인 토큰 (값 미러 금지 — 하우스 규약 §2)
  jc-design-system/scripts/jc_tokens.py 를 import 해 signature-tokens.md §6 JSON 을 런타임 로드한다.
  탐색 순서: ① 형제 경로 parents[2]/jc-design-system → ② ~/.claude/skills/jc-design-system
            → ③ ~/.claude/skills/synced/*/jc-design-system
  템플릿의 `@design-tokens:start ~ end` CSS 블록은 미러이며, 빌드 때 SoT 값으로 통째로 교체된다.
  SoT 로드 실패 시에만 아래 _FALLBACK_TOKENS(§6 발췌)를 쓴다.

산출
  dashboard_[프로젝트]_[YYYYMMDD].html (메인) · 시리즈 모드 시 .series-data/[series_id].json

사용 (Windows: python / 한글 출력은 PYTHONIOENCODING=utf-8 권장)
  python build_dashboard.py --input minutes.json --out <출력폴더> [--theme light|dark]
  python build_dashboard.py --sample <출력폴더>        # 내장 샘플로 빌드
  python build_dashboard.py --dump-sample sample.json  # 입력 JSON 형식 예시 저장
  python build_dashboard.py --print-css                # SoT 토큰 CSS 출력(템플릿 미러 갱신용)
  python build_dashboard.py --self-test

의존: 표준 라이브러리. Pillow가 있으면 로고를 축소해 임베드(없으면 원본 임베드 — 파일만 커진다).
"""
from __future__ import annotations

import argparse
import base64
import importlib.util
import io
import json
import re
import sys
import tempfile
from dataclasses import asdict, dataclass, field, fields, is_dataclass
from datetime import date
from pathlib import Path
from typing import Optional

# UTF-8 stdout/stderr 강제 (Windows cp949 환경 크래시 방지)
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SKILL_DIR / "assets" / "dashboard-template.html"
SKILL_VERSION = "v2.2.0"          # SKILL.md frontmatter version 과 동기
PUBLISHER = "리멤버 MICE비즈팀"     # 발행 명의 기본 (RULE-NO-COMPANY v2). 발주처는 client_company 로 주입
MIN_HTML_BYTES = 40_000           # 빌드 무결성 하한 (템플릿 단독 약 45KB)

TOKEN_START = "/* @design-tokens:start"
TOKEN_END = "/* @design-tokens:end */"

# 구 jc 시그니처(legacy-jc) 금지 목록 — 산출물에 섞이면 검증 실패. 값은 legacy 판별용으로만 둔다.
LEGACY_HEX = ("0A2540", "2962FF", "FF5722", "E91E63", "00E676", "1A3556", "B8C5D6")  # legacy-jc 금지

# =====================================================================
# 디자인 토큰 — jc-design-system SoT 런타임 로드
# =====================================================================

# 폴백 상수 — 출처: jc-design-system/references/signature-tokens.md §6 JSON (v2.1.0 발췌).
# SoT 로드 실패 시에만 사용한다. 값을 바꾸려면 SoT를 고치고 여기는 손대지 않는다.
_FALLBACK_TOKENS = {
    "color": {
        "bg": "#FBFAF6", "surface": "#FFFFFF", "surfaceAlt": "#F4F1EA", "surfaceSoft": "#EFEBE2",
        "border": "#DCD6C8", "borderStrong": "#CFC8BC", "line": "#C9C9C0",
        "text": "#1A1A1A", "textSecondary": "#4A463F", "textMuted": "#6E6E6E", "textCaption": "#8C867A",
        "accent": "#EB6F2A", "accentStrong": "#B8431A", "accentLight": "#F5A05A",
        "accentSoftLine": "#F3B48A", "accentSoft": "#FFF1E6",
        "point": {"steel": "#476580", "steelTint": "#E8EEF3"},
        "semantic": {"success": "#196B24", "successBg": "#E7EFE8", "warning": "#D39A1F",
                     "warningBg": "#FBF2DF", "danger": "#D93636", "dangerBg": "#FBE9E9"},
        "data": ["#EB6F2A", "#476580", "#4A463F", "#8C867A", "#F3B48A", "#D39A1F"],
        "dark": {
            "bg": "#141210", "panel": "#211E1A", "surface": "#2A2620", "surfaceAlt": "#322D26",
            "border": "#3E3931", "line": "#4A443B", "text": "#F4F0E9", "textSub": "#A89F92",
            "textDim": "#6E655A", "brownText": "#C9C0B2", "accent": "#EB6F2A", "accentText": "#F08A4C",
            "accentLight": "#F5A05A", "accentTint": "#3A2A1E", "steelText": "#8FAEC7",
            "steelTint": "#26313A", "success": "#6FBF7C", "successBg": "#22301F",
            "danger": "#F07A7A", "dangerBg": "#3A2323", "warning": "#E2B558", "warningBg": "#3A3021",
        },
    },
    "font": {"ko": "'Pretendard Variable', Pretendard, -apple-system, 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif",
             "mono": "'JetBrains Mono', 'D2Coding', Consolas, monospace"},
    "shadow": {"card": "0 2px 12px rgba(74,70,63,0.08)"},
}
# 다크 카드 그림자 — 출처: mode-mapping.md §3 (§6 JSON에 없는 비색상 값)
_DARK_SHADOW = "0 2px 12px rgba(0,0,0,0.32)"

# CSS 변수 → (라이트 스펙, 다크 스펙). 변수 이름은 usage-guide.md §3.4 (팀 보드·플레이북 HTML과 동일).
# 스펙: ("c", key)=color(.point/.semantic) · ("d", key)=color.dark · ("s", i)=color.data[i] · ("lit", 값)
TOKEN_ROLES: list[tuple[str, tuple, tuple]] = [
    ("--paper",        ("c", "bg"),             ("d", "panel")),        # 페이지 캔버스 (대시보드 다크 = 패널)
    ("--surface",      ("c", "surface"),        ("d", "surface")),      # 카드·패널
    ("--surface-warm", ("c", "surfaceAlt"),     ("d", "surfaceAlt")),   # 표 헤더·칸반 열·트랙
    ("--line-soft",    ("c", "surfaceSoft"),    ("d", "border")),       # 표 행 구분
    ("--border",       ("c", "border"),         ("d", "border")),
    ("--border-strong", ("c", "borderStrong"),  ("d", "line")),
    ("--line",         ("c", "line"),           ("d", "line")),
    ("--grid",         ("c", "surfaceSoft"),    ("d", "line")),         # 차트 격자 (mode-mapping §3)
    ("--ink",          ("c", "text"),           ("d", "text")),
    ("--brown",        ("c", "textSecondary"),  ("d", "brownText")),
    ("--ink-sub",      ("c", "textMuted"),      ("d", "textSub")),
    ("--warm-gray",    ("c", "textCaption"),    ("d", "textDim")),      # 캡션·단위 전용 (본문 금지)
    ("--orange",       ("c", "accent"),         ("d", "accent")),       # 면·룰·큰 글자 전용
    ("--orange-deep",  ("c", "accentStrong"),   ("d", "accentText")),   # 작은 강조 텍스트 (RULE-WCAG)
    ("--orange-soft",  ("c", "accentLight"),    ("d", "accentLight")),
    ("--orange-pale",  ("c", "accentSoftLine"), ("c", "accentSoftLine")),
    ("--orange-tint",  ("c", "accentSoft"),     ("d", "accentTint")),
    ("--steel",        ("c", "steel"),          ("d", "steelText")),
    ("--steel-tint",   ("c", "steelTint"),      ("d", "steelTint")),
    ("--positive",     ("c", "success"),        ("d", "success")),
    ("--positive-bg",  ("c", "successBg"),      ("d", "successBg")),
    ("--negative",     ("c", "danger"),         ("d", "danger")),
    ("--negative-bg",  ("c", "dangerBg"),       ("d", "dangerBg")),
    ("--amber",        ("c", "warning"),        ("d", "warning")),
    ("--amber-bg",     ("c", "warningBg"),      ("d", "warningBg")),
    ("--s1",           ("s", 0),                ("s", 0)),              # 차트 시리즈 S1~S5 (순서 고정)
    ("--s2",           ("s", 1),                ("s", 1)),
    ("--s3",           ("s", 2),                ("s", 2)),
    ("--s4",           ("s", 3),                ("s", 3)),
    ("--s5",           ("s", 4),                ("s", 4)),
    ("--btn-primary",  ("c", "accentStrong"),   ("c", "accentStrong")), # 흰 글자 5.45:1 (작은 버튼 글자 AA)
    ("--on-fill",      ("c", "surface"),        ("c", "surface")),      # 채움 버튼·토스트 위 글자
    ("--shadow",       ("shadow", "card"),      ("lit", _DARK_SHADOW)),
]


def find_design_system(start: Optional[Path] = None) -> Optional[Path]:
    """하우스 규약 §2 순서로 jc-design-system 폴더를 찾는다. 샌드박스 경로는 보지 않는다."""
    here = Path(start) if start else Path(__file__).resolve()
    cands: list[Path] = []
    if len(here.parents) >= 3:
        cands.append(here.parents[2] / "jc-design-system")
    home = Path.home()
    cands.append(home / ".claude" / "skills" / "jc-design-system")
    cands.extend(sorted(home.glob(".claude/skills/synced/*/jc-design-system")))
    for c in cands:
        if (c / "references" / "signature-tokens.md").is_file() and (c / "scripts" / "jc_tokens.py").is_file():
            return c
    return None


def _import_jc_tokens(sot: Path):
    prev = sys.dont_write_bytecode
    sys.dont_write_bytecode = True  # SoT 스킬 폴더에 __pycache__를 만들지 않는다 (읽기 전용 참조)
    try:
        spec = importlib.util.spec_from_file_location("jc_tokens", sot / "scripts" / "jc_tokens.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        return mod
    finally:
        sys.dont_write_bytecode = prev


def _local_color(tok: dict, key: str) -> str:
    c = tok.get("color", {})
    v = c.get(key)
    if v is None:
        v = c.get("point", {}).get(key)
    if v is None:
        v = c.get("semantic", {}).get(key)
    return v if isinstance(v, str) else ""


def load_theme(start: Optional[Path] = None) -> dict:
    """SoT 토큰 → {light, dark, print, font, mono, source, sot, logo_light, logo_dark}."""
    sot = find_design_system(start)
    jt, tok = None, {}
    if sot is not None:
        try:
            jt = _import_jc_tokens(sot)
            tok = jt.load_tokens(sot) or {}
        except Exception:  # noqa: BLE001 — 로더 실패는 폴백으로
            jt, tok = None, {}
    source = "sot" if tok else "fallback"
    if not tok:
        tok, jt = _FALLBACK_TOKENS, None

    def color(k: str) -> str:
        return jt.color(tok, k) if jt else _local_color(tok, k)

    def dark(k: str) -> str:
        return jt.dark(tok, k) if jt else tok.get("color", {}).get("dark", {}).get(k, "")

    def resolve(spec: tuple) -> str:
        kind, key = spec
        if kind == "c":
            return color(key)
        if kind == "d":
            return dark(key)
        if kind == "s":
            data = tok.get("color", {}).get("data", [])
            return data[key] if key < len(data) else ""
        if kind == "shadow":
            return tok.get("shadow", {}).get(key, "")
        return str(key)  # "lit"

    light = {var: resolve(ls) for var, ls, _ in TOKEN_ROLES}
    darkv = {var: resolve(ds) for var, _, ds in TOKEN_ROLES}
    printv = dict(light)
    printv["--paper"] = light["--surface"]  # 인쇄 캔버스는 흰 종이 (mode-mapping §4.2)
    font = tok.get("font", {})
    logo_light = logo_dark = None
    if source == "sot" and jt is not None:
        logo_light = jt.asset(tok, "logoLight", sot)
        logo_dark = jt.asset(tok, "logoDark", sot)
    return {
        "light": light, "dark": darkv, "print": printv, "source": source, "sot": sot,
        "font": font.get("ko") or _FALLBACK_TOKENS["font"]["ko"],
        "mono": font.get("mono") or _FALLBACK_TOKENS["font"]["mono"],
        "logo_light": logo_light if logo_light and Path(logo_light).is_file() else None,
        "logo_dark": logo_dark if logo_dark and Path(logo_dark).is_file() else None,
    }


def build_token_css(theme: dict) -> str:
    """템플릿 @design-tokens 블록 전체(라이트·다크·인쇄 라이트 강제)를 만든다."""
    def block(selector: str, values: dict, important: bool = False, extra: str = "") -> str:
        imp = " !important" if important else ""
        body = "".join(f"  {k}: {v}{imp};\n" for k, v in values.items())
        return f"{selector} {{\n{body}{extra}}}\n"

    head = (f"{TOKEN_START} — jc-design-system v2 리멤버 웜 페이퍼 토큰 (미러)\n"
            "   출처: jc-design-system/references/signature-tokens.md §6 JSON · mode-mapping.md §3(다크) §4.2(인쇄)\n"
            "   빌드 때 build_dashboard.py 가 jc_tokens.py 로 SoT 를 런타임 로드해 이 블록을 통째로 교체한다.\n"
            "   직접 고치지 말 것 — SoT 를 고친 뒤 `python scripts/build_dashboard.py --print-css` 로 재생성. */\n")
    root_extra = (f"  --font: {theme['font']};\n  --font-mono: {theme['mono']};\n"
                  "  --r-card: 12px;\n  --r-btn: 6px;\n")
    css = head
    css += block(":root", theme["light"], extra=root_extra)
    css += block(':root[data-theme="dark"]', theme["dark"])
    css += "/* RULE-PRINT-LIGHT — 다크 토글 상태여도 인쇄·PDF는 라이트 */\n@media print {\n"
    css += "".join("  " + ln + "\n" for ln in
                   block(':root, :root[data-theme="dark"]', theme["print"], important=True).splitlines())
    css += "}\n" + TOKEN_END
    return css


def _replace_token_block(template: str, css: str) -> str:
    s = template.find(TOKEN_START)
    e = template.find(TOKEN_END)
    if s < 0 or e < 0 or e < s:
        raise ValueError("템플릿에 @design-tokens 블록 표지가 없습니다 (assets/dashboard-template.html 확인)")
    return template[:s] + css + template[e + len(TOKEN_END):]


def _logo_data_uri(path: Optional[Path], max_h: int = 64) -> Optional[str]:
    """로고 PNG → data URI. Pillow가 있으면 높이 max_h로 축소(비율 유지, 재염색 없음)."""
    if not path:
        return None
    raw = Path(path).read_bytes()
    try:
        from PIL import Image  # type: ignore
        with Image.open(io.BytesIO(raw)) as im:
            if im.height > max_h:
                w = round(im.width * max_h / im.height)
                im = im.resize((w, max_h), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, format="PNG", optimize=True)
            raw = buf.getvalue()
    except Exception:  # noqa: BLE001 — Pillow 미설치·실패 시 원본 그대로
        pass
    return "data:image/png;base64," + base64.b64encode(raw).decode("ascii")


# =====================================================================
# 데이터 모델 (8축 + 메타)
# =====================================================================

@dataclass
class Decision:
    text: str
    timestamp: Optional[str] = None
    rationale: Optional[str] = None


@dataclass
class ActionItem:
    id: str
    owner: str
    action: str
    due: str
    priority: str  # P0/P1/P2/P3
    status: str    # TODO/DOING/BLOCKED/DONE
    linked: Optional[str] = None
    source: Optional[str] = None
    note: Optional[str] = None
    is_carry_over: bool = False


@dataclass
class Risk:
    text: str
    impact: str  # 상/중/하
    response: Optional[str] = None
    timestamp: Optional[str] = None


@dataclass
class PendingItem:
    text: str
    reason: str
    next_review: Optional[str] = None
    owner: Optional[str] = None
    is_carry_over: bool = False


@dataclass
class NextStep:
    title: str
    date_str: Optional[str] = None
    attendees: Optional[str] = None
    agenda: Optional[str] = None


@dataclass
class StrategyNote:
    who: str = ""
    what: str = ""
    when_: str = ""
    where: str = ""
    why: str = ""
    how: str = ""


@dataclass
class DashboardData:
    """대시보드 통합 데이터 모델"""
    project_name: str
    meeting_date: str          # YYYY-MM-DD
    meeting_time: str = ""     # HH:MM~HH:MM
    location: str = ""
    attendees: list[str] = field(default_factory=list)
    meeting_type: str = "A"    # A/B/C/D/E
    type_label: str = "외부 클라이언트 미팅"
    mode: str = "internal"     # external/internal
    theme: str = "light"       # light/dark — 첫 화면 테마(저장된 사용자 선택이 있으면 그쪽 우선)
    client_id: Optional[str] = None   # client-overlays.md 발주처 슬롯 ID. None = 리멤버 기본
    client_company: str = ""          # {{client_company}} 주입 슬롯 (헤더 표기)
    publisher: str = ""               # 비우면 PUBLISHER(리멤버 MICE비즈팀)

    # 8축
    agenda: list[str] = field(default_factory=list)
    discussion: dict = field(default_factory=dict)  # {agenda_idx: [(speaker, text)]}
    decisions: list[Decision] = field(default_factory=list)
    actions: list[ActionItem] = field(default_factory=list)
    risks: list[Risk] = field(default_factory=list)
    pending: list[PendingItem] = field(default_factory=list)
    next_steps: list[NextStep] = field(default_factory=list)
    strategy_note: Optional[StrategyNote] = None

    # 시리즈 모드
    series_id: Optional[str] = None
    series_session_no: Optional[int] = None
    series_completion_rate: Optional[float] = None

    # Slack 페이스트용 1줄 코멘트 (Internal 모드)
    strategy_oneliner: Optional[str] = None

    # 메타
    author: str = ""  # {{author_name}} 주입 슬롯. 기본값 없음
    redaction_log: list[dict] = field(default_factory=list)


_NESTED = {"decisions": Decision, "actions": ActionItem, "risks": Risk,
           "pending": PendingItem, "next_steps": NextStep}


def _make(cls, d: dict, warnings: list):
    names = {f.name for f in fields(cls)}
    if cls is StrategyNote and "when" in d and "when_" not in d:
        d = {**d, "when_": d["when"]}
    unknown = [k for k in d if k not in names and not (cls is StrategyNote and k == "when")]
    if unknown:
        warnings.append(f"{cls.__name__}: 모르는 필드 무시 {unknown}")
    return cls(**{k: v for k, v in d.items() if k in names})


def data_from_dict(d: dict, warnings: Optional[list] = None) -> DashboardData:
    """JSON dict → DashboardData. 모르는 필드는 무시하고 warnings에 기록."""
    warnings = warnings if warnings is not None else []
    base = {}
    names = {f.name for f in fields(DashboardData)}
    for k, v in d.items():
        if k not in names:
            warnings.append(f"DashboardData: 모르는 필드 무시 '{k}'")
            continue
        if k in _NESTED and isinstance(v, list):
            v = [_make(_NESTED[k], x, warnings) if isinstance(x, dict) else x for x in v]
        elif k == "strategy_note" and isinstance(v, dict):
            v = _make(StrategyNote, v, warnings)
        base[k] = v
    for req in ("project_name", "meeting_date"):
        if not base.get(req):
            raise ValueError(f"필수 필드 누락: {req}")
    return DashboardData(**base)


# =====================================================================
# JSON 직렬화
# =====================================================================

def _serialize(obj):
    if is_dataclass(obj):
        return {k: _serialize(v) for k, v in asdict(obj).items()}
    if isinstance(obj, (list, tuple)):
        return [_serialize(item) for item in obj]
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    return obj


def to_json_payload(data: DashboardData) -> dict:
    """DashboardData → 대시보드 주입용 dict (discussion을 [speaker, text] 배열로 정규화)."""
    payload = _serialize(data)
    if isinstance(payload.get("discussion"), dict):
        payload["discussion"] = {
            str(k): [[i[0], i[1]] if isinstance(i, (list, tuple)) and len(i) >= 2 else i for i in v]
            for k, v in payload["discussion"].items()
        }
    return payload


def _script_safe_json(obj) -> str:
    """<script> 안에 넣을 JSON — '</' 를 끊어 스크립트 조기 종료를 막는다."""
    return json.dumps(obj, ensure_ascii=False, indent=2).replace("</", "<\\/")


# =====================================================================
# HTML 빌더
# =====================================================================

def render_dashboard_html(data: DashboardData, template_path: Path = TEMPLATE_PATH,
                          theme: Optional[dict] = None) -> str:
    if not template_path.exists():
        raise FileNotFoundError(f"템플릿 미발견: {template_path}")
    theme = theme or load_theme()
    html = template_path.read_text(encoding="utf-8")
    html = _replace_token_block(html, build_token_css(theme))
    brand = {
        "publisher": data.publisher or PUBLISHER,
        "clientCompany": data.client_company or None,
        "logoLight": _logo_data_uri(theme.get("logo_light")),
        "logoDark": _logo_data_uri(theme.get("logo_dark")),
        "theme": data.theme if data.theme in ("light", "dark") else "light",
        "skillVersion": SKILL_VERSION,
        "tokenSource": theme["source"],
    }
    title = f"{data.project_name} 회의록 대시보드 ({data.meeting_date})"
    html = html.replace("{{TITLE}}", _escape_html(title))
    html = html.replace("{{BRAND}}", _script_safe_json(brand))
    html = html.replace("{{INITIAL_DATA}}", _script_safe_json(to_json_payload(data)))
    return html


def _escape_html(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# =====================================================================
# 시리즈 데이터 동기화
# =====================================================================

def _calc_completion(actions: list[ActionItem]) -> float:
    if not actions:
        return 0.0
    return round(sum(1 for a in actions if a.status == "DONE") / len(actions), 2)


def sync_series_data(data: DashboardData, output_dir: Path) -> Optional[Path]:
    """시리즈 모드면 .series-data/[series_id].json 에 본 회차를 누적한다."""
    if not data.series_id:
        return None
    series_dir = output_dir / ".series-data"
    series_dir.mkdir(parents=True, exist_ok=True)
    series_path = series_dir / f"{data.series_id}.json"

    existing: dict = {}
    if series_path.exists():
        try:
            existing = json.loads(series_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}

    sessions = existing.get("sessions", [])
    session_no = data.series_session_no or (len(sessions) + 1)
    new_session = {
        "session_no": session_no,
        "date": data.meeting_date,
        "type": data.meeting_type,
        "actions": _serialize(data.actions),
        "pending_items": _serialize(data.pending),
        "decisions_count": len(data.decisions),
        "completion_rate": _calc_completion(data.actions),
    }
    sessions = [s for s in sessions if s.get("session_no") != session_no] + [new_session]
    sessions.sort(key=lambda s: s.get("session_no", 0))

    all_actions = [a for s in sessions for a in s.get("actions", [])]
    count = lambda st: sum(1 for a in all_actions if a.get("status") == st)  # noqa: E731
    carry: dict = {}
    for a in all_actions:
        if a.get("is_carry_over") and a.get("id"):
            carry[a["id"]] = carry.get(a["id"], 0) + 1
    total = len(all_actions)
    output = {
        "series_id": data.series_id,
        "project_name": data.project_name,
        "client_id": data.client_id,
        "default_type": data.meeting_type,
        "created_at": existing.get("created_at", date.today().isoformat()),
        "last_updated": date.today().isoformat(),
        "sessions": sessions,
        "cumulative_stats": {
            "total_sessions": len(sessions), "total_actions": total,
            "done": count("DONE"), "doing": count("DOING"), "blocked": count("BLOCKED"), "todo": count("TODO"),
            "completion_rate": round(count("DONE") / total, 2) if total else 0.0,
            "long_pending_actions": [aid for aid, c in carry.items() if c >= 3],
        },
    }
    series_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    return series_path


def load_series_carry_over(series_id: str, output_dir: Path) -> tuple[list[ActionItem], list[PendingItem]]:
    """직전 회차의 미완료 Action·미결 사항을 carry-over 대상으로 돌려준다."""
    series_path = output_dir / ".series-data" / f"{series_id}.json"
    if not series_path.exists():
        return [], []
    try:
        existing = json.loads(series_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return [], []
    sessions = existing.get("sessions", [])
    if not sessions:
        return [], []
    latest = sessions[-1]
    a_names = {f.name for f in fields(ActionItem)}
    p_names = {f.name for f in fields(PendingItem)}
    actions = [ActionItem(**{**{k: v for k, v in a.items() if k in a_names}, "is_carry_over": True})
               for a in latest.get("actions", []) if a.get("status") in ("TODO", "DOING", "BLOCKED")]
    pending = [PendingItem(**{**{k: v for k, v in p.items() if k in p_names}, "is_carry_over": True})
               for p in latest.get("pending_items", [])]
    return actions, pending


# =====================================================================
# 메인 빌드 + 검증
# =====================================================================

def _slug(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9가-힣-]", "-", name.lower().strip()).strip("-") or "meeting"


def build_dashboard(data: DashboardData, output_dir: Path, template_path: Optional[Path] = None,
                    theme: Optional[dict] = None) -> Path:
    """대시보드 .html 생성 + 시리즈 데이터 동기화. 생성된 .html 경로를 돌려준다."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    html = render_dashboard_html(data, template_path or TEMPLATE_PATH, theme)
    out = output_dir / f"dashboard_{_slug(data.project_name)}_{data.meeting_date.replace('-', '')}.html"
    out.write_text(html, encoding="utf-8")
    sync_series_data(data, output_dir)
    return out


def validate_dashboard_html(html_path: Path, theme: Optional[dict] = None) -> dict:
    """생성 HTML 검증 — 치환·라이브러리·SoT 토큰·legacy 색 0·인쇄 라이트·크기."""
    html_path = Path(html_path)
    if not html_path.exists():
        return {"valid": False, "issues": ["파일 미생성"], "size": 0}
    theme = theme or load_theme()
    content = html_path.read_text(encoding="utf-8")
    up = content.upper()
    issues = []
    for ph in ("{{TITLE}}", "{{INITIAL_DATA}}", "{{BRAND}}"):
        if ph in content:
            issues.append(f"플레이스홀더 미치환 {ph}")
    if "react" not in content.lower():
        issues.append("React 미연결")
    if "recharts" not in content.lower():
        issues.append("Recharts 미연결")
    for var in ("--orange", "--paper", "--s1"):
        val = theme["light"][var].upper()
        if f"{var.upper()}: {val}" not in up:
            issues.append(f"SoT 토큰 미적용 {var}={val}")
    if f"--PAPER: {theme['dark']['--paper'].upper()}" not in up:
        issues.append("다크 토큰 미적용")
    if "@MEDIA PRINT" not in up:
        issues.append("인쇄 라이트 강제 블록 없음 (RULE-PRINT-LIGHT)")
    legacy = [h for h in LEGACY_HEX if re.search(rf"(?<![0-9A-F]){h}(?![0-9A-F])", up)]
    if legacy:
        issues.append(f"legacy-jc 색 혼입 {legacy}")
    size = html_path.stat().st_size
    if size < MIN_HTML_BYTES:
        issues.append(f"파일 크기 {size}B < {MIN_HTML_BYTES}B (빌드 누락 의심)")
    return {"valid": not issues, "size": size, "issues": issues, "token_source": theme["source"]}


# =====================================================================
# 샘플 데이터 (가명 — RULE-NO-COMPANY)
# =====================================================================

def sample_data() -> DashboardData:
    return DashboardData(
        project_name="A사 고객 컨퍼런스 2026 Discovery",
        meeting_date="2026-05-09",
        meeting_time="14:00~15:30",
        location="리멤버 회의실",
        attendees=["호스트 (리멤버 MICE비즈팀)", "김부장 (A사)", "협력사 담당자 (운영 대행)"],
        meeting_type="A",
        type_label="외부 클라이언트 미팅",
        mode="internal",
        client_id="a-corp-2026",
        client_company="A사",
        agenda=["행사 컨셉 검토", "일정 협의", "예산 범위", "후속 미팅 일정"],
        discussion={0: [("호스트 (리멤버 MICE비즈팀)", "1일 컨퍼런스 + 데모 부스 결합 제안"),
                        ("김부장 (A사)", "데모 부스보다 1:1 미팅룸 비중 강조")]},
        decisions=[
            Decision(text="행사 형식: 1일 컨퍼런스 + 1:1 미팅룸 50%·데모 부스 50%", timestamp="00:23", rationale="양측 동의"),
            Decision(text="행사 일자: 2026-06-18(목)", timestamp="00:41", rationale="A사 분기 마감 직후 + 베뉴 가용일"),
            Decision(text="베뉴 답사: 2026-05-22 양측 동행", timestamp="00:44"),
        ],
        actions=[
            ActionItem(id="AC-DISC-001", owner="호스트 (리멤버 MICE비즈팀)", action="베뉴 후보 3곳 비교 자료 제출",
                       due="2026-05-12", priority="P1", status="TODO"),
            ActionItem(id="AC-DISC-002", owner="호스트 (리멤버 MICE비즈팀)", action="타깃 데이터 기반 초청 대상 250명 추출",
                       due="2026-05-14", priority="P1", status="DOING"),
            ActionItem(id="AC-DISC-003", owner="김부장 (A사)", action="본사 동시통역 결재 진행",
                       due="2026-05-15", priority="P1", status="BLOCKED"),
            ActionItem(id="AC-DISC-004", owner="협력사 담당자 (운영 대행)", action="베뉴 가예약 6/18·6/25 양일",
                       due="2026-05-12", priority="P0", status="DONE"),
        ],
        risks=[Risk(text="베뉴 가용일 6월 중순 충돌 다수", impact="상", timestamp="00:32",
                    response="6/18·6/25 양일 가예약, 6/12까지 확정")],
        pending=[PendingItem(text="동시통역 부스 설치 여부", reason="A사 본사 결재 필요",
                             next_review="다음 미팅 (5/16)", owner="김부장 (A사)")],
        next_steps=[NextStep(title="다음 미팅", date_str="2026-05-16(금) 14:00",
                             attendees="본 미팅 동일 + A사 본사 담당", agenda="동시통역 결재 결과 + 베뉴 답사 계획")],
        strategy_note=StrategyNote(
            who="김부장이 창구지만 결재 권한은 본사 담당",
            what="표면은 컨셉 협의, 실제는 운영 역량 검증",
            when_="6/18 행사 기준 5/9 미팅은 빠듯 — 5/16 이후 베뉴 확정이 마감선",
            where="결정 라인: 김부장 → 본사 담당 → 글로벌 본사",
            why="A사 국내 사업 확장 시점, 행사 성과가 차기 분기 예산 근거",
            how="1:1 미팅룸 성과 지표(KPI)를 5/16 미팅 안건으로 사전 합의"),
        strategy_oneliner="5/16 본사 담당 참석 미팅이 실질 검증 — KPI 사전 합의 필수",
        series_id="a-corp-discovery",
        series_session_no=1,
    )


# =====================================================================
# 자가 테스트
# =====================================================================

def _lum(hexv: str) -> float:
    h = hexv.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a: str, b: str) -> float:
    """WCAG 2.1 대비비 (mode-mapping.md §9)."""
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _template_mirror() -> str:
    t = TEMPLATE_PATH.read_text(encoding="utf-8")
    s, e = t.find(TOKEN_START), t.find(TOKEN_END)
    return t[s:e + len(TOKEN_END)] if s >= 0 and e >= 0 else ""


def self_test() -> int:
    ok = True

    def check(label: str, cond: bool, detail: str = "") -> None:
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'} {label}" + (f" — {detail}" if detail and not cond else ""))
        ok = ok and cond

    theme = load_theme()
    print(f"토큰 출처: {theme['source']} ({theme['sot'] or 'SoT 미발견 — §6 폴백'})")
    check("토큰 역할 전부 해석(빈 값 0)", all(theme["light"].values()) and all(theme["dark"].values()),
          str([k for k, v in {**theme['light'], **theme['dark']}.items() if not v]))
    css = build_token_css(theme).upper()
    leg = [h for h in LEGACY_HEX if h in css]
    check("legacy-jc 색 0 (생성 CSS)", not leg, str(leg))
    check("차트 시리즈 S1 = 액센트", theme["light"]["--s1"].upper() == theme["light"]["--orange"].upper())

    L, D = theme["light"], theme["dark"]
    pairs = [
        ("라이트 본문 ink/paper", L["--ink"], L["--paper"], 4.5),
        ("라이트 뮤트 ink-sub/surface", L["--ink-sub"], L["--surface"], 4.5),
        ("라이트 작은 강조 orange-deep/surface", L["--orange-deep"], L["--surface"], 4.5),
        ("라이트 배지 orange-deep/orange-tint", L["--orange-deep"], L["--orange-tint"], 4.5),
        ("버튼 on-fill/btn-primary", L["--on-fill"], L["--btn-primary"], 4.5),
        ("라이트 부정 negative/surface", L["--negative"], L["--surface"], 4.5),
        ("라이트 긍정 positive/positive-bg", L["--positive"], L["--positive-bg"], 4.5),
        ("다크 본문 ink/paper", D["--ink"], D["--paper"], 4.5),
        ("다크 뮤트 ink-sub/surface", D["--ink-sub"], D["--surface"], 4.5),
        ("다크 작은 강조 orange-deep/surface", D["--orange-deep"], D["--surface"], 4.5),
        ("오렌지 큰 글자 orange/surface (≥3.0)", L["--orange"], L["--surface"], 3.0),
    ]
    for label, fg, bg, need in pairs:
        r = contrast(fg, bg)
        check(f"RULE-WCAG {label} {r:.2f}:1 ≥ {need}", r >= need)
    small_orange = contrast(L["--orange"], L["--paper"])
    check(f"오렌지 텍스트는 큰 글자 전용 확인 (캔버스 위 {small_orange:.2f}:1 < 4.5)", small_orange < 4.5)

    # 폴백 경로: SoT를 못 찾았다고 가정해도 빈 값 없이 동작해야 하고, 폴백 상수는 SoT와 같아야 한다
    global find_design_system
    real_find = find_design_system
    find_design_system = lambda start=None: None  # noqa: E731
    try:
        fb = load_theme()
    finally:
        find_design_system = real_find
    check("폴백 경로 동작 (SoT 미발견 가정, 빈 값 0)",
          fb["source"] == "fallback" and all(fb["light"].values()) and all(fb["dark"].values()))
    if theme["source"] == "sot":
        diff = [k for k in theme["light"] if fb["light"][k] != theme["light"][k] or fb["dark"][k] != theme["dark"][k]]
        if diff:
            print(f"  주의 폴백 상수가 SoT와 다름 {diff} — _FALLBACK_TOKENS를 signature-tokens.md §6에 맞춰 갱신")
        else:
            print("  PASS 폴백 상수 = SoT §6 값 (드리프트 0)")

    mirror = _template_mirror()
    check("템플릿 @design-tokens 블록 존재", bool(mirror))
    if mirror and mirror != build_token_css(theme):
        print("  주의 템플릿 미러가 현재 SoT와 다름 — 빌드 결과는 SoT 값으로 교체되므로 무해. "
              "`--print-css`로 미러 갱신 권장")

    with tempfile.TemporaryDirectory() as tmp:
        tmpd = Path(tmp)
        data = sample_data()
        data.decisions.append(Decision(text="스크립트 종료 표기 방어 테스트 </script><b>x</b>"))
        out = build_dashboard(data, tmpd, theme=theme)
        v = validate_dashboard_html(out, theme)
        check(f"샘플 빌드·검증 ({out.name}, {v['size']:,}B)", v["valid"], str(v["issues"]))
        html = out.read_text(encoding="utf-8")
        check("SoT 액센트 값 주입", f"--orange: {L['--orange']}" in html)
        check("데이터 주입(프로젝트명)", "A사 고객 컨퍼런스 2026 Discovery" in html)
        check("</script> 조기 종료 방어", html.count("</script>") == html.count("<script"))
        if theme["source"] == "sot":
            check("리멤버 로고 2종 임베드(라이트·다크)", html.count("data:image/png;base64,") == 2)
        else:
            print("  건너뜀 로고 임베드 (SoT 미발견 — 헤더는 발행 명의 텍스트로 대체)")
        check("발행 명의 기본값", PUBLISHER in html)

        # JSON 입력 왕복
        payload = to_json_payload(sample_data())
        warns: list = []
        back = data_from_dict(json.loads(json.dumps(payload, ensure_ascii=False)), warns)
        check("JSON → DashboardData 왕복", to_json_payload(back) == payload and not warns, str(warns))

        # 시리즈 누적 + carry-over
        s1 = sample_data()
        sync_series_data(s1, tmpd / "series")
        s2 = sample_data(); s2.series_session_no = 2
        sync_series_data(s2, tmpd / "series")
        doc = json.loads((tmpd / "series" / ".series-data" / "a-corp-discovery.json").read_text(encoding="utf-8"))
        check("시리즈 회차 누적 (2회)", doc["cumulative_stats"]["total_sessions"] == 2)
        ca, cp = load_series_carry_over("a-corp-discovery", tmpd / "series")
        check("carry-over (미완료 Action 3 · 미결 1)", len(ca) == 3 and len(cp) == 1 and all(a.is_carry_over for a in ca))

    print("build_dashboard self-test", "PASS" if ok else "FAIL")
    return 0 if ok else 1


# =====================================================================
# CLI
# =====================================================================

def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="mice-meeting-minutes HTML 회의록 대시보드 빌더")
    ap.add_argument("--input", type=Path, help="8축 데이터 JSON (DashboardData 필드)")
    ap.add_argument("--out", type=Path, help="출력 폴더")
    ap.add_argument("--theme", choices=("light", "dark"), help="첫 화면 테마 (기본 light)")
    ap.add_argument("--sample", type=Path, metavar="OUTDIR", help="내장 샘플로 빌드")
    ap.add_argument("--dump-sample", type=Path, metavar="FILE", help="입력 JSON 형식 예시 저장")
    ap.add_argument("--print-css", action="store_true", help="SoT 토큰 CSS 블록 출력")
    ap.add_argument("--self-test", action="store_true", help="자가 테스트")
    a = ap.parse_args(argv)

    if a.self_test:
        return self_test()
    if a.print_css:
        print(build_token_css(load_theme()))
        return 0
    if a.dump_sample:
        a.dump_sample.write_text(json.dumps(to_json_payload(sample_data()), ensure_ascii=False, indent=2),
                                 encoding="utf-8")
        print(f"샘플 JSON 저장: {a.dump_sample}")
        return 0
    if a.sample:
        data, out_dir = sample_data(), a.sample
    elif a.input and a.out:
        warns: list = []
        data = data_from_dict(json.loads(a.input.read_text(encoding="utf-8")), warns)
        for w in warns:
            print("경고:", w)
        out_dir = a.out
    else:
        ap.print_help()
        return 1
    if a.theme:
        data.theme = a.theme
    theme = load_theme()
    path = build_dashboard(data, out_dir, theme=theme)
    v = validate_dashboard_html(path, theme)
    print(f"대시보드 생성: {path}")
    print(f"검증: {'통과' if v['valid'] else '검토 필요'} · {v['size']:,}B · 토큰 {v['token_source']}"
          + (f" · {v['issues']}" if v["issues"] else ""))
    return 0 if v["valid"] else 2


if __name__ == "__main__":
    sys.exit(main())
