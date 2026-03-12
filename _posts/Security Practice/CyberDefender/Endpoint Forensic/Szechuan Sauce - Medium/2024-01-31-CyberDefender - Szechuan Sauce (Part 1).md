---
title: CyberDefender - Szechuan Sauce (Part 1)
tags: [CyberDefender, Endpoint Forensics]

category: "Security Practice｜CyberDefender｜Endpoint Forensic｜Szechuan Sauce - Medium"
date: 2024-01-31
---

# CyberDefender - Szechuan Sauce (Part 1)
<!-- more -->
* Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/31
* [Part 2]({{base.url}}/CyberDefender-Szechuan-Sauce-(Part-2)/)

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

## Q1
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

Flag: `2012 R2`

## Q2
> What’s the Operating System of the Desktop? (four words separated by spaces) 

### Recon
這一題可以參考[Hunter - Part 1 - Q5]({{base.url}}/CyberDefender-Hunter-(Part-1)#Q5)，我可以直接把Software的registry export出來，然後用registry explorer查看`/root/Microsoft/Windows NT/CurrentVersion`就會知道Desktop的OS

### Exploit
![圖片.png](https://hackmd.io/_uploads/SJlmnxMmT.png)

Flag: `Windows 10 Enterprise Evaluation`

## Q3
> What was the IP address assigned to the domain controller? 

### Recon
可以參考[Hunter - Part 1 - Q2]({{base.url}}/CyberDefender-Hunter-(Part-1)#Q2)

### Exploit
就是察看Server的SYSTEM中，`ControlSet001/Services/Tcpip/Parameters/Interfaces/`
![圖片.png](https://hackmd.io/_uploads/rkCmT0Xma.png)

Flag: `10.42.85.10`

## Q4
> What was the timezone of the Server? 

### Recon
可以先參考[Hunter Part 1 - Q6]({{base.url}}/CyberDefender-Hunter-(Part-1)#Q6)

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

Flag: `UTC-6`

## Q5
> What was the initial entry vector (how did they get in)?. Provide protocol name. 

### Recon
從上一題就可以知道他是利用RDP連到domain controller

Flag: `RDP`

## Q6
> What was the malicious process used by the malware? (one word) 

### Recon
這一題提到malware馬上就要想到
1. 他怎麼傳送過去到受害主機 → wireshark → Export Object
2. 如果他有跑起來，可不可以直接知道是哪一支檔案 → memory analysis → volatility → pslist
3. 如果可以dump出來就送到virustotal看

### Exploit
1. 首先我先用volatility看他執行process的狀況
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
    當然有幾個我是有一點懷疑，例如`WmiPrvSE.exe`, `WMIADAP.exe`, `spoolsv.exe`等等，不過查了一下應該都是windows裡面內建的正常程序，不過也不能掉以輕心，可能是被駭客換過只是名字一樣，不過有一個process令人擔心，就是**coreupdater.exe**，因為查資料的時候無意間看到[這個網站](https://www.hybrid-analysis.com/sample/10f3b92002bb98467334161cf85d0b1730851f9256f83c27db125e9a0c1cfda6/5f7695f4a553eb21aa0cdfe1#mitre-matrix-modal)，裡面有提到詳細這支程式的攻擊手法和IP位置，因此感覺不是巧合，先dump出來再說
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

Flag: `coreupdater`

## Q7
> Which process did malware migrate to after the initial compromise? (one word) 

### Recon
這一題的直覺是利用volatility的malfind看有沒有利用coreupdater去inject哪一些process

### Exploit
從結果可以看到有幾個process有問題: 
```
Process: Microsoft.Acti Pid: 1292 Address: 0x10500120000
Process: svchost.exe Pid: 1236 Address: 0x1b10ee0000
Process: spoolsv.exe Pid: 3724 Address: 0x4afbf20000
Process: explorer.exe Pid: 3472 Address: 0x5770000
Process: ServerManager. Pid: 400 Address: 0x5dc9ce0000
```

```bash
$ ./volatility_2.6_win64_standalone.exe -f citadeldc01.mem --profile Win2012R2x64 malfind | findstr "Process: "
Volatility Foundation Volatility Framework 2.6
Process: Microsoft.Acti Pid: 1292 Address: 0x10500120000
Process: Microsoft.Acti Pid: 1292 Address: 0x10500100000
Process: Microsoft.Acti Pid: 1292 Address: 0x105001f0000
Process: Microsoft.Acti Pid: 1292 Address: 0x7ff5ff8d0000
Process: Microsoft.Acti Pid: 1292 Address: 0x7ff5ff8e0000
Process: svchost.exe Pid: 1236 Address: 0x1b10ee0000
Process: spoolsv.exe Pid: 3724 Address: 0x4afbf20000
Process: spoolsv.exe Pid: 3724 Address: 0x4afc1f0000
Process: spoolsv.exe Pid: 3724 Address: 0x4afc070000
Process: spoolsv.exe Pid: 3724 Address: 0x4afc260000
Process: explorer.exe Pid: 3472 Address: 0x5770000
Process: explorer.exe Pid: 3472 Address: 0xd840000
Process: ServerManager. Pid: 400 Address: 0x5dc9ce0000
Process: ServerManager. Pid: 400 Address: 0x5dc9cb0000
Process: ServerManager. Pid: 400 Address: 0x5dc9e70000
```

Flag: `spoolsv`

## Q8
> Identify the IP Address that delivered the payload. 

### Recon
直覺會想要volatility的netscan，但是結果實在是太多了，後來轉念一想直接看封包不就好了，所以我直接看原本傳送`coreupdater.exe`到server的IP

### Exploit
![圖片.png](https://hackmd.io/_uploads/Syh-4-4Qp.png)

Flag: `194.61.24.102`

## Q9
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

Flag: `203.78.103.109`

## Q10
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

Flag: `C:\Windows\System32\coreupdater.exe`

## Reference
[^szechuan-sauce-wp]:[CyberDefenders: Szechuan Sauce CTF Writeup](https://ellisstannard.medium.com/cyberdefenders-szechuan-sauce-writeup-ab172eb7666c)