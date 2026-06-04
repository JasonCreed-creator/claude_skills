# jc-design 매핑 — 큐시트 XLSX

xlsx는 CSS 변수가 불가능한 매체다. `build_runsheet.py`는 jc-design-system SoT(`signature-tokens.md §6` JSON)를 **런타임 로드**하고, 실패 시 미러 hex로 폴백한다. 값의 정본은 항상 jc-design-system.

> 값 SoT: `jc-design-system/references/signature-tokens.md §6`(라이트 JSON). openpyxl은 `#` 없는 6자리 사용.

---

## 1. 역할 → 토큰 매핑

| 위치 | 시맨틱 역할 | SoT 토큰 | 미러 hex |
|------|-----------|---------|---------|
| 행사 헤더(타이틀·일자·베뉴·버전) | 헤더·타이틀 | `--jc-primary` | `0A2540` |
| 컬럼 헤더 행 (Cue#…비고) | 액센트 | `--jc-accent` | `2962FF` |
| 세그먼트 경계 구분 행 | 중립 강조면 | `--jc-border-strong` | `C9CFD8` |
| 연출 cue·전환 강조 | 포인트(핫) | `--jc-point-orange` | `FF5722` |
| 휴식/전환 행 배경 | 보조 면 | `--jc-surface-alt` | `F4F6FA` |
| 본문 텍스트 | 본문 | `--jc-text` + Pretendard | `1A1D24` |

> 미러 hex는 SoT 로드 실패 시 폴백 + 추적용. **하드코딩이 아니라 SoT 미러**임을 코드 주석으로 표기한다(RULE 준수).

---

## 2. 런타임 로드 패턴 (mice-estimate 선례 재사용)

```python
def _load_jc_tokens():
    import json, re
    from pathlib import Path
    try:
        sot = Path(__file__).resolve().parents[2] / "jc-design-system" / "references" / "signature-tokens.md"
        m = re.search(r"```json\s*\n(.*?)\n```", sot.read_text(encoding="utf-8"), re.S)
        return json.loads(m.group(1)) if m else {}
    except Exception:
        return {}
```

`_jc("primary", "0A2540")` 처럼 (SoT 키, 미러 폴백) 형태로 조회한다.

---

## 3. 클라이언트 오버레이

- `event.client_id`가 있으면 `jc-design-system/references/client-overlays.md`의 primary/accent/logo를 적용.
- 없으면(None) 개인 시그니처 그대로. 큐시트는 내부 운영 문서라 기본 시그니처 권장.

---

## 4. 폰트·글꼴

- 한글: `Pretendard`. 숫자(시간·Cue#)는 가독 위해 일반 셀로 두되 정렬 우측.
- 헤더 Bold + 흰색(액센트/프라이머리 배경 위), 본문 일반.

---

## 5. 인쇄 고려 (RULE-PRINT-LIGHT 정합)

큐시트는 현장 인쇄 빈도가 높다. 기본이 라이트(흰 배경)이므로 별도 다크 강제 불필요. 헤더 진한 배경은 인쇄 시 토너 과다가 아니도록 면적을 헤더·컬럼행으로 제한한다.
