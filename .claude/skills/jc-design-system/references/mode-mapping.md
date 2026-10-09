# Mode Mapping — 라이트/다크 · 인쇄 · 대비비

값의 정본은 `signature-tokens.md`. 이 문서는 어느 값을 언제 쓰는지와 대비비 검증만 다룬다.

---

## 1. 산출물 유형별 기본 모드

| 산출물 | 기본 | 다크 허용 범위 |
|--------|------|----------------|
| PPTX 제안서·소개서·발표덱 | 라이트 | 표지 · 섹션 구분 · 클로징 3종(`#141210`). 본문 안 다크 패널은 `#211E1A` 슬라이드당 1회. 덱 전체 30% 이하 |
| HTML 대시보드·팀 보드 | 라이트 | `data-theme="dark"` 토글. 인쇄는 라이트 강제(§4.2) |
| HTML 문서·플레이북·리포트 | 라이트 | 다크 밴드 페이지당 1개 이하 |
| XLSX 견적·시트 | 라이트 | 타이틀 밴드만 잉크(`#1A1A1A`) 배경 + 오렌지 라벨 |
| DOCX 대본·보고서 | 라이트 | 없음 |
| Slack 캔버스·구글독 | 해당 없음 | 서식은 플랫폼 기본. 색 지정 없음 |

## 2. 라이트 (기본)

`signature-tokens.md §1.1~1.4` 그대로. 캔버스 `#FBFAF6`, 카드 `#FFFFFF`, 잉크 `#1A1A1A`, 액센트 `#EB6F2A`.

## 3. 다크 매핑

| 역할 | 라이트 | 다크 |
|------|--------|------|
| 배경 | `#FBFAF6` | 슬라이드 스테이지 `#141210` / 대시보드·패널 `#211E1A` |
| 카드 | `#FFFFFF` | `#2A2620` |
| 웜 서피스 | `#F4F1EA` | `#322D26` |
| 보더 | `#DCD6C8` | `#3E3931` |
| 구분선 | `#C9C9C0` | `#4A443B` |
| 본문 | `#1A1A1A` | `#F4F0E9` |
| 보조(brown) | `#4A463F` | `#C9C0B2` |
| 뮤트 | `#6E6E6E` | `#A89F92` |
| 캡션 | `#8C867A` | `#6E655A` |
| 오렌지 면 | `#EB6F2A` | `#EB6F2A` (유지) |
| 오렌지 텍스트 | `#B8431A` | `#F08A4C` |
| 오렌지 틴트 | `#FFF1E6` | `#3A2A1E` |
| Steel 텍스트 | `#476580` | `#8FAEC7` |
| Steel 틴트 | `#E8EEF3` | `#26313A` |
| 긍정 / 배경 | `#196B24` / `#E7EFE8` | `#6FBF7C` / `#22301F` |
| 부정 / 배경 | `#D93636` / `#FBE9E9` | `#F07A7A` / `#3A2323` |
| 앰버 / 배경 | `#D39A1F` / `#FBF2DF` | `#E2B558` / `#3A3021` |
| 그림자 | `0 2px 12px rgba(74,70,63,.08)` | `0 2px 12px rgba(0,0,0,.32)` |
| 로고 | remember-black.png | remember-offwhite.png |

차트 시리즈는 다크에서도 동일(S1~S5). 축·그리드만 `#4A443B`.

## 4. 자동 전환 규칙

### 4.1 HTML 산출물

```css
:root { --paper:#FBFAF6; --surface:#FFFFFF; --ink:#1A1A1A; /* … §1 라이트 */ }
:root[data-theme="dark"] { --paper:#211E1A; --surface:#2A2620; --ink:#F4F0E9; /* … §3 다크 */ }
```

- 토글은 `data-theme` 속성 하나로. 컴포넌트는 변수만 참조하고 색을 직접 쓰지 않는다.
- 기본값 라이트. 사용자 선택은 `localStorage`에 저장해도 되지만 첫 렌더는 라이트.
- Chart.js 등 캔버스 차트는 `getComputedStyle(document.documentElement).getPropertyValue('--s1')`로 읽어 테마 전환 시 `chart.update()`.

### 4.2 인쇄 강제 변환 (RULE-PRINT-LIGHT)

```css
@media print {
  :root, :root[data-theme="dark"] {
    --paper:#FFFFFF !important; --surface:#FFFFFF !important; --surface-warm:#F4F1EA !important;
    --ink:#1A1A1A !important; --ink-sub:#6E6E6E !important; --border:#DCD6C8 !important;
  }
  .dark-band, .objet { background:#FFFFFF !important; color:#1A1A1A !important; }
}
```

인쇄 컨텍스트에서만 덮어쓰고 화면 상태는 유지한다. 잠금·내부 전용 블록은 `.no-print`로 제외.

## 5. 콘트라스트 검증 (WCAG 2.1, sRGB 상대 휘도 §9 공식으로 실측)

### 5.1 라이트

