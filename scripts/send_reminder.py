import requests
import os
import sys
import datetime

# Get webhook key from environment variables
webhook_key = os.environ.get('WEBHOOK_KEY')
if not webhook_key:
    print("Error: WEBHOOK_KEY not found in environment variables")
    sys.exit(1)

# Get message type from environment variables
message_type = os.environ.get('MESSAGE_TYPE', 'morning')

# Define the webhook URL
url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"

# Set the headers
headers = {
    "Content-Type": "application/json"
}

# Get current date for the message
current_date = datetime.datetime.now().strftime("%Y年%m月%d日")

# Define message content based on message type
if message_type == "morning":
    content = f"早安! 今天是{current_date}，祝你有美好的一天！"
elif message_type == "evening":
    content = f"晚安! {current_date}即将结束，祝你有个好梦！"
else:
    print(f"Error: Unknown message type '{message_type}'")
    sys.exit(1)

# Prepare the data for the request
data = {
    "msgtype": "text",
    "text": {
        "content": content
    }
}

# Send the request
try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    
    if response.status_code != 200:
        print(f"Error: Request failed with status code {response.status_code}")
        sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"Error: Failed to send request: {str(e)}")
    sys.exit(1)

print(f"Successfully sent {message_type} reminder!")