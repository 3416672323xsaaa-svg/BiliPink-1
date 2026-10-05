import yt_dlp


class FormatChecker:


    def get_quality(self, bv):


        url = (
            "https://www.bilibili.com/video/"
            + bv
        )


        options = {

            "quiet": True,

            "skip_download": True

        }



        try:


            with yt_dlp.YoutubeDL(options) as ydl:


                info = ydl.extract_info(

                    url,

                    download=False

                )



            qualities = set()



            for f in info["formats"]:


                height = f.get("height")


                if height:

                    qualities.add(height)



            result = sorted(

                qualities,

                reverse=True

            )


            return [

                str(x)+"P"

                for x in result

            ]



        except Exception as e:


            print(
                "清晰度错误:",
                e
            )


            return []
