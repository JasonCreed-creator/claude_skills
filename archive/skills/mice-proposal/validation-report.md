# mice-proposal v2.1 검증 결과 리포트

**검증 일자**: 2026-05-25
**검증 환경**: Node 22 / pptxgenjs 4.0.1 / react-icons 5.6.0 / sharp 0.34.5 / LibreOffice (PDF 변환)
**가상 RFP 시나리오**: REMEMBER SUMMIT 2026 (HR Tech 컨퍼런스, 리멤버 협업, 1,200명)
**적용 모드**: JC + 리멤버 오버레이 / 혼합 이미지 / 최소 다크 / Heroicons
**검증 슬라이드 수**: 17장 (패턴 중심 압축 검증)

---

## 1. 검증 결과 종합

### 최종 점수
- **PASS**: 17 / 17 (100%) — 결함 수정 후
- **검증 전 PASS**: 13 / 17 (76%)
- **발견 결함**: 4건 (CRITICAL 2건 + MINOR 2건)
- **수정 완료**: 4건 (100%)

---

## 2. 패턴별 검증 결과

| 슬라이드 | 패턴 | 검증 전 | 수정 후 | 결함 ID |
|---------|------|--------|--------|--------|
| 01 | IMG-HERO + MASTER-TITLE | ✅ PASS | ✅ PASS | - |
| 02 | MASTER-SECTION_DIVIDER | 🐛 CRITICAL | ✅ PASS | F1 |
| 03 | CHART-C3 + ICON | ⚠️ MINOR | ✅ PASS | F4 |
| 04 | DIAG-D4 + ICON | ✅ PASS | ✅ PASS | - |
| 05 | TBL-T2 (매트릭스 표) | ✅ PASS | ✅ PASS | - |
| 06 | TBL-T4 (예산표) | ✅ PASS | ✅ PASS | - |
| 07 | CHART-C1 (도넛) | ✅ PASS | ✅ PASS | - |
| 08 | CHART-C2 (바) | ✅ PASS | ✅ PASS | - |
| 09 | DIAG-D1 (조직도) | ✅ PASS | ✅ PASS | - |
| 10 | DIAG-D2 + ICON | ✅ PASS | ✅ PASS | - |
| 11 | DIAG-D3 (타임라인) | ⚠️ MINOR | ✅ PASS | F3 |
| 12 | INFO-I1 (퍼널) | ✅ PASS | ✅ PASS | - |
| 13 | INFO-I2 (매트릭스) | 🐛 CRITICAL | ✅ PASS | F2 |
| 14 | INFO-I3 (레이더) | ✅ PASS | ✅ PASS | - |
| 15 | DARK-C3 | ⚠️ MINOR | ✅ PASS | F4 |
| 16 | DARK-D4 | ✅ PASS | ✅ PASS | - |
| 17 | MASTER-THANK_YOU | ✅ PASS | ✅ PASS | - |

---

## 3. 결함 상세 및 수정 내역

### F1 (CRITICAL) — MASTER_SECTION_DIVIDER 제목 텍스트 잘림

- **증상**: 섹션 제목 "행사 개요 및 컨셉"의 마지막 글자 "셉"이 박스 끝에 걸쳐서 시각적으로 잘려 보임
- **원인**: section_title placeholder 박스 폭(`w: 8"`)과 fontSize(36pt)에 비해 한글 5자 + 영문 1자 텍스트가 길어 오버플로우
- **수정**: 
  - `slide-masters.md` MASTER_SECTION_DIVIDER 정의: `w: 8 → 8.5`, `fontSize: 36 → 32`
  - section_desc도 동일하게 `w: 8 → 8.5` 적용
- **재검증**: ✅ PASS (충분한 여백 확보)

### F2 (CRITICAL) — INFO-I2 매트릭스 라벨 충돌

- **증상**: 
  1. 사분면 라벨 "프리미엄 리더"가 Y축 라벨 "↑ 전문성"과 겹침
  2. 데이터 점 라벨 "경쟁사 A"가 X축 라벨 "규모 →"와 겹쳐 잘림
- **원인**: 
  1. 사분면 라벨이 코너 끝(`x + halfW + 0.2`, `y + 0.2`)에 너무 가깝게 배치
  2. X축 라벨이 매트릭스 내부 우측(`x + w - 1.5`)에 배치되어 점과 충돌
