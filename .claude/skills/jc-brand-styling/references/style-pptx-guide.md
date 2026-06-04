# style_pptx.py 상세 가이드

`scripts/style_pptx.py` — 이미 존재하는 `.pptx`에 jc 시그니처(+선택적 클라이언트 오버레이)를 입히는 후처리 엔진의 상세 동작·옵션·트러블슈팅. SKILL.md의 요약을 보강한다.

> 토큰 값의 정본은 항상 `jc-design-system/references/signature-tokens.md §6`(라이트)·`mode-mapping.md §3`(다크)다. 이 문서는 *적용 로직*만 설명하며 색 값을 재정의하지 않는다.

## 1. 무엇을 바꾸나 (적용 규칙)

| 대상 | 규칙 | 정본 |
|------|------|------|
| 헤딩 폰트 | run 크기 ≥ `--heading-min`(기본 24pt) **또는** bold → `font.heading` 첫 토큰(Pretendard) | `signature-tokens.md §2.1` |
| 본문 폰트 | 그 외 모든 텍스트 run → `font.ko` 첫 토큰(Pretendard) | `signature-tokens.md §2.1` |
| 텍스트색 | 도형 채움 배경 대비로 흰(`surface`) vs Deep Navy(`text`) 중 대비 큰 쪽 | `RULE-WCAG` / `mode-mapping.md §9` |
| 비텍스트 도형 채움 | accent → Point Pool(orange·magenta·neon·blue) → data 시리즈 순환 | `signature-tokens.md §1.2~1.4` |
| 표 셀 텍스트 | 셀 텍스트도 위 폰트·색 규칙 적용 | — |
| 그룹 도형 | 재귀 진입해 내부 도형까지 처리 | — |
| 그림(PICTURE) | 건드리지 않음(채움 순환 대상 아님) | — |

**폰트는 시그니처 고정** — 오버레이로도 바꾸지 않는다. python-pptx는 run당 단일 폰트명만 받으므로 폴백 체인의 **첫 항목**(Pretendard)을 심고, 미설치 환경 폴백(Apple SD Gothic Neo→Malgun Gothic→Arial)은 실행 로그로 안내한다(`signature-tokens.md §2.3`).

## 2. CLI

```
python3 style_pptx.py <입력.pptx> [-o 출력.pptx] [--client <id>] [--heading-min PT] [--self-test]
```

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `입력.pptx` | (필수) | 후처리할 기존 PPTX. `.pptx`가 아니면 종료코드 2. |
| `-o, --output` | `<입력>_jc.pptx` | 출력 경로. 원본을 덮어쓰지 않도록 기본은 접미사 추가. |
| `--client <id>` | (없음) | `client-overlays.md`의 `client_id`. 매칭 블록의 primary/accent를 적용(null·플레이스홀더는 시그니처 유지). 못 찾으면 경고 후 시그니처로 진행. |
| `--heading-min PT` | `24.0` | 헤딩으로 간주할 최소 pt. mice-proposal 표지처럼 큰 텍스트가 많으면 올린다. |
| `--self-test` | — | 샘플 PPTX를 코드로 생성→적용→재검증. 입력 없이 엔진 동작만 확인. |

**종료코드**: `0` 성공 / `1` python-pptx 미설치(친절 안내 출력) / `2` 입력 오류·적용 실패.

## 3. SoT 토큰 로딩 (값 미러링 금지)

형제 경로로 `jc-design-system`을 찾아 런타임 로드한다:

```python
_SOT = Path(__file__).resolve().parents[2] / "jc-design-system"
# jc-brand-styling/scripts/style_pptx.py → parents[2] = .claude/skills/
sys.path.insert(0, str(_SOT / "scripts"))
from jc_tokens import load_tokens, color
tok = load_tokens(_SOT)             # signature-tokens.md §6 JSON
```

- 로드 성공 → primary/accent/surface/text/point/data/font를 SoT에서 읽는다.
- 로드 실패(파일 없음·파싱 실패) → **출처 주석을 단 `_FALLBACK` 미러**로만 폴백. 이 폴백 값들은 `signature-tokens.md §6`과 동일하며 `check_drift.py` FORBIDDEN 값을 한 건도 포함하지 않는다.
- 실행 로그 첫 줄에 `토큰 출처: SoT(jc-design-system)` 또는 `폴백 미러`를 찍어 어느 경로였는지 드러낸다.

## 4. 오버레이 적용 (3토큰 한정)

`--client <id>` 지정 시 `client-overlays.md`의 ```json 블록을 파싱해 `client_id`가 일치하는 항목을 찾는다(슬러그 검증으로 §2 스키마 예시는 제외). 적용은 **primary·accent만**:

```python
if _valid_hex(o.get("primary")): sig["primary"] = o["primary"]
if _valid_hex(o.get("accent")):  sig["accent"]  = o["accent"]
```

- `null`·플레이스홀더(`"#XXXXXX | null"`)·잘못된 hex → 무시(시그니처 유지).
- `logo_path`는 본 엔진이 텍스트/도형 서식만 다루므로 직접 합성하지 않는다(로고 배치는 산출물 생성 스킬 또는 수동 작업 — `RULE-NO-COMPANY`상 경로는 외부 주입).
- font/bg/surface/size/space/radius는 **절대** 오버레이하지 않는다(시그니처 고정).

어떤 오버레이를 쓸지는 `jc-theme-factory`가 결정한다. 신규 오버레이가 필요하면 거기서 `validate_overlay.py`로 검증·발행 후 `client-overlays.md`에 등록하고, 그 `client_id`를 여기에 넘긴다.

## 5. RULE-PPTX-HEX 처리

python-pptx의 `RGBColor.from_string()`은 `#` 없는 6자리 16진수만 받는다. `to_pptx_hex()`가 `#`를 제거하고 대문자화한다:

