---
title: CyberDefender - BlackEnergy
tags: [CyberDefender, Endpoint Forensics]

category: "Security/Practice/CyberDefender/Endpoint Forensic"
---

# CyberDefender - BlackEnergy
:::spoiler TOC
[TOC]
:::
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/99

## Scenario
> A multinational corporation has been hit by a cyber attack that has led to the theft of sensitive data. The attack was carried out using a variant of the BlackEnergy v2 malware that has never been seen before. The company's security team has acquired a memory dump of the infected machine, and they want you, as a soc analyst, to analyze the dump to understand the attack scope and impact.

## ==Q1==
> Which volatility profile would be best for this machine?

### Exploit
就是起手式:
```bash
$ ./volatility_2.6_win64_standalone.exe -f CYBERDEF-567078-20230213-171333.raw imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : WinXPSP2x86, WinXPSP3x86 (Instantiated with WinXPSP2x86)
                     AS Layer1 : IA32PagedMemory (Kernel AS)
                     AS Layer2 : FileAddressSpace (D:\NTU\CTF\CyberDefenders\BlackEnergy\CYBERDEF-567078-20230213-171333.raw)
                      PAE type : No PAE
                           DTB : 0x39000L
                          KDBG : 0x8054cde0L
          Number of Processors : 1
     Image Type (Service Pack) : 3
                KPCR for CPU 0 : 0xffdff000L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2023-02-13 18:29:11 UTC+0000
     Image local date and time : 2023-02-13 10:29:11 -0800
```

:::spoiler Flag
Flag: `WinXPSP2x86`
:::

## ==Q2==
> How many processes were running when the image was acquired? 

### Exploit
直覺是pslist，然後扣掉exit的那些process，就是答案
```bash
$ ./volatility_2.6_win64_standalone.exe -f CYBERDEF-567078-20230213-171333.raw pslist
Volatility Foundation Volatility Framework 2.6
Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit
---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0x89c037f8 System                    4      0     55      245 ------      0
0x89965020 smss.exe                368      4      3       19 ------      0 2023-02-14 04:54:15 UTC+0000
0x89a98da0 csrss.exe               592    368     11      321      0      0 2023-02-14 04:54:15 UTC+0000
0x89a88da0 winlogon.exe            616    368     18      508      0      0 2023-02-14 04:54:15 UTC+0000
0x89938998 services.exe            660    616     15      240      0      0 2023-02-14 04:54:15 UTC+0000
0x89aa0020 lsass.exe               672    616     21      335      0      0 2023-02-14 04:54:15 UTC+0000
0x89aaa3d8 VBoxService.exe         832    660      9      115      0      0 2023-02-14 04:54:15 UTC+0000
0x89aab590 svchost.exe             880    660     21      295      0      0 2023-02-13 17:54:16 UTC+0000
0x89a9f6f8 svchost.exe             968    660     10      244      0      0 2023-02-13 17:54:17 UTC+0000
0x89730da0 svchost.exe            1060    660     51     1072      0      0 2023-02-13 17:54:17 UTC+0000
0x897289a8 svchost.exe            1108    660      5       78      0      0 2023-02-13 17:54:17 UTC+0000
0x899adda0 svchost.exe            1156    660     13      192      0      0 2023-02-13 17:54:17 UTC+0000
0x89733938 explorer.exe           1484   1440     14      489      0      0 2023-02-13 17:54:18 UTC+0000
0x897075d0 spoolsv.exe            1608    660     10      106      0      0 2023-02-13 17:54:18 UTC+0000
0x89694388 wscntfy.exe             480   1060      1       28      0      0 2023-02-13 17:54:30 UTC+0000
0x8969d2a0 alg.exe                 540    660      5      102      0      0 2023-02-13 17:54:30 UTC+0000
0x89982da0 VBoxTray.exe            376   1484     13      125      0      0 2023-02-13 17:54:30 UTC+0000
0x8994a020 msmsgs.exe              636   1484      2      157      0      0 2023-02-13 17:54:30 UTC+0000
0x89a0b2f0 taskmgr.exe            1880   1484      0 --------      0      0 2023-02-13 18:25:15 UTC+0000   2023-02-13 18:26:21 UTC+0000
0x899dd740 rootkit.exe             964   1484      0 --------      0      0 2023-02-13 18:25:26 UTC+0000   2023-02-13 18:25:26 UTC+0000
0x89a18da0 cmd.exe                1960    964      0 --------      0      0 2023-02-13 18:25:26 UTC+0000   2023-02-13 18:25:26 UTC+0000
0x896c5020 notepad.exe             528   1484      0 --------      0      0 2023-02-13 18:26:55 UTC+0000   2023-02-13 18:27:46 UTC+0000
0x89a0d180 notepad.exe            1432   1484      0 --------      0      0 2023-02-13 18:28:25 UTC+0000   2023-02-13 18:28:40 UTC+0000
0x899e6da0 notepad.exe            1444   1484      0 --------      0      0 2023-02-13 18:28:42 UTC+0000   2023-02-13 18:28:47 UTC+0000
0x89a0fda0 DumpIt.exe              276   1484      1       25      0      0 2023-02-13 18:29:08 UTC+0000
```

:::spoiler Flag
Flag: `19`
:::

## ==Q3==
> What is the process ID of cmd.exe? 

### Exploit
呈上題

:::spoiler Flag
Flag: `1960`
:::

## ==Q4==
> What is the name of the most suspicious process? 

### Exploit
呈第3題，感覺這個process應該就是提權的工具

:::spoiler Flag
Flag: `rootkit.exe`
:::

## ==Q5==
> Which process shows the highest likelihood of code injection? 