| 조합 | 대비비 | 등급 | 판정 |
|------|--------|------|------|
| `#1A1A1A` on `#FFFFFF` | 17.40:1 | AAA | 본문 |
| `#1A1A1A` on `#FBFAF6` | 16.66:1 | AAA | 본문 |
| `#4A463F` on `#FBFAF6` | 8.98:1 | AAA | 보조 본문 |
| `#6E6E6E` on `#FFFFFF` | 5.10:1 | AA | 뮤트 본문 |
| `#6E6E6E` on `#FBFAF6` | 4.88:1 | AA | 뮤트 본문 |
| `#8C867A` on `#FFFFFF` | 3.62:1 | 큰 텍스트만 | 캡션·단위·푸터 한정 |
| `#EB6F2A` on `#FFFFFF` | 3.07:1 | 큰 텍스트만 | 24px+ / 18px+ Bold 강조어 |
| `#EB6F2A` on `#FBFAF6` | 2.94:1 | FAIL | 작은 오렌지 텍스트 금지 |
| `#B8431A` on `#FFFFFF` | 5.45:1 | AA | 작은 강조·링크·배지 텍스트 |
| `#B8431A` on `#FFF1E6` | 4.92:1 | AA | 오렌지 배지 |
| `#FFFFFF` on `#EB6F2A` | 3.07:1 | 큰 텍스트만 | 솔리드 KPI 숫자(48pt) OK, 소형 라벨은 `#FFF1E6`가 아닌 크기로 해결 |
| `#FFFFFF` on `#B8431A` | 5.45:1 | AA | Primary 버튼 hover |
| `#476580` on `#FFFFFF` | 6.10:1 | AA | Steel 텍스트 |
| `#476580` on `#E8EEF3` | 5.22:1 | AA | Steel 배지 |
| `#196B24` on `#FFFFFF` | 6.62:1 | AA | 긍정 |
| `#196B24` on `#E7EFE8` | 5.65:1 | AA | 긍정 배지 |
| `#D93636` on `#FFFFFF` | 4.63:1 | AA | 부정 |
| `#D93636` on `#FBE9E9` | 3.96:1 | 큰 텍스트만 | 부정 배지는 Bold 14px+ |
| `#D39A1F` on `#FFFFFF` | 2.50:1 | FAIL | 앰버 단독 텍스트 금지 |
| `#1A1A1A` on `#F4F1EA` | 15.43:1 | AAA | 표 헤더 |

### 5.2 다크

| 조합 | 대비비 | 등급 |
|------|--------|------|
| `#F4F0E9` on `#141210` | 16.45:1 | AAA |
| `#F4F0E9` on `#211E1A` | 14.61:1 | AAA |
| `#F4F0E9` on `#332F29` | 11.71:1 | AAA |
| `#CFC8BC` on `#141210` | 11.25:1 | AAA |
| `#A89F92` on `#211E1A` | 6.35:1 | AA |
| `#F08A4C` on `#141210` | 7.51:1 | AAA |
| `#F08A4C` on `#211E1A` | 6.67:1 | AA |
| `#F5A05A` on `#141210` | 8.95:1 | AAA |
| `#F5A05A` on `#332F29` | 6.37:1 | AA |
| `#EB6F2A` on `#211E1A` | 5.41:1 | AA (큰 텍스트 권장) |
| `#8FAEC7` on `#211E1A` | 7.15:1 | AAA |
| `#6FBF7C` on `#211E1A` | 7.44:1 | AAA |
| `#F07A7A` on `#211E1A` | 6.14:1 | AA |

### 5.3 결론 규칙

1. 오렌지 텍스트는 큰 글자 전용. 작은 글자 강조는 `#B8431A`, 다크에서는 `#F08A4C`.
2. 캡션색은 보조 정보에만. 앰버는 배지 배경으로만.
3. 부정 배지는 Bold 14px 이상.

## 6. 모드 결정 우선순위

1. 사용자 명시 지정
2. 산출물 유형 기본값(§1)
3. 인쇄·PDF 배포본은 항상 라이트(§4.2)

## 7~8. (폐지)

v1의 Tier 컬러·priority 다크 변형은 스폰서 데크 전용이었으므로 v2.0.0에서 삭제.

## 9. WCAG AA 대비비 계산 표준

### 9.1 상대 휘도

```
c = ch / 255
c_lin = c / 12.92            (c <= 0.03928)
      = ((c + 0.055) / 1.055) ** 2.4
L = 0.2126 R + 0.7152 G + 0.0722 B
ratio = (L_hi + 0.05) / (L_lo + 0.05)
```

### 9.2 기준

| 텍스트 | 기준 |
|--------|------|
| 본문(18pt 미만 일반 / 14pt 미만 Bold) | 4.5:1 |
| 큰 텍스트(18pt+ Bold / 24pt+ 일반) | 3.0:1 |
| 비텍스트 UI·그래픽 | 3.0:1 |
| AAA(선택) | 7.0:1 |

### 9.3 도구

WebAIM Contrast Checker(https://webaim.org/resources/contrastchecker/) 또는 위 공식의 Python 구현. §5 표는 공식 구현으로 2026-09-21 계산.
