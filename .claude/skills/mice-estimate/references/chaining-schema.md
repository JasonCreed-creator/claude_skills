# 체이닝 스키마 — mice-estimate 입출력 (ChainPayload/v1)

**참조**: 풀 워크플로우 체이닝 원안 master-plan-2026-05-25.md §5-1 (구 마스터플랜, 아카이브) → 현행 흐름 정본은 `jc-design-system/references/chaining-protocol.md` §5
**적용 범위**: mice-estimate 고유 입출력 페이로드 정의(§2~§4) + 직렬화 헬퍼(§7). 상류 출력 함수는 각 스킬 정본에 정의되어 있다(§6).

mice-estimate가 다른 MICE 스킬과 데이터를 주고받기 위한 JSON 스키마와 워크플로우상의 위치를 정의한다.

> **봉투 정본**: 공통 `ChainPayload/v1` 봉투 구조(`$schema`·`source`·`version`·`generatedAt`·`target`(선택)·`clientId`(선택, null 가능)·`projectTitle`)와 전체 워크플로우·source enum·§3-1 별칭 규칙은 [jc-design-system/references/chaining-protocol.md](../../jc-design-system/references/chaining-protocol.md) 참조.
> 요약: 모든 체이닝 JSON은 최상위에 `"$schema": "ChainPayload/v1"` + `source`(생산 스킬) + `version`(생산 스킬 SKILL.md frontmatter 버전)을 두고, 그 아래에 아래 정의된 mice-estimate 고유 페이로드를 평탄하게 담는다. 본 문서는 mice-estimate **고유 입출력 페이로드 매핑**만 정의한다. 정본 키(chaining-protocol §4): `eventScale` `venue` `options` `sections` `totalAmount` — 앞 셋은 **입력**(§2·§3, 출력 봉투 최상위에는 싣지 않고 `metadata.target/guarantee/venueName`·`optionsApplied`로 대체), 뒤 둘은 **출력**(§4). 출력 봉투는 `totalAmountVat`도 함께 싣는다(jc-pptx VAT 캡션이 읽음).
> **실명 금지**(RULE-NO-COMPANY v2): 아래 예시의 발주처·베뉴·행사명은 `{{client_company}}`·`{{venue}}`·`{{event_name}}` 자리표시자다 — 실제 값은 세션에서 주입한다.

---

## 1. 풀 워크플로우상의 위치

```
[RFP·추진계획]
     ↓
mice-rfp-analyzer ──→ 분석 보고서(.docx) + 평가 매트릭스(.xlsx)
     │ GO 판정 시
     ├──→ jc-pptx(제안서) ──→ proposal.pptx
     │         ↓ 덱 확정 시 — §2 봉투 (eventScale · venue · options · displayType)
     └──→ §3 전용 봉투 (eventScale · budgetRange · estimate_hint)
               ↓
          mice-estimate ──→ outputs/리멤버견적서_{{event_name}}_{{YYMMDD}}.xlsx   ⭐ 본 스킬
               ↓ §4 봉투 (totalAmount · totalAmountVat · sections)
     ┌─────────┼──────────────────┐
     ↓         ↓                  ↓
 jc-pptx    mice-ops-docs     mice-aftermath
 ⑦예산 슬라이드  예산 집행률(계획측)  결과보고 '계획 예산'
 (역방향)                          (행사 종료 후)
```

본 스킬은 상류 **mice-rfp-analyzer·jc-pptx**에서 입력을 받고, 하류 **jc-pptx(⑦예산 역방향)·mice-ops-docs·mice-aftermath**로 출력을 전달한다. 흐름 정본: chaining-protocol §5 `[덱 확정]`·`[견적 확정]`·`[행사 종료]`.

---

## 2. 입력 스키마 — `jc-pptx`에서 받기

jc-pptx가 제안서 덱을 확정한 뒤 견적 단계로 넘길 때 내는 봉투(생산 측 정본: `jc-pptx/references/proposal-playbook.md` §6). 견적 입력 키는 **봉투 최상위에 평탄**하게 실린다 — 중첩 `estimate_hint` 객체가 아니다. 같은 봉투의 `deck_meta`·`sections`·`coverage_map`·`presentation`은 덱·대본용이라 견적과 무관하므로 무시한다.

