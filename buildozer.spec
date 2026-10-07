[app]
# 应用基础信息
package.name = bilipink
package.domain = org.bilipink
source.dir = .
source.include_exts = py,png,jpg,jpeg,json,ttf
source.exclude_dirs = tests, bin, .git

# 版本
version = 0.1

# 主程序入口
app.mainmodule = main.py

# KivyMD依赖
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests

# Android设置
android.api = 33
android.ndk = 25b
android.permissions = INTERNET,MANAGE_EXTERNAL_STORAGE,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO
android.allow_backup = True

# 横竖屏
orientation = portrait

# 图标（没有可以先留空）
# icon.filename = icon.png

# 字体 + assets目录（Action会自动把ffmpeg下载到assets）
android.add_assets = NotoSansSC-Regular.ttf,assets

# 关闭警告
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 0
