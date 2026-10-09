---
name: jc-pptx
description: 리멤버 MICE비즈팀의 PPTX 산출물 전부 — 발주처 제안서(RFP·비딩 대응), 리멤버 MICE 솔루션 소개서, 발표덱, 결과보고 덱 — 를 리멤버 웜 페이퍼 룩으로 구성·빌드·검수하는 단일 프레젠테이션 엔진. 실측 문법(주장형 헤드라인·네비게이션·KPI·구조 도해·16종 슬라이드 타입)과 제안서 설득 설계(배점 역설계·원 메시지·근거 있는 차별화)를 내재하고, python-pptx deck_kit으로 Claude Design DS 슬라이드 템플릿 10종과 같은 지오메트리를 빌드한다. 다음 상황에서 반드시 이 스킬을 사용할 것 — 사용자가 'PPT', 'PPTX', '슬라이드', '데크', '장표', '발표자료', '제안서', '소개서', '비딩 자료', 'PT 자료', '피티', '프레젠테이션', '이걸로 PPT 구성해줘', '장표로 만들어줘', '제안서 써줘', '기존 PPT 리멤버 톤으로 바꿔줘', '리스킨'을 언급할 때. RFP·추진계획·회의록·기획 메모를 주며 덱을 요청할 때. 기본 pptx 스킬 대신 본 스킬을 우선 사용한다(기본 pptx는 빌드 기계로만 참조). 형제 경계 — 디자인 토큰 값은 jc-design-system(읽기만), RFP 7축 분석·GO/NO-GO는 mice-rfp-analyzer(상류), 견적 xlsx는 mice-estimate, 발표 대본은 pt-script(하류), 운영계획서·결과보고서 문서는 mice-ops-docs, 완성 덱의 적대 검증은 jc-redteam. HTML 슬라이드·랜딩은 본 스킬 밖.
version: "v2.1.0"
---

# JC PPTX v2 — 리멤버 프레젠테이션 엔진

**동작 모델**: 콘텐츠를 주면 → 본 스킬이 구성한다. 문법·룩은 불변, 콘텐츠·스토리라인·밀도는 가변. 룩은 리멤버 웜 페이퍼 하나(`jc-design-system` v2).

```
[입력] 브리프·RFP·회의록 → 메시지 추출 → 스토리라인 → 타입 매핑 → 카피 변환
      → 리멤버 테마 → 빌드(deck_kit) → 검수(check_deck) → jc-redteam → 납품
```

## 용도별 진입

| 용도 | 스토리라인 | 참조 |
|------|-----------|------|
| **발주처 제안서** (RFP·비딩·위탁) | 대응형 — 배점표가 목차의 상위 규칙 | `references/proposal-playbook.md` |
| **리멤버 솔루션 소개서** (세일즈) | 설득형 — 문제→자격→구조→가치→논증→클로징 | `scripts/examples/build_deck2.py`(2026-09 실증 34장) |
| **발표덱·경영진 보고** | 보고형 — 결론 선행 | `references/design-language.md §3` |
| **결과보고 덱** | 보고형 + KPI | `mice-ops-docs` 결과보고 ChainPayload 수용 |
| **기존 PPTX 리스킨** | 서식만 교체 | `scripts/restyle_pptx.py` |

## 워크플로우 (기획안 1회 확인 → 빌드 → 검수)

되돌릴 수 있는 작업(구성안·초안 파일·분석)은 합리적 기본값으로 바로 진행하고, 고른 기본값을 한 줄로 밝힌다. 사용자 확인은 기획안 1회뿐이다. 외부 발송·게시는 승인 후.

### ① 기획안 — 1회 확인 (파일 생성 전)
1. **인테이크**: 프로젝트명 / 용도 / 청중 / 콘텐츠 소스 / 발주처 슬롯(로고·표지 이미지·푸터 행사명). 누락은 추론으로 채우고 '가정' 표기(되묻지 않는다). ChainPayload(`mice-rfp-analyzer`·`mice-meeting-minutes`)가 있으면 재분석하지 않는다.
2. **제안서면 설득 설계 먼저**: 배점 역설계 → 커버리지 매핑표 → 원 메시지 → 근거 있는 차별화 → 발주처 언어 미러링 → 리스크 선제 응답 (`proposal-playbook.md §2`).
3. **기획안 제시**: 핵심 메시지 1문장 + `[번호 | 타입 T01~T16 | 헤드라인 초안 | 콘텐츠 슬롯]` 표 + 다크 슬라이드 위치(표지·섹션·클로징) + 분량. 헤드라인은 이 단계에서 이미 주장 문장. 구성·핵심 메시지만 한 번 확인받는다(사용자가 "바로 만들어"라고 했으면 확인 없이 진행).

### ② 빌드
4. **테마**: 기본 `remember`(`references/themes.md`). 발주처 슬롯은 `jc-design-system/references/client-overlays.md §1`. 발주처 컬러는 받지 않는다.
5. **빌드**: `scripts/deck_kit.py` — 그리드 상수·컴포넌트 헬퍼만 사용, 좌표·색 하드코딩 금지. 한글 서체는 `set_font_all`(latin·ea·cs)로. 사진 없으면 `image_placeholder` + 이미지 브리프(임의 스톡 금지, 이미지 생성이 필요하면 Higgsfield).
6. **자가 검수**: `python scripts/check_deck.py <deck.pptx>` 위반 0까지.

