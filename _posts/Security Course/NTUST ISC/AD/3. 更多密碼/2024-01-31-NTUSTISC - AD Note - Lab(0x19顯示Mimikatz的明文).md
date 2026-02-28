---
title: NTUSTISC - AD Note - Lab(顯示Mimikatz的明文)
tags: [NTUSTISC, AD, information security]

category: "Security Course｜NTUST ISC｜AD｜3. 更多密碼"
date: 2024-01-31
---

# NTUSTISC - AD Note - Lab(顯示Mimikatz的明文)
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=l1na5hFGpAPk6Uux&t=4257)

## Background
之前在進行mimikatz的實作時，會看到很多wdigest是(null)的情況，主要原因是windows的設定的問題，所以只要把設定改回來，就可以正常顯示了，主要是windows不主動存取明文密碼
* [What is WDigest](https://www.sohu.com/a/569244434_121124375)
    > WDigest即摘要身份驗證，摘要身份驗證是一種質詢/響應協議，主要在WindowsServer2003中用於LDAP和基於Web的身份驗證。它利用超文本傳輸協議(HTTP)和簡單身份驗證安全層(SASL)交換進行身份驗證

---
[什麼是安全性識別碼？](https://learn.microsoft.com/zh-tw/windows-server/identity/ad-ds/manage/understand-security-identifiers)
> 安全性識別碼可用來唯一識別安全性主體或安全性群組。 安全性主體可以代表可由作業系統驗證的任何實體，例如使用者帳戶、電腦帳戶，或在使用者或電腦帳戶的安全性內容中執行的執行緒或進程。
>
> 每個帳戶或群組，或帳戶安全性內容中執行的每個進程，都有由授權單位發出的唯一 SID，例如 Windows 網域控制站。 SID 會儲存在安全性資料庫中。 系統會產生 SID，以識別建立帳戶或群組時的特定帳戶或群組。 當 SID 做為使用者或群組的唯一識別碼時，永遠不會再次用來識別其他使用者或群組。

## Lab

### ==顯示Mimikatz的明文==
1. 只要打開regedit，在`電腦\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest`可能會看到`UseLogonCredential`的名稱，只要把對應的數值改成1就可以了，當然如果沒看到的話也可以自己新增
![](https://hackmd.io/_uploads/BkQAC8ERn.png)
2. 重開機
重開機前可以先把之前mimikatz的結果存起來，照樣之後可以對照著看
3. Result
    我挑了幾個SID一樣的結果來看
    ![](https://hackmd.io/_uploads/HktIkvVA2.png)
    
    ![](https://hackmd.io/_uploads/B1uqyDE02.png)
    左邊的是新增config之前，右邊的是重開機之後，可以看到原本(null)的地方大部分都有被顯示出來
