# JC Palette Mapping — 홈베이스 캔버스용 토큰/타이포 매핑

홈베이스 모드(기본)에서 **jc-design-system 토큰을 캔버스 아트에 어떻게 쓰는지**의 매핑이다.
**값 정본은 항상 `jc-design-system/references/signature-tokens.md`** (§1 컬러·§1.8 스케일·§2 폰트, 기계 파싱은 §6 JSON). 본 문서는 그 값을 *아트오브젝트*라는 매체에 어떻게 연결하는지만 설명한다. **색·폰트 값을 여기에 박지 않는다 — 빌드 시 SoT에서 읽는다**(플레이북 §3, `jc_tokens.py`의 `load_tokens`/`color`).

---

## 1. SoT 런타임 로딩 (미러 금지)

```python
from pathlib import Path
import sys
# 빌드 스크립트를 jc-visual-philosophy/scripts/ 깊이에서 실행한다는 전제 → parents[2] = .claude/skills/
# (다른 깊이/임시 경로에서 돌리면 parents 인덱스를 그에 맞게 조정한다.)
SOT = Path(__file__).resolve().parents[2] / "jc-design-system"   # 형제 경로
sys.path.insert(0, str(SOT / "scripts"))
from jc_tokens import load_tokens, color
tok = load_tokens(SOT)
accent = color(tok, "accent")                 # "#2962FF" (Electric Blue)
primary = color(tok, "primary")               # "#0A2540" (Deep Navy)
scale_blue = tok["color"]["scales"]["blue"]    # 5단계 deep→bg 리스트
```

값을 못 박는 이유: 시그니처가 바뀌면 캔버스도 자동으로 따라가야 같은 가족으로 남는다. `check_drift.py`(존재 시)의 FORBIDDEN 값은 절대 쓰지 않는다.

---

## 2. 캔버스 역할 → jc 토큰 매핑

아트오브젝트는 UI가 아니므로 컴포넌트 토큰이 아니라 **표현 역할**로 매핑한다.

| 캔버스 역할 | jc 토큰(키) | 비고 |
|------------|------------|------|
| 캔버스 바탕(라이트) | `bg` / `surface` | 인쇄 라이트 권장 — `#F8F9FB`/`#FFFFFF` 계열 |
| 캔버스 바탕(다크 풀블리드, 의도 시) | `primary` (`#0A2540`) | 표지 아트·임팩트 키비주얼. 인쇄 배포면 라이트로 |
| 주 형태·구조선·대형 도형 | `primary` / `primary-soft` | 뼈대·기념비적 형태 |
| 시그니처 강조(앵커 컬러) | `accent` (`#2962FF`) | 일렉트릭 블루 — 작품의 시그니처 시각 신호 |
| 강조 보조 톤 | `accent-strong` / `accent-light` / `accent-soft` | 같은 색조의 명도 변주 |
| 포인트 강세(최대 3종 동시) | `point.orange` / `point.magenta` / `point.neon` / `point.blue` | 핫스팟·리듬 강세. 면적 절제 |
| 임상 라벨·잉크 텍스트 | `text` / `text-muted` | 캡션·레퍼런스 마커 |
| 미세 구분선·그리드 마크 | `border` / `border-strong` | 과학 도감의 격자·눈금 |

> 마젠타(`point.magenta`)는 Track B(독립 전략가) 퍼스널 브랜드 포인트 후보다(`signature-tokens.md §1.6`). 개인 키비주얼이면 마젠타 강세를 우선 고려.

---

## 3. §1.8 인포그래픽 스케일 — 캔버스 아트의 핵심 무기

홈베이스 모드에서 **"과학 도감 미학"(조밀한 반복·단계적 그라데이션)을 jc답게** 내는 핵심이다. 단일 카테고리 구분은 §1.4 data 시리즈를, **연속·단계·깊이 표현은 §1.8 스케일**을 쓴다.

| 스케일 | 캔버스 용도 |
|--------|------------|
| `scale-blue` (deep→bg 5단계) | 모노크로매틱 마스터피스의 기본축. 깊이·거리·강도의 그라데이션. **전부 기존 시그니처 토큰이라 신규 색 0** |
| `scale-green` | 성장·유기적 리듬·생태 모티프 |
| `scale-red` | 열·강도·경고 톤의 단계 |
| `scale-amber` | 따뜻함·시간·아카이브 톤의 단계 |

- 토큰명 `--jc-scale-<hue>-<1..5>`, 기계 파싱 `tok["color"]["scales"][<hue>]`.
- **활용 예**: scale-blue 5단계로 동심원/등고선/히트필드를 그리면 *상상 속 학문의 다이어그램* 질감이 jc 팔레트 안에서 완성된다. 색 수를 늘리지 않고 5단계 명도만으로 깊이를 쌓는 게 홈베이스의 정석.

---

## 4. 타이포 (홈베이스)

| 캔버스 역할 | jc 폰트(키) | 굵기 |
|------------|------------|------|
| 작품 제목·대형 타이포 제스처 | `heading` (Pretendard) | `bold`(700) / `semibold`(600) |
| 한글 본문·문구 앵커 | `ko` (Pretendard) | `regular`(400) / `medium`(500) — 원본 권장대로 thin 우선 |
| 임상 라벨·레퍼런스 마커·좌표·번호 | `mono` (JetBrains Mono) | `regular` — 과학 도감의 측정값 질감 |

- 폰트 파일 출처·미설치 시 다운로드는 `references/fonts-strategy.md`. (이 환경엔 Pretendard 미설치 → 다운로드 필요.)
- 홈베이스에서 canvas-fonts 디스플레이 폰트는 쓰지 않는다(자유 모드 전용).
- 타이포 스케일·라인하이트가 필요하면 `signature-tokens.md §3`(size)·§3.1(leading). 단 아트오브젝트는 UI 스케일에 얽매이지 않고 구도가 요구하는 크기를 쓰되, 페이지 이탈·겹침 0.

---

## 5. 색 사용 절제 (홈베이스 정신)

`signature-tokens.md §1.6` 규칙을 아트에 적용:

- **일렉트릭 블루(accent)**: 면적 제한 없음 — 작품의 시그니처 신호로 자유롭게.
- **포인트 풀 4종**: 한 화면 동시 최대 3종. 리듬 강세·카테고리 암시에만.
- **네온 그린**: 면적 5% 이내. 인쇄물은 폴백 `#00C853` 자동.
- **딥 네이비**: 뼈대·핵심 강조에 한정.
- **"의도적·응집된 제한 팔레트"**: 원본이 요구한 미학과 jc 절제 규칙이 정확히 같은 방향이다 — 색을 줄이고 형태로 말한다.

---

## 6. 모드·인쇄 (홈베이스)

- 기본 라이트(`mode-mapping.md §2`). MICE 배포물(키비주얼·표지)은 **인쇄 라이트 권장**(`#RULE-PRINT-LIGHT`, `mode-mapping.md §4.2`).
- 다크 풀블리드(`primary` 바탕)는 *표지 아트·임팩트 키비주얼*의 의도된 디자인일 때만. 인쇄 배포가 목적이면 라이트로 전환.
- 작품 안 **가독 텍스트**(제목·라벨)는 배경 대비 4.5:1↑(`#RULE-WCAG`, 계산 `mode-mapping.md §9`). 예: 흰 바탕 위 본문 그린이 필요하면 `success`(2.24:1 FAIL) 대신 `success-strong`(`#00733B`, 6.36:1).
