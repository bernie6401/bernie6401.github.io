---
title: Simple Crypto - 0x05(2023 Lab - LSB)
tags: [CTF, Crypto, eductf]

category: "Security/Course/NTU CS/Crypto"
---

# Simple Crypto - 0x05(2023 Lab - LSB)
<!-- more -->

## Background
[ [edu-ctf 2023] week01 - crypto1 ](https://www.youtube.com/live/mqQ2zgK8a0Y?si=GRgtEKGHsCNcKuqU&t=7176)

## Source code
:::spoiler Source Code
```python
#! /usr/bin/python3
from Crypto.Util.number import bytes_to_long, getPrime
import os

from secret import FLAG

p = getPrime(1024)
q = getPrime(1024)
n = p * q
phi = (p - 1) * (q - 1)
e = 65537
d = pow(e, -1, phi)

m = bytes_to_long(FLAG + os.urandom(256 - len(FLAG)))
assert m < n
enc = pow(m, e, n)
print(n)
print(e)
print(enc)
while True:
    inp = int(input().strip())
    pt = pow(inp, d, n)
    print(pt % 3)
```
:::

## Recon
這一題是變形過的Lease Significant Bit，上課教的例子是mod 2下的結果，而看source code可以知道目前他是mod 3下的結果，但換湯不換藥，只要把上課教的部分全部換成mod 3就可以了

1. 首先計算$3^{-1},3^{-2},3^{-3},3^{-4},...,3^{-(log_3^n)}\ (mod\ 3)$，並建立一個table
2. 依序執行上課教的流程
    1. 密文*$(3^{-1})^e$
    2. 合併要減掉的部分，也就是把之前已知道所有部分都乘以table上對應的反元素
    3. 再把oracle回傳的假明文減掉上面合併的部分(記得mod)，就是我們要的bit

## Exploit
:::spoiler Whole Scrip
```python
from pwn import remote
from Crypto.Util.number import long_to_bytes, inverse
from math import log
proc = remote("edu-ctf.zoolab.org", 10005)
n, e, enc = proc.recvlines(3)
n = int(n.decode())
e = int(e.decode())
enc = int(enc.decode())
print(f"n is {n}")
print(f"e is {e}")
mult = inverse(pow(3, e, n), n)
msg = enc
pt = []

pow_3_inv_tbl = [ pow(3, -i, n) for i in range(int(log(n, 3))) ]

for i in range(int(log(n, 3))):
    proc.sendline(str(msg).encode())
    res = int(proc.recvline().strip())
    sub = 0
    for idx, p in enumerate(pt):
        sub = (sub + ((p * pow_3_inv_tbl[i-idx]) % n)) % n
    pt.append((res - sub) %3)
    if i % 100 == 0:
        print(long_to_bytes(int("".join([str(p) for p in pt][::-1]), 3)))
    msg = (msg * mult) % n
    
print(long_to_bytes(int("".join([str(p) for p in pt][::-1]), 3)))
```
:::