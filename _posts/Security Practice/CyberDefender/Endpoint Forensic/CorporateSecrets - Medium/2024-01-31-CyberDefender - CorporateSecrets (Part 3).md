---
title: CyberDefender - CorporateSecrets (Part 3)
tags: [CyberDefender, Endpoint Forensics]

category: "Security Practice｜CyberDefender｜Endpoint Forensic｜CorporateSecrets - Medium"
date: 2024-01-31
---

# CyberDefender - CorporateSecrets (Part 3)
<!-- more -->
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/33
Part 1: https://hackmd.io/@SBK6401/r18z7VIm6
Part 2: https://hackmd.io/@SBK6401/ByFhEE8X6
Part 4: https://hackmd.io/@SBK6401/H1rAEV87p

:::spoiler TOC
[TOC]
:::

## Tools: 
* FTK Imager
* Registry Explorer
* RegRipper
* HxD
* DB Browser for SQLite
* HindSight
* Event Log Explorer
* MFTDump


## ==Q19==
> Which user installed LibreCAD on the system?

### Exploit
我是直接看該檔案在哪個user的資料夾來判斷，當然這個做法有點問題

:::spoiler Flag
Flag: `miriam.grapes`
:::

## ==Q20==
> How many times "admin" logged into the system? 

### Recon
呈第14題

