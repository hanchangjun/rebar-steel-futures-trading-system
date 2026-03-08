# 定时任务功能使用指南

## 📋 概述

本系统已集成基于 APScheduler 的定时任务功能，可以自动执行螺纹钢期货的市场分析、交易信号监控等任务，并通过企业微信推送通知。

---

## 🎯 功能特性

### 1. 每日收盘后市场分析报告
- **执行时间**: 每个工作日 15:30
- **功能**: 分析螺纹钢期货的市场状况，生成完整的技术分析报告
- **推送内容**: 
  - 市场概况（价格、涨跌幅）
  - 技术指标分析（MA、MACD、RSI、KDJ、布林带）
  - 买卖点判断
  - 交易建议（支撑位、压力位、止损止盈、仓位建议）
  - 风险提示

### 2. 每日开盘前市场摘要
- **执行时间**: 每个工作日 8:30
- **功能**: 生成每日开盘前的市场摘要
- **推送内容**:
  - 昨日收盘价格和涨跌幅
  - 今日开盘价格
  - 关键支撑位和压力位
  - 今日重点关注事项
  - 风险提示

### 3. 交易信号监控
- **执行时间**: 交易时段（9:00-15:00）每 30 分钟
- **功能**: 实时监控交易信号
- **触发条件**:
  - MACD 金叉/死叉
  - RSI 超买超卖
  - 突破压力位/跌破支撑位
  - 其他重要技术信号
- **推送内容**: 
  - 信号类型（买入/卖出）
  - 当前价格
  - 信号强度
  - 关键价位
  - 交易建议

---

## ⚙️ 配置文件

定时任务的配置文件位于：`config/scheduler_config.json`

### 配置说明

```json
{
  "scheduler": {
    "enabled": true,              // 是否启用定时任务功能
    "timezone": "Asia/Shanghai"   // 时区设置
  },
  "tasks": {
    "daily_market_analysis": {
      "enabled": true,            // 是否启用此任务
      "name": "每日收盘后市场分析报告",
      "description": "每个工作日收盘后（15:30）发送螺纹钢期货市场分析报告",
      "cron": {
        "hour": 15,               // 小时 (0-23)
        "minute": 30,             // 分钟 (0-59)
        "day_of_week": "mon-fri"  // 星期几 (mon-fri = 周一到周五)
      }
    },
    "morning_market_summary": {
      "enabled": true,
      "name": "每日开盘前市场摘要",
      "description": "每个工作日开盘前（8:30）发送螺纹钢期货市场摘要",
      "cron": {
        "hour": 8,
        "minute": 30,
        "day_of_week": "mon-fri"
      }
    },
    "monitor_trading_signals": {
      "enabled": true,
      "name": "交易信号监控",
      "description": "交易时段（9:00-15:00）每30分钟监控一次交易信号",
      "cron": [
        {"hour": 9, "minute": 0, "day_of_week": "mon-fri"},
        {"hour": 9, "minute": 30, "day_of_week": "mon-fri"},
        {"hour": 10, "minute": 0, "day_of_week": "mon-fri"},
        {"hour": 10, "minute": 30, "day_of_week": "mon-fri"},
        {"hour": 11, "minute": 0, "day_of_week": "mon-fri"},
        {"hour": 13, "minute": 30, "day_of_week": "mon-fri"},
        {"hour": 14, "minute": 0, "day_of_week": "mon-fri"},
        {"hour": 14, "minute": 30, "day_of_week": "mon-fri"}
      ]
    }
  }
}
```

### 配置示例

#### 示例 1: 修改每日市场分析报告的执行时间

```json
"daily_market_analysis": {
  "enabled": true,
  "cron": {
    "hour": 16,           // 改为 16:00 执行
    "minute": 0,
    "day_of_week": "mon-fri"
  }
}
```

#### 示例 2: 禁用交易信号监控

```json
"monitor_trading_signals": {
  "enabled": false,       // 禁用此任务
  ...
}
```

