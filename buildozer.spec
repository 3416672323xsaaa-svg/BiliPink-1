[app]
#标题允许中文
title = appname
package.name = packagename
package.domain = io.packagename

source.dir = .
source.include_exts = py,png,jpg,jpeg,atlas

version = 0.0.1

requirements = python3,kivy,kivymd,libiconv,libffi

# 程序入口，根目录必须存在 main.py
entrypoint = main.py

# 权限
android.permissions = INTERNET

#sdk ndk设置
android.accept_sdk_license = True
android.allow_api_min = 21
android.api = 33
android.minapi = 21
android.ndk = 25b

exclude_patterns = **/test/*, **/tests/*

p4a.bootstrap = sdl2

#强制输出apk，不要aab
android.release_artifact = apk

# ==========签名配置 不要加#注释==========
android.keystore = app-release.keystore
android.keystore_storepass = android
android.keystore_keypass = android
android.keystore_alias = appkey

[buildozer]
log_level = 2
warn_on_root = 1
