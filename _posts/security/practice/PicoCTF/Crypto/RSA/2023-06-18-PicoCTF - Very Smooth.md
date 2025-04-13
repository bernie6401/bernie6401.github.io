---
title: PicoCTF - Very Smooth
tags: [PicoCTF, CTF, Crypto]

category: "Security/Practice/PicoCTF/Crypto/RSA"
---

# PicoCTF - Very Smooth
###### tags: `PicoCTF` `CTF` `Crypto`

## Background
[$p-1$ Smooth](https://ctf-wiki.org/crypto/asymmetric/rsa/rsa_module_attack/#p-1)

## Source code
:::spoiler Source Code
```python=
#!/usr/bin/python

from binascii import hexlify
from gmpy2 import *
import math
import os
import sys

if sys.version_info < (3, 9):
    math.gcd = gcd
    math.lcm = lcm

_DEBUG = False

FLAG  = open('flag.txt').read().strip()
FLAG  = mpz(hexlify(FLAG.encode()), 16)
SEED  = mpz(hexlify(os.urandom(32)).decode(), 16)
STATE = random_state(SEED)

def get_prime(state, bits):
    return next_prime(mpz_urandomb(state, bits) | (1 << (bits - 1)))

def get_smooth_prime(state, bits, smoothness=16):
    p = mpz(2)
    p_factors = [p]
    while p.bit_length() < bits - 2 * smoothness:
        factor = get_prime(state, smoothness)
        p_factors.append(factor)
        p *= factor

    bitcnt = (bits - p.bit_length()) // 2

    while True:
        prime1 = get_prime(state, bitcnt)
        prime2 = get_prime(state, bitcnt)
        tmpp = p * prime1 * prime2
        if tmpp.bit_length() < bits:
            bitcnt += 1
            continue
        if tmpp.bit_length() > bits:
            bitcnt -= 1
            continue
        if is_prime(tmpp + 1):
            p_factors.append(prime1)
            p_factors.append(prime2)
            p = tmpp + 1
            break

    p_factors.sort()

    return (p, p_factors)

e = 0x10001

while True:
    p, p_factors = get_smooth_prime(STATE, 1024, 16)
    if len(p_factors) != len(set(p_factors)):
        continue
    # Smoothness should be different or some might encounter issues.
    q, q_factors = get_smooth_prime(STATE, 1024, 17)
    if len(q_factors) != len(set(q_factors)):
        continue
    factors = p_factors + q_factors
    if e not in factors:
        break

if _DEBUG:
    import sys
    sys.stderr.write(f'p = {p.digits(16)}\n\n')
    sys.stderr.write(f'p_factors = [\n')
    for factor in p_factors:
        sys.stderr.write(f'    {factor.digits(16)},\n')
    sys.stderr.write(f']\n\n')

    sys.stderr.write(f'q = {q.digits(16)}\n\n')
    sys.stderr.write(f'q_factors = [\n')
    for factor in q_factors:
        sys.stderr.write(f'    {factor.digits(16)},\n')
    sys.stderr.write(f']\n\n')

n = p * q

m = math.lcm(p - 1, q - 1)
d = pow(e, -1, m)

c = pow(FLAG, e, n)

print(f'n = {n.digits(10)}')
print(f'c = {c.digits(10)}')

```
:::

```bash
n = 4f7aa864f662a42a92220e372f5ff25a142aef26106a0dbdf573a66594966ac5dd03848745bb6a80402cad7ac6f2bf93f9ed840edd9c157dfd5d265ce2403e155a29666df8f9b98167ad2452e5a63fd0b7b14ffe966db60c6e2c65b0f602f5c22eb030c0335187759909abd4df622118c23463bcc42650e0a7761257452bf40069ca50dbe0c922d8823a9dcc4231b3952d31d1e977cb520528c6a450405f2a2ee6134db8c61ceb4478a647b0469712cc4f3d1369ef3dfd3d876a2c77bac5a149ccf3723a6e8c3ba1deb0675f25def8da9de2b3ac8b3e38d5ac5c9736b9af087b3fc53450136428e07d58fbc00f6609a4cc14eb0a13a7e76056a241256e03e95d
c = e41a61908eb48b85dc78975c288e62a271b1f237fdc958162727d2930b9af850e908137655c5955a078ff1aa63f5509fbaf79d179d24d209a061c36e0709437b8d2641f41d354bdea062084ea3be8637ed1c4bd8cf63d16c942976dd9d6188fc5e419afae17493d7cdb93d84052637d15e7fa1f852f4f5d786c86bfd024df0dfcf8431e7230cfbbce76a1835b178020ef839af42c377706918a50aac56f79285d743f4a177425eb00eaeb2bebe99343911ab653fe64bb61e140153b113f8554fe29561756fafc7460683d59dd3ee50eb48b718443b9f49e663b6dd02b0a15297468ec30a4f487e328103cdbc59d1d66fc4f03ef75ae45d6ce2035fdfaeb86b7
```

## Recon
相關的證明可以直接看背景知識的連結，但還是可以分析一下Source Code
* 55-65行先產生$p$和$q$，產生的方式是call get_smooth_prime function
* 詳細進去看會發現26-29行有一個while loop是產生基本的$p$，而產生prime number的bit length被設定在$2^{15}$，而跳出loop的條件是$p_1*p_2*p_3*p_4*...=p$的bit length大於$1024-2*16=992$，所以此時的$p$已經是一個smooth value
* 接著看下面的while loop，發現會先產生兩個prime，而且entropy也很低，只有10多個bits而已，而跳出while loop的條件是第43行的判斷式，當$p=p * prime_1 * prime_2+1$是質數時就會跳出來，而這也符合一開始的解題思路，就是<font color="FF0000">$p-1$是smooth value</font>

## Exploit - $p-1$ Smooth
```python=
from gmpy2 import *
from Crypto.Util.number import long_to_bytes

a = 2
n = 2
N = "4f7aa864f662a42a92220e372f5ff25a142aef26106a0dbdf573a66594966ac5dd03848745bb6a80402cad7ac6f2bf93f9ed840edd9c157dfd5d265ce2403e155a29666df8f9b98167ad2452e5a63fd0b7b14ffe966db60c6e2c65b0f602f5c22eb030c0335187759909abd4df622118c23463bcc42650e0a7761257452bf40069ca50dbe0c922d8823a9dcc4231b3952d31d1e977cb520528c6a450405f2a2ee6134db8c61ceb4478a647b0469712cc4f3d1369ef3dfd3d876a2c77bac5a149ccf3723a6e8c3ba1deb0675f25def8da9de2b3ac8b3e38d5ac5c9736b9af087b3fc53450136428e07d58fbc00f6609a4cc14eb0a13a7e76056a241256e03e95d"
e = 65537
c = "e41a61908eb48b85dc78975c288e62a271b1f237fdc958162727d2930b9af850e908137655c5955a078ff1aa63f5509fbaf79d179d24d209a061c36e0709437b8d2641f41d354bdea062084ea3be8637ed1c4bd8cf63d16c942976dd9d6188fc5e419afae17493d7cdb93d84052637d15e7fa1f852f4f5d786c86bfd024df0dfcf8431e7230cfbbce76a1835b178020ef839af42c377706918a50aac56f79285d743f4a177425eb00eaeb2bebe99343911ab653fe64bb61e140153b113f8554fe29561756fafc7460683d59dd3ee50eb48b718443b9f49e663b6dd02b0a15297468ec30a4f487e328103cdbc59d1d66fc4f03ef75ae45d6ce2035fdfaeb86b7"
c = int(c, 16)
N = int(N, 16)
while True:
    a = powmod(a, n, N)
    res = gcd(a-1, N)
    if res != 1 and res != N:
        q = N // res
        d = invert(e, (res-1)*(q-1))
        m = powmod(c, d, N)
        print(bytes.fromhex('{:x}'.format(m)).decode('utf-8'))
        break
    n += 1

```

## Reference
[$p-1$ Smooth](https://ctf-wiki.org/crypto/asymmetric/rsa/rsa_module_attack/#p-1)