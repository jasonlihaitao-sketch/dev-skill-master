#!/usr/bin/env bash
#
# capture.sh — 本地 ~/.claude/skills/ → 仓库
#
# 把 ~/.claude/skills/dev-* 抓回 dev-skill-master/skills/，用于你在本地
# 直接改了 skill、测好后想把改动送回仓库真相源的场景。
#
# 安全语义：覆盖前对每个文件做 diff，若仓库存在「本地没有的新改动」
# ——即仓库比本地更新、会被无声抹掉——脚本停下并报冲突文件，由你手动处理后再跑。
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HOME/.claude/skills"
DST="$REPO_DIR/skills"

SKILLS=(dev-init dev-flow dev-requirement dev-design dev-implement dev-review)

if [[ ! -d "$SRC" ]]; then
  echo "错误：找不到源目录 $SRC" >&2
  exit 1
fi
mkdir -p "$DST"

conflicts=()
for s in "${SKILLS[@]}"; do
  ssrc="$SRC/$s"
  sdst="$DST/$s"
  [[ -d "$ssrc" ]] || { echo "警告：本地缺失 $ssrc，跳过" >&2; continue; }

  # 冲突检测：仓库存在、且仓库里有「本地没有的文件」或「同名但内容不同(仓库新)」的文件
  if [[ -d "$sdst" ]]; then
    while IFS= read -r -d '' f; do
      rel="${f#"$sdst"/}"
      srcf="$ssrc/$rel"
      if [[ ! -e "$srcf" ]]; then
        conflicts+=("$s/$rel (仓库独有，覆盖将丢失)")
      elif ! diff -q "$f" "$srcf" >/dev/null 2>&1; then
        # 方向是本地→仓库，仓库差异会被抹掉
        conflicts+=("$s/$rel (仓库与本地不同，覆盖将丢失仓库改动)")
      fi
    done < <(find "$sdst" -type f -not -name '.DS_Store' -print0)
  fi
done

if (( ${#conflicts[@]} > 0 )); then
  echo "❌ 检测到冲突，已中止(未做任何改动)。以下文件会被覆盖丢失：" >&2
  printf '  - %s\n' "${conflicts[@]}" >&2
  echo "" >&2
  echo "处理建议：若仓库改动是要保留的，先 git pull / 用 install.sh 同步到本地再改；" >&2
  echo "          若确认丢弃仓库改动，删除对应文件后重跑 capture.sh。" >&2
  exit 1
fi

# 无冲突，执行覆盖(排除 .DS_Store)
for s in "${SKILLS[@]}"; do
  ssrc="$SRC/$s"
  sdst="$DST/$s"
  [[ -d "$ssrc" ]] || continue
  rm -rf "$sdst"
  rsync -a --exclude='.DS_Store' "$ssrc/" "$sdst/"
  echo "✓ ~/.claude/skills/$s → $s"
done

echo ""
echo "完成：已把本地 skills 抓回仓库。记得 git add/commit/push。"
