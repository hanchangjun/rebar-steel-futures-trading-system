# 代码提交到 GitHub 操作指南

## 📋 前提条件

在开始之前，请确保您已经：
- ✅ 拥有 GitHub 账号
- ✅ 本地已安装 Git
- ✅ 项目代码已完成开发

---

## 🚀 操作步骤

### 步骤 1: 在 GitHub 上创建仓库

1. 登录 [GitHub](https://github.com/)
2. 点击右上角的 **"+"** 号
3. 选择 **"New repository"**
4. 填写仓库信息：
   - **Repository name**: `rebar-steel-futures-trading-system` (或您喜欢的名称)
   - **Description**: 螺纹钢期货买卖点交易系统
   - **Public/Private**: 选择 **Public** 或 **Private**
   - ⚠️ **不要**勾选 "Initialize this repository with a README"
   - ⚠️ **不要**添加 .gitignore 或 license
5. 点击 **"Create repository"**

创建后，GitHub 会显示仓库地址，例如：
```
https://github.com/your-username/rebar-steel-futures-trading-system.git
```

---

### 步骤 2: 在本地配置 Git（如果还未配置）

检查 Git 用户配置：

```bash
git config --global user.name
git config --global user.email
```

如果未配置，请执行：

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

### 步骤 3: 添加远程仓库

进入项目目录：

```bash
cd /workspace/projects
```

添加远程仓库（将 `YOUR_USERNAME` 替换为您的 GitHub 用户名）：

```bash
git remote add origin https://github.com/YOUR_USERNAME/rebar-steel-futures-trading-system.git
```

验证远程仓库配置：

```bash
git remote -v
```

---

### 步骤 4: 推送代码到 GitHub

推送代码到远程仓库：

```bash
git push -u origin main
```

**参数说明**：
- `-u`: 设置上游分支，以后推送可以简化为 `git push`
- `origin`: 远程仓库名称
- `main`: 分支名称

---

### 步骤 5: 验证推送

1. 刷新 GitHub 仓库页面
2. 确认所有文件都已上传
3. 检查提交历史是否正确

---

## 🔧 常见问题

### Q1: 推送时提示 "fatal: remote origin already exists"

**A**: 远程仓库已存在，需要先删除或修改

**解决方案 1**: 删除现有远程仓库
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

**解决方案 2**: 修改远程仓库地址
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

---

### Q2: 推送时提示 "Authentication failed"

**A**: 需要配置 GitHub 认证

**解决方案**:

**方式 1: 使用 Personal Access Token（推荐）**
1. 访问 GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 点击 **"Generate new token"**
3. 勾选 `repo` 权限
4. 生成 token 并复制
5. 推送时使用 token 作为密码

**方式 2: 使用 SSH 密钥**
```bash
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your.email@example.com"

# 复制公钥
cat ~/.ssh/id_ed25519.pub

# 添加到 GitHub
# GitHub → Settings → SSH and GPG keys → New SSH key

# 修改远程仓库为 SSH
git remote set-url origin git@github.com:YOUR_USERNAME/REPO_NAME.git
```

---

### Q3: 提示 "error: failed to push some refs"

**A**: 远程仓库有本地没有的提交

**解决方案**:
```bash
# 拉取远程更新
git pull origin main --allow-unrelated-histories

# 解决冲突（如果有）
# 手动编辑冲突文件后：

git add .
git commit -m "Merge remote changes"
git push origin main
```

---

### Q4: 想要推送到不同的分支

**A**: 指定分支名称

```bash
# 创建并切换到新分支
git checkout -b feature/new-feature

# 推送到新分支
git push -u origin feature/new-feature
```

---

## 📝 完整操作示例

```bash
# 1. 进入项目目录
cd /workspace/projects

# 2. 检查当前状态
git status

# 3. 添加远程仓库（替换为您的地址）
git remote add origin https://github.com/YOUR_USERNAME/rebar-steel-futures-trading-system.git

# 4. 验证远程仓库
git remote -v

# 5. 推送代码
git push -u origin main

# 6. 如果需要输入凭据，输入：
#    Username: YOUR_GITHUB_USERNAME
#    Password: YOUR_GITHUB_TOKEN (不是登录密码)
```

---

## 🔄 后续操作

### 提交新更改

```bash
# 1. 查看更改
git status

# 2. 添加文件
git add .

# 3. 提交更改
git commit -m "feat: 添加新功能"

# 4. 推送到 GitHub
git push
```

### 拉取最新更改

```bash
git pull origin main
```

---

## 🛡️ 安全建议

1. **不要在代码中包含敏感信息**
   - API 密钥
   - 密码
   - 个人信息

2. **使用 .gitignore 文件**
   项目已包含 .gitignore，确保敏感文件不会被提交

3. **定期更新依赖**
   定期运行 `pip install --upgrade -r requirements.txt`

---

## 📚 推荐的仓库结构

```
rebar-steel-futures-trading-system/
├── README.md                      # 项目说明
├── AGENT.md                       # Agent 规范
├── .gitignore                     # Git 忽略文件
├── requirements.txt               # Python 依赖
├── config/                        # 配置文件
│   ├── agent_llm_config.json
│   └── scheduler_config.json
├── src/                           # 源代码
│   ├── agents/                    # Agent 代码
│   ├── tools/                     # 工具代码
│   ├── scheduler/                 # 定时任务
│   ├── storage/                   # 存储模块
│   ├── utils/                     # 工具函数
│   └── main.py                    # 主入口
├── tests/                         # 测试代码
├── assets/                        # 资源文件
├── docs/                          # 文档
├── scripts/                       # 脚本
├── test_scheduler.py              # 定时任务测试
├── test_wechat_notification.py    # 企业微信测试
└── check_integration.py           # 集成检查脚本
```

---

## 🎯 快速命令参考

```bash
# 查看状态
git status

# 查看提交历史
git log --oneline

# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin <URL>

# 推送代码
git push -u origin main

# 拉取更新
git pull origin main

# 创建分支
git checkout -b <branch-name>

# 切换分支
git checkout <branch-name>
```

---

## ✅ 完成检查清单

提交代码前，请确认：

- [ ] 代码已测试通过
- [ ] 文档已更新
- [ ] 敏感信息已排除
- [ ] .gitignore 配置正确
- [ ] 提交信息清晰明确
- [ ] README.md 完整

---

## 📞 遇到问题？

如果遇到问题，请：

1. 查看错误信息
2. 检查 Git 配置
3. 确认 GitHub 仓库地址
4. 验证网络连接
5. 查看 [Git 官方文档](https://git-scm.com/doc)

---

**祝您提交顺利！** 🎉
