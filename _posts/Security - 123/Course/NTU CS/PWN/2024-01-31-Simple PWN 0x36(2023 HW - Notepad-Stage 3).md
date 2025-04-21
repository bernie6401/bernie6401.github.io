---
title: Simple PWN 0x36(2023 HW - Notepad-Stage 3)
tags: [eductf, CTF, PWN]

category: "Security/Course/NTU CS/PWN"
---

# Simple PWN 0x36(2023 HW - Notepad-Stage 3)
<!-- more -->

## Source code
呈上上題

## Recon
這一題沒時間解出來，所以僅僅做個紀錄，包含和各位大老討論的結果以及流程
1. 首先，後端有一個洞，就是在login的write，他的buf仔細和其他有call到write做對比會發現，他並沒有清掉buf的內容，這代表他會完完整整的把裡面的內容送到前端，但為甚麼前面兩題都沒有這個問題呢?因為前端並沒有把buf的內容印出來，所以首要目標是找到一個方法可以leak出內容的shellcode之類的，這樣我們就可以抓到text / libc base address
2. 知道這些事情可以幹嘛呢?check token有一個bof的洞，我們可以利用這個洞來傳送rop，所以需要ret2libc抓到base address之後在蓋rop
3. ROP具體的內容是甚麼呢?有兩種方法可以拿到flag，一個是拿到shell之後setuid(0)，因為backend 有 suid 權限，所以我們才可以用 setuid(0) 以root 執行，然後cat /flag_root；第二種是直接ORW，看flag是啥這樣