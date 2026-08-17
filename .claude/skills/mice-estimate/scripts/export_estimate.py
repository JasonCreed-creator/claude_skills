"""산출내역서(공공·국가계약법형) 자동 본문 작성기.

구 "M&C 견적서 작성기". 리멤버 전환(D1)으로 양식 명칭을 일반화 리네임했으나,
함수명 `export_mnc_estimate`·파일 `mnc_template.xlsx`·format 값 `mnc`는 하위호환을
위해 그대로 유지한다 — `mnc`는 산출내역서(공공형) 양식을 가리키는 레거시 코드 키다.

calc_estimate 결과 + 산출내역서(공공형) 템플릿 → 세부산출내역 7개 섹션 자동 작성된 xlsx.

방식 A (자동 산출) 전용 진입점:
    export_mnc_estimate(template_path, output_path, result, meta)

처리 흐름:
1. 템플릿 복사
2. Row 21 이하 기존 데이터 영역 안전 정리 (병합 해제 + 값 클리어)
3. 7개 섹션 순차 작성 (Row 21부터):
   1) 베뉴 사용료
   2) 시스템 구축
   3) 디자인·브랜딩
   4) 운영·보험
   5) 추가옵션
   6) 모객 솔루션
   7) PCO 기획료
4. 합계영역 (Row 12~17) 수식 갱신
5. 헤더 영역 (Row 3~8) 외부 주입 변수 채움
6. B8 한글 금액 + K9 RFP 금액 채움
7. 무결성 검증 (재오픈 + pkVat 일치)

SSOT: 견적Configurator_로직명세서_v1_0.md §5.3, §8
"""

import shutil
from pathlib import Path
from typing import Optional

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter

from calc_estimate import OPTS
from korean_amount import format_estimate_amount


# ============================================================
# 스타일 정의 (jc-design-system SoT 정본 매핑 — references/jc-design-mapping.md)
# 값의 정본: jc-design-system signature-tokens.md §6 JSON 정본 (라이트).
# xlsx는 CSS 변수 불가 → hex 리터럴 매체 불가피. 각 값은 SoT 라이트 정본과
# 일치시키고 'SoT 미러' 주석으로 추적성 유지. openpyxl은 '#' 없는 RRGGBB 사용.
# ============================================================

# jc-design-system(SoT) 런타임 로딩: 실행 시 §6 JSON 에서 값을 읽고, 실패하면 미러 폴백.
def _load_jc_tokens():
    import json, re
    from pathlib import Path
    try:
        sot = Path(__file__).resolve().parents[2] / "jc-design-system" / "references" / "signature-tokens.md"
        m = re.search(r"```json\s*\n(.*?)\n```", sot.read_text(encoding="utf-8"), re.S)
        return json.loads(m.group(1)) if m else {}
    except Exception:
        return {}

_JC = _load_jc_tokens()
def _jc(key, fallback):
    c = _JC.get("color", {})
    v = c.get(key) or c.get("point", {}).get(key) or c.get("semantic", {}).get(key) or fallback
    return v.lstrip("#")

COLOR_BRAND_PRIMARY  = _jc("primary", "0A2540")       # --jc-primary (Deep Navy, 헤더/타이틀)
COLOR_BRAND_ACCENT   = _jc("accent", "2962FF")        # --jc-accent (Electric Blue, 카테고리 강조)
COLOR_NEUTRAL_LIGHT  = _jc("borderStrong", "C9CFD8")  # --jc-border-strong (소계 배경)
COLOR_SEMANTIC_DANGER= _jc("danger", "D32F2F")        # --jc-danger (소계 금액 강조)
COLOR_NEUTRAL_WHITE  = _jc("surface", "FFFFFF")       # --jc-surface (흰색)

FONT_BODY = Font(name='Pretendard', size=12)
FONT_BODY_BOLD = Font(name='Pretendard', size=12, bold=True)
FONT_WHITE_BOLD = Font(name='Pretendard', size=12, bold=True, color=COLOR_NEUTRAL_WHITE)
FONT_SUBTOTAL = Font(name='Pretendard', size=12, bold=True, color=COLOR_SEMANTIC_DANGER)

FILL_CATEGORY = PatternFill('solid', fgColor=COLOR_BRAND_ACCENT)
FILL_SUBTOTAL = PatternFill('solid', fgColor=COLOR_NEUTRAL_LIGHT)

side_thin = Side(style='thin')
side_hair = Side(style='hair')

