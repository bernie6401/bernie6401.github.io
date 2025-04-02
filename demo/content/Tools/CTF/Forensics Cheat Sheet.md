---
title: Forensics Cheat Sheet
tags: [Forensics, Tools, CTF]

---

# Forensics Cheat Sheet
## Windows
### Where
* SOFTWARE: `root/Windows/System32/config/SOFTWARE`
* SYSTEM: `root/Windows/System32/config/SYSTEM`
* NTUSER.DAT: `root/Users/{username}/NTUSER.DAT`
* \$MFT: `root/$MFT`

### SOFTWARE Information
* 原本電腦OS的基本資訊(Build Number/Product Name/):
    `SOFTWARE/Microsoft/Windows NT/CurrentVersion`
* 檢查SID:
    `SOFTWARE/Microsoft/Windows NT/CurrentVersion/ProfileList`
* 查看登入:
    `SOFTWARE/Microsoft/Windows NT/CurrentVersion/Winlogon`
* StartUp Run:
    `SOFTWARE/Microsoft/Windows/CurrentVersion/Run`
#### NTUSER.DAT(每個使用者都不一樣)
* UserAssit:
    `root/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/UserAssist`
* Recent Docs:
    `root/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/RecentDocs`
### System Information
* 電腦名稱:
    `SYSTEM/ControlSet001/Control/ComputerName/ComputerName`
* 電腦IP/DHCP相關資訊:
    `SYSTEM/ControlSet001/Services/Tcpip/Parameters/Interfaces/`
* 時區:
    `SYSTEM/ControlSet001/Control/TimeZoneInformation`
* USB資訊:
    `SYSTEM/ControlSet001/Enum/USBSTOR/`
* CPU架構:
    `SYSTEM/ControlSet001/Control/Session Manager/Environment/`


### Database
* Chrome History:
    `./Users/{username}/AppData/Local/Google/Chrome/User Data/Default/History`
* Firefox History:
    `./Users/{username}/AppData/Roaming/Mozilla/Firefox/Profiles/{random}.default-release/places.sqlite`
* Skype Chat History:
    `./Users/{username}/AppData/Roaming/Skype/{account name}`
    
### Taskbar
* `./Users/{username}/AppData/Roaming/Microsoft/Internet Explorer/Quick Launch/User Pinned/TaskBar`


## mac-OS
### plist
```bash
$ sudo apt install libplist-utils -y
$ plistutil -i {plist file} -o {output file}
```
* System Version:
    `./root/System/Library/CoreServices/SystemVersion.plist`
* Browser Bookmark
    `./root/Users/{username}/Library/Safari/Bookmarks.plist`
* Password information
    `./root/private/var/db/dslocal/nodes/Default/users/{username}.plist`
* The process responsible for connecting iPhones/iPads with MacOS is lockdown
    `./root/private/var/db/dslocal/nodes/Default/users/_usbmux.plist`
* Spotlight(這個不需要透過plistutil就可以直接cat)
    `./root/Users/{username}/Library/Application Support/com.apple.spotlight/com.apple.spotlight.Shortcuts`
### Event Log
* 短期檔案系統變更儲存在`.fseventsd`中，必須使用`mac_apt`這個工具幫忙parse(FSEVENTS)
    `./root/.fseventsd/`
* ScreenTime: 一樣要透過`mac_apt`幫忙parse(SCREENTIME)，記得要把`RMAdminStore-Local.sqlite-wal`這個檔案和`RMAdminStore-Local.sqlite`放在一起執行
    `./root/private/var/folders/bf/{random strings}/0/com.apple.ScreenTimeAgent/Store/RMAdminStore-Local.sqlite`
### Database
* Note
    `./root/Users/{username}/Library/Group Containers/group.com.apple.notes`
* Quarantined Events
    `./root/Users/{username}/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2`
* Messages
    `./root/Users/{username}/Library/Messages/chat.db`
    
## Volatilitys
* [主要的CheatSheet](https://hackmd.io/@TuX-/BymMpKd0s)
* ldrmodules: 更進階的dlllist，可以顯示被隱藏的dll，以及dll的狀態
    `$ ./volatility_2.6_win64_standalone.exe -f {image name} --profile {profile name} ldrmodules --pid {pid}`
* 如果要dump被injected過的process:
    `$ ./volatility_2.6_win64_standalone.exe -f {image name} --profile {profile name} malfind --pid {pid} --dump-dir={output folder}`
* dump hash
    `$ ./volatility_2.6_win64_standalone.exe -f {image name} --profile {profile name} hashdump > ntlm.hash`
* 如果是要找到某個東西的timestamp，可以考慮直接用timeliner這個plubin，主要的功能是就是建立記憶體中的各種痕跡資訊的時間線
    `$ ./volatility_2.6_win64_standalone.exe -f {image name} --profile {profile name} timeliner `
* 查看網路連線紀錄
    `$ ./volatility_2.6_win64_standalone.exe -f {image name} --profile {profile name} netscan`
* 在memory中用yarascan去search不同的pattern
    `$ ./volatility_2.6_win64_standalone.exe -f {image name} --profile {profile name} yarascan -Y "example strings"`
* console中的command紀錄
    `$ ./volatility_2.6_win64_standalone.exe -f {image name} --profile {profile name} consoles`
* 查看iexplorer的紀錄
    `$ ./volatility_2.6_win64_standalone.exe -f {image name} --profile {profile name} iehistory`