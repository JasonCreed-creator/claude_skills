# 체이닝 스키마 — mice-market-intel

`mice-market-intel`의 출력 `ChainPayload` 매핑 정본. 봉투 구조는 **정본 `jc-design-system/references/chaining-protocol.md`(ChainPayload/v1)**. 본 문서는 *본 스킬 고유 페이로드*만 정의한다.

> 봉투 공통(chaining-protocol §1·§2): `$schema:"ChainPayload/v1"` · `source` · `version` · `generatedAt` · (`target`) · (`clientId`) · (`projectTitle`). 페이로드는 봉투와 같은 최상위에 평탄 공존. `version`은 SKILL.md frontmatter 현재 값을 그대로 쓴다(예시에 고정 버전 금지).

---

## 1. 입력 (소비)
주로 *생산자*다. 다만 `jc-strategy-canvas`/`mice-rfp-analyzer`의 `open_questions`(미검증 항목)를 **재조사 의뢰**로 받는다 — `detect_input_source()`(chaining-protocol §7)로 판별하고, 그 항목들을 Phase 1 아웃라인 시드로 흡수.

| 보낸 스킬 | `open_questions` 형태 | 아웃라인 시드 | 회신(`target` = 보낸 스킬) |
|-----------|---------------------|--------------|---------------------------|
| `mice-rfp-analyzer` | 객체 `{item, type, source/route}` — `type: client_history` | T4 발주처/정책 환경(발주 이력) | `policy_demand[]` |
| `mice-rfp-analyzer` | 같은 형태 — `type: competitor` | T7 타깃 주체 심층 프로파일(비딩 맞수) | `competitors[]` (`competitor_tier` 포함) |
| `mice-rfp-analyzer` | 같은 형태 — `type: client_query` | 조사하지 않음(발주처 질의 대상) | — |
| `jc-strategy-canvas` | 문자열 배열(미검증 칸 설명) | 해당 템플릿(T1 규모·T2 경쟁 등) | 해당 키 + `gaps` |

정본: `mice-rfp-analyzer/references/chaining-guide.md` §3-2(송신), `jc-strategy-canvas/references/chaining-schema.md` §2(송신).

## 2. 출력 (배출)

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-market-intel",
  "version": "<SKILL.md frontmatter version>",
  "generatedAt": "YYYY-MM-DDTHH:MM:SS+09:00",
  "target": "jc-strategy-canvas",
  "clientId": null,
  "projectTitle": "{{topic}}",

  "topic": "{{topic}}",
  "scope": { "purpose": "신사업 사업성", "as_of": "YYYY-MM-DD" },
  "market_size": {
    "tam": { "value": "...", "unit": "억원", "year": 2025, "sources": [0], "source_tier": "T1" },
    "sam": { "value": "...", "confidence": "single_source", "sources": [1] },
    "som": { "value": "[미확인]" }
  },
  "competitors": [
    {
      "name": "{{경쟁사 공개명}}", "competitor_tier": "direct",
      "flagship": "...", "share_est": "...", "strengths": ["..."], "weaknesses": ["..."],
      "scores": { "positioning": 4, "brand": 3, "content": 4, "portfolio": 3,
                  "attendee_evidence": 2, "client_trust": 4, "sponsor_pull": 3, "revenue_model": 2 },
      "tension_axes": { "axis_a": { "label": "규모", "score": 4 }, "axis_b": { "label": "전문성", "score": 2 },
                        "quadrant": "고1저2" },
      "sources": [2, 3], "source_tier": "T2"
    }
  ],
  "whitespace_candidates": [
    { "segment": "지역 중견 B2B 전문 컨퍼런스", "evidence": "상위 경쟁사 미커버(T2 미방어 세그먼트 탐지)",
      "uncovered_by": ["{{경쟁사 공개명}}"], "sources": [4], "source_tier": "T2" }
  ],
  "trends": [ { "label": "하이브리드 포맷 확산", "signal": "...", "sources": [4], "source_tier": "T2" } ],
  "sponsor_candidates": [ { "industry": "...", "company": "{{후보 공개명}}", "fit": "...", "sources": [5] } ],
  "policy_demand": [ { "item": "지원사업", "detail": "...", "sources": [6], "source_tier": "T1" } ],
  "benchmarks": [ { "event": "{{외부 벤치마크 행사}}", "takeaway": "...", "sources": [7] } ],
  "gaps": ["SAM 세그먼트 비율 [미확인]", "경쟁사 점유 [단일출처]"],
  "sources": [
    { "id": 0, "url": "...", "publisher": "통계청 KOSIS", "date": "2025", "accessed": "YYYY-MM-DD", "source_tier": "T1" }
  ]
}
```

- **`source_tier`**(T1~T4) = 출처 신뢰 등급(`source-tiering.md`). v1.1.0까지 `tier`였던 키를 개명했다 — 경쟁사 티어와 헷갈리지 않게. 하위호환: 수신 측은 `source_tier`가 없으면 `tier`를 같은 뜻으로 읽는다.
- **`competitor_tier`**(`direct`·`adjacent`·`aspirational`) = 경쟁 관계 티어(`competitive-analysis-method.md` 1단계).
- **`scores{}`** = 9차원 중 1~8차원 1~5점, **`tension_axes`** = 9차원 긴장축 양극 각각의 점수와 사분면. **단일 합산 점수는 싣지 않는다** — 수신 측도 평균 내지 않는다.
- **`whitespace_candidates[]`** = 미방어 세그먼트 *후보*와 근거. 우선순위·채택은 `jc-strategy-canvas`(F5) 판단이다.

- `sources[]`는 **인덱스 참조**(각 데이터의 `sources:[id]`가 가리킴) — 출처 추적성 보장.
- `source_tier`/`confidence`/`gaps`로 **근거 강도를 다운스트림에 전달**. 강도 낮은 데이터는 하류에서 단정 자제 신호.
- `scope.as_of`(조사 기준일)와 각 출처의 `date`(데이터 기준)·`accessed`(조회일)는 필수 — 하류 스킬이 수치의 시점을 알고 쓰게 한다.

## 3. 다운스트림 매핑

| → 대상 | 전달 핵심 | 대상 활용 |
|--------|----------|----------|
| `jc-strategy-canvas` | `market_size`·`competitors`(+`competitor_tier`·`scores`·`tension_axes`)·`whitespace_candidates`·`trends` | F2(5 Forces — `competitor_tier`로 기존경쟁 강도)·F5(포지셔닝 — `whitespace_candidates`로 타깃 세그먼트 후보)·F6(TAM/SAM/SOM) `[검증]` 근거 |
| `mice-rfp-analyzer` | `competitors`·`policy_demand` | 7축 중 경쟁·전략권고 사전 근거, `open_questions` 재조사 회신(4축 "추정" 보강) |
| `jc-pptx` | `market_size`·`trends`·`benchmarks`·`sponsor_candidates` | 제안서 배경·시장 논거 슬라이드, 스폰서 제안서·소개서의 후보·타깃 산업 |

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
                     └─(ChainPayload)─► jc-pptx            (시장 논거·스폰서 후보)
   (역방향) strategy-canvas/rfp-analyzer 의 open_questions ─► market-intel 재조사 아웃라인 시드(T4·T7 등) ─► 보낸 스킬로 회신
```
