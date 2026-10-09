# Shared Rules — 공통 룰 정본

여러 소비 스킬(jc-pptx · mice-ops-docs · mice-meeting-minutes · pt-script · mice-rfp-analyzer · mice-estimate · mice-run-of-show · mice-aftermath · jc-strategy-canvas · mice-market-intel · jc-redteam · mice-team-board · jc-kv-guide)에 반복 등장하는 공통 규칙의 권위 정의. 소비 문서는 짧은 인라인 리마인더 + `정본: jc-design-system/references/shared-rules.md#<RULE-ID>` 링크만 둔다.

색상 값의 정본은 `signature-tokens.md`, 다크·대비는 `mode-mapping.md`. 본 문서는 정책만 정의한다.

---

## 규칙 인덱스

| ID | 규칙 | 적용 |
|----|------|------|
| `RULE-WCAG` | WCAG AA 대비 목표 | 전 산출물 |
| `RULE-PRINT-LIGHT` | 다크 산출물도 인쇄 시 라이트 강제 | HTML |
| `RULE-PPTX-HEX` | python-pptx/pptxgenjs hex는 `#` 없이 6자리 | PPTX |
| `RULE-NO-COMPANY` | 발주처·담당자 식별정보는 외부 주입, 리멤버 명의는 기본 | 전 산출물 |
| `RULE-VISUAL-ROUTING` | 시각 에셋 소스 우선순위 | 이미지 포함 산출물 |
| `RULE-VERSION-FACTS` | 제품·버전 팩트는 실검증 + 검증일 병기 | 전 문서·스크립트 |

---

## RULE-WCAG

- 본문 4.5:1 이상, 큰 텍스트(18pt+ Bold / 24pt+) 3.0:1 이상, 비텍스트 3.0:1 이상.
- 리멤버 팔레트 실측 결론(`mode-mapping.md §5`): 오렌지 `#EB6F2A` 텍스트는 큰 글자 전용, 작은 강조는 `#B8431A`, 다크 위는 `#F08A4C`. 캡션 `#8C867A`는 보조 정보만. 앰버 단독 텍스트 금지.
- 계산 표준: `mode-mapping.md §9`(sRGB 상대 휘도, WebAIM 기준값).
- 체크: 새 색 조합을 쓰면 §9 공식으로 계산해 표에 추가한다.

## RULE-PRINT-LIGHT

- 다크 토글이 있는 HTML도 인쇄·PDF는 항상 라이트. `@media print`에서 토큰을 라이트로 덮어쓰고 화면 상태는 유지.
- 잠금·내부 전용 블록(단가·마진 등)은 `.no-print`로 인쇄 제외.
- 구현: `mode-mapping.md §4.2`.

## RULE-PPTX-HEX

- python-pptx `RGBColor.from_string("EB6F2A")`, pptxgenjs `color: "EB6F2A"` — `#`가 붙으면 무음 실패.
- HTML/CSS는 `#EB6F2A`. 같은 값이라도 매체별 표기가 다르다. `jc_tokens.color(tok, key, hash_prefix=False)`가 변환한다.
- 체크: 빌드 후 hex 문자열에 `#` 0건.

## RULE-NO-COMPANY (v2 재정의)

**정의**: 산출물의 발행 명의는 리멤버 MICE비즈팀이 기본이다. 그 외 식별 정보 — 발주처·고객사·담당자 실명·연락처·협력사 — 는 산출 시 외부 주입 변수로만 받는다.

- 허용(기본 명의): `(주)리멤버앤컴퍼니 마켓데이터사업실 · MICE 비즈팀`, 로고 2종, 공용 문의 `mice_solution@remember.co.kr`, 양식 명칭("리멤버 견적서", "산출내역서" — 리멤버 양식 단일).
- 주입 슬롯: `{{client_company}}` `{{client_contact}}` `{{event_name}}` `{{venue}}` `{{author_name}}` `{{author_title}}` + 스킬별 슬롯.
- 금지: 개인 휴대전화·사설 메일을 대외 문서에 넣는 것. 구 소속사(M&C) 명칭·프로젝트명·누적 건수를 리멤버 명의 문서에 넣는 것(2026-09-18 결정). 팀원 경력은 범위·규모 표현으로만("APEC 국제회의 ~ BCWW 초대형 박람회", 18년, 2만 명 규모).
- 고객사 실명 레퍼런스는 노출 동의 확인 후에만(익명 요청 사례 있음). 미확인이면 익명 표기(A사·I사).
- 체크: 대외 산출물에 M&C·엠앤씨·mnccom 0건, 개인 연락처 0건.

## RULE-VISUAL-ROUTING

- 사진·래스터 히어로: ① `assets/objet-*.png` 7점(다크 슬라이드) ② 발주처·베뉴 제공 원본 ③ 생성 이미지(Higgsfield 등, 연결돼 있을 때만). 임의 스톡 금지 — 없으면 플레이스홀더 + 이미지 브리프.
- 표·차트·다이어그램·인포그래픽·SVG/HTML: Claude 코드로 직접 렌더.
- 라이트 캔버스 위 오브제 금지.

## RULE-VERSION-FACTS

- 제품명·모델명·버전·가격 등 시점 종속 팩트는 기록 직전 공식 소스로 실검증하고 `(YYYY-MM-DD 검증 기준)`을 병기한다. 계열명 우선, 스냅숏 ID는 코드에 필요할 때만.
- 근거: 폐기 모델 ID가 스크립트에 남으면 실행 시 404(2026-07 실사례).
- 체크: jc-redteam 검증 체크리스트 §1-8.

---

## 변경 이력

- **v2.2.0 (2026-10-09)** — 소비 스킬 목록에 mice-estimate 추가, 허용 양식명 '산출내역서(공공형)' → '산출내역서'(리멤버 양식 단일, mice-estimate v3.3.0 기준).
- **v2.1.0 (2026-10-05)** — 소비 스킬 목록을 라이브 기준으로 갱신, RULE-NO-COMPANY 예시의 고객사 실명 삭제.
- **v2.0.0 (2026-09-21)** — 리멤버 전환. RULE-NO-COMPANY를 "리멤버 명의 기본 + 발주처 주입"으로 재정의, M&C 언급 금지·레퍼런스 실명 동의 규칙 추가. RULE-WCAG에 리멤버 팔레트 실측 결론 추가. RULE-VISUAL-ROUTING을 오브제 우선으로 개정. mice-sponsor-deck 등 폐지 스킬 참조 제거.
- v1.2.0 (2026-07-03) RULE-VERSION-FACTS 신설 · v1.1.0 (2026-06-04) RULE-VISUAL-ROUTING 신설 · v1.0.0 (2026-06-02) 4룰 통합.
