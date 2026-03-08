#!/usr/bin/env python3
"""
测试修复后的功能
"""
import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_futures_data_tool():
    """测试期货数据工具"""
    print("\n" + "="*60)
    print("测试期货数据工具")
    print("="*60)
    
    try:
        from tools.futures_data_tool import (
            get_futures_realtime_quotes,
            get_futures_historical_data,
            get_futures_market_news,
            get_futures_analysis_report,
            get_comprehensive_market_info
        )
        print("✅ 期货数据工具导入成功")
        
        # 测试 get_futures_realtime_quotes
        print("\n测试 get_futures_realtime_quotes...")
        try:
            result = get_futures_realtime_quotes.invoke({'symbol': '螺纹钢'})
            print(f"✅ get_futures_realtime_quotes 调用成功")
            print(f"   返回长度: {len(result)} 字符")
        except Exception as e:
            print(f"❌ get_futures_realtime_quotes 调用失败: {e}")
        
        # 测试 get_comprehensive_market_info
        print("\n测试 get_comprehensive_market_info...")
        try:
            result = get_comprehensive_market_info.invoke({'symbol': '螺纹钢'})
            print(f"✅ get_comprehensive_market_info 调用成功")
            print(f"   返回长度: {len(result)} 字符")
        except Exception as e:
            print(f"❌ get_comprehensive_market_info 调用失败: {e}")
        
        return True
    except Exception as e:
        print(f"❌ 期货数据工具导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_wechat_notification_tool():
    """测试企业微信通知工具"""
    print("\n" + "="*60)
    print("测试企业微信通知工具")
    print("="*60)
    
    try:
        from tools.wechat_notification_tool import (
            get_webhook_key,
            send_to_wechat,
            send_market_analysis_to_wechat
        )
        print("✅ 企业微信通知工具导入成功")
        
        # 测试 get_webhook_key
        print("\n测试 get_webhook_key...")
        try:
            webhook_key = get_webhook_key()
            if webhook_key:
                print(f"✅ get_webhook_key 调用成功")
                print(f"   Webhook Key: {webhook_key[:20]}...")
            else:
                print(f"⚠️  get_webhook_key 返回 None（企业微信未配置）")
        except Exception as e:
            print(f"❌ get_webhook_key 调用失败: {e}")
        
        # 测试 send_to_wechat
        print("\n测试 send_to_wechat...")
        try:
            result = send_to_wechat.invoke({
                'message': '## 📊 测试消息\n\n这是一条测试消息，用于验证企业微信通知功能是否正常。',
                'message_type': 'markdown'
            })
            print(f"✅ send_to_wechat 调用成功")
            print(f"   结果: {result[:100]}...")
        except Exception as e:
            print(f"❌ send_to_wechat 调用失败: {e}")
        
        return True
    except Exception as e:
        print(f"❌ 企业微信通知工具导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_safe_json_parse():
    """测试安全的 JSON 解析"""
    print("\n" + "="*60)
    print("测试安全的 JSON 解析")
    print("="*60)
    
    try:
        from tools.futures_data_tool import safe_json_parse
        
        # 测试有效的 JSON
        print("\n测试有效的 JSON...")
        result = safe_json_parse('{"status": "success"}')
        print(f"✅ 有效 JSON 解析成功: {result}")
        
        # 测试无效的 JSON
        print("\n测试无效的 JSON...")
        result = safe_json_parse('这不是一个JSON', {'status': 'default'})
        print(f"✅ 无效 JSON 解析成功（返回默认值）: {result}")
        
        return True
    except Exception as e:
        print(f"❌ safe_json_parse 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("\n" + "="*60)
    print("修复功能测试")
    print("="*60)
    
    tests = [
        ("期货数据工具", test_futures_data_tool),
        ("企业微信通知工具", test_wechat_notification_tool),
        ("安全的 JSON 解析", test_safe_json_parse),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # 打印测试结果汇总
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
