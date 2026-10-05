import re
import requests


class BiliInput:

    def extract_url(self, text):

        urls = re.findall(
            r'https?://[^\s]+',
            text
        )

        for url in urls:
            if "bilibili.com" in url or "b23.tv" in url:
                return url

        return None


    def parse(self, text):

        text = text.strip()


        # BV号
        bv = re.search(
            r'BV[a-zA-Z0-9]+',
            text
        )

        if bv:
            return {
                "type": "BV",
                "value": bv.group()
            }


        # AV号
        av = re.search(
            r'av(\d+)',
            text,
            re.I
        )

        if av:
            return {
                "type": "AV",
                "value": av.group(1)
            }


        # 纯数字AV
        if text.isdigit():

            return {
                "type": "AV",
                "value": text
            }


        # 提取链接
        url = self.extract_url(text)

        if url:

            if "b23.tv" in url:

                return {
                    "type": "SHORT",
                    "value": url
                }


            return {
                "type": "URL",
                "value": url
            }


        return {
            "type": "ERROR",
            "value": None
        }



    # 展开b23短链接
    def expand_short(self, url):

        try:

            r = requests.get(
                url,
                allow_redirects=True,
                timeout=10
            )

            return r.url


        except:

            return None
