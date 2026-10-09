# Apps Script 웹 대시보드

---

## 1. 구조

- 시트에 바인딩된 Apps Script 프로젝트. 서버 코드(`.gs`)가 시트를 읽고 HTML 서비스로 대시보드를 그린다.
- `styles.css`가 리멤버 웜 페이퍼 대시보드의 구현체다. CSS 변수 이름은 `jc-design-system/references/usage-guide.md §3`과 같다(`--paper`·`--ink`·`--orange`·`--s1`… ).
- 파일 목록·엔트리 함수 이름은 실측 필요(보드 프로젝트 폴더 CLAUDE.md 참조).

## 2. 수정 절차

1. 보드 프로젝트 폴더(로컬 사본)에서 수정.
2. 로컬 미리보기: `python -m http.server`로 정적 HTML 확인(`file://`은 내장 브라우저가 거부).
3. 사용자 승인.
4. 반영: ① 사용자가 Apps Script 편집기에 붙여넣기 ② PC 세션이 Chrome 확장으로 코드 교체(`chrome-ext-recipes.md §3`) ③ clasp·CI 배포가 설정돼 있으면 그 경로(회사 계정 배포는 사용자).
5. 웹앱 새 버전 배포 → 대시보드 새로고침으로 확인.

## 3. 토큰 동기화

- `styles.css`의 값은 `jc-design-system` 토큰과 같아야 한다. 디자인 시스템 버전이 바뀌면 `styles.css`도 같이 맞추고 비고에 디자인 시스템 버전을 적는다.
- 보드에서 임의로 새 색을 만들지 않는다.