### ③ 검수·납품
7. 렌더 확인(PowerPoint 또는 soffice→PNG) → 시각 결함 수정 → `jc-redteam` 검수(제안서는 `proposal-playbook.md §5` 완료 게이트 6항 포함) → PPTX + PDF 납품. 폰트 미설치 PC 공유는 PDF.

## 절대 규칙

- **한 슬라이드 = 한 메시지.** 본문 제목은 주장 문장(명사구 금지), 강조어구는 슬라이드당 1개 오렌지.
- **네비게이션 전 슬라이드 반복**: 아이브로우(`NN · SECTION`) + 푸터(좌 행사명 · 중앙 페이지 · 우 로고). deck_kit이 자동.
- **다크는 표지·섹션 구분·클로징만**(덱의 30% 이하). 그라디언트·솔리드 KPI·다크 패널은 슬라이드당 1회.
- **테마 토큰 외 색 금지.** 오렌지 텍스트는 큰 글자 전용, 작은 강조는 딥 오렌지(RULE-WCAG).
- **명의·식별정보**: 리멤버 MICE비즈팀 명의 기본, 발주처·담당자는 슬롯 주입. 구 소속사 언급·누적 건수 금지(RULE-NO-COMPANY v2).
- **안티패턴 8종**(`design-language.md §7`) — check_deck.py가 기계 검수.

## 파일 구조

```
jc-pptx/
├── SKILL.md
├── references/
│   ├── design-language.md          # 문법 SoT: 7원칙·엔진·밀도·카피·안티패턴
│   ├── slide-types.md              # 16종 타입 지오메트리 + DS 템플릿 10종 매핑
│   ├── themes.md                   # remember 기본 프리셋(토큰 매핑) · 명명 프리셋 · 주입 규칙
│   ├── proposal-playbook.md        # 제안서 설득 설계 · 7섹션 골격 · 유형별 강조 · 완료 게이트 · 체이닝
│   └── remember-deck-templates.md  # T1~T12 HTML 문법 + DS 슬라이드 01~10 레시피
├── scripts/
│   ├── deck_kit.py                 # 빌드 헬퍼 (그리드·테마·네비·컴포넌트·표지·클로징)
│   ├── check_deck.py               # 안티패턴 자동 검수 CLI
│   ├── restyle_pptx.py             # 기존 PPTX 리스킨(서체·텍스트색·도형 채움)
│   └── examples/
│       ├── remember_kit.py         # 2026-09-18 소개서 실증 빌더(v1 kit 위 리멤버 토큰) — 참고용
│       └── build_deck2.py          # 소개서 34장 A/B안 빌드 스크립트 — 슬라이드 함수 레시피 참고용
└── assets/
    ├── texture-dark.png · texture-light.png   # 명명 프리셋용 텍스처 (remember 프리셋은 미사용)
```

로고·오브제는 `jc-design-system/assets/`에서 런타임으로 읽는다.

## 생태계 연결

- 디자인 정본: `jc-design-system` v2 (`jc-design-system/scripts/jc_tokens.py` 런타임 로드)
- 상류: `mice-rfp-analyzer`(요건·배점·차별화) · `mice-meeting-minutes`(Discovery 데이터) · `mice-ops-docs`(결과보고)
- 하류: `mice-estimate`(견적 힌트) · `pt-script`(발표 대본)
- 검증: `jc-redteam` (납품 전 필수)
- 봉투: `jc-design-system/references/chaining-protocol.md` — source `jc-pptx`, 발표 메타는 `presentation` 키(하류 `pt-script`가 읽음). 구 source `mice-proposal`은 하위호환 별칭

## 변경 이력

- v2.1.0 (2026-10-05): '3턴' 워크플로우 → '기획안 1회 확인 → 빌드 → 검수'(기본값 진행). 예제 빌더의 '리더' 직함 → '팀장', 구 jc-remember-html 경로 → jc-design-system, 고객사 실명 → 가명(A사 등).
  존재하지 않는 LICENSE.txt 참조 삭제, `python3` → `python`.

### v2.0.0 (2026-09-21)
- 룩을 리멤버 웜 페이퍼 단일 기본으로 전환. `remember` 프리셋이 jc-design-system v2 토큰을 런타임 매핑.
- `mice-proposal` v3.0.1 흡수 — 설득 설계·7섹션 골격·유형별 강조·완료 게이트를 `proposal-playbook.md`로. pptxgenjs 빌드 경로 폐기.
- `jc-remember-html` 덱 템플릿 T1~T12 + DS 슬라이드 10종 레시피를 `remember-deck-templates.md`로 흡수. `jc-brand-styling` `style_pptx.py`를 `restyle_pptx.py`로 흡수.
- deck_kit v2: 한글 서체 ea 지정, 그라디언트·링·오브제·로고 푸터·다크 표지/섹션/클로징·표(가로선) 헬퍼 추가. 2026-09-18 소개서 빌드 스크립트를 `examples/`로 회수.
- 샌드박스 절대경로 제거, SoT 탐색을 형제 경로 → `~/.claude/skills` → synced 순으로.

### v1.0.0 (2026-08)
실측 레퍼런스 6종 문법 추출, 16종 타입, dark-premium·light-vivid 프리셋.
