"""
build_dashboard.py — HTML 인터랙티브 대시보드 빌더 (v2 메인 산출물)

dashboard-template.html에 8축 추출 데이터 + 메타 정보를 JSON으로 주입하여
단일 HTML 파일을 생성한다. 사용자는 이 파일을 다운로드해 브라우저에서 열고
window.storage 또는 localStorage에 시리즈 데이터를 누적할 수 있다.

산출:
  - dashboard_[프로젝트]_[YYYYMMDD].html (메인)
  - 시리즈 모드 시 .series-data/[series_id].json 동기화

데이터 구조는 v1의 build_minutes.py의 MinutesData를 dict로 직렬화하여 재사용.
"""

import json
import re
import sys
from dataclasses import dataclass, field, asdict, is_dataclass
from datetime import date
from pathlib import Path
from typing import Optional

# UTF-8 stdout/stderr 강제 (Windows cp949 환경 크래시 방지)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


# =====================================================================
# 데이터 모델 (v1 구조 호환 + 대시보드용 필드 보강)
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
    """대시보드용 통합 데이터 모델"""
    project_name: str
    meeting_date: str          # YYYY-MM-DD
    meeting_time: str = ""     # HH:MM~HH:MM
    location: str = ""
    attendees: list[str] = field(default_factory=list)
    meeting_type: str = "A"    # A/B/C/D/E
    type_label: str = "외부 클라이언트 미팅"
    mode: str = "internal"     # external/internal
    client_id: str = "personal"

    # 8축 데이터
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

    # Slack 요약용 1줄 코멘트 (Internal 모드)
    strategy_oneliner: Optional[str] = None

    # 메타
    author: str = ""  # 외부 주입 필수, 기본값 없음 (회사·인명 종속 회피)
    redaction_log: list[dict] = field(default_factory=list)


# =====================================================================
# JSON 직렬화
# =====================================================================

def _serialize(obj):
    """dataclass·list·dict를 JSON 직렬화 가능 형태로 변환"""
    if is_dataclass(obj):
        return {k: _serialize(v) for k, v in asdict(obj).items()}
    if isinstance(obj, list):
        return [_serialize(item) for item in obj]
    if isinstance(obj, tuple):
        return [_serialize(item) for item in obj]
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    return obj


def to_json_payload(data: DashboardData) -> dict:
    """DashboardData → JSON dict 변환 (대시보드 주입용)"""
    payload = _serialize(data)

    # discussion이 dict[agenda_idx] = [(speaker, text), ...] 구조이면 [{speaker, text}] 형태로 정규화
    if isinstance(payload.get("discussion"), dict):
        normalized_discussion = {}
        for k, v in payload["discussion"].items():
            normalized_discussion[str(k)] = [
                ([item[0], item[1]] if isinstance(item, (list, tuple)) and len(item) >= 2
                 else item)
                for item in v
            ]
        payload["discussion"] = normalized_discussion

    return payload


# =====================================================================
# HTML 빌더
# =====================================================================

def render_dashboard_html(data: DashboardData,
                           template_path: Path) -> str:
    """템플릿에 데이터 주입하여 최종 HTML 문자열 반환"""
    if not template_path.exists():
        raise FileNotFoundError(f"템플릿 미발견: {template_path}")

    template = template_path.read_text(encoding="utf-8")

    # 페이지 제목
    title = f"{data.project_name} 미팅 대시보드 ({data.meeting_date})"

    # JSON 데이터
    payload = to_json_payload(data)
    payload_json = json.dumps(payload, ensure_ascii=False, indent=2)

    # 플레이스홀더 치환
    html = template.replace("{{TITLE}}", _escape_html(title))
    html = html.replace("{{INITIAL_DATA}}", payload_json)

    return html


def _escape_html(s: str) -> str:
    """HTML 엔티티 이스케이프"""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


# =====================================================================
# 시리즈 데이터 동기화
# =====================================================================

