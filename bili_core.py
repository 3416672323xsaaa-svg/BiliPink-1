import re
import requests
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Android; Mobile) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Referer": "https://www.bilibili.com/"
}

class BiliCore:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def _extract_bv_av(self, text: str):
        text = text.strip()
        bv_pat = re.compile(r"BV([A-Z0-9a-z]{10})")
        av_pat = re.compile(r"av(\d+)")
        bv_match = bv_pat.search(text)
        av_match = av_pat.search(text)

        if "b23.tv" in text:
            try:
                r = self.session.get(text, allow_redirects=True, timeout=15)
                text = r.url
            except Exception:
                pass

        bvid = bv_match.group(0) if bv_match else None
        aid = int(av_match.group(1)) if av_match else None
        return bvid, aid

    def get_video_full_info(self, input_text: str):
        bvid, aid = self._extract_bv_av(input_text)
        if not bvid and not aid:
            raise ValueError("无法识别BV/AV/b23短链接")

        params = {}
        if bvid:
            params["bvid"] = bvid
        else:
            params["aid"] = aid

        resp = self.session.get(
            "https://api.bilibili.com/x/web-interface/view",
            params=params,
            timeout=20
        )
        js = resp.json()
        if js["code"] != 0:
            raise Exception(f"视频信息接口错误: {js.get('message','未知错误')}")

        data = js["data"]
        stat = data["stat"]
        owner = data["owner"]
        cid = data["cid"]

        play_params = {"bvid": data["bvid"], "cid": cid}
        play_resp = self.session.get(
            "https://api.bilibili.com/x/player/playurl",
            params=play_params,
            timeout=20
        )
        play_js = play_resp.json()
        quality_list = []
        audio_list = []
        codec_text = "-"
        video_streams = {}
        audio_streams = {}

        if play_js.get("code") == 0:
            play_data = play_js["data"]
            accept_quality = play_data.get("accept_quality", [])
            accept_desc = play_data.get("accept_description", [])
            for qid, name in zip(accept_quality, accept_desc):
                quality_list.append({"id": qid, "name": name})

            dash = play_data.get("dash")
            if dash:
                for v in dash.get("video", []):
                    video_streams[v["id"]] = v["baseUrl"]
                for au in dash.get("audio", []):
                    br = au.get("bandwidth",0)
                    name = f"{round(br/1024)}K"
                    audio_streams[au["id"]] = au["baseUrl"]
                    audio_list.append({"id": au["id"], "name": name})
                codecs = {v["codecs"] for v in dash.get("video",[])}
                codec_text = "/".join(sorted(list(codecs)))

        # 无音视频流直接抛出异常
        if len(video_streams) == 0 or len(audio_streams) ==0:
            raise Exception("获取视频流失败，可能为会员视频或地区限制")

        dimension = play_js["data"].get("dimension",{})
        w = dimension.get("width","?")
        h = dimension.get("height","?")
        pub_ts = data["pubdate"]
        pubdate_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(pub_ts))

        result = {
            "title": data["title"],
            "cover": data["pic"],
            "up_name": owner["name"],
            "up_uid": owner["mid"],
            "bvid": data["bvid"],
            "aid": data["aid"],
            "cid": cid,

            "view": stat["view"],
            "like": stat["like"],
            "coin": stat["coin"],
            "favorite": stat["favorite"],
            "reply": stat["reply"],
            "danmaku": stat["danmaku"],
            "share": stat["share"],

            "pubdate": pubdate_str,
            "tname": data["tname"],
            "duration_str": f"{data['duration']//60}:{data['duration']%60:02d}",
            "resolution": f"{w}x{h}",
            "codec_text": codec_text,
            "quality_list": quality_list,
            "audio_list": audio_list,
            "video_streams": video_streams,
            "audio_streams": audio_streams
        }
        return result
