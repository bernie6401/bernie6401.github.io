---
title: PicoCTF - Dachshund Attacks
tags: [PicoCTF, CTF, Crypto]

category: "Security/Practice/PicoCTF/Crypto/RSA"
---

# PicoCTF - Dachshund Attacks
###### tags: `PicoCTF` `CTF` `Crypto`

## Background
How about if the private key is too small? Refer [Extending Wiener’s Attack ](https://ctf-wiki.org/crypto/asymmetric/rsa/d_attacks/rsa_extending_wiener/)

## Exploit - Small Private Key
1. git clone https://github.com/pablocelayes/rsa-wiener-attack
Put the exploit file in this repo.
2. Whole Exploit
    ```python
    from pwn import *
    from Crypto.Util.number import long_to_bytes
    import ContinuedFractions, Arithmetic


    context.arch = 'amd64'
    r = remote("mercury.picoctf.net", 37455)

    def wiener_hack(e, n):
        # firstly git clone https://github.com/pablocelayes/rsa-wiener-attack.git !
        frac = ContinuedFractions.rational_to_contfrac(e, n)
        convergents = ContinuedFractions.convergents_from_contfrac(frac)
        for (k, d) in convergents:
            if k != 0 and (e * d - 1) % k == 0:
                phi = (e * d - 1) // k
                s = n - phi + 1
                discr = s * s - 4 * n
                if (discr >= 0):
                    t = Arithmetic.is_perfect_square(discr)
                    if t != -1 and (s + t) % 2 == 0:
                        print("Hacked!")
                        return d
        return False

    r.recvline()
    e = int(str(r.recvline().strip().decode()).split(" ")[-1])
    n = int(str(r.recvline().strip().decode()).split(" ")[-1])
    c = int(str(r.recvline().strip().decode()).split(" ")[-1])

    d = wiener_hack(e, n)
    print(long_to_bytes(pow(c, d, n)))

    r.interactive()
    ```

## Reference
[CTF_RSA解密学习指南(三) - 低解密指数攻击](https://zhuanlan.zhihu.com/p/76228394)