---
title: NTUSTISC - AD Note - Lab(環境調查BloodHound)
tags: [NTUSTISC, AD, information security]

category: "Security｜Course｜NTUST ISC｜AD｜1. 環境調查Normal"
---

# NTUSTISC - AD Note - Lab(環境調查BloodHound)
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=SycYwgWohlu97dc3)

## Background
[[Windows Programming] IPC 通知機制與安全設定](https://medium.com/renee0918/how-to-protect-windows-global-event-c19bba0ce890)
> 當系統中需要同步處理某些資源的存取權時，可以使用 Windows 的同步處理物件協調不同 process 間對於共同資源的互動，Windows 提供的同步處理物件有四種，分別是: Event, Mutex, Semaphore, Waitable timer，本篇只會提到 Event 喔！
>
>假設系統中有兩個 process：process A 得等待 process B 完成某些特定工作後才能繼續執行。windows 提供的 event 機制能讓 process B 完成工作後發出訊號通知 process A，而 process A 則進入等待狀態直到接受到訊號後才繼續執行後續工作。Process 間只需定好溝通的 event name 就可以輕鬆達成跨程序間的通訊 (Inter-process communication : IPC)，正因為簡單好實現的特性，event 常被用在程序間的溝通與同步。


## Lab Time - 環境調查

### BloodHound AD
* 說明: 環境調查的視覺化工具
* 版本: 4.0.3 
    :::info
    <font color="FF0000">8/29更新：經過實測還是建議使用4.1.0</font>，詳細原因可以參考[^bloodhound-bug]，原作者說明這是一個bug，已在4.1.0做了修正，所以還是以4.1.0為主，雖然聽講師說可能會少東西，不過對我們小專案來說應該沒差
    :::
* Link: [BloodHound GitHub](https://github.com/BloodHoundAD/BloodHound/releases/tag/4.0.3)
* 必要條件: 必須裝設Neo4j Server / Graph Database, 而且必須要是community version，[link](https://neo4j.com/download-center/#community)
1. Download Collector
BloodHound是一個環境調查的視覺化工具，所以要先在我們的環境先蒐集一些環境上的資訊，再導入到BloodHound中進行分析，因此我們應該先下載能夠蒐集環境資訊的[Collector](https://github.com/BloodHoundAD/BloodHound)我是直接把整包clone下來，然後用隨身碟傳到VM(因為那時候Win10已經加入AD，我懶得改回來上網)
    :::info
    Note:
    Windows的defender會擋`BloodHound-master/Collectors/SharpHound.exe`和`SharpHound.ps1`這兩個files，所以記得關掉defender
    :::
2. Use the Collector First
    :::info
    Note: 記得要用bear的網域帳號登入，SharpHound.exe才找的到LDAP
    :::
    CMD直接進入`C:\tools\BloodHound-master\Collectors`，然後直接執行`$ SharpHound.exe`
    :::spoiler Implementation
    ```bash
    $ SharpHound.exe
    2023-08-29T11:02:31.4846421+08:00|INFORMATION|This version of SharpHound is compatible with the 4.3.1 Release of BloodHound
    2023-08-29T11:02:31.6707467+08:00|INFORMATION|Resolved Collection Methods: Group, LocalAdmin, Session, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote
    2023-08-29T11:02:31.6985917+08:00|INFORMATION|Initializing SharpHound at 上午 11:02 on 2023/8/29
    2023-08-29T11:02:31.9891653+08:00|INFORMATION|[CommonLib LDAPUtils]Found usable Domain Controller for kuma.org : WIN-818G5VCOLJO.kuma.org
    2023-08-29T11:02:32.3820391+08:00|INFORMATION|Loaded cache with stats: 163 ID to type mappings.
     163 name to SID mappings.
     1 machine sid mappings.
     2 sid to domain mappings.
     0 global catalog mappings.
    2023-08-29T11:02:32.3915435+08:00|INFORMATION|Flags: Group, LocalAdmin, Session, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote
    2023-08-29T11:02:32.6206999+08:00|INFORMATION|Beginning LDAP search for kuma.org
    2023-08-29T11:02:32.8062803+08:00|INFORMATION|Producer has finished, closing LDAP channel
    2023-08-29T11:02:32.8230625+08:00|INFORMATION|LDAP channel closed, waiting for consumers
    2023-08-29T11:03:03.3930708+08:00|INFORMATION|Status: 0 objects finished (+0 0)/s -- Using 42 MB RAM
    2023-08-29T11:03:13.1743544+08:00|INFORMATION|Consumers finished, closing output channel
    Closing writers
    2023-08-29T11:03:13.2209345+08:00|INFORMATION|Output channel closed, waiting for output task to complete
    2023-08-29T11:03:13.3058132+08:00|INFORMATION|Status: 204 objects finished (+204 5.1)/s -- Using 44 MB RAM
    2023-08-29T11:03:13.3058132+08:00|INFORMATION|Enumeration finished in 00:00:40.6864986
    2023-08-29T11:03:13.3918361+08:00|INFORMATION|Saving cache with stats: 163 ID to type mappings.
     163 name to SID mappings.
     1 machine sid mappings.
     2 sid to domain mappings.
     0 global catalog mappings.
    2023-08-29T11:03:13.4075189+08:00|INFORMATION|SharpHound Enumeration Completed at 上午 11:03 on 2023/8/29! Happy Graphing!
    ```
    :::
    理論上成功的話，會在該folder中出現一個.zip file with name `<TimeStamp>.BloodHound.zip`此時按照之前啟動BloodHound的方法啟動BloodHound，然後把zip folder拖進去就可以了
    ![](https://hackmd.io/_uploads/rk8rZJjT2.png)

### ==如何偵測AD==
有兩種方法，也可以同時使用
1. Lots of Event ID: 4662
如果同一時間偵測到很多4662 event的操作，那很有可能是bloodhound，就算不是也一定是類似的情蒐工具
2. Event ID: 5146
bloodhound喜歡存取的對象是: ==lsarpc/samr/srvsvc==，所以只要有這幾個event出現，就很有可能是bloodhound，而這個event也是像4662一樣預設是關閉的，所以要先到Group Policy Editor打開
![](https://hackmd.io/_uploads/HJjbgTZRn.png)

    :::danger
    我查找了5146的event但都沒有偵測到，我有把GPO打開，但是還是沒有偵測到，我是有在Event Viewer中看到很像的，例如5145/5156之類的，但看起來都不是，另外，講師的影片中在59:11的地方也是顯示Event 5145，所以我不知道該怎麼解決這個lab遇到的問題
    :::


    可以使用Event Viewer中的Create Custom View，自動的filter出想要的Event
![](https://hackmd.io/_uploads/HkDjhnWR3.png)

#### Result
:::spoiler Screenshot of Event 4662
![](https://hackmd.io/_uploads/rJRXT3Z0n.png)


![](https://hackmd.io/_uploads/SyZxpn-R3.png)
可以看到從3:53~3:54的時間當中有超多的event 4662紀錄，而同時可以看到再另外一台主機中，我也是在差不多時間執行SharpHound.exe，進行情蒐
:::



## Reference
[^bloodhound-bug]:[ Bloodhound 4.0 - doesn’t upload all data #402 ](https://github.com/BloodHoundAD/BloodHound/issues/402)