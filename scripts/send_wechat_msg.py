#!/usr/bin/env python3
import os
import sys
import pathlib

# Ensure utils module can be imported
script_dir = pathlib.Path(__file__).parent
if script_dir not in sys.path:
    sys.path.append(str(script_dir))

from utils.wechat_tool import send_wechat_message


def main():
    # 从环境变量获取 webhook key
    webhook_key = os.environ.get('WEBHOOK_KEY')
    if not webhook_key:
        print("Error: WEBHOOK_KEY not found in environment variables")
        sys.exit(1)
        
    # 调用工具发送消息
    send_wechat_message(webhook_key, content="hello world from CronHub")


if __name__ == "__main__":
    main()