BORDER_HAIR = Border(left=side_hair, right=side_hair, top=side_hair, bottom=side_hair)
BORDER_ITEM_A = Border(left=side_thin, right=side_hair, top=side_hair, bottom=side_hair)
BORDER_ITEM_K = Border(left=side_hair, right=side_thin, top=side_hair, bottom=side_hair)
BORDER_SUBTOTAL = Border(left=side_hair, right=side_hair, top=side_hair, bottom=side_thin)

ALIGN_CENTER = Alignment(horizontal='center', vertical='center')
ALIGN_RIGHT  = Alignment(horizontal='right',  vertical='center')
ALIGN_LEFT   = Alignment(horizontal='left',   vertical='center', wrap_text=True)


# ============================================================
# 메인 진입점
# ============================================================

def export_mnc_estimate(
    template_path: str,
    output_path: str,
    result: dict,
    meta: dict,
    verify: bool = True,
) -> str:
    """calc_estimate 결과를 산출내역서(공공형) 양식 xlsx로 출력 (레거시 함수명 mnc 유지).

    Args:
        template_path: assets/mnc_template.xlsx 절대경로 (산출내역서 공공형 템플릿)
        output_path: 생성할 출력 xlsx 절대경로
        result: calc_estimate() 반환 dict
        meta: 외부 주입 변수 dict (project_title, customer_name, event_period, event_venue,
              supplier_* 13개, rfp_amount 등). 모든 슬롯은 사용자가 매번 주입.
        verify: True면 저장 후 재오픈하여 무결성 + pkVat 일치 검증

    Returns:
        output_path (생성·검증 완료된 경로)
    """
    shutil.copy(template_path, output_path)
    wb = load_workbook(output_path)
    ws = wb.active

    # 시트명 변경 (옵션)
    if meta.get('project_title'):
        try:
            ws.title = meta['project_title'][:31]   # Excel 시트명 31자 제한
        except Exception:
            pass

    # 1) 기존 본문 정리
    _clear_body_rows(ws, start_row=21, end_row=200)

    # 2) 헤더 영역 채움
    _write_headers(ws, meta)

    # 3) 7개 섹션 작성
    sections = _build_section_data(result, meta)
    subtotal_cells = []
    next_row = 21

    for section in sections:
        # 카테고리 헤더 행
        _write_category_row(ws, next_row, section['title'])
        next_row += 1

        # 데이터 행들
        item_start = next_row
        for item in section['rows']:
            _write_item_row(ws, next_row, item)
            next_row += 1
        item_end = next_row - 1

        # 소계 행
        _write_subtotal_row(ws, next_row, item_start, item_end)
        subtotal_cells.append(f'I{next_row}')
        next_row += 1

        # 구분선
        ws.row_dimensions[next_row].height = 10
        next_row += 1

    # 4) 합계영역 (Row 12~17) 갱신 — 방식 A 룰
    #    I12 = 모든 소계 SUM, I13 = 0 (PCO는 body section), I15 = 0 (할인 없음)
    #    I14, I16, I17은 기존 수식 유지 (템플릿 그대로)
    if subtotal_cells:
        ws['I12'] = '=' + '+'.join(subtotal_cells)
    else:
        ws['I12'] = 0
    ws['I13'] = 0
    ws['I15'] = 0
    # I14, I16, I17은 템플릿 수식 그대로 유지 (overwrite 금지)

    # 5) B8 한글 금액 (calc_estimate의 pkVat 직접 사용 — recalc 불요)
    ws['B8'] = format_estimate_amount(result['pkVat'])

    # 6) K9 RFP 금액 (외부 주입, 없으면 0)
    ws['K9'] = meta.get('rfp_amount', 0)

    wb.save(output_path)

    if verify:
        _verify_integrity(output_path, result)

    return output_path


# ============================================================
# 섹션 데이터 빌드
# ============================================================

# 라벨 매핑 (sysBreakdown 키 → 표시 이름)
_SYS_LABELS = {
    'video':        '영상 콘솔/LED 출력',
    'scaler4k':     '4K 스케일러/KVM',
    'audio':        '음향 시스템',
    'engineer':     '엔지니어',
    'presentation': '발표 지원',
    'registration': '등록 시스템',
    'misc':         '기타 시스템',
}
_DES_LABELS = {
    'env': '환경 디자인',
    'web': '웹페이지',
    'kv':  '키비주얼',
}
_OPS_LABELS = {
    'desk':      '접수대',
    'ops':       '운영 인력',
    'insurance': '보험',
}


