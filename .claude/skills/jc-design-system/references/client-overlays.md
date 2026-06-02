# Client Overlays — 클라이언트별 컬러·로고 토글

시그니처는 고정 자산이다. 클라이언트별 차별화는 이 파일의 오버레이만으로 처리한다.

---

## 1. 오버레이 원칙

### 1.1 주입 가능 토큰 (3개만)

| 토큰 | 오버레이 가능 여부 | 비고 |
|------|------|------|
| `primary` | ✅ | 헤더·표지·로고 영역 |
| `accent` | ✅ | 강조·CTA·KPI |
| `logo_path` | ✅ | 클라이언트 로고 이미지 경로 |
| `text` / `text-muted` | ❌ | 시그니처 고정 |
| `bg` / `surface` | ❌ | 시그니처 고정 |
| `font` | ❌ | 시그니처 고정 |
| `size` / `space` / `radius` | ❌ | 시그니처 고정 |

### 1.2 폴백 규칙

- `null` 값 → 시그니처 토큰 그대로 사용
- 로고 미제공 → 로고 영역 비표시 (텍스트 클라이언트명만)
- 클라이언트 미지정 → 무클라이언트(개인 브랜드) 모드

---

## 2. 오버레이 스키마

```json
{
  "client_id": "string — 영문 소문자·하이픈 (예: mc, remember, darktrace)",
  "client_name": "string — 산출물 표기용 정식 명칭 (외부 주입: {{client_company}})",
  "track": "A | B | personal — A=Track A(소속사 트랙), B=Track B(독립), personal=개인 브랜드",
  "overrides": {
    "primary": "#XXXXXX | null",
    "accent": "#XXXXXX | null",
    "logo_path": "assets/clients/{client_id}.png | null"
  },
  "notes": "string — 사용 컨텍스트 메모 (선택)"
}
```

---

## 3. 클라이언트 오버레이 샘플

### 3.1 무클라이언트 (개인 브랜드 / 기본값)

```json
{
  "client_id": "personal",
  "client_name": "{{author_name}} / {{personal_brand}}",
  "track": "personal",
  "overrides": {
    "primary": null,
    "accent": null,
    "logo_path": null
  },
  "notes": "Track B 퍼스널 브랜드 산출물 기본값. 시그니처 그대로 사용. client_name은 외부 주입 변수로 처리."
}
```

### 3.2 소속사 (Track A — 한국 PCO 일반)

```json
{
  "client_id": "mc",
  "client_name": "{{company_name}}",
  "track": "A",
  "overrides": {
    "primary": null,
    "accent": null,
    "logo_path": "assets/clients/mc.png"
  },
  "notes": "Track A 행사 기획 전략 역할 산출물. 컬러는 시그니처 유지, 로고만 적용. 외부 제출용 표지에 클라이언트 로고 사용. client_name은 외부 주입 변수."
}
```

### 3.3 데이터 파트너사 (협업 사업 예시)

```json
{
  "client_id": "remember",
  "client_name": "{{client_company}}",
  "track": "B",
  "overrides": {
    "primary": "#0A2540",
    "accent": "#2962FF",
    "logo_path": "assets/clients/remember.png"
  },
  "notes": "연례 컨퍼런스 예시 등 협업 행사 산출물. 시그니처 컬러를 그대로 유지하되 파트너사 로고 병기. client_name은 외부 주입 변수."
}
```

### 3.4 Darktrace Korea (개별 행사 클라이언트)

```json
{
  "client_id": "darktrace",
  "client_name": "Darktrace Korea",
  "track": "B",
  "overrides": {
    "primary": "#0A2540",
    "accent": "#E91E63",
    "logo_path": "assets/clients/darktrace.png"
  },
  "notes": "Discovery Meeting 단계. 보안·테크 톤이라 Magenta 액센트로 차별화. 6월 행사 확정 시 재검토."
}
```

### 3.5 ConfEx 박람회 (수주 목표)

```json
{
  "client_id": "confex",
  "client_name": "ConfEx",
  "track": "B",
  "overrides": {
    "primary": null,
    "accent": "#FF5722",
    "logo_path": "assets/clients/confex.png"
  },
  "notes": "2026년 핵심 매출 프로젝트. 박람회 활성도 강조 위해 Vivid Orange 액센트."
}
```

---

## 4. 오버레이 적용 흐름

```
산출물 생성 요청
       ↓
client_id 지정?
   ├─ Yes → client-overlays.md 에서 매칭 항목 조회
   │         └─ overrides.primary / accent / logo_path 적용
   │             (null 항목은 시그니처 유지)
   └─ No  → personal 오버레이 적용 (시그니처 그대로)
       ↓
산출물 빌드
```

---

## 5. 신규 클라이언트 추가 절차

1. 본 파일에 `## 3.X 클라이언트명` 섹션 추가
2. 위 스키마에 따라 JSON 블록 작성
3. 로고 파일은 `assets/clients/{client_id}.png` 경로로 배치
4. 오버레이 컬러는 클라이언트 CI 가이드 확인 후 결정 (추측 금지)
5. CI 미공개 시 시그니처 그대로 + 로고만 적용 권장

---

## 6. 컬러 충돌 회피 규칙

- 클라이언트 primary가 시그니처 Deep Navy(`#0A2540`)와 채도 차이 30% 이내면 시그니처 유지
- 클라이언트 accent가 Point Pool 4종 중 하나와 ΔE < 5 이면 해당 포인트로 통합
- 인쇄용 산출물에서 형광·네온 계열 클라이언트 컬러는 채도 -20% 적용 후 사용
