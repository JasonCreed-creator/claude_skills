---
name: jc-mcp-builder
description: 외부 서비스(Slack·Google Drive/Calendar·CRM·행사 등록 시스템 등)나 mice-* 산출 데이터(견적·KPI·회의록)를 외부 LLM/도구가 다루게 해주는 MCP(Model Context Protocol) 서버를 설계·구현·테스트·평가하는 개발 가이드. Python(FastMCP) / Node·TypeScript(MCP SDK) 양쪽을 다룬다. 다음 상황에서 반드시 이 스킬을 사용할 것 사용자가 'MCP 서버', 'MCP 만들기', 'MCP 빌드', '커넥터', '외부 API 연동', '도구 서버', 'tool server', 'FastMCP', 'MCP SDK', 'Slack 연동 서버', 'Google 연동 서버', '행사 등록 시스템 연동', 'CRM 연동', 'LLM이 우리 데이터/도구 쓰게'를 언급할 때. MICE 워크플로우(mice-estimate 견적·mice-dashboard KPI·mice-meeting-minutes 회의록)를 외부 에이전트가 읽고 쓰게 하는 커넥터를 만들 때. ChainPayload/v1 JSON을 주고받는 도구를 설계할 때. 형제 경계 — 이것은 *외부 서비스 연동 서버를 개발하는 가이드*다. 산출물 색·테마·디자인 토큰과는 무관하므로 '테마/팔레트/오버레이'는 jc-theme-factory, '디자인 토큰'은 jc-design-system 영역이며 여기서 다루지 않는다. 결론·문서 적대적 검증은 jc-redteam, 데이터 봉투 규약 정의는 jc-design-system/chaining-protocol 영역. 단발성 스크립트 한 개를 짜는 일에는 과하다 — 재사용 가능한 도구 서버(다수 도구·외부 인증·페이지네이션)를 만들 때만 쓴다. 실행형 지시는 실행 전 jc-prompt-builder 브리프를 거친다.
version: "v1.0.1"
license: Complete terms in LICENSE.txt
---

# JC MCP Server Development Guide

원본 프리셋 `mcp-builder`의 기술 골격(4단계 워크플로우·SDK 가이드·평가 하니스)을 **그대로 보존**하면서, 도입부·용례·트리거만 jc 생태계의 **MICE 도구 커넥터** 관점으로 프레이밍한 경량 개조판이다. 기술 본문(`reference/` 4종·`scripts/`)은 원문 영어 그대로이며, 이 SKILL.md가 "왜·언제 MICE 맥락에서 쓰는가"를 한국어로 안내한다.

## Overview

LLM·외부 에이전트가 외부 서비스나 mice-* 산출 데이터를 **도구(tool)로 다루게** 해주는 MCP 서버를 만든다. MCP 서버의 품질은 "LLM이 이 서버로 실제 업무를 얼마나 잘 끝내는가"로 측정한다.

**이 스킬이 겨냥하는 MICE 커넥터 용례:**

- **mice 데이터 노출** — `mice-estimate`의 견적·산출내역이나 `mice-dashboard`의 KPI/실적을, 외부 LLM/도구가 조회·집계·질의할 수 있도록 읽기 도구로 노출하는 서버. (예: `estimate_get_breakdown`, `dashboard_list_kpis`)
- **외부 서비스 커넥터** — Slack·Google Drive/Calendar·CRM·행사 등록(registration) 시스템을 MICE 운영 워크플로우에 묶는 커넥터. (예: `slack_send_message`, `gcal_create_event`, `registration_list_attendees`)
- **체이닝 도구** — 도구의 입력/출력으로 `ChainPayload/v1` JSON 봉투를 주고받아, 다른 mice-* 스킬이 만든 데이터를 외부 에이전트가 소비·생산하게 하는 도구 설계.

> **언제 쓰지 말아야 하나:** 산출물의 색·테마는 jc-theme-factory / jc-design-system, 결론·문서 검증은 jc-redteam 영역이다. 또 단발성 변환 스크립트 1개로 끝나는 일이면 MCP 서버는 과하다 — 재사용·다수 도구·외부 인증·페이지네이션이 필요할 때만 서버로 만든다.

### MICE 커넥터 ↔ ChainPayload/v1

