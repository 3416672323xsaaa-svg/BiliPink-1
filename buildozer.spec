[app]

title = BiliPink
package.name = bilipink
package.domain = org.bilipink

source.dir = .
source.include_exts = py,png,jpg,jpeg,json,kv

version = 1.0
requirements = python3,kivy,requests,yt-dlp
entrypoint = main.py

orientation = portrait
fullscreen = 0

# Android13+ 新权限，删除废弃存储权限
android.permissions = INTERNET,READ_MEDIA_VIDEO,READ_MEDIA_IMAGES
android.permissions_api33plus = INTERNET,READ_MEDIA_VIDEO,READ_MEDIA_IMAGES

android.accept_sdk_license = True
android.api = 33
android.minapi = 21

android.ndk = 25b
android.sdk = 33
android.ndk_api = 21

android.archs = arm64-v8a
p4a.bootstrap = sdl2

android.gradle_download = https://services.gradle.org/distributions/gradle-7.6.4-all.zip
android.gradle_plugin = 7.4.2
p4a.gradle_options = -Dorg.gradle.java.home=/usr/lib/jvm/temurin-17-jdk-amd64

exclude_patterns = **/test/*, **/tests/*

[buildozer]
log_level = 2
warn_on_root = 1
