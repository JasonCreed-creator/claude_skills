# Report Structure — .docx 분석 보고서 구조

mice-rfp-analyzer가 생성하는 .docx 분석 보고서의 목차·섹션 구조·서식 정의.

---

## 파일 사양

- **파일명**: `rfp-analysis-report_[발주처]_[행사명]_[YYYYMMDD].docx`
- **분량**: 8~15페이지 (RFP 분량에 비례) / Quick 모드 4~6페이지
- **용지**: A4 세로
- **여백**: 상하좌우 25mm
- **본문 글꼴**: Pretendard 10.5pt
- **줄간격**: 1.4
- **색상**: jc-design-system signature 토큰 호출

---

## 표준 모드 — 섹션 구조

### 표지 (1페이지)

```
[발주처 로고 영역]   *발주처 로고는 사용자 제공 시에만 삽입, 없으면 생략

RFP 분석 보고서

[행사명]
[발주처명]

────────────────

분석 일자: YYYY-MM-DD
분석자:   [작업자명]
판정:    GO / GO 조건부 / HOLD / NO-GO  ← 색상 박스로 강조
종합 점수: X.X / 5.0
추정 승률: XX% (참고용)
```

### 1. Executive Summary (1페이지)

3분 안에 의사결정 가능한 핵심 정보만:

```
■ 결론
[GO/NO-GO 판정 + 핵심 사유 1줄]

■ 핵심 메시지 (GO인 경우)
1. [메시지 1]
2. [메시지 2]
3. [메시지 3]

■ 결정적 변수 Top 3
1. [변수 1 + 영향]
2. [변수 2 + 영향]
3. [변수 3 + 영향]

■ 즉시 대응 필요 사항
- [질의 사항 / 협상 포인트 / 자원 투입 결정]
```

### 2. RFP 개요 (0.5~1페이지)

| 항목 | 내용 |
|------|------|
| 발주처 | |
| 행사명 | |
| 행사 일자 | |
| 행사 장소 | |
| 행사 규모 | |
| 발주가 | |
| 제안 마감 | |
| 응찰 자격 | |

### 3. 7축 분석 — 본론 (5~10페이지)

#### 3-1. 요건 분석 (1~1.5페이지)
- 필수 요건 리스트 + 우리 측 대응 가능 여부
- 선택 요건 + 가산 요건
- **함정 키워드 경고** (별첨·협의·등 등)

#### 3-2. 평가 기준 분석 (1~1.5페이지)
- 평가 항목별 배점·가중치 표
- 우리 강점 영역 vs 평가 가중치 매핑 차트
- 표준 패턴 대비 발주처 의도 해석

#### 3-3. 리스크 분석 (1~2페이지)
- 독소 조항 등급별 정리표 (상/중/하)
- 영역별 분석 (책임·배상·변경권 등)
- 리스크 프리미엄 권고 (입찰가 영향)

#### 3-4. 경쟁 환경 분석 (0.5~1페이지)
- 응찰 자격 진입 장벽
- 예상 경쟁사 풀 (추정 명시)
- SWOT 매트릭스
- 차별화 포인트 도출

#### 3-5. 일정 압박 분석 (0.5페이지)
- 단계별 일정 + D-Day
- 압박 강도 표시
- 단계별 리스크 코멘트

#### 3-6. 예산 분석 (1페이지)
- 발주가 vs 추정 원가 비교
- 추정 마진율 + 표준 대비
- 입찰가 권고 시뮬레이션

#### 3-7. 전략 권고 (1~2페이지)
- 7축 종합 점수표
- GO/NO-GO 판정 + 사유
- 핵심 메시지 도출 로직
- 승률 추정 + 가정 명시

### 4. 부록 (1~2페이지)

#### 4-1. 추출 원문 발췌
RFP에서 핵심 조항 발췌 (페이지·조항 표기)

#### 4-2. 발주처 추가 질의 사항
질의 마감 전 발주처에 던질 질문 리스트

#### 4-3. 후속 액션 체크리스트
응찰 결정 시 1주차·2주차 액션 항목

---

## Quick 모드 — 섹션 구조 (4~6페이지)