#### 示例 3: 在周末也执行任务

```json
"daily_market_analysis": {
  "enabled": true,
  "cron": {
    "hour": 15,
    "minute": 30,
    "day_of_week": "*"    // * 表示每天
  }
}
```

---

## 🔧 API 接口

系统提供了定时任务管理的 RESTful API 接口：

### 1. 获取所有任务列表

**接口**: `GET /scheduler/jobs`

**响应示例**:
```json
{
  "status": "success",
  "total": 10,
  "jobs": [
    {
      "id": "daily_market_analysis",
      "name": "send_daily_market_analysis_task",
      "next_run_time": "2026-03-09T15:30:00+08:00",
      "trigger": "cron[hour=15, minute=30, day_of_week=mon-fri]"
    },
    ...
  ]
}
```

### 2. 获取指定任务详情

**接口**: `GET /scheduler/jobs/{job_id}`

**示例**:
```bash
curl http://localhost:5000/scheduler/jobs/daily_market_analysis
```

### 3. 暂停任务

**接口**: `POST /scheduler/jobs/{job_id}/pause`

**示例**:
```bash
curl -X POST http://localhost:5000/scheduler/jobs/daily_market_analysis/pause
```

### 4. 恢复任务

**接口**: `POST /scheduler/jobs/{job_id}/resume`

**示例**:
```bash
curl -X POST http://localhost:5000/scheduler/jobs/daily_market_analysis/resume
```

### 5. 删除任务

**接口**: `DELETE /scheduler/jobs/{job_id}`

**示例**:
```bash
curl -X DELETE http://localhost:5000/scheduler/jobs/daily_market_analysis
```

### 6. 手动触发任务

**接口**: `POST /scheduler/trigger/{job_id}`

**示例**:
```bash
curl -X POST http://localhost:5000/scheduler/trigger/daily_market_analysis
```

### 7. 获取调度器状态

**接口**: `GET /scheduler/status`

**响应示例**:
```json
{
  "status": "success",
  "running": true,
  "job_count": 10
}
```

---

## 🧪 测试功能

系统提供了完整的测试脚本：`test_scheduler.py`

### 运行测试

```bash
python test_scheduler.py
```

### 测试内容

1. ✅ 调度器初始化测试
2. ✅ API 端点测试
3. ✅ 每日市场分析任务测试
4. ✅ 每日市场摘要任务测试
5. ✅ 交易信号监控任务测试

---

## 🚀 使用场景

### 场景 1: 自动接收每日报告

**需求**: 每天收盘后自动收到市场分析报告

**配置**: 确保以下配置启用
```json
"daily_market_analysis": {
  "enabled": true
}
```

**效果**: 每个工作日 15:30，系统会自动分析市场并发送报告到企业微信

---

### 场景 2: 实时监控重要信号

**需求**: 在交易时段实时监控重要的买入/卖出信号

**配置**: 确保以下配置启用
```json
"monitor_trading_signals": {
  "enabled": true
}
```

**效果**: 
- 交易时段每 30 分钟检查一次市场
- 发现重要信号立即推送到企业微信
- 不重要信号不推送，避免骚扰

---

### 场景 3: 自定义执行时间

**需求**: 希望在特定时间收到报告

**配置**: 修改配置文件中的执行时间
```json
"daily_market_analysis": {
  "cron": {
    "hour": 16,      // 改为下午 4 点
    "minute": 0,
    "day_of_week": "mon-fri"
  }
}
```

---

### 场景 4: 临时暂停任务

**需求**: 暂时不接收通知

**方法**: 使用 API 暂停任务
```bash
curl -X POST http://localhost:5000/scheduler/jobs/daily_market_analysis/pause
```

**恢复任务**:
```bash
curl -X POST http://localhost:5000/scheduler/jobs/daily_market_analysis/resume
```

---

## 📊 日志查看

定时任务的所有操作都会记录在日志中。

### 日志位置

`/app/work/logs/bypass/app.log`

### 查看日志

