# 계약완료 메시지 → 파싱 · 신규/갱신 판단 · contract 페이로드

`MICE 계약완료` 봇 메시지를 파싱해 기존 행과 대조(신규/갱신·상태 힌트)하고 `contract` 페이로드(§6)로 넘기는 규칙. 시트 열 정의·행 값 표·시트 조작은 `mice-team-board`. 2026-09-13·16 실제 등록 사례 6건으로 검증(고객사명은 가명 처리).

---

## 1. 메시지 스키마

```
[MICE 계약완료] {고객사}/@{영업 담당}
* 고객사: {고객사}
   * 산업 lv1: {…}   * 산업 lv2: {…}
* 주제: {행사명 또는 계약명}
* 계약 매출(부가세 별도): {숫자}원
   * 계약금(부가세 별도): {숫자 | 조건 문구}
* 행사일시: {영문 날짜, UTC}
* 행사장소: {베뉴}
* 목표: {쇼업·리드 목표 문장}
* 타깃조건: {조건 서술}
   * 사전 모수 파악 자료: {URL | -}
* 재계약ID: {…}   * 아이템ID: {…}
* 계약서류: {Drive URL}
* 인입채널: {관리영업 | 행사 | 기타}
* 비고/참고사항: {결제 조건·PO·리드 수·특이사항}
* 운영요청: @리드젠_cell_a | @리드젠_cell_b
cc. @리드젠프로젝트 @리드세일즈팀
```

## 2. 파싱 규칙

| 필드 | 처리 |
|------|------|
| 행사일시 | **UTC → KST(+9)** 변환. 예 `October 20th, 2026 at 4:00 AM UTC` → 2026-10-20 13:00. 시각이 12:00 AM UTC면 09:00 KST(날짜는 같음) |
| 계약 매출 | 숫자만 추출(원, VAT 별도). "VAT제외" 표기 유지 |
| 계약금 | 숫자 또는 조건 문구("행사 끝난 후 전액완납")를 비고로 |
| 목표 | 쇼업 수·리드 수를 숫자로 뽑아 게런티·예상 참가로 |
| 타깃조건 | 원문은 `target_conditions`에 보존. 보드에는 요지만 O 비고(`notes`)에 |
| 운영요청 | Cell A/B → 담당 운영 PM 미정 표시 |
| 주제 `[DMS 파트너십 계약]` | 자사 주최형 스폰서십 → §4 |

## 3. 메시지 필드 → payload 키 (`contract.*`)

시트 열(A~P)·배정/마일스톤 탭 규칙의 정본은 `mice-team-board/references/sheet-schema.md` §2~3이고, 행 값 표는 `mice-team-board/scripts/board_rows.py`가 이 페이로드로 만든다. 본 절은 메시지 → payload 매핑만 정한다(열은 참고 표기).

| 메시지 필드 | payload 키 | 보드 열(참고) |
|-------------|-----------|---------------|
| 고객사 · 산업 lv1/lv2 | `client` · `industry[]` | C · — |
| 주제 | `title` | B |
| 계약 매출 | `revenue`(원, VAT 별도, 숫자) | N |
| 계약금 | `deposit`(숫자 또는 null) · `deposit_note`(조건 문구) | O에 포함 |
| 행사일시 | `event_at_kst`(UTC → KST) | F |
| 행사장소 | `venue` | K |
| 목표 | `guarantee`(쇼업) · `leads` | L·M · O에 포함 |
| 타깃조건 | `target_conditions`(원문) | 요지만 O에 포함 |
| 재계약ID · 아이템ID · 인입채널 | `renewal_id` · `item_id` · `inbound` | O에 포함 |
| 계약서류 | `docs_url` | — |
| 비고/참고사항 | `notes`에 녹임 | O |
| 운영요청 | `ops_cell` | O에 포함 |
| `@영업 담당` | `sales_owner` | 배정 탭(영업 3 M/D) — 수기 |
| (판단) 유형 · 신규/갱신 · 상태 | `type`(①~④) · `action` · `matched_row` · `status_hint` | D · A · E |

