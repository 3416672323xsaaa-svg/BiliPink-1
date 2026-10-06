from pathlib import Path
import yt_dlp
import threading
import re
import uuid
import json
import requests

from bili_api import get_bili_stat, get_bili_cid


class Downloader:
    def __init__(self, save_root: str = None):
        # 如果没有传入路径，自动使用Kivy APP私有目录（安卓高版本安全，不需要存储权限）
        if save_root is None:
            try:
                from kivy.app import App
                app = App.get_running_app()
                save_root = Path(app.user_data_dir) / "Downloads"
            except Exception:
                # 兜底，本地电脑运行场景
                save_root = Path("./Downloads")

        self.save_root = Path(save_root)
        self.save_root.mkdir(exist_ok=True, parents=True)
        self.running_tasks = {}

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
        # 清除安卓禁止的文件名字符：\/:*?"<>|
        cleaned = re.sub(r'[\/:*?"<>|]', "", name).strip()
        # 限制总长度，防止文件名过长报错
        if len(cleaned) > 180:
            cleaned = cleaned[:180]
        return cleaned

    def get_video_info(self, url_or_bv: str):
        """解析视频全部信息，APK打包稳定"""
        bv = self.extract_bv(url_or_bv)
        if not bv:
            return {"ok": False, "msg": "无法识别BV/AV号"}
        target_url = f"https://www.bilibili.com/video/{bv}"
        try:
            ydl_opts = {"quiet": True, "no_warnings": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(target_url, download=False)
            stat_data = get_bili_stat(bv)
            cid_data = get_bili_cid(bv)

            return {
                "ok": True,
                "title": info.get("title", ""),
                "description": info.get("description", ""),
                "uploader": info.get("uploader", ""),
                "upload_date": info.get("upload_date", ""),
                "duration": info.get("duration", 0),
                "thumbnail": info.get("thumbnail"),
                "formats": info.get("formats", []),
                "webpage_url": info.get("webpage_url", ""),
                "bvid": bv,
                "aid": stat_data.get("aid"),
                "mid": stat_data.get("mid", ""),
                "like": stat_data.get("like", 0),
                "coin": stat_data.get("coin", 0),
                "favorite": stat_data.get("favorite", 0),
                "view": stat_data.get("view", 0),
                "reply": stat_data.get("reply", 0),
                "danmaku": stat_data.get("danmaku", 0),
                "tname": stat_data.get("tname", ""),
                "cid": cid_data.get("cid", None)
            }
        except Exception as e:
            return {"ok": False, "msg": f"解析失败：{str(e)}"}

    def _download_cover(self, cover_url, save_path):
        try:
            resp = requests.get(cover_url, timeout=12)
            resp.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(resp.content)
            return True
        except Exception:
            return False

    def _download_danmaku(self, cid, save_path):
        if not cid:
            return False
        try:
            resp = requests.get(f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}", timeout=12)
            resp.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(resp.content)
            return True
        except Exception:
            return False

    def download(self, url_or_bv: str, mode="视频+音频", quality="最高画质", cookiefile=None, callback=None):
        """
        callback回调：
        字符串：普通文本消息
        dict {"type":"download_progress","percent":xx,"msg":"xxx"} 下载进度
        """
        task_id = str(uuid.uuid4())
        bv = self.extract_bv(url_or_bv)
        target_url = f"https://www.bilibili.com/video/{bv}" if bv else url_or_bv

        def ydl_progress_hook(d):
            if callback is None:
                return
            if d["status"] == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate")
                downloaded = d.get("downloaded_bytes", 0)
                if total:
                    pct = round((downloaded / total) * 100, 1)
                    callback({"type": "download_progress", "percent": pct, "msg": f"下载 {pct}%"})
            elif d["status"] == "finished":
                callback({"type": "download_progress", "percent": 100, "msg":"分片下载完成"})

        def worker():
            try:
                if callback:
                    callback("准备下载任务")
                out_dir = self.save_root / task_id
                out_dir.mkdir(exist_ok=True)

                # 只做一次解析！杜绝重复请求
                ydl_opts_info = {"quiet": True, "no_warnings": True}
                with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                    info = ydl.extract_info(target_url, download=False)
                stat_data = get_bili_stat(bv)
                cid_data = get_bili_cid(bv)
                cid = cid_data.get("cid")
                aid = stat_data.get("aid")

                # 组装文件名：标题 [BVxxxx][avxxxx]
                title_raw = info.get("title", "")
                if aid:
                    full_name = f"{title_raw} [{bv}][av{aid}]"
                else:
                    full_name = f"{title_raw} [{bv}]"
                safe_filename = self.clean_filename(full_name)

                # 写入元数据meta.json
                meta = {
                    "task_id": task_id,
                    "title": title_raw,
                    "bvid": bv,
                    "aid": aid,
                    "mid": stat_data.get("mid",""),
                    "uploader": info.get("uploader",""),
                    "tname": stat_data.get("tname",""),
                    "like": stat_data.get("like",0),
                    "coin": stat_data.get("coin",0),
                    "favorite": stat_data.get("favorite",0),
                    "view": stat_data.get("view",0),
                    "cid": cid
                }
                meta_file = out_dir / "meta.json"
                with open(meta_file,"w",encoding="utf-8") as f:
                    json.dump(meta,f,ensure_ascii=False,indent=2)

                # 下载封面
                cover_url = info.get("thumbnail")
                if cover_url:
                    if callback:
                        callback({"type": "download_progress", "percent":3, "msg":"保存封面"})
                    self._download_cover(cover_url, out_dir / "cover.jpg")

                # 下载弹幕，复用已获取cid
                if cid:
                    if callback:
                        callback({"type": "download_progress", "percent":6, "msg":"保存弹幕"})
                    self._download_danmaku(cid, out_dir / "danmaku.xml")

                # APK无ffmpeg适配 best单文件
                ydl_opts = {
                    "outtmpl": str(out_dir / f"{safe_filename}.%(ext)s"),
                    "quiet": False,
                    "no_warnings": False,
                    "format": "best",
                    "progress_hooks": [ydl_progress_hook]
                }
                if cookiefile and Path(cookiefile).exists():
                    ydl_opts["cookiefile"] = cookiefile

                if callback:
                    callback({"type": "download_progress", "percent":10, "msg":"开始拉取视频流"})

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([target_url])

                if callback:
                    callback({"type":"download_progress","percent":100,"msg":"下载完成，单文件输出，无需ffmpeg合并"})

            except Exception as err:
                err_msg = str(err)
                if callback:
                    if "403" in err_msg:
                        callback("B站403拒绝访问，请加载Cookie")
                    else:
                        callback(f"下载异常：{err_msg}")
            finally:
                if task_id in self.running_tasks:
                    del self.running_tasks[task_id]

        thr = threading.Thread(target=worker, daemon=True)
        self.running_tasks[task_id] = thr
        thr.start()
        return task_id
