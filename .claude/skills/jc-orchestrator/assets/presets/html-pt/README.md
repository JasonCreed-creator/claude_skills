# 프리셋: html-pt — HTML 프레젠테이션 8에이전트 팀

RFP·브리프를 입력받아 **단일 HTML 프레젠테이션**(Reveal.js 기반)을 산출하는 완성 팀 구성. jc-orchestrator 카탈로그 8 아키타입의 실증 인스턴스다.

- **출처**: 2026-05-07 대화에서 저작·실빌드된 v1(html-pt-team.zip)의 스펙 기반 **재생성본(v2)**. 표준 agent-template 포맷으로 정규화 + v1 실증 교훈 3건 반영. 원본 v1 zip 발견 시 diff 대조 병합할 것 — 세부 프롬프트 뉘앙스는 재생성 과정에서 손실됐을 수 있음
- **스택**: Reveal.js + Tailwind CSS(CDN) + GSAP + Chart.js + Pretendard — 단일 HTML 배포, 빌드 도구 불필요
- **v1 대비 개선**: ① visual-designer가 jc-design-system 토큰을 SoT 앵커로 참조(v1은 하드코딩) ② 모든 에이전트 입출력 계약 명문화(컨텍스트 격리 대응) ③ 실행 의미론 정직화(순차 파이프라인 + 제한적 병렬)

## Phase 구조 · 의존성

```
Phase 1  strategy-planner ∥ research-agent      ← 유일한 병렬 구간(상호 독립 입력)
Phase 2  content-writer → structure-architect
Phase 3  visual-designer → animation-engineer   ← 순차 필수(v1 교훈: 동시 편집 충돌)
Phase 4  build-qa-engineer
Phase 5  risk-reviewer
```

- 산출물 디렉터리: `outputs/` — 파일명 규칙 `NN-slug-요지.md/html`
- Phase 경계마다 사용자 승인 포인트(prompts.md §3)

## 경량 모드 (10장 이하 PT)

strategy-planner → content-writer → visual-designer → build-qa-engineer 4개로 축소. research(근거가 이미 있을 때)·structure(단순 선형 구조)·animation(정적 슬라이드)·risk(내부용 저부담)를 생략한다. 생략 판단은 구성안 승인 시 명시.

## 파일

```
html-pt/
├── README.md          # 본 파일 — Phase 구조·경량 모드·출처
├── prompts.md         # 킥오프·에이전트 호출·Phase 승인 표준 프롬프트 3종
└── agents/            # 8 에이전트 정의 (agent-template 준수)
    ├── strategy-planner.md
    ├── research-agent.md
    ├── content-writer.md
    ├── structure-architect.md
    ├── visual-designer.md
    ├── animation-engineer.md
    ├── build-qa-engineer.md
    └── risk-reviewer.md
```

## 사용법 (Code 기준)

1. `agents/` 를 프로젝트의 `.claude/agents/` 로 복사
2. `inputs/` 에 RFP·브리프 업로드
3. prompts.md §1 킥오프 프롬프트로 시작 — kickoff-code.md 블록(쓰기 경계·커밋 권한·완료 신호) 명문화
4. Phase 경계 승인 → Phase 5 감수 반영 → 최종 HTML

Chat·Cowork에서는 각 킥오프 템플릿(kickoff-chat/cowork.md)의 실행 의미론으로 동일 역할 순서를 운용한다.
