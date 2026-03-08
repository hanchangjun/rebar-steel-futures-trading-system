"""
企业微信通知工具
用于将行情分析结果推送到企业微信群
"""

import json
import re
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from langchain.tools import tool, ToolRuntime
from coze_coding_utils.runtime_ctx.context import new_context
from coze_workload_identity import Client
from cozeloop.decorator import observe

import requests

logger = logging.getLogger(__name__)


def get_webhook_key() -> str:
    """
    从环境变量获取企业微信机器人 webhook key
    
    Returns:
        webhook key
    """
    try:
        client = Client()
        wechat_bot_credential = client.get_integration_credential("integration-wechat-bot")
        webhook_key = json.loads(wechat_bot_credential)["webhook_key"]
        if "https" in webhook_key:
            webhook_key = re.search(r"key=([a-zA-Z0-9-]+)", webhook_key).group(1)
        return webhook_key
    except Exception as e:
        logger.error(f"获取企业微信 webhook key 失败: {e}")
        raise ValueError("无法获取企业微信 webhook key，请检查配置")


@tool
def send_to_wechat(message: str, message_type: str = "markdown", runtime: ToolRuntime = None) -> str:
    """
    发送消息到企业微信
    
    Args:
        message: 要发送的消息内容
        message_type: 消息类型，支持 "text"（文本）或 "markdown"（Markdown格式），默认为 "markdown"
    
    Returns:
        发送结果
    """
    try:
        # 获取 webhook key
        webhook_key = get_webhook_key()
        send_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
        
        # 构造消息体
        if message_type == "markdown":
            payload = {
                "msgtype": "markdown",
                "markdown": {
                    "content": message
                }
            }
        else:
            payload = {
                "msgtype": "text",
                "text": {
                    "content": message
                }
            }
        
        # 发送请求
        response = requests.post(send_url, json=payload, timeout=15)
        response.raise_for_status()
        result = response.json()
        
        if result.get("errcode", 0) != 0:
            logger.error(f"企业微信消息发送失败: {result}")
            return f"发送失败: {result}"
        
        logger.info("企业微信消息发送成功")
        return f"发送成功: {result}"
        
    except Exception as e:
        logger.error(f"发送企业微信消息异常: {e}")
        return f"发送异常: {str(e)}"


@tool
def send_market_analysis_to_wechat(analysis_result: str, runtime: ToolRuntime = None) -> str:
    """
    将市场分析结果格式化后发送到企业微信
    
    Args:
        analysis_result: 分析结果文本
    
    Returns:
        发送结果
    """
    try:
        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 格式化消息为 Markdown
        message = f"""## 📊 螺纹钢期货行情分析

**时间**: {current_time}

{analysis_result}

---

*⚠️ 以上分析仅供参考，不构成投资建议*
*📈 请根据自身风险承受能力谨慎决策*
"""
        
        # 发送消息
        result = send_to_wechat.invoke({
            "message": message,
            "message_type": "markdown"
        })
        
        return result
        
    except Exception as e:
        logger.error(f"发送市场分析到企业微信失败: {e}")
        return f"发送失败: {str(e)}"


@tool
def send_alert_to_wechat(alert_message: str, alert_level: str = "info", runtime: ToolRuntime = None) -> str:
    """
    发送紧急通知到企业微信
    
    Args:
        alert_message: 告警消息
        alert_level: 告警级别，可选 "info", "warning", "error"，默认为 "info"
    
    Returns:
        发送结果
    """
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 根据告警级别设置图标
        level_icons = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "🚨"
        }
        icon = level_icons.get(alert_level, "ℹ️")
        
        # 构造告警消息
        message = f"""## {icon} 交易系统告警

**时间**: {current_time}
**级别**: {alert_level.upper()}

**告警信息**:
{alert_message}

请及时查看并处理！
"""
        
        # 发送消息
        result = send_to_wechat.invoke({
            "message": message,
            "message_type": "markdown"
        })
        
        return result
        
    except Exception as e:
        logger.error(f"发送告警到企业微信失败: {e}")
        return f"发送失败: {str(e)}"


