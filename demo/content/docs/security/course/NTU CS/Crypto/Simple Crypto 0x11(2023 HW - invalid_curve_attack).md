---
title: Simple Crypto 0x11(2023 HW - invalid_curve_attack)
tags: [CTF, Crypto, eductf]

---

# Simple Crypto 0x11(2023 HW - invalid_curve_attack)
## Background
[pekobot - maple](https://github.com/maple3142/My-CTF-Challenges/blob/7d9141ac7b61fdbb71f29c07d489018d7c0a0aaa/AIS3%20Pre-exam%202022/pekobot/README.md)
> 這邊我會嘗試用簡單的講法把這個攻擊簡述一遍，詳細還是建議 [Crypton](https://github.com/ashutosh1206/Crypton/blob/master/Diffie-Hellman-Key-Exchange/Attack-Invalid-Curve-Point/README.md) 或是其他地方的說明。
>
>Invalid Curve Attack 大致上來說利用的是當一個不在原本曲線 $E$ 上的 $P$ 進行 scalar multiplication 的一些特性，使用類似 [Pohlig–Hellman algorithm](https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm) 的辦法在不同的 subgroup 解 [DLP](https://en.wikipedia.org/wiki/Discrete_logarithm) 然後用 [CRT](https://en.wikipedia.org/wiki/Chinese_remainder_theorem) 解回原本的 private key。
>
>一個 Short Weierstrass curve 長這樣:
>
>$$
>y^2 = x^3 + ax + b
>$$
>
>而它的 point doubling formula ($R=2P$) 是:
>
>$$
>\begin{aligned}
>s &= \frac{3x_P^2+a}{2y_P} \\
>x_R &= s^2 - 2x_P \\
>y_R &= y_P + s(x_R - x_P)
>\end{aligned}
>$$
>
>由此可見一個 Short Weierstrass curve 在做 scalar multiplication 時並沒有使用到 $b$，
>因此對一個 $P \notin E$ 的點做 scalar multiplication 相當於在另一個 $b' \neq b$ 的 $E': y^2 = x^3 + ax + b'$ 上運算。
>
>這會帶來的問題是 $E'$ 通常和特別選過的 $E$ 不同，它的 curve order $\#(E')=n$ 分解後不一定都有個 large prime order subgroup 存在。當 $E'$ 上存在一個 order 為 $f$ 的 small subgroup 時，我們可以將原本 $Q=dP$ 的問題轉換成 $(n/f)Q=d((n/f)P)$，然後就能在短時間內解出 $d \bmod{f}$ 的值。
>
>所以只要有多個夠小的 $f_1, f_2, f_3, \cdots$，利用上面的方法找出 $d_i \equiv d \pmod{f_i}$，然後利用 CRT 就能算出 $d \bmod{\prod_{i=1}^{b} f_i}$ 的結果。因此要得到真正的 $d$ 就得找出足夠多的 $f_i$ 使得 $\prod_{i=1}^{b} f_i > n > d$ 才行。
>
>當然，一個 $E'$ 通常不會提供這麼多的 $f_i$ 能達成這個條件，所以會有多個 $E', E'', E''', \cdots$ 分別提供不同的 $f_i$，然後用一樣的方法在 subgroup 中解 DLP，最後應用 CRT 即可求出需要的 $d$。
>
>這題原先的曲線 $E$ 是 NIST P-256，所以我先將 $a$ 固定，然後暴力搜尋其他不同的 $b'$ 得到 $E'$，把夠小的 $f_i$ 紀錄下來。這部分可以參考 [find_curves.sage](https://github.com/maple3142/My-CTF-Challenges/blob/7d9141ac7b61fdbb71f29c07d489018d7c0a0aaa/AIS3%20Pre-exam%202022/pekobot/find_curves.sage)。
>
>為了減少之後的計算量，我把 $b'$, $E'$ 上的 generator $G'$, $\#(E')$ 還有 $f_i$ 都記錄了下來
>
>剩下就是利用這些預先計算好的參數，將各個 $E'$ 的 $G'$ 當作 public key $P$ 傳給 oracle，然後得到 $Q=dP$，然後用前面的方法得到 $d \equiv d \pmod{f_i}$ 的值，最後使用 CRT 求回 $d$ 即可。

## Source code
:::spoiler Server
```python=
from sage.all import *
from elliptic_curve_97cadb52fbd7b2cd import Curve, Point
from Crypto.Util.number import bytes_to_long
from secret import FLAG

# NIST P-256
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551

print("Give me a G and I will give you the hint.")
E = Curve(p, a, b)
Gx = int(input("Gx: "))
Gy = int(input("Gy: "))
G = Point(E, Gx, Gy)
hint = G * bytes_to_long(FLAG)
print(hint)
```
:::

:::spoiler Self-Defined Elliptic Curve
```python=
# Reference: https://github.com/maple3142/My-CTF-Challenges/blob/7d9141ac7b61fdbb71f29c07d489018d7c0a0aaa/AIS3%20Pre-exam%202022/pekobot/README.md
class Curve:
    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b

    def __eq__(self, other):
        if isinstance(other, Curve):
            return self.p == other.p and self.a == other.a and self.b == other.b
        return None

    def __str__(self):
        return "y^2 = x^3 + %dx + %d over F_%d" % (self.a, self.b, self.p)


class Point:
    def __init__(self, curve, x, y):
        if curve == None:
            self.curve = self.x = self.y = None
            return
        self.curve = curve
        self.x = x % curve.p
        self.y = y % curve.p

    def __str__(self):
        if self == INFINITY:
            return "INF"
        return "(%d, %d)" % (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.curve == other.curve and self.x == other.x and self.y == other.y
        return None

    def __add__(self, other):
        if not isinstance(other, Point):
            return None
        if other == INFINITY:
            return self
        if self == INFINITY:
            return other
        p = self.curve.p
        if self.x == other.x:
            if (self.y + other.y) % p == 0:
                return INFINITY
            else:
                return self.double()
        p = self.curve.p
        l = ((other.y - self.y) * pow(other.x - self.x, -1, p)) % p
        x3 = (l * l - self.x - other.x) % p
        y3 = (l * (self.x - x3) - self.y) % p
        return Point(self.curve, x3, y3)

    def __neg__(self):
        return Point(self.curve, self.x, self.curve.p - self.y)

    def __mul__(self, e):
        if e == 0:
            return INFINITY
        if self == INFINITY:
            return INFINITY
        if e < 0:
            return (-self) * (-e)
        ret = self * (e // 2)
        ret = ret.double()
        if e % 2 == 1:
            ret = ret + self
        return ret

    def __rmul__(self, other):
        return self * other

    def double(self):
        if self == INFINITY:
            return INFINITY
        p = self.curve.p
        a = self.curve.a
        l = ((3 * self.x * self.x + a) * pow(2 * self.y, -1, p)) % p
        x3 = (l * l - 2 * self.x) % p
        y3 = (l * (self.x - x3) - self.y) % p
        return Point(self.curve, x3, y3)


INFINITY = Point(None, None, None)
```
:::
## Recon
1. 觀察source code會發現maple實作了一個沒有檢查我們傳送的點是否在一開始創的橢圓曲線上的elliptiv curve class，然後他把我們給的point當作參數，創立一個初始點，可以看一下下面裡個範例，如果是maple的實作，給予一個根本不在該Elliptic Curve的點他還是會算一個G+G的點給你，只是該點其實是在別的曲線上的2G這個點，反觀正常的sage中的實作會發現只要給予的點不在該曲線上就會直接報錯
    ![](https://hackmd.io/_uploads/H15TTzBZa.png)
    :::spoiler maple 實作的Elliptic Curve
    ```python
    >>> from elliptic_curve_97cadb52fbd7b2cd import Curve, Point
    >>> p=23
    >>> a=5
    >>> b=1
    >>> E = Curve(p, a, b)
    >>> G = Point(E, 4, 4)
    >>> print(G)
    (4, 4)
    >>> print(G+G)
    (19, 3)
    >>> fake_G = Point(E, 4, 3)
    >>> print(fake_G+fake_G)
    (17, 1)
    ```
    :::

    :::spoiler 正常的Elliptic Curve
    ```python!
    >>> from sage.all import *
    >>> p=23
    >>> a=5
    >>> b=1
    >>> E = EllipticCurve(Zmod(p), [a, b])
    >>> G = E(4, 4)
    >>> print(G)
    (4 : 4 : 1)
    >>> fake_G = E(4, 3)
    Traceback (most recent call last):
      File "sage/structure/category_object.pyx", line 839, in sage.structure.category_object.CategoryObject.getattr_from_category (build/cythonized/sage/structure/category_object.c:7216)
    KeyError: 'point_homset'

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "/home/sbk6401/anaconda3/envs/sageenv/lib/python3.11/site-packages/sage/schemes/projective/projective_subscheme.py", line 122, in point
        return self._point(self.point_homset(), v, check=check)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/sbk6401/anaconda3/envs/sageenv/lib/python3.11/site-packages/sage/schemes/elliptic_curves/ell_point.py", line 259, in __init__
        point_homset = curve.point_homset()
                       ^^^^^^^^^^^^^^^^^^
      File "sage/structure/category_object.pyx", line 833, in sage.structure.category_object.CategoryObject.__getattr__ (build/cythonized/sage/structure/category_object.c:7135)
      File "sage/structure/category_object.pyx", line 848, in sage.structure.category_object.CategoryObject.getattr_from_category (build/cythonized/sage/structure/category_object.c:7301)
      File "sage/cpython/getattr.pyx", line 356, in sage.cpython.getattr.getattr_from_other_class (build/cythonized/sage/cpython/getattr.c:2717)
    AttributeError: 'IntegerModRing_generic_with_category' object has no attribute '__custom_name'

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/sbk6401/anaconda3/envs/sageenv/lib/python3.11/site-packages/sage/schemes/elliptic_curves/ell_generic.py", line 582, in __call__
        return plane_curve.ProjectivePlaneCurve.__call__(self, *args, **kwds)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/sbk6401/anaconda3/envs/sageenv/lib/python3.11/site-packages/sage/schemes/generic/scheme.py", line 266, in __call__
        return self.point(args)
               ^^^^^^^^^^^^^^^^
      File "/home/sbk6401/anaconda3/envs/sageenv/lib/python3.11/site-packages/sage/schemes/projective/projective_subscheme.py", line 124, in point
        return self._point(self, v, check=check)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/sbk6401/anaconda3/envs/sageenv/lib/python3.11/site-packages/sage/schemes/elliptic_curves/ell_point.py", line 298, in __init__
        raise TypeError("Coordinates %s do not define a point on %s" % (list(v), curve))
    TypeError: Coordinates [4, 3, 1] do not define a point on Elliptic Curve defined by y^2 = x^3 + 5*x + 1 over Ring of integers modulo 23
    ```
    :::
2. 有了這個性質就可以回去參考一下maple在github上的說明，我們要解決的問題是$hint=G*flag$中的flag到底是甚麼，如果是像前面舉例的那樣($p=23/a=5/b=1/order=31$)很小的order，其實只要直接算`discrete_log(K, G, operation='+')`就可以了，範例如下，可以看到我先定義`K = E(19, 3)`，算出`discete log=28`，事後驗證也證明$K=28*G$。但是，像題目中這樣這麼大的order，如果要計算discrete_log的話會非常非常久的時間，總之我先往smooth order的方向思考，也就是說order被factor後其實是由好幾個小的prime所組成，我是直接調整$b$這個不會被Elliptic Curve Multiplication運算使用到的參數(代表其他參數$p, a$要照舊)，然後factor曲線的order看夠不夠smooth，但這樣找也一樣要非常非常久，或者說找到的$b$所得到的order都不夠smooth，最大的prime都還是超過$2^{65}$(e.g. 範例如下)
    ```python!
    >>> G = E.gen(0)
    >>> print(G)
    (15 : 1 : 1)
    >>> K = E(19, 3)
    >>> discrete_log(K, G, operation='+')
    28
    >>> 28 * G
    (19 : 3 : 1)
    ```
    
    ```sage
    sage: p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
    ....: a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
    ....: b = 56
    sage: E = EllipticCurve(Zmod(p), [a, b])
    sage: factor(E.order())
    3^3 * 13967 * 67679 * 559243 * 11024719 * 127273871 * 1213196727283 * 171447020014729 * 27796463802665410393
    sage: 27796463802665410393.bit_length()
    65
    ```
3. 所以我開始朝maple的說明繼續前進，如果有invalid curve的問題就可以考慮用Pohlig–Hellman algorithm的方法求出flag為多少，就如同maple在background中提到的，我們選擇不同的$b$所產生的Elliptic Curve Order被factor後不一定有一個超大prime存在，因此我們就可以把問題簡化($n$就是改變$b$之後取得的Elliptic Curve Order)
$$
hint=flag*G\\
\hookrightarrow {n \over prime}hint=flag'\times {n\over prime} G\\
flag'=discrete\_log({n \over prime}hint, {n\over prime} G, operation='+')
$$
4. 等我們找到很多個$b$就可以找到很多不同的$flag'$，最後我們再用CRT找出真正的$flag$為何就可以了，也就是
$$
flag\equiv flag'\ (mod\ prime_1)\\
flag\equiv flag''\ (mod\ prime_2)\\
flag\equiv flag'''\ (mod\ prime_3)\\
...
$$
所以重點在於要找到足夠多的$flag'$和$prime_n$組合
## Exploit
實作的部分主要是參考[^hackthebox-invalid-curve-attack-wp]的幫忙，大致上就和上面提到的差不多
```python=
from sage.all import *
from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
from pwn import *

# NIST P-256
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc

def solveDL():
    b = randint(1, p)
    E = EllipticCurve(Zmod(p), [a, b])
    G = E.gen(0)
    order = E.order()
    # print(order)
    factors = prime_factors(order)
    # print(factors)
    valid = []
    for factor in factors:
        if factor <= 2**40:
            valid.append(factor)
    prime = valid[-1]
    new_G = G * int(order / prime)
    tmp_point = new_G.xy()
    tmp_x, tmp_y = str(tmp_point[0]), str(tmp_point[1])

    try:
        r = remote('10.113.184.121', 10034)
        r.recvline()
        r.sendlineafter(b'Gx: ', tmp_x.encode())
        r.sendlineafter(b'Gy: ', tmp_y.encode())
        hint = r.recvline().decode().strip()
        ct_x, ct_y = hint.rstrip(')').lstrip('(').split(', ')
        r.close()
    except Exception as e:
        r.close()
        print(e)
        return None, None

    # print(f'Position (ct_x, ct_y) = ({ct_x}, {ct_y})')
    new_hint = E(int(ct_x), int(ct_y))
    aprt_of_flag = discrete_log(new_hint, new_G, operation='+')
    print(f"Flag' found: {aprt_of_flag}")
    return (aprt_of_flag, prime)
    
def getDLs():
    dlogs = []
    primes = []
    for i in range(1, 16):
        log, prime = solveDL()
        if log != None:
            dlogs.append(log)
            primes.append(prime)
        print(f"counter: {i}")
    return dlogs, primes

dlogs, primes = getDLs()
print(f"dlogs: {dlogs}")
print(f"primes: {primes}")
super_secret = CRT_list(dlogs, primes)
print(f'Flag: {long_to_bytes(super_secret).decode()}')
```
:::spoiler Result
```bash!
$ $ python exp.py
[+] Opening connection to 10.113.184.121 on port 10034: Done
[*] Closed connection to 10.113.184.121 port 10034
Flag' found: 27360610332
counter: 1
[+] Opening connection to 10.113.184.121 on port 10034: Done
[*] Closed connection to 10.113.184.121 port 10034
Flag' found: 1023158172
counter: 2
[+] Opening connection to 10.113.184.121 on port 10034: Done
[*] Closed connection to 10.113.184.121 port 10034
Flag' found: 19279
counter: 3
[+] Opening connection to 10.113.184.121 on port 10034: Done
[*] Closed connection to 10.113.184.121 port 10034
Flag' found: 99180577
counter: 4
[+] Opening connection to 10.113.184.121 on port 10034: Done
[*] Closed connection to 10.113.184.121 port 10034
not enough values to unpack (expected 2, got 1)
counter: 5
[+] Opening connection to 10.113.184.121 on port 10034: Done
[*] Closed connection to 10.113.184.121 port 10034
Flag' found: 1431258
counter: 6
[+] Opening connection to 10.113.184.121 on port 10034: Done
[*] Closed connection to 10.113.184.121 port 10034
Flag' found: 152629534
counter: 7
[+] Opening connection to 10.113.184.121 on port 10034: Done
[*] Closed connection to 10.113.184.121 port 10034
Flag' found: 36835
counter: 8
[+] Opening connection to 10.113.184.121 on port 10034: Done
[*] Closed connection to 10.113.184.121 port 10034
Flag' found: 15673959
counter: 9
[+] Opening connection to 10.113.184.121 on port 10034: Done
[*] Closed connection to 10.113.184.121 port 10034
Flag' found: 301945137539
counter: 10
[+] Opening connection to 10.113.184.121 on port 10034: Done
[*] Closed connection to 10.113.184.121 port 10034
Flag' found: 2906
counter: 11
[+] Opening connection to 10.113.184.121 on port 10034: Done
[*] Closed connection to 10.113.184.121 port 10034
Flag' found: 111332288773
counter: 12
[+] Opening connection to 10.113.184.121 on port 10034: Done
[*] Closed connection to 10.113.184.121 port 10034
Flag' found: 245821
counter: 13
[+] Opening connection to 10.113.184.121 on port 10034: Done
[*] Closed connection to 10.113.184.121 port 10034
Flag' found: 7711492
counter: 14
[+] Opening connection to 10.113.184.121 on port 10034: Done
[*] Closed connection to 10.113.184.121 port 10034
not enough values to unpack (expected 2, got 1)
counter: 15
dlogs: [27360610332, 1023158172, 19279, 99180577, 1431258, 152629534, 36835, 15673959, 301945137539, 2906, 111332288773, 245821, 7711492]
primes: [144923720933, 357189282511, 62189, 572762753, 1649429, 172592237, 163171, 34381453, 443616973637, 11159, 568852214543, 371177, 8924527]
Flag: FLAG{YouAreARealECDLPMaster}
```
:::

Flag: `FLAG{YouAreARealECDLPMaster}`
## Reference
[^hackthebox-invalid-curve-attack-wp]:[Business CTF 2022: Invalid curve attack - 400 Curves](https://www.hackthebox.com/blog/business-ctf-2022-400-curves-write-up)