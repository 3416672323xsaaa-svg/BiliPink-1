from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window


Window.clearcolor = (1, 0.45, 0.65, 1)


class BiliPinkApp(App):

    def build(self):

        root = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        title = Label(
            text="BiliPink 视频下载器",
            font_size=28,
            size_hint=(1,0.15)
        )

        root.add_widget(title)


        self.url_input = TextInput(
            hint_text="输入 BV号 / AV号 / B站链接 / 分享文字",
            multiline=False,
            size_hint=(1,0.12)
        )

        root.add_widget(self.url_input)


        self.info = Label(
            text="等待解析视频信息...",
            size_hint=(1,0.4)
        )

        root.add_widget(self.info)


        button = Button(
            text="解析视频",
            size_hint=(1,0.15)
        )

        button.bind(
            on_press=self.parse_video
        )

        root.add_widget(button)


        download = Button(
            text="开始下载",
            size_hint=(1,0.15)
        )

        root.add_widget(download)


        return root


    def parse_video(self, instance):

        text = self.url_input.text

        if text:

            self.info.text = (
                "检测到输入:\n"
                + text
                + "\n\n"
                "下一步接入B站解析模块"
            )

        else:

            self.info.text = "请输入视频地址"


BiliPinkApp().run()
