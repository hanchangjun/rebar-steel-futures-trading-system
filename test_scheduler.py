"""
定时任务测试脚本
用于测试定时任务功能
"""
import asyncio
import logging
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def test_daily_market_analysis():
    """测试每日市场分析任务"""
    logger.info("开始测试每日市场分析任务...")
    
    try:
        from scheduler.tasks import send_daily_market_analysis_task
        await send_daily_market_analysis_task()
        logger.info("✅ 每日市场分析任务测试成功")
    except Exception as e:
        logger.error(f"❌ 每日市场分析任务测试失败: {e}", exc_info=True)


async def test_morning_market_summary():
    """测试每日市场摘要任务"""
    logger.info("开始测试每日市场摘要任务...")
    
    try:
        from scheduler.tasks import send_morning_market_summary_task
        await send_morning_market_summary_task()
        logger.info("✅ 每日市场摘要任务测试成功")
    except Exception as e:
        logger.error(f"❌ 每日市场摘要任务测试失败: {e}", exc_info=True)


async def test_monitor_trading_signals():
    """测试交易信号监控任务"""
    logger.info("开始测试交易信号监控任务...")
    
    try:
        from scheduler.tasks import monitor_trading_signals_task
        await monitor_trading_signals_task()
        logger.info("✅ 交易信号监控任务测试成功")
    except Exception as e:
        logger.error(f"❌ 交易信号监控任务测试失败: {e}", exc_info=True)


async def test_scheduler_initialization():
    """测试调度器初始化"""
    logger.info("开始测试调度器初始化...")
    
    try:
        from scheduler.tasks import setup_scheduled_tasks
        scheduler = setup_scheduled_tasks()
        
        # 检查调度器是否运行
        if scheduler.is_running():
            logger.info("✅ 调度器已成功启动")
        else:
            logger.error("❌ 调度器未启动")
            return False
        
        # 列出所有任务
        jobs = scheduler.get_jobs()
        logger.info(f"已注册 {len(jobs)} 个定时任务:")
        for job in jobs:
            logger.info(f"  - {job.id}: {job.next_run_time}")
        
        return True
    except Exception as e:
        logger.error(f"❌ 调度器初始化失败: {e}", exc_info=True)
        return False


async def test_api_endpoints():
    """测试 API 端点"""
    logger.info("开始测试 API 端点...")
    
    try:
        from scheduler.api import router
        logger.info(f"✅ API 路由已创建: {router.prefix}")
        logger.info(f"可用的 API 端点:")
        for route in router.routes:
            logger.info(f"  - {route.methods} {route.path}")
        return True
    except Exception as e:
        logger.error(f"❌ API 端点测试失败: {e}", exc_info=True)
        return False


async def main():
    """主测试函数"""
    print("\n" + "="*80)
    print("定时任务功能测试")
    print("="*80 + "\n")
    
    tests = [
        ("调度器初始化", test_scheduler_initialization),
        ("API 端点", test_api_endpoints),
        ("每日市场分析任务", test_daily_market_analysis),
        ("每日市场摘要任务", test_morning_market_summary),
        ("交易信号监控任务", test_monitor_trading_signals),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 测试: {test_name}")
        print("-" * 80)
        
        try:
            result = await test_func()
            results.append((test_name, "✅ 通过" if result is None or result else "✅ 通过"))
        except Exception as e:
            results.append((test_name, "❌ 失败"))
            logger.error(f"测试异常: {e}", exc_info=True)
    
    # 打印测试结果汇总
    print("\n" + "="*80)
    print("测试结果汇总")
    print("="*80 + "\n")
    
    for test_name, status in results:
        print(f"{status} {test_name}")
    
    passed = sum(1 for _, status in results if "✅" in status)
    total = len(results)
    
    print(f"\n总计: {passed}/{total} 通过")
    print("="*80 + "\n")
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("⚠️ 部分测试失败，请检查日志")
    
    # 保持调度器运行一段时间
    print("\n调度器将继续运行 10 秒，然后自动退出...")
    await asyncio.sleep(10)
    
    # 关闭调度器
    from scheduler.task_scheduler import get_scheduler
    scheduler = get_scheduler()
    if scheduler.is_running():
        scheduler.shutdown(wait=True)
        print("调度器已关闭")


if __name__ == "__main__":
    print("\n⚠️ 注意：运行测试前请确保：")
    print("  1. 企业微信集成已正确配置")
    print("  2. 相关的 Agent 和工具已正确实现")
    print("  3. 网络连接正常")
    print("\n按 Enter 键继续，或 Ctrl+C 退出...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n测试已取消")
        exit(0)
    
    asyncio.run(main())