MICE 데이터를 다루는 도구는 입력 검증·출력 형식에서 생태계 데이터 규약 `ChainPayload/v1`을 따를 수 있다. 봉투 구조(`$schema`/`source`/`version`/`generatedAt`, 평탄 페이로드)와 입력 라우팅(`detect_input_source`)의 **정본**은 `jc-design-system/references/chaining-protocol.md`이며, 본 스킬은 그 규약을 재정의하지 않고 참조만 한다.

- 도구가 mice-* 산출 JSON을 **입력으로 받을 때**: `$schema == "ChainPayload/v1"` 확인 → `source`로 페이로드 파싱 분기 (정본 §6·§7). 봉투가 아니면 일반 파일/인라인 데이터로 처리.
- 도구가 데이터를 **출력으로 낼 때**: 봉투 메타(camelCase)를 최상위에 두고 스킬 고유 페이로드를 평탄하게 공존시킨다 (정본 §2·§3).
- Pydantic/Zod 입력 스키마에 봉투 필드를 반영하면, 외부 에이전트가 MICE 데이터를 일관되게 주고받을 수 있다.
- 회사·개인 식별 정보는 봉투·페이로드·예시 어디에도 **하드코딩하지 않는다** (`RULE-NO-COMPANY`). 클라이언트/공급자/발주처 값은 외부 주입 변수·환경변수로만 처리한다. (정본 §6-3)

---

# Process

## 🚀 High-Level Workflow

고품질 MCP 서버 제작은 4단계로 진행한다. (원본 기술 골격 유지)

### Phase 1: Deep Research and Planning

#### 1.1 Understand Modern MCP Design

**API Coverage vs. Workflow Tools:**
Balance comprehensive API endpoint coverage with specialized workflow tools. Workflow tools can be more convenient for specific tasks, while comprehensive coverage gives agents flexibility to compose operations. Performance varies by client—some clients benefit from code execution that combines basic tools, while others work better with higher-level workflows. When uncertain, prioritize comprehensive API coverage.

*(MICE 적용 노트: 예컨대 mice-dashboard 커넥터라면 `dashboard_list_kpis`·`dashboard_get_round` 같은 기본 조회 도구를 폭넓게 덮되, "최근 행사 실적 요약" 같은 자주 쓰는 작업은 워크플로우 도구로 따로 두는 식으로 균형을 잡는다.)*

**Tool Naming and Discoverability:**
Clear, descriptive tool names help agents find the right tools quickly. Use consistent prefixes (e.g., `github_create_issue`, `github_list_repos`) and action-oriented naming.

*(MICE 적용 노트: 서비스 접두사를 mice 도메인에 맞춰 일관화한다 — `estimate_*`, `dashboard_*`, `slack_*`, `gcal_*`, `registration_*`.)*

**Context Management:**
Agents benefit from concise tool descriptions and the ability to filter/paginate results. Design tools that return focused, relevant data. Some clients support code execution which can help agents filter and process data efficiently.

**Actionable Error Messages:**
Error messages should guide agents toward solutions with specific suggestions and next steps.

#### 1.2 Study MCP Protocol Documentation

**Navigate the MCP specification:**

Start with the sitemap to find relevant pages: `https://modelcontextprotocol.io/sitemap.xml`

Then fetch specific pages with `.md` suffix for markdown format (e.g., `https://modelcontextprotocol.io/specification/draft.md`).

Key pages to review:
- Specification overview and architecture
- Transport mechanisms (streamable HTTP, stdio)
- Tool, resource, and prompt definitions

#### 1.3 Study Framework Documentation

**Recommended stack:**
- **Language**: TypeScript (high-quality SDK support and good compatibility in many execution environments e.g. MCPB. Plus AI models are good at generating TypeScript code, benefiting from its broad usage, static typing and good linting tools)
- **Transport**: Streamable HTTP for remote servers, using stateless JSON (simpler to scale and maintain, as opposed to stateful sessions and streaming responses). stdio for local servers.

**Load framework documentation:**

- **MCP Best Practices**: [📋 View Best Practices](./reference/mcp_best_practices.md) - Core guidelines

**For TypeScript (recommended):**
- **TypeScript SDK**: Use WebFetch to load `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript Guide](./reference/node_mcp_server.md) - TypeScript patterns and examples

**For Python:**
- **Python SDK**: Use WebFetch to load `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python Guide](./reference/python_mcp_server.md) - Python patterns and examples

