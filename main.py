# ==========【字体注册，必须放在整个文件最顶部】==========
from kivy.core.text import LabelBase
LabelBase.register(
    name="NotoSansSC",
    fn_regular="NotoSansSC‑Regular.ttf"
)
from kivymd.font_definitions import theme_font_styles
theme_font_styles["H3"]["font_name"] = "NotoSansSC"
theme_font_styles["H6"]["font_name"] = "NotoSansSC"
theme_font_styles["Body1"]["font_name"] = "NotoSansSC"
theme_font_styles["Body2"]["font_name"] = "NotoSansSC"
theme_font_styles["Caption"]["font_name"] = "NotoSansSC"
# ======================================================

from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.imagery import AsyncImage
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import mainthread
import threading
import os
import time

# 导入业务模块
from bili_core import BiliCore
from downloader import Downloader


KV = """

MDScreen:

    md_bg_color:"#FFF5F8"


    MDBoxLayout:

        orientation:"vertical"
        padding:12
        spacing:10


        MDCard:

            size_hint_y:None
            height:110

            radius:[25,25,25,25]

            md_bg_color:"#FB7299"


            MDBoxLayout:

                orientation:"vertical"
                padding:15


                MDLabel:

                    text:"BiliPink"

                    font_style:"H3"

                    theme_text_color:"Custom"

                    text_color:"#FFFFFF"



                MDLabel:

                    text:"哔哩哔哩视频下载器"

                    theme_text_color:"Custom"

                    text_color:"#FFFFFF"





        ScrollView:
            size_hint_y: 1
            MDBoxLayout:
                orientation:"vertical"
                spacing:15
                size_hint_y: None
                height: self.minimum_height


                MDCard:

                    radius:[20]
                    padding:15


                    MDBoxLayout:

                        orientation:"vertical"
                        spacing:10


                        MDTextField:
                            id:url
                            hint_text:"输入 BV / AV / b23短链接"

                        MDRaisedButton:
                            text:"🔍 解析视频"
                            md_bg_color:"#FB7299"
                            pos_hint:{"center_x":0.5}
                            on_press: app.on_click_parse()


                MDCard:
                    radius:[20]
                    padding:15

                    MDBoxLayout:
                        orientation:"vertical"
                        spacing:8

                        MDLabel:
                            text:"🎬 视频信息"
                            font_style:"H6"

                        AsyncImage:
                            id:cover
                            size_hint_y:None
                            height:180
                            allow_stretch:True
                            keep_ratio:True

                        MDLabel:
                            id:title
                            text:"标题: 等待解析"

                        MDLabel:
                            id:up
                            text:"UP主:"

                        MDLabel:
                            id:uid
                            text:"UID:"

                        MDLabel:
                            id:bvid
                            text:"BV号:"

                        MDLabel:
                            id:aid
                            text:"AV号:"

                        MDLabel:
                            id:cid
                            text:"CID:"


                MDCard:
                    radius:[20]
                    padding:15

                    MDBoxLayout:
                        orientation:"vertical"
                        spacing:8

                        MDLabel:
                            text:"📊 数据统计"
                            font_style:"H6"

                        MDLabel:
                            id:stats
                            text:"""
播放:
点赞:
投币:
收藏:
评论:
弹幕:
分享:
"""


                MDCard:
                    radius:[20]
                    padding:15

                    MDBoxLayout:
                        orientation:"vertical"

                        MDLabel:
                            text:"📅 视频资料"

                        MDLabel:
                            id:detail
                            text:"""
发布时间:
分区:
类型:
时长:
尺寸:
"""


                MDCard:
                    radius:[20]
                    padding:15

                    MDBoxLayout:
                        orientation:"vertical"

                        MDLabel:
                            text:"⚙ 下载设置"
                            font_style:"H6"

                        MDLabel:
                            text:"清晰度"

                        MDRaisedButton:
                            id:quality_btn
                            text:"选择清晰度"
                            pos_hint:{"center_x":0.5}
                            on_press: app.open_quality_menu()

                        MDLabel:
                            text:"编码格式"

                        MDLabel:
                            id:codec
                            text:"AVC / HEVC / AV1"

                        MDLabel:
                            text:"音质"

                        MDRaisedButton:
                            id:audio_btn
                            text:"320K"
                            pos_hint:{"center_x":0.5}
                            on_press: app.open_audio_menu()

                        MDLabel:
                            text:"下载类型"

                        MDLabel:
                            text:"""
🎬 视频

🎵 音频

📦 MP4
"""


                MDCard:
                    radius:[20]
                    padding:15

                    MDBoxLayout:
                        orientation:"vertical"

                        MDLabel:
                            text:"🚀 下载状态"
                            font_style:"H6"

                        MDProgressBar:
                            id:progress

                        MDLabel:
                            id:status
                            text:"""
等待下载...

速度:
剩余:
保存位置:
"""


                MDRaisedButton:
                    text:"⬇ 开始下载"
                    md_bg_color:"#FB7299"
                    pos_hint:{"center_x":0.5}
                    on_press: app.on_click_download()

                MDRaisedButton:
                    text:"📂 下载历史"
                    pos_hint:{"center_x":0.5}
                    on_press: app.on_click_history()

"""


