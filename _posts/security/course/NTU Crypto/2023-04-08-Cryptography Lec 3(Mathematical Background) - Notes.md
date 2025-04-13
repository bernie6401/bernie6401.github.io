---
title: Cryptography Lec 3(Mathematical Background) - Notes
tags: [Cryptography, NTU]

category: "Security/Course/NTU Crypto"
---

# Cryptography Lec 3(Mathematical Background) - Notes
###### tags: `Cryptography` `NTU`

## Background
:::spoiler [Euclidean Algorithm(輾轉相除法)](https://youtu.be/qym5D5bhoQs)
Given $a$ and $b$ with $a \ge b$
Compute $gcd(a,\ b)=gcd(b,\ a\ mod\ b)$, $gcd(a,\ 0)=a$
For example
$$
Compute\ gcd(140,\ 297)\\
297=2*140+17 \\
140=8*17+4 \\
17=4*4+1 \\
4=4*4+0 
$$
Then we found the $gcd(140,\ 297)=1$

---
Another Example:
$$
Compute\ gcd(270,\ 192)\\
270=1*192+78\\
192=2*78+36\\
78=2*36+6\\
36=6*6+0
$$
Then we found $gcd(270,\ 192)=6$
:::

:::spoiler [Extended Euclidean Algorithm](https://youtu.be/hB34-GSDT3k)
其實就只是把原本用Euclidean Algorithm算出來的$gdc(a,\ b)$，變成Linear Combination的形式而已
For example above:
As we know $gcd(270,\ 192)=6$, then...
$$
6=78-36*2\\
36=192-2*78\\
78=270-1*192
$$
$$\downarrow$$
$$
\begin{aligned}
6&=78-(192-2*78)*2\\
&=78-[192-2*(270-1*192)]*2\\
&=78-[192*3-2*270]*2\\
&=270-1*192-192*6+4*270\\
&=270*5-7*192
\end{aligned}
$$
Then we know the linear combination coefficient of $gcd(270,\ 192)$ is $+5$ and $-7$
:::

:::spoiler [質數愈大愈孤獨：談質數分布](https://ir.nctu.edu.tw/bitstream/11536/129288/1/yaucenter-20131201-08.pdf)
Prime Number Theorem:
$$\lim\limits_{x\to \infty}{x \over \pi(x)}=\ln(x)$$
![](https://i.imgur.com/lsITjjM.png)
:::

***
Good Reference about Linear Algebra: [大學基礎代數](https://math.ntnu.edu.tw/~li/algebra-html/algebra.pdf)
:::spoiler [Linear Algebra - Group](https://ccjou.wordpress.com/2011/09/16/%E7%B7%9A%E6%80%A7%E4%BB%A3%E6%95%B8%E8%A3%A1%E7%9A%84%E4%BB%A3%E6%95%B8%E7%B5%90%E6%A7%8B/)
純量加法的代數結構稱為阿貝爾群(Abelian Group)。考慮整數集 $\mathbb{Z}$ (包含正整數、負整數與零)，我們觀察出任兩個整數的加法運算滿足以下五個性質：

1. 加法具有封閉性，如果 $x$ 和 $y$ 屬於 $\mathbb{Z}$，那麼 $x+y$ 也屬於 $\mathbb{Z}$。
2. 加法具有交換性，兩整數之和與其計算位置無關
    $x+y=y+x$
3. 加法具有結合性，排序固定的三個整數之和與其執行加法的順序無關，
    $(x+y)+z=x+(y+z)$
4. 存在一整數 0 使得任何整數與其相加皆不改變，
    $x+0=0+x=x$，
    因此 0 也稱為加法單位元。
5. 任何加法都可以「回復」，意即每一整數皆存在逆元，如下：
    $x+(-x)=(-x)+x=0$。
---
再舉一個例子
考慮正實數集 $\mathbb{R}_{+}$，並以 $\times$ 表示一般的乘法運算：

$x\times y=xy$。

明顯地，正實數乘法滿足封閉性、交換性與結合性。上例中 $0$ 的角色被實數 $1$ 所取代，$1$ 稱為乘法單位元，滿足下式：
$x\times 1=1\times x=x$

每一個正實數 $x$ 的逆元為其倒數，因為
$\displaystyle x\times\left(\frac{1}{x}\right)=\left(\frac{1}{x}\right)\times x=1$。

---
Example of Groups:
Addition: Integers, Reals, Rationals
Multiplication: Nonzero Reals, Rationals

---
:::success
上例整數 $\mathbb{Z}$ 的加法 $+$ 與正實數 $\mathbb{R}_{+}$ 的乘法 $\times$ 共同滿足的五個性質即為阿貝爾群的定義。正式地說，給定一個集合 ${G}$ 與二元運算 $\ast$，若滿足上述五個性質，**<font color="FF0000">即封閉性、交換性、結合性，存在一運算單位元，且每一元素皆存在對應的逆元</font>**，我們便稱 $({G},\ast)$ 為阿貝爾群。
:::

:::spoiler [【代數】Field：體](http://ohmycakelus.blogspot.com/2012/02/field.html)
>Def：Field
>一個Field  $\mathbb{F}$定義在一個集合與兩種運算方式之下，兩種運算分別為加法($+$)與乘法($*$)。若 a, b, c為F中的元素，則具有以下性質：
> 1. 乘法與加法封閉性與唯一性：$a + b$ 與 $a * b$ 唯一且皆屬於$\mathbb{F}$
> 2. 乘法與加法單位元素：$0$、$1$ 屬於$\mathbb{F}$，使得 a + 0 = a 且 a * 1 = a
> 3. 乘法與加法反元素：任意$a$皆存在$b$、$c$ ，使得$a + b = 0$、$a * c = 1$，(只有$0$沒有乘法反元素)
> 4. 乘法與加法交換律：$a + b = b + a$、$a * b = b * a$
> 5. 乘法與加法結合律：$(a + b) + c = a + (b + c)$、$(a * b) * c = a * (b * c)$
> 6. 乘法對加法的分配律：$a * (b + c) = ab + ac$
> $\mathbb{R}$是一個Field、有理數也是一個 Field、$Z2：\{0, 1\}$，其中$1 + 1 = 0$，其餘運算與與正常運算相同，這也是一個Field。
>
>經由加法與乘法反元素，可以定義減法與除法為與反元素相加或相乘。

:::info
Field's order代表field elements的數量，所以若是一個field的order是finite，就是一個finite field(Galois Fields)，通常會表示成$GF(p)$

:::

:::spoiler [環 (Ring) 與體 (Field)](http://ohmycakelus.blogspot.com/2013/03/blog-post_31.html)
>環是一個擁有兩個二元運算的集合，通常以加法和乘法表示，此集合在加法下會構成一個可交換群，並在乘法下構成一個 monoid，同時乘法對加法具有分配律，也就是說，滿足以下性質的集合就稱為一個環：
>
> 1. 具有加法及乘法運算，且具有封閉性。
> 2. 有加法單位元 0。
> 3. 有加法反元素 -a。
> 4. 有加法結合律。
> 5. 有加法交換律。
> 6. 有乘法單位元 1。
> 7. 有乘法結合律。
> 8. $a*(b+c) = a*b + a*c$
$(b+c)*a = b*a + c*a。$
:::

:::spoiler Polynomial Rings
其實就是一般的Rings只是裡面的元素都是由多項式組成
而我們說$f$ is irreducible over $R$代表$f$不能分解成degree是正的多項式乘積(簡單來說就是不能因式分解)
:::info
承接上述的$GF(p)$為例，若是$GF(2)$就代表多項式的元素之間在做加減等運算時，每一個項的係數都要$mod\ 2$，例如：
$$f(x)=x^7+x^5+x^4+x^3+x+1$$
$$g(x)=x^3+x+1$$
$$f(x)+g(x)=x^7+x^5+x^4$$
因為其他項次的係數$mod\ 2$之後就變成零了
* 多項式找最大公因式也可以使用Euclid's Algorithm
:::

***
:::spoiler [Euler φ function](https://ithelp.ithome.com.tw/articles/10225768)
φ(n)：比$n$小且與$n$互質的數的數量
:::

:::spoiler 數論篇
What is $\mathbb{Z}, \mathbb{Z}_n, \mathbb{Z}_n^*, \mathbb{Z}_p, \mathbb{Z}_p^*$

Reference:
[密碼學卷宗 數論篇 - 上卷](https://ithelp.ithome.com.tw/articles/10224328)
[密碼卷宗 數論篇 - 下卷](https://ithelp.ithome.com.tw/articles/10224347), 
[Difference between $Z_n^*$ and $Z_n$[closed]](https://crypto.stackexchange.com/questions/47797/difference-between-z-n-and-z-n)
> * <font color="FF000">$\mathbb{Z}$</font>整數集合
    * 是從負無窮大到正無窮大的所有整數形成的集合
    * $\mathbb{Z} = \{ ...,-2,-1,0,1,2,... \}$
>---
> * <font color="FF000">$\mathbb{Z}_n$</font>餘數集合
    * 模運算產生的集合，被稱為「模$n$之最小餘數集合(Set of least residues modulo n)」
    * $\mathbb{Z}_n = \{0,1,2,3,...,(n-1)\}$
    * 比較 $\mathbb{Z}$ 和 $\mathbb{Z}_n$
    ![](https://i.imgur.com/410Mz5l.png)
>---
> * <font color="FF000">$\mathbb{Z}_n^*$</font>
    $\mathbb{Z}_n^*$ doesn't mean $\mathbb{Z}_n−\{0\}$. You must remove all elements that are not invertible mod $n$, which is equivalent to keeping only the elements that are coprimes to $n$.
    For example: $Z_9^*=\{1,2,4,5,7\}$.
> ---
> * <font color="FF000">$\mathbb{Z}_p$</font>
> $\mathbb{Z}_p$就是上述的概念只是$n$一定是prime number，另外$\mathbb{Z}_p^*$就是$\mathbb{Z}_p$除去0，意味着$\mathbb{Z}_p$中的所有元素都是可逆的，0除外，而$\mathbb{Z}_p^*$的大小就是$p-1$
:::

:::spoiler 模運算
$$xy\ mod\ q=(x\ mod q)(y\ mod\ q)\ mod\ q$$
:::

---

## Chinese Remainder Theorem $\to$ RSA
:::spoiler Fermat's Little Theorem
{% raw %}{%youtube SyK3IXPITco %}{% endraw %}
:::warning
假定 $a∈Z$，$p$是一個質數，且：
$$(a,p)=1$$
則：
$$a^{p−1}≡1(mod\ p)$$

:::
$\downarrow$
[韓信點兵問題$\to$RSA 密碼系統上的應用](https://youtu.be/NkvCZ8qJ34w)

---

## Discrete Logarithms
:::spoiler Basic Definition
If $g$ is a generator of $\mathbb{Z}_n^*$, then for all $y$ there is a unique $x$ such that
$$y=g^x\ mod\ n$$
This is called discrete algorithm of $y$ and we use the notation
$$x=\log_g(y)$$
or more precisely:
$$x=\log_{g,n}(y)$$
For example:
![](https://i.imgur.com/xtTZniH.png)
:::

:::spoiler [Quadratic Residue](http://gotonsb-numbertheory.blogspot.com/2014/04/quadratic-residues.html)
> 「二次剩餘」定義
任意非零平方整數除以某個數後可能的餘數，我們稱之為「二次剩餘」。用數學式表達如下：
For $x,m≠0$, $a$ is a **quadratic residue** $mod\ m$ if $x^2=a\ (mod\ m)$. Otherwise, $a$ is a **quadratic nonresidue(二次非剩餘)**.
>
>例如對模10而言，可能的餘數集合為{0,1,4,5,6,9}：
$$
\left\{ 
  \begin{array}{c}
    0^2≡0\\
    1^2≡1\\
    2^2≡4\\
    3^2≡9\\
    4^2≡6\\
    5^2≡5\\
    6^2≡6\\
    7^2≡9\\
    8^2≡4\\
    9^2≡1
  \end{array}
  \ \ mod\ 10
\right.
$$
:::

:::spoiler [Blum Integers](https://blog.csdn.net/qq_41359358/article/details/113715657)
簡單來說就是一個整數$N\in\mathbb{Z}$, 是兩個質數的乘積$N=p*q$，而$p,\ q$剛好滿足
$$
\begin{aligned}
3&= q\ (mod\ 4)\\
3&= p\ (mod\ 4)
\end{aligned}
$$
例如：
$$
\begin{aligned}
33&=3*11\\
3&= 3\ (mod\ 4)\\
3&= 11\ (mod\ 4)\\\
or\\
21&=3*7\\
3&= 3\ (mod\ 4)\\
3&= 7\ (mod\ 4)
\end{aligned}
$$
:::

:::spoiler Legendre Symbol
課本定義：Let $p$ be an odd prime and $a$ an integer. The Legendre symbol is defined to be
$$
\left(\dfrac{a}{p}\right)=
\left\{
  \begin{array}{c}
    0,\ if\ p|a\\
    1,\ if\ a\in Q_p\\
    -1,\ if\ a\in \overline{Q}_p
  \end{array}
\right.
$$

代表的意義就是當$a$相對於$p$可以開根號的話，Legendre Symbol就是$1\to$Quadratic Residue，否則就是$0\to$Nonquadratic Residue
:::

:::spoiler [橢圓曲線密碼學Elliptic Curve Cryptography, ECC(觀念篇)](https://ithelp.ithome.com.tw/articles/10251031)

### Description
> 橢圓曲線密碼學（英語：Elliptic Curve Cryptography，縮寫：ECC）是一種基於橢圓曲線數學的公開密鑰加密演算法。橢圓曲線在密碼學中的使用是在1985年由Neal Koblitz和Victor Miller分別獨立提出的。
>
> ECC的主要優勢是它相比RSA加密演算法使用較小的密鑰長度並提供相當等級的安全性[1]。ECC的另一個優勢是可以定義群之間的雙線性映射，基於Weil對或是Tate對；雙線性映射已經在密碼學中發現了大量的應用，例如基於身份的加密。
> 
>![](https://i.imgur.com/0X9aTNr.png)

### Terminology
* 橢圓曲線
橢圓曲線是由以下形式的方程式定義 的平面曲線

$${\displaystyle y^{2}=x^{3}+ax+b,\ where\ a,b \in \mathbb{Z}}\to Weierstrass方程式$$
![](https://i.imgur.com/kI5v9LO.png)

* 橢圓曲線運算規則(群組規則, Group)
    * Addition
        > 過曲線上的兩點$P$、$Q$畫一條直線，找到直線與橢圓曲線的交點 $-R$
        交點關於$x$軸對稱位置的點，定義為$PQ$，即為加法。如下圖所示：$P+Q = R$
        ![](https://i.imgur.com/EaWrb4c.png)
    
    * Multiplication(兩倍運算)
        > 上述方法無法解釋$PP$，即兩點重合的情況。因此在這種情況下，將橢圓曲線在$P$點的切線，與橢圓曲線的交點，交點關於$x$軸對稱位置的點，定義為$P+P$，即$2P$，即為二倍運算
        ![](https://i.imgur.com/xmjQKQi.png)
    
    * 無窮遠點
        > 如果將$A$與$-A$相加，過$A$與$-A$的直線平行於$y$軸，可以認為直線與橢圓曲線相交於無窮遠點。
        ![](https://i.imgur.com/eJLZXfq.png)

* Properties
    * 曲線上的任何點都以X軸反射(y=0),並且仍是同樣的曲線 (奇特的對稱性)
    * 任何不垂直的線穿過曲線最多只會有三個交點
* How to use the properties in Encryption System?
    > 將橢圓曲線比喻成擊球遊戲, 把球從A點擊向B點,當再碰撞到曲線上的點後會反彈到(x軸以上或以下)另一邊的C點，先想像成把球在兩個點移動稱為"打點(dot)"
    >
    >A dot B = C
    >A dot A = B
    >A dot C = D
    >... ... ...
    >
    >這裡只有兩個點(稱為: 最初點&最終點)，將最初的點P自行打點 n次(as Private Key) 會得到一個最終點Q(as Public Key)即使你知道"最初點"和"最終點"，要找出n是非常非常之困難!
    ![](https://i.imgur.com/OrZNQfE.gif)

:::info
> 橢圓曲線是連續的，容易被推算，因此，並不適合用於加密；所以，我們必須把橢圓曲線變成離散的點

至於怎麼轉換可見原文，但轉換前後如下圖所示:
<center class="half">
    <img src="https://i.imgur.com/xmjQKQi.png" width="300" height="300"/><img src="https://i.imgur.com/CDI9wVH.png" width="300" height="300"/>
</center>
:::

:::spoiler Elliptic Curve Cryptography Application
* Application
    * RSA 同演算法可以直接實現簽章及加密，ECC 需要分別實作
    * ECDSA (Elliptic Curve Digital Signature Algorithm)
    * ECIES (Elliptic Curve Integrated Encryption Scheme)
    * ECDH (Elliptic Curve Diffie–Hellman key Exchange)
    * TLS/SSL 數位憑證
    * 基於身份加密
    * 區塊鏈數位簽名
    * 序號產生驗證
* ECC 安全性
    > ECC 一樣採用數學難題，進行設計，但難度比REA 質因數分寫還要難，而且運算比RSA 還要快
    :::warning
    詳細例子的計算過程以及前面提到的有關橢圓曲線的描述可以參考(大推，講得非常清楚): [Elliptic Curve Diffie Hellman](https://youtu.be/F3zzNa42-tQ)
    :::

:::spoiler Discrete Logarithm Problem
課本的說明：
> $(G\ \times)$是abelian group，在給定$g,\ h \in G$的情況下，要找到一個$x$(若其存在)使得$g^x=h$
> 在$(\mathbb{Z}/\mathbb{NZ},\ +)$很簡單
> 在$(GF(p),\ +)$很困難(hard)
> 在Elliptic Curve groups超級困難