def _build_section_data(result: dict, meta: dict) -> list:
    """7개 섹션의 row 데이터 리스트 빌드.

    각 row 튜플: (item_name, description, spec, unit_price, qty, dur, amount)
    amount는 항상 직접 값 (방식 A는 calc_estimate가 이미 계산함).
    """
    sections = []

    # 1. 베뉴 사용료
    venue_name = meta.get('event_venue') or '(외부 주입 - 베뉴명)'
    sections.append({
        'title': '1. 베뉴 사용료',
        'rows': [
            (venue_name, '5성급 표준 대관료', '1일 full day', result['s1'], 1, 1, result['s1']),
        ],
    })

    # 2. 시스템 구축
    sys_rows = []
    for key, label in _SYS_LABELS.items():
        amt = result.get('sysBreakdown', {}).get(key, 0)
        if amt > 0:
            sys_rows.append((label, '', '1식', amt, 1, 1, amt))
    sections.append({'title': '2. 시스템 구축', 'rows': sys_rows})

    # 3. 디자인 및 브랜딩
    des_rows = []
    for key, label in _DES_LABELS.items():
        amt = result.get('desBreakdown', {}).get(key, 0)
        if amt > 0:
            des_rows.append((label, '', '1식', amt, 1, 1, amt))
    sections.append({'title': '3. 디자인 및 브랜딩', 'rows': des_rows})

    # 4. 운영 및 보험
    ops_rows = []
    for key, label in _OPS_LABELS.items():
        amt = result.get('opsBreakdown', {}).get(key, 0)
        if amt > 0:
            ops_rows.append((label, '', '1식', amt, 1, 1, amt))
    sections.append({'title': '4. 운영 및 보험', 'rows': ops_rows})

    # 5. 추가옵션
    ot_rows = []
    for opt_id, amt in result.get('otBreakdown', {}).items():
        if amt <= 0:
            continue
        if opt_id == 'booth':
            label = '부스 운영'
            spec = f"{amt // 1_000_000}개"
        else:
            label = OPTS.get(opt_id, {}).get('label', opt_id)
            spec = '1식'
        ot_rows.append((label, '', spec, amt, 1, 1, amt))
    if not ot_rows:
        ot_rows = [('(추가옵션 없음)', '', '', 0, 0, 0, 0)]
    sections.append({'title': '5. 추가옵션', 'rows': ot_rows})

    # 6. 모객 솔루션
    g = result.get('g', 0)
    mobil_rows = []
    if result.get('rsvpPkg', 0) > 0:
        mobil_rows.append(('RSVP 관리', '모객 게런티 기준', f'{g}명', 40_000, g, 1, result['rsvpPkg']))
    if result.get('showup', 0) > 0:
        mobil_rows.append(('쇼업 보장', '모객 게런티 기준', f'{g}명', 350_000, g, 1, result['showup']))
    if not mobil_rows:
        mobil_rows = [('(모객 솔루션 없음)', '', '', 0, 0, 0, 0)]
    sections.append({'title': '6. 모객 솔루션', 'rows': mobil_rows})

    # 7. PCO 기획료
    sections.append({
        'title': '7. PCO 기획료',
        'rows': [
            ('PCO 기획료', '운영비의 25% (만원 미만 절사)', '1식', result['s5'], 1, 1, result['s5']),
        ],
    })

    return sections


# ============================================================
# 행 작성 헬퍼
# ============================================================

def _safe_unmerge_in_range(ws, start_row: int, end_row: int):
    """row 범위에 걸친 모든 병합셀을 안전 해제."""
    to_unmerge = []
    for merged_range in list(ws.merged_cells.ranges):
        if merged_range.min_row >= start_row and merged_range.max_row <= end_row:
            to_unmerge.append(str(merged_range))
        elif merged_range.min_row <= end_row and merged_range.max_row >= start_row:
            # 부분 겹침
            to_unmerge.append(str(merged_range))
    for rng in to_unmerge:
        try:
            ws.unmerge_cells(rng)
        except (KeyError, ValueError):
            pass


def _clear_body_rows(ws, start_row: int, end_row: int):
    """본문 행 영역의 값·서식·병합 안전 정리."""
    _safe_unmerge_in_range(ws, start_row, end_row)
    for row in range(start_row, end_row + 1):
        for col in range(1, 12):  # A~K
            cell = ws.cell(row=row, column=col)
            cell.value = None
            # 행 높이는 기본값으로 두고 필요 시 작성 단계에서 설정


