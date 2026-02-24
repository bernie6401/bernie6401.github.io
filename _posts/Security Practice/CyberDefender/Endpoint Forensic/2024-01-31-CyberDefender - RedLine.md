---
title: CyberDefender - RedLine
tags: [CyberDefender, Endpoint Forensics]

category: "Security Practice｜CyberDefender｜Endpoint Forensic"
date: 2024-01-31
---

# CyberDefender - RedLine
<!-- more -->
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/106
:::spoiler TOC
[TOC]
:::

## Background
這一次的instance必須要使用volatility3才能解

## ==Q1==
> What is the name of the suspicious process? 

### Recon
直覺會想到直接pslist看有哪一些正在執行的process，不過[^redline-wp]提供了不一樣的想法，既然他是可疑的process，那就代表有機會操作一些malware會有的pattern例如injection之類的，所以可以先從malfind下手，看一下有哪一個process正在執行類似的操作

### Exploit
* 方法一: 直接pslist
    :::spoiler Command Result
    ```bash
    $ python vol.py -f MemoryDump.mem windows.pslist
    PID     PPID    ImageFileName   Offset(V)       Threads Handles SessionId       Wow64   CreateTime      ExitTime  File output

    4       0       System  0xad8185883180  157     -       N/A     False   2023-05-21 22:27:10.000000      N/A     Disabled
    108     4       Registry        0xad81858f2080  4       -       N/A     False   2023-05-21 22:26:54.000000      N/Disabled
    332     4       smss.exe        0xad81860dc040  2       -       N/A     False   2023-05-21 22:27:10.000000      N/Disabled
    452     444     csrss.exe       0xad81861cd080  12      -       0       False   2023-05-21 22:27:22.000000      N/Disabled
    528     520     csrss.exe       0xad8186f1b140  14      -       1       False   2023-05-21 22:27:25.000000      N/Disabled
    552     444     wininit.exe     0xad8186f2b080  1       -       0       False   2023-05-21 22:27:25.000000      N/Disabled
    588     520     winlogon.exe    0xad8186f450c0  5       -       1       False   2023-05-21 22:27:25.000000      N/Disabled
    676     552     services.exe    0xad8186f4d080  7       -       0       False   2023-05-21 22:27:29.000000      N/Disabled
    696     552     lsass.exe       0xad8186fc6080  10      -       0       False   2023-05-21 22:27:29.000000      N/Disabled
    824     676     svchost.exe     0xad818761d240  22      -       0       False   2023-05-21 22:27:32.000000      N/Disabled
    852     552     fontdrvhost.ex  0xad818761b0c0  5       -       0       False   2023-05-21 22:27:33.000000      N/Disabled
    860     588     fontdrvhost.ex  0xad818761f140  5       -       1       False   2023-05-21 22:27:33.000000      N/Disabled
    952     676     svchost.exe     0xad81876802c0  12      -       0       False   2023-05-21 22:27:36.000000      N/Disabled
    1016    588     dwm.exe 0xad81876e4340  15      -       1       False   2023-05-21 22:27:38.000000      N/A     Disabled
    448     676     svchost.exe     0xad8187721240  54      -       0       False   2023-05-21 22:27:41.000000      N/Disabled
    752     676     svchost.exe     0xad8187758280  21      -       0       False   2023-05-21 22:27:43.000000      N/Disabled
    1012    676     svchost.exe     0xad818774c080  19      -       0       False   2023-05-21 22:27:43.000000      N/Disabled
    1196    676     svchost.exe     0xad81877972c0  34      -       0       False   2023-05-21 22:27:46.000000      N/Disabled
    1280    4       MemCompression  0xad8187835080  62      -       N/A     False   2023-05-21 22:27:49.000000      N/Disabled
    1376    676     svchost.exe     0xad81878020c0  15      -       0       False   2023-05-21 22:27:49.000000      N/Disabled
    1448    676     svchost.exe     0xad818796c2c0  30      -       0       False   2023-05-21 22:27:52.000000      N/Disabled
    1496    676     svchost.exe     0xad81879752c0  12      -       0       False   2023-05-21 22:27:52.000000      N/Disabled
    1644    676     svchost.exe     0xad8187a112c0  6       -       0       False   2023-05-21 22:27:58.000000      N/Disabled
    1652    676     svchost.exe     0xad8187a2d2c0  10      -       0       False   2023-05-21 22:27:58.000000      N/Disabled
    1840    676     spoolsv.exe     0xad8187acb200  10      -       0       False   2023-05-21 22:28:03.000000      N/Disabled
    1892    676     svchost.exe     0xad8187b34080  14      -       0       False   2023-05-21 22:28:05.000000      N/Disabled
    2024    676     svchost.exe     0xad8187b65240  7       -       0       False   2023-05-21 22:28:11.000000      N/Disabled
    2076    676     svchost.exe     0xad8187b94080  10      -       0       False   2023-05-21 22:28:19.000000      N/Disabled
    2144    676     vmtoolsd.exe    0xad81896ab080  11      -       0       False   2023-05-21 22:28:19.000000      N/Disabled
    2152    676     vm3dservice.ex  0xad81896ae240  2       -       0       False   2023-05-21 22:28:19.000000      N/Disabled
    2200    676     VGAuthService.  0xad81896b3300  2       -       0       False   2023-05-21 22:28:19.000000      N/Disabled
    2404    2152    vm3dservice.ex  0xad8186619200  2       -       1       False   2023-05-21 22:28:32.000000      N/Disabled
    3028    676     dllhost.exe     0xad8185907080  12      -       0       False   2023-05-21 22:29:20.000000      N/Disabled
    832     676     msdtc.exe       0xad8185861280  9       -       0       False   2023-05-21 22:29:25.000000      N/Disabled
    1232    676     svchost.exe     0xad8186f4a2c0  7       -       0       False   2023-05-21 22:29:39.000000      N/Disabled
    1392    448     sihost.exe      0xad8189e94280  11      -       1       False   2023-05-21 22:30:08.000000      N/Disabled
    1064    676     svchost.exe     0xad8189d7c2c0  15      -       1       False   2023-05-21 22:30:09.000000      N/Disabled
    1600    448     taskhostw.exe   0xad8189d07300  10      -       1       False   2023-05-21 22:30:09.000000      N/Disabled
    3204    752     ctfmon.exe      0xad8189c8b280  12      -       1       False   2023-05-21 22:30:11.000000      N/Disabled
    3556    588     userinit.exe    0xad818c02f340  0       -       1       False   2023-05-21 22:30:28.000000      2023-05-21 22:30:43.000000         Disabled
    3580    3556    explorer.exe    0xad818c047340  76      -       1       False   2023-05-21 22:30:28.000000      N/Disabled
    3944    824     WmiPrvSE.exe    0xad818c054080  13      -       0       False   2023-05-21 22:30:44.000000      N/Disabled
    3004    676     svchost.exe     0xad818c4212c0  7       -       0       False   2023-05-21 22:30:55.000000      N/Disabled
    1116    676     svchost.exe     0xad818c426080  6       -       1       False   2023-05-21 22:31:00.000000      N/Disabled
    3160    824     StartMenuExper  0xad818cad3240  14      -       1       False   2023-05-21 22:31:21.000000      N/Disabled
    4116    824     RuntimeBroker.  0xad818cd93300  3       -       1       False   2023-05-21 22:31:24.000000      N/Disabled
    4228    676     SearchIndexer.  0xad818ce06240  15      -       0       False   2023-05-21 22:31:27.000000      N/Disabled
    4448    824     RuntimeBroker.  0xad818c09a080  9       -       1       False   2023-05-21 22:31:33.000000      N/Disabled
    464     3580    SecurityHealth  0xad818979d080  3       -       1       False   2023-05-21 22:31:59.000000      N/Disabled
    3252    3580    vmtoolsd.exe    0xad8189796300  8       -       1       False   2023-05-21 22:31:59.000000      N/Disabled
    5136    676     SecurityHealth  0xad818d374280  7       -       0       False   2023-05-21 22:32:01.000000      N/Disabled
    5328    3580    msedge.exe      0xad818d0980c0  54      -       1       False   2023-05-21 22:32:02.000000      N/Disabled
    4396    5328    msedge.exe      0xad818d515080  7       -       1       False   2023-05-21 22:32:19.000000      N/Disabled
    1144    5328    msedge.exe      0xad818d75f080  18      -       1       False   2023-05-21 22:32:38.000000      N/Disabled
    4544    5328    msedge.exe      0xad818d75b080  14      -       1       False   2023-05-21 22:32:39.000000      N/Disabled
    5340    5328    msedge.exe      0xad818d7b3080  10      -       1       False   2023-05-21 22:32:39.000000      N/Disabled
    5704    824     RuntimeBroker.  0xad8185962080  5       -       1       False   2023-05-21 22:32:44.000000      N/Disabled
    1764    824     dllhost.exe     0xad818d176080  7       -       1       False   2023-05-21 22:32:48.000000      N/Disabled
    1916    824     SearchApp.exe   0xad818d099080  24      -       1       False   2023-05-21 22:33:05.000000      N/Disabled
    6200    676     SgrmBroker.exe  0xad818d09f080  7       -       0       False   2023-05-21 22:33:42.000000      N/Disabled
    6696    676     svchost.exe     0xad818c532080  8       -       0       False   2023-05-21 22:34:07.000000      N/Disabled
    7312    824     ApplicationFra  0xad818e84f300  10      -       1       False   2023-05-21 22:35:44.000000      N/Disabled
    7772    676     svchost.exe     0xad818e88e140  3       -       0       False   2023-05-21 22:36:03.000000      N/Disabled
    6724    3580    Outline.exe     0xad818e578080  0       -       1       True    2023-05-21 22:36:09.000000      2023-05-21 23:01:24.000000         Disabled
    4224    6724    Outline.exe     0xad818e88b080  0       -       1       True    2023-05-21 22:36:23.000000      2023-05-21 23:01:24.000000         Disabled
    7160    824     SearchApp.exe   0xad818ccc4080  57      -       1       False   2023-05-21 22:39:13.000000      N/Disabled
    4628    6724    tun2socks.exe   0xad818de82340  0       -       1       True    2023-05-21 22:40:10.000000      2023-05-21 23:01:24.000000         Disabled
    6048    448     taskhostw.exe   0xad818dc5d080  5       -       1       False   2023-05-21 22:40:20.000000      N/Disabled
    8264    824     RuntimeBroker.  0xad818eec8080  4       -       1       False   2023-05-21 22:40:33.000000      N/Disabled
    3608    676     svchost.exe     0xad818d07a080  3       -       0       False   2023-05-21 22:41:28.000000      N/Disabled
    6644    824     SkypeApp.exe    0xad818d3ac080  49      -       1       False   2023-05-21 22:41:52.000000      N/Disabled
    5656    824     RuntimeBroker.  0xad81876e8080  0       -       1       False   2023-05-21 21:58:19.000000      2023-05-21 22:02:01.000000         Disabled
    8952    824     TextInputHost.  0xad818e6db080  10      -       1       False   2023-05-21 21:59:11.000000      N/Disabled
    5808    824     HxTsr.exe       0xad818de5d080  0       -       1       False   2023-05-21 21:59:58.000000      2023-05-21 22:07:45.000000         Disabled
    2388    5328    msedge.exe      0xad818e54c340  18      -       1       False   2023-05-21 22:05:35.000000      N/Disabled
    6292    5328    msedge.exe      0xad818d7a1080  20      -       1       False   2023-05-21 22:06:15.000000      N/Disabled
    3876    448     taskhostw.exe   0xad8189b30080  8       -       1       False   2023-05-21 22:08:02.000000      N/Disabled
    372     824     SkypeBackgroun  0xad8186f49080  3       -       1       False   2023-05-21 22:10:00.000000      N/Disabled
    1120    676     MsMpEng.exe     0xad818945c080  12      -       0       False   2023-05-21 22:10:01.000000      N/Disabled
    6076    824     ShellExperienc  0xad818eb18080  14      -       1       False   2023-05-21 22:11:36.000000      N/Disabled
    7336    824     RuntimeBroker.  0xad818e8bb080  2       -       1       False   2023-05-21 22:11:39.000000      N/Disabled
    7964    5328    msedge.exe      0xad818dee5080  19      -       1       False   2023-05-21 22:22:09.000000      N/Disabled
    6544    5328    msedge.exe      0xad818c0ea080  18      -       1       False   2023-05-21 22:22:35.000000      N/Disabled
    5964    676     svchost.exe     0xad818ef86080  5       -       0       False   2023-05-21 22:27:56.000000      N/Disabled
    8896    5328    msedge.exe      0xad8187a39080  18      -       1       False   2023-05-21 22:28:21.000000      N/Disabled
    5156    5328    msedge.exe      0xad818c553080  14      -       1       False   2023-05-21 22:28:22.000000      N/Disabled
    5896    8844    oneetx.exe      0xad8189b41080  5       -       1       True    2023-05-21 22:30:56.000000      N/Disabled
    7732    5896    rundll32.exe    0xad818d1912c0  1       -       1       True    2023-05-21 22:31:53.000000      N/Disabled
    6324    1496    audiodg.exe     0xad818df2e080  4       -       0       False   2023-05-21 22:42:56.000000      N/Disabled
    2228    3580    FTK Imager.exe  0xad818d143080  10      -       1       False   2023-05-21 22:43:56.000000      N/Disabled
    5636    3580    notepad.exe     0xad818db45080  1       -       1       False   2023-05-21 22:46:50.000000      N/Disabled
    2044    676     svchost.exe     0xad8189b27080  28      -       0       False   2023-05-21 22:49:29.000000      N/Disabled
    8708    676     svchost.exe     0xad818d431080  5       -       0       False   2023-05-21 22:57:33.000000      N/Disabled
    5476    676     svchost.exe     0xad818e752080  9       -       0       False   2023-05-21 22:58:08.000000      N/Disabled
    6596    676     TrustedInstall  0xad818dc88080  4       -       0       False   2023-05-21 22:58:13.000000      N/Disabled
    2332    824     TiWorker.exe    0xad818e780080  4       -       0       False   2023-05-21 22:58:13.000000      N/Disabled
    4340    676     VSSVC.exe       0xad818e888080  3       -       0       False   2023-05-21 23:01:06.000000      N/Disabled
    7540    824     smartscreen.ex  0xad818e893080  14      -       1       False   2023-05-21 23:02:26.000000      N/Disabled
    8920    3580    FTK Imager.exe  0xad818ef81080  20      -       1       False   2023-05-21 23:02:28.000000      N/Disabled
    5480    448     oneetx.exe      0xad818d3d6080  6       -       1       True    2023-05-21 23:03:00.000000      N/Disabled
    ```
    :::
