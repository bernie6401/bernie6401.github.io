---
title: Cryptography and Network Security – Homework 1
tags: [NTUCNS, NTU]

category: "Security/Course/NTU CNS/Homework"
---

# Cryptography and Network Security – Homework 1
<!-- more -->

[![hackmd-github-sync-badge](https://hackmd.io/Tq2dPdTKQv6p3AvNbmyNig/badge)](https://hackmd.io/Tq2dPdTKQv6p3AvNbmyNig)

###### tags: `NTUCNS`
:::spoiler TOC
[TOC]
:::
:::info
[Official Solution](https://hackmd.io/@uqzWTXyyTk6IYTBwcPwnoA/BJZNQfcTo)
:::
Student ID: `R11921A16`
Name: 何秉學

## Handwriting

### 1. CIA
**Ans:** 
**Confidentiality** means all of the sensitive messages or information that can be protected so that just the people who have the authentication can edit or browse the information.

**Integrity** refers to the completeness of the message you transferred and ensured that the message is not altered by an unauthenticated person.

**Availability** means the system must be workable during the service time. In addition, the latency during querying is tolerable and is as short as possible.

The real-world instance including these security requirements is the bank duty system. That is, it must be guaranteed that the sensitive message is not accessible during transferring time such as the account information, bank card id, especially the bank card password, etc. Furthermore, the bank system must maintain the completeness of its service such as website service and the querying time must be tolerable. Moreover, it must ensure the data is safe that won't be altered by anybody during transmission.

### 2. Hash Function
**Ans:**
**one-wayness** means a function $y=f(x)$ is one-way if it is easy to compute $y$ from $x$ but "hard" to compute $x$ from $y$. For instance, it's usually used for password storage and data encryption such as RSA or Diffie-Hellman, to generate keys that are used to encrypt and decrypt data.

**weak collision resistance**: For given $m$ then find (compute) a collision $(m, m’)$ is difficult. That is, $h(m)=h(m')$ is hard to find $m'$ when $m$ is given. This objective is for the integrity of data. For instance, it's usually used to verify file integrity or password verification. When the user uploads a file or enters the password, the hash value must be the same as the data stored in the database.

**strong collision resistance**: Difficult to find a (some) collision $(m, m’)$. That is, it's difficult(computationally infeasible) to find any two value that has the same hash value. For example, digital signatures and message authentication codes will use this concept to construct the algorithm. This concept can guarantee that the digital signature is unique furthermore, it's infeasible for attackers to find the collision.
    
    
### 3. Multi-prime RSA
1. Ans: Assume $c$ is the cipher that encrypted by RSA, $d$ is the inverse of chosen $e$, and $n$ is the multiplication result of two prime.
$$
c^d\ mod\ n=(m^e)^d\ mod\ n=m^{ed}\ mod\ n=m^1\ mod\ n=m,\ \because d \equiv e^{-1}\ mod\  \phi(N)
$$

2. Ans: First reason: it's easily to find $p=q=\sqrt{N}$ when $N$ is given.
Second reason: when $p=q$, some message that $x∈\{0…N−1\}$ can not be decrypted while $x≡0\ (mod\ p)$. However, this is not a big problem if two prime number is as big as enough.
3. Ans: WLOG, we can use 3-prime number as RSA parameters and we can also use CRT(Chinese Remainder Theorem) to optimize the problem $M \equiv C^d\ (mod\ N)$, where $N=P_1*P_2*P_3$ and also they're pairwise coprime. So, our objective is to find what $M$ is that we just try to decrypt a cipher $C$. Also, we wonder if CRT can optimize the computation process.

    First, we assume
    $$
    \left\{ 
      \begin{array}{c}
        x\ \equiv \ m_1\ (mod\ P_1) \\ 
        x\ \equiv \ m_2\ (mod\ P_2) \\ 
        x\ \equiv \ m_3\ (mod\ P_3)
      \end{array}
    \right.
    \ \ and\ \ 
    \left\{ 
      \begin{array}{c}
        m_1\ \equiv \ C^d\ (mod\ P_1) \\ 
        m_2\ \equiv \ C^d\ (mod\ P_2) \\ 
        m_3\ \equiv \ C^d\ (mod\ P_3)
      \end{array}
    \right.
    $$

    Second, we have to compute what is $m_1$, $m_2$, $m_3$ by using Fermat's Little Theorem, which is defined as following:
    :::info
    If $P$ is a prime number, then $a^P \equiv a\ (mod\ P)$.
    If $P$ is a prime number and $a$ is not divisible by $P$, i.e. $a \equiv b\ (mod\ P)\ where\ b \ne 0$, then $a^{P-1} \equiv 1\ (mod\ P)$.
    :::

    $$
    \left\{ 
      \begin{array}{c}
          \begin{aligned}
            m_1\ &≡ \ C^d\ (mod\ P_1) \\
            &≡\ (C^{P_1-1})^{\alpha_1}*C^{\beta_1}\ (mod\ P_1) \\
            &≡\ C^{\beta_1}\ (mod\ P_1)
            \end{aligned}
      \end{array}
      \ \because\ (C^{P_1-1})^{\alpha_1}=1
    \right.
    $$
    $$
    \left\{ 
      \begin{array}{c}
          \begin{aligned}
            m_2\ &≡ \ C^d\ (mod\ P_2) \\
            &≡\ (C^{P_2-1})^{\alpha_2}*C^{\beta_2}\ (mod\ P_2) \\
            &≡\ C^{\beta_2}\ (mod\ P_2)
            \end{aligned}
      \end{array}
      \ \because\ (C^{P_2-1})^{\alpha_2}=1
    \right.
    $$
    $$
    \left\{ 
      \begin{array}{c}
          \begin{aligned}
            m_3\ &≡ \ C^d\ (mod\ P_3) \\
            &≡\ (C^{P_3-1})^{\alpha_3}*C^{\beta_3}\ (mod\ P_3) \\
            &≡\ C^{\beta_3}\ (mod\ P_3)
            \end{aligned}
      \end{array}
      \ \because\ (C^{P_3-1})^{\alpha_3}=1
    \right.
    $$

    Third, we can compute $x$ by using $m_1$, $m_2$, $m_3$ and CRT
    We compute two of them first.
    $$
    \left\{ 
      \begin{array}{c}
        x\ \equiv \ m_1\ (mod\ P_1) \\ 
        x\ \equiv \ m_2\ (mod\ P_2)
      \end{array}
    \right.
    $$
    At the beginning, we use Euclidean Algorithm to construct $1=aP_1+bP_2$ where $\{a,\ b\} \in \mathbb{Z}$, then $x=aP_1m_2+bP_2m_1+P_1P_2k'$ where $\{a,\ b,\ k'\} \in \mathbb{Z}$
    $$x \equiv aP_1m_2+bP_2m_1\ (mod\ P_1P_2)$$
    Next, we compute the rest of them and repeat the previous step
    $$
    \left\{ 
      \begin{array}{c}
      \begin{aligned}
        x &≡ aP_1m_2+bP_2m_1\ (mod\ P_1P_2) \\ 
        x &≡ \ m_3\ (mod\ P_3)
        \end{aligned}
      \end{array}
    \right.
    $$
    To construct $1=cP_3+dP_1P_2$ by using Euclidean Algorithm then $x=cP_3(aP_1m_2+bP_2m_1)+dP_1P_2m_3+P_1P_2P_3k''$ where $\{a,b,c,d,k',k''\} \in \mathbb{Z}$
    And done, the $x$ is uniquely equivalent to $M$ that what we want.

    ---
    We can make an instance to prove the correctness.
    Assume $P_1=3$, $P_2=7$, $P_3=13$ and $n=3×7×13=273$，$φ(n)= 2×6×12=144$，we choose $e=5$，and the inverse of $e$ is $d=29$

    Encryption: $c= m^e\ (mod\ n)=18^5\ mod\ 273=135$
    Decryption: $m= c^d\ (mod\ n)=135^{29}\ mod\ 273=18$

    Now, we use CRT to optimize the computation process
    Assume
    $$
    \left\{ 
      \begin{array}{c}
        x\ \equiv \ m_1\ (mod\ 3) \\ 
        x\ \equiv \ m_2\ (mod\ 7) \\ 
        x\ \equiv \ m_3\ (mod\ 13)
      \end{array}
    \right.
    \ \ and\ \ 
    \left\{ 
      \begin{array}{c}
        m_1\ \equiv \ 135^{29}\ (mod\ 3) \\ 
        m_2\ \equiv \ 135^{29}\ (mod\ 7) \\ 
        m_3\ \equiv \ 135^{29}\ (mod\ 13)
      \end{array}
    \right.
    $$

    Then
    $$
    \left\{ 
      \begin{array}{c}
          \begin{aligned}
            m_1\ &≡ \ 135^{29}\ (mod\ 3) \\
            &≡\ (135^2)^{14}*135^1\ (mod\ 3) \\
            &≡\ 135\ (mod\ 3) \\
            &≡\ 0\ (mod\ 3)
            \end{aligned}
      \end{array}
      \ \because\ (135^2)^{14}=1
    \right.
    $$
    $$
    \left\{ 
      \begin{array}{c}
          \begin{aligned}
            m_2\ &≡ \ 135^{29}\ (mod\ 7) \\
            &≡\ (135^6)^{4}*135^5\ (mod\ 7) \\
            &≡\ 2^5\ (mod\ 7) \\
            &≡\ 4\ (mod\ 7)
            \end{aligned}
      \end{array}
      \ \because\ (135^6)^{4}=1
    \right.
    $$
    $$
    \left\{ 
      \begin{array}{c}
          \begin{aligned}
            m_3\ &≡ \ 135^{29}\ (mod\ 13) \\
            &≡\ (135^{12})^{2}*135^5\ (mod\ 13) \\
            &≡\ 5^5\ (mod\ 13) \\
            &≡\ 5\ (mod\ 13)
            \end{aligned}
      \end{array}
      \ \because\ (135^{12})^{2}=1
    \right.
    $$

    Next, we can start to compute $x$.
    $$
    \left\{ 
      \begin{array}{c}
        x\ \equiv \ 0\ (mod\ 3) \\ 
        x\ \equiv \ 4\ (mod\ 7) \\ 
        x\ \equiv \ 5\ (mod\ 13)
      \end{array}
    \right.
    $$
    We compute 2 of them first.
    The $gcd(3,7)=1$, so we tried to construct $1=1*7+(-2)*3\ \to$
    $$
    \begin{aligned}
    x&=7*1*0+3*(-2)*4+21k\\
    &=-24+21k,\ k \in \mathbb{Z}\\
    x&\equiv 18\ (mod\ 21) 
    \end{aligned}
    $$
    Then we compute
    $$
    \left\{ 
      \begin{array}{c}
      x\equiv 18\ (mod\ 21) \\
      x\equiv \ 5\ (mod\ 13)
      \end{array}
    \right.
    $$
    Repeat previous step, the $gcd(13,21)=1$, then we can construct $1=21*5+13*(-8)$
    $$
    \begin{aligned}
    x&=21*5*5+13*(-8)*18+21*13k' \\
    &=-1347+273k' \\
    x&=18,\ if\ k'=5
    \end{aligned}
    $$

    Finally, we decrypt $M=x=18$ successfully by using CRT to optimize the whole computation process.

4. Ans: The advantages of the multi-prime RSA algorithm are mainly manifested in two aspects:
    1. It can reduce the calculation amount of key generation.
    2. The application of CRT can reduce the calculation amount of decryption and signature.

    On the other hand, the smaller the prime factor, the easier it is to factorize large numbers. Data published by RSA Laboratories shows that the more prime numbers used, the lower the RSA strength. The following table lists the amount of computation (unit: MIPS·year) required to break the 2-to-multiple prime RSA system.
    
    So, here is another disadvantage of multi-prime RSA that requires larger key sizes to achieve the same level of security as regular RSA. This can lead to slower encryption and decryption times and larger storage requirements for keys.

    | Key Length | 2 Prime Number | 3 Prime Number |4 Prime Number|5 Prime Number|
    | ---------- | -------- | -------- | --- | --- |
    |512 bits|$2.1*10^6$|Easy|Very Easy|Very Very Easy|
    |768 bits|$4.0*10^{11}$|$1.2*10^8$|Easy|Very Easy|
    |1024 bits|$1.4*10^{16}$|$3.0*10^{11}$|$2.1*10^8$|Easy|
    |1536 bits|$8.2*10^{23}$|$1.8*10^{17}$|$1.9*10^{13}$|$4.2*10^{10}$|
    |2048 bits|$3.8*10^{30}$|$1.5*10^{22}$|$3.2*10^{17}$|$2.3*10^{14}$|


5. (skip)


### 4. Fun With Semantic Security
I'll prove all these theorem by contrapositive. In addition, the premise of these question is that $E(Enc(k,\ m),\ Dec)$ is $S.S.$(semantic secure), so $|Pr[Exp^{SS}(0)=1]-Pr[Exp^{SS}(1)=1]| \le \varepsilon$
Assume $f(\cdot )$ is a guessing function that adversary used to guess $b'$ by the return value from challenger. The model is the same as lecture taught shown as below. Assume $\mathbb{K},\mathbb{M}$ are both group with a binary operation $+$ and $\{k,m\} \xleftarrow{R} (\mathbb{K},\mathbb{M})$
![](https://i.imgur.com/jBohSG4.png)

1. Ans: Assume $SS_{adv}[B, E']$ is negligible $\implies\ SS_{adv}[A, E]$ is negligible. Therefore, I can use contrapositive to prove if $E(Enc, Dec)$ is not $S.S.\ \implies E'(Enc', Dec')$ is not $S.S.$ as well. Because there must exist a magic function $f(\cdot)$ that can guess $b'$ with high confidence $\varepsilon' \gt \varepsilon$

    Assume $c=Enc(k,\ m_b)$ and $E$ is not $S.S.$, then we know
    $$
    \begin{aligned}
    SS_{adv}[c,\ E]&=|Pr[Exp^{SS}(0)=1]-Pr[Exp^{SS}(1)=1]| \\
    &=|Pr[b'=1|b=0]-Pr[b'=1|b=1]| \\
    &=|Pr[f(c)=1|b=0]-Pr[f(c)=1|b=1]| \\
    &=|Pr[f(Enc(k,\ m_b))=1|b=0]-Pr[f(Enc(k,\ m_b))=1|b=1]| \\
    &=|Pr[f(Enc(k,\ m_0))=1]-Pr[f(Enc(k,\ m_1))=1]| \gt \varepsilon
    \end{aligned}
    $$

    But how about $E'$ that defined a new decryption cipher? We also can use the magic function that found in original decryption cipher to address this question.
    $$
    \begin{aligned}
    SS_{adv}[c,\ E']&=|Pr[Exp^{SS}(0)=1]-Pr[Exp^{SS}(1)=1]| \\
    &=|Pr[b'=1|b=0]-Pr[b'=1|b=1]| \\
    &=|Pr[f(c||r)=1|b=0]-Pr[f(c||r)=1|b=1]| \\
    &=|Pr[f(Enc(k,\ m_b)||r)=1|b=0]-Pr[f(Enc(k,\ m_b)||r)=1|b=1]|
    \end{aligned}
    $$
    Though, we don't know the length of $r$ (i.e. $|r|$), we still can repeat the guessing process while decrease the 1 byte of $c||r$ for each time until the parameter of function $f(\cdot)$ is $|c|$, then I can still aware of the guessing result with high confidence.
    That is 
    $$
    \begin{aligned}
    SS_{adv}[c,\ E']&=|Pr[f(Enc(k,\ m_b)||r)=1|b=0]-Pr[f(Enc(k,\ m_b)||r)=1|b=1]| \\
    &= |Pr[f(Enc(k,\ m_b))=1|b=0]-Pr[f(Enc(k,\ m_b))=1|b=1]| \\
    &= |Pr[f(Enc(k,\ m_0))=1]-Pr[f(Enc(k,\ m_1))=1]| \gt \varepsilon
    \end{aligned}
    $$

    Then, we know that if $E$ is not $S.S.$, then $E'$ is not $S.S.$ as well. In other words, if $E$ is $S.S.$, then $E'$ is $S.S.$ definitely.

2. Ans: Follow the concept above and we assume $m'=m+r$ and $m_b' = m_b+r$. 
    Premise: $E(Enc(k,m), Dec(\cdot))$ is $S.S.$ then $E(Enc(k,m+r), Dec(\cdot))$ is $S.S.$ as well where $r \xleftarrow{R} \mathbb{M}$. Because $\mathbb{M}$ is a group that with a binary operation +, $m+r\in \mathbb{M}$ which means $E(Enc'(k,m_b'),\ Dec(\cdot))$ is $S.S.$ as well.

    Again, if $E(Enc, Dec)$ is not $S.S.$ then there must exist a magic function $f'(\cdot)$ that can guess $b'$ with high confidence $\varepsilon' \gt \varepsilon$

    Assume $c=Enc(k,\ m_b')$ and $E$ is not $S.S.$, then we know
    $$
    \begin{aligned}
    SS_{adv}[c,\ E]&=|Pr[Exp^{SS}(0)=1]-Pr[Exp^{SS}(1)=1]| \\
    &=|Pr[b'=1|b=0]-Pr[b'=1|b=1]| \\
    &=|Pr[f'(c)=1|b=0]-Pr[f'(c)=1|b=1]| \\
    &=|Pr[f'(Enc(k,\ m_b'))=1|b=0]-Pr[f'(Enc(k,\ m_b'))=1|b=1]| \\
    &=|Pr[f'(Enc(k,\ m_0'))=1]-Pr[f'(Enc(k,\ m_1'))=1]| \gt \varepsilon
    \end{aligned}
    $$

    But how about $E'$ that defined a new decryption cipher? We also can use the magic function that found in original decryption cipher to address this question.
    $$
    \begin{aligned}
    SS_{adv}[c,\ E']&=|Pr[Exp^{SS}(0)=1]-Pr[Exp^{SS}(1)=1]| \\
    &=|Pr[b'=1|b=0]-Pr[b'=1|b=1]| \\
    &=|Pr[f'(Enc'(k,\ m_b+r)||r)=1|b=0]-Pr[f'(Enc'(k,\ m_b+r)||r)=1|b=1]|
    \end{aligned}
    $$
    Again, we don't know $|r|$, we still can repeat the guessing process while decrease the 1 byte of $c||r$ for each time (i.e. $f'([Enc'(k,m_b')||r][:-j])$ where $j=\{1,\cdots,|r|\}$).
    In a word,
    $$
    \begin{aligned}
    SS_{adv}[c,\ E']&=|Pr[f'(Enc(k,\ m_b')||r)=1|b=0]-Pr[f'(Enc'(k,\ m_b')||r)=1|b=1]| \\
    &= |Pr[f'(Enc(k,\ m_b'))=1|b=0]-Pr[f'(Enc(k,\ m_b'))=1|b=1]| \\
    &= |Pr[f'(Enc(k,\ m_0'))=1]-Pr[f'(Enc(k,\ m_1'))=1]| \gt \varepsilon
    \end{aligned}
    $$

    Then, we know that if $E$ is not $S.S.$, then $E'$ is not $S.S.$ as well. In other words, if $E$ is $S.S.$, then $E'$ is $S.S.$ definitely.


3. Ans: Follow the concept of previous 2 questions and we assume $k'=k+r$. 
    Premise: $E(Enc(k,m), Dec(\cdot))$ is $S.S.$ then $E(Enc(k+r,m), Dec(\cdot))$ is $S.S.$ as well where $r \xleftarrow{R} \mathbb{K}$. Because $\mathbb{K}$ is a group that with a binary operation +, $k+r\in \mathbb{K}$ which means $E(Enc'(k',m_b),\ Dec(\cdot))$ is $S.S.$ as well.

    Again, if $E(Enc, Dec)$ is not $S.S.$ then there must exist a magic function $f''(\cdot)$ that can guess $b'$ with high confidence $\varepsilon' \gt \varepsilon$

    Assume $c=Enc(k',\ m_b)$ and $E$ is not $S.S.$, then we know
    $$
    \begin{aligned}
    SS_{adv}[c,\ E]&=|Pr[Exp^{SS}(0)=1]-Pr[Exp^{SS}(1)=1]| \\
    &=|Pr[b'=1|b=0]-Pr[b'=1|b=1]| \\
    &=|Pr[f''(c)=1|b=0]-Pr[f''(c)=1|b=1]| \\
    &=|Pr[f''(Enc(k',\ m_b))=1|b=0]-Pr[f''(Enc(k',\ m_b))=1|b=1]| \\
    &=|Pr[f''(Enc(k',\ m_0))=1]-Pr[f''(Enc(k',\ m_1))=1]| \gt \varepsilon
    \end{aligned}
    $$

    But how about $E'$ that defined a new decryption cipher? We also can use the magic function that found in original decryption cipher to address this question.
    $$
    \begin{aligned}
    SS_{adv}[c,\ E']&=|Pr[Exp^{SS}(0)=1]-Pr[Exp^{SS}(1)=1]| \\
    &=|Pr[b'=1|b=0]-Pr[b'=1|b=1]| \\
    &=|Pr[f''(Enc'(k',\ m_b)||r)=1|b=0]-Pr[f''(Enc'(k',\ m_b)||r)=1|b=1]|
    \end{aligned}
    $$
    Again, we don't know $|r|$, we still can repeat the guessing process while decrease the 1 byte of $c||r$ for each time (i.e. $f'([Enc'(k,m_b')||r][:-j])$ where $j=\{1,\cdots,|r|\}$).
    In a word,
    $$
    \begin{aligned}
    SS_{adv}[c,\ E']&=|Pr[f''(Enc(k',\ m_b)||r)=1|b=0]-Pr[f''(Enc'(k',\ m_b)||r)=1|b=1]| \\
    &= |Pr[f''(Enc(k',\ m_b))=1|b=0]-Pr[f''(Enc(k',\ m_b))=1|b=1]| \\
    &= |Pr[f''(Enc(k',\ m_0))=1]-Pr[f''(Enc(k',\ m_1))=1]| \gt \varepsilon
    \end{aligned}
    $$

    Then, we know that if $E$ is not $S.S.$, then $E'$ is not $S.S.$ as well. In other words, if $E$ is $S.S.$, then $E'$ is $S.S.$ definitely.


