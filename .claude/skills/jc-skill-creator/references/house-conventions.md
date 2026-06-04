# House Conventions — jc 스킬 불변식 상세

모든 jc 스킬이 지키는 규칙의 상세·근거·템플릿. 요지는 SKILL.md, 개조 전용 절차는 `docs/preset-adaptation-playbook.md`.

## 디렉터리 표준

```
jc-<도메인>/
├─ SKILL.md          # 진입점 (<500줄). 워크플로우·판단 위주
├─ references/       # 상세 문서(.md). >300줄이면 목차
├─ scripts/          # 결정적·반복 작업(.py). stdlib 우선, 동작 검증 필수
└─ assets/           # 템플릿(.html/.xlsx/.ttf 등) — 산출에 직접 쓰는 파일
```

## frontmatter 템플릿

```yaml
---
name: jc-<도메인>            # 디렉터리명과 정확히 일치
description: <한국어·푸시형>  # 무엇을 + 언제 트리거(키워드·맥락) + 형제 경계(언제 쓰지 말지)
version: "v1.0.0"           # SemVer. 수정 시 범프
license: Complete terms in LICENSE.txt
---
```

### description 작성 규칙 (트리거의 전부)

- **무엇을**: 스킬이 만드는 산출물·하는 일 한 문장.
- **언제(키워드·맥락)**: "다음 상황에서 반드시 이 스킬을 사용할 것 …" + 사용자가 실제 칠 법한 한국어 표현·동의어를 폭넓게. Claude는 스킬을 *덜* 트리거하므로 약간 푸시하게.
- **언제 쓰지 말지(형제 경계)**: 인접 jc 스킬과의 경계를 명시(예: "검증은 jc-redteam, 디자인 토큰은 jc-design-system"). 오트리거 방지.
- 본문(SKILL.md body)에 'when to use'를 넣지 말 것 — 전부 description에.

## 불변식 상세

### 1. SoT 앵커 (토큰 값 미러 금지)
- 색·타이포·사이즈·간격 값을 본문/코드에 박지 않는다. `jc-design-system`에서 런타임 로드.
- 코드: 형제 경로 `Path(__file__).resolve().parents[2] / "jc-design-system"` → `scripts/jc_tokens.py`의 `load_tokens`/`color`.
- 라이트/다크·인쇄·WCAG 계산은 `mode-mapping.md`(§3·§4.2·§9). 클라이언트 차별화는 `client-overlays.md`(3토큰).
- 부득이한 미러는 출처(`§6`/`§3`)를 주석에. `scripts/check_drift.py` FORBIDDEN 값 금지.

### 2. 홈베이스 원칙
- jc 시그니처가 기본값. 임의 팔레트·대체 브랜드·아트 자유는 이름 붙은 opt-in으로만.
- 폰트는 시그니처 고정(Pretendard/Inter/JetBrains Mono) — 디자인 산출물에서 오버레이 대상 아님.

### 3. 공통 룰 참조 (값 재정의 금지)
- 인라인 리마인더만 + `jc-design-system/references/shared-rules.md#<RULE-ID>` 링크.
- `RULE-WCAG`(본문 4.5:1↑) · `RULE-PRINT-LIGHT`(다크 HTML 인쇄 라이트) · `RULE-NO-COMPANY`(식별정보 외부 주입) · `RULE-PPTX-HEX`(python-pptx/pptxgenjs는 # 없는 6자리).

### 4. 회사·개인정보 금지
- 회사명·실명·부서·발주처 하드코딩 0건. 외부 주입 변수: `{{client_company}}`·`{{author_name}}`·`{{personal_brand}}`·`{{author_title}}`·`{{company_name}}` + 스킬별 슬롯.

### 5. 생태계 연결 (재발명 금지)
- 검증 → `jc-redteam`(결론·문서=3축, LP=마케팅 패널). 프리셋의 자체 "fresh Claude 리더 테스트"는 jc-redteam으로 치환.
- 데이터 입출력 → `ChainPayload/v1`(`chaining-protocol.md`).
- 디자인 → `jc-design-system`.

## 자가점검 (마감)

- [ ] name 일치·version·license
- [ ] description 한국어·푸시형 + 형제 경계
- [ ] 토큰 하드코딩 0건(SoT 참조), FORBIDDEN 0건
- [ ] 홈베이스 원칙(자유=opt-in)
- [ ] `#RULE-*` 인라인 + 링크
- [ ] 식별정보 외부 주입
- [ ] 생태계 연결 명시
- [ ] SKILL.md <500줄, 반복작업 scripts/ 번들
- [ ] (디자인/소비 스킬) `check_drift.py` 정합 + CONSUMERS 등록 검토
