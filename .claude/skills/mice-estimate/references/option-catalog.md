# 옵션 카탈로그 (option-catalog)

**SSOT**: 견적Configurator_로직명세서_v1_0.md §4
**구현**: `scripts/calc_estimate.py` 의 `OPTS` 딕셔너리 + `apply_option_constraints()`

`ot` (추가옵션) 섹션에 들어가는 9종 옵션의 단가·그룹·상호배제 규칙. M&C 양식의 자동 산출에서 사용.

---

## 1. 9종 옵션 표

| ID | 라벨 | 단가 | 그룹 | 비고 |
|---|---|---|---|---|
| `souvenir` | 기념품 | **인당 50,000원** | — | 합계 = target × 50,000 |
| `emcee` | 사회자 | 1,500,000원 | — | 고정 |
| `photo` | 사진촬영 | 800,000원 | **media** | 그룹 내 택 1 |
| `video` | 동영상 촬영 | 2,000,000원 | **media** | 그룹 내 택 1. ⚠️ s2 video와 별개 |
| `aving` | AVING 미디어 패키지 | 2,500,000원 | **media** | 그룹 내 택 1 (사진+영상+보도) |
| `scaler4k` | 4K 스케일러/KVM | 2,500,000원 | — | target ≥ 100 시 s2 자동 포함 (옵션 비활성화) |
| `survey` | 사후설문조사 | 1,000,000원 | — | 고정 |
| `photowall_basic` | 포토월 (일반형) | 500,000원 | **photowall** | 그룹 내 택 1 |
| `photowall_premium` | 포토월 (고급형) | 2,000,000원 | **photowall** | 그룹 내 택 1 |

---

## 2. 상호배제 규칙

`apply_option_constraints(options, target)` 가 다음 순서로 정규화:

### 2.1 media 그룹 (택 1)

- 멤버: `photo`, `video`, `aving`
- 둘 이상 True면 **첫 멤버만 유지**, 나머지 자동 False
- 사용자가 "사진+영상 모두" 요청 시 `aving`(통합 패키지)으로 안내

### 2.2 photowall 그룹 (택 1)

- 멤버: `photowall_basic`, `photowall_premium`
- 둘 다 True면 첫 멤버만 유지

### 2.3 scaler4k 자동 포함 / 옵션 무효화

- **target ≥ 100**: s2(시스템 구축)에 자동 포함 (단가 2,500,000)
  → 사용자가 옵션에서 True 해도 **자동 False** (중복 청구 방지)
- **target < 100**: s2에 미포함. 옵션 True 시만 ot에 반영.

---

## 3. ⚠️ s2.video vs ot.video 혼동 방지

| 항목 | 위치 | 의미 | 단가 | 활성화 |
|---|---|---|---|---|
| **s2 video** | 시스템 구축 (Section 2) | 영상 콘솔/LED 출력 | 2,000,000 | 5성급 행사에 항상 포함 |
| **ot video** | 추가옵션 (`OPTS['video']`) | 동영상 촬영 (촬영팀) | 2,000,000 | 사용자 선택 시만 |

→ 단가는 같지만 다른 항목. 코드에서 `SYS_VIDEO_PRICE` vs `OPTS['video']['price']` 로 구분.
→ 사용자가 "영상 빼주세요" 라고 하면 ot.video를 끄는 것 (s2.video는 5성급 기본 — 별도 협의).

---

## 4. boothCount (옵션은 아니지만 ot에 합산)

```python
ot += boothCount × 1,000,000
```

- 0~50개 지원
- 부스 1개당 100만원 (단가 단일)
- otBreakdown에 `'booth': boothCount × 1_000_000` 키로 표시

---

## 5. 사용 예시

### 5.1 기본 (옵션 없음)

```python
result = calc_estimate({'target': 100, 'options': {}})
result['ot']  # → 0
```

### 5.2 video + emcee (단순)

```python
result = calc_estimate({
    'target': 100,
    'options': {'video': True, 'emcee': True}
})
result['ot']  # → 2_000_000 + 1_500_000 = 3_500_000
```

### 5.3 media 그룹 충돌 (자동 정규화)

```python
result = calc_estimate({
    'target': 100,
    'options': {'photo': True, 'video': True, 'aving': True}
})
result['optionsApplied']['photo']   # → True (첫 멤버)
result['optionsApplied']['video']   # → False (자동 해제)
result['optionsApplied']['aving']   # → False
result['ot']                        # → 800_000 (photo만)
```

### 5.4 scaler4k 중복 청구 방지

```python
# target=100, scaler4k 옵션 True로 설정
result = calc_estimate({
    'target': 100,
    'options': {'scaler4k': True}
})
result['optionsApplied']['scaler4k']  # → False (자동 해제)
result['sysBreakdown']['scaler4k']    # → 2_500_000 (s2에 포함)
result['ot']                          # → 0 (옵션은 비활성)
```

### 5.5 부스 포함

```python
result = calc_estimate({
    'target': 100,
    'options': {'survey': True},
    'boothCount': 3,
})
result['otBreakdown']  # → {'survey': 1_000_000, 'booth': 3_000_000}
result['ot']           # → 4_000_000
```

---

## 6. UI 안내 가이드 (사용자와의 대화)

대화로 옵션 받을 때 권장 질문 순서:

1. "행사에 영상 콘솔과 4K 스케일러는 항상 포함되어 있습니다. **별도 동영상 촬영팀**(2M)·**사진촬영**(800K)·**AVING 통합**(2.5M) 중 필요한 것이 있나요?"
2. "사회자(MC) 1.5M 포함할까요?"
3. "기념품(인당 5만)이 있나요? 있다면 인원수 확인."
4. "포토월(일반 500K / 고급 2M) 설치할까요?"
5. "사후 설문조사(1M)는 어떻게 할까요?"
6. "부스 운영이 있나요? 몇 개?"

→ 사용자 답변을 `options` 사전으로 매핑하여 `calc_estimate()` 호출.