> 하위호환: `source: "mice-proposal"`은 jc-pptx의 별칭 — 수신 시 `jc-pptx`로 치환해 같은 규칙으로 처리한다(chaining-protocol §3-1·§7). 새로 생산하지 않는다.

```json
{
  "$schema": "ChainPayload/v1",
  "source": "jc-pptx",
  "version": "<SKILL.md frontmatter version>",
  "generatedAt": "YYYY-MM-DDTHH:MM:SS+09:00",
  "target": "mice-estimate",
  "clientId": null,
  "projectTitle": "{{event_name}}",

  "client": "{{client_company}}",
  "eventDate": "YYYY-MM-DD",
  "eventScale": { "target": 100, "guarantee": 90 },
  "venue": { "type": "5star", "region": "{{region}}", "name": "{{venue}}", "rental": null },
  "options": {
    "video": false, "emcee": true, "souvenir": true, "scaler4k": false, "survey": false,
    "photowall_basic": false, "photowall_premium": false, "photo": false, "aving": false
  },
  "displayType": "led",
  "boothCount": 0,
  "format": "remember"
}
```

> `format`은 항상 `remember`(v3.3.0 양식 단일화 — 다른 값은 무시하고 리멤버 양식으로 작성). `version`은 생산 스킬의 SKILL.md frontmatter 버전을 그대로 싣는다.

### 필드 매핑 (input JSON → calc_estimate_remember cfg)

| ChainPayload 필드 | → cfg 키 | 변환 |
|---|---|---|
| `eventScale.target` | `target` | 그대로 (40~500) |
| `eventScale.guarantee` | `guarantee` | null이면 target |
| `venue` = `null` | `venueRental=None` · `venueName=''` | 대관료 자동 산출 — §3 처리 규칙과 동일(상류 proposal-playbook §6이 `venue: null` 허용) |
| `venue.rental` | `venueRental` | null이면 자동 산출(target × 데이터셋 5성 인당 단가) |
| `venue.name` | `venueName` | 그대로(참조용) |
| `options` | `options` | 그대로 (9개 불리언 키) — null이면 전부 False |
| `displayType` | `displayType` | `led`(기본) 또는 `projector` — 스케일러(≥100명 & LED → 시스템 s2)·화면중계(LED만 과금) 게이트 |
| `boothCount` | `boothCount` | 그대로 |
| `format` | (양식) | 항상 `remember` (v3.3.0 — 분기 없음) |
| `projectTitle`, `client` | (Excel 헤더) | 리멤버 양식 상단 메타(Project Title)·시트명·파일명에 사용 |
| `eventDate` | (Excel 헤더) | 비고(일시) 기입용 — calc 입력 아님 |
| `clientId` | (봉투 메타) | 출력 봉투(§4) `clientId`로 무변경 승계 |

---

## 3. 입력 스키마 — `mice-rfp-analyzer`에서 받기 (§3-1 전용 봉투)

