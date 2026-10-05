[app]
title = BiliPink
version = 1.0

package.name = bilipink
package.domain = org.bilipink

source.dir = .
source.main = main.py

requirements = python3,kivy,requests

android.api = 34
android.minapi = 24
android.build_tools_version = 35.0.0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE

android.orientation = portrait

p4a.bootstrap = sdl2


[buildozer]
log_level = 2
warn_on_root = 0
