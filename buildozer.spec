[app]

title = BiliPink
package.name = bilipink
package.domain = org.bilipink

source.dir = .
source.include_exts = py,png,jpg,jpeg,json,kv

version = 1.0
requirements = python3,kivy,requests

entrypoint = main.py

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_MEDIA_VIDEO,READ_MEDIA_IMAGES
android.permissions_api33plus = INTERNET,READ_MEDIA_VIDEO,READ_MEDIA_IMAGES

android.accept_sdk_license = True
android.api = 33
android.minapi = 21

android.ndk = 25b
android.sdk = 33

android.archs = arm64-v8a
p4a.bootstrap = sdl2

exclude_patterns = **/test/*,**/tests/*

[buildozer]
log_level = 2
warn_on_root = 1
