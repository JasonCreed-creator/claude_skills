#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""board_rows — mice-slack-ops contract ChainPayload → 팀 보드 프로젝트 탭 행(TSV) (stdlib).

열 정의 정본: mice-team-board/references/sheet-schema.md §2 (A~P).
payload 키: mice-slack-ops/references/contract-message.md §3·§6.
사용: python board_rows.py payload.json [--today 2026-10-05] [--project-id P-2026-012]
      python board_rows.py --self-test
출력: 헤더 + 1행 TSV. 갱신(action=update)이면 바꾸는 열만 채우고 나머지는 비운다(빈칸 = 유지).
상태(E): 신규는 '계약'(status_hint '준비'면 '준비'). 갱신은 status_hint가 '계약'·'준비'일 때만 채우고
         기본 'keep'이면 빈칸 — 이미 '준비' 이후인 행을 '계약'으로 되돌리지 않는다.
비고(O): payload `notes`(O열 완성 문자열)를 그대로 쓴다. notes가 비었을 때만 구조 필드로 조립한다.
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
STATUS_HINTS = {"keep", "계약", "준비"}
# notes가 비었을 때만 쓰는 조립 순서 (contract-message.md §6)
NOTE_FIELDS = (("leads", "리드"), ("renewal_id", "재계약ID"), ("item_id", "아이템ID"),
               ("inbound", "인입"), ("ops_cell", "운영 Cell"))


def build_notes(c: dict) -> str:
    """O열 비고. notes가 있으면 그대로(구조 필드 재기재 금지), 없으면 구조 필드로 조립."""
    if c.get("notes"):
        return str(c["notes"])
    parts = [c.get("deposit_note") or ""]
    for key, label in NOTE_FIELDS:
        if c.get(key) not in (None, ""):
            parts.append(f"{label} {c[key]}")
    return " · ".join(p for p in parts if p)


def build_status(c: dict) -> str:
    """E열 상태. status_hint: keep(기본) | 계약 | 준비."""
    hint = c.get("status_hint") or "keep"
    if hint not in STATUS_HINTS:
        raise ValueError(f"status_hint '{hint}' — keep | 계약 | 준비 중 하나여야 합니다")
    if c.get("action") == "update":
        return "" if hint == "keep" else hint
    return "준비" if hint == "준비" else "계약"


def build_row(payload: dict, today: str, project_id: str = "") -> dict:
    c = payload["contract"]
    event = (c.get("event_at_kst") or "")[:10]
    guarantee = c.get("guarantee")
    row = {
        "프로젝트ID": c.get("matched_row") or project_id,
        "행사명": c.get("title", ""),
        "발주처": c.get("client", ""),
        "유형": c.get("type", ""),
        "상태": build_status(c),
        "행사일": event,
        "베뉴": c.get("venue", ""),
        "게런티": "" if guarantee is None else str(guarantee),
        "예상 참가": "" if guarantee is None else str(guarantee),
        "계약금액": "" if c.get("revenue") is None else str(int(c["revenue"])),
        "비고": build_notes(c),
        "등록일": today,
    }
    if c.get("action") == "update":
        row = {k: (v if k in UPDATE_COLS or k == "프로젝트ID" else "") for k, v in row.items()}
    return row


def to_tsv(row: dict) -> str:
    return "\t".join(HEADER) + "\n" + "\t".join(row.get(h, "") for h in HEADER)


def self_test() -> int:
    full_notes = "행사 후 전액 완납 · 리드 50 · 재계약ID 1 · 아이템ID 2 · 인입 관리영업 · 운영 Cell A"
    p = {"$schema": "ChainPayload/v1", "source": "mice-slack-ops", "contract": {
        "client": "가나클라우드", "title": "가나 서밋 2026", "revenue": 33000000.0,
        "deposit_note": "행사 후 전액 완납", "event_at_kst": "2026-10-20T13:00:00+09:00",
        "venue": "A호텔", "guarantee": 30, "leads": 50, "renewal_id": "1", "item_id": "2", "inbound": "관리영업",
        "ops_cell": "A", "type": "①", "action": "new", "notes": full_notes}}
    # 신규: 상태 '계약', 비고 = notes 그대로(구조 필드 중복 조립 없음)
    r = build_row(p, "2026-10-05", "P-2026-012")
    assert r["프로젝트ID"] == "P-2026-012" and r["행사일"] == "2026-10-20" and r["계약금액"] == "33000000"
    assert r["게런티"] == "30" and r["상태"] == "계약"
    assert r["비고"] == full_notes and r["비고"].count("운영 Cell") == 1 and r["비고"].count("재계약ID") == 1
    tsv = to_tsv(r).splitlines()
    assert len(tsv) == 2 and len(tsv[1].split("\t")) == len(HEADER) == 16
    # 신규 + status_hint '준비'
    p["contract"]["status_hint"] = "준비"
    assert build_row(p, "2026-10-05", "P-2026-012")["상태"] == "준비"
    # notes가 비면 구조 필드로 조립(하위호환)
    p["contract"].update(notes="", status_hint="keep")
    f = build_row(p, "2026-10-05", "P-2026-012")
    assert f["비고"] == full_notes, f["비고"]
    # 갱신: 기본 keep → 상태 빈칸(유지), 바꾸지 않는 열 빈칸
    p["contract"].update(action="update", matched_row="P-2026-003", notes=full_notes)
    del p["contract"]["status_hint"]
    u = build_row(p, "2026-10-05")
    assert u["프로젝트ID"] == "P-2026-003" and u["발주처"] == "" and u["등록일"] == "" and u["계약금액"] == "33000000"
    assert u["상태"] == "", u["상태"]
    assert u["비고"] == full_notes
    # 갱신 + status_hint '계약'(견적 선등록 행) / '준비'
    for hint in ("계약", "준비"):
        p["contract"]["status_hint"] = hint
        assert build_row(p, "2026-10-05")["상태"] == hint
    p["contract"]["status_hint"] = "keep"
    assert build_row(p, "2026-10-05")["상태"] == ""
    # 잘못된 힌트는 거부
    p["contract"]["status_hint"] = "진행"
    try:
        build_row(p, "2026-10-05")
    except ValueError:
        pass
    else:
        raise AssertionError("잘못된 status_hint 미검출")
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
