[app]

title = BiliPink

package.name = bilipink
package.domain = org.bilipink

source.dir = .
source.main = main.py

version = 1.0

requirements = python3,kivy,requests

source.include_exts = py,png,jpg,json,html,txt
source.exclude_dirs = tests,bin,.github,__pycache__

android.api = 35
android.sdk = 35
android.ndk = 25b
android.build_tools_version = 35.0.0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.orientation = portrait

p4a.bootstrap = sdl2

android.debug = True
android.python_optimize = 0


[buildozer]

log_level = 2
warn_on_root = 0
