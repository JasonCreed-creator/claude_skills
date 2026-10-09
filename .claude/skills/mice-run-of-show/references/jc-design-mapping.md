# jc-design-system 매핑 — 큐시트 XLSX (리멤버 웜 페이퍼)

xlsx는 CSS 변수가 불가능한 매체다. `build_runsheet.py`는 jc-design-system SoT(`signature-tokens.md §6` JSON)를 **런타임 로드**하고, 로드 실패 시에만 §6 폴백 상수를 쓴다. 값의 정본은 항상 jc-design-system. 사용 패턴은 `jc-design-system/references/usage-guide.md`(큐시트: 헤더 잉크 밴드 + 웜 서피스 행).

> openpyxl은 `#` 없는 6자리 사용. 탐색 순서: 형제 경로 → `~/.claude/skills/jc-design-system` → `~/.claude/skills/synced/*/jc-design-system`.

---

## 1. 역할 → 토큰 매핑 (`TOKEN_ROLES`)

| 위치 | 역할 | SoT 키 (§6 color) | §6 폴백 |
|------|------|------------------|---------|
| 타이틀·메타 행 (행사명·일자·베뉴·버전·발행 명의) | 잉크 밴드 | `primary` | `1A1A1A` |
| 잉크 위 글자 | 웜 페이퍼 글자 | `bg` | `FBFAF6` |
| 컬럼 헤더 행 면 (Cue#…비고) | 웜 서피스 | `surfaceSoft` | `EFEBE2` |
| 컬럼 헤더 하단 룰 | 오렌지 룰 | `accent` | `EB6F2A` |
| 연출 cue 강조 글자 | 딥 오렌지(작은 글자용) | `accentStrong` | `B8431A` |
| 휴식·전환 행 배경 | 보조 면 | `surfaceAlt` | `F4F1EA` |
| 셀 테두리 | 테두리 | `borderStrong` | `CFC8BC` |
| 본문 텍스트 | 본문 + Pretendard | `text` | `1A1A1A` |

- 조회 키는 §6에 **실재하는 키만** 쓴다. v1.0.0은 없는 키(`orange`)를 조회해 연출 cue 색만 구 값으로 폴백되며 색이 섞였다 → v1.1.0에서 수정, `--self-test`가 키 누락·legacy 색 혼입을 실패로 잡는다.
- 오렌지 글자는 작은 글씨에서 `accentStrong`만(대비 확보, `shared-rules.md#RULE-WCAG`).

---

## 2. 발주처 · 명의

- 발행 명의 기본 `리멤버 MICE비즈팀`(메타 행). `event['publisher']`로 바꿀 수 있다.
- 발주처는 행사명·베뉴 등 텍스트로만 주입한다. 발주처 색을 받아도 리멤버 오렌지·잉크는 바꾸지 않는다(`client-overlays.md`).
- 구 네이비·일렉트릭블루 룩은 legacy-jc 오버레이로 명시 요청 시만(jc-design-system 경유). 기본 산출에는 쓰지 않는다.

---

## 3. 폰트

- 한글·영문 `Pretendard`. 숫자(시간·Cue#)는 일반 셀, 가운데 정렬.
- 타이틀 Bold(웜 페이퍼 글자 on 잉크), 컬럼 헤더 Bold(잉크 글자 on 웜 서피스), 본문 일반.

---

## 4. 인쇄 (RULE-PRINT-LIGHT)

큐시트는 현장 인쇄 빈도가 높다. 기본이 라이트이므로 다크 강제 불필요. 잉크 면적은 타이틀·메타 2행으로 제한해 토너 과다를 막는다.
