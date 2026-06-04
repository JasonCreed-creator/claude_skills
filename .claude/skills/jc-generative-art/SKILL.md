---
name: jc-generative-art
description: 알고리즘 철학(.md)을 세우고 그것을 시드 재현 가능한 p5.js 제너러티브 아트(.html 단일 아티팩트)로 표현하는 코드 아트 스킬. 흐름 필드·파티클·노이즈장·재귀·결정화 등 살아 있는 알고리즘으로 생성하며, 시드 탐색(prev/next/random/jump)·파라미터 슬라이더·Regenerate/Reset/Download PNG UX를 단일 자가완결 HTML로 제공한다. 다음 상황에서 반드시 이 스킬을 사용할 것 사용자가 '제너러티브 아트', '생성 아트', 'generative art', 'p5.js', '플로우 필드', 'flow field', '파티클', 'particle system', '코드 아트', 'creative coding', '모션 배경', '시드 아트', 'seed art', '알고리즘 아트'를 언급할 때. MICE 행사의 모션 배경·데이터 아트·컨퍼런스 비주얼·데크 배경을 코드로 생성해달라고 할 때. **기본 룩은 jc 시그니처 한 가족** — 아트 팔레트는 jc data 시리즈(signature-tokens.md §1.4), 뷰어 UI는 Pretendard·Deep Navy·Electric Blue·라이트 기본. **임의/자유 팔레트는 사용자가 '자유 팔레트 모드'/'free art'를 명시할 때만**. 형제 경계 — 정적 캔버스 아트(.pdf/.png 포스터·키비주얼·무드보드)는 jc-visual-philosophy, 상태관리·라우팅 있는 인터랙티브 *앱*(React)은 jc-artifact-builder, 데이터 KPI·차트 대시보드는 mice-dashboard 영역. 본 스킬은 *p5.js 제너러티브/코드 아트* 전용이다. 디자인 토큰 정의·조회는 jc-design-system, 산출물에 테마/오버레이 입히기는 jc-theme-factory. 기존 아티스트 작품 모사 금지(저작권).
version: "v1.0.0"
license: Complete terms in LICENSE.txt
---

# JC Generative Art

알고리즘 철학을 세우고 그것을 **시드 재현 가능한 p5.js 제너러티브 아트**로 표현한다. 원본 프리셋 `algorithmic-art`(p5.js 제너러티브 아트)를 jc 생태계용으로 개조한 버전이다.

원본은 뷰어 UI를 **Anthropic 브랜딩**(Poppins/Lora·`#d97757`·그라디언트)으로 박아두고, 아트 팔레트를 *임의*로 두었다. 본 스킬은 [개조 플레이북 §4 홈베이스 원칙](../../../docs/preset-adaptation-playbook.md)을 적용해 둘을 뒤집는다:

> 뷰어 크롬은 **jc 시그니처 고정**(Pretendard·Deep Navy·Electric Blue·라이트 기본), 아트 팔레트 기본은 **jc data 시리즈**. 색의 자유(자유 팔레트 모드)는 사용자가 *명시할 때만* opt-in.

원본의 **생성 철학·시드 재현성·파라미터 탐색 UX는 그대로 살린다.** 바뀐 건 브랜딩과 기본 팔레트뿐이다.

## 무엇을 만드나 (산출물)

생성은 **두 단계**다:

1. **알고리즘 철학 (.md)** — 어떤 계산적 미학을 추구하는지 4~6문단 선언.
2. **p5.js 제너러티브 아트 (.html 단일 아티팩트)** — 그 철학을 코드로 표현. p5.js만 CDN, 나머지(알고리즘·파라미터·UI) 전부 인라인. claude.ai 아티팩트나 어떤 브라우저에서도 즉시 동작.

> 단일 자가완결 HTML 원칙: 외부 파일·임포트 없음(p5.js CDN 예외). 별도 `.js`를 만들지 말고 알고리즘을 HTML에 **인라인 임베드**한다.

## MICE 용도

