---
name: jc-landing-page
version: "v1.1.0"
description: jc-design-system 테마 기반 B2B 모바일 최적화 랜딩페이지(ABM/리드젠/웨비나)를 단일 HTML 파일로 생성. 사용자가 "랜딩페이지", "랜딩", "LP", "리드 페이지", "신청 페이지", "웨비나 페이지", "ABM 페이지", "리포트 신청", "백서 다운로드", "세미나 모집" 등을 언급하거나, 특정 캠페인/리포트/웨비나/제품의 모바일 단일 페이지를 만들어달라고 요청할 때 트리거. 고정비율 스케일링(375px·rem)·Pretendard·Google Apps Script 폼 백엔드가 표준 산출물. 색·타이포는 jc-design-system 정본 + 캠페인별 client-overlays로 주입. **1차 산출물 직후 jc-redteam의 'LP 마케팅 패널' 모드(5인 마케터 + 3인 고객)로 검증해 최종본을 도출 — 검증 생략 불가.**
---

# JC B2B 모바일 랜딩페이지 표준

B2B 캠페인용 모바일 랜딩페이지를 만들 때 따르는 표준이다. **단일 HTML 파일**로 산출하며, Google Apps Script를 백엔드로 사용한다. 색·타이포는 **jc-design-system 정본**을 기본으로 하고, 캠페인별 컬러는 jc-design-system의 **client-overlays**로 토글한다.

---

## 0. 작업 시작 전 인풋 체크 (필수 절차)

이 skill이 발동되면 **코드 작업을 시작하기 전에 반드시 아래 체크리스트를 사용자에게 노출**한다.
빠른 답변이 들어오더라도, 누락된 항목이 있으면 **무엇이 빠졌는지 명시적으로 알려주고** 추가 정보를 요청한다.

작업자가 가이드 문서나 자료를 한 번에 첨부할 수도 있고, 항목별로 답할 수도 있다.
첨부 자료에서 항목이 채워지면 OK 표시 후, 빈 항목만 추가로 묻는다.

### 0.1 캠페인 유형 먼저 확인

**가장 먼저 묻는 질문 (이게 정해져야 추가 인풋 범위가 결정됨):**

> "이번 랜딩페이지는 어떤 용도인가요?
> A) 리드마그넷 다운로드용 (리포트/백서 신청 → 자료 발송)
> B) ABM 컨택 전환용 (미팅 제안 / 상담 신청 / 데모 요청)
> C) A+B 혼합형 (자료 다운로드 + 후속 상담 제안 동시)"

### 0.2 공통 인풋 체크리스트 (모든 유형 공통)

| # | 항목 | 설명 | 누락 시 처리 |
|---|---|---|---|
| 1 | **고객사 / 캠페인명** | 어느 고객사 / 어떤 캠페인용인지 | 작업자에게 질문 |
| 2 | **타겟 (Persona)** | 누구에게 보여줄 페이지인지. 직급/직무/산업/회사 규모. 가능하면 "어떤 리스트로 전달되는지"까지 (예: 칸타 웨비나 신청자 670명, 마케팅팀장 이상 50%) | 작업자에게 질문 |
| 3 | **핵심 메시지 / 후킹 카피** | Hero 섹션 한 줄. 없으면 타겟·자료 내용 기반으로 클로드가 3개 제안 후 작업자가 선택 | 클로드가 제안 |
| 4 | **고객사 컬러 / 톤** | 브랜드 컬러 (HEX 또는 이미지), 분위기 (신뢰감/혁신/따뜻함 등) | 작업자에게 질문 — 절대 임의로 정하지 않는다 |
| 5 | **로고 / 이미지 자료** | 고객사 로고, 발표자 사진, 차트 이미지 등 | 자료 첨부 요청 |
| 6 | **폼 수집 항목** | 기본(이름/회사/직책/이메일/전화) 외에 추가로 받고 싶은 정보 (관심 분야, 도입 시기, 예산 등) | 기본값으로 진행, 작업자 확인 |
| 7 | **CTA 문구** | "리포트 받기", "미팅 신청하기", "30분 무료 진단" 등. 캠페인 유형에 따라 다름 | 클로드가 유형 기반으로 제안 |
| 8 | **Google Apps Script URL** | 폼 백엔드 URL. 작업자가 GAS 배포 후 제공. 처음엔 플레이스홀더로 진행 가능 | 플레이스홀더로 진행, 작업자에게 명시 |
| 9 | **삽입할 영상 유무** | Hero에 배경으로 들어갈 영상이 있는지 / 만들 계획이 있는지. **있다면 9번 섹션의 표준 즉시 안내한다.** | 작업자에게 질문 — 영상 있다고 답하면 0.6 절차 적용 |

### 0.3 유형별 추가 인풋

#### A. 리드마그넷 다운로드용 추가 항목

| # | 항목 | 설명 |
|---|---|---|
| A1 | **리드마그넷 자료 파일** | 실제로 제공할 리포트/백서 PDF (이걸 미리 받아야 페이지에서 자료의 핵심 인사이트를 티저로 노출 가능) |
| A2 | **자료 미리보기 / 목차** | 페이지에 노출할 미리보기 이미지, 핵심 챕터, 데이터 한 줄 요약. 자료를 받았다면 클로드가 추출 가능 |
| A3 | **자료 발송 방식** | 신청 즉시 다운로드 링크 노출 / 이메일로 자동 발송 / 영업 검토 후 수동 발송 — 어느 쪽인지 |
| A4 | **자료 발송용 이메일 템플릿** | 자동 발송이면 이메일 본문 필요. 없으면 클로드가 별도 이메일 템플릿을 작성해 제공 |

#### B. ABM 컨택 전환용 추가 항목

