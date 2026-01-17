---
title: PicoCTF - Eavesdrop
tags: [PicoCTF, CTF, Misc]

category: "Security｜Practice｜PicoCTF｜Misc｜Flow"
date: 2024-01-31
---

# PicoCTF - Eavesdrop
<!-- more -->

## Recon
這一題是有關eavesdropping，代表有一個中間人監聽了所有conversation，先用一些基本的手段看一下整體的pcap packets(strings searching/IO Graphs/Statistic/Extract Default Protocol File...)，但是如果跟一下tcp的packets，可以發現傳輸兩方的對話紀錄，包括傳輸資料的加密方式等等，所以我們就可以直接把傳輸資料解密得到flag

## Exploit - Extract File & Decrypt
1. Follow TCP Packets
    ```
    Hey, how do you decrypt this file again?
    You're serious?
    Yeah, I'm serious
    *sigh* openssl des3 -d -salt -in file.des3 -out file.txt -k supersecretpassword123
    Ok, great, thanks.
    Let's use Discord next time, it's more secure.
    C'mon, no one knows we use this program like this!
    Whatever.
    Hey.
    Yeah?
    Could you transfer the file to me again?
    Oh great. Ok, over 9002?
    Yeah, listening.
    Sent it
    Got it.
    You're unbelievable
    ```
    從以上對話紀錄可以知道他們在9002 port有傳輸資料，並且解密的command是`openssl des3 -d -salt -in file.des3 -out file.txt -k supersecretpassword123`
2. Extract File
我們可以增加兩個column專門顯示source/destination port
![](https://hackmd.io/_uploads/B1ZrNEdOh.png)
然後找到port 9002的地方，可以發現No.57有附帶資料，把這筆資料另存起來
![](https://hackmd.io/_uploads/r11KNV_O2.png)
Note: 儲存資料到file.des3的時候，內容必須要是`Salted__9BæÄ'÷b4Ó[ÐNXämn±'-ärGsðÏú :›çk¿«@Û=6`
Note2: 也可以用`tcpflow`的方式把資料download下來
    ```bash!
    $ sudo tcpflow -r {pcap file}
    ```
3. Decrypt File
    ```bash!
    $ openssl des3 -d -salt -in file.des3 -out file.txt -k supersecretpassword123
    *** WARNING : deprecated key derivation used.
    Using -iter or -pbkdf2 would be better.
    ```

Flag: `picoCTF{nc_73115_411_dd54ab67}`

## Reference
[ Restructuring PCAP Network Packets (PicoCTF 2022 #45 'eavesdrop') ](https://youtu.be/Sb5PS-DddXY)