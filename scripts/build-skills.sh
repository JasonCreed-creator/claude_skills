#!/bin/bash
# build-skills.sh — 모든 스킬을 claude.ai 업로드용 .skill(zip) 패키지로 빌드.
# 출력: dist/skills/<skill>.skill  (dist/ 는 .gitignore 처리 — 빌드 산출물)
# 사용: bash scripts/build-skills.sh
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS="$ROOT/.claude/skills"
OUT="$ROOT/dist/skills"

rm -rf "$OUT"
mkdir -p "$OUT"

cd "$SKILLS"
count=0
for d in */; do
  s="${d%/}"
  [ -f "$s/SKILL.md" ] || continue   # SKILL.md 없는 항목(_README.txt 등) 제외
  zip -q -r "$OUT/$s.skill" "$s" -x '*.DS_Store' '*/__pycache__/*' '*.pyc'
  echo "  ✅ $s.skill"
  count=$((count+1))
done

echo "완료 → $OUT  ($count skills)"
echo "각 .skill 을 claude.ai → Settings → Capabilities(Skills) 에 업로드하세요."
