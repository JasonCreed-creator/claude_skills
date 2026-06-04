# 체이닝 스키마 — mice-aftermath

`mice-aftermath`의 입출력 `ChainPayload` 매핑. 봉투 구조는 **정본 `jc-design-system/references/chaining-protocol.md`(ChainPayload/v1)**. 본 문서는 *본 스킬 고유 페이로드*만 정의한다.

> 봉투 공통: `$schema:"ChainPayload/v1"` · `source` · `version` · `generatedAt` · (`target`) · (`clientId`). 페이로드는 봉투와 같은 최상위에 평탄 공존. 식별은 `source`로 수렴.

본 스킬은 **사후 단계 소비자 겸 생산자**다 — 상류 결과 데이터를 받아 종합하고, 케이스를 차기 영업 스킬로 배출한다.

---

## 1. 입력 (소비)

행사 결과 데이터를 다음에서 받는다. 모두 있으면 가장 풍부하고, 일부만 있어도 동작(없는 축은 직접 입력/`[미확보]`).

| source | 전달 핵심 | aftermath 활용(8축) |
|--------|----------|---------------------|
| `mice-dashboard` | `kpis`·`insights`·`actualSpending`·`rounds` | 3축 성과·7축 피드백 |
| `mice-estimate` | `totalAmount`·`sections`(계획 예산) | 4축 예산 대비(계획측) |
| `mice-meeting-minutes` | `strategic_notes`·리스크·Action·미결 | 6축 교훈·8축 차기 |
| `mice-run-of-show` | `plan`(계획 타임라인) vs 실제 | 5축 운영 하이라이트 |

### 입력 매핑 (핵심 필드)
```
dashboard.kpis[]            → 3축 KPI (목표 대비). dashboard에 목표 없으면 사용자 보완.
estimate.totalAmount/sections → 4축 '계획 예산' 측 (실집행은 사용자/정산 입력)
minutes.strategic_notes/risks → 6축 교훈, 8축 차기 권고 시드
run-of-show.plan.cues       → 5축 계획 대비 실제(정시성·전환)
```
> **목표(target) 확보 원칙**: 성과는 목표 대비로만 의미가 있다. dashboard가 실적만 주면 목표(KPI 타깃·예산 계획)를 사용자에게 받아 결합한다(SKILL.md Phase 1).

---

## 2. 출력 (배출)

결과보고 + 케이스를 차기 영업 스킬로.

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-aftermath",
  "version": "v1.0.0",
  "generatedAt": "2026-06-05T10:00:00+09:00",
  "target": "mice-proposal",
  "clientId": null,

  "event": { "title": "{{행사명}}", "date": "2026-06-20", "type": "conference",
             "scale": 1180, "client": "{{발주처 또는 익명}}" },
  "performance": {
    "kpis": [ { "name": "참가자 수", "target": 1000, "actual": 1180, "rate": 1.18, "verdict": "달성" } ],
    "budget": { "planned": 0, "actual": 0, "delta_pct": -3.2 }
  },
  "cases": [
    {
      "title": "목표 118% 모객·재계약 확정",
      "challenge": "...", "approach": ["...", "..."],
      "result": ["참가 1,180명(목표 1,000, 118%)", "CSAT 4.2(목표 4.0)"],
      "proof": ["등록 정산", "설문 n=412", "재계약 의향서"],
      "reuse_tier": ["R1", "R2"],
      "anonymize": "consent_or_T社"
    }
  ],
  "lessons": [ { "issue": "등록 전환율 미달", "cause": "리마인드 부족", "fix": "D-7/D-1 자동 리마인드" } ],
  "next": ["차기 재개최 권고", "자동 리마인드 도입"],
  "reportFile": "결과보고서_{{행사명}}_260620.html"
}
```

---

## 3. 다운스트림 매핑

| → 대상 | 전달 핵심 | 대상 활용 |
|--------|----------|----------|
| `mice-proposal` | `cases`(R1)·`performance`·`event` | 차기 비딩 제안서의 **수행실적·유사사례** 슬라이드 |
| `mice-sponsor-deck` | `cases`(R2)·`performance.kpis`(노출·리드) | 스폰서 **ROI 케이스**·실적 증빙 |
| `mice-market-intel`/`jc-strategy-canvas` | `cases`(R3)·`performance` | 벤치마크·시장 검증 근거(선택) |

- `reuse_tier`가 `target`을 결정한다(R1→proposal, R2→sponsor-deck, R3→market-intel/strategy-canvas).
- `anonymize` 플래그를 다운스트림이 존중한다(외부 자료 생성 시 익명화 적용).

---

## 4. 표준 규약 (chaining-protocol 준수)

- 저장: `.chaining/[event]_[YYYYMMDD]_to_[target].json` (chaining-protocol §6-4).
- 받은 데이터 임의 변경 금지(§6-2). 자사·개인 식별 하드코딩 금지(`RULE-NO-COMPANY`).
- 미확보 수치는 페이로드에 `null`/`[미확보]`로 — 다운스트림에 "단정 자제" 신호.

---

## 5. 체이닝 흐름 요약 (선순환)

```
mice-dashboard ─┐
mice-estimate  ─┤
mice-meeting-minutes ─┼─► mice-aftermath ─► 결과보고서(HTML/md)
mice-run-of-show ─┘            │
                              ├─(ChainPayload, R1)─► mice-proposal     (차기 비딩 실적 레퍼런스)
                              └─(ChainPayload, R2)─► mice-sponsor-deck (스폰서 ROI 케이스)
   ※ 한 행사의 결과가 다음 수주·협찬의 자산이 되는 선순환 고리
```

> source enum 등록 (완료): `mice-aftermath`를 봉투 정본(`chaining-protocol.md` §1 적용대상 + §3 enum + §4 매핑 + §5 엣지)에 **등록 완료**(F-1). 다운스트림은 `source` 문자열로 식별한다.
