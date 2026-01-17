---
title: PicoCTF - mus1c
tags: [PicoCTF, CTF, General Skill]

category: "Security｜Practice｜PicoCTF｜General Skills"
date: 2023-06-19
---

# PicoCTF - mus1c
<!-- more -->
###### tags: `PicoCTF` `CTF` `General Skill`

## Source code
:::spoiler Lyrics
```
Pico's a CTFFFFFFF
my mind is waitin
It's waitin

Put my mind of Pico into This
my flag is not found
put This into my flag
put my flag into Pico


shout Pico
shout Pico
shout Pico

My song's something
put Pico into This

Knock This down, down, down
put This into CTF

shout CTF
my lyric is nothing
Put This without my song into my lyric
Knock my lyric down, down, down

shout my lyric

Put my lyric into This
Put my song with This into my lyric
Knock my lyric down

shout my lyric

Build my lyric up, up ,up

shout my lyric
shout Pico
shout It

Pico CTF is fun
security is important
Fun is fun
Put security with fun into Pico CTF
Build Fun up
shout fun times Pico CTF
put fun times Pico CTF into my song

build it up

shout it
shout it

build it up, up
shout it
shout Pico
```
:::

## Recon
這一題挺詭異的，想了超級無敵久，完全就是只能看別人的WP[1]

## Exploit - New Programming Language
1. 查詢歌詞的一些關鍵字會發現rockstar這個網站
    > Rockstar is a computer programming language designed for creating programs that are also hair metal power ballads.
    感覺上也和題目的歌詞有關係
2. 把歌詞貼到[decoder](https://codewithrockstar.com/online)會出現一堆數字，猜測應該是ascii code
3. Decode ascii and get flag: `picoCTF{rrrocknrn0113r}`

## Reference
[mus1c - Write up](https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/mus1c.md)