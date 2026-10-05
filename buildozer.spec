[app]

title = BiliPink

package.name = bilipink
package.domain = org.bilipink

source.dir = .
source.main = main.py

version = 1.0

requirements = python3,kivy,requests

source.include_exts = py,png,jpg,kv,atlas,json

android.api = 34
android.minapi = 24

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.orientation = portrait

p4a.bootstrap = sdl2


[buildozer]

log_level = 2
warn_on_root = 0