RFP 분석 단계의 mice-estimate 전용 봉투(생산 측 정본: `mice-rfp-analyzer/references/chaining-guide.md` §3-1, `target: "mice-estimate"`). 베뉴·옵션이 미정일 수 있어 일부 필드는 `null`. 6축 금액 데이터는 같은 봉투의 `estimate_hint`로 함께 온다.

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-rfp-analyzer",
  "version": "<SKILL.md frontmatter version>",
  "generatedAt": "YYYY-MM-DDTHH:MM:SS+09:00",
  "target": "mice-estimate",
  "clientId": null,
  "projectTitle": "{{event_name}}",

  "client": "{{client_company}}",
  "rfpId": "{{공고번호 또는 null}}",
  "eventDate": "YYYY-MM-DD",
  "budgetRange": { "min": null, "max": 120000000, "currency": "KRW", "vatIncluded": true },
  "evaluationCriteria": [
    { "name": "가격", "weight": 30 },
    { "name": "기술/실적", "weight": 70 }
  ],
  "eventScale": { "target": 100, "guarantee": null },
  "venue": null,
  "options": null,
  "boothCount": 0,
  "format": "remember",
  "notes": "RFP 단계 — 베뉴·옵션 TBD. 발주처 지정 서식: (있으면 명칭·요구 항목)",

  "estimate_hint": {
    "budget_announced": 120000000,
    "estimated_cost": 95000000,
    "recommended_bid": 114000000,
    "vat": "포함",
    "risk_premium": 0.05
  }
}
```

### 처리 규칙

- `venue: null` → `venueRental=None` → 대관료 자동 산출(target × 데이터셋 5성 인당 단가). `venue.name`만 있고 `rental: null`이면 이름만 참조.
- `options: null` → 모든 옵션 False. `eventScale.guarantee: null` → target. `displayType`가 없으면 `led`(엔진 기본값).
- 출력 봉투(§4) `metadata.estimatedFrom = "rfp_default"` 플래그.
- `budgetRange`·`evaluationCriteria`는 calc 입력이 아니다 — 산출 후 비교·가격 점수 가중 판단용.
- **`estimate_hint` 활용** — calc 입력이 아니다. 산출 후 제안가(`pk` VAT 별도 · `pkVat` VAT 포함)를 `budget_announced`·`recommended_bid`와 대비해 **어디에 있는지 한 줄**(예: "제안가 ○○원 — 발주가 대비 △%, 권고 입찰가 대비 ▽%")로 명시한다 → SKILL.md Step 6.5 완료 게이트 6(가격 산식 연동). `vat`('별도'|'포함')에 맞춰 비교 기준(pk vs pkVat)을 맞추고, `risk_premium`은 제안가 결정(pricing-strategy.md) 때 참고하되 원가에 자동 가산하지 않는다.
- `notes`의 발주처 지정 서식(산출내역서 항목명·합계 구조)은 섹션 안 항목명·비고로 맞춘다(SKILL.md Step 1).

---

## 4. 출력 스키마 — jc-pptx·mice-ops-docs·mice-aftermath로 전달

mice-estimate가 견적 산출 + Excel 생성 후 후속 스킬에 전달하는 봉투. `target`은 수신 스킬(선택 — 생략하면 세 스킬 공통 봉투). 저장: `.chaining/{{event_name}}_{{YYYYMMDD}}_to_{{target}}.json` (`target` 없으면 `_to_any`, chaining-protocol §6-4).

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-estimate",
  "version": "<SKILL.md frontmatter version>",
  "generatedAt": "YYYY-MM-DDTHH:MM:SS+09:00",
  "target": "jc-pptx",
  "clientId": null,
  "projectTitle": "{{event_name}}",
  "format": "remember",
  "isCustom": false,
  "totalAmount": 83750000,
  "totalAmountVat": 92125000,
  "sections": {
    "s1_venue":      18000000,
    "s2_system":     10700000,
    "s3_design":      4500000,
    "s4_operations":  1800000,
    "s5_pco":         9750000,
    "ot_options":           0,
    "rsvpPkg":        4000000,
    "showup":        35000000
  },
  "breakdown": {
    "sys": {"video": 2000000, "scaler4k": 2500000, "audio": 2000000,
            "engineer": 1000000, "presentation": 1200000,
            "registration": 1000000, "misc": 1000000},
    "des": {"env": 2500000, "web": 1000000, "kv": 1000000},
    "ops": {"desk": 500000, "ops": 900000, "insurance": 400000},
    "ot":  {}
  },
  "optionsApplied": {
    "video": false, "emcee": false, "souvenir": false,
    "scaler4k": false, "survey": false,
    "photowall_basic": false, "photowall_premium": false,
    "photo": false, "aving": false
  },
  "metadata": {
    "target": 100,
    "guarantee": 100,
    "venueName": "{{venue}}",
    "createdAt": "YYYY-MM-DD",
    "estimatedFrom": "user_input"
  },
  "estimateFile": "outputs/리멤버견적서_{{event_name}}_{{YYMMDD}}.xlsx"
}
```

> 금액 예시는 데이터셋 골든 벡터(target=100, 옵션 없음)의 값이다 — 실제 봉투에는 세션 산출값이 들어간다.

### `estimatedFrom` 가능 값

| 값 | 의미 |
|---|---|
| `user_input` | 사용자가 채팅으로 직접 항목·단가 입력 (방식 B) |
| `auto_calc` | calc_estimate_remember 자동 산출 (방식 A, 체이닝 입력 없이) |
| `rfp_default` | mice-rfp-analyzer §3-1 봉투 입력 + 베뉴·옵션 표준값 추정 |
| `proposal_chain` | jc-pptx 입력(구 mice-proposal 별칭) + 자동 산출 |