| # | 항목 | 설명 |
|---|---|---|
| B1 | **제안하는 미팅/상담의 정체** | 30분 무료 진단 / 1시간 솔루션 데모 / 임원 미팅 / 사례 공유 세션 등 무엇을 약속하는지 |
| B2 | **미팅에서 다룰 내용 / Agenda** | 페이지에 "이런 걸 얻으실 수 있습니다" 형태로 노출할 가치 약속 |
| B3 | **담당자 / 발표자 정보** | 미팅 상대가 누구인지 (직책, 약력, 사진). B2B에선 누구를 만나는지가 큰 신뢰 요소 |
| B4 | **사후 팔로업 프로세스** | 신청 → 몇 시간 내 연락 / 어떤 채널로 / 누가 연락 — 작업자가 알고 있어야 페이지의 약속 카피를 정확히 쓸 수 있음 |
| B5 | **레퍼런스 / 신뢰 요소** | 기존 고객사 로고, 케이스 스터디, 데이터(예: "도입사 평균 리드 전환율 X% 향상") |

#### C. 혼합형 (A+B 모두) 추가 항목

- A1~A4 + B1~B5 **모두** 필요.
- **다만 페이지 구조에서 우선순위가 무엇인지** 확인:
  - "자료가 메인, 미팅은 옵션" (1차 전환: 다운로드 / 2차 전환: 미팅 신청)
  - "미팅이 메인, 자료는 미끼" (자료는 다운로드 게이트로만 활용, 핵심 CTA는 미팅)
- 폼 안에 "미팅도 함께 신청하시겠어요?" 토글/체크박스 자주 사용

### 0.4 체크리스트 노출 방식 (표준 응답 템플릿)

skill이 발동되면 클로드는 다음 형식으로 응답한다:

```
랜딩페이지 작업 들어가기 전에, 표준 인풋 체크리스트로 한 번 정리할게요.
첨부해주신 자료에서 채워진 항목은 ✅, 추가로 필요한 항목은 ❓ 표시합니다.

[캠페인 유형]
❓ A) 리드마그넷 다운로드용 / B) ABM 컨택 전환용 / C) 혼합형 — 어떤 유형인가요?

[공통 항목]
✅ 1. 고객사 / 캠페인명: (자료에서 파악된 내용)
❓ 2. 타겟 (Persona):
✅ 3. 핵심 메시지:
❓ 4. 고객사 컬러 / 톤:
... (이하 9번까지)

❓ 9. 삽입할 영상이 있나요?
   - 있다 → 영상 사양 안내 (모바일 9:16 세로형 필수)
   - 없다 → 일반 정적 hero로 진행
   - 만들 예정 → 영상 제작 가이드 먼저 제공

[유형별 추가 항목]
(유형이 정해지면 그에 맞는 항목 노출)

답변 주시는 대로 작업 들어가겠습니다.
빠른 진행을 원하시면 "기본값으로 진행"이라고 말씀해주세요 —
빠진 항목은 클로드 판단으로 채우되, 4번 컬러처럼 임의로 정하면 안 되는 항목은 다시 묻겠습니다.
```

### 0.5 "기본값으로 진행" 모드

작업자가 "빨리", "기본값으로", "그냥 시작해" 같은 표현을 쓰면:
- **임의로 정할 수 있는 항목**(폼 수집 항목, CTA 문구, 미리보기 구성 등)은 클로드가 판단해서 진행
- **임의로 정할 수 없는 항목**(고객사 컬러 / 타겟 / 리드마그넷 실제 파일 / 미팅 약속 내용 / 영상 사양 등)은 **반드시 다시 묻는다**
- 빠진 채로 시작한 항목은 산출물 전달 시 "이 부분은 플레이스홀더로 두었으니 확인 부탁드립니다"로 명시

### 0.6 영상 삽입 답변별 후속 조치 (9번 항목 후속)

작업자가 9번 항목에 응답한 후 처리 분기:

#### "영상 있다 — 이미 만들어져 있다"
1. **영상 파일 첨부 요청**
2. **영상 사양 검증** (ffprobe 또는 메타정보 확인):
   - 종횡비가 **9:16 (세로)** 인가? → 아니면 9.1 경고 표시
   - 해상도 720x1280 이상 / 1080x1920 이하인가?
   - 길이 5~15초인가?
   - 오디오 트랙이 있는가? → 있으면 제거 안내
3. **검증 통과** → 9번 섹션의 통합 표준대로 hero에 풀블리드 배경으로 임베드
4. **검증 실패** → 9.1 가이드 노출 후 작업자에게 재제작 권유 또는 차선책(레터박스/크롭) 합의

#### "영상 있다 — 만들 계획이다 (헉스필드/AI 영상 등)"
**즉시 9.1 가이드를 노출**한다. 영상이 만들어진 후에 작업을 시작하지 말고, **사양을 먼저 알려주고** 작업자가 그 사양대로 영상을 만들도록 한다. 사양을 모르고 만들면 16:9 가로 영상이 나와서 짜깁기 후처리만 늘어남.

#### "영상 없다"
9번 섹션을 건너뛰고 일반 정적 hero로 진행.

---

## 1. 절대 규칙 (Non-negotiable)

### 1.1 회색 텍스트 금지
- **본문 텍스트에 회색 계열(`#666`, `#888`, `#999`, `gray-400~600`, `rgba(0,0,0,0.5)` 등)을 절대 사용하지 않는다.**
- 이유: 모바일 화면에서 잘 안 보이고, 디스플레이 밝기·각도에 따라 가독성이 무너진다.
- 강조도가 다른 본문이 필요한 경우:
  - **밝은 배경에서는** → 메인 텍스트 색(jc-design-system `--jc-text #1A1D24`) 그대로 유지하되 **font-weight 또는 font-size로 위계를 만든다.**
  - **어두운 배경에서는** → **흰색(`#ffffff`) 또는 jc 다크 텍스트(`#E8ECF2`)를 그대로 사용한다.** 회색 흰색(`#ccc`, `#aaa` 등)으로 약화시키지 않는다. 보조 텍스트는 흰색 + `opacity: 0.85` 정도까지만 허용 (그 이하 금지).