## CTF

### 5. Simple Crypto

#### Recon
* Round 1
Just simple ROT-13
* Round 2
Just simple rail fence cipher
* Round 3
    Can observe that the question gave the `b64encode(c1)` and `m1` and we need to decrypt to `m2` using `b64encode(c2)` it gave us. I thought about it for a long time. It seems one-time-pad reused problem. Because the length of `b64encode(c1)` and `m1` are the same. So, I `xor` them and get the key. In addition, I repeated the operation that `xor` `b64encode(c2)` and key then I got the plain text message. The whole script is as below.

    The attack can be success only if the length of `b64encode(c1)` greater than the length of `b64encode(c2)`. It means we can get enough key to decrypt `c2`, otherwise, the plain text is incomplete.
* Round 4
    Hint 1: One-layer fence is not solid enough, how about two?
    Hint 2: You can safely ignore all white spaces and punctuation marks.
    1. You can observe that every time the cipher is just changed the capital of the letter and the semantic sentence is preserved. So, we can assume that it encrypt every bits in alphabetic with its upper or lower letter(i.e. upper letter is represented to 1, otherwise, is represented to 0). Therefore, you can use the script below to transfer every character to binary.
    2. After the conversion, the length of the binary is $155$, it means we have to find something like morse code to decode it. At the beginning, my perspective is baudot code that encrypt/decrypt the code with every 5 bits. This is perfectly coincide the factor of $155$, however, nothing plaintext-like string appeared. Then I continued looking for another baudot-like cipher. The answer is bacon cipher that similar to baudot which is also encrypt/decrypt the code with every 5 bits.
    3. After the conversion, the string was still incorrect. So, I tried various methods to decrypt it. Then I think the this question mentioned fence again that means this is the advanced fence question that I should address. Therefore, I tried rail fence cipher again to decrypt it to semantic meaningful string(means I can read it as normal English).

