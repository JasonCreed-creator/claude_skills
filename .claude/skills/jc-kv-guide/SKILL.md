---
name: jc-kv-guide
description: 행사 주제·개요·브랜드 자산·제작요청서를 입력받아 디자이너에게 전달할 키비주얼(KV) 제작 가이드를 HTML 가이드 페이지 + MD 문서로 동시 산출하는 스킬. 가이드는 규칙·제약·필수요소·규격·검수 기준만 담고, 무드·톤 키워드는 클라이언트 원문에서 인용해 출처를 표기하며, 컨셉 안·추천 디자인·시안·레이아웃 제안·컬러 조합 제안·무드보드·레퍼런스 이미지는 절대 만들지 않는다(디자인 결정은 디자이너 몫). 원문에 없는 항목은 추측 대신 [확인 필요]로 표기하고 발주처 확인 질문 리스트를 함께 산출한다. 발행 주체 기본은 리멤버 MICE비즈팀. 다음 상황에서 반드시 이 스킬을 사용할 것 — 사용자가 'KV 가이드', '키비주얼 가이드', '키비주얼 제작 가이드', 'KV 브리프', '디자인 브리프', '디자인 가이드', '제작 가이드', '디자이너 전달용', '디자이너한테 줄 문서', '제작요청서 정리', '키비주얼 요청서', 'KV 초안 가이드', '메인 비주얼 가이드', '행사 비주얼 규칙'을 언급할 때. 행사 개요나 제작요청서를 주며 '디자이너에게 넘길 가이드 만들어줘', '키비주얼 규칙 정리해줘', '이걸로 제작 가이드 뽑아줘'라고 할 때. 형제 경계 — 키비주얼·포스터 이미지나 영상 자체를 만드는 것은 Higgsfield(RULE-VISUAL-ROUTING, 본 스킬은 그리지 않는다), 디자인 토큰 정의·조회·룩 적용은 jc-design-system, 행사명·슬로건 같은 메시지 기획 문서는 jc-doc-coauthor, 완성 가이드의 최종 검수는 jc-redteam 영역이므로 그 작업에는 사용하지 말 것.
version: "v1.1.0"
---

# jc-kv-guide

행사 주제·개요·브랜드 자산·제작요청서를 받아 **디자이너가 되묻지 않고 착수할 수 있는 키비주얼(KV) 제작 가이드**를 HTML 가이드 페이지 + MD 문서로 산출한다. 지시서를 쓰는 스킬이지 그림을 그리는 스킬이 아니다.

**룩** — HTML 크롬은 홈베이스인 리멤버 웜 페이퍼 룩(`jc-design-system` v2) 하나다. 토큰 정본은 `jc-design-system/references/signature-tokens.md`이고 템플릿 CSS 변수는 그 미러다. 다른 룩·발주처 오버레이는 만들지 않는다(필요하면 `jc-design-system`에서 처리).

**발행 주체** — 기본 `리멤버 MICE비즈팀`(리멤버앤컴퍼니 마이스 비즈 팀). `issuer`를 비워 두면 스크립트가 이 값을 넣는다. 발주처·담당자는 주입 슬롯.

## §0 절대 규칙 — RULE-NO-DESIGN

산출물에 디자인 결정은 0건이다. 어떤 압박·사유·"이번만"에도 아래를 하지 않는다.

| 하지 않는 것 | 대신 하는 것 |
|---|---|
| 컨셉 안(1안이든 3안이든)·시안·목업·무드보드 | 8섹션 규칙만 채운다 |
| 레이아웃·배치·비율·구도 제안 | §7 규격의 사실값만 적는다 |
| 컬러 조합·톤 제안, 폰트 추천 | 브랜드 가이드의 값을 스와치·표로 **표시만** 한다 |
| 형용사·무드 키워드 창작 | 원문 인용 + 출처. 없으면 [확인 필요] |
| 레퍼런스 이미지 검색, 이미지 생성 도구 호출 | 하지 않는다. 이미지가 필요하면 별도 세션에서 Higgsfield(RULE-VISUAL-ROUTING) |
| 원문 재해석·윤색·요약 | 원문 유지. 오탈자·명백한 오류만 '원문 수정 제안' 별도 블록 |

