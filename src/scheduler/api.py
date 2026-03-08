"""
定时任务管理 API
提供定时任务的查询、启动、暂停等管理功能
"""
import logging
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException

from scheduler.task_scheduler import get_scheduler

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/scheduler", tags=["定时任务管理"])


@router.get("/jobs")
async def get_jobs() -> Dict[str, Any]:
    """
    获取所有定时任务列表
    
    Returns:
        任务列表信息
    """
    try:
        scheduler = get_scheduler()
        jobs = scheduler.get_jobs()
        
        job_list = []
        for job in jobs:
            job_list.append({
                "id": job.id,
                "name": job.name,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                "trigger": str(job.trigger),
            })
        
        return {
            "status": "success",
            "total": len(job_list),
            "jobs": job_list
        }
    except Exception as e:
        logger.error(f"获取定时任务列表失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs/{job_id}")
async def get_job_detail(job_id: str) -> Dict[str, Any]:
    """
    获取指定任务详情
    
    Args:
        job_id: 任务ID
    
    Returns:
        任务详情
    """
    try:
        scheduler = get_scheduler()
        job = scheduler.scheduler.get_job(job_id)
        
        if not job:
            raise HTTPException(status_code=404, detail=f"任务不存在: {job_id}")
        
        return {
            "status": "success",
            "job": {
                "id": job.id,
                "name": job.name,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                "trigger": str(job.trigger),
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取任务详情失败: {job_id}, 错误: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/jobs/{job_id}/pause")
async def pause_job(job_id: str) -> Dict[str, Any]:
    """
    暂停指定任务
    
    Args:
        job_id: 任务ID
    
    Returns:
        操作结果
    """
    try:
        scheduler = get_scheduler()
        scheduler.pause_job(job_id)
        
        return {
            "status": "success",
            "message": f"任务已暂停: {job_id}"
        }
    except Exception as e:
        logger.error(f"暂停任务失败: {job_id}, 错误: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/jobs/{job_id}/resume")
async def resume_job(job_id: str) -> Dict[str, Any]:
    """
    恢复指定任务
    
    Args:
        job_id: 任务ID
    
    Returns:
        操作结果
    """
    try:
        scheduler = get_scheduler()
        scheduler.resume_job(job_id)
        
        return {
            "status": "success",
            "message": f"任务已恢复: {job_id}"
        }
    except Exception as e:
        logger.error(f"恢复任务失败: {job_id}, 错误: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/jobs/{job_id}")
async def remove_job(job_id: str) -> Dict[str, Any]:
    """
    删除指定任务
    
    Args:
        job_id: 任务ID
    
    Returns:
        操作结果
    """
    try:
        scheduler = get_scheduler()
        scheduler.remove_job(job_id)
        
        return {
            "status": "success",
            "message": f"任务已删除: {job_id}"
        }
    except Exception as e:
        logger.error(f"删除任务失败: {job_id}, 错误: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_scheduler_status() -> Dict[str, Any]:
    """
    获取调度器状态
    
    Returns:
        调度器状态信息
    """
    try:
        scheduler = get_scheduler()
        
        return {
            "status": "success",
            "running": scheduler.is_running(),
            "job_count": len(scheduler.get_jobs())
        }
    except Exception as e:
        logger.error(f"获取调度器状态失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/trigger/{job_id}")
async def trigger_job(job_id: str) -> Dict[str, Any]:
    """
    手动触发指定任务（立即执行）
    
    Args:
        job_id: 任务ID
    
    Returns:
        操作结果
    """
    try:
        scheduler = get_scheduler()
        scheduler.scheduler.modify_job(job_id, next_run_time=None)
        
        return {
            "status": "success",
            "message": f"任务已触发: {job_id}"
        }
    except Exception as e:
        logger.error(f"触发任务失败: {job_id}, 错误: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# 注册路由到 FastAPI 应用
def register_scheduler_routes(app):
    """
    注册定时任务管理路由到 FastAPI 应用
    
    Args:
        app: FastAPI 应用实例
    """
    app.include_router(router)
    logger.info("定时任务管理路由已注册")
