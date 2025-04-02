---
title: Cryptography Lec 4(Information Theory) - Notes
tags: [Cryptography, NTU]

---

# Cryptography Lec 4(Information Theory) - Notes
###### tags: `Cryptography` `NTU`

## Background
:::spoiler Shannon's Theorem
假設：$(P,\ C,\ K,\ e_k(\cdot),\ d_k(\cdot))$是一個cryptosystem，且$P,\ C,\ K$各自集合的數量都是一樣的
則：
$$此cryptosystem具有perfect\ secrecy\\
iff\\
每一把key被使用的機率都相同，i.e.{1 \over \#K}，且對於每個m\in P和c\in C都有一個獨立的key\ k使得e_k(m)=c
$$