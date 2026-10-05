[app]
title = BiliPink
package.name = bilipink
package.domain = org.bilipink
version = 1.0

source.dir = .
source.main = app.py
package.version = 1.0

requirements = python3,kivy,flask,yt-dlp,requests

source.include_exts = py,png,jpg,json,html,txt
source.exclude_dirs = tests,bin,.github,__pycache__

android.api = 33
android.ndk = 25b
android.sdk = 24

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.orientation = portrait
p4a.bootstrap = sdl2
android.debug = True
android.python_optimize = 0

[buildozer]
log_level = 2
warn_on_root = 0
