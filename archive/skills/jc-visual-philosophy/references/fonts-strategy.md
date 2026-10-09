# Fonts Strategy — 폰트 전략 (경량 유지)

핵심 제약: **canvas-fonts 30여 개(.ttf)를 이 레포에 대량 복사하지 않는다**(레포 경량 유지). 홈베이스 기본 폰트는 Pretendard, 자유 모드 디스플레이 폰트는 **원본 경로 참조 또는 다운로드**로 해결한다.

---

## 1. 모드별 폰트 정책 요약

| 모드 | 한글/혼용 | 숫자·임상 라벨 | 디스플레이(장식) |
|------|----------|---------------|------------------|
| 🏠 홈베이스 | **Pretendard** | JetBrains Mono | (사용 안 함) |
| 🎨 자유 아트 | 자유(Pretendard 포함) | 자유 | **canvas-fonts .ttf 허용** |

폰트 스택·폴백 정본은 `jc-design-system/references/signature-tokens.md §2`(+§2.3 미설치 폴백). 값은 SoT에서 읽고 본 문서에 박지 않는다.

---

## 2. 홈베이스 폰트 — Pretendard 확보

이 실행 환경에는 **Pretendard가 기본 설치돼 있지 않을 수 있다**(시스템 fc-list에 한국어 폰트가 IPAGothic 정도만 존재). 원본 `canvas-design`이 "필요한 폰트는 다운로드해서 쓰라"고 했듯, Pretendard도 빌드 시 확보한다.

**확보 순서**:

1. **이미 설치돼 있으면** 그대로 사용(`fc-list | grep -i pretendard`).
2. 없으면 **공식 GitHub 릴리스에서 .ttf/.otf 다운로드** 후 임시 경로에 두고 렌더러에 등록:
   - 저장소: `orioncactus/pretendard` (GitHub). 릴리스 자산의 `Pretendard-Regular.ttf` / `-SemiBold` / `-Bold` 등 필요 weight.
   - 웹 폰트(CDN, HTML→PDF 파이프라인일 때): jsDelivr 등에서 `pretendard` 패키지의 `dist/web/static/pretendard.css`를 `<link>`로.
3. 다운로드도 불가하면 **폴백**(`§2.3`): `Apple SD Gothic Neo`(Mac) / `Malgun Gothic`(Win) / 시스템 sans. 폴백을 썼으면 사용자에게 한 줄 고지.
4. 숫자·좌표·레퍼런스 마커용 모노가 필요하면 **JetBrains Mono**도 같은 방식(`JetBrains/JetBrainsMono` 릴리스). 단 이 폰트는 canvas-fonts 폴더에도 있으므로(원본 경로) 거기서 가져와도 된다.

> 다운로드한 폰트 파일을 **이 스킬 디렉터리에 커밋하지 않는다.** 빌드 임시 경로(예: `/tmp/fonts/`)에 두고 렌더 후 버린다. 레포에는 *전략 문서*만 남는다.

---

## 3. 자유 모드 폰트 — canvas-fonts (대량 복사 금지)

자유 아트 모드에서만 원본의 디스플레이 폰트를 쓴다. **레포에 복사하지 말고 두 경로 중 하나로 접근**한다:

### 경로 A — 원본 폴더 직접 참조 (이 환경에서 가능할 때 권장)

원본 프리셋이 그대로 마운트돼 있으면 거기서 직접 로드한다:

```
/mnt/skills/examples/canvas-design/canvas-fonts/
```

이 폴더에 .ttf 54개 + 각 OFL 라이선스 .txt가 있다. 렌더러 폰트 경로로 이 디렉터리를 가리키면 복사 없이 사용 가능. (존재 여부는 빌드 시 확인.)

### 경로 B — 다운로드 (원본 폴더가 없을 때)

canvas-fonts는 전부 **오픈 라이선스(OFL)** 구글/오픈 폰트라 출처에서 받을 수 있다. 필요한 1~3종만 받아 임시 경로에 두고 쓴다(전부 받지 않는다). 대표 디스플레이 폰트와 출처 패밀리:

| 폰트(파일) | 성격 | 출처 패밀리 |
|-----------|------|-------------|
| `Boldonse-Regular.ttf` | 굵은 임팩트 디스플레이 | Google Fonts: Boldonse |
| `Gloock-Regular.ttf` | 하이콘트라스트 세리프 | Google Fonts: Gloock |
| `EricaOne-Regular.ttf` | 두꺼운 포스터 | Google Fonts: Erica One |
| `Italiana-Regular.ttf` | 우아한 디돈 세리프 | Google Fonts: Italiana |
| `BigShoulders-Bold.ttf` | 콘덴스트 산세리프 | Google Fonts: Big Shoulders |
| `Silkscreen-Regular.ttf` | 픽셀/레트로 | Google Fonts: Silkscreen |
| `PoiretOne-Regular.ttf` | 기하학 아르데코 | Google Fonts: Poiret One |
| `JetBrainsMono-*.ttf` | 모노(임상 라벨·홈베이스 공용) | JetBrains Mono |

> 전체 54종 목록이 필요하면 원본 폴더(경로 A)를 `ls` 하면 된다 — 본 문서에 전부 나열하지 않는다(경량). 어떤 폰트든 **OFL 라이선스 .txt를 함께 확인**하고, 산출물에 라이선스 위반·기존 작품 모사가 없게 한다.

---

## 4. 폰트를 아트의 일부로 (원본 정신)

- 추상 작품이면 폰트를 **캔버스 위 오브젝트로** 끌어들인다(디지털 식자만 하지 말 것) — 글자를 형태·패턴의 일부로.
- 텍스트 스케일은 맥락이 결정(속삭이는 라벨 vs 강한 타이포 제스처). 어떤 스케일이든 **페이지 이탈·겹침 0**.
- 홈베이스는 Pretendard의 weight 변주(400~700)만으로도 충분히 표현력 있다 — 굵기·자간·크기 대비로 위계를 만든다.

---

## 5. 체크리스트

- [ ] 레포에 .ttf 대량 복사 0건(전략 문서만 남김)
- [ ] 홈베이스: Pretendard 확보(설치→다운로드→폴백 순), 미설치 시 다운로드 또는 폴백 고지
- [ ] 자유 모드: 원본 경로(A) 우선, 없으면 필요한 폰트만 다운로드(B). 전부 받지 않음
- [ ] 사용한 모든 폰트의 OFL 라이선스 확인, 기존 작품 모사 0건
- [ ] 다운로드 폰트는 임시 경로 사용, 스킬 디렉터리에 커밋 안 함
