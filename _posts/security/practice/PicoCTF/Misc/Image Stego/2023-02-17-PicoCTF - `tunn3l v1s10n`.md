---
title: PicoCTF - `tunn3l v1s10n`
tags: [PicoCTF, CTF, Misc]

category: "Security > Practice > PicoCTF > Misc > Image Stego"
---

# PicoCTF - `tunn3l v1s10n`
###### tags: `PicoCTF` `CTF` `Misc`
Challenge: [tunn3l v1s10n](https://play.picoctf.org/practice/challenge/112?category=4&page=1)

## Background
[[筆記] BMP點陣圖格式說明](https://www.jinnsblog.com/2009/08/bmp-format-graphic-illustration.html)


## Exploit - Recover file
1. Analyze
    ```bash!
    $ exiftool tunn3l_v1s10n
    ExifTool Version Number         : 11.88
    File Name                       : tunn3l_v1s10n
    Directory                       : .
    File Size                       : 2.8 MB
    File Modification Date/Time     : 2023:02:17 04:11:33+08:00
    File Access Date/Time           : 2023:02:17 04:12:37+08:00
    File Inode Change Date/Time     : 2023:02:17 04:11:35+08:00
    File Permissions                : rw-r--r--
    File Type                       : BMP
    File Type Extension             : bmp
    MIME Type                       : image/bmp
    BMP Version                     : Unknown (53434)
    Image Width                     : 1134
    Image Height                    : 306
    Planes                          : 1
    Bit Depth                       : 24
    Compression                     : None
    Image Length                    : 2893400
    Pixels Per Meter X              : 5669
    Pixels Per Meter Y              : 5669
    Num Colors                      : Use BitDepth
    Num Important Colors            : All
    Red Mask                        : 0x27171a23
    Green Mask                      : 0x20291b1e
    Blue Mask                       : 0x1e212a1d
    Alpha Mask                      : 0x311a1d26
    Color Space                     : Unknown (,5%()
    Rendering Intent                : Unknown (826103054)
    Image Size                      : 1134x306
    Megapixels                      : 0.347
    ```
    It seems a `bmp` file and check the file signature of the 2 bytes is `42 4D` :heavy_check_mark: 
2. Check file headers
According to [BMP_file_format](https://en.wikipedia.org/wiki/BMP_file_format) and [BMP點陣圖格式說明](https://www.jinnsblog.com/2009/08/bmp-format-graphic-illustration.html)
![](https://i.imgur.com/YU6exro.png)
    * :heavy_check_mark:size: `8E 26 2C 00` $\to$ `0x2C268E` $\to$ `2893454 bytes`
![](https://i.imgur.com/H6G44kT.png)
    * :heavy_check_mark:reserved1: `00 00`
    * :heavy_check_mark:reserved2:  `00 00`
    * :negative_squared_cross_mark:offset: `BA D0 00 00` $\to$ `0xD0BA` $\to$ `53434` means it'll read the bitmap data from offset 53434 bytes. But actually, the data of bitmap is just connect with the header. So, we just need to shift 14 bytes for file header + 40 bytes for info header = 54 bytes $\to$ `0x36`
![](https://i.imgur.com/crETYOD.png)

---

We can peek the data first...
![](https://i.imgur.com/DWesnDl.png)
It said `notaflag{sorry}`, means we need to recover other parts.

---

3. Check info headers
![](https://i.imgur.com/SMZn71k.png)
* :negative_squared_cross_mark:size：`BA D0 00 00` $\to$ `0x0DBA` $\to$ `3514 bytes` means the size of info header. However, the real size is `40 bytes` $\to$ `0x28` $\to$ `28 00 00 00`

Something strange with the following header:
* width：`6E 04 00 00` $\to$ `0x46E` $\to$ `1134 pixels`
* height：`32 01 00 00` $\to$ `0x132` $\to$ `306 pixels`
* bits：`18 00` $\to$ `0x18` $\to$ `each pixels need 24 bits`
If these headers are true:
$$
1134\ pixels\ *\ 306\ pixels\ *\ 24\ bits\ per\ pixel\ /\ 8\ bits\ per\ byte=1041012\ bytes
$$
And this is obviously not the real storage size system told us(2893454 bytes)

4. Modify height pixels
$$
2893454\ bytes\ *\ 8\ bits\ per\ bytes\ /\ 24\  bits\ per\ pixel\ /\ 1134\ pixels=850.5\ pixels
$$
The height should be 850 pixels $\to$ `0x352` $\to$ `52 03 00 00`

5. Done!!!
    :::spoiler flag
    ![](https://i.imgur.com/IJMO8Pd.jpg)
    :::
## Reference
[CTFtime Write Up](https://ctftime.org/writeup/28157)