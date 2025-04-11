---
title: PicoCTF - advanced-potion-making
tags: [PicoCTF, CTF, Misc]

category: "Security/Practice/PicoCTF/Misc/Image Stego"
---

# PicoCTF - advanced-potion-making
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: [advanced-potion-making](https://play.picoctf.org/practice/challenge/205?bookmarked=0&category=4&page=1&search=&solved=0)

## Background
[PNG文件格式详解](https://blog.mythsman.com/post/5d2d62b4a2005d74040ef7eb/)
[隐写分析(2) PNG图片隐写](https://zhuanlan.zhihu.com/p/599657891)

## Exploit - Recover + StegSolve
Modify the file signature and length to the right value.
`89 50 42 11 0D 0A 1A 0A 00 12 13 14 49 48 44 52`
$\to$
`89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52`
* ![](https://i.imgur.com/Pv1ojSN.png)
* ![](https://i.imgur.com/vLgguSp.png)


![](https://i.imgur.com/ZT4PsQ5.png)

## Reference