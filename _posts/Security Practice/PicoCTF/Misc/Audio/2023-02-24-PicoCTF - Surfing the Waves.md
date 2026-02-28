---
title: PicoCTF - Surfing the Waves
tags: [PicoCTF, CTF, Misc]

category: "Security Practice｜PicoCTF｜Misc｜Audio"
date: 2023-02-24
---

# PicoCTF - Surfing the Waves
<!-- more -->
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: [Surfing the Waves](https://play.picoctf.org/practice/challenge/117?category=4&page=3)

## Description & Hint
While you're going through the FBI's servers, you stumble across their incredible taste in music. One [main.wav](https://mercury.picoctf.net/static/cf917a179937f814d966e53bb1fd4b90/main.wav) you found is particularly interesting, see if you can find the flag!
Hint:
* Music is cool, but what other kinds of waves are there?
* Look deep below the surface

## Exploit - <font color="FF0000">通靈</font>
1. Audacity to Analyze
The sound seems quite normal but when you zoom in the audio track, it looks like something encode. 
![](https://i.imgur.com/D1H1jpU.png)
2. Read it - `scipy.io`
Use `scipy.io` library to read it and print the data out.
    ```python!
    >>> from scipy.io.wavfile import read
    >>> rate, data = read("./main.wav")
    >>> print(data)
    [2007 2503 2005 ... 4503 4501 7501]
    >>> import numpy as np
    >>> print(np.unique(data))
    [1000 1001 1002 1003 1004 1005 1006 1007 1008 1009 1500 1501 1502 1503
     1504 1505 1506 1507 1508 1509 2000 2001 2002 2003 2004 2005 2006 2007
     2008 2009 2500 2501 2502 2503 2504 2505 2506 2507 2508 2509 3000 3001
     3002 3003 3004 3005 3006 3007 3008 3009 3500 3501 3502 3503 3504 3505
     3506 3507 3508 3509 4000 4001 4002 4003 4004 4005 4006 4007 4008 4009
     4500 4501 4502 4503 4504 4505 4506 4507 4508 4509 5000 5001 5002 5003
     5004 5005 5006 5007 5008 5009 5500 5501 5502 5503 5504 5505 5506 5507
     5508 5509 6000 6001 6002 6003 6004 6005 6006 6007 6008 6009 6500 6501
     6502 6503 6504 6505 6506 6507 6508 6509 7000 7001 7002 7003 7004 7005
     7006 7007 7008 7009 7500 7501 7502 7503 7504 7505 7506 7507 7508 7509
     8000 8001 8002 8003 8004 8005 8006 8007 8008 8009 8500 8501 8502 8503
     8504 8505 8506 8507 8508 8509]
    ```
    Seems it has some rule $\to$
    `1000 ~ 1009`
    `1500 ~ 1509`
    `2000 ~ 2009`
    ...
    `8500 ~ 8509`
    It has exactly 16 intervals $\to$ hex value
3. Let's try to exploit it
* Whole exploit
    :::spoiler exploit
    ```python!
    from scipy.io.wavfile import read
    from tqdm import trange

    path = '.'
    rate, data = read(path + "/main.wav")

    decode_dic = {
        10 : "0",
        15 : "1",
        20 : "2",
        25 : "3",
        30 : "4",
        35 : "5",
        40 : "6",
        45 : "7",
        50 : "8",
        55 : "9",
        60 : "A",
        65 : "B",
        70 : "C",
        75 : "D",
        80 : "E",
        85 : "F",
    }

    message = ''
    for i in trange(len(data)):
        message += decode_dic[data[i] // 100]

    print(bytes.fromhex(message).decode())
    ```
    :::
Then you can get the source code and flag...

## Reference
[picoCTF 2021 Surfing the Waves](https://youtu.be/tDPetapjm74)