- **행사 모션 배경** — 컨퍼런스 인트로/로비 스크린의 살아 있는 흐름장.
- **데이터 아트** — 참가자/세션 데이터의 미적 추상화(설명 차트는 mice-dashboard).
- **컨퍼런스 비주얼** — 키노트 백드롭·세션 전환 비주얼.
- **데크 배경** — 제안서·스폰서 데크 표지의 제너러티브 텍스처.

## 워크플로우

### 1단계 — 알고리즘 철학 (.md)

계산적 미학 선언을 4~6문단으로 쓴다. 정적 이미지가 아니라 **살아 있는 알고리즘의 세계관**을 정의한다:

- **무브먼트 명명**(1~2단어): "Organic Turbulence" / "Quantum Harmonics" / "Emergent Stillness".
- **철학 서술**: 계산 과정·노이즈/랜덤 패턴·파티클 행동·장 역학·시간적 진화·창발적 복잡성을 통해 어떻게 발현되는지.
- **크래프트맨십 강조**: 최종 알고리즘이 "수많은 반복으로 정교하게 빚은, 그 분야 최정상의 산물"처럼 느껴져야 함을 반복해 강조.
- **창작 여지**: 방향은 구체적으로, 구현 디테일은 다음 단계의 고급 해석 여지를 남긴다.

> 핵심: 아름다움은 **결과 프레임이 아니라 과정(process)**에 산다. 각 실행(시드)은 고유하다.

#### 개념적 씨앗 추론

구현 전에, 사용자 요청에서 **미묘하고 세련된 개념적 실**을 뽑아 알고리즘 *안에* 짜 넣는다. 아는 사람은 직관적으로 느끼고, 모르는 사람은 그냥 훌륭한 제너러티브 작품을 경험한다. 재즈 연주자가 다른 곡을 화성으로 인용하듯 — 드러내지 않되 깊이를 더한다.

### 2단계 — p5.js 구현 (.html)

#### STEP 0: 템플릿 먼저 읽기 (필수)

HTML을 쓰기 **전에** 반드시:

1. `templates/viewer.html`을 **Read** 도구로 읽는다.
2. 구조·jc 브랜딩(Pretendard·Deep Navy·Electric Blue·라이트 기본)·시드 컨트롤·액션 버튼을 파악한다.
3. 그 파일을 **문자 그대로 시작점**으로 쓴다(영감이 아니라 출발점).
4. **FIXED 섹션은 그대로 유지**: 네이비 헤더, 사이드바 구조, jc 색·폰트, Seed(prev/next/random/jump), Actions(Regenerate/Reset/Download PNG).
5. **VARIABLE 섹션만 교체**: p5.js 알고리즘, params 객체, Parameters 슬라이더, Colors(선택).

구조·원칙 참고서는 `templates/generator_reference.js`(아티팩트엔 포함하지 않음 — 인라인 임베드).

피할 것: ❌ HTML 맨땅 작성 ❌ 커스텀 색 체계 발명 ❌ Anthropic 프리셋 색(`#d97757`·`#6a9bcc`·`#788c5d`·`#141413`·`#faf9f5`)·Poppins/Lora ❌ 사이드바 구조 변경 ❌ 예시 흐름 필드를 그대로 베끼기.

#### 시드 재현성 (Art Blocks 패턴)

```javascript
randomSeed(params.seed);   // 항상 시드 고정
noiseSeed(params.seed);    // 같은 시드 = 항상 동일 결과
```

#### 파라미터 구조 — 철학에서 자연 도출

"이 시스템에서 조절 가능한 성질은?"을 묻는다 — 수량·스케일·확률·비율·각도·임계값. "패턴 종류"가 아니라 "튜닝 가능한 속성"으로 사고한다.

```javascript
let params = {
  seed: 12345,                                   // 항상 포함
  // jc data 시리즈 (signature-tokens.md §1.4)
  colorPalette: ['#2962FF', '#E91E63', '#FF5722', '#00E676'],
  bgColor: '#0A2540',                            // Deep Navy (§1.1)
  // ↓ 당신 알고리즘을 제어하는 파라미터들
};
```

