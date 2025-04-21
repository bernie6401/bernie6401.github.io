---
title: NTUSTISC - AD Note - Lab(查詢本地使用者)
tags: [NTUSTISC, AD, information security]

category: "Security/Course/NTUST ISC/AD/1. 環境調查Normal"
---

# NTUSTISC - AD Note - Lab(查詢本地使用者)
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=SycYwgWohlu97dc3)

## Lab Time - 環境調查

### ==查詢本地使用者==
常用的cheat sheet
```bash!
$ net user
$ net user <username>
```
:::spoiler Implementation
```bash!
$ net user

\\DESKTOP-G95U93T 的使用者帳戶

-------------------------------------------------------------------------------
Administrator            DefaultAccount           Guest
low                      user                     WDAGUtilityAccount
命令已經成功完成。
$ net user administrator
使用者名稱             Administrator
全名
註解                   管理電腦/網域的內建帳戶
使用者的註解
國家/區域碼            000 (系統預設值)
帳戶使用中             Yes
帳戶到期               從不

上次設定密碼           ‎2021/‎9/‎28 下午 10:10:39
密碼到期               從不
可變更密碼             ‎2021/‎9/‎28 下午 10:10:39
請輸入密碼             Yes
使用者可以變更密碼     Yes

容許的工作站           全部
登入指令檔
使用者設定檔
主目錄
上次登入時間           ‎2023/‎8/‎26 上午 12:48:36

可容許的登入時數       全部

本機群組會員           *Administrators
全域群組會員           *None
命令已經成功完成。
```
:::

要注意的地方是：
1. 帳戶是否使用中 - 
2. 帳戶到期
3. 密碼到期
4. 上次設定密碼
5. 本機群組會員
6. 全域群組會員