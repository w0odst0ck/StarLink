#!/usr/bin/env bash
# 一键发布：提交 + 推送 → GitHub Actions 自动生成 site-data 并部署 Pages。
#
# 用法：
#   ./scripts/publish.sh                 # 提交 + 推送（提交信息自动生成）
#   ./scripts/publish.sh "提交信息"       # 指定提交信息
#   ./scripts/publish.sh --dry-run       # 只看变更，不提交不推送
#
# 前置：vault/stars/ 已入库；site-data.json 由 CI 生成，本地无需跑 pages。
set -euo pipefail

cd "$(dirname "$0")/.."

DRY=""
MSG=""
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY=1
  shift
fi
if [[ -n "${1:-}" ]]; then
  MSG="$1"
fi

if [[ -n "$DRY" ]]; then
  echo "▶ [dry-run] 变更预览（未提交）:"
  git status --short
  exit 0
fi

git add -A
if [[ -z "$MSG" ]]; then
  MSG="chore: update vault"
fi
git commit -m "$MSG" || { echo "✗ 无变更可提交"; exit 0; }
git push

echo "✓ 已推送 → GitHub Actions 自动生成 + 部署（约 1-2 分钟生效）"
