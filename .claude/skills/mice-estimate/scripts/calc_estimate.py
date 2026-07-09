"""견적 자동 산출 엔진 — calcEstimate.js의 Python 포팅.

원본: src/lib/calcEstimate.js (MiceConfigurator SaaS)
SSOT: 견적Configurator_로직명세서_v1_0.md §5
검증: §9 100명 표준견적 = 83,750,000원 (VAT별도) / 92,125,000원 (VAT포함)

사용:
    from calc_estimate import calc_estimate, OPTS, apply_option_constraints

    result = calc_estimate({
        'target': 100,
        'guarantee': 100,
        'options': {'video': True, 'emcee': True},
    })
    print(result['pk'], result['pkVat'])

CLI 자가검증:
    python calc_estimate.py
    → SSOT §9 시뮬레이션 일치 여부 출력 (exit 0=통과, 1=실패)
"""

import math
from typing import Optional


# ============================================================
# SSOT §5.4 하드코딩 14상수 (Phase 1 DB 마이그레이션 대상)
# ============================================================

TARGET_MIN = 40
TARGET_MAX = 500
GUARANTEE_MIN = 40
BOOTH_UNIT_PRICE = 1_000_000

VENUE_PER_PAX_5STAR = 180_000

# s2 시스템 구축 고정가
SYS_VIDEO_PRICE = 2_000_000           # ⚠️ 옵션 'video'(동영상 촬영)와 별개. 5성급 기본 영상콘솔
SYS_SCALER4K_PRICE = 2_500_000        # target ≥ 100 시 s2 자동 포함
SYS_ENGINEER_PRICE = 1_000_000
SYS_PRESENTATION_PRICE = 1_200_000

# s3 디자인 고정가
DES_WEB_PRICE = 1_000_000
DES_KV_PRICE = 1_000_000

# 모객 솔루션 단가 (per guarantee)
RSVP_ORIG_PRICE = 50_000
RSVP_PKG_PRICE = 40_000
SHOWUP_ORIG_PRICE = 450_000
SHOWUP_PKG_PRICE = 350_000

# s5 PCO 기획료
PCO_FEE_RATE = 0.25
PCO_FEE_TRUNCATE_UNIT = 10_000        # 만원 미만 절사


# ============================================================
# SSOT §4 옵션 카탈로그 (9종) + 상호배제 그룹
# ============================================================

OPTS = {
    'souvenir':          {'label': '기념품',              'price_per_pax': 50_000, 'group': None},
    'emcee':             {'label': '사회자',              'price': 1_500_000,      'group': None},
    'photo':             {'label': '사진촬영',            'price': 800_000,        'group': 'media'},
    'video':             {'label': '동영상 촬영',         'price': 2_000_000,      'group': 'media'},
    'aving':             {'label': 'AVING 미디어 패키지', 'price': 2_500_000,      'group': 'media'},
    'scaler4k':          {'label': '4K 스케일러/KVM',     'price': 2_500_000,      'group': None},
    'survey':            {'label': '사후설문조사',        'price': 1_000_000,      'group': None},
    'photowall_basic':   {'label': '포토월 (일반형)',     'price': 500_000,        'group': 'photowall'},
    'photowall_premium': {'label': '포토월 (고급형)',     'price': 2_000_000,      'group': 'photowall'},
}

EXCLUSION_GROUPS = ['media', 'photowall']


def apply_option_constraints(options: Optional[dict], target: int) -> dict:
    """SSOT §4 옵션 상호배제 규칙 적용.

    - media 그룹 (photo·video·aving): 최대 1개. 여러 개 True면 첫 멤버만 유지.
    - photowall 그룹 (basic·premium): 최대 1개.
    - scaler4k 자동: target ≥ 100 시 s2에 자동 포함되므로 옵션에서 False 강제 (중복청구 방지).
    """
    result = {k: False for k in OPTS}
    if options:
        result.update({k: bool(v) for k, v in options.items() if k in OPTS})

    for group in EXCLUSION_GROUPS:
        members = [k for k, v in OPTS.items() if v['group'] == group]
        active = [k for k in members if result.get(k, False)]
        if len(active) > 1:
            keep = active[0]
            for k in active[1:]:
                result[k] = False

    if target >= 100:
        result['scaler4k'] = False

    return result


# ============================================================
# 섹션별 계산 함수 (SSOT §5.3)
# ============================================================

def _calc_s1_venue(c: dict) -> int:
    """Section 1: 베뉴 사용료. venueRental 직접입력 우선, 없으면 target × 180,000."""
    rental = c.get('venueRental')
    if rental is not None:
        return int(rental)
    return c['target'] * VENUE_PER_PAX_5STAR