---

## 5. 후속 스킬에서의 활용

| 수신 스킬 | 읽는 키 | 용도 | 수신 측 정본 |
|---|---|---|---|
| jc-pptx | `totalAmount` · `totalAmountVat` · `sections` | 제안서 ⑦예산 견적 요약 슬라이드(역방향 — 덱 확정 후 견적이 되돌아간다). 총액은 VAT 별도/포함 캡션, `sections` 키별 금액은 표 행, 숫자는 봉투 값 그대로 | `jc-pptx/references/proposal-playbook.md` §1 '보강' |
| mice-ops-docs | `totalAmount` · `sections` | 예산 집행률(계획측) — 실집행은 운영 입력 | `mice-ops-docs/references/chaining-schema.md` |
| mice-aftermath | `totalAmount` · `sections` | 결과보고 '계획 예산'(4축 예산 대비 계획측) — 실집행·계약가는 사용자 입력, 입찰가 회고는 mice-rfp-analyzer 봉투의 `estimate_hint.recommended_bid` | `mice-aftermath/references/chaining-schema.md` |

- pt-script는 견적 봉투를 **읽지 않는다**(`pt-script/references/chaining-schema.md` §6 — 분석·견적·결과보고는 대본 입력이 아님). 발표 대본에 금액이 필요하면 jc-pptx ⑦예산 슬라이드를 거친다.
- 수신 측은 `clientId`·`projectTitle`을 무변경 승계하고(chaining-protocol §6-2), 봉투의 금액을 재산출하거나 임의로 바꾸지 않는다. 발주처 슬롯은 수신 스킬이 자기 입력에서 채운다(§6-3).

---

## 6. 적용 범위 (현행)

| 항목 | 상태 |
|---|---|
| 입출력 JSON 스키마 정의 (본 문서 §2~§4) | ✅ |
| ChainPayload 직렬화 헬퍼 (mice-estimate 측) | ✅ §7 `to_chain_payload()` — 세션에서 붙여 쓰는 참조 구현 |
| 상류 출력 함수 — jc-pptx | ✅ `jc-pptx/references/proposal-playbook.md` §6에 정의(견적 입력 키 최상위 평탄) |
| 상류 출력 함수 — mice-rfp-analyzer | ✅ `mice-rfp-analyzer/references/chaining-guide.md` §3-1에 정의(전용 봉투 + `estimate_hint`) |
| 하류 수신 — jc-pptx ⑦예산 · mice-ops-docs · mice-aftermath | 각 수신 측 정본(§5 표) |
| 풀 워크플로우 end-to-end 검증 | 세션마다 SKILL.md Step 6.5 완료 게이트(입력 반영 전수성 · 가격 산식 연동)로 확인 |

---

## 7. 직렬화 헬퍼 (선택)

`calc_estimate_remember` 결과를 그대로 ChainPayload/v1 출력으로 변환하는 참조 구현. `version`은 하드코딩하지 않고 **SKILL.md frontmatter에서 읽는다**. `target`은 선택 — `'jc-pptx'` | `'mice-ops-docs'` | `'mice-aftermath'` | `None`(공통).

인자 계약:
- `cfg` — calc 입력 dict(**필수**). calc 결과에는 `optionsApplied`가 없으므로 §4의 9키 불리언을 `cfg['options']`에서 만든다.
- `meta` — SKILL.md Step 4 방식 A의 `meta` 그대로. 봉투 키(`projectTitle`·`clientId`·`venueName`·`createdAt`·`estimatedFrom`·`estimateFile`)를 우선 읽고, 없으면 export용 snake_case 키(`project_title`·`venue_text`)로 폴백한다. 상류 봉투가 있으면 `clientId`·`projectTitle`은 무변경 승계(§5). **`estimatedFrom`은 기본값이 없다** — §4 표의 4값 중 하나를 명시(누락 시 `KeyError`로 드러난다).
- `skill_dir` — 이 스킬 폴더. 세션에 붙여넣어 실행하면 `__file__`이 없으므로 **반드시 넘긴다**(환경변수 `MICE_ESTIMATE_SKILL`도 받는다). 호출 예: SKILL.md Step 6 `to_chain_payload(result, meta, cfg, target='jc-pptx', skill_dir=SKILL)`.

