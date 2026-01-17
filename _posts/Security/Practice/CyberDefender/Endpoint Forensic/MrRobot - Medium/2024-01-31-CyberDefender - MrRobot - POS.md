---
title: CyberDefender - MrRobot - POS
tags: [NTUSTISC, CyberDefender, Endpoint Forensics]

category: "Security｜Practice｜CyberDefender｜Endpoint Forensic｜MrRobot - Medium"
date: 2024-01-31
---

# CyberDefender - MrRobot - POS
<!-- more -->
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/88
Target 1: https://hackmd.io/@SBK6401/SkJAThwla
Target 2: https://hackmd.io/@SBK6401/HJz2FPne6

:::spoiler TOC
[TOC]
:::

## Lab - POS

### 起手式
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x86_23418, Win7SP0x86, Win7SP1x86 (Instantiated with WinXPSP2x86)
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : WindowsCrashDumpSpace32 (Unnamed AS)
                     AS Layer3 : FileAddressSpace (D:\NTU\CTF\CyberDefenders\c69-Grrcon2015\pos01\memory.dmp)
                      PAE type : PAE
                           DTB : 0x3ecde260L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2015-10-09 12:52:56 UTC+0000
     Image local date and time : 2015-10-09 08:52:56 -0400
```
重要資訊System Name: 

### ==Q21==
> What is the malware CNC's server?

#### Background
[輕鬆理解什麼是 C&C 伺服器 原文網址：https://itw01.com/2G2BLEW.html](https://itw01.com/2G2BLEW.html)
> 通常我們在網路上看到的文章說 C&C 伺服器的 IP 地址或者域名，這裏的 C&C 伺服器說的就是上面的中轉伺服器，為什麼是中轉伺服器而不是本地主機呢？
> 那是因為中轉伺服器是惡意軟體和僵屍網絡的直連伺服器，是最直接接觸的伺服器，通常在惡意軟體分析或者僵屍網絡分析的時候首先分析出來的，所有控制者傳送的指令都是經過中轉伺服器傳送到目標伺服器的

#### Recon
看了前面的background就可以直覺想到應該是和網路的部分相關，那就是直接netscan看IP符合題目的提示

#### Exploit
我的想法是既然是類似webshell的操作，代表應該是能夠開webshell的process，剛好iexplorer.exe的IP
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 netscan
Offset(P)          Proto    Local Address                  Foreign Address      State            Pid      Owner          Created
...
0x3e135df8         TCPv4    10.1.1.10:58751                54.84.237.92:80      CLOSE_WAIT       3208     iexplore.exe
...
```

:::spoiler Flag
Flag: `54.84.237.92`
:::

### ==Q22==
> What is the common name of the malware used to infect the POS system?

#### Recon
這一題又是新的觀念，本來以為會事和pslist之類的有關，但看了[^cyberdefender-mrrobot-wp]的說明才知道具體怎麼做，首先通過前一題，我們知道iexplore.exe的操作有點問題，但iexplore.exe應該是個沒啥問題的process，再者通過題幹可以知道他應該是被malware注入或是操到其他的攻擊，此時就可以把該process dump出來，但不是利用procdump而是要搭配malfind才對，因為如果用procdump他是直接把iexplore.exe dump出來，丟到virustotal八成是沒啥問題

#### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 malfind | findstr iexplore
Volatility Foundation Volatility Framework 2.6
Process: iexplore.exe Pid: 3208 Address: 0x50000
Process: iexplore.exe Pid: 3136 Address: 0x50000
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 malfind --pid 3208 -D .\output
```
可以先看一下malfind的全部結果再決定要特別把哪一個process dump出來，丟到virustotal之後會看到八成是dexter這支trojan malware，詳細結果可以看[這邊](https://www.virustotal.com/gui/file/bf067ffc68f3f1c23bc3402e4494d83e738cc6e158c4f57176b4f5def412e056)，另外我還有看到ithome的這篇早期的文章，FYI，[PoS系統遭致Dexter木馬程式感染!鴻璟科技提供專業的安全對策](https://www.ithome.com.tw/pr/78499)

:::spoiler Flag
Flag: `dexter`
:::

### ==Q23==
> In the POS malware whitelist. What application was specific to Allsafecybersec?

#### Recon
這一題要找的是Allsafecybersec有哪些特別的應用程式，正確的操作是先把該process有使用到的dll dump出來，然後再sting search查看，不過看了[^cyberdefender-mrrobot-wp]的操作，也是可以直接把前一題的process dump出來的結果，string search看一下.exe有哪一些，如果要看嚴謹的版本可以看[^cyberdefender-mrrobot-wp2]，不過我是覺得這一題問的很奇怪就是了，看了半天也不知道要表達甚麼

#### Exploit
```bash
$ strings process.0x83f324d8.0x50000.dmp | grep '.exe'
allsafe_protector.exe
svchost.exe
iexplore.exe
explorer.exe
smss.exe
csrss.exe
winlogon.exe
lsass.exe
spoolsv.exe
alg.exe
wuauclt.exe
.exe;.bat;.reg;.vbs;
iexplore.exe
lHost.exe
```

:::spoiler Flag
Flag: `allsafe_protector.exe`
:::

### ==Q24==
> What is the name of the file the malware was initially launched from?

#### Background
```bash
$ volatility_2.6_win64_standalone.exe -h
...
                iehistory       Reconstruct Internet Explorer cache / history
```

#### Recon
因為前面都有提到此malware是透過注入ieplore.exe來達到C&C Server的目的，因此可以用iehistory這個plugin查看儲存在cache中的紀錄

#### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 iehistory
Volatility Foundation Volatility Framework 2.6
**************************************************
Process: 1836 explorer.exe
Cache type "DEST" at 0x510182b
Last modified: 2015-10-09 08:35:57 UTC+0000
Last accessed: 2015-10-09 12:35:58 UTC+0000
URL: pos@http://54.84.237.92/allsafe_update.exe
**************************************************
Process: 1836 explorer.exe
Cache type "DEST" at 0x5101b93
Last modified: 2015-10-09 08:35:57 UTC+0000
Last accessed: 2015-10-09 12:35:58 UTC+0000
URL: pos@http://54.84.237.92/allsafe_update.exe
```

:::spoiler Flag
Flag: `allsafe_update.exe`
:::

## Reference
[^cyberdefender-mrrobot-wp]:[MrRobot Walkthrough — Cyberdefenders](https://responderj01.medium.com/mrrobot-walkthrough-cyberdefenders-7694e3120897)
[^cyberdefender-mrrobot-wp2]:[CyberDefenders: Mr. Robot](https://beginninghacking.net/2022/05/20/cyberdefenders-mr-robot/)