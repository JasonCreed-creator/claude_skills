#!/usr/bin/env python3
"""
calc_estimate_remember.py — 리멤버 견적 자동 산출 엔진 (방식 A, 리멤버 양식)

단일 출처: 컨피규레이터 src/lib/calcEstimate.js (커밋: 데이터셋 source.commit 참조)
단가·산식·검증 벡터는 assets/remember_pricing_dataset_v1.json 에서 로드한다 (하드코딩 금지).

이식 합격 기준: golden_vectors 전 케이스 + adjustment_vector 0원 일치.
자가검증: `python calc_estimate_remember.py`

산식 미묘점 (README_코웍이식 §반드시 지킬 산식 미묘점):
- PCO: floor(opCost×0.25/10000)×10000 (만원 미만 절사, 반올림 아님)
- opCost = s1+s2+s3+s4+ot+rsvpPkg+genManage — showup·leadPkg 조정 델타 미포함
- audio/misc ceil 기준점 (target−50)/100, ops/insurance는 (target−100)/100
- 등록시스템 target>200 부터 키오스크(100명당 1대·대당 100만)
- 스케일러: 100명 이상 & displayType≠projector → 시스템(s2), 100명 미만 → 옵션(ot)만
- 화면중계: displayType==='led' 일 때만 과금
- 모객 제외(excludeLeads) = guarantee 0 치환. genManage는 유지
"""
import json, math, os

_DIR = os.path.dirname(os.path.abspath(__file__))
_DATASET_CANDIDATES = [
    os.path.join(_DIR, '..', 'assets', 'remember_pricing_dataset_v1.json'),
    os.path.join(_DIR, 'remember_pricing_dataset_v1.json'),
]

def load_dataset(path=None):
    paths = [path] if path else _DATASET_CANDIDATES
    for p in paths:
        if p and os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                return json.load(f)
    raise FileNotFoundError('remember_pricing_dataset_v1.json 을 찾을 수 없습니다: ' + str(paths))

_DS = load_dataset()
C = _DS['constants']

def _num_or(value, default):
    """오버라이드 가드: 유한수 & 0 이상만 인정, 그 외 기본값 폴백."""
    try:
        v = float(value)
        if math.isfinite(v) and v >= 0:
            return v
    except (TypeError, ValueError):
        pass
    return default

def kpi_label(g):
    """KPI 인정선 라벨 (금액 무관·표기용). kpi_rules 복제."""
    g = int(g or 0)
    if g <= 0:
        return None
    ratio, tier = (0.0, 1) if g <= 50 else (0.15, 2) if g <= 100 else (0.20, 3)
    min_ack = max(40, math.ceil(g * (1 - ratio)))
    pct = int(round((1 - ratio) * 100))
    under_floor = g < 40
    return {'min_ack': min_ack, 'ratio': ratio, 'tier': tier,
            'text': f'KPI 달성선 {min_ack}명 ({pct}% 인정·{tier}단계)',
            'under_floor_ui': under_floor}

