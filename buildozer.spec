[app]
package.name = biliparser
package.domain = org.biliparser

# 漏掉这个title就直接报错！！
title = BiliPink

source.dir = .
source.include_exts = py,png,jpg,jpeg,json,txt

version = 0.1

android.api = 33
android.minapi = 21
android.ndk = 25b

requirements = python3,kivy,requests,yt_dlp

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,ACCESS_NETWORK_STATE

fullscreen = 0
orientation = portrait

log_level = 2
android.accept_license = True
android.skip_update = True

[buildozer]
log_level = 2
warn_on_root = 1
