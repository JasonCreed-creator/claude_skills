# 슬라이드 마스터 & 네이티브 자리표시자 (v1.0)

이 문서는 pptxgenjs의 `defineSlideMaster`를 활용해 PowerPoint **네이티브 그림 자리표시자**를 정의하는 방법을 다룬다. 사용자가 PowerPoint에서 placeholder를 **우클릭 → 그림 변경**으로 직접 교체할 수 있는 방식이다.

---

## 0. 기존 회색 박스 방식 vs 네이티브 자리표시자

| 방식 | 장점 | 단점 |
|------|------|------|
| **회색 박스 placeholder** (기본) | 시각적으로 명확, 캡션 가능, pptxgenjs 단순 | 우클릭 교체 불가, 사용자가 박스 삭제 후 이미지 삽입해야 함 |
| **네이티브 그림 자리표시자** (이 문서) | PowerPoint UI에서 우클릭 → 그림 변경 가능, 슬라이드 마스터 일괄 관리 | 마스터 정의 코드 복잡, 캡션 별도 처리 필요 |

**권장 적용 기준**:
- 회색 박스 방식 → 일반 제안서 (기본값)
- 네이티브 자리표시자 → 사용자가 향후 같은 템플릿으로 여러 행사 제안서를 반복 생성할 때, 또는 제안서 제출 후 발주처가 직접 이미지를 교체할 가능성이 있을 때

---

## 1. 표준 슬라이드 마스터 정의 (5종)

다음 5개의 슬라이드 마스터를 표준으로 정의한다. 모두 `defineSlideMaster`로 등록 후 `pres.addSlide({ masterName: ... })`로 사용한다.

### 1-1. MASTER_TITLE (표지)

```javascript
pres.defineSlideMaster({
  title: "MASTER_TITLE",
  background: { color: "0A2540" },  // JC Deep Navy
  objects: [
    // 배경 이미지 placeholder (풀블리드)
    {
      placeholder: {
        options: {
          name: "title_hero",
          type: "pic",         // ← 핵심: 그림 자리표시자
          x: 0, y: 0, w: 13.33, h: 7.5
        },
        text: ""
      }
    },
    // 다크 오버레이 (반투명)
    {
      rect: {
        x: 0, y: 0, w: 13.33, h: 7.5,
        fill: { color: "0A2540", transparency: 40 }
      }
    },
    // 제목 placeholder
    {
      placeholder: {
        options: {
          name: "title_main",
          type: "title",
          x: 1, y: 3.0, w: 11.33, h: 1.5,
          align: "center", valign: "middle",
          fontSize: 44, bold: true, color: "FFFFFF"
        },
        text: "[행사명 입력]"
      }
    },
    // 부제 placeholder
    {
      placeholder: {
        options: {
          name: "title_sub",
          type: "body",
          x: 1, y: 4.5, w: 11.33, h: 0.6,
          align: "center", valign: "middle",
          fontSize: 20, color: "B8C5D6"
        },
        text: "[슬로건 또는 부제]"
      }
    },
    // 로고 placeholder (하단 좌측)
    {
      placeholder: {
        options: {
          name: "logo",
          type: "pic",
          x: 0.5, y: 6.5, w: 1.5, h: 0.8
        },
        text: ""
      }
    }
  ]
});

// 사용
const titleSlide = pres.addSlide({ masterName: "MASTER_TITLE" });
titleSlide.addText("REMEMBER SUMMIT 2026", { placeholder: "title_main" });
titleSlide.addText("HR Tech의 다음 10년", { placeholder: "title_sub" });
// 이미지는 PowerPoint에서 placeholder 우클릭 → 그림 변경으로 추가
```

### 1-2. MASTER_SECTION_DIVIDER (섹션 구분)

```javascript
pres.defineSlideMaster({
  title: "MASTER_SECTION_DIVIDER",
  background: { color: "0A2540" },
  objects: [
    // 큰 섹션 번호 (반투명)
    {
      placeholder: {
        options: {
          name: "section_num",
          type: "body",
          x: 0.5, y: 1.5, w: 4, h: 3,
          fontSize: 120, bold: true,
          color: "FFFFFF", transparency: 70,
          align: "left", valign: "middle"
        },
        text: "01"
      }
    },
    // 섹션 제목
    // v1.1 패치 (2026-05-25): 박스 폭 8 → 8.5, fontSize 36 → 32 (한글 5자 이상 잘림 방지)
    {
      placeholder: {
        options: {
          name: "section_title",
          type: "title",
          x: 4.5, y: 3, w: 8.5, h: 1.5,
          fontSize: 32, bold: true, color: "FFFFFF",
          align: "left", valign: "middle"
        },
        text: "[섹션 제목]"
      }
    },
    // 섹션 부제
    {
      placeholder: {
        options: {
          name: "section_desc",
          type: "body",
          x: 4.5, y: 4.5, w: 8.5, h: 1,
          fontSize: 14, color: "B8C5D6",
          align: "left", valign: "top"
        },
        text: "[섹션 한 줄 요약]"
      }
    }
  ]
});

// 사용
const divider = pres.addSlide({ masterName: "MASTER_SECTION_DIVIDER" });
divider.addText("02", { placeholder: "section_num" });
divider.addText("운영 계획", { placeholder: "section_title" });
divider.addText("D-90부터 D+30까지, 단계별 실행 로드맵", { placeholder: "section_desc" });
```

