#!/usr/bin/env python3
"""
简单的定时任务功能测试脚本
"""
import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    
    try:
        from scheduler.task_scheduler import get_scheduler
        print("✅ scheduler.task_scheduler 导入成功")
    except Exception as e:
        print(f"❌ scheduler.task_scheduler 导入失败: {e}")
        return False
    
    try:
        from scheduler.api import router
        print("✅ scheduler.api 导入成功")
    except Exception as e:
        print(f"❌ scheduler.api 导入失败: {e}")
        return False
    
    return True


def test_scheduler_creation():
    """测试调度器创建"""
    print("\n测试调度器创建...")
    
    try:
        from scheduler.task_scheduler import get_scheduler
        scheduler = get_scheduler()
        print(f"✅ 调度器创建成功")
        print(f"   运行状态: {scheduler.is_running()}")
        return True
    except Exception as e:
        print(f"❌ 调度器创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_loading():
    """测试配置文件加载"""
    print("\n测试配置文件加载...")
    
    try:
        import json
        config_path = os.path.join(os.path.dirname(__file__), 'config/scheduler_config.json')
        
        if not os.path.exists(config_path):
            print(f"❌ 配置文件不存在: {config_path}")
            return False
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"✅ 配置文件加载成功")
        print(f"   调度器启用: {config.get('scheduler', {}).get('enabled', False)}")
        print(f"   时区: {config.get('scheduler', {}).get('timezone', 'N/A')}")
        print(f"   任务数量: {len(config.get('tasks', {}))}")
        
        return True
    except Exception as e:
        print(f"❌ 配置文件加载失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("="*60)
    print("定时任务功能测试")
    print("="*60)
    
    tests = [
        ("模块导入", test_imports),
        ("调度器创建", test_scheduler_creation),
        ("配置文件加载", test_config_loading),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n总计: {passed}/{total} 通过")
    print("="*60)


if __name__ == "__main__":
    main()
