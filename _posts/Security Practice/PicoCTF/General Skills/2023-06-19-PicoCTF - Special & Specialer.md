---
title: PicoCTF - Special & Specialer
tags: [PicoCTF, CTF, General Skill]

category: "Security Practice｜PicoCTF｜General Skills"
date: 2023-06-19
---

# PicoCTF - Special & Specialer
<!-- more -->
###### tags: `PicoCTF` `CTF` `General Skill`

## Recon
這兩題都蠻有趣的，感覺打提權應該會用到，所以一起紀錄，第一題是要get shell，關於這一題我是直接看學長之前解題的WP，payload是`${0}`就直接拿到shell了，詳細的原理我也不清楚，第二題比較簡單，就直接用網路的資源替換一下`ls, cat`這兩個指令就拿到flag了

## Exploit
* 代替`cat`的方法：
    ```bash
    # Method 1
    $ while read line; do
    while> echo $line;
    while> done <{filename}}

    # Method 2
    $ exec 3<{filename}} # Assign file descriptor 3 for reading
    $ while read -u 3 line; do
    while> echo $line
    while> done

    # Method 3
    $ echo "$(<{filename})"
    ```

* 代替`ls`的方法
    ```bash
    # Method 1
    $ echo *

    # Method 2
    $ echo */*

    # Method 3
    $ echo * .*

    # Method 4
    $ dir

    # Method 5
    $ printf '%s\n' *

    # Method 6
    $ grep -l '.*' ./*

    # Method 7
    $ find .

    # Method 8
    $ stat -c '%s %A %n' *

    # Method 9
    $ lsattr ./*

    # Method 10
    $ vim .
    ```

## Reference
[Cat without cat on the commandline](https://jarv.org/posts/cat-without-cat/)
[Alternatives to the 'ls' command to list the contents of a directory](https://ubunlog.com/en/alternativas-al-comando-ls/)