---
title: Simple Crypto - 0x04(2023 Lab - POA)
tags: [CTF, Crypto, eductf]

---

# Simple Crypto - 0x04(2023 Lab - POA)
## Background
[ Crypto I - Timmy](https://youtu.be/dYyNeMeDM20?si=BEvBPBzCsg8oWv_Q&t=8317)

## Source Code
:::spoiler Source Code
```python
#! /usr/bin/python3
from Crypto.Cipher import AES
import os

from secret import FLAG

def pad(data, block_size):
    data += bytes([0x80] + [0x00] * (15 - len(data) % block_size))
    return data
# padding style: <oooooo[0x80][0x00]...[0x00]> (find first [0x80])

def unpad(data, block_size):
    if len(data) % block_size:
        raise ValueError

    padding_len = 0
    for i in range(1, len(data) + 1):
        if data[-i] == 0x80:
            padding_len = i
            break
        elif data[-i] != 0x00:
            raise ValueError
    else:
        raise ValueError

    return data[:-padding_len]

key = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC)
ct = cipher.encrypt(pad(FLAG, AES.block_size))
iv = cipher.iv
print((iv + ct).hex())

# same encryption

while True:
    try:
        inp = bytes.fromhex(input().strip()) # hex style input
        iv, ct = inp[:16], inp[16:] # get first 16 bytes from input 
        cipher = AES.new(key, AES.MODE_CBC, iv) 
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        print("Well received :)")
    except ValueError:
        print("Something went wrong :(")

```
:::

## Recon
這一題是簡單的padding oracle attack，他一樣是應用在CBC mode上，只是他padding的方式和上課教的有一點不一樣，他會先在最後放一個0x80然後接續放0x00直到長度%16==0，同樣的，我們可以用上課教的方式:
* What we have: 我們有的東西就是密文，所以可以利用它動一些手腳
* Our Goal 1: 目標是要取得原本和47進行XOR的數字是多少
* Our Goal 2: 這樣才可以取得最後的明文69
![](https://hackmd.io/_uploads/r1p3yoGlp.png)
* How to achieve: 我們可以簡單猜一個byte，從0x00開始，把密文換成猜測的byte，這樣256種組合和原本的Goal 1所求的byte進行XOR後會padding正確(也就是0x01)，此時假設我們已經猜到目前是0x2f符合padding正確的目標，代表現在的假明文是0x01，則原本和0x47進行XOR的數字就是0x01⊕0x2f，然後我們就可以回到原本解密的流程，也就是原本的密文0x47⊕剛剛得知的(0x01⊕0x2f)，就會得到想要的正確的明文0x69
![](https://hackmd.io/_uploads/H1yKboMlp.png)

所以套用到今天的lab意思也是一樣，如果要知道padding是否正確可以問oracle，反正只要符合明文+0x80+(0...15)\*0x00，這一題的flag長度可以從題目給的ciphertext看出來，顯然扣掉16bytes的initial vector後，flag的長度是32 bytes，也就是說我們從第二個block開始解，我們可以單獨把第一個ciphertext block當成第二個ciphertext block的initial vector，合併後再一起送出去，然後不斷變化IV的最後一個byte，如果oracle回傳`Well received :)`代表第一個bytes猜對了，我們就可以把flag的最後一個bytes求出來$\to$我們猜的byte⊕原本ciphertext的最後一個byte⊕0x80(0x80是我們判斷padding正確的依據)，當然找到真正的plaintext byte後要把我們猜測的block恢復原狀，接著繼續找下一個byte
## Exploit
:::spoiler Whole Exploit Script
```python
import sys
from pwn import *
from tqdm import trange

p = remote('edu-ctf.zoolab.org',10004)
# p = process(['python', './POA_4af88990ab364609.py'])

ct = p.readline()[:-1].decode()
ct = bytes.fromhex(ct)
iv, ct1, ct2 = ct[:16], ct[16:32], ct[32:48]
flag = bytearray(32) 
index = 31

count1 = 0
_iv, _ct1, _ct2 = bytearray(ct[:16]), bytearray(ct[16:32]), bytearray(ct[32:48])
for i in range(15, -1, -1):
    count2 = count1
    count1 = 0
    for j in range(256):
        _ct1[i] = j
        p.sendline(bytearray.hex(_ct1+_ct2).encode())
        reply = p.readline()[:-1].decode()
        if reply == 'Well received :)':
            count1 += 1
            if j != ct1[i]:
                flag[index] = ct1[i] ^ _ct1[i] ^ 128

    if abs(count1 - count2) == 1:
        flag[index] = 128
    _ct1[i] = 0 ^ flag[index] ^ ct1[i]
    index -= 1

_iv, _ct1, _ct2 = bytearray(ct[:16]), bytearray(ct[16:32]), bytearray(ct[32:48])
for i in range(15, -1, -1):
    for j in range(256):
        _iv[i] = j
        p.sendline(bytearray.hex(_iv+_ct1).encode())
        reply = p.readline()[:-1].decode()
        if reply == 'Well received :)':
            flag[index] = _iv[i] ^ iv[i] ^ 128
            break
    _iv[i] = 0 ^ flag[index] ^ iv[i]
    index -= 1

print(bytes(flag))
```
:::