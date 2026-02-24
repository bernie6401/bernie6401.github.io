---
title: TaiwanHolyHigh - Windows Forensics - $MFT Resident / Non-Resident File
tags: [TaiwanHolyHigh, Forensics, Windows]

category: "Security Course｜Tai.HolyHigh｜Windows OS Forensics"
date: 2024-01-31
---

# TaiwanHolyHigh - Windows Forensics - \$MFT Resident / Non-Resident File
<!-- more -->
:::spoiler TOC
[TOC]
:::

## Background
\$MFT儲存的內容
1. ==Status==
2. ==\$MFT Record==(File Identify/Location)
3. ==Timestamp==
    * Standard Info
    * Filename
4. ==Resident==
    * 特性如下:
        * $SO\ne 0$: 意思就是resident file的前面一定有其他檔案，而他一定不會是\$MFT的開頭
        * No File Slack: 沒有檔案暫存區，意味著他會住在一個剛剛好的大小的房間中
        * Physical Size = Logical Size: 這個就和前一個有相關，logical size就是實際住進去房間的檔案大小，而physical size就是飯店給予我們房間的大小，所以$physical\_size\ge logical\_size$
        * 如果resident file因為駭客的攻擊(injection/trojan/backdoor...)使得檔案大小變大，而失去原本resident file的身分，則該檔案就會被搬出目前的地方，就算之後檔案大小變回來，還是無法再住回原本的地方，這就是攻擊方所遺留的攻擊痕跡
    * 如何判斷?如果檔名後面接的是`18 00 00 00 01 00`就是resident file，例如：
        :::spoiler 範例
        ![](https://hackmd.io/_uploads/rynQ2dFGp.png)
        :::
        或者是看`18 00 00 00 10 00`的前面第二個byte(就是non-resident flag)，是`00`代表不是non-resident file，反之就是
        :::spoiler flag範例
        ![](https://hackmd.io/_uploads/HkAy6_tMa.png)
        :::
    * 檔案大小
        `18 00 00 00 10 00`後面接著的四個bytes就是檔案大小$\to$換成10禁制就對了，另外如果此檔案是resident file，則檔案大小後面除了固定的`18 00 00 00`以外，後面還會有該檔案原本的file signature，以此為例就是`89 50 4E 47`也就是png的magical header
        :::spoiler flag範例
        ![](https://hackmd.io/_uploads/SkwzAOtGa.png)
        此範例就是`02 02`$\to$514 bytes
        :::
5. ==non-Resident File==
    如果是non-resident file，檔名的後面一點會接的是`80 00 00 00 48 00 00 00`，再後面就是non-resident flag
    ![](https://hackmd.io/_uploads/HJk7NFtf6.png)
    另外，檔案的大小會在flag往後數40個bytes的地方，以底下範例來說就是`F6 09 00 00`
    ![](https://hackmd.io/_uploads/BJWMBtKMT.png)

## Lab - Resident File

### Lab - Offset 43208704(d)
先找檔名，後面會跟著`18 00 00 00 01 00`，前面會有non-resident flag(前面第二個byte)，再後面會跟著檔案大小`D0 01`，再後面一點會跟著原本這個file的signature
* Non-Resident Flag: `00`
* File Size: `D0 01` = 464 bytes

### Lab - Offset 43110400(d)
* Non-Resident Flag: `00`
* File Size: `FE 01` = 510 bytes

## Lab - Non-Resident File

### Lab - Offset 43462656(d)
* Non-Resident Flag: `01`
* File Size: `F6 09` = 2550 bytes

### Lab - Offset 43485184(d)
* Non-Resident Flag: `01`
* File Size: `42 0E` = 3650 bytes

### Lab - Offset 62343168(d)
* Non-Resident Flag: `01`
* File Size: `F7 12` = 4855 bytes


## 現場考試

### Offset 51472384(d)
Non-Resient File
* Status: `01 00` $\to$ file
* \$MFT Record: `5A C4` $\to$ `0x3116800`
* Standard Info
    * Create Time = Modify Time = `1997, 12, 8, 8, 0`
    * \$MFT Modify Time = Access Time = `2010, 8, 11, 2, 30, 18, 151785`
* Filename Timestamp: `2010, 8, 11, 2, 30, 18, 151785`
* Non-Resident Flag: `01`
* File Size: `FD 02` $\to$ 765 bytes

### Offset 65898496(d)
Resident File
* Status: `00 00` $\to$ file
* \$MFT Record: `62 FB` $\to$ `0x3ed8800`
* Standard Info
    * Create Time = Access Time = `2011, 2, 1, 2, 6, 16`
    * Modify Time = `2011, 2, 1, 2, 4, 21`
    * \$MFT Modify Time = `2011, 2, 9, 2, 21, 46, 662258`
* Filename Timestamp: `2011, 2, 9, 2, 16, 36, 547024`
* Non-Resident Flag: `00`
* File Size: `99 01` $\to$ 409 bytes

### Offset 64329728(d)
Non-Resident File(曾經是resident file)
* Status: `01 00` $\to$ file
* \$MFT Record: `66 F5` $\to$ `0x3d59800`
* Standard Info
    * Create Time = Access Time = `2011, 2, 3, 1, 17, 53, 184265`
    * Modify Time = `2011, 2, 3, 1, 17, 53, 272156`
    * \$MFT Modify Time = `2011, 2, 8, 23, 27, 47, 201321`
* Filename Time: `2011, 2, 3, 1, 17, 53, 184265`
* Non-Resident Flag: `01`
* File Size: `21 01` $\to$ 289 bytes

### Offset 65873920(d)
Non-Resident File
* Status: `00 00` $\to$ deleted file
* \$MFT Record: `4A FB` $\to$ `0x3ed2800`
* Standard Info
    * Create Time = Access Time = `2011, 2, 1, 2, 7, 42`
    * Modify Time = `2011, 2, 1, 2, 7, 22`
    * \$MFT Modify Time = `2011, 2, 9, 2, 21, 46, 701321`
* Filename Time: `2011, 2, 9, 2, 16, 36, 400539`
* Non-Resident Flag: `01`
* File Size: `6E 02` $\to$ 622 bytes