* 方法二: 用malfind排出一些正常的process
    ```bash
    $ python vol.py -f MemoryDump.mem windows.malfind
    Volatility 3 Framework 2.4.2
    Progress:  100.00               PDB scanning finished
    PID     Process Start VPN       End VPN Tag     Protection      CommitCharge    PrivateMemory   File output     Hexdump Disasm

    5896    oneetx.exe      0x400000        0x437fff        VadS    PAGE_EXECUTE_READWRITE  56      1       Disabled
    4d 5a 90 00 03 00 00 00 MZ......
    04 00 00 00 ff ff 00 00 ........
    b8 00 00 00 00 00 00 00 ........
    40 00 00 00 00 00 00 00 @.......
    00 00 00 00 00 00 00 00 ........
    00 00 00 00 00 00 00 00 ........
    00 00 00 00 00 00 00 00 ........
    00 00 00 00 00 01 00 00 ........
    0x400000:       dec     ebp
    0x400001:       pop     edx
    0x400002:       nop
    0x400003:       add     byte ptr [ebx], al
    0x400005:       add     byte ptr [eax], al
    0x400007:       add     byte ptr [eax + eax], al
    0x40000a:       add     byte ptr [eax], al
    7540    smartscreen.ex  0x2505c140000   0x2505c15ffff   VadS    PAGE_EXECUTE_READWRITE  1       1       Disabled
    48 89 54 24 10 48 89 4c H.T$.H.L
    24 08 4c 89 44 24 18 4c $.L.D$.L
    89 4c 24 20 48 8b 41 28 .L$.H.A(
    48 8b 48 08 48 8b 51 50 H.H.H.QP
    48 83 e2 f8 48 8b ca 48 H...H..H
    b8 60 00 14 5c 50 02 00 .`..\P..
    00 48 2b c8 48 81 f9 70 .H+.H..p
    0f 00 00 76 09 48 c7 c1 ...v.H..
    0x2505c140000:  mov     qword ptr [rsp + 0x10], rdx
    0x2505c140005:  mov     qword ptr [rsp + 8], rcx
    0x2505c14000a:  mov     qword ptr [rsp + 0x18], r8
    0x2505c14000f:  mov     qword ptr [rsp + 0x20], r9
    0x2505c140014:  mov     rax, qword ptr [rcx + 0x28]
    0x2505c140018:  mov     rcx, qword ptr [rax + 8]
    0x2505c14001c:  mov     rdx, qword ptr [rcx + 0x50]
    0x2505c140020:  and     rdx, 0xfffffffffffffff8
    0x2505c140024:  mov     rcx, rdx
    0x2505c140027:  movabs  rax, 0x2505c140060
    0x2505c140031:  sub     rcx, rax
    0x2505c140034:  cmp     rcx, 0xf70
    0x2505c14003b:  jbe     0x2505c140046
    ```
    可以看到`oneetx.exe`和`smartscreen.ex`都有進行一些可疑操作，果然`oneetx.exe`就是答案

:::spoiler Flag
Flag: `oneetx.exe`
:::

## ==Q2==
> What is the child process name of the suspicious process?

### Recon
透過上一題的結果可以知道PID 5896的`oneetx.exe`創造了`rundll32.exe`，所以`rundll32.exe`就是`oneetx.exe`的子程序

### Exploit
:::spoiler Flag
Flag: `rundll32.exe`
:::

## ==Q3==
> What is the memory protection applied to the suspicious process memory region?

### Recon
這一題因為不知道他到底在問甚麼，所以是參考[^redline-wp]的說明，主要可以從Q1的結果看他的protection，這應該就有點像是unix的權限ㄅ

### Exploit

:::spoiler Flag
Flag: `PAGE_EXECUTE_READWRITE  `
:::

## ==Q4==
> What is the name of the process responsible for the VPN connection?

### Recon
這一題也是從上上一題的結果慢慢try出來的，不過如果此細看有一些process也是常見的東西
* [什麼是svchost.exe？](https://daydayreview.com/svchost-exe%E3%80%82%E5%AE%83%E6%98%AF%E4%BB%80%E9%BA%BC%EF%BC%8C%E7%82%BA%E4%BB%80%E9%BA%BC%E5%9C%A8%E6%88%91%E7%9A%84%E9%9B%BB%E8%85%A6%E4%B8%8A%E9%81%8B%E8%A1%8C%EF%BC%9F/)
    > svchost.exe被稱為服務主機，是一個軟體程式，是Windows操作系統的一部分，被許多Windows應用程式使用。一台計算機的svchost.exe應該位於系統文件夾中的'\windows\System32'。
    > 在啟動時，服務控制管理器啟動svchost.exe，以管理從動態鏈接庫（DLLs）運行的系統服務。因此，對於每個正在運行的服務，都有一個svchost.exe的實例來管理它。
    > 它通過確保各種服務和進程共享資源來幫助減少CPU負荷。動態鏈接庫有被各種軟體應用程式所利用的代碼。它們需要svchost.exe作為額外的軟體來確保運行這些不同服務的效率。這可以確保Windows或其他程式所需的DLL文件被有效加載。
* [dllhost.exe](https://baike.baidu.com/item/dllhost.exe/8193205)
    > dllhost.exe是微軟Windows操作系統的一部分。dllhost.exe用於管理DLL應用，在任務管理器中可以找到，這個程序對是微軟Windows系統的正常運行是非常重要的。

### Exploit
[Outline](https://getoutline.org/zh-TW/)
> Outline 可讓任何人建立和執行自己專屬的 VPN，以及分享 VPN 的存取權。由於經過特殊設計，Outline 可防禦封鎖機制，並讓你控制自己的伺服器設定，包含伺服器的所在位置。Outline 採用公開透明的技術及完整開放原始碼，而且經過兩家安全性機構的稽核，確保這款軟體採用最新技術且安全無虞。

:::spoiler Flag
Flag: `Outline.exe`
:::

## ==Q5==
> What is the attacker's IP address?

### Recon
直覺就是netscan

### Exploit
:::spoiler Command Result
```bash
$ python vol.py -f MemoryDump.mem windows.netscan
Volatility 3 Framework 2.4.2
Progress:  100.00               PDB scanning finished
Offset  Proto   LocalAddr       LocalPort       ForeignAddr     ForeignPort     State   PID     Owner   Created

