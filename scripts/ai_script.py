import requests
import os

# 配置
url = "https://aiclound.vip/v1/chat/completions"
api_key = os.getenv("API_KEY")

# 请求头
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {api_key}"
}

data = {
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "帮我写一个python的贪吃蛇"}],
    "stream": False
}

# 发送请求
response = requests.post(url, headers=headers, json=data)

# 输出结果
print(response.json())