#### 핵심 알고리즘 — 철학을 표현

"어떤 패턴을 쓸까?"가 아니라 "이 철학을 코드로 어떻게 표현할까?"를 묻는다.

- **유기적 창발** → 시간에 따라 누적/성장하는 요소, 자연 규칙에 구속된 랜덤, 피드백 루프.
- **수학적 아름다움** → 기하 관계·비율, 삼각함수·하모닉스, 정밀 계산이 만드는 의외의 패턴.
- **통제된 카오스** → 엄격한 경계 안의 랜덤 변주, 분기·상전이, 무질서에서 떠오르는 질서.

알고리즘은 옵션 메뉴가 아니라 철학에서 흘러나온다.

## 홈베이스 원칙 — 색·폰트

| 요소 | 기본값 (홈베이스) | 출처 |
|------|------------------|------|
| 뷰어 UI 폰트 | Pretendard(한·UI), JetBrains Mono(숫자·시드) | `signature-tokens.md §2` |
| 뷰어 헤더 | Deep Navy `#0A2540` | `signature-tokens.md §1.1` |
| 뷰어 액센트(슬라이더·CTA) | Electric Blue `#2962FF` | `signature-tokens.md §1.2` |
| 뷰어 기본 모드 | 라이트(`#F8F9FB` 배경) | `mode-mapping.md §1` |
| **아트 팔레트(기본)** | **jc data 시리즈** `#2962FF/#E91E63/#FF5722/#00E676/#0A2540/#7C3AED` | `signature-tokens.md §1.4` |
| 아트 팔레트(다크 캔버스 보정) | `#5B8DEF/#F04D85/#FF7649/#33EE92/#C9CFD8/#A78BFA` | `mode-mapping.md §3.2` |
| 아트 팔레트(연속/단계) | 인포그래픽 스케일 `scale-blue/green/red/amber` | `signature-tokens.md §1.8` |

- **값 미러링 최소화**: 토큰은 가능하면 SoT(`jc-design-system/references/`) 참조로 설명한다. viewer.html·generator_reference.js의 아트 팔레트 상수는 **출처(§1.4/§3.2)를 주석으로 명시한 의도적 복제**다(런타임 JSON 파싱이 없는 단일 HTML 아티팩트라 불가피). 정본은 항상 `signature-tokens.md §6 JSON`.
- **자유 팔레트 모드(opt-in)**: 사용자가 "자유 팔레트"/"free art"/"이 브랜드 컬러로"를 *명시*하면 그때만 jc 팔레트를 벗어난다. 명시 없으면 항상 jc 홈베이스.
- 어떤 경우에도 **Anthropic 프리셋 색·Poppins/Lora는 0건**.

## 시드 탐색 & 변주

뷰어는 시드 내비게이션을 기본 내장한다(prev/next/random/jump + 표시). 같은 알고리즘에서 시드만 바꿔 무한 변주를 탐색 — 한 판(plate)에서 여러 프린트를 뽑는 것과 같다. 100개 변주 요청 시 시드 1~100을 순회시킬 수 있다.

## 공통 룰 (정본 위임)

값은 재정의하지 않고 정본을 가리킨다 — `jc-design-system/references/shared-rules.md#<RULE-ID>`.

- **`RULE-NO-COMPANY`** — 회사명·실명·부서 등 식별 정보 하드코딩 0건. 작품 제목·서명이 필요하면 외부 주입 변수(`{{personal_brand}}` 등)로만. 정본 `shared-rules.md#RULE-NO-COMPANY`.
- **`RULE-WCAG`** — 뷰어 UI 텍스트 대비 본문 4.5:1↑. jc 토큰 조합은 충족(헤더 흰 텍스트 on Navy 14:1). 계산 표준 `mode-mapping.md §9`. → `#RULE-WCAG`
- **`RULE-PRINT-LIGHT`** — 뷰어를 인쇄/PDF로 뽑으면 배경 라이트 강제(토너 절약). viewer.html `@media print` 포함. → `#RULE-PRINT-LIGHT`
- 아트 팔레트 상수는 `check_drift.py` FORBIDDEN(비-jc 색) 값을 쓰지 않는다.

