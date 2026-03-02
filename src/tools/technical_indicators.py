"""
技术指标计算工具
用于计算期货交易中常用的技术指标
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
from langchain.tools import tool


@tool
def calculate_ma(data: list[dict], period: int = 20) -> str:
    """
    计算移动平均线 (Moving Average)
    
    Args:
        data: K线数据列表，每个元素包含 'close' 价格
        period: 均线周期，默认为20
    
    Returns:
        包含MA数据的JSON字符串
    """
    df = pd.DataFrame(data)
    
    if 'close' not in df.columns:
        return "错误：数据中缺少 'close' 字段"
    
    df['MA'] = df['close'].rolling(window=period).mean()
    
    # 返回最新的MA值
    latest_ma = df['MA'].iloc[-1] if not pd.isna(df['MA'].iloc[-1]) else None
    latest_close = df['close'].iloc[-1]
    
    result = {
        'indicator': 'MA',
        'period': period,
        'latest_value': float(latest_ma) if latest_ma else None,
        'latest_close': float(latest_close),
        'above_ma': latest_close > latest_ma if latest_ma else False,
        'ma_series': df['MA'].tail(5).tolist()  # 最近5天的MA值
    }
    
    return str(result)


@tool
def calculate_ema(data: list[dict], period: int = 12) -> str:
    """
    计算指数移动平均线 (Exponential Moving Average)
    
    Args:
        data: K线数据列表，每个元素包含 'close' 价格
        period: 均线周期，默认为12
    
    Returns:
        包含EMA数据的JSON字符串
    """
    df = pd.DataFrame(data)
    
    if 'close' not in df.columns:
        return "错误：数据中缺少 'close' 字段"
    
    df['EMA'] = df['close'].ewm(span=period, adjust=False).mean()
    
    latest_ema = df['EMA'].iloc[-1]
    latest_close = df['close'].iloc[-1]
    
    result = {
        'indicator': 'EMA',
        'period': period,
        'latest_value': float(latest_ema),
        'latest_close': float(latest_close),
        'above_ema': latest_close > latest_ema,
        'ema_series': df['EMA'].tail(5).tolist()
    }
    
    return str(result)


@tool
def calculate_macd(data: list[dict], fast_period: int = 12, 
                   slow_period: int = 26, signal_period: int = 9) -> str:
    """
    计算MACD指标 (Moving Average Convergence Divergence)
    
    Args:
        data: K线数据列表，每个元素包含 'close' 价格
        fast_period: 快线周期，默认为12
        slow_period: 慢线周期，默认为26
        signal_period: 信号线周期，默认为9
    
    Returns:
        包含MACD数据的JSON字符串
    """
    df = pd.DataFrame(data)
    
    if 'close' not in df.columns:
        return "错误：数据中缺少 'close' 字段"
    
    # 计算快速和慢速EMA
    ema_fast = df['close'].ewm(span=fast_period, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow_period, adjust=False).mean()
    
    # MACD线
    df['MACD'] = ema_fast - ema_slow
    
    # 信号线
    df['Signal'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()
    
    # 柱状图
    df['Histogram'] = df['MACD'] - df['Signal']
    
    latest_macd = df['MACD'].iloc[-1]
    latest_signal = df['Signal'].iloc[-1]
    latest_histogram = df['Histogram'].iloc[-1]
    prev_histogram = df['Histogram'].iloc[-2] if len(df) > 1 else 0
    
    # 信号判断
    signal = None
    if latest_macd > latest_signal and prev_histogram < 0 and latest_histogram > 0:
        signal = "金叉买入信号"
    elif latest_macd < latest_signal and prev_histogram > 0 and latest_histogram < 0:
        signal = "死叉卖出信号"
    
    result = {
        'indicator': 'MACD',
        'fast_period': fast_period,
        'slow_period': slow_period,
        'signal_period': signal_period,
        'macd': float(latest_macd),
        'signal': float(latest_signal),
        'histogram': float(latest_histogram),
        'trend': '多头' if latest_macd > 0 else '空头',
        'signal': signal
    }
    
    return str(result)


@tool
def calculate_rsi(data: list[dict], period: int = 14) -> str:
    """
    计算RSI指标 (Relative Strength Index)
    
    Args:
        data: K线数据列表，每个元素包含 'close' 价格
        period: RSI周期，默认为14
    
    Returns:
        包含RSI数据的JSON字符串
    """
    df = pd.DataFrame(data)
    
    if 'close' not in df.columns:
        return "错误：数据中缺少 'close' 字段"
    
    if len(df) < period + 1:
        return f"错误：数据不足，至少需要 {period + 1} 条数据"
    
    # 计算价格变化
    delta = df['close'].diff()
    
    # 计算上涨和下跌
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # 计算平均上涨和下跌
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    # 计算RSI
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    latest_rsi = df['RSI'].iloc[-1]
    
    # 信号判断
    signal = None
    if latest_rsi > 70:
        signal = "超买，考虑卖出"
    elif latest_rsi < 30:
        signal = "超卖，考虑买入"
    elif latest_rsi > 50:
        signal = "强势区域"
    else:
        signal = "弱势区域"
    
    result = {
        'indicator': 'RSI',
        'period': period,
        'latest_value': float(latest_rsi) if not pd.isna(latest_rsi) else None,
        'signal': signal,
        'overbought': latest_rsi > 70 if not pd.isna(latest_rsi) else False,
        'oversold': latest_rsi < 30 if not pd.isna(latest_rsi) else False,
        'rsi_series': df['RSI'].tail(5).tolist()
    }
    
    return str(result)


@tool
def calculate_kdj(data: list[dict], n: int = 9, m1: int = 3, m2: int = 3) -> str:
    """
    计算KDJ指标 (Stochastic Oscillator)
    
    Args:
        data: K线数据列表，每个元素包含 'high', 'low', 'close' 价格
        n: 周期，默认为9
        m1: K值平滑系数，默认为3
        m2: D值平滑系数，默认为3
    
    Returns:
        包含KDJ数据的JSON字符串
    """
    df = pd.DataFrame(data)
    
    if not all(col in df.columns for col in ['high', 'low', 'close']):
        return "错误：数据中缺少 'high', 'low', 'close' 字段"
    
    if len(df) < n:
        return f"错误：数据不足，至少需要 {n} 条数据"
    
    # 计算RSV
    low_list = df['low'].rolling(window=n).min()
    high_list = df['high'].rolling(window=n).max()
    
    # 避免除以零
    denominator = high_list - low_list
    denominator = denominator.replace(0, np.nan)
    
    rsv = (df['close'] - low_list) / denominator * 100
    rsv = rsv.fillna(50)  # 如果分母为0，设为50
    
    # 计算K、D、J值
    df['K'] = rsv.ewm(com=m1 - 1, adjust=False).mean()
    df['D'] = df['K'].ewm(com=m2 - 1, adjust=False).mean()
    df['J'] = 3 * df['K'] - 2 * df['D']
    
    latest_k = df['K'].iloc[-1]
    latest_d = df['D'].iloc[-1]
    latest_j = df['J'].iloc[-1]
    
    # 信号判断
    signal = None
    if latest_k > 80 and latest_d > 80:
        signal = "超买，考虑卖出"
    elif latest_k < 20 and latest_d < 20:
        signal = "超卖，考虑买入"
    elif latest_k > latest_d and df['K'].iloc[-2] <= df['D'].iloc[-2]:
        signal = "K线上穿D线，买入信号"
    elif latest_k < latest_d and df['K'].iloc[-2] >= df['D'].iloc[-2]:
        signal = "K线下穿D线，卖出信号"
    
    result = {
        'indicator': 'KDJ',
        'n': n,
        'k_value': float(latest_k),
        'd_value': float(latest_d),
        'j_value': float(latest_j),
        'signal': signal,
        'overbought': latest_k > 80,
        'oversold': latest_k < 20
    }
    
    return str(result)


@tool
def calculate_bollinger_bands(data: list[dict], period: int = 20, 
                              std_dev: float = 2.0) -> str:
    """
    计算布林线指标 (Bollinger Bands)
    
    Args:
        data: K线数据列表，每个元素包含 'close' 价格
        period: 周期，默认为20
        std_dev: 标准差倍数，默认为2.0
    
    Returns:
        包含布林线数据的JSON字符串
    """
    df = pd.DataFrame(data)
    
    if 'close' not in df.columns:
        return "错误：数据中缺少 'close' 字段"
    
    if len(df) < period:
        return f"错误：数据不足，至少需要 {period} 条数据"
    
    # 计算中轨（均线）
    df['Middle'] = df['close'].rolling(window=period).mean()
    
    # 计算标准差
    df['Std'] = df['close'].rolling(window=period).std()
    
    # 计算上轨和下轨
    df['Upper'] = df['Middle'] + (df['Std'] * std_dev)
    df['Lower'] = df['Middle'] - (df['Std'] * std_dev)
    
    latest_close = df['close'].iloc[-1]
    latest_upper = df['Upper'].iloc[-1]
    latest_lower = df['Lower'].iloc[-1]
    latest_middle = df['Middle'].iloc[-1]
    
    # 计算带宽
    bandwidth = (latest_upper - latest_lower) / latest_middle if latest_middle else 0
    
    # 信号判断
    signal = None
    if latest_close > latest_upper:
        signal = "价格突破上轨，可能回调"
    elif latest_close < latest_lower:
        signal = "价格跌破下轨，可能反弹"
    elif bandwidth < 0.1:
        signal = "布林带收窄，注意突破"
    
    position_str = "above_upper" if latest_close > latest_upper else "below_lower" if latest_close < latest_lower else "middle"
    
    result = {
        'indicator': 'Bollinger Bands',
        'period': period,
        'std_dev': std_dev,
        'upper': float(latest_upper),
        'middle': float(latest_middle),
        'lower': float(latest_lower),
        'close': float(latest_close),
        'bandwidth': float(bandwidth),
        'signal': signal,
        'position': position_str
    }
    
    return str(result)


@tool
def analyze_volume(data: list[dict], period: int = 5) -> str:
    """
    分析成交量
    
    Args:
        data: K线数据列表，每个元素包含 'volume' 和 'close' 价格
        period: 平均成交量周期，默认为5
    
    Returns:
        包含成交量分析数据的JSON字符串
    """
    df = pd.DataFrame(data)
    
    if 'volume' not in df.columns:
        return "错误：数据中缺少 'volume' 字段"
    
    # 计算平均成交量
    df['Avg_Volume'] = df['volume'].rolling(window=period).mean()
    
    # 计算成交量比率
    df['Volume_Ratio'] = df['volume'] / df['Avg_Volume']
    
    # 计算价格变化
    df['Price_Change'] = df['close'].pct_change()
    
    latest_volume = df['volume'].iloc[-1]
    latest_avg_volume = df['Avg_Volume'].iloc[-1]
    latest_volume_ratio = df['Volume_Ratio'].iloc[-1]
    latest_price_change = df['Price_Change'].iloc[-1]
    
    # 信号判断
    signal = []
    if latest_volume_ratio > 1.5:
        signal.append("成交量放大")
    elif latest_volume_ratio < 0.7:
        signal.append("成交量萎缩")
    
    if latest_price_change > 0 and latest_volume_ratio > 1.2:
        signal.append("放量上涨，动能强劲")
    elif latest_price_change < 0 and latest_volume_ratio > 1.2:
        signal.append("放量下跌，抛压沉重")
    
    result = {
        'indicator': 'Volume Analysis',
        'period': period,
        'latest_volume': float(latest_volume),
        'avg_volume': float(latest_avg_volume),
        'volume_ratio': float(latest_volume_ratio),
        'price_change': float(latest_price_change * 100) if not pd.isna(latest_price_change) else 0,
        'signal': signal if signal else "成交量正常"
    }
    
    return str(result)


@tool
def calculate_all_indicators(data: list[dict]) -> str:
    """
    计算所有技术指标的综合分析
    
    Args:
        data: K线数据列表，每个元素包含 'open', 'high', 'low', 'close', 'volume'
    
    Returns:
        包含所有指标综合分析的JSON字符串
    """
    if not data:
        return "错误：数据为空"
    
    try:
        # 调用各个指标计算函数
        ma_result = calculate_ma.invoke({'data': data, 'period': 20})
        ema_result = calculate_ema.invoke({'data': data, 'period': 12})
        macd_result = calculate_macd.invoke({'data': data})
        rsi_result = calculate_rsi.invoke({'data': data})
        kdj_result = calculate_kdj.invoke({'data': data})
        bb_result = calculate_bollinger_bands.invoke({'data': data})
        volume_result = analyze_volume.invoke({'data': data})
        
        # 综合信号
        signals = []
        
        # 解析各个指标信号
        if '金叉买入信号' in macd_result:
            signals.append('MACD金叉')
        if '死叉卖出信号' in macd_result:
            signals.append('MACD死叉')
        
        if '超买' in rsi_result:
            signals.append('RSI超买')
        if '超卖' in rsi_result:
            signals.append('RSI超卖')
        
        if 'K线上穿D线' in kdj_result:
            signals.append('KDJ金叉')
        if 'K线下穿D线' in kdj_result:
            signals.append('KDJ死叉')
        
        # 最新价格
        latest_close = float(data[-1]['close']) if 'close' in data[-1] else 0
        
        result = {
            'latest_price': latest_close,
            'MA': ma_result,
            'EMA': ema_result,
            'MACD': macd_result,
            'RSI': rsi_result,
            'KDJ': kdj_result,
            'Bollinger_Bands': bb_result,
            'Volume': volume_result,
            'signals': signals,
            'summary': f"综合信号：{', '.join(signals) if signals else '暂无明显信号'}"
        }
        
        return str(result)
        
    except Exception as e:
        return f"错误：计算指标时发生异常 - {str(e)}"
