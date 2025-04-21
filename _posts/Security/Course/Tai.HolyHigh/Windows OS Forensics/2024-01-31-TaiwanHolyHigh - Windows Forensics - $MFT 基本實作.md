---
title: TaiwanHolyHigh - Windows Forensics - $MFT 基本實作
tags: [TaiwanHolyHigh, Forensics, Windows]

category: "Security/Course/Tai.HolyHigh/Windows OS Forensics"
---

# TaiwanHolyHigh - Windows Forensics - \$MFT 基本實作
<!-- more -->
:::spoiler TOC
[TOC]
:::
:::info
以下引用若無特別說明皆來自於講師的上課簡報
:::

## Background
* \$MFT儲存的內容
    1. ==Status==: SO=22, LE=2，也就是目前此檔案的狀態，分為以下四種
        * `0000`: Delete File
        * `0100`: File
        * `0200`: Delete Folder
        * `0300`: Folder
    2. ==\$MFT Record==(File Identify/Location): SO=44, LE=4，也就是此檔案在record在\$MFT的位置在哪邊
    3. ==Timestamp==
        * Standard Info: SO=80, LE=32(Creat+Modified+\$MFT Modified+Access)，很容易就可以更改，如果要更改，可以參考[New Filetime](https://newfiletime.en.softonic.com/?ex=RAMP-1462.1)這個工具
        * Filename: SO=184, LE=32(Creat+Modified+\$MFT Modified+Access)
            很難被更改(但還是可以更改)
    4. ==Resident / non-Resident File==
        下一篇詳細說明
        
:::info
以下三個練習都是Resident File
:::

## Lab - Offset 43110400(d)
* \$MFT長度一段就是1024 Bytes，我把結束的位址減掉開頭的位置就知道了，或是可以直接用HxD底下看長度(0x400)
    ![](https://hackmd.io/_uploads/rk0s7QKza.png)
    ![](https://hackmd.io/_uploads/rJjnQ7tfT.png)
    ```python
    >>> 0x291D400-0x291D000
    1024
    ```
* 從上圖也可以看到magical word就是`FILE0`$\to$`46 49 4C 45 30`

### Overview(從上到下)
![](https://hackmd.io/_uploads/S1l-DgEtzp.png)

* Staus: `01 00`$\to$File
* `04 00 00 00`是固定的
* \$MFT Record: `74 A4`先轉換endian然後變十進位，在乘以1024就會是目前此檔案的開頭位址
    ```python
    >>> mft_record = '74 A4'
    >>> mft_record = int("".join(mft_record.split(' ')[::-1]), 16)
    >>> hex(mft_record * 1024)
    '0x291d000'
    ```
* `48 00 00 00 18 00 00 00`是固定的
* Standard Info Timestamp
    此部分可以用之前的script換算
    :::spoiler Script 過程
    ```python
    >>> import datetime
    >>> def ad_timestamp(timestamp):
    ...     if timestamp != 0:
    ...         return datetime.datetime(1601, 1, 1) + datetime.timedelta(seconds=timestamp/10000000)
    ...     return np.nan
    ...
    >>> create_time = '8D 6C AD E4 B5 BD CB 01'
    >>> create_time = int("".join(create_time.split(' ')[::-1]), 16)
    >>> ad_timestamp(create_time)
    datetime.datetime(2011, 1, 27, 0, 5, 23, 349211)
    >>> modify_time = '00 DE 13 B1 09 92 C9 01'
    >>> modify_time = int("".join(modify_time.split(' ')[::-1]), 16)
    >>> ad_timestamp(modify_time)
    datetime.datetime(2009, 2, 18, 20, 44, 28)
    >>> mft_modify = 'E7 CE AF E4 B5 BD CB 01'
    >>> mft_modify = int("".join(mft_modify.split(' ')[::-1]), 16)
    >>> ad_timestamp(mft_modify)
    datetime.datetime(2011, 1, 27, 0, 5, 23, 364836)
    >>> access_time = '00 DE 13 B1 09 92 C9 01'
    >>> access_time = int("".join(access_time.split(' ')[::-1]), 16)
    >>> ad_timestamp(access_time)
    datetime.datetime(2009, 2, 18, 20, 44, 28)
    ```
    :::
    Create: `2011, 1, 27, 0, 5, 23, 349211`
    Modify: `2009, 2, 18, 20, 44, 28`
    \$MFT: `2011, 1, 27, 0, 5, 23, 364836`
    Access: `2009, 2, 18, 20, 44, 28`
* Filename Timestamp
    ```python
    >>> filename = '8D 6C AD E4 B5 BD CB 01'
    >>> filename = int("".join(filename.split(' ')[::-1]), 16)
    >>> ad_timestamp(filename)
    datetime.datetime(2011, 1, 27, 0, 5, 23, 349211)
    ```
    Filename Timestamp都是`2011, 1, 27, 0, 5, 23, 349211`，和前面的create time相同

## Lab - Offset 43208704(d)
* Staus: `01 00`$\to$File
* \$MFT Record: `D4 A4`
    ```python
    >>> hex(int("".join('d4 a4'.split(' ')[::-1]), 16) * 1024)
    '0x2935000'
    ```
* Standard Info Timestamp
    ```python
    >>> create_time = 'E3 8D 30 E5 B5 BD CB 01'
    >>> create_time = int("".join(create_time.split(' ')[::-1]), 16)
    >>> ad_timestamp(create_time)
    datetime.datetime(2011, 1, 27, 0, 5, 24, 208586)
    >>> modify_time = '00 99 75 C2 57 7A C9 01'
    >>> modify_time = int("".join(modify_time.split(' ')[::-1]), 16)
    >>> ad_timestamp(modify_time)
    datetime.datetime(2009, 1, 19, 17, 2, 50)
    ```
    Create Time = \$MFT Modify Time = `2011, 1, 27, 0, 5, 24, 208586`
    Modify Time = Access Time = `2009, 1, 19, 17, 2, 50`
* Filename Timestamp
    Filename Time = Create Time = `2011, 1, 27, 0, 5, 24, 208586`
    
## Lab - Offset 53550080(d)
* Staus: `01 00`$\to$File
* \$MFT Record: `47 CC`
    ```python
    >>> hex(int("".join('47 CC'.split(' ')[::-1]), 16) * 1024)
    '0x3311c00'
    ```
* Standard Info Timestamp
    :::spoiler 運算過程
    ```python
    >>> create_time = '1D 3F 6E F8 B3 C0 CB 01'
    >>> create_time = int("".join(create_time.split(' ')[::-1]), 16)
    >>> ad_timestamp(create_time)
    datetime.datetime(2011, 1, 30, 19, 29, 10, 984476)
    >>> modify_time = '00 6E A6 FC D2 E0 CA 01'
    >>> modify_time = int("".join(modify_time.split(' ')[::-1]), 16)
    >>> ad_timestamp(modify_time)
    datetime.datetime(2010, 4, 20, 21, 46, 52)
    >>> mft_modify = '77 A1 70 F8 B3 C0 CB 01'
    >>> mft_modify = int("".join(mft_modify.split(' ')[::-1]), 16)
    >>> ad_timestamp(mft_modify)
    datetime.datetime(2011, 1, 30, 19, 29, 11, 101)
    >>> access_time = '1D 3F 6E F8 B3 C0 CB 01'
    >>> access_time = int("".join(access_time.split(' ')[::-1]), 16)
    >>> ad_timestamp(access_time)
    datetime.datetime(2011, 1, 30, 19, 29, 10, 984476)
    ```
    :::
    Create Time = Access Time = `2011, 1, 30, 19, 29, 10, 984476`
    Modify Time = `2010, 4, 20, 21, 46, 52`
    \$MFT Modify Time = `2011, 1, 30, 19, 29, 11, 101`
    
* Filename Timestamp
    Create Time = \$MFT Modify Time = Access Time = `2011, 1, 30, 19, 29, 10, 984476`
    Modify Time = `2010, 4, 20, 21, 46, 52`