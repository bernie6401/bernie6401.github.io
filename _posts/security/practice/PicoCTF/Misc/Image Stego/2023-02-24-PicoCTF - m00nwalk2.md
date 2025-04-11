---
title: PicoCTF - m00nwalk2
tags: [PicoCTF, CTF, Misc]

category: "Security/Practice/PicoCTF/Misc/Image Stego"
---

# PicoCTF - m00nwalk2
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: [m00nwalk2](https://play.picoctf.org/practice?category=4&page=3)

## Description & Hint
Revisit the last transmission. We think this [transmission](https://jupiter.challenges.picoctf.org/static/a33c9e5dae30c560704e6f2ffaba35c7/message.wav) contains a hidden message. There are also some clues [clue 1](https://jupiter.challenges.picoctf.org/static/a33c9e5dae30c560704e6f2ffaba35c7/clue1.wav), [clue 2](https://jupiter.challenges.picoctf.org/static/a33c9e5dae30c560704e6f2ffaba35c7/clue2.wav), [clue 3](https://jupiter.challenges.picoctf.org/static/a33c9e5dae30c560704e6f2ffaba35c7/clue3.wav).

Hint:
* Use the clues to extract the another flag from the .wav file


## Background
[m00nwalk](/rrUS4fS8QxicWvvjqziIqg)

## Exploit - QSSTV
1. Follow the write up of m00nwalk then you'll get 3 images from 3 clues respectively.
![](https://i.imgur.com/Vq8ciM2.png)
![](https://i.imgur.com/Y5nS8wS.png)
![](https://i.imgur.com/C0xk8YL.png)

2. Search Alan Eliasen the Future Boy
It's a [website](https://futureboy.us/) that contains encoding steganography files.
So, we select the message file and enter the password
![](https://i.imgur.com/dx3zsVj.png)
Then we got the flag
`picoCTF{the_answer_lies_hidden_in_plain_sight}`