- 단, **placeholder 텍스트, disabled 상태, 보더 라인, 구분선**은 회색 허용.

### 1.2 고정 비율 스케일링 (반응형 X)
- **기준 폭: 375px** (iPhone SE / 갤럭시 일반형 기준)
- 디자인 기준 폭에서 보이는 모든 요소의 비율·위치·줄바꿈이 **모든 화면 크기에서 동일하게 유지**되어야 한다.
- 구현 방식: `viewport` 메타태그 + 루트 폰트 사이즈를 화면 폭에 비례시키는 방식 (아래 5번 항목 참조).
- **미디어 쿼리로 레이아웃을 다르게 짜는 일반 반응형 방식은 사용하지 않는다.**
- 데스크톱(태블릿/PC)에서 열린 경우: **모바일 화면 그대로**, 가운데 정렬 + 좌우 회색/검정 배경 처리. PC용 별도 레이아웃을 만들지 않는다.

### 1.3 줄바꿈 처리
- 디자인 시안에서 잡은 줄바꿈이 디바이스 폭에 따라 깨지지 않도록 한다.
- **권장 방식 (우선순위 순):**
  1. **강제 줄바꿈이 꼭 필요한 자리에만 `<br>`** — 카피의 의도된 호흡을 살릴 곳
  2. **줄바꿈 자체를 어색하지 않게 카피를 다듬어 자연스럽게 흐르도록** — 강제 줄바꿈이 어색해질 것 같으면 차라리 한 줄로 흐르게
  3. 단어 단위 줄바꿈 보호가 필요한 경우 `<span style="white-space: nowrap;">중요한 구절</span>` 활용
- 1.2의 고정 비율 스케일링이 적용되면 줄바꿈은 모든 화면에서 동일하게 유지되므로, 한 번 잡아두면 안전하다.

### 1.4 개인정보 수집·이용 동의 필수
- 폼이 있는 모든 페이지에 **개인정보 수집·이용 동의 체크박스를 반드시 포함한다.**
- 표준 문구는 4번 항목 참조.

---

## 2. 기본 기술 스택

- **단일 HTML 파일** (CSS, JS 모두 인라인/내장)
- **폰트**: Pretendard CDN (jc-design-system 표준 폰트)
  ```html
  <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css" />
  ```
  → `font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, system-ui, sans-serif;`
- **폼 백엔드**: Google Apps Script (POST endpoint, JSON body)
- **버튼·UI 인터랙션**: 바닐라 JS (라이브러리 최소화)
- **이미지**: 가능하면 Base64 인라인 또는 CDN URL. 외부 이미지 사용 시 차후 깨짐 위험 명시.
  - 이미지 에셋은 jc-design-system의 RULE-VISUAL-ROUTING을 따른다 (사진/래스터=Higgsfield, 표·다이어그램·차트=Claude 자체).

---

## 3. 페이지 구조 표준

기본 흐름 (위에서 아래 순서):

1. **Hero 섹션** — 카피 1~2줄 + 핵심 가치 한 줄 + 시각적 후킹 (배경, 일러스트, 영상 풀블리드 등) — 영상 있으면 9번 섹션 적용
2. **문제 제기 / 페인포인트** — 타겟의 현재 상황을 짚어주는 섹션
3. **솔루션 / 제공 내용** — 무엇을 어떻게 제공하는지
4. **차별점 / 신뢰 요소** — 데이터, 레퍼런스, 발표자, 후기 등
5. **CTA 섹션 (폼)** — 신청/다운로드/문의 폼
6. **하단 푸터** — 회사 정보, 개인정보 처리방침 링크
7. **Sticky CTA 버튼** (하단 고정) — 페이지 어디에서나 폼으로 점프
8. **Bottom-sheet 모달** (선택) — Sticky CTA 클릭 시 폼이 바텀시트로 올라오는 형태도 자주 사용

---

## 4. 폼 표준

### 4.1 기본 필드 (B2B 기준)
- 이름 (필수)
- 회사명 (필수)
- 직책 / 부서 (필수 또는 선택, 캠페인에 따라)
- 이메일 (필수) — 회사 이메일 권장 안내
- 전화번호 (필수) — **자동 하이픈 처리 JS 포함**
- 캠페인별 추가 질문 (관심사, 도입 시기, 예산 등 — 캠페인에 따라)

### 4.2 전화번호 자동 하이픈 JS
```javascript
function autoHyphen(value) {
  return value.replace(/[^0-9]/g, '')
    .replace(/(^02|^0505|^1[0-9]{3}|^0[0-9]{2})([0-9]+)?([0-9]{4})$/,
      (m, p1, p2, p3) => p2 ? `${p1}-${p2}-${p3}` : `${p1}-${p3}`);
}
// input의 oninput 이벤트에 연결
```

### 4.3 개인정보 수집·이용 동의 (필수 포함)

**체크박스 + 동의 내용 펼침/접힘 구조**로 구현. 표준 문구:

```
[필수] 개인정보 수집·이용에 동의합니다.

수집 항목: 이름, 회사명, 직책, 이메일, 전화번호
수집 목적: 신청한 [리포트/웨비나/세미나/상담] 제공 및 관련 정보 안내,
          [발송 주체 회사명]의 B2B 마케팅 솔루션 안내
보유 기간: 수집일로부터 3년 (또는 동의 철회 시까지)

귀하는 동의를 거부할 권리가 있으며, 거부 시 신청이 제한될 수 있습니다.
```

체크 안 하면 제출 버튼 비활성화 또는 alert 처리.

