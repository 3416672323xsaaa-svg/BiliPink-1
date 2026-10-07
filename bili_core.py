import re
import requests
import time

HEADERS = {
    "User‑Agent": "Mozilla/5.0 (Android; Mobile) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Referer": "https://www.bilibili.com/"
}

class BiliCore:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def _extract_bv_av(self, text: str):
        """从输入提取 bvid / aid，支持 b23短链接"""
        text = text.strip()
        bv_pat = re.compile(r"BV([A‑Z0‑9a‑z]{10})")
        av_pat = re.compile(r"av(\d+)")
        bv_match = bv_pat.search(text)
        av_match = av_pat.search(text)

        if "b23.tv" in text:
            r = self.session.get(text, allow_redirects=True, timeout=15)
            text = r.url

        bvid = bv_match.group(0) if bv_match else None
        aid = int(av_match.group(1)) if av_match else None
        return bvid, aid

    def get_video_full_info(self, input_text: str):
        bvid, aid = self._extract_bv_av(input_text)
        if not bvid and not aid:
            raise ValueError("无法识别BV/AV/b23链接")

        params = {}
        if bvid:
            params["bvid"] = bvid
        else:
            params["aid"] = aid

        resp = self.session.get(
            "https://api.bilibili.com/x/web‑interface/view",
            params=params,
            timeout=20
        )
        js = resp.json()
        if js["code"] != 0:
            raise Exception(f"接口错误: {js.get('message','unknown')}")

        data = js["data"]
        stat = data["stat"]
        owner = data["owner"]

        # 获取播放流，清晰度列表
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
        codec_text = "‑"

        if play_js.get("code") == 0:
            play_data = play_js["data"]
            accept_quality = play_data.get("accept_quality", [])
            accept_desc = play_data.get("accept_description", [])
            for qid, name in zip(accept_quality, accept_desc):
                quality_list.append({"id": qid, "name": name})

            dash = play_data.get("dash")
            if dash:
                audio_items = dash.get("audio", [])
                for au in audio_items:
                    br = au.get("bandwidth",0)
                    kb = round(br / 1024)
                    audio_list.append({"id": au["id"], "name": f"{kb}K"})
                video_items = dash.get("video",[])
                codecs = {v["codecs"] for v in video_items}
                codec_text = "/".join(sorted(list(codecs)))

        pub_ts = data["pubdate"]
        pubdate_str = time.strftime("%Y‑%m‑%d %H:%M", time.localtime(pub_ts))

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
            "resolution": play_js["data"].get("dimension",{}).get("width","?") + "x" + str(play_js["data"].get("dimension",{}).get("height","?")),
            "codec_text": codec_text,

            "quality_list": quality_list,
            "audio_list": audio_list
        }
        return result
