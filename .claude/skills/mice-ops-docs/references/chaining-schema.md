# 체이닝 스키마 — mice-ops-docs

봉투는 `jc-design-system/references/chaining-protocol.md`(ChainPayload/v1) 정본. 여기서는 본 스킬의 고유 페이로드만 정한다. `version`은 생산 스킬의 현재 SemVer를 넣는다(예시 값 복사 금지).

---

## 1. 입력

| source | 받는 키 | 쓰는 곳 |
|--------|---------|---------|
| `mice-run-of-show` | `plan.cues[]`(`cueNo`·`clock`·`segment`·`durationMin`·`owner`) · `eventDate` | 운영계획서 3섹션 · 지연 KPI |
| `mice-meeting-minutes` | `client` · `project_context` · `strategic_notes` · Action | 운영계획서 1·2·7섹션 |
| `mice-estimate` | `totalAmount` · `sections` | 예산 집행률(계획측) |
| `mice-slack-ops` | `contract` | 행사 개요 · 모객 목표 |

실측 진행 시각은 페이로드가 아니라 사용자 입력(현장 리포트·무전 기록)으로 받는다.

```json
{ "actual": [ { "cueNo": "C01", "start": "09:04", "end": "09:36" } ] }
```

## 2. 출력

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-ops-docs",
  "version": "<현재 버전>",
  "generatedAt": "2026-10-20T18:00:00+09:00",
  "target": "mice-aftermath",
  "projectTitle": "{{행사명}}",
  "kpis": [
    { "id": "showup", "label": "쇼업", "unit": "명", "target": 300, "actual": 284, "rate": 0.947 }
  ],
  "insights": ["오후 세션 착석률 61% — 네트워킹 동선이 세션장과 멀었음(현장 리포트)"],
  "actualSpending": { "planned": null, "actual": null, "note": "[미확보]" },
  "rounds": [ { "cueNo": "C05", "segment": "기조연설", "delayMin": 7, "overMin": 4 } ],
  "dashboardFile": "대시보드_{{행사ID}}.html"
}
```

- `kpis[].target`이 없으면 `null`, `rate`도 `null`.
- `rounds`는 `scripts/plan_vs_actual.py --json` 출력 그대로.