### Exploit
不過我不知道為甚麼答案是21，然後我只有找到20個，看了4672也沒有紀錄(怪怪的)
![圖片.png](https://hackmd.io/_uploads/Syfldc8Xa.png)

:::spoiler Flag
Flag: `21`
:::

## ==Q21==
> What is the name of the DHCP domain the device was connected to? 

### Recon
直接看`SYSTEM/ControlSet001/Services/Tcpip/Parameters/Interfaces/`
![圖片.png](https://hackmd.io/_uploads/HJqjU5IQ6.png)

:::spoiler Flag
Flag: `fruitinc.xyz`
:::

## ==Q22==
> What time did Tim download his background image?
(Oh Boy 3AM . Answer in MM/DD/YYYY HH:MM format (UTC).) 

### Recon
原本的直覺是像第18題一樣把db file export出來看他的網路操作行為，不過其實可以直接看他下載的file，看他的create time就好

### Exploit
![圖片.png](https://hackmd.io/_uploads/SJfBFLvXa.png)

:::spoiler Flag
Flag: `04/05/2020 03:49`
:::

## ==Q23==
> How many times did Jim launch the Tor Browser?

### Exploit
直接把Jim的NTUSER.dat export出來後用timeline explorer看userassist，不過我不確定為甚麼答案是2，因為我查到的都是3
![圖片.png](https://hackmd.io/_uploads/rJz_098Q6.png)
![圖片.png](https://hackmd.io/_uploads/ByTKR9UmT.png)
還有另外一個方法是看prefetch，從FTK中export出`TOR.EXE-4B50033F.pf`，用PECmd.exe解析，但這個更怪了，結果顯示只有執行過一次，所以prefetch參考就好
:::spoiler
```bash
$ ./PECmd.exe -f TOR.EXE-4B50033F.pf
PECmd version 1.5.0.0

Author: Eric Zimmerman (saericzimmerman@gmail.com)
https://github.com/EricZimmerman/PECmd

Command line: -f TOR.EXE-4B50033F.pf

Keywords: temp, tmp

Processing TOR.EXE-4B50033F.pf

Created on: 2023-11-06 17:15:55
Modified on: 2020-04-16 04:52:40
Last accessed on: 2023-11-06 17:17:52

Executable name: TOR.EXE
Hash: 4B50033F
File size (bytes): 88,080
Version: Windows 10 or Windows 11

Run count: 1
Last run: 2020-04-16 04:52:30

Volume information:

#0: Name: \VOLUME{01d60963b1096880-ecb16432} Serial: ECB16432 Created: 2020-04-03 02:58:03 Directories: 11 File references: 71

Directories referenced: 11

00: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1
01: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER
02: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER
03: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\DATA
04: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\DATA\TOR
05: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\TOR
06: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS
07: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\GLOBALIZATION
08: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\GLOBALIZATION\SORTING
09: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32
10: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\EN-US

Files referenced: 58

00: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\NTDLL.DLL
01: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\TOR\TOR.EXE (Executable: True)
02: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\KERNEL32.DLL
03: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\KERNELBASE.DLL
04: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\LOCALE.NLS
05: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\ADVAPI32.DLL
06: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\MSVCRT.DLL
07: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\SECHOST.DLL
08: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\RPCRT4.DLL
09: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\SHELL32.DLL
10: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\CFGMGR32.DLL
11: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\UCRTBASE.DLL
12: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\SHCORE.DLL
13: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\COMBASE.DLL
14: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\BCRYPTPRIMITIVES.DLL
15: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\WINDOWS.STORAGE.DLL
16: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\SHLWAPI.DLL
17: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\GDI32.DLL
18: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\GDI32FULL.DLL
19: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\MSVCP_WIN.DLL
20: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\USER32.DLL
21: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\WIN32U.DLL
22: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\KERNEL.APPCORE.DLL
23: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\POWRPROF.DLL
24: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\PROFAPI.DLL
25: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\WS2_32.DLL
26: \VOLUME{01d60963b1096880-ecb16432}\$MFT
27: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\IPHLPAPI.DLL
28: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\TOR\LIBSSP-0.DLL
29: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\TOR\LIBEVENT-2-1-6.DLL
30: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\TOR\ZLIB1.DLL
31: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\TOR\LIBWINPTHREAD-1.DLL
32: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\TOR\LIBSSL-1_1-X64.DLL
33: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\TOR\LIBCRYPTO-1_1-X64.DLL
34: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\CRYPTSP.DLL
35: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\RSAENH.DLL
36: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\BCRYPT.DLL
37: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\GLOBALIZATION\SORTING\SORTDEFAULT.NLS
38: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\CRYPTBASE.DLL
39: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\IMM32.DLL
40: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\DATA\TOR\TORRC-DEFAULTS
41: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\DATA\TOR\TORRC
42: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\MSWSOCK.DLL
43: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\DATA\TOR\STATE
44: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\DATA\TOR\CONTROL_AUTH_COOKIE.TMP (Keyword: True)
45: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\DATA\TOR\GEOIP
46: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\DATA\TOR\GEOIP6
47: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\DATA\TOR\CACHED-CERTS
48: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\EN-US\KERNELBASE.DLL.MUI
49: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\DATA\TOR\CACHED-MICRODESC-CONSENSUS
50: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\DATA\TOR\CACHED-MICRODESCS
51: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\DATA\TOR\CACHED-MICRODESCS.NEW
52: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\DATA\TOR\UNVERIFIED-MICRODESC-CONSENSUS
53: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\DATA\TOR\STATE.TMP (Keyword: True)
54: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\NSI.DLL
55: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\DHCPCSVC6.DLL
56: \VOLUME{01d60963b1096880-ecb16432}\WINDOWS\SYSTEM32\DHCPCSVC.DLL
57: \VOLUME{01d60963b1096880-ecb16432}\PROGRAM1\BROWSER\TORBROWSER\DATA\TOR\CACHED-MICRODESC-CONSENSUS.TMP (Keyword: True)


---------- Processed TOR.EXE-4B50033F.pf in 0.04772100 seconds ----------
```
:::

:::spoiler Flag
Flag: `2`
:::

## ==Q24==
> There is a png photo of an iPhone in Grapes's files. Find it and provide the SHA-1 hash. 

### Recon
看了第一個hint才知道有stego的成分在裡面，首先要找到藏圖片的檔案是哪一張，我判斷是`samplePhone.jpg`這一張

### Exploit
有了圖片之後就是最擅長的misc基本操作，結果在binwalk的時候發現有附加檔案在裡面，就直接foremost提出來
```bash
$ binwalk -e samplePhone.jpg

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
5962          0x174A          PNG image, 1000 x 1000, 8-bit/color RGBA, non-interlaced
6003          0x1773          Zlib compressed data, best compression
$ foremost -v samplePhone.jpg
Foremost version 1.5.7 by Jesse Kornblum, Kris Kendall, and Nick Mikus
Audit File

Foremost started at Tue Nov  7 01:32:54 2023
Invocation: foremost -v samplePhone.jpg
Output directory: /mnt/d/NTU/CTF/CyberDefenders/CorporateSecrets/Exported File/output
Configuration file: /etc/foremost.conf
Processing: samplePhone.jpg
|------------------------------------------------------------------
File: samplePhone.jpg
Start: Tue Nov  7 01:32:54 2023
Length: 164 KB (167947 bytes)

Num      Name (bs=512)         Size      File Offset     Comment

0:      00000011.png         158 KB            5962       (1000 x 1000)
*|
Finish: Tue Nov  7 01:32:54 2023

1 FILES EXTRACTED

png:= 1
------------------------------------------------------------------

Foremost finished at Tue Nov  7 01:32:54 2023
$ cd output/png
$ file *
00000011.png: PNG image data, 1000 x 1000, 8-bit/color RGBA, non-interlaced
```
![圖片.png](https://hackmd.io/_uploads/BJMD8sUX6.png)

:::info
也可以像[^wp]直接用`$ binwalk --dd=".*" samplePhone.jpg`，一樣可以解壓縮出原本的圖片
:::

:::spoiler Flag
Flag: `537fe19a560ba3578d2f9095dc2f591489ff2cde`
:::

## ==Q25==
> When was the last time a docx file was opened on the device?
(An apple a day keeps the docx away. Answer in UTC, YYYY-MM-DD HH:MM:SS) 

### Recon
我原本的直覺是想可以parse \$MFT或是該檔案的lnk去看他的改動時間，但很不幸的MFT沒有這筆資料(?)，另外也沒有lnk檔案，所以只能通靈，以下解題過程是參考解完的hint

### Exploit
直接看RecentDocs的資訊就找的到了，該紀錄在Jim的NTUSER.DAT中，`Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs`
![圖片.png](https://hackmd.io/_uploads/SJvJlOw7p.png)

:::spoiler Flag
Flag: `2020-04-11 23:23:36`
:::

## ==Q26==
> How many entries does the MFT of the filesystem have?

### Exploit
我是直接在`/root`的地方export出\$MFT file，然後去看magic header(`FILE0`)的數量有多少(`219811`)，但這樣不準確(不清楚為甚麼)，我記得之前[@Jimmy說過](https://hackmd.io/@SBK6401/HJ-hG7Kzp#Lab---Offset-43110400d)
> $MFT長度一段就是1024 Bytes(0x400)

所以我想說可以把最後出現的位置除已0x400可能就是答案$\to 0xd6aac00/0x400=219819.0$
![圖片.png](https://hackmd.io/_uploads/BkUuMwDmp.png)
* 方法一
    不過以上的方法是確實可行的，因為計算entries不是只要看有多少有紀錄的File，而是整個\$MFT有多少空間，意思是我們要看最後位址是多少再除以0x400，而不是只算到最後一個FILE0的地方就直接除已0x400
    ![圖片.png](https://hackmd.io/_uploads/SJCs2DwX6.png)
    該檔案的最後位址是在0xd6bfff0
    $(0xd6bfff0+0x10)/0x400 = 219904.0$
    加上0x10是因為要算出完整的0x400才算一個，也就是我們要算最後一個就要padding
* 方法二
    後來參考[^wp]才知道比較正確的解法
    1. clone [mftdump](https://github.com/mcs6502/mftdump/blob/master/mftdump.py)
    2. create python 2 environment
    3. dump mft file
        ```bash
        $ conda activate py27
        $ python mftdump.py "MFT" > MFTdumpOutput.txt
        ```
    4. 看解出多少entries再扣掉最前面兩行不算的部分
        ![圖片.png](https://hackmd.io/_uploads/HJ20owwQp.png)
        ![圖片.png](https://hackmd.io/_uploads/SkmssPvXa.png)
        $219906-2=219904$

:::spoiler Flag
Flag: `219904`
:::

## ==Q27==
> Tim wanted to fire an employee because they were ......?(Be careful what you wish for)

### Exploit
呈第15題，直接看Tim的瀏覽紀錄就會知道了

:::spoiler Flag
Flag: `stinky`
:::

## Reference
[^wp]:[CyberDefenders: CorporateSecrets](https://forensicskween.com/ctf/cyberdefenders/corporatesecrets/)