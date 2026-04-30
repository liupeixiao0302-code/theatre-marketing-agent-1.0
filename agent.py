import time
import hmac
import hashlib
import base64
import requests
from multi_source_fetcher import fetch_all_sources

# 获取 secret 的钉钉机器人的加签密钥
DINGTALK_SECRET = "your_dingtalk_secret"  # 填入你的钉钉 secret

DEEPSEEK_API_KEY = "your_deepseek_api_key"  # 填入 DeepSeek API Key
DINGTALK_WEBHOOK = "your_dingtalk_webhook"  # 填入钉钉 Webhook

# ===== 生成加签 =====
def generate_sign(timestamp):
    """
    计算加签值
    """
    string_to_sign = f"{timestamp}\n{DINGTALK_SECRET}"
    secret = bytes(DINGTALK_SECRET, encoding="utf-8")
    message = bytes(string_to_sign, encoding="utf-8")
    hmac_sign = hmac.new(secret, message, hashlib.sha256).digest()
    sign = base64.b64encode(hmac_sign).decode("utf-8")
    return sign

# ===== 调用 DeepSeek =====
def generate_marketing_report(public_opinion):
    prompt = f"""
你是顶级演出宣发总监，擅长从海量舆情中提炼重点。

下面是从百度新闻、微博、B站、豆瓣抓取的原始网页内容。
这些内容非常杂乱，你需要提炼真正有价值的信息。

请输出：

【1.舆情核心总结】
公众正在讨论什么？

【2.潜在爆点】
哪些内容可能成为传播点？

【3.风险预警】
是否有负面或质疑？

【4.今日宣发动作清单】
必须具体到平台 + 内容类型

【5.可直接发布文案3条】

项目：话剧《德龄与慈禧》

全网原始数据：
{public_opinion}
"""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    return result["choices"][0]["message"]["content"]

# ===== 发送钉钉 =====
def send_to_dingtalk(text):
    """
    发送钉钉消息（加签）
    """
    timestamp = str(int(time.time() * 1000))  # 当前时间戳（毫秒）
    sign = generate_sign(timestamp)

    data = {
        "msgtype": "text",
        "text": {
            "content": f"🎭《德龄与慈禧》宣发Agent日报\n\n{text}"
        }
    }

    webhook_url = f"{DINGTALK_WEBHOOK}&timestamp={timestamp}&sign={sign}"

    response = requests.post(webhook_url, json=data)

    if response.status_code != 200:
        print(f"钉钉消息发送失败：{response.status_code}, {response.text}")
    else:
        print("消息发送成功")

# ===== 主流程 =====
def main():
    print("开始抓取全网舆情...")
    public_opinion = fetch_all_sources()

    print("开始生成宣发报告...")
    report = generate_marketing_report(public_opinion)

    print("发送钉钉...")
    send_to_dingtalk(report)

    print("完成")

if __name__ == "__main__":
    main()