#### 1.4 Plan Your Implementation

**Understand the API:**
Review the service's API documentation to identify key endpoints, authentication requirements, and data models. Use web search and WebFetch as needed.

*(MICE 적용 노트: 외부 서비스(Slack/Google/CRM/등록 시스템)는 공식 API 문서로, mice-* 데이터를 노출할 땐 해당 스킬의 chaining 문서로 데이터 모델을 파악한다.)*

**Tool Selection:**
Prioritize comprehensive API coverage. List endpoints to implement, starting with the most common operations.

---

### Phase 2: Implementation

#### 2.1 Set Up Project Structure

See language-specific guides for project setup:
- [⚡ TypeScript Guide](./reference/node_mcp_server.md) - Project structure, package.json, tsconfig.json
- [🐍 Python Guide](./reference/python_mcp_server.md) - Module organization, dependencies

#### 2.2 Implement Core Infrastructure

Create shared utilities:
- API client with authentication
- Error handling helpers
- Response formatting (JSON/Markdown)
- Pagination support

#### 2.3 Implement Tools

For each tool:

**Input Schema:**
- Use Zod (TypeScript) or Pydantic (Python)
- Include constraints and clear descriptions
- Add examples in field descriptions

**Output Schema:**
- Define `outputSchema` where possible for structured data
- Use `structuredContent` in tool responses (TypeScript SDK feature)
- Helps clients understand and process tool outputs

**Tool Description:**
- Concise summary of functionality
- Parameter descriptions
- Return type schema

**Implementation:**
- Async/await for I/O operations
- Proper error handling with actionable messages
- Support pagination where applicable
- Return both text content and structured data when using modern SDKs

**Annotations:**
- `readOnlyHint`: true/false
- `destructiveHint`: true/false
- `idempotentHint`: true/false
- `openWorldHint`: true/false

> **MICE 데이터 규약 노트:** mice-* 데이터를 입출력하는 도구라면 입력/출력 스키마에 `ChainPayload/v1` 봉투를 반영한다(위 "MICE 커넥터 ↔ ChainPayload/v1" 참조). 봉투/페이로드/예시에 회사·실명 하드코딩 금지(`RULE-NO-COMPANY`) — 인증 정보·클라이언트 값은 환경변수/외부 주입으로만.

---

### Phase 3: Review and Test

#### 3.1 Code Quality

Review for:
- No duplicated code (DRY principle)
- Consistent error handling
- Full type coverage
- Clear tool descriptions

#### 3.2 Build and Test

**TypeScript:**
- Run `npm run build` to verify compilation
- Test with MCP Inspector: `npx @modelcontextprotocol/inspector`

**Python:**
- Verify syntax: `python -m py_compile your_server.py`
- Test with MCP Inspector

See language-specific guides for detailed testing approaches and quality checklists.

---

### Phase 4: Create Evaluations

After implementing your MCP server, create comprehensive evaluations to test its effectiveness.

**Load [✅ Evaluation Guide](./reference/evaluation.md) for complete evaluation guidelines.**

#### 4.1 Understand Evaluation Purpose

Use evaluations to test whether LLMs can effectively use your MCP server to answer realistic, complex questions.

#### 4.2 Create 10 Evaluation Questions

To create effective evaluations, follow the process outlined in the evaluation guide:

1. **Tool Inspection**: List available tools and understand their capabilities
2. **Content Exploration**: Use READ-ONLY operations to explore available data
3. **Question Generation**: Create 10 complex, realistic questions
4. **Answer Verification**: Solve each question yourself to verify answers

#### 4.3 Evaluation Requirements

Ensure each question is:
- **Independent**: Not dependent on other questions
- **Read-only**: Only non-destructive operations required
- **Complex**: Requiring multiple tool calls and deep exploration
- **Realistic**: Based on real use cases humans would care about
- **Verifiable**: Single, clear answer that can be verified by string comparison
- **Stable**: Answer won't change over time

#### 4.4 Output Format

