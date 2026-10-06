[app]
title = MyApp
package.name = myapp
package.domain = org.myapp

source.dir = .

source.include_exts = py,png,jpg,jpeg,svg,kv,json

version = 1.0

requirements = python3,kivy,kivymd,requests

orientation = portrait

android.permissions = INTERNET

android.api = 35

android.minapi = 23

android.ndk = 25.2.9519653

android.archs = arm64-v8a

android.release_keystore = %(dir)s/release.keystore
android.release_keyalias = release
android.release_keystore_password = android
android.release_keyalias_password = android

[buildozer]
log_level = 2
warn_on_root = 1
