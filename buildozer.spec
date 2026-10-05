[app]
title = BiliPink
package.name = bilipink
package.domain = org.bilipink

source.dir = .
source.main = app.py
package.version = 0.1

requirements = python3,kivy,flask,yt‑dlp,requests

source.include_exts = py,png,jpg,json,txt,html,xml
source.exclude_dirs = tests,bin,.github,__pycache__

android.api = 33
android.ndk = 25b
android.sdk = 24

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.orientation = portrait
p4a.bootstrap = sdl2
android.debug = True
android.python_optimize = 0

[buildozer]
log_level = 2
warn_on_root = 0
 
