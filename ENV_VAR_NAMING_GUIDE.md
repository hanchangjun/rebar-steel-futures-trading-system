"""
环境变量配置说明

Vibe Coding 平台环境变量命名规范和配置方法
"""

## 环境变量命名规范

平台要求环境变量 Key 必须符合以下规则：
- ✅ 只能包含：下划线（_）、字母（a-z, A-Z）、数字（0-9）
- ✅ 不能以数字开头
- ✅ 最多 63 个字符

### 示例

✅ 符合规范：
- `INTEGRATION_WECHAT_BOT`
- `WECHAT_WEBHOOK_KEY`
- `COZE_API_KEY`
- `MY_CONFIG_123`

❌ 不符合规范：
- `integration-wechat-bot` (包含连字符)
- `123_CONFIG` (以数字开头)
- `CONFIG-WITH-DASHES` (包含连字符)

---

## 企业微信配置方式

### 方式 1: 使用集成管理（推荐）

无需手动配置环境变量，通过平台界面添加集成。

**优点**:
- 自动管理
- 安全性高
- 无需修改代码

**步骤**:
1. 项目 → 集成 → 添加企业微信机器人
2. 粘贴 Webhook URL
3. 保存

---

### 方式 2: 使用环境变量

如果平台不支持集成管理，使用环境变量配置。

**环境变量**:
```
Key: INTEGRATION_WECHAT_BOT
Value: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=XXXXX
```

**注意**: Key 使用下划线而非连字符

---

## 当前系统配置状态

系统已支持以下配置方式：

### 优先级 1: 集成管理（coze_workload_identity）
```python
from coze_workload_identity import Client

client = Client()
credential = client.get_integration_credential('integration-wechat-bot')
```

### 优先级 2: 环境变量（备用）
如果集成管理不可用，可以添加环境变量支持。

---

## 常见问题

### Q: 提示 "Key由_、字母、数字组成" 怎么办？

A: 将连字符（-）替换为下划线（_）
- `integration-wechat-bot` → `INTEGRATION_WECHAT_BOT`
- `coze-api-key` → `COZE_API_KEY`

### Q: 不能以数字开头怎么办？

A: 在前面添加字母前缀
- `123_KEY` → `KEY_123`
- `2024_CONFIG` → `CONFIG_2024`

### Q: 超过 63 个字符怎么办？

A: 使用缩写
- `VERY_LONG_INTEGRATION_NAME_THAT_EXCEEDS_LIMIT` → `VL_INT_NAME`

---

## 推荐的环境变量命名

```
# 企业微信
INTEGRATION_WECHAT_BOT
WECHAT_BOT_WEBHOOK_KEY

# 大模型
COZE_MODEL_API_KEY
MODEL_BASE_URL

# 数据库
DB_HOST
DB_PORT
DB_USERNAME
DB_PASSWORD
```

---

## 总结

- ✅ 优先使用集成管理功能（无需环境变量）
- ✅ 如需环境变量，使用下划线命名
- ❌ 避免使用连字符、特殊字符
- ❌ 避免以数字开头