```python
def to_pptx_hex(h): return h.strip().lstrip("#").upper()   # "#2962FF" → "2962FF"
RGBColor.from_string(to_pptx_hex(sig["accent"]))
```

같은 색이라도 **HTML/CSS는 `#2962FF`, PPTX는 `2962FF`** — 매체에 따라 표기가 다르다. 정본: `shared-rules.md#RULE-PPTX-HEX`.

## 6. 텍스트색 대비 자동 선택 (RULE-WCAG)

각 도형의 채움색(단색이면 그 hex, 아니면 슬라이드 `surface` 가정)을 배경으로 보고, 흰색과 Deep Navy 중 **대비비가 큰 쪽**을 텍스트색으로 고른다. 대비 공식은 `mode-mapping.md §9.1`(sRGB→상대휘도)을 그대로 구현. 동률이면 어두운색(Deep Navy)을 택해 밝은 배경 기본을 보장한다.

- 흰 텍스트 on Deep Navy = 14.04:1 (AAA)
- Deep Navy 텍스트 on 흰 배경 = 16.30:1 (AAA)
- 흰 텍스트 on Electric Blue accent = 4.79:1 (AA 본문)

(수치 정본: `mode-mapping.md §9.5`)

## 7. 자가검증 (`--self-test`)

입력 파일 없이 엔진이 실제로 동작하는지 회귀 확인한다. 절차:

1. python-pptx로 샘플 2슬라이드 PPTX 생성(제목 32pt + 본문 / 빈 슬라이드에 둥근 사각형 3개).
2. `style_presentation()`으로 스타일 적용 → `sample_jc.pptx`.
3. 출력을 **다시 열어** 적용된 폰트·도형 채움색을 추출해 검증.
4. `텍스트 런 > 0` & `도형 채움 > 0` & `시그니처 폰트 적용됨`이면 PASS, 종료코드 0.

기대 출력(SoT 로드 성공 시):

```
[self-test] 시그니처 로드: SoT
            primary=#0A2540 accent=#2962FF heading-font=Pretendard
[self-test] 샘플 PPTX 생성: sample.pptx (~29KB)
[self-test] 스타일 적용 → sample_jc.pptx (~29KB)
            슬라이드 2 · 텍스트 런 3개 재서식 · 비텍스트 도형 3개 채움
            채움 순환 풀: #2962FF, #FF5722, #E91E63, #00E676, #0A2540, #7C3AED
[self-test] 검증: 적용된 폰트 ['Pretendard'] · 도형 채움색 ['#2962FF', '#FF5722', '#E91E63']
[self-test] 결과: ✅ PASS
```

## 8. python-pptx 미설치 대응

`import pptx` 실패 시 **무음 실패하지 않고** 설치법 + 토큰값을 담은 안내를 stderr로 출력하고 종료코드 1로 끝낸다. 설치:

```bash
pip install python-pptx        # 또는
python3 -m pip install python-pptx
```

설치 권한이 없는 환경이면 안내에 찍힌 토큰값(헤딩/본문 폰트·텍스트색·도형 순환 규칙)을 참고해 수동 적용하거나, python-pptx가 설치된 환경에서 실행한다.

## 9. 트러블슈팅

| 증상 | 원인 | 대응 |
|------|------|------|
| `토큰 출처: 폴백 미러`로 뜸 | 형제 경로에서 `jc-design-system`을 못 찾음 | 스킬이 `.claude/skills/` 하위에 있는지 확인. 폴백값은 SoT와 동일하므로 결과는 같다. |
| 색이 안 바뀜(PPTX) | hex에 `#`가 붙어 RGBColor가 거부 | `to_pptx_hex()`를 거치는지 확인(`RULE-PPTX-HEX`). |
| 폰트가 화면에서 다르게 보임 | 뷰어 환경에 Pretendard 미설치 | 정상 — 폴백 체인(Apple SD Gothic Neo→Malgun Gothic→Arial)으로 렌더. 파일의 폰트 지정 자체는 Pretendard. |
| 헤딩인데 본문 폰트가 먹음 | run 크기가 `--heading-min` 미만 | `--heading-min`을 낮추거나, 원본 슬라이드의 폰트 크기를 확인. bold면 크기와 무관하게 헤딩 처리됨. |
| 일부 도형이 안 채워짐 | 텍스트가 있거나 그림이거나 채움 불가 도형 | 의도된 동작 — 텍스트 도형은 텍스트 규칙으로, 그림은 건드리지 않음. |
| `--client` 무시됨 | `client_id` 오타 또는 미등록 | 경고 메시지 확인. `jc-theme-factory`로 오버레이 등록 여부 점검. |

## 10. 점검 체크리스트 (적용 후)

- [ ] 출력 파일이 생성됐고 0바이트가 아님
- [ ] 토큰 값 SoT 런타임 참조(하드코딩 0건), `check_drift.py` FORBIDDEN 0건
- [ ] hex `#` 없는 6자리로 RGBColor 전달(`RULE-PPTX-HEX`)
- [ ] 폰트 시그니처 유지(Pretendard), 오버레이로 폰트 안 바뀜
- [ ] 흰/Deep Navy 텍스트 대비 WCAG AA↑(`RULE-WCAG`)
- [ ] 오버레이는 primary/accent 3토큰만, null은 시그니처 유지
- [ ] 회사·개인정보 무주입(엔진은 서식만 변경, `RULE-NO-COMPANY`)
- [ ] `--self-test` PASS, 최종 카피·대비는 `jc-redteam` 점검 가능
