import requests
import random
import json
import time
import os
import datetime
from lxml import etree
from fake_useragent import UserAgent

def get_random_ua():  # 随机UA
    ua = UserAgent()
    return ua.random

def load_existing_data():
    # 如果文件存在，加载现有数据
    if os.path.exists("NiHaoWu.json"):
        try:
            with open("NiHaoWu.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_data(data):
    # 保存数据到JSON文件
    with open("NiHaoWu.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def remove_duplicates(data):
    # 去重
    return list(set(data))

def send_to_wechat(content):
    # 获取环境变量
    webhook_key = os.environ.get('WEBHOOK_KEY')

    if not webhook_key:
        print("Warning: Missing WEBHOOK_KEY, skipping WeChat notification")
        return False

    # 定义 URL
    webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"

    # 设置请求头
    webhook_headers = {"Content-Type": "application/json"}

    # 准备 webhook 数据
    webhook_data = {
        "msgtype": "text",
        "text": {"content": content}
    }

    # 发送 webhook 请求
    try:
        response = requests.post(webhook_url, headers=webhook_headers, json=webhook_data)
        print(f"企业微信发送状态: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: 请求失败，状态码 {response.status_code}")
            return False
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error: 发送企业微信请求失败: {str(e)}")
        return False

def main():
    # 获取当前日期时间
    current_datetime = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

    # 加载现有数据
    existing_data = load_existing_data()
    print(f"已加载现有数据 {len(existing_data)} 条")

    url = 'https://www.nihaowua.com/'
    count = 0
    new_data = []
    max_retries = 10  # 最大重试次数

    # 抓取50次
    while count < 50:
        try:
            headers = {
                'User-Agent': get_random_ua()
            }

            retries = 0
            while retries < max_retries:
                try:
                    res = requests.get(url=url, headers=headers, timeout=10)
                    res.encoding = 'utf-8'
                    selector = etree.HTML(res.text)
                    xpath_reg = "//section/div/*/text()"
                    results = selector.xpath(xpath_reg)

                    if results:
                        content = results[0]
                        new_data.append(content)
                        count += 1
                        print(f'********正在爬取中，这是第{count}次爬取********')
                        break
                    else:
                        print("未找到内容，重试...")
                        retries += 1
                except requests.exceptions.RequestException:
                    print(f"请求失败，重试 ({retries}/{max_retries})...")
                    retries += 1

                if retries >= max_retries:
                    print("达到最大重试次数，跳过此次抓取")
                    break

                time.sleep(2)  # 每次抓取间隔2秒

        except Exception as e:
            print(f"发生错误: {e}")
            time.sleep(3)  # 出错后等待时间长一点

    # 统计本次新抓取的数据
    print(f"\n===== 统计信息 =====")
    print(f"本次成功抓取: {len(new_data)} 条数据")

    # 检查新数据中的重复
    unique_new_data = remove_duplicates(new_data)
    new_duplicates = len(new_data) - len(unique_new_data)
    print(f"本次抓取数据中的重复: {new_duplicates} 条")

    # 合并新旧数据
    all_data = existing_data + new_data

    # 去重
    unique_data = remove_duplicates(all_data)
    total_duplicates = len(all_data) - len(unique_data)
    print(f"合并后总数据: {len(all_data)} 条")
    print(f"去重后总数据: {len(unique_data)} 条")
    print(f"总共去除重复: {total_duplicates} 条")

    # 计算新增的唯一数据
    new_unique_count = len(unique_data) - len(existing_data)
    print(f"本次新增唯一数据: {new_unique_count} 条")

    # 保存去重后的数据
    save_data(unique_data)
    print(f"数据已保存到 NiHaoWu.json")

    # 准备发送到企业微信的消息
    wechat_message = f"""数据抓取报告 - {current_datetime}

本次抓取: {len(new_data)} 条
本次数据中重复: {new_duplicates} 条
本次新增唯一数据: {new_unique_count} 条
当前总数据量: {len(unique_data)} 条

GitHub Actions 自动抓取任务已完成！"""

    # 发送到企业微信
    send_to_wechat(wechat_message)

if __name__ == '__main__':
    main()
