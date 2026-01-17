---
title: NTUSTISC - AD Note - Lab(遠端執行(RDP))
tags: [NTUSTISC, AD, information security]

category: "Security｜Course｜NTUST ISC｜AD｜4. 遠端執行-讀檔"
date: 2024-01-31
---

# NTUSTISC - AD Note - Lab(遠端執行(RDP))
<!-- more -->
[TOC]

Lecture Video: [ 2022/05/11 AD 安全 2 ](https://youtu.be/ubNMQ7_dcm0?si=26g2Lz2CB-O-7S5d)

## Background
[What is EULA?](https://zh.wikipedia.org/wiki/%E6%9C%80%E7%BB%88%E7%94%A8%E6%88%B7%E8%AE%B8%E5%8F%AF%E5%8D%8F%E8%AE%AE)
> 終端使用者授權合約（英語：end-user license agreements，英文縮寫：EULA）是指軟體的開發者或發行者授權使用者使用特定軟體產品時的規定，大多私有軟體附帶此合約，如不接受則無法安裝。不過自由軟體則較少使用這個合約

## Lab
此Lab主要是要讓我們可以遠端執行其他人的電腦，當我們已經取得local admin時，但domain admin遲遲沒有出現，我們就需要多找幾台主機試看看，可不可以登入或是遠端連線，這樣從一台主機出發，多幾台主機一起蹲domain admin的機會就會變大，可能會有疑問，要怎麼知道其他電腦的密碼呢?如果這一間公司它沒有使用之前介紹過的[LAPS密碼管理工具](https://learn.microsoft.com/zh-tw/windows-server/identity/laps/laps-overview)，而且又是委外管理，則很有可能會有多台主機的密碼都一樣，然後再用前面提到的多種密碼提取方法(Brute Force SAM/Password Spraying etc)，得到更多台主機的密碼，然後再利用Mimikatz之類的工具把lsass的info leak出來，就有可能得到domain admin的密碼

### ==遠端執行(RDP)==

#### Linux / Kali
* Tools
    * xfreerdp
        ```bash
        $ sudo apt install freerdp2-x11 -y
        ```
    * Libfreerdp
        先到[https://packages.debian.org/sid/libfreerdp-client2-2](https://packages.debian.org/sid/libfreerdp-client2-2)這個頁面看一下要下載哪一個版本，Kali是amd64
        ```bash
        $ cd ~/Downloads
        $ wget http://ftp.tw.debian.org/debian/pool/main/f/freerdp2/libfreerdp-client2-2_2.10.0+dfsg1-1.1_amd64.deb
        ```

#### Windows
* Tools: [Psexec.exe](https://learn.microsoft.com/zh-tw/sysinternals/downloads/psexec)
    微軟的遠端執行工具，具有微軟的簽章，第一次使用需要接受EULA
    ```bash
    $ PsExec.exe -i \\<Remote IP> -accepteula -u [<domain>]\<Remote Username> -p <Remote Password> cmd
    ```

##### ==How to use xfreerdp==
網路上有很多文章和教學[^xfreerdp-teach][^xfreerdp-teach-2]，不過他們的情況和我們的狀況有點不一樣
:::success
使用條件：Win2016一定要打開，事先取得帳號的密碼
:::
1. Check Win10 IP
    ```bash!
    $ ipconfig

    Windows IP 設定


    乙太網路卡 Ethernet0:

       連線特定 DNS 尾碼 . . . . . . . . : localdomain
       連結-本機 IPv6 位址 . . . . . . . : fe80::e490:37a2:d10e:a709%5
       IPv4 位址 . . . . . . . . . . . . : 192.168.222.129
       子網路遮罩 . . . . . . . . . . . .: 255.255.255.0
       預設閘道 . . . . . . . . . . . . .: 192.168.222.2
    ```
2. Connect
    ```bash!
    $ xfreerdp /d:kuma.org /p:1qaz@WSX3edc /v:192.168.222.129 /u:administrator
    ```
    ![](https://hackmd.io/_uploads/By1s-2V1T.png)

:::warning
Libfreerdp不知道為甚麼，安裝都會失敗，而且網路上也沒有其他教學或資源，所以先skip，反正有xfreerdp可以用
:::
##### ==How to use PsExec==
```bash!
$ PsExec.exe -i \\192.168.222.129 -accepteula -u kuma.org\administrator -p 1qaz@WSX3edc cmd

PsExec v2.43 - Execute processes remotely
Copyright (C) 2001-2023 Mark Russinovich
Sysinternals - www.sysinternals.com


Microsoft Windows [版本 10.0.18363.592]
(c) 2019 Microsoft Corporation. 著作權所有，並保留一切權利。

C:\Windows\system32>whoami
kuma\administrator
```

:::danger
值得一提的是，PsExec或xfreerdp貌似無法登入bear的帳號，只能連線administrator的帳號
:::

##### ==How to detect PsExec==
* Event ID: 7045 $\to$ 必須在遭受遠端連線的主機開啟此event，因為相關特徵是只有被遠端的主機才會產生的行為
* 

## Reference
[^xfreerdp-teach]:[[Linux] 使用 xfreerdp 遠端登入 Windows 桌面](https://ephrain.net/linux-%E4%BD%BF%E7%94%A8-xfreerdp-%E9%81%A0%E7%AB%AF%E7%99%BB%E5%85%A5-windows-%E6%A1%8C%E9%9D%A2/)
[^xfreerdp-teach-2]:[linux版連RDP遠端桌面-xfreerdp](https://blog.davidou.org/archives/2663)
