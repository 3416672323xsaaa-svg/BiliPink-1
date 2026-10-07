from pathlib import Path
import threading
import re
import uuid
import json
import requests


class Downloader:
    def __init__(self, save_root: str = None):
        if save_root is None:
            try:
                from kivy.app import App
                app = App.get_running_app()
                save_root = Path(app.user_data_dir) / "Downloads"
            except Exception:
                save_root = Path("./Downloads")

        self.save_root = Path(save_root)
        self.save_root.mkdir(exist_ok=True, parents=True)
        self.running_tasks = {}
        self.api = None

    @staticmethod
    def extract_bv(text: str):
        bv_match = re.search(r"BV[a-zA-Z0-9]{10}", text)
        av_match = re.search(r"av(\d+)", text, re.IGNORECASE)
        if bv_match:
            return bv_match.group(0)
        if av_match:
            return f"av{av_match.group(1)}"
        return None

    @staticmethod
    def clean_filename(name: str) -> str:
        cleaned = re.sub(r'[\/:*?"<>|]', "", name).strip()
        if len(cleaned) > 180:
            cleaned = cleaned[:180]
        return cleaned

    def _download_cover(self, cover_url, save_path):
        try:
            resp = requests.get(cover_url, timeout=12)
            resp.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(resp.content)
            return True
        except Exception:
            return False

    def _download_file(self, url, filepath, callback=None):
        headers = {
            "User‑Agent": "Mozilla/5.0 (Android; Mobile)",
            "Referer": "https://www.bilibili.com"
        }
        resp = requests.get(url, headers=headers, stream=True, timeout=20)
        total_size = int(resp.headers.get('content‑length', 0))
        downloaded_size = 0
        chunk_size = 1024 * 128
        with open(filepath, "wb") as f:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size > 0 and callback:
                        pct = round((downloaded_size / total_size)*100,1)
                        callback(f"下载进度：{pct}%")
        if callback:
            callback("文件分片下载完成")

    def download(self, bv, mode, quality, callback=None):
        """
        bv: BV号
        mode: "视频+音频"/"只下载视频"/"只下载音频"
        quality: 清晰度标识
        callback: 状态回调函数
        return task_id 字符串 / None
        """
        # 延迟导入BiliAPI，避免顶层导入连锁崩溃
        from bili_api import BiliAPI
        if self.api is None:
            self.api = BiliAPI()

        task_id = str(uuid.uuid4())

        def worker():
            try:
                if callback:
                    callback("准备下载任务")
                video_info = self.api.get_info(bv)
                if not video_info:
                    if callback:
                        callback("获取视频信息失败")
                    return None

                out_dir = self.save_root / task_id
                out_dir.mkdir(exist_ok=True)

                title_raw = video_info["title"]
                aid = video_info["aid"]
                cid = video_info["cid"]

                if aid:
                    full_name = f"{title_raw} [{bv}][av{aid}]"
                else:
                    full_name = f"{title_raw} [{bv}]"
                safe_filename = self.clean_filename(full_name)

                meta = {
                    "task_id": task_id,
                    "title": title_raw,
                    "bvid": bv,
                    "aid": aid,
                    "cid": cid
                }
                meta_file = out_dir / "meta.json"
                with open(meta_file, "w", encoding="utf‑8") as f:
                    json.dump(meta, f, ensure_ascii=False, indent=2)

                cover_url = video_info.get("cover")
                if cover_url and callback:
                    callback("保存封面")
                    self._download_cover(cover_url, out_dir / "cover.jpg")

                # 获取音视频直链
                play_data = self.api.get_download_url(bv)
                video_url = play_data["video_urls"].get(str(quality))
                audio_url = play_data["audio_url"]

                if mode in ("视频+音频", "只下载视频") and video_url:
                    self._download_file(video_url, out_dir / f"{safe_filename}.mp4", callback)
                if mode in ("视频+音频", "只下载音频") and audio_url:
                    self._download_file(audio_url, out_dir / f"{safe_filename}.m4a", callback)

                if callback:
                    callback("✅全部下载完成（视频音频分开保存）")

            except Exception as e:
                if callback:
                    callback(f"下载异常：{str(e)}")
            finally:
                if task_id in self.running_tasks:
                    del self.running_tasks[task_id]

        thr = threading.Thread(target=worker, daemon=True)
        self.running_tasks[task_id] = thr
        thr.start()
        return task_id
