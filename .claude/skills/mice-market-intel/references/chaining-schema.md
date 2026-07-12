# 체이닝 스키마 — mice-market-intel

`mice-market-intel`의 출력 `ChainPayload` 매핑 정본. 봉투 구조는 **정본 `jc-design-system/references/chaining-protocol.md`(ChainPayload/v1)**. 본 문서는 *본 스킬 고유 페이로드*만 정의한다.

> 봉투 공통: `$schema:"ChainPayload/v1"` · `source` · `version` · `generatedAt` · (`target`) · (`clientId`). 페이로드는 봉투와 같은 최상위에 평탄 공존.

---

## 1. 입력 (소비)
주로 *생산자*다. 다만 `jc-strategy-canvas`/`mice-rfp-analyzer`의 `open_questions`(미검증 항목)를 **재조사 의뢰**로 받을 수 있다 — 그 항목들을 Phase 1 아웃라인 시드로 흡수.

## 2. 출력 (배출)

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-market-intel",
  "version": "v1.0.2",
  "generatedAt": "2026-06-04T10:00:00+09:00",
  "target": "jc-strategy-canvas",
  "clientId": null,

  "topic": "{{topic}}",
  "scope": { "purpose": "신사업 사업성", "as_of": "2026-06-04" },
  "market_size": {
    "tam": { "value": "...", "unit": "억원", "year": 2025, "sources": [0], "tier": "T1" },
    "sam": { "value": "...", "confidence": "single_source", "sources": [1] },
    "som": { "value": "[미확인]" }
  },
  "competitors": [
    { "name": "{{경쟁사 공개명}}", "flagship": "...", "share_est": "...", "strengths": ["..."], "weaknesses": ["..."], "sources": [2,3], "tier": "T2" }
  ],
  "trends": [ { "label": "하이브리드 포맷 확산", "signal": "...", "sources": [4], "tier": "T2" } ],
  "sponsor_candidates": [ { "industry": "...", "company": "{{후보 공개명}}", "fit": "...", "sources": [5] } ],
  "policy_demand": [ { "item": "지원사업", "detail": "...", "sources": [6], "tier": "T1" } ],
  "benchmarks": [ { "event": "{{레퍼런스 행사}}", "takeaway": "...", "sources": [7] } ],
  "gaps": ["SAM 세그먼트 비율 [미확인]", "경쟁사 점유 [단일출처]"],
  "sources": [
    { "id": 0, "url": "...", "publisher": "통계청 KOSIS", "date": "2025", "tier": "T1" }
  ]
}
```

- `sources[]`는 **인덱스 참조**(각 데이터의 `sources:[id]`가 가리킴) — 출처 추적성 보장.
- `tier`/`confidence`/`gaps`로 **근거 강도를 다운스트림에 전달**. 강도 낮은 데이터는 하류에서 단정 자제 신호.

## 3. 다운스트림 매핑

| → 대상 | 전달 핵심 | 대상 활용 |
|--------|----------|----------|
| `jc-strategy-canvas` | `market_size`·`competitors`·`trends` | F2(5 Forces)·F5(포지셔닝)·F6(TAM/SAM/SOM) `[검증]` 근거 |
| `mice-rfp-analyzer` | `competitors`·`policy_demand` | 7축 중 경쟁·전략권고 사전 근거 |
| `mice-proposal` | `market_size`·`trends`·`benchmarks` | 제안서 배경·시장 논거 슬라이드 |
| `mice-sponsor-deck` | `sponsor_candidates`·산업 분포 | 스폰서 후보·타깃 산업 |

## 4. 표준 규약 (chaining-protocol 준수)

- 저장: `.chaining/[topic]_[YYYYMMDD]_to_[target].json` (chaining-protocol §6-4).
- 받은 데이터 임의 변경 금지(§6-2). 자사·개인 식별 하드코딩 금지(`RULE-NO-COMPANY`) — 단 *조사 대상* 공개 기업명은 사실·출처와 함께 허용.
- `gaps` 비어있지 않으면 다운스트림에 "근거 보강 필요" 신호.

## 5. 체이닝 흐름 요약

```
[조사 의뢰] ─► mice-market-intel ─► 리서치 리포트(md/HTML)
                     │
                     ├─(ChainPayload)─► jc-strategy-canvas (프레임워크 [검증] 근거)
                     ├─(ChainPayload)─► mice-rfp-analyzer  (경쟁 축)
                     ├─(ChainPayload)─► mice-proposal      (시장 논거)
                     └─(ChainPayload)─► mice-sponsor-deck  (스폰서 후보)
   (역방향) strategy-canvas/rfp 의 open_questions ─► market-intel 재조사 아웃라인 시드
```
