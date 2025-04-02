---
title: PicoCTF - AES-ABC
tags: [PicoCTF, CTF, Crypto]

---

# PicoCTF - AES-ABC
###### tags: `PicoCTF` `CTF` `Crypto`

## Background
[What is PPM file?](https://www.adobe.com/tw/creativecloud/file-types/image/raster/ppm-file.html)

## Source code
:::spoiler Source Code
```python=
#!/usr/bin/env python

from Crypto.Cipher import AES
from key import KEY
import os
import math

BLOCK_SIZE = 16
UMAX = int(math.pow(256, BLOCK_SIZE))


def to_bytes(n):
    s = hex(n)
    s_n = s[2:]
    if 'L' in s_n:
        s_n = s_n.replace('L', '')
    if len(s_n) % 2 != 0:
        s_n = '0' + s_n
    decoded = s_n.decode('hex')

    pad = (len(decoded) % BLOCK_SIZE)
    if pad != 0: 
        decoded = "\0" * (BLOCK_SIZE - pad) + decoded
    return decoded


def remove_line(s):
    # returns the header line, and the rest of the file
    return s[:s.index('\n') + 1], s[s.index('\n')+1:]


def parse_header_ppm(f):
    data = f.read()

    header = ""

    for i in range(3):
        header_i, data = remove_line(data)
        header += header_i

    return header, data
        

def pad(pt):
    padding = BLOCK_SIZE - len(pt) % BLOCK_SIZE
    return pt + (chr(padding) * padding)


def aes_abc_encrypt(pt):
    cipher = AES.new(KEY, AES.MODE_ECB)
    ct = cipher.encrypt(pad(pt))

    blocks = [ct[i * BLOCK_SIZE:(i+1) * BLOCK_SIZE] for i in range(len(ct) / BLOCK_SIZE)]
    iv = os.urandom(16)
    blocks.insert(0, iv)
    
    for i in range(len(blocks) - 1):
        prev_blk = int(blocks[i].encode('hex'), 16)
        curr_blk = int(blocks[i+1].encode('hex'), 16)

        n_curr_blk = (prev_blk + curr_blk) % UMAX
        blocks[i+1] = to_bytes(n_curr_blk)

    ct_abc = "".join(blocks)
 
    return iv, ct_abc, ct


if __name__=="__main__":
    with open('flag.ppm', 'rb') as f:
        header, data = parse_header_ppm(f)
    
    iv, c_img, ct = aes_abc_encrypt(data)

    with open('body.enc.ppm', 'wb') as fw:
        fw.write(header)
        fw.write(c_img)

```
:::
## Recon
這一題也蠻有趣的，可以先看一下他怎麼加密的
1. 先把ppm file的header, data parse出來
2. 在51行用AES-ECB加密data，而我們知道ECB mode就很不安全
3. 在53行再把每一個block分出來並在開頭的地方插入initial vector
4. 57-62行的for-loop，就是把兩個block相加再mod UMAX就是對應的下一個block的值，意即:
$$
c[0] \leftarrow Initial\ Vector=AES[0]\\
c[i+1] \leftarrow (AES[i+1]+c[i])\ \% \ 2^{128}\\
k*2^{128} \leftarrow AES[i+1]+c[i]-c[i+1],\ k \in \{0,1\}, \{AES[\ ], c[\ ]\} \in 2^{128}
$$
所以綜上所述，我們可以把ciphertext還原成AES的版本，這樣應該可以看到flag的一些資訊，即使不知道一開始的key也可以(從最後面的block算回來)
$$
AES[i] \leftarrow k*2^{128}-c[i-1]+c[i]
$$


## Exploit
```python=
#!/usr/bin/env python

from Crypto.Cipher import AES
# from key import KEY
import os
import math

BLOCK_SIZE = 16
UMAX = int(math.pow(256, BLOCK_SIZE))


def to_bytes(n):
    s = hex(n)
    s_n = s[2:]
    if 'L' in s_n:
        s_n = s_n.replace('L', '')
    if len(s_n) % 2 != 0:
        s_n = '0' + s_n
    decoded = bytes.fromhex(s_n)#s_n.decode('hex')

    pad = (len(decoded) % BLOCK_SIZE)
    if pad != 0: 
        decoded = b"\0" * (BLOCK_SIZE - pad) + decoded
    return decoded


def remove_line(s):
    # returns the header line, and the rest of the file
    return s[:s.index(b'\n') + 1], s[s.index(b'\n')+1:]


def parse_header_ppm(f):
    data = f.read()

    header = b""

    for i in range(3):
        header_i, data = remove_line(data)
        header += header_i

    return header, data
        

def pad(pt):
    padding = BLOCK_SIZE - len(pt) % BLOCK_SIZE
    return pt + (chr(padding) * padding)


def abc_decrypt(ct):
    blocks = [ct[i * BLOCK_SIZE:(i+1) * BLOCK_SIZE] for i in range(len(ct) // BLOCK_SIZE)]

    k = 0
    for idx in range(len(blocks)-1, 0, -1):
        curr_blk = int(blocks[idx].hex(), 16)
        prev_blk = int(blocks[idx-1].hex(), 16)
        if (k * UMAX + curr_blk - prev_blk) < 0:
            tmp = UMAX + curr_blk - prev_blk
        else:
            tmp = curr_blk - prev_blk

        blocks[idx] = to_bytes(tmp)

    pt_abc = b"".join(blocks)
    return pt_abc

if __name__=="__main__":
    with open('body.enc.ppm', 'rb') as f:
        header, data = parse_header_ppm(f)

    pt_img = abc_decrypt(data)
    
    # iv, c_img, ct = aes_abc_encrypt(data)

    with open('body.dec.ppm', 'wb') as fw:
        fw.write(header)
        fw.write(pt_img)

```
![](https://hackmd.io/_uploads/Hk18swavh.png)
Flag: `picoCTF{d0Nt_r0ll_yoUr_0wN_aES}`

## Reference
[AES-ABC Write up](https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/AES-ABC.md)