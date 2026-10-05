from history import History


h = History()


h.add(
    "测试视频",
    "123",
    "BV123",
    "/Download/test.mp4"
)


print(
    h.load()
)
