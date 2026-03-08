# 代码推送指南

## 当前状态

✅ **代码已完成修复和提交**
- 工作区干净，无未提交的更改
- 已有 3 个待推送的提交：
  1. `docs: 添加自动推送脚本和指南`
  2. `docs: 添加修复功能测试脚本和详细说明文档`
  3. `fix: 修复市场数据获取和企业微信通知的异常处理`

## 如何推送到 GitHub

由于当前环境无法进行交互式输入，您需要手动推送代码。请选择以下任一方式：

### 方式一：使用 HTTPS + Personal Access Token（推荐）

1. **创建 GitHub Personal Access Token**
   - 访问 https://github.com/settings/tokens
   - 点击 "Generate new token (classic)"
   - 选择权限：
     - `repo` (完整仓库访问权限)
   - 点击生成并复制 Token（⚠️ 只显示一次，请立即复制）

2. **推送代码**
   ```bash
   # 方法 1：使用 git credential helper
   cd /workspace/projects
   git config credential.helper store
   git push -u origin main
   # 输入用户名和 Token（Token 作为密码）

   # 方法 2：在 URL 中包含 Token（一次性）
   git push https://<YOUR_TOKEN>@github.com/hanchangjun/rebar-steel-futures-trading-system.git main
   ```

### 方式二：使用 SSH Key

1. **生成 SSH Key**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. **添加到 GitHub**
   - 复制公钥：`cat ~/.ssh/id_ed25519.pub`
   - 访问 https://github.com/settings/keys
   - 点击 "New SSH key"，粘贴公钥

3. **更改远程仓库 URL**
   ```bash
   git remote set-url origin git@github.com:hanchangjun/rebar-steel-futures-trading-system.git
   git push -u origin main
   ```

### 方式三：使用 GitHub CLI（如果已安装）

```bash
# 登录
gh auth login

# 推送
gh repo sync hanchangjun/rebar-steel-futures-trading-system
# 或
git push -u origin main
```

## 自动推送脚本

项目中提供了自动推送脚本（需要交互式输入）：

### Python 版本
```bash
python auto_push.py
```

### Shell 版本
```bash
bash auto_push.sh
```

## 验证推送成功

推送后，可以访问以下链接确认：
- 仓库主页：https://github.com/hanchangjun/rebar-steel-futures-trading-system
- 查看提交历史：https://github.com/hanchangjun/rebar-steel-futures-trading-system/commits/main

## 常见问题

### Q1: 推送失败提示 "Authentication failed"
**A**: 检查 Token 是否正确，确保 Token 有 `repo` 权限，且未过期。

### Q2: 提示 "Updates were rejected"
**A**: 远程仓库可能有新的提交，先拉取远程更改：
   ```bash
   git pull --rebase origin main
   git push origin main
   ```

### Q3: 如何查看待推送的提交？
**A**: 运行以下命令：
   ```bash
   git log origin/main..main
   ```

### Q4: 如何撤销本地提交？
**A**: 运行以下命令（谨慎使用）：
   ```bash
   # 撤销最近一次提交（保留更改）
   git reset --soft HEAD~1

   # 撤销最近一次提交（丢弃更改）
   git reset --hard HEAD~1
   ```

## 项目修复摘要

本次修复解决了以下问题：

1. **市场数据获取失败**
   - 添加 `safe_json_parse` 函数安全解析 JSON
   - 统一工具返回格式（包含 `status` 字段）
   - 增强异常处理机制

2. **企业微信通知配置异常**
   - 改进 `get_webhook_key` 函数，支持多种配置方式
   - 未配置时返回友好提示而非抛出异常
   - 修复 FaaS 环境的 logger 初始化问题

3. **定时任务模块错误**
   - 修复 `__name__` 变量未定义问题
   - 将 logger 初始化改为明确字符串

4. **新增功能**
   - 提供 Python 和 Shell 版本的自动推送脚本
   - 提供详细的修复功能测试脚本

## 联系支持

如遇到其他问题，请参考：
- GitHub 官方文档：https://docs.github.com
- Git 官方文档：https://git-scm.com/doc
