---
title: PicoCTF - WebNet0
tags: [PicoCTF, CTF, Misc]

category: "Security Practice｜PicoCTF｜Misc｜Flow"
date: 2024-01-31
---

# PicoCTF - WebNet0
<!-- more -->

## Background
[解密TLS協議全記錄之利用wireshark解密](https://blog.csdn.net/walleva96/article/details/106844033)

## Recon
這一題其實就只是利用wireshark把訊息解密就這樣，所以看了一些文章後就按圖施工就好，解密完後就直接string search就找到了

## Exploit - TLS Decrypt
1. 在`Edit/Preferences/RSA Keys/`中`Add new keyfile`
![](https://hackmd.io/_uploads/ByMdwwSe6.png)
2. 加入題目給的private key file後記得要重新開啟該pcap file
![](https://hackmd.io/_uploads/S1PMPDSx6.png)