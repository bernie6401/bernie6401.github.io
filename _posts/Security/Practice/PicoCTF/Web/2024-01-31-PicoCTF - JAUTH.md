---
title: PicoCTF - JAUTH
tags: [Web, PicoCTF, CTF]

category: "Security｜Practice｜PicoCTF｜Web"
date: 2024-01-31
---

# PicoCTF - JAUTH
<!-- more -->

## Background
[NTUCNS - HW3 - JWT Authentication](https://hackmd.io/JO7xByQgQWK67eU0goHMeA?view#c)

## Exploit - JWR + None
其實這一題有一點奇怪，應該說之前在解CNS作業的驗證時，TA說目前應該是不行以Alg=None的形式進行驗證的設計，我以為是後端的框架都不支援了，但應該說是不建議這樣的做法，所以這一題比想像中簡單，我還以為要把公鑰找出來，再進行sign
1. 用類似jwt.io的網站([online tool](https://token.dev/))，但支援alg=none的編碼
Payload: `eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJhdXRoIjoxNjg3NzY0MjM1MTAzLCJhZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwOS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzExNC4wIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNjg3NzY0MjM1fQ`
![](https://hackmd.io/_uploads/B1vcsALOn.png)


Flag: `picoCTF{succ3ss_@u7h3nt1c@710n_72bf8bd5}`

## Reference
[ picoCTF : JAUTH (Challenge 8) ](https://youtu.be/njsjTVcwGwY)