class BiliPink(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Pink"
        self.bili_core = BiliCore()
        self.downloader = Downloader()

        self.video_data = None
        self.selected_quality = None
        self.selected_audio = None
        self.quality_list = []
        self.audio_list = None

        self.menu_quality = None
        self.menu_audio = None

        self.download_running = False
        return Builder.load_string(KV)

    def on_click_parse(self):
        input_text = self.root.ids.url.text.strip()
        if not input_text:
            self.root.ids.status.text = "请输入 BV / AV / b23链接"
            return
        self.root.ids.status.text = "解析中，请稍候..."
        threading.Thread(target=self.parse_task, args=(input_text,), daemon=True).start()

    def parse_task(self, url):
        try:
            info = self.bili_core.get_video_full_info(url)
            self.set_info_ui(info)
        except Exception as err:
            self.parse_failed(str(err))

    @mainthread
    def set_info_ui(self, info):
        if not info:
            self.root.ids.status.text = "解析失败！检查链接或网络"
            return
        self.video_data = info
        self.quality_list = info["quality_list"]
        self.audio_list = info["audio_list"]

        self.root.ids.cover.source = info["cover"]
        self.root.ids.title.text = f"标题: {info['title']}"
        self.root.ids.up.text = f"UP主: {info['up_name']}"
        self.root.ids.uid.text = f"UID: {info['up_uid']}"
        self.root.ids.bvid.text = f"BV号: {info['bvid']}"
        self.root.ids.aid.text = f"AV号: {info['aid']}"
        self.root.ids.cid.text = f"CID: {info['cid']}"

        self.root.ids.stats.text = f"""
播放: {info['view']}
点赞: {info['like']}
投币: {info['coin']}
收藏: {info['favorite']}
评论: {info['reply']}
弹幕: {info['danmaku']}
分享: {info['share']}
"""
        self.root.ids.detail.text = f"""
发布时间: {info['pubdate']}
分区: {info['tname']}
类型: 普通视频
时长: {info['duration_str']}
尺寸: {info['resolution']}
"""
        self.root.ids.codec.text = info.get("codec_text","AVC / HEVC / AV1")
        self.root.ids.status.text = "✅解析成功，请选择清晰度、音质后下载"

    @mainthread
    def parse_failed(self, msg):
        self.root.ids.status.text = f"❌解析错误：{msg}"

    def open_quality_menu(self):
        if not self.video_data:
            self.root.ids.status.text = "请先解析视频！"
            return
        items = []
        for q in self.quality_list:
            items.append({
                "text": q["name"],
                "on_press": lambda x=q: self.select_quality(x)
            })
        self.menu_quality = MDDropdownMenu(caller=self.root.ids.quality_btn, items=items, width_mult=4)
        self.menu_quality.open()

    def select_quality(self, item):
        self.selected_quality = item
        self.root.ids.quality_btn.text = item["name"]
        self.menu_quality.dismiss()

    def open_audio_menu(self):
        if not self.video_data:
            self.root.ids.status.text = "请先解析视频！"
            return
        items = []
        for a in self.audio_list:
            items.append({
                "text": a["name"],
                "on_press": lambda x=a: self.select_audio(x)
            })
        self.menu_audio = MDDropdownMenu(caller=self.root.ids.audio_btn, items=items, width_mult=4)
        self.menu_audio.open()

    def select_audio(self, item):
        self.selected_audio = item
        self.root.ids.audio_btn.text = item["name"]
        self.menu_audio.dismiss()

    def download_progress_callback(self, current, total, speed_bps, save_path):
        pct = (current / total)*100 if total>0 else 0
        speed_kb = speed_bps / 1024
        remain_sec = ((total‑current)/speed_bps) if speed_bps>0 else 0
        self.update_download_ui(pct, speed_kb, remain_sec, save_path)

    @mainthread
    def update_download_ui(self, percent, speed_kb, remain_sec, save_path):
        self.root.ids.progress.value = percent
        self.root.ids.status.text = f"""
下载中 {percent:.1f}%

速度: {speed_kb:.1f} KB/s
剩余: {int(remain_sec)}秒
保存位置: {save_path}
"""

    @mainthread
    def download_finish_ui(self, ok, filepath):
        self.download_running = False
        self.root.ids.progress.value = 100 if ok else 0
        if ok:
            self.root.ids.status.text = f"✅下载完成\n{filepath}"
        else:
            self.root.ids.status.text = "❌下载失败"

    def on_click_download(self):
        if self.download_running:
            self.root.ids.status.text = "正在下载，请勿重复点击"
            return
        if not self.video_data:
            self.root.ids.status.text = "请先解析视频！"
            return
        if not self.selected_quality or not self.selected_audio:
            self.root.ids.status.text = "请选择清晰度和音质！"
            return

        self.download_running = True
        self.root.ids.status.text = "开始启动下载任务..."
        self.root.ids.progress.value = 0

        def dl_thread():
            try:
                # 文件名格式：标题[AVxxx][BVxxx]
                title = self.video_data["title"].replace("/","_").replace("\\","_").replace(":","_")
                fn_name = f"{title}[AV{self.video_data['aid']}][{self.video_data['bvid']}]"

                ok, out_file = self.downloader.download_by_info(
                    video_info=self.video_data,
                    quality_item=self.selected_quality,
                    audio_item=self.selected_audio,
                    base_filename=fn_name,
                    progress_cb=self.download_progress_callback
                )
                self.download_finish_ui(ok, out_file)
            except Exception as e:
                self.download_finish_ui(False, str(e))

        threading.Thread(target=dl_thread, daemon=True).start()

    def on_click_history(self):
        self.root.ids.status.text = "📂下载历史功能待后续扩展"


if __name__ == "__main__":
    try:
        BiliPink().run()
    except Exception as e:
        import traceback
        traceback.print_exc()
