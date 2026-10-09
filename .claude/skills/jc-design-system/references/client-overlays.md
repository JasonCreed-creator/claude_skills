# Client Overlays — 발주처 슬롯 · legacy-jc · 아카이브

리멤버 웜 페이퍼가 기본이자 유일한 룩이다. 발주처(고객사)는 **슬롯 3곳**만 바꾼다. 오렌지·서체·간격은 바꾸지 않는다.

---

## 1. 발주처 슬롯 (바꿀 수 있는 것 3곳)

| 슬롯 | 위치 | 기본값 |
|------|------|--------|
| `logo_path` | 표지·클로징 좌상단 (다크 배경이므로 발주처 로고의 다크 대응본 필요) | 없음 — 슬롯 비움 |
| `cover_image` | 표지 우측 배경 (오브제 ↔ 발주처 이미지·베뉴 사진) | `assets/objet-03-slit.png` |
| `footer_text` | 전 슬라이드 푸터 좌측 행사명 | `{행사명}` |

- 발주처 브랜드 컬러를 받아도 팔레트에 넣지 않는다. 필요하면 발주처 로고 원색 그대로만 노출.
- 발주처 로고 재염색·비율 왜곡 금지. 라이트 카드 위에 둘 때는 원본, 다크 위에는 화이트 버전.
- `assets/overlay-sample/`(remember-proposal-ds)에 발주처 슬롯 적용 예시가 있다.

### 1.1 스키마

```json
{
  "client_id": "a-corp-2026",
  "client_name": "{{client_company}}",
  "type": "client",
  "slots": {
    "logo_path": "assets/clients/a-corp-2026-logo-dark.png | null",
    "cover_image": "assets/clients/a-corp-2026-venue.png | null",
    "footer_text": "{{행사명 — 예: A사 고객 감사의 밤 2026}}"
  },
  "overrides": { "primary": null, "accent": null, "logo_path": null },
  "notes": "컬러 오버라이드는 항상 null — 스키마 호환용으로만 유지"
}
```

`overrides` 블록은 구 스크립트(`restyle_pptx.py`)와의 호환을 위해 남겨 두며 값은 항상 `null`이다.

## 2. 리멤버 기본 (오버레이 없음)

```json
{
  "client_id": "remember",
  "client_name": "리멤버 MICE비즈팀",
  "type": "house",
  "slots": { "logo_path": "assets/remember-black.png", "cover_image": "assets/objet-03-slit.png", "footer_text": "{행사명}" },
  "overrides": { "primary": null, "accent": null, "logo_path": null },
  "notes": "기본값. 발주처 미지정이면 이것."
}
```

발행 명의: `(주)리멤버앤컴퍼니 마켓데이터사업실 · MICE 비즈팀`, 공용 문의 `mice_solution@remember.co.kr`. 개인 휴대전화·사설 메일은 대외 문서에 넣지 않는다.

## 3. 명명 오버레이

### 3.3 legacy-jc (구 개인 시그니처, opt-in 전용)

사용자가 "jc 시그니처", "네이비·블루 톤", "예전 스타일"을 명시할 때만 적용한다. 기본값이 아니며 소비 스킬이 자동 선택하지 않는다.

```json
{
  "client_id": "legacy-jc",
  "client_name": "{{personal_brand}}",
  "type": "legacy",
  "overrides": { "primary": "#0A2540", "accent": "#2962FF", "logo_path": null },
  "deck_theme": {
    "bg_base": "F8F9FB", "bg_card": "FFFFFF", "text_primary": "1A1D24", "text_body": "1A1D24",
    "text_muted": "5A6270", "accent": "2962FF", "accent_sub": "E91E63", "line": "E5E8ED",
    "point": ["FF5722", "E91E63", "00E676", "2962FF"],
    "data": ["2962FF", "E91E63", "FF5722", "00E676", "0A2540", "7C3AED"],
    "font_heading": "Pretendard", "font_body": "Pretendard"
  },
  "notes": "v1.x jc-design-system 시그니처 스냅숏(2026-08-18). 값 갱신 없음."
}
```

## 4. 아카이브 (사용 금지)

| client_id | 사유 |
|-----------|------|
| `confex` | v1 Track B 수주 목표. 리멤버 전환으로 종결 |

재개 시 §1.1 스키마로 신규 등록한다. 구 소속사 시절 오버레이는 2026-10-05 목록에서 삭제했다(RULE-NO-COMPANY). 이력은 git 히스토리 참조.

## 5. 적용 흐름

```
발주처 지정? ─ Yes → §1.1 블록 조회 → slots 3종 주입 (컬러는 그대로)
             └ No  → §2 remember 기본
"jc 시그니처" 명시? → §3.3 legacy-jc (deck_theme 전체 교체)
```

## 6. 신규 발주처 등록

1. 본 파일 §1에 블록 추가(`client_id`는 영문 소문자·하이픈).
2. 로고 파일은 `assets/clients/<client_id>-logo.png`(라이트) · `-logo-dark.png`(다크).
3. 표지 이미지는 발주처 제공 원본 또는 베뉴 사진. 없으면 오브제 유지.
4. 컬러는 등록하지 않는다.
