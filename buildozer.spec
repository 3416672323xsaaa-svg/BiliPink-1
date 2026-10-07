[app]
title = BiliPink
package.name = bilipink
package.domain = org.bilipink
source.dir = .
source.include_exts = py,png,jpg,jpeg,json,ttf
source.exclude_dirs = tests, bin, .git

package.version = 0.1
app.mainmodule = main.py

requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests

android.api = 33
android.ndk = 25b
android.accept_sdk_license = True
android.permissions = INTERNET,MANAGE_EXTERNAL_STORAGE,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO
android.allow_backup = True
orientation = portrait

android.add_assets = NotoSansSC-Regular.ttf,assets
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 0
