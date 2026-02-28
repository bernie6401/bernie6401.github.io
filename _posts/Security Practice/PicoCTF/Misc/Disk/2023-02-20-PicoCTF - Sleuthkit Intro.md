---
title: PicoCTF - Sleuthkit Intro
tags: [PicoCTF, CTF, Misc]

category: "Security Practice｜PicoCTF｜Misc｜Disk"
date: 2023-02-20
---

# PicoCTF - Sleuthkit Intro
<!-- more -->
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: [Sleuthkit Intro](https://play.picoctf.org/practice/challenge/301?category=4&page=2)

## Description
> Download the disk image and use <font color="FF0000">mmls</font> on it to find the size of the Linux partition. Connect to the remote checker service to check your answer and get the flag. Note: if you are using the webshell, download and extract the disk image into /tmp not your home directory.

    Download disk image
    Access checker program: nc saturn.picoctf.net 52279
    
[最新kali之mmls](https://blog.csdn.net/qq_40399982/article/details/114882879?spm=1001.2014.3001.5506)


## Exploit - Follow the description
```bash!
$ file disk.img.gz
disk.img.gz: gzip compressed data, was "disk.img", last modified: Tue Sep 21 19:34:53 2021, from Unix, original size modulo 2^32 104857600
$ gzip -d disk.img.gz
$ ls
disk.img
$ mmls disk.img
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
001:  -------   0000000000   0000002047   0000002048   Unallocated
002:  000:000   0000002048   0000204799   0000202752   Linux (0x83)
$ nc saturn.picoctf.net 52279
What is the size of the Linux partition in the given disk image?
Length in sectors: 202752
202752
Great work!
picoCTF{mm15_f7w!}
```