### Exploit
直覺會看`malfind`，然後找相關的process
:::spoiler malfind result
```bash
$ ./volatility_2.6_win64_standalone.exe -f CYBERDEF-567078-20230213-171333.raw malfind
Volatility Foundation Volatility Framework 2.6
Process: csrss.exe Pid: 592 Address: 0x7f6f0000
Vad Tag: Vad  Protection: PAGE_EXECUTE_READWRITE
Flags: Protection: 6

0x7f6f0000  c8 00 00 00 84 01 00 00 ff ee ff ee 08 70 00 00   .............p..
0x7f6f0010  08 00 00 00 00 fe 00 00 00 00 10 00 00 20 00 00   ................
0x7f6f0020  00 02 00 00 00 20 00 00 8d 01 00 00 ff ef fd 7f   ................
0x7f6f0030  03 00 08 06 00 00 00 00 00 00 00 00 00 00 00 00   ................

0x7f6f0000 c8000000         ENTER 0x0, 0x0
0x7f6f0004 8401             TEST [ECX], AL
0x7f6f0006 0000             ADD [EAX], AL
0x7f6f0008 ff               DB 0xff
0x7f6f0009 ee               OUT DX, AL
0x7f6f000a ff               DB 0xff
0x7f6f000b ee               OUT DX, AL
0x7f6f000c 087000           OR [EAX+0x0], DH
0x7f6f000f 0008             ADD [EAX], CL
0x7f6f0011 0000             ADD [EAX], AL
0x7f6f0013 0000             ADD [EAX], AL
0x7f6f0015 fe00             INC BYTE [EAX]
0x7f6f0017 0000             ADD [EAX], AL
0x7f6f0019 0010             ADD [EAX], DL
0x7f6f001b 0000             ADD [EAX], AL
0x7f6f001d 2000             AND [EAX], AL
0x7f6f001f 0000             ADD [EAX], AL
0x7f6f0021 0200             ADD AL, [EAX]
0x7f6f0023 0000             ADD [EAX], AL
0x7f6f0025 2000             AND [EAX], AL
0x7f6f0027 008d010000ff     ADD [EBP-0xffffff], CL
0x7f6f002d ef               OUT DX, EAX
0x7f6f002e fd               STD
0x7f6f002f 7f03             JG 0x7f6f0034
0x7f6f0031 0008             ADD [EAX], CL
0x7f6f0033 06               PUSH ES
0x7f6f0034 0000             ADD [EAX], AL
0x7f6f0036 0000             ADD [EAX], AL
0x7f6f0038 0000             ADD [EAX], AL
0x7f6f003a 0000             ADD [EAX], AL
0x7f6f003c 0000             ADD [EAX], AL
0x7f6f003e 0000             ADD [EAX], AL

Process: winlogon.exe Pid: 616 Address: 0x4a5e0000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 4, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x4a5e0000  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x4a5e0010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x4a5e0020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x4a5e0030  00 00 00 00 25 00 25 00 01 00 00 00 00 00 00 00   ....%.%.........

0x4a5e0000 0000             ADD [EAX], AL
0x4a5e0002 0000             ADD [EAX], AL
0x4a5e0004 0000             ADD [EAX], AL
0x4a5e0006 0000             ADD [EAX], AL
0x4a5e0008 0000             ADD [EAX], AL
0x4a5e000a 0000             ADD [EAX], AL
0x4a5e000c 0000             ADD [EAX], AL
0x4a5e000e 0000             ADD [EAX], AL
0x4a5e0010 0000             ADD [EAX], AL
0x4a5e0012 0000             ADD [EAX], AL
0x4a5e0014 0000             ADD [EAX], AL
0x4a5e0016 0000             ADD [EAX], AL
0x4a5e0018 0000             ADD [EAX], AL
0x4a5e001a 0000             ADD [EAX], AL
0x4a5e001c 0000             ADD [EAX], AL
0x4a5e001e 0000             ADD [EAX], AL
0x4a5e0020 0000             ADD [EAX], AL
0x4a5e0022 0000             ADD [EAX], AL
0x4a5e0024 0000             ADD [EAX], AL
0x4a5e0026 0000             ADD [EAX], AL
0x4a5e0028 0000             ADD [EAX], AL
0x4a5e002a 0000             ADD [EAX], AL
0x4a5e002c 0000             ADD [EAX], AL
0x4a5e002e 0000             ADD [EAX], AL
0x4a5e0030 0000             ADD [EAX], AL
0x4a5e0032 0000             ADD [EAX], AL
0x4a5e0034 2500250001       AND EAX, 0x1002500
0x4a5e0039 0000             ADD [EAX], AL
0x4a5e003b 0000             ADD [EAX], AL
0x4a5e003d 0000             ADD [EAX], AL
0x4a5e003f 00               DB 0x0

Process: winlogon.exe Pid: 616 Address: 0x2afc0000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 4, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x2afc0000  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x2afc0010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x2afc0020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x2afc0030  00 00 00 00 23 00 23 00 01 00 00 00 00 00 00 00   ....#.#.........

0x2afc0000 0000             ADD [EAX], AL
0x2afc0002 0000             ADD [EAX], AL
0x2afc0004 0000             ADD [EAX], AL
0x2afc0006 0000             ADD [EAX], AL
0x2afc0008 0000             ADD [EAX], AL
0x2afc000a 0000             ADD [EAX], AL
0x2afc000c 0000             ADD [EAX], AL
0x2afc000e 0000             ADD [EAX], AL
0x2afc0010 0000             ADD [EAX], AL
0x2afc0012 0000             ADD [EAX], AL
0x2afc0014 0000             ADD [EAX], AL
0x2afc0016 0000             ADD [EAX], AL
0x2afc0018 0000             ADD [EAX], AL
0x2afc001a 0000             ADD [EAX], AL
0x2afc001c 0000             ADD [EAX], AL
0x2afc001e 0000             ADD [EAX], AL
0x2afc0020 0000             ADD [EAX], AL
0x2afc0022 0000             ADD [EAX], AL
0x2afc0024 0000             ADD [EAX], AL
0x2afc0026 0000             ADD [EAX], AL
0x2afc0028 0000             ADD [EAX], AL
0x2afc002a 0000             ADD [EAX], AL
0x2afc002c 0000             ADD [EAX], AL
0x2afc002e 0000             ADD [EAX], AL
0x2afc0030 0000             ADD [EAX], AL
0x2afc0032 0000             ADD [EAX], AL
0x2afc0034 2300             AND EAX, [EAX]
0x2afc0036 2300             AND EAX, [EAX]
0x2afc0038 0100             ADD [EAX], EAX
0x2afc003a 0000             ADD [EAX], AL
0x2afc003c 0000             ADD [EAX], AL
0x2afc003e 0000             ADD [EAX], AL

Process: winlogon.exe Pid: 616 Address: 0xe880000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 4, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x0e880000  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x0e880010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x0e880020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x0e880030  00 00 00 00 25 00 25 00 01 00 00 00 00 00 00 00   ....%.%.........

0x0e880000 0000             ADD [EAX], AL
0x0e880002 0000             ADD [EAX], AL
0x0e880004 0000             ADD [EAX], AL
0x0e880006 0000             ADD [EAX], AL
0x0e880008 0000             ADD [EAX], AL
0x0e88000a 0000             ADD [EAX], AL
0x0e88000c 0000             ADD [EAX], AL
0x0e88000e 0000             ADD [EAX], AL
0x0e880010 0000             ADD [EAX], AL
0x0e880012 0000             ADD [EAX], AL
0x0e880014 0000             ADD [EAX], AL
0x0e880016 0000             ADD [EAX], AL
0x0e880018 0000             ADD [EAX], AL
0x0e88001a 0000             ADD [EAX], AL
0x0e88001c 0000             ADD [EAX], AL
0x0e88001e 0000             ADD [EAX], AL
0x0e880020 0000             ADD [EAX], AL
0x0e880022 0000             ADD [EAX], AL
0x0e880024 0000             ADD [EAX], AL
0x0e880026 0000             ADD [EAX], AL
0x0e880028 0000             ADD [EAX], AL
0x0e88002a 0000             ADD [EAX], AL
0x0e88002c 0000             ADD [EAX], AL
0x0e88002e 0000             ADD [EAX], AL
0x0e880030 0000             ADD [EAX], AL
0x0e880032 0000             ADD [EAX], AL
0x0e880034 2500250001       AND EAX, 0x1002500
0x0e880039 0000             ADD [EAX], AL
0x0e88003b 0000             ADD [EAX], AL
0x0e88003d 0000             ADD [EAX], AL
0x0e88003f 00               DB 0x0

Process: winlogon.exe Pid: 616 Address: 0x16be0000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 4, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x16be0000  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x16be0010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x16be0020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x16be0030  00 00 00 00 28 00 28 00 01 00 00 00 00 00 00 00   ....(.(.........

0x16be0000 0000             ADD [EAX], AL
0x16be0002 0000             ADD [EAX], AL
0x16be0004 0000             ADD [EAX], AL
0x16be0006 0000             ADD [EAX], AL
0x16be0008 0000             ADD [EAX], AL
0x16be000a 0000             ADD [EAX], AL
0x16be000c 0000             ADD [EAX], AL
0x16be000e 0000             ADD [EAX], AL
0x16be0010 0000             ADD [EAX], AL
0x16be0012 0000             ADD [EAX], AL
0x16be0014 0000             ADD [EAX], AL
0x16be0016 0000             ADD [EAX], AL
0x16be0018 0000             ADD [EAX], AL
0x16be001a 0000             ADD [EAX], AL
0x16be001c 0000             ADD [EAX], AL
0x16be001e 0000             ADD [EAX], AL
0x16be0020 0000             ADD [EAX], AL
0x16be0022 0000             ADD [EAX], AL
0x16be0024 0000             ADD [EAX], AL
0x16be0026 0000             ADD [EAX], AL
0x16be0028 0000             ADD [EAX], AL
0x16be002a 0000             ADD [EAX], AL
0x16be002c 0000             ADD [EAX], AL
0x16be002e 0000             ADD [EAX], AL
0x16be0030 0000             ADD [EAX], AL
0x16be0032 0000             ADD [EAX], AL
0x16be0034 2800             SUB [EAX], AL
0x16be0036 2800             SUB [EAX], AL
0x16be0038 0100             ADD [EAX], EAX
0x16be003a 0000             ADD [EAX], AL
0x16be003c 0000             ADD [EAX], AL
0x16be003e 0000             ADD [EAX], AL

Process: winlogon.exe Pid: 616 Address: 0x2b010000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 4, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x2b010000  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x2b010010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x2b010020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x2b010030  00 00 00 00 2c 00 2c 00 01 00 00 00 00 00 00 00   ....,.,.........

0x2b010000 0000             ADD [EAX], AL
0x2b010002 0000             ADD [EAX], AL
0x2b010004 0000             ADD [EAX], AL
0x2b010006 0000             ADD [EAX], AL
0x2b010008 0000             ADD [EAX], AL
0x2b01000a 0000             ADD [EAX], AL
0x2b01000c 0000             ADD [EAX], AL
0x2b01000e 0000             ADD [EAX], AL
0x2b010010 0000             ADD [EAX], AL
0x2b010012 0000             ADD [EAX], AL
0x2b010014 0000             ADD [EAX], AL
0x2b010016 0000             ADD [EAX], AL
0x2b010018 0000             ADD [EAX], AL
0x2b01001a 0000             ADD [EAX], AL
0x2b01001c 0000             ADD [EAX], AL
0x2b01001e 0000             ADD [EAX], AL
0x2b010020 0000             ADD [EAX], AL
0x2b010022 0000             ADD [EAX], AL
0x2b010024 0000             ADD [EAX], AL
0x2b010026 0000             ADD [EAX], AL
0x2b010028 0000             ADD [EAX], AL
0x2b01002a 0000             ADD [EAX], AL
0x2b01002c 0000             ADD [EAX], AL
0x2b01002e 0000             ADD [EAX], AL
0x2b010030 0000             ADD [EAX], AL
0x2b010032 0000             ADD [EAX], AL
0x2b010034 2c00             SUB AL, 0x0
0x2b010036 2c00             SUB AL, 0x0
0x2b010038 0100             ADD [EAX], EAX
0x2b01003a 0000             ADD [EAX], AL
0x2b01003c 0000             ADD [EAX], AL
0x2b01003e 0000             ADD [EAX], AL

Process: winlogon.exe Pid: 616 Address: 0x3ad10000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 4, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x3ad10000  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x3ad10010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x3ad10020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x3ad10030  00 00 00 00 25 00 25 00 01 00 00 00 00 00 00 00   ....%.%.........

0x3ad10000 0000             ADD [EAX], AL
0x3ad10002 0000             ADD [EAX], AL
0x3ad10004 0000             ADD [EAX], AL
0x3ad10006 0000             ADD [EAX], AL
0x3ad10008 0000             ADD [EAX], AL
0x3ad1000a 0000             ADD [EAX], AL
0x3ad1000c 0000             ADD [EAX], AL
0x3ad1000e 0000             ADD [EAX], AL
0x3ad10010 0000             ADD [EAX], AL
0x3ad10012 0000             ADD [EAX], AL
0x3ad10014 0000             ADD [EAX], AL
0x3ad10016 0000             ADD [EAX], AL
0x3ad10018 0000             ADD [EAX], AL
0x3ad1001a 0000             ADD [EAX], AL
0x3ad1001c 0000             ADD [EAX], AL
0x3ad1001e 0000             ADD [EAX], AL
0x3ad10020 0000             ADD [EAX], AL
0x3ad10022 0000             ADD [EAX], AL
0x3ad10024 0000             ADD [EAX], AL
0x3ad10026 0000             ADD [EAX], AL
0x3ad10028 0000             ADD [EAX], AL
0x3ad1002a 0000             ADD [EAX], AL
0x3ad1002c 0000             ADD [EAX], AL
0x3ad1002e 0000             ADD [EAX], AL
0x3ad10030 0000             ADD [EAX], AL
0x3ad10032 0000             ADD [EAX], AL
0x3ad10034 2500250001       AND EAX, 0x1002500
0x3ad10039 0000             ADD [EAX], AL
0x3ad1003b 0000             ADD [EAX], AL
0x3ad1003d 0000             ADD [EAX], AL
0x3ad1003f 00               DB 0x0

Process: winlogon.exe Pid: 616 Address: 0x3f750000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 4, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x3f750000  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x3f750010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x3f750020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x3f750030  00 00 00 00 27 00 27 00 01 00 00 00 00 00 00 00   ....'.'.........

0x3f750000 0000             ADD [EAX], AL
0x3f750002 0000             ADD [EAX], AL
0x3f750004 0000             ADD [EAX], AL
0x3f750006 0000             ADD [EAX], AL
0x3f750008 0000             ADD [EAX], AL
0x3f75000a 0000             ADD [EAX], AL
0x3f75000c 0000             ADD [EAX], AL
0x3f75000e 0000             ADD [EAX], AL
0x3f750010 0000             ADD [EAX], AL
0x3f750012 0000             ADD [EAX], AL
0x3f750014 0000             ADD [EAX], AL
0x3f750016 0000             ADD [EAX], AL
0x3f750018 0000             ADD [EAX], AL
0x3f75001a 0000             ADD [EAX], AL
0x3f75001c 0000             ADD [EAX], AL
0x3f75001e 0000             ADD [EAX], AL
0x3f750020 0000             ADD [EAX], AL
0x3f750022 0000             ADD [EAX], AL
0x3f750024 0000             ADD [EAX], AL
0x3f750026 0000             ADD [EAX], AL
0x3f750028 0000             ADD [EAX], AL
0x3f75002a 0000             ADD [EAX], AL
0x3f75002c 0000             ADD [EAX], AL
0x3f75002e 0000             ADD [EAX], AL
0x3f750030 0000             ADD [EAX], AL
0x3f750032 0000             ADD [EAX], AL
0x3f750034 27               DAA
0x3f750035 0027             ADD [EDI], AH
0x3f750037 0001             ADD [ECX], AL
0x3f750039 0000             ADD [EAX], AL
0x3f75003b 0000             ADD [EAX], AL
0x3f75003d 0000             ADD [EAX], AL
0x3f75003f 00               DB 0x0

Process: winlogon.exe Pid: 616 Address: 0x5d080000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 4, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x5d080000  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x5d080010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x5d080020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x5d080030  00 00 00 00 28 00 28 00 01 00 00 00 00 00 00 00   ....(.(.........

0x5d080000 0000             ADD [EAX], AL
0x5d080002 0000             ADD [EAX], AL
0x5d080004 0000             ADD [EAX], AL
0x5d080006 0000             ADD [EAX], AL
0x5d080008 0000             ADD [EAX], AL
0x5d08000a 0000             ADD [EAX], AL
0x5d08000c 0000             ADD [EAX], AL
0x5d08000e 0000             ADD [EAX], AL
0x5d080010 0000             ADD [EAX], AL
0x5d080012 0000             ADD [EAX], AL
0x5d080014 0000             ADD [EAX], AL
0x5d080016 0000             ADD [EAX], AL
0x5d080018 0000             ADD [EAX], AL
0x5d08001a 0000             ADD [EAX], AL
0x5d08001c 0000             ADD [EAX], AL
0x5d08001e 0000             ADD [EAX], AL
0x5d080020 0000             ADD [EAX], AL
0x5d080022 0000             ADD [EAX], AL
0x5d080024 0000             ADD [EAX], AL
0x5d080026 0000             ADD [EAX], AL
0x5d080028 0000             ADD [EAX], AL
0x5d08002a 0000             ADD [EAX], AL
0x5d08002c 0000             ADD [EAX], AL
0x5d08002e 0000             ADD [EAX], AL
0x5d080030 0000             ADD [EAX], AL
0x5d080032 0000             ADD [EAX], AL
0x5d080034 2800             SUB [EAX], AL
0x5d080036 2800             SUB [EAX], AL
0x5d080038 0100             ADD [EAX], EAX
0x5d08003a 0000             ADD [EAX], AL
0x5d08003c 0000             ADD [EAX], AL
0x5d08003e 0000             ADD [EAX], AL

Process: winlogon.exe Pid: 616 Address: 0x62220000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 4, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x62220000  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x62220010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x62220020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x62220030  00 00 00 00 2a 00 2a 00 01 00 00 00 00 00 00 00   ....*.*.........

0x62220000 0000             ADD [EAX], AL
0x62220002 0000             ADD [EAX], AL
0x62220004 0000             ADD [EAX], AL
0x62220006 0000             ADD [EAX], AL
0x62220008 0000             ADD [EAX], AL
0x6222000a 0000             ADD [EAX], AL
0x6222000c 0000             ADD [EAX], AL
0x6222000e 0000             ADD [EAX], AL
0x62220010 0000             ADD [EAX], AL
0x62220012 0000             ADD [EAX], AL
0x62220014 0000             ADD [EAX], AL
0x62220016 0000             ADD [EAX], AL
0x62220018 0000             ADD [EAX], AL
0x6222001a 0000             ADD [EAX], AL
0x6222001c 0000             ADD [EAX], AL
0x6222001e 0000             ADD [EAX], AL
0x62220020 0000             ADD [EAX], AL
0x62220022 0000             ADD [EAX], AL
0x62220024 0000             ADD [EAX], AL
0x62220026 0000             ADD [EAX], AL
0x62220028 0000             ADD [EAX], AL
0x6222002a 0000             ADD [EAX], AL
0x6222002c 0000             ADD [EAX], AL
0x6222002e 0000             ADD [EAX], AL
0x62220030 0000             ADD [EAX], AL
0x62220032 0000             ADD [EAX], AL
0x62220034 2a00             SUB AL, [EAX]
0x62220036 2a00             SUB AL, [EAX]
0x62220038 0100             ADD [EAX], EAX
0x6222003a 0000             ADD [EAX], AL
0x6222003c 0000             ADD [EAX], AL
0x6222003e 0000             ADD [EAX], AL

Process: svchost.exe Pid: 880 Address: 0x980000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 9, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x00980000  4d 5a 90 00 03 00 00 00 04 00 00 00 ff ff 00 00   MZ..............
0x00980010  b8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00   ........@.......
0x00980020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x00980030  00 00 00 00 00 00 00 00 00 00 00 00 f8 00 00 00   ................

0x00980000 4d               DEC EBP
0x00980001 5a               POP EDX
0x00980002 90               NOP
0x00980003 0003             ADD [EBX], AL
0x00980005 0000             ADD [EAX], AL
0x00980007 000400           ADD [EAX+EAX], AL
0x0098000a 0000             ADD [EAX], AL
0x0098000c ff               DB 0xff
0x0098000d ff00             INC DWORD [EAX]
0x0098000f 00b800000000     ADD [EAX+0x0], BH
0x00980015 0000             ADD [EAX], AL
0x00980017 004000           ADD [EAX+0x0], AL
0x0098001a 0000             ADD [EAX], AL
0x0098001c 0000             ADD [EAX], AL
0x0098001e 0000             ADD [EAX], AL
0x00980020 0000             ADD [EAX], AL
0x00980022 0000             ADD [EAX], AL
0x00980024 0000             ADD [EAX], AL
0x00980026 0000             ADD [EAX], AL
0x00980028 0000             ADD [EAX], AL
0x0098002a 0000             ADD [EAX], AL
0x0098002c 0000             ADD [EAX], AL
0x0098002e 0000             ADD [EAX], AL
0x00980030 0000             ADD [EAX], AL
0x00980032 0000             ADD [EAX], AL
0x00980034 0000             ADD [EAX], AL
0x00980036 0000             ADD [EAX], AL
0x00980038 0000             ADD [EAX], AL
0x0098003a 0000             ADD [EAX], AL
0x0098003c f8               CLC
0x0098003d 0000             ADD [EAX], AL
0x0098003f 00               DB 0x0
```
:::

