"""
企业微信通知工具（修复版）
用于将行情分析结果推送到企业微信群
"""

import json
import re
import logging
import os
from typing import Dict, Any, Optional
from datetime import datetime
from langchain.tools import tool, ToolRuntime
from coze_coding_utils.runtime_ctx.context import new_context
from coze_workload_identity import Client
from cozeloop.decorator import observe

import requests

logger = logging.getLogger("tools.wechat_notification_tool")


def get_webhook_key() -> Optional[str]:
    """
    获取企业微信机器人 webhook key
    
    优先级：
    1. 从 coze_workload_identity 获取集成配置
    2. 从环境变量 INTEGRATION_WECHAT_BOT 获取
    3. 从环境变量 WECHAT_BOT_WEBHOOK_KEY 获取
    
    Returns:
        webhook key，如果未配置则返回 None
    """
    # 方式 1: 从 coze_workload_identity 获取
    try:
        client = Client()
        wechat_bot_credential = client.get_integration_credential("integration-wechat-bot")
        webhook_key = json.loads(wechat_bot_credential)["webhook_key"]
        if "https" in webhook_key:
            match = re.search(r"key=([a-zA-Z0-9-]+)", webhook_key)
            if match:
                webhook_key = match.group(1)
        logger.info(f"从 coze_workload_identity 获取 webhook key 成功")
        return webhook_key
    except Exception as e:
        logger.warning(f"从 coze_workload_identity 获取 webhook key 失败: {e}")
    
    # 方式 2: 从环境变量 INTEGRATION_WECHAT_BOT 获取
    try:
        webhook_url = os.getenv("INTEGRATION_WECHAT_BOT")
        if webhook_url:
            if "https" in webhook_url:
                match = re.search(r"key=([a-zA-Z0-9-]+)", webhook_url)
                if match:
                    webhook_key = match.group(1)
                    logger.info(f"从环境变量 INTEGRATION_WECHAT_BOT 获取 webhook key 成功")
                    return webhook_key
            else:
                logger.info(f"从环境变量 INTEGRATION_WECHAT_BOT 获取 webhook key 成功（直接是 key）")
                return webhook_url
    except Exception as e:
        logger.warning(f"从环境变量 INTEGRATION_WECHAT_BOT 获取 webhook key 失败: {e}")
    
    # 方式 3: 从环境变量 WECHAT_BOT_WEBHOOK_KEY 获取
    try:
        webhook_key = os.getenv("WECHAT_BOT_WEBHOOK_KEY")
        if webhook_key:
            logger.info(f"从环境变量 WECHAT_BOT_WEBHOOK_KEY 获取 webhook key 成功")
            return webhook_key
    except Exception as e:
        logger.warning(f"从环境变量 WECHAT_BOT_WEBHOOK_KEY 获取 webhook key 失败: {e}")
    
    # 所有方式都失败
    logger.error("无法获取企业微信 webhook key，请检查配置")
    return None


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
        
        if not webhook_key:
            error_msg = "⚠️ 企业微信通知未配置，消息未发送。请检查配置：\n"
            error_msg += "  1. 在 Vibe Coding 平台添加企业微信机器人集成\n"
            error_msg += "  2. 或设置环境变量 INTEGRATION_WECHAT_BOT 或 WECHAT_BOT_WEBHOOK_KEY"
            logger.warning(error_msg)
            return error_msg
        
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
            return f"❌ 发送失败: {result}"
        
        logger.info("✅ 企业微信消息发送成功")
        return f"✅ 发送成功: {result}"
        
    except Exception as e:
        logger.error(f"❌ 发送企业微信消息异常: {e}")
        return f"❌ 发送异常: {str(e)}"


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
        logger.error(f"❌ 发送市场分析到企业微信失败: {e}")
        return f"❌ 发送失败: {str(e)}"


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
        logger.error(f"❌ 发送告警到企业微信失败: {e}")
        return f"❌ 发送失败: {str(e)}"


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
        signal_icons = {
            "买入": "🟢",
            "卖出": "🔴",
            "观望": "🟡"
        }
        icon = signal_icons.get(signal_type, "📊")
        
        # 构造交易信号消息
        message = f"""## {icon} 螺纹钢期货交易信号

**时间**: {current_time}

### 信号概要
- **信号类型**: {signal_type} {icon}
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
        logger.error(f"❌ 发送交易信号到企业微信失败: {e}")
        return f"❌ 发送失败: {str(e)}"


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
    发送每日行情汇总报告到企业微信
    
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

### 行情数据
- **开盘价**: {open_price}
- **最高价**: {high_price}
- **最低价**: {low_price}
- **收盘价**: {close_price}
- **涨跌幅**: {change_percent}

### 市场分析
{analysis}

---

*数据来源：交易所官方*
"""
        
        # 发送消息
        result = send_to_wechat.invoke({
            "message": message,
            "message_type": "markdown"
        })
        
        return result
        
    except Exception as e:
        logger.error(f"❌ 发送每日报告到企业微信失败: {e}")
        return f"❌ 发送失败: {str(e)}"


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
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 构造错误消息
        message = f"""## 🚨 系统错误通知

**时间**: {current_time}

**错误信息**:
{error_message}

请及时检查系统日志并处理！

日志位置: /app/work/logs/bypass/app.log
"""
        
        # 发送消息
        result = send_to_wechat.invoke({
            "message": message,
            "message_type": "markdown"
        })
        
        return result
        
    except Exception as e:
        logger.error(f"❌ 发送错误通知到企业微信失败: {e}")
        return f"❌ 发送失败: {str(e)}"
