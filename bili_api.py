import requests


class BiliAPI:


    def __init__(self):

        self.headers = {

            "User-Agent":
            "Mozilla/5.0"

        }



    def get_info(self, bvid):


        url = (
            "https://api.bilibili.com/"
            "x/web-interface/view"
        )


        params = {

            "bvid": bvid

        }


        try:

            r = requests.get(

                url,

                params=params,

                headers=self.headers,

                timeout=10

            )


            data = r.json()


            if data.get("code") != 0:

                print(
                    "接口错误:",
                    data.get("message")
                )

                return None



            video = data["data"]



            result = {

                "title":
                video["title"],


                "aid":
                video["aid"],


                "bvid":
                video["bvid"],


                "cover":
                "https:" + video["pic"],


                "description":
                video["desc"],


                "duration":
                video["duration"],


                "owner":
                video["owner"]["name"],


                "uid":
                video["owner"]["mid"],


                "view":
                video["stat"]["view"],


                "like":
                video["stat"]["like"],


                "coin":
                video["stat"]["coin"],


                "favorite":
                video["stat"]["favorite"],


                "comment":
                video["stat"]["reply"]

            }


            return result



        except Exception as e:

            print(
                "错误:",
                e
            )

            return None
