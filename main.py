from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.clock import Clock
import threading

from bili_core import BiliCore
from bili_api import BiliAPI
from downloader import Downloader
from formats import FormatChecker
from history import History


Window.clearcolor = (1, 0.45, 0.65, 1)


class BiliPink(App):

    def build(self):
        self.core = BiliCore()
        self.api = BiliAPI()
        self.formatter = FormatChecker()
        self.history = History()

        self.downloader = Downloader()
        self.current_bv = None

        root = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=8
        )

        root.add_widget(
            Label(
                text="BiliPink\n哔哩哔哩视频下载器",
                font_size=24,
                size_hint=(1, 0.14)
            )
        )

        self.input = TextInput(
            hint_text="输入BV / AV / B站链接",
            multiline=False,
            size_hint=(1, 0.09)
        )
        root.add_widget(self.input)

        self.cover = AsyncImage(
            size_hint=(1, 0.22)
        )
        root.add_widget(self.cover)

        self.info = Label(
            text="等待解析",
            font_size=13,
            size_hint=(1, 0.26)
        )
        root.add_widget(self.info)

        self.quality = Spinner(
            text="清晰度",
            values=(),
            size_hint=(1, 0.09)
        )
        root.add_widget(self.quality)

        self.mode = Spinner(
            text="视频+音频",
            values=(
                "视频+音频",
                "只下载视频",
                "只下载音频"
            ),
            size_hint=(1, 0.09)
        )
        root.add_widget(self.mode)

        parse = Button(
            text="解析视频",
            size_hint=(1, 0.09)
        )
        parse.bind(on_press=self.parse_video)
        root.add_widget(parse)

        download = Button(
            text="开始下载",
            size_hint=(1, 0.09)
        )
        download.bind(on_press=self.download)
        root.add_widget(download)

        self.status = Label(
            text="",
            font_size=12,
            size_hint=(1, 0.09)
        )
        root.add_widget(self.status)

        return root

    def safe_update_status(self, text):
        # 线程安全！子线程更新UI必须扔到Kivy主线程
        Clock.schedule_once(lambda dt: self.update_status(text), 0)

    def update_status(self, text):
        self.status.text = text

    def _parse_worker(self,bv):
        try:
            data = self.api.get_info(bv)
            if data:
                def ui_update(dt):
                    self.cover.source = data["cover"]
                    self.info.text = (
                        f"标题：{data['title']}\n"
                        f"UP主：{data['owner']}\nUID：{data['uid']}\n"
                        f"▶播放:{data['view']} 👍赞:{data['like']}\n"
                        f"🪙币:{data['coin']} ⭐收藏:{data['favorite']}"
                    )
                    qualities = self.formatter.get_quality(bv)
                    if qualities:
                        self.quality.values = qualities
                        self.quality.text = qualities[0]
                    self.safe_update_status("✅解析成功")
                Clock.schedule_once(ui_update,0)
            else:
                self.safe_update_status("❌获取视频信息失败")
        except Exception as e:
            self.safe_update_status(f"解析异常:{str(e)}")

    def parse_video(self, btn):
        bv = self.core.convert(self.input.text.strip())
        if not bv:
            self.safe_update_status("无法识别链接")
            return
        self.current_bv = bv
        self.safe_update_status("🔍正在解析...")
        # 解析网络请求放到后台子线程，防止主线阻塞闪退
        threading.Thread(target=self._parse_worker,args=(bv,),daemon=True).start()

    def _download_worker(self):
        """真正下载跑在后台子线程，不卡死/闪退APP"""
        try:
            task_id = self.downloader.download(
                self.current_bv,
                self.mode.text,
                self.quality.text,
                callback=self.safe_update_status
            )
            if task_id:
                self.history.add(task_id, str(self.downloader.save_root))
                self.safe_update_status("✅下载全部完成")
            else:
                self.safe_update_status("❌下载任务失败")
        except Exception as e:
            self.safe_update_status(f"异常:{str(e)}")

    def download(self, btn):
        if not self.current_bv:
            self.safe_update_status("⚠请先解析视频")
            return
        self.safe_update_status("🔄启动下载任务...")
        # 启动后台线程做下载，**绝对不能主线做网络IO**
        threading.Thread(target=self._download_worker, daemon=True).start()


if __name__ == "__main__":
    BiliPink().run()
