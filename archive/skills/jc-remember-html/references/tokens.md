# tokens.md — 리멤버 웜 페이퍼 룩 토큰 정본

추출원: 리멤버_MICE_Business_v70.pptx(54p) · 리멤버_MICE_데이터사업해부와_상품설계_통합본_v1.pptx(44p). 두 덱의 근사값을 단일 정본으로 정규화했다(오렌지 #E97132/#EB6F2A → #EB6F2A, 페이퍼 #FBFAF6/#FAFAF5 → #FBFAF6).

## 1. 라이트 팔레트 (기본)

| 토큰 | 값 | 역할 |
|------|-----|------|
| paper | `#FBFAF6` | 캔버스 배경 |
| surface | `#FFFFFF` | 카드·패널 |
| surface-warm | `#F4F1EA` | 테이블 헤더·인풋 배경 |
| ink | `#1A1A1A` | 본문 텍스트 |
| ink-sub | `#6E6E6E` | 보조 텍스트 |
| warm-gray | `#8C867A` | 캡션·뮤트·단위 |
| border | `#DCD6C8` | 카드 경계선 |
| line | `#C9C9C0` | 구분 룰·차트 보조 그리드 |
| line-soft | `#EFEBE2` | 테이블 행 구분 |
| brown | `#4A463F` | 서브 잉크·다크 면 |
| charcoal | `#332F29` | 다크 패널(사진 위)·캡슐 |
| orange | `#EB6F2A` | 주 액센트 |
| orange-deep | `#B8431A` | 호버·강조 텍스트·링크 |
| orange-soft | `#F5A05A` | 그라디언트 종점 |
| orange-tint | `#FFF1E6` | 하이라이트 면·배지 배경 |
| orange-pale | `#F3B48A` | 차트 S5·타임라인 룰 |
| steel | `#476580` | 보조 액센트·정보 |
| positive | `#196B24` | 긍정 지표 (배경 `#E7EFE8`) |
| negative | `#D93636` | 부정 지표·경고 (배경 `#FBE9E9`) |
| steel-tint | `#E8EEF3` | 스틸 배지 배경 |

그라디언트: `linear-gradient(135deg, #EB6F2A, #F5A05A)` — 슬라이드/화면당 1회.
섹션 디바이더 진한 변형: `linear-gradient(135deg, #E8641F, #F5A05A)`.

## 2. 다크 매핑

| 라이트 | → 다크 | 값 |
|--------|--------|-----|
| paper | canvas | `#211E1A` (오브제 배경은 `#141210`) |
| surface | surface | `#2A2620` |
| border | border | `#3E3931` |
| ink | ink | `#F4F0E9` |
| ink-sub | sub | `#A89F92` |
| warm-gray(값 표기) | mono-dim | `#6E655A` |
| orange(텍스트) | orange-text | `#F08A4C` |
| steel(텍스트) | steel-text | `#8FAEC7` |

면 채움 오렌지는 다크에서도 `#EB6F2A` 유지, **텍스트로 쓸 때만** `#F08A4C`.

## 3. 타이포그래피

- 서체: `'Pretendard Variable', Pretendard, sans-serif` (CDN: cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9)
- 보조 모노(토큰값·타임코드·번호): `'JetBrains Mono', monospace`
- 스케일 1.250 (Major Third):

| 토큰 | px / weight / letter-spacing |
|------|------------------------------|
| display | 49 / 700 / -1.5px |
| h1 | 39 / 700 / -1px |
| h2 | 31 / 700 / -0.5px |
| h3 | 25 / 600 / -0.3px |
| h4 | 20 / 600 / 0 |
| body | 16 / 400 / 0 (line-height 1.6~1.7) |
| small | 14 / 400 |
| caption | 12 / 400 / +0.2px |

숫자는 항상 `font-variant-numeric: tabular-nums`, 단위는 warm-gray로 분리 표기(예: `12,480` + ` 명`).
16:9 1280×720 기준 슬라이드 본문 최소 12px, 1920×1080이면 24px 미만 금지.

## 4. 간격 · 라운드 · 그림자 · 그리드

- 간격 base 4px: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64
- 라운드: 버튼 r6~8 · 카드 r10~12 · 배지 pill(999)
- 그림자: `0 2px 12px rgba(74,70,63,0.08)` 한 단계만. 다크 패널 강조 시 `0 12px 32px rgba(33,30,26,0.35)`
- 그리드: 12col · gutter 24 · content 1200. 덱 16:9 좌우 여백 8%, 문서 패딩 상하 32 / 좌우 36

## 5. 차트 규칙

- 시리즈 순서: S1 `#EB6F2A` → S2 `#476580` → S3 `#4A463F` → S4 `#8C867A` → S5 `#F3B48A`
- 주인공 시리즈만 오렌지, 비교군은 Steel·Brown·Gray. 시계열 강조는 과거 `#C9C9C0` → 현재 `#EB6F2A` 점증
- 증감: 긍정 `#196B24` / 부정 `#D93636`
- 축·기준선 Ink 2px, 보조 그리드 `#C9C9C0`, 수평 바 트랙 `#F4F1EA`

## 6. 로고 · 오브제 운용

**로고타입 2종** (재염색·왜곡 금지):
- `assets/remember-black.png` — 라이트 배경(paper·surface·tint) 전용
- `assets/remember-offwhite.png` — 다크 배경(웜 블랙·brown·사진 위) 전용
- 최소 높이 16px, 클리어스페이스 'R' 높이의 1/2

**오브제 7점** (다크 전용 히어로 · 슬라이드당 1점 · 텍스트는 반대편 여백):

| ID | 파일 | 용도 |
|----|------|------|
| OBJ-01 | objet-01-bulb.png | 아이디어·인사이트 타이틀 |
| OBJ-02 | objet-02-torn.png | 전환·대비 디바이더 |
| OBJ-03 | objet-03-slit.png | 오프닝 타이틀 배경 |
| OBJ-04 | objet-04-glow.png | 클로징·배경 그라디언트 |
| OBJ-05 | objet-05-ribbed.png | 데이터 섹션 텍스처 |
| OBJ-06 | objet-06-coil.png | 구조·프로세스 히어로 |
| OBJ-07 | objet-07-sphere.png | 데이터 사업·네트워크 |

배경 적용 레시피: `background-image: linear-gradient(90deg, rgba(20,18,16,0.72), rgba(20,18,16,0.25)), url('...'); background-size: cover;` — 텍스트 쪽 오버레이를 더 진하게.
