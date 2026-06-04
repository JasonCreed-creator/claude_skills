---
name: jc-skill-forge
description: 기획자님(이진철)의 개인 스킬 라이브러리(mice-*, jc-*)를 외부 Claude 스킬 생태계와 대조해 업그레이드·대체·통폐합·신규보강하는 라이브러리 관리 스킬. 다음 상황에서 반드시 이 스킬을 사용할 것 — 사용자가 '스킬 업그레이드', '스킬 인테이크', '스킬 통폐합', '스킬 스캔', '외부 스킬 찾아줘', '쓸만한 스킬 찾아줘', '내 스킬 업데이트', '스킬 라이브러리 점검', '스킬 정리', 'skill intake', 'skill upgrade'를 언급할 때. 외부 컬렉션(superpowers, stratarts, ComposioHQ, VoltAgent, Deep-Research 등)을 뒤져 기존 자산을 개선·교체·병합할지 판단해달라고 요청할 때. 기본 동작은 읽기 전용 스캔·제안이며, 파일 변경은 사용자가 명시적으로 승인(GO)한 항목에만 적용한다. 단, 다음은 이 스킬 영역이 아니다 — 백지에서 새 스킬을 직접 제작·평가하는 일반 작업은 skill-creator 영역. 특정 산출물 생성은 각 전용 스킬(제안서=mice-proposal, 견적=mice-estimate, 대본=pt-script, 대시보드=mice-dashboard, 회의록=mice-meeting-minutes, RFP분석=mice-rfp-analyzer, 스폰서데크=mice-sponsor-deck) 영역. 완성물의 적대적 검증만 단독으로 필요하면 jc-redteam 영역. 이 스킬은 '외부 생태계 대조를 통한 내 라이브러리 진화'에만 트리거한다.
version: "v1.0.0"
license: Complete terms in LICENSE.txt
---

# jc-skill-forge

기획자님의 스킬 라이브러리를 외부 생태계와 대조해 진화시키는 관리 스킬.

## 0. 가드레일 (발동 즉시 따른다, 위반 금지)
- 기본 모드 = 읽기 전용. 1~4단계(스캔·판정·제안)에서는 어떤 파일도 변경하지 않는다.
- 5단계 승인 게이트에서 기획자님이 GO한 항목에만 6~7단계(적용)를 수행한다.
- GitHub는 동기화 저장소다. 이 스킬은 git 명령(브랜치·커밋·머지·push)을 절대 수행하지 않는다. 스킬 파일은 로컬에서 직접 편집하고, GitHub 동기화는 기획자님이 평소 방식대로 처리한다.
- 변경 전 원본 SKILL.md를 `_archive/<YYYYMMDD>/`로 복사해 보존(롤백용).
- 외부 스킬 그대로 복사·설치 금지 → SKILL.md 패턴만 흡수해 기획자님 네이밍(jc-*, mice-*)으로 재구성.
- 외부 스크립트(.py/.sh 등)는 내용 검토 전 실행·포함 금지.
- 고밀도 스킬 변경은 3턴 분할(기획→빌드→검수).
- 호칭 "기획자님", 응답 구조 핵심 결론→분석→실행 전략→리스크/추가.

## 범위
사용자가 지정한 도메인·소스(예: "전략", "stratarts")로 한정. 미지정 시 전체 라이브러리 대상.

## 1. 인벤토리 — 현재 자산
- skills 디렉토리를 Glob(`**/SKILL.md`)으로 스캔, 각 스킬의 name·description·핵심 역할을 표로 정리.
- CLAUDE.md / PROGRESS.md를 읽어 현재 로드맵·확정사항·금지사항을 컨텍스트로 반영.

## 2. 외부 소스 스캔 — 화이트리스트만
WebFetch로 최신 상태 확인(범위 한정):
- obra/superpowers · maigentic/stratarts · Weizhena/Deep-Research-skills
- ComposioHQ/awesome-claude-skills · VoltAgent/awesome-agent-skills
- sales-skills/sales · anthropics/skills
- 디렉토리 보강: claudeskills.info, lobehub.com/skills
각 후보의 name·description·핵심 차별점·라이선스·최종 업데이트·코드실행 여부·출처 URL 기록.

## 3. 적합도 필터
기획자님 프로필(MICE 전략·제안·리서치·신사업 BM / Track A 현직·Track B 독립 / Chat·Cowork·Code 3환경)에 부합하는 후보만 남기고, 나머지는 SKIP 사유와 함께 제외.

## 4. 결정 매트릭스
살아남은 후보를 기존 자산과 매핑:
- UPGRADE: 기존 스킬에 외부의 우월한 패턴 흡수
- REPLACE: 기존을 외부 기반으로 전면 교체(드묾)
- MERGE: 중복 스킬 통폐합
- NEW: 부재 구간 신규 보강
- SKIP: 불채택
각 결정에 근거·영향범위·심각도(Critical/Major/Minor)·예상 작업량 명시.

## 5. 승인 게이트 — 필수 정지점
1~4를 "스킬 인테이크 제안 리포트"로 출력하고 정지한다.
기획자님이 적용 대상을 확정(예: "UPGRADE 3건, NEW 2건만 GO")하기 전엔 다음 단계로 진행하지 않는다.

## 6. 적용 — 승인분만 (로컬 파일 직접 편집)
- 변경 전 원본 스킬 폴더를 `_archive/<날짜>/`로 복사(`cp -r`).
- 승인된 항목만 Edit/Write로 로컬 스킬 파일에 직접 반영. 외부는 패턴만 흡수해 jc-*/mice- 네이밍 + jc-design-system 토큰 + 운영 원칙(호칭·응답구조·3턴분할)으로 재구성.
- git 작업은 하지 않는다.

## 7. 검증·로그
- jc-redteam 관점으로 변경된 SKILL.md를 인테이크 감수(트리거 정확도·중복·보안·오탈자).
- PROGRESS.md에 인테이크 로그(날짜·소스·결정·근거) 추가, 필요시 CLAUDE.md 스킬 목록 갱신.
- 마지막에 변경 요약과 `_archive` 백업 위치를 보고한다. GitHub 동기화는 기획자님이 평소 방식대로 — 스킬은 push하지 않는다.

## 환경 분기
- Claude Code: 전체 1~7단계 수행(로컬 파일 직접 편집·서브에이전트 병렬 가능).
- Claude Cowork: 1~5단계 병렬 스캔 가능, 적용은 동일 게이트.
- Claude Chat: 1~5단계(스캔·제안)까지만. 로컬 파일이 없으므로 실제 적용은 Code에서 이어서.
