---
title: PicoCTF - corrupt-key-1
tags: [PicoCTF, CTF, Crypto]

category: "Security/Practice/PicoCTF/Crypto/RSA"
---

# PicoCTF - corrupt-key-1
<!-- more -->
###### tags: `PicoCTF` `CTF` `Crypto`

## Source code
* private.key
    ```bash
    -----BEGIN RSA PRIVATE KEY-----
    MIICXAIBAAKBgQC4yxzKmbasQYdsGIRXMqXL/Idd80bukALOYIUItfz2tgpax3Iq
    LWTvdOFEOjOOcKc+Y6MD86ya3xmFlWmfbp8wwAnSGcfZjE7IQgNhCDQCnHlWfvwI
    9mtLw/Vkv7VxVGoGt+SPs1u5zOqaLNRDSfgpJCB436ZNUlknv9VdCZwCTwIDAQAB
    AoGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQQDnAFaP9Qa9WJKv
    klkhJeBsvpvUXf6v6TGjM8E0YwI9TwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAkEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJBAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAACQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
    -----END RSA PRIVATE KEY-----
    ```
* msg.enc
    ```bash
    71dc d160 9ac4 a05c d14f 04a9 b43c 2aa3
    83d2 a8d6 749b b978 75d5 437a a944 45f2
    4073 f605 ef1c 5657 8d0e 7a2d f3be b5c1
    7741 8476 0b3d 44fc b97e 6631 b6fe 2487
    6258 d445 a7d7 4c7c e3cc 00ec f925 f442
    c91d 10c9 cefb 9ca6 9c88 da3c 9d26 6c96
    9033 63d5 6a13 7b64 1fc3 8709 2416 f7fb
    eb4c 4c94 cc8e 157f cc0e d122 159c 27d5
    ```

## Recon
可見private.key的內文被corrupted了，必須要修復才能夠解密ciphertext，但看來看去也找不到相關的write up，或是修復的方法，從[連結](https://connor-mccartney.github.io/cryptography/rsa/corrupt-key-1-picoMini)這篇write up也看不懂如何修復，雖然他有附上code，但是很多error也無法debug(主要是看不懂)，總而言之我們的目標就是找出$p$為何

2023/6/18 更新：有空可以看一下[RSA Private Key Recovery](https://github.com/Mr-Aur0ra/RSA/blob/master/(9)%E7%A7%81%E9%92%A5%E6%96%87%E4%BB%B6%E4%BF%AE%E5%A4%8D/godlikeRSA/fix.py)的code

## Exploit - Recover Private Key File
1. 先看沒有corrupt的部份的訊息為何
    ```bash
    $ openssl rsa -in private.key -text -noout
    RSA Private-Key: (1024 bit, 2 primes)
    modulus:
        00:b8:cb:1c:ca:99:b6:ac:41:87:6c:18:84:57:32:
        a5:cb:fc:87:5d:f3:46:ee:90:02:ce:60:85:08:b5:
        fc:f6:b6:0a:5a:c7:72:2a:2d:64:ef:74:e1:44:3a:
        33:8e:70:a7:3e:63:a3:03:f3:ac:9a:df:19:85:95:
        69:9f:6e:9f:30:c0:09:d2:19:c7:d9:8c:4e:c8:42:
        03:61:08:34:02:9c:79:56:7e:fc:08:f6:6b:4b:c3:
        f5:64:bf:b5:71:54:6a:06:b7:e4:8f:b3:5b:b9:cc:
        ea:9a:2c:d4:43:49:f8:29:24:20:78:df:a6:4d:52:
        59:27:bf:d5:5d:09:9c:02:4f
    publicExponent: 65537 (0x10001)
    privateExponent: 0
    prime1:
        00:e7:00:56:8f:f5:06:bd:58:92:af:92:59:21:25:
        e0:6c:be:9b:d4:5d:fe:af:e9:31:a3:33:c1:34:63:
        02:3d:4f:00:00:00:00:00:00:00:00:00:00:00:00:
        00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:
        00:00:00:00:00
    prime2: 0
    exponent1: 0
    exponent2: 0
    coefficient: 0
    ```
    所以由上可知
    ```bash
    n = 0x00b8cb1cca99b6ac41876c18845732a5cbfc875df346ee9002ce608508b5fcf6b60a5ac7722a2d64ef74e1443a338e70a73e63a303f3ac9adf198595699f6e9f30c009d219c7d98c4ec84203610834029c79567efc08f66b4bc3f564bfb571546a06b7e48fb35bb9ccea9a2cd44349f829242078dfa64d525927bfd55d099c024f
    e = 0x10001
    p = 0xe700568ff506bd5892af92592125e06cbe9bd45dfeafe931a333c13463023d4f0000000000000000000000000000000000000000000000000000000000000000
    ```
2. 由[連結](https://connor-mccartney.github.io/cryptography/rsa/corrupt-key-1-picoMini)提供的code進行修復，雖然這個code很多error也不能work但先假設可以找到$p$
3. 找到$p$就是一個正常的RSA decrypt
    ```python=
    from Crypto.Util.number import *

    n = 0x00b8cb1cca99b6ac41876c18845732a5cbfc875df346ee9002ce608508b5fcf6b60a5ac7722a2d64ef74e1443a338e70a73e63a303f3ac9adf198595699f6e9f30c009d219c7d98c4ec84203610834029c79567efc08f66b4bc3f564bfb571546a06b7e48fb35bb9ccea9a2cd44349f829242078dfa64d525927bfd55d099c024f
    e = 0x10001
    p = 0xe700568ff506bd5892af92592125e06cbe9bd45dfeafe931a333c13463023d4fc25c71b1e8c70d8c28c10fe025474ea96f90887e707f76205565e9e241d571bb
    q = n//p
    d = pow(e, -1, (p-1)*(q-1))
    c = open('msg.enc', 'rb').read()
    c = bytes_to_long(c)
    m = pow(c, d, n)
    print(long_to_bytes(m))
    ```
    ```bash!
    $ python exp-flag.py
    b'\x02\x858\xd4\x05\xd3\xf3Z\xdf!\xffW\x9e\x1ee\xaf\x02+1[8\xc5|t\xc6\x95\xe7\xe3m"/*V\x02\x04\xedZ\xe9Q\x05}/\x999\xce\xb7\xe1\xcc\x9e\xb8W^\xb6\xcd\x05\xa4\xd7xG\x9aI\xe2\x86F\xebW\x00Here is your flag: picoCTF{d741543f172970457e6a9aaa890935b8}'
    ```
# Reference
[corrupt-key-1 Write Up](https://connor-mccartney.github.io/cryptography/rsa/corrupt-key-1-picoMini)