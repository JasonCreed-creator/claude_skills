# ChainPayload/v1 — 스킬 간 데이터 전달 봉투 규약

스킬 A의 산출 데이터를 스킬 B가 재분석 없이 이어받기 위한 JSON 봉투. 봉투(헤더)는 여기서 정의하고, 페이로드 내용은 각 스킬의 `references/chaining-*.md`가 정의한다.

---

## 1. 봉투 구조

```json
{
  "$schema": "ChainPayload/v1",
  "source": "mice-rfp-analyzer",
  "version": "{{생산 스킬 SemVer — 해당 SKILL.md frontmatter에서 읽음}}",
  "generatedAt": "2026-10-05T10:00:00+09:00",
  "target": "jc-pptx",
  "clientId": "a-corp-2026",
  "projectTitle": "A사 고객 감사의 밤 2026",
  "...": "이하 스킬 고유 페이로드 (평탄 구조)"
}
```

봉투 필드와 페이로드 필드는 같은 최상위 객체에 평탄하게 공존한다. 봉투 필드명은 예약어이며 camelCase가 정본이다. `version`은 예시에 숫자를 박지 않는다 — 생산 스킬이 자기 frontmatter 값을 넣는다.

## 2. 공통 메타 필드

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `$schema` | string | ✅ | 항상 `"ChainPayload/v1"` |
| `source` | string | ✅ | 생산 스킬 ID (§3) |
| `version` | string | ✅ | 생산 스킬 SemVer |
| `generatedAt` | ISO 8601 | ✅ | 생성 시각(+09:00) |
| `target` | string | 선택 | 수신 스킬 힌트 (§3 enum 중 하나) |
| `clientId` | string \| null | 선택 | `client-overlays.md`의 발주처 슬롯 ID. null = 리멤버 기본 |
| `projectTitle` | string | 권장 | 행사·프로젝트명 |

## 3. source / target enum (라이브 스킬 기준, 2026-10-05)

| 단계 | 스킬 ID |
|------|---------|
| 리서치·전략 | `mice-market-intel` · `jc-strategy-canvas` · `mice-rfp-analyzer` · `mice-meeting-minutes` |
| 제안·견적·발표 | `jc-pptx` · `mice-estimate` · `pt-script` |
| 운영·현장 | `mice-run-of-show` · `mice-ops-docs` |
| 사후 | `mice-aftermath` |
| 팀 운영 | `mice-slack-ops` · `mice-team-board` |
| 검증 | `jc-redteam` (수신 전용, 임의 산출물 수용) |

### 3-1. 하위호환 별칭 (수신 측이 자동 치환, 새로 생산하지 않는다)

| 구 source | → 해석 | 비고 |
|-----------|--------|------|
| `mice-proposal` · `mice-sponsor-deck` | `jc-pptx` | 2026-09-21 jc-pptx로 흡수 |
| `mice-dashboard` | `mice-ops-docs` | KPI 대시보드는 mice-ops-docs |
| `jc-pptx(구 mice-proposal 별칭)` 류 괄호 표기 | 괄호 앞 ID | 문자열 정규화 |

## 4. 페이로드 정본 위치

| source | 정본 | 핵심 키 |
|--------|------|---------|
| mice-market-intel | `mice-market-intel/references/chaining-schema.md` | `market_size` `competitors` `trends` `sponsor_candidates` `gaps` `sources` |
| jc-strategy-canvas | `jc-strategy-canvas/references/chaining-schema.md` | `recommendation` `differentiation_axes` `key_messages` `evidence_flags` `open_questions` |
| mice-rfp-analyzer | `mice-rfp-analyzer/references/chaining-guide.md` | `rfp_meta` `requirements` `evaluation_focus` `differentiation_points` `proposal_structure_hint` |
| mice-meeting-minutes | `mice-meeting-minutes/references/chaining-guide.md` | `client` `project_context` `discovery_data` `strategic_notes` |
| jc-pptx | `jc-pptx/references/proposal-playbook.md §체이닝` | `deck_meta` `sections` `coverage_map` `estimate_hint` `presentation` |
| mice-estimate | `mice-estimate/references/chaining-schema.md` | `eventScale` `venue` `options` `sections` `totalAmount` |
| pt-script | `pt-script/references/chaining-schema.md` | `proposal_meta` (발표 세그먼트 시간) |
| mice-run-of-show | `mice-run-of-show/references/chaining-schema.md` | `plan` (`startTime` `endTime` `cues`) |
| mice-ops-docs | `mice-ops-docs/references/chaining-schema.md` | `kpis` `insights` `actualSpending` `rounds` |
| mice-aftermath | `mice-aftermath/references/chaining-schema.md` | `event` `performance` `cases` `lessons` `next` |
| mice-slack-ops | `mice-slack-ops/references/contract-message.md §6` | `contract` (계약완료 메시지 파싱 결과) |
| mice-team-board | `mice-team-board/references/sheet-schema.md` | 수신 전용 — `contract` → 프로젝트 탭 행 |
| jc-redteam | 스키마 없음 | 임의 산출물 수용 |

