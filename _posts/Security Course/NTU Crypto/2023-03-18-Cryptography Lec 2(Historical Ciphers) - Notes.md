---
title: Cryptography Lec 2(Historical Ciphers) - Notes
tags: [Cryptography, NTU]

category: "Security Course｜NTU Crypto"
date: 2023-03-18
---

# Cryptography Lec 2(Historical Ciphers) - Notes
<!-- more -->
###### tags: `Cryptography` `NTU`

:::spoiler [資訊安全筆記2 The Vigenere Cipher](https://ithelp.ithome.com.tw/articles/10160406)
> The Vigenere Cipher是一種"polyalphabetic cipher"用一串的 Key 不斷地重複！例如 abcabcabcabc
計算方法：
例如key = d 代表a會變成d所以 w 會變成 Z
>
>課本上的例子：
>![](http://ithelp.ithome.com.tw/upload/images/20141017/201410172334255441370129a1a_resize_600.png)
:::

:::spoiler [Playfair Cipher](https://www.geeksforgeeks.org/playfair-cipher-with-examples/)
> The Playfair Cipher Encryption Algorithm: 
The Algorithm consists of 2 steps:
> 1. Generate the key Square(5×5): 
> 2. Algorithm to encrypt the plain text: The plaintext is split into pairs of two letters (digraphs). If there is an odd number of letters, a Z is added to the last letter.
    > For example:
    ```
    PlainText: "instruments"
    After Split: 'in' 'st' 'ru' 'me' 'nt' 'sz'
    ```
>
> :::info
> Note that: Pair cannot be made with same letter. Break the letter in single and add a bogus letter to the previous letter.
> :::
> 1. Plain Text: “hello”
>After Split: ‘he’ ‘lx’ ‘lo’
>Here ‘x’ is the bogus letter.
>
> 2. If the letter is standing alone in the process of pairing, then add an extra bogus letter with the alone letter
Plain Text: “helloe”
After Split: ‘he’ ‘lx’ ‘lo’ ‘ez’
Here ‘z’  is the bogus letter.

## Exception
![](https://i.imgur.com/k5VkTmF.png)
![](https://media.geeksforgeeks.org/wp-content/uploads/20190818175431/encryption-of-me.png)

---
![](https://i.imgur.com/g80Uouf.png)
![](https://media.geeksforgeeks.org/wp-content/uploads/20190818175435/encryption-of-st.png)

---
![](https://i.imgur.com/i7qd7iw.png)
![](https://media.geeksforgeeks.org/wp-content/uploads/20190818175433/encryption-of-nt.png)
:::

---
Introduce the encryption flow of Enigma
[WWII納粹德國密碼機Enigma](https://youtu.be/BxCKKbvxEiE)