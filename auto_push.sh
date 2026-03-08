#!/bin/bash
#
# 自动推送脚本
# 用于将代码推送到 GitHub
#

echo "========================================="
echo "  自动推送到 GitHub"
echo "========================================="
echo ""

# 检查当前分支
CURRENT_BRANCH=$(git branch --show-current)
echo "当前分支: $CURRENT_BRANCH"

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  警告: 工作区有未提交的更改"
    echo "请先提交或暂存这些更改"
    git status --short
    exit 1
fi

# 检查是否有待推送的提交
AHEAD_COUNT=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo "0")
if [ "$AHEAD_COUNT" -eq 0 ]; then
    echo "✅ 没有待推送的提交"
    echo "当前分支与远程分支同步"
    exit 0
fi

echo ""
echo "待推送的提交数: $AHEAD_COUNT"
echo ""
echo "最近的提交:"
git log --oneline -5

echo ""
echo "========================================="
echo "  开始推送"
echo "========================================="
echo ""

# 推送代码
git push -u origin main

# 检查推送结果
if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "  ✅ 推送成功！"
    echo "========================================="
    echo ""
    echo "您的代码已成功推送到 GitHub"
    echo "仓库地址: https://github.com/hanchangjun/rebar-steel-futures-trading-system"
else
    echo ""
    echo "========================================="
    echo "  ❌ 推送失败"
    echo "========================================="
    echo ""
    echo "请检查："
    echo "1. GitHub Token 是否正确"
    echo "2. 网络连接是否正常"
    echo "3. 仓库地址是否正确"
    exit 1
fi