:::spoiler Flag
Flag: `svchost.exe`
:::

## ==Q6==
> There is an odd file referenced in the recent process. Provide the full path of that file. 

### Exploit
這一題是靠賽出來的，所以還是參考[^wp]比較正常的解法，從上一題已經知道svchost.exe是已經被注入的process，所以我們可以把已經注入過的process dump出來，因為已經很久沒有做相關的題目所以有點卡，如果直接procdump的話是直接把沒有注入過且完整的process dump下來，放到virustotal只會一堆綠，所以要做的應該是malfind搭配dump才對，接著再去分析裡面的strings
```bash
$ ./volatility_2.6_win64_standalone.exe -f CYBERDEF-567078-20230213-171333.raw --profile WinXPSP2x86 malfind --pid 880 --dump-dir="./Exported Files/"
$ strings ./Exported\ Files/process.0x89aab590.0x980000.dmp -n 15
!This program cannot be run in DOS mode.
{3D5A1694-CC2C-4ee7-A3D5-A879A9E3A623}
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
Content-Type: application/x-www-form-urlencoded
DispatchCommand
GetCurrentProcessId
CoCreateInstance
InterlockedExchange
ConfAllocGetTextByNameA
ConfAllocGetTextByNameW
ConfGetListNodeByName
ConfGetNodeByName
ConfGetNodeTextA
ConfGetNodeTextW
ConfGetRootNode
RkLoadKernelImage
RkProtectObject
SrvAddRequestBinaryData
SrvAddRequestStringData
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@>@@@?456789:;<=@@@@@@@
 !"#$%&'()*+,-./0123@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@q
xCYBERDEF-567078_40BF25D3
C:\WINDOWS\system32\drivers\str.sys
</=(>@>G>O>T>X>\>
        030e0l0p0t0x0|0
```

