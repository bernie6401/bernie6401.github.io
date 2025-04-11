---
title: PicoCTF - Compress and Attack
tags: [PicoCTF, CTF, Crypto]

category: "Security/Practice/PicoCTF/Crypto"
---

# PicoCTF - Compress and Attack
###### tags: `PicoCTF` `CTF` `Crypto`

## Background
* zlib compression property
詳細說明一下zlib的壓縮特性是當壓縮的內容出現重複字元的時候，壓縮過後的長度會不變
```bash
>>> import zlib
>>> enc = zlib.compress(bytes("picoCTF{picoCTF{testing_123456}".encode("utf-8")))
>>> len(enc)
33
>>> enc = zlib.compress(bytes("picoCTF{tepicoCTF{testing_123456}".encode("utf-8")))
>>> len(enc)
33
>>> enc = zlib.compress(bytes("picoCTF{tekpicoCTF{testing_123456}".encode("utf-8")))
>>> len(enc)
34
```
此時重複的部分就是`picoCTF{`，若是繼續增加重複的部分(例如：`picoCTF{te`)，壓縮後的長度也不會變，這樣就可以當作一個oracle，也就是利用長度來判斷增加的字元是不是flag重複的一部分

## Source code
:::spoiler
```python=
#!/usr/bin/python3 -u

import zlib
from random import randint
import os
from Crypto.Cipher import Salsa20

flag = open("./flag").read()


def compress(text):
    return zlib.compress(bytes(text.encode("utf-8")))

def encrypt(plaintext):
    secret = os.urandom(32)
    cipher = Salsa20.new(key=secret)
    return cipher.nonce + cipher.encrypt(plaintext)

def main():
    while True:
        usr_input = input("Enter your text to be encrypted: ")
        compressed_text = compress(flag + usr_input)
        encrypted = encrypt(compressed_text)
        
        nonce = encrypted[:8]
        encrypted_text =  encrypted[8:]
        print(nonce)
        print(encrypted_text)
        print(len(encrypted_text))

if __name__ == '__main__':
    main()
```
:::

## Recon
這一題很有趣，可以看一下source code發現他特意把`encrypted_text`的長度leak出來當作解題的一部分資訊，透過上述提到的`zlib`特性，可以把這個資訊當成一個oracle
```bash
$ nc mercury.picoctf.net 33976
Enter your text to be encrypted: p
b'0\xc17\x10?%a\xeb'
b"'\xdf\x99\xb0\xd99dvf\xf6\x88\xbfl\xc3\x10\xff\x16,\xf7*\xad\xb3\xb1\xc7\x94\xaam\xc5\xac\xfat^]\x0e\xd8\xfbV\xed\xdd\xf7\xbe\xb0\xed\x8ff\x9e"
46
Enter your text to be encrypted: pi
b'H\x03l\x16\xb12S\xad'
b'\xc4\x0c\xb1\x9e{q\x9e\x93Q\xeb\xa5G\xbb\x01%\xe6\x1d4\x96\xf3\r+C4\x1c\xe9-\x99ghC\x0c\xef\xec\xba\xb1\x1b\xfa\xa2\x16\xda\x00\x85tq\x02@'
47
Enter your text to be encrypted: pic
b'\xa4\x81\x7f\xb6\x9e\xadW\xef'
b"\xd2\xe4\x8a2WY]^0$g\x17\xd0\xe8\xd1\x95\xbd \x9eX+\x06\xf8\xcc\x8e\xa8\xfa\xdf\xb3\xac:k\x15\xdb\xa0#'\xb7\xf7^\x06\xce!it\x11\xdd\xa3"
48
Enter your text to be encrypted: pico
b'<\x06\x8f\x18\xcf\xf3\x91\x11'
b'\x84k\xc9\xf4~\x81\xdar\x9bR\x08\x87K\xb7\x1c\xda\x18\x08+\xc1\xfa\x9c\xce\xe1\x7f\x93\xd9\xe6\xf4Jmv\x08\x9b\xaa\xb4\xc0\xb6\xa6f\xdb\x9acF\x0e\x8eF\x98'
48
Enter your text to be encrypted: picoC
b'\x18\x07\xd4"C\x94\xd8\xfe'
b'g\tWkH\x10\xa4\x8a\x80\xcc\xd8\x94\x02\x08T\x93AV\x0f\x97\xca\x82\xf3\xd1\xd8\xb0\r\xb2\x05\xc6\xbe{\x00\xd8\xc4\xbd\x84\x0fn\x14\xb6\xcf|\x15\xf5\xf2\xf9l'
48
...
```
透過上述測試，可以判斷長度應該就是固定48，此時我們就可以依序加入guessing character，並透過oracle判斷加入的字元是對的還是錯的

## Exploit
```python=
from pwn import *

context.arch = 'amd64'

r = remote("mercury.picoctf.net", 33976)

def oracle(plaintext):
    r.recvuntil(b"Enter your text to be encrypted: ")
    r.sendline(plaintext.encode())
    nonce = r.recvline().strip().hex()
    encrypted_text = r.recvline().strip().hex()
    return r.recvline().strip().decode()


current_char = ""
guessing_flag = "picoCTF{"
fit_length = oracle(guessing_flag)
print(guessing_flag)
while current_char != "}":
    for i in string.printable:
        if oracle(guessing_flag + i) == fit_length:
            print(i)
            guessing_flag += i
            current_char = i
            break
        
print(guessing_flag)
r.close()
```
Flag: `picoCTF{sheriff_you_solved_the_crime}`

## Reference
[maple3142 - compress-and-attack](https://blog.maple3142.net/2021/03/30/picoctf-2021-writeups/#compress-and-attack)
[CompressAndAttack Write up](https://github.com/apoirrier/CTFs-writeups/blob/master/PicoCTF/Crypto/CompressAndAttack.md)