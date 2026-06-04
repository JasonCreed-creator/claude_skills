# Mint Overlay — 신규 클라이언트 오버레이 발행

원본 Theme Factory의 "Create your Own Theme"에 대응한다. 단, 자유로운 새 테마를 만드는 게 아니라 **시그니처 위에 얹는 3토큰 오버레이**를 만드는 것이다. 시그니처(폰트·사이즈·간격·텍스트/배경)는 절대 건드리지 않는다.

> 등록 포맷·충돌 규칙의 정본은 `jc-design-system/references/client-overlays.md`(§2 스키마, §5 추가 절차, §6 충돌 회피). 본 문서는 그 절차를 발행 워크플로우로 운용하는 방법이다.

## 발행 절차 (5단계)

### 1. 입력 수집

사용자에게 받는다(추측 금지):

- **client_id**: 영문 소문자·하이픈 (예: `acme`, `t-社`)
- **client_name**: 표기용 정식 명칭 — 단, 산출물에는 외부 주입 변수(`{{client_company}}`)로 들어가며 스킬·문서에 **하드코딩하지 않는다**(`RULE-NO-COMPANY`)
- **track**: `A`(소속사) / `B`(독립) / `personal`
- **브랜드 컬러 또는 톤**: CI 가이드의 HEX가 있으면 그대로, 없으면 분위기(신뢰/보안/활성/성장)만 받아 `overlay-catalog.md`의 톤 매핑으로 후보 제시
- **logo**: 파일(있으면 `assets/clients/{client_id}.png`로 배치, 없으면 텍스트명만)

### 2. 3토큰으로 축소

받은 정보를 오버레이 가능한 3토큰으로만 매핑한다.

| 받은 것 | → 오버레이 토큰 | 규칙 |
|---------|----------------|------|
| 헤더·표지·로고 영역 색 | `primary` | 시그니처 Deep Navy와 근접하면 `null`(시그니처 유지) |
| 강조·CTA·KPI 색 | `accent` | Point Pool 4종 중 가장 가까운 색으로 통합 권장 |
| 로고 | `logo_path` | 없으면 `null` |
| 폰트·사이즈·간격·본문색 | (없음) | **오버레이 불가 — 시그니처 고정** |

CI 컬러가 Point Pool 밖이면, 풀 안에서 가장 가까운 색으로 흡수하거나(아래 검증의 ΔE 규칙) 시그니처 유지 + 로고만 적용을 권한다. 임의 신색을 만들지 않는다.

### 3. 자동 검증 (`scripts/validate_overlay.py`)

```bash
python3 scripts/validate_overlay.py --primary "#0A2540" --accent "#7C3AED" --print
```

검증 항목:

1. **3토큰 한정** — primary/accent/logo 외 입력 거부.
2. **WCAG 대비** (`RULE-WCAG`, 계산 `mode-mapping.md §9.1`):
   - 흰 텍스트 on `primary` ≥ 4.5:1 (헤더 풀블리드에 흰 글씨가 얹히므로)
   - 흰 텍스트 on `accent` ≥ 3.0:1 (큰 텍스트/버튼) — 본문 라벨로 쓸 거면 4.5:1
3. **색충돌 회피** (`client-overlays.md §6`):
   - primary가 Deep Navy(`#0A2540`)와 채도 차 30% 이내 → 시그니처 유지 권고
   - accent가 Point Pool 4종 중 하나와 ΔE(CIE76) < 5 → 그 포인트로 통합 권고
   - `--print` 지정 시 형광·네온 계열 accent는 인쇄용 채도 −20% 권고
4. **다크 모드 가독성** — accent를 `mode-mapping.md §3` 규칙으로 밝힌 값이 다크 배경(`#0A1220`)에서 충분한지 점검.

검증은 **차단이 아니라 권고** 위주다(Critical=WCAG 실패만 차단). 경고는 사용자에게 보여주고 결정을 받는다.

### 4. 리뷰

검증 통과안을 사용자에게 보여준다 — primary/accent 스와치, 흰 텍스트 대비비, 통합/유지 권고, 다크 변형. `build_showcase.py --preview-overlay`로 그 오버레이 카드만 미리 렌더해 확인시킨다. 사용자 OK 전까지 등록하지 않는다.

### 5. SoT 등록

승인되면 `jc-design-system/references/client-overlays.md`에 `## 3.X {client_name}` 섹션을 추가하고 스키마 JSON 블록을 기록한다:

```json
{
  "client_id": "acme",
  "client_name": "{{client_company}}",
  "track": "B",
  "overrides": {
    "primary": "#0A2540 | null",
    "accent": "#XXXXXX | null",
    "logo_path": "assets/clients/acme.png | null"
  },
  "notes": "사용 컨텍스트 메모"
}
```

등록 후 `overlay-catalog.md` 표에도 한 줄 추가하고, `build_showcase.py`를 다시 돌려 쇼케이스를 갱신한다. 이후 모든 산출물 스킬이 `client_id`로 이 오버레이를 호출할 수 있다.

## 안티패턴 (하지 말 것)

- ❌ 폰트쌍 바꾸기 — 시그니처 고정. 원본 Theme Factory의 폰트 선택 기능은 jc에서 폐기.
- ❌ text/bg/surface/border 색 오버레이 — 3토큰 밖.
- ❌ CI 미확인 상태에서 색 추측 — 시그니처 유지 + 로고만.
- ❌ Point Pool 밖 임의색 신설 — 가까운 풀 색으로 흡수.
- ❌ client_name·로고를 스킬/스크립트에 하드코딩 — 외부 주입 변수로.
