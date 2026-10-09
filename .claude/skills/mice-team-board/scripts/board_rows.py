#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""board_rows — mice-slack-ops contract ChainPayload → 팀 보드 프로젝트 탭 행(TSV) (stdlib).

열 매핑 정본: mice-slack-ops/references/contract-message.md §3 (A~P).
사용: python board_rows.py payload.json [--today 2026-10-05] [--project-id P-2026-012]
      python board_rows.py --self-test
출력: 헤더 + 1행 TSV. 갱신(action=update)이면 바꾸는 열만 채우고 나머지는 비운다.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

HEADER = ["프로젝트ID", "행사명", "발주처", "유형", "상태", "행사일", "G", "H", "I", "J",
          "베뉴", "게런티", "예상 참가", "계약금액", "비고", "등록일"]
UPDATE_COLS = {"행사명", "상태", "게런티", "예상 참가", "계약금액", "비고"}


def build_row(payload: dict, today: str, project_id: str = "") -> dict:
    c = payload["contract"]
    event = (c.get("event_at_kst") or "")[:10]
    notes = [c.get("notes") or "", c.get("deposit_note") or ""]
    for key, label in (("renewal_id", "재계약ID"), ("item_id", "아이템ID"), ("inbound", "인입"), ("ops_cell", "운영 Cell")):
        if c.get(key):
            notes.append(f"{label} {c[key]}")
    guarantee = c.get("guarantee")
    row = {
        "프로젝트ID": c.get("matched_row") or project_id,
        "행사명": c.get("title", ""),
        "발주처": c.get("client", ""),
        "유형": c.get("type", ""),
        "상태": "계약",
        "행사일": event,
        "베뉴": c.get("venue", ""),
        "게런티": "" if guarantee is None else str(guarantee),
        "예상 참가": "" if guarantee is None else str(guarantee),
        "계약금액": "" if c.get("revenue") is None else str(int(c["revenue"])),
        "비고": " · ".join(n for n in notes if n),
        "등록일": today,
    }
    if c.get("action") == "update":
        row = {k: (v if k in UPDATE_COLS or k == "프로젝트ID" else "") for k, v in row.items()}
    return row


def to_tsv(row: dict) -> str:
    return "\t".join(HEADER) + "\n" + "\t".join(row.get(h, "") for h in HEADER)


def self_test() -> int:
    p = {"$schema": "ChainPayload/v1", "source": "mice-slack-ops", "contract": {
        "client": "가나클라우드", "title": "가나 서밋 2026", "revenue": 33000000.0,
        "deposit_note": "행사 후 전액 완납", "event_at_kst": "2026-10-20T13:00:00+09:00",
        "venue": "A호텔", "guarantee": 30, "renewal_id": "1", "item_id": "2", "inbound": "관리영업",
        "ops_cell": "A", "type": "①", "action": "new", "notes": "리드 50"}}
    r = build_row(p, "2026-10-05", "P-2026-012")
    assert r["프로젝트ID"] == "P-2026-012" and r["행사일"] == "2026-10-20" and r["계약금액"] == "33000000"
    assert r["게런티"] == "30" and r["상태"] == "계약" and "재계약ID 1" in r["비고"]
    tsv = to_tsv(r).splitlines()
    assert len(tsv) == 2 and len(tsv[1].split("\t")) == len(HEADER) == 16
    p["contract"].update(action="update", matched_row="P-2026-003")
    u = build_row(p, "2026-10-05")
    assert u["프로젝트ID"] == "P-2026-003" and u["발주처"] == "" and u["등록일"] == "" and u["계약금액"] == "33000000"
    print("self-test OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("payload", nargs="?")
    ap.add_argument("--today", default=dt.date.today().isoformat())
    ap.add_argument("--project-id", default="")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.payload:
        ap.error("payload.json 경로가 필요합니다")
    payload = json.loads(Path(a.payload).read_text(encoding="utf-8"))
    sys.stdout.write(to_tsv(build_row(payload, a.today, a.project_id)) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
