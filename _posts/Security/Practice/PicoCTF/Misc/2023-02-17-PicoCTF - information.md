---
title: PicoCTF - information
tags: [PicoCTF, CTF, Misc]

category: "Security/Practice/PicoCTF/Misc"
---

# PicoCTF - information
<!-- more -->
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: https://play.picoctf.org/practice/challenge/186?category=4&page=1

## Background
[ExifTool](https://ubunlog.com/zh-TW/exiftool-manipula-metadatos-ubuntu/)

## Exploit
```bash!
$ exiftool cat.jpg
ExifTool Version Number         : 11.88
File Name                       : cat.jpg
Directory                       : .
File Size                       : 858 kB
File Modification Date/Time     : 2023:02:16 02:15:29+08:00
File Access Date/Time           : 2023:02:16 16:09:51+08:00
File Inode Change Date/Time     : 2023:02:16 12:31:32+08:00
File Permissions                : rwxrwxrwx
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.02
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Current IPTC Digest             : 7a78f3d9cfb1ce42ab5a3aa30573d617
Copyright Notice                : PicoCTF
Application Record Version      : 4
XMP Toolkit                     : Image::ExifTool 10.80
License                         : cGljb0NURnt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9
Rights                          : PicoCTF
Image Width                     : 2560
Image Height                    : 1598
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 2560x1598
Megapixels                      : 4.1
```
In License row, it's obviously a base64 encoding string
`picoCTF{the_m3tadata_1s_modified}`

## Reference
[picoCTF 2021: Forensics - information](https://reversingfun.com/posts/picoctf-2021-forensics/#information)