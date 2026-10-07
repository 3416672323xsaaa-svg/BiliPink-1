import requests
import time


class BiliAPI:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Android; Mobile)",
            "Referer": "https://www.bilibili.com"
        }

    def get_info(self, bvid):
        url = "https://api.bilibili.com/x/web-interface/view"
        params = {"bvid": bvid}
        try:
            r = requests.get(url, params=params, headers=self.headers, timeout=12)
            data = r.json()
            if data.get("code") != 0:
                print("接口错误:", data.get("message"))
                return None
            video = data["data"]
            stat = video["stat"]
            pub_time_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(video["pubdate"]))
            create_time_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(video["ctime"]))
            copyright_text = "原创" if video["copyright"] == 1 else "转载"
            tag_list = []
            for t in video.get("tags", []):
                tag_list.append(t["tag_name"])
            tags_str = "，".join(tag_list) if tag_list else "无"
            result = {
                "title": video["title"],
                "aid": video["aid"],
                "bvid": video["bvid"],
                "cid": video["cid"],
                "cover": "https:" + video["pic"],
                "desc": video["desc"],
                "pubdate": pub_time_str,
                "ctime": create_time_str,
                "duration": video["duration"],
                "tname": video["tname"],
                "tid": video["tid"],
                "copyright": copyright_text,
                "part_count": video["videos"],
                "tags": tags_str,
                "owner": video["owner"]["name"],
                "uid": video["owner"]["mid"],
                "view": stat["view"],
                "danmaku": stat["danmaku"],
                "reply": stat["reply"],
                "like": stat["like"],
                "coin": stat["coin"],
                "favorite": stat["favorite"],
                "share": stat["share"]
            }
            return result
        except Exception as e:
            print("错误:", e)
            return None

    def get_download_url(self, bvid):
        """获取dash音视频直链，供downloader、formats调用"""
        try:
            page_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
            resp_page = requests.get(page_url, headers=self.headers, timeout=12)
            page_json = resp_page.json()
            cid = page_json["data"]["cid"]

            play_api = f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&qn=112&fnval=4048"
            resp_play = requests.get(play_api, headers=self.headers, timeout=12)
            play_json = resp_play.json()
            play_data = play_json["data"]

            video_urls = {}
            for v_item in play_data["dash"]["video"]:
                qn_key = str(v_item["id"])
                video_urls[qn_key] = v_item["baseUrl"]
            audio_url = play_data["dash"]["audio"][0]["baseUrl"]

            return {
                "video_urls": video_urls,
                "audio_url": audio_url
            }
        except Exception as e:
            print("获取播放链接异常", e)
            return {"video_urls": {}, "audio_url": None}
