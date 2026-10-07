from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

Window.clearcolor = (1, 0.45, 0.65, 1)


class BiliPink(App):
    def build(self):
        root = BoxLayout(orientation="vertical")
        root.add_widget(Label(text="✅测试成功！APP正常跑起来了", font_size=26))
        return root


if __name__ == "__main__":
    BiliPink().run()
