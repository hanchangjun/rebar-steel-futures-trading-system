"""
定时任务定义
包含所有需要定时执行的任务
"""
import logging
import json
import os
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from agents.agent import build_agent
from scheduler.task_scheduler import get_scheduler
from coze_coding_utils.runtime_ctx.context import new_context, Context
from langchain_core.messages import HumanMessage
from cozeloop.decorator import observe

logger = logging.getLogger(__name())

# 加载定时任务配置
def load_scheduler_config():
    """加载定时任务配置"""
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, "config/scheduler_config.json")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"定时任务配置加载成功: {config_path}")
        return config
    except FileNotFoundError:
        logger.warning(f"定时任务配置文件不存在: {config_path}，使用默认配置")
        return {"scheduler": {"enabled": True}, "tasks": {}}
    except Exception as e:
        logger.error(f"加载定时任务配置失败: {e}", exc_info=True)
        return {"scheduler": {"enabled": True}, "tasks": {}}

# 加载配置
SCHEDULER_CONFIG = load_scheduler_config()


@observe
async def send_daily_market_analysis_task():
    """
    每日收盘后发送市场分析报告任务
    
    执行时间：每个工作日收盘后（15:30）
    """
    logger.info(f"开始执行每日市场分析任务: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 构建上下文
        ctx = new_context(method="daily_market_analysis")
        
        # 构建 Agent
        agent = build_agent(ctx=ctx)
        
        # 构造分析请求
        prompt = """
        请帮我分析螺纹钢期货的市场状况，并把分析结果推送到企业微信。
        
        分析要求：
        1. 获取最新行情数据
        2. 进行技术指标分析（MA、MACD、RSI、KDJ、布林带等）
        3. 识别买卖信号
        4. 提供交易建议（包括支撑位、压力位、止损止盈、仓位建议）
        5. 强调风险控制和止损纪律
        6. 使用 Markdown 格式输出完整分析报告
        7. 将结果通过企业微信发送
        """
        
        # 调用 Agent
        messages = [HumanMessage(content=prompt)]
        result = await agent.ainvoke({"messages": messages}, config={"configurable": {"thread_id": f"daily_analysis_{datetime.now().strftime('%Y%m%d')}"}})
        
        logger.info(f"每日市场分析任务执行成功: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        logger.error(f"每日市场分析任务执行失败: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, 错误: {e}", exc_info=True)
        raise


@observe
async def send_morning_market_summary_task():
    """
    每日开盘前发送市场摘要任务
    
    执行时间：每个工作日开盘前（8:30）
    """
    logger.info(f"开始执行每日市场摘要任务: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 构建上下文
        ctx = new_context(method="morning_market_summary")
        
        # 构建 Agent
        agent = build_agent(ctx=ctx)
        
        # 构造摘要请求
        prompt = """
        请帮我生成螺纹钢期货的市场摘要，并发送到企业微信。
        
        摘要内容要求：
        1. 昨日收盘价格和涨跌幅
        2. 今日开盘价格
        3. 关键支撑位和压力位
        4. 今日重点关注事项
        5. 风险提示
        6. 使用简洁的 Markdown 格式
        """
        
        # 调用 Agent
        messages = [HumanMessage(content=prompt)]
        result = await agent.ainvoke({"messages": messages}, config={"configurable": {"thread_id": f"morning_summary_{datetime.now().strftime('%Y%m%d')}"}})
        
        logger.info(f"每日市场摘要任务执行成功: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        logger.error(f"每日市场摘要任务执行失败: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, 错误: {e}", exc_info=True)
        raise


@observe
async def monitor_trading_signals_task():
    """
    监控交易信号任务（交易时段每30分钟执行一次）
    
    执行时间：交易时段（9:00-15:00）每30分钟
    """
    logger.info(f"开始执行交易信号监控任务: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 构建上下文
        ctx = new_context(method="monitor_trading_signals")
        
        # 构建 Agent
        agent = build_agent(ctx=ctx)
        
        # 构造监控请求
        prompt = """
        请帮我监控螺纹钢期货的交易信号，如果出现强烈的买入或卖出信号，请及时发送到企业微信。
        
        监控要求：
        1. 获取最新行情数据
        2. 计算技术指标
        3. 检查是否出现重要信号（MACD金叉/死叉、RSI超买超卖、突破压力位/跌破支撑位等）
        4. 如果出现重要信号，立即发送到企业微信
        5. 如果没有重要信号，则不发送消息
        """
        
        # 调用 Agent
        messages = [HumanMessage(content=prompt)]
        result = await agent.ainvoke({"messages": messages}, config={"configurable": {"thread_id": f"signal_monitor_{datetime.now().strftime('%Y%m%d_%H%M')}"}})
        
        logger.info(f"交易信号监控任务执行成功: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        logger.error(f"交易信号监控任务执行失败: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, 错误: {e}", exc_info=True)
        raise


def register_all_tasks(scheduler: AsyncIOScheduler):
    """
    注册所有定时任务
    
    Args:
        scheduler: APScheduler 调度器实例
    """
    # 检查调度器是否启用
    if not SCHEDULER_CONFIG.get("scheduler", {}).get("enabled", True):
        logger.info("定时任务功能已禁用，跳过任务注册")
        return
    
    logger.info("开始注册定时任务...")
    
    tasks_config = SCHEDULER_CONFIG.get("tasks", {})
    
    # 1. 每日收盘后发送市场分析报告（工作日 15:30）
    if tasks_config.get("daily_market_analysis", {}).get("enabled", True):
        cron_config = tasks_config["daily_market_analysis"].get("cron", {})
        scheduler.add_cron_job(
            func=send_daily_market_analysis_task,
            job_id="daily_market_analysis",
            hour=cron_config.get("hour", 15),
            minute=cron_config.get("minute", 30),
            day_of_week=cron_config.get("day_of_week", "mon-fri")
        )
        logger.info(f"已注册: 每日收盘后市场分析报告 (工作日 {cron_config.get('hour', 15)}:{cron_config.get('minute', 30)})")
    
    # 2. 每日开盘前发送市场摘要（工作日 8:30）
    if tasks_config.get("morning_market_summary", {}).get("enabled", True):
        cron_config = tasks_config["morning_market_summary"].get("cron", {})
        scheduler.add_cron_job(
            func=send_morning_market_summary_task,
            job_id="morning_market_summary",
            hour=cron_config.get("hour", 8),
            minute=cron_config.get("minute", 30),
            day_of_week=cron_config.get("day_of_week", "mon-fri")
        )
        logger.info(f"已注册: 每日开盘前市场摘要 (工作日 {cron_config.get('hour', 8)}:{cron_config.get('minute', 30)})")
    
    # 3. 交易时段监控交易信号（工作日 9:00-15:00，每30分钟）
    if tasks_config.get("monitor_trading_signals", {}).get("enabled", True):
        cron_configs = tasks_config["monitor_trading_signals"].get("cron", [])
        for i, cron_config in enumerate(cron_configs):
            scheduler.add_cron_job(
                func=monitor_trading_signals_task,
                job_id=f"monitor_trading_signals_{i}",
                hour=cron_config.get("hour"),
                minute=cron_config.get("minute"),
                day_of_week=cron_config.get("day_of_week", "mon-fri")
            )
        logger.info(f"已注册: 交易信号监控 (工作日每30分钟，共 {len(cron_configs)} 个任务)")
    
    logger.info("所有定时任务注册完成")
    
    # 打印已注册的任务
    jobs = scheduler.get_jobs()
    logger.info(f"已注册 {len(jobs)} 个定时任务:")
    for job in jobs:
        logger.info(f"  - {job.id}: {job.next_run_time}")


def setup_scheduled_tasks():
    """
    设置并启动定时任务
    
    这个函数应该在应用启动时调用
    """
    try:
        # 获取调度器
        scheduler = get_scheduler()
        
        # 注册所有任务
        register_all_tasks(scheduler)
        
        # 启动调度器
        scheduler.start()
        
        logger.info("定时任务设置完成并已启动")
        return scheduler
        
    except Exception as e:
        logger.error(f"设置定时任务失败: {e}", exc_info=True)
        raise
