#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mice-sponsor-deck v2.0 - Sample Generator

가상 시나리오 'TOBESOFT TECH FORUM 2026' 의 콘텐츠 JSON 을 생성한다.
- 1차 입력: sponsor-candidates.json (mice-meeting-minutes 체이닝 시뮬레이션)
- 2차 출력: deck-content.json (HTML 1차 + PPTX 2차 단일 source)
- 3차 출력: validation-summary.json (자가 검증 결과)

본 스크립트는 sprint-03 검증 에이전트 (3 logic check) 가 실행한다.
실제 HTML / PPTX 빌드는 별도 빌더가 수행하며 본 스크립트는 입력 데이터 준비만 담당한다.

Usage:
    python3 sample_generator.py [--out-dir OUT_DIR]

기본 출력 디렉토리: C:/Users/icejc/mice-skills-work/sprint-03-mice-sponsor-deck/_samples/

UTF-8 stdout 표준 (Sprint 2 백로그 BL-S2-근본 반영):
    sys.stdout.reconfigure(encoding='utf-8') - Windows cp949 환경 대응
"""

import sys
import json
import os
import argparse
from datetime import datetime
from pathlib import Path

# Windows cp949 환경 대응 - UTF-8 stdout 표준
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


# ============================================================
# 1. 가상 시나리오 - TOBESOFT TECH FORUM 2026
# ============================================================
SCENARIO = {
    "event_meta": {
        "event_name": "TOBESOFT TECH FORUM 2026",
        "event_subtitle": "AI·Cloud·Enterprise Tech의 다음 10년",
        "event_date": "2026-09-15",
        "event_venue": "코엑스 컨벤션홀",
        "event_type": "conference",
        "organizer": "[주최사명]",
        "expected_attendees": 5200,
        "is_provisional_slots": False
    },
    "audience": {
        "industry_distribution": {
            "tech": 42,
            "finance": 24,
            "manufacturing": 18,
            "healthcare": 10,
            "others": 6
        },
        "decision_maker_ratio": 32,
        "c_level_plus_executive_ratio": 23,
        "b2b_ratio": 87,
        "data_source": "2024년 회차 등록 + 자기 응답"
    }
}


# ============================================================
# 2. mice-meeting-minutes 체이닝 시뮬레이션 - sponsor-candidates.json
# ============================================================
def build_sponsor_candidates_json():
    """
    mice-meeting-minutes 가 Discovery 미팅에서 추출했을 sponsor candidates JSON 을 생성.
    실제 체이닝 시나리오에서는 mice-meeting-minutes 가 출력하는 파일.
    """
    return {
        "$schema": "mice-sponsor-deck/v2.0",
        "event_meta": SCENARIO["event_meta"],
        "sponsor_candidates": [
            {
                "name": "[Tech 기업 A]",
                "industry": "tech",
                "tier_target": "T1",
                "priority": "high",
                "decision_maker": "CMO",
                "expected_budget_krw": None,
                "notes": "AI 솔루션 핵심 메시지 매칭. 작년 유사 행사 협찬 이력 있음."
            },
            {
                "name": "[Tech 기업 B]",
                "industry": "tech",
                "tier_target": "T2",
                "priority": "high",
                "decision_maker": "마케팅 본부장",
                "expected_budget_krw": None,
                "notes": "Cloud 사업 강화 전략 - 키노트 세션 슬롯 관심"
            },
            {
                "name": "[Finance 기업 A]",
                "industry": "finance",
                "tier_target": "T2",
                "priority": "high",
                "decision_maker": "디지털전략 임원",
                "expected_budget_krw": None,
                "notes": "VIP 만찬 좌석 6석 강조 필요. 금융 산업 ROI 케이스 강조."
            },
            {
                "name": "[Tech 기업 C]",
                "industry": "tech",
                "tier_target": "T3",
                "priority": "med",
                "decision_maker": None,
                "expected_budget_krw": None,
                "notes": "트랙 세션 스폰서 관심 표명. 부스 18~27㎡ 충분."
            },
            {
                "name": "[B2B 산업재 기업 A]",
                "industry": "b2b",
                "tier_target": "T3",
                "priority": "med",
                "decision_maker": "사업개발 임원",
                "expected_budget_krw": None,
                "notes": "Tech 컨퍼런스를 통해 IT 의사결정권자 1:1 매칭 미팅 관심"
            },
            {
                "name": "[Tech 기업 D]",
                "industry": "tech",
                "tier_target": "T4",
                "priority": "low",
                "decision_maker": None,
                "expected_budget_krw": None,
                "notes": "신생 SaaS 스타트업 - 컴팩트 부스 + 사이니지 충분"
            }
        ],
        "audience_hints": {
            "industry_distribution": {
                "tech": 42,
                "finance": 24,
                "manufacturing": 18,
                "healthcare": 10,
                "others": 6
            },
            "decision_maker_ratio": 32,
            "c_level_plus_executive_ratio": 23,
            "b2b_ratio": 87,
            "data_source": "2024년 회차 등록 + 자기 응답"
        },
        "extracted_from": "mice-meeting-minutes",
        "extraction_date": "2026-05-27",
        "meeting_minutes_ref": {
            "meeting_id": "discovery-tobesoft-2026-04-10",
            "section": "Action Items + 전략 메모"
        }
    }


# ============================================================
# 3. sponsor-candidates -> deck-content 변환
# ============================================================
INDUSTRY_LABELS = {
    "tech": "IT·소프트웨어",
    "finance": "금융·보험",
    "manufacturing": "제조·산업재",
    "healthcare": "헬스케어·바이오",
    "cpg": "유통·소비재",
    "b2b": "산업재·B2B 제조",
    "public": "공공·교육·연구",
    "others": "기타"
}

ROI_INDUSTRY_LABELS = {
    "tech": "Tech 산업 스폰서 ROI",
    "finance": "Finance 산업 스폰서 ROI",
    "cpg": "CPG 산업 스폰서 ROI",
    "b2b": "B2B 산업재 스폰서 ROI",
    "public": "공공·교육·연구 스폰서 ROI"
}

# CHART_SERIES — jc-design-system(SoT) §6 JSON 의 color.data 를 런타임 로딩(실패 시 폴백).
# 주의: "0A2540"은 data-5(Deep Navy 5순위 차트 시리즈) 정본이며 *페이지 배경 아님*.
#       다크 차트 시리즈는 mode-mapping.md §3.2 (data-5=C9CFD8) 정본 사용.
def _load_jc_data():
    import json, re
    from pathlib import Path
    try:
        sot = Path(__file__).resolve().parents[2] / "jc-design-system" / "references" / "signature-tokens.md"
        m = re.search(r"```json\s*\n(.*?)\n```", sot.read_text(encoding="utf-8"), re.S)
        return (json.loads(m.group(1)).get("color", {}) or {}).get("data") if m else None
    except Exception:
        return None

CHART_COLORS = [c.lstrip("#") for c in (_load_jc_data()
                or ["#2962FF", "#E91E63", "#FF5722", "#00E676", "#0A2540"])][:5]  # SoT 라이트 data 시리즈

# Tier 컬러 토큰 (HEX without #) — SoT 미러: 라이트 Tier 정본 (design-tokens-mapping.md §2.2 / signature-tokens.md)
# 다크(dark_mixed) 렌더 시 Tier 다크 변형은 mode-mapping.md §7 정본을 빌더가 적용
# (T1 #F06292 · T2 #5B8DEF · T3 #FF7043 · T4 #B8C5D6 · T5 #3D5F87 · T6 #69F0AE).
TIER_COLORS_HEX = {
    "T1": "E91E63",
    "T2": "2962FF",
    "T3": "FF5722",
    "T4": "5A6270",
    "T5": "C9CFD8",
    "T6": "00E676"
}

TIER_COLOR_TOKENS = {
    "T1": "--jc-point-magenta",
    "T2": "--jc-accent",
    "T3": "--jc-point-orange",
    "T4": "--jc-text-muted",
    "T5": "--jc-border-strong",
    "T6": "--jc-point-neon"
}


def select_top_industries(sponsor_candidates, k=2):
    """sponsor_candidates 의 industry 빈도 분석 -> 상위 k개 산업 자동 선정."""
    freq = {}
    for c in sponsor_candidates:
        ind = c["industry"]
        # tier T1, T2 우선순위 부여
        weight = 3 if c["tier_target"] in ("T1", "T2") else 1
        freq[ind] = freq.get(ind, 0) + weight
    # priority high 가중치 추가
    for c in sponsor_candidates:
        if c["priority"] == "high":
            freq[c["industry"]] = freq.get(c["industry"], 0) + 2
    sorted_inds = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [ind for ind, _ in sorted_inds[:k]]


def build_industry_distribution(audience_hints):
    """audience_hints 의 industry distribution -> deck-content 형식."""
    dist = audience_hints.get("industry_distribution", {})
    items = sorted(dist.items(), key=lambda x: x[1], reverse=True)
    result = []
    for idx, (key, ratio) in enumerate(items):
        result.append({
            "name": INDUSTRY_LABELS.get(key, key),
            "ratio": ratio,
            "color": CHART_COLORS[idx] if idx < len(CHART_COLORS) else "5A6270"
        })
    return result


def build_tiers():
    """Tier 5단 표준 구조 (sponsor-candidates 의 tier_target 와 정렬)."""
    return [
        {
            "id": "T1", "name_ko": "타이틀", "name_en": "Title",
            "slots": 1, "price": None, "price_display": "가격 별도 협의",
            "color_token": TIER_COLOR_TOKENS["T1"], "color_hex": TIER_COLORS_HEX["T1"],
            "benefits_summary": [
                "행사명 결합권",
                "키노트 발표 30분",
                "메인 사이니지 8회",
                "VIP 만찬 단독 호스트",
                "부스 54㎡ 메인 동선"
            ]
        },
        {
            "id": "T2", "name_ko": "플래티넘", "name_en": "Platinum",
            "slots": 3, "price": None, "price_display": "가격 별도 협의",
            "color_token": TIER_COLOR_TOKENS["T2"], "color_hex": TIER_COLORS_HEX["T2"],
            "benefits_summary": [
                "메인 무대 노출",
                "프리미엄 부스 36㎡",
                "VIP 만찬 6석",
                "보도자료 공동 명시",
                "SNS 2회"
            ]
        },
        {
            "id": "T3", "name_ko": "골드", "name_en": "Gold",
            "slots": 6, "price": None, "price_display": "가격 별도 협의",
            "color_token": TIER_COLOR_TOKENS["T3"], "color_hex": TIER_COLORS_HEX["T3"],
            "benefits_summary": [
                "트랙 세션 30분",
                "표준 부스 27㎡",
                "임원 라운지 출입",
                "홈페이지 노출",
                "리드 400건"
            ]
        },
        {
            "id": "T4", "name_ko": "실버", "name_en": "Silver",
            "slots": 10, "price": None, "price_display": "가격 별도 협의",
            "color_token": TIER_COLOR_TOKENS["T4"], "color_hex": TIER_COLORS_HEX["T4"],
            "benefits_summary": [
                "사이니지 2회",
                "컴팩트 부스 15㎡",
                "프로그램북 광고",
                "리드 200건"
            ]
        },
        {
            "id": "T5", "name_ko": "브론즈", "name_en": "Bronze",
            "slots": "무제한", "price": None, "price_display": "가격 별도 협의",
            "color_token": TIER_COLOR_TOKENS["T5"], "color_hex": TIER_COLORS_HEX["T5"],
            "benefits_summary": [
                "프로그램북 내지",
                "홈페이지 리스트",
                "행사 패스"
            ]
        }
    ]


def build_matrix():
    """Benefits Matrix - 7카테고리에서 컨퍼런스 우선순위 (5 연사, 7 VIP, 1 브랜딩) 발췌."""
    return {
        "categories": [
            {"id": 1, "ko": "브랜딩 노출"},
            {"id": 2, "ko": "미디어 노출"},
            {"id": 4, "ko": "부스·공간"},
            {"id": 5, "ko": "연사·세션 권리"},
            {"id": 6, "ko": "리드·CRM"},
            {"id": 7, "ko": "VIP·네트워킹"}
        ],
        "rows": [
            {"item": "메인 사이니지", "category_id": 1,
             "T1": "8회", "T2": "6회", "T3": "4회", "T4": "2회", "T5": "✓"},
            {"item": "보도자료 명시", "category_id": 2,
             "T1": "메인", "T2": "공동", "T3": "본문", "T4": "부록", "T5": "—"},
            {"item": "공식 SNS 포스트", "category_id": 2,
             "T1": "3회", "T2": "2회", "T3": "1회", "T4": "—", "T5": "—"},
            {"item": "부스 면적", "category_id": 4,
             "T1": "54㎡", "T2": "36㎡", "T3": "27㎡", "T4": "15㎡", "T5": "—"},
            {"item": "키노트·세션", "category_id": 5,
             "T1": "키노트 30분", "T2": "메인 45분", "T3": "트랙 30분", "T4": "—", "T5": "—"},
            {"item": "리드 데이터", "category_id": 6,
             "T1": "1,000건+", "T2": "600건", "T3": "400건", "T4": "200건", "T5": "—"},
            {"item": "VIP 만찬 좌석", "category_id": 7,
             "T1": "단독 10석", "T2": "6석", "T3": "—", "T4": "—", "T5": "—"}
        ],
        "slot_row": {"T1": "1석", "T2": "3석", "T3": "6석", "T4": "10석", "T5": "무제한"}
    }


def build_roi_cases(top_industries, total_attendees, audience_hints):
    """상위 산업 ROI 케이스 - roi-case-templates.md §3, §4, §6 베이스."""
    cases = []
    dec_ratio = audience_hints.get("decision_maker_ratio", 30)
    c_level_ratio = audience_hints.get("c_level_plus_executive_ratio", 23)
    dist = audience_hints.get("industry_distribution", {})

    for ind in top_industries:
        ind_ratio = dist.get(ind, 0)
        ind_participants = round(total_attendees * ind_ratio / 100)
        decision_makers = round(ind_participants * dec_ratio / 100)
        c_level = round(total_attendees * (ind_ratio / 100) * (c_level_ratio / 100))

        if ind == "tech":
            booth_visitors = round(decision_makers * 0.12)
            leads = round(booth_visitors * 0.35)
            cases.append({
                "industry": "tech",
                "industry_label": "Tech 산업 스폰서 ROI",
                "premise": [
                    f"IT 참가자 약 {ind_participants:,}명",
                    f"IT 의사결정권자 약 {decision_makers:,}명"
                ],
                "formula": [
                    "부스 전환율 12% × 의사결정권자",
                    "리드 전환율 35% 적용"
                ],
                "estimate": {
                    "headline": f"리드 약 {max(leads-5, 5)}~{leads+5}건",
                    "secondary": "PR 가치 약 KRW 25M"
                },
                "caption": "ⓘ 본 수치는 산업 벤치마크 기반 추정치이며, 실제 결과는 노출 환경·콘텐츠 품질에 따라 변동됩니다."
            })
        elif ind == "finance":
            cases.append({
                "industry": "finance",
                "industry_label": "Finance 산업 스폰서 ROI",
                "premise": [
                    f"금융 참가자 약 {ind_participants:,}명",
                    f"C-Level + 임원 약 {c_level:,}명"
                ],
                "formula": [
                    "VIP 만찬 단독 직접 접점 8~10명",
                    "1:1 미팅 평균 LTV × 5% 전환"
                ],
                "estimate": {
                    "headline": "직접 접점 약 8~10명",
                    "secondary": "잠재 영업 가치 산업 벤치마크 기반"
                },
                "caption": "ⓘ 본 수치는 산업 벤치마크 기반 추정치이며, 실제 결과는 노출 환경·콘텐츠 품질에 따라 변동됩니다."
            })
        elif ind in ("manufacturing", "b2b"):
            booth_visitors = round(decision_makers * 0.10)
            leads = round(booth_visitors * 0.30)
            cases.append({
                "industry": "b2b",
                "industry_label": "B2B 산업재 스폰서 ROI",
                "premise": [
                    f"산업 참가자 약 {ind_participants:,}명",
                    f"의사결정권자 약 {decision_makers:,}명"
                ],
                "formula": [
                    "부스 전환율 10% × 의사결정권자",
                    "1:1 매칭 미팅 견적 가능성 30%"
                ],
                "estimate": {
                    "headline": f"리드 약 {leads}건",
                    "secondary": "잠재 거래 가치 산업 벤치마크 기반"
                },
                "caption": "ⓘ 본 수치는 산업 벤치마크 기반 추정치이며, 실제 결과는 노출 환경·콘텐츠 품질에 따라 변동됩니다."
            })
    return cases


def build_kpis(meta, audience_hints):
    """청중 KPI 4개."""
    return [
        {
            "value": meta["expected_attendees"],
            "unit": "명",
            "label": "예상 참가자",
            "source": audience_hints.get("data_source", "")
        },
        {
            "value": audience_hints.get("decision_maker_ratio", 32),
            "unit": "%",
            "label": "의사결정권자",
            "source": "자기 응답 데이터"
        },
        {
            "value": audience_hints.get("c_level_plus_executive_ratio", 23),
            "unit": "%",
            "label": "C-Level + 임원",
            "source": "직급 기반 분류"
        },
        {
            "value": audience_hints.get("b2b_ratio", 87),
            "unit": "%",
            "label": "B2B 비율",
            "source": "자기 응답"
        }
    ]


def build_deck_content(candidates_json, color_mode="dark_mixed"):
    """sponsor-candidates.json -> deck-content.json 변환."""
    meta = candidates_json["event_meta"]
    audience_hints = candidates_json.get("audience_hints", {})
    sponsor_candidates = candidates_json["sponsor_candidates"]

    top_industries = select_top_industries(sponsor_candidates, k=2)

    return {
        "meta": {
            "event_name": meta["event_name"],
            "event_subtitle": meta.get("event_subtitle"),
            "event_date": meta["event_date"],
            "event_venue": meta["event_venue"],
            "client_id": None,
            "naming_mode": "ko_first",
            "price_mode": "on_request",
            "color_mode": color_mode,
            "deck_version": "v1.0",
            "is_provisional": meta.get("is_provisional_slots", False)
        },
        "audience": {
            "kpis": build_kpis(meta, audience_hints),
            "industry_distribution": build_industry_distribution(audience_hints),
            "decision_maker_ratio": audience_hints.get("decision_maker_ratio"),
            "data_source": audience_hints.get("data_source", "")
        },
        "assets": {
            "offline": [
                {"name": "메인 무대 백드롭 로고 노출", "tier_min": "T1",
                 "quantification": "8시간 연속 노출 × 5,200명"},
                {"name": "행사장 입구 아치", "tier_min": "T1",
                 "quantification": "전 참가자 진입 동선"},
                {"name": "리셉션 카운터 로고", "tier_min": "T2",
                 "quantification": "등록 시점 100% 노출"},
                {"name": "행사장 사이니지", "tier_min": "T3",
                 "quantification": "8회 위치 노출"},
                {"name": "프로그램북 표지", "tier_min": "T2",
                 "quantification": "단독 또는 공동"}
            ],
            "digital": [
                {"name": "공식 웹사이트 메인 배너", "tier_min": "T1",
                 "quantification": "행사 전 3개월 노출"},
                {"name": "행사 앱 스플래시 로고", "tier_min": "T1",
                 "quantification": "앱 진입 시 100%"},
                {"name": "공식 SNS 단독 포스트", "tier_min": "T2",
                 "quantification": "3회 게시"},
                {"name": "이메일 뉴스레터 헤더 로고", "tier_min": "T2",
                 "quantification": "발송 4회 × 28,000명"},
                {"name": "행사 LIVE 사이드 배너", "tier_min": "T3",
                 "quantification": "스트리밍 전 시간"}
            ],
            "vip_content": [
                {"name": "VIP 만찬 단독 호스트", "tier_min": "T1",
                 "quantification": "10석 단독 테이블"},
                {"name": "키노트 발표 슬롯", "tier_min": "T1",
                 "quantification": "30분 메인 무대"},
                {"name": "B2B 매칭 미팅", "tier_min": "T2",
                 "quantification": "6미팅 × 30분"},
                {"name": "임원 라운지 출입권", "tier_min": "T2",
                 "quantification": "5명 출입 패스"}
            ]
        },
        "tiers": build_tiers(),
        "matrix": build_matrix(),
        "roi_cases": build_roi_cases(
            top_industries,
            meta.get("expected_attendees", 5200),
            audience_hints
        ),
        "section_8": {
            "type": "reference_cases",
            "data": [
                {"event_name": "[유사 행사명 1]", "year": 2023,
                 "attendees": 4200, "sponsors": 12},
                {"event_name": "[유사 행사명 2]", "year": 2024,
                 "attendees": 5800, "sponsors": 15}
            ]
        },
        "contact": {
            "headline": "지금 함께하실 수 있는 13개 슬롯이 남아있습니다",
            "next_steps": [
                "1. 견적 협의 — 본 사무국 담당자 연락",
                "2. Tier 선정 — 산업·예산 매칭 1:1 컨설팅",
                "3. 계약서 송부 — 2주 이내 신청 시 우선 배정"
            ],
            "manager_name": "[담당자 이름]",
            "manager_title": "[직급]",
            "manager_email": "[이메일]",
            "manager_phone": "[연락처]",
            "deadline": "2026-08-15"
        },
        "_sponsor_candidates_carried_over": [
            {
                "name": c["name"],
                "industry": c["industry"],
                "tier_target": c["tier_target"],
                "priority": c["priority"]
            }
            for c in sponsor_candidates
        ]
    }


# ============================================================
# 4. 자가 검증 - 회사 종속 표현·필수 필드·트리거 충돌
# ============================================================
FORBIDDEN_TERMS = [
    "엠앤씨",
    "M&C커뮤니케이션즈",
    "리멤버앤컴퍼니"
]


def scan_forbidden_terms(obj, path="$"):
    """JSON 객체 전체를 재귀 스캔하여 회사 종속 표현 검출."""
    findings = []
    if isinstance(obj, str):
        for term in FORBIDDEN_TERMS:
            if term in obj:
                findings.append({"path": path, "term": term, "value": obj})
    elif isinstance(obj, dict):
        for k, v in obj.items():
            findings.extend(scan_forbidden_terms(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            findings.extend(scan_forbidden_terms(v, f"{path}[{i}]"))
    return findings


def validate_required_fields(deck_content):
    """필수 필드 검증."""
    errors = []
    required = [
        ("meta.event_name", deck_content["meta"]["event_name"]),
        ("meta.event_date", deck_content["meta"]["event_date"]),
        ("meta.event_venue", deck_content["meta"]["event_venue"]),
        ("audience.kpis", deck_content["audience"]["kpis"]),
        ("tiers", deck_content["tiers"]),
        ("matrix.rows", deck_content["matrix"]["rows"]),
        ("roi_cases", deck_content["roi_cases"]),
        ("contact.headline", deck_content["contact"]["headline"])
    ]
    for name, value in required:
        if value is None or (isinstance(value, (list, str)) and len(value) == 0):
            errors.append(f"Missing or empty required field: {name}")

    # roi_cases 최소 2개
    if len(deck_content["roi_cases"]) < 2:
        errors.append(
            f"roi_cases must have at least 2 industries, "
            f"got {len(deck_content['roi_cases'])}"
        )

    # 3단 구조 검증
    for i, case in enumerate(deck_content["roi_cases"]):
        for stage in ("premise", "formula", "estimate"):
            if stage not in case or not case[stage]:
                errors.append(
                    f"roi_cases[{i}] missing required stage: {stage}"
                )
        if "caption" not in case or "추정치" not in case["caption"]:
            errors.append(
                f"roi_cases[{i}] missing required caption with '추정치'"
            )

    # industry distribution 합계 100%
    dist = deck_content["audience"]["industry_distribution"]
    total_ratio = sum(d["ratio"] for d in dist)
    if abs(total_ratio - 100) > 1:
        errors.append(
            f"industry_distribution sum must be 100%, got {total_ratio}%"
        )

    return errors


def validate_tier_colors(deck_content):
    """Tier 색상이 design-tokens-mapping.md 룰과 일치하는지 검증."""
    expected_tokens = TIER_COLOR_TOKENS
    expected_hex = TIER_COLORS_HEX
    errors = []
    for tier in deck_content["tiers"]:
        tid = tier["id"]
        if tier.get("color_token") != expected_tokens.get(tid):
            errors.append(
                f"Tier {tid} color_token mismatch: "
                f"got {tier.get('color_token')}, "
                f"expected {expected_tokens.get(tid)}"
            )
        if tier.get("color_hex") != expected_hex.get(tid):
            errors.append(
                f"Tier {tid} color_hex mismatch: "
                f"got {tier.get('color_hex')}, "
                f"expected {expected_hex.get(tid)}"
            )
    return errors


def run_self_validation(candidates_json, deck_content):
    """전체 자가 검증."""
    return {
        "forbidden_terms_in_candidates": scan_forbidden_terms(candidates_json),
        "forbidden_terms_in_deck_content": scan_forbidden_terms(deck_content),
        "required_field_errors": validate_required_fields(deck_content),
        "tier_color_errors": validate_tier_colors(deck_content),
        "validation_passed": True  # 채워질 예정
    }


# ============================================================
# 5. main
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="mice-sponsor-deck v2.0 sample scenario generator"
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default="C:/Users/icejc/mice-skills-work/sprint-03-mice-sponsor-deck/_samples",
        help="Output directory for generated JSON files"
    )
    parser.add_argument(
        "--color-mode",
        type=str,
        choices=["light", "dark_mixed"],
        default="dark_mixed",
        help="Color mode for the deck (light or dark_mixed)"
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("mice-sponsor-deck v2.0 - Sample Scenario Generator")
    print("=" * 70)
    print(f"Scenario: TOBESOFT TECH FORUM 2026")
    print(f"Output: {out_dir.absolute()}")
    print(f"Color mode: {args.color_mode}")
    print()

    # Step 1: mice-meeting-minutes 체이닝 시뮬레이션
    print("[Step 1] mice-meeting-minutes → sponsor-candidates.json")
    candidates = build_sponsor_candidates_json()
    candidates_path = out_dir / "sponsor-candidates.json"
    with open(candidates_path, "w", encoding="utf-8") as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
    print(f"  - {candidates_path.name}: {len(candidates['sponsor_candidates'])} candidates")
    print(f"    - high priority: {sum(1 for c in candidates['sponsor_candidates'] if c['priority'] == 'high')}")
    print(f"    - med priority: {sum(1 for c in candidates['sponsor_candidates'] if c['priority'] == 'med')}")
    print(f"    - low priority: {sum(1 for c in candidates['sponsor_candidates'] if c['priority'] == 'low')}")
    print()

    # Step 2: deck-content.json 변환
    print("[Step 2] sponsor-candidates.json → deck-content.json")
    deck_content = build_deck_content(candidates, color_mode=args.color_mode)
    deck_path = out_dir / "deck-content.json"
    with open(deck_path, "w", encoding="utf-8") as f:
        json.dump(deck_content, f, ensure_ascii=False, indent=2)
    print(f"  - {deck_path.name}: deck content single source ready")
    print(f"    - tiers: {len(deck_content['tiers'])}")
    print(f"    - matrix rows: {len(deck_content['matrix']['rows'])}")
    print(f"    - roi_cases: {len(deck_content['roi_cases'])} industries")
    print(f"    - color_mode: {deck_content['meta']['color_mode']}")
    print()

    # Step 3: 자가 검증
    print("[Step 3] Self-validation")
    validation = run_self_validation(candidates, deck_content)

    has_errors = (
        len(validation["forbidden_terms_in_candidates"]) > 0
        or len(validation["forbidden_terms_in_deck_content"]) > 0
        or len(validation["required_field_errors"]) > 0
        or len(validation["tier_color_errors"]) > 0
    )
    validation["validation_passed"] = not has_errors

    validation_path = out_dir / "validation-summary.json"
    with open(validation_path, "w", encoding="utf-8") as f:
        json.dump(validation, f, ensure_ascii=False, indent=2)

    if validation["validation_passed"]:
        print(f"  - PASS: No forbidden terms, all required fields present")
        print(f"  - PASS: Tier colors match design-tokens-mapping.md")
    else:
        print("  - FAIL items:")
        if validation["forbidden_terms_in_candidates"]:
            print(f"    - Forbidden terms in candidates: "
                  f"{len(validation['forbidden_terms_in_candidates'])}")
        if validation["forbidden_terms_in_deck_content"]:
            print(f"    - Forbidden terms in deck content: "
                  f"{len(validation['forbidden_terms_in_deck_content'])}")
        if validation["required_field_errors"]:
            print(f"    - Required field errors: "
                  f"{len(validation['required_field_errors'])}")
            for err in validation["required_field_errors"]:
                print(f"        · {err}")
        if validation["tier_color_errors"]:
            print(f"    - Tier color errors: "
                  f"{len(validation['tier_color_errors'])}")

    print(f"  - {validation_path.name} written")
    print()

    # Summary
    print("=" * 70)
    print(f"Generated files in {out_dir.absolute()}:")
    print(f"  1. sponsor-candidates.json  (mice-meeting-minutes chaining input)")
    print(f"  2. deck-content.json        (HTML/PPTX single source)")
    print(f"  3. validation-summary.json  (self-validation report)")
    print()
    print(f"Status: {'PASS' if validation['validation_passed'] else 'FAIL'}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 70)

    return 0 if validation["validation_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
