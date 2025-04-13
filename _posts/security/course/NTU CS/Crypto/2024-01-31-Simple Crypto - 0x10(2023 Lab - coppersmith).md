---
title: Simple Crypto - 0x10(2023 Lab - coppersmith)
tags: [CTF, Crypto, eductf]

category: "Security/Course/NTU CS/Crypto"
---

# Simple Crypto - 0x10(2023 Lab - coppersmith)

## Background
[coppersmith相關攻擊](https://ctf-wiki.org/crypto/asymmetric/rsa/rsa_coppersmith_attack/)

## Source code
:::spoiler Source Code
```python=
from Crypto.Util.number import bytes_to_long, getPrime
from secret import FLAG

assert len(FLAG) <= 30

p = getPrime(1024)
q = getPrime(1024)
n = p * q
e = 3
padding = b"Padding in cryptography is a fundamental concept employed to ensure that data, typically in the form of plaintext, aligns properly with the encryption algorithm's block size. This process is crucial for symmetric block ciphers like AES and asymmetric encryption algorithms such as RSA. Padding involves adding extra bits to the input data before encryption, making it fit neatly into fixed-size blocks. The primary purpose of padding is to prevent information leakage by ensuring that the last block of plaintext is always complete, even when the original data's size isn't a perfect multiple of the block size. Common padding schemes include PKCS#7, PKCS#1 (for RSA), and ANSI X.923, each with its rules for padding and unpadding data. Proper padding ensures data integrity, security, and compatibility within cryptographic protocols."
pt = padding + FLAG
ct = pow(bytes_to_long(pt), e, n)
print(f"{e = }")
print(f"{n = }")
print(f"{ct = }")
# e = 3
# n = 11548249006448728920152703839381630946834097081458641312395741399152626808167055308830597218237419306363812953570976143239712039037941209800604194908083149885941768218371746741812573578768412807189143962911312361667909189521442378332430658999991458388376075547304981934158525694587528155624390264161508298680598416212224037418377397597560818727159266535257243347737195812548494888452510974912762585150695881388036715559552242157015756455473208463066542053661043988897316002396230791287157322382659981842882278113445574922266102197380093864871418103716702341116793118630092030597784102701252267617442078055768183287429
# ct = 10016669153906644953016660527326048255337800602435656916304698358749910229624738375584073093905785564737742726549033330343901680652357648652891913260149958947299067801907769873568759955053120633017158582128001396334187309835478967775943564724073809481988489791896725867047366927584419210464759674986336704398037888892734158765679221980466827060998749130113847401820986980535379266905587107992796676977541915779320084736207068268591500847603252838325486939367980604888710370629644796971859833251926677637185722683564847418746350226830775205063128441515048529918173084258483536354002888691012853231754416802134513394608
```
:::

## Recon
這一題看到`e=3`直覺會想到[小明文攻擊](https://zhuanlan.zhihu.com/p/76228394)，但是前提除了$e$要很小以外，明文也不能太大，要不然會找很久，他的原理是(假設`e=3`):
$$
\because C\equiv m^3\ mod\ N\\
\therefore m^3=C+k\times N \\
↪m=\root 3 \of {C+k\times N}
$$
所以可以枚舉很多的k，並且依次開三次方，直到開出整數為止，但就像前面的前提，明文不能太大，不然也會找的很痛苦，此時就可以用到上課教到的coppersmith，解出這樣的問題

* Review Coppersmith Attack
    問題：如果有一個$\{f(x)\equiv 0\ (mod\ N)\ |x=r, N\in \mathbb{Z}, f(x)\in \mathbb{Z}{[x]}\}$，當$x=r$的時候會同餘$0$
    想求：$r$是多少能符合以上的式子
    
    ---
    首先這個問題因為mod是一個循環，所以正常情況下很難知道$r$多少能符合，因此我們可以簡化一下問題，或者說增加一些限制，這樣在尋找$r$的時候會比較好找一點
    
    1. 首先構造一個
        $$
        \{Q(x)=s(x)\cdot f(x)+t(x)\cdot N\ (mod\ N)\ |\ Q(r)\equiv 0\ (mod\ N), r\in \mathbb{Z}\}
        $$
        在這裡可以先把$r$帶進去這個構造的式子，就會發現其實跟一開始求的問題，也就是$f(x)\equiv 0\ (mod\ N)$其實一樣，但為甚麼要這樣做呢?是因為把問題拉到實數域中求解後比較好做，等我們拿到$r$在實數域得到的root之後就可以帶回去$f(x)$中。
    
        我們可以把$r$想像成是一個flag，然後flag會有一個最大可能性的上界，也就是$R$，假設flag有32個字元，代表256個bits，我們可以想像$R=2^{256}$，我們不知道flag是多少，但一定在$R$的這個範圍中，且flag一定是整數(換算成int的話)
    2. 所以我們就可以重新寫一個bounded equation
        $$
        Q(r)=|Q_nr^n+...+Q_2r^2+Q_1r^1+Q_0|\le |Q_n|R^n+...+|Q_2|R^2+|Q_1|R+|Q_0|
        $$
        有了這個bound equation後，我們就可以說
        $$
        \because |Q(r)| < |Q(R)| < N且Q(r) ≡ 0\ mod\ N\\
        \therefore Q(r)=0
        $$
        有了以上條件和說明，此時我們確定把問題拉到實數域上了，現在還不知到$r$為多少
    3. 而要知道$r$就必須知道$Q(r)$，只要得到$Q(r)$再利用找root的sage method就可以直接得到$r$為多少，但在得到$Q(r)$之前我們要先得到$Q(R)$，我們可以利用前面提到的$s(x)\cdot f(x)+t(x)\cdot N\ (mod\ N)$建一個多項式，然後用matrix表示並把$R$帶入，再利用LLL求shortest vector，此時的shortest vector是以$x=R$為條件帶入，所以只要在各個term把$R$除掉，就可以得到$Q(r)$各個term的係數，然後就求得$r$為多少了，舉例來說：
    
        在RSA中，已知$c= m^e\ (mod\ N)$，當我們今天拿到一個有padding明文(當然我們拿到的是密文，只是知道明文有經過padding，且padding的部分我們知道，另外flag的大小也不能太大，具體能多大可以看影片)，且$e=3$，我們可以rewrite整個式子(假設padding的部分為$a$，flag的部分為$x$)
        $$
        \begin{aligned}
        m &= padding + flag\\
        c &= m^3 = (padding + flag)^3\ (mod\ N)\\
        f(x) &= (padding + flag)^3 - c\ (mod\ N)
        \end{aligned}\\
        \downarrow\\
        s(x)\cdot f(x)+t(x)\cdot N\ (mod\ N)\\
        =c_3(x^3 + 3ax^2 + 3a^2x + (a^3 - c)) + (c_2x^2 + c_1x + c_0)\cdot N\\
        =\begin{bmatrix}
          c_3, c_2, c_1, c_0
        \end{bmatrix}\cdot\begin{bmatrix}
          x^3 & 3ax^2 & 3a^2x & a^3 - c\\
          0 & Nx^2 & 0 & 0 \\
          0 & 0 & Nx & 0\\
          0 & 0 & 0 & N
        \end{bmatrix}
        $$
        $s(x)=c_3$，如果把$f(x)$乘開就會是$x^3 + 3ax^2 + 3a^2x + (a^3 - c)$，而$t(x)=c_2x^2 + c_1x + c_0$。此時把矩陣的$x$帶入上界$R$再利用LLL求shortest vector，也就是
        $$
        \begin{bmatrix}
        c_3R^3\\
        (c_33a + c_2N)*R^2\\
        (c_33a^2 + c_1N)*R\\
        (c_3(a^3-c) + c_0N)
        \end{bmatrix}^T
        $$
        詳細過程如下:
        $$
        \begin{aligned}
        M&=\begin{bmatrix}
          R^3 & 3aR^2 & 3a^2R & a^3 - c\\
          0 & NR^2 & 0 & 0 \\
          0 & 0 & NR & 0\\
          0 & 0 & 0 & N\\
        \end{bmatrix} | x = R\\
        LLL(M)&=\begin{bmatrix}
        c_3R^3\\
        (c_33a + c_2N)*R^2\\
        (c_33a^2 + c_1N)*R\\
        (c_3(a^3-c) + c_0N)
        \end{bmatrix}^T
        \end{aligned}\\
        ↪Q(x)=\begin{bmatrix}
        c_3\\
        c_33a + c_2N\\
        c_33a^2 + c_1N\\
        c_3(a^3-c) + c_0N
        \end{bmatrix}^T\begin{bmatrix}
          x^3\\
          x^2\\
          x^1\\
          x^0
        \end{bmatrix}\le Q(R) = \begin{bmatrix}
          Q_3\\
          Q_2\\
          Q_1\\
          Q_0
        \end{bmatrix}^T
        \begin{bmatrix}
          R^3\\
          R^2\\
          R\\
          1\\
        \end{bmatrix}\le N
        $$
    4. 求flag(也就是求得$Q(x)$的root $x_0$)
        由以上過程，我們已經取得了$Q(x)$，則我們就可以在實數域中求$Q(x)$的根$x_0$

* 基本上這一題就是按照上面講的這樣解就可以了

## Exploit
```python=
from Crypto.Util.number import *
from pwn import log


e = 3
n = 11548249006448728920152703839381630946834097081458641312395741399152626808167055308830597218237419306363812953570976143239712039037941209800604194908083149885941768218371746741812573578768412807189143962911312361667909189521442378332430658999991458388376075547304981934158525694587528155624390264161508298680598416212224037418377397597560818727159266535257243347737195812548494888452510974912762585150695881388036715559552242157015756455473208463066542053661043988897316002396230791287157322382659981842882278113445574922266102197380093864871418103716702341116793118630092030597784102701252267617442078055768183287429
ct = 10016669153906644953016660527326048255337800602435656916304698358749910229624738375584073093905785564737742726549033330343901680652357648652891913260149958947299067801907769873568759955053120633017158582128001396334187309835478967775943564724073809481988489791896725867047366927584419210464759674986336704398037888892734158765679221980466827060998749130113847401820986980535379266905587107992796676977541915779320084736207068268591500847603252838325486939367980604888710370629644796971859833251926677637185722683564847418746350226830775205063128441515048529918173084258483536354002888691012853231754416802134513394608
l = 30
R = 1 << (l * 8)
padding = b"Padding in cryptography is a fundamental concept employed to ensure that data, typically in the form of plaintext, aligns properly with the encryption algorithm's block size. This process is crucial for symmetric block ciphers like AES and asymmetric encryption algorithms such as RSA. Padding involves adding extra bits to the input data before encryption, making it fit neatly into fixed-size blocks. The primary purpose of padding is to prevent information leakage by ensuring that the last block of plaintext is always complete, even when the original data's size isn't a perfect multiple of the block size. Common padding schemes include PKCS#7, PKCS#1 (for RSA), and ANSI X.923, each with its rules for padding and unpadding data. Proper padding ensures data integrity, security, and compatibility within cryptographic protocols."
a = bytes_to_long(padding) * (R)
M = [
    [R^3, 3 * a * R^2, 3 * a^2 * R, a^3 - ct],
    [0, n * R^2, 0, 0],
    [0, 0, n * R, 0],
    [0, 0, 0, n]
]
L = matrix(M).LLL()
v = L[0]
F.<x> = PolynomialRing(ZZ)
Q = (v[0] // R^3) * x^3 + (v[1] // R^2) * x^2 + (v[2] // R) * x + v[3]
# print(Q.roots())
v = L[0]
F.<x> = PolynomialRing(ZZ)
Q = (v[0] // R^3) * x^3 + (v[1] // R^2) * x^2 + (v[2] // R) * x + v[3]
# print(Q.roots()[0][0])
log.info(f'Flag: {long_to_bytes(Q.roots()[0][0]).decode()}')
```
Flag: `FLAG{RandomPaddingIsImportant}`