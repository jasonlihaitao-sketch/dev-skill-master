#!/usr/bin/env bash
#
# install.sh — 仓库 → 本地 ~/.claude/skills/
#
# 把 dev-skill-master/skills/dev-* 覆盖到 ~/.claude/skills/dev-*，
# 让 Claude 读取到仓库里的最新版用于测试。
#
# 安全语义：覆盖前对每个文件做 diff，若目标(本地)存在「源(仓库)没有的新改动」
# ——即目标比源更新、会被无声抹掉——脚本停下并报冲突文件，由你手动处理后再跑。
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$REPO_DIR/skills"
DST="$HOME/.claude/skills"

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
  [[ -d "$ssrc" ]] || { echo "警告：源缺失 $ssrc，跳过" >&2; continue; }

  # 冲突检测：目标存在、且目标里有「源没有的文件」或「同名但内容不同(目标新)」的文件
  if [[ -d "$sdst" ]]; then
    while IFS= read -r -d '' f; do
      rel="${f#"$sdst"/}"
      srcf="$ssrc/$rel"
      if [[ ! -e "$srcf" ]]; then
        # 目标独有、源没有 → 覆盖会丢
        conflicts+=("$s/$rel (本地独有，覆盖将丢失)")
      elif ! diff -q "$f" "$srcf" >/dev/null 2>&1; then
        # 同名内容不同，方向是仓库→本地，本地差异会被抹掉
        conflicts+=("$s/$rel (本地与仓库不同，覆盖将丢失本地改动)")
      fi
    done < <(find "$sdst" -type f -not -name '.DS_Store' -print0)
  fi
done

if (( ${#conflicts[@]} > 0 )); then
  echo "❌ 检测到冲突，已中止(未做任何改动)。以下文件会被覆盖丢失：" >&2
  printf '  - %s\n' "${conflicts[@]}" >&2
  echo "" >&2
  echo "处理建议：若本地改动是你要保留的，改用 capture.sh 把本地抓回仓库；" >&2
  echo "          若确认丢弃本地改动，删除对应文件后重跑 install.sh。" >&2
  exit 1
fi

# 无冲突，执行覆盖(排除 .DS_Store)
for s in "${SKILLS[@]}"; do
  ssrc="$SRC/$s"
  sdst="$DST/$s"
  [[ -d "$ssrc" ]] || continue
  rm -rf "$sdst"
  rsync -a --exclude='.DS_Store' "$ssrc/" "$sdst/"
  echo "✓ $s → ~/.claude/skills/$s"
done

echo ""
echo "完成：已把仓库 skills 同步到 ~/.claude/skills/。"
