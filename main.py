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
# 修复缺失导入
from kivymd.uix.imagery import AsyncImage
from kivy.clock import mainthread
import threading


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


            MDBoxLayout:


                orientation:"vertical"

                spacing:15

                adaptive_height:True



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

                        # 修复：MDDropDownItem不能直接摆放，替换为按钮用来弹出下拉菜单
                        MDRaisedButton:
                            id:quality_btn
                            text:"选择清晰度"
                            pos_hint:{"center_x":0.5}

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





                MDRaisedButton:

                    text:"📂 下载历史"



"""


class BiliPink(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Pink"
        return Builder.load_string(KV)


if __name__ == "__main__":
    try:
        BiliPink().run()
    except Exception as e:
        print(f"APP异常：{e}")
