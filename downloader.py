from pathlib import Path
import yt_dlp
import threading
import re
import uuid


class Downloader:
    def __init__(self, save_root: str):
        self.save_root = Path(save_root)
        self.save_root.mkdir(exist_ok=True, parents=True)
        self.running_tasks = {}

    @staticmethod
    def extract_bv(text: str):
        """提取BV / av号"""
        bv_match = re.search(r"BV[a-zA-Z0-9]{10}", text)
        av_match = re.search(r"av(\d+)", text, re.IGNORECASE)
        if bv_match:
            return bv_match.group(0)
        if av_match:
            return f"av{av_match.group(1)}"
        return None

    def get_video_info(self, url_or_bv: str):
        """获取视频元信息，不下载"""
        bv = self.extract_bv(url_or_bv)
        if bv:
            target_url = f"https://www.bilibili.com/video/{bv}"
        else:
            target_url = url_or_bv

        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(target_url, download=False)
                return {
                    "ok": True,
                    "title": info.get("title", ""),
                    "duration": info.get("duration", 0),
                    "formats": info.get("formats", [])
                }
        except Exception as e:
            return {"ok": False, "msg": f"解析失败：{str(e)}"}

    def download(self, url_or_bv: str, mode="视频+音频", quality="最高画质", cookiefile=None, callback=None):
        """
        下载入口
        :param url_or_bv: bv/av/完整链接
        :param mode: 视频+音频 / 仅视频 / 仅音频
        :param quality: 最高画质
        :param cookiefile: cookie文件路径 可选
        :param callback: 回调函数 callback(msg_str)
        :return: task_id
        """
        task_id = str(uuid.uuid4())
        bv = self.extract_bv(url_or_bv)
        if bv:
            target_url = f"https://www.bilibili.com/video/{bv}"
        else:
            target_url = url_or_bv

        def _worker():
            try:
                if callback:
                    callback("开始准备下载任务")

                out_dir = self.save_root / task_id
                out_dir.mkdir(exist_ok=True)

                ydl_opts = {
                    "outtmpl": str(out_dir / "%(title)s.%(ext)s"),
                    "quiet": False,
                    "no_warnings": False,
                    "merge_output_format": "mp4",
                }

                if cookiefile and Path(cookiefile).exists():
                    ydl_opts["cookiefile"] = cookiefile

                # 模式选择
                if mode == "仅视频":
                    ydl_opts["format"] = "bestvideo"
                elif mode == "仅音频":
                    ydl_opts["format"] = "bestaudio"
                else:
                    ydl_opts["format"] = "bestvideo+bestaudio/best"

                if callback:
                    callback("开始拉取资源……")

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([target_url])

                if callback:
                    callback("下载完成；注意：APK无ffmpeg，音视频合并会失败，会输出分片文件")

            except Exception as err:
                err_text = str(err)
                if "ffmpeg" in err_text.lower():
                    msg = "ffmpeg合并失败，已下载分片视频音频文件"
                elif "403" in err_text:
                    msg = "B站拒绝访问，可能需要Cookie"
                else:
                    msg = f"下载失败：{err_text}"
                if callback:
                    callback(msg)
            finally:
                if task_id in self.running_tasks:
                    del self.running_tasks[task_id]

        thr = threading.Thread(target=_worker, daemon=True)
        self.running_tasks[task_id] = thr
        thr.start()
        return task_id
