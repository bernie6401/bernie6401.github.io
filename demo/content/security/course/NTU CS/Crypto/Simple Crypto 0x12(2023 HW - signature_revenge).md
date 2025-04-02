---
title: Simple Crypto 0x12(2023 HW - signature_revenge)
tags: [eductf, CTF, Crypto]

---

# Simple Crypto 0x12(2023 HW - signature_revenge)
## Background
![](https://hackmd.io/_uploads/Skf4o1tGp.png)
![](https://hackmd.io/_uploads/B16No1FzT.png)

## Source code
:::spoiler Source Code
```python
from Crypto.Util.number import *
from hashlib import sha256, md5
from ecdsa import SECP256k1
from ecdsa.ecdsa import Public_key, Private_key
from secret import FLAG
import os
E = SECP256k1
G, n = E.generator, E.order
d = bytes_to_long( os.urandom(32 - len(FLAG)) + FLAG )
pubkey = Public_key(G, d*G)
prikey = Private_key(pubkey, d)

magic1 = md5(d.to_bytes(32, "big")).digest()
magic2 = md5(d.to_bytes(32, "big")[::-1]).digest()

h1 = sha256(b"https://www.youtube.com/watch?v=IBnrn2pnPG8").digest()
h2 = sha256(b"https://www.youtube.com/watch?v=1H2cyhWYXrE").digest()

k1 = bytes_to_long(magic1 + magic2)
k2 = bytes_to_long(magic2 + magic1)

sig1 = prikey.sign(bytes_to_long(h1), k1)
sig2 = prikey.sign(bytes_to_long(h2), k2)

print(f'P = ({pubkey.point.x()}, {pubkey.point.y()})')
print(f'sig1 = ({sig1.r}, {sig1.s})')
print(f'sig2 = ({sig2.r}, {sig2.s})')

# P = (70427896289635684269185763735464004880272487387417064603929487585697794861713, 83106938517126976838986116917338443942453391221542116900720022828358221631968)
# sig1 = (26150478759659181410183574739595997895638116875172347795980556499925372918857, 50639168022751577246163934860133616960953696675993100806612269138066992704236)
# sig2 = (8256687378196792904669428303872036025324883507048772044875872623403155644190, 90323515158120328162524865800363952831516312527470472160064097576156608261906)
```
:::
## Recon
仔細看source code會發現他和上課講的例子很不一樣，上課講的方式是考慮已知$k1$, $k2$的長度是符合用lattice找的情況，用LLL找到$k1, k2$再回推d，但這一題一開始遇到最大的困難在於
$$
k_1=2^{128} magic_1+magic_2\\
k_2=2^{128} magic_2+magic_1
$$
很明顯$k_1, k_2$的bit_length都已經超過用Lattice找的範圍($K<n^{1\over 2}$，所以如果換個想法呢?我們不找$k_1, k_2$，我們改找$magic_1, magic_2$，之後再回推$k_1, k_2$再回推$d$是不是和原本的目的一樣，設想:

$k_1 + tk_2 + u \equiv 0\ (mod\ n)$
$\to magic_1*2^{128} + magic_2 + t(magic_2*2^{128} + magic_1) + u \equiv 0 (mod\ n)$
$\to (t+2^{128})magic_1 + (1 + t*2^{128})*magic_2+u\equiv 0 (mod\ n)$
$\to magic_1+(1 + t*2^{128})(t+2^{128})^{-1}magic_2+(t+2^{128})^{-1}u\equiv 0 (mod\ n)$
此時新的$t,u$
$$
new_t=(1 + t*2^{128})(t+2^{128})^{-1}\\
new_u=(t+2^{128})^{-1}u
$$

---
接著就是我一直困惑的地方，也是非常需要感謝Yaan的地方，LLL算出來是三個basi，然後做線性組合才會是投影片上的$vec=(-k1, k2, K)$(或是有一定的倍數)，並不是一開就會是那個vector


## Exploit - Lattice
1. 建立已知的訊息
    ```python
    E = SECP256k1
    G, n = E.generator, E.order
    P = (70427896289635684269185763735464004880272487387417064603929487585697794861713, 83106938517126976838986116917338443942453391221542116900720022828358221631968)
    sig1 = (26150478759659181410183574739595997895638116875172347795980556499925372918857, 50639168022751577246163934860133616960953696675993100806612269138066992704236)
    sig2 = (8256687378196792904669428303872036025324883507048772044875872623403155644190, 90323515158120328162524865800363952831516312527470472160064097576156608261906)

    h1 = bytes_to_long(sha256(b"https://www.youtube.com/watch?v=IBnrn2pnPG8").digest())
    h2 = bytes_to_long(sha256(b"https://www.youtube.com/watch?v=1H2cyhWYXrE").digest())
    ```
2. 實作一下原本的公式
    ```python
    r1, s1 = sig1
    r2, s2 = sig2
    s1_inv = inverse(s1, n)
    s2_inv = inverse(s2, n)
    r1_inv = inverse(r1, n)
    r2_inv = inverse(r2, n)

    t = -s1_inv * s2 * r1 * r2_inv
    u = s1_inv * r1 * h2 * r2_inv - s1_inv * h1
    b_matrix_K = 2**128
    dommy = 2**128
    ```
3. 建立B matrix
    ```python
    new_t = (1 + dommy * t) * inverse((dommy + t), n)
    new_u = u * inverse((dommy + t), n)
    b_matrix = [
        [int(n.digits()), 0, 0],
        [new_t, 1, 0],
        [new_u, 0, b_matrix_K]
    ]

    ```
4. 解LLL找最小的vector
    ```python
    LLL_reduced_basis = matrix(b_matrix).LLL()
    basis0 = LLL_reduced_basis[0]
    basis1 = LLL_reduced_basis[1]
    basis2 = LLL_reduced_basis[2]
    print(basis0, basis1, basis2)
    ```
5. 有了$magic_1, magic_2$之後就可以爆搜找$d$，並還原出原本的flag $\to$ 非常感謝Yaan提供script給我參考，最主要是這邊有障礙，首先可以先看一下找到的LLL長怎樣
    ```bash
    (-221227854189652752387006500971265535677, 154796202886613489929017650654193194295, 0) (-78316557126501995251733139438552596659, 1809028261633383948620558940699892506, 340282366920938463463374607431768211456) (-190260135239507154352414451870270937822, -390278805794181212650296278313898033211, 0)
    ```
    會發現只有basis1的後面是跟著K，代表線性組合的係數$j$不能為零，因為這樣就會讓我們想要的vector(-m1, m2, K)的最後那個K不是K而是零，而且後面在算factor的inverse時也會出現錯誤，所以詳細的推倒會變成:
    $$
    \begin{aligned}
    vector&=i*basis_0+j*basis_1+k*basis_2\\
    =&(i*basis_0[x]+j*basis_1[x]+k*basis_2[x]\\
    &,i*basis_0[y]+j*basis_1[y]+k*basis_2[y]\\
    &,i*basis_0[z]+j*basis_1[z]+k*basis_2[z])\\
    &= (-j*m1, j*m2, j*K)
    \end{aligned}
    $$
    可以看一下為甚麼會變成這樣，原因是從LLL找到的basis，第一個和第三個basis，他們的最後一個dimension都是零，代表vector的最後一個dimension$\to i*basis_0[z]+j*basis_1[z]+k*basis_2[z] = j*basis_1[z]$，所以當我們找到正確的i, j, k時，要記得把$j$取inverse除掉，才會是正確的$maic_1, magic_2$
    
    有了$magic_1, magic_2$之後，就是找$k_1$和$d$，最後我們就可以拿到flag了
    ```python
    def verify(d):
        return b"FLAG" in long_to_bytes(d)

    for i in range(-10,10):
        for j in range(-10,10):
            for k in range(-10, 10):
                if not j:
                    continue
                vec = i*basis0 + j*basis1 + k*basis2
                factor_inv = pow(j,-1,n)
                m1 = -(factor_inv*vec[0])
                m2 = factor_inv*vec[1]
                k1 = m1*(2**128)+m2
                d = ((s1*k1-h1)*r1_inv)%n
                if verify(d):
                    print(long_to_bytes(d))
                    check_flag = True
                    break

            if check_flag:
                break
        if check_flag:
            break
    ```

:::spoiler 完整的script
```python
from Crypto.Util.number import *
from hashlib import sha256, md5
from ecdsa import SECP256k1
from secret import FLAG

E = SECP256k1
G, n = E.generator, E.order
P = (70427896289635684269185763735464004880272487387417064603929487585697794861713, 83106938517126976838986116917338443942453391221542116900720022828358221631968)
sig1 = (26150478759659181410183574739595997895638116875172347795980556499925372918857, 50639168022751577246163934860133616960953696675993100806612269138066992704236)
sig2 = (8256687378196792904669428303872036025324883507048772044875872623403155644190, 90323515158120328162524865800363952831516312527470472160064097576156608261906)

h1 = bytes_to_long(sha256(b"https://www.youtube.com/watch?v=IBnrn2pnPG8").digest())
h2 = bytes_to_long(sha256(b"https://www.youtube.com/watch?v=1H2cyhWYXrE").digest())

r1, s1 = sig1
r2, s2 = sig2
s1_inv = inverse(s1, n)
s2_inv = inverse(s2, n)
r1_inv = inverse(r1, n)
r2_inv = inverse(r2, n)

t = -s1_inv * s2 * r1 * r2_inv
u = s1_inv * r1 * h2 * r2_inv - s1_inv * h1
b_matrix_K = 2**128
dommy = 2**128

new_t = (1 + dommy * t) * inverse((dommy + t), n)
new_u = u * inverse((dommy + t), n)

b_matrix = [
    [int(n.digits()), 0, 0],
    [new_t, 1, 0],
    [new_u, 0, b_matrix_K]
]

LLL_reduced_basis = matrix(b_matrix).LLL()
basis0 = LLL_reduced_basis[0]
basis1 = LLL_reduced_basis[1]
basis2 = LLL_reduced_basis[2]
print(basis0, basis1, basis2)

def verify(d):
    return b"FLAG" in long_to_bytes(d)

for i in range(-10,10):
    for j in range(-10,10):
        for k in range(-10, 10):
            if not j:
                continue
            vec = i*basis0 + j*basis1 + k*basis2
            factor_inv = pow(j,-1,n)
            m1 = -(factor_inv*vec[0])
            m2 = factor_inv*vec[1]
            k1 = m1*(2**128)+m2
            d = ((s1*k1-h1)*r1_inv)%n
            if verify(d):
                print(long_to_bytes(d))
                check_flag = True
                break
                
        if check_flag:
            break
    if check_flag:
        break

# (-221227854189652752387006500971265535677, 154796202886613489929017650654193194295, 0) (-78316557126501995251733139438552596659, 1809028261633383948620558940699892506, 340282366920938463463374607431768211456) (-190260135239507154352414451870270937822, -390278805794181212650296278313898033211, 0)
# b'\xad\xc4u\xcf\x11\x1f\xd7R$FLAG{LLLisreaLLyusefuL}'        
```
:::

Flag: `FLAG{LLLisreaLLyusefuL}`