import requests
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

KEYWORDS = "德龄与慈禧 秦霄贤 话剧"

def fetch_baidu_news():
    url = f"https://news.baidu.com/ns?word={quote(KEYWORDS)}&tn=news&rn=20"
    r = requests.get(url, headers=HEADERS)
    return "\n\n【百度新闻】\n" + r.text[:2000]

def fetch_weibo():
    url = f"https://s.weibo.com/weibo?q={quote(KEYWORDS)}"
    r = requests.get(url, headers=HEADERS)
    return "\n\n【微博讨论】\n" + r.text[:2000]

def fetch_bilibili():
    url = f"https://search.bilibili.com/all?keyword={quote(KEYWORDS)}"
    r = requests.get(url, headers=HEADERS)
    return "\n\n【B站视频】\n" + r.text[:2000]

def fetch_douban():
    url = f"https://www.douban.com/search?q={quote(KEYWORDS)}"
    r = requests.get(url, headers=HEADERS)
    return "\n\n【豆瓣讨论】\n" + r.text[:2000]

def fetch_all_sources():
    data = ""
    try:
        data += fetch_baidu_news()
        data += fetch_weibo()
        data += fetch_bilibili()
        data += fetch_douban()
    except Exception as e:
        data += f"\n抓取异常: {e}"

    return data
