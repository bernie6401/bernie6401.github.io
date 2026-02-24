---
title: PicoCTF - Secrets
tags: [PicoCTF, CTF, Web]

category: "Security Practice｜PicoCTF｜Web"
date: 2023-06-26
---

# PicoCTF - Secrets
<!-- more -->
###### tags: `PicoCTF` `CTF` `Web`

## Recon
* Description: We have several pages hidden. Can you find the one with the flag?
* Hint: folders folders folders

這一題也是蠻有趣的

## Exploit - <font color="FF0000">通靈</font>
1. 首先看一下網頁的source code，沒什麼特別的地方，但有看到`secret/assets/index.css`，所以有一個route是secrets，試看看有甚麼東西
![](https://hackmd.io/_uploads/HywRa08_n.png)

2. 發現這樣的想法是對的，陸續看一下source code有甚麼其他route，就繼續加在URL就對了
![](https://hackmd.io/_uploads/HyumC0U_2.png)


Payload: `view-source:http://saturn.picoctf.net:65352/secret/hidden/superhidden/`
Flag: `picoCTF{succ3ss_@h3n1c@10n_790d2615}`

## Reference
[ secrets | picoCTF 2022 ](https://youtu.be/40DYCMInk5E)