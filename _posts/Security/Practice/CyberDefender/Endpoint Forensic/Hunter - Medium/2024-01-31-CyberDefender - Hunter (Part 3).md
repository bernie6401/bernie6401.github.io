---
title: CyberDefender - Hunter (Part 3)
tags: [CyberDefender, Endpoint Forensics]

category: "Security/Practice/CyberDefender/Endpoint Forensic/Hunter - Medium"
---

# CyberDefender - Hunter (Part 3)
<!-- more -->
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/32
Part 1: https://hackmd.io/@SBK6401/By1BpZIf6
Part 2: https://hackmd.io/@SBK6401/HJlmeuwfT

:::spoiler TOC
[TOC]
:::

## Tools
* [JLECmd](https://ericzimmerman.github.io/#!index.md)

## ==Q21==
> One of the installed applications is a file shredder. What is the name of the application? (two words space separated) 

### Recon
承接上一題，我們已經知道BCWipe就是題目要的答案，也就是類似file shredder的工具，但前面六個字還是沒有想法，看了一下外層資料夾才發現[Jetico](https://www.jetico.com/)是啥東西啊，上網查才發現是提供各種data encryption/data wiping/endpoint data protection之類的公司，所以這一題的正確答案是`Jetico BCWipe`

:::spoiler Flag
Flag: `Jetico BCWipe`
:::

## ==Q22==
> How many prefetch files were discovered on the system? 

### Recon
就只是到`/root/Windows/Prefetch/`中數有多少的.pf檔案(善用排序)
![圖片.png](https://hackmd.io/_uploads/ByDB9sgX6.png)

:::spoiler Flag
Flag: `174`
:::

## ==Q23==
> How many times was the file shredder application executed? 

### Recon
我們已經知道file shredder就是BCWipe這個軟體，那我們如果要知道這個軟體的相關資訊可以直接看prefetch file(就像[Part 1 - Q9](https://hackmd.io/@SBK6401/By1BpZIf6#Q9)一樣)

### Exploit
從結果可以得知共執行五次
:::spoiler Result
```bash
$ ./PECmd.exe -f BCWIPE.EXE-36F3F2DF.pf
PECmd version 1.5.0.0

Author: Eric Zimmerman (saericzimmerman@gmail.com)
https://github.com/EricZimmerman/PECmd

Command line: -f BCWIPE.EXE-36F3F2DF.pf

Keywords: temp, tmp

Processing BCWIPE.EXE-36F3F2DF.pf

Created on: 2023-11-02 04:55:47
Modified on: 2016-06-21 12:02:45
Last accessed on: 2023-11-02 04:55:53

Executable name: BCWIPE.EXE
Hash: 36F3F2DF
File size (bytes): 72,524
Version: Windows 8.0, Windows 8.1, or Windows Server 2012(R2)

Run count: 5
Last run: 2016-06-21 12:02:35
Other run times: 2016-06-21 12:02:39, 2016-06-21 12:01:35, 2016-06-21 12:01:00, 2016-06-21 12:00:56

Volume information:

#0: Name: \DEVICE\HARDDISKVOLUME2 Serial: 669B1B2A Created: 2016-06-21 09:09:24 Directories: 14 File references: 84
#1: Name: \DEVICE\HARDDISKVOLUMESHADOWCOPY1 Serial: 669B1B2A Created: 2016-06-21 09:09:24 Directories: 0 File references: 0
#2: Name: \DEVICE\HARDDISKVOLUMESHADOWCOPY2 Serial: 669B1B2A Created: 2016-06-21 09:09:24 Directories: 0 File references: 0

Directories referenced: 14

00: \DEVICE\HARDDISKVOLUME2\$RECYCLE.BIN
01: \DEVICE\HARDDISKVOLUME2\$RECYCLE.BIN\S-1-5-21-2489440558-2754304563-710705792-1001
02: \DEVICE\HARDDISKVOLUME2\PROGRAM FILES (X86)
03: \DEVICE\HARDDISKVOLUME2\PROGRAM FILES (X86)\JETICO
04: \DEVICE\HARDDISKVOLUME2\PROGRAM FILES (X86)\JETICO\BCWIPE
05: \DEVICE\HARDDISKVOLUME2\PROGRAM FILES (X86)\JETICO\SHARED
06: \DEVICE\HARDDISKVOLUME2\WINDOWS
07: \DEVICE\HARDDISKVOLUME2\WINDOWS\FONTS
08: \DEVICE\HARDDISKVOLUME2\WINDOWS\GLOBALIZATION
09: \DEVICE\HARDDISKVOLUME2\WINDOWS\GLOBALIZATION\SORTING
10: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSTEM32
11: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSTEM32\EN-US
12: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64
13: \DEVICE\HARDDISKVOLUME2\WINDOWS\WINSXS\X86_MICROSOFT.WINDOWS.COMMON-CONTROLS_6595B64144CCF1DF_6.0.9600.17031_NONE_A9EFDB8B01377EA7

Files referenced: 113

00: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSTEM32\NTDLL.DLL
01: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSTEM32\WOW64.DLL
02: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSTEM32\WOW64WIN.DLL
03: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSTEM32\WOW64CPU.DLL
04: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSTEM32\KERNEL32.DLL
05: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\KERNEL32.DLL
06: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSTEM32\USER32.DLL
07: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\NTDLL.DLL
08: \DEVICE\HARDDISKVOLUME2\PROGRAM FILES (X86)\JETICO\BCWIPE\BCWIPE.EXE (Executable: True)
09: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\KERNELBASE.DLL
10: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSTEM32\LOCALE.NLS
11: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\VERSION.DLL
12: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\USER32.DLL
13: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\GDI32.DLL
14: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\COMDLG32.DLL
15: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\ADVAPI32.DLL
16: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\SHELL32.DLL
17: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\MSVCRT.DLL
18: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\SHLWAPI.DLL
19: \DEVICE\HARDDISKVOLUME2\WINDOWS\WINSXS\X86_MICROSOFT.WINDOWS.COMMON-CONTROLS_6595B64144CCF1DF_6.0.9600.17031_NONE_A9EFDB8B01377EA7\COMCTL32.DLL
20: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\SECHOST.DLL
21: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\RPCRT4.DLL
22: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\COMBASE.DLL
23: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\SSPICLI.DLL
24: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\SHCORE.DLL
25: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\CRYPTBASE.DLL
26: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\BCRYPTPRIMITIVES.DLL
27: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\IMM32.DLL
28: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\MSCTF.DLL
29: \DEVICE\HARDDISKVOLUME2\WINDOWS\WINDOWSSHELL.MANIFEST
30: \DEVICE\HARDDISKVOLUME2\PROGRAM FILES (X86)\JETICO\SHARED\BCWIPE.DLL
31: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\OLE32.DLL
32: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\OLEAUT32.DLL
33: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\SFC.DLL
34: \DEVICE\HARDDISKVOLUME2\PROGRAM FILES (X86)\JETICO\BCWIPE\LANGFILE2.DLL
35: \DEVICE\HARDDISKVOLUME2\PROGRAM FILES (X86)\JETICO\BCWIPE\LICENSE.TXT
36: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\CRYPT32.DLL
37: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\MSASN1.DLL
38: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\WINTRUST.DLL
39: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\CRYPTSP.DLL
40: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\RSAENH.DLL
41: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\BCRYPT.DLL
42: \DEVICE\HARDDISKVOLUME2\WINDOWS\GLOBALIZATION\SORTING\SORTDEFAULT.NLS
43: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\IMAGEHLP.DLL
44: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSTEM32\EN-US\CRYPT32.DLL.MUI
45: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\NCRYPT.DLL
46: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\NTASN1.DLL
47: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\GPAPI.DLL
48: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\PROFAPI.DLL
49: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\NTMARTA.DLL
50: \DEVICE\HARDDISKVOLUME2\$RECYCLE.BIN\S-1-5-21-2489440558-2754304563-710705792-1001\DESKTOP.INI
51: \DEVICE\HARDDISKVOLUME2\$RECYCLE.BIN\S-1-5-21-2489440558-2754304563-710705792-1001\$IJJWGAC
52: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\UXTHEME.DLL
53: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\SETUPAPI.DLL
54: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\CFGMGR32.DLL
55: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSTEM32\EN-US\SETUPAPI.DLL.MUI
56: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\DWMAPI.DLL
57: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSTEM32\EN-US\USER32.DLL.MUI
58: \DEVICE\HARDDISKVOLUME2\WINDOWS\FONTS\STATICCACHE.DAT
59: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\KERNEL.APPCORE.DLL
60: \DEVICE\HARDDISKVOLUME2\PROGRAM FILES (X86)\JETICO\SHARED\BCWIPELIB2.DLL
61: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\FLTLIB.DLL
62: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\PSAPI.DLL
63: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\NETAPI32.DLL
64: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\MPR.DLL
65: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\NETUTILS.DLL
66: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\SRVCLI.DLL
67: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\WKSCLI.DLL
68: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\PROPSYS.DLL
69: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\CLBCATQ.DLL
70: \DEVICE\HARDDISKVOLUME2\PROGRAMDATA\MICROSOFT\WINDOWS\CACHES\CVERSIONS.2.DB
71: \DEVICE\HARDDISKVOLUME2\PROGRAMDATA\MICROSOFT\WINDOWS\CACHES\{6AF0698E-D558-4F6E-9B3C-3716689AF493}.2.VER0X0000000000000004.DB
72: \DEVICE\HARDDISKVOLUME2\PROGRAMDATA\MICROSOFT\WINDOWS\CACHES\{DDF571F2-BE98-426D-8288-1A9A39C3FDA2}.2.VER0X0000000000000002.DB
73: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSTEM32\EN-US\PROPSYS.DLL.MUI
74: \DEVICE\HARDDISKVOLUME2\USERS\HUNTER\DESKTOP\DESKTOP.INI
75: \DEVICE\HARDDISKVOLUME2\USERS\HUNTER\DOCUMENTS\DESKTOP.INI
76: \DEVICE\HARDDISKVOLUME2\USERS\HUNTER\MUSIC\DESKTOP.INI
77: \DEVICE\HARDDISKVOLUME2\USERS\HUNTER\PICTURES\DESKTOP.INI
78: \DEVICE\HARDDISKVOLUME2\USERS\HUNTER\VIDEOS\DESKTOP.INI
79: \DEVICE\HARDDISKVOLUME2\USERS\HUNTER\DOWNLOADS\DESKTOP.INI
80: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\URLMON.DLL
81: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\IERTUTIL.DLL
82: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\WININET.DLL
83: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\USERENV.DLL
84: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\SECUR32.DLL
85: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\PCACLI.DLL
86: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\APPHELP.DLL
87: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\SFC_OS.DLL
88: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\DEVRTL.DLL
89: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\WBEM\WBEMPROX.DLL
90: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\WS2_32.DLL
91: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\WBEMCOMN.DLL
92: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\NSI.DLL
93: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\WBEM\WBEMSVC.DLL
94: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\WBEM\FASTPROX.DLL
95: \DEVICE\HARDDISKVOLUME2\$MFT
96: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\VSSAPI.DLL
97: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\VSSTRACE.DLL
98: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\DSROLE.DLL
99: \DEVICE\HARDDISKVOLUME2\WINDOWS\SYSWOW64\BCD.DLL
100: \DEVICE\HARDDISKVOLUME2\USERS\HUNTER\APPDATA\LOCAL\TEMP\BCS576923DD.TMP (Keyword: True)
101: \DEVICE\HARDDISKVOLUMESHADOWCOPY1\$MFT
102: \DEVICE\HARDDISKVOLUMESHADOWCOPY2\$MFT
103: \DEVICE\HARDDISKVOLUME2\$RECYCLE.BIN\S-1-5-21-2489440558-2754304563-710705792-1001\$RJJWGAC\VKORPPVHKXUVQCVJ
104: \DEVICE\HARDDISKVOLUME2\$RECYCLE.BIN\S-1-5-21-2489440558-2754304563-710705792-1001\SHATBBMS.DIF:???
105: \DEVICE\HARDDISKVOLUME2\~BCWIPE.TMP\BCW-DIR-NODES\DIR1:??? (Keyword: True)
106: \DEVICE\HARDDISKVOLUME2\~BCWIPE.TMP\BCW-DIR-NODES\DIR2:??? (Keyword: True)
107: \DEVICE\HARDDISKVOLUME2\USERS\HUNTER:???
108: \DEVICE\HARDDISKVOLUME2\$RECYCLE.BIN\C7A6090EE:???
109: \DEVICE\HARDDISKVOLUME2\WINDOWS\APPPATCH\SYSMAIN.SDB
110: \DEVICE\HARDDISKVOLUME2\USERS\HUNTER\APPDATA\LOCAL\TEMP\S64_5762C6FA.TMP (Keyword: True)
111: \DEVICE\HARDDISKVOLUME2\USERS\HUNTER\APPDATA\LOCAL\MICROSOFT\WINDOWS\CACHES\CVERSIONS.1.DB
112: \DEVICE\HARDDISKVOLUME2\USERS\HUNTER\APPDATA\LOCAL\MICROSOFT\WINDOWS\CACHES\{AFBF9F1A-8EE8-4C77-AF34-C647E37CA0D9}.1.VER0X0000000000000002.DB


---------- Processed BCWIPE.EXE-36F3F2DF.pf in 0.07580980 seconds ----------
```
:::
:::spoiler Flag
Flag: `5`
:::

## ==Q24==
> Using prefetch, determine when was the last time ZENMAP.EXE-56B17C4C.pf was executed? 

### Recon
直接看[Part 1 - Q9](https://hackmd.io/@SBK6401/By1BpZIf6#Q9)的輸出結果就好了

:::spoiler Flag
Flag: `06/21/2016 12:08:13 PM`
:::

## ==Q25==
> A JAR file for an offensive traffic manipulation tool was executed. What is the absolute path of the file? 

### Recon
通常直覺會是到program file去看一下，不過有時候載下來的軟體可能是portable version，所以我也到downloads去看，發現唯一一個jar file就是burpsuite

:::spoiler Flag
Flag: `C:\Users\Hunter\Downloads\burpsuite_free_v1.7.03.jar`
:::

## ==Q26==
> The suspect employee tried to exfiltrate data by sending it as an email attachment. What is the name of the suspected attachment? 

### Recon
用[pst viewer](https://goldfynch.com/pst-viewer/index.html#0/33474)瀏覽一下信件就知道了

:::spoiler Flag
Flag: `Pictures.7z`
:::

## ==Q27==
> Shellbags shows that the employee created a folder to include all the data he will exfiltrate. What is the full path of that folder? 

### Recon
看一下pictures裡面的資料夾很明顯的Exfil就是我們的目標
![圖片.png](https://hackmd.io/_uploads/SksFlnlXa.png)

:::spoiler Flag
Flag: `C:\Users\Hunter\Pictures\Exfil`
:::

## ==Q28==
> The user deleted two JPG files from the system and moved them to $Recycle-Bin. What is the file name that has the resolution of 1920x1200? 

### Recon
這應該是嘗試，如果刪除檔案會直接丟到recycle bin，所以可以直接到這邊去撈，不過從recycle bin撈到的檔案貌似損毀，紙看到應該是貓貓的耳朵
![$RP3TBNW.jpg](https://hackmd.io/_uploads/SJzGb3lmT.jpg)

所以可以查看一下原圖是甚麼，我是直接從Pictures裡面的private中撈檔案
![ws_Small_cute_kitty_1920x1200.jpg](https://hackmd.io/_uploads/SkQ8ZngX6.jpg)
剛好檔案大小誠如題目所述

:::spoiler Flag
Flag: `ws_Small_cute_kitty_1920x1200.jpg`
:::

## ==Q29==
> Provide the name of the directory where information about jump lists items (created automatically by the system) is stored? 

### Background
[ChatGPT](https://chat.openai.com/c/80f38bc8-4d9b-41a2-ae96-2a0e1f0b3e68)
* 甚麼是windows jump list
    > Windows Jump List（視窗跳躍清單）是微軟Windows操作系統的一個功能，它允許用戶在任務欄或開始菜單中快速訪問最近使用的文件或網站。
    > Jump List通常包含以下元素：
    > 
    > 最近打開的文件：這些是您最近打開的文件或應用程序，讓您可以快速重新訪問它們。
    > 
    > 固定的項目：您可以將特定文件或應用程序釘選到Jump List中，以便隨時方便訪問。
    > 
    > 一些應用程序還可以自定義Jump List，提供特定功能或快速操作的選項。
    > Jump List通常會顯示在相應應用程序的任務欄圖標上，並提供一個方便的方式來訪問最近的活動。
    > 
    > 請注意，某些應用程序可能會選擇不支持Jump List功能，這取決於開發人員的實現方式。

### Recon
我直接問ChatGPT後得到以下回答: 
> The directory where information about jump list items (created automatically by the system) is stored in Windows is:
>```shell
>%APPDATA%\Microsoft\Windows\Recent\AutomaticDestinations
>```
>This directory contains files that store information about recently accessed items and is used by the Jump List feature in Windows. Each file corresponds to a specific application or taskbar icon. Please note that these files are in a binary format and are not meant to be manually modified.

:::spoiler Flag
Flag: `AutomaticDestinations`
:::

## ==Q30==
> Using JUMP LIST analysis, provide the full path of the application with the AppID of "aa28770954eaeaaa" used to bypass network security monitoring controls. 

### Recon
該用到新工具的時候了，下載[JLECmd](https://ericzimmerman.github.io/#!index.md)後可以直接查看.ms file，就是我們上一題找到的地方，在`Recent/CustomDestinations`的地方有這一題著重探到的`aa28770954eaeaaa`，export出來之後就可以開始分析

### Exploit
```shell
$ ./JLECmd.exe -f aa28770954eaeaaa.customDestinations-ms
JLECmd version 1.5.0.0

Author: Eric Zimmerman (saericzimmerman@gmail.com)
https://github.com/EricZimmerman/JLECmd

Command line: -f aa28770954eaeaaa.customDestinations-ms

Processing D:\Software\CTF\Misc\JLECmd\aa28770954eaeaaa.customDestinations-ms

Source file: D:\Software\CTF\Misc\JLECmd\aa28770954eaeaaa.customDestinations-ms

--- AppId information ---
AppID: aa28770954eaeaaa, Description: null
--- DestList information ---
  Entries:  1

  Entry #: 0, lnk count: 3 Rank: 1.4013E-45

--- Lnk #0 information ---
  Lnk target created:  2000-01-01 00:00:00
  Lnk target modified: 2000-01-01 00:00:00
  Lnk target accessed: 2016-06-21 10:51:23

  Absolute path: Tor Browser\Browser\firefox.exe

--- Lnk #1 information ---
  Lnk target created:  2000-01-01 00:00:00
  Lnk target modified: 2000-01-01 00:00:00
  Lnk target accessed: 2016-06-21 10:51:23

  Absolute path: Tor Browser\Browser\firefox.exe

--- Lnk #2 information ---
  Lnk target created:  2000-01-01 00:00:00
  Lnk target modified: 2000-01-01 00:00:00
  Lnk target accessed: 2016-06-21 10:51:23

  Absolute path: Tor Browser\Browser\firefox.exe



---------- Processed D:\Software\CTF\Misc\JLECmd\aa28770954eaeaaa.customDestinations-ms in 0.27381430 seconds ----------
```

我們到了jump list的absolute path之後就可以回去翻他在哪邊，原來是在desktop
![圖片.png](https://hackmd.io/_uploads/rykII2gXp.png)

:::spoiler Flag
Flag: `C:\Users\Hunter\Desktop\Tor Browser\Browser\firefox.exe`
:::

## Reference
[Cyberdefenders.org Hunter Walkthrough](https://medium.com/@cyberforensicator57/cyberdefenders-org-hunter-walkthrough-65c0c6cb8e87)