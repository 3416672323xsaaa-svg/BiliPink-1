from bili_api import BiliAPI


api = BiliAPI()


result = api.get_info(
    "BV1xx411c7mD"
)


print(result)