def sync_series_data(data: DashboardData, output_dir: Path) -> Optional[Path]:
    """
    시리즈 모드 활성화 시 .series-data/[series_id].json 동기화.
    이미 존재하면 carry-over 처리, 없으면 신규 생성.
    """
    if not data.series_id:
        return None

    series_dir = output_dir / ".series-data"
    series_dir.mkdir(parents=True, exist_ok=True)
    series_path = series_dir / f"{data.series_id}.json"

    # 기존 데이터 로드 (있으면)
    existing = {}
    if series_path.exists():
        try:
            existing = json.loads(series_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}

    # 본 회차 데이터 추가
    sessions = existing.get("sessions", [])
    session_no = data.series_session_no or (len(sessions) + 1)

    actions_payload = _serialize(data.actions)
    pending_payload = _serialize(data.pending)

    new_session = {
        "session_no": session_no,
        "date": data.meeting_date,
        "type": data.meeting_type,
        "actions": actions_payload,
        "pending_items": pending_payload,
        "decisions_count": len(data.decisions),
        "completion_rate": _calc_completion(data.actions),
    }

    # 동일 회차 갱신, 없으면 추가
    sessions = [s for s in sessions if s.get("session_no") != session_no]
    sessions.append(new_session)
    sessions.sort(key=lambda s: s.get("session_no", 0))

    # 누적 통계
    all_actions = []
    for s in sessions:
        all_actions.extend(s.get("actions", []))

    total = len(all_actions)
    done = sum(1 for a in all_actions if a.get("status") == "DONE")
    blocked = sum(1 for a in all_actions if a.get("status") == "BLOCKED")
    todo = sum(1 for a in all_actions if a.get("status") == "TODO")
    doing = sum(1 for a in all_actions if a.get("status") == "DOING")

    # 장기 미해결 (3회차 이상 carry-over)
    carry_count = {}
    for a in all_actions:
        aid = a.get("id")
        if a.get("is_carry_over") and aid:
            carry_count[aid] = carry_count.get(aid, 0) + 1
    long_pending = [aid for aid, c in carry_count.items() if c >= 3]

    output = {
        "series_id": data.series_id,
        "project_name": data.project_name,
        "client_id": data.client_id,
        "default_type": data.meeting_type,
        "created_at": existing.get("created_at", date.today().isoformat()),
        "last_updated": date.today().isoformat(),
        "sessions": sessions,
        "cumulative_stats": {
            "total_sessions": len(sessions),
            "total_actions": total,
            "done": done,
            "doing": doing,
            "blocked": blocked,
            "todo": todo,
            "completion_rate": round(done / total, 2) if total else 0.0,
            "long_pending_actions": long_pending,
        },
    }

    series_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    return series_path


def _calc_completion(actions: list[ActionItem]) -> float:
    if not actions:
        return 0.0
    done = sum(1 for a in actions if a.status == "DONE")
    return round(done / len(actions), 2)


def load_series_carry_over(series_id: str,
                            output_dir: Path) -> tuple[list[ActionItem],
                                                        list[PendingItem]]:
    """이전 회차 데이터에서 carry-over 대상 자동 추출"""
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

    # 가장 최근 세션의 미완료 Action + 모든 미결 사항
    latest = sessions[-1]
    carry_actions = []
    for a_dict in latest.get("actions", []):
        if a_dict.get("status") in ("TODO", "DOING", "BLOCKED"):
            a_dict["is_carry_over"] = True
            carry_actions.append(ActionItem(**{
                k: v for k, v in a_dict.items()
                if k in ActionItem.__dataclass_fields__
            }))

    carry_pending = []
    for p_dict in latest.get("pending_items", []):
        p_dict["is_carry_over"] = True
        carry_pending.append(PendingItem(**{
            k: v for k, v in p_dict.items()
            if k in PendingItem.__dataclass_fields__
        }))

    return carry_actions, carry_pending


# =====================================================================
# 메인 빌드 함수
# =====================================================================

def build_dashboard(data: DashboardData,
                    output_dir: Path,
                    template_path: Optional[Path] = None) -> Path:
    """
    대시보드 .html 생성 + 시리즈 데이터 동기화.

    Returns:
        생성된 .html 파일 경로
    """
    if template_path is None:
        template_path = (Path(__file__).parent.parent
                         / "assets" / "dashboard-template.html")

    output_dir.mkdir(parents=True, exist_ok=True)

    # HTML 렌더링
    html = render_dashboard_html(data, template_path)

    # 파일명
    date_str = data.meeting_date.replace("-", "")
    project_slug = re.sub(r"[^a-zA-Z0-9가-힣-]", "-",
                          data.project_name.lower().strip())
    filename = f"dashboard_{project_slug}_{date_str}.html"
    output_path = output_dir / filename

    output_path.write_text(html, encoding="utf-8")

    # 시리즈 데이터 동기화
    sync_series_data(data, output_dir)

    return output_path


# =====================================================================
# 검증
# =====================================================================

