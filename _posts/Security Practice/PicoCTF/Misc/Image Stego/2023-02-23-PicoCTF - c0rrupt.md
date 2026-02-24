---
title: PicoCTF - c0rrupt
tags: [PicoCTF, CTF, Misc]

category: "Security Practice｜PicoCTF｜Misc｜Image Stego"
date: 2023-02-23
---

# PicoCTF - c0rrupt
<!-- more -->
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: [c0rrupt](https://play.picoctf.org/practice/challenge/53?category=4&page=3)

## Background
[advanced-potion-making:two::+1:](/uwox6r5hQ6St_8G-4mv1_g)

## Exploit - Recover PNG file
1. Analyze
* Header
`89 65 4E 34 0D 0A B0 AA`
$\to$
`89 50 4E 47 0D 0A 1A 0A`
* IHDR
`43 22 44 52`
$\to$
`49 48 44 52`
Then use `pngcheck` to analyze the file. It said the header still have some error.
    ```bash!
    $ pngcheck mystery
    mystery  CRC error in chunk pHYs (computed 38d82c82, expected 495224f0)
    ERROR: mystery
    ```
* Revise `pHYs`
You can open an arbitrary png file and observe `pHYs` part.
    * Normal one
    ![](https://i.imgur.com/tyAfklr.png)
    * Corrupt one
    ![](https://i.imgur.com/YodQp0O.png)
`70 48 59 73 AA`
$\to$
`70 48 59 73 00`

    ```bash!
    $ pngcheck mystery
    mystery  invalid chunk length (too large)
    ERROR: mystery
    ```
    Still error

* Again
We can observe a normal png file
    * Normal one
    ![](https://i.imgur.com/vNAVQu8.png)
    * Corrupt one
    ![](https://i.imgur.com/EM5DLGx.png)
`52 24 F0 AA AA`
$\to$
`52 24 F0 00 00`
    ```bash!
    $ pngcheck mystery
    mystery:  invalid chunk name "�DET" (ffffffab 44 45 54)
    ERROR: mystery
    ```
    Still error about IDAT
* Recover IDAT
`AB 44 45 54`
$\to$
`49 44 41 54`

Then we recover the whole file successfully...
![](https://i.imgur.com/zbBzmc5.png)