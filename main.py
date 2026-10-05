from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.spinner import Spinner
from kivy.core.window import Window

from bili_core import BiliCore
from bili_api import BiliAPI
from downloader import Downloader
from formats import FormatChecker
from history import History



Window.clearcolor = (
    1,
    0.45,
    0.65,
    1
)



class BiliPink(App):


    def build(self):

        self.core = BiliCore()

        self.api = BiliAPI()

        self.formatter = FormatChecker()

        self.history = History()

        self.downloader = Downloader(
            self.update_status
        )


        self.current_bv = None



        root = BoxLayout(

            orientation="vertical",

            padding=15,

            spacing=10

        )



        root.add_widget(
            Label(
                text="BiliPink\n哔哩哔哩视频下载器",
                font_size=26,
                size_hint=(1,0.15)
            )
        )



        self.input = TextInput(

            hint_text="输入BV / AV / B站链接",

            multiline=False,

            size_hint=(1,0.1)

        )

        root.add_widget(self.input)



        self.cover = AsyncImage(

            size_hint=(1,0.25)

        )

        root.add_widget(self.cover)



        self.info = Label(

            text="等待解析",

            size_hint=(1,0.25)

        )

        root.add_widget(self.info)



        self.quality = Spinner(

            text="清晰度",

            values=(),

            size_hint=(1,0.1)

        )

        root.add_widget(self.quality)



        self.mode = Spinner(

            text="视频+音频",

            values=(

                "视频+音频",

                "只下载视频",

                "只下载音频"

            ),

            size_hint=(1,0.1)

        )

        root.add_widget(self.mode)



        parse = Button(

            text="解析视频",

            size_hint=(1,0.1)

        )

        parse.bind(
            on_press=self.parse_video
        )

        root.add_widget(parse)



        download = Button(

            text="开始下载",

            size_hint=(1,0.1)

        )

        download.bind(
            on_press=self.download
        )

        root.add_widget(download)



        self.status = Label(

            text="",

            size_hint=(1,0.1)

        )

        root.add_widget(self.status)



        return root





    def update_status(self,text):

        self.status.text=text





    def parse_video(self,btn):


        bv=self.core.convert(

            self.input.text

        )


        if not bv:

            self.status.text="无法识别"

            return



        self.current_bv=bv



        data=self.api.get_info(

            bv

        )


        if data:


            self.cover.source=data["cover"]


            self.info.text=(

                "标题："
                +data["title"]

                +"\nUP主："
                +data["owner"]

                +"\nUID："
                +str(data["uid"])

                +"\n播放："
                +str(data["view"])

                +"\n点赞："
                +str(data["like"])

                +"\n投币："
                +str(data["coin"])

                +"\n收藏："
                +str(data["favorite"])

                +"\n评论："
                +str(data["comment"])

            )



            qualities=self.formatter.get_quality(

                bv

            )


            if qualities:

                self.quality.values=qualities

                self.quality.text=qualities[0]



            self.status.text="解析成功"



        else:

            self.status.text="获取失败"






    def download(self,btn):


        if not self.current_bv:

            self.status.text="请先解析"

            return



        self.status.text="开始下载"



        info=self.downloader.download(

            self.current_bv,

            self.mode.text,

            self.quality.text

        )


        if info:


            self.history.add(

                info,

                "/storage/emulated/0/Download/BiliPink"

            )


        self.status.text="下载完成"





BiliPink().run()
