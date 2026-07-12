# 배포 지시서 — jc-orchestrator v1.1.0 (2026-07-10 챗 빌드)

> 본 지시서는 스킬 레포에 수록 후 Code 세션에서 집행한다(챗 다운로드에만 두지 말 것).
> 챗 샌드박스 빌드는 라이브러리에 영구 반영되지 않는다 — 배포는 사용자 환경에서만 유효.

## 0. 전제

- 산출물: `jc-orchestrator.skill` (ZIP) — SKILL.md v1.1.0 + LICENSE + references 5종 + assets(템플릿 1 + 프리셋 2종: html-pt 10파일 / code-conductor 8파일)
- 성격: 신규 스킬(자사 23 → 24종). 지침 §8 에이전트 팩토리의 실행체(상세 SoT)
- v1.1.0 증분: code-conductor 프리셋(비용 라우팅 + 강제 게이트 + 스위치) — v1.0.0은 배포 전이므로 본 버전으로 최초 배포
- 진행 중인 Phase 5·CP2와 독립 트랙 — 단, ⑤·⑥은 Phase 5 부트스트랩과 순서 조정 가능

## 1. 집행 순서 (스킬 배포)

1. **소스 반영** — 압축 해제 → Drive 작업본 `Skills/library/jc-orchestrator/` 배치 → git 정본 `~/repos` 복사
2. **커밋·PR** — `jc-orchestrator: v1.1.0 신규 — 에이전트 팩토리 실행체화 + 프리셋 2종(html-pt·code-conductor)` / 작업 브랜치 → 드래프트 PR
3. **README 카탈로그 갱신** — 신규 스킬 1행 추가
4. **jc-prompt-builder 정합** — routing-map.md §2 '에이전트 팩토리' 행: "전용 스킬 없음(직접 수행)" → "매핑=jc-orchestrator" / SKILL.md §6 경계 표 동일 갱신. ※계류 중인 v1.1.0 개정에 흡수 권고(별도 터치 최소화). description-registry 재생성(`build_routing_map.py`) 시 본 스킬 포함 확인
5. **전역 설치** — `~/.claude/skills` 배치(Phase 5 전역 부트스트랩과 연동)
6. **claude.ai 업로드** — `.skill` ZIP 수동 업로드
7. **3채널 검증** — git 소스 / 전역 설치본 / claude.ai 업로드본 각각 존재·버전 확인('소스 반영 ≠ 배포')

## 2. code-conductor 환경 설치 (스킬 배포와 별개 — 선택 시)

- 절차·검증 정본: `assets/presets/code-conductor/INSTALL.md`
- **§0 사전 실측 필수**: claude 버전(prompt_id 필드) / 모델 문자열 유효성 — 통과 전 게이트 활성 금지
- **§4 실측 검증 필수**: (a)메인 차단 + (b)서브에이전트 통과가 **함께** 확인되어야 완성. (b) 실패 시 즉시 `fable off`
- 2머신(icejc / Jason) 각각 설치, 결과는 PROGRESS.md에 머신별 1줄 로그
- ③리매핑(env.sh)은 선택 — 비용 우선이면 생략

## 3. 후속 확인 항목

- **html-pt 원본 대조**: Code Phase 0 P0의 'html-pt-orchestrator 소재' 확인 시 → 프리셋 재생성본(v2)과 원본(v1) diff 대조, 유의미한 프롬프트 뉘앙스는 병합 후 patch 범프
- **지침 §8 개정 반영 확인**: 사용자 설정 UI 반영 여부(미반영 시 이중 SoT 드리프트)
- **RED 재현 테스트**(선택): 복합 프로젝트 지시를 스킬 없이/있이 각 1회 던져 팩토리 발동·구성안 형식 준수 여부 실측

## 4. 체크리스트

- [ ] 1. 소스 반영 (Drive + ~/repos)
- [ ] 2. 커밋 + 드래프트 PR
- [ ] 3. README 카탈로그
- [ ] 4. jc-prompt-builder routing-map·§6 (v1.1.0 흡수 여부 판정 포함)
- [ ] 5. 전역 설치
- [ ] 6. claude.ai 업로드
- [ ] 7. 3채널 검증
- [ ] (선택) code-conductor 설치 — 머신 A / 머신 B + 실측 (a)(b) + PROGRESS 로그
- [ ] 후속: html-pt v1 대조 / 지침 §8 반영 확인