#### Exploit
* Round 1 [ROT-Based online solver](https://gchq.github.io/CyberChef/#recipe=ROT13(true,true,false,5)&input=RGlham1odm9kamktb2N6am16b2R4dmdndCBuenhwbXo)
* Round 2 [Rail Fense Cipher online solver](https://gchq.github.io/CyberChef/#recipe=Rail_Fence_Cipher_Decode(5,0))
* Round 3 One-Time-Pad
* Round 4 Binary encrypt in Alphabetic → Bacon Cipher → Rail Fence Cipher
   4-1. Alphabet → Binary
        Alphabet → Binary
	
   ```python
   import re
   ciphertext = input("Cipher Text of Round 4: ")
   ciphertext = ciphertext.replace('!', '').replace(',', '').replace('.', '').replace(' ', '')
   plaintext = ''
   for i in range(len(ciphertext)):
      plaintext += 'A' if re.search(r"[a-z]", ciphertext[i]) else 'B'
   # print(plaintext)
   for i in range(0, len(plaintext), 5):
      print(plaintext[i:i+5], end=" ")
   ```
   4-2. [Bacon Cipher](https://gchq.github.io/CyberChef/#recipe=Bacon_Cipher_Decode('Standard%20(I%3DJ%20and%20U%3DV)','0/1',false))
   4-3. [Rail Fense Cipher online solver](https://gchq.github.io/CyberChef/#recipe=Rail_Fence_Cipher_Decode(5,0))
* Round 5 Base64 decode

   Flag 5: `CNS{5upeR_3asy_c1a55ic@l_cryp70!}`

### 6. ElGamal Cryptosystem

#### Recon
1. 6-1
![](https://i.imgur.com/2gSBJin.png)
    As the screenshot above, seems it reused $a$ that it should be chosen randomly.
    Thus, as the algorithm taught on class
    $$c_1=c_1'=(self.g)^y\ (mod\ self.P)$$
    $$c_2=(self.pk)^y\ (mod\ self.P)\ *\ flag1\ (mod\ self.P)$$
    $$c_2=(self.pk)^y\ (mod\ self.P)\ *\ m_2\ (mod\ self.P)$$

2. 6-2
3. 6-3
    Keys quantities: 5
    Threshold: 5(That means the user needs $5$ keys to generate the secret(constant term of the formula)


#### Exploit
1. 6-1
    $$tmp = (self.pk)^y\ (mod\ self.P)=c_2'*inverse(m_2,\ self.P)\ \%\ self.P$$
$$flag1 = c_2*inverse(tmp,\ self.P)\ \%\ self.P$$
    ::: spoiler source code
    ```python=
    from pwn import *
    from Crypto.Util.number import bytes_to_long, long_to_bytes
    from Crypto.Util.number import inverse

    r = remote('cns.csie.org', 6001)
    context.arch = 'amd64'

    r.recvuntil(b"P = ")
    p = int(r.recvline().strip().decode())
    r.recvuntil(b"g = ")
    g = int(r.recvline().strip().decode())
    r.recvuntil(b"cipher = (")
    c1 = int(r.recvuntil(b", ").decode().replace(", ", ""))
    c2 = int(r.recvuntil(b")").decode().replace(")", ""))

    log.info("P = {}".format(p))
    log.info("g = {}".format(g))
    log.info("c1 = {}".format(c1))
    log.info("c2 = {}".format(c2))


    m2 = '1'
    r.recvuntil(b"Do you want to encrypt something? (y/n): ")
    r.sendline(b'y')
    r.recvuntil(b"Give me your message: ")
    r.sendline(m2.encode())
    r.recvuntil(b"Your cyphertext (")
    c1_ = int(r.recvuntil(b", ").decode().replace(", ", ""))
    c2_ = int(r.recvuntil(b")").decode().replace(")", ""))

    log.info("c1\' = {}".format(c1_))
    log.info("c2\' = {}".format(c2_))
    m2 = bytes_to_long(m2.encode())
    log.info("m2 = {}".format(m2))


    tmp = c2_ * inverse(m2, p) % p
    flag = c2 * inverse(tmp, p) % p
    flag = bytes.fromhex(hex(flag).replace('0x', "")).decode('utf-8')

    log.info(flag)

    r.close()

    r.interactive()
    ```
    :::
    Flag 6-1: `CNS{n0_r3us3d_3ph3m3ra1_K3Y!}`
2. 6-2(Bonus)
3. 6-3
    Assume: $$m_n={c_1}^{f(n)}\ (mod\ self.P),\ n\in\{1,...,5\}$$where $self.P$ is a group defined by author, $c_1$ is the user-chosen string that should be decrypted
    So, I can put each of the response from the server into `Lagrange Interpolation Formula`, that is 
    $$
    \begin{aligned}
    f(x)&=ax^4+bx^3+cx^2+dx+sk\\ 
    &=f(1){(x-x_2)(x-x_3)(x-x_4)(x-x_5) \over (x_1-x_2)(x_1-x_3)(x_1-x_4)(x_1-x_5)} \\ 
    &+ f(2){(x-x_1)(x-x_3)(x-x_4)(x-x_5) \over (x_2-x_1)(x_2-x_3)(x_2-x_4)(x_2-x_5)} \\ 
    &+ f(3){(x-x_1)(x-x_2)(x-x_4)(x-x_5) \over (x_3-x_1)(x_3-x_2)(x_3-x_4)(x_3-x_5)} \\ 
    &+ f(4){(x-x_1)(x-x_2)(x-x_3)(x-x_5) \over (x_4-x_1)(x_4-x_2)(x_4-x_3)(x_4-x_5)} \\ 
    &+ f(5){(x-x_1)(x-x_2)(x-x_3)(x-x_4) \over (x_5-x_1)(x_5-x_2)(x_5-x_3)(x_5-x_4)}
    \end{aligned}
    $$
    Then if we wonder $sk$ at the constant of the formula, we can put $x=0,\ x_1=1,\ x_2=2,\ x_3=3,\ x_4=4,\ x_5=5$ into function, that is
    $$f(0)=5f(1)-10f(2)+10f(3)-5f(4)+f(5)=sk$$

    $$c_1^{sk}=m_1^5*inverse(m_2^{10},\ self.P)*m_3^{10}*inverse(m_4^5,\ self.P)*m_5$$

    :::info
    Note that, we can set $c_1=C1$ which is one return value from `ElGamal Encryption`: $\{C1, C2\} \leftarrow en_{ElGamal}(randomeNumber, message)$
    :::

    So, the flag is:
    $$
    \begin{aligned}
    flag &= C2*[inverse(C1, self.P)]^{sk}\  \% \ self.P\\
    &= C2*[inverse(C1^{sk}, self.P)]\  \% \ self.P \\
    &= C2*[inverse(c_1^{sk}, self.P)]\  \% \ self.P
    \end{aligned}
    $$
    :::spoiler 6-3 source code
    ```python=
    from pwn import *
    from Crypto.Util.number import bytes_to_long, long_to_bytes
    from Crypto.Util.number import inverse

    r = remote('cns.csie.org', 6003)
    context.arch = 'amd64'


    r.recvuntil(b"P = ")
    p = int(r.recvline().strip().decode())
    r.recvuntil(b"g = ")
    g = int(r.recvline().strip().decode())
    r.recvuntil(b"cipher = (")
    c1 = int(r.recvuntil(b", ").decode().replace(", ", ""))
    c2 = int(r.recvuntil(b")\n").decode().replace(")\n", ""))

    log.info("P = {}".format(p))
    log.info("g = {}".format(g))
    log.info("c1 = {}".format(c1))
    log.info("c2 = {}".format(c2))


    message_user_input = str(c1)
    m = []
    # print(r.recvline())
    for i in range(1, 6):
        r.recvuntil(b'Do you want to decrypt something? (y/n): ')
        r.sendline(b'y')
        r.recvuntil(b'Give me your c1: ')
        r.sendline(message_user_input.encode())
        r.recvuntil(b'(1~5): ')
        # r.recvline()
        r.sendline(str(i).encode())
        m.append(int(r.recvline().decode()))

        log.info("m{} = {}".format(i, m[-1]))


    tmp = ((m[0]**5)*inverse(m[1]**10, p)*(m[2]**10)*inverse(m[3]**5, p)*m[4]) % p
    flag = bytes.fromhex(long_to_bytes((c2 * inverse(tmp, p)) % p).hex().replace("0x", "")).decode('utf-8')

    log.info(flag)

    r.close()
    ```
    :::

    Flag 6-3: `CNS{l4gr4ng3_P0lyn0m14L_12_s0_34SY}`
    :::danger
    It may not work sometimes, so, please re-run it again
    :::
    
    
### 7. Bank

#### Recon
If I register an account, I earn `$10`. In addition, If the register name contain `I love CNS`, I can earn `$15` that `$5` for extra.
Obviously, I should find SHA-1 collision for earning extra money to buy the flag.
The main flow is like:
1. Find a string that have SHA-1 collision(assume A and B)
2. Register A account and login to earn `$10` then logout
3. Register B account
4. Login by B account
5. At this moment, the money will be saved in A account due to collision
6. Then logout and re-login A account and buy the flag(now A account should have `$20`)

#### Essential Source Code
```python=116
...
match cmd:
    case 1:
        # register
        username = input_untruncated("Username: ").strip(b"\n")
        if username in keys:
            print("The username already used, try another")
            continue

        key = keys[username] = random.randbytes(16)
        print(
            f"Here is your passkey, store it in a safe place: {base64.b64encode(key).decode()}"
        )
        h = sha1(username)
        balances[h] += NEW_USER_GIFT
        if b"I love CNS" in username:
            # good students get bonus
            balances[h] += CNS_LOVER_BONUS
...
```

#### Exploit
Just find the collision of SHA-1
:::spoiler source code
    ```python
    from pwn import *

    context.arch = 'amd64'

    for i in range(2):
        # r = process('./server.py')
        r = remote('cns.csie.org', 44377)

        magic1 = open('shattered-1.pdf', 'rb').read() + b'I love CNS'
        magic2 = open('shattered-2.pdf', 'rb').read() + b'I love CNS'

        '''Register "I love CNS and get the passkey"'''
        r.recvuntil(b'Your choice: ')
        r.sendline(b'1')
        r.recvuntil(b'Username: ')
        r.sendline(magic1)
        passkey = r.recvline().decode('utf-8').split(': ')[1].replace('\n', '')
        log.info("Normal account passkey: {}".format(passkey))

        '''Register another account that has same sha1 value with previous one'''
        r.recvuntil(b'Your choice: ')
        r.sendline(b'1')
        r.recvuntil(b'Username: ')

        r.sendline(magic2)
        passkey_collision = r.recvline().decode('utf-8').split(': ')[1].replace('\n', '')
        log.info("Collision account passkey: {}".format(passkey_collision))

        '''Login Normal Account and Get money'''
        r.recvuntil(b'Your choice: ')
        r.sendline(b'2')
        r.recvuntil(b'Username: ')
        r.sendline(magic1)
        r.recvuntil(b'Passkey in Base64: ')
        r.sendline(passkey.encode())

        '''Logout'''
        r.recvuntil(b'Your choice: ')
        r.sendline(b'1')

        '''Login Collision Account'''
        r.recvuntil(b'Your choice: ')
        r.sendline(b'2')
        r.recvuntil(b'Username: ')
        r.sendline(magic2)
        r.recvuntil(b'Passkey in Base64: ')
        r.sendline(passkey_collision.encode())

        '''Logout'''
        r.recvuntil(b'Your choice: ')
        r.sendline(b'1')

        '''Login Normal Account and Get money'''
        r.recvuntil(b'Your choice: ')
        r.sendline(b'2')
        r.recvuntil(b'Username: ')
        r.sendline(magic1)
        r.recvuntil(b'Passkey in Base64: ')
        r.sendline(passkey.encode())

        r.recvuntil(b'You have $')
        money = r.recvline().decode().split(" ")[0]
        log.info("Your money is: {}".format(money))

        r.recvuntil(b'Your choice: ')
        if i == 0:
            r.sendline(b'2')
            r.recvuntil(b'Here is your flag 1:')
            flag1 = r.recvline().strip().decode()
            log.info("Flag1: {}".format(flag1))
        elif i == 1:
            r.sendline(b'3')
            r.recvuntil(b'Here is your flag 2:')
            flag2 = r.recvline().strip().decode()
            log.info("Flag2: {}".format(flag2))

        r.close()

    r.interactive()
    ```
:::
Flag 7-1: `CNS{ha$h_i5_m15used}`
Flag 7-2: `CNS{$ha1_15_n0t_c0ll1510n_r3s1st@nt}`

### 8. Clandestine Operation

#### Recon
1. Encrypted by AES
2. Mode: CBC
3. Padding type: `PKCS#7`
4. Padding Oracle Attack
  * ::: spoiler Seems padding oracle
    `menus.py/askNahida()`
    ```python=22
    ...
    if choice == 1:
        ID = input('Please give me the ID (hex encoded): ').strip()
        try:
            decrypt(ID)
            print('Hint: It seems feasible...')
        except Exception as e:
            if e.__class__.__name__ == 'UnicodeDecodeError':
                print('Hint:', 'Not a valid ID...')
            else:
                print('Hint:', e)
    ...
    ```
    `cryptoFunc.py`
    ```python=11
    def unpad(c):
        length = c[-1]
        for char in c[-length:]:
            if char != length:
                raise paddingError('incorrect padding')
        return c[:-length]
    def decrypt(c):
        aes = AES.new(secret.key, AES.MODE_CBC, secret.iv)
        return unpad(aes.decrypt(binascii.unhexlify(c))).decode()
    ...
    ```
    :::

#### Exploit
Just padding oracle attack
:::spoiler 8-1 source code
```python=
from pwn import *
from tqdm import trange
from itertools import cycle

r = remote('cns.csie.org', 44399)
context.arch = 'amd64'


r.recvuntil(b'Your choice:')
r.sendline(b'2')


def test_validity(response, error):
    padding_correct = True if error != response else False
    return padding_correct

def split_len(seq, length):
    return [seq[i : i + length] for i in range(0, len(seq), length)]

def block_search_byte(size_block, i, pos, l):

    # If ct_pos = 10 and
    # i = 0 return: 0000000000000000000000000000000a
    # i = 1 return: 00000000000000000000000000000a
    # i = 2 return: 000000000000000000000000000a
    # ...
    # i = 15 return: 0a

    hex_char = hex(pos).split("0x")[1]
    return ("00" * (size_block - (i + 1)) + ("0" if len(hex_char) % 2 != 0 else "") + hex_char + "".join(l))

def block_padding(size_block, i):

    # It'll return 
    # '00000000000000000000000000000001'
    # '00000000000000000000000000000202'
    # '00000000000000000000000000030303'
    # ...
    # '10101010101010101010101010101010'

    l = []
    for t in range(0, i + 1):
        l.append(("0" if len(hex(i + 1).split("0x")[1]) % 2 != 0 else "") + (hex(i + 1).split("0x")[1]))
    return "00" * (size_block - (i + 1)) + "".join(l)

def hex_xor(s1, s2):
    b = bytearray()
    for c1, c2 in zip(bytes.fromhex(s1), cycle(bytes.fromhex(s2))):
        b.append(c1 ^ c2)
    return b.hex()

def call_oracle(tmp_ID):
    r.recvuntil(b'Your choice:')
    r.sendline(b'1')
    r.recvuntil(b'Please give me the ID (hex encoded): ')
    # print(tmp_ID)

    r.sendline(tmp_ID.encode())


    return r.recvline().strip().decode()



cipher = '70309f98653e87df804263d5a0348f115c36bc7c2cddfe02ffd44528083635404815ed8c0f14ad8cbbb1c7bc12bf21725fa15c0e7ba326e433ec41ddfaf41d27aa18ce4381a61d187ecbdcc9740747d300b7f354bb68139f2306508a06a04fbe'
found = False
valide_value = []
result = []
size_block = 16
len_block = size_block * 2
cipher_block = split_len(cipher, len_block)
error = 'Hint: PADDING ERROR : incorrect padding'

if len(cipher_block) == 1:
    print("[-] Abort there is only one block")
    sys.exit()

# for each cipher_block
for block in reversed(range(1, len(cipher_block))):
    if len(cipher_block[block]) != len_block:
        print("[-] Abort length block doesn't match the size_block")
        break
    print("[+] Search value block : ", block, "\n")
    # for each byte of the block
    for i in range(0, size_block):
        # test each byte max 255
        for ct_pos in range(0, 256):
            # 1 xor 1 = 0 or valide padding need to be checked
            if ct_pos != i + 1 or ( len(valide_value) > 0 and int(valide_value[-1], 16) == ct_pos ):

                bk = block_search_byte(size_block, i, ct_pos, valide_value)
                bp = cipher_block[block - 1]
                bc = block_padding(size_block, i)

                tmp = hex_xor(bk, bp)
                # print(bk)
                cb = hex_xor(tmp, bc)

                if block == 5:
                    up_cipher = cipher_block[0] + cipher_block[1] + cipher_block[2] + cipher_block[3] + cb + cipher_block[5]
                elif block == 4:
                    up_cipher = cipher_block[0] + cipher_block[1] + cipher_block[2] + cb + cipher_block[4]
                elif block == 3:
                    up_cipher = cipher_block[0] + cipher_block[1] + cb + cipher_block[3]
                elif block == 2:
                    up_cipher = cipher_block[0] + cb + cipher_block[2]
                else:
                    up_cipher = cb + cipher_block[1]

                # we call the oracle, our god
                response = call_oracle( up_cipher )

                if test_validity(response, error):
                    found = True
                    print(up_cipher)

                    # data analyse and insert in right order
                    value = re.findall("..", bk)
                    valide_value.insert(0, value[size_block - (i + 1)])

                    bytes_found = "".join(valide_value)
                    if ( i == 0 and int(bytes_found, 16) > size_block and block == len(cipher_block) - 1 ):
                        print( "[-] Error decryption failed the padding is > " + str(size_block) )
                        sys.exit()

                    print( "\033[36m" + "\033[1m" + "[+]" + "\033[0m" + " Found", i + 1, "bytes :", bytes_found, )
                    print("")

                    break
        if found == False:
            # lets say padding is 01 for the last byte of the last block (the padding block)
            if len(cipher_block) - 1 == block and i == 0:
                value = re.findall("..", bk)
                valide_value.insert(0, "01")
            else:
                print("\n[-] Error decryption failed")
                result.insert(0, "".join(valide_value))
                hex_r = "".join(result)
                print("[+] Partial Decrypted value (HEX):", hex_r.upper())
                padding = int(hex_r[len(hex_r) - 2 : len(hex_r)], 16)
                print( "[+] Partial Decrypted value (ASCII):", bytes.fromhex(hex_r[0 : -(padding * 2)]).decode(), )
                sys.exit()
        found = False

    result.insert(0, "".join(valide_value))
    valide_value = []

print("")
hex_r = "".join(result)
print("[+] Decrypted value (HEX):", hex_r.upper())
padding = int(hex_r[len(hex_r) - 2 : len(hex_r)], 16)
print("[+] Decrypted value (ASCII):", bytes.fromhex(hex_r[0 : -(padding * 2)]).decode(),)


r.interactive()
```
:::

Flag 8-1: `CNS{Aka_BIT_f1ipp1N9_atTaCk!}`

---
In plaintext of `69...` block, we need to tamper specific bytes like(`Cyno` $\to$ `Azar`).
We can xor the previous ciphertext block(`5c...`)
```bash!
>>> m1 = 'Cyno'.encode('utf-8').hex()
>>> m2 = 'Azar'.encode('utf-8').hex()
>>> hex(int(m1,16)^int(m2,16))
'0x2030f1d'
>>> hex(int('28083635',16)^int('2030f1d',16))
'0x2a0b3928'
```
So, the `xor_patch` is `0x2030f1d` that we have to xor to the cipher block, `5c...`. And we got 

![](https://imgur.com/wzdc8WN.png)
:::spoiler 8-2 source code
```python=
from pwn import *
from tqdm import trange
from itertools import cycle
from tqdm import trange

r = remote('cns.csie.org', 44399)
context.arch = 'amd64'


r.recvuntil(b'Your choice:')
r.sendline(b'1')
r.recvuntil(b'Please speak out the secret word: ')
r.sendline(b'CNS{Aka_BIT_f1ipp1N9_atTaCk!}')

# Try to find the magic number to fit the decryption decode process properly
# for i in trange(0, 2**16):
#     r.recvuntil(b'Your choice:')
#     r.sendline(b'1')
#     r.recvuntil(b'Please enter your ID (hex encoded): ')


#     ID_prefix = '70309f98653e87df804263d5a0348f11'
#     ID_fake_1 = '{0:0>4x}'.format(i)
#     ID_fake_2 = 'bc7c2cddfe02ffd445' #5C36
#     # print(ID_fake_2)
#     ID_fake_3 = '2a0b392840'  # XOR_Patch
#     ID_postfix = '4815ed8c0f14ad8cbbb1c7bc12bf21725fa15c0e7ba326e433ec41ddfaf41d27aa18ce4381a61d187ecbdcc9740747d300b7f354bb68139f2306508a06a04fbe'

#     r.sendline((ID_prefix + ID_fake_1 + ID_fake_2 + ID_fake_3 + ID_postfix).encode())

#     response = r.recvline().strip().decode()
#     # print(response)

#     if 'Authentication failed' not in response and i != 23606:
#         log.info("The magic number is: {}".format(i))
#         print(ID_prefix + ID_fake_1 + ID_fake_2 + ID_fake_3 + ID_postfix)
#         print(response)
        # break
''' The magic number is 11065(Decimal) '''

r.recvuntil(b'Your choice:')
r.sendline(b'1')
r.recvuntil(b'Please enter your ID (hex encoded): ')
ID_prefix = '70309f98653e87df804263d5a0348f11'
ID_fake_1 = '{0:0>4x}'.format(11065)
ID_fake_2 = 'bc7c2cddfe02ffd445' #5C36
ID_fake_3 = '2a0b392840'  # XOR_Patch
ID_postfix = '4815ed8c0f14ad8cbbb1c7bc12bf21725fa15c0e7ba326e433ec41ddfaf41d27aa18ce4381a61d187ecbdcc9740747d300b7f354bb68139f2306508a06a04fbe'
r.sendline((ID_prefix + ID_fake_1 + ID_fake_2 + ID_fake_3 + ID_postfix).encode())
r.recvline()
flag = r.recvline().strip().decode().split('. ')[-1]
log.info("flag = {}".format(flag))
```
:::

Flag 8-2: `CNS{W15h_y0U_hav3_a_n1c3_d@y!}`

## Reference

### Multi-prime RSA
[多素数RSA系统简介](https://blog.csdn.net/bhw98/article/details/19676)
[Why should the primes used in RSA be distinct?](https://crypto.stackexchange.com/questions/26861/why-should-the-primes-used-in-rsa-be-distinct)
[利用CRT加速RSA解密](https://youtu.be/NkvCZ8qJ34w?t=4203)
[What is multi-prime RSA (RSA-MP)?](https://crypto.stackexchange.com/questions/67043/what-is-multi-prime-rsa-rsa-mp)

---

### Classic
[MAC訊息驗證碼](https://ithelp.ithome.com.tw/articles/10188333)
[密碼雜湊函式](https://zh.wikipedia.org/wiki/%E5%AF%86%E7%A2%BC%E9%9B%9C%E6%B9%8A%E5%87%BD%E6%95%B8)
[Diffie-Hellman](http://www.tsnien.idv.tw/Security_WebBook/chap3/3-6%20Diffie-Hellman%20%E9%91%B0%E5%8C%99%E4%BA%A4%E6%8F%9B%E6%B3%95.html)
[Linux匹配文字grep指令用法教學與範例](https://blog.gtwang.org/linux/linux-grep-command-tutorial-examples/)
[How can I split multiple joined words?](https://stackoverflow.com/questions/195010/how-can-i-split-multiple-joined-words)
[subprocess --- Subprocess management](https://docs.python.org/zh-tw/3.7/library/subprocess.html)
[How to Check SHA1 Hash of a String](https://osxdaily.com/2012/06/06/check-sha1-hash-of-string/)

---

### ElGamal Cryptosystem
[Known plaintext attack on ElGamal encryption](https://crypto.stackexchange.com/questions/18362/known-plaintext-attack-on-elgamal-encryption?newreg=56d9dd5e0e4e4270854809dd8c47eeca)

---

### Bank
[長度擴充攻擊 | Length Extension Attack (LEA)](https://maojui.me/Crypto/LEA/)
[SHA-1 psuedo code](https://zh.wikipedia.org/wiki/SHA-1#SHA-0%E7%9A%84%E7%A0%B4%E8%A7%A3)
[LEA-CTF實例](https://github.com/oalieno/Crypto-Course/tree/9430c4dcb3b1666098a84b37d4c2122205003609/HASH/Length-Extension-Attack)
[HashPump教學](https://www.cnblogs.com/pcat/p/5478509.html)
[淺談HASH長度擴充攻擊](https://iter01.com/525343.html)
[SHA-1 is a Shambles](https://sha-mbles.github.io/)

---

### Clandestine Operation:
[Padding Oracle Attack - github](https://github.com/mpgn/Padding-oracle-attack/blob/master/exploit.py)
[[2022 fall] 0923 Crypto](https://youtu.be/hnXtaiyvQ3s?t=7801)