def _write_category_row(ws, row: int, title: str):
    """카테고리 헤더 행: A~I 병합 + 액센트 배경(SoT 미러: --jc-accent #2962FF) + 흰색 Bold."""
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=9)
    ws.merge_cells(start_row=row, start_column=10, end_row=row, end_column=11)  # J:K 병합
    cell = ws.cell(row=row, column=1, value=title)
    cell.fill = FILL_CATEGORY
    cell.font = FONT_WHITE_BOLD
    cell.alignment = ALIGN_LEFT
    cell.border = BORDER_HAIR
    ws.row_dimensions[row].height = 25.0


def _write_item_row(ws, row: int, item: tuple):
    """데이터 행: 7컬럼 (A=item, B=desc, C=spec, D=unit_price, E=qty, F=dur, I=amount)."""
    item_name, desc, spec, unit_price, qty, dur, amount = item

    ws.cell(row=row, column=1, value=item_name)
    ws.cell(row=row, column=2, value=desc or '')
    ws.cell(row=row, column=3, value=spec or '')
    ws.cell(row=row, column=4, value=unit_price)
    ws.cell(row=row, column=5, value=qty)
    ws.cell(row=row, column=6, value=dur)
    ws.cell(row=row, column=9, value=amount)

    # 스타일 적용
    for col in range(1, 12):
        cell = ws.cell(row=row, column=col)
        cell.font = FONT_BODY
        if col == 1:
            cell.border = BORDER_ITEM_A
            cell.alignment = ALIGN_LEFT
        elif col == 11:
            cell.border = BORDER_ITEM_K
        else:
            cell.border = BORDER_HAIR
            if col in (4, 5, 6, 9):
                cell.alignment = ALIGN_RIGHT
                cell.number_format = '#,##0'
            else:
                cell.alignment = ALIGN_LEFT

    # J:K 병합
    ws.merge_cells(start_row=row, start_column=10, end_row=row, end_column=11)

    ws.row_dimensions[row].height = 25.0


def _write_subtotal_row(ws, row: int, item_start: int, item_end: int):
    """소계 행: A:H 병합 ("소계") + I열 SUM + 회색 배경 + 빨강 텍스트."""
    # A:H 병합
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=8)
    # J:K 병합
    ws.merge_cells(start_row=row, start_column=10, end_row=row, end_column=11)

    label_cell = ws.cell(row=row, column=1, value='소계')
    label_cell.fill = FILL_SUBTOTAL
    label_cell.font = FONT_BODY_BOLD
    label_cell.alignment = ALIGN_RIGHT
    label_cell.border = BORDER_SUBTOTAL

    sum_cell = ws.cell(row=row, column=9, value=f'=SUM(I{item_start}:I{item_end})')
    sum_cell.fill = FILL_SUBTOTAL
    sum_cell.font = FONT_SUBTOTAL
    sum_cell.alignment = ALIGN_RIGHT
    sum_cell.number_format = '#,##0'
    sum_cell.border = BORDER_SUBTOTAL

    # K열도 회색 배경 (이어보이게)
    for col in (10, 11):
        c = ws.cell(row=row, column=col)
        c.fill = FILL_SUBTOTAL
        c.border = BORDER_SUBTOTAL

    ws.row_dimensions[row].height = 25.0


def _write_headers(ws, meta: dict):
    """헤더 영역 (Row 3~9) 외부 주입 변수 채움.

    슬롯 키 → Excel 셀 매핑은 SKILL.md Step 3.5 참조.
    모든 값이 None/빈 문자열일 수 있음 (사용자가 단계적 입력 시).
    """
    # 행사 정보 (좌측)
    ws['B3'] = meta.get('project_title', '')
    ws['B4'] = meta.get('customer_name', '')
    ws['B5'] = meta.get('event_period', '')
    ws['B6'] = meta.get('event_venue', '')
    # B7 (견적일시)는 템플릿의 =TODAY() 수식 유지
    # B8 (한글금액)은 메인에서 별도 처리

    # 공급자 정보 (우측, 외부 주입)
    ws['I3'] = meta.get('supplier_company', '')
    ws['I4'] = meta.get('supplier_biz_reg_no', '')
    ws['K4'] = meta.get('supplier_representative', '')
    ws['I5'] = meta.get('supplier_address', '')
    ws['I6'] = meta.get('supplier_biz_type', '')
    ws['K6'] = meta.get('supplier_biz_item', '')
    ws['I7'] = meta.get('supplier_manager', '')
    ws['K7'] = meta.get('supplier_email', '')
    ws['I8'] = meta.get('supplier_phone', '')
    ws['K8'] = meta.get('supplier_fax', '')


