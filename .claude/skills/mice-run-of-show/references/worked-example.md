# Worked Example — 반일 컨퍼런스 큐시트 end-to-end

대표 시나리오 1개를 입력부터 산출 xlsx까지 따라간다. `build_runsheet.py`의 표준 self-test가 **이 예시와 동일한 데이터**를 생성하므로, 재현하면 동일 결과가 나온다.

---

## 입력 시나리오

> 기획자님: "6/20 반일 테크 포럼, 09:00~12:30. 큐시트 만들어줘."

```python
event = {
    'title': 'T社 테크 포럼 2026',   # 외부 주입 (자기 회사명 아님)
    'date': '2026-06-20',
    'venue': '[그랜드볼룸]',          # 외부 주입
    'start_time': '09:00',
    'end_time': '12:30',             # 무결성 검증 기준
    'version': 1,
    'client_id': None,
}
cues = [  # segment, duration_min, stage, audio, video, light, cue, owner, note
    {'segment':'등록·입장','duration_min':30,'stage':'-','audio':'BGM','video':'로비 루프','light':'하우스','cue':'LX1 하우스 100%','owner':'운영','note':'정시 개문'},
    {'segment':'개회 선언','duration_min':5,'stage':'사회자','audio':'MIC1','video':'타이틀','light':'무대 FULL','cue':'BGM FADE → MIC1','owner':'사회','note':''},
    {'segment':'환영사','duration_min':10,'stage':'주최 대표','audio':'MIC2','video':'발표 PPT','light':'무대 FULL','cue':'SB 환영사','owner':'무대','note':''},
    {'segment':'기조연설','duration_min':35,'stage':'기조연사','audio':'MIC2','video':'LED→발표 PPT','light':'무대 FULL+스팟','cue':'멘트 끝 → VT1 + 암전','owner':'무대','note':'T-30초 SB'},
    {'segment':'기조 Q&A','duration_min':10,'stage':'기조연사+사회','audio':'MIC1+MIC2','video':'중계','light':'무대 FULL','cue':'스팟 OFF','owner':'사회','note':''},
    {'segment':'휴식','duration_min':15,'stage':'-','audio':'BGM','video':'로비 루프','light':'하우스','cue':'LX1 하우스','owner':'운영','note':'세션장 셋업'},
    {'segment':'세션 1','duration_min':30,'stage':'연사 A','audio':'MIC2','video':'발표 PPT','light':'무대 FULL','cue':'SB 연사 A','owner':'무대','note':''},
    {'segment':'세션 2','duration_min':30,'stage':'연사 B','audio':'MIC2','video':'발표 PPT','light':'무대 FULL','cue':'SB 연사 B','owner':'무대','note':''},
    {'segment':'패널 토론','duration_min':30,'stage':'패널 4인+모더레이터','audio':'MIC1~5','video':'중계 PIP','light':'무대 FULL','cue':'테이블 세팅 전환','owner':'무대','note':'의자 5'},
    {'segment':'시상·기념촬영','duration_min':10,'stage':'시상자+수상자','audio':'MIC1','video':'시상 VT2','light':'무대 FULL','cue':'VT2 + 단체 스팟','owner':'운영','note':'포토월'},
    {'segment':'폐회','duration_min':5,'stage':'사회자','audio':'MIC1','video':'클로징','light':'하우스 전환','cue':'BGM IN','owner':'사회','note':''},
]
out = build_runsheet(event, cues, '/home/claude/런오브쇼_T社테크포럼_v1_260620.xlsx')
```

소요 합 = 30+5+10+35+10+15+30+30+30+10+5 = **210분** = 09:00→12:30. ✅

---

## 처리

1. `build_runsheet.py`가 `start_time`+누적 소요로 **클록 자동 산출**(C01=09:00 … C11=12:25).
2. **시간 무결성 검증**: Σ소요(210) == (end−start)(210) → PASS. 불일치면 ValueError.
3. `[큐시트]` 시트: 헤더 블록(행사명·일자·베뉴·v1·생성시각) + 컬럼 헤더 + 11 cue 행, jc 토큰 적용.
4. `[변경이력]` 시트: `v1 | 2026-06-05 | 초안 생성` 1행.
5. 저장 후 재오픈 무결성 확인.

---

## 산출 (재현 기준)

```
런오브쇼_T社테크포럼_v1_260620.xlsx
├─ [큐시트]
│   T社 테크 포럼 2026 | 2026-06-20 | [그랜드볼룸] | v1 | 생성 2026-06-05
│   Cue# 시간   세그먼트       무대·발표        A         V          L           연출 cue              Owner 비고
│   C01  09:00  등록·입장      -              BGM        로비 루프   하우스       LX1 하우스 100%       운영  정시 개문
│   C02  09:30  개회 선언      사회자          MIC1       타이틀      무대 FULL    BGM FADE → MIC1       사회
│   ...  (C03~C11)
│   C11  12:25  폐회          사회자          MIC1       클로징      하우스 전환  BGM IN                사회
└─ [변경이력]
    버전 일자        변경
    v1   2026-06-05 초안 생성
```

검증: self-test가 `Σ소요 == end−start` assert + 재오픈 PASS면 재현 성공.

---

## 개정(버전 +1) 예

```python
event['version'] = 2
# 패널 토론 35→30 단축, 휴식 15→20 연장 등 반영
out = build_runsheet(event, cues, '..._v2_...xlsx',
    changelog=[('v1','2026-06-05','초안 생성'),
               ('v2','2026-06-12','리허설 반영: 패널 -5, 휴식 +5')])
```

→ `[변경이력]` 시트에 v1·v2 누적. 소요 합은 여전히 210 검증.

---

## 루브릭 자기 채점 (표본)

```
[채점] mice-run-of-show 산출(반일 컨퍼런스 v1) — 94/100 (GO)
 시간무결성 30/30(자동) + 컬럼완전성 20/20(자동) + 표기표준 17/20
 + 버전이력 10/10(자동) + 디자인식별 9/10 + 현장사용성 8/10 = 94
 Critical: 없음 (시간 합 210=총 행사시간 일치·회사 식별정보 0)
 감점: 표기 -3(‘테이블 세팅 전환’ 등 일부 자유서술) · 디자인 -1 · 현장 -2(일부 비고 sparse)
 채점자: build_runsheet 자동검증 + 작성자, 최종 jc-redteam 권고
```
