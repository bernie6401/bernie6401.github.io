---
title: PicoCTF - Matryoshka doll
tags: [PicoCTF, CTF, Misc]

category: "Security/Practice/PicoCTF/Misc/General"
---

# PicoCTF - Matryoshka doll
<!-- more -->
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: [](https://play.picoctf.org/practice/challenge/129?category=4&page=1)

## Exploit - `rar` in `rar`
1. Hint
The hint said:
    > Wait, you can hide files inside files? But how do you find them?

    So...I tried `stegsolve`, `HxD`, `exiftool`, `string dolls.jpg | grep "{"`, `$ zsteg dolls.jpg` ... All these are in vain
2. <font color="FF0000">通靈</font>: Changed the extension to `.rar`
And it can be uncompressed
![](https://i.imgur.com/sNfhE2J.png)

3. Repeat until find `flag.txt`...