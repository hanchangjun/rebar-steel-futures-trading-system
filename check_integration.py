#!/usr/bin/env python3
"""
检查 Vibe Coding 平台集成配置
"""
import sys
import os
import json

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def check_integration_config():
    """检查集成配置"""
    print("="*60)
    print("Vibe Coding 平台集成配置检查")
    print("="*60)

    # 检查环境变量
    print("\n1. 检查环境变量:")
    print("-" * 60)

    env_vars = [
        "COZE_WORKLOAD_IDENTITY_API_KEY",
        "COZE_INTEGRATION_MODEL_BASE_URL",
        "COZE_WORKSPACE_PATH"
    ]

    for var in env_vars:
        value = os.getenv(var)
        if value:
            # 脱敏显示（只显示前后各4个字符）
            masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
            print(f"✅ {var}: {masked}")
        else:
            print(f"❌ {var}: 未设置")

    # 检查企业微信集成
    print("\n2. 检查企业微信集成:")
    print("-" * 60)

    try:
        from coze_workload_identity import Client

        client = Client()
        try:
            credential = client.get_integration_credential('integration-wechat-bot')
            cred_dict = json.loads(credential)

            print(f"✅ 企业微信集成已配置")
            print(f"   Webhook Key: {cred_dict.get('webhook_key', 'N/A')[:20]}...")

            # 检查是否为完整 URL
            webhook_key = cred_dict.get('webhook_key', '')
            if "https" in webhook_key:
                print(f"   配置类型: 完整 URL")
            else:
                print(f"   配置类型: 仅 Key")

        except Exception as e:
            print(f"❌ 企业微信集成未配置")
            print(f"   错误信息: {e}")

    except ImportError:
        print(f"⚠️  coze_workload_identity 模块未安装")
    except Exception as e:
        print(f"❌ 检查企业微信集成时出错: {e}")

    # 检查模型集成
    print("\n3. 检查大模型集成:")
    print("-" * 60)

    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
    if base_url:
        print(f"✅ 模型集成已配置")
        print(f"   Base URL: {base_url}")
    else:
        print(f"❌ 模型集成未配置")

    # 检查 Agent 配置
    print("\n4. 检查 Agent 配置:")
    print("-" * 60)

    try:
        config_path = os.path.join(os.path.dirname(__file__), 'config/agent_llm_config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        print(f"✅ Agent 配置文件存在")
        print(f"   模型: {config.get('config', {}).get('model', 'N/A')}")
        print(f"   温度: {config.get('config', {}).get('temperature', 'N/A')}")
        print(f"   工具数量: {len(config.get('tools', []))}")

    except FileNotFoundError:
        print(f"❌ Agent 配置文件不存在: {config_path}")
    except Exception as e:
        print(f"❌ 读取 Agent 配置失败: {e}")

    print("\n" + "="*60)
    print("检查完成")
    print("="*60)


def test_wechat_integration():
    """测试企业微信集成"""
    print("\n" + "="*60)
    print("测试企业微信集成")
    print("="*60)

    try:
        from coze_workload_identity import Client
        import requests
        import re

        client = Client()

        # 获取 webhook_key
        wechat_bot_credential = client.get_integration_credential("integration-wechat-bot")
        webhook_key = json.loads(wechat_bot_credential)["webhook_key"]

        # 如果是完整 URL，提取 key
        if "https" in webhook_key:
            match = re.search(r"key=([a-zA-Z0-9-]+)", webhook_key)
            if match:
                webhook_key = match.group(1)

        print(f"\n准备发送测试消息...")
        print(f"Webhook Key: {webhook_key[:20]}...")

        # 构造测试消息
        SEND_URL = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
        data = {
            "msgtype": "text",
            "text": {
                "content": "📊 Vibe Coding 平台集成配置测试\n\n✅ 测试成功！企业微信通知功能正常工作。\n\n发送时间: " + __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }

        # 发送消息
        response = requests.post(SEND_URL, json=data, headers={"Content-Type": "application/json"}, timeout=15)
        response.raise_for_status()
        result = response.json()

        if result.get("errcode") == 0:
            print(f"\n✅ 测试消息发送成功！")
            print(f"   请检查企业微信群是否收到消息")
        else:
            print(f"\n❌ 测试消息发送失败")
            print(f"   错误码: {result.get('errcode')}")
            print(f"   错误信息: {result.get('errmsg')}")

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    # 检查配置
    check_integration_config()

    # 询问是否测试企业微信
    print("\n" + "="*60)
    print("是否要测试企业微信集成？")
    print("  输入 'y' 或 'yes' 进行测试")
    print("  输入其他任何内容跳过")
    print("="*60)

    try:
        choice = input("\n请选择: ").strip().lower()
        if choice in ['y', 'yes']:
            test_wechat_integration()
        else:
            print("\n已跳过测试")
    except KeyboardInterrupt:
        print("\n\n已取消")
    except EOFError:
        print("\n\n已跳过测试")


if __name__ == "__main__":
    main()