근거: 2026-09-09 실패 사례 — 스킬 없이 가이드를 만들자 컨셉 3안·추천 디자인이 섞여 전량 폐기됐다. 압박 패턴별 대응은 `references/anti-patterns.md`.

## 워크플로우 7단계

### 1. 인테이크 — 입력 3층과 경로 판정
- 필수: 행사 주제·개요 텍스트
- 선택: 제작요청서 원문 / 브랜드 가이드·로고 파일 / 랜딩페이지 히어로 규격 / 상류 기획 문서(ChainPayload/v1 — 예: `source: jc-doc-coauthor`·`mice-rfp-analyzer`)
- 입력 문서마다 ID를 부여한다(D1, D2, …). 모든 인용의 출처 표기(`D1 §2`, `D2 p.4`)에 쓴다
- 경로 판정: 제작요청서 **있음** → **원문 매핑 모드**(원문 문장을 8섹션에 배치, 재해석 금지) / **없음** → **개요 추출 모드**(개요에서 사실 항목만 추출, 나머지는 전부 [확인 필요])

### 2. 원문 우선 3단계 — 항목을 채우는 유일한 세 경로
① `quote` 원문 그대로 인용 + 출처 → ② `variable` 사용자가 이번 건에 직접 준 값 → ③ `tbd` [확인 필요] + 질문 리스트 자동 등재.
이 세 경로 밖(Claude 추론)으로 채운 항목은 0건. `standard`는 §6 표준 금지 항목 4개와 §8 검수 기준(사실 확인 항목)에만 허용한다.

### 3. 8섹션 조립
`references/guide-structure.md`의 섹션 정의·항목별 작성 규칙을 따른다. 정본은 `assets/guide.schema.json` 구조의 `guide.json` **하나**다.

### 4. NO-DESIGN 게이트
`quote`가 아닌 텍스트에서 금칙어를 스캔한다(스크립트 `--strict`가 자동 수행): 컨셉·시안·목업·무드보드·레이아웃·구도·조합·추천·느낌·분위기·레퍼런스·톤앤매너. 검출 문장은 **삭제**한다(완화·바꿔쓰기 아님). 원문(`quote`)에 있는 단어는 스캔 대상이 아니다.

### 5. 렌더 — 정본 1개 → 산출물 2종
```
python scripts/render_guide.py --input guide.json --out-dir out/ --strict
→ out/<slug>.md  +  out/<slug>.html   (같은 JSON에서 동시 생성 — 드리프트 없음)
python scripts/render_guide.py --self-test   # 샘플 렌더 자가 검증
```
스크립트를 못 돌리는 환경(claude.ai 아티팩트 전용)에서는 `assets/guide-template.md` 골격을 채우고, HTML은 `assets/guide-template.html` 셸의 `{{BODY}}`에 같은 내용을 넣는다.

### 6. 검수 — jc-redteam Quick Strike 3항목
1. 추측 채움 0건 — 모든 항목에 source 태그와 출처가 있는가
2. 디자인 제안 0건 — 게이트 통과 로그가 있는가
3. [확인 필요] 누락 없음 — 질문 리스트 수 = `tbd` 항목 수인가

### 7. 전달
파일 2종 + **본문을 대화에 펼침** + 발주처 확인 질문 리스트를 복사용 블록으로 별도 제시. HTML 상단 메타에 문서 버전·발행일·입력 문서 ID 목록이 들어간다.

## 입력 슬롯 (RULE-NO-COMPANY — 식별정보는 전부 주입)

