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

## lsass.exe
* 作用：Local Security Authority Subsystem Service，Windows 核心安全服務。
* 用途：管理 登入驗證、使用者 token 和安全政策。
* 安全角度：是非常敏感的系統進程，攻擊者經常嘗試 dump LSASS memory 來竊取帳號密碼（尤其是 NTLM hashes）。