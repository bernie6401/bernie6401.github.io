---
title: NTUSTISC - CyberDefender - MrRobot - Target 1
tags: [NTUSTISC, CyberDefender, Endpoint Forensics]

category: "Security Practice｜CyberDefender｜Endpoint Forensic｜MrRobot - Medium"
date: 2024-01-31
---

# NTUSTISC - CyberDefender - MrRobot - Target 1
<!-- more -->
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/88
Target 2: https://hackmd.io/@SBK6401/HJz2FPne6
POS: https://hackmd.io/@SBK6401/BJpJqDhlp

:::spoiler TOC
[TOC]
:::
Lecture Video: [ 2022/06/29 藍隊安全系列課程 04 ](https://youtu.be/4u5ckjfFRuM?si=MKeBkxyz5vcnsJfh)
[Volatility - Cheat Sheet](https://hackmd.io/@TuX-/BymMpKd0s)

## Background
* vmss2core
    題目下載之後會得到一些.vmss的檔案，這時候就需要下載[vmss2core.exe](https://flings.vmware.com/vmss2core)，.vmss是VMware經過轉換的snapshot，而這個工具可以把snapshot轉換成memory dump
    :::spoiler Execution Result
    ```bash
    $ vmss2core-sb-8456865.exe -W .\c69-Grrcon2015\pos01\POS-01-c4e8f786.vmss
    vmss2core version 8456865 Copyright (C) 1998-2017 VMware, Inc. All rights reserved.
    ... 10 MBs written.
    ... 20 MBs written.
    ... 30 MBs written.
    ...
    ... 1020 MBs written.
    Finished writing core.
    ```
    :::
* Volatility3: 安裝可以直接參考影片，建議直接使用windows exe protable file，這樣比較方便也穩定，而且還不需要擔心環境的問題

## Lab - Target 1

### 起手式
```bash
$ python vol.py -f memory.dmp imageinfo
Volatility Foundation Volatility Framework 2.6.1
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x86_23418, Win7SP0x86, Win7SP1x86_24000, Win7SP1x86 (Instantiated with WinXPSP2x86)
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : WindowsCrashDumpSpace32 (Unnamed AS)
                     AS Layer3 : FileAddressSpace (D:\Downloads\Trash\CyberDefenders\c69-Grrcon2015\target1\memory.dmp)
                      PAE type : PAE
                           DTB : 0x3ecc3260L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2015-10-09 12:53:02 UTC+0000
     Image local date and time : 2015-10-09 08:53:02 -0400
```
重要資訊System Name: Win7SP0x86

### ==Q1==
> What email address tricked the front desk employee into installing a security update? 

#### Recon
既然要找到email，可以有兩種思路，一種是直接看哪些檔案帶有email中常見的string，例如From之類的；另外一種思路是，查看之前執行過的process中有甚麼是和email有關係的，本題以思路1當作主要方式:

#### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 yarascan -Y "From:"
Volatility Foundation Volatility Framework 2.6
Rule: r1
Owner: Process OUTLOOK.EXE Pid 3196
0x086dffe1  46 72 6f 6d 3a 20 54 68 65 20 57 68 69 74 33 52   From:.The.Whit3R
0x086dfff1  30 73 33 20 3c 74 68 33 77 68 31 74 33 72 30 73   0s3.<th3wh1t3r0s
0x086e0001  33 40 67 6d 61 69 6c 2e 63 6f 6d 3e 0d 0a 54 6f   3@gmail.com>..To
0x086e0011  3a 20 3c 66 72 6f 6e 74 64 65 73 6b 40 61 6c 6c   :.<frontdesk@all
0x086e0021  73 61 66 65 63 79 62 65 72 73 65 63 2e 63 6f 6d   safecybersec.com
0x086e0031  3e 0d 0a 43 6f 6e 74 65 6e 74 2d 54 79 70 65 3a   >..Content-Type:
0x086e0041  20 6d 75 6c 74 69 70 61 72 74 2f 61 6c 74 65 72   .multipart/alter
0x086e0051  6e 61 74 69 76 65 3b 20 62 6f 75 6e 64 61 72 79   native;.boundary
0x086e0061  3d 22 30 30 31 61 31 31 33 34 33 32 37 38 62 64   ="001a11343278bd
0x086e0071  61 30 64 36 30 35 32 31 61 36 31 65 39 35 22 0d   a0d60521a61e95".
0x086e0081  0a 52 65 74 75 72 6e 2d 50 61 74 68 3a 20 74 68   .Return-Path:.th
0x086e0091  33 77 68 31 74 33 72 30 73 33 40 67 6d 61 69 6c   3wh1t3r0s3@gmail
0x086e00a1  2e 63 6f 6d 0d 0a 58 2d 4d 53 2d 45 78 63 68 61   .com..X-MS-Excha
0x086e00b1  6e 67 65 2d 4f 72 67 61 6e 69 7a 61 74 69 6f 6e   nge-Organization
0x086e00c1  2d 4e 65 74 77 6f 72 6b 2d 4d 65 73 73 61 67 65   -Network-Message
0x086e00d1  2d 49 64 3a 20 34 35 35 36 64 33 61 34 2d 33 38   -Id:.4556d3a4-38
```

:::spoiler Flag
Flag: `th3wh1t3r0s3@gmail.com`
:::

### ==Q2==
> What is the filename that was delivered in the email?

#### Recon
這一題一樣是要找和email相關的文件，有提示是一個執行檔，所以主要想法應該是把剛剛的process執行過程中的memory dump下來，再去分析他，試圖string search有沒有.exe的部分

#### Exploit
1. 先查詢當時執行那些process
    Command: `python vol.py -f ..\memory.dmp --profile Win7SP0x86 pslist`
    :::spoiler Command Result
    ```python
    $ python vol.py -f ..\memory.dmp --profile Win7SP0x86 pslist
    Volatility Foundation Volatility Framework 2.6.1
    Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit
    ---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
    0x83d334e8 System                    4      0     94      500 ------      0 2015-10-09 11:30:44 UTC+0000
    0x84edcbf0 smss.exe                276      4      2       30 ------      0 2015-10-09 11:30:44 UTC+0000
    0x84ecbb18 csrss.exe               368    360      9      366      0      0 2015-10-09 11:30:47 UTC+0000
    0x84f97628 wininit.exe             420    360      3       77      0      0 2015-10-09 11:30:48 UTC+0000
    0x855f6d40 csrss.exe               432    412     11      366      1      0 2015-10-09 11:30:48 UTC+0000
    0x8561d030 winlogon.exe            480    412      3      115      1      0 2015-10-09 11:30:48 UTC+0000
    0x84e979f8 services.exe            528    420      9      200      0      0 2015-10-09 11:30:48 UTC+0000
    0x8583b030 lsass.exe               536    420      9      851      0      0 2015-10-09 11:30:48 UTC+0000
    0x8583d960 lsm.exe                 544    420     10      163      0      0 2015-10-09 11:30:48 UTC+0000
    0x8586fd40 svchost.exe             644    528     11      351      0      0 2015-10-09 11:30:48 UTC+0000
    0x84e01448 svchost.exe             720    528      6      276      0      0 2015-10-09 11:30:50 UTC+0000
    0x85935030 svchost.exe             796    528     19      446      0      0 2015-10-09 11:30:51 UTC+0000
    0x85969030 svchost.exe             836    528     17      405      0      0 2015-10-09 11:30:52 UTC+0000
    0x85978940 svchost.exe             864    528     30     1036      0      0 2015-10-09 11:30:52 UTC+0000
    0x859cc2c0 svchost.exe            1008    528     13      650      0      0 2015-10-09 11:30:52 UTC+0000
    0x85a138f0 svchost.exe            1124    528     16      484      0      0 2015-10-09 11:30:53 UTC+0000
    0x8582c8d8 spoolsv.exe            1228    528     12      273      0      0 2015-10-09 11:30:53 UTC+0000
    0x85a55d40 svchost.exe            1256    528     17      304      0      0 2015-10-09 11:30:53 UTC+0000
    0x85ae3030 vmtoolsd.exe           1432    528      8      274      0      0 2015-10-09 11:30:54 UTC+0000
    0x85976318 svchost.exe            1784    528      5       99      0      0 2015-10-09 11:30:54 UTC+0000
    0x85ae0cb0 dllhost.exe            1888    528     13      196      0      0 2015-10-09 11:30:54 UTC+0000
    0x858b69e8 msdtc.exe              1980    528     12      145      0      0 2015-10-09 11:30:55 UTC+0000
    0x85c09968 dwm.exe                2088    836      3       93      1      0 2015-10-09 11:31:04 UTC+0000
    0x85c1e5f8 explorer.exe           2116   2060     23      912      1      0 2015-10-09 11:31:04 UTC+0000
    0x85c39030 taskhost.exe           2252    528      7      150      1      0 2015-10-09 11:31:04 UTC+0000
    0x859281f0 vmtoolsd.exe           2388   2116      7      164      1      0 2015-10-09 11:31:04 UTC+0000
    0x8598c920 SearchIndexer.         2544    528     13      670      0      0 2015-10-09 11:31:10 UTC+0000
    0x85d0d030 iexplore.exe           2996   2984      6      463      1      0 2015-10-09 11:31:27 UTC+0000
    0x85cd3d40 OUTLOOK.EXE            3196   2116     22     1678      1      0 2015-10-09 11:31:32 UTC+0000
    0x85d01510 svchost.exe            3232    528      9      131      0      0 2015-10-09 11:31:34 UTC+0000
    0x85b43a58 sppsvc.exe             3900    528      4      153      0      0 2015-10-09 11:32:54 UTC+0000
    0x83eb5d40 cmd.exe                2496   2116      1       22      1      0 2015-10-09 11:33:42 UTC+0000
    0x83e5cd40 conhost.exe             916    432      3       83      1      0 2015-10-09 11:33:42 UTC+0000
    0x83f105f0 cmd.exe                1856   2996      1       33      1      0 2015-10-09 11:35:15 UTC+0000
    0x83f13d40 conhost.exe            1624    432      3       81      1      0 2015-10-09 11:35:15 UTC+0000
    0x83fb86a8 cmd.exe                3064   2116      1       22      1      0 2015-10-09 11:37:32 UTC+0000
    0x83fa9030 conhost.exe             676    432      3       83      1      0 2015-10-09 11:37:32 UTC+0000
    0x83fb2d40 cmd.exe                3784   2196      1       24      1      0 2015-10-09 11:39:22 UTC+0000
    0x83fc7c08 conhost.exe            1824    432      3       85      1      0 2015-10-09 11:39:22 UTC+0000
    0x84013598 TeamViewer.exe         2680   1696     28      632      1      0 2015-10-09 12:08:46 UTC+0000
    0x84017d40 tv_w32.exe             4064   2680      2       83      1      0 2015-10-09 12:08:47 UTC+0000
    0x858bc278 TeamViewer_Des         1092   2680     16      405      1      0 2015-10-09 12:10:56 UTC+0000
    0x83f1ed40 mstsc.exe              2844   2116     11      484      1      0 2015-10-09 12:12:03 UTC+0000
    ```
    :::
    重要資訊: OUTLOOK.EXE -> PID -> ==3196==
2. 把執行OUTLOOK.EXE時候的memory dump下來
    ```bash
    $ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 memdump -p 3196 --dump-dir .\output\proc_dump_pid3196
    Volatility Foundation Volatility Framework 2.6
    ************************************************************************
    Writing OUTLOOK.EXE [  3196] to 3196.dmp
    ```
3. String Search `.exe`
    ```bash
    $ strings 3196.dmp | grep "\.exe" > output.txt
    ```
    經過不斷的嘗試最後找到`AnyConnectInstaller.exe`為最終答案

:::spoiler Flag
Flag: `AnyConnectInstaller.exe`
:::

### ==Q3==
> What is the name of the rat's family used by the attacker? 

#### Background
[深度調研：真實世界里的大規模RAT家族 ](https://www.freebuf.com/articles/network/268795.html)
> 遠程控制木馬(Remote Access Trojans，簡稱為 RAT)是一種主流的惡意程序，它賦予了攻擊者遠程監控和控制受害者主機的能力

#### Recon
這一題是要找出RAT家族程式的名字，所以從上一題可以知道受害電腦從email下載了一個程式(AnyConnect.exe)，所以如果要知道他是RAT家族的甚麼名字，可以透過hash直接上網查找或是直接用virustotal比對database，但反正第一步一定是要先取得這隻程式的樣本

#### Exploit
1. 找出文件中含有`AnyConnect`的字樣
    ```bash
    $ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 filescan | findstr "AnyConnect"
    Volatility Foundation Volatility Framework 2.6
    0x000000003df12dd0      2      0 RW-rwd \Device\HarddiskVolume2\Users\anyconnect\AnyConnect\AnyConnectInstaller.exe
    0x000000003df1cf00      4      0 R--r-d \Device\HarddiskVolume2\Users\anyconnect\AnyConnect\AnyConnectInstaller.exe
    0x000000003e0bc5e0      7      0 R--r-d \Device\HarddiskVolume2\Users\frontdesk\Downloads\AnyConnectInstaller.exe
    0x000000003e2559b0      8      0 R--rwd \Device\HarddiskVolume2\Users\frontdesk\Downloads\AnyConnectInstaller.exe
    0x000000003e2ae8e0      8      0 RWD--- \Device\HarddiskVolume2\Users\anyconnect\AnyConnect\AnyConnectInstaller.exe
    0x000000003ed57968      4      0 R--r-d \Device\HarddiskVolume2\Users\frontdesk\Downloads\AnyConnectInstaller.exe
    ```
2. 把該文件dump出來
    ```bash
    $ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 dumpfiles -n -D .\output\dumpfiles -Q 0x000000003e0bc5e0
    Volatility Foundation Volatility Framework 2.6
    ImageSectionObject 0x3e0bc5e0   None   \Device\HarddiskVolume2\Users\frontdesk\Downloads\AnyConnectInstaller.exe
    DataSectionObject 0x3e0bc5e0   None   \Device\HarddiskVolume2\Users\frontdesk\Downloads\AnyConnectInstaller.exe
    ```
    :::info
    -n: 代表包含文件原始名稱
    -Q: 代表physical offset
    -D: 代表dump出來要放的位址
    :::
3. 放到VirusTotal上查詢
詳細的審查結果可以看[這邊](https://www.virustotal.com/gui/file/94a4ef65f99c594a8bfbfbc57f369ec2b6a5cf789f91be89976086aaa507cd47)

:::spoiler Flag
Flag: `XtremeRat`
:::

### ==Q4==
> The malware appears to be leveraging process injection. What is the PID of the process that is injected?

#### Recon
這一題延伸了第二題的process list，因為process injection的操作，代表目前的process一定會出現在pslist，然後我是用暴力try try看，畢竟提示是四個digits，扣掉一些常見的windows process，應該沒剩多少
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 pslist
Volatility Foundation Volatility Framework 2.6
Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit
---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
...
0x85d0d030 iexplore.exe           2996   2984      6      463      1      0 2015-10-09 11:31:27 UTC+0000
...
```
:::spoiler Flag
Flag: `2996` $\to$ iexplore.exe
:::

### ==Q5==
> What is the unique value the malware is using to maintain persistence after reboot? 

#### Background
[註冊表中的運行鍵是什麼？ ](https://www.enigmasoftware.com/zh-hant/what-are-run-keys-registry/)
![](https://hackmd.io/_uploads/ryyXWrFla.png)

#### Recon
我們都知道惡意程式會在機碼設定重開機後自動執行，例如在:
`電腦\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
`電腦\HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run`
所以如果要看會不會重開機後自動執行，就直接看機碼

#### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 printkey -K "Microsoft\Windows\CurrentVersion\Run"
Volatility Foundation Volatility Framework 2.6
Legend: (S) = Stable   (V) = Volatile

----------------------------
Registry: \SystemRoot\System32\Config\SOFTWARE
Key name: Run (S)
Last updated: 2015-10-09 10:36:11 UTC+0000

Subkeys:

Values:
REG_SZ        VMware User Process : (S) "C:\Program Files\VMware\VMware Tools\vmtoolsd.exe" -n vmusr
REG_EXPAND_SZ MrRobot         : (S) c:\users\anyconnect\AnyConnect\AnyConnectInstaller.exe
```
:::info
printkey: 印出機碼路徑/子路徑/內容
-K: 機碼的路徑
:::

:::spoiler Flag
Flag: `MrRobot`
:::

### ==Q6==
> Malware often uses a unique value or name to ensure that only one copy runs on the system. What is the unique name the malware is using? 

#### Background
* [Windows HANDLE是什麼](https://blog.csdn.net/maowei117/article/details/55254855)
    這一篇講的出奇的好，他用程式設計的角度解釋為甚麼我們需要使用handle，若不使用的話會在甚麼情況出現問題等等，所以我對handle的理解是它就像一個pointer一樣，可以指向一個結構、process或是資源，而不同的結構創造出的handle不能通用，原因的話，文章中有提到，總而言之各個process產生的時候都需要各種不同的資源，例如螢幕、記憶體、鍵盤等等資源，而這些資源要怎麼只在這個process中被使用呢?答案就是利用handle，他可以只在該Process中指向該process所需要的資源，而不會和其他process搞混，如果再更進階一點可以看這一篇: [什麼是句柄？爲什麼會有句柄？HANDLE](https://www.twblogs.net/a/5db28078bd9eee310ee61694)
    > Handle本身是一個32位的無符號整數，它用來代表一個內核對象。它並不指向實際的內核對象，用戶模式下的程序永遠不可能獲得一個內核對象的實際地址（一般情況下）。那麼Handle的意義何在？它實際上是作爲一個索引在一個表中查找對應的內核對象的實際地址。那麼這個表在哪裏呢？每個進程都有這樣的一個表，叫句柄表。該表的第一項就是進程自己的句柄，這也是爲什麼你調用GetCurrentProcess()總是返回0x7FFFFFFF原因。
    > 簡單地說，Handle就是一種用來"間接"代表一個內核對象的整數值。你可以在程序中使用handle來代表你想要操作的內核對象。這裏的內核對象包括：事件（Event）、線程、進程、Mutex等等。我們最常見的就是文件句柄（file handle）
* [如何打開.dat 文件](https://www.freecodecamp.org/chinese/news/dat-file-how-to-open-the-dat-file-format-extension/)
    > DAT 文件是一個數據文件，其中包含有關用於創建它的程序的特定信息。

#### Recon
回到目前的題目，雖然沒有提到handle等字眼，但我們可以推測其實每一個process在建立的時候都會有一個特殊的handle table，而且該table是for該process唯一的，則我們就可以往handle的方向去想，再搭配前面找到的PID，就可以幫助我們找到答案。

#### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 handles -p 2996 | findstr ".dat"
Volatility Foundation Volatility Framework 2.6
0x85d11700   2996      0x150   0x1f0001 Mutant           fsociety0.dat
```
根據主要參考WP[^cyberdefender-mrrobot-wp]的說法
> Malware typically uses a mutant/mutex to run a single copy of malware on the system and to avoid reinfecting the host, which can increase the chances of detection by security tools.

而根據[MSDN-HANDLE](https://learn.microsoft.com/zh-tw/windows-hardware/drivers/debugger/-handle)中的說明，mutant是handle的其中一種類型，他還有其他的，例如event, file, port, directory之類的
:::spoiler Flag
Flag: `fsociety0.dat`
:::

### ==Q7==
> It appears that a notorious hacker compromised this box before our current attackers. Name the movie he or she is from. 

#### Recon
這一題的重點在於我要找到一個名字，所以直覺會想說從username開始找，所以一樣從

#### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 filescan | findstr User > .\output\filescan\findstr_User.txt
```
然後就利用一些文字編輯器，找名字，應該沒有很多，所以可以找到一些名字，大部分是`frontdesk`, `FRONTD~1`, `Administrator`等等，但應該可以找到`gideon`和`zerocool`的名字，前者應該是原使用者的名字，而後者應該是駭客的名字，上網搜尋一下發現zerocool是《Hackers》(1995年上映的電影)中出現的駭客名字

:::spoiler Flag
Flag: `Hackers`
:::

### ==Q8==
> What is the NTLM password hash for the administrator account?

#### Background
[NTUSTISC - AD Note - Lab(透過Mimikatz取得Local Admin的NTLM)](https://hackmd.io/@SBK6401/H15R2zNAh)

#### Recon
既然是要找NTLM hash，可以使用hashdump這個Plugin

#### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 hashdump
Volatility Foundation Volatility Framework 2.6
Administrator:500:aad3b435b51404eeaad3b435b51404ee:79402b7671c317877b8b954b3311fa82:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
front-desk:1000:aad3b435b51404eeaad3b435b51404ee:2ae4c526659523d58350e4d70107fc11:::
```

:::spoiler Flag
Flag: `79402b7671c317877b8b954b3311fa82`
:::

### ==Q9==
> The attackers appear to have moved over some tools to the compromised front desk host. How many tools did the attacker move? 

#### Recon
Attacker既然有用到一些指令操作，搬運一些檔案，我們直覺可以想到也許可以從console身上撈到一點command的歷史紀錄，判斷font desk有哪些exe file

#### Exploit
:::spoiler Command Result
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 consoles
...
C:\Windows\system32>cd ..                                                       
                                                                                
C:\Windows>cd Temp                                                              
                                                                                
C:\Windows\Temp>dir                                                             
 Volume in drive C has no label.                                                
 Volume Serial Number is FE0F-F423                                              
                                                                                
 Directory of C:\Windows\Temp                                                   
                                                                                
10/09/2015  07:29 AM    <DIR>          .                                        
10/09/2015  07:29 AM    <DIR>          ..                                       
10/09/2015  01:27 AM                 0 DMIE58D.tmp                              
10/09/2015  06:57 AM            50,176 getlsasrvaddr.exe                        
10/09/2015  02:02 AM             7,572 MpCmdRun.log                             
10/09/2015  12:07 AM             4,636 MpSigStub.log                            
10/09/2015  03:37 AM    <DIR>          MPTelemetrySubmit                        
10/09/2015  06:45 AM            36,864 nbtscan.exe                              
10/09/2015  06:44 AM           503,800 Rar.exe                                  
10/09/2015  01:28 AM           180,224 TS_A16D.tmp                              
10/09/2015  01:28 AM           196,608 TS_A3BF.tmp                              
10/09/2015  01:28 AM           376,832 TS_A42D.tmp                              
10/09/2015  01:28 AM           114,688 TS_A528.tmp                              
10/09/2015  01:28 AM           425,984 TS_A5C5.tmp                              
10/09/2015  01:28 AM           131,072 TS_A807.tmp                              
10/09/2015  01:28 AM           655,360 TS_A911.tmp                              
10/09/2015  01:28 AM           114,688 TS_AA79.tmp                              
10/09/2015  01:28 AM           180,224 TS_AF79.tmp                              
10/08/2015  11:43 PM    <DIR>          vmware-SYSTEM                            
10/09/2015  07:16 AM                 0 w.tmp                                    
10/09/2015  06:45 AM           199,168 wce.exe                                  
              17 File(s)      3,177,896 bytes                                   
               4 Dir(s)  22,602,948,608 bytes free
...
```
:::
可以從該指令的結果輸出，看出該文件含有幾個exe file: `getlsasrvaddr.exe`, `nbtscan.exe`, `Rar.exe`, `wce.exe`，所以基本上答案應該是4但因為`getlsasrvaddr.exe`和`wce.exe`都是來自一個[wce](https://github.com/returnvar/wce)github repo中，所以其實只有算3個

:::spoiler Flag
Flag: `3`
:::

### ==Q10==
> What is the password for the front desk local administrator account? 

#### Background
runas就是windows的command用來"以系統管理員權限"執行一些指令或是開啟process

#### Recon
同樣要取得admin的password，可以直接看上一題的console輸出，或是直接hashcat NTLM的hash，詳細的操作可以看[NTUSTISC - AD Note - Lab(Brute Force SAM)](https://hackmd.io/@SBK6401/B1LqaNGCh/https%3A%2F%2Fhackmd.io%2F%40SBK6401%2FS1KgaEz0h)
```bash
$ $ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 hashdump > ntlm.hash
$ hashcat.exe -a 0 -m 1000 ntlm.hash rockyou.txt --force
```
不過如果從console上來看也可以看出他的一些操作，因為attacker的目的同樣是要把credential的password dump出來，所以最後一定會有相關的訊息跑出來

#### Exploit
Console的操作如下:
```bash
$ cd ..
$ cd Temp
$ dir
$ wce.exe -w
$ wce.exe -w > w.tmp # 從這邊取得frontdesk\ALLSAFECYBERSEC的密碼為THzV7mpz
---
$ cd ..
$ cd Temp
$ wce.exe -w
$ runas /profile /user:Administrator # 這邊應該是不太熟悉runas的操作
$ runas /profile /user:Administrator cmd # 應該是利用剛剛取得Administartor的密碼進行提權
---
$ cd ..
$ cd Temp
$ dir
$ wce.exe -w
$ wce.exe -w > w.tmp # 從這邊取得Administrator\front-desk-PC的密碼為flagadmin@1234
```
然後實際用[online tool](https://codebeautify.org/ntlm-hash-generator)查看該密碼的ntlm的確是前兩題得到的`79402b7671c317877b8b954b3311fa82`

:::spoiler Flag
Flag: `flagadmin@1234`
:::

### ==Q11==
> What is the std create data timestamp for the nbtscan.exe tool? 

#### Background
[nbtscan 掃描WINDOWS網絡NetBIOS信息軟件](https://blog.csdn.net/weixin_40277264/article/details/121207530)
> 互聯網搜索引擎nbtscan是一個掃描WINDOWS網絡NetBIOS信息的小工具。只能用於局域網，可以顯示IP，主機名，用戶名稱和MAC地址等等。

#### Recon
如果是要找到某個東西的timestamp，可以考慮直接用timeliner這個plubin，主要的功能是就是建立記憶體中的各種痕跡資訊的時間線

#### Exploit
```bash!
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 timeliner | findstr nbtscan.exe
Volatility Foundation Volatility Framework 2.6
2015-10-09 10:45:12 UTC+0000|[SHIMCACHE]| \??\C:\Windows\Temp\nbtscan.exe|
```

:::spoiler Flag
Flag: `2015-10-09 10:45:12 UTC`
:::

### ==Q12==
> The attackers appear to have stored the output from the nbtscan.exe tool in a text file on a disk called nbs.txt. What is the IP address of the first machine in that file?

#### Recon
這一題要先把nbs.txt找出來，再把它dump出來，之後查看這支file存的內容

#### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 filescan | findstr nbs.txt
Volatility Foundation Volatility Framework 2.6
0x000000003fdb7808      8      0 -W-r-- \Device\HarddiskVolume2\Windows\Temp\nbs.txt
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 dumpfiles -n -D .\output\dumpfiles -Q 0x000000003fdb7808
Volatility Foundation Volatility Framework 2.6
DataSectionObject 0x3fdb7808   None   \Device\HarddiskVolume2\Windows\Temp\nbs.txt
$ strings file.None.0x83eda598.nbs.txt.dat
10.1.1.2        ALLSAFECYBERSEC\AD01            SHARING DC
10.1.1.3        ALLSAFECYBERSEC\EX01            SHARING
10.1.1.20       ALLSAFECYBERSEC\FRONT-DESK-PC   SHARING
10.1.1.21       ALLSAFECYBERSEC\GIDEON-PC       SHARING
```

:::spoiler Flag
Flag: `10.1.1.2`
:::

### ==Q13==
> What is the full IP address and the port was the attacker's malware using? 

#### Recon
這一題和網路有關，所以可以使用網路相關的plugin，不過不管是windows的執行檔，還是python的版本，在help的說明中都沒有提到這一題該使用的plugin，看了別人的WP才知道要用netscan不過help man根本沒寫，找了超久，可能是版本更新後忘了寫上去?反正在[github的舊版wiki](https://github.com/volatilityfoundation/volatility/wiki/Command-Reference)有這東西。另外根據我們上一題的結果知道，attacker掃到的內網IP中，第一台機器就是`10.1.1.2`，所以可以鎖定這個IP繼續查

#### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 netscan
Volatility Foundation Volatility Framework 2.6
Offset(P)          Proto    Local Address                  Foreign Address      State            Pid      Owner          Created
...
0x3deba9a0         UDPv4    10.1.1.20:56813                *:*                                   3232     svchost.exe    2015-10-09 11:32:55 UTC+0000
0x3e143978         UDPv4    10.1.1.20:1900                 *:*                                   3232     svchost.exe    2015-10-09 11:32:55 UTC+0000
0x3e25bc60         UDPv4    10.1.1.20:138                  *:*                                   4        System         2015-10-09 11:30:49 UTC+0000
0x3e2b0f50         UDPv4    10.1.1.20:137                  *:*                                   4        System         2015-10-09 11:30:49 UTC+0000
0x3e2b08a8         TCPv4    10.1.1.20:139                  0.0.0.0:0            LISTENING        4        System
0x3de98df8         TCPv4    10.1.1.20:49261                10.1.1.21:445        ESTABLISHED      4        System
0x3e0d0df8         TCPv4    10.1.1.20:49208                10.1.1.3:80          ESTABLISHED      3196     OUTLOOK.EXE
0x3e0eedf8         TCPv4    10.1.1.20:49205                180.76.254.120:22    ESTABLISHED      2996     iexplore.exe
0x3e1e5008         TCPv4    10.1.1.20:49330                10.1.1.2:139         CLOSED           4        System
0x3e1f0df8         TCPv4    10.1.1.20:49207                10.1.1.3:80          ESTABLISHED      3196     OUTLOOK.EXE
0x3e1fadf8         TCPv4    10.1.1.20:49314                10.1.1.3:443         CLOSED           3196     OUTLOOK.EXE
0x3fa4dbf8         TCPv4    10.1.1.20:49333                10.1.1.3:443         CLOSED           3196     OUTLOOK.EXE
0x3fa8d1d8         TCPv4    10.1.1.20:49336                10.1.1.3:443         CLOSED           3196     OUTLOOK.EXE
0x3fa95df8         TCPv4    10.1.1.20:49297                192.96.201.138:5938  ESTABLISHED      2680     TeamViewer.exe
0x3fb7a560         TCPv4    10.1.1.20:49301                10.1.1.21:3389       ESTABLISHED      2844     mstsc.exe
0x3fc426a8         TCPv4    10.1.1.20:49291                107.6.97.19:5938     ESTABLISHED      2680     TeamViewer.exe
```
:::spoiler Flag
Flag: `180.76.254.120:22`
:::

### ==Q14==
> It appears the attacker also installed legit remote administration software. What is the name of the running process?

#### Recon
這一題超簡單，應該寫到前面幾題就可以寫這一題了，也就是attacker還安裝了別種RDP軟體，看了前面的pslist就知道TeamViewer在搞事

#### Exploit
:::spoiler Flag
Flag: `TeamViewer.exe`
:::

### ==Q15==
> It appears the attackers also used a built-in remote access method. What IP address did they connect to?

#### Background
[Windows 內建的遠端桌面連線工具設定與使用教學](https://www.kjnotes.com/windows/31)
mstsc是windows內建的遠端連線工具

#### Recon
這也超簡單，看一下上上一題的netscan執行結果，就可以知道他有執行mstsc.exe的process，如果直接看pslist也看得出來他有執行，所以在前面幾題的時候久可以朝這個方向思考可能的攻擊手法

#### Exploit
:::spoiler Flag
Flag: `10.1.1.21`
:::

## Reference
[^cyberdefender-mrrobot-wp]:[MrRobot Walkthrough — Cyberdefenders](https://responderj01.medium.com/mrrobot-walkthrough-cyberdefenders-7694e3120897)