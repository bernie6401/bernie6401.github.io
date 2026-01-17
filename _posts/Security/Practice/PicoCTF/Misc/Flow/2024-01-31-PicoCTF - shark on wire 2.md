---
title: PicoCTF - shark on wire 2
tags: [PicoCTF, CTF, Misc]

category: "Security｜Practice｜PicoCTF｜Misc｜Flow"
date: 2024-01-31
---

# PicoCTF - shark on wire 2
<!-- more -->

## Recon
這一提出的很硬要，誰知道會把flag藏在這種地方，也沒有任何的提示，如果不是看[^pico-misc-shark-on-wire-2-wp-zomry1]根本不知道這題要表達甚麼，也可能是我太蔡

1. Simple Recon
首先做一些基本的recon，諸如dump files/string search/follow tcp or udp之類的，會發現UDP packets會有一些訊息出現，其中出現Start和一些a/b最後接著end
![](https://hackmd.io/_uploads/rkASlUD02.png)
![](https://hackmd.io/_uploads/BkxFgLPRn.png)
2. Set filter as `udp.port==22`
會發現其中所有的len都一樣，就只有source port不一樣，同樣都是5xxx開頭，而後三位數就是flag
![](https://hackmd.io/_uploads/BJq71UvC2.png)
3. Extract Flag
所以只要把所有的port擷取出來拚在一起，就可以拿到flag了

## Exploit
```python!
import pyshark

capture = pyshark.FileCapture('./PicoCTF/Misc/shark on wire 2/capture.pcap', display_filter='udp.port == 22')

data = []
for pkt in capture:
    if pkt.udp.port != '5000':
        data.append(chr(int(pkt.udp.port[1:])))
print("".join(data))
```

Flag: `picoCTF{p1LLf3r3d_data_v1a_st3g0}`

## Reference
[^pico-misc-shark-on-wire-2-wp-zomry1]:[PicoCTF 2019 - shark on wire 2:-1:](https://zomry1.github.io/shark-on-wire-2/)