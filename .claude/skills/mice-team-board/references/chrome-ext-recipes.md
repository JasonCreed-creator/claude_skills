# Chrome 확장(claude-in-chrome) 레시피 — 구글 시트 · Apps Script

PC의 Claude Code 세션에서만 쓴다. 요지는 `jc-session-protocol/references/windows-env.md §3`과 같다.

---

## 1. 셀 입력

1. 이름 상자(Name Box)에 셀 주소 입력 → Enter.
2. F2로 편집 모드.
3. ctrl+a로 기존 내용 선택.
4. 값 타이핑 → Enter.

여러 셀은 행 단위로 반복. 큰 표는 사용자에게 TSV 붙여넣기를 요청하는 편이 빠르고 안전하다.

## 2. 메뉴 실행

상단 커스텀 메뉴 클릭 → 항목 클릭. 첫 실행 OAuth 승인 창은 자동화가 막힌다 → 사용자가 직접 승인.

## 3. Apps Script 코드 교체

- 편집기에 `<input type=file>`을 주입하고 `file_upload`로 파일 내용을 넣은 뒤, monaco `pushEditOperations`로 전체 교체.
- 큰 교체 직후 저장 버튼이 60초가량 무시될 수 있다 → 기다렸다 다시 저장.

## 4. 막히는 동작 (사용자 몫)

- 행·셀 삭제, Delete 키, 붙여넣기
- OAuth 승인 클릭, hCaptcha
- 화면 잠금 중에는 페이지가 활성화되지 않음
