[app]

title = appname

package.name = packagename
package.domain = io.packagename

source.dir = .
source.include_exts = py,png,jpg,jpeg,atlas

version = 0.0.1

requirements = python3,kivy,kivymd

entrypoint = main.py

android.permissions = INTERNET

android.accept_sdk_license = True

android.allow_api_min = 21
android.api = 33
android.minapi = 21
android.ndk = 25b

exclude_patterns = **/test/*, **/tests/*

p4a.bootstrap = sdl2

android.release_artifact = apk


# 签名
android.keystore = app-release.keystore
android.keystore_storepass = android
android.keystore_keypass = android
android.keystore_alias = appkey


[buildozer]

log_level = 2
warn_on_root = 1