유형 ① 리멤버 MICE 솔루션(모객+운영) / ② 일반 행사(게런티 없음) / ③ DMS·주최형 / ④ 커스터마이즈.

## 4. 신규 vs 갱신 판단

1. 발주처(C) + 행사일(F) 또는 행사명(B)으로 기존 행을 먼저 대조한다.
2. 이미 "견적"·"계약" 상태로 등록된 건(견적 단계에서 선등록)이면 **행 갱신** — 행사명·계약금액·게런티·비고 교체. 마일스톤·정산·배정 행을 새로 만들지 않는다(2026-09-16 A사 사례).
   - 상태는 `status_hint`로 넘긴다: 기존 행이 `견적`이면 `"계약"`, `계약`·`준비` 이후면 `"keep"`(기본 — 역행 금지), 이 메시지로 MICE PM 배정·킥오프 착수가 확인되면 `"준비"`.
3. 없으면 **신규 행** + 표준 마일스톤 생성(메뉴 "표준 마일스톤 생성") + 영업 배정 행.
4. 판단이 갈리면 사용자에게 두 후보를 보여주고 결정을 받는다.

## 5. DMS 스폰서십 (③ 주최형)

- 자체 행사라 계약금액이 따로 없고 파트너(스폰서)별 계약이 쌓인다. 보드에는 행사 1행 + 계약금액 = 파트너 합계(가상 예: 스폰서 B사 5,000만 + C사 4,000만 + D사 3,000만 = 1억 2,000만).
- 스폰서별 계약완료 메시지는 같은 행의 비고에 누적. Slack 프로토콜상 스레드는 스폰서별로 따로.

## 6. ChainPayload (source `mice-slack-ops`)

```json
{
  "$schema": "ChainPayload/v1", "source": "mice-slack-ops", "version": "<스킬 버전>",
  "generatedAt": "2026-09-21T09:00:00+09:00", "target": "mice-team-board",
  "projectTitle": "A사 테크 서밋 2026",
  "contract": {
    "client": "A사", "industry": ["클라우드 서비스", ""],
    "title": "A사 테크 서밋 2026",
    "revenue": 30000000, "deposit": null, "deposit_note": "행사 후 전액 완납(USD)",
    "event_at_kst": "2026-10-20T13:00:00+09:00", "venue": "[5성 호텔]",
    "guarantee": 30, "leads": 50, "target_conditions": "기업리스트 100+ · 임원급 이상 …",
    "renewal_id": "00000", "item_id": "00000", "docs_url": "https://drive.google.com/…",
    "inbound": "관리영업", "ops_cell": "A", "sales_owner": "김OO",
    "type": "①", "action": "update", "matched_row": "P-2026-003", "status_hint": "keep",
    "notes": "행사 후 전액 완납(USD) · PO 대체 · 리드 50(참석 30 + 신청 20) · 타깃 임원급 이상 · 재계약ID 00000 · 아이템ID 00000 · 인입 관리영업 · 운영 Cell A F/U"
  }
}
```

- `action`은 `new | update`. `matched_row`는 갱신 시 기존 프로젝트ID.
- `status_hint`는 `keep | 계약 | 준비`(기본 `keep`, §4). 신규는 `계약`(또는 `준비`), 갱신은 `계약`·`준비`일 때만 E열을 바꾸고 `keep`이면 비워 둔다(유지).
- `notes`는 **O열 비고 완성 문자열**이다 — 결제 조건 · PO/계약서 형태 · 리드 수 · 타깃 요지 · 재계약ID · 아이템ID · 인입채널 · 운영 Cell 순, ` · ` 구분. 구조 필드(`deposit_note`·`leads`·`target_conditions`·`renewal_id`·`item_id`·`inbound`·`ops_cell`)는 기계 판독용으로 함께 두되 `board_rows.py`는 `notes`를 그대로 쓰고 다시 붙이지 않는다(`notes`가 비었을 때만 구조 필드로 조립).
- `sales_owner`·`deposit`(숫자)은 프로젝트 탭에 쓰지 않는다. 배정 탭 영업 3 M/D 행은 수기.
