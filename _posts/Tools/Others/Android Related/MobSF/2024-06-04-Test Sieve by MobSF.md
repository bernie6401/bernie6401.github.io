---
title: Test Sieve by MobSF
tags: [Android, MobSF]

category: "Tools/Others/Android Related/MobSF"
---

# Test Sieve by MobSF
<!-- more -->
這個工具真的很完整，而且蠻萬用的，光是靜態分析就很詳細

## Static Analysis
* Overview
    一開始就告訴測試者有多少的東西被export，和Drozer分析的一樣
    ![圖片](https://hackmd.io/_uploads/H1oU-p3E0.png)
* Application Permission
    MobSF還可以分析實際寫的code並且查看哪邊有Permission相關的威脅，在Code Analysis的地方有重複的提到External Read/Write的漏洞
    ![圖片](https://hackmd.io/_uploads/SJW6fTnV0.png)
* Manifest Analysis
    這一段就很像Drozer做attack surface後的結果，也就是activity/service/broadcast receiver/content providers exported + is debuggable
    * Activity Exported
        ![圖片](https://hackmd.io/_uploads/HJZw4ahVC.png)
        ![圖片](https://hackmd.io/_uploads/HJhO4p2EA.png)
    * Service Exported
        ![圖片](https://hackmd.io/_uploads/r1msNa3VR.png)
        ![圖片](https://hackmd.io/_uploads/rJXTNpnER.png)
    * Content Providers Exported
        ![圖片](https://hackmd.io/_uploads/BkrR4a3NC.png)
        ![圖片](https://hackmd.io/_uploads/B1GJHa24C.png)
        在Code Analysis的地方有重複的提到這個漏洞
    * Debuggable
        ![圖片](https://hackmd.io/_uploads/SyObSpn4A.png)
        在Code Analysis的地方有重複的提到這個漏洞
    * 其他
        * 版本過低
            ![圖片](https://hackmd.io/_uploads/SyVkL63VC.png)
        * Backupable
            ![圖片](https://hackmd.io/_uploads/B1LSvpn4A.png)
        * 和最近的CVE PoC分析
            這個功能蠻好的，例如下圖，這三個漏洞都是去分析`FileSelectActivity`/`MainLoginActivity`/`PWList`得出可能會有StrandHogg 2.0 或StrandHogg的問題，關於StrandHogg 2.0 的說明可以看[twcert的文章](https://www.twcert.org.tw/tw/cp-104-3636-6072b-1.html)，簡單來說這個惡意軟體的效果是常駐在各個正常執行的軟體背後，並且竊取一些機敏資料
            ![圖片](https://hackmd.io/_uploads/HJf0IpnN0.png)
            ![圖片](https://hackmd.io/_uploads/S16AL634R.png)
            ![圖片](https://hackmd.io/_uploads/H12kva34C.png)
            > StrandHogg 2.0 的運作原理，和去年發現的 StrandHogg 相當類似，都可在感染後將自己隱藏在正常的軟體身後；當用戶開啟正常軟體時，真正執行的並不是這個正常版的軟體，而是植入了惡意軟體程式碼的「分身」。
            > 新版 StrandHogg 2.0 除了上述的類似功能外，還能讓惡意軟體偽裝成任意的 Android App；先前的版本只能偽裝成 TaskAffinity 這支 App，甚至能在用戶點按開啟任何 App 時立刻偽裝成該 App。
* Code Analysis
    * SQL DB可以被Access
        ![圖片](https://hackmd.io/_uploads/ryhkWA24R.png)
    * Hardcoded Sensitve Data including IP
        ![圖片](https://hackmd.io/_uploads/H1C7-R2NC.png)
    * Debuggable
        ![圖片](https://hackmd.io/_uploads/Sk3I-C3NC.png)
    * Read/Write External Storage
        ![圖片](https://hackmd.io/_uploads/SJ_TZR2NA.png)

## Dynamic Analysis