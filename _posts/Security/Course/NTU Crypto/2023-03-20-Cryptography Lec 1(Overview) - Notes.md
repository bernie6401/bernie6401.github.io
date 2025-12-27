---
title: Cryptography Lec 1(Overview) - Notes
tags: [Cryptography, NTU]

category: "Security｜Course｜NTU Crypto"
---

# Cryptography Lec 1(Overview) - Notes
<!-- more -->
###### tags: `Cryptography` `NTU`

## Background
Chosen Plaintext Attack(CPA security)
Attacker只可以拿到plaintext相對應的ciphertext，通常是在同一把key重複使用的情況下

Chosen Cipnertext Attack(CCA security)
Attacker不只可以拿到plaintext相對應的ciphertext，他也可以知道ciphertext相對應的plaintext，進而得知很多額外的資訊

Mode of Operation
e.g. ECB, CBC, CTR, GCM...(Nonsecure $\to$ Secure)
選擇甚麼樣的mode和選擇麼加密演算法是完全獨立的事情，也可以每一個block都使用完全不同的加密演算法