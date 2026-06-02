"""한글 금액 변환 유틸리티"""

def num_to_korean(n):
    """숫자를 한글 금액 표기로 변환
    예: 302405960 → '삼억이백사십만오천구백육십'
        1292800000 → '십이억구천이백팔십만'
    """
    n = int(round(n))
    if n == 0:
        return "영"
    
    digits = ['', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
    small_units = ['', '십', '백', '천']
    big_units = ['', '만', '억', '조']
    
    groups = []
    while n > 0:
        groups.append(n % 10000)
        n //= 10000
    
    result = ''
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i]
        if g == 0:
            continue
        group_str = ''
        for j in range(3, -1, -1):
            d = (g // (10 ** j)) % 10
            if d == 0:
                continue
            if d == 1 and j > 0:
                group_str += small_units[j]
            else:
                group_str += digits[d] + small_units[j]
        result += group_str + big_units[i]
    
    return result


def format_estimate_amount(total):
    """견적금액 문자열 생성 (B8셀용)
    예: '금 삼억이백사십만오천구백육십원 정 (￦302,405,960/원) 부가세 포함'
    """
    korean = num_to_korean(total)
    formatted = f"{int(round(total)):,}"
    return f"금 {korean}원 정 (￦{formatted}/원) 부가세 포함"
