[app]

# 包名，不能有中文、空格
package.name = bilipink
package.domain = org.bilipink

# App名称（手机桌面显示名字）
app.title = BiliPink

# 包版本
package.version = 0.1

# 依赖清单，yt-dlp+requests，kivy做界面
requirements = python3,kivy,yt-dlp==2026.4.12,requests

# 包含的文件后缀，保证 bili_api.py、html、json全部打包进APK
source.include_exts = py,png,jpg,json,txt,html,xml

# 主程序入口，改成你的启动py文件名
source.main = main.py

# 安卓设置
android.api = 33
android.ndk = 25b
android.sdk = 24

# 安卓权限：网络、读写存储
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# 关闭自动屏幕旋转，固定竖屏
android.orientation = portrait

# 不使用android bootstrap（kivy稳定）
android.bootstrap = sdl2

# 启用webview如果后面需要，当前可选关闭
android.enable_webview = False

# 日志输出，打包调试用
android.debug = True

# 禁用一些不需要的组件，减小包体积
android.add_libs_armeabi_v7a =
android.add_libs_arm64_v8a =
android.add_assets =

# 忽略不需要的文件
source.exclude_exts = spec
source.exclude_dirs = tests, bin, .github, __pycache__

# 不压缩python字节码（防止部分安卓下模块加载失败）
android.python_optimize = 0

[buildozer]

# 日志等级
log_level = 2
warn_on_root = 0
