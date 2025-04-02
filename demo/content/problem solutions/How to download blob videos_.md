---
title: How to download blob videos?
tags: [problem solution]

---

# How to download blob videos?
參考資料: https://stackoverflow.com/questions/42901942/how-do-we-download-a-blob-url-video
參考資料: https://superuser.com/questions/1260846/downloading-m3u8-videos

## Prerequisite
有兩種方法，一種是利用ffmpeg，另外一種是[yt-dlp](https://github.com/yt-dlp/yt-dlp/wiki/Installation)，前者下載比較慢，後者快很多，但都可以正確的下載
```bash
# Ffmpeg
$ sudo apt install ffmpeg -y

# yt-dlp Windows
$ choco install yt-dlp

# yt-dlp linux
sudo add-apt-repository ppa:tomtomtom/yt-dlp    # Add ppa repo to apt
sudo apt update                                 # Update package list
sudo apt install yt-dlp                         # Install yt-dlp
```
## Step
1. 透過Browser的F12找出m3u8的封包
    ![image](https://hackmd.io/_uploads/HyrYRTR4kl.png)
2. 透過yt-dlp下載
    複製封包的Request URL
    ```bash
    $ yt-dlp "https://surrit.com/9e2613de-2337-4cfd-aab5-2a68c0fbad14/playlist.m3u8"
    ```