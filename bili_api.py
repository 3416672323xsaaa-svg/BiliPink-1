import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Referer": "https://www.bilibili.com/"
}

def get_bili_stat(bvid):
    """获取点赞，投币，收藏，播放，评论，弹幕数，UP主mid，分区tname，aid(AV号)"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    data = resp.json()
    if data["code"] != 0:
        return {}
    stat = data["data"]["stat"]
    owner = data["data"]["owner"]
    aid = data["data"]["aid"]
    return {
        "aid": aid,
        "mid": owner["mid"],
        "like": stat["like"],
        "coin": stat["coin"],
        "favorite": stat["favorite"],
        "view": stat["view"],
        "reply": stat["reply"],
        "danmaku": stat["danmaku"],
        "tname": data["data"]["tname"]
    }

def get_bili_cid(bvid):
    """获取cid，用来下载弹幕"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    data = resp.json()
    if data["code"] != 0:
        return {}
    cid = data["data"]["cid"]
    return {"cid": cid}
