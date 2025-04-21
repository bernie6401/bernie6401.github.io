---
title: NTUSTISC - AD Note - Lab(查詢網域群組)
tags: [NTUSTISC, AD, information security]

category: "Security/Course/NTUST ISC/AD/1. 環境調查Normal"
---

# NTUSTISC - AD Note - Lab(查詢網域群組)
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=SycYwgWohlu97dc3)

## Lab Time - 環境調查

### ==查詢網域群組==
常用的cheat sheet
`Domain Admins`, `Schema Admins`, `Enterprise Admins`是預設的權限，通常一進到AD網域都會先看這幾個權限有哪些成員
```bash!
$ net groups /domain # 查詢網域中群組的資料
$ net groups "Domain Admins" /domain
$ net groups "Schema Admins" /domain
$ net groups "Enterprise Admins" /domain
```
:::spoiler Implementation
```bash
$ net groups /domain
這項要求會在網域 kuma.org 下的網域控制站處理。


\\WIN-818G5VCOLJO.kuma.org 的群組帳戶

-------------------------------------------------------------------------------
*accounting
*Cloneable Domain Controllers
*DnsUpdateProxy
*Domain Admins
*Domain Computers
*Domain Controllers
*Domain Guests
*Domain Users
*Enterprise Admins
*Enterprise Key Admins
*Enterprise Read-only Domain Controllers
*Executives
*Group Policy Creator Owners
*IT Admins
*Key Admins
*marketing
*Office Admin
*Project management
*Protected Users
*Read-only Domain Controllers
*sales
*Schema Admins
*Senior management
命令已經成功完成。
$ net groups "Domain Admins" /domain
這項要求會在網域 kuma.org 下的網域控制站處理。

群組名稱     Domain Admins
註解         Designated administrators of the domain

成員

-------------------------------------------------------------------------------
Administrator
命令已經成功完成。
$ net groups "Schema Admins" /domain
這項要求會在網域 kuma.org 下的網域控制站處理。

群組名稱     Schema Admins
註解         Designated administrators of the schema

成員

-------------------------------------------------------------------------------
Administrator
命令已經成功完成。
$ net groups "Enterprise Admins" /domain
這項要求會在網域 kuma.org 下的網域控制站處理。

群組名稱     Enterprise Admins
註解         Designated administrators of the enterprise

成員

-------------------------------------------------------------------------------
Administrator
命令已經成功完成。
```
可以看到目前這三個預設的群組，都只有Administrator在裡面而已
:::
* 具有特殊功能的群組
    * Remote Desktop Users
    在這個群組的成員，可以隨意登入別人的RDP(Remote Desktop Protocol)
    * Group Policy Creator Owners
    在這個群組的成員，可以隨意建立GPO，這樣他就可以強制所有帳戶執行他所設定的規則，例如所有人執行後門程式之類的
    * Server Operators
    這是一組進行維護的群組，可以控制整個DC，或是備份他
    * DNSAdmins
    可以管理DNS的紀錄，也可以在主機上跑DLL(執行後門)
    * Backup Operators
    可以備份DC
    * Print Operators
    重開任何主機(超重要)

---

### ==小提醒：加入網域的電腦是沒有隱私的==
尤其是C槽，加入網域後C槽預設是共享的，Domain Admin可以任意查看，但是會留下足跡，所以站在加入網域的角度來說，不要隨便放私人的東西在C槽，而站在Domain Admin的角度來說，不要隨便亂看別人的C槽，因為這樣會留下認證足跡，可能會供攻擊者一些必要資訊