[app]
package.name = biliparser
package.domain = org.biliparser

source.dir = .
source.include_exts = py,png,jpg,jpeg,json,txt

version = 0.1

android.api = 33
android.minapi = 21
android.ndk = 25b

requirements = python3,kivy,requests,yt_dlp

# 权限
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,ACCESS_NETWORK_STATE

fullscreen = 0
orientation = portrait

log_level = 2

# 关键：禁止buildozer自动调用sdkmanager去下载组件，尽量复用已下载SDK
android.accept_license = True
android.skip_update = True

[buildozer]
log_level = 2
warn_on_root = 1