0xad81861e2310  TCPv4   0.0.0.0 49668   0.0.0.0 0       LISTENING       1840    spoolsv.exe     2023-05-21 22:28:09.000000
0xad81861e2310  TCPv6   ::      49668   ::      0       LISTENING       1840    spoolsv.exe     2023-05-21 22:28:09.000000
0xad81861e2470  TCPv4   0.0.0.0 5040    0.0.0.0 0       LISTENING       1196    svchost.exe     2023-05-21 22:30:31.000000
0xad81861e2730  TCPv4   0.0.0.0 135     0.0.0.0 0       LISTENING       952     svchost.exe     2023-05-21 22:27:36.000000
0xad81861e2b50  TCPv4   0.0.0.0 49665   0.0.0.0 0       LISTENING       552     wininit.exe     2023-05-21 22:27:36.000000
0xad81861e2b50  TCPv6   ::      49665   ::      0       LISTENING       552     wininit.exe     2023-05-21 22:27:36.000000
0xad81861e2e10  TCPv4   0.0.0.0 49665   0.0.0.0 0       LISTENING       552     wininit.exe     2023-05-21 22:27:36.000000
0xad81861e3230  TCPv4   0.0.0.0 49664   0.0.0.0 0       LISTENING       696     lsass.exe       2023-05-21 22:27:36.000000
0xad81861e3390  TCPv4   0.0.0.0 135     0.0.0.0 0       LISTENING       952     svchost.exe     2023-05-21 22:27:36.000000
0xad81861e3390  TCPv6   ::      135     ::      0       LISTENING       952     svchost.exe     2023-05-21 22:27:36.000000
0xad81861e34f0  TCPv4   0.0.0.0 49664   0.0.0.0 0       LISTENING       696     lsass.exe       2023-05-21 22:27:36.000000
0xad81861e34f0  TCPv6   ::      49664   ::      0       LISTENING       696     lsass.exe       2023-05-21 22:27:36.000000
0xad81861e37b0  TCPv4   0.0.0.0 49666   0.0.0.0 0       LISTENING       1012    svchost.exe     2023-05-21 22:27:49.000000
0xad81861e37b0  TCPv6   ::      49666   ::      0       LISTENING       1012    svchost.exe     2023-05-21 22:27:49.000000
0xad81861e3910  TCPv4   0.0.0.0 49667   0.0.0.0 0       LISTENING       448     svchost.exe     2023-05-21 22:27:58.000000
0xad81861e3910  TCPv6   ::      49667   ::      0       LISTENING       448     svchost.exe     2023-05-21 22:27:58.000000
0xad81861e3a70  TCPv4   0.0.0.0 49668   0.0.0.0 0       LISTENING       1840    spoolsv.exe     2023-05-21 22:28:09.000000
0xad81861e3bd0  TCPv4   0.0.0.0 49666   0.0.0.0 0       LISTENING       1012    svchost.exe     2023-05-21 22:27:49.000000
0xad81861e3e90  TCPv4   0.0.0.0 49667   0.0.0.0 0       LISTENING       448     svchost.exe     2023-05-21 22:27:58.000000
0xad818662ecb0  TCPv4   0.0.0.0 445     0.0.0.0 0       LISTENING       4       System  2023-05-21 22:29:04.000000
0xad818662ecb0  TCPv6   ::      445     ::      0       LISTENING       4       System  2023-05-21 22:29:04.000000
0xad818662f390  TCPv4   0.0.0.0 7680    0.0.0.0 0       LISTENING       5476    svchost.exe     2023-05-21 22:58:09.000000
0xad818662f390  TCPv6   ::      7680    ::      0       LISTENING       5476    svchost.exe     2023-05-21 22:58:09.000000
0xad81878518f0  UDPv4   192.168.190.141 138     *       0               4       System  2023-05-21 22:27:56.000000
0xad8187852250  UDPv4   192.168.190.141 137     *       0               4       System  2023-05-21 22:27:56.000000
0xad818902a5d0  TCPv4   192.168.190.141 139     0.0.0.0 0       LISTENING       4       System  2023-05-21 22:27:56.000000
0xad818971f870  UDPv4   0.0.0.0 56250   *       0               6644    SkypeApp.exe    2023-05-21 22:58:07.000000
0xad818971f870  UDPv6   ::      56250   *       0               6644    SkypeApp.exe    2023-05-21 22:58:07.000000
0xad81897eb010  TCPv4   10.0.85.2       55439   20.22.207.36    443     CLOSED  448     svchost.exe     2023-05-21 23:00:40.000000
0xad81898a6d10  UDPv4   127.0.0.1       57787   *       0               448     svchost.exe     2023-05-21 22:28:54.000000
0xad81898bc7f0  UDPv4   0.0.0.0 5355    *       0               1448    svchost.exe     2023-05-21 22:57:37.000000
0xad81898bc7f0  UDPv6   ::      5355    *       0               1448    svchost.exe     2023-05-21 22:57:37.000000
0xad8189a291b0  TCPv4   0.0.0.0 55972   0.0.0.0 0       LISTENING       5964    svchost.exe     2023-05-21 22:27:57.000000
0xad8189a291b0  TCPv6   ::      55972   ::      0       LISTENING       5964    svchost.exe     2023-05-21 22:27:57.000000
0xad8189a29470  TCPv4   0.0.0.0 55972   0.0.0.0 0       LISTENING       5964    svchost.exe     2023-05-21 22:27:57.000000
0xad8189a2a7b0  TCPv4   0.0.0.0 49669   0.0.0.0 0       LISTENING       676     services.exe    2023-05-21 22:29:08.000000
0xad8189a2a910  TCPv4   0.0.0.0 49669   0.0.0.0 0       LISTENING       676     services.exe    2023-05-21 22:29:08.000000
0xad8189a2a910  TCPv6   ::      49669   ::      0       LISTENING       676     services.exe    2023-05-21 22:29:08.000000
0xad8189a30a20  TCPv4   192.168.190.141 53660   38.121.43.65    443     CLOSED  4628    tun2socks.exe   2023-05-21 22:00:25.000000
0xad8189a844e0  UDPv4   10.0.85.2       58844   *       0               5328    msedge.exe      2023-05-21 22:51:53.000000
0xad8189cea350  UDPv4   0.0.0.0 5050    *       0               1196    svchost.exe     2023-05-21 22:30:27.000000
0xad818c17ada0  UDPv4   0.0.0.0 52051   *       0               4628    tun2socks.exe   2023-05-21 22:24:14.000000
0xad818c367b30  TCPv4   192.168.190.141 49710   204.79.197.203  443     CLOSE_WAIT      1916    SearchApp.exe   2023-05-21 22:33:09.000000
0xad818c3b22e0  UDPv4   0.0.0.0 63218   *       0               1448    svchost.exe     2023-05-21 22:39:15.000000
0xad818c3b22e0  UDPv6   ::      63218   *       0               1448    svchost.exe     2023-05-21 22:39:15.000000
0xad818d004ba0  UDPv4   0.0.0.0 63917   *       0               1448    svchost.exe     2023-05-21 23:02:48.000000
0xad818d004ba0  UDPv6   ::      63917   *       0               1448    svchost.exe     2023-05-21 23:02:48.000000
0xad818d1bc010  TCPv4   10.0.85.2       55424   52.182.143.208  443     CLOSE_WAIT      6644    SkypeApp.exe    2023-05-21 22:57:59.000000
0xad818d2f7b00  TCPv4   10.0.85.2       55460   52.159.127.243  443     CLOSED  448     svchost.exe     2023-05-21 23:01:08.000000
0xad818d5352b0  TCPv4   10.0.85.2       53659   204.79.197.237  443     CLOSED  3580    explorer.exe    2023-05-21 22:00:25.000000
0xad818da19700  UDPv4   0.0.0.0 500     *       0               448     svchost.exe     2023-05-21 22:27:56.000000
0xad818da1ab50  UDPv4   0.0.0.0 4500    *       0               448     svchost.exe     2023-05-21 22:27:56.000000
0xad818da1d8a0  UDPv4   0.0.0.0 4500    *       0               448     svchost.exe     2023-05-21 22:27:56.000000
0xad818da1d8a0  UDPv6   ::      4500    *       0               448     svchost.exe     2023-05-21 22:27:56.000000
0xad818da1dbc0  UDPv4   0.0.0.0 0       *       0               448     svchost.exe     2023-05-21 22:27:57.000000
0xad818da1dbc0  UDPv6   ::      0       *       0               448     svchost.exe     2023-05-21 22:27:57.000000
0xad818da1e520  UDPv4   0.0.0.0 0       *       0               448     svchost.exe     2023-05-21 22:27:57.000000
0xad818da1f010  UDPv4   0.0.0.0 500     *       0               448     svchost.exe     2023-05-21 22:27:56.000000
0xad818da1f010  UDPv6   ::      500     *       0               448     svchost.exe     2023-05-21 22:27:56.000000
0xad818da202d0  UDPv4   0.0.0.0 0       *       0               5964    svchost.exe     2023-05-21 22:27:57.000000
0xad818da202d0  UDPv6   ::      0       *       0               5964    svchost.exe     2023-05-21 22:27:57.000000
0xad818da21bd0  UDPv4   0.0.0.0 0       *       0               5964    svchost.exe     2023-05-21 22:27:57.000000
0xad818dbc1a60  TCPv4   192.168.190.141 49713   104.119.188.96  443     CLOSE_WAIT      1916    SearchApp.exe   2023-05-21 22:33:11.000000
0xad818dd05370  UDPv4   0.0.0.0 5353    *       0               5328    msedge.exe      2023-05-21 23:01:32.000000
0xad818dd07440  UDPv4   0.0.0.0 5353    *       0               5328    msedge.exe      2023-05-21 23:01:32.000000
0xad818dd07440  UDPv6   ::      5353    *       0               5328    msedge.exe      2023-05-21 23:01:32.000000
0xad818de4aa20  TCPv4   10.0.85.2       55462   77.91.124.20    80      CLOSED  5896    oneetx.exe      2023-05-21 23:01:22.000000
0xad818df1d920  TCPv4   192.168.190.141 55433   38.121.43.65    443     CLOSED  4628    tun2socks.exe   2023-05-21 23:00:02.000000
0xad818e3698f0  UDPv4   0.0.0.0 5353    *       0               5328    msedge.exe      2023-05-21 22:05:24.000000
0xad818e3701a0  UDPv4   0.0.0.0 5353    *       0               5328    msedge.exe      2023-05-21 22:05:24.000000
0xad818e3701a0  UDPv6   ::      5353    *       0               5328    msedge.exe      2023-05-21 22:05:24.000000
0xad818e370b00  UDPv4   0.0.0.0 5353    *       0               5328    msedge.exe      2023-05-21 22:05:24.000000
0xad818e371dc0  UDPv4   0.0.0.0 5353    *       0               5328    msedge.exe      2023-05-21 22:05:24.000000
0xad818e371dc0  UDPv6   ::      5353    *       0               5328    msedge.exe      2023-05-21 22:05:24.000000
0xad818e3a1200  UDPv4   0.0.0.0 5355    *       0               1448    svchost.exe     2023-05-21 22:57:37.000000
0xad818e4a6900  UDPv4   0.0.0.0 0       *       0               5480    oneetx.exe      2023-05-21 22:39:47.000000
0xad818e4a6900  UDPv6   ::      0       *       0               5480    oneetx.exe      2023-05-21 22:39:47.000000
0xad818e4a9650  UDPv4   0.0.0.0 0       *       0               5480    oneetx.exe      2023-05-21 22:39:47.000000
0xad818e77da20  TCPv4   192.168.190.141 52434   204.79.197.200  443     CLOSED  -       -       2023-05-21 23:02:20.000000
0xad818ef06c70  UDPv6   fe80::a406:8c42:43a9:413        1900    *       0               3004    svchost.exe     2023-05-21 22:40:16.000000
0xad818ef09b50  UDPv6   fe80::4577:874:81a:78cd 1900    *       0               3004    svchost.exe     2023-05-21 22:40:16.000000
0xad818ef0b5e0  UDPv6   ::1     1900    *       0               3004    svchost.exe     2023-05-21 22:40:16.000000
0xad818ef0ec90  UDPv6   fe80::a406:8c42:43a9:413        55910   *       0               3004    svchost.exe     2023-05-21 22:40:16.000000
0xad818ef0f140  UDPv6   fe80::4577:874:81a:78cd 55911   *       0               3004    svchost.exe     2023-05-21 22:40:16.000000
0xad818ef0f2d0  UDPv6   ::1     55912   *       0               3004    svchost.exe     2023-05-21 22:40:16.000000
0xad818ef0fdc0  UDPv4   192.168.190.141 55913   *       0               3004    svchost.exe     2023-05-21 22:40:16.000000
0xad818ef10270  UDPv4   10.0.85.2       137     *       0               4       System  2023-05-21 22:40:16.000000
0xad818ef11530  UDPv4   192.168.190.141 1900    *       0               3004    svchost.exe     2023-05-21 22:40:16.000000
0xad818ef116c0  UDPv4   10.0.85.2       1900    *       0               3004    svchost.exe     2023-05-21 22:40:16.000000
0xad818ef11850  UDPv4   10.0.85.2       138     *       0               4       System  2023-05-21 22:40:16.000000
0xad818ef119e0  UDPv4   127.0.0.1       1900    *       0               3004    svchost.exe     2023-05-21 22:40:16.000000
0xad818ef13150  UDPv4   10.0.85.2       55914   *       0               3004    svchost.exe     2023-05-21 22:40:16.000000
0xad818ef132e0  UDPv4   127.0.0.1       55915   *       0               3004    svchost.exe     2023-05-21 22:40:16.000000
0xad818ef77b40  TCPv4   192.168.190.141 55176   192.168.190.2   53      CLOSED  1448    svchost.exe     2023-05-21 23:01:39.000000
0xad818f88cc80  UDPv4   0.0.0.0 5355    *       0               1448    svchost.exe     2023-05-21 23:01:26.000000
0xad818f88cc80  UDPv6   ::      5355    *       0               1448    svchost.exe     2023-05-21 23:01:26.000000
0xad818f894340  UDPv4   0.0.0.0 5355    *       0               1448    svchost.exe     2023-05-21 23:01:26.000000
0xad8190dd8800  UDPv4   0.0.0.0 5353    *       0               1448    svchost.exe     2023-05-21 23:01:25.000000
0xad8190dd8800  UDPv6   ::      5353    *       0               1448    svchost.exe     2023-05-21 23:01:25.000000
0xad8190dd8990  UDPv4   0.0.0.0 5353    *       0               1448    svchost.exe     2023-05-21 23:01:25.000000
0xad8190dd97a0  UDPv4   0.0.0.0 0       *       0               1448    svchost.exe     2023-05-21 23:01:25.000000
0xad8190dd97a0  UDPv6   ::      0       *       0               1448    svchost.exe     2023-05-21 23:01:25.000000
0xad8190e12b10  UDPv6   fe80::a406:8c42:43a9:413        1900    *       0               3004    svchost.exe     2023-05-21 23:01:29.000000
0xad8190e161c0  UDPv6   ::1     1900    *       0               3004    svchost.exe     2023-05-21 23:01:29.000000
0xad8190e16e40  UDPv4   192.168.190.141 1900    *       0               3004    svchost.exe     2023-05-21 23:01:29.000000
0xad8190e19230  UDPv6   ::1     57094   *       0               3004    svchost.exe     2023-05-21 23:01:29.000000
0xad8190e1a1d0  UDPv4   192.168.190.141 57095   *       0               3004    svchost.exe     2023-05-21 23:01:29.000000
0xad8190e1a360  UDPv4   127.0.0.1       57096   *       0               3004    svchost.exe     2023-05-21 23:01:29.000000
0xad8190e1a680  UDPv4   127.0.0.1       1900    *       0               3004    svchost.exe     2023-05-21 23:01:29.000000
0xad8190e1acc0  UDPv6   fe80::a406:8c42:43a9:413        57093   *       0               3004    svchost.exe     2023-05-21 23:01:29.000000
0xad8190e59a60  UDPv4   0.0.0.0 55536   *       0               4628    tun2socks.exe   2023-05-21 23:00:47.000000
0xad8190e59d80  UDPv4   0.0.0.0 56228   *       0               4628    tun2socks.exe   2023-05-21 23:00:38.000000
0xad8190e5b040  UDPv4   0.0.0.0 49734   *       0               4628    tun2socks.exe   2023-05-21 23:00:41.000000
```
:::
直接看`oneetx.exe`的PID就可以看到了

:::spoiler Flag
Flag: `77.91.124.20`
:::

## ==Q6==
> Based on the previous artifacts. What is the name of the malware family?

### Recon
這題也找了超久，[^redline-wp]是直接用string search看有沒有readline stealer的字樣，但也沒說key words哪來的，所以就直接先送flag後看官解

### Exploit
1. 因為這是一隻真正的trojan樣本，所以可以從上一題看到他傳送資訊給C2C server的IP，而我們可以把該IP透過virustotal查看
2. 從community中，最下面有一個[RedLine的討論](https://www.virustotal.com/gui/collection/f6cb8976174a8e375963a0821b3a0a19205d9d739b4522be61e8408eaf5534d0)
    ![](https://hackmd.io/_uploads/ByHYH6ibT.png)
3. 該文章說明`RedLine Stealer`是一隻怎樣的惡意程式
    > RedLine Stealer is a malware available on underground forums for sale apparently as standalone ($100/$150 depending on the version) or also on a subscription basis ($100/month). This malware harvests information from browsers such as saved credentials, autocomplete data, and credit card information. A system inventory is also taken when running on a target machine, to include details such as the username, location data, hardware configuration, and information regarding installed security software. More recent versions of RedLine added the ability to steal cryptocurrency. FTP and IM clients are also apparently targeted by this family, and this malware has the ability to upload and download files, execute commands, and periodically send back information about the infected computer.

:::spoiler Flag
Flag: `Redline Stealer`
:::

## ==Q7==
> What is the full URL of the PHP file that the attacker visited?

### Recon
這一題也不到怎麼用正規的方式知道他訪問了哪些頁面，所以也是參考[^redline-wp]的解法才知道可以用string search

### Exploit
從前面可以知道C&C server IP是`77.91.124.20`，則我們可以知道他應該是request這個IP所建立的網站
```bash
$ strings MemoryDump.mem | grep "http://77.91.124.20"
http://77.91.124.20/ E
http://77.91.124.20/store/gamel
http://77.91.124.20/ E
http://77.91.124.20/DSC01491/
http://77.91.124.20/DSC01491/
http://77.91.124.20/store/games/index.php
http://77.91.124.20/store/games/index.php
http://77.91.124.20/store/games/index.php
```

:::spoiler Flag
Flag: `http://77.91.124.20/store/games/index.php`
:::

## ==Q8==
> What is the full path of the malicious executable?

### Recon
最後一題也超簡單，直接看filescan搭配findstr把有關`oneetx.exe`的string print出來後就知道位置在哪裡

### Exploit
```bash
$ python vol.py -f MemoryDump.mem windows.filescan | findstr oneetx.exe
0xad818d436c70.0\Users\Tammam\AppData\Local\Temp\c3912af058\oneetx.exe  216
0xad818da36c30  \Users\Tammam\AppData\Local\Temp\c3912af058\oneetx.exe  216
0xad818ef1a0b0  \Users\Tammam\AppData\Local\Temp\c3912af058\oneetx.exe  216
```

:::spoiler Flag
Flag: `C:\Users\Tammam\AppData\Local\Temp\c3912af058\oneetx.exe`
:::

## Reference
[^redline-wp]:[CyberDefenders Challenges: RedLine Walkthrough](https://medium.com/@iCreaM/cyberdefenders-challenges-redline-walkthrough-1212bca626)