### 1-3. MASTER_CONTENT_BASIC (기본 콘텐츠)

```javascript
pres.defineSlideMaster({
  title: "MASTER_CONTENT_BASIC",
  background: { color: "FFFFFF" },
  objects: [
    // 슬라이드 번호 (우상단)
    {
      placeholder: {
        options: {
          name: "page_num",
          type: "body",
          x: 12.5, y: 0.3, w: 0.6, h: 0.3,
          fontSize: 10, color: "5A6270",
          align: "right", valign: "top"
        },
        text: ""
      }
    },
    // 슬라이드 제목
    {
      placeholder: {
        options: {
          name: "content_title",
          type: "title",
          x: 0.5, y: 0.5, w: 12.33, h: 0.7,
          fontSize: 28, bold: true, color: "0A2540",
          align: "left", valign: "middle",
          margin: 0
        },
        text: "[제목]"
      }
    },
    // 푸터 (제안사명·페이지)
    {
      placeholder: {
        options: {
          name: "footer",
          type: "body",
          x: 0.5, y: 7.15, w: 12.33, h: 0.3,
          fontSize: 9, color: "5A6270",
          align: "left", valign: "middle"
        },
        text: "{{company_name}} │ [행사명] 제안서"
      }
    }
  ]
});
```

### 1-4. MASTER_CONTENT_WITH_HERO (좌측 이미지 + 우측 콘텐츠)

```javascript
pres.defineSlideMaster({
  title: "MASTER_CONTENT_WITH_HERO",
  background: { color: "FFFFFF" },
  objects: [
    // 좌측 메인 이미지 자리표시자 (절반 폭)
    {
      placeholder: {
        options: {
          name: "hero_image",
          type: "pic",
          x: 0, y: 0, w: 6.5, h: 7.5
        },
        text: ""
      }
    },
    // 우측 제목
    {
      placeholder: {
        options: {
          name: "content_title",
          type: "title",
          x: 7.0, y: 1.5, w: 5.83, h: 1,
          fontSize: 32, bold: true, color: "0A2540",
          align: "left", valign: "middle", margin: 0
        },
        text: "[제목]"
      }
    },
    // 우측 본문
    {
      placeholder: {
        options: {
          name: "content_body",
          type: "body",
          x: 7.0, y: 3.0, w: 5.83, h: 4,
          fontSize: 14, color: "1A1D24",
          align: "left", valign: "top"
        },
        text: "[본문]"
      }
    }
  ]
});
```

### 1-5. MASTER_THANK_YOU (Thank You)

```javascript
pres.defineSlideMaster({
  title: "MASTER_THANK_YOU",
  background: { color: "0A2540" },
  objects: [
    // 배경 이미지 자리표시자
    {
      placeholder: {
        options: {
          name: "thanks_hero",
          type: "pic",
          x: 0, y: 0, w: 13.33, h: 7.5
        },
        text: ""
      }
    },
    // 다크 오버레이
    {
      rect: {
        x: 0, y: 0, w: 13.33, h: 7.5,
        fill: { color: "0A2540", transparency: 50 }
      }
    },
    // Thank You
    {
      placeholder: {
        options: {
          name: "thanks_title",
          type: "title",
          x: 1, y: 2.5, w: 11.33, h: 1.5,
          fontSize: 72, bold: true, color: "FFFFFF",
          align: "center", valign: "middle"
        },
        text: "Thank You"
      }
    },
    // 담당자 정보
    {
      placeholder: {
        options: {
          name: "contact_info",
          type: "body",
          x: 1, y: 4.5, w: 11.33, h: 1.5,
          fontSize: 14, color: "B8C5D6",
          align: "center", valign: "top"
        },
        text: "{{company_name}} {{author_dept}} │ {{author_name}} {{author_title}}\n{{author_phone}} │ {{author_email}}"
      }
    }
  ]
});
```

---

## 2. 자리표시자 type 종류

pptxgenjs에서 사용 가능한 placeholder type:

| type | 용도 | 비고 |
|------|------|------|
| `"title"` | 슬라이드 제목 | 한 슬라이드에 1개 권장 |
| `"body"` | 본문 텍스트 | 여러 개 가능 |
| `"pic"` | 그림 자리표시자 | **PowerPoint에서 우클릭 → 그림 변경 가능** |
| `"chart"` | 차트 자리표시자 | |
| `"tbl"` | 표 자리표시자 | |
| `"media"` | 미디어 (비디오) | |