def calc_estimate_remember(cfg):
    """cfg 키: target(필수), guarantee, mode('full'|'excludeLeads'), venueRental,
    displayType('led'|'projector'), options(dict), genAttendees,
    boothCount/boothUnitPrice, boothPremiumCount/boothPremiumUnitPrice,
    souvenirPrice/souvenirQty, adjust({s1,s2,s3,s4,ot,leadPkg} 델타)"""
    t = int(cfg['target'])
    mode = cfg.get('mode', 'full')
    g_in = int(cfg.get('guarantee') or 0)
    g = 0 if mode == 'excludeLeads' else g_in
    opts = cfg.get('options') or {}
    display = cfg.get('displayType', 'led')
    gen = int(round(_num_or(cfg.get('genAttendees'), 0)))
    gen = max(0, gen)
    adj = cfg.get('adjust') or {}

    zero_sys = {k: 0 for k in ('video','scaler4k','audio','engineer','presentation','registration','misc')}
    zero_des = {k: 0 for k in ('env','web','kv')}
    zero_ops = {k: 0 for k in ('desk','ops','insurance')}

    # isCustom: 자동견적 불가 → 전 항목 0
    if t > _DS['bounds']['target_max']:
        return {'isCustom': True, 't': t, 'g': g, 'u': t,
                's1': 0, 's2': 0, 's3': 0, 's4': 0, 's5': 0, 'ot': 0,
                'rsvpOrig': 0, 'rsvpPkg': 0, 'leadOrig': 0, 'leadPkg': 0,
                'showup': 0, 'genManage': 0, 'genCount': 0, 'opCost': 0, 'pk': 0,
                'pkVat': 0, 'pk_excluding_options': 0,
                'sysBreakdown': zero_sys, 'desBreakdown': zero_des, 'opsBreakdown': zero_ops,
                'otBreakdown': {}, 'kpi': None}

    # ---- s1 베뉴 (택1 — 후보 합산 금지)
    s1 = int(_num_or(cfg.get('venueRental'), t * C['VENUE_PER_PAX_5STAR'])) \
         if cfg.get('venueRental') is not None else t * C['VENUE_PER_PAX_5STAR']

    # ---- s2 시스템
    sys_b = {
        'video': 2000000,
        'scaler4k': 2500000 if (t >= 100 and display != 'projector') else 0,
        'audio': 1500000 + math.ceil(max(0, t - 50) / 100) * 500000,
        'engineer': 1000000,
        'presentation': 1200000,
        'registration': (1000000 + (t // 100) * 1000000) if t > 200
                        else (1000000 + max(0, t - 100) * 5000),
        'misc': 500000 + math.ceil(max(0, t - 50) / 100) * 500000,
    }
    s2 = sum(sys_b.values())

    # ---- s3 디자인
    env = 2000000 if t <= 50 else 2500000 if t <= 100 else 3000000 if t <= 150 else 3500000
    des_b = {'env': env, 'web': 1000000, 'kv': 1000000}
    s3 = sum(des_b.values())

    # ---- s4 운영
    ops_b = {
        'desk': math.ceil(t / 50) * 250000,
        'ops': 900000 + math.ceil(max(0, t - 100) / 100) * 300000,
        'insurance': 400000 + math.ceil(max(0, t - 100) / 100) * 100000,
    }
    s4 = sum(ops_b.values())

    # ---- 옵션 (ot)
    ot_b = {}
    u = t  # u = 인원 에코 (기념품 수량과 무관 — golden 준거)
    souvenir_qty = t
    if opts.get('souvenir'):
        unit = int(_num_or(cfg.get('souvenirPrice'), C['SOUVENIR_UNIT_PRICE']))
        souvenir_qty = int(_num_or(cfg.get('souvenirQty'), t))
        ot_b['souvenir'] = souvenir_qty * unit
    if opts.get('emcee'):
        ot_b['emcee'] = 1500000
    # 미디어 택1 (photo/video/aving)
    if opts.get('aving'):
        ot_b['aving'] = 2500000
    elif opts.get('photo'):
        ot_b['photo'] = 800000
    elif opts.get('video_sketch') or opts.get('video'):
        ot_b['video_sketch'] = 2000000
    if opts.get('scaler4k') and t < 100:  # 100명 이상은 s2 포함 — 중복 과금 금지
        ot_b['scaler4k'] = 2500000
    if opts.get('screenRelay') and display == 'led':  # LED 게이트
        ot_b['screenRelay'] = 2500000
    if opts.get('fullRecording'):
        ot_b['fullRecording'] = 3500000
    if opts.get('survey'):
        ot_b['survey'] = 1000000
    # 포토월 택1
    if opts.get('photowall_premium'):
        ot_b['photowall_premium'] = 2000000
    elif opts.get('photowall_basic') or opts.get('photowall'):
        ot_b['photowall_basic'] = 500000
    if opts.get('rsvpHandling'):  # 순수 응대 대행 (모객 제외 모드 전용 UI)
        ot_b['rsvpHandling'] = t * C['GEN_ATTENDEE_UNIT_PRICE']
    bc = int(_num_or(cfg.get('boothCount'), 0))
    if bc > 0:
        ot_b['booth_standard'] = bc * int(_num_or(cfg.get('boothUnitPrice'), C['BOOTH_UNIT_PRICE']))
    bpc = int(_num_or(cfg.get('boothPremiumCount'), 0))
    if bpc > 0:
        ot_b['booth_premium'] = bpc * int(_num_or(cfg.get('boothPremiumUnitPrice'), C['BOOTH_PREMIUM_UNIT_PRICE']))
    ot = sum(ot_b.values())

    # ---- 모객 / 참관객
    rsvpOrig = g * C['RSVP_LIST_PRICE']
    rsvpPkg  = g * C['RSVP_PKG_PRICE']
    showup   = g * C['SHOWUP_PKG_PRICE']
    leadOrig = g * C['LEAD_LIST_PER_PAX']
    leadPkg  = rsvpPkg + showup
    genManage = gen * C['GEN_ATTENDEE_UNIT_PRICE']

    # ---- 조정 델타 (소계 가산 → opCost·s5·pk 재계산; leadPkg 델타는 opCost 미포함)
    s1 += int(adj.get('s1', 0)); s2 += int(adj.get('s2', 0))
    s3 += int(adj.get('s3', 0)); s4 += int(adj.get('s4', 0))
    ot += int(adj.get('ot', 0)); leadPkg += int(adj.get('leadPkg', 0))

    # ---- PCO (만원 미만 절사) / 총액
    opCost = s1 + s2 + s3 + s4 + ot + rsvpPkg + genManage  # showup 미포함
    s5 = (opCost * 25 // 100) // 10000 * 10000
    pk = s1 + s2 + s3 + s4 + s5 + ot + leadPkg + genManage

    # 옵션 제외 파생 (PCO 재계산, genManage 유지)
    s5_noopt = ((opCost - ot) * 25 // 100) // 10000 * 10000
    pk_noopt = pk - ot - (s5 - s5_noopt)

    out = {'isCustom': False, 't': t, 'g': g, 'u': u,
           's1': s1, 's2': s2, 's3': s3, 's4': s4, 's5': s5, 'ot': ot,
           'rsvpOrig': rsvpOrig, 'rsvpPkg': rsvpPkg, 'leadOrig': leadOrig,
           'leadPkg': leadPkg, 'showup': showup,
           'genManage': genManage, 'genCount': gen, 'opCost': opCost, 'pk': pk,
           'pkVat': round(pk * 1.1), 'pk_excluding_options': pk_noopt,
           'sysBreakdown': sys_b, 'desBreakdown': des_b, 'opsBreakdown': ops_b,
           'otBreakdown': ot_b, 'souvenirQty': souvenir_qty, 'kpi': kpi_label(g)}
    if adj:
        out['adjusted'] = True
    return out

# ---------------- 자가검증 ----------------
def _selftest():
    ds = _DS
    fails = []
    def check(name, exp, got):
        for k, v in exp.items():
            gv = got.get(k)
            if isinstance(v, dict):
                for kk, vv in v.items():
                    if got.get(k, {}).get(kk) != vv:
                        fails.append(f"{name}.{k}.{kk}: 기대 {vv} / 산출 {got.get(k,{}).get(kk)}")
            elif gv != v:
                fails.append(f"{name}.{k}: 기대 {v} / 산출 {gv}")
    n = 0
    for v in ds['golden_vectors']:
        cfg = dict(v['input']); cfg['mode'] = v.get('mode', 'full')
        r = calc_estimate_remember(cfg)
        check(v['id'], v['expected'], r)
        if 'expected_pk_excluding_options' in v and not r['isCustom']:
            if r['pk_excluding_options'] != v['expected_pk_excluding_options']:
                fails.append(f"{v['id']}.pk_excluding_options: 기대 {v['expected_pk_excluding_options']} / 산출 {r['pk_excluding_options']}")
        n += 1
    av = ds['adjustment_vector']
    cfg = dict(av['base_input']); cfg['adjust'] = av['adjust']
    check('adjustment', av['expected'], calc_estimate_remember(cfg))
    n += 1
    # headcount_grid 전행 대조 (무옵션·모객제외·베뉴자동)
    gerr = 0
    for row in ds['headcount_grid']:
        r = calc_estimate_remember({'target': row['target'], 'guarantee': 0, 'mode': 'excludeLeads'})
        for key, exp in (('s2', row['s2']), ('s3', row['s3']), ('s4', row['s4']), ('s5', row['s5']), ('pk', row['pk'])):
            if r[key] != exp:
                gerr += 1; fails.append(f"grid[{row['target']}].{key}: 기대 {exp} / 산출 {r[key]}")
        if r['sysBreakdown'] != row['sys'] or r['desBreakdown'] != row['des'] or r['opsBreakdown'] != row['ops']:
            gerr += 1; fails.append(f"grid[{row['target']}] breakdown 불일치")
    if fails:
        print(f"FAIL ({len(fails)}건)")
        for f in fails[:30]:
            print(" -", f)
        return 1
    print(f"ALL PASS — golden {len(ds['golden_vectors'])} + adjustment 1 + grid {len(ds['headcount_grid'])}행 = 0원 일치")
    return 0

if __name__ == '__main__':
    raise SystemExit(_selftest())