:::spoiler Flag
Flag: `C:\WINDOWS\system32\drivers\str.sys`
:::

## ==Q7==
> What is the name of the injected dll file loaded from the recent process? 

### Recon
這一題完全沒有想法，同樣是參考[^wp]，學到一個新東西，不過思路差不多，我是想如果可以利用dlllist直接看pid 880 load進甚麼樣的dll就可以篩選出正確的答案，不過有一個新的plugin更強，叫做==ldrmodules==
> The ldrmodules plugin can be used to list the loaded modules (DLLs) in a process, and it can also be used to detect unlinked/hidden DLLs. We can use this plugin to examine the malicious svchost.exe process, which has a PID of 880.

如果比對我的方法和[^wp]的方法會發現就是只有差在答案的那一個dll沒有顯示出來而已

### Exploit
:::spoiler dlllist (我的方法)
```bash
$ ./volatility_2.6_win64_standalone.exe -f CYBERDEF-567078-20230213-171333.raw --profile WinXPSP2x86 dlllist --pid 880
************************************************************************
svchost.exe pid:    880
Command line : C:\WINDOWS\system32\svchost -k DcomLaunch
Service Pack 3

Base             Size  LoadCount Path
---------- ---------- ---------- ----
0x01000000     0x6000     0xffff C:\WINDOWS\system32\svchost.exe
0x7c900000    0xaf000     0xffff C:\WINDOWS\system32\ntdll.dll
0x7c800000    0xf6000     0xffff C:\WINDOWS\system32\Kernel32.dll
0x77dd0000    0x9b000     0xffff C:\WINDOWS\system32\ADVAPI32.dll
0x77e70000    0x92000     0xffff C:\WINDOWS\system32\RPCRT4.dll
0x77fe0000    0x11000     0xffff C:\WINDOWS\system32\Secur32.dll
0x5cb70000    0x26000        0x1 C:\WINDOWS\system32\ShimEng.dll
0x6f880000   0x1ca000        0x1 C:\WINDOWS\AppPatch\AcGenral.DLL
0x7e410000    0x91000      0x34c C:\WINDOWS\system32\USER32.dll
0x77f10000    0x49000      0x1f6 C:\WINDOWS\system32\GDI32.dll
0x76b40000    0x2d000        0x4 C:\WINDOWS\system32\WINMM.dll
0x774e0000   0x13d000       0x7e C:\WINDOWS\system32\ole32.dll
0x77c10000    0x58000      0x2ee C:\WINDOWS\system32\msvcrt.dll
0x77120000    0x8b000       0x74 C:\WINDOWS\system32\OLEAUT32.dll
0x77be0000    0x15000        0x1 C:\WINDOWS\system32\MSACM32.dll
0x77c00000     0x8000        0x7 C:\WINDOWS\system32\VERSION.dll
0x7c9c0000   0x817000        0x3 C:\WINDOWS\system32\SHELL32.dll
0x77f60000    0x76000       0x76 C:\WINDOWS\system32\SHLWAPI.dll
0x769c0000    0xb4000        0x4 C:\WINDOWS\system32\USERENV.dll
0x5ad70000    0x38000        0x1 C:\WINDOWS\system32\UxTheme.dll
0x773d0000   0x103000        0x4 C:\WINDOWS\WinSxS\x86_Microsoft.Windows.Common-Controls_6595b64144ccf1df_6.0.2600.5512_x-ww_35d4ce83\comctl32.dll
0x5d090000    0x9a000        0x1 C:\WINDOWS\system32\comctl32.dll
0x77690000    0x21000        0x1 C:\WINDOWS\system32\NTMARTA.DLL
0x71bf0000    0x13000        0x1 C:\WINDOWS\system32\SAMLIB.dll
0x76f60000    0x2c000        0x2 C:\WINDOWS\system32\WLDAP32.dll
0x76a80000    0x64000        0x1 c:\windows\system32\rpcss.dll
0x71ab0000    0x17000       0x23 c:\windows\system32\WS2_32.dll
0x71aa0000     0x8000       0x24 c:\windows\system32\WS2HELP.dll
0x00670000   0x2c5000        0x1 C:\WINDOWS\system32\xpsp2res.dll
0x76fd0000    0x7f000        0x4 C:\WINDOWS\system32\CLBCATQ.DLL
0x77050000    0xc5000        0x4 C:\WINDOWS\system32\COMRes.dll
0x760f0000    0x53000        0x1 c:\windows\system32\termsrv.dll
0x74f70000     0x6000        0x1 c:\windows\system32\ICAAPI.dll
0x77920000    0xf3000        0x1 c:\windows\system32\SETUPAPI.dll
0x76c30000    0x2e000        0x1 C:\WINDOWS\system32\WINTRUST.dll
0x77a80000    0x95000       0x6c C:\WINDOWS\system32\CRYPT32.dll
0x77b20000    0x12000       0x6b C:\WINDOWS\system32\MSASN1.dll
0x76c90000    0x28000        0x1 C:\WINDOWS\system32\IMAGEHLP.dll
0x776c0000    0x12000        0x1 c:\windows\system32\AUTHZ.dll
0x75110000    0x1f000        0x1 c:\windows\system32\mstlsapi.dll
0x77cc0000    0x32000        0x1 c:\windows\system32\ACTIVEDS.dll
0x76e10000    0x25000        0x1 c:\windows\system32\adsldpc.dll
0x5b860000    0x55000        0x5 C:\WINDOWS\system32\NETAPI32.dll
0x76b20000    0x11000        0x1 c:\windows\system32\ATL.DLL
0x76bc0000     0xf000        0x1 C:\WINDOWS\system32\REGAPI.dll
0x68000000    0x36000        0x1 C:\WINDOWS\system32\rsaenh.dll
0x74980000   0x113000        0x1 C:\WINDOWS\system32\msxml3.dll
0x771b0000    0xaa000       0x69 C:\WINDOWS\system32\wininet.dll
0x71ad0000     0x9000        0x1 C:\WINDOWS\system32\wsock32.dll
0x76ee0000    0x3c000        0x2 C:\WINDOWS\system32\RASAPI32.DLL
0x76e90000    0x12000        0x2 C:\WINDOWS\system32\rasman.dll
0x76eb0000    0x2f000        0x2 C:\WINDOWS\system32\TAPI32.dll
0x76e80000     0xe000        0x3 C:\WINDOWS\system32\rtutils.dll
0x722b0000     0x5000        0x1 C:\WINDOWS\system32\sensapi.dll
0x7e1e0000    0xa2000        0x1 C:\WINDOWS\system32\urlmon.dll
0x71a50000    0x3f000        0x1 C:\WINDOWS\System32\mswsock.dll
0x76f20000    0x27000        0x1 C:\WINDOWS\system32\DNSAPI.dll
0x76fc0000     0x6000        0x1 C:\WINDOWS\system32\rasadhlp.dll
```
:::

