---
title: Forensics Cheat Sheet
tags: [Forensics, Tools, CTF]

category: "Tools｜CTF"
date: 2024-01-31
---

# Forensics Cheat Sheet
<!-- more -->

## Forensics Tools
* [LNK Parser](https://code.google.com/archive/p/lnk-parser/downloads)
* [PECmd - Prefetch parser](https://ericzimmerman.github.io/#!index.md): 用來解析 Windows Prefetch 檔案
    ```bash
    $ PECmd.exe -f C:\\Windows\\Prefetch\\<PrefetchFile>
    ```
* [EvtxECmd - Event Log Parser](https://ericzimmerman.github.io/#!index.md)
    ```bash
    $ EvtxECmd.exe -f Security.evtx --csv out
    ```
* [JLECmd - Jump List Parser](https://ericzimmerman.github.io/#!index.md)
    ```bash
    $ ./JLECmd.exe -f aa28770954eaeaaa.customDestinations-ms
    ```

### Microsoft Office
* [Oletools](https://github.com/decalage2/oletools): 是一套專為分析 Microsoft Office 文件（如 doc, xls, docx, xlsm）而設計的 Python 工具集，用於偵測潛在的惡意Macro（VBA巨集）和分析OLE2檔案結構
    ```bash
    $ pip install -U oletools
    $ olevba <filename> # 用於提取、解析 Word 或 Excel 中的 VBA 巨集代碼，並檢測是否有可疑行為（如啟動程式、下載檔案）
    ```
* [xlmdeobfuscator](https://github.com/DissectMalware/XLMMacroDeobfuscator): 是一款用於分析惡意 Excel 4.0 (XLM) 巨集的開源工具。它透過模擬執行和暴破技術，能將混淆的巨集指令還原，直接提取出網址、shell 執行命令等威脅情資 (IOCs)，幫助分析人員快速辨識惡意文件。 
    ```bash
    $ pip install XLMMacroDeobfuscator
    $ xlmdeobfuscator --file <惡意文件.xlsm> # 對惡意 Excel 文件進行分析並輸出還原後的程式碼
    $ xlmdeobfuscator --file <文件> --no-indent --output-formula-format "[[INT-FORMULA]]" # 僅顯示反混淆後的公式
    ```
* [oledump.py](https://github.com/DidierStevens/DidierStevensSuite/blob/master/oledump.py): 如果不想要點開xlsm，而是直接把其中的vba dump下來，就可以用這個
    ```bash
    $ python oledump.py invoice-42369643.xlsm 
    A: xl/vbaProject.bin 
    A1: 573 'PROJECT' 
    A2: 113 'PROJECTwm' 
    A3: 97 'UZdcUQeJ/\x01CompObj' 
    A4: 290 'UZdcUQeJ/\x03VBFrame' 
    A5: 94 'UZdcUQeJ/f' 
    A6: 7124 'UZdcUQeJ/o' 
    A7: M 11454 'VBA/Module1' # M 代表Module
    A8: m 1196 'VBA/Sheet1' # m 應該不重要
    A9: m 1015 'VBA/ThisWorkbook' 
    A10: M 1566 'VBA/UZdcUQeJ'
    $ python oledump.py -s 7 -v invoice-42369643.xlsm # 把A7的部分dump下來
    ```

### Disk Analysis
* [Foremost](https://darkranger.no-ip.org/archives/v5/document/linux/foremost_recovery.htm): 針對所支援的檔案結構去進行資料搜尋與救援
    ```bash
    $ foremost -v <filename>
    ```
* [Sleuth kit/Autopsy](https://blog.csdn.net/wxh0000mm/article/details/99447206)
* [FTK Imager](https://www.exterro.com/ftk-imager)
* [Logontracer]({{base.url}}/How-to-install-LogonTracer/): Just use GUI to present event log traced on windows
    ```bash
    $ python logontracer.py -r -o 8000 -u neo4j -p neo4j -s localhost
    ```

### Memory Forensics
#### Volatility
* 建議直接使用[windown protable version](https://www.volatilityfoundation.org/releases)會比較穩定而且不需要處理環境的問題
* [Volatility - Cheat Sheet](https://hackmd.io/@TuX-/BymMpKd0s)
* [Volatility 3](https://github.com/volatilityfoundation/volatility3)
    
    Set up & How2Use
    * [Windows Volatility 3 Problems & Solutions](https://blog.csdn.net/u011250160/article/details/120461405)
    * [Windows Set up Tutorials](https://volatility3.readthedocs.io/en/latest/getting-started-windows-tutorial.html)
    
    ```bash
    $ git clone https://github.com/volatilityfoundation/volatility3
    $ cd volatility3
    $ pip install -r requirement.txt
    $ python vol.py -f <path to memory image> plugin_name plugin_option
    $ python vol.py -h # For help
    ```
    
* [Volatility 2](https://github.com/volatilityfoundation/volatility)
    ```bash
    $ conda create --name py27 python=2.7
    $ conda activate py27
    $ git clone https://github.com/volatilityfoundation/volatility
    $ cd volatility
    $ pip install pycrypto
    $ pip install distorm3
    $ python vol.py -f <path to memory image> plugin_name plugin_option
    $ python vol.py -h # For help
    ```

* 教學
    `$ ./vol.exe -f <image name> --profile <profile name> <cmd>`
    ```bash
    $ ./vol.exe -f <image name> --profile <profile name> <cmd>

    # <cmd>
    imageinfo # 看目前的memory來自哪一種profile，e.g. WinXPSP2x86, WinXPSP3x86
    pslist # 查看process info

    malfind --pid <pid> --dump-dir <output folder> # 如果要dump被injected過的process
    dlllist --pid <pid> # 查看該process load什麼樣的dll
    ldrmodules --pid <pid> # ldrmodules: 更進階的dlllist，可以顯示被隱藏的dll，以及dll的狀態
    handles --pid <pid> # 查看該process的handle有哪些
    
    hashdump > ntlm.hash # dump hash
    dumpfile -n -D <output path> -Q <memory address>

    timeliner # 如果是要找到某個東西的timestamp，可以考慮直接用timeliner這個plubin，主要的功能是就是建立記憶體中的各種痕跡資訊的時間線
    consoles # console中的command紀錄
    iehistory # 查看iexplorer的紀錄
    printkey -K <機碼的路徑> # 印出機碼路徑/子路徑/內容
    
    netscan # 查看網路連線紀錄
    filescan # 可以從mem中找出各種file的path
    yarascan -Y "example strings" # 在memory中用yarascan去search不同的pattern
    ```

#### 其他
* [vmss2core](https://flings.vmware.com/vmss2core): .vmss是VMware經過轉換的snapshot，而這個工具可以把snapshot轉換成memory dump
    ```bash
    $ vmss2core.exe -W <.vmss file>
    ```

### Registry
* [Regshot](https://sourceforge.net/projects/regshot/): 可以snapshot目前registry的狀態並且和第二次的snapshot做比較
* [Registry Explorer](https://ericzimmerman.github.io/#!index.md): 用來分析reg file

#### Registry在哪裡
* SOFTWARE: `root/Windows/System32/config/SOFTWARE`
    ```bash
    SOFTWARE/Microsoft/Windows NT/CurrentVersion # 原本電腦OS的基本資訊(Build Number/Product Name/)
    SOFTWARE/Microsoft/Windows NT/CurrentVersion/ProfileList # 檢查SID
    SOFTWARE/Microsoft/Windows NT/CurrentVersion/Winlogon # 查看登入
    SOFTWARE/Microsoft/Windows/CurrentVersion/Run # StartUp Run
    ```
* SYSTEM: `root/Windows/System32/config/SYSTEM`
    ```bash
    SYSTEM/ControlSet001/Control/ComputerName/ComputerName # 電腦名稱
    SYSTEM/ControlSet001/Control/TimeZoneInformation # 時區
    SYSTEM/ControlSet001/Control/Session Manager/Environment/ # CPU架構
    SYSTEM/ControlSet001/Services/Tcpip/Parameters/Interfaces/ # 電腦IP/DHCP相關資訊
    SYSTEM/ControlSet001/Enum/USBSTOR/ # USB資訊
    ```
* NTUSER.DAT: `root/Users/<username>/NTUSER.DAT`
    ```bash
    root/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/UserAssist # UserAssit
    root/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/RecentDocs # Recent Docs
    ```
* \$MFT: `root/$MFT`
* Database相關
    ```bash
    ./Users/<username>/AppData/Local/Google/Chrome/User Data/Default/History # Chrome History
    ./Users/<username>/AppData/Roaming/Mozilla/Firefox/Profiles/<random>.default-release/places.sqlite # Firefox History
    ./Users/<username>/AppData/Roaming/Skype/<account name> # Skype Chat History
    ```
* Taskbar相關
    ```bash
    ./Users/<username>/AppData/Roaming/Microsoft/Internet Explorer/Quick Launch/User Pinned/TaskBar
    ```

### Incident Response (查看Log)
* 如果是直接給一個log file，那麼多多利用unix command會方便很多grep, cat, cut, uniq, sort...
    ```bash
    $ cat access.log | cut -d '"' -f 6| sort | uniq | grep -v -E "AH01276|Mozilla" --color=auto
    ```
* [Timeline Explorer](https://ericzimmerman.github.io/#!index.md):為時間軸資訊分析提供了一個全面、高效且高度整合的系統，用於搜尋不同資源的時間線軸資訊，並可以輕鬆過濾、分組與排序
* For Linux: [aureport 教學]({{base.url}}/BTLO-Paranoid/): 是 Linux 系統上 auditd (Linux Audit Daemon) 的報告工具，主要用於 分析系統安全審計日誌 (audit logs)。它屬於 Linux 原生審計與事件監控工具，能幫助系統管理員和資安分析人員快速彙整、搜尋和報告各種安全事件。

## mac-OS
### plist
Apple 系統用來儲存設定與資料的檔案格式
```bash
$ sudo apt install libplist-utils -y
$ plistutil -i <plist file> -o <output file>
```

```bash
./root/System/Library/CoreServices/SystemVersion.plist # System Version
./root/private/var/db/dslocal/nodes/Default/users/<username>.plist # Password information
./root/private/var/db/dslocal/nodes/Default/users/_usbmux.plist # The process responsible for connecting iPhones/iPads with MacOS is lockdown
./root/Users/<username>/Library/Safari/Bookmarks.plist # Browser Bookmark
./root/Users/<username>/Library/Application Support/com.apple.spotlight/com.apple.spotlight.Shortcuts # Spotlight(這個不需要透過plistutil就可以直接cat)
```

### Event Log
* 短期檔案系統變更儲存在`.fseventsd`中，必須使用`mac_apt`這個工具幫忙parse(FSEVENTS): `./root/.fseventsd/`
* ScreenTime: 一樣要透過`mac_apt`幫忙parse(SCREENTIME)，記得要把`RMAdminStore-Local.sqlite-wal`這個檔案和`RMAdminStore-Local.sqlite`放在一起執行: `./root/private/var/folders/bf/<random strings>/0/com.apple.ScreenTimeAgent/Store/RMAdminStore-Local.sqlite`

### Database
* Note: `./root/Users/<username>/Library/Group Containers/group.com.apple.notes`
* Quarantined Events: `./root/Users/<username>/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2`
* Messages: `./root/Users/<username>/Library/Messages/chat.db`