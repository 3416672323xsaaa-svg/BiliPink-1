[app]

# 应用名称，随便改
title = MyKivyApp

# 包名（小写字母，不能有空格）
package.name = mykivyapp

# 域名格式，随便写
package.domain = org.mykivyapp

# 源码入口文件
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# python依赖，把你需要的写进去
requirements = python3,kivy,kivymd

# ----------------核心p4a配置，解决404关键----------------
p4a.fork = kivy
p4a.branch = release-2024.04

# 只编译arm64-v8a，减少下载文件，大幅降低404概率
android.archs = arm64-v8a

android.api = 33
android.minapi = 21

# 开启release打包
android.release_artifact = apk

# 权限，需要联网就保留这一行
android.permissions = INTERNET

# 不开启安卓存储限制（按需）
android.accept_sdk_license = True

# 不启用可选功能
android.ndk = 25b
android.enable_androidx = True

# 关闭不需要的功能，减少编译负载
android.use_android_icu = False
android.gradle_dependencies = 

# 日志
log_level = 2

# 不使用预编译bootstrap
p4a.bootstrap = sdl2

# 图标（没有可以注释掉，#开头）
# icon.filename = icon.png
