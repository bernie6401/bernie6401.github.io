---
title: PicoCTF - Mind your Ps and Qs
tags: [PicoCTF, CTF, Crypto]

---

# PicoCTF - Mind your Ps and Qs
###### tags: `PicoCTF` `CTF` `Crypto`
Challenge: [Mind your Ps and Qs](https://play.picoctf.org/practice/challenge/162?category=2&page=1)

## Background
[RSA (觀念篇) ](https://ithelp.ithome.com.tw/articles/10250721)

## Source code
```txt
Decrypt my super sick RSA:
c: 421345306292040663864066688931456845278496274597031632020995583473619804626233684
n: 631371953793368771804570727896887140714495090919073481680274581226742748040342637
e: 65537
```
## Exploit - Find P & Q By [Online Tool](https://www.alpertron.com/ECM.HTM)
1. Find P & Q
Use online tool to do prime factorize on `n`
p $\to$ 1461849912200000206276283741896701133693
q $\to$ 431899300006243611356963607089521499045809

2. Write exploit
    ```python!
    e = 65537
    M = 631371953793368771804570727896887140714061729769155038068711341335911329840163136
    k = 1
    # p = 1461849912200000206276283741896701133693
    # q = 431899300006243611356963607089521499045809

    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x-(b//a)*y, y)

    def modinv(a, m):
        g, x, y = egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

    while(True):
        if (1 + k * M) % e == 0:
            print('k = ', k, ' and d = ', (1 + k * M) / e)
            break
        else:
            k += 1

    d = modinv(e, M)
    c = 421345306292040663864066688931456845278496274597031632020995583473619804626233684
    n = 631371953793368771804570727896887140714495090919073481680274581226742748040342637
    plain = pow(c, d, n)
    print(plain)
    print(hex(plain))
    print(bytearray.fromhex(hex(plain)[2:]))
    ```

## Reference
[picoCTF 2021 Mind your Ps and Qs](https://youtu.be/-ixz-2gi9r0)