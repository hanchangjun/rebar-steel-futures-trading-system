# 定时任务功能 - 部署说明

## ✅ 功能已完成

定时发送市场分析报告功能已经完全集成到系统中！

### 📦 完成的工作

1. **创建定时任务调度器** (`src/scheduler/task_scheduler.py`)
   - ✅ 基于 APScheduler 的异步调度器
   - ✅ 支持 Cron 表达式和间隔调度
   - ✅ 任务生命周期管理（启动、暂停、恢复、删除）
   - ✅ 事件监听和日志记录

2. **实现定时任务** (`src/scheduler/tasks.py`)
   - ✅ 每日收盘后市场分析报告（15:30）
   - ✅ 每日开盘前市场摘要（8:30）
   - ✅ 交易信号监控（每30分钟）
   - ✅ 从配置文件加载任务配置

3. **创建管理 API** (`src/scheduler/api.py`)
   - ✅ GET `/scheduler/jobs` - 获取所有任务列表
   - ✅ GET `/scheduler/jobs/{job_id}` - 获取任务详情
   - ✅ POST `/scheduler/jobs/{job_id}/pause` - 暂停任务
   - ✅ POST `/scheduler/jobs/{job_id}/resume` - 恢复任务
   - ✅ DELETE `/scheduler/jobs/{job_id}` - 删除任务
   - ✅ POST `/scheduler/trigger/{job_id}` - 手动触发任务
   - ✅ GET `/scheduler/status` - 获取调度器状态

4. **配置文件** (`config/scheduler_config.json`)
   - ✅ 可配置的任务执行时间
   - ✅ 可单独启用/禁用每个任务
   - ✅ 支持时区设置

5. **集成到主应用** (`src/main.py`)
   - ✅ 应用启动时自动初始化调度器
   - ✅ 应用关闭时自动关闭调度器
   - ✅ 注册管理 API 路由

6. **文档**
   - ✅ `SCHEDULER_GUIDE.md` - 完整使用指南
   - ✅ `test_scheduler.py` - 完整测试脚本
   - ✅ `test_scheduler_simple.py` - 简化测试脚本

---

## 🎯 功能说明

### 1. 每日收盘后市场分析报告

**执行时间**: 每个工作日 15:30

**功能**:
- 获取螺纹钢期货最新行情
- 进行技术指标分析（MA、MACD、RSI、KDJ、布林带）
- 识别买卖信号
- 提供交易建议（支撑位、压力位、止损止盈、仓位建议）
- 通过企业微信发送完整报告

**消息格式**:
```markdown
## 📊 螺纹钢期货行情分析

**时间**: 2026-03-08 15:30:00

【市场概况】
当前价格：3067元/吨
涨跌幅：+0.26%
市场状态：震荡

【技术分析】
...

【交易建议】
...

---

*⚠️ 以上分析仅供参考，不构成投资建议*
```

---

### 2. 每日开盘前市场摘要

**执行时间**: 每个工作日 8:30

**功能**:
- 生成每日开盘前的市场摘要
- 提供关键支撑位和压力位
- 列出当日重点关注事项
- 发送风险提示

---

### 3. 交易信号监控

**执行时间**: 交易时段（9:00-15:00）每30分钟

**功能**:
- 实时监控交易信号
- 检测重要技术信号（MACD金叉/死叉、RSI超买超卖等）
- 发现重要信号立即推送到企业微信
- 不重要信号不推送，避免骚扰

---

## ⚙️ 配置方法

### 1. 修改执行时间

编辑 `config/scheduler_config.json`:

```json
{
  "tasks": {
    "daily_market_analysis": {
      "enabled": true,
      "cron": {
        "hour": 16,    // 改为 16:00 执行
        "minute": 0,
        "day_of_week": "mon-fri"
      }
    }
  }
}
```

### 2. 启用/禁用任务

```json
{
  "tasks": {
    "daily_market_analysis": {
      "enabled": false   // 禁用此任务
    }
  }
}
```

### 3. 修改 Cron 表达式

支持的字段：
- `hour`: 小时 (0-23)
- `minute`: 分钟 (0-59)
- `day_of_week`: 星期几 (mon-fri, mon, tue, wed, thu, fri, sat, sun, *)
- `day`: 日期 (1-31)

---

## 🚀 使用方法

### 方法 1: 自动运行（推荐）

应用启动后，定时任务会自动运行：