# ============================================================
# 무결성 검증
# ============================================================

def _verify_integrity(output_path: str, result: dict):
    """저장된 xlsx 재오픈 + 핵심 셀 검증.

    검증 항목:
    1. 재오픈 가능 (zip 무결성)
    2. B8 셀이 format_estimate_amount(pkVat) 와 일치
    3. I12 (합계) 수식이 SUM 참조 형태로 존재 (값 검증은 recalc 후 가능 — 본 함수는 수식 존재만)
    """
    wb = load_workbook(output_path)
    ws = wb.active

    expected_b8 = format_estimate_amount(result['pkVat'])
    actual_b8 = ws['B8'].value
    if actual_b8 != expected_b8:
        raise AssertionError(
            f"B8 mismatch:\n  expected: {expected_b8}\n  actual:   {actual_b8}"
        )

    i12 = ws['I12'].value
    if not (isinstance(i12, str) and i12.startswith('=')):
        raise AssertionError(f"I12 합계 수식 누락 또는 형식 불일치: {i12!r}")

    wb.close()
    return True


# ============================================================
# 리멤버 양식 — v1 방식 (calcEstimate 미적용, 헤더만 갱신)
# ============================================================

def export_remember_estimate(
    template_path: str,
    output_path: str,
    meta: dict,
) -> str:
    """리멤버 양식 — v1 방식 (헤더만 외부 주입 변수로 채움).

    SSOT는 산출내역서(공공형) 양식만 다룸. 리멤버 calcEstimate 적용은 별도 사이클(Sprint 1.6).
    본 함수는 v1 동작 유지 (회귀 없음) 만 보장.
    """
    shutil.copy(template_path, output_path)
    wb = load_workbook(output_path)

    # Opt1 sheet 우선, 없으면 첫 시트
    sheet_name = next(
        (n for n in wb.sheetnames if 'Opt1' in n or 'Premium' in n),
        wb.sheetnames[0]
    )
    ws = wb[sheet_name]

    # 행사 정보 (외부 주입 변수)
    ws['B11'] = meta.get('project_title', '')
    ws['B12'] = meta.get('package_type', '')
    ws['B13'] = meta.get('event_venue', '')
    ws['B14'] = meta.get('event_notes', '')
    ws['B15'] = meta.get('proposal_date', '')

    # 공급자 정보 (외부 주입 변수)
    ws['G11'] = meta.get('proposal_date', '')
    ws['G12'] = meta.get('validity_period', '제안일자로 부터 30일')
    ws['G13'] = meta.get('supplier_company', '')
    ws['G14'] = meta.get('supplier_address', '')
    ws['G15'] = meta.get('supplier_manager', '')
    ws['G16'] = meta.get('supplier_contact', '')

    # 시트명 변경
    if meta.get('project_title'):
        try:
            ws.title = meta['project_title'][:31]
        except Exception:
            pass

    wb.save(output_path)
    return output_path


# ============================================================
# CLI 자가검증
# ============================================================

def _self_test():
    """본 모듈 단독 실행 시 SSOT §9 시나리오로 샘플 1건 생성·검증."""
    import sys
    from calc_estimate import calc_estimate

    HERE = Path(__file__).parent
    template = HERE / '..' / 'assets' / 'mnc_template.xlsx'
    out = HERE / '_self_test_output.xlsx'

    if not template.exists():
        print(f"FAIL: template not found at {template}")
        return 1

    result = calc_estimate({
        'target': 100, 'guarantee': 100,
        'options': {}, 'boothCount': 0,
    })
    assert result['pk'] == 83_750_000, f"calc_estimate 자체 오류: pk={result['pk']}"

    meta = {
        'project_title': 'Self Test Standard',
        'customer_name': '(self-test)',
        'event_period': '(self-test)',
        'event_venue': '(self-test 5성급)',
        # supplier 슬롯은 비워둠 (외부 주입 변수)
    }

    export_mnc_estimate(str(template), str(out), result, meta, verify=True)

    print(f"PASS: {out}")
    print(f"  pk     = {result['pk']:,}")
    print(f"  pkVat  = {result['pkVat']:,}")

    out.unlink()  # 자가검증 결과물 즉시 삭제
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(_self_test())
