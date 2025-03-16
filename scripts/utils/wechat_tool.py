import requests
import os
import sys
import json


def send_wechat_message(webhook_key, content="hello world"):
    """
    发送企业微信消息的工具函数。
    
    Args:
        webhook_key (str): 企业微信 webhook 的密钥
        content (str): 要发送的消息内容，默认为 "hello world"
        
    Returns:
        tuple: (status_code, response_text) 如果成功
        
    Raises: 
        SystemExit: 如果失败
    """
    if not webhook_key:
        print("Error: WEBHOOK_KEY is empty")
        sys.exit(1)
        
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        if response.status_code != 200:
            print(f"Error: Request failed with status code {response.status_code}")
            sys.exit(1)
            
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to send request: {str(e)}")
        sys.exit(1)