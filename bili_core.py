# bili_core.py（修复版，不再依赖 bili_input）
import requests
import re

class BiliCore:
    def __init__(self):
        pass

    # AV转BV
    def av_to_bv(self, aid):
        url = (
            "https://api.bilibili.com/"
            "x/web-interface/view"
        )
        try:
            r = requests.get(
                url,
                params={
                    "aid":aid
                },
                timeout=10
            )
            data=r.json()
            if data["code"]==0:
                return data["data"]["bvid"]
        except Exception:
            pass
        return None

    def _parse_input(self,text):
        text = text.strip()
        bv_match = re.search(r"BV([A-Za-z0-9]{10})", text)
        av_match = re.search(r"av(\d+)", text, re.IGNORECASE)
        short_match = re.search(r"b23\.tv/\w+", text)
        if bv_match:
            return {"type":"BV", "value": bv_match.group(0)}
        if av_match:
            return {"type":"AV", "value": av_match.group(1)}
        if short_match:
            return {"type":"SHORT", "value": short_match.group(0)}
        return {"type":None, "value":None}

    def _expand_short(self, short_url):
        try:
            resp = requests.head(f"https://{short_url}", allow_redirects=True, timeout=8)
            return resp.url
        except Exception:
            return None

    # 处理用户输入
    def convert(self,text):
        result = self._parse_input(text)
        if result["type"]=="BV":
            return result["value"]
        if result["type"]=="AV":
            return self.av_to_bv(
                result["value"]
            )
        if result["type"]=="SHORT":
            url=self._expand_short(
                result["value"]
            )
            if url:
                bv=re.search(
                    r'BV[a-zA-Z0-9]+',
                    url
                )
                if bv:
                    return bv.group()
        return None
