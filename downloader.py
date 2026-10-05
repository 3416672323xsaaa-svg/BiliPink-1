import yt_dlp
import os
import re


class Downloader:

    def __init__(self, callback=None):
        self.callback = callback

        # APK优先APP私有目录，无需存储权限；Termux/Pydroid降级公共路径
        try:
            from kivy.app import App
            self.path = os.path.join(
                App.get_running_app().user_data_dir,
                "Downloads"
            )
        except Exception:
            self.path = "/storage/emulated/0/Download/BiliPink"

        os.makedirs(self.path, exist_ok=True)

    def send(self, msg):
        if self.callback:
            self.callback(msg)

    def clean_filename(self, name):
        """清理Android非法文件名字符"""
        name = re.sub(r'[\\/:*?"<>|]', "_", name)
        return name.strip()

    def progress(self, d):
        """下载进度钩子，带异常捕获，防止闪退"""
        try:
            status = d.get("status")
            if status == "downloading":
                percent = d.get("_percent_str", "0%")
                speed = d.get("_speed_str", "")
                eta = d.get("_eta_str", "")
                self.send(f"下载中 {percent} {speed} 剩余 {eta}")
            elif status == "finished":
                self.send("下载完成，正在处理...")
            elif status == "error":
                self.send("下载过程发生错误")
        except Exception:
            pass

    def get_info(self, url, cookiefile=None):
        """仅解析元信息，不下载，用于获取标题预览"""
        try:
            options = {
                "quiet": False,
                "no_warnings": False,
                "noplaylist": True,
                "retries": 5
            }
            if cookiefile:
                options["cookiefile"] = cookiefile
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)
            return info
        except Exception as e:
            self.send(f"解析失败:{str(e)}")
            return None

    def download(self, bv_input, mode="视频+音频", quality="最高画质", cookiefile=None):
        # 兼容：输入是完整链接直接用；否则拼接BV地址
        if bv_input.startswith("http"):
            url = bv_input
        else:
            url = "https://www.bilibili.com/video/" + bv_input

        self.send("正在解析...")
        info = self.get_info(url, cookiefile=cookiefile)
        if not info:
            return None

        title = self.clean_filename(info.get("title", "BiliVideo"))
        self.send(f"解析成功:{title}")

        # 清晰度format配置
        if quality == "最高画质":
            fmt = "bestvideo*+bestaudio/best"
        else:
            height = quality.replace("P", "")
            fmt = f"bestvideo*[height<={height}]+bestaudio/best"

        dl_options = {
            "outtmpl": os.path.join(self.path, title + "_%(id)s.%(ext)s"),
            "noplaylist": True,
            "retries": 5,
            "fragment_retries": 5,
            "progress_hooks": [self.progress],
            # =====发布APK的时候改成 True =====
            "quiet": False,
            "no_warnings": False
        }

        if cookiefile:
            dl_options["cookiefile"] = cookiefile

        if mode == "只下载音频":
            dl_options["format"] = "bestaudio"
            dl_options["postprocessors"] = [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}
            ]
        else:
            dl_options["format"] = fmt
            dl_options["merge_output_format"] = "mp4"

        try:
            self.send("开始下载...")
            # 不用process_ie_result，兼容性写法，牺牲一次请求换版本兼容
            with yt_dlp.YoutubeDL(dl_options) as ydl:
                result = ydl.download([url])
            self.send("下载成功")
            return result
        except Exception as e:
            error = str(e)
            if "ffmpeg" in error.lower():
                self.send(f"ffmpeg合并失败:{error}")
            elif "403" in error:
                self.send("B站拒绝访问，可能需要Cookie")
            else:
                self.send(f"下载失败:{error}")
            return None
