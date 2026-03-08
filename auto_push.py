#!/usr/bin/env python3
"""
自动推送脚本
用于将代码推送到 GitHub
"""
import os
import sys
import subprocess

def run_command(cmd):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout, result.returncode
    except subprocess.CalledProcessError as e:
        return e.stderr, e.returncode

def main():
    """主函数"""
    print("="*60)
    print("  自动推送到 GitHub")
    print("="*60)
    print()

    # 检查当前分支
    stdout, _ = run_command("git branch --show-current")
    current_branch = stdout.strip()
    print(f"当前分支: {current_branch}")

    # 检查是否有未提交的更改
    stdout, _ = run_command("git status --porcelain")
    if stdout.strip():
        print("⚠️  警告: 工作区有未提交的更改")
        print("请先提交或暂存这些更改")
        print(stdout)
        sys.exit(1)

    # 检查是否有待推送的提交
    stdout, _ = run_command("git rev-list --count @{u}..HEAD 2>/dev/null")
    ahead_count = stdout.strip() or "0"
    if ahead_count == "0":
        print("✅ 没有待推送的提交")
        print("当前分支与远程分支同步")
        sys.exit(0)

    print()
    print(f"待推送的提交数: {ahead_count}")
    print()
    print("最近的提交:")
    stdout, _ = run_command("git log --oneline -5")
    print(stdout)

    print()
    print("="*60)
    print("  开始推送")
    print("="*60)
    print()

    # 推送代码
    print("正在推送...")
    print("提示: 请输入以下凭据：")
    print("  Username: hanchangjun")
    print("  Password: <您的 GitHub Personal Access Token>")
    print()

    try:
        subprocess.run("git push -u origin main", shell=True, check=True)
        print()
        print("="*60)
        print("  ✅ 推送成功！")
        print("="*60)
        print()
        print("您的代码已成功推送到 GitHub")
        print("仓库地址: https://github.com/hanchangjun/rebar-steel-futures-trading-system")
    except subprocess.CalledProcessError as e:
        print()
        print("="*60)
        print("  ❌ 推送失败")
        print("="*60)
        print()
        print("错误信息:")
        print(e.stderr)
        print()
        print("请检查：")
        print("1. GitHub Token 是否正确")
        print("2. 网络连接是否正常")
        print("3. 仓库地址是否正确")
        sys.exit(1)

if __name__ == "__main__":
    main()