### 4.4 폼 제출 처리 패턴
```javascript
async function submitForm(data) {
  try {
    const res = await fetch('GOOGLE_APPS_SCRIPT_WEB_APP_URL', {
      method: 'POST',
      mode: 'no-cors',  // GAS는 CORS 응답을 못 주므로 필요
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(data)
    });
    // no-cors 모드에서는 response를 읽을 수 없으므로 성공 화면으로 즉시 전환
    showSuccessScreen();
  } catch (e) {
    alert('신청 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
  }
}
```

GAS 코드 자리에 플레이스홀더(`GOOGLE_APPS_SCRIPT_WEB_APP_URL`)를 명시적으로 남겨두고, 작업물 안내 시 "이 부분에 GAS 배포 URL을 넣으시면 됩니다"라고 명시한다.

---

## 5. 고정 비율 스케일링 구현 (핵심)

**이 섹션은 본 스킬의 가장 중요한 기술 표준이다.** 화면이 작아지든 커지든 디자인 기준 폭에서 잡힌 **폰트·여백·이미지·버튼의 비율이 그대로 유지**되어, 모든 요소가 함께 작아지거나 함께 커진다. iPhone SE에서 보든 갤럭시 노트에서 보든 폴더블 펼친 상태에서 보든 데스크톱에서 보든, **눈에 보이는 비율은 100% 동일**해야 한다.

### 5.0 작동 원리 (먼저 이해할 것)

핵심 트릭은 **`html`의 `font-size`(=1rem 기준값)를 화면 폭에 비례해서 실시간으로 바꾸는 것**이다.

- 기준 폭(375px)에서 → `html { font-size: 16px }` → `1rem = 16px`
- 화면이 320px이 되면 → `html { font-size: 13.65px }` → `1rem = 13.65px` (자동으로 모든 rem 값이 줄어듦)
- 화면이 414px이 되면 → `html { font-size: 17.66px }` → `1rem = 17.66px` (자동으로 모든 rem 값이 커짐)

즉 **rem으로 잡힌 모든 값은 화면 폭에 정확히 비례**한다. 폰트 18px → 1.125rem으로 적은 순간, 화면 폭과 함께 자동으로 스케일된다.

이게 작동하려면 다음 3개가 **모두** 만족되어야 한다:
1. viewport 메타태그가 `maximum-scale=1.0`으로 잠겨 있어야 (사용자 핀치줌으로 인한 깨짐 방지)
2. **모든 크기 단위가 rem** (px 섞이면 그 부분만 안 줄어들어 비율이 깨짐)
3. 루트 폰트 사이즈 스크립트가 `resize`·`orientationchange`에 모두 반응해야

### 5.1 viewport 메타태그 (반드시 이대로)
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
```

- `maximum-scale=1.0` + `user-scalable=no` → 사용자가 핀치줌해도 비율이 깨지지 않음 (스크립트로 폭 추적 중이므로 줌이 들어오면 계산이 어그러진다)
- `viewport-fit=cover` → 노치/펀치홀 영역까지 활용 (안전영역은 `env(safe-area-inset-*)`로 따로 처리)

### 5.2 루트 폰트 사이즈 스크립트 (표준 코드, 이대로 사용)

```html
<script>
  (function() {
    // ============ 비례 스케일링 설정 ============
    const BASE_WIDTH = 375;   // 디자인 기준 폭 (이 폭에서 1rem = 16px)
    const BASE_FONT = 16;     // 기준 폭에서의 1rem 값 (px)
    const MAX_WIDTH = 500;    // 이 폭 이상은 모바일 폭으로 고정 (데스크톱에서 가운데 정렬)
    const MIN_WIDTH = 280;    // 이 폭 이하로는 더 줄이지 않음 (구형 폴더블 접힘 상태 보호)
    // ===========================================

    function setRootFontSize() {
      // documentElement.clientWidth 사용 — window.innerWidth는 스크롤바 폭을 포함해 데스크톱에서 1~17px 오차 발생
      let width = document.documentElement.clientWidth || window.innerWidth;

      // 클램프: MIN ~ MAX 사이로 제한
      if (width > MAX_WIDTH) width = MAX_WIDTH;
      if (width < MIN_WIDTH) width = MIN_WIDTH;

      // 1rem = (현재 폭 / 기준 폭) * 기준 폰트
      // 예: 화면 폭 414 → (414 / 375) * 16 = 17.66px → 1rem = 17.66px
      const fontSize = (width / BASE_WIDTH) * BASE_FONT;
      document.documentElement.style.fontSize = fontSize + 'px';
    }

    // 최초 1회 실행 — DOM 파싱 직후 즉시 적용되어야 FOUC(스타일 깜빡임) 없음
    setRootFontSize();

    // 화면 회전·창 크기 변경·DPI 변경 모두 대응
    window.addEventListener('resize', setRootFontSize);
    window.addEventListener('orientationchange', setRootFontSize);

    // iOS Safari 주소창 표시/숨김으로 인한 viewport 변화 대응
    window.addEventListener('pageshow', setRootFontSize);
  })();
</script>
```

**스크립트 배치 위치 — 반드시 `<head>` 안, CSS 다음, 다른 모든 JS 앞.** body 안에 두면 FOUC가 생긴다.

### 5.3 CSS 안전망 (px 실수를 자동으로 잡아주는 보조 장치)

스킬 표준은 **모든 값을 rem으로 작성하는 것**이지만, 작업 중 px이 끼어들 수 있다. 다음 CSS를 항상 깔아두어 px 실수가 들어와도 비례가 무너지지 않게 한다.

```css
/* 1. 박스 모델 통일 */
*, *::before, *::after {
  box-sizing: border-box;
}

/* 2. 루트 폰트 사이즈 fallback — 스크립트가 로드되기 전에도 비례 비슷하게 작동 */
:root {
  /* 4vw → 화면 폭 400px에서 16px. 스크립트가 즉시 덮어쓰므로 거의 안 쓰이지만 보험. */
  font-size: clamp(13px, 4.2667vw, 21.33px);  /* MIN_WIDTH=280 → 13px, BASE=375 → 16px, MAX=500 → 21.33px */
}