```bash
# 启动应用
python -m uvicorn src.main:app --host 0.0.0.0 --port 5000
```

调度器会自动注册并在指定时间执行任务。

---

### 方法 2: 手动触发任务

通过 API 手动触发任务执行：

```bash
# 触发每日市场分析任务
curl -X POST http://localhost:5000/scheduler/trigger/daily_market_analysis

# 触发每日市场摘要任务
curl -X POST http://localhost:5000/scheduler/trigger/morning_market_summary

# 触发交易信号监控任务
curl -X POST http://localhost:5000/scheduler/trigger/monitor_trading_signals_0
```

---

### 方法 3: 查看任务状态

```bash
# 查看所有任务
curl http://localhost:5000/scheduler/jobs

# 查看调度器状态
curl http://localhost:5000/scheduler/status

# 查看指定任务详情
curl http://localhost:5000/scheduler/jobs/daily_market_analysis
```

---

### 方法 4: 暂停/恢复任务

```bash
# 暂停任务
curl -X POST http://localhost:5000/scheduler/jobs/daily_market_analysis/pause

# 恢复任务
curl -X POST http://localhost:5000/scheduler/jobs/daily_market_analysis/resume
```

---

## 🧪 测试功能

### 运行简单测试

```bash
cd /workspace/projects
python test_scheduler_simple.py
```

**测试内容**:
- ✅ 模块导入
- ✅ 调度器创建
- ✅ 配置文件加载

---

### 运行完整测试

```bash
cd /workspace/projects
python test_scheduler.py
```

**测试内容**:
- ✅ 调度器初始化
- ✅ API 端点
- ✅ 每日市场分析任务
- ✅ 每日市场摘要任务
- ✅ 交易信号监控任务

---

## 📊 日志查看

### 查看定时任务日志

```bash
# 查看最新的定时任务日志
tail -n 50 /app/work/logs/bypass/app.log | grep "定时任务"

# 实时监控日志
tail -f /app/work/logs/bypass/app.log | grep "定时任务"
```

### 日志示例

```
2026-03-08 15:30:00 - INFO - 应用启动中...
2026-03-08 15:30:00 - INFO - 定时任务已成功启动
2026-03-08 15:30:00 - INFO - 已注册 10 个定时任务:
2026-03-08 15:30:00 - INFO -   - daily_market_analysis: 2026-03-09 15:30:00
2026-03-08 15:30:00 - INFO - 开始执行每日市场分析任务: 2026-03-08 15:30:00
2026-03-08 15:30:15 - INFO - 每日市场分析任务执行成功: 2026-03-08 15:30:15
```

---

## ⚠️ 前置条件

在使用定时任务功能前，请确保：

1. ✅ 企业微信机器人已正确配置
2. ✅ Webhook URL 已在平台配置
3. ✅ Agent 和工具正常运行
4. ✅ 网络连接正常

---

## 💡 常见问题

### Q1: 如何确认定时任务是否运行？

**A**: 
1. 检查调度器状态: `GET /scheduler/status`
2. 查看任务列表: `GET /scheduler/jobs`
3. 查看日志: `tail -f /app/work/logs/bypass/app.log`

---

### Q2: 如何修改任务执行时间？

**A**: 编辑 `config/scheduler_config.json` 文件，修改对应任务的 `cron` 配置，然后重启应用。

---

### Q3: 如何临时暂停某个任务？

**A**: 使用 API 暂停任务：
```bash
curl -X POST http://localhost:5000/scheduler/jobs/{job_id}/pause
```

---

### Q4: 任务执行失败怎么办？

**A**:
1. 查看详细错误日志
2. 检查企业微信配置
3. 测试 Agent 是否正常工作
4. 使用 API 手动触发任务测试

---

## 📚 相关文档

- [定时任务功能使用指南](./SCHEDULER_GUIDE.md) - 详细使用说明
- [企业微信通知功能使用指南](./WECHAT_NOTIFICATION_GUIDE.md)
- [企业微信配置指南](./WECHAT_CONFIG_GUIDE.md)

---

## 🎉 总结

定时任务功能已完全集成，您可以：

- 📱 每天自动接收市场分析报告
- 🚨 实时获取重要交易信号
- 📊 每日开盘前了解市场概况
- ⚙️ 灵活管理定时任务

配置完成后，系统将自动在指定时间执行任务，无需人工干预！

---

**如有问题，请参考完整文档或联系技术支持**
