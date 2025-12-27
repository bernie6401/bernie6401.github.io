---
title: 'PicoCTF - Disk, disk, sleuth! II'
tags: [PicoCTF, CTF, Misc]

category: "Security｜Practice｜PicoCTF｜Misc｜Disk"
---

# PicoCTF - Disk, disk, sleuth! II
<!-- more -->
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: [Disk, disk, sleuth! II](https://play.picoctf.org/practice/challenge/137?category=4&page=2)

## Description & Hint
All we know is the file with the flag is named `down-at-the-bottom.txt`... Disk image: `dds2-alpine.flag.img.gz`
Hint 1: The sleuthkit has some great tools for this challenge as well.
Hint 2: Sleuthkit docs here are so helpful: [TSK Tool Overview](http://wiki.sleuthkit.org/index.php?title=TSK_Tool_Overview)
Hint 3: This disk can also be booted with [qemu](https://idobest.pixnet.net/blog/post/22040213)!

## Background
[Linux安装、使用Sleuth kit/Autopsy](https://blog.csdn.net/wxh0000mm/article/details/99447206)

## Exploit - Use Autopsy Tool to analyze
In root folder.
![](https://i.imgur.com/3Vvbk2R.png)
:::spoiler flag
```
_     _     _     _     _     _     _     _     _     _     _     _     _  
  / \   / \   / \   / \   / \   / \   / \   / \   / \   / \   / \   / \   / \ 
 ( p ) ( i ) ( c ) ( o ) ( C ) ( T ) ( F ) ( { ) ( f ) ( 0 ) ( r ) ( 3 ) ( n )
  \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/ 
   _     _     _     _     _     _     _     _     _     _     _     _     _  
  / \   / \   / \   / \   / \   / \   / \   / \   / \   / \   / \   / \   / \ 
 ( s ) ( 1 ) ( c ) ( 4 ) ( t ) ( 0 ) ( r ) ( _ ) ( n ) ( 0 ) ( v ) ( 1 ) ( c )
  \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/ 
   _     _     _     _     _     _     _     _     _     _     _  
  / \   / \   / \   / \   / \   / \   / \   / \   / \   / \   / \ 
 ( 3 ) ( _ ) ( d ) ( b ) ( 5 ) ( 9 ) ( d ) ( a ) ( a ) ( 5 ) ( } )
  \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/   \_/ 


------------------------------METADATA------------------------------
```
:::