/* 3. body는 1rem(=16px @375)을 기본 폰트로 */
body {
  font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  font-size: 1rem;              /* @375 = 16px */
  line-height: 1.5;
  color: #1A1D24;
  -webkit-text-size-adjust: 100%;   /* iOS Safari가 가로모드에서 폰트를 임의로 키우는 것 방지 */
  -webkit-font-smoothing: antialiased;
}

/* 4. 이미지·영상도 비례 스케일 — 부모 폭 100% + 자동 높이 */
img, video, svg, picture {
  max-width: 100%;
  height: auto;
  display: block;
}
```

### 5.4 모든 크기는 rem 단위로 작성 (절대 규칙)

- **px 대신 rem 사용** — 폰트, 패딩, 마진, width, height, border-radius, gap, top/left/right/bottom 좌표 등 **거의 모든 값**
- **px 허용 예외 (이것만)**:
  - `border: 1px solid` (보더 두께)
  - `box-shadow`의 blur radius 1~2px 미세값
  - `outline` 두께
- **% / vw / vh 사용 시 주의**:
  - `%`는 부모 기준이라 의도대로 비례 스케일됨 — OK
  - `vw`는 viewport 폭 기준이라 `MAX_WIDTH` 초과 시 데스크톱에서 너무 커짐 — **사용 금지** (단 5.3의 fallback에서만 예외)
  - `vh`는 hero 섹션 높이(`100vh`) 정도에만 쓰고, 내부 요소 크기에는 사용 금지
- 기준 폭 375px에서 디자인할 때 **px → rem 변환은 ÷16**

**px → rem 빠른 환산표 (디자인 자주 쓰는 값):**

| 디자인 px @375 | rem | 디자인 px @375 | rem |
|---|---|---|---|
| 8px | 0.5rem | 32px | 2rem |
| 10px | 0.625rem | 36px | 2.25rem |
| 12px | 0.75rem | 40px | 2.5rem |
| 14px | 0.875rem | 48px | 3rem |
| 16px | 1rem | 56px | 3.5rem |
| 18px | 1.125rem | 64px | 4rem |
| 20px | 1.25rem | 80px | 5rem |
| 24px | 1.5rem | 100px | 6.25rem |
| 28px | 1.75rem | 120px | 7.5rem |

### 5.5 컨테이너 구조

```css
html, body {
  margin: 0;
  padding: 0;
  background: #1A1D24;       /* 데스크톱에서 양 옆에 보이는 배경색 (캠페인 톤에 맞게 조정) */
  overflow-x: hidden;        /* 가로 스크롤 차단 */
}

.page-container {
  max-width: 31.25rem;       /* 500px → 데스크톱에서 모바일 폭으로 고정 */
  margin: 0 auto;            /* 가운데 정렬 */
  background: #ffffff;       /* 페이지 본문 배경 (캠페인에 따라 조정) */
  min-height: 100vh;
  overflow-x: hidden;
  position: relative;        /* sticky CTA 등 자식 absolute 기준점 */
}
```

### 5.6 Sticky CTA 버튼 처리

```css
.sticky-cta {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 31.25rem;          /* 500px → 페이지 컨테이너와 동일 */
  padding-bottom: env(safe-area-inset-bottom, 0);  /* iPhone 노치/홈바 영역 회피 */
  z-index: 100;
}
```

### 5.7 검증 방법 (작업 마무리 시 반드시 확인)

브라우저 개발자 도구에서 다음 3개 폭으로 토글하며 **모든 요소의 비율과 위치가 동일하게 줄어들고/커지는지** 확인:

| 검증 폭 | 확인 사항 |
|---|---|
| **320px** (iPhone SE 1세대) | 텍스트가 비례 축소되며 줄바꿈 동일. 버튼 터치 영역 충분 |
| **375px** (기준) | 디자인 그대로 |
| **414px** (iPhone Plus) | 비례 확대되어 여전히 디자인 비율 동일 |
| **500px** 이상 (데스크톱) | 모바일 폭으로 고정, 좌우 배경색 노출, 가운데 정렬 |

**비율이 깨졌다면 99% 원인은 px이 섞여 들어간 것이다.** 개발자 도구에서 의심 요소 클릭 → Computed 탭에서 단위가 px로 그대로 박혀있는지 확인.

### 5.8 흔한 실수 (Anti-patterns)

❌ **미디어 쿼리로 다른 폰트 사이즈 지정** — `@media (max-width: 360px) { font-size: 14px }` 같은 것. 본 스킬의 스케일링과 충돌한다. 미디어 쿼리는 **레이아웃 분기에 사용하지 않는다.**
❌ **`vw` 단위 남발** — 데스크톱에서 폭 고정이 풀려서 폰트가 거대해짐
❌ **`100vh` 내부 요소에 사용** — iOS Safari 주소창 변화로 깜빡거림. hero 높이 정도만 허용
❌ **`px`로 폰트 사이즈 지정** — 스케일링에서 빠짐. 그 텍스트만 비율 깨짐
❌ **`maximum-scale=1.0`을 빼고 빌드** — 사용자가 핀치줌하는 순간 모든 계산이 어그러짐
❌ **스크립트를 `<body>` 하단에 두기** — FOUC 발생, 로드 직후 큰 폰트가 0.3초쯤 보였다가 줄어듦

---

## 6. 컬러 / 브랜딩 (jc-design-system 정본)

**기본 팔레트는 jc-design-system 정본을 따른다** — accent `#2962FF`(CTA/링크), text `#1A1D24`, surface `#FFFFFF`, 다크 `#0A1220` 계열. (정본: `jc-design-system/references/signature-tokens.md` §6 / `mode-mapping.md` §3.)
- **캠페인별 컬러**는 jc-design-system의 **client-overlays**로 토글한다 — 시그니처 위에 캠페인 액센트만 덮어쓰는 방식. 임의 색 고정 대신 오버레이 변수로 주입.
- 컬러 가이드를 못 받았으면 톤(warm/cool·신뢰/혁신)을 확인하고 jc 오버레이로 제안한다.
- 회색 금지(1.1)는 어떤 오버레이에서도 그대로 적용. 공통 룰(WCAG·인쇄 라이트·개인정보)은 `jc-design-system/references/shared-rules.md` 정본 참조.