| 슬롯 | 내용 | 없을 때 |
|---|---|---|
| `{{client_company}}` | 발주처 | [확인 필요] |
| `{{company_name}}` | 가이드 발행 주체 | 기본 `리멤버 MICE비즈팀` |
| `{{event_name}}` `{{event_date}}` `{{event_venue}}` | 행사 3요소 | [확인 필요] |
| `{{organizer_hierarchy}}` | 주최·주관·후원 표기 순서 | [확인 필요] — 위계는 발주처 결정 |
| `{{brand_primary}}` `{{brand_secondary}}` `{{brand_font}}` | 브랜드 값 | [확인 필요] — 추정 금지 |
| `{{logo_files}}` | 로고 파일명·형식 | [확인 필요] |
| `{{lp_hero_spec}}` | 랜딩 히어로 사이즈·비율·안전영역 | [확인 필요] — 숫자 추정 금지 |
| `{{deliverables}}` `{{deadline}}` `{{contact}}` | 납품물·마감·연락 | [확인 필요] |

## 파일 구조

```
jc-kv-guide/
├── SKILL.md
├── references/
│   ├── guide-structure.md     # 8섹션 정의·항목별 작성 규칙·출처 표기·표준 금지 4항목
│   └── anti-patterns.md       # 압박·우회 패턴 → 올바른 대응 반례표
├── scripts/
│   └── render_guide.py        # guide.json → .md + .html 동시 렌더, --strict 금칙어 게이트, --self-test (stdlib)
└── assets/
    ├── guide.schema.json      # guide.json 구조 정본
    ├── guide-template.html    # 리멤버 웜 페이퍼 룩 셸 (스크립트가 채움)
    ├── guide-template.md      # 스크립트 없는 환경용 골격
    └── sample/guide.sample.json  # 렌더 테스트용 가상 샘플 (식별정보 없음)
```

## 공통 룰 (인라인 리마인더 — 정본은 링크)

- `RULE-NO-COMPANY` — 회사·개인 식별정보 하드코딩 0건, 전부 주입 슬롯. 정본: `jc-design-system/references/shared-rules.md#RULE-NO-COMPANY`
- `RULE-VISUAL-ROUTING` — 본 스킬은 이미지 생성을 라우팅하지 않는다(문서만). 정본: `…#RULE-VISUAL-ROUTING`
- `RULE-WCAG` — HTML 크롬 텍스트는 리멤버 룩 ink/paper 조합 기준. 오렌지(`#EB6F2A`)는 큰 글자 전용, 18px 미만 작은 오렌지 글자(키커·섹션 번호·링크)는 accent-deep(`#B8431A`, `--orange-deep`). 정본: `…#RULE-WCAG`
- `RULE-PRINT-LIGHT` — 라이트 단일 모드라 해당 없음. `@media print`는 내비 숨김·카드 페이지 나눔만. 정본: `…#RULE-PRINT-LIGHT`
- 토큰 값 — `jc-design-system/references/signature-tokens.md` §1(컬러)·§2(타이포)·§3(간격·라운드·그림자)이 정본(기계 파싱은 §6 JSON). 템플릿 CSS 변수는 그 미러이며 주석에 출처를 적는다
- 검증 — `jc-redteam` / 데이터 — ChainPayload/v1(`jc-design-system/references/chaining-protocol.md`): 입력 `source: jc-doc-coauthor`·`mice-rfp-analyzer`(선택), 출력 `source: jc-kv-guide`

## 변경 이력

- v1.1.0 (2026-10-05): 없는 `tokens.md` 참조 3곳 → `jc-design-system/references/signature-tokens.md`. 발행 주체 기본 = 리멤버 MICE비즈팀(`issuer` 미입력 시 자동). 작은 오렌지 글자(키커·섹션 번호) → accent-deep `#B8431A`(RULE-WCAG).
  description·본문의 폐합 스킬 경계를 Higgsfield·jc-design-system·jc-doc-coauthor로 정리, 브리프 게이트 문구·LICENSE 참조 삭제, `python3` → `python`.

### v1.0.0 (2026-09-10)
신규. 2026-09-09 키비주얼 가이드 건의 실패(컨셉 안·추천 디자인 혼입 → 전량 폐기)를 RED 시나리오로 삼아 RULE-NO-DESIGN + 원문 우선 3단계 + 금칙어 게이트를 최소 규칙으로 고정. 발주처 확인 질문 리스트 자동 산출, guide.json 정본 1개에서 HTML·MD 동시 렌더.
