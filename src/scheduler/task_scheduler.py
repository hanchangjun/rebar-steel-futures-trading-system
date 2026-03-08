"""
定时任务管理器
使用 APScheduler 实现定时任务调度
"""
import logging
from typing import Optional, Callable, Any
from datetime import datetime, time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from cozeloop.decorator import observe

logger = logging.getLogger(__name__)


class TaskScheduler:
    """定时任务调度器"""

    def __init__(self):
        """初始化调度器"""
        self.scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")
        self._register_event_listeners()
        logger.info("定时任务调度器已初始化")

    def _register_event_listeners(self):
        """注册事件监听器"""
        def job_executed_listener(event):
            """任务执行成功事件监听器"""
            logger.info(
                f"定时任务执行成功: {event.job_id} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

        def job_error_listener(event):
            """任务执行失败事件监听器"""
            logger.error(
                f"定时任务执行失败: {event.job_id} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Exception: {event.exception}"
            )

        self.scheduler.add_listener(job_executed_listener, EVENT_JOB_EXECUTED)
        self.scheduler.add_listener(job_error_listener, EVENT_JOB_ERROR)

    def start(self):
        """启动调度器"""
        try:
            if not self.scheduler.running:
                self.scheduler.start()
                logger.info("定时任务调度器已启动")
        except Exception as e:
            logger.error(f"定时任务调度器启动失败: {e}")
            raise

    def shutdown(self, wait=True):
        """关闭调度器"""
        if self.scheduler.running:
            self.scheduler.shutdown(wait=wait)
            logger.info("定时任务调度器已关闭")

    def add_cron_job(
        self,
        func: Callable,
        job_id: str,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        day_of_week: Optional[str] = None,
        day: Optional[int] = None,
        **kwargs
    ):
        """
        添加 Cron 定时任务

        Args:
            func: 任务函数
            job_id: 任务ID
            hour: 小时 (0-23)
            minute: 分钟 (0-59)
            day_of_week: 星期几 (0-6, 0=周一, 6=周日) 或 Mon/Tue/Wed/Thu/Fri/Sat/Sun
            day: 日期 (1-31)
            **kwargs: 其他参数
        """
        try:
            trigger = CronTrigger(
                hour=hour,
                minute=minute,
                day_of_week=day_of_week,
                day=day,
                timezone="Asia/Shanghai"
            )
            self.scheduler.add_job(func, trigger, id=job_id, **kwargs)
            logger.info(f"已添加 Cron 定时任务: {job_id} (hour={hour}, minute={minute})")
        except Exception as e:
            logger.error(f"添加 Cron 定时任务失败: {job_id}, 错误: {e}")
            raise

    def add_interval_job(
        self,
        func: Callable,
        job_id: str,
        minutes: Optional[int] = None,
        hours: Optional[int] = None,
        **kwargs
    ):
        """
        添加间隔定时任务

        Args:
            func: 任务函数
            job_id: 任务ID
            minutes: 间隔分钟数
            hours: 间隔小时数
            **kwargs: 其他参数
        """
        try:
            trigger = IntervalTrigger(minutes=minutes, hours=hours, timezone="Asia/Shanghai")
            self.scheduler.add_job(func, trigger, id=job_id, **kwargs)
            logger.info(f"已添加间隔定时任务: {job_id} (minutes={minutes}, hours={hours})")
        except Exception as e:
            logger.error(f"添加间隔定时任务失败: {job_id}, 错误: {e}")
            raise

    def remove_job(self, job_id: str):
        """
        移除定时任务

        Args:
            job_id: 任务ID
        """
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"已移除定时任务: {job_id}")
        except Exception as e:
            logger.error(f"移除定时任务失败: {job_id}, 错误: {e}")
            raise

    def get_jobs(self):
        """
        获取所有任务

        Returns:
            任务列表
        """
        return self.scheduler.get_jobs()

    def pause_job(self, job_id: str):
        """
        暂停任务

        Args:
            job_id: 任务ID
        """
        try:
            self.scheduler.pause_job(job_id)
            logger.info(f"已暂停任务: {job_id}")
        except Exception as e:
            logger.error(f"暂停任务失败: {job_id}, 错误: {e}")
            raise

    def resume_job(self, job_id: str):
        """
        恢复任务

        Args:
            job_id: 任务ID
        """
        try:
            self.scheduler.resume_job(job_id)
            logger.info(f"已恢复任务: {job_id}")
        except Exception as e:
            logger.error(f"恢复任务失败: {job_id}, 错误: {e}")
            raise

    def is_running(self):
        """
        检查调度器是否正在运行

        Returns:
            bool: 是否正在运行
        """
        return self.scheduler.running


# 全局调度器实例
_global_scheduler: Optional[TaskScheduler] = None


def get_scheduler() -> TaskScheduler:
    """
    获取全局调度器实例（单例模式）

    Returns:
        TaskScheduler: 调度器实例
    """
    global _global_scheduler
    if _global_scheduler is None:
        _global_scheduler = TaskScheduler()
    return _global_scheduler


def init_scheduler():
    """
    初始化并启动调度器
    """
    scheduler = get_scheduler()
    if not scheduler.is_running():
        scheduler.start()
        logger.info("定时任务调度器初始化完成")
    return scheduler
