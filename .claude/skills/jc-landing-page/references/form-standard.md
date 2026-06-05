# 폼 표준 (jc-landing-page)

B2B 랜딩 폼의 기본 필드·전화번호 자동 하이픈·개인정보 수집·이용 동의·제출 처리(GAS) 정본. SKILL.md §4가 이 문서를 가리킨다. 개인정보 동의는 SKILL.md §1.4(필수)와 연동.

### 4.1 기본 필드 (B2B 기준)
- 이름 (필수)
- 회사명 (필수)
- 직책 / 부서 (필수 또는 선택, 캠페인에 따라)
- 이메일 (필수) — 회사 이메일 권장 안내
- 전화번호 (필수) — **자동 하이픈 처리 JS 포함**
- 캠페인별 추가 질문 (관심사, 도입 시기, 예산 등 — 캠페인에 따라)

### 4.2 전화번호 자동 하이픈 JS
```javascript
function autoHyphen(value) {
  return value.replace(/[^0-9]/g, '')
    .replace(/(^02|^0505|^1[0-9]{3}|^0[0-9]{2})([0-9]+)?([0-9]{4})$/,
      (m, p1, p2, p3) => p2 ? `${p1}-${p2}-${p3}` : `${p1}-${p3}`);
}
// input의 oninput 이벤트에 연결
```

### 4.3 개인정보 수집·이용 동의 (필수 포함)

**체크박스 + 동의 내용 펼침/접힘 구조**로 구현. 표준 문구:

```
[필수] 개인정보 수집·이용에 동의합니다.

수집 항목: 이름, 회사명, 직책, 이메일, 전화번호
수집 목적: 신청한 [리포트/웨비나/세미나/상담] 제공 및 관련 정보 안내,
          [발송 주체 회사명]의 B2B 마케팅 솔루션 안내
보유 기간: 수집일로부터 3년 (또는 동의 철회 시까지)

귀하는 동의를 거부할 권리가 있으며, 거부 시 신청이 제한될 수 있습니다.
```

체크 안 하면 제출 버튼 비활성화 또는 alert 처리.

### 4.4 폼 제출 처리 패턴
```javascript
async function submitForm(data) {
  try {
    const res = await fetch('GOOGLE_APPS_SCRIPT_WEB_APP_URL', {
      method: 'POST',
      mode: 'no-cors',  // GAS는 CORS 응답을 못 주므로 필요
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(data)
    });
    // no-cors 모드에서는 response를 읽을 수 없으므로 성공 화면으로 즉시 전환
    showSuccessScreen();
  } catch (e) {
    alert('신청 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
  }
}
```

GAS 코드 자리에 플레이스홀더(`GOOGLE_APPS_SCRIPT_WEB_APP_URL`)를 명시적으로 남겨두고, 작업물 안내 시 "이 부분에 GAS 배포 URL을 넣으시면 됩니다"라고 명시한다.

---
