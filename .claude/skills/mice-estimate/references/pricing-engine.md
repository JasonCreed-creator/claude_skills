# 가격 산출 엔진 (pricing-engine)

**SSOT**: 견적Configurator_로직명세서_v1_0.md §5
**구현 파일**: `scripts/calc_estimate.py`
**검증**: SSOT §9 100명 표준견적 = 83,750,000원 (자가검증 PASS)

`calcEstimate.js` (MiceConfigurator SaaS의 견적 엔진) 의 Python 포팅. M&C 양식의 자동 산출에 사용. 리멤버 양식은 본 엔진 미사용 (별도 단가 — Sprint 1.6 분리).

---

## 1. 호출 방법

```python
from calc_estimate import calc_estimate

result = calc_estimate({
    'target': 100,              # 필수. 40~500
    'guarantee': 100,           # None이면 target과 동일
    'venueRental': None,        # None이면 target × 180,000 (5성급)
    'venueName': '조선팰리스 강남',
    'options': {'video': True, 'emcee': True},
    'boothCount': 0,
})

print(result['pk'])     # 최종 견적 (VAT별도)
print(result['pkVat'])  # VAT 포함
```

---

## 2. 입력 (c)

| 키 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `target` | int | (필수) | 총 참석인원. 40~500. 500 초과 시 isCustom=True 별도 협의 모드 |
| `guarantee` | int / None | None | 모객 게런티 (RSVP·쇼업 과금 기준). None이면 target |
| `venueRental` | int / None | None | 베뉴 대관료. None이면 target × 180,000 (5성급 자동) |
| `venueName` | str / None | None | 베뉴명 (참조용) |
| `options` | dict / None | None | 옵션 활성화 사전. 그룹 상호배제 자동 적용 |
| `boothCount` | int | 0 | 부스 수 (0~50). booth × 100만 |

---

## 3. 출력 dict

| 키 | 의미 |
|---|---|
| `isCustom` | bool. target>500이면 True, 모든 금액 0 |
| `t`, `g` | 입력된 target / guarantee |
| `s1` | Section 1: 베뉴 사용료 |
| `s2` | Section 2: 시스템 구축 합계 |
| `s3` | Section 3: 디자인·브랜딩 합계 |
| `s4` | Section 4: 운영·보험 합계 |
| `s5` | Section 5: PCO 기획료 (opCost×25% 절사) |
| `ot` | 추가옵션 합계 |
| `rsvpOrig` / `rsvpPkg` | RSVP 정가 / 할인가 |
| `showupOrig` / `showup` | 쇼업 정가 / 할인가 |
| `leadOrig` / `leadPkg` | rsvpOrig+showupOrig / rsvpPkg+showup |
| `opCost` | s1+s2+s3+s4+ot+rsvpPkg (PCO 기획료 산출 기준) |
| `pk` | **최종 견적 (VAT별도)** = s1+s2+s3+s4+s5+ot+rsvpPkg+showup |
| `pkVat` | pk × 1.1 (반올림) |
| `sysBreakdown` | s2 항목별 사전 |
| `desBreakdown` | s3 항목별 사전 |
| `opsBreakdown` | s4 항목별 사전 |
| `otBreakdown` | ot 옵션별 사전 |
| `optionsApplied` | 상호배제 적용 후 최종 옵션 활성화 상태 |

---

## 4. 섹션별 공식 (SSOT §5.3)

### Section 1: 베뉴 사용료 (s1)

```
s1 = venueRental (있으면)  또는  target × 180,000
```

### Section 2: 시스템 구축 (s2)

| 항목 | 공식 | 비고 |
|---|---|---|
| video | 2,000,000 (고정) | ⚠️ 옵션 `video`(동영상촬영)와 별개 — s2의 video는 영상 콘솔 |
| scaler4k | target ≥ 100 → 2,500,000 / 미만 → 0 | 100명 이상 자동 포함 |
| audio | 1,500,000 + ⌈max(0, target-50) / 100⌉ × 500,000 | |
| engineer | 1,000,000 | |
| presentation | 1,200,000 | |
| registration | target > 200: 1,000,000 + ⌊target/100⌋ × 1,000,000<br>target ≤ 200: 1,000,000 + max(0, target-100) × 5,000 | 200/201 경계에서 1.5M 점프 (SSOT 명시) |
| misc | 500,000 + ⌈max(0, target-50) / 100⌉ × 500,000 | |

