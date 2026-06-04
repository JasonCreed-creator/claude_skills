# 프리셋 → jc 스킬 개조 플레이북

기본 제공(프리셋) 스킬 1종을 jc 생태계 스킬로 개조할 때 따르는 **반복 가능한 변환 절차**다. `web-artifacts-builder → jc-artifact-builder`, `remember-landing-page → jc-landing-page` 에서 검증된 패턴을 정본화한 것. 진행 추적은 [`preset-optimization-roadmap.md`](preset-optimization-roadmap.md).

## 0. 개조 전 판별 (3분류)

| 분류 | 판단 기준 | 처리 |
|------|----------|------|
| **개조(adapt)** | 기능이 MICE 워크플로우에 유효하고, 생태계와 충돌하지 않거나 길들일 수 있음 | 아래 §1~§8 전체 적용 |
| **경량개조(light)** | 기능은 보존하되 jc 색·디자인 의존이 약함(예: 코드 인프라) | §1·§2·§6·§8만 |
| **흡수/폐합(merge)** | 기존 스킬과 중복 | 기능을 기존 스킬로 이관, 폐합 사유를 커밋·로드맵에 기록 |

## 1. 명명 & 구조

- 디렉터리·frontmatter `name` 모두 `jc-<도메인>`(소문자·하이픈)으로 일치.
- 표준 레이아웃:
  ```
  jc-<name>/
  ├─ SKILL.md          # 진입점 (<500줄, 스캔 가능)
  ├─ references/       # 상세 문서(.md) — 필요 시 로드
  ├─ scripts/          # 결정적·반복 작업(.py) — 매 호출 재발명 방지
  └─ assets/           # 템플릿(.html/.xlsx 등)
  ```
- 형제 스킬이 쓰는 곳에는 `license: Complete terms in LICENSE.txt` 라인을 맞춘다.

## 2. Frontmatter (트리거의 핵심)

- `description`은 **한국어 우선 + 푸시형**. Claude는 스킬을 *덜* 트리거하는 경향이 있으므로, 무엇을 하는지 + **언제 써야 하는지(키워드·맥락)** + **언제 쓰면 안 되는지(형제 스킬 경계)**를 모두 description에 담는다(본문 말고).
- 형제 description의 톤·길이·"다음 상황에서 반드시 이 스킬을 사용할 것 …" 패턴을 따른다.
- `version`: SemVer, 신규는 `v1.0.0`.

## 3. SoT 앵커링 (값 미러링 금지)

- 색·타이포·사이즈·간격 **값을 본문/코드에 박지 않는다.** 빌드 시 `jc-design-system`에서 읽는다:
  - 토큰: `references/signature-tokens.md §6 JSON` (구현체 `scripts/jc_tokens.py`의 `load_tokens`/`color`).
  - 라이트/다크·인쇄: `references/mode-mapping.md` (§3 매핑, §4.2 인쇄 라이트 강제, §9 WCAG 계산).
  - 클라이언트 차별화: `references/client-overlays.md` (primary/accent/logo 3토큰만, 충돌 회피 §6).
- 형제 경로로 SoT 탐색: `Path(__file__).resolve().parents[2] / "jc-design-system"`.
- 미러가 불가피하면 출처(`§6`)를 주석에 남기고, `scripts/check_drift.py`의 FORBIDDEN 값은 절대 쓰지 않는다.

## 4. 홈베이스 원칙 (자유는 명시적 opt-in)

프리셋이 "임의 테마/임의 팔레트/대체 브랜드/예술적 자유"를 silent default로 둔다면, jc 시그니처를 기본값으로 **뒤집고** 자유는 이름 붙은 옵션으로 노출한다.

- 디자인 산출물(제안서·대시보드·데크·문서): 시그니처 **고정**. 차별화는 오버레이 3토큰만.
- 폰트는 어떤 경우에도 시그니처 고정(Pretendard/Inter/JetBrains Mono) — 오버레이 대상 아님.
- 아트 오브젝트(캔버스/제너러티브): jc 팔레트·jc 브랜딩 크롬이 기본, "free art 모드"는 사용자가 명시할 때만.

## 5. 공통 룰 참조 (값 재정의 금지)

본문엔 짧은 인라인 리마인더만, 근거는 `jc-design-system/references/shared-rules.md#<RULE-ID>`로 위임:

- `RULE-WCAG` — 본문 4.5:1↑(계산 표준 `mode-mapping.md §9`).
- `RULE-PRINT-LIGHT` — 다크 HTML도 인쇄 시 라이트 강제.
- `RULE-NO-COMPANY` — 회사·실명·부서 하드코딩 금지, 외부 주입 변수만(`{{client_company}}`·`{{author_name}}`·`{{personal_brand}}`·`{{author_title}}`·`{{company_name}}`).
- `RULE-PPTX-HEX` — pptxgenjs/python-pptx 계열엔 `#` 없는 6자리(HTML/CSS는 `#` 포함). PPTX 산출 스킬만.

## 6. 생태계 연결 (재발명 금지)

- **검증**: 산출물 최종 점검은 `jc-redteam`(결론·문서=3축, LP=마케팅 패널). 프리셋이 자체 "fresh Claude로 리더 테스트"를 시키면 그 자리에 jc-redteam을 끼운다.
- **데이터 입출력**: 다른 mice-* 산출 JSON 소비/배출은 `chaining-protocol.md`의 `ChainPayload/v1` 봉투.
- **디자인**: §3 그대로.

## 7. 진행형 디스클로저 & 스크립트 번들

- SKILL.md는 워크플로우·판단 위주(<500줄). 토큰표·긴 절차·매체별 디테일은 `references/`로.
- 매 호출마다 같은 헬퍼를 새로 짤 징후가 보이면 `scripts/`에 한 번 만들어 번들(예: 쇼케이스 생성기·검증기).

## 8. 마감 체크리스트

- [ ] `name`(디렉터리=frontmatter) `jc-*` 일치, `version` 설정
- [ ] description 한국어·푸시형 + 형제 경계 명시
- [ ] 토큰 값 하드코딩 0건(SoT 런타임 참조), FORBIDDEN 값 0건
- [ ] 홈베이스 원칙 적용(자유는 명시 opt-in)
- [ ] `#RULE-*` 인라인 리마인더 + 정본 링크
- [ ] 회사·개인정보 하드코딩 0건(외부 주입 변수)
- [ ] 가능한 생태계 연결(jc-redteam / ChainPayload / jc-design-system) 명시
- [ ] (디자인/소비 스킬이면) `check_drift.py` CONSUMERS 등록 검토
- [ ] 로드맵 트래커 상태 갱신 + 커밋 `<스킬명>: <요약>`
