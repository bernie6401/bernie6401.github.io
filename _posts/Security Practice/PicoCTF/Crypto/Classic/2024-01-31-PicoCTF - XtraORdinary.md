---
title: PicoCTF - XtraORdinary
tags: [PicoCTF, CTF, Crypto]

category: "Security Practice｜PicoCTF｜Crypto｜Classic"
date: 2024-01-31
---

# PicoCTF - XtraORdinary
<!-- more -->

## Background
[How to Convert Hex String to Bytes in Python?](https://blog.finxter.com/how-to-convert-hex-string-to-bytes-in-python/)
[Python 好用模組介紹 - itertools & more-itertools](https://myapollo.com.tw/blog/python-itertools-more-itertools/)
[Python File readline() Method](https://www.w3schools.com/python/ref_file_readline.asp)
[Python append to a file](https://www.geeksforgeeks.org/python-append-to-a-file/)

## Source code
:::spoiler Source Code
```python=
#!/usr/bin/env python3

from random import randint
with open('flag.txt', 'rb') as f:
    flag = f.read()

with open('secret-key.txt', 'rb') as f:
    key = f.read()

def encrypt(ptxt, key):
    ctxt = b''
    for i in range(len(ptxt)):
        a = ptxt[i]
        b = key[i % len(key)]
        ctxt += bytes([a ^ b])
    return ctxt

ctxt = encrypt(flag, key)

random_strs = [
    b'my encryption method',
    b'is absolutely impenetrable',
    b'and you will never',
    b'ever',
    b'ever',
    b'ever',
    b'ever',
    b'ever',
    b'ever',
    b'break it'
]

for random_str in random_strs:
    for i in range(randint(0, pow(2, 8))):
        for j in range(randint(0, pow(2, 6))):
            for k in range(randint(0, pow(2, 4))):
                for l in range(randint(0, pow(2, 2))):
                    for m in range(randint(0, pow(2, 0))):
                        ctxt = encrypt(ctxt, random_str)

with open('output.txt', 'w') as f:
    f.write(ctxt.hex())
```
:::

## Recon
這一題我覺得出的不錯，首先他把flag和secret-key做XOR，然後做了一大堆random_strs之間的XOR，但我們都知道XOR做了兩次等於沒做，所以最後的output其實就是
$$
flag \oplus key \oplus lots\ of\ random\ string=output
$$
所以如果我們要得到flag首先就是要先把random string的成分拿掉，因為他只有32種結果，也就是
1. `my encryption method`
2. `is absolutely impenetrable`
3. `and you will never`
4. `ever`
5. `break it`

之間的排列組合，進行XOR，然後我們可以用itertools中的combinations method，先把所有組合排出來(這個寫法還不錯，可以學起來)，然後依序把結果存起來，接著我們就要找出key是多少，由於第14行會把key延伸(反正大概就是這個意思)，而我們唯一知道的是最後的flag一定是`picoCTF{`開頭，也就是說這個key有大機率應該只有8個字元，那我們就可以拿前面得到的32種結果，直接和`picoCTF{`進行XOR然後查看一下最後的strings有沒有有意義且長度小於8的，從結果來看，的確有一個`Africa!`的東西印入眼簾，看起來應該就是我們的key，所以我們就可以直接進行最後的XOR得到flag

## Exploit
```python!
from itertools import product
from pwn import *
from itertools import combinations

root_path = "D:/NTU/CTF/PicoCTF/Crypto/XtraORdinary/"
with open(root_path + 'output.txt', 'r') as f:
    cipher = bytes.fromhex(f.read())

temp_pt = open(root_path + 'temp_plaintext.txt', 'a')


def decrypt(ctxt, key):
    ptxt = b''
    for i in range(len(ctxt)):
        a = ctxt[i]
        b = key[i % len(key)]
        ptxt += bytes([a ^ b])
    return ptxt

def sub_lists (l):
    comb = []
    for i in range(1,len(l)+1):
        comb += [list(j) for j in combinations(l, i)]
    return comb

random_strs = [
    b'my encryption method',
    b'is absolutely impenetrable',
    b'and you will never',
    b'ever',
    b'break it'
]
combos = sub_lists(random_strs)


'''
1st Step - Try to xor all combination of random strings
'''
for i in range(len(combos)):
    tmp_cipher = cipher
    for j in range(len(combos[i])):
        # print(combos[i][j])
        tmp_cipher = decrypt(tmp_cipher, combos[i][j])
    # print()
    print(bytes.fromhex(tmp_cipher.hex()).decode('cp437'))
    temp_pt.writelines(tmp_cipher.hex() + '\n')
temp_pt.close()

'''
2nd Step - Try to find key
'''
key = b'picoCTF{'
cipher = open(root_path + 'temp_plaintext.txt', 'r').readlines()
for i in range(len(cipher)):
    ptxt = decrypt(bytes.fromhex(cipher[i].strip()), key)
    print(bytes.fromhex(ptxt.hex()).decode('cp437'))

'''
3rd Step - Find flag
'''
key = b'Africa!'
cipher = open(root_path + 'temp_plaintext.txt', 'r').readlines()
for i in range(len(cipher)):
    ptxt = decrypt(bytes.fromhex(cipher[i].strip()), key)
    if 'picoCTF{' in bytes.fromhex(ptxt.hex()).decode('cp437'):
        print(f"Flag = {bytes.fromhex(ptxt.hex()).decode('cp437')}")
        break
```

## Reference
[pico crypto XtraORdinary wp - partender810](https://partender810.hatenablog.com/entry/2021/05/19/210459#XtraORdinary-150pt)
[XtraORdinary WP - whiteSHADOW1234](https://github.com/whiteSHADOW1234/picoCTF_writeup/blob/main/picoCTF_writeup(11~15page).md#xtraordinary)