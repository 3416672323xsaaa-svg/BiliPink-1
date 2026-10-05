import json
import os
import time



class History:


    def __init__(self):

        self.file="history.json"


        if not os.path.exists(self.file):

            with open(
                self.file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    [],
                    f
                )



    def add(self,info,path):


        data=self.load()



        data.append({

            "title":
            info.get("title",""),


            "aid":
            info.get("id",""),


            "time":
            time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),


            "path":
            path

        })



        with open(

            self.file,

            "w",

            encoding="utf-8"

        ) as f:


            json.dump(

                data,

                f,

                ensure_ascii=False,

                indent=4

            )





    def load(self):


        with open(

            self.file,

            "r",

            encoding="utf-8"

        ) as f:


            return json.load(f)
