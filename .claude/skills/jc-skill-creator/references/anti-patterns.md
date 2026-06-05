# jc-skill 제작 안티패턴 라이브러리

스킬을 만들 때 실제로 밟는 함정 + 교정. 각 항목은 `scoring-rubric.md`의 감점 기준과 연결된다(lint가 자동 적발하는 것은 [lint] 표시).

## A. 메타데이터·명명

### A-1. 디렉터리명과 frontmatter `name` 불일치 [lint C2]
- **증상**: 폴더는 `jc-foo`인데 `name: foo` 또는 오타. 스킬 로더가 못 찾거나 중복 등록.
- **교정**: `name` == 디렉터리 basename, 정확히 `jc-<도메인>`. (house-conventions §디렉터리)

### A-2. version 누락·비-SemVer [lint C1·C3]
- **증상**: `version` 없음, 또는 `1.0`·`2.0`처럼 SemVer 아님. 수정해도 안 올림.
- **교정**: 신규 `v1.0.0`, 수정 시 범프(patch/minor/major). frontmatter 4필드(name·description·version·license) 항상 채운다.

### A-3. LICENSE 누락 [lint C6]
- **증상**: `LICENSE.txt` 없이 스킬만 추가. 배포·공개 시 라이선스 불명.
- **교정**: 루트에 `LICENSE.txt`(라이브러리 표준 Apache 2.0). 신규 스킬 체크리스트 필수.

## B. description (트리거의 전부)

### B-1. 너무 짧거나 '무엇을'만 [lint C4]
- **증상**: "견적서를 만든다." 한 줄. Claude가 *언제* 부를지 몰라 **undertrigger**.
- **교정**: 무엇을 + **언제(키워드·맥락 폭넓게)** + **형제 경계**. 200–1024자. 사용자가 실제 칠 한국어 동의어를 넉넉히. (house-conventions §description)

### B-2. 형제 경계 없음 → 오트리거 [lint C4]
- **증상**: 인접 스킬과 키워드가 겹치는데 "쓰지 말 것"이 없어 엉뚱한 스킬이 뜬다(예: '결과보고서'로 dashboard·aftermath 동시 후보).
- **교정**: "단, …는 <형제 스킬> 영역이므로 그쪽을 쓸 것" 문장을 description에 명시. near-miss를 직접 거명.

### B-3. 영어 description
- **증상**: 영어로 작성 → 한국어 트리거 표현과 매칭 약화.
- **교정**: 한국어 우선·푸시형. (영어 키워드는 병기 가능하나 본문은 한국어.)

## C. 디자인·식별정보

### C-1. 회사·실명 하드코딩 [lint C7 / Critical]
- **증상**: 산출 템플릿·예시에 금칙 회사 상호(`M&C커뮤니케이션즈`)·실명·부서(`신사업실`)·실제 이메일이 그대로 박힘. 공개 레포면 PII 노출, Track A/B 재사용 깨짐.
- **교정**: 외부 주입 변수만(`{{company_name}}`·`{{author_name}}`·`{{author_dept}}`·`{{author_email}}` 등). 정본 `shared-rules.md#RULE-NO-COMPANY`. **단** sanitizer 차단 리스트는 *일부러 보유*(면제).

### C-2. 디자인 토큰 값 미러링 [drift-guard]
- **증상**: `#2962FF` 같은 hex를 본문·코드에 박음. SoT(`jc-design-system`)와 drift.
- **교정**: 런타임 로드(`jc_tokens.py`), 라이트/다크는 `mode-mapping.md`. 부득이한 미러는 출처(`§6`/`§3`) 주석 + `check_drift.py` 통과. (house-conventions §SoT 앵커)

### C-3. 자유 팔레트를 silent default로
- **증상**: 임의 색·대체 브랜드를 기본값처럼 노출.
- **교정**: jc 시그니처가 홈베이스(기본). 자유는 '자유 모드' 명시적 opt-in으로만. (홈베이스 원칙)

## D. 구조·생태계

### D-1. 500줄 넘는 SKILL.md [lint C5]
- **증상**: 모든 디테일을 SKILL.md에 욱여넣음 → 컨텍스트 과부하.
- **교정**: SKILL.md는 워크플로우·판단(<500줄). 상세는 `references/`로 분리(진행형 디스클로저).

### D-2. 평가 기계 재발명
- **증상**: 벤치마크·eval-viewer·description 최적화 루프를 스킬 안에 복제(500줄).
- **교정**: 상위 skill-creator 기계에 위임(`upstream-machinery.md`). 본 레포는 *규칙*만 얹는다.

### D-3. 검증 자체 채점으로 흉내
- **증상**: stratarts식 "스코어링"으로 우호적 자기 검증.
- **교정**: 결론·산출물의 견고성은 `jc-redteam`(적대적)으로. 본 루브릭(lint)은 *규약 준수*만 재고 *품질 판단*은 redteam에 넘긴다. 둘은 보완재.

### D-4. 반복 작업을 매번 수작업
- **증상**: 같은 변환·집계를 대화로 반복.
- **교정**: `scripts/`로 한 번 만들고 자가검증(`--self-test`) 붙인다. (진행형 디스클로저 + 스크립트 번들)

### D-5. 체이닝 미배선
- **증상**: 데이터 입출력을 임의 포맷으로 → 형제 스킬과 안 붙음.
- **교정**: `ChainPayload/v1`(`chaining-protocol.md`) 봉투. source enum 등록까지 마친다.
