# 베뉴 DB (venue-db)

**상태**: ⏳ **데이터 보류 — MiceConfigurator 자산 이관 필요**
**스키마**: 본 문서로 동결
**데이터 채움 일정**: Sprint 1 종료 후 별도 사이클(Sprint 1.5) 또는 Phase 1 DB 마이그레이션 시
**SSOT**: 견적Configurator_로직명세서_v1_0.md §3 (cfg.venueRental 자동 산출), §5.3 Section 1 (s1 베뉴 사용료)

본 문서는 v2.0에서 **스키마와 슬롯만 동결**한다. 실제 20개 베뉴 데이터는 MiceConfigurator(사용자 자체 개발 SaaS) 의 자산으로, 본 스킬로 이관되기 전까지 calcEstimate 는 `venueRental` 직접입력 또는 `target × VENUE_PER_PAX_5STAR` 자동 산출 두 경로로만 동작한다.

---

## 1. 베뉴 식별 스키마

각 베뉴는 다음 필드를 갖는다:

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `venue_id` | str | ✅ | 슬러그 형태 (예: `seoul-gangnam-chosun-palace`) |
| `venue_name` | str | ✅ | 표시 이름 (외부 주입 변수, 마케팅 명칭) |
| `region` | str | ✅ | 지역 (예: "서울 강남", "서울 광화문", "성남 분당") |
| `venue_type` | str | ✅ | `5star` / `conference_center` / `convention_center` / `hotel_grade1` |
| `max_capacity` | int | ✅ | 최대 수용 인원 (착석 기준) |
| `per_pax_rate` | int / null | 선택 | 베뉴별 인당 단가. null 이면 type별 표준 단가(`VENUE_PER_PAX_5STAR` 등) 적용 |
| `min_rental` | int / null | 선택 | 최소 대관료 (작은 행사 시 baseline) |
| `amenities` | list[str] | 선택 | 비고 키워드 (예: ["LED 월", "VIP 라운지", "주차 200대"]) |
| `notes` | str | 선택 | 추가 메모 |

### 1.1 JSON 직렬화 예시 (스키마)

```json
{
  "venue_id": "seoul-gangnam-chosun-palace",
  "venue_name": "{외부 주입 - 베뉴 마케팅 명칭}",
  "region": "서울 강남",
  "venue_type": "5star",
  "max_capacity": 500,
  "per_pax_rate": null,
  "min_rental": null,
  "amenities": ["{외부 주입}"],
  "notes": ""
}
```

---

## 2. 슬롯 20개 (데이터 보류)

MiceConfigurator 의 베뉴 DB로부터 이관 예정. 본 Sprint 종료 시점에서는 식별자만 잡혀있고 실데이터는 비어있음. 사용자가 실데이터를 제공하면 본 문서에 채워넣음.

| # | venue_id | region | venue_type | max_capacity | per_pax_rate | 상태 |
|---|---|---|---|---|---|---|
| 1 | {slot-01} | (서울 강남) | 5star | TBD | TBD | ⏳ |
| 2 | {slot-02} | (서울 강남) | 5star | TBD | TBD | ⏳ |
| 3 | {slot-03} | (서울 광화문) | 5star | TBD | TBD | ⏳ |
| 4 | {slot-04} | (서울 광화문) | 5star | TBD | TBD | ⏳ |
| 5 | {slot-05} | (서울 중구) | 5star | TBD | TBD | ⏳ |
| 6 | {slot-06} | (서울 중구) | 5star | TBD | TBD | ⏳ |
| 7 | {slot-07} | (서울 잠실) | 5star | TBD | TBD | ⏳ |
| 8 | {slot-08} | (서울 잠실) | conference_center | TBD | TBD | ⏳ |
| 9 | {slot-09} | (서울 영등포) | 5star | TBD | TBD | ⏳ |
| 10 | {slot-10} | (서울 영등포) | conference_center | TBD | TBD | ⏳ |
| 11 | {slot-11} | (서울 마포) | 5star | TBD | TBD | ⏳ |
| 12 | {slot-12} | (서울 용산) | 5star | TBD | TBD | ⏳ |
| 13 | {slot-13} | (서울 강북) | hotel_grade1 | TBD | TBD | ⏳ |
| 14 | {slot-14} | (서울 강남) | conference_center | TBD | TBD | ⏳ |
| 15 | {slot-15} | (성남 분당) | 5star | TBD | TBD | ⏳ |
| 16 | {slot-16} | (성남 분당) | convention_center | TBD | TBD | ⏳ |
| 17 | {slot-17} | (경기 일산) | convention_center | TBD | TBD | ⏳ |
| 18 | {slot-18} | (인천 송도) | convention_center | TBD | TBD | ⏳ |
| 19 | {slot-19} | (부산 해운대) | 5star | TBD | TBD | ⏳ |
| 20 | {slot-20} | (제주) | 5star | TBD | TBD | ⏳ |

