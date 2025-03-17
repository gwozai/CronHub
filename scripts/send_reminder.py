import requests
import os
import sys
import datetime

# 获取环境变量
webhook_key = os.environ.get('WEBHOOK_KEY')
ai_api_key = os.environ.get('AI_API_KEY')
message_type = os.environ.get('MESSAGE_TYPE', 'morning')

if not webhook_key or not ai_api_key:
    print("Error: Missing WEBHOOK_KEY or AI_API_KEY")
    sys.exit(1)

# 定义 URL
webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
ai_url = "https://aiclound.vip/v1/chat/completions"

# 设置请求头
webhook_headers = {"Content-Type": "application/json"}
ai_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {ai_api_key}"
}

# 获取当前日期
current_date = datetime.datetime.now().strftime("%Y年%m月%d日")

# 定义 AI 提示词（要求简洁流畅并带健康提醒）
if message_type == "morning":
    prompt = f"生成一句简洁流畅的早安问候，包含日期 {current_date}，语气温暖，末尾加一句简短的健康提醒。"
elif message_type == "evening":
    prompt = f"生成一句简洁流畅的晚安问候，包含日期 {current_date}，语气温馨，末尾加一句简短的健康提醒。"
else:
    print(f"Error: Unknown message type '{message_type}'")
    sys.exit(1)

# 调用 AI API 生成消息
ai_data = {
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": prompt}],
    "stream": False
}

try:
    ai_response = requests.post(ai_url, headers=ai_headers, json=ai_data)
    ai_response.raise_for_status()
    content = ai_response.json()["choices"][0]["message"]["content"].strip()
except requests.exceptions.RequestException as e:
    print(f"Error: Failed to call AI API: {str(e)}")
    sys.exit(1)

# 准备 webhook 数据
webhook_data = {
    "msgtype": "text",
    "text": {"content": content}
}

# 发送 webhook 请求
try:
    response = requests.post(webhook_url, headers=webhook_headers, json=webhook_data)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    if response.status_code != 200:
        print(f"Error: Request failed with status code {response.status_code}")
        sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"Error: Failed to send webhook request: {str(e)}")
    sys.exit(1)

print(f"Successfully sent {message_type} reminder!")