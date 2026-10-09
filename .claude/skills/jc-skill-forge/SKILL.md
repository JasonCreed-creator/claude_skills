---
name: jc-skill-forge
description: 기획자님의 Claude 스킬 라이브러리(jc-*·mice-*)를 만들고·고치고·점검하고·배포하는 단일 메타 스킬. 신규 스킬 제작, 기존 스킬 개선·버전업, 외부 스킬 생태계 대조 인테이크(업그레이드·대체·통폐합), 정기 라이브러리 점검(Quick Scan / Full Stocktake), 정본 레포 → claude.ai 업로드·Claude Code 로컬 설치 배포 파이프라인, 하우스 규약(명명·description·리멤버 SoT 앵커·공통 룰·Windows 경로)을 담는다. 다음 상황에서 반드시 이 스킬을 사용할 것 — 사용자가 '스킬 만들어줘', '새 스킬', '스킬 제작', '스킬 개선', '스킬 수정', '버전 올려', '스킬 업그레이드', '스킬 인테이크', '스킬 통폐합', '스킬 정리', '스킬 점검', '스킬 라이브러리', '외부 스킬 찾아줘', '쓸만한 스킬', '스킬 업로드', '스킬 배포', '스킬 빌드', '.skill 파일', '스킬 동기화', '스킬셋 개정'을 언급할 때. 기본 제공 스킬을 우리 것으로 바꿔달라고 할 때. 기본 skill-creator 대신 본 스킬을 우선 사용한다(skill-creator는 평가 기계로만). 소스 수정은 `_archive` 백업 후 바로 진행하고, 배포(Code 설치·claude.ai 업로드 안내)·삭제는 승인 후, claude.ai 업로드와 git 커밋·푸시는 사용자 몫이다. 형제 경계 — 산출물 자체 생성은 각 전용 스킬, 완성 스킬의 적대 검증은 jc-redteam, 세션·턴 규약은 jc-session-protocol, 디자인 토큰 값은 jc-design-system.
version: "v2.2.1"
license: Complete terms in LICENSE.txt
---

# jc-skill-forge v2 — 스킬 라이브러리 관리

정본 레포 `C:\.Claude\Code\claude_skills`(GitHub `JasonCreed-creator/claude_skills`)의 `.claude/skills/`를 편집하고, `.skill`로 묶어 claude.ai에 올리며, Claude Code에는 `~/.claude/skills`로 설치한다. (2026-09-21 구 스킬 제작 스킬의 하우스 규약 흡수)

## 0. 가드레일

- 소스 수정(되돌릴 수 있음): 원본을 `_archive/<YYYYMMDD>/<스킬>/`(로컬 롤백 백업 — gitignore, 커밋 안 됨)로 보존한 뒤 합리적 기본값으로 바로 진행하고, 고른 기본값을 한 줄로 밝힌다. 단계마다 묻지 않는다.
- 인테이크·전수 점검·통폐합처럼 범위가 큰 변경만 계획(대상·버전·변경 요지 표) 1회 확인 후 적용.
- 되돌릴 수 없는 작업(로컬 설치 덮어쓰기·폐합 스킬 삭제 안내 실행·배포)만 승인 후. 폐합 스킬도 삭제가 아니라 git 보관소로 아카이브(ARCHIVE 정의는 §3 — `_archive/`가 아니다).
- **소스 반영 ≠ 배포.** 보고는 스킬마다 ①소스 반영 ②Code 로컬 설치 ③claude.ai 업로드를 따로 적는다. ③은 사용자가 Settings > Capabilities에서 직접 한다 — 업로드했다고 가정하지 않는다.
- 패키지는 ZIP `.skill`(내부 `<name>/SKILL.md`)만. tar.gz 등 다른 형식 금지.
- git 커밋·푸시는 사용자 몫. 스킬은 커밋 메시지 초안(`<스킬명>: <요약>`)만 제시한다.
- 외부 스킬은 복사하지 않고 패턴만 흡수해 jc-*/mice-* 네이밍으로 재구성. 외부 스크립트는 검토 전 실행·포함 금지.
- `~/.claude/skills/synced/`는 편집하지 않는다(10분마다 덮어씀). `mice-estimate`는 사용자가 직접 관리 — 건드리지 않는다(2026-09-21).
- 호칭 "기획자님". 응답 구조: 핵심 결론 → 분석 → 실행 → 리스크.

## 1. 모드 판별