---

## 7. 산출물 체크리스트

페이지를 완성하고 사용자에게 전달하기 전, 다음 항목을 확인한다:

- [ ] **Step 0 인풋 체크리스트의 필수 항목이 모두 답변되었거나, 플레이스홀더로 처리한 항목이 작업자에게 명시되었다**
- [ ] **영상 삽입 여부(9번)가 확인되었고, 영상이 있다면 9번 섹션 표준대로 통합되었다**
- [ ] 본문 어디에도 회색 텍스트가 사용되지 않았다 (어두운 배경에서는 흰색)
- [ ] viewport 메타태그가 `maximum-scale=1.0, user-scalable=no, viewport-fit=cover`로 설정되어 있다
- [ ] 루트 폰트 사이즈 스크립트가 `<head>` 안 CSS 다음 위치에 있고 BASE_WIDTH = 375다
- [ ] 스크립트가 `resize`·`orientationchange`·`pageshow` 3개 이벤트에 모두 바인딩되어 있다
- [ ] 모든 크기가 rem 단위로 작성되어 있다 (border 1px / shadow blur 등 명시 예외만 px)
- [ ] vw 단위가 사용되지 않았다 (있다면 5.3 fallback 1줄만)
- [ ] 페이지 컨테이너 `max-width`가 rem 단위로 (`31.25rem` = 500px) 설정되어 있다
- [ ] **320px / 375px / 414px / 500px+ 4개 폭에서 모두 비율이 동일하게 유지된다 (개발자 도구로 토글 확인)**
- [ ] 데스크톱에서 열어도 모바일 폭으로 가운데 정렬되어 보인다
- [ ] 폼에 개인정보 수집·이용 동의 체크박스가 있고, 미체크 시 제출이 막힌다
- [ ] 전화번호 자동 하이픈이 동작한다
- [ ] Google Apps Script URL 자리에 플레이스홀더가 명시되어 있고 사용자에게 안내했다
- [ ] Sticky CTA가 있다면 페이지 컨테이너와 같은 max-width로 가운데 정렬된다
- [ ] 줄바꿈 의도가 모든 화면 폭에서 유지된다 (고정 비율이므로 자동 보장)
- [ ] **1차 HTML 완성 후 jc-redteam 'LP 마케팅 패널' 검증을 실행했는가?**
- [ ] **패널 결과를 반영한 v2 HTML이 별도 파일로 생성되었는가?**
- [ ] **변경 근거가 작업자에게 함께 전달되었는가?**

---

## 8. 작업 톤

- 작업 의뢰자는 시각적 결과물 기준으로 판단한다. 설명보다 결과물을 먼저 보여준다.
- 한 번에 끝까지 만들어 보여주고, 피드백 받아 빠르게 수정한다.
- 캠페인 컬러/이미지/문구 가이드가 없으면 추측하지 말고 짧게 확인한다.
- **1차 HTML이 완성되면 곧바로 jc-redteam 'LP 마케팅 패널' 검증을 자동 실행한다. 검증 없이 1차를 최종으로 제출하지 않는다.**

---

## 9. Hero 배경 영상 통합 표준 (영상이 있을 때 무조건 이대로)

작업자가 Hero에 영상을 넣겠다고 답한 순간, **무조건 이 섹션의 표준 그대로 통합한다.** 영상을 별도 박스에 넣거나, 컨테이너 안에 카드처럼 떡 박는 방식은 사용하지 않는다. **풀블리드(full-bleed) 배경 + 그라데이션 페이드** 방식만 사용한다.

### 9.1 작업자에게 먼저 알려줄 영상 사양 (Pre-production 가이드)

영상을 만들기 전에 작업자가 알아야 하는 것. 이미 만들어진 영상을 가져왔어도 이 사양을 충족해야 풀블리드 배경으로 깔린다.

**필수 사양:**

| 항목 | 사양 | 이유 |
|---|---|---|
| **종횡비** | **9:16 (세로형) 필수** | 모바일 풀스크린(세로) hero에 풀블리드로 깔리려면 세로 영상이어야 함. 16:9 가로 영상을 풀블리드로 깔면 양옆이 잘리거나 위아래에 빈 공간 생김. |
| **해상도** | 720×1280 또는 1080×1920 | 720p가 모바일에서 충분. 더 키우면 용량만 늘어남 |
| **길이** | 5~15초 (10초 권장) | 짧으면 임팩트 부족, 길면 로딩 부담 + 다시 보고 싶지 않게 됨 |
| **루프 친화** | 첫 프레임과 마지막 프레임이 시각적으로 유사 | 무한 반복 시 점프컷이 보이지 않게 |
| **오디오** | **불필요 (제거)** | 모바일 자동재생은 muted 필수. 오디오 트랙은 용량만 차지 |
| **용량** | 1MB 이하 권장 | 모바일 LTE에서 즉시 로딩되어야 함 (3G 환경 고려) |
| **코덱** | H.264 (Constrained Baseline + yuv420p) | 모든 브라우저에서 100% 호환. High profile은 일부 환경에서 재생 안 됨 |

**콘텐츠 구성 가이드 (작업자에게 영상 만들기 전 전달):**