def validate_dashboard_html(html_path: Path) -> dict:
    """생성된 HTML 검증"""
    if not html_path.exists():
        return {"valid": False, "error": "파일 미생성"}

    content = html_path.read_text(encoding="utf-8")
    issues = []

    # 플레이스홀더 잔존 확인
    if "{{TITLE}}" in content:
        issues.append("TITLE 플레이스홀더 미치환")
    if "{{INITIAL_DATA}}" in content:
        issues.append("INITIAL_DATA 플레이스홀더 미치환")

    # 핵심 라이브러리 호출 확인
    if "react@18" not in content and "React" not in content:
        issues.append("React 라이브러리 미연결")
    if "recharts" not in content.lower():
        issues.append("Recharts 라이브러리 미연결")

    # jc-design-system 시그니처 토큰 확인
    signature_hex = ["0A2540", "2962FF", "FF5722", "E91E63", "00E676"]
    missing_tokens = [h for h in signature_hex
                      if f"#{h}" not in content.upper().replace(" ", "")
                      and h not in content.upper()]
    if missing_tokens:
        issues.append(f"시그니처 토큰 미적용: {missing_tokens}")

    return {
        "valid": len(issues) == 0,
        "size": html_path.stat().st_size,
        "issues": issues,
    }


# =====================================================================
# CLI 테스트
# =====================================================================

if __name__ == "__main__":
    sample = DashboardData(
        project_name="clientA-discovery",
        meeting_date="2026-05-09",
        meeting_time="14:00~15:30",
        location="PCO 본사 회의실",
        attendees=["참석자 1 (PCO)", "참석자 2 (협력사)", "참석자 3 (발주처)"],
        meeting_type="A",
        type_label="외부 클라이언트 미팅",
        mode="internal",
        client_id="clientA",
        agenda=["행사 컨셉 검토", "일정 협의", "예산 협의", "후속 미팅 일정"],
        decisions=[
            Decision(text="행사 형식: 1일 컨퍼런스 + 1:1 미팅룸 50%·데모 부스 50%",
                     timestamp="00:01", rationale="양측 동의"),
            Decision(text="행사 일자: 2026-06-18(목)",
                     timestamp="00:04", rationale="고객사A 분기 + 베뉴 가용"),
            Decision(text="베뉴 답사: 2026-05-22 양사 동행",
                     timestamp="00:04"),
        ],
        actions=[
            ActionItem(id="CA-DISC-001", owner="참석자 1 (PCO)",
                       action="베뉴 후보 3곳 비교 자료 제출", due="2026-05-12",
                       priority="P1", status="TODO"),
            ActionItem(id="CA-DISC-002", owner="참석자 2 (협력사)",
                       action="명함 데이터 기반 타겟 250명 추출", due="2026-05-14",
                       priority="P1", status="TODO"),
            ActionItem(id="CA-DISC-003", owner="참석자 3 (발주처)",
                       action="본사 동시통역 결재 진행", due="2026-05-15",
                       priority="P1", status="BLOCKED"),
            ActionItem(id="CA-DISC-004", owner="참석자 1 (PCO)",
                       action="베뉴 사전 가예약 6/18·6/25 양일", due="2026-05-12",
                       priority="P0", status="TODO"),
        ],
        risks=[
            Risk(text="베뉴 가용일 6월 중순 충돌 다수", impact="상",
                 timestamp="00:07", response="6/18·6/25 양일 사전 가예약"),
        ],
        pending=[
            PendingItem(text="동시통역 부스 설치 여부",
                        reason="고객사A 본사 결재 필요",
                        next_review="다음 미팅 (5/16)",
                        owner="김부장 (고객사A)"),
        ],
        next_steps=[
            NextStep(title="다음 미팅", date_str="2026-05-16(금) 14:00",
                     attendees="본 미팅 동일 + 고객사A 본사 시니어",
                     agenda="동시통역 결재 결과 + 베뉴 답사 결과"),
        ],
        strategy_note=StrategyNote(
            who="김부장이 의사결정자로 보이지만 실제 권한은 본사 시니어",
            what="표면적 행사 컨셉 협의 + 실제로는 운영 역량 검증",
            when_="6월 18일 행사 기준 5/9 미팅은 약간 빠듯",
            where="결정 라인 김부장 → 본사 시니어 → 글로벌 본사",
            why="고객사A 한국 시장 본격 진출 시점",
            how="1:1 미팅룸 ROI 측정 KPI 사전 합의가 다음 행사 수주 관건"
        ),
        strategy_oneliner="본사 시니어 5/16 미팅이 진짜 클라이언트 검증 — KPI 사전 합의 필수",
        series_id="clientA-discovery",
        series_session_no=1,
    )

    output_dir = Path("./output")
    path = build_dashboard(sample, output_dir)
    print(f"✅ 대시보드 생성: {path}")

    validation = validate_dashboard_html(path)
    print(f"검증 결과: {validation}")
