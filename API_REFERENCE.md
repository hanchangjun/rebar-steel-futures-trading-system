# 螺纹钢期货交易系统 - API 使用文档

## 📚 目录

1. [API 概述](#api-概述)
2. [接口列表](#接口列表)
3. [请求格式](#请求格式)
4. [响应格式](#响应格式)
5. [调用示例](#调用示例)
6. [错误码说明](#错误码说明)
7. [最佳实践](#最佳实践)

---

## API 概述

### 基本信息

- **Base URL**: `http://localhost:5000`
- **Content-Type**: `application/json`
- **字符编码**: `UTF-8`
- **请求方法**: POST

### 接口类型

| 接口类型 | 端点 | 说明 |
|---------|------|------|
| 非流式接口 | `/run` | 同步请求，等待完整结果返回 |
| 流式接口 | `/stream_run` | 异步请求，实时推送结果 |

---

## 接口列表

### 1. 非流式接口 (`/run`)

#### 接口描述
同步请求接口，发送查询后等待系统返回完整结果。

#### 请求方式
```http
POST /run
Content-Type: application/json
```

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| type | string | 是 | 固定值："query" |
| session_id | string | 是 | 会话ID，用于区分不同用户 |
| message | string | 是 | 用户消息内容 |

#### 请求示例
```json
{
  "type": "query",
  "session_id": "user_001",
  "message": "请帮我查询螺纹钢期货的实时行情"
}
```

#### 响应示例
```json
{
  "run_id": "uuid-xxxx-xxxx-xxxx",
  "result": "【市场概况】\n当前价格：3067元/吨\n..."
}
```

#### 特点
- ✅ 简单易用，适合快速查询
- ✅ 完整结果一次返回
- ❌ 需要等待完整处理完成
- ❌ 复杂查询可能超时

---

### 2. 流式接口 (`/stream_run`)

#### 接口描述
异步请求接口，实时推送处理结果，适合复杂查询。

#### 请求方式
```http
POST /stream_run
Content-Type: application/json
```

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| type | string | 是 | 固定值："query" |
| session_id | string | 是 | 会话ID，用于区分不同用户 |
| message | string | 是 | 用户消息内容 |

#### 请求示例
```json
{
  "type": "query",
  "session_id": "user_001",
  "message": "请帮我查询螺纹钢期货的实时行情，并分析当前的市场状况，给出买卖建议"
}
```

#### 响应格式
采用 Server-Sent Events (SSE) 格式，实时推送数据块。

```
event: message
data: {"type": "tool_call", "tool": "get_futures_realtime_quotes", ...}

event: message
data: {"type": "tool_result", "tool": "get_futures_realtime_quotes", ...}

event: message
data: {"type": "content", "content": "【市场概况】\n..."}
```

#### 特点
- ✅ 实时查看处理进度
- ✅ 适合复杂长时间查询
- ✅ 用户体验更好
- ❌ 实现稍微复杂

---

## 请求格式

### 基本结构

```json
{
  "type": "query",
  "session_id": "会话ID",
  "message": "用户消息内容"
}
```

### 参数说明

#### type
- **类型**: string
- **必填**: 是
- **说明**: 固定值 "query"，标识这是查询请求
- **示例**: `"query"`

#### session_id
- **类型**: string
- **必填**: 是
- **说明**: 用于标识会话，支持多轮对话记忆
- **格式**: 建议使用唯一标识符
- **示例**:
  - `"user_001"`
  - `"session_20260302_001"`
  - `"8f3d9e1a-5c2b-4d7f-9e8a-1b3d5e7f9a2c"`

#### message
- **类型**: string
- **必填**: 是
- **说明**: 用户要查询的内容或问题
- **格式**: 自然语言文本
- **示例**:
  - `"请帮我查询螺纹钢期货的实时行情"`
  - `"当前螺纹钢期货价格是多少？"`
  - `"我有以下K线数据，请帮我计算所有技术指标：[数据]"`

---

## 响应格式

### 非流式响应

#### 成功响应
```json
{
  "run_id": "8f3d9e1a-5c2b-4d7f-9e8a-1b3d5e7f9a2c",
  "result": "【市场概况】\n当前价格：3067元/吨\n涨跌幅：+0.26%\n...",
  "status": "success"
}
```

#### 错误响应
```json
{
  "status": "error",
  "error_code": "INVALID_INPUT",
  "error_message": "输入格式错误",
  "stack_trace": "...",
  "run_id": "8f3d9e1a-5c2b-4d7f-9e8a-1b3d5e7f9a2c"
}
```

#### 字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| run_id | string | 请求唯一标识 |
| result | string | 查询结果内容 |
| status | string | 请求状态：success/error |
| error_code | string | 错误码（仅错误时） |
| error_message | string | 错误信息（仅错误时） |
| stack_trace | string | 错误堆栈（仅错误时） |

---

### 流式响应

#### SSE 格式

```
event: message
data: {"type": "tool_call", "content": "正在获取实时行情..."}

event: message
data: {"type": "content", "content": "【市场概况】\n当前价格：3067元/吨"}

event: message
data: {"type": "done", "run_id": "8f3d9e1a-5c2b-4d7f-9e8a-1b3d5e7f9a2c"}
```

#### 数据类型

| type | 说明 | content 示例 |
|------|------|--------------|
| `tool_call` | 工具调用 | 正在获取实时行情... |
| `tool_result` | 工具返回 | {"price": 3067, ...} |
| `content` | 内容输出 | 【市场概况】\n... |
| `error` | 错误信息 | 获取数据失败 |
| `done` | 完成 | 请求处理完成 |

---

## 调用示例

### 1. 使用 curl 调用

#### 非流式接口
```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "type": "query",
    "session_id": "user_001",
    "message": "请帮我查询螺纹钢期货的实时行情"
  }'
```

#### 流式接口
```bash
curl -X POST http://localhost:5000/stream_run \
  -H "Content-Type: application/json" \
  -d '{
    "type": "query",
    "session_id": "user_001",
    "message": "请帮我查询螺纹钢期货的实时行情，并分析当前的市场状况，给出买卖建议"
  }'
```

---

### 2. 使用 Python 调用

#### 非流式接口
```python
import requests
import json

# 接口地址
url = "http://localhost:5000/run"

# 请求头
headers = {
    "Content-Type": "application/json"
}

# 请求参数
payload = {
    "type": "query",
    "session_id": "user_001",
    "message": "请帮我查询螺纹钢期货的实时行情"
}

# 发送请求
response = requests.post(url, headers=headers, json=payload)

# 解析响应
if response.status_code == 200:
    result = response.json()
    print(result["result"])
else:
    print(f"请求失败: {response.status_code}")
    print(response.text)
```

#### 流式接口
```python
import requests
import json

# 接口地址
url = "http://localhost:5000/stream_run"

# 请求头
headers = {
    "Content-Type": "application/json"
}

# 请求参数
payload = {
    "type": "query",
    "session_id": "user_001",
    "message": "请帮我查询螺纹钢期货的实时行情，并分析当前的市场状况，给出买卖建议"
}

# 发送请求（流式）
response = requests.post(url, headers=headers, json=payload, stream=True)

# 逐行读取响应
for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        # 解析 SSE 格式
        if line.startswith('data: '):
            data = json.loads(line[6:])  # 去掉 'data: ' 前缀
            print(data)
```

#### Python 封装类
```python
import requests
import json
from typing import Optional, Dict, Any
import time

class FuturesTradingClient:
    """螺纹钢期货交易系统客户端"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
    
    def query(
        self,
        message: str,
        session_id: str = "default",
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        查询接口
        
        Args:
            message: 用户消息
            session_id: 会话ID
            stream: 是否使用流式接口
        
        Returns:
            查询结果
        """
        url = f"{self.base_url}/stream_run" if stream else f"{self.base_url}/run"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "type": "query",
            "session_id": session_id,
            "message": message
        }
        
        if stream:
            return self._stream_request(url, headers, payload)
        else:
            return self._sync_request(url, headers, payload)
    
    def _sync_request(
        self,
        url: str,
        headers: Dict[str, str],
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """同步请求"""
        response = requests.post(url, headers=headers, json=payload, timeout=600)
        response.raise_for_status()
        return response.json()
    
    def _stream_request(
        self,
        url: str,
        headers: Dict[str, str],
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """流式请求"""
        response = requests.post(url, headers=headers, json=payload, stream=True)
        response.raise_for_status()
        
        results = []
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = json.loads(line[6:])
                    results.append(data)
                    print(f"[{data.get('type', 'unknown')}] {data.get('content', '')}")
        
        return {
            "status": "success",
            "data": results
        }
    
    def get_realtime_quotes(self, symbol: str = "螺纹钢") -> str:
        """获取实时行情"""
        message = f"请帮我查询{symbol}期货的实时行情"
        result = self.query(message, stream=False)
        return result.get("result", "")
    
    def analyze_market(
        self,
        symbol: str = "螺纹钢"
    ) -> str:
        """分析市场"""
        message = f"请帮我查询{symbol}期货的实时行情，并分析当前的市场状况，给出买卖建议"
        result = self.query(message, stream=True)
        return result
    
    def get_market_news(self, symbol: str = "螺纹钢") -> str:
        """获取市场新闻"""
        message = f"请帮我获取{symbol}期货的最新市场新闻"
        result = self.query(message, stream=False)
        return result.get("result", "")


# 使用示例
if __name__ == "__main__":
    client = FuturesTradingClient()
    
    # 获取实时行情
    quotes = client.get_realtime_quotes()
    print("实时行情:")
    print(quotes)
    
    # 分析市场
    print("\n市场分析:")
    client.analyze_market()
    
    # 获取新闻
    print("\n市场新闻:")
    news = client.get_market_news()
    print(news)
```

---

### 3. 使用 JavaScript 调用

#### 非流式接口
```javascript
async function queryFutures(message, sessionId = "default") {
    const url = "http://localhost:5000/run";
    
    const payload = {
        type: "query",
        session_id: sessionId,
        message: message
    };
    
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log(result.result);
        return result;
        
    } catch (error) {
        console.error("请求失败:", error);
    }
}

// 使用示例
queryFutures("请帮我查询螺纹钢期货的实时行情");
```

#### 流式接口
```javascript
async function streamQueryFutures(message, sessionId = "default") {
    const url = "http://localhost:5000/stream_run";
    
    const payload = {
        type: "query",
        session_id: sessionId,
        message: message
    };
    
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
            const { done, value } = await reader.read();
            
            if (done) {
                break;
            }
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.substring(6));
                    console.log(data);
                }
            }
        }
        
    } catch (error) {
        console.error("请求失败:", error);
    }
}

// 使用示例
streamQueryFutures("请帮我查询螺纹钢期货的实时行情，并分析当前的市场状况，给出买卖建议");
```

---

### 4. 使用 Postman 调用

#### 配置步骤
1. 创建新请求
2. 选择 POST 方法
3. 输入 URL: `http://localhost:5000/run`
4. 在 Headers 中添加：
   - Key: `Content-Type`
   - Value: `application/json`
5. 在 Body 中选择 `raw` 和 `JSON`
6. 输入请求参数：
```json
{
  "type": "query",
  "session_id": "user_001",
  "message": "请帮我查询螺纹钢期货的实时行情"
}
7. 点击 Send 发送请求
```

---

## 错误码说明

### HTTP 状态码

| 状态码 | 说明 | 处理建议 |
|--------|------|---------|
| 200 | 请求成功 | 正常处理响应结果 |
| 400 | 请求参数错误 | 检查请求格式和参数 |
| 500 | 服务器内部错误 | 稍后重试或联系技术支持 |
| 504 | 请求超时 | 减少查询复杂度或增加超时时间 |

### 业务错误码

| 错误码 | 说明 | 处理建议 |
|--------|------|---------|
| INVALID_INPUT | 输入格式错误 | 检查 message 字段格式 |
| INVALID_SESSION | 会话ID无效 | 使用有效的 session_id |
| DATA_NOT_FOUND | 数据未找到 | 确认查询内容是否正确 |
| TIMEOUT | 请求超时 | 简化查询或使用流式接口 |
| RATE_LIMIT | 请求频率过高 | 稍后重试 |
| SERVICE_ERROR | 服务异常 | 联系技术支持 |

---

## 最佳实践

### 1. 请求优化

#### 使用合适的接口
- **简单查询**：使用非流式接口 `/run`
- **复杂分析**：使用流式接口 `/stream_run`

#### 设置合理的超时时间
```python
response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=600  # 10分钟超时
)
```

---

### 2. 错误处理

#### 完整的错误处理
```python
def query_with_retry(message, max_retries=3):
    for i in range(max_retries):
        try:
            result = client.query(message)
            return result
        except requests.exceptions.Timeout:
            if i < max_retries - 1:
                print(f"请求超时，重试 {i + 1}/{max_retries}")
                time.sleep(2 ** i)  # 指数退避
            else:
                raise
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            raise
```

---

### 3. 性能优化

#### 批量查询
```python
async def batch_query(messages):
    tasks = [client.query(msg) for msg in messages]
    results = await asyncio.gather(*tasks)
    return results
```

#### 缓存结果
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_quotes(session_id):
    return client.get_realtime_quotes()
```

---

### 4. 日志记录

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_query(message, session_id):
    logger.info(f"Query: {message}, Session: {session_id}")
    
    try:
        result = client.query(message, session_id)
        logger.info(f"Success: {len(result)}")
        return result
    except Exception as e:
        logger.error(f"Failed: {e}")
        raise
```

---

### 5. 会话管理

```python
class SessionManager:
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, user_id):
        session_id = f"{user_id}_{int(time.time())}"
        self.sessions[session_id] = {
            "user_id": user_id,
            "created_at": time.time(),
            "message_count": 0
        }
        return session_id
    
    def get_session(self, session_id):
        return self.sessions.get(session_id)
    
    def update_session(self, session_id):
        if session_id in self.sessions:
            self.sessions[session_id]["message_count"] += 1
            self.sessions[session_id]["last_active"] = time.time()
```

---

## 版本历史

### v1.0.0 (2026-03-02)
- ✅ 发布基础 API 接口
- ✅ 支持非流式和流式两种接口
- ✅ 支持多轮对话
- ✅ 完整的错误处理

---

## 技术支持

如有问题，请：
1. 查看本文档的错误码说明
2. 检查请求格式是否正确
3. 查看系统日志文件
4. 联系技术支持

---

**版权所有 © 2026 螺纹钢期货买卖点交易系统**