## 생태계 연결

- **검증**: 1차 산출 아티팩트의 카피·대비·브랜딩 일치·회사 종속 표현은 `jc-redteam`으로 최종 점검(원본의 "fresh Claude 리더 테스트" 자리에 jc-redteam을 끼운다).
- **테마**: 특정 클라이언트 톤이 필요하면 `jc-theme-factory`(3토큰 오버레이) → 단, 아트 팔레트 자유는 본 스킬의 '자유 팔레트 모드'가 담당. 디자인 토큰 자체는 `jc-design-system`.
- **데이터 아트 입력**: 다른 mice-* 산출 JSON을 시각화 소스로 받을 때는 `chaining-protocol.md`의 `ChainPayload/v1` 봉투를 따른다(설명형 차트는 mice-dashboard로 보낸다).

## 형제 경계 (언제 다른 스킬로)

| 원하는 것 | 담당 스킬 |
|-----------|-----------|
| **정적** 캔버스 아트(.pdf/.png 포스터·키비주얼·무드보드·표지 아트) | `jc-visual-philosophy` |
| 상태관리·라우팅·다중 컴포넌트 인터랙티브 **앱**(React/shadcn) | `jc-artifact-builder` |
| 데이터 KPI·차트·인포그래픽 **대시보드** | `mice-dashboard` |
| 디자인 토큰 정의·조회 | `jc-design-system` |
| 산출물에 테마/오버레이 입히기 | `jc-theme-factory` |

본 스킬은 **살아 있는 p5.js 알고리즘**(시드·파라미터·움직임) 전용이다.

## 파일 구조

```
jc-generative-art/
├── SKILL.md                          # 본 파일 — 진입점
├── templates/
│   ├── viewer.html                   # ★ 모든 HTML 아티팩트의 시작점 (jc 리브랜딩)
│   └── generator_reference.js        # p5.js 구조·원칙 참고서(아티팩트엔 인라인 임베드)
└── references/
    └── jc-art-palette.md             # 아트 팔레트(data 시리즈·다크·스케일) + p5.js 사용 스니펫
```

- **`templates/viewer.html`**: 매번 시작점. **유지**: 레이아웃·사이드바·jc 색/폰트·시드 컨트롤·액션 버튼. **교체**: p5.js 알고리즘·파라미터 정의·Parameters/Colors UI. 파일 내 주석이 FIXED vs VARIABLE을 표시한다.
- **`references/jc-art-palette.md`**: jc 팔레트를 p5.js에서 어떻게 쓰는지(시드 기반 색 선택·다크 배경 보정·연속 스케일) 모은 참고. 값 정본은 항상 `signature-tokens.md`.

## 빠른 체크리스트

- [ ] 알고리즘 철학(.md) 먼저 → p5.js 아트(.html). 시드 재현성(`randomSeed`+`noiseSeed`) 보장
- [ ] `templates/viewer.html`을 시작점으로 사용(STEP 0). FIXED 섹션 보존
- [ ] 뷰어 = Pretendard·Deep Navy·Electric Blue·라이트 기본. Anthropic 색·Poppins/Lora 0건
- [ ] 아트 팔레트 기본 = jc data 시리즈(§1.4). 자유 팔레트는 사용자 명시 시에만
- [ ] 시드 컨트롤(prev/next/random/jump) + Regenerate/Reset/Download PNG 동작
- [ ] 단일 자가완결 HTML(p5.js만 CDN, 알고리즘 인라인)
- [ ] 회사·개인정보 하드코딩 0건(외부 주입 변수) · `check_drift.py` FORBIDDEN 색 0건
- [ ] 1차 산출 후 `jc-redteam`으로 점검 가능
