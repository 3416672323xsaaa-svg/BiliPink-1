[app]

# (str) Title of your application
title = BiliPink

# (str) Package name
package.name = bilipink

# (str) Package domain
package.domain = org.bilipink

# (str) Version
version = 1.0

# (str) Source code location
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,json,txt

# (str) Application entry point
entrypoint = main.py

# (str) Supported orientation
orientation = portrait


# (list) Requirements
requirements = python3,kivy,requests


# (str) Android permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE


# (bool) Fullscreen
fullscreen = 0


# (int) Android API
android.api = 35

# (int) Minimum Android API
android.minapi = 23

# (str) Android NDK version
android.ndk = 25b


# (bool)
android.accept_sdk_license = True


# (str) Android architecture
android.archs = arm64-v8a, armeabi-v7a


# (bool) Copy python files
android.copy_libs = 1


[buildozer]

# (int) Log level
log_level = 2