```
영상 안에 보여줄 핵심 시각 요소는 영상 세로 35~70% 구간에 배치하세요.
이유: hero 페이지 상단(0~35%)에는 카피가 얹히고
     하단(70~100%)에는 CTA·Trust 요소가 얹히기 때문에
     그 영역은 그라데이션으로 가려집니다.
     실제로 사용자에게 보이는 영상 영역은 가운데 35%뿐입니다.

또한 모바일 화면이 좁기 때문에 좌우 양 끝의 요소는 잘릴 수 있습니다.
중요한 시각 요소는 화면 중앙에 배치하세요.
```

**AI 영상 생성 도구(헉스필드 등) 사용 시 프롬프트 명시 사항:**

```
Aspect ratio: 9:16 VERTICAL (mobile portrait, 720x1280)
Composition: Key visual elements positioned in the CENTER VERTICAL 35-70%
of the frame. Top 35% and bottom 30% will be obscured by page gradient
overlay. Do not place critical content in those zones.
No audio track required.
```

### 9.2 영상 후처리 표준 (FFmpeg)

작업자가 영상 파일을 가져오면 작업 시작 전에 다음 명령으로 후처리한다:

```bash
ffmpeg -i input.mp4 \
  -an \
  -c:v libx264 \
  -profile:v baseline \
  -level 3.0 \
  -pix_fmt yuv420p \
  -crf 28 \
  -preset slow \
  -movflags +faststart \
  -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black" \
  rejected.mp4
```

**옵션 의미:**
- `-an`: 오디오 트랙 완전 제거
- `-profile:v baseline + -pix_fmt yuv420p`: 모든 브라우저 호환성 100%
- `-crf 28`: 모바일에 충분한 화질, 용량 최소화
- `-movflags +faststart`: 메타데이터 앞으로 이동 → 스트리밍 즉시 시작
- `scale + pad`: 9:16이 아닌 영상이 들어와도 강제로 9:16에 맞춤 (검정 패딩)

### 9.3 표준 HTML 구조 (Hero 섹션)

```html
<section id="hero">
  <!-- Z0: 영상 - 풀블리드(전체 inset:0) -->
  <div class="hero-bg-wrap">
    <video class="hero-bgvid" autoplay muted loop playsinline preload="auto" disablepictureinpicture aria-hidden="true">
      <source src="video.mp4" type="video/mp4">
    </video>
  </div>

  <!-- Z1: 그라데이션 페이드 - 상단·하단을 가려서 카피·CTA 가독성 확보 -->
  <div class="hero-bg-fade"></div>

  <!-- Z2: 컬러 액센트 (선택) -->
  <div class="hero-color"></div>

  <!-- Z3: 상단 카피 -->
  <div class="hero-body">
    <div class="hero-kicker">...</div>
    <h1 class="hero-h1">...</h1>
    <div class="hero-sub">...</div>
  </div>

  <!-- Z3: 하단 CTA + Trust -->
  <div class="hero-bottom">
    <button class="cta">CTA 문구</button>
    <div class="hero-trust">...</div>
  </div>
</section>
```

### 9.4 표준 CSS (그대로 사용)

```css
/* Hero 컨테이너 - 모바일 풀스크린 */
#hero{
  position:relative;
  min-height:100svh;
  display:flex;
  flex-direction:column;
  justify-content:flex-start;
  padding:96px 20px 220px;
  background:#0A1220;        /* 영상 로딩 전 배경 */
  overflow:hidden;
}

/* 영상 컨테이너 - 풀블리드 (hero 전체 채움) */
.hero-bg-wrap{
  position:absolute;
  inset:0;                    /* hero 전체 영역 */
  z-index:0;
  overflow:hidden;
  background:#0A1220;
}

/* 영상 - 컨테이너 가득 채우고 느린 줌인 */
.hero-bgvid{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:cover;
  object-position:center 50%;  /* 영상 중앙이 hero 중앙에 오게 (콘텐츠에 따라 조정 가능) */
  transform-origin:50% 50%;
  transform:scale(1);
  animation:heroZoom 10s ease-out forwards;
}
@keyframes heroZoom{
  from{transform:scale(1)}
  to{transform:scale(1.15)}
}

/* 그라데이션 페이드 - 상단(카피) + 하단(CTA) 영역 가림 */
.hero-bg-fade{
  position:absolute;
  inset:0;
  z-index:1;
  pointer-events:none;
  background:linear-gradient(
    180deg,
    #0A1220 0%,
    #0A1220 calc(38% - 20px),                   /* 상단 38%까지 솔리드 */
    rgba(10,18,32,0.75) calc(50% - 20px),
    rgba(10,18,32,0.35) calc(68% - 20px),
    rgba(10,18,32,0) calc(82% - 20px),            /* 50~82%는 영상 노출 */
    rgba(10,18,32,0.4) 92%,
    rgba(10,18,32,0.9) 100%                       /* 하단 다시 짙게 */
  );
}

/* 컬러 액센트 - 좌상단 부드러운 빛 (선택) */
.hero-color{
  position:absolute;
  inset:0;
  z-index:2;
  background:radial-gradient(ellipse 70% 45% at 90% 5%, rgba(41,98,255,.18) 0%, transparent 60%);
  pointer-events:none;
}

/* 상단 카피 영역 - 영상 위로 */
.hero-body{
  position:relative;
  z-index:3;
  max-width:480px;
  width:100%;
}

/* 하단 CTA 영역 - 영상 위로 + 자체 검정 페이드 */
.hero-bottom{
  position:absolute;
  left:0;
  right:0;
  bottom:0;
  z-index:3;
  padding:0 20px 48px;
  background:linear-gradient(to top, #0A1220 0%, #0A1220 50%, rgba(10,18,32,.85) 100%);
}
```

### 9.5 절대 하지 말 것 (Anti-patterns)

다음 방식은 EOS·NICE 등의 케이스에서 명백히 잘못된 것으로 확인됨. 절대 사용 금지:

❌ **영상을 hero-body 안에 카드처럼 넣기** (`<video>` 위에 border-radius + box-shadow) → "박스가 박혀있는 느낌"
❌ **영상 영역을 50~75%로 제한** (`bottom:0; height:60%`) → 풀블리드가 안 됨, 박스 느낌
❌ **mask-image로 외곽 페이드** → "박힌 박스를 가리려는 짜깁기" 티가 남
❌ **filter:blur로 흐리게** → 영상의 분위기가 죽고, 굳이 영상 넣은 의미 없어짐
❌ **16:9 가로 영상을 풀블리드 시도** → 양옆 잘리고 위아래 빈 공간
❌ **그라데이션이 과채도/밝은 색** → jc 다크(`#0A1220`) 계열 저채도 톤이 시네마틱

### 9.6 영상이 16:9 가로형으로 이미 만들어진 경우 (Fallback)

이상적으로는 9.1대로 9:16로 다시 만드는 게 맞지만, 시간/비용상 어렵다면 다음 차선책을 작업자와 합의 후 적용:

**옵션 A: 가로 영상을 풀블리드로 깔되 일부만 보이게** (가장 흔한 차선책)
- `object-fit: cover` + `object-position`으로 영상 일부만 노출
- 핵심 시각 요소가 가운데에 있다면 `object-position: center center`
- 좌측 요소가 중요하면 `object-position: 30% center`
- 양옆이 잘리는 것은 감수

**옵션 B: 가로 영상을 hero 상단 절반에 배치 (레터박스식)**
- hero 상단 50%에만 영상, 하단은 일반 카피·CTA
- 영상은 정상 비율로 보이지만 EOS 같은 풀블리드 느낌은 아님

**옵션 C: 작업자에게 9:16 재제작 권유**
- 가장 좋은 결과물을 위해서는 재제작이 정답임을 명확히 알린다
- 9.1 가이드 다시 노출

어떤 차선책이든 **작업자에게 한계를 명시**한다: "16:9 가로 영상은 EOS 같은 풀블리드 느낌을 100% 재현할 수 없습니다. 이 부분 인지하고 진행하시겠습니까?"

### 9.7 산출물 검증 (영상 통합 시)

페이지 완성 후 영상 통합 부분 추가 체크:

- [ ] 영상이 9:16 세로형인가? (아니면 9.6 차선책 적용했고 작업자가 인지했나)
- [ ] 영상 용량이 1MB 이하인가? (FFmpeg 후처리 완료)
- [ ] 오디오 트랙이 제거되었나?
- [ ] H.264 Baseline + yuv420p로 인코딩되었나? (모바일 호환성)
- [ ] `inset:0` 풀블리드로 깔렸나? (박스 아님)
- [ ] mask-image나 filter:blur 같은 안티패턴 사용 안 했나?
- [ ] 상단 카피, 하단 CTA 영역이 그라데이션으로 가려져 가독성 확보되었나?
- [ ] 영상이 `autoplay muted loop playsinline`으로 모바일 자동재생 보장되나?
- [ ] 영상 로드 전에도 hero가 깔끔하게 보이나? (배경색 fallback)
- [ ] 영상이 무한 반복 시 점프컷이 어색하지 않은가?

---

## 10. 산출물 검증 — 'LP 마케팅 패널' (필수, 생략 불가)

**1차 HTML이 완성되면 곧바로 'LP 마케팅 패널'(5인 마케터 + 3인 고객)로 검증한다.** 검증 없이 1차를 최종으로 제출하지 않는다. (구 Phase 10 = MARKETING_AGENT.) 아래 요약만으로 **즉시 실행 가능**하며, **상세 절차·진행 규칙·검수 체크리스트의 정본은 `jc-redteam/references/lp-marketing-panel.md`** 다(DRY — 패널 본체는 jc-redteam 소유, 본 §10은 자기완결 실행 요약).

- **발동 시점**: Phase 0 완료 → 본 표준대로 1차 HTML 생성·노출 직후 자동. 작업자가 "검증 생략"을 명시한 경우에만 건너뜀.
- **진입 고지(한 줄)**: "1차 산출물 완성. 5인 마케터 + 3인 고객 패널로 최종본을 도출합니다."

**패널 구성 (즉시 실행용 요약):**
- 5인 마케터: 세스 고딘(메시지·차별점) · 닐 파텔(전환·데이터) · 조 풀리지(콘텐츠·신뢰자산) · 앤 핸들리(B2B 카피·줄바꿈) · 에이프릴 던포드(포지셔닝·타겟 명확성)
- 3인 고객: 의사결정권자(ROI·첫 3초 임팩트) · 실무자(실용성·영업콜 우려) · 결재자(비용·개인정보·리스크)

**6단계 (끊김 없이, 각 단계 `## N단계` 헤더로 구분):**
1) 산출물 1줄 요약 → 2) 5인 1차 토론→1차 합의안 → 3) 합의안 기반 LP 검토포인트 정리 → 4) 3인 고객 솔직 피드백(문제만) → 5) 5인 2차 토론→최종 액션리스트(우선순위1/2 + '유지'+근거) → 6) 액션 반영 **v2 HTML**(별도 파일 `[campaign]_lp_v2.html`) + '변경 근거' 섹션(어느 페르소나의 어떤 지적 반영)

**핵심 규칙**: 1발언 합의 금지(충돌이 가치) · 고객은 문제만(해결은 마케터) · 모든 피드백 수용 금지('유지'+근거 명시) · v2는 1차 대비 최소 1-2개 시그니처 변경. *(압축 모드·고객 페르소나 상세·전체 체크리스트는 정본 참조.)*

> 일반 결론·문서 검증은 jc-redteam 기본 3축, **LP 산출물**은 위 패널을 쓴다. 역할은 분리(빌더 vs 최종 게이트), **검증 단계만 공유**한다.