def _calc_s2_system(c: dict) -> tuple:
    """Section 2: 시스템 구축. returns (total, breakdown_dict)."""
    t = c['target']

    video = SYS_VIDEO_PRICE
    scaler4k = SYS_SCALER4K_PRICE if t >= 100 else 0
    audio = 1_500_000 + math.ceil(max(0, t - 50) / 100) * 500_000
    engineer = SYS_ENGINEER_PRICE
    presentation = SYS_PRESENTATION_PRICE

    if t > 200:
        registration = 1_000_000 + (t // 100) * 1_000_000
    else:
        registration = 1_000_000 + max(0, t - 100) * 5_000

    misc = 500_000 + math.ceil(max(0, t - 50) / 100) * 500_000

    breakdown = {
        'video': video, 'scaler4k': scaler4k, 'audio': audio,
        'engineer': engineer, 'presentation': presentation,
        'registration': registration, 'misc': misc,
    }
    return sum(breakdown.values()), breakdown


def _calc_s3_design(c: dict) -> tuple:
    """Section 3: 디자인·브랜딩. returns (total, breakdown_dict)."""
    t = c['target']

    if t <= 50:
        env = 2_000_000
    elif t <= 100:
        env = 2_500_000
    elif t <= 150:
        env = 3_000_000
    else:
        env = 3_500_000

    breakdown = {'env': env, 'web': DES_WEB_PRICE, 'kv': DES_KV_PRICE}
    return sum(breakdown.values()), breakdown


def _calc_s4_operations(c: dict) -> tuple:
    """Section 4: 운영·보험. returns (total, breakdown_dict)."""
    t = c['target']

    desk = math.ceil(t / 50) * 250_000
    ops = 900_000 + math.ceil(max(0, t - 100) / 100) * 300_000
    insurance = 400_000 + math.ceil(max(0, t - 100) / 100) * 100_000

    breakdown = {'desk': desk, 'ops': ops, 'insurance': insurance}
    return sum(breakdown.values()), breakdown


def _calc_options(c: dict, options_applied: dict) -> tuple:
    """추가옵션 (ot) = Σ(활성 옵션) + boothCount × 1,000,000. returns (total, breakdown)."""
    t = c['target']
    booth_count = int(c.get('boothCount', 0) or 0)

    breakdown = {}
    for opt_id, active in options_applied.items():
        if not active:
            continue
        spec = OPTS[opt_id]
        if 'price_per_pax' in spec:
            breakdown[opt_id] = t * spec['price_per_pax']
        else:
            breakdown[opt_id] = spec['price']

    if booth_count > 0:
        breakdown['booth'] = booth_count * BOOTH_UNIT_PRICE

    return sum(breakdown.values()), breakdown


def _calc_rsvp_showup(c: dict) -> tuple:
    """모객 솔루션. returns (rsvpOrig, rsvpPkg, showupOrig, showup)."""
    g = c.get('guarantee') if c.get('guarantee') is not None else c['target']
    return (
        g * RSVP_ORIG_PRICE,
        g * RSVP_PKG_PRICE,
        g * SHOWUP_ORIG_PRICE,
        g * SHOWUP_PKG_PRICE,
    )


def _calc_s5_pco(op_cost: int) -> int:
    """Section 5: PCO 기획료 = ⌊opCost × 25% / 10,000⌋ × 10,000 (만원 미만 절사)."""
    return math.floor((op_cost * PCO_FEE_RATE) / PCO_FEE_TRUNCATE_UNIT) * PCO_FEE_TRUNCATE_UNIT


# ============================================================
# 메인 진입점 — calcEstimate.js와 동일 시그니처
# ============================================================

def calc_estimate(c: dict) -> dict:
    """SSOT §5.1 calcEstimate(c) 의 Python 포팅.

    Args:
        c: {
            'target': int,              # 필수. 40~500. 500 초과 시 isCustom=True.
            'guarantee': int = None,    # None이면 target과 동일.
            'venueRental': int = None,  # None이면 target × 180,000 (5성급 자동).
            'venueName': str = None,
            'options': dict = None,     # {'video': True, ...}. 그룹 상호배제 자동 적용.
            'boothCount': int = 0,
        }

    Returns: dict with keys
        isCustom, t, g,
        s1, s2, s3, s4, s5, ot,
        rsvpOrig, rsvpPkg, showupOrig, showup, leadOrig, leadPkg,
        opCost, pk, pkVat,
        sysBreakdown, desBreakdown, opsBreakdown, otBreakdown,
        optionsApplied.
    """
    if c.get('target') is None:
        raise ValueError("견적 계산 실패: 'target'(목표 인원) 값이 없습니다. target을 지정해주세요.")

    target = int(c['target'])
    c = {**c, 'target': target}

    if target > TARGET_MAX:
        return {
            'isCustom': True,
            't': target,
            'g': c.get('guarantee') if c.get('guarantee') is not None else target,
            's1': 0, 's2': 0, 's3': 0, 's4': 0, 's5': 0, 'ot': 0,
            'rsvpOrig': 0, 'rsvpPkg': 0, 'showupOrig': 0, 'showup': 0,
            'leadOrig': 0, 'leadPkg': 0,
            'opCost': 0, 'pk': 0, 'pkVat': 0,
            'sysBreakdown': {}, 'desBreakdown': {}, 'opsBreakdown': {}, 'otBreakdown': {},
            'optionsApplied': {k: False for k in OPTS},
        }

    options_applied = apply_option_constraints(c.get('options'), target)

    s1 = _calc_s1_venue(c)
    s2, sys_breakdown = _calc_s2_system(c)
    s3, des_breakdown = _calc_s3_design(c)
    s4, ops_breakdown = _calc_s4_operations(c)
    ot, ot_breakdown = _calc_options(c, options_applied)

    rsvp_orig, rsvp_pkg, showup_orig, showup = _calc_rsvp_showup(c)

    op_cost = s1 + s2 + s3 + s4 + ot + rsvp_pkg
    s5 = _calc_s5_pco(op_cost)

    pk = s1 + s2 + s3 + s4 + s5 + ot + rsvp_pkg + showup
    pk_vat = round(pk * 1.1)

    return {
        'isCustom': False,
        't': target,
        'g': c.get('guarantee') if c.get('guarantee') is not None else target,
        's1': s1, 's2': s2, 's3': s3, 's4': s4, 's5': s5,
        'ot': ot,
        'rsvpOrig': rsvp_orig, 'rsvpPkg': rsvp_pkg,
        'showupOrig': showup_orig, 'showup': showup,
        'leadOrig': rsvp_orig + showup_orig,
        'leadPkg': rsvp_pkg + showup,
        'opCost': op_cost,
        'pk': pk, 'pkVat': pk_vat,
        'sysBreakdown': sys_breakdown,
        'desBreakdown': des_breakdown,
        'opsBreakdown': ops_breakdown,
        'otBreakdown': ot_breakdown,
        'optionsApplied': options_applied,
    }


# ============================================================
# CLI 자가검증 (SSOT §9)
# ============================================================

def _self_test() -> int:
    """SSOT §9 시뮬레이션 예시(100명 표준 = 83,750,000원)와 일치 검증."""
    print("=" * 64)
    print("SSOT §9 검증: 100명 표준견적 (5성급, 옵션 없음)")
    print("=" * 64)

    result = calc_estimate({
        'target': 100,
        'guarantee': 100,
        'venueRental': None,
        'venueName': '조선팰리스 강남',
        'options': {},
        'boothCount': 0,
    })

    expected = {
        's1':      18_000_000,
        's2':      10_700_000,
        's3':       4_500_000,
        's4':       1_800_000,
        'ot':               0,
        'rsvpPkg':  4_000_000,
        'opCost':  39_000_000,
        's5':       9_750_000,
        'showup':  35_000_000,
        'pk':      83_750_000,
        'pkVat':   92_125_000,
    }

    all_pass = True
    for k, expected_v in expected.items():
        actual_v = result[k]
        status = 'PASS' if actual_v == expected_v else 'FAIL'
        marker = '[O]' if actual_v == expected_v else '[X]'
        print(f"  {marker} {k:10s}  expected={expected_v:>15,}  actual={actual_v:>15,}  {status}")
        if actual_v != expected_v:
            all_pass = False

    print()
    print(f"  sysBreakdown: {result['sysBreakdown']}")
    print(f"  desBreakdown: {result['desBreakdown']}")
    print(f"  opsBreakdown: {result['opsBreakdown']}")
    print(f"  optionsApplied: { {k: v for k, v in result['optionsApplied'].items() if v} or '(all False)' }")
    print()

    if all_pass:
        print("RESULT: SSOT §9 검증 통과 (PASS)")
        return 0
    else:
        print("RESULT: SSOT §9 검증 실패 (FAIL)")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(_self_test())
