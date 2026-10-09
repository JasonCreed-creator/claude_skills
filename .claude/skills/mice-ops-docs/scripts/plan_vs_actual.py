#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""plan_vs_actual — 큐시트 계획 vs 실측 시각 → 지연·초과 세그먼트 KPI (stdlib).

입력: mice-run-of-show ChainPayload(JSON, plan.cues) + 실측 JSON({"actual":[{cueNo,start,end}]})
출력: 표(기본) 또는 --json 으로 rounds 배열 + 요약
사용: python plan_vs_actual.py plan.json actual.json [--json] [--tolerance 2]
      python plan_vs_actual.py --self-test
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def to_min(hhmm: str) -> int:
    h, m = hhmm.strip().split(":")
    return int(h) * 60 + int(m)


def compare(plan: dict, actual: dict, tolerance: int = 2) -> dict:
    cues = plan.get("plan", {}).get("cues", [])
    acts = {a["cueNo"]: a for a in actual.get("actual", [])}
    rounds, delays = [], []
    for c in cues:
        a = acts.get(c["cueNo"])
        row = {"cueNo": c["cueNo"], "segment": c.get("segment", ""), "delayMin": None, "overMin": None}
        if a and a.get("start"):
            row["delayMin"] = to_min(a["start"]) - to_min(c["clock"])
            delays.append(row["delayMin"])
            if a.get("end") and c.get("durationMin") is not None:
                row["overMin"] = (to_min(a["end"]) - to_min(a["start"])) - int(c["durationMin"])
        rounds.append(row)
    measured = [r for r in rounds if r["delayMin"] is not None]
    on_time = [r for r in measured if r["delayMin"] <= tolerance]
    summary = {
        "cues": len(rounds),
        "measured": len(measured),
        "onTimeRate": round(len(on_time) / len(measured), 3) if measured else None,
        "avgDelayMin": round(sum(delays) / len(delays), 1) if delays else None,
        "overSegments": sum(1 for r in rounds if (r["overMin"] or 0) > tolerance),
        "toleranceMin": tolerance,
    }
    return {"rounds": rounds, "summary": summary}


def render(result: dict) -> str:
    lines = ["| Cue | 세그먼트 | 시작 지연(분) | 초과(분) |", "|-----|----------|---------------|----------|"]
    for r in result["rounds"]:
        d = "[미확보]" if r["delayMin"] is None else r["delayMin"]
        o = "[미확보]" if r["overMin"] is None else r["overMin"]
        lines.append(f"| {r['cueNo']} | {r['segment']} | {d} | {o} |")
    s = result["summary"]
    lines.append("")
    lines.append(f"정시 시작률 {s['onTimeRate']} · 평균 지연 {s['avgDelayMin']}분 · 초과 세그먼트 {s['overSegments']}개 (허용 {s['toleranceMin']}분)")
    return "\n".join(lines)


def self_test() -> int:
    plan = {"plan": {"cues": [
        {"cueNo": "C01", "clock": "09:00", "segment": "등록", "durationMin": 30},
        {"cueNo": "C02", "clock": "09:30", "segment": "개회", "durationMin": 10},
        {"cueNo": "C03", "clock": "09:40", "segment": "기조연설", "durationMin": 30},
    ]}}
    actual = {"actual": [
        {"cueNo": "C01", "start": "09:00", "end": "09:32"},
        {"cueNo": "C02", "start": "09:33", "end": "09:43"},
    ]}
    r = compare(plan, actual)
    assert r["rounds"][0]["delayMin"] == 0 and r["rounds"][0]["overMin"] == 2
    assert r["rounds"][1]["delayMin"] == 3 and r["rounds"][1]["overMin"] == 0
    assert r["rounds"][2]["delayMin"] is None
    s = r["summary"]
    assert s["measured"] == 2 and s["onTimeRate"] == 0.5 and s["avgDelayMin"] == 1.5 and s["overSegments"] == 0
    assert "[미확보]" in render(r)
    print("self-test OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", nargs="?")
    ap.add_argument("actual", nargs="?")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--tolerance", type=int, default=2)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not (a.plan and a.actual):
        ap.error("plan.json actual.json 두 파일이 필요합니다")
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    actual = json.loads(Path(a.actual).read_text(encoding="utf-8"))
    result = compare(plan, actual, a.tolerance)
    sys.stdout.write((json.dumps(result, ensure_ascii=False, indent=2) if a.json else render(result)) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
