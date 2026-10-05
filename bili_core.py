from bili_input import BiliInput
import requests
import re



class BiliCore:


    def __init__(self):

        self.input = BiliInput()



    # AV转BV
    def av_to_bv(self, aid):


        url = (
            "https://api.bilibili.com/"
            "x/web-interface/view"
        )


        try:

            r = requests.get(

                url,

                params={
                    "aid":aid
                },

                timeout=10

            )


            data=r.json()


            if data["code"]==0:

                return data["data"]["bvid"]


        except:

            pass


        return None




    # 处理用户输入
    def convert(self,text):


        result = self.input.parse(text)



        if result["type"]=="BV":

            return result["value"]



        if result["type"]=="AV":

            return self.av_to_bv(
                result["value"]
            )



        if result["type"]=="SHORT":


            url=self.input.expand_short(
                result["value"]
            )


            if url:


                bv=re.search(
                    r'BV[a-zA-Z0-9]+',
                    url
                )


                if bv:

                    return bv.group()



        return None
