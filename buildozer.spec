[app]
package.name = biliparser
package.domain = org.biliparser
title = BiliPink

source.dir = .
source.include_exts = py,png,jpg,jpeg,json,txt

version = 0.1

android.api = 33
android.minapi = 21
android.ndk = 25b

# 先移除yt‑dlp，先保证APK能编译出来
requirements = python3,kivy,requests

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
fullscreen = 0
orientation = portrait

log_level = 2
android.accept_license = True
android.skip_update = True

[buildozer]
log_level = 2
warn_on_root = 1
