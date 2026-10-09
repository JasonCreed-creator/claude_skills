JC MICE 스킬 라이브러리 — claude.ai 웹 설치본에서 추출한 현재 소스 (9종)

[구조]  .claude/skills/<스킬명>/SKILL.md (+ references/ scripts/ assets/)

[설치]
1) 이 zip을 jc-claude-context 레포 "루트"에서 압축 해제
   → <repo>/.claude/skills/ 아래 9개 스킬 폴더가 생깁니다
2) git add . && git commit -m "chore: import 9 MICE skills as source of truth"
   → 이제 git으로 버전 관리됩니다
3) 그 레포 루트에서 Claude Code 실행 (cwd=레포 루트)
   → .claude/skills/ 자동 인식
4) R1_SoT_consolidation 패키지의 §7 Project Instructions 투입 → 작업
5) 작업 후 변경된 7개 스킬을 각각 zip → claude.ai 웹 Settings>Features 에 재업로드

* _README.txt 는 설치 후 삭제해도 됩니다.
