from formats import FormatChecker


f = FormatChecker()


url = "这里放你的B站视频链接"


print(
    f.get_quality(url)
)
