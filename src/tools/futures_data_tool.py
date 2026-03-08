"""
期货行情数据获取工具（修复版）
用于获取螺纹钢期货的实时行情和历史数据
"""

import json
import re
from typing import Dict, Any, Optional
from langchain.tools import tool, ToolRuntime
from coze_coding_utils.runtime_ctx.context import new_context
from coze_coding_dev_sdk import SearchClient


def safe_json_parse(text: str, default: Any = None) -> Any:
    """
    安全地解析 JSON 字符串
    
    Args:
        text: 要解析的文本
        default: 解析失败时返回的默认值
    
    Returns:
        解析后的对象或默认值
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return default if default is not None else {"error": "无法解析 JSON", "raw_text": text}


@tool
def get_futures_realtime_quotes(symbol: str = "螺纹钢",
                                contract: Optional[str] = None,
                                runtime: ToolRuntime = None) -> str:
    """
    获取期货实时行情数据
    
    Args:
        symbol: 期货品种名称，默认为"螺纹钢"
        contract: 合约代码（如 RB2505），如果不指定则获取主力合约
    
    Returns:
        包含实时行情数据的JSON字符串
    """
    ctx = runtime.context if runtime else new_context(method="futures_quotes")
    client = SearchClient(ctx=ctx)
    
    # 构建搜索查询
    if contract:
        query = f"{symbol}期货 {contract} 实时行情"
    else:
        query = f"{symbol}期货 主力合约 实时行情"
    
    try:
        response = client.web_search(query=query, count=5, need_summary=True)
        
        if not response.web_items:
            return json.dumps({
                "status": "error",
                "message": "未找到相关行情数据",
                "query": query
            }, ensure_ascii=False)
        
        # 提取关键信息
        results = []
        for item in response.web_items[:3]:
            result = {
                'title': item.title,
                'source': item.site_name,
                'url': item.url,
                'snippet': item.snippet,
                'summary': item.summary if hasattr(item, 'summary') else ""
            }
            results.append(result)
        
        # 尝试从摘要中提取价格信息
        price_info = extract_price_info(query, response.summary if response.summary else "")
        
        output = {
            'status': 'success',
            'query': query,
            'summary': response.summary,
            'price_info': price_info,
            'sources': results,
            'note': '以上数据来源于网络搜索，实际交易请以交易所官方数据为准'
        }
        
        return json.dumps(output, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"获取行情数据失败：{str(e)}",
            "query": query
        }, ensure_ascii=False)


@tool
def get_futures_historical_data(symbol: str = "螺纹钢",
                               contract: str = "RB2505",
                               period: str = "日K",
                               days: int = 30,
                               runtime: ToolRuntime = None) -> str:
    """
    获取期货历史K线数据（通过搜索获取）
    
    Args:
        symbol: 期货品种名称，默认为"螺纹钢"
        contract: 合约代码，默认为"RB2505"
        period: K线周期，如"日K"、"60分钟"、"15分钟"
        days: 历史天数，默认为30
    
    Returns:
        包含历史数据的JSON字符串（注意：由于是通过搜索获取，可能无法获取完整的历史K线数据）
    """
    ctx = runtime.context if runtime else new_context(method="futures_history")
    client = SearchClient(ctx=ctx)
    
    query = f"{symbol}期货 {contract} {period}K线 历史{days}天 数据"
    
    try:
        response = client.web_search(query=query, count=5)
        
        if not response.web_items:
            return json.dumps({
                "status": "error",
                "message": f"未找到 {contract} 的历史数据",
                "query": query
            }, ensure_ascii=False)
        
        results = []
        for item in response.web_items[:3]:
            result = {
                'title': item.title,
                'source': item.site_name,
                'url': item.url,
                'snippet': item.snippet
            }
            results.append(result)
        
        output = {
            'status': 'success',
            'symbol': symbol,
            'contract': contract,
            'period': period,
            'days': days,
            'sources': results,
            'note': '由于通过搜索获取历史数据有限，建议通过专业的期货数据接口获取完整K线数据'
        }
        
        return json.dumps(output, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"获取历史数据失败：{str(e)}",
            "query": query
        }, ensure_ascii=False)


@tool
def get_futures_market_news(symbol: str = "螺纹钢",
                           count: int = 5,
                           runtime: ToolRuntime = None) -> str:
    """
    获取期货市场新闻和资讯
    
    Args:
        symbol: 期货品种名称
        count: 获取新闻数量，默认为5
    
    Returns:
        包含市场新闻的JSON字符串
    """
    ctx = runtime.context if runtime else new_context(method="futures_news")
    client = SearchClient(ctx=ctx)
    
    query = f"{symbol}期货 行情 新闻 最新"
    
    try:
        response = client.web_search(query=query, count=count, time_range="1d")
        
        if not response.web_items:
            return json.dumps({
                "status": "error",
                "message": "未找到相关新闻",
                "query": query
            }, ensure_ascii=False)
        
        news_list = []
        for item in response.web_items:
            news = {
                'title': item.title,
                'source': item.site_name,
                'url': item.url,
                'snippet': item.snippet,
                'publish_time': item.publish_time if hasattr(item, 'publish_time') else None
            }
            news_list.append(news)
        
        output = {
            'status': 'success',
            'symbol': symbol,
            'news_count': len(news_list),
            'news': news_list
        }
        
        return json.dumps(output, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"获取市场新闻失败：{str(e)}",
            "query": query
        }, ensure_ascii=False)


@tool
def get_futures_analysis_report(symbol: str = "螺纹钢",
                               runtime: ToolRuntime = None) -> str:
    """
    获取期货品种的分析报告和研报
    
    Args:
        symbol: 期货品种名称
    
    Returns:
        包含分析报告的JSON字符串
    """
    ctx = runtime.context if runtime else new_context(method="futures_analysis")
    client = SearchClient(ctx=ctx)
    
    query = f"{symbol}期货 分析报告 研报 机构观点"
    
    try:
        response = client.web_search(query=query, count=5, need_summary=True)
        
        if not response.web_items:
            return json.dumps({
                "status": "error",
                "message": "未找到相关分析报告",
                "query": query
            }, ensure_ascii=False)
        
        reports = []
        for item in response.web_items:
            report = {
                'title': item.title,
                'source': item.site_name,
                'url': item.url,
                'snippet': item.snippet,
                'summary': item.summary if hasattr(item, 'summary') else ""
            }
            reports.append(report)
        
        output = {
            'status': 'success',
            'symbol': symbol,
            'report_count': len(reports),
            'summary': response.summary,
            'reports': reports
        }
        
        return json.dumps(output, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"获取分析报告失败：{str(e)}",
            "query": query
        }, ensure_ascii=False)


def extract_price_info(query: str, summary: str) -> Dict[str, Any]:
    """
    从文本中提取价格信息
    
    Args:
        query: 搜索查询
        summary: 搜索摘要
    
    Returns:
        包含价格信息的字典
    """
    price_info = {
        'current_price': None,
        'change': None,
        'change_percent': None,
        'high': None,
        'low': None,
        'volume': None
    }
    
    if not summary:
        return price_info
    
    # 提取当前价格
    price_pattern = r'(\d+\.?\d*)[元吨]?'
    prices = re.findall(pattern=price_pattern, string=summary)
    
    if prices:
        price_info['current_price'] = prices[0] + " 元/吨"
    
    # 提取涨跌额
    change_pattern = r'[涨跌][-+]?(\d+\.?\d*)'
    change = re.search(pattern=change_pattern, string=summary)
    if change:
        price_info['change'] = change.group(0)
    
    # 提取涨跌幅
    percent_pattern = r'[涨跌][-+]?(\d+\.?\d*)%'
    percent = re.search(pattern=percent_pattern, string=summary)
    if percent:
        price_info['change_percent'] = percent.group(0)
    
    return price_info


@tool
def get_comprehensive_market_info(symbol: str = "螺纹钢",
                                  contract: str = None,
                                  runtime: ToolRuntime = None) -> str:
    """
    获取综合市场信息（包括行情、新闻、分析）
    
    Args:
        symbol: 期货品种名称
        contract: 合约代码（可选）
    
    Returns:
        包含综合市场信息的JSON字符串
    """
    try:
        # 获取实时行情
        quotes_result = get_futures_realtime_quotes.invoke({
            'symbol': symbol,
            'contract': contract,
            'runtime': runtime
        })
        quotes = safe_json_parse(quotes_result, {"status": "error", "message": "无法获取行情数据"})
        
        # 获取市场新闻
        news_result = get_futures_market_news.invoke({
            'symbol': symbol,
            'count': 3,
            'runtime': runtime
        })
        news = safe_json_parse(news_result, {"status": "error", "message": "无法获取新闻"})
        
        # 获取分析报告
        analysis_result = get_futures_analysis_report.invoke({
            'symbol': symbol,
            'runtime': runtime
        })
        analysis = safe_json_parse(analysis_result, {"status": "error", "message": "无法获取分析报告"})
        
        output = {
            'status': 'success',
            'symbol': symbol,
            'contract': contract,
            'quotes': quotes,
            'news': news,
            'analysis': analysis,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'note': '以上数据来源于网络搜索，实际交易请以交易所官方数据为准'
        }
        
        return json.dumps(output, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"获取综合市场信息失败：{str(e)}",
            "symbol": symbol,
            "contract": contract
        }, ensure_ascii=False)