## 5. 체이닝 흐름 (실사용 경로)

```
[주제·시장 질문] → mice-market-intel ──→ jc-strategy-canvas ──→ jc-pptx / mice-rfp-analyzer
[RFP·추진계획] → mice-rfp-analyzer ──→ jc-pptx(제안서) ──→ mice-estimate(견적) ──→ pt-script(PT 대본)
[회의 메모]   → mice-meeting-minutes ──→ jc-strategy-canvas / jc-pptx / mice-ops-docs(운영계획서)
[수주 후]     → jc-pptx·pt-script ──→ mice-run-of-show(큐시트) ──→ mice-ops-docs(계획 대비 실제)
[행사 종료]   → mice-ops-docs·mice-estimate·mice-run-of-show ──→ mice-aftermath(결과보고) ──→ jc-pptx(레퍼런스 슬라이드)
[Slack 계약완료 메시지] → mice-slack-ops ──→ mice-team-board(행 등록, 시트 쓰기는 승인 후)
모든 산출물 ──→ jc-redteam
```

## 6. 수신 규칙

### 6-1. 판별
`$schema`가 `ChainPayload/v1`이 아니면 체이닝 입력으로 취급하지 않는다(파일·텍스트·대화 입력으로 처리).

### 6-2. 무변경 승계
`source`로 페이로드 정본(§4)을 찾아 필드를 해석한다. 모르는 필드는 무시하고 경고만. 봉투에 있는 팩트(금액·일정·규모)를 재분석하거나 임의로 바꾸지 않는다. 보정이 필요하면 사유를 남기고, 충돌 시 봉투 값 + 사용자 확인.

### 6-3. 발주처 슬롯
`clientId`가 있으면 `client-overlays.md` 슬롯을 그대로 승계한다. 실명 하드코딩 금지(`shared-rules.md#RULE-NO-COMPANY`).

### 6-4. 저장 위치
`.chaining/[project_or_topic]_[YYYYMMDD]_to_[target].json`. `target`이 없으면 `_to_any`.

## 7. source 판별 (detect_input_source)

```python
ALIASES = {"mice-proposal": "jc-pptx", "mice-sponsor-deck": "jc-pptx", "mice-dashboard": "mice-ops-docs"}  # 폐합 source 별칭(§3-1)

def detect_input_source(payload: dict) -> str | None:
    if payload.get("$schema") != "ChainPayload/v1":
        return None
    src = str(payload.get("source", "")).split("(")[0].strip()
    return ALIASES.get(src, src) or None
```

반환값이 §3 enum에 없으면 경고 후 범용 입력으로 처리한다.

## 8. 변경 이력

- **v2.1.0 (2026-10-05)** — enum을 라이브 스킬 기준으로 재작성: `mice-run-of-show`·`mice-aftermath`를 라이브로 복구(v2.0.0의 "폐지" 표기 오류 정정), `jc-strategy-canvas`·`mice-market-intel`·`mice-ops-docs`·`mice-team-board` 등록. 폐합 source는 별칭 표로. §6 절 번호(6-1~6-4)·§7 판별 함수 명시(소비 스킬 참조 정합). 예시 버전 하드코딩·고객사 실명 제거.
- v2.0.0 (2026-09-21) — 라이브 스킬 8종으로 enum 정리, `projectTitle` 권장 필드.
- v1.x (2026-05~07) — 봉투 규약 신설, camelCase 정본화(이력은 git).
