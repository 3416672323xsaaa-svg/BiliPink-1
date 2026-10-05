[app]

# APP名称
title = BiliPink

# 包名
package.name = bilipink

# 域名（随便写）
package.domain = org.bilipink


# 程序入口
source.dir = .

# 支持的文件
source.include_exts = py,png,jpg,jpeg,json,kv


# Python依赖
requirements = python3,kivy,requests,yt-dlp


# APP版本
version = 1.0


# 屏幕方向
orientation = portrait


# Android权限
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE


# Android架构
android.archs = arm64-v8a


# 不使用全屏
fullscreen = 0



[buildozer]


# 日志等级
log_level = 2


# 编译警告
warn_on_root = 1



[python-for-android]

# 使用最新版本
p4a.branch = master
