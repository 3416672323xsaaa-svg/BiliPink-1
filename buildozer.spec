[app]

title = MyKivyApp
package.name = mykivyapp
package.domain = org.mykivyapp

version = 1.0

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

requirements = python3,kivy,kivymd

p4a.fork = kivy
p4a.branch = master

android.archs = arm64-v8a
android.api = 33
android.minapi = 21

android.release_artifact = apk
android.permissions = INTERNET
android.accept_sdk_license = True

android.ndk = 25b
android.enable_androidx = True
android.use_android_icu = False
android.gradle_dependencies = 

log_level = 2
p4a.bootstrap = sdl2

# icon.filename = icon.png