```
표지 (1페이지)
↓
Executive Summary (1페이지)
↓
요건 분석 — 필수만 (1페이지)
↓
평가 기준 분석 (1~2페이지)
↓
전략 권고 — GO/NO-GO + 핵심 메시지 (1페이지)
```

---

## 서식 규칙

### 제목 위계
| 위계 | 글꼴 | 크기 | 색상 | 간격 |
|------|------|------|------|------|
| 표지 메인 | Pretendard ExtraBold | 32pt | Primary Navy | - |
| 표지 서브 | Pretendard SemiBold | 18pt | Dark Gray | - |
| 섹션 1단계 (1.) | Pretendard ExtraBold | 18pt | Primary Navy | 위 24pt 아래 12pt |
| 섹션 2단계 (1-1.) | Pretendard SemiBold | 14pt | Primary Navy | 위 18pt 아래 9pt |
| 섹션 3단계 | Pretendard SemiBold | 12pt | Dark Gray | 위 12pt 아래 6pt |
| 본문 | Pretendard | 10.5pt | Dark Gray | 줄간격 1.4 |
| 캡션 | Pretendard | 9pt | Mid Gray | 줄간격 1.2 |

### 강조 박스 (Executive Summary, 핵심 메시지)
- 배경: #F0F4FA (Light Navy Tint)
- 좌측 테두리: 4pt Primary Navy
- 패딩: 12pt
- 본문 글꼴 동일

### 판정 색상 박스
- GO: 배경 #00E676, 글자 흰색, 굵게
- GO 조건부: 배경 #00E676 50% 투명도, 글자 Primary Navy
- HOLD: 배경 #FF5722, 글자 흰색, 굵게
- NO-GO: 배경 #E91E63, 글자 흰색, 굵게

### 표 서식
- 헤더 행: 배경 Primary Navy, 글자 흰색, SemiBold 10pt
- 데이터 행: 짝수 #F8F9FB / 홀수 흰색
- 테두리: 헤더 하단 2pt Primary Navy / 데이터 행 0.5pt #E0E0E0
- 셀 패딩: 8pt

### 아이콘·기호 사용
- ■ 섹션 인트로 강조
- ▼ 하위 항목 도입
- ▶ 결과·결론 강조
- ⚠️ 경고·리스크 항목
- ✅ 충족·강점
- ❌ 미충족·약점
- → 인과 관계

### 페이지 번호
- 위치: 하단 가운데
- 형식: "X / Y"
- 글꼴: Pretendard 9pt, Mid Gray

### 페이지 머리글
- 좌: [발주처] - [행사명]
- 우: RFP 분석 보고서
- 글꼴: Pretendard 8pt, Mid Gray
- 하단 구분선: 0.5pt #E0E0E0

---

## 색상 토큰 (jc-design-system 호출)

```python
# build_report.py 에서 사용
COLOR_PRIMARY      = RGBColor(0x0A, 0x25, 0x40)  # Deep Navy
COLOR_ACCENT       = RGBColor(0x29, 0x62, 0xFF)  # Electric Blue
COLOR_NEON         = RGBColor(0x00, 0xE6, 0x76)  # Neon Green
COLOR_ORANGE       = RGBColor(0xFF, 0x57, 0x22)  # Orange
COLOR_MAGENTA      = RGBColor(0xE9, 0x1E, 0x63)  # Magenta
COLOR_DARK_GRAY    = RGBColor(0x33, 0x33, 0x33)  # 본문
COLOR_MID_GRAY     = RGBColor(0x77, 0x77, 0x77)  # 캡션
COLOR_LIGHT_NAVY   = RGBColor(0xF0, 0xF4, 0xFA)  # 강조 박스 배경
COLOR_LIGHT_GRAY   = RGBColor(0xF8, 0xF9, 0xFB)  # 짝수 행 배경
COLOR_BORDER       = RGBColor(0xE0, 0xE0, 0xE0)  # 테두리
```

---

## 발주처 명시 규칙

- 표지 / 머리글 / 1장 RFP 개요 / 본문 직접 인용 시에만 발주처 명 사용
- 발주처 로고는 사용자가 명시적으로 제공한 경우에만 삽입
- **발주처 컬러를 보고서 디자인에 적용하지 않음** (작업자 베이스 유지)
- 단, 발주처 명을 표지 외에는 과도하게 반복하지 않음 (분석자 시선 강조)
