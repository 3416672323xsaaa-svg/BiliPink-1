import json
import os
import time


class History:
    def __init__(self):
        # 使用Kivy安卓私有沙盒目录，不能直接用相对路径
        from kivy.app import App
        app = App.get_running_app()
        data_dir = App.get_running_app().user_data_dir
        self.file = os.path.join(data_dir, "history.json")

        try:
            if not os.path.exists(self.file):
                with open(self.file, "w", encoding="utf-8") as f:
                    json.dump([], f)
        except Exception:
            pass

    def add(self, task_id_str, path):
        """
        main传入：task_id_str 字符串(uuid), path保存路径
        """
        try:
            data = self.load()
            data.append({
                "task_id": task_id_str,
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "path": path
            })
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def load(self):
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
