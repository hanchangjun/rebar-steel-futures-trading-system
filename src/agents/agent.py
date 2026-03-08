"""
螺纹钢期货买卖点交易系统 Agent
"""

import os
import json
from typing import Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver

# 导入工具
from tools.futures_data_tool import (
    get_futures_realtime_quotes,
    get_futures_historical_data,
    get_futures_market_news,
    get_futures_analysis_report,
    get_comprehensive_market_info
)
from tools.technical_indicators import (
    calculate_ma,
    calculate_ema,
    calculate_macd,
    calculate_rsi,
    calculate_kdj,
    calculate_bollinger_bands,
    analyze_volume,
    calculate_all_indicators
)
from tools.wechat_notification_tool import (
    send_to_wechat,
    send_market_analysis_to_wechat,
    send_alert_to_wechat,
    send_trading_signal_to_wechat,
    send_daily_report_to_wechat,
    send_error_to_wechat
)

LLM_CONFIG = "config/agent_llm_config.json"

# 默认保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40


def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:]  # type: ignore


class AgentState(MessagesState):
    messages: Annotated[list[AnyMessage], _windowed_messages]


def build_agent(ctx=None):
    """
    构建螺纹钢期货交易分析 Agent
    
    Args:
        ctx: 可选的运行时上下文
    
    Returns:
        构建好的 Agent 实例
    """
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)
    
    # 读取配置文件
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    
    # 从环境变量获取 API 配置
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
    
    # 初始化 LLM
    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        top_p=cfg['config'].get('top_p', 0.9),
        max_completion_tokens=cfg['config'].get('max_completion_tokens', 10000),
        timeout=cfg['config'].get('timeout', 600),
        streaming=True,
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )
    
    # 配置工具列表
    tools = [
        # 期货数据获取工具
        get_futures_realtime_quotes,
        get_futures_historical_data,
        get_futures_market_news,
        get_futures_analysis_report,
        get_comprehensive_market_info,
        
        # 技术指标计算工具
        calculate_ma,
        calculate_ema,
        calculate_macd,
        calculate_rsi,
        calculate_kdj,
        calculate_bollinger_bands,
        analyze_volume,
        calculate_all_indicators,
        
        # 企业微信通知工具
        send_to_wechat,
        send_market_analysis_to_wechat,
        send_alert_to_wechat,
        send_trading_signal_to_wechat,
        send_daily_report_to_wechat,
        send_error_to_wechat
    ]
    
    # 创建 Agent
    agent = create_agent(
        model=llm,
        system_prompt=cfg.get("sp", "你是一个专业的期货交易分析师。"),
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
    
    return agent
