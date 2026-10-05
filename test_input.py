from bili_input import BiliInput


b = BiliInput()


tests = [
    "BV1xx411xx",
    "av123456",
    "123456",
    "快来看这个视频 https://b23.tv/test"
]


for t in tests:
    print("输入:", t)
    print("结果:", b.parse(t))
    print("----------------")