지역 분포는 SSOT 작성자(사용자)의 일반적 행사 분포 패턴을 추정한 시안 — 실데이터 이관 시 갱신.

---

## 3. 룩업 함수 시그니처 (예약 — 실데이터 입수 후 구현)

```python
def lookup_venue(venue_id: str) -> dict | None:
    """venue_id로 메타데이터 조회. 미존재 시 None.
    
    데이터 보류 상태에서는 항상 None 반환 (호출자가 venueRental 직접입력 또는
    target × VENUE_PER_PAX_5STAR 폴백 사용).
    """
    return None


def list_venues_by_region(region: str) -> list[dict]:
    """지역명으로 베뉴 후보 조회. 데이터 보류 상태에서는 빈 리스트 반환."""
    return []
```

---

## 4. calcEstimate 와의 연동 (현재 / 미래)

### 4.1 현재 (v2.0, 데이터 보류)

`calc_estimate.py` 의 Section 1 베뉴 사용료(s1) 계산:

```python
def _calc_s1_venue(c):
    rental = c.get('venueRental')
    if rental is not None:
        return int(rental)         # 사용자가 직접 입력한 경우
    return c['target'] * VENUE_PER_PAX_5STAR    # 자동 산출 (5성급 표준)
```

→ 베뉴별 단가가 다른 경우라도 사용자가 `venueRental` 에 직접 입력하면 그 값 사용.

### 4.2 미래 (데이터 입수 후, Sprint 1.5)

```python
def _calc_s1_venue(c):
    venue_id = c.get('venueId')
    if venue_id:
        meta = lookup_venue(venue_id)
        if meta:
            if meta['per_pax_rate']:
                rental = c['target'] * meta['per_pax_rate']
            else:
                rental = c['target'] * VENUE_PER_PAX_5STAR
            if meta['min_rental'] and rental < meta['min_rental']:
                rental = meta['min_rental']
            return rental
    # 폴백: 기존 로직
    ...
```

---

## 5. 보류 사항 및 추가 자산 정합

| 항목 | 보류 사유 | 해소 방법 |
|---|---|---|
| 20개 베뉴 실데이터 (이름·단가·수용·비고) | MiceConfigurator 자산, 본 스킬로 미이관 | 사용자가 SaaS 데이터 export → 본 문서로 옮김 |
| 베뉴별 `per_pax_rate` 차등화 | SSOT §5.3 가 단일 상수(`VENUE_PER_PAX_5STAR`) 사용 | 데이터 이관 + calcEstimate 보강 동반 |
| `convention_center`·`hotel_grade1` 등 비-5성급 단가 | SSOT 미정의 | 사용자 단가 정책 명시 |
| 베뉴 amenities·notes 의 자유텍스트 표준화 | 실데이터 형태 미확인 | 데이터 이관 시 결정 |

본 보류 사항은 [validation-report.md](../../validation-report.md) 의 "백로그 승계" 섹션에 기록되어 Sprint 1.5 또는 Phase 1에서 처리.

---

## 6. 본 Sprint 의 결정

- ✅ 스키마 동결 (필드 9종, JSON 직렬화 형태)
- ✅ 슬롯 20개 식별자 + 지역 분포 시안 (실데이터 이관 시 갱신)
- ✅ 룩업 함수 시그니처 예약 (구현은 데이터 입수 후)
- ⏳ 실데이터 채움 — **Sprint 1.5 또는 사용자 자산 이관 후**
- ❌ calcEstimate 가 venue_id 기반 룩업 사용하도록 변경 — **데이터 입수 전까지 보류**
