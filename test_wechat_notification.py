"""
测试企业微信通知功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.wechat_notification_tool import send_to_wechat

def test_wechat_notification():
    """测试企业微信通知"""
    print("开始测试企业微信通知...")
    
    # 测试消息
    test_message = """## 🧪 企业微信通知测试

这是一条测试消息，用于验证企业微信通知功能是否正常工作。

**测试内容**:
- Markdown 格式支持
- 粗体文本
- 列表展示
- 表格支持

| 功能 | 状态 |\n|------|------|\n| 文本消息 | ✅ |\n| Markdown | ✅ |\n| 图标支持 | ✅ |

测试时间：2026-03-08

如果收到这条消息，说明企业微信通知功能正常！🎉
"""
    
    try:
        result = send_to_wechat.invoke({
            "message": test_message,
            "message_type": "markdown"
        })
        
        print(f"\n发送结果: {result}")
        
        if "成功" in result:
            print("\n✅ 企业微信通知功能测试成功！")
        else:
            print(f"\n❌ 企业微信通知发送失败: {result}")
            return False
            
        return True
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现异常: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_wechat_notification()
    sys.exit(0 if success else 1)