```bash
# 查看最新的定时任务日志
tail -n 50 /app/work/logs/bypass/app.log | grep "定时任务"

# 查看所有定时任务相关日志
grep "定时任务" /app/work/logs/bypass/app.log

# 实时监控日志
tail -f /app/work/logs/bypass/app.log | grep "定时任务"
```

### 日志示例

```
2026-03-08 15:30:00 - INFO - 开始执行每日市场分析任务: 2026-03-08 15:30:00
2026-03-08 15:30:15 - INFO - 每日市场分析任务执行成功: 2026-03-08 15:30:15
2026-03-08 15:30:15 - INFO - 定时任务执行成功: daily_market_analysis at 2026-03-08 15:30:15
```

---

## ⚠️ 注意事项

### 1. 企业微信配置

定时任务依赖企业微信通知功能，确保：
- ✅ 企业微信机器人已正确配置
- ✅ Webhook URL 已在平台配置
- ✅ 可以正常发送测试消息

### 2. 时区设置

- 系统默认使用 `Asia/Shanghai` 时区
- 修改时区时请同步修改配置文件中的 `timezone` 字段

### 3. 任务冲突

- 避免设置过于频繁的执行时间
- 多个任务同时执行可能影响性能
- 建议任务间隔至少 5 分钟

### 4. 网络依赖

- 任务执行需要网络连接
- 确保服务器可以访问外部 API
- 网络异常时任务会记录错误日志

### 5. 错误处理

- 任务执行失败会自动记录日志
- 单个任务失败不会影响其他任务
- 建议定期检查日志

---

## 🔍 故障排查

### 问题 1: 定时任务未执行

**可能原因**:
- 调度器未启动
- 任务被禁用
- 配置文件错误

**解决方案**:
1. 检查调度器状态: `GET /scheduler/status`
2. 检查配置文件是否正确
3. 查看日志: `tail -n 100 /app/work/logs/bypass/app.log`

---

### 问题 2: 任务执行失败

**可能原因**:
- 企业微信配置错误
- Agent 执行异常
- 网络连接问题

**解决方案**:
1. 查看详细错误日志
2. 测试企业微信通知功能
3. 测试 Agent 是否正常工作

---

### 问题 3: 企业微信收不到消息

**可能原因**:
- Webhook URL 配置错误
- 机器人被删除
- 消息格式错误

**解决方案**:
1. 手动发送测试消息
2. 检查企业微信机器人状态
3. 查看 Agent 日志

---

### 问题 4: 任务执行时间不准确

**可能原因**:
- 时区设置错误
- 服务器时间不准

**解决方案**:
1. 检查服务器时间
2. 确认时区配置
3. 同步系统时间

---

## 💡 最佳实践

### 1. 合理设置执行时间

- 收盘报告：建议 15:30-16:00
- 开盘摘要：建议 8:30-9:00
- 信号监控：建议交易时段每 30-60 分钟

### 2. 监控任务执行

- 定期查看日志
- 监控企业微信消息接收
- 使用 API 查询任务状态

### 3. 错误告警

- 设置任务失败告警
- 定期检查系统健康
- 备份重要配置

### 4. 性能优化

- 避免过于频繁的任务
- 合理设置任务超时
- 监控系统资源使用

---

## 📚 相关文档

- [企业微信通知功能使用指南](./WECHAT_NOTIFICATION_GUIDE.md)
- [企业微信配置指南](./WECHAT_CONFIG_GUIDE.md)
- [系统部署指南](./DEPLOYMENT_GUIDE.md)

---

## 🎉 总结

定时任务功能让系统可以自动化执行市场分析和交易监控，无需人工干预。

配置完成后，您将能够：
- 📱 自动接收每日市场分析报告
- 🚨 实时获取重要交易信号
- 📊 每日开盘前了解市场概况
- ⚙️ 灵活管理定时任务

立即开始配置，享受自动化带来的便利吧！

---

**如有问题，请参考故障排查部分或联系技术支持**
