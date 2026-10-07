class FormatChecker:
    def get_quality(self, bv):
        # 延迟导入，避免顶层导入连锁崩溃
        from bili_api import BiliAPI
        try:
            api = BiliAPI()
            play_info = api.get_download_url(bv)
            video_urls = play_info.get("video_urls", {})
            qualities = []
            # key是qn清晰度数字，B站qn：120=4K,116=2K,112=1080P,96=720P等
            qn_map = {
                "120": "4K",
                "116": "2K",
                "112": "1080P",
                "96": "720P",
                "64": "480P",
                "32": "360P",
                "16": "240P"
            }
            for qn in video_urls.keys():
                name = qn_map.get(qn, f"{qn}")
                qualities.append(name)
            return qualities
        except Exception as e:
            print("清晰度错误:", e)
            return []
