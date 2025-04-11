---
title: PicoCTF - Double DES
tags: [PicoCTF, CTF, Crypto]

category: "Security > Practice > PicoCTF > Crypto > DES-AES"
---

# PicoCTF - Double DES
###### tags: `PicoCTF` `CTF` `Crypto`

## Background
* Meet in the middle attack

## Source code
:::spoiler
```python=
#!/usr/bin/python3 -u
from Crypto.Cipher import DES
import binascii
import itertools
import random
import string


def pad(msg):
    block_len = 8
    over = len(msg) % block_len
    pad = block_len - over
    return (msg + " " * pad).encode()

def generate_key():
    return pad("".join(random.choice(string.digits) for _ in range(6)))


FLAG = open("flag").read().rstrip()
KEY1 = generate_key()
KEY2 = generate_key()


def get_input():
    try:
        res = binascii.unhexlify(input("What data would you like to encrypt? ").rstrip()).decode()
    except:
        res = None
    return res

def double_encrypt(m):
    msg = pad(m)

    cipher1 = DES.new(KEY1, DES.MODE_ECB)
    enc_msg = cipher1.encrypt(msg)
    cipher2 = DES.new(KEY2, DES.MODE_ECB)
    return binascii.hexlify(cipher2.encrypt(enc_msg)).decode()


print("Here is the flag:")
print(double_encrypt(FLAG))

while True:
    inputs = get_input()
    if inputs:
        print(double_encrypt(inputs))
    else:
        print("Invalid input.")
```
:::

## Recon
The keyspace is small($10^6$), so we can put the encryption plaintext in a dictionary. The complexity is $O(2*10^6)$.

## Exploit
```python=
from pwn import *
from tqdm import tqdm
import ddes
from Crypto.Cipher import DES
from itertools import product


message = ddes.pad(binascii.unhexlify('00').decode())
enc_message = bytes.fromhex("6ee2234a9e61e816")
flag = bytes.fromhex("0446d14e0b7dbd6202a704e86d05747382cc26567449bbebb3ab76f42ce8be4957c2731923859baf")


my_dict = {}
for i in tqdm(product(string.digits, repeat=6), total=10 ** 6):
    key1 = ddes.pad("".join(i))
    cipher1 = DES.new(key1, DES.MODE_ECB)
    enc_msg1 = cipher1.encrypt(message)
    my_dict[enc_msg1] = key1

for j in tqdm(product(string.digits, repeat=6), total=10 ** 6):
    key2 = ddes.pad("".join(j))
    cipher2 = DES.new(key2, DES.MODE_ECB)
    dec_msg2 = cipher2.decrypt(enc_message)
    if dec_msg2 in my_dict:
        cipher1 = DES.new(my_dict[dec_msg2], DES.MODE_ECB)
        print("flag = ", bytes.fromhex(cipher1.decrypt(cipher2.decrypt(flag)).hex()).decode('cp437'))


```

## Reference
[maple3142 - Double DES](https://blog.maple3142.net/2021/03/30/picoctf-2021-writeups/#double-des)