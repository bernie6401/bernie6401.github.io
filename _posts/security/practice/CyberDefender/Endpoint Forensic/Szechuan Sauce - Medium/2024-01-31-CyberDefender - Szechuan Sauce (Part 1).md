---
title: CyberDefender - Szechuan Sauce (Part 1)
tags: [CyberDefender, Endpoint Forensics]

category: "Security/Practice/CyberDefender/Endpoint Forensic/Szechuan Sauce - Medium"
---

# CyberDefender - Szechuan Sauce (Part 1)
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/31
Part 2: https://hackmd.io/@SBK6401/HkAbt-NXT
:::spoiler TOC
[TOC]
:::

## Scenario
> An employee at a large company was assigned a task with a two-day deadline. Realizing that he could not complete the task in that timeframe, he sought help from someone else. After one day, he received a notification from that person who informed him that he had managed to finish the assignment and sent it to the employee as a test. However, the person also sent a message to the employee stating that if he wanted the completed assignment, he would have to pay $160.
>
> The helper's demand for payment revealed that he was actually a threat actor. The company's digital forensics team was called in to investigate and identify the attacker, determine the extent of the attack, and assess potential data breaches. The team must analyze the employee's computer and communication logs to prevent similar attacks in the future.

## Tools
* volatility2
* FTK
* Timeline Explorer
* Wireshark
* Registry Explorer

## 前提
這一題有分兩個裝置，一個是Desktop，另外一個是server，也分別對這兩個進行FTK packet和export memory，所以在分析的時候要特別注意，以下問題的順序會在這兩個裝置之間切換
## ==Q1==
> What’s the Operating System version of the Server? (two words) 
### Recon
這一題是針對server，所以可以直接用volatility對server memory進行分析，或者是直接用FTK對register進行稽核
起手式
```bash
$ ./volatility_2.6_win64_standalone.exe -f citadeldc01.mem imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win8SP0x64, Win81U1x64, Win2012R2x64_18340, Win2012R2x64, Win2012x64, Win8SP1x64_18340, Win8SP1x64 (Instantiated with Win8SP1x64)
                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
                     AS Layer2 : FileAddressSpace (D:\NTU\CTF\CyberDefenders\Szechuan Sauce\citadeldc01.mem)
                      PAE type : No PAE
                           DTB : 0x1a7000L
                          KDBG : 0xf800cba9ba20L
          Number of Processors : 2
     Image Type (Service Pack) : 0
                KPCR for CPU 0 : 0xfffff800cbaea000L
                KPCR for CPU 1 : 0xffffd0019fd55000L
             KUSER_SHARED_DATA : 0xfffff78000000000L
           Image date and time : 2020-09-19 04:39:59 UTC+0000
     Image local date and time : 2020-09-18 21:39:59 -0700
```

