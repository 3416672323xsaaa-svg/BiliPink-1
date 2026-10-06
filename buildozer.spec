[app]

# 应用名称
title = appname

# 包名（只能英文）
package.name = packagename

# 包域名
package.domain = io.packagename


# 项目目录
source.dir = .

# 包含的文件类型
source.include_exts = py,png,jpg,jpeg,atlas


# 版本
version = 0.0.1


# Python依赖
# 第一次先用最小配置，成功后再加kivymd
requirements = python3,kivy


# 入口文件
# 根目录必须有main.py
entrypoint = main.py



# Android权限
android.permissions = INTERNET



# Android SDK
android.accept_sdk_license = True

android.api = 33

android.minapi = 21

android.allow_api_min = 21


# NDK版本
android.ndk = 25b



# 使用SDL2
p4a.bootstrap = sdl2


# 手动指定python-for-android
p4a.source_dir = /home/runner/.buildozer/p4a



# 输出APK，不生成AAB
android.release_artifact = apk



# 排除文件
exclude_patterns = **/test/*, **/tests/*



# 签名
# 如果没有这个文件，先注释掉这四行
android.keystore = app-release.keystore
android.keystore_storepass = android
android.keystore_keypass = android
android.keystore_alias = appkey



[buildozer]


# 日志等级
log_level = 2


# 不建议root警告
warn_on_root = 1