:::spoiler ldrmodules ([^wp]的方法)
```bash
$ ./volatility_2.6_win64_standalone.exe -f CYBERDEF-567078-20230213-171333.raw --profile WinXPSP2x86 ldrmodules --pid 880
Pid      Process              Base       InLoad InInit InMem MappedPath
-------- -------------------- ---------- ------ ------ ----- ----------
     880 svchost.exe          0x6f880000 True   True   True  \WINDOWS\AppPatch\AcGenral.dll
     880 svchost.exe          0x01000000 True   False  True  \WINDOWS\system32\svchost.exe
     880 svchost.exe          0x77f60000 True   True   True  \WINDOWS\system32\shlwapi.dll
     880 svchost.exe          0x74f70000 True   True   True  \WINDOWS\system32\icaapi.dll
     880 svchost.exe          0x76f60000 True   True   True  \WINDOWS\system32\wldap32.dll
     880 svchost.exe          0x77c00000 True   True   True  \WINDOWS\system32\version.dll
     880 svchost.exe          0x5ad70000 True   True   True  \WINDOWS\system32\uxtheme.dll
     880 svchost.exe          0x76e80000 True   True   True  \WINDOWS\system32\rtutils.dll
     880 svchost.exe          0x771b0000 True   True   True  \WINDOWS\system32\wininet.dll
     880 svchost.exe          0x76c90000 True   True   True  \WINDOWS\system32\imagehlp.dll
     880 svchost.exe          0x76bc0000 True   True   True  \WINDOWS\system32\regapi.dll
     880 svchost.exe          0x77dd0000 True   True   True  \WINDOWS\system32\advapi32.dll
     880 svchost.exe          0x76f20000 True   True   True  \WINDOWS\system32\dnsapi.dll
     880 svchost.exe          0x77be0000 True   True   True  \WINDOWS\system32\msacm32.dll
     880 svchost.exe          0x7e1e0000 True   True   True  \WINDOWS\system32\urlmon.dll
     880 svchost.exe          0x68000000 True   True   True  \WINDOWS\system32\rsaenh.dll
     880 svchost.exe          0x722b0000 True   True   True  \WINDOWS\system32\sensapi.dll
     880 svchost.exe          0x76e10000 True   True   True  \WINDOWS\system32\adsldpc.dll
     880 svchost.exe          0x76b40000 True   True   True  \WINDOWS\system32\winmm.dll
     880 svchost.exe          0x773d0000 True   True   True  \WINDOWS\WinSxS\x86_Microsoft.Windows.Common-Controls_6595b64144ccf1df_6.0.2600.5512_x-ww_35d4ce83\comctl32.dll
     880 svchost.exe          0x71a50000 True   True   True  \WINDOWS\system32\mswsock.dll
     880 svchost.exe          0x5b860000 True   True   True  \WINDOWS\system32\netapi32.dll
     880 svchost.exe          0x00670000 True   True   True  \WINDOWS\system32\xpsp2res.dll
     880 svchost.exe          0x76e90000 True   True   True  \WINDOWS\system32\rasman.dll
     880 svchost.exe          0x77a80000 True   True   True  \WINDOWS\system32\crypt32.dll
     880 svchost.exe          0x71ab0000 True   True   True  \WINDOWS\system32\ws2_32.dll
     880 svchost.exe          0x77cc0000 True   True   True  \WINDOWS\system32\activeds.dll
     880 svchost.exe          0x71ad0000 True   True   True  \WINDOWS\system32\wsock32.dll
     880 svchost.exe          0x774e0000 True   True   True  \WINDOWS\system32\ole32.dll
     880 svchost.exe          0x77920000 True   True   True  \WINDOWS\system32\setupapi.dll
     880 svchost.exe          0x7e410000 True   True   True  \WINDOWS\system32\user32.dll
     880 svchost.exe          0x7c900000 True   True   True  \WINDOWS\system32\ntdll.dll
     880 svchost.exe          0x77f10000 True   True   True  \WINDOWS\system32\gdi32.dll
     880 svchost.exe          0x77120000 True   True   True  \WINDOWS\system32\oleaut32.dll
     880 svchost.exe          0x5cb70000 True   True   True  \WINDOWS\system32\shimeng.dll
     880 svchost.exe          0x74980000 True   True   True  \WINDOWS\system32\msxml3.dll
     880 svchost.exe          0x009a0000 False  False  False \WINDOWS\system32\msxml3r.dll
     880 svchost.exe          0x77e70000 True   True   True  \WINDOWS\system32\rpcrt4.dll
     880 svchost.exe          0x769c0000 True   True   True  \WINDOWS\system32\userenv.dll
     880 svchost.exe          0x7c800000 True   True   True  \WINDOWS\system32\Kernel32.dll
     880 svchost.exe          0x76fd0000 True   True   True  \WINDOWS\system32\clbcatq.dll
     880 svchost.exe          0x76b20000 True   True   True  \WINDOWS\system32\atl.dll
     880 svchost.exe          0x71bf0000 True   True   True  \WINDOWS\system32\samlib.dll
     880 svchost.exe          0x77690000 True   True   True  \WINDOWS\system32\ntmarta.dll
     880 svchost.exe          0x77c10000 True   True   True  \WINDOWS\system32\msvcrt.dll
     880 svchost.exe          0x760f0000 True   True   True  \WINDOWS\system32\termsrv.dll
     880 svchost.exe          0x76fc0000 True   True   True  \WINDOWS\system32\rasadhlp.dll
     880 svchost.exe          0x76c30000 True   True   True  \WINDOWS\system32\wintrust.dll
     880 svchost.exe          0x7c9c0000 True   True   True  \WINDOWS\system32\shell32.dll
     880 svchost.exe          0x77050000 True   True   True  \WINDOWS\system32\comres.dll
     880 svchost.exe          0x76eb0000 True   True   True  \WINDOWS\system32\tapi32.dll
     880 svchost.exe          0x76a80000 True   True   True  \WINDOWS\system32\rpcss.dll
     880 svchost.exe          0x5d090000 True   True   True  \WINDOWS\system32\comctl32.dll
     880 svchost.exe          0x71aa0000 True   True   True  \WINDOWS\system32\ws2help.dll
     880 svchost.exe          0x776c0000 True   True   True  \WINDOWS\system32\authz.dll
     880 svchost.exe          0x76ee0000 True   True   True  \WINDOWS\system32\rasapi32.dll
     880 svchost.exe          0x77b20000 True   True   True  \WINDOWS\system32\msasn1.dll
     880 svchost.exe          0x75110000 True   True   True  \WINDOWS\system32\mstlsapi.dll
     880 svchost.exe          0x77fe0000 True   True   True  \WINDOWS\system32\secur32.dll
```
:::
可以看到==msxml3r.dll==的三種狀態都是False，代表這個dll不在已經load的memory中，也不在初始化的階段，更不在目前的process memory中，意味著別的工具試圖隱藏該dll