:::spoiler Flag
Flag: `2012 R2`
:::
## ==Q2==
> What’s the Operating System of the Desktop? (four words separated by spaces) 
### Recon
這一題可以參考[Hunter - Part 1 - Q5](https://hackmd.io/@SBK6401/By1BpZIf6#Q5)，我可以直接把Software的registry export出來，然後用registry explorer查看`/root/Microsoft/Windows NT/CurrentVersion`就會知道==Desktop==的OS
### Exploit
![圖片.png](https://hackmd.io/_uploads/SJlmnxMmT.png)

:::spoiler Flag
Flag: `Windows 10 Enterprise Evaluation`
:::
## ==Q3==
> What was the IP address assigned to the domain controller? 
### Recon
可以參考[Hunter - Part 1 - Q2](https://hackmd.io/@SBK6401/By1BpZIf6#Q2)
### Exploit
就是察看Server的SYSTEM中，`ControlSet001/Services/Tcpip/Parameters/Interfaces/`
![圖片.png](https://hackmd.io/_uploads/rkCmT0Xma.png)

:::spoiler Flag
Flag: `10.42.85.10`
:::
## ==Q4==
> What was the timezone of the Server? 
### Recon
可以先參考[Hunter Part 1 - Q6](https://hackmd.io/@SBK6401/By1BpZIf6#Q6)
### Exploit
這一題很迷，先查看Server的SYSTEM的`ControlSet001/Control/TimeZoneInformation/`的TimeZoneKeyName是Pacific Standard Time，代表不是UTC-8就是UTC-7，但這兩個都不是答案，隨便try了以後再看hint發現，原來是Admin設定錯時區，要發現這一件事情真的很難，看了[^szechuan-sauce-wp]還是一知半解，不過我試著自己操作和解釋

1. 首先，根據hint的說明，可以知道domain controller的timezone和應該是和desktop不一樣所以才會有這樣的問題
    這件事情可以從NTP(Network Time Protocol)看到，這主要是用於同步時間的protocol，所以從這些封包中可以看到他的時間是無法同步的，由此可知時間的timezone可能有問題
    ![圖片.png](https://hackmd.io/_uploads/SJZGakVQ6.png)

    [What is NTP?](https://zh.wikipedia.org/zh-tw/%E7%B6%B2%E8%B7%AF%E6%99%82%E9%96%93%E5%8D%94%E5%AE%9A)
    > 網路時間協定（英語：Network Time Protocol，縮寫：NTP）是在資料網路潛伏時間可變的電腦系統之間通過封包交換進行時鐘同步的一個網路協定，位於OSI模型的應用層。自1985年以來，NTP是目前仍在使用的最古老的網際網路協定之一。NTP由德拉瓦大學的David L. Mills設計。 
2. 具體來說到底差多少呢?這個可以從Server的event log和封包的時間差換算，我的想法是先把sercurity event log 從server export出來，然後找到RDP的登入時間，再比對wireshark的封包比對相對的時間就可以知道正確差多少
    1. Event Log在`/root/Windows/System32/winevt/Logs/`中，轉換成csv檔後再用timeline explorer打開
        ```bash
        $ ./EvtxECmd.exe -f Security.evtx --csv output
        ```
    2. 找到一樣的封包和event紀錄
        ![圖片.png](https://hackmd.io/_uploads/Hk2QskEXp.png)
        可以看到event log的時間是`2020-09-19 03:21:48`，而封包的時間是`2020-09-19 02:21:47`，兩者大約差了一個小時，因為當時的月份是9月也就是還在夏令時間，所以正確的時間應該是UTC-7，也就是說封包的時間是UTC-7的結果，而server上的3點是快了一小時的結果，所以應該是UTC-6就是server上設定的時間

:::spoiler Flag
Flag: `UTC-6`
:::
## ==Q5==
> What was the initial entry vector (how did they get in)?. Provide protocol name. 
### Recon
從上一題就可以知道他是利用RDP連到domain controller

:::spoiler Flag
Flag: `RDP`
:::
## ==Q6==
> What was the malicious process used by the malware? (one word) 
### Recon
這一題提到malware馬上就要想到
1. 他怎麼傳送過去到受害主機$\to$wireshark$\to$Export Object
2. 如果他有跑起來，可不可以直接知道是哪一支檔案$\to$memory analysis$\to$volatility$\to$pslist
3. 如果可以dump出來就送到virustotal看
### Exploit
1. 首先我先用volatility看他執行process的狀況
    :::spoiler Result
    ```bash
    $ ./volatility_2.6_win64_standalone.exe -f citadeldc01.mem --profile Win2012R2x64 pslist
    Volatility Foundation Volatility Framework 2.6
    Offset(V)          Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                         Exit
    ------------------ -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
    0xffffe0005f273040 System                    4      0     98        0 ------      0 2020-09-19 01:22:38 UTC+0000

    0xffffe00060354900 smss.exe                204      4      2        0 ------      0 2020-09-19 01:22:38 UTC+0000

    0xffffe000602c2080 csrss.exe               324    316      8        0      0      0 2020-09-19 01:22:39 UTC+0000

    0xffffe000602cc900 wininit.exe             404    316      1        0      0      0 2020-09-19 01:22:40 UTC+0000

    0xffffe000602c1900 csrss.exe               412    396     10        0      1      0 2020-09-19 01:22:40 UTC+0000

    0xffffe00060c11080 services.exe            452    404      5        0      0      0 2020-09-19 01:22:40 UTC+0000

    0xffffe00060c0e080 lsass.exe               460    404     31        0      0      0 2020-09-19 01:22:40 UTC+0000

    0xffffe00060c2a080 winlogon.exe            492    396      4        0      1      0 2020-09-19 01:22:40 UTC+0000

    0xffffe00060c84900 svchost.exe             640    452      8        0      0      0 2020-09-19 01:22:40 UTC+0000

    0xffffe00060c9a700 svchost.exe             684    452      6        0      0      0 2020-09-19 01:22:40 UTC+0000

    0xffffe00060ca3900 svchost.exe             800    452     12        0      0      0 2020-09-19 01:22:40 UTC+0000

    0xffffe00060d09680 dwm.exe                 808    492      7        0      1      0 2020-09-19 01:22:40 UTC+0000

    0xffffe00060d1e080 svchost.exe             848    452     39        0      0      0 2020-09-19 01:22:41 UTC+0000

    0xffffe00060d5d500 svchost.exe             928    452     16        0      0      0 2020-09-19 01:22:41 UTC+0000

    0xffffe00060da2080 svchost.exe            1000    452     18        0      0      0 2020-09-19 01:22:41 UTC+0000

    0xffffe00060e09900 svchost.exe             668    452     16        0      0      0 2020-09-19 01:22:41 UTC+0000

    0xffffe00060f73900 Microsoft.Acti         1292    452      9        0      0      0 2020-09-19 01:22:57 UTC+0000

    0xffffe00060fe1900 dfsrs.exe              1332    452     16        0      0      0 2020-09-19 01:22:57 UTC+0000

    0xffffe00060ff3080 dns.exe                1368    452     16        0      0      0 2020-09-19 01:22:57 UTC+0000

    0xffffe00060ff7900 ismserv.exe            1392    452      6        0      0      0 2020-09-19 01:22:57 UTC+0000

    0xffffe000614aa200 VGAuthService.         1556    452      2        0      0      0 2020-09-19 01:22:57 UTC+0000

    0xffffe00061a30900 vmtoolsd.exe           1600    452      9        0      0      0 2020-09-19 01:22:57 UTC+0000

    0xffffe00061a9a800 wlms.exe               1644    452      2        0      0      0 2020-09-19 01:22:57 UTC+0000

    0xffffe00061a9b2c0 dfssvc.exe             1660    452     11        0      0      0 2020-09-19 01:22:57 UTC+0000

    0xffffe0006291b7c0 svchost.exe            1956    452     30        0      0      0 2020-09-19 01:23:20 UTC+0000

    0xffffe000629b3080 vds.exe                 796    452     11        0      0      0 2020-09-19 01:23:20 UTC+0000

    0xffffe000629926c0 svchost.exe            1236    452      8        0      0      0 2020-09-19 01:23:21 UTC+0000

    0xffffe000629de900 WmiPrvSE.exe           2056    640     11        0      0      0 2020-09-19 01:23:21 UTC+0000

    0xffffe00062a26900 dllhost.exe            2216    452     10        0      0      0 2020-09-19 01:23:21 UTC+0000

    0xffffe00062a2a900 msdtc.exe              2460    452      9        0      0      0 2020-09-19 01:23:21 UTC+0000

    0xffffe000631cb900 spoolsv.exe            3724    452     13        0      0      0 2020-09-19 03:29:40 UTC+0000

    0xffffe00062fe7700 coreupdater.ex         3644   2244      0 --------      2      0 2020-09-19 03:56:37 UTC+0000   2020-09-19 03:56:52 UTC+0000
    0xffffe00062f04900 taskhostex.exe         3796    848      7        0      1      0 2020-09-19 04:36:03 UTC+0000

    0xffffe00063171900 explorer.exe           3472   3960     39        0      1      0 2020-09-19 04:36:03 UTC+0000

    0xffffe00060ce2080 ServerManager.          400   1904     10        0      1      0 2020-09-19 04:36:03 UTC+0000

    0xffffe00063299280 vm3dservice.ex         3260   3472      1        0      1      0 2020-09-19 04:36:14 UTC+0000

    0xffffe00062ede1c0 vmtoolsd.exe           2608   3472      8        0      1      0 2020-09-19 04:36:14 UTC+0000

    0xffffe00063021900 FTK Imager.exe         2840   3472      9        0      1      0 2020-09-19 04:37:04 UTC+0000

    0xffffe0006313f900 WMIADAP.exe            3056    848      5        0      0      0 2020-09-19 04:37:42 UTC+0000

    0xffffe00062c0a900 WmiPrvSE.exe           2764    640      6        0      0      0 2020-09-19 04:37:42 UTC+0000
    ```
    :::
    當然有幾個我是有一點懷疑，例如`WmiPrvSE.exe`, `WMIADAP.exe`, `spoolsv.exe`等等，不過查了一下應該都是windows裡面內建的正常程序，不過也不能掉以輕心，可能是被駭客換過只是名字一樣，不過有一個process令人擔心，就是==coreupdater.exe==，因為查資料的時候無意間看到[這個網站](https://www.hybrid-analysis.com/sample/10f3b92002bb98467334161cf85d0b1730851f9256f83c27db125e9a0c1cfda6/5f7695f4a553eb21aa0cdfe1#mitre-matrix-modal)，裡面有提到詳細這支程式的攻擊手法和IP位置，因此感覺不是巧合，先dump出來再說
2. 我是用volatility procdump，但是遇到一些問題導致dump不出來，可能是和paging有關係，導致PEB結構parse不出來
    ```bash
    $ ./volatility_2.6_win64_standalone.exe -f citadeldc01.mem --profile Win2012R2x64 procdump -p 3644 --dump-dir="Export Files/Server"
    Volatility Foundation Volatility Framework 2.6
    Process(V)         ImageBase          Name                 Result
    ------------------ ------------------ -------------------- ------
    0xffffe00062fe7700 ------------------ coreupdater.ex       Error: PEB at 0x7ff5ffffe000 is unavailable (possibly due to paging)
    ```
    這邊有簡單說明甚麼是PEB[ [edu-ctf 2023] week06 - rev2 ](https://www.youtube.com/live/uc230kDnd1A?si=aswYxVbqKIykjuRk&t=7457)
3. 所以我們就要想有甚麼其他方法可以把這個file export出來，可以從他怎麼傳進server開始切入，如果從wireshark的export file可以dump出來
    ![圖片.png](https://hackmd.io/_uploads/rydC5lVmT.png)
4. 丟到virustotal果然很有問題
    [完整分析結果](https://www.virustotal.com/gui/file/10f3b92002bb98467334161cf85d0b1730851f9256f83c27db125e9a0c1cfda6)
    ![圖片.png](https://hackmd.io/_uploads/B15zigE7T.png)

:::spoiler Flag
Flag: `coreupdater`
:::
## ==Q7==
> Which process did malware migrate to after the initial compromise? (one word) 
### Recon
這一題的直覺是利用volatility的malfind看有沒有利用coreupdater去inject哪一些process
### Exploit
從結果可以看到有幾個process有問題: 
`Process: Microsoft.Acti Pid: 1292 Address: 0x10500120000`
`Process: svchost.exe Pid: 1236 Address: 0x1b10ee0000`
`Process: spoolsv.exe Pid: 3724 Address: 0x4afbf20000`
`Process: explorer.exe Pid: 3472 Address: 0x5770000`
`Process: ServerManager. Pid: 400 Address: 0x5dc9ce0000`

:::spoiler Result
```bash
$ ./volatility_2.6_win64_standalone.exe -f citadeldc01.mem --profile Win2012R2x64 malfind
Volatility Foundation Volatility Framework 2.6
Process: Microsoft.Acti Pid: 1292 Address: 0x10500120000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: PrivateMemory: 1, Protection: 6

0x10500120000  00 00 00 00 00 00 00 00 b4 26 f3 1c 40 13 00 01   .........&..@...
0x10500120010  ee ff ee ff 02 00 00 00 20 01 12 00 05 01 00 00   ................
0x10500120020  20 01 12 00 05 01 00 00 00 00 12 00 05 01 00 00   ................
0x10500120030  00 00 12 00 05 01 00 00 0f 00 00 00 00 00 00 00   ................

0x00120000 0000             ADD [EAX], AL
0x00120002 0000             ADD [EAX], AL
0x00120004 0000             ADD [EAX], AL
0x00120006 0000             ADD [EAX], AL
0x00120008 b426             MOV AH, 0x26
0x0012000a f31c40           SBB AL, 0x40
0x0012000d 1300             ADC EAX, [EAX]
0x0012000f 01ee             ADD ESI, EBP
0x00120011 ff               DB 0xff
0x00120012 ee               OUT DX, AL
0x00120013 ff02             INC DWORD [EDX]
0x00120015 0000             ADD [EAX], AL
0x00120017 0020             ADD [EAX], AH
0x00120019 0112             ADD [EDX], EDX
0x0012001b 000501000020     ADD [0x20000001], AL
0x00120021 0112             ADD [EDX], EDX
0x00120023 000501000000     ADD [0x1], AL
0x00120029 0012             ADD [EDX], DL
0x0012002b 000501000000     ADD [0x1], AL
0x00120031 0012             ADD [EDX], DL
0x00120033 00050100000f     ADD [0xf000001], AL
0x00120039 0000             ADD [EAX], AL
0x0012003b 0000             ADD [EAX], AL
0x0012003d 0000             ADD [EAX], AL
0x0012003f 00               DB 0x0

Process: Microsoft.Acti Pid: 1292 Address: 0x10500100000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: PrivateMemory: 1, Protection: 6

0x10500100000  00 00 00 00 00 00 00 00 08 00 10 00 05 01 00 00   ................
0x10500100010  08 00 10 00 05 01 00 00 00 00 12 00 05 01 00 00   ................
0x10500100020  20 0d 10 00 05 01 00 00 00 10 10 00 05 01 00 00   ................
0x10500100030  00 d0 10 00 05 01 00 00 00 00 00 00 00 00 00 00   ................

0x00100000 0000             ADD [EAX], AL
0x00100002 0000             ADD [EAX], AL
0x00100004 0000             ADD [EAX], AL
0x00100006 0000             ADD [EAX], AL
0x00100008 0800             OR [EAX], AL
0x0010000a 1000             ADC [EAX], AL
0x0010000c 0501000008       ADD EAX, 0x8000001
0x00100011 0010             ADD [EAX], DL
0x00100013 000501000000     ADD [0x1], AL
0x00100019 0012             ADD [EDX], DL
0x0010001b 000501000020     ADD [0x20000001], AL
0x00100021 0d10000501       OR EAX, 0x1050010
0x00100026 0000             ADD [EAX], AL
0x00100028 0010             ADD [EAX], DL
0x0010002a 1000             ADC [EAX], AL
0x0010002c 0501000000       ADD EAX, 0x1
0x00100031 d010             RCL BYTE [EAX], 0x1
0x00100033 000501000000     ADD [0x1], AL
0x00100039 0000             ADD [EAX], AL
0x0010003b 0000             ADD [EAX], AL
0x0010003d 0000             ADD [EAX], AL
0x0010003f 00               DB 0x0

Process: Microsoft.Acti Pid: 1292 Address: 0x105001f0000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: PrivateMemory: 1, Protection: 6

0x105001f0000  00 00 00 00 00 00 00 00 5c 67 95 04 1e 40 00 01   ........\g...@..
0x105001f0010  ee ff ee ff 02 00 00 00 20 01 1f 00 05 01 00 00   ................
0x105001f0020  20 01 1f 00 05 01 00 00 00 00 1f 00 05 01 00 00   ................
0x105001f0030  00 00 1f 00 05 01 00 00 0f 00 00 00 00 00 00 00   ................

0x001f0000 0000             ADD [EAX], AL
0x001f0002 0000             ADD [EAX], AL
0x001f0004 0000             ADD [EAX], AL
0x001f0006 0000             ADD [EAX], AL
0x001f0008 5c               POP ESP
0x001f0009 6795             XCHG EBP, EAX
0x001f000b 041e             ADD AL, 0x1e
0x001f000d 40               INC EAX
0x001f000e 0001             ADD [ECX], AL
0x001f0010 ee               OUT DX, AL
0x001f0011 ff               DB 0xff
0x001f0012 ee               OUT DX, AL
0x001f0013 ff02             INC DWORD [EDX]
0x001f0015 0000             ADD [EAX], AL
0x001f0017 0020             ADD [EAX], AH
0x001f0019 011f             ADD [EDI], EBX
0x001f001b 000501000020     ADD [0x20000001], AL
0x001f0021 011f             ADD [EDI], EBX
0x001f0023 000501000000     ADD [0x1], AL
0x001f0029 001f             ADD [EDI], BL
0x001f002b 000501000000     ADD [0x1], AL
0x001f0031 001f             ADD [EDI], BL
0x001f0033 00050100000f     ADD [0xf000001], AL
0x001f0039 0000             ADD [EAX], AL
0x001f003b 0000             ADD [EAX], AL
0x001f003d 0000             ADD [EAX], AL
0x001f003f 00               DB 0x0

Process: Microsoft.Acti Pid: 1292 Address: 0x7ff5ff8d0000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: PrivateMemory: 1, Protection: 6

0x7ff5ff8d0000  00 00 00 00 00 00 00 00 78 0d 00 00 00 00 00 00   ........x.......
0x7ff5ff8d0010  0c 00 00 00 49 c7 c2 00 00 00 00 48 b8 f0 e4 4f   ....I......H...O
0x7ff5ff8d0020  d6 ff 7f 00 00 ff e0 49 c7 c2 01 00 00 00 48 b8   .......I......H.
0x7ff5ff8d0030  f0 e4 4f d6 ff 7f 00 00 ff e0 49 c7 c2 02 00 00   ..O.......I.....

0xff8d0000 0000             ADD [EAX], AL
0xff8d0002 0000             ADD [EAX], AL
0xff8d0004 0000             ADD [EAX], AL
0xff8d0006 0000             ADD [EAX], AL
0xff8d0008 780d             JS 0xff8d0017
0xff8d000a 0000             ADD [EAX], AL
0xff8d000c 0000             ADD [EAX], AL
0xff8d000e 0000             ADD [EAX], AL
0xff8d0010 0c00             OR AL, 0x0
0xff8d0012 0000             ADD [EAX], AL
0xff8d0014 49               DEC ECX
0xff8d0015 c7               DB 0xc7
0xff8d0016 c20000           RET 0x0
0xff8d0019 0000             ADD [EAX], AL
0xff8d001b 48               DEC EAX
0xff8d001c b8f0e44fd6       MOV EAX, 0xd64fe4f0
0xff8d0021 ff               DB 0xff
0xff8d0022 7f00             JG 0xff8d0024
0xff8d0024 00ff             ADD BH, BH
0xff8d0026 e049             LOOPNZ 0xff8d0071
0xff8d0028 c7               DB 0xc7
0xff8d0029 c20100           RET 0x1
0xff8d002c 0000             ADD [EAX], AL
0xff8d002e 48               DEC EAX
0xff8d002f b8f0e44fd6       MOV EAX, 0xd64fe4f0
0xff8d0034 ff               DB 0xff
0xff8d0035 7f00             JG 0xff8d0037
0xff8d0037 00ff             ADD BH, BH
0xff8d0039 e049             LOOPNZ 0xff8d0084
0xff8d003b c7               DB 0xc7
0xff8d003c c20200           RET 0x2
0xff8d003f 00               DB 0x0

Process: Microsoft.Acti Pid: 1292 Address: 0x7ff5ff8e0000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: PrivateMemory: 1, Protection: 6

0x7ff5ff8e0000  d8 ff ff ff ff ff ff ff 08 00 00 00 00 00 00 00   ................
0x7ff5ff8e0010  01 00 00 00 00 00 00 00 00 02 0e 03 38 00 00 00   ............8...
0x7ff5ff8e0020  68 41 95 09 0c 00 00 00 b8 11 49 d5 ff 7f 00 00   hA........I.....
0x7ff5ff8e0030  00 10 e2 d4 ff 7f 00 00 f0 e0 ec d4 ff 7f 00 00   ................

0xff8e0000 d8ff             FDIVR ST0, ST7
0xff8e0002 ff               DB 0xff
0xff8e0003 ff               DB 0xff
0xff8e0004 ff               DB 0xff
0xff8e0005 ff               DB 0xff
0xff8e0006 ff               DB 0xff
0xff8e0007 ff08             DEC DWORD [EAX]
0xff8e0009 0000             ADD [EAX], AL
0xff8e000b 0000             ADD [EAX], AL
0xff8e000d 0000             ADD [EAX], AL
0xff8e000f 0001             ADD [ECX], AL
0xff8e0011 0000             ADD [EAX], AL
0xff8e0013 0000             ADD [EAX], AL
0xff8e0015 0000             ADD [EAX], AL
0xff8e0017 0000             ADD [EAX], AL
0xff8e0019 020e             ADD CL, [ESI]
0xff8e001b 0338             ADD EDI, [EAX]
0xff8e001d 0000             ADD [EAX], AL
0xff8e001f 006841           ADD [EAX+0x41], CH
0xff8e0022 95               XCHG EBP, EAX
0xff8e0023 090c00           OR [EAX+EAX], ECX
0xff8e0026 0000             ADD [EAX], AL
0xff8e0028 b81149d5ff       MOV EAX, 0xffd54911
0xff8e002d 7f00             JG 0xff8e002f
0xff8e002f 0000             ADD [EAX], AL
0xff8e0031 10e2             ADC DL, AH
0xff8e0033 d4ff             AAM 0xff
0xff8e0035 7f00             JG 0xff8e0037
0xff8e0037 00f0             ADD AL, DH
0xff8e0039 e0ec             LOOPNZ 0xff8e0027
0xff8e003b d4ff             AAM 0xff
0xff8e003d 7f00             JG 0xff8e003f
0xff8e003f 00               DB 0x0

Process: svchost.exe Pid: 1236 Address: 0x1b10ee0000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: PrivateMemory: 1, Protection: 6

0x1b10ee0000  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x1b10ee0010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x1b10ee0020  00 00 ee 10 1b 00 00 00 00 00 00 00 00 00 00 00   ................
0x1b10ee0030  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................

0x10ee0000 0000             ADD [EAX], AL
0x10ee0002 0000             ADD [EAX], AL
0x10ee0004 0000             ADD [EAX], AL
0x10ee0006 0000             ADD [EAX], AL
0x10ee0008 0000             ADD [EAX], AL
0x10ee000a 0000             ADD [EAX], AL
0x10ee000c 0000             ADD [EAX], AL
0x10ee000e 0000             ADD [EAX], AL
0x10ee0010 0000             ADD [EAX], AL
0x10ee0012 0000             ADD [EAX], AL
0x10ee0014 0000             ADD [EAX], AL
0x10ee0016 0000             ADD [EAX], AL
0x10ee0018 0000             ADD [EAX], AL
0x10ee001a 0000             ADD [EAX], AL
0x10ee001c 0000             ADD [EAX], AL
0x10ee001e 0000             ADD [EAX], AL
0x10ee0020 0000             ADD [EAX], AL
0x10ee0022 ee               OUT DX, AL
0x10ee0023 101b             ADC [EBX], BL
0x10ee0025 0000             ADD [EAX], AL
0x10ee0027 0000             ADD [EAX], AL
0x10ee0029 0000             ADD [EAX], AL
0x10ee002b 0000             ADD [EAX], AL
0x10ee002d 0000             ADD [EAX], AL
0x10ee002f 0000             ADD [EAX], AL
0x10ee0031 0000             ADD [EAX], AL
0x10ee0033 0000             ADD [EAX], AL
0x10ee0035 0000             ADD [EAX], AL
0x10ee0037 0000             ADD [EAX], AL
0x10ee0039 0000             ADD [EAX], AL
0x10ee003b 0000             ADD [EAX], AL
0x10ee003d 0000             ADD [EAX], AL
0x10ee003f 00               DB 0x0

Process: spoolsv.exe Pid: 3724 Address: 0x4afbf20000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: PrivateMemory: 1, Protection: 6

0x4afbf20000  fc 48 89 ce 48 81 ec 00 20 00 00 48 83 e4 f0 e8   .H..H......H....
0x4afbf20010  cc 00 00 00 41 51 41 50 52 51 56 48 31 d2 65 48   ....AQAPRQVH1.eH
0x4afbf20020  8b 52 60 48 8b 52 18 48 8b 52 20 48 8b 72 50 48   .R`H.R.H.R.H.rPH
0x4afbf20030  0f b7 4a 4a 4d 31 c9 48 31 c0 ac 3c 61 7c 02 2c   ..JJM1.H1..<a|.,

0xfbf20000 fc               CLD
0xfbf20001 48               DEC EAX
0xfbf20002 89ce             MOV ESI, ECX
0xfbf20004 48               DEC EAX
0xfbf20005 81ec00200000     SUB ESP, 0x2000
0xfbf2000b 48               DEC EAX
0xfbf2000c 83e4f0           AND ESP, -0x10
0xfbf2000f e8cc000000       CALL 0xfbf200e0
0xfbf20014 41               INC ECX
0xfbf20015 51               PUSH ECX
0xfbf20016 41               INC ECX
0xfbf20017 50               PUSH EAX
0xfbf20018 52               PUSH EDX
0xfbf20019 51               PUSH ECX
0xfbf2001a 56               PUSH ESI
0xfbf2001b 48               DEC EAX
0xfbf2001c 31d2             XOR EDX, EDX
0xfbf2001e 6548             DEC EAX
0xfbf20020 8b5260           MOV EDX, [EDX+0x60]
0xfbf20023 48               DEC EAX
0xfbf20024 8b5218           MOV EDX, [EDX+0x18]
0xfbf20027 48               DEC EAX
0xfbf20028 8b5220           MOV EDX, [EDX+0x20]
0xfbf2002b 48               DEC EAX
0xfbf2002c 8b7250           MOV ESI, [EDX+0x50]
0xfbf2002f 48               DEC EAX
0xfbf20030 0fb74a4a         MOVZX ECX, WORD [EDX+0x4a]
0xfbf20034 4d               DEC EBP
0xfbf20035 31c9             XOR ECX, ECX
0xfbf20037 48               DEC EAX
0xfbf20038 31c0             XOR EAX, EAX
0xfbf2003a ac               LODSB
0xfbf2003b 3c61             CMP AL, 0x61
0xfbf2003d 7c02             JL 0xfbf20041
0xfbf2003f 2c               DB 0x2c

Process: spoolsv.exe Pid: 3724 Address: 0x4afc1f0000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: PrivateMemory: 1, Protection: 6

0x4afc1f0000  4d 5a 90 00 03 00 00 00 04 00 00 00 ff ff 00 00   MZ..............
0x4afc1f0010  b8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00   ........@.......
0x4afc1f0020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x4afc1f0030  00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00   ................

0xfc1f0000 4d               DEC EBP
0xfc1f0001 5a               POP EDX
0xfc1f0002 90               NOP
0xfc1f0003 0003             ADD [EBX], AL
0xfc1f0005 0000             ADD [EAX], AL
0xfc1f0007 000400           ADD [EAX+EAX], AL
0xfc1f000a 0000             ADD [EAX], AL
0xfc1f000c ff               DB 0xff
0xfc1f000d ff00             INC DWORD [EAX]
0xfc1f000f 00b800000000     ADD [EAX+0x0], BH
0xfc1f0015 0000             ADD [EAX], AL
0xfc1f0017 004000           ADD [EAX+0x0], AL
0xfc1f001a 0000             ADD [EAX], AL
0xfc1f001c 0000             ADD [EAX], AL
0xfc1f001e 0000             ADD [EAX], AL
0xfc1f0020 0000             ADD [EAX], AL
0xfc1f0022 0000             ADD [EAX], AL
0xfc1f0024 0000             ADD [EAX], AL
0xfc1f0026 0000             ADD [EAX], AL
0xfc1f0028 0000             ADD [EAX], AL
0xfc1f002a 0000             ADD [EAX], AL
0xfc1f002c 0000             ADD [EAX], AL
0xfc1f002e 0000             ADD [EAX], AL
0xfc1f0030 0000             ADD [EAX], AL
0xfc1f0032 0000             ADD [EAX], AL
0xfc1f0034 0000             ADD [EAX], AL
0xfc1f0036 0000             ADD [EAX], AL
0xfc1f0038 0000             ADD [EAX], AL
0xfc1f003a 0000             ADD [EAX], AL
0xfc1f003c 0001             ADD [ECX], AL
0xfc1f003e 0000             ADD [EAX], AL

Process: spoolsv.exe Pid: 3724 Address: 0x4afc070000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: PrivateMemory: 1, Protection: 6

0x4afc070000  4d 5a 41 52 55 48 89 e5 48 83 ec 20 48 83 e4 f0   MZARUH..H...H...
0x4afc070010  e8 00 00 00 00 5b 48 81 c3 b7 57 00 00 ff d3 48   .....[H...W....H
0x4afc070020  81 c3 34 b6 02 00 48 89 3b 49 89 d8 6a 04 5a ff   ..4...H.;I..j.Z.
0x4afc070030  d0 00 00 00 00 00 00 00 00 00 00 00 f0 00 00 00   ................

0xfc070000 4d               DEC EBP
0xfc070001 5a               POP EDX
0xfc070002 41               INC ECX
0xfc070003 52               PUSH EDX
0xfc070004 55               PUSH EBP
0xfc070005 48               DEC EAX
0xfc070006 89e5             MOV EBP, ESP
0xfc070008 48               DEC EAX
0xfc070009 83ec20           SUB ESP, 0x20
0xfc07000c 48               DEC EAX
0xfc07000d 83e4f0           AND ESP, -0x10
0xfc070010 e800000000       CALL 0xfc070015
0xfc070015 5b               POP EBX
0xfc070016 48               DEC EAX
0xfc070017 81c3b7570000     ADD EBX, 0x57b7
0xfc07001d ffd3             CALL EBX
0xfc07001f 48               DEC EAX
0xfc070020 81c334b60200     ADD EBX, 0x2b634
0xfc070026 48               DEC EAX
0xfc070027 893b             MOV [EBX], EDI
0xfc070029 49               DEC ECX
0xfc07002a 89d8             MOV EAX, EBX
0xfc07002c 6a04             PUSH 0x4
0xfc07002e 5a               POP EDX
0xfc07002f ffd0             CALL EAX
0xfc070031 0000             ADD [EAX], AL
0xfc070033 0000             ADD [EAX], AL
0xfc070035 0000             ADD [EAX], AL
0xfc070037 0000             ADD [EAX], AL
0xfc070039 0000             ADD [EAX], AL
0xfc07003b 00f0             ADD AL, DH
0xfc07003d 0000             ADD [EAX], AL
0xfc07003f 00               DB 0x0

Process: spoolsv.exe Pid: 3724 Address: 0x4afc260000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: PrivateMemory: 1, Protection: 6

0x4afc260000  4d 5a 90 00 03 00 00 00 04 00 00 00 ff ff 00 00   MZ..............
0x4afc260010  b8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00   ........@.......
0x4afc260020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x4afc260030  00 00 00 00 00 00 00 00 00 00 00 00 e0 00 00 00   ................

0xfc260000 4d               DEC EBP
0xfc260001 5a               POP EDX
0xfc260002 90               NOP
0xfc260003 0003             ADD [EBX], AL
0xfc260005 0000             ADD [EAX], AL
0xfc260007 000400           ADD [EAX+EAX], AL
0xfc26000a 0000             ADD [EAX], AL
0xfc26000c ff               DB 0xff
0xfc26000d ff00             INC DWORD [EAX]
0xfc26000f 00b800000000     ADD [EAX+0x0], BH
0xfc260015 0000             ADD [EAX], AL
0xfc260017 004000           ADD [EAX+0x0], AL
0xfc26001a 0000             ADD [EAX], AL
0xfc26001c 0000             ADD [EAX], AL
0xfc26001e 0000             ADD [EAX], AL
0xfc260020 0000             ADD [EAX], AL
0xfc260022 0000             ADD [EAX], AL
0xfc260024 0000             ADD [EAX], AL
0xfc260026 0000             ADD [EAX], AL
0xfc260028 0000             ADD [EAX], AL
0xfc26002a 0000             ADD [EAX], AL
0xfc26002c 0000             ADD [EAX], AL
0xfc26002e 0000             ADD [EAX], AL
0xfc260030 0000             ADD [EAX], AL
0xfc260032 0000             ADD [EAX], AL
0xfc260034 0000             ADD [EAX], AL
0xfc260036 0000             ADD [EAX], AL
0xfc260038 0000             ADD [EAX], AL
0xfc26003a 0000             ADD [EAX], AL
0xfc26003c e000             LOOPNZ 0xfc26003e
0xfc26003e 0000             ADD [EAX], AL

Process: explorer.exe Pid: 3472 Address: 0x5770000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: PrivateMemory: 1, Protection: 6

0x05770000  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x05770010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x05770020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x05770030  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................

0x05770000 0000             ADD [EAX], AL
0x05770002 0000             ADD [EAX], AL
0x05770004 0000             ADD [EAX], AL
0x05770006 0000             ADD [EAX], AL
0x05770008 0000             ADD [EAX], AL
0x0577000a 0000             ADD [EAX], AL
0x0577000c 0000             ADD [EAX], AL
0x0577000e 0000             ADD [EAX], AL
0x05770010 0000             ADD [EAX], AL
0x05770012 0000             ADD [EAX], AL
0x05770014 0000             ADD [EAX], AL
0x05770016 0000             ADD [EAX], AL
0x05770018 0000             ADD [EAX], AL
0x0577001a 0000             ADD [EAX], AL
0x0577001c 0000             ADD [EAX], AL
0x0577001e 0000             ADD [EAX], AL
0x05770020 0000             ADD [EAX], AL
0x05770022 0000             ADD [EAX], AL
0x05770024 0000             ADD [EAX], AL
0x05770026 0000             ADD [EAX], AL
0x05770028 0000             ADD [EAX], AL
0x0577002a 0000             ADD [EAX], AL
0x0577002c 0000             ADD [EAX], AL
0x0577002e 0000             ADD [EAX], AL
0x05770030 0000             ADD [EAX], AL
0x05770032 0000             ADD [EAX], AL
0x05770034 0000             ADD [EAX], AL
0x05770036 0000             ADD [EAX], AL
0x05770038 0000             ADD [EAX], AL
0x0577003a 0000             ADD [EAX], AL
0x0577003c 0000             ADD [EAX], AL
0x0577003e 0000             ADD [EAX], AL

Process: explorer.exe Pid: 3472 Address: 0xd840000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: PrivateMemory: 1, Protection: 6

0x0d840000  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x0d840010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x0d840020  00 00 84 0d 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x0d840030  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................

0x0d840000 0000             ADD [EAX], AL
0x0d840002 0000             ADD [EAX], AL
0x0d840004 0000             ADD [EAX], AL
0x0d840006 0000             ADD [EAX], AL
0x0d840008 0000             ADD [EAX], AL
0x0d84000a 0000             ADD [EAX], AL
0x0d84000c 0000             ADD [EAX], AL
0x0d84000e 0000             ADD [EAX], AL
0x0d840010 0000             ADD [EAX], AL
0x0d840012 0000             ADD [EAX], AL
0x0d840014 0000             ADD [EAX], AL
0x0d840016 0000             ADD [EAX], AL
0x0d840018 0000             ADD [EAX], AL
0x0d84001a 0000             ADD [EAX], AL
0x0d84001c 0000             ADD [EAX], AL
0x0d84001e 0000             ADD [EAX], AL
0x0d840020 0000             ADD [EAX], AL
0x0d840022 840d00000000     TEST [0x0], CL
0x0d840028 0000             ADD [EAX], AL
0x0d84002a 0000             ADD [EAX], AL
0x0d84002c 0000             ADD [EAX], AL
0x0d84002e 0000             ADD [EAX], AL
0x0d840030 0000             ADD [EAX], AL
0x0d840032 0000             ADD [EAX], AL
0x0d840034 0000             ADD [EAX], AL
0x0d840036 0000             ADD [EAX], AL
0x0d840038 0000             ADD [EAX], AL
0x0d84003a 0000             ADD [EAX], AL
0x0d84003c 0000             ADD [EAX], AL
0x0d84003e 0000             ADD [EAX], AL

Process: ServerManager. Pid: 400 Address: 0x5dc9ce0000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: PrivateMemory: 1, Protection: 6

0x5dc9ce0000  00 00 00 00 00 00 00 00 0a e5 1b 68 63 23 00 01   ...........hc#..
0x5dc9ce0010  ee ff ee ff 02 00 00 00 20 01 ce c9 5d 00 00 00   ............]...
0x5dc9ce0020  20 01 ce c9 5d 00 00 00 00 00 ce c9 5d 00 00 00   ....].......]...
0x5dc9ce0030  00 00 ce c9 5d 00 00 00 0f 00 00 00 00 00 00 00   ....]...........

0xc9ce0000 0000             ADD [EAX], AL
0xc9ce0002 0000             ADD [EAX], AL
0xc9ce0004 0000             ADD [EAX], AL
0xc9ce0006 0000             ADD [EAX], AL
0xc9ce0008 0ae5             OR AH, CH
0xc9ce000a 1b6863           SBB EBP, [EAX+0x63]
0xc9ce000d 2300             AND EAX, [EAX]
0xc9ce000f 01ee             ADD ESI, EBP
0xc9ce0011 ff               DB 0xff
0xc9ce0012 ee               OUT DX, AL
0xc9ce0013 ff02             INC DWORD [EDX]
0xc9ce0015 0000             ADD [EAX], AL
0xc9ce0017 0020             ADD [EAX], AH
0xc9ce0019 01ce             ADD ESI, ECX
0xc9ce001b c9               LEAVE
0xc9ce001c 5d               POP EBP
0xc9ce001d 0000             ADD [EAX], AL
0xc9ce001f 0020             ADD [EAX], AH
0xc9ce0021 01ce             ADD ESI, ECX
0xc9ce0023 c9               LEAVE
0xc9ce0024 5d               POP EBP
0xc9ce0025 0000             ADD [EAX], AL
0xc9ce0027 0000             ADD [EAX], AL
0xc9ce0029 00ce             ADD DH, CL
0xc9ce002b c9               LEAVE
0xc9ce002c 5d               POP EBP
0xc9ce002d 0000             ADD [EAX], AL
0xc9ce002f 0000             ADD [EAX], AL
0xc9ce0031 00ce             ADD DH, CL
0xc9ce0033 c9               LEAVE
0xc9ce0034 5d               POP EBP
0xc9ce0035 0000             ADD [EAX], AL
0xc9ce0037 000f             ADD [EDI], CL
0xc9ce0039 0000             ADD [EAX], AL
0xc9ce003b 0000             ADD [EAX], AL
0xc9ce003d 0000             ADD [EAX], AL
0xc9ce003f 00               DB 0x0

Process: ServerManager. Pid: 400 Address: 0x5dc9cb0000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: PrivateMemory: 1, Protection: 6

0x5dc9cb0000  00 00 00 00 00 00 00 00 90 44 ce c9 5d 00 00 00   .........D..]...
0x5dc9cb0010  90 44 ce c9 5d 00 00 00 00 00 ce c9 5d 00 00 00   .D..].......]...
0x5dc9cb0020  e0 0d cb c9 5d 00 00 00 00 10 cb c9 5d 00 00 00   ....].......]...
0x5dc9cb0030  00 d0 cb c9 5d 00 00 00 02 00 00 00 00 00 00 00   ....]...........

0xc9cb0000 0000             ADD [EAX], AL
0xc9cb0002 0000             ADD [EAX], AL
0xc9cb0004 0000             ADD [EAX], AL
0xc9cb0006 0000             ADD [EAX], AL
0xc9cb0008 90               NOP
0xc9cb0009 44               INC ESP
0xc9cb000a ce               INTO
0xc9cb000b c9               LEAVE
0xc9cb000c 5d               POP EBP
0xc9cb000d 0000             ADD [EAX], AL
0xc9cb000f 009044cec95d     ADD [EAX+0x5dc9ce44], DL
0xc9cb0015 0000             ADD [EAX], AL
0xc9cb0017 0000             ADD [EAX], AL
0xc9cb0019 00ce             ADD DH, CL
0xc9cb001b c9               LEAVE
0xc9cb001c 5d               POP EBP
0xc9cb001d 0000             ADD [EAX], AL
0xc9cb001f 00e0             ADD AL, AH
0xc9cb0021 0dcbc95d00       OR EAX, 0x5dc9cb
0xc9cb0026 0000             ADD [EAX], AL
0xc9cb0028 0010             ADD [EAX], DL
0xc9cb002a cb               RETF
0xc9cb002b c9               LEAVE
0xc9cb002c 5d               POP EBP
0xc9cb002d 0000             ADD [EAX], AL
0xc9cb002f 0000             ADD [EAX], AL
0xc9cb0031 d0cb             ROR BL, 0x1
0xc9cb0033 c9               LEAVE
0xc9cb0034 5d               POP EBP
0xc9cb0035 0000             ADD [EAX], AL
0xc9cb0037 0002             ADD [EDX], AL
0xc9cb0039 0000             ADD [EAX], AL
0xc9cb003b 0000             ADD [EAX], AL
0xc9cb003d 0000             ADD [EAX], AL
0xc9cb003f 00               DB 0x0

Process: ServerManager. Pid: 400 Address: 0x5dc9e70000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: PrivateMemory: 1, Protection: 6

0x5dc9e70000  b9 f4 ff f6 05 36 da 28 00 01 74 1c 48 8b 43 10   .....6.(..t.H.C.
0x5dc9e70010  48 8d 15 59 05 00 00 44 0f b6 48 60 44 8b 80 ec   H..Y...D..H`D...
0x5dc9e70020  00 00 00 e8 44 bf e0 ff 48 8b 4b 28 41 be 05 00   ....D...H.K(A...
0x5dc9e70030  00 00 41 8b d6 e8 16 d0 f4 ff 48 8b 43 08 41 8d   ..A.......H.C.A.

0xc9e70000 b9f4fff605       MOV ECX, 0x5f6fff4
0xc9e70005 36da28           FISUBR DWORD [SS:EAX]
0xc9e70008 0001             ADD [ECX], AL
0xc9e7000a 741c             JZ 0xc9e70028
0xc9e7000c 48               DEC EAX
0xc9e7000d 8b4310           MOV EAX, [EBX+0x10]
0xc9e70010 48               DEC EAX
0xc9e70011 8d1559050000     LEA EDX, [0x559]
0xc9e70017 44               INC ESP
0xc9e70018 0fb64860         MOVZX ECX, BYTE [EAX+0x60]
0xc9e7001c 44               INC ESP
0xc9e7001d 8b80ec000000     MOV EAX, [EAX+0xec]
0xc9e70023 e844bfe0ff       CALL 0xc9c7bf6c
0xc9e70028 48               DEC EAX
0xc9e70029 8b4b28           MOV ECX, [EBX+0x28]
0xc9e7002c 41               INC ECX
0xc9e7002d be05000000       MOV ESI, 0x5
0xc9e70032 41               INC ECX
0xc9e70033 8bd6             MOV EDX, ESI
0xc9e70035 e816d0f4ff       CALL 0xc9dbd050
0xc9e7003a 48               DEC EAX
0xc9e7003b 8b4308           MOV EAX, [EBX+0x8]
0xc9e7003e 41               INC ECX
0xc9e7003f 8d               DB 0x8d
```
:::

:::spoiler Flag
Flag: `spoolsv`
:::
## ==Q8==
> Identify the IP Address that delivered the payload. 
### Recon
直覺會想要volatility的netscan，但是結果實在是太多了，後來轉念一想直接看封包不就好了，所以我直接看原本傳送`coreupdater.exe`到server的IP
### Exploit
![圖片.png](https://hackmd.io/_uploads/Syh-4-4Qp.png)

:::spoiler Flag
Flag: `194.61.24.102`
:::
## ==Q9==
> What IP Address was the malware calling to? 
### Recon
直覺就是volatility netscan再grep
### Exploit
```bash
$ ./volatility_2.6_win64_standalone.exe -f citadeldc01.mem --profile Win2012R2x64 netscan | grep coreupdater
Volatility Foundation Volatility Framework 2.6
0x20fc7590         TCPv4    10.42.85.10:62613              203.78.103.109:443   ESTABLISHED      3644     coreupdater.ex
0x60182590         TCPv4    10.42.85.10:62613              203.78.103.109:443   ESTABLISHED      3644     coreupdater.ex
```

:::spoiler Flag
Flag: `203.78.103.109`
:::
## ==Q10==
> Where did the malware reside on the disk? 
### Recon
這一題直覺會在FTK上找，不過仔細想想可以直接volatility filescan再grep還比較快
### Exploit
```bash
$ ./volatility_2.6_win64_standalone.exe -f citadeldc01.mem --profile Win2012R2x64 filescan | grep coreupdater.exe
Volatility Foundation Volatility Framework 2.6
0x00000000130ddf20     16      0 RWD--- \Device\HarddiskVolume2\Windows\System32\coreupdater.exereupdater.exe.2424urv.partial
0x000000002082ff20      5      0 R--r-d \Device\HarddiskVolume2\Windows\System32\coreupdater.exereupdater.exe
0x0000000052317f20     16      0 RWD--- \Device\HarddiskVolume2\Windows\System32\coreupdater.exereupdater.exe.2424urv.partial
0x000000005faa4f20      5      0 R--r-d \Device\HarddiskVolume2\Windows\System32\coreupdater.exereupdater.exe
```

:::spoiler Flag
Flag: `C:\Windows\System32\coreupdater.exe`
:::
## Reference
[^szechuan-sauce-wp]:[CyberDefenders: Szechuan Sauce CTF Writeup](https://ellisstannard.medium.com/cyberdefenders-szechuan-sauce-writeup-ab172eb7666c)