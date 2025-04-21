---
title: CyberDefender - Hunter (Part 2)
tags: [CyberDefender, Endpoint Forensics]

category: "Security/Practice/CyberDefender/Endpoint Forensic/Hunter - Medium"
---

# CyberDefender - Hunter (Part 2)
<!-- more -->
Challenge: https://cyberdefenders.org/blueteam-ctf-challenges/32
Part 1: https://hackmd.io/@SBK6401/By1BpZIf6
Part 3: https://hackmd.io/@SBK6401/HylP8ixQp

:::spoiler TOC
[TOC]
:::

## Tools
* [PST Viewer](https://goldfynch.com/pst-viewer/index.html#0/33474/2098436)
* [xml parser](https://jsonformatter.org/xml-parser)
* [DB Browser for SQLlite](https://sqlitebrowser.org/dl/)

## ==Q11==
> How many ports were scanned? 

### Exploit
呈上題
![](https://hackmd.io/_uploads/r1Gbf_vM6.png)

:::spoiler Flag
Flag: `1000`
:::

## ==Q12==
> What ports were found "open"?(comma-separated, ascending)

### Exploit
呈上題
![](https://hackmd.io/_uploads/HJfozdDG6.png)

:::spoiler Flag
Flag: `22,80,9929,31337`
:::

## ==Q13==
> What was the version of the network scanner running on this computer?

### Exploit
呈上題
![](https://hackmd.io/_uploads/B11RMuwzT.png)

:::spoiler Flag
Flag: `7.12`
:::

## ==Q14==
> The employee engaged in a Skype conversation with someone. What is the skype username of the other party?

### Recon
直覺要先找到skype相關的文件放在哪邊，看了[^hunter-wp]的說明才知道是放在`\root\Users\Hunter\AppData\Roaming\Skype\hunterehpt`，而所有和對話、帳戶等訊息都放在`main.db`這個檔案中
![](https://hackmd.io/_uploads/H18KDdvzp.png)

### Exploit
又是使用新工具的時候([DB Browser for SQLlite](https://sqlitebrowser.org/dl/))，直接看Message這個table，一開始就講到了兩個名字$\to$`linux-rul3z`和`hunterehpt`
![](https://hackmd.io/_uploads/rJlyRL_vG6.png)

:::spoiler Flag
Flag: `linux-rul3z`
:::

## ==Q15==
> What is the name of the application both parties agreed to use to exfiltrate data and provide remote access for the external attacker in their Skype conversation?

### Exploit
呈上題
觀察兩者的對話紀錄就知道是`teamviewer`

:::spoiler Flag
Flag: `teamviewer`
:::

## ==Q16==
> What is the Gmail email address of the suspect employee?

### Exploit
呈上題
直覺會從其他的table撈資料，我找到一個`Contacts`的table，裡面就有hunter自己本身的gmail address

:::spoiler Flag
Flag: `ehptmsgs@gmail.com`
:::

## ==Q17==
> It looks like the suspect user deleted an important diagram after his conversation with the external attacker. What is the file name of the deleted diagram? 

### Recon
這一題完全沒有想法，也是看了[^hunter-wp]才知道，他先找到了outlook的backup file，在`\root\Users\Hunter\Documents\Outlook Files`中有一個pst file，可以用[線上工具](https://goldfynch.com/pst-viewer/index.html#0/32898)去parse，然後就可以看到email之間的通訊紀錄

### Exploit
在important的folder中可以發現一張網路架構圖，應該就是這一題的答案，回推原本在skype上的時間，兩人互相道別的時候是`2016/06/21 08:48:56`，接著就轉而用email互相通訊，包含附上network design和制訂如何洩漏檔案出去之類的事情
![](https://hackmd.io/_uploads/SJDmuYPMT.png)

:::spoiler Flag
Flag: `home-network-design-networking-for-a-single-family-home-case-house-arkko-1433-x-792.jpg`
:::

## ==Q18==
> The user Documents' directory contained a PDF file discussing data exfiltration techniques. What is the name of the file? 

### Recon

### Exploit
仔細看一下Document裡面的一些pdf，會看到有一個叫做`Ryan_VanAntwerp_thesis.pdf`就是答案
:::spoiler Flag
Flag: `Ryan_VanAntwerp_thesis.pdf`
:::

## ==Q19==
> What was the name of the Disk Encryption application Installed on the victim system? (two words space separated) 

### Recon
題目要求找出磁碟加密的軟體名稱是甚麼，看到的第一直覺是想要找出駭客在受害者電腦安裝的軟體有哪些，首先看到BCWipe，根據[軟體王的介紹](https://www.softking.com.tw/6785/)
> 這個軟體提供了許多種的安全級別來讓你選擇所要清除的文件文件。
> 別認為把 Windows 的資源回收筒清掉就算將文件都刪除了而放心？然而這些文件大多仍然存在你的電腦的硬碟中，隨時都可能被有心人士給取走。
> 而這個幫你把硬碟清的一乾二淨、絲毫不留痕。對於一些存有重要敏感文件的電腦，該軟體會是你一個強力而有力的文件清除工具。

進到該資料夾可以看到有一個奇怪的log(==UnInstall.log==)，看了一下應該是有關卸載的初步資訊
:::spoiler UnInstall.log
```
C 0 6/21/2016 4:44 AM
8 0 AdmPrivRequired
C 0 6/21/2016 4:44 AM
12 0 C:\Program Files (x86)\Jetico
C 0 6/21/2016 4:44 AM
0 0 C:\Program Files (x86)\Jetico\BCWipe
C 0 6/21/2016 4:44 AM
6 0 BCWipe 6.0
C 0 6/21/2016 4:44 AM
80000001 0 C:\Windows\system32\drivers\bcswap.sys
C 0 6/21/2016 4:44 AM
80000001 0 C:\Windows\system32\drivers\fsh.sys
C 0 6/21/2016 4:44 AM
80000001 0 C:\Windows\system32\drivers\MftWipeFilter.sys
C 0 6/21/2016 4:44 AM
B 0 "C:\Program Files (x86)\Jetico\BCWipe\BCWipeTM.exe" uninstall
C 0 6/21/2016 4:44 AM
12 0 C:\Program Files (x86)\Jetico\Shared\
C 0 6/21/2016 4:44 AM
1 0 C:\Program Files (x86)\Jetico\Shared\BCShExt.dll
C 0 6/21/2016 4:44 AM
1 0 C:\Program Files (x86)\Jetico\Shared\BCWipe.dll
C 0 6/21/2016 4:44 AM
1 0 C:\Program Files (x86)\Jetico\Shared\BCWipeLib2.dll
C 0 6/21/2016 4:44 AM
12 0 C:\Program Files (x86)\Jetico\Shared64\
C 0 6/21/2016 4:44 AM
80000001 0 C:\Program Files (x86)\Jetico\Shared64\BCShExt.dll
C 0 6/21/2016 4:44 AM
80000001 0 C:\Program Files (x86)\Jetico\Shared64\langfile2.dll
C 0 6/21/2016 4:44 AM
1 0 C:\Windows\BCUnInstall.exe
C 0 6/21/2016 4:44 AM
5 2 SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\BCWipe.exe
C 0 6/21/2016 4:44 AM
5 2 SOFTWARE\Jetico
C 0 6/21/2016 4:44 AM
5 1 SOFTWARE\Jetico
C 0 6/21/2016 4:44 AM
5 2 SOFTWARE\Jetico\BCWipe
C 0 6/21/2016 4:44 AM
5 1 SOFTWARE\Jetico\BCWipe
C 0 6/21/2016 4:44 AM
5 0 CLSID\{7850a720-705f-11d0-a9eb-0080488625e5}
C 0 6/21/2016 4:44 AM
5 0 *\shellex\ContextMenuHandlers\BCShellMenu
C 0 6/21/2016 4:44 AM
5 0 Drive\shellex\ContextMenuHandlers\BCShellMenu
C 0 6/21/2016 4:44 AM
5 0 Drive\shellex\PropertySheetHandlers\BCShellPage
C 0 6/21/2016 4:44 AM
5 0 Drive\shellex\DragDropHandlers\BCShellMenu
C 0 6/21/2016 4:44 AM
5 0 Folder\shellex\ContextMenuHandlers\BCShellMenu
C 0 6/21/2016 4:44 AM
5 0 Directory\shellex\DragDropHandlers\BCShellMenu
C 0 6/21/2016 4:44 AM
5 0 CLSID\{645FF040-5081-101B-9F08-00AA002F954E}\Shell\YBCWipe
C 0 6/21/2016 4:44 AM
5 0 CLSID\{645FF040-5081-101B-9F08-00AA002F954E}\Shell\YBCWipe\command
C 0 6/21/2016 4:44 AM
80000005 0 CLSID\{7850a720-705f-11d0-a9eb-0080488625e5}
C 0 6/21/2016 4:44 AM
80000005 0 CLSID\{645FF040-5081-101B-9F08-00AA002F954E}\Shell\YBCWipe
C 0 6/21/2016 4:44 AM
80000005 0 CLSID\{645FF040-5081-101B-9F08-00AA002F954E}\Shell\YBCWipe\command
C 0 6/21/2016 4:44 AM
5 2 SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BCWipe
C 0 6/21/2016 4:44 AM
10 2 SOFTWARE\Microsoft\Windows\CurrentVersion\Run\BCWipeTM Startup
C 0 6/21/2016 4:44 AM
8000000A 0 BCSWAP
C 0 6/21/2016 4:44 AM
5 2 SOFTWARE\Jetico\BCWipe\Service\LogOff
C 0 6/21/2016 4:44 AM
5 2 SOFTWARE\Jetico\BCWipe\Service\Startup
C 0 6/21/2016 4:44 AM
5 2 SOFTWARE\Jetico\BCWipe\Service\Terminate
C 0 6/21/2016 4:44 AM
5 2 SOFTWARE\Jetico\BCWipe\Service\Startup1
C 0 6/21/2016 4:44 AM
A 0 BCWipeSvc
C 0 6/21/2016 4:44 AM
B 0 "C:\Program Files (x86)\Jetico\BCWipe\BCWipeSvc.exe" -remove
C 0 6/21/2016 4:44 AM
19 0 C:\Program Files (x86)\Jetico\BCWipe\bcgpupdt.dll$Remove$C:\Program Files (x86)\Jetico\BCWipe\BCWipeTM.exe
C 0 6/21/2016 4:44 AM
8000000A 0 fsh
C 0 6/21/2016 4:44 AM
8000000A 0 MftWipeFilter
C 0 6/21/2016 4:44 AM
7 0 C:\ProgramData\Microsoft\Windows\Start Menu\Programs\BCWipe
C 0 6/21/2016 4:44 AM
4 0 C:\ProgramData\Microsoft\Windows\Start Menu\Programs\BCWipe\
C 0 6/21/2016 4:44 AM
3 0 C:\ProgramData\Microsoft\Windows\Start Menu\Programs\BCWipe\BCWipe Help.lnk
C 0 6/21/2016 4:44 AM
3 0 C:\ProgramData\Microsoft\Windows\Start Menu\Programs\BCWipe\ReadMe.lnk
C 0 6/21/2016 4:44 AM
3 0 C:\ProgramData\Microsoft\Windows\Start Menu\Programs\BCWipe\About BCWipe.lnk
C 0 6/21/2016 4:44 AM
3 0 C:\ProgramData\Microsoft\Windows\Start Menu\Programs\BCWipe\BCWipe.lnk
C 0 6/21/2016 4:44 AM
3 0 C:\ProgramData\Microsoft\Windows\Start Menu\Programs\BCWipe\Crypto Swap.lnk
C 0 6/21/2016 4:44 AM
3 0 C:\ProgramData\Microsoft\Windows\Start Menu\Programs\BCWipe\BCWipe Task Manager.lnk
C 0 6/21/2016 4:44 AM
3 0 C:\ProgramData\Microsoft\Windows\Start Menu\Programs\BCWipe\Automatic Update.lnk
C 0 6/21/2016 4:53 AM
C 1 DisableReboot
```
:::
從這份文件中就可以看到有一個軟體叫做Crypto Swap，就是我們要找的目標

:::spoiler Flag
Flag: `Crypto Swap`
:::

## ==Q20==
> What are the serial numbers of the two identified USB storage? 

### Recon
這一題也是參考[^hunter-wp-2]才知道要從registry中撈資訊

### Exploit
在`SYSTEM/ControlSet001/Enum/USBSTOR/`中就有紀錄關於USB完整的資訊
![圖片.png](https://hackmd.io/_uploads/B1SiVsxm6.png)

和自己電腦中比較，不知到為甚麼居然沒有USBSTOR
![圖片.png](https://hackmd.io/_uploads/Hy15rjgQa.png)

:::spoiler Flag
Flag: `07B20C03C80830A9,AAI6UXDKZDV8E9OU`(serial number最後沒有`&0`這兩個字元)
:::

## Reference
[^hunter-wp]:[ Cyberdefenders.org Hunter Walkthrough ](https://youtu.be/0P0DTXiG9qE?si=PLyJ2Y9gvrt9ZePo)
[^hunter-wp-2]:[Cyberdefenders.org Hunter Walkthrough](https://medium.com/@cyberforensicator57/cyberdefenders-org-hunter-walkthrough-65c0c6cb8e87)