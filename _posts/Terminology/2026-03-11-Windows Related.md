---
layout: post
title: "Windows Related"
date: 2026-03-11
category: "Terminology"
tags: []
draft: false
toc: true
comments: true
---

# Windows Related
<!-- more -->

## Active Directory (AD)
有關AD的基本名詞，可以參考[NTUSTISC - AD Note - 環境建置 & Background]({{base.url}}/NTUSTISC-AD-Note-0x01環境建置-&-Background/)，包含 `Directory Service`, `Active Directory`, `Active Directory Domain Service`, `LDAP`, `Organization Units(OU)`, `Group Policy Object(GPO)`

* 可以把 AD 想像成一種 專門用於身份、權限、群組和資源管理的資料庫 + 服務。
* LDAP是一種**用來存取「目錄服務（Directory Service）」的網路協定**，目錄服務可以理解為：一個專門存放組織資訊的資料庫，常見儲存內容：`使用者帳號、密碼（hash）、email、部門、群組權限、電腦設備`，很多企業內部系統的 登入驗證 都會透過 LDAP。常見實作包括：Microsoft Active Directory，所以既然這是一個database，就存在和database server溝通的場景，query command就可能存在injection的risk
* LDAPS = LDAP + SSL/TLS: 在 LDAP 的基礎上加上 加密層 (SSL/TLS)。

## lsass.exe VS SAM
SAM只會存取本地用戶的NTLM Hash，而lsass.exe是只要有存取過目前電腦的使用者都會被記錄，例如domain admin或是其他使用者利用smb連過來也會被lsass紀錄
### lsass
* 作用：Local Security Authority Subsystem Service，Windows 核心安全服務。
* 用途：管理 登入驗證、使用者 token 和安全政策。
* 安全角度：是非常敏感的系統進程，攻擊者經常嘗試 dump LSASS memory 來竊取帳號密碼（尤其是 NTLM hashes）。

### SAM(Security Account Manager)
* 就是一個用於windows的數據庫文件，用於儲存用戶的密碼，並且對於本地端或遠端的使用者進行身分認證
* 在`C:\Windows\System32\config\SAM`

## LM（LAN Manager）& NTLM（NT LAN Manager）

| 名稱   | 是什麼                                |
| ---- | ---------------------------------- |
| LM   | 舊的 Windows password hash（非常不安全）    |
| NTLM | 新一代 hash + authentication protocol |

* LM 是非常早期的 Windows 密碼雜湊機制，來源於舊版 LAN Manager 網路系統。
* NTLM 是 LM 的改進版，用於 Windows NT 系列。不只是 hash，它也是一種 challenge-response authentication protocol。
    * 雖然比 LM 好，但 NTLM 仍然有安全問題，因此在現代 AD 環境中，微軟推薦使用：<span style="background-color: yellow">Kerberos</span>

## WDigest
是一種 Windows 身分驗證機制（authentication protocol / package），它存在於 Windows 的 LSASS authentication packages 中，主要用途是支援 HTTP Digest Authentication。但在資安領域它更有名的原因是：它曾經會在記憶體中保存明文密碼（plaintext password）。

## LAPS(本機系統管理員密碼解決方案)
是 Microsoft 提供的一種 管理 Windows 本機 Administrator 密碼的解決方案，LAPS = 自動為每台電腦設定不同的本機 Administrator 密碼，並把密碼安全地存到 Active Directory。

## Software
* [什麼是svchost.exe？](https://daydayreview.com/svchost-exe%E3%80%82%E5%AE%83%E6%98%AF%E4%BB%80%E9%BA%BC%EF%BC%8C%E7%82%BA%E4%BB%80%E9%BA%BC%E5%9C%A8%E6%88%91%E7%9A%84%E9%9B%BB%E8%85%A6%E4%B8%8A%E9%81%8B%E8%A1%8C%EF%BC%9F/)
    > svchost.exe被稱為服務主機，是一個軟體程式，是Windows操作系統的一部分，被許多Windows應用程式使用。一台計算機的svchost.exe應該位於系統文件夾中的'\windows\System32'。
    > 在啟動時，服務控制管理器啟動svchost.exe，以管理從動態鏈接庫（DLLs）運行的系統服務。因此，對於每個正在運行的服務，都有一個svchost.exe的實例來管理它。
    > 它通過確保各種服務和進程共享資源來幫助減少CPU負荷。動態鏈接庫有被各種軟體應用程式所利用的代碼。它們需要svchost.exe作為額外的軟體來確保運行這些不同服務的效率。這可以確保Windows或其他程式所需的DLL文件被有效加載。
* [dllhost.exe](https://baike.baidu.com/item/dllhost.exe/8193205)
    > dllhost.exe是微軟Windows操作系統的一部分。dllhost.exe用於管理DLL應用，在任務管理器中可以找到，這個程序對是微軟Windows系統的正常運行是非常重要的。