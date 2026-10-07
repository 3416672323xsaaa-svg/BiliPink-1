[app]
title = BiliPink
package.name = bilipink
package.domain = org.bilipink.dl

source.dir = .
source.include_exts = py,png,jpg,jpeg,svg,ttf,txt
source.exclude_dirs = tests, bin, .git

version = 0.1
requirements = python3,kivy,requests

android.api = 33
android.ndk = 25b
android.archs = arm64‑v8a
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

fullscreen = 0
orientation = portrait
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 0
accept_sdk_license = True
