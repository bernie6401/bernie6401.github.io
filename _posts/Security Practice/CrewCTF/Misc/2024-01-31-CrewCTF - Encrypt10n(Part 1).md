---
title: CrewCTF - Encrypt10n(Part 1)
tags: [CTF, CrewCTF, Misc]

category: "Security Practice｜CrewCTF｜Misc"
date: 2024-01-31
---

# CrewCTF - Encrypt10n(Part 1)
<!-- more -->

## Background
[Volatility 3](https://github.com/volatilityfoundation/volatility3)

## Recon
* Description: We made a memory dump on the criminal machine after entering the crime scene. Our investigator thought he was using encryption software to hide the secret. can you help me to detect it?
* Q1 : crew{password}
這種類型之前沒碰過，所以看了別人的WP學一下[^CTFTime_WP]
首先他有提到他有用加密的技術隱藏secret，所以我們的目的就是要找到password

## Exploit - Memory Forensics
1. 先找到運行的OS version或其他軟硬體資訊
    ```bash
    $ python ../../Software/CTF/Misc/volatility/vol.py -f dump.raw imageinfo
    Volatility Foundation Volatility Framework 2.6.1
    INFO    : volatility.debug    : Determining profile based on KDBG search...
              Suggested Profile(s) : Win7SP1x86_23418, Win7SP0x86, Win7SP1x86_24000, Win7SP1x86
                         AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                         AS Layer2 : FileAddressSpace (/mnt/d/Download/Trash/dump.raw)
                          PAE type : PAE
                               DTB : 0x185000L
                              KDBG : 0x82b3db78L
              Number of Processors : 1
         Image Type (Service Pack) : 1
                    KPCR for CPU 0 : 0x839a5000L
                 KUSER_SHARED_DATA : 0xffdf0000L
               Image date and time : 2023-02-16 12:03:16 UTC+0000
         Image local date and time : 2023-02-16 14:03:16 +0200
    ```
    重點: `Suggested Profile(s) : Win7SP1x86_23418, Win7SP0x86, Win7SP1x86_24000, Win7SP1x86`
2. 列出當時系統正在運行的process
    ```bash
    $ python ../../Software/CTF/Misc/volatility/vol.py -f dump.raw pslist --profile=Win7SP0x86
    Volatility Foundation Volatility Framework 2.6.1
    Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit
    ---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
    0x8413a938 System                    4      0     88      520 ------      0 2023-02-16 12:00:48 UTC+0000
    0x84e481c8 smss.exe                252      4      2       29 ------      0 2023-02-16 12:00:49 UTC+0000
    0x84cae358 csrss.exe               340    324      8      550      0      0 2023-02-16 12:00:53 UTC+0000
    0x844ea030 wininit.exe             392    324      3       77      0      0 2023-02-16 12:00:54 UTC+0000
    0x84ef5030 csrss.exe               400    384      9      223      1      0 2023-02-16 12:00:54 UTC+0000
    0x8573dd20 winlogon.exe            456    384      6      114      1      0 2023-02-16 12:00:54 UTC+0000
    0x85749868 services.exe            496    392      8      228      0      0 2023-02-16 12:00:54 UTC+0000
    0x85763030 lsass.exe               508    392      7      578      0      0 2023-02-16 12:00:55 UTC+0000
    0x85764030 lsm.exe                 516    392     10      149      0      0 2023-02-16 12:00:55 UTC+0000
    0x857bd510 svchost.exe             624    496     11      362      0      0 2023-02-16 12:00:56 UTC+0000
    0x85809510 svchost.exe             704    496      7      298      0      0 2023-02-16 12:00:56 UTC+0000
    0x85859920 svchost.exe             784    496     23      510      0      0 2023-02-16 12:00:56 UTC+0000
    0x8586da80 svchost.exe             832    496     15      265      0      0 2023-02-16 12:00:57 UTC+0000
    0x85872bb0 svchost.exe             856    496     22      731      0      0 2023-02-16 12:00:57 UTC+0000
    0x85875460 svchost.exe             880    496     47     1013      0      0 2023-02-16 12:00:57 UTC+0000
    0x8588f370 audiodg.exe             960    784      6      132      0      0 2023-02-16 12:00:57 UTC+0000
    0x858c2420 svchost.exe            1092    496     18      389      0      0 2023-02-16 12:00:58 UTC+0000
    0x857d6030 spoolsv.exe            1288    496     15      270      0      0 2023-02-16 12:00:59 UTC+0000
    0x857d1030 dwm.exe                1296    832      6      114      1      0 2023-02-16 12:00:59 UTC+0000
    0x857c7030 svchost.exe            1324    496     21      310      0      0 2023-02-16 12:00:59 UTC+0000
    0x857a5d20 explorer.exe           1384   1276     33      923      1      0 2023-02-16 12:00:59 UTC+0000
    0x857c4d20 taskhost.exe           1400    496     10      197      1      0 2023-02-16 12:00:59 UTC+0000
    0x85837898 svchost.exe            1560    496     11      146      0      0 2023-02-16 12:01:00 UTC+0000
    0x841d1030 VGAuthService.         1720    496      4       85      0      0 2023-02-16 12:01:01 UTC+0000
    0x841d7118 vmtoolsd.exe           1736   1384     10      181      1      0 2023-02-16 12:01:02 UTC+0000
    0x85856030 vm3dservice.ex         1836    496      5       60      0      0 2023-02-16 12:01:03 UTC+0000
    0x85857d20 vmtoolsd.exe           1856    496     14      291      0      0 2023-02-16 12:01:03 UTC+0000
    0x841e5678 vm3dservice.ex         1880   1836      3       44      1      0 2023-02-16 12:01:03 UTC+0000
    0x85a26030 svchost.exe             384    496      8       93      0      0 2023-02-16 12:01:05 UTC+0000
    0x85a6e5d0 dllhost.exe             876    496     21      191      0      0 2023-02-16 12:01:05 UTC+0000
    0x85941c28 dllhost.exe            1744    496     18      200      0      0 2023-02-16 12:01:05 UTC+0000
    0x85ab6260 msdtc.exe              1128    496     15      154      0      0 2023-02-16 12:01:06 UTC+0000
    0x85ac8b00 WmiPrvSE.exe            232    624     10      193      0      0 2023-02-16 12:01:06 UTC+0000
    0x841f4470 SearchIndexer.         2148    496     14      604      0      0 2023-02-16 12:01:08 UTC+0000
    0x85b2a030 VSSVC.exe              2276    496      7      118      0      0 2023-02-16 12:01:11 UTC+0000
    0x85b80cb8 SearchProtocol         2372   2148      9      284      0      0 2023-02-16 12:01:13 UTC+0000
    0x85b855f8 SearchFilterHo         2392   2148      6      104      0      0 2023-02-16 12:01:13 UTC+0000
    0x85b97d20 svchost.exe            2480    496     15      232      0      0 2023-02-16 12:01:15 UTC+0000
    0x85bc5398 wmpnetwk.exe           2632    496     11      212      0      0 2023-02-16 12:01:16 UTC+0000
    0x85bba030 WmiPrvSE.exe           2860    624     15      319      0      0 2023-02-16 12:01:25 UTC+0000
    0x85c53030 WmiApSrv.exe           3004    496      6      112      0      0 2023-02-16 12:01:30 UTC+0000
    0x85c596c0 TrueCrypt.exe          3196   1384      2       67      1      0 2023-02-16 12:02:07 UTC+0000
    0x84d54d20 sppsvc.exe             3736    496      6      154      0      0 2023-02-16 12:03:05 UTC+0000
    0x84d567f0 svchost.exe            3776    496     15      353      0      0 2023-02-16 12:03:05 UTC+0000
    0x844fcd20 DumpIt.exe             4072   1384      2       38      1      0 2023-02-16 12:03:14 UTC+0000
    0x844ba6e0 conhost.exe            4080    400      2       51      1      0 2023-02-16 12:03:14 UTC+0000
    ```
    重點：`0x85c596c0 TrueCrypt.exe          3196   1384      2       67      1      0 2023-02-16 12:02:07 UTC+0000`
    [TrueCrypt - Wiki](https://zh.wikipedia.org/zh-tw/TrueCrypt)
    > TrueCrypt是一款已停止開發的動態（On-the-fly）磁碟加密軟體，支援Windows、macOS和Linux作業系統。它可在單個檔案和磁碟分割區中建立加密區，也可以加密整個作業系統，解密後使用者即可像普通分割區一樣使用其中的檔案。TrueCrypt支援使用密碼、金鑰檔案作為解密憑據。 
3. 取得密碼
    用volatility 2的plugin(目前好像只有Ver. 2有這個plugin)
    ```bash
    $ python ../../Software/CTF/Misc/volatility/vol.py -f dump.raw --profile=Win7SP0x86 truecryptsummary
    Volatility Foundation Volatility Framework 2.6.1
    Registry Version     TrueCrypt Version 7.0a
    Password             Strooooong_Passwword at offset 0x8d23de44
    Process              TrueCrypt.exe at 0x85c596c0 pid 3196
    Service              truecrypt state SERVICE_RUNNING
    Kernel Module        truecrypt.sys at 0x8d20a000 - 0x8d241000
    Symbolic Link        Volume{a2e4e949-a9a8-11ed-859c-50eb71124999} -> \Device\TrueCryptVolumeZ mounted 2023-02-16 12:02:56 UTC+0000
    Driver               \Driver\truecrypt at 0x3f02fc98 range 0x8d20a000 - 0x8d240980
    Device               TrueCrypt at 0x84e2a9d8 type FILE_DEVICE_UNKNOWN
    ```

Flag: `crew{Strooooong_Passwword}`
    
## Reference
[^CTFTime_WP]:[CTFTime - Encrypt10n](https://ctftime.org/writeup/37415)