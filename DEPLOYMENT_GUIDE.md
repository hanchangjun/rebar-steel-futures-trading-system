# 螺纹钢期货交易系统 - 本地部署指南

## 📋 目录

1. [环境要求](#环境要求)
2. [安装步骤](#安装步骤)
3. [启动服务](#启动服务)
4. [测试验证](#测试验证)
5. [常见问题](#常见问题)
6. [生产部署建议](#生产部署建议)

---

## 环境要求

### 系统要求
- **操作系统**: Linux / macOS / Windows
- **Python 版本**: 3.10 或更高版本
- **内存**: 至少 2GB RAM
- **磁盘空间**: 至少 1GB 可用空间

### 必需软件
- Python 3.10+
- pip (Python 包管理器)
- git (可选，用于版本控制)

---

## 安装步骤

### 步骤 1: 检查 Python 版本

```bash
python --version
# 或
python3 --version
```

**预期输出**：Python 3.10.0 或更高版本

如果版本低于 3.10，请先升级 Python。

---

### 步骤 2: 获取项目代码

#### 方式 A: 从 Git 仓库克隆（推荐）

```bash
# 如果项目在 Git 仓库
git clone <repository-url>
cd futures-trading-system
```

#### 方式 B: 直接复制项目文件

```bash
# 进入项目目录
cd /workspace/projects
```

---

### 步骤 3: 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**为什么要使用虚拟环境？**
- 隔离项目依赖，避免与系统 Python 冲突
- 便于管理不同项目的依赖
- 提高可移植性

---

### 步骤 4: 安装依赖

```bash
# 确保在虚拟环境中
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

**依赖包说明**：

| 依赖包 | 版本 | 用途 |
|--------|------|------|
| fastapi | 最新版 | Web 框架 |
| uvicorn | 最新版 | ASGI 服务器 |
| langchain | 1.0.3 | LLM 框架 |
| langgraph | 1.0.2 | 智能体框架 |
| pandas | 2.2.2 | 数据处理 |
| numpy | 2.2.6 | 数值计算 |
| requests | 2.32.5 | HTTP 请求 |
| coze-coding-dev-sdk | 0.5.9 | Coze 开发 SDK |

---

### 步骤 5: 验证安装

```bash
# 检查关键包是否安装成功
python -c "import fastapi; import langchain; import pandas; print('安装成功！')"
```

**预期输出**：`安装成功！`

---

## 启动服务

### 方式 1: HTTP 服务模式（推荐）

这是最常用的方式，启动一个 HTTP 服务，可以通过 API 调用智能体。

```bash
# 激活虚拟环境（如果还没激活）
source venv/bin/activate  # Linux / macOS
# 或
venv\Scripts\activate  # Windows

# 启动 HTTP 服务（默认端口 5000）
python src/main.py -m http -p 5000
```

**启动参数说明**：

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `-m` | 运行模式 | http | `-m http` |
| `-p` | 端口号 | 5000 | `-p 8000` |

**其他启动示例**：

```bash
# 使用端口 8000
python src/main.py -m http -p 8000

# 使用端口 3000
python src/main.py -m http -p 3000
```

**启动成功标志**：

看到以下输出表示启动成功：

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:5000
```

**访问地址**：
- 本地访问: http://localhost:5000
- 局域网访问: http://[你的IP]:5000

---

### 方式 2: Agent 模式（开发测试）

用于直接测试 Agent 功能，不需要启动 HTTP 服务。

```bash
python src/main.py -m agent
```

这会运行一个内置的测试查询，输出 Agent 的响应。

---

### 方式 3: 脚本化部署

创建启动脚本，便于重复使用。

#### Linux / macOS 脚本

创建文件 `start.sh`：

```bash
#!/bin/bash

# 激活虚拟环境
source venv/bin/activate

# 设置环境变量（如果需要）
export APP_ENV=production
export APP_PORT=5000

# 启动服务
python src/main.py -m http -p $APP_PORT
```

**赋予执行权限**：
```bash
chmod +x start.sh
```

**启动服务**：
```bash
./start.sh
```

#### Windows 脚本

创建文件 `start.bat`：

```batch
@echo off

REM 激活虚拟环境
call venv\Scripts\activate

REM 设置环境变量（如果需要）
set APP_ENV=production
set APP_PORT=5000

REM 启动服务
python src/main.py -m http -p %APP_PORT%

pause
```

**启动服务**：
```bash
start.bat
```

---

## 测试验证

### 测试 1: 健康检查

```bash
# 检查服务是否运行
curl http://localhost:5000

# 或使用浏览器访问
# http://localhost:5000
```

---

### 测试 2: 简单查询

```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "type": "query",
    "session_id": "test_001",
    "message": "你好，请介绍一下自己"
  }'
```

**预期输出**：

```json
{
  "run_id": "uuid-xxxx-xxxx-xxxx",
  "result": "你好！我是螺纹钢期货交易分析系统..."
}
```

---

### 测试 3: 查询实时行情

```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "type": "query",
    "session_id": "test_002",
    "message": "请帮我查询螺纹钢期货的实时行情"
  }'
```

---

### 测试 4: 综合分析

```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "type": "query",
    "session_id": "test_003",
    "message": "请帮我查询螺纹钢期货的实时行情，并分析当前的市场状况，给出买卖建议"
  }'
```

---

### 测试 5: 使用 Python 客户端

创建测试文件 `test_client.py`：

```python
import requests

def test_query():
    url = "http://localhost:5000/run"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "type": "query",
        "session_id": "test_python",
        "message": "请帮我查询螺纹钢期货的实时行情"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        print("查询成功！")
        print(result.get("result", ""))
    except requests.exceptions.RequestException as e:
        print(f"查询失败: {e}")

if __name__ == "__main__":
    test_query()
```

**运行测试**：
```bash
python test_client.py
```

---

## 常见问题

### 问题 1: 端口被占用

**错误信息**：
```
OSError: [Errno 48] Address already in use
```

**解决方案**：

1. 查找占用端口的进程：
```bash
# Linux / macOS
lsof -i :5000

# Windows
netstat -ano | findstr :5000
```

2. 终止占用进程或更换端口：
```bash
# 更换端口启动
python src/main.py -m http -p 8000
```

---

### 问题 2: Python 版本不兼容

**错误信息**：
```
SyntaxError: invalid syntax
```

**解决方案**：

```bash
# 检查 Python 版本
python --version

# 如果版本低于 3.10，升级 Python
# Ubuntu / Debian
sudo apt-get update
sudo apt-get install python3.10

# macOS (使用 Homebrew)
brew install python@3.10

# Windows
# 从 python.org 下载安装
```

---

### 问题 3: 依赖包安装失败

**错误信息**：
```
ERROR: Could not find a version that satisfies the requirement xxx
```

**解决方案**：

```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像源安装
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或逐个安装失败的包
pip install <package-name>
```

---

### 问题 4: 虚拟环境无法激活

**错误信息**：
```
bash: venv/bin/activate: No such file or directory
```

**解决方案**：

```bash
# 重新创建虚拟环境
python -m venv venv

# 检查虚拟环境目录
ls -la venv/
```

---

### 问题 5: 依赖冲突

**错误信息**：
```
ERROR: pip's dependency resolver does not currently take into account...
```

**解决方案**：

```bash
# 卸载现有依赖，重新安装
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# 或使用 pip-tools 管理依赖
pip install pip-tools
pip-compile requirements.in
pip-sync requirements.txt
```

---

### 问题 6: 服务启动后无法访问

**症状**：启动成功，但无法访问 http://localhost:5000

**排查步骤**：

1. 检查服务是否真的在运行：
```bash
ps aux | grep python
```

2. 检查防火墙设置：
```bash
# Linux (ufw)
sudo ufw allow 5000

# macOS
# 系统偏好设置 -> 安全性与隐私 -> 防火墙
```

3. 检查端口监听：
```bash
netstat -tuln | grep 5000
```

---

### 问题 7: 查询超时

**错误信息**：
```
requests.exceptions.Timeout
```

**解决方案**：

1. 增加客户端超时时间：
```python
response = requests.post(url, json=payload, timeout=300)  # 5分钟
```

2. 简化查询内容
3. 使用流式接口代替非流式接口

---

## 生产部署建议

### 1. 使用 Gunicorn + Uvicorn Workers

**安装**：
```bash
pip install gunicorn
```

**启动**：
```bash
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:5000 \
  --timeout 600
```

**参数说明**：
- `--workers 4`: 4个工作进程
- `--worker-class uvicorn.workers.UvicornWorker`: 使用 Uvicorn worker
- `--bind 0.0.0.0:5000`: 绑定所有网卡，端口 5000
- `--timeout 600`: 超时时间 600 秒

---

### 2. 使用 Supervisor 守护进程

**安装**：
```bash
# Ubuntu / Debian
sudo apt-get install supervisor

# CentOS / RHEL
sudo yum install supervisor
```

**配置文件** `/etc/supervisor/conf.d/futures-trading.conf`：

```ini
[program:futures-trading]
command=/path/to/venv/bin/python /path/to/src/main.py -m http -p 5000
directory=/path/to/project
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/futures-trading.err.log
stdout_logfile=/var/log/futures-trading.out.log
```

**启动**：
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start futures-trading
```

---

### 3. 使用 Docker 容器化

**Dockerfile**：

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "src/main.py", "-m", "http", "-p", "5000"]
```

**构建和运行**：

```bash
# 构建镜像
docker build -t futures-trading-system .

# 运行容器
docker run -d \
  --name futures-trading \
  -p 5000:5000 \
  futures-trading-system
```

---

### 4. 使用 Nginx 反向代理

**Nginx 配置** `/etc/nginx/sites-available/futures-trading`：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 超时设置
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
    }
}
```

**启用配置**：

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/futures-trading /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

---

### 5. 日志管理

**日志位置**：
- 应用日志：`/app/work/logs/bypass/app.log`
- Nginx 日志：`/var/log/nginx/`
- Supervisor 日志：`/var/log/futures-trading.*.log`

**日志轮转配置** `/etc/logrotate.d/futures-trading`：

```bash
/app/work/logs/bypass/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 www-data www-data
}
```

---

### 6. 监控和告警

**健康检查脚本** `health_check.sh`：

```bash
#!/bin/bash

response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"type": "query", "session_id": "health_check", "message": "ping"}')

if [ $response -eq 200 ]; then
    echo "Service is healthy"
    exit 0
else
    echo "Service is unhealthy (HTTP $response)"
    # 发送告警通知
    # curl -X POST $WEBHOOK_URL -d "Service is down!"
    exit 1
fi
```

**定时检查**：

```bash
# 添加到 crontab
*/5 * * * * /path/to/health_check.sh
```

---

### 7. 性能优化

#### 数据库连接池
```python
# 在配置中设置数据库连接池
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20
```

#### 缓存设置
```python
# 使用 Redis 缓存查询结果
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_TTL = 300  # 5分钟
```

#### 并发控制
```python
# 在启动命令中设置工作进程数
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

---

## 快速启动清单

完成以下检查清单，确保系统可以正常运行：

- [ ] Python 版本 >= 3.10
- [ ] 虚拟环境已创建并激活
- [ ] 所有依赖包已安装
- [ ] 配置文件存在且正确
- [ ] 端口未被占用
- [ ] 防火墙规则已配置
- [ ] 服务启动成功
- [ ] 健康检查通过
- [ ] 查询测试成功
- [ ] 日志正常输出

---

## 获取帮助

如果遇到问题：

1. **查看日志**：
```bash
tail -f /app/work/logs/bypass/app.log
```

2. **检查系统状态**：
```bash
ps aux | grep python
netstat -tuln | grep 5000
```

3. **查看文档**：
- README.md - 系统概述
- USER_GUIDE.md - 用户手册
- API_REFERENCE.md - API 文档

4. **联系技术支持**（如果可用）

---

## 总结

本部署指南涵盖了从环境准备到生产部署的完整流程。按照本指南操作，您应该能够在本地成功部署螺纹钢期货交易系统。

**关键步骤回顾**：
1. ✅ 检查环境要求
2. ✅ 创建虚拟环境
3. ✅ 安装依赖
4. ✅ 启动服务
5. ✅ 测试验证
6. ✅ 生产优化

祝您部署顺利！🚀

---

**版权所有 © 2026 螺纹钢期货买卖点交易系统**
