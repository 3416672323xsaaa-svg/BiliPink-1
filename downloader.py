import os
import time
import requests
import subprocess
import shutil
import re
from kivy.resources import resource_find

class Downloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent":"Mozilla/5.0 Android",
            "Referer":"https://www.bilibili.com/"
        })

    def _download_file(self, url, save_path, offset, progress_cb, file_label):
        resp = self.session.get(url, stream=True, timeout=30)
        resp.raise_for_status()
        local_total = int(resp.headers.get('content-length',0))
        downloaded = 0
        chunk_size = 1024*128
        start_time = time.time()

        with open(save_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    elapsed = time.time() - start_time
                    speed_bps = chunk_size / elapsed if elapsed>0 else 0
                    global_downloaded = offset + downloaded
                    progress_cb(global_downloaded, offset+local_total, speed_bps, f"{file_label}: {downloaded/local_total*100:.1f}%")
        return local_total

    def _ffmpeg_merge_with_progress(self, ffmpeg_bin, video_path, audio_path, out_path, progress_cb):
        cmd = [
            ffmpeg_bin,
            "-i", video_path,
            "-i", audio_path,
            "-c", "copy",
            "-y", out_path,
            "-progress", "pipe:1",
            "-v", "error"
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time_regex = re.compile(r"out_time_ms=(\d+)")
        duration_regex = re.compile(r"duration=(\d+\.\d+)")
        duration_sec = None

        while proc.poll() is None:
            try:
                line = proc.stdout.readline()
            except TimeoutError:
                continue
            if not line:
                continue
            dur_match = duration_regex.search(line)
            if dur_match:
                duration_sec = float(dur_match.group(1))
            t_match = time_regex.search(line)
            if t_match and duration_sec:
                current_ms = int(t_match.group(1))
                pct = current_ms / (duration_sec * 1000)
                progress_cb(int(pct*10000),10000, 0, f"合并中: {pct*100:.1f}%")
        return proc.returncode == 0

    def download_by_info(self, video_info, quality_item, audio_item, base_filename, progress_cb):
        save_dir = "/storage/emulated/0/Download/BiliPink" if os.name == "posix" else "./BiliPink"
        os.makedirs(save_dir, exist_ok=True)
        temp_dir = os.path.join(save_dir, "tmp")
        os.makedirs(temp_dir, exist_ok=True)

        video_tmp = os.path.join(temp_dir, "video.m4s")
        audio_tmp = os.path.join(temp_dir, "audio.m4s")
        out_mp4 = os.path.join(save_dir, f"{base_filename}.mp4")

        try:
            video_url = video_info["video_streams"][quality_item["id"]]
            audio_url = video_info["audio_streams"][audio_item["id"]]

            # 下载视频流
            self._download_file(video_url, video_tmp, 0, progress_cb, "视频流")
            # 下载音频流，offset分段
            self._download_file(audio_url, audio_tmp, 5000, progress_cb, "音频流")

            ffmpeg_path = resource_find("assets/ffmpeg")
            if not ffmpeg_path:
                raise Exception("APK assets目录找不到ffmpeg二进制！")
            os.chmod(ffmpeg_path, 0o755)

            merge_ok = self._ffmpeg_merge_with_progress(ffmpeg_path, video_tmp, audio_tmp, out_mp4, progress_cb)
            if not merge_ok:
                raise Exception("FFmpeg合并失败")

        finally:
            # 成功/失败都会清理临时文件
            if os.path.exists(video_tmp):
                os.remove(video_tmp)
            if os.path.exists(audio_tmp):
                os.remove(audio_tmp)
            shutil.rmtree(temp_dir, ignore_errors=True)

        return (True, out_mp4)
