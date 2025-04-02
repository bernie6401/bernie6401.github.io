---
title: Simple Crypto - 0x09(2023 Lab - signature)
tags: [CTF, Crypto, eductf]

---

# Simple Crypto - 0x09(2023 Lab - signature)
## Background
[ [edu-ctf 2023] week03 - crypto2 - ECDSA](https://www.youtube.com/live/u4ZVc8PuJC0?si=ychlqdZnGVfFYRAV&t=4075)
>![](https://hackmd.io/_uploads/ryVbmdMWp.png)
>
>![](https://hackmd.io/_uploads/HkJMXOG-T.png)

## Source code
:::spoiler Source Code
```python=
from random import randint
from Crypto.Util.number import *
from hashlib import sha256
from ecdsa import SECP256k1
from ecdsa.ecdsa import Public_key, Private_key, Signature
from secret import FLAG

E = SECP256k1
G, n = E.generator, E.order

d = randint(1, n)
k = randint(1, n)
pubkey = Public_key(G, d*G)
prikey = Private_key(pubkey, d)
print(f'P = ({pubkey.point.x()}, {pubkey.point.y()})')

for _ in range(3):
    print('''
1) Request for Signature
2) Check the Permission
3) exit''')
    option = input()
    if option == '1':
        msg = input('What do you want? ')
        if msg == 'Give me the FLAG.':
                print('No way!')
        else:
            h = sha256(msg.encode()).digest()
            # k = k * 1337 % n
            sig = prikey.sign(bytes_to_long(h), k)
            print(f'sig = ({sig.r}, {sig.s})')

    elif option == '2':
        msg = 'Give me the FLAG.'
        r = input('r: ')
        s = input('s: ')
        h = bytes_to_long(sha256(msg.encode()).digest())
        verified = pubkey.verifies(h, Signature(int(r), int(s)))
        if verified:
            print(FLAG)
        else:
            print('Bad signature')
    else:
        print("bye~")
        break


```
:::
## Recon
這一題主要就是利用上課提到的nonce $k$不隨機的問題，因為$k$只能用一次，也就代表他需要夠隨機，如果像LCG這樣的psudo random generator產生的話，一但被compromise，就會被推導出private key $d$，而這個lab就是有這樣的問題
1. 觀察source code會發現不同的nonce $k$之間會產生一個1337倍數的關係，然後如果request `Give me the FLAG.`的signature會被拒絕，所以只能自己產生`Give me the FLAG.`的signature再丟給server檢查，如果過了就可以拿到flag，但重點是要怎麼偽造signature假裝是server簽的?就是要想辦法拿到server產生的private key $d$，可以詳細看一下source code中提到，通常public key都一樣，所以重點是$d$才能產生private key，然後用private key簽署message
    ```python
    E = SECP256k1
    G, n = E.generator, E.order
    d = randint(1, n)
    pubkey = Public_key(G, d*G)
    prikey = Private_key(pubkey, d)
    ↓
    sig = prikey.sign(bytes_to_long(h), k)
    ```
2. 已知(題目給的部分)
    只要我們給兩次要簽章的message，總共可以得到以下資訊
    $$
    coordinate\ (x_0,\ y_0),\\
    hash\ H_1,\ hash\ H_2,\\
    signature\ (s_1,\ r_1),\ (s_2,\ r_2)
    $$
3. 推導
    假設$msg=b'a'$
    $$
    H_1 = H_2 = sha256(msg)\\
    \begin{aligned}
    k_1 &= {s_1}^{-1} \cdot (H_1 + d\cdot r_1)={s_1}^{-1} \cdot H_1 + d\cdot r_1 \cdot {s_1}^{-1}\\
    k_2 &= {s_2}^{-1} \cdot (H_2 + d\cdot r_2) = 1337\times k_1=\\
    &= {s_2}^{-1} \cdot H_2 + {s_2}^{-1}\cdot d\cdot r_2\\
    &= 1337 \cdot {s_1}^{-1} \cdot H_1 + 1337 \cdot d\cdot r_1 \cdot {s_1}^{-1}
    \end{aligned}\\
    \downarrow \\
    d\cdot (H_2\cdot {s_2}^{-1} - 1337\cdot H_1\cdot {s_1}^{-1})=1337\cdot r_1\cdot {s_1}^{-1}-r_2\cdot {s_2}^{-1}\\
    \hookrightarrow d = {1337\cdot r_1\cdot {s_1}^{-1}-r_2\cdot {s_2}^{-1} \over H_2\cdot {s_2}^{-1} - 1337\cdot H_1\cdot {s_1}^{-1}}
    $$
4. 得到原本的private key $d$之後就可以直接選一個亂數nonce $k$，然後重新自己簽署`Give me the FLAG.`的signature
## Exploit
:::spoiler Whole Exploit
```python=
from pwn import *
from Crypto.Util.number import *
from hashlib import sha256
from ecdsa import SECP256k1
from ecdsa.ecdsa import Public_key, Private_key, Signature

# r = process(["python", "./signature_416666d57b34123f.py"])
r = remote('10.113.184.121', 10033)

# Receive Some Info from Server
msg = 'a'
E = SECP256k1
G, n = E.generator, E.order
r.recvuntil(b'P = (')
x, y = r.recvline().decode().strip().rstrip(')').split(', ')
r.recvlines(3)
r.sendline(b'1')
r.sendlineafter(b'What do you want?', msg.encode())
r.recvuntil(b'sig = (')
r1, s1 = r.recvline().decode().strip().rstrip(')').split(', ')
r.recvlines(3)
r.sendline(b'1')
r.sendlineafter(b'What do you want?', msg.encode())
r.recvuntil(b'sig = (')
r2, s2 = r.recvline().decode().strip().rstrip(')').split(', ')

log.info(f'x = {x}\ny = {y}')
log.info(f'r1 = {r1}\ns1 = {s1}')
log.info(f'r2 = {r2}\ns2 = {s2}')

# Calculte Private Key - d
hash_msg = sha256(msg.encode()).digest()
inv_s1 = inverse(int(s1), n)
inv_s2 = inverse(int(s2), n)
hash_msg_decimal = bytes_to_long(hash_msg)
r1 = int(r1)
r2 = int(r2)
d = inverse(1337 * r1 * inv_s1 - r2 * inv_s2, n) * (hash_msg_decimal * inv_s2 - 1337 * hash_msg_decimal * inv_s1)
k1 = inv_s1 * (hash_msg_decimal + d * r1)
k2 = inv_s2 * (hash_msg_decimal + d * r2)
assert k2 % n == k1 * 1337 % n

# Forgery Signature & Send it
k = randint(1, n)
pubkey = Public_key(G, d*G)
prikey = Private_key(pubkey, d)
flag_msg = 'Give me the FLAG.'
flag_msg_h = sha256(flag_msg.encode()).digest()
sig = prikey.sign(bytes_to_long(flag_msg_h), k)
r.recvlines(3)
r.sendline(b'2')
r.sendlineafter(b'r: ', sig.r.digits().encode())
r.sendlineafter(b's: ', sig.s.digits().encode())
flag = r.recvline().strip().decode()

log.info(f'Flag: {flag}')

r.close()
:::

```bash
$ python exp.py
[+] Opening connection to 10.113.184.121 on port 10033: Done
[*] x = 80833128996081892656118221427167942614367970190999112028100047868271602908158
    y = 7692760766381285656486680270900861598977131934640663688795645395086394523342
[*] r1 = 57205296794452689467192257573140114834242454684651993799259557149551452463654
    s1 = 46076932900642565773729561332617152693574412598169577544559584675273278539735
[*] r2 = 32274988576741840972950688950377038880296385056439434547263507357520953909449
    s2 = 38964710627625045025023640822136515580011444306594995093726779755542228691436
[*] Flag: b'FLAG{EphemeralKeyShouldBeRandom}'
[*] Closed connection to 10.113.184.121 port 10033
```

Flag: `FLAG{EphemeralKeyShouldBeRandom}`