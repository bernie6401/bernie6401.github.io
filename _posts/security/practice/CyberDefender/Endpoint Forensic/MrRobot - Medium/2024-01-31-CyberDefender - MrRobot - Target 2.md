---
title: CyberDefender - MrRobot - Target 2
tags: [NTUSTISC, CyberDefender, Endpoint Forensics]

category: "Security/Practice/CyberDefender/Endpoint Forensic/MrRobot - Medium"
---

# CyberDefender - MrRobot - Target 2
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/88
Target 1: https://hackmd.io/@SBK6401/SkJAThwla
POS: https://hackmd.io/@SBK6401/BJpJqDhlp

:::spoiler TOC
[TOC]
:::
Lecture Video: [ 2022/06/29 藍隊安全系列課程 04 ](https://youtu.be/4u5ckjfFRuM?si=MKeBkxyz5vcnsJfh)
[Volatility - Cheat Sheet](https://hackmd.io/@TuX-/BymMpKd0s)

## Background

## Lab - Target 2

### 起手式
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x86_23418, Win7SP0x86, Win7SP1x86 (Instantiated with WinXPSP2x86)
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : WindowsCrashDumpSpace32 (Unnamed AS)
                     AS Layer3 : FileAddressSpace (D:\NTU\CTF\CyberDefenders\c69-Grrcon2015\target2\memory.dmp)
                      PAE type : PAE
                           DTB : 0x3ed36260L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2015-10-09 12:53:12 UTC+0000
     Image local date and time : 2015-10-09 08:53:12 -0400
```
重要資訊System Name: Win7SP0x86

### ==Q16==
> It appears the attacker moved latterly from the front desk machine to the security admins (Gideon) machine and dumped the passwords. What is Gideon's password? 

#### Recon
根據題目的敘述，我首先會想看他的console，看他有甚麼樣的檔案或是process上的操作，果不其然他有使用到前面提到的wce.exe工具，並且他把結果存在某一個檔案中，接下來就是把檔案dump出來，看裡面的內容這樣

#### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 consoles > .\output\consoles.txt
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 filescan | findstr w.tmp
Volatility Foundation Volatility Framework 2.6
0x000000003fcf2798      8      0 -W-r-- \Device\HarddiskVolume2\Users\gideon\w.tmp
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 dumpfiles -n -D .\output -Q 0x000000003fcf2798
Volatility Foundation Volatility Framework 2.6
DataSectionObject 0x3fcf2798   None   \Device\HarddiskVolume2\Users\gideon\w.tmp
$ strings file.None.0x85a35da0.w.tmp.dat
WCE v1.42beta (Windows Credentials Editor) - (c) 2010-2013 Amplia Security - by Hernan Ochoa (hernan@ampliasecurity.com)
Use -h for help.
gideon\ALLSAFECYBERSEC:t76fRJhS
GIDEON-PC$\ALLSAFECYBERSEC:s9O3t%sd1q>:u5Za8Xrx_3Eg;(\qapu<"Rn$#QQJlsD m#;z2hbJkr*tLe>0)F[S)'USh3BKJILn3-?vt]q=s-Cp.ws9wVik[]5?#F\*l/J19+`PYco:au;T
```

:::spoiler Flag
Flag: `t76fRJhS`
:::

### ==Q17==
> Once the attacker gained access to "Gideon," they pivoted to the AllSafeCyberSec domain controller to steal files. It appears they were successful. What password did they use?

#### Background
[rar.exe的使用方法](https://maplege.github.io/2017/09/06/toolRar/)
> -HP ：帶文件頭加密，更安全，沒有密碼無法查看里面的文件列表

#### Recon
題目敘述提到的狀況可以從console中看出來，可以看到他先把c槽掛在自己的z槽上面(這可能需要一點AD的概念才會比較清楚，可以看之前寫的[NTUSTISC - AD Note - Lab(SMB遠端讀寫)](https://hackmd.io/@SBK6401/B1LqaNGCh/https%3A%2F%2Fhackmd.io%2F%40SBK6401%2FSyn5Q8rga))，然後把一個rar.exe丟到對方的c槽底下(`z:\crownjewels`)，接著把所有東西(.txt)都壓縮，而如果知道rar.exe中-hp的意思就知道他後面帶的東西是壓縮的密碼也就是本題的答案

#### Exploit
:::spoiler Flag
Flag: `123qwe!@#`
:::

### ==Q18==
> What was the name of the RAR file created by the attackers? 

#### Recon
這一題意外的超簡單，就看console中的內容就知道壓縮的檔案名稱是啥了

#### Exploit
:::spoiler Flag
Flag: `crownjewlez.rar`
:::

### ==Q19==
> How many files did the attacker add to the RAR archive? 

#### Background

#### Recon
這一題比較複雜，因為如果單看console中的內容會發現dump出來的部分不完全，所以可以把這一個console的process memory dump出來，然後查看裡面的內容

#### Exploit
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 memdump --pid 3048 -D .\output\    # 按照之前的console查詢結果，可以知道pid是3048
$ strings -el 3048.dmp > 3048.txt
$ strings 3048.txt | grep '\\crownjewels\\'| grep ".txt"
\crownjewels\SecretSauce2.txt
\crownjewels\SecretSauce1.txt
\crownjewels\SecretSauce3.txt
```
1. 記得要把dump出來的memory轉換成16-bits little endian才能看到完整的可視內容
2. 然後如果看前面console的結果可以得知他是在`crownjewels`這個folder底下執行rar的壓縮，所以可以下grep的pipe command，可以知道只有三個.txt檔案

:::spoiler Flag
Flag: `3`
:::

### ==Q20==
> The attacker appears to have created a scheduled task on Gideon's machine. What is the name of the file associated with the scheduled task?

#### Background
[Windows 工作排程](https://medium.com/coding-learning-sharing/windows-%E5%B7%A5%E4%BD%9C%E6%8E%92%E7%A8%8B-56989747a1ce)
[Windows 如何透過工作排程設定開機自動連線](https://helpcenter.trendmicro.com/zh-tw/article/tmka-07819)

#### Recon
看到scheduled task就要想到windows內建的task scheduler的功能，詳細的工具教學可以看上面的background，總之他新增的東西通常會放在`Windows/System32/Tasks`，所以我們可以直接用filescan搭配上述地址的關鍵自進行搜尋

#### Exploit
可以看到task大部分都是microsoft或是google update的東西，只有一個有點奇怪，應該就是這一題的access point
```bash
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86  filescan | findstr \Windows\System32\Tasks\
Volatility Foundation Volatility Framework 2.6
...
0x000000003fc399b8      8      0 R--r-d \Device\HarddiskVolume2\Windows\System32\Tasks\At1
...
$ volatility_2.6_win64_standalone.exe -f memory.dmp --profile Win7SP0x86 dumpfiles -n -Q 0x000000003fc399b8 -D .\output
Volatility Foundation Volatility Framework 2.6
DataSectionObject 0x3fc399b8   None   \Device\HarddiskVolume2\Windows\System32\Tasks\At1
$ cat file.None.0x85a86af0.At1.dat
��<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.0" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo />
  <Triggers>
    <TimeTrigger>
      <StartBoundary>2015-10-09T08:00:00</StartBoundary>
    </TimeTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>@AtServiceAccount</UserId>
      <LogonType>InteractiveTokenOrPassword</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Actions Context="Author">
    <Exec>
      <Command>c:\users\gideon\1.bat</Command>
    </Exec>
  </Actions>
</Task>%
```
可以看到執行label寫說要執行`c:\users\gideon\1.bat`這個script

:::spoiler Flag
Flag: `1.bat`
:::

## Reference
[^cyberdefender-mrrobot-wp]:[MrRobot Walkthrough — Cyberdefenders](https://responderj01.medium.com/mrrobot-walkthrough-cyberdefenders-7694e3120897)