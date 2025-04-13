---
title: NTUSTISC - AD Note - Lab(偵測LSASS)
tags: [NTUSTISC, AD, information security]

category: "Security/Course/NTUST ISC/AD/3. 更多密碼"
---

# NTUSTISC - AD Note - Lab(偵測LSASS)
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=l1na5hFGpAPk6Uux&t=4257)

## Background
得到更高權限之後，會想要更多的密碼
* 密碼收集
    * SAM.hive(Security Account Manager)
    * Password Spraying(用猜的)
    * GPO
    * 記憶體(lsass)
        * How to detect LSASS access?
        利用Sysmon這個工具中有設定的event ID: 10，這個工具類似Event Viewer但更多元更強，下載可見[Sysmon](https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon)
        * How to install?
        簡單來說它需要先準備一個config file，然後安裝的時候就會一起把config設定好(每一間公司或每一個人都不一樣，算是機密)
            ```bash
            $ Sysmon64.exe -i sysmonconfig-export.xml
            ```

## Lab

### ==偵測LSASS==
利用Sysmon Event ID: 10
1. 準備sysmonconfig
    就像前面說的，每一間公司的sysmonconfig都是機密，所以我們這次的lab，講師也有準備簡易的sysmonconfig
    ```xml
    <Sysmon schemaversion="4.1">
        <HashAlgorithm>SHA256</HashAlgorithm>
        <EventFiltering>
            <ProcessAccess default="include">   
            </ProcessAccess>
        </EventFiltering>
    </Sysmon>
    ```
2. 安裝Sysmon
    按照前面提到的指令，並把sysconfig準備好
    ```bash
    $ Sysmon64.exe -i sysmonconfig-export.xml

    System Monitor v15.0 - System activity monitor
    By Mark Russinovich and Thomas Garnier
    Copyright (C) 2014-2023 Microsoft Corporation
    Using libxml2. libxml2 is Copyright (C) 1998-2012 Daniel Veillard. All Rights Reserved.
    Sysinternals - www.sysinternals.com

    Loading configuration file with schema version 4.10
    Sysmon schema version: 4.90
    ```
    :::warning
    實作中這邊遇到問題，理論上準備好sysmonconfig之後下command應該會安裝，但他只跑到一半就結束了，不確定是不是因為沒有連網還是其他設定沒有做好，總之，sysmon算是不能用了，所以之後還有其他的lab會用到就只能跳過
    :::
3. Skip