핵심은 `type: "pic"`. 이걸 정의하면 PowerPoint에서 해당 영역에 그림 아이콘이 보이고, **클릭 또는 우클릭하면 즉시 이미지 교체** 가능하다.

---

## 3. 마스터 vs 회색 박스 — 선택 의사결정

워크플로우에 다음 분기를 추가:

```
Phase 2.5 (구조 설계 후, 슬라이드 생성 전):
  사용자에게 질문:
  "이미지 자리 처리 방식을 선택해주세요.
   
   [A] 회색 박스 + 캡션 (기본) — 추천. 즉시 확인 용이.
   [B] PowerPoint 네이티브 자리표시자 — 발주처 또는 협력사가
       PowerPoint에서 직접 이미지를 교체할 가능성이 있을 때.
       슬라이드 마스터에 정의된 위치만 사용 가능.
   [A+B] 혼합 — 표지·섹션구분·Thank You만 마스터, 본문은 회색 박스."
  
  → [A+B] 권장 (시각 강조 슬라이드는 마스터, 본문은 유연성 확보)
```

---

## 4. [A+B] 혼합 모드 실행 예시

```javascript
// 1. 5개 마스터 정의 (위 §1 코드)
defineMasters(pres);

// 2. 표지 슬라이드 — 마스터 사용
const titleSlide = pres.addSlide({ masterName: "MASTER_TITLE" });
titleSlide.addText("REMEMBER SUMMIT 2026", { placeholder: "title_main" });
titleSlide.addText("HR Tech의 다음 10년", { placeholder: "title_sub" });
// 사용자는 PowerPoint에서 title_hero 자리 우클릭 → 그림 변경

// 3. 섹션 구분 — 마스터 사용
const sec1 = pres.addSlide({ masterName: "MASTER_SECTION_DIVIDER" });
sec1.addText("01", { placeholder: "section_num" });
sec1.addText("행사 개요 및 컨셉", { placeholder: "section_title" });
sec1.addText("HR 리더 1,200명이 한자리에", { placeholder: "section_desc" });

// 4. 본문 슬라이드 — 회색 박스 방식 (마스터 없이)
const contentSlide = pres.addSlide();
contentSlide.background = { color: "FFFFFF" };
// 제목, 본문, 회색 박스 placeholder 직접 추가
addImagePlaceholder(contentSlide, {
  x: 6.5, y: 2.0, w: 6.0, h: 3.6,
  caption: "[이미지: 메인 무대 렌더링]"
});

// 5. Thank You — 마스터 사용
const endSlide = pres.addSlide({ masterName: "MASTER_THANK_YOU" });
endSlide.addText("{{company_name}} {{author_dept}} │ {{author_name}} {{author_title}}\n{{author_email}} │ {{author_phone}}", { placeholder: "contact_info" });
```

---

## 5. 마스터 사용 시 주의사항

### 5-1. 마스터 자리표시자는 위치 변경 불가
사용자가 PowerPoint에서 자리표시자 위치를 옮기면 어색할 수 있다. 표지·섹션구분처럼 위치가 고정된 슬라이드에만 적용.

### 5-2. type "pic" 자리표시자에 이미지가 없을 때
PowerPoint에서 빈 그림 아이콘이 보인다. 사용자가 클릭하면 파일 탐색기가 열린다. **캡션 텍스트는 자동으로 추가되지 않으므로**, 캡션이 필요하면 마스터 정의에 별도 텍스트 박스 추가.

### 5-3. 마스터를 사용하지 않는 슬라이드와 혼용 가능
`pres.addSlide()` (마스터 없이) 와 `pres.addSlide({ masterName: ... })` 를 자유롭게 섞을 수 있다.

### 5-4. 슬라이드 노트 자동 안내 (마스터 모드)
마스터 모드 슬라이드에는 다음 노트를 자동 삽입:

```javascript
slide.addNotes(
  "■ 그림 자리표시자 사용법\n" +
  "이 슬라이드의 그림 영역은 PowerPoint 네이티브 자리표시자입니다.\n" +
  "1. 영역을 클릭하면 파일 탐색기가 열립니다.\n" +
  "2. 또는 우클릭 → '그림 변경' → '파일에서' 로 교체.\n" +
  "3. 이미지가 영역에 자동으로 맞춰 삽입됩니다."
);
```

---

## 6. 검증 체크리스트

- [ ] 5개 마스터(`MASTER_TITLE`, `MASTER_SECTION_DIVIDER`, `MASTER_CONTENT_BASIC`, `MASTER_CONTENT_WITH_HERO`, `MASTER_THANK_YOU`)가 정의되어 있음
- [ ] 그림 자리표시자 type이 `"pic"`으로 명시
- [ ] placeholder의 `name`이 중복되지 않음
- [ ] 마스터 사용 슬라이드에 노트 안내 자동 삽입
- [ ] [A+B] 혼합 모드: 강조 슬라이드만 마스터, 본문은 회색 박스
- [ ] PowerPoint에서 실제로 자리표시자 우클릭이 동작하는지 확인 (실 테스트 필요)
