---
title: NTUSTISC - AD Note - Lab(錯誤配置)
tags: [NTUSTISC, AD, information security]

category: "Security｜Course｜NTUST ISC｜AD｜2. 提升權限"
date: 2024-01-31
---

# NTUSTISC - AD Note - Lab(錯誤配置)
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=M0LV3dBCMCOy58LN&t=3600)

## Background
* 提權方法
    * 利用弱點
    * Hijack Token
    * Guess Password
    * 管理服務
    * 錯誤配置
        * 服務使用高權限執行且檔案權限配置錯誤，所以只要把這項服務替換成惡意程式，最後再利用前面提到的print operator重開機，就可以達到控制的目的
        * 透過[accesschk.exe](https://docs.microsoft.com/en-us/sysinternals/downloads/accesschk)找出有問題的地方
            ```bash!
            $ accesschk.exe <user> <path>
            ```
        * For example
            ```bash!
            $ accesschk.exe "Administrator" "C:\Program Files\"

            Accesschk v6.15 - Reports effective permissions for securable objects
            Copyright (C) 2006-2022 Mark Russinovich
            Sysinternals - www.sysinternals.com
            RW C:\Program Files
            ```

## Lab Time - 本地提權

### ==錯誤配置==
找出low有存取權限的service檔案
```bash!
$ accesschk.exe "low" "C:\tools"

Accesschk v6.15 - Reports effective permissions for securable objects
Copyright (C) 2006-2022 Mark Russinovich
Sysinternals - www.sysinternals.com

RW C:\tools\AccessChk
RW C:\tools\accesschk.exe
RW C:\tools\AccessChk.zip
RW C:\tools\BloodHound-master
RW C:\tools\BloodHound-win32-x64
RW C:\tools\BloodHound-win32-x64-4.0.3.zip
RW C:\tools\BloodHound-win32-x64-4.1.0
RW C:\tools\BloodHound-win32-x64-4.1.0.zip
RW C:\tools\Certify.exe
RW C:\tools\DNSAdmin-DLL.dll
RW C:\tools\KDU-1.1.0
RW C:\tools\KmdManager.exe
RW C:\tools\mimikatz_trunk
RW C:\tools\neo4j-community-4.3.4
RW C:\tools\neo4j-community-4.3.4-windows.zip
RW C:\tools\nopad
RW C:\tools\openssl.zip
RW C:\tools\PrintSpoofer64.exe
RW C:\tools\Procdump
RW C:\tools\ProcessExplorer
RW C:\tools\PSTools
RW C:\tools\Rubeus.exe
RW C:\tools\Windows-Kernel-Explorer-master
```