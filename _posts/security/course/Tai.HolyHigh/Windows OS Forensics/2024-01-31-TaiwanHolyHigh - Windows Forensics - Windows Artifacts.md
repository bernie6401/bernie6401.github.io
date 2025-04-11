---
title: TaiwanHolyHigh - Windows Forensics - Windows Artifacts
tags: [TaiwanHolyHigh, Forensics, Windows]

category: "Security > Course > Tai.HolyHigh > Windows OS Forensics"
---

# TaiwanHolyHigh - Windows Forensics - Windows Artifacts
[TOC]

:::info
以下引用若無特別說明皆來自於講師的上課簡報
:::
## Artifacts Background
> 使用者操作 Windows 作業系統時會在系統中留下或產生許多行為紀錄，稱之為 Artifacts

* Artifacts種類
    * 特定路徑或資料夾: 
        * Program Files/Program Data
        * Download
        * Temp$\to$這在玩分析memory中很常出現
    * 電腦特定檔案:
        * LNK
        * Email$\to$這在玩分析memory中也很常出現
        * 系統還原檔(VSS, [volume shadow copy](https://learn.microsoft.com/zh-tw/windows-server/storage/file-server/volume-shadow-copy-service)): 站在藍隊的角度可以藉此知道受害者的遭到入侵的一些證據；站在紅隊的角度可以藉此撈到一些受害者的基敏資料
* Artifacts分析面向
    * 檔案Metadata: Timestamp(一般檔案的MAC time至少有兩個, Modify/Access/Create Time)可以藉此知道檔案的異動時間
    * 應用程式: 
        * 記憶體: volatility可以針對某個PID dump出執行該process的memory，也是常見的技巧
        * [Prefetch File](https://read01.com/zh-tw/6nOOGaj.html)
            > 一般位於C槽windows文件夾下（`C:\Windows\Prefetch`），主要是用來存放系統已訪問的文件預讀信息；一開始創建此文件夾主要是為了加快系統的啟動過程。
    * 使用者的操作行為
        * Audit(AD很常碰到的event ID: 4662...)
        * Volatility的console可以看到駭客的command
        * Volatility的malfind可以看到惡意注入的payload...
    * 網路行為
        * Volatility的netscan
## Most Recently Used(MRU) Background
就是泛指各種windows存取使用者最近access過的檔案、路徑或網路位置，是一種行為，攻防兩端都會注意的地方
* Overview
    ![](https://hackmd.io/_uploads/rk1zs9mfT.png)
* 攻擊者會留下的足跡: `.lnk`, `Jump List`, `User Assist Registry`, `Prefetch`，如果攻擊者想要植入惡意程式，鑑識可以從以上四個地方看出這個intention
    * `Jump List`就有點像是一個shortcut，可以跳到某個地方執行或開啟something
    * `User Assist Registry`
        > 個別使用者近期執行過的行為
        
        因為我的基碼內都是空的所以沒辦法demo，不過按照上課講的重點，通常會有兩種檔案，一個是以ascii顯示路徑的檔案，這通常是沒有執行過的東西；另外一種是以rot13編碼的路徑，這就是有執行過的