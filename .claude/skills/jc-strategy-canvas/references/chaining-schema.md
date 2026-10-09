# 체이닝 스키마 — jc-strategy-canvas

`jc-strategy-canvas`의 입력/출력 `ChainPayload` 매핑 정본. 봉투(envelope) 구조는 **정본 `jc-design-system/references/chaining-protocol.md`(ChainPayload/v1)** 를 따른다. 본 문서는 *본 스킬 고유 페이로드*만 정의한다.

> 봉투 공통 필드(chaining-protocol §1·§2): `$schema:"ChainPayload/v1"` · `source` · `version` · `generatedAt` · (`target`) · (`clientId`) · (`projectTitle`). 페이로드는 봉투와 **같은 최상위에 평탄(flat)하게** 공존.

---

## 1. 입력 (소비) — 본 스킬이 받는 것

`detect_input_source()`(chaining-protocol §7)로 `source`를 판별해 분기한다(폐합 source 별칭 자동 치환, §3-1). 모르는 필드는 무시하고 경고만.

### 1-1. ← mice-market-intel
시장·경쟁 리서치 데이터를 프레임워크 `[검증]` 근거로 흡수.

| 받는 키(예) | 매핑 대상 |
|------------|----------|
| `market_size` (tam/sam/som, 출처) | F6 TAM/SAM/SOM 직접 채움 + 출처 각주 |
| `competitors[]` (이름·점유·강약) | F2 기존경쟁/신규진입, F5 경쟁 대안 |
| `competitors[].competitor_tier` (direct/adjacent/aspirational) | F2 기존경쟁 강도 — direct=정면 경쟁 강도, adjacent=인접·신규진입 압박, aspirational=목표 기준선(경쟁 강도에 넣지 않고 F5 참조점으로) |
| `competitors[].scores{}`·`tension_axes` | F5 경쟁 대안 비교 축·긴장축 2×2 근거(데이터 맵 — 포지셔닝 결정은 본 스킬 F5) |
| `whitespace_candidates[]` | F5 타깃 세그먼트·차별화 축 *후보* — 우선순위·채택 판단은 본 스킬 ③~④ |
| `trends[]` / `demand_signals` | F2 대체재, F4 pain/gain |
| `sources[]` (URL·일자) + 각 데이터의 `source_tier`(T1~T4, 구 `tier`) | 각 칸 `[검증]` 표식 근거 — T3·T4 단독이면 `[가설]`로 낮춘다 |

### 1-2. ← mice-meeting-minutes
Discovery/협의 회의록에서 고객 니즈·결정 흡수.

| 받는 키(예) | 매핑 대상 |
|------------|----------|
| `discovery_data` (니즈·목표·KPI) | ① 인테이크, F4 JTBD(기능/감정 job) |
| `project_context` (예산·일정·이해관계자) | F1 C$/R$ 제약, F3 약점/위협 |
| `strategic_notes` | F3 SWOT 시드 |

### 1-3. ← mice-aftermath
자사 수행실적 케이스(R3)를 *내부 실적 근거*로 흡수. 외부 시장 데이터가 아니라 자사 증거이므로 F3·F5의 자사 측 칸에만 쓴다.

| 받는 키(예) | 매핑 대상 |
|------------|----------|
| `cases[]` (`reuse_tier`에 R3, `result`·`proof`) | F3 강점(S)·F5 차별화 축의 `[검증]` 근거(proof 병기) |
| `performance` (`kpis`·`budget`) | F6 SOM 현실 점유 근거, F1 비용구조(C$) 실적치 |

- `anonymize` 플래그를 존중한다 — 외부 공유용 캔버스에서는 발주처를 가명 처리.

> 봉투가 없거나 `$schema≠ChainPayload/v1`이면 체이닝 입력이 아니라 파일/텍스트/대화 입력으로 처리한다. 받은 페이로드는 임의 변경하지 않고, 보정이 필요하면 사유를 남긴다(chaining-protocol §6-2 무변경 승계).

---

## 2. 출력 (배출) — 본 스킬이 내보내는 것

전략 캔버스 확정 후, 다운스트림으로 전략 논거를 전달.

```json
{
  "$schema": "ChainPayload/v1",
  "source": "jc-strategy-canvas",
  "version": "<SKILL.md frontmatter version>",
  "generatedAt": "2026-06-04T10:00:00+09:00",
  "target": "jc-pptx",
  "clientId": null,
  "projectTitle": "{{project_or_topic}}",

  "topic": "{{project_or_topic}}",
  "decision": "신규 분야 진입 GO/NO-GO",
  "frameworks_used": ["F6", "F2", "F3", "F1"],
  "recommendation": {
    "headline": "조건부 GO — SOM 손익분기 충족 시",
    "options": [
      { "name": "공격", "premise": "...", "risks": ["..."], "resources": ["..."] },
      { "name": "관망", "premise": "...", "risks": ["..."], "resources": ["..."] }
    ]
  },
  "differentiation_axes": ["운영 데이터 IP", "발주처 네트워크"],
  "key_messages": ["...", "..."],
  "evidence_flags": { "verified": 12, "hypothesis": 5, "estimate": 3 },
  "open_questions": ["SAM 세그먼트 비율 미검증 → market-intel 재의뢰"]
}
```

### 2-1. → jc-pptx
`recommendation`·`differentiation_axes`·`key_messages`를 제안서·소개서의 전략 논거·핵심 메시지로 사용. (덱 쪽 매핑은 `jc-pptx/references/proposal-playbook.md` 권위.)

### 2-2. → mice-rfp-analyzer
자사 전략 캔버스를 비딩 *전략권고 축*의 사전 입력으로. `recommendation.options`·`differentiation_axes`를 7축 중 전략권고·경쟁 축에 주입.

---

## 3. 표준 규약 (chaining-protocol 준수)

- 저장 위치: `.chaining/[project_or_topic]_[YYYYMMDD]_to_[target].json` (chaining-protocol §6-4).
- `version`은 SKILL.md frontmatter 현재 값을 그대로 쓴다(예시에 고정 버전을 적지 않는다).
- `source: jc-strategy-canvas`는 chaining-protocol §3 enum(리서치·전략 단계)에 등재돼 있고, 페이로드 정본 위치는 §4 표가 이 문서를 가리킨다.
- `evidence_flags`는 캔버스의 `[검증]/[가설]/[추정]` 집계 — 다운스트림이 *근거 강도*를 알고 쓰게 한다. **`[가설]/[추정]` 비중이 높은 권고는 제안서(jc-pptx)에서 단정 표현 자제** 신호.
- `open_questions`는 미검증 항목 — `mice-market-intel` 재의뢰 트리거.
- 리멤버 명의 기본, 회사·실명 하드코딩 금지(`RULE-NO-COMPANY`) — `{{변수}}` 슬롯 + `clientId` 슬롯만.

## 4. 체이닝 흐름 요약

```
mice-market-intel ─(시장·경쟁 데이터)─┐
mice-meeting-minutes ─(Discovery)────┤
mice-aftermath ─(자사 실적 R3)────────┼─► jc-strategy-canvas ─► 전략 캔버스(HTML)
                                      │         │
                                      │         ├─(ChainPayload)─► jc-pptx (전략 논거)
                                      │         └─(ChainPayload)─► mice-rfp-analyzer (전략권고 축)
                                      │         ↓
                                      └─────── jc-redteam (전략 결론 적대 검증, ⑤)
```
