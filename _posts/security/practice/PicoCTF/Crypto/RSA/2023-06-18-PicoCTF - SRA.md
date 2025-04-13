---
title: PicoCTF - SRA
tags: [PicoCTF, CTF, Crypto]

category: "Security/Practice/PicoCTF/Crypto/RSA"
---

# PicoCTF - SRA
<!-- more -->
###### tags: `PicoCTF` `CTF` `Crypto`

## Source code
:::spoiler Source Code
```python=
from Crypto.Util.number import getPrime, inverse, bytes_to_long
from string import ascii_letters, digits
from random import choice

pride = "".join(choice(ascii_letters + digits) for _ in range(16))
gluttony = getPrime(128)
greed = getPrime(128)
lust = gluttony * greed
sloth = 65537
envy = inverse(sloth, (gluttony - 1) * (greed - 1))

anger = pow(bytes_to_long(pride.encode()), sloth, lust)

print(f"{anger = }")
print(f"{envy = }")

print("vainglory?")
vainglory = input("> ").strip()

if vainglory == pride:
    print("Conquered!")
    with open("/challenge/flag.txt") as f:
        print(f.read())
else:
    print("Hubris!")

```
:::

## Recon
這一題也蠻有趣的，有給$e, d, c$，而我們知道$ed\equiv 1\ (mod\ \phi(n))$但目前不知道$n$是多少，這也是這一題比較難的地方，不過仔細看$p, q$的bits range只有128 bits，感覺有機會可以爆破，試想:
$$
e*d-1=\phi(n) * k=(p-1)*(q-1)*k
$$
所以我們只要先用[online tool](https://www.dcode.fr/prime-factors-decomposition)，分析所有的質因數，再暴力破解看可能的$p$有多少就可以了
:::spoiler Screenshot
![](https://hackmd.io/_uploads/BJPyZn3D3.png)
:::

## Exploit
* Note: 使用以下的script，需要利用這個[online tool](https://www.dcode.fr/prime-factors-decomposition)，然後把結果以逗號分開，再用list的方式當作input, e.g. `[2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 5, 7, 17, 19, 151, 2363909, 75519055285493, 6681450981644264152589, 118264780684392418025651473217]`
* Note2: 我寫的script沒辦法處理候選的$p$有三個以上的情況，因為我懶得寫，所以它會自動斷線再重新連線重新計算一次，以我的經驗大約3-4次就可以拿到flag了
```python=
from pwn import *
from itertools import combinations
from Crypto.Util.number import isPrime, inverse, long_to_bytes

context.arch = 'amd64'

# 這個寫法超屌，要學起來，來自Martin Carlisle大大
def sub_lists (l):
    comb = []
    for i in range(1,len(l)+1):
        comb += [list(j) for j in combinations(l, i)]
    return comb

def main():
    r = remote("saturn.picoctf.net", 64350)

    c = int(r.recvline().strip().decode().split(" ")[-1])
    d = int(r.recvline().strip().decode().split(" ")[-1])
    e = 65537
    log.info(f"c = {c}\nd = {d}")

    k_phi = d * e - 1
    print("k_phi = ", k_phi)

    k_phi_factor = eval(input())
    combos = sub_lists(k_phi_factor)

    '''Find (p-1)'''
    primes = set()
    for l in combos:
        product = 1
        # multiply them together to get p-1
        for k in l:
            product = product * k
        if product.bit_length()==128 and isPrime(product+1):
            primes.add(product+1)
    print(primes)

    if len(primes) == 2:
        phi = 1
        n = 1
        for candidate in primes:
            phi *= (candidate - 1)
            n *= candidate


        assert inverse(e, phi) == d
        print(long_to_bytes(pow(c, d, n)))
        r.sendline(long_to_bytes(pow(c, d, n)))
        r.interactive()
        r.close()
        sys.exit(0)

    else:
        r.close()
        return False

if __name__ == '__main__':
    while not main():
        main()
```
Flag: `picoCTF{7h053_51n5_4r3_n0_m0r3_2b7ad1ae}`

## Reference
[picoCTF 2023 SRA](https://youtu.be/3DPWLnrqHZ0)
[PicoCTF: SRA Challenge](https://eshard.com/posts/picoctf-sra-challenge)
[maple3142 - SRA](https://blog.maple3142.net/2023/03/29/picoctf-2023-writeups/#sra)