---
title: 'How to Securely Collaborate on Data: Decentralized Threshold HE and Secure Key Update - Notes'
tags: [Meeting Paper, NTU]

category: "Survey Papers/Crypto"
---

# How to Securely Collaborate on Data: Decentralized Threshold HE and Secure Key Update - Notes
<!-- more -->
###### tags: `Meeting Paper` `NTU`
:::info
Kim, E., Jeong, J., Yoon, H., Kim, Y., Cho, J., & Cheon, J. H. (2020). How to securely collaborate on data: Decentralized threshold he and secure key update. IEEE Access, 8, 191319-191329.
:::
[TOC]

## Background

### [Threshold Homomorphic Encryption - 閾值同態加密在隱私計算中的應用](https://www.cnblogs.com/pam-sh/p/16446840.html)
:::spoiler 
> 1. 單密鑰同態加密
只有一個私鑰，且不同公鑰加密的密文無法相互計算。
> 2. 閾值同態加密（多密鑰加密）
支持多個私鑰，不同公鑰加密的密文可以互相計算。
> #### 問題
> 1. 多方聯合計算最安全的途徑是各自生成、保存公私鑰,但由於算法限制,不同公鑰加密的信息無法進行相互計算,導致隱私計算無法進行
> 2. 假設多方使用一套公私鑰,雖然計算可以順利進行,但系統安全性會大大下降,系統中只要有一方被成功攻擊,私鑰就會泄露。
> 3. 假設多方使用一套公私鑰,則無法決定由哪個參與方生成公私鑰
> #### Solution - Threshold Homomorphic Encryption
> 由於單密鑰同態加密在實際應用中存在諸多關於密鑰使用、管理的問題,閾值同態加密(多密鑰同態加密)應運而生。簡單來說,閾值同態加密算法中存在多個私鑰、一個(或多個公鑰,使用該公鑰系統加密的密文之間可以相互計算,並且只有當參與解密的私鑰數量達到一定閾值時,才能成功解密密文,所以這種多密鑰同態加密算法又被稱為閾值同態加密
> #### Definition
> 閾值同態加密算法同樣可以概括為以下4個函數。(,,)
> * $(pk, sk, ek) \leftarrow Keygen(Params)$: 密鑰生成函數,其中$pk$是公鑰、$sk$是私鑰、$ek$是用於計算的密鑰
> * $c \leftarrow Enc(pk, m)$: 加密函數,使用公鑰$pk$加密明文$m$信息得到密文$c$
> * $m \leftarrow Dec(c, sk_1, sk_2,\cdot \cdot \cdot ,sk_k)$: 解密函數,最少$k$個私鑰參與，才能解密得到明文
> * $c \leftarrow Eval((c_1,pk_1,ek_1), (c_2, pk_2, ek_2), \cdot \cdot \cdot , (c_N, pk_N, ek_N))$: 密文計算函數，在多個密文上進行計算、獲得最終結果，計算過程需要密鑰$ek$參與
:::

### [Learning with Errors (LWE)](https://zhuanlan.zhihu.com/p/621070457)


### [多密鑰同態加密](https://blog.csdn.net/weixin_43476788/article/details/105388612)
:::spoiler 
> 多密鑰同態加密的概念，以及基於NTRU密碼系統的具體實現，最早由L’opez-Alt等人描述。該方案的一個缺點是，在密鑰生成時必須知道參與方數量的上限，因為參數隨著參與方數量的增加而增加。(類似的實現在LWE下是可能的，但它只支持固定數量的參與方)
:::

### [Norm](https://ch-hsieh.blogspot.com/2010/04/norm.html) / [Infinity Norm](https://juejin.cn/post/7022248588767920142)
:::spoiler 
> Norm：一般翻譯成範數
(在英語中 norm 有規範的意思，比如我們說normalization就是把某種東西/物品/事件 做 正規化，也就是加上規範使其正常化)，不過個人認為其實翻譯成 範數 也是看不懂的...這邊建議把 Norm 想成長度就好 (事實上norm是長度的抽象推廣)，
>
>也許讀者會認為好端端的長度不用，為何又要發明一個 norm 來自討苦吃?? 既抽象又艱澀。
>
>事實上想法是這樣的：
>比如說現在想要比較兩個數字 $3 , 5$ 之間的大小，則我們可以馬上知道 $3<5$；同樣的，如果再考慮小數與無理數如 $1.8753$ 與 $π$，我們仍然可以比較大小 $1.8753<π=3.1415...$ 故可以發現我們有辦法對 "純量" 做明確的比大小，WHY? 因為前述例子中 $3, 5, 1.8753$ or $π$ 其各自的大小有辦法被 "measure "!
>
>但是如果是現在考慮的是一組數字 我們如何去measure 其大小呢?? 比如說
> $$x:=[1, -2, 0.1, 0 ]^T$$
> 上式的大小該是多少? 是 $1? −2? 0.1???$
>再者如果更過分一點，我們考慮一個矩陣
> $$A = \left[ {\begin{array}{*{20}{c}} 
1&2\\ 
3&4 
\end{array}} \right]$$
也正是如此，可以發現我們確實需要新的 "長度" 的定義來幫助我們如何去 measure 矩陣/向量/甚至是函數的大小。
>
>故此，我們首先定義甚麼是Norm，(也就是把 "長度" or "大小" 的本質抽離出來)

---
>L-infinity norm給出了一個向量的每個元素中最大的那個元素幅值。
例如，對於向量 $X= [-6, 4, 2]$，其 L-infinity norm就是$6$。
在L-infinity norm中，只有最大的元素有才具有影響。因此，例如，如果你的向量代表建造一座建築物的成本，通過最小化L-infinity norm，我們就可以做到減小建築物最昂貴的那部分成本。
:::



## In This Paper

### Threshold HE VS. Multi-Key HE
兩者的差別依照原文的解釋是整合之前產生共同的公鑰的就是Threshold HE，而在整合之後產生公鑰的就是Multi-Key HE

### Proactive Secrete Sharing
:::spoiler 
> 主動式秘密共享方案是指對移動敵手安全的秘密共享方案，這些敵手可以在一段時間內監視秘密共享者，但對一個時間單位內可訪問的共享者數量有限制。為了保護共享的秘密不被對手發現，應定期更新共享的秘密，使共享的秘密保持不變，以前的共享不再有用
:::

### [What is Homomorphic encryption evaluation key](https://crypto.stackexchange.com/questions/73176/what-is-homomorphic-encryption-evaluation-key)
:::spoiler 
> ### In short
>
>Public key is used to encrypt, private key is used to decrypt, and evaluation key is used to perform homomorphic operations (usually, homomorphic product or, the somehow equivalent operation, a logic AND gate).
>### In detail
>
>Public and private keys in homomorphic encryption (HE) schemes are just the same as in other types of schemes.
>
>The evaluation key ($evk$) is also public, it is typically generated using the private key, and it is used to control the noise growth or the ciphertext expansion during homomorphic evaluation.
>
>Some schemes have a "Key-switching" key instead of the evaluation key, but they are more or less the same. For instance, in the description of FV and YASHE, you can see that to perform a homomorphic product, one first multiplies the ciphertexts, $\tilde{c}_{mult} := c_1 \otimes c_2$, then uses this "extra public key" to adjust $\tilde{c}_{mult}$, that is, to get a ciphertext cmult
>
>with the correct dimension and that can be decrypted using the original secret key.
>
>So, in general, this is how you use $evk$: you perform a homomorphic operation that introduces a lot of noise or that generates a ciphertext in higher dimension, then you perform an extra operation using $evk$ to "correct" that ciphertext.
:::