| 모드 | 트리거 | 절차 |
|------|--------|------|
| **A 인테이크** | 외부 스킬 대조·업그레이드·통폐합 | §2 스캔 → §3 판정 → 계획 1회 확인 → 적용 → 검증 |
| **B 신규 제작** | 없던 기능을 새로 | 실패 시나리오(RED) → 최소 SKILL.md(GREEN) → 반례 표(REFACTOR) → 하우스 규약 → 검증 |
| **C 개선·버전업** | 기존 스킬 수정 | `_archive` → 변경 → `version` 범프 → 변경 이력 → 린트 |
| **D 점검** | 정기·구조 변경 전 | Quick Scan(변경분: 트리거·version·이력) / Full Stocktake(전체: 중복·최신성·활용도·범위적합 4축 + 세션 로그 실사용 집계) |
| **E 배포** | 업로드·설치·동기화 | `references/deploy-pipeline.md` — 린트 → 빌드(.skill ZIP) → 업로드 안내(사용자) → 로컬 설치(승인) |

## 2. 인테이크 스캔 (모드 A)

- 인벤토리: `.claude/skills/**/SKILL.md`(`_archive` 제외) name·description·version 표 + 최근 세션 로그에서 실제 Skill 호출 집계(활용도).
- 외부 소스 화이트리스트: anthropics/skills · obra/superpowers · maigentic/stratarts · Weizhena/Deep-Research-skills · ComposioHQ/awesome-claude-skills · VoltAgent/awesome-agent-skills · sales-skills/sales · claudeskills.info · lobehub.com/skills. 후보별 name·차별점·라이선스·최종 갱신·코드 실행 여부·URL.
- 적합도: 리멤버 MICE비즈팀 팀장 업무(견적·제안서·운영계획·현장·결과보고·Slack 운영·팀 보드) + Code·Cowork·Claude Design 서피스. 저작 품질 보조 기준: 실패 시나리오 기반(RED→GREEN), 반례 차단(REFACTOR).

## 3. 결정 매트릭스

UPGRADE(패턴 흡수) · REPLACE(전면 교체, 드묾) · MERGE(통폐합) · NEW(신규) · ARCHIVE(폐합) · SKIP. 각 결정에 근거·영향 범위·심각도·작업량. NEW 전 중복 탐색: 로컬 → 화이트리스트 → GitHub → 웹.

**ARCHIVE 실행** = `git mv .claude/skills/<n> archive/skills/<n>` + `scripts/lint_skills.py`의 LIVE/ARCHIVED 갱신 + `archive/README.md` 폐합 → 후속 매핑 행 추가 + `jc-design-system/references/chaining-protocol.md` §3에서 제거(봉투를 내던 스킬이면 §3-1 별칭·§7 ALIASES에 후속 스킬로 등록). `_archive/`는 로컬 롤백 백업(gitignore)일 뿐 폐합 보관소가 아니다. 커밋은 사용자.

## 4. 하우스 규약 (요지 — 상세 `references/house-conventions.md`)

1. 명명·구조: 디렉터리 = `name` = `jc-<도메인>`/`mice-<도메인>`. SKILL.md(<300줄 권장, <500 상한) + references/ + scripts/ + assets/.
2. description: 한국어·푸시형, 무엇을 + 언제(키워드) + 형제 경계. **1,024자 이하**. 폐지 게이트 문구(브리프·범위·턴 분할)·폐합 스킬 이름 금지.
2-1. 진행 규약 정본 = `jc-session-protocol` SKILL.md §3(고밀도 산출물만 기획안 1회 확인). forge 고유분: 소스 수정 = 백업 후 즉시, 배포·삭제 = 승인. 호칭은 사용자 '기획자님'(§0), 산출물 속 직함 '팀장'(house-conventions §6.2). 모델명은 jc-session-protocol §5.
3. SoT 앵커: 색·서체·간격은 `jc-design-system` v2(리멤버) 런타임 로드. 값 미러 금지.
4. 명의: 리멤버 MICE비즈팀 기본, 발주처·담당자 주입(RULE-NO-COMPANY v2).
5. 생태계: 검증 `jc-redteam` · 세션 `jc-session-protocol` · 봉투 `ChainPayload/v1`. 재발명 금지.
6. 경로: `/mnt/skills` 금지. SoT 탐색은 형제 → `~/.claude/skills` → synced. 스크립트는 `python`(3.14, Windows)에서 실행 검증.
7. 스크립트는 자가 테스트(`--self-test` 또는 `test_*.py`)를 갖는다.

## 5. 마감 절차