### Section 3: 디자인·브랜딩 (s3)

| 항목 | 공식 |
|---|---|
| env | target ≤ 50: 2,000,000 / ≤ 100: 2,500,000 / ≤ 150: 3,000,000 / 150+: 3,500,000 |
| web | 1,000,000 |
| kv | 1,000,000 |

### Section 4: 운영·보험 (s4)

| 항목 | 공식 |
|---|---|
| desk | ⌈target / 50⌉ × 250,000 |
| ops | 900,000 + ⌈max(0, target-100) / 100⌉ × 300,000 |
| insurance | 400,000 + ⌈max(0, target-100) / 100⌉ × 100,000 |

### 추가옵션 (ot)

```
ot = Σ(활성화된 OPTS 단가)  + boothCount × 1,000,000
```

옵션 카탈로그·상호배제 규칙은 [option-catalog.md](option-catalog.md) 참조.

### 모객 솔루션

| 항목 | 정가 | 할인가 |
|---|---|---|
| RSVP 관리 | guarantee × 50,000 | guarantee × 40,000 (`rsvpPkg`) |
| 쇼업 보장 | guarantee × 450,000 | guarantee × 350,000 (`showup`) |

### Section 5: PCO 기획료 (s5)

```
opCost = s1 + s2 + s3 + s4 + ot + rsvpPkg
s5 = ⌊(opCost × 0.25) / 10,000⌋ × 10,000   # 만원 미만 절사
```

### 최종 합계 (pk)

```
pk    = s1 + s2 + s3 + s4 + s5 + ot + rsvpPkg + showup    (VAT별도)
pkVat = round(pk × 1.1)                                    (VAT 10% 포함)
```

---

## 5. 14개 하드코딩 상수 (모듈 상단)

| 상수 | 값 | Phase 1 DB화 |
|---|---|---|
| `TARGET_MIN` | 40 | ○ |
| `TARGET_MAX` | 500 | ○ |
| `GUARANTEE_MIN` | 40 | ○ |
| `BOOTH_UNIT_PRICE` | 1,000,000 | ○ |
| `VENUE_PER_PAX_5STAR` | 180,000 | ○ |
| `SYS_VIDEO_PRICE` | 2,000,000 | ○ |
| `SYS_SCALER4K_PRICE` | 2,500,000 | ○ |
| `SYS_ENGINEER_PRICE` | 1,000,000 | ○ |
| `SYS_PRESENTATION_PRICE` | 1,200,000 | ○ |
| `DES_WEB_PRICE` | 1,000,000 | ○ |
| `DES_KV_PRICE` | 1,000,000 | ○ |
| `RSVP_PKG_PRICE` | 40,000 (per g) | ○ |
| `SHOWUP_PKG_PRICE` | 350,000 (per g) | ○ |
| `PCO_FEE_RATE` | 0.25 | ○ |

(`RSVP_ORIG_PRICE`, `SHOWUP_ORIG_PRICE`, `PCO_FEE_TRUNCATE_UNIT`은 14상수 외 보조 상수 — 정가 표시 및 절사 단위)

---

## 6. 자가검증 실행

```bash
cd 02-build/scripts
python calc_estimate.py
```

→ SSOT §9 (100명 = 83,750,000원) 일치 시 exit 0, 불일치 시 exit 1.

---

## 7. 호환성 메모

- **시그니처**: calcEstimate.js와 동일. cfg 객체 키도 동일 (camelCase 유지).
- **호출처 무변경 보장**: pk, sections, breakdown 키가 동일하게 반환됨.
- **Phase 1 DB화 이후**: `calcEstimateV2` 가 DB lookup 후 동일 시그니처 반환 예정. v1 wrapper 유지.
- **golden test 30건 0원 일치**: SSOT §10에 명시. 본 Python 포팅도 동일 검증 통과 필수 (Sprint 1에서는 §9 단일 케이스 검증, 나머지 29건은 Phase 1 마이그레이션 시).
