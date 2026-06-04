# Overlay Catalog — 적용 가능한 테마(=오버레이) 목록

원본 Theme Factory의 "Themes Available(10종)"에 대응하는, jc 생태계의 실제 선택지다. 다만 **무관한 10개 테마가 아니라 "1개 시그니처 + N개 클라이언트 오버레이"** 구조다.

> **값의 정본은 `jc-design-system/references/client-overlays.md`.** 본 카탈로그는 쇼케이스·선택 UX를 위한 요약(정체성 한 줄 + accent 미리보기)이며, 실제 적용 시 색 값은 SoT에서 런타임 로드한다. 등록 항목이 바뀌면 `scripts/build_showcase.py`가 SoT를 다시 읽어 쇼케이스를 갱신한다.

## 시그니처 (오버레이 없음 = 기본값)

| 정체성 | primary | accent | 폰트(불변) | 용도 |
|--------|---------|--------|-----------|------|
| **JC 시그니처** | Deep Navy `#0A2540` | Electric Blue `#2962FF` | Pretendard / Inter / JetBrains Mono | 개인 브랜드·무클라이언트 기본. 신뢰·전문 톤 |

시그니처 값의 정본은 `signature-tokens.md §1`. 오버레이를 지정하지 않으면 항상 이 시그니처가 적용된다.

## 등록된 클라이언트 오버레이

각 오버레이는 시그니처 위에 `primary`/`accent`/`logo`만 덮어쓴다. `null`은 시그니처 유지.

| client_id | 정체성 한 줄 | primary | accent | track | 비고 |
|-----------|-------------|---------|--------|-------|------|
| `personal` | 개인 브랜드 기본값 — 시그니처 그대로 | (시그니처) | (시그니처) | personal | 미지정 시 폴백 |
| `mc` | 소속사 트랙 — 컬러는 시그니처, 로고만 적용 | (시그니처) | (시그니처) | A | 외부 제출 표지에 클라이언트 로고 |
| `remember` | 협업 컨퍼런스 — 시그니처 유지 + 파트너 로고 병기 | Deep Navy | Electric Blue | B | 시그니처 컬러 그대로 |
| `darktrace` | 보안·테크 톤 — Magenta 액센트로 차별화 | Deep Navy | Magenta `#E91E63` | B | Discovery 단계, 행사 확정 시 재검토 |
| `confex` | 박람회 활성도 강조 — Vivid Orange 액센트 | (시그니처 navy) | Orange `#FF5722` | B | 핵심 매출 프로젝트 |

> 위 accent 값(Magenta/Orange 등)은 전부 jc Point Pool 정본 색이다 — 임의색이 아니다. 그래서 오버레이를 써도 전체 룩이 한 가족으로 묶인다.

## 정체성 → 톤 매핑 가이드

신규 클라이언트의 "분위기"만 받았을 때 어떤 Point 액센트를 권할지의 출발점(최종은 클라이언트 CI 확인 후):

| 요청 톤 | 권장 accent | 근거 |
|---------|------------|------|
| 신뢰·금융·공공·B2B 기본 | Electric Blue `#2962FF` (시그니처) | 가장 안전, 시그니처와 동일 |
| 보안·테크·프리미엄·차별화 | Magenta `#E91E63` | Track B 퍼스널 브랜드 포인트 후보 |
| 활성도·박람회·리테일·에너지 | Vivid Orange `#FF5722` | 핫·우선순위 톤 |
| 성장·친환경·헬스·라이브 | Neon Green `#00E676` (면적 5%↓, 인쇄 폴백 `#00C853`) | 성장·긍정 |

이 4색이 jc Point Pool 전부다. **이 밖의 색을 임의로 만들지 않는다.** 클라이언트 CI가 풀 밖이면 `mint-overlay.md`의 충돌 회피 규칙으로 가장 가까운 풀 색에 통합하거나, 시그니처 유지 + 로고만 적용한다.

## 선택 흐름

```
사용자에게 적용할 오버레이 확인
   ├─ 등록된 것 중 선택        → 그 client_id로 적용 (apply-guide.md)
   ├─ 미지정                   → personal(시그니처) 적용
   └─ 맞는 게 없음 / 신규      → mint-overlay.md 발행 절차
```
