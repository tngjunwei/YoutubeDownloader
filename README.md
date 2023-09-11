# Youtube audio file downloader

This python script downloads `.mp4` files from Youtube and converts it to `.mp3` format.

Due to Youtube requirements, you may need to input an API code the first time.

Download your own platform specific `ffmpeg.exe`. For Windows, download and unzip from [FFMEG builds](https://www.gyan.dev/ffmpeg/builds/), then put the `ffmpeg.exe` executable file in the same directory as the pythons script.


## Getting Started

```cmd
pip -r requirements.txt
python yt-downloader.py [Youtube URL]
```