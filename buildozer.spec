[app]

# 包名，只能小写字母数字，不能有中文
package.name = bilidownload
package.domain = org.bili.dl

source.dir = .
source.include_exts = py,png,jpg,jpeg,svg,ttf,txt
source.exclude_dirs = tests, bin, .git

# 应用版本
version = 0.1

# 要安装的依赖，kivy**不要写版本号**
requirements = python3,kivy,requests

# 安卓配置
android.api = 33
android.ndk = 25b
android.sdk = 24
android.archs = arm64‑v8a
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# 应用界面设置
fullscreen = 0
orientation = portrait

# 图标
icon.filename = icon.png

# 日志
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 0