@tool
def send_trading_signal_to_wechat(
    signal_type: str,
    price: str,
    signal_strength: str,
    support_level: str,
    resistance_level: str,
    stop_loss: str,
    take_profit: str,
    position_size: str,
    runtime: ToolRuntime = None
) -> str:
    """
    发送交易信号到企业微信
    
    Args:
        signal_type: 信号类型（买入/卖出/观望）
        price: 当前价格
        signal_strength: 信号强度（强/中/弱）
        support_level: 支撑位
        resistance_level: 压力位
        stop_loss: 止损位
        take_profit: 止盈位
        position_size: 仓位建议
    
    Returns:
        发送结果
    """
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 根据信号类型设置图标和颜色
        signal_config = {
            "买入": {"icon": "🟢", "emoji": "📈"},
            "卖出": {"icon": "🔴", "emoji": "📉"},
            "观望": {"icon": "⚪", "emoji": "⏸️"}
        }
        config = signal_config.get(signal_type, {"icon": "⚪", "emoji": "⏸️"})
        
        # 构造交易信号消息
        message = f"""## {config['icon']} 螺纹钢期货交易信号

**时间**: {current_time}

### 信号概要
- **信号类型**: {signal_type} {config['emoji']}
- **当前价格**: {price}
- **信号强度**: {signal_strength}

### 关键价位
- **支撑位**: {support_level}
- **压力位**: {resistance_level}
- **止损位**: {stop_loss}
- **止盈位**: {take_profit}

### 交易建议
- **仓位建议**: {position_size}

---

*⚠️ 以上信号仅供参考，请结合自身判断进行决策*
*🎯 严格执行止损纪律，控制风险*
"""
        
        # 发送消息
        result = send_to_wechat.invoke({
            "message": message,
            "message_type": "markdown"
        })
        
        return result
        
    except Exception as e:
        logger.error(f"发送交易信号到企业微信失败: {e}")
        return f"发送失败: {str(e)}"


@tool
def send_daily_report_to_wechat(
    date: str,
    open_price: str,
    high_price: str,
    low_price: str,
    close_price: str,
    change_percent: str,
    analysis: str,
    runtime: ToolRuntime = None
) -> str:
    """
    发送每日行情报告到企业微信
    
    Args:
        date: 日期
        open_price: 开盘价
        high_price: 最高价
        low_price: 最低价
        close_price: 收盘价
        change_percent: 涨跌幅
        analysis: 分析内容
    
    Returns:
        发送结果
    """
    try:
        # 构造每日报告消息
        message = f"""## 📈 螺纹钢期货每日报告

**日期**: {date}

### 今日行情
| 指标 | 数值 |
|------|------|
| 开盘价 | {open_price} |
| 最高价 | {high_price} |
| 最低价 | {low_price} |
| 收盘价 | {close_price} |
| 涨跌幅 | {change_percent} |

### 技术分析
{analysis}

### 明日展望
请关注关键技术位的变化，及时调整交易策略。

---

*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*📊 数据仅供参考，实际交易以交易所为准*
"""
        
        # 发送消息
        result = send_to_wechat.invoke({
            "message": message,
            "message_type": "markdown"
        })
        
        return result
        
    except Exception as e:
        logger.error(f"发送每日报告到企业微信失败: {e}")
        return f"发送失败: {str(e)}"


@tool
def send_error_to_wechat(error_message: str, runtime: ToolRuntime = None) -> str:
    """
    发送系统错误到企业微信
    
    Args:
        error_message: 错误消息
    
    Returns:
        发送结果
    """
    try:
        return send_alert_to_wechat.invoke({
            "alert_message": error_message,
            "alert_level": "error"
        })
    except Exception as e:
        return f"发送错误消息失败: {str(e)}"
