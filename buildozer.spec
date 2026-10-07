import os
import requests

class Downloader:
    def __init__(self, save_root=None):
        # 安卓默认保存路径：应用私有目录
        if save_root is None:
            self.save_root = "./"
        else:
            self.save_root = save_root
        self.callback = None

    def download(self, bv, mode, quality, callback=None):
        self.callback = callback
        # 这里只做下载逻辑，视频/音频url由bili_api提前解析出来
        try:
            video_info = self._get_video_info(bv)
            title = video_info["title"]
            av = video_info["aid"]
            bvid = video_info["bvid"]
            # 文件名：标题[AVxxxx][BVxxxx]
            safe_title = self._clean_filename(title)
            filename = f"{safe_title}[AV{av}][{bvid}]"

            video_url = None
            audio_url = None
            if mode == "视频+音频" or mode == "只下载视频":
                video_url = video_info["video_urls"][quality]
            if mode == "视频+音频" or mode == "只下载音频":
                audio_url = video_info["audio_url"]

            # 开始分片下载
            if video_url:
                self._download_file(video_url, os.path.join(self.save_root, filename + ".mp4"))
            if audio_url:
                self._download_file(audio_url, os.path.join(self.save_root, filename + ".m4a"))
            return filename
        except Exception as e:
            if self.callback:
                self.callback(f"下载失败：{str(e)}")
            return None

    def _get_video_info(self, bv):
        # 交由bili_api获取真实音视频链接，这里只做中转
        from bili_api import BiliAPI
        api = BiliAPI()
        return api.get_download_url(bv)

    def _clean_filename(self, name):
        # 清理文件名非法字符
        invalid_chars = r'\/:*?"<>|'
        for c in invalid_chars:
            name = name.replace(c, "_")
        return name

    def _download_file(self, url, filepath):
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bilibili.com"
        }
        resp = requests.get(url, headers=headers, stream=True)
        total_size = int(resp.headers.get('content-length', 0))
        downloaded_size = 0
        chunk_size = 1024*256
        with open(filepath, "wb") as f:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size > 0 and self.callback:
                        percent = round(downloaded_size / total_size * 100, 2)
                        self.callback(f"下载进度：{percent}%")
        if self.callback:
            self.callback("文件下载完成")[app]

title = BiliPink
package.name = bilipink
package.domain = org.bilipink

source.dir = .
source.include_exts = py,png,jpg,jpeg,json,kv

version = 1.0
requirements = python3,kivy,requests
p4a.pip_install = yt‑dlp

entrypoint = main.py

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_MEDIA_VIDEO,READ_MEDIA_IMAGES
android.permissions_api33plus = INTERNET,READ_MEDIA_VIDEO,READ_MEDIA_IMAGES

android.accept_sdk_license = True
android.api = 33
android.minapi = 21

android.ndk = 25b
android.sdk = 33

android.archs = arm64‑v8a
p4a.bootstrap = sdl2

android.gradle_download = https://services.gradle.org/distributions/gradle‑7.6.4‑all.zip
android.gradle_plugin = 7.4.2
p4a.gradle_options = ‑Dorg.gradle.java.home=$JAVA_HOME

exclude_patterns = **/test/*,**/tests/*

[buildozer]
log_level = 2
warn_on_root = 1
