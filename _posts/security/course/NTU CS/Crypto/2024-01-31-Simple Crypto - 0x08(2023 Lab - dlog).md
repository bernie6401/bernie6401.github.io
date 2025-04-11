---
title: Simple Crypto - 0x08(2023 Lab - dlog)
tags: [CTF, Crypto, eductf]

category: "Security/Course/NTU CS/Crypto"
---

# Simple Crypto - 0x08(2023 Lab - dlog)
## Background
[ [edu-ctf 2023] week03 - crypto2 ](https://www.youtube.com/live/u4ZVc8PuJC0?si=2wbiGreg_BZQ-dff)
[Cryptography and Network Security – Homework 2 - Little Knowledge Proof](https://hackmd.io/@SBK6401/SJobiaxQ3#5-Little-Knowledge-Proof)
## Source code
:::spoiler Source Code
```python
from Crypto.Util.number import isPrime, bytes_to_long
import os

from secret import FLAG

p = int(input("give me a prime: ").strip())
if not isPrime(p):
    print("Do you know what is primes?")
    exit(0)

if p.bit_length() != 1024:
    print("Bit length need to be 1024")
    exit(0)

g = int(input("give me a number: ").strip())
flag = bytes_to_long(FLAG)

print('The hint about my secret:', pow(g, flag, p))

```
:::
## Recon
基本上這一題和上一個學期上的CNS中，作業二的[Little Knowledge Proof](https://hackmd.io/@SBK6401/SJobiaxQ3#5-Little-Knowledge-Proof)概念一模一樣，當時還不知道這是啥騷操作，現在覺得非常簡單，就是套用了Pohlig-Hellman的原理進行破解

1. 首先看source code需要我們提供一個prime($N$)，然後跟一個不重要的底數$g$，接著題目return一個hint就是$hint=g^{flag}\ mod(N)$，因此按照discrete log的難度，我們很難針對hint進行brute force，縱使我們知道N,g,hint也一樣，但因為N是我們提供的，所以我可以故意給他一個smooth prime，也就是$N-1$是由多個prime相乘而得
2. 我們可以用上課教過的Pohlig-Hellman原理去思考，也就是先把群的範圍縮小，再利用BSGS的方法找到$x_i$，這時雖然得到$x_i$但由於是mod $p_i$的結果，就不是真正的$x$，要利用CRT把多個$x_i$還原成原本的$x$，幸虧以上操作sage都做好了

## Exploit
記得要進入conda中sage的環境，如果沒有的話可以直接創一個: `conda create --name sageenv sage=10.0 -c conda-forge -y`，然後可以直接`python exp.py`也可以直接`sage exp.py`，但重點是`from sage.all import *`是一定要加的，如果要像之前CNS那樣使用Pohlig-Hellman的函數，就一定要另外分開寫一個專門的script，因為他沒辦法相容pwntools的remote method，但可以相容local process，真的有點奇怪。另外sage也沒辦法接受`log.info(f"...")`的語法，所以全部都要換成`print`
```python
from pwn import *
from Crypto.Util.number import *
from sage.all import *

smooth_prime = 2
while True:
    bitLen = smooth_prime.bit_length()
    if bitLen > 1024:
        smooth_prime = 2
    if bitLen == 1024:
        if isPrime(smooth_prime + 1):
            print(smooth_prime+1)
            smooth_prime = smooth_prime + 1
            break
    smooth_prime *= getPrime(10)

r = remote("10.113.184.121", 10032)
# r = process(["python", "dlog_bfc156b3a0eec196.py"])

g = 2
r.recvuntil(b": ")
r.sendline(str(smooth_prime).encode())
r.recvuntil(b'give me a number: ')
r.sendline(str(g).encode())
r.recvuntil(b'The hint about my secret: ')
hint = r.recvline()

print(f'Smooth Prime is: {smooth_prime}')
print("g = 2")
print(f'hint = {hint.decode().strip()}')

flag = discrete_log(Mod(hint, smooth_prime), Mod(g, smooth_prime))
print(f"Flag = {long_to_bytes(flag).decode()}")

r.close()
```