```python
import os
import re
from datetime import datetime
from pathlib import Path

OPTION_KEYS = ('video', 'emcee', 'souvenir', 'scaler4k', 'survey',
               'photowall_basic', 'photowall_premium', 'photo', 'aving')   # §4 optionsApplied 9키


def _skill_version(skill_dir) -> str:
    """SKILL.md frontmatter의 version — 봉투 version은 항상 여기서 읽는다(하드코딩 금지). 못 읽으면 'unknown'."""
    try:
        text = (Path(skill_dir) / 'SKILL.md').read_text(encoding='utf-8')
    except OSError:
        return 'unknown'
    m = re.search(r'^version:\s*"?([^"\n]+)"?\s*$', text, re.M)
    return m.group(1).strip() if m else 'unknown'


def to_chain_payload(result: dict, meta: dict, cfg: dict, target: str | None = None,
                     skill_dir=None) -> dict:
    """calc_estimate_remember 결과 → ChainPayload/v1 출력.
    cfg      : calc 입력 dict — optionsApplied는 cfg['options']에서 만든다(calc 결과에 없음).
    meta     : 방식 A meta — 봉투 키 우선, snake_case 폴백. estimatedFrom은 필수(기본값 없음).
    skill_dir: 이 스킬 폴더 — 세션 붙여넣기 실행에는 __file__이 없으므로 필수."""
    skill_dir = skill_dir or os.environ.get('MICE_ESTIMATE_SKILL')
    if not skill_dir:
        raise ValueError('skill_dir(이 스킬 폴더)을 넘기세요 — 세션 붙여넣기 실행에는 __file__이 없습니다')
    options = (cfg or {}).get('options') or {}
    return {
        '$schema': 'ChainPayload/v1',
        'source': 'mice-estimate',
        'version': _skill_version(skill_dir),
        'generatedAt': datetime.now().astimezone().isoformat(timespec='seconds'),
        'target': target,                                   # 선택 — None이면 공통 봉투
        'clientId': meta.get('clientId'),                   # 상류 봉투에서 무변경 승계(null 가능)
        'projectTitle': meta.get('projectTitle') or meta.get('project_title', ''),
        'format': 'remember',   # v3.3.0 — 단일 양식
        'isCustom': result['isCustom'],
        'totalAmount': result['pk'],
        'totalAmountVat': result['pkVat'],
        'sections': {
            's1_venue':      result['s1'],
            's2_system':     result['s2'],
            's3_design':     result['s3'],
            's4_operations': result['s4'],
            's5_pco':        result['s5'],
            'ot_options':    result['ot'],
            'rsvpPkg':       result['rsvpPkg'],
            'showup':        result['showup'],
        },
        'breakdown': {
            'sys': result['sysBreakdown'],
            'des': result['desBreakdown'],
            'ops': result['opsBreakdown'],
            'ot':  result['otBreakdown'],
        },
        'optionsApplied': {k: bool(options.get(k, False)) for k in OPTION_KEYS},   # cfg에서 생성 — calc 결과에 없음
        'metadata': {
            'target':         result['t'],
            'guarantee':      result['g'],
            'venueName':      meta.get('venueName') or meta.get('venue_text') or (cfg or {}).get('venueName', ''),
            'createdAt':      meta.get('createdAt') or datetime.now().strftime('%Y-%m-%d'),
            'estimatedFrom':  meta['estimatedFrom'],        # 필수 — 'user_input'|'auto_calc'|'rfp_default'|'proposal_chain'
        },
        'estimateFile': meta.get('estimateFile', ''),     # 예: outputs/리멤버견적서_{{event_name}}_{{YYMMDD}}.xlsx
    }
```

본 헬퍼는 문서 안의 참조 구현이다 — 호출 측 세션에서 붙여 쓰되 `skill_dir=SKILL`·`cfg`를 반드시 넘긴다. 스크립트로 분리하는 일은 산출 로직 파일 변경을 수반하므로 별도 버전에서 다룬다.
