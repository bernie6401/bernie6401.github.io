---
title: NTUSTISC - AD Note - Lab(利用弱點)
tags: [information security, NTUSTISC, AD]

---

# NTUSTISC - AD Note - Lab(利用弱點)
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=M0LV3dBCMCOy58LN&t=3600)

## Background
* [Internet Information Services(IIS)](https://zhuanlan.zhihu.com/p/145430397)
    > IIS是縮寫，全稱Internet Information Services ( IIS,互聯網信息服務 ),是由微軟公司提供的基於運行Microsoft Windows的互聯網基本服務。
    >
    > IIS是指World Wide Web server服務，IIS是一種Web（網頁）服務組件，專業的說，IIS可以賦予一部主機電腦一組以上的IP地址，而且還可以有一個以上的域名作為Web網站。做過服務器配置的都應該知道IIS。制作好了網站怎麽才能讓別人瀏覽，就是通過網站服務器來實現的。IIS只是網站服務器的一種而已。
    > ### 簡單來說：
    >
    >Internet Information Service（IIS）是windows開設web網頁服務的組件，用來搭載網站運行程序的平台的。還能提供FTP，SMTP等服務。
    >
    ><font color="ff0000">在UNIX或Linux平台上，Apache就是網站服務器。
    >
    >而對於Windows NT/2000來說，IIS就是標準的網站服務器。</font>
    >
    >IIS是一種服務，是Windows 2000 Server系列的一個組件。不同於一般的應用程序，它就像驅動程序一樣是操作系統的一部分，具有在系統啟動時被同時啟動的服務功能。
    如果想知道如何在win10啟用IIS或是建置網站server，可以看這個影片[^IIS-on-windows]
* 一般權限(就像前面的lab那樣)
    * 取得網域使用者資訊
    * Scan Port
    * Check Group Policy Object
* 高權限好處
    * Dump Password or Hash
    * Turn off Defender
    * Check the other users' info
* 本地特出使用者
    * ==NT Authority\System==(本地端真正的最高權限使用者)
    * NT Authority\Network Service
    * NT Authority\Local Service
    * NT Authority\IUSR
* 提權方法
    * 利用弱點(通常是直接用Windows CVE直接打看看)，可參考[^win-exp-suggest-fei]
    * Hijack Token
    * Guess Password
        就像前面環境觀察中提到的一樣，可以從`Active Directory Users and Computers`的description中看看有沒有密碼的提示，或是查看`$ net user`變更密碼的時間是哪時候，然後考慮爆破
        * Local Admin比Domain Admin好拿
        * 通常是固定密碼
            * 所有主機都相同
            * 可能很多人知道
            * 弱密碼
            * 系統初始化包
        * Solution: 可以參考[本機系統管理員密碼解決方案(LAPS)](https://learn.microsoft.com/zh-tw/windows-server/identity/laps/laps-overview)
    * 管理服務
    * 錯誤配置
## Lab Time - 本地提權
### ==利用弱點==
```bash
$ git clone https://github.com/bitsadmin/wesng.git --depth 1
$ cd wesng
$ python wes.py --update
$ systeminfo.exe > systeminfo.txt # 這條指令是windows內建的指令，所以一定要在cmd中操作
$ python wes.py systeminfo.txt
```
:::spoiler Result
```
python wes.py systeminfo.txt
Windows Exploit Suggester 1.03 ( https://github.com/bitsadmin/wesng/ )
[+] Parsing systeminfo output
[+] Operating System
    - Name: Windows 11 for x64-based Systems
    - Generation: 11
    - Build: 5
    - Version: None
    - Architecture: x64-based
    - Installed hotfixes (3): KB5028948, KB5029263, KB5028756
[+] Loading definitions
    - Creation date of definitions: 20230901
[+] Determining missing patches
[!] Found vulnerabilities!

Date: 20211214
CVE: CVE-2019-0887
KB: KB5008215
Title: Remote Desktop Services?Remote Code Execution Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Remote Code Execution
Exploit: n/a

Date: 20211214
CVE: CVE-2020-0655
KB: KB5008215
Title: Remote Desktop Services?Remote Code Execution Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Remote Code Execution
Exploit: n/a

Date: 20211216
CVE: CVE-2021-43216
KB: KB5008215
Title: Microsoft Local Security Authority (LSA) Server Information Disclosure Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Information Disclosure
Exploit: n/a

Date: 20211215
CVE: CVE-2021-43217
KB: KB5008215
Title: Windows Encrypting File System (EFS) Remote Code Execution Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Critical
Impact: Remote Code Execution
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43219
KB: KB5008215
Title: DirectX Graphics Kernel File Denial of Service Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Denial of Service
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43222
KB: KB5008215
Title: Microsoft Message Queuing Information Disclosure Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Information Disclosure
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43224
KB: KB5008215
Title: Windows Common Log File System Driver Information Disclosure Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Information Disclosure
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43226
KB: KB5008215
Title: Windows Common Log File System Driver Elevation of Privilege Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Elevation of Privilege
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43227
KB: KB5008215
Title: Storage Spaces Controller Information Disclosure Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Information Disclosure
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43228
KB: KB5008215
Title: SymCrypt Denial of Service Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Denial of Service
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43229
KB: KB5008215
Title: Windows NTFS Elevation of Privilege Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Elevation of Privilege
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43230
KB: KB5008215
Title: Windows NTFS Elevation of Privilege Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Elevation of Privilege
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43231
KB: KB5008215
Title: Windows NTFS Elevation of Privilege Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Elevation of Privilege
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43232
KB: KB5008215
Title: Windows Event Tracing Remote Code Execution Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Remote Code Execution
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43233
KB: KB5008215
Title: Remote Desktop Client Remote Code Execution Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Critical
Impact: Remote Code Execution
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43234
KB: KB5008215
Title: Windows Fax Service Remote Code Execution Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Remote Code Execution
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43235
KB: KB5008215
Title: Storage Spaces Controller Information Disclosure Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Information Disclosure
Exploit: n/a

Date: 20211216
CVE: CVE-2021-43236
KB: KB5008215
Title: Microsoft Message Queuing Information Disclosure Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Information Disclosure
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43237
KB: KB5008215
Title: Windows Setup Elevation of Privilege Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Elevation of Privilege
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43238
KB: KB5008215
Title: Windows Remote Access Elevation of Privilege Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Elevation of Privilege
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43239
KB: KB5008215
Title: Windows Recovery Environment Agent Elevation of Privilege Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Elevation of Privilege
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43240
KB: KB5008215
Title: NTFS Set Short Name Elevation of Privilege Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Elevation of Privilege
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43246
KB: KB5008215
Title: Windows Hyper-V Denial of Service Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Denial of Service
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43247
KB: KB5008215
Title: Windows TCP/IP Driver Elevation of Privilege Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Elevation of Privilege
Exploit: n/a

Date: 20211216
CVE: CVE-2021-43248
KB: KB5008215
Title: Windows Digital Media Receiver Elevation of Privilege Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Elevation of Privilege
Exploit: n/a

Date: 20211214
CVE: CVE-2021-41333
KB: KB5008215
Title: Windows Print Spooler Elevation of Privilege Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Elevation of Privilege
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43207
KB: KB5008215
Title: Windows Common Log File System Driver Elevation of Privilege Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Elevation of Privilege
Exploit: n/a

Date: 20211214
CVE: CVE-2021-43880
KB: KB5008215
Title: Windows Mobile Device Management Elevation of Privilege Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Elevation of Privilege
Exploit: n/a

Date: 20211216
CVE: CVE-2021-43883
KB: KB5008215
Title: Windows Installer Elevation of Privilege Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Elevation of Privilege
Exploit: n/a

Date: 20211216
CVE: CVE-2021-43893
KB: KB5008215
Title: Windows Encrypting File System (EFS) Elevation of Privilege Vulnerability
Affected product: Windows 11 for x64-based Systems
Affected component: Microsoft
Severity: Important
Impact: Elevation of Privilege
Exploit: n/a

[-] Missing patches: 1
    - KB5008215: patches 30 vulnerabilities
[I] KB with the most recent release date
    - ID: KB5008215
    - Release date: 20211216
[+] Done. Displaying 30 of the 30 vulnerabilities found.
```
:::

## Reference
[^win-exp-suggest-fei]:[Day32 - Windows 提權(3)-Windows Exploit Suggester](https://ithelp.ithome.com.tw/articles/10281994)
[^IIS-on-windows]:[ 【網站伺服器 IIS】Windows 10 IIS 安裝與啟用 ASP.NET 網站設定 ](https://youtu.be/he6Ndmx3V5I?si=QzyDH441M2z7NwIk)