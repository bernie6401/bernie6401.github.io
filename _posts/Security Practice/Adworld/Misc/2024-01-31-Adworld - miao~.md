---
title: Adworld - miao~
tags: [Adworld, CTF, Misc]

category: "Security Practice｜Adworld｜Misc"
date: 2024-01-31
---

# Adworld - miao~
<!-- more -->

## Recon
這題也是看了別人的WP[^miao_WP_1]和官解

## Exploit
1. 用foremost搜索或救援檔案(神奇的解法，一開始完全想不到)
    ```bash!
    $ foremost -v miao\~.jpg
    Foremost version 1.5.7 by Jesse Kornblum, Kris Kendall, and Nick Mikus
    Audit File

    Foremost started at Sat Jul 15 15:21:29 2023
    Invocation: foremost -v miao~.jpg
    Output directory: /home/sbk6401/CTF/Adworld/Misc/miao~/output
    Configuration file: /etc/foremost.conf
    Processing: miao~.jpg
    |------------------------------------------------------------------
    File: miao~.jpg
    Start: Sat Jul 15 15:21:29 2023
    Length: 1 MB (1242752 bytes)

    Num      Name (bs=512)         Size      File Offset     Comment

    0:      00000000.jpg          55 KB               0
    1:      00000111.wav           1 MB           57212
    *|
    Finish: Sat Jul 15 15:21:29 2023

    2 FILES EXTRACTED

    jpg:= 1
    rif:= 1
    ------------------------------------------------------------------

    Foremost finished at Sat Jul 15 15:21:29 2023
    ```
    可以看到抓到其中有一個`.wav`檔案
2. 分析音檔
用audacity開頻譜圖，可以看到`CatCTF`的字樣
![](https://hackmd.io/_uploads/SJAntp19n.png)

3. 用DeepSound的軟體解密，而密碼就是上面拿到的`CatCTF`
![](https://hackmd.io/_uploads/H1369Ty5n.png)

4. Decode Encrypted Flag
用[獸語online decode](https://roar.iiilab.com/)
    ```bash!
    ~呜喵喵喵喵呜呜啊呜啊呜喵呜呜~喵啊喵啊喵啊呜喵呜~~~喵~呜喵啊喵啊喵喵喵呜呜~呜~呜喵呜呜啊啊~呜啊喵啊呜喵呜呜啊~喵~呜呜喵喵~喵喵喵呜呜呜喵~呜喵呜呜啊~呜啊啊喵啊呜喵呜呜喵~喵~呜喵呜~~喵喵喵呜啊呜啊喵呜喵呜呜啊~呜啊啊喵啊呜~啊喵~~喵~呜呜喵喵喵喵喵喵呜啊呜呜~呜喵呜呜~喵~喵啊喵啊呜~~啊啊~喵~呜呜喵喵啊喵喵喵呜呜呜呜~呜喵呜呜~呜啊~啊喵啊呜~~啊啊~喵~呜呜喵喵呜喵喵喵呜啊喵呜喵呜喵呜呜啊呜啊啊啊喵啊呜喵喵呜啊~喵~呜喵呜喵喵喵喵喵呜啊喵喵呜呜喵呜呜~喵~啊啊喵啊呜~~啊啊~喵~呜喵呜~啊喵喵喵呜呜~喵啊呜喵呜呜啊啊呜喵啊喵啊呜~呜~喵~喵~呜呜喵喵喵喵喵喵呜啊喵喵啊呜喵呜呜~呜呜呜啊喵啊呜喵呜啊喵啊
    ```
    ![](https://hackmd.io/_uploads/S1xdjTy9h.png)

Flag: `CatCTF{d0_y0u_Hate_c4t_ba3k1ng_?_M1ao~}`

## Reference
[^miao_WP_1]:[ZimaBlue WP](https://www.cnblogs.com/ZimaBlue/articles/17024728.html)