Create an XML file with this structure:

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>
<!-- More qa_pairs... -->
</evaluation>
```

> **MICE 적용 노트:** 견적/KPI 커넥터라면 "특정 행사의 항목별 합계", "전년 대비 참가자 증감"처럼 *읽기 전용·검증 가능·안정적인* 질문 10개를 만들고, 정답은 도구를 직접 호출해 스스로 검산한다. 평가 실행은 `scripts/evaluation.py`(하니스) + `scripts/connections.py`(전송) 사용.

---

# Reference Files

## 📚 Documentation Library

개발 중 필요할 때 로드한다. (원본 4종 — 영문 기술 문서 그대로 보존)

### Core MCP Documentation (Load First)
- **MCP Protocol**: Start with sitemap at `https://modelcontextprotocol.io/sitemap.xml`, then fetch specific pages with `.md` suffix
- [📋 MCP Best Practices](./reference/mcp_best_practices.md) - Universal MCP guidelines including:
  - Server and tool naming conventions
  - Response format guidelines (JSON vs Markdown)
  - Pagination best practices
  - Transport selection (streamable HTTP vs stdio)
  - Security and error handling standards

### SDK Documentation (Load During Phase 1/2)
- **Python SDK**: Fetch from `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- **TypeScript SDK**: Fetch from `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`

### Language-Specific Implementation Guides (Load During Phase 2)
- [🐍 Python Implementation Guide](./reference/python_mcp_server.md) - Complete Python/FastMCP guide with:
  - Server initialization patterns
  - Pydantic model examples
  - Tool registration with `@mcp.tool`
  - Complete working examples
  - Quality checklist

- [⚡ TypeScript Implementation Guide](./reference/node_mcp_server.md) - Complete TypeScript guide with:
  - Project structure
  - Zod schema patterns
  - Tool registration with `server.registerTool`
  - Complete working examples
  - Quality checklist

### Evaluation Guide (Load During Phase 4)
- [✅ Evaluation Guide](./reference/evaluation.md) - Complete evaluation creation guide with:
  - Question creation guidelines
  - Answer verification strategies
  - XML format specifications
  - Example questions and answers
  - Running an evaluation with the provided scripts

### Scripts (평가 하니스)
- `scripts/evaluation.py` — MCP 서버 평가 하니스 (Claude로 질문셋 실행)
- `scripts/connections.py` — stdio/SSE/streamable-HTTP 전송 추상화 (evaluation.py가 import)
- `scripts/example_evaluation.xml` — 평가 XML 예시
- `scripts/requirements.txt` — `anthropic`, `mcp` 의존성 (`pip install -r scripts/requirements.txt`)

---

# 생태계 연결

- **데이터 입출력**: mice-* 산출 JSON 소비/배출은 `ChainPayload/v1` 봉투를 따른다. 정본: `jc-design-system/references/chaining-protocol.md` (봉투 §2·§3, 입력 라우팅 §7).
- **검증**: 완성된 MCP 서버 설계 판단·문서를 적대적으로 재검증하려면 `jc-redteam`에 넘긴다(결론·문서=3축). 원본의 "fresh Claude로 도구를 평가" 절차는 Phase 4의 `scripts/evaluation.py` 하니스로 수행한다.
- **디자인 무관**: 본 스킬은 코드 인프라라 jc 디자인 토큰 의존이 없다. 색·테마가 필요한 산출물은 jc-theme-factory / jc-design-system 영역.
- **공통 룰**: `RULE-NO-COMPANY` 적용 — 서버 코드·도구 예시·평가 데이터에 회사명·실명 하드코딩 금지, 외부 주입 변수/환경변수만. 정본 `jc-design-system/references/shared-rules.md`.

# 파일 구조

```
jc-mcp-builder/
├── SKILL.md                       # 본 파일 — jc/MICE 프레이밍 진입점
├── LICENSE.txt                    # 원본 라이선스 (그대로 복사)
├── reference/                     # 원본 4종 영문 기술 문서 (그대로 보존)
│   ├── mcp_best_practices.md      # MCP 네이밍·응답형식·페이지네이션·전송·보안
│   ├── node_mcp_server.md         # TypeScript/MCP SDK 구현 가이드 + 예제
│   ├── python_mcp_server.md       # Python/FastMCP 구현 가이드 + 예제
│   └── evaluation.md              # 평가 질문 작성·검증·XML 포맷·실행법
└── scripts/                       # 원본 그대로 복사 (평가 하니스)
    ├── evaluation.py              # MCP 서버 평가 하니스
    ├── connections.py            # stdio/SSE/HTTP 전송 추상화
    ├── example_evaluation.xml     # 평가 XML 예시
    └── requirements.txt           # anthropic, mcp
```
