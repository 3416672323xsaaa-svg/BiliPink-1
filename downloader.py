import yt_dlp
import os


class Downloader:


    def __init__(self, callback=None):

        self.callback = callback

        self.path = (
            "/storage/emulated/0/"
            "Download/BiliPink"
        )


        os.makedirs(
            self.path,
            exist_ok=True
        )



    def progress(self,d):


        if d["status"] == "downloading":


            total = d.get(
                "total_bytes"
            ) or d.get(
                "total_bytes_estimate"
            )


            now = d.get(
                "downloaded_bytes",
                0
            )


            if total:


                percent = (

                    now / total * 100

                )


                text = (

                    "下载中 "

                    + str(round(percent,1))

                    + "%"

                )


                if self.callback:

                    self.callback(text)



        elif d["status"]=="finished":


            if self.callback:

                self.callback(
                    "合并视频中..."
                )





    def download(

        self,

        bv,

        mode="视频+音频",

        quality="最高画质"

    ):


        url=(

            "https://www.bilibili.com/video/"

            +bv

        )



        if quality=="最高画质":

            fmt="bestvideo"

        else:


            h=quality.replace(
                "P",
                ""
            )


            fmt=(

                "bestvideo[height<="
                +h+
                "]"

            )




        if mode=="只下载音频":


            options={


                "outtmpl":

                self.path+

                "/%(title)s【AV%(id)s】.%(ext)s",


                "format":

                "bestaudio",


                "postprocessors":[

                    {

                    "key":
                    "FFmpegExtractAudio",

                    "preferredcodec":
                    "mp3"

                    }

                ],


                "progress_hooks":[

                    self.progress

                ]

            }



        else:


            options={


                "outtmpl":

                self.path+

                "/%(title)s【AV%(id)s】.%(ext)s",


                "format":

                fmt+

                "+bestaudio",


                "merge_output_format":

                "mp4",


                "progress_hooks":[

                    self.progress

                ]

            }




        with yt_dlp.YoutubeDL(options) as ydl:


            info=ydl.extract_info(

                url,

                download=True

            )


            return info