:::spoiler Flag
Flag: `msxml3r.dll`
:::

## ==Q8==
> What is the base address of the injected dll?

### Exploit
承接第六題，知道malfind之後，他會顯示base address
```bash
$ ./volatility_2.6_win64_standalone.exe -f CYBERDEF-567078-20230213-171333.raw --profile WinXPSP2x86 malfind --pid 880 --dump-dir="
./Exported Files/"
Volatility Foundation Volatility Framework 2.6
Process: svchost.exe Pid: 880 Address: 0x980000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: CommitCharge: 9, MemCommit: 1, PrivateMemory: 1, Protection: 6

0x00980000  4d 5a 90 00 03 00 00 00 04 00 00 00 ff ff 00 00   MZ..............
0x00980010  b8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00   ........@.......
0x00980020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0x00980030  00 00 00 00 00 00 00 00 00 00 00 00 f8 00 00 00   ................

0x00980000 4d               DEC EBP
0x00980001 5a               POP EDX
0x00980002 90               NOP
0x00980003 0003             ADD [EBX], AL
0x00980005 0000             ADD [EAX], AL
0x00980007 000400           ADD [EAX+EAX], AL
0x0098000a 0000             ADD [EAX], AL
0x0098000c ff               DB 0xff
0x0098000d ff00             INC DWORD [EAX]
0x0098000f 00b800000000     ADD [EAX+0x0], BH
0x00980015 0000             ADD [EAX], AL
0x00980017 004000           ADD [EAX+0x0], AL
0x0098001a 0000             ADD [EAX], AL
0x0098001c 0000             ADD [EAX], AL
0x0098001e 0000             ADD [EAX], AL
0x00980020 0000             ADD [EAX], AL
0x00980022 0000             ADD [EAX], AL
0x00980024 0000             ADD [EAX], AL
0x00980026 0000             ADD [EAX], AL
0x00980028 0000             ADD [EAX], AL
0x0098002a 0000             ADD [EAX], AL
0x0098002c 0000             ADD [EAX], AL
0x0098002e 0000             ADD [EAX], AL
0x00980030 0000             ADD [EAX], AL
0x00980032 0000             ADD [EAX], AL
0x00980034 0000             ADD [EAX], AL
0x00980036 0000             ADD [EAX], AL
0x00980038 0000             ADD [EAX], AL
0x0098003a 0000             ADD [EAX], AL
0x0098003c f8               CLC
0x0098003d 0000             ADD [EAX], AL
0x0098003f 00               DB 0x0
```

:::spoiler Flag
Flag: `0x980000`
:::

## Reference
[^wp]:[BlackEnergy Walkthrough — Cyberdefenders](https://responderj01.medium.com/blackenergy-walkthrough-cyberdefenders-8502d4e37301)