---
title: PicoCTF - Transformation
tags: [PicoCTF, CTF, Reverse]

category: "Security Practice｜PicoCTF｜Reverse"
date: 2023-06-18
---

# PicoCTF - Transformation
<!-- more -->
###### tags: `PicoCTF` `CTF` `Reverse`
Challenge: [Transformation](https://play.picoctf.org/practice/challenge/104?category=3&page=1)

## Source code
enc file content: `灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸彥㜰㍢㐸㙽`
Transformation Code
```python!
''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])
```
Seems it shift the first character with 8 bits and concatenate the 2nd character then go through `len(flag)`

## Exploit
My perspective is just recover the strings
:::spoiler
```python=
flag = '灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸彥㜰㍢㐸㙽'
enc = ''

def decimalToBinary(n):
    return bin(n).replace("0b", "")

def binToHexa(n):
    bnum = int(n)
    temp = 0
    mul = 1
    count = 1
    hexaDeciNum = ['0'] * 100
    i = 0
    while bnum != 0:
        rem = bnum % 10
        temp = temp + (rem*mul)
        if count % 4 == 0:
            if temp < 10:
                hexaDeciNum[i] = chr(temp+48)
            else:
                hexaDeciNum[i] = chr(temp+55)
            mul = 1
            temp = 0
            count = 1
            i = i+1
        else:
            mul = mul*2
            count = count+1
        bnum = int(bnum/10)
    if count != 1:
        hexaDeciNum[i] = chr(temp+48)
    if count == 1:
        i = i-1
    hex_string = ''
    while i >= 0:
        hex_string += hexaDeciNum[i]
        i = i-1
    return hex_string


for i in range(0, len(flag)):
    plaintext1 = decimalToBinary(ord(flag[i]))
    while(len(plaintext1) != 16):
        plaintext1 = '0' + plaintext1
    plaintext2 = plaintext1[-8:]
    plaintext1 = plaintext1[0:8]
    enc += binToHexa(plaintext1)
    enc += binToHexa(plaintext2)
print(bytes.fromhex(enc).decode('utf-8'))
```
:::