1. `python scripts/lint_skills.py <스킬폴더>` ERROR 0(프론트매터·폐합·없는 스킬 참조·"N턴"·구 모델 ID·"리더"·구 시그니처 HEX·깨진 경로·컴파일). 스크립트 자가 테스트 통과.
2. `version` 범프(SemVer) + SKILL.md 변경 이력 1항.
2-1. 신규·폐합 시 같은 커밋에서 `lint_skills.py` LIVE/ARCHIVED + `jc-design-system/references/chaining-protocol.md` §3 enum(봉투 비대상 줄 포함)·§3-1 별칭·§7 ALIASES를 갱신한다. 린트가 §3 분류 누락·잔존을 WARN으로 잡는다.
3. README 카탈로그·`docs/CHANGELOG-<날짜>.md`·`PROGRESS.md` 갱신, 모드 A 판정은 `docs/skill-intake-log.md`(단일 트래커)에 누적.
4. `jc-redteam` '스킬 인테이크 감수'(Deep — 트리거 정확도·형제 중복·금지 문구·외부 스크립트 보안·lint 대조, `jc-redteam/references/chaining-guide.md` §jc-skill-forge).
5. 배포(모드 E): `python scripts/build_skills.py` → `dist/skills/*.skill`(ZIP) → claude.ai 업로드 + 구스킬 삭제는 사용자 → `python scripts/install_local.py`(승인 후). 보고는 ①②③ 채널별.
6. 커밋 메시지 초안 제시. 커밋·푸시는 사용자.

## 6. 파일 구조

```
jc-skill-forge/
├── SKILL.md
├── references/
│   ├── house-conventions.md    # 불변식 상세 · 프론트매터 템플릿 · 자가점검
│   ├── deploy-pipeline.md      # 정본 레포 → .skill → claude.ai → ~/.claude/skills (동기화 규칙 포함)
│   └── upstream-machinery.md   # 상위 skill-creator 평가 기계 포인터(탐색 순서: 개인 → synced → 원 레포)
└── scripts/
    ├── lint_skills.py          # 정합 검사 (경로 인자 · 체이닝 enum 분류 대조 · --self-test)
    ├── build_skills.py         # .skill(ZIP) 패키징, zip 없는 Windows 대응 (--self-test)
    └── install_local.py        # ~/.claude/skills 정션/복사 설치·해제 (--self-test)
```

## 변경 이력

- v2.2.1 (2026-10-09): deploy-pipeline §1 업로드 상태 팩트 현행화(폐합 19종 삭제·라이브 19종 재업로드·doc-coauthoring OFF → 30종) + 삭제·끄기 확장프로그램 대행·수동 업로드 경로 명시. 스크립트·규약 무변경.
- v2.2.0 (2026-10-09): ARCHIVE를 레포 실제(`archive/skills/` git 보관소 + LIVE/ARCHIVED + archive README + 체이닝 별칭)로 정의, `_archive/`는 로컬 롤백 백업으로만. 진행 규약·모델은 jc-session-protocol 정본 포인터, 호칭 구분 명시, description에 skill-creator 대비 우선 1문. lint에 description 인용 트리거 중복 WARN(스킬 간 같은 트리거 = 재중복 신호) 추가.
  마감에 체이닝 enum 동시 갱신 항목, 린트에 'LIVE ⊆ chaining-protocol §3' WARN·`CURRENT_MODELS` 상수, upstream 탐색 순서(synced 확인), deploy §6 구 `/skillupgrade` 잔존 삭제 안내.
- v2.1.0 (2026-10-05): 린트 강화(경로 인자·`--self-test`, 폐합·없는 스킬 참조·"N턴"·구 모델 ID·"리더"·구 시그니처 HEX·깨진 상대경로), build·install 자가 테스트 추가.
  배포 문서를 현재 실태로 — 소스 반영≠배포(3채널 보고), claude.ai 업로드는 사용자 몫, ZIP(.skill)만·tar.gz 금지. 소스 수정은 백업 후 진행·배포만 승인, "리더"→"팀장".

### v2.0.0 (2026-09-21)
- `jc-skill-creator` v1.0.1 흡수(하우스 규약·저작 검증 루프·상위 기계 포인터). 모드 5종으로 재편(인테이크·제작·개선·점검·배포).
- 하우스 규약 v2: 리멤버 홈베이스, description 1,024자 상한, 브리프 게이트 문구 금지, `/mnt` 금지, Windows `python` 검증.
- 스크립트 3종 신설(lint·build·install). 배포 파이프라인 문서화(synced 10분 갱신·개인 스킬 우선·Cowork는 claude.ai만).
- 2026-09-21 전수조사 결과 반영: 커스텀 30 → 14종 재편의 실행 도구.

### v1.0.3 (2026-07-12) 이전
CP1·CP3 인테이크 패턴 흡수(저작 품질 기준·중복 탐색 순서·점검 2모드). 이력은 git.