- **수정**:
  - `infographic-patterns.md` `addMatrix()` 함수:
    - 사분면 라벨 좌표를 0.3" 안쪽으로 이동, y는 +0.3 내림 (상단 라벨 Y축 라벨 회피)
    - X축 라벨 `xLabel`을 매트릭스 우측 **바깥**(`x + w + 0.1`)에 배치
    - Y축 라벨 `yLabel`을 매트릭스 상단 **바깥**(`y - 0.5`)에 배치
  - 호출 예시: 매트릭스 y 시작 좌표에 0.5" 여유 확보 권장 (사용 노트 추가)
- **재검증**: ✅ PASS (모든 라벨 명확하게 표시, 충돌 없음)

### F3 (MINOR) — DIAG-D3 타임라인 구간 밴드 가시성 부족

- **증상**: 4개 구간 밴드 중 1개만 미약하게 보이고 나머지 3개는 거의 식별 불가
- **원인**: 컬러 4종이 모두 매우 옅음(`EBF4F9`, `D5E8F3`, `BFDCED`, `EBF4F9`) + 투명도 50%까지 적용되어 가시성 거의 0
- **수정**:
  - `visual-patterns.md` DIAG-D3 패치 노트 추가
  - 권장 컬러: `D5E8F3 / A7CFE5 / 7AB6D6 / D5E8F3` (단계별 진해짐 — 시간 흐름 시각화)
  - 투명도: 50% → 20%
- **재검증**: ✅ PASS (모든 구간 밴드가 명확히 식별됨, 단계 진행감 표현)

### F4 (MINOR) — 빅넘버 콜아웃 천단위 콤마 누락

- **증상**: 슬라이드 03 (라이트 빅넘버), 슬라이드 15 (다크 빅넘버) 모두 "1200"으로 표시. 한국 비즈니스 문서 관행상 "1,200"이 표준
- **원인**: `String(value)` 단순 변환으로 콤마 미적용
- **수정**:
  - `visual-patterns.md` `addBigNumberCallout()` 함수: number 타입 체크 후 `toLocaleString("ko-KR")` 적용
  - `dark-mode-patterns.md` `addDarkBigNumberCallout()` 함수: 동일 수정
  - string 타입 value (예: "9.5K")는 그대로 출력하여 호환성 유지
- **재검증**: ✅ PASS ("1,200" 정상 표시)

---

## 4. 검증 안 한 정상 동작 (Known Behavior)

다음은 결함이 아니지만 사용자에게 안내가 필요한 동작:

### KB-1. 마스터 그림 자리표시자의 PDF 렌더 비표시
- **현상**: PDF로 변환 시 마스터에 정의된 `type: "pic"` 자리표시자 영역이 보이지 않음 (슬라이드 01의 HERO 영역, 17의 THANKS_HERO)
- **이유**: 자리표시자는 PowerPoint UI에서만 표시되는 편집 보조 요소. 실제 콘텐츠가 없으면 빈 영역으로 처리됨
- **사용자 경험**: PowerPoint에서 열면 자리표시자 영역 클릭으로 이미지 삽입 가능. PDF 출력 시에는 안 보이는 게 정상

### KB-2. 한글·영문 사이 자동 공백 (Auto-Spacing)
- **현상**: "HR Tech 의 다음 10 년", "리멤버 DB 활용" 등 한글·영문 사이에 자동으로 공백이 들어가 보임
- **이유**: PowerPoint/LibreOffice의 동아시아 텍스트 자동 정렬 기능. Pretendard 폰트 미설치 환경에서 시스템 폰트로 폴백 시 더 두드러짐
- **해결**: 
  - 사용자 PC에 Pretendard 설치 권장 (슬라이드 노트에 안내 자동 삽입됨)
  - 또는 PowerPoint 옵션 → 한국어 → "한글과 영어 텍스트 사이에 공백 추가" 해제

---

## 5. 검증 환경 한계

- **검증 도구**: LibreOffice headless PDF 변환 → pdftoppm 이미지 추출
- **한계**: 
  - PowerPoint 네이티브와 LibreOffice 렌더링 결과가 미세하게 다를 수 있음
  - 폰트 폴백 동작이 환경마다 다름 (검증 환경에는 Pretendard 미설치, 시스템 한글 폰트로 렌더됨)
  - 자리표시자 우클릭 → 그림 변경 인터랙션은 실제 PowerPoint에서만 확인 가능 (LibreOffice는 별도 검증 필요)
- **권장**: 다음 실제 RFP 작업 시 첫 PPTX 생성 결과를 사용자 PC의 PowerPoint에서 한 번 더 확인

---

## 6. 후속 조치 (없음)

검증으로 발견된 결함 4건 모두 수정 완료. v2.1은 실전 사용 가능 상태.

다음 작업은 **실제 RFP를 입력으로 한 제안서 생성**이 적절함.
