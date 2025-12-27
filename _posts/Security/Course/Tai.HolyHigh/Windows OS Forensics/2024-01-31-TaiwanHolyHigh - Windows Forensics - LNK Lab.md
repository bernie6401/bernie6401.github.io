---
title: TaiwanHolyHigh - Windows Forensics - LNK Lab
tags: [TaiwanHolyHigh, Forensics, Windows]

category: "Security｜Course｜Tai.HolyHigh｜Windows OS Forensics"
---

# TaiwanHolyHigh - Windows Forensics - LNK Lab
<!-- more -->
[TOC]

:::info
以下引用若無特別說明皆來自於講師的上課簡報
:::

## Background
* What is .LNK?
    > LNK 檔為 Windows 系統中，執行程式或開啟檔案後會留存的捷徑檔，該檔案內會有相當多的資訊
* Where is .LNK?
    > 預設 LNK 檔案會放在使用者目錄下，可透過以下指令檢視：`$ dir c:\Users\{username}\*.lnk /b /s`
    :::spoiler 執行結果
    ```bash
    $ dir c:\Users\Bernie\*.lnk /b /s
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group1\1 - Desktop.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group2\1 - Run.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group2\2 - Search.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group2\3 - Windows Explorer.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group2\4 - Control Panel.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group2\5 - Task Manager.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group3\01a - Windows PowerShell.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group3\02a - Windows PowerShell.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group3\03 - Computer Management.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group3\04 - Disk Management.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group3\04-1 - NetworkStatus.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group3\05 - Device Manager.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group3\06 - SystemAbout.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group3\07 - Event Viewer.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group3\08 - PowerAndSleep.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group3\09 - Mobility Center.lnk
    c:\Users\Bernie\AppData\Local\Microsoft\Windows\WinX\Group3\10 - AppsAndFeatures.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\Chromium.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\File Shredder.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\Google Chrome.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\Microsoft Edge.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\Oracle VM VirtualBox.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\Shows Desktop.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\Window Switcher.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\AnyDesk.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\Discord.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\Excel.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\File Explorer.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\Firefox.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\LINE (2).lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\PowerPoint.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\Sublime Text 3.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\Task Manager.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\The Interactive Disassembler (2).lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\The Interactive Disassembler.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\Visual Studio Code.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\VMware Workstation Pro.lnk
    c:\Users\Bernie\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\Word.lnk
    c:\Users\Bernie\Desktop\Test-Dragon.lnk
    c:\Users\Bernie\Links\Desktop.lnk
    c:\Users\Bernie\Links\Downloads.lnk
    c:\Users\Bernie\OneDrive\Personal Vault.lnk
    ```
    :::

## Lab
可以先到[這邊](https://code.google.com/archive/p/lnk-parser/downloads)下載`lnk_parser_cmd.exe`

### ==利用lnk parser leak info==
```bash
$ lnk_parser_cmd.exe
Please enter the name of the shortcut file, or a directory you wish to scan: D:\NTU\Taiwan Holy High 8-th\Windows OS Forensics\LNK
Select a report to output:
 1      HTML
 2      Comma-separated values (CSV)
 3      HTML and CSV
 0      No report
Select: 0
Do you want to output results to the console? (Y/N) y
```
:::danger
切記，輸入要parse的folder中不能有任何中文字，不然會無法正確parse到路徑
:::
:::spoiler 執行結果
```bash
[Filename]:                             D:\NTU\Taiwan Holy High 8-th\Windows OS Forensics\LNK\$RU2R11Q.lnk

[Header]
Date created:                           01/15/2022 (09:05:22.858) [UTC]
Last accessed:                          01/15/2022 (09:12:41.429) [UTC]
Last modified:                          01/15/2022 (09:12:41.429) [UTC]
File size:                              36735600 bytes
File attributes:                        0x00000020      (FILE_ATTRIBUTE_ARCHIVE)
Icon index:                             0
ShowWindow value:                       1               (SW_SHOWNORMAL / SW_NORMAL)
Hot key value:                          0x0000          (None)
Link flags:                             0x0000009b      (HasLinkTargetIDList, HasLinkInfo, HasRelativePath, HasWorkingDir, IsUnicode)

[Link Target ID List]
CLSID:                                  20d04fe0-3aea-1069-a2d8-08002b30309d = My Computer

Drive:                                  C:\

Last modified:                          01/15/2022 (09:13:52.0) [UTC]
Folder attributes:                      0x00000010      (FILE_ATTRIBUTE_DIRECTORY)
Short directory name:                   PROGRA~1
Date created:                           03/19/2019 (04:52:44.0) [UTC]
Last accessed:                          01/15/2022 (09:13:52.0) [UTC]
Long directory name:                    Program Files

Last modified:                          01/15/2022 (09:13:22.0) [UTC]
Folder attributes:                      0x00000010      (FILE_ATTRIBUTE_DIRECTORY)
Short directory name:                   EnCase21.4
Date created:                           01/15/2022 (09:05:20.0) [UTC]
Last accessed:                          01/15/2022 (09:14:06.0) [UTC]
Long directory name:                    EnCase21.4

File size:                              36735600 bytes
Last modified:                          01/15/2022 (09:12:42.0) [UTC]
File attributes:                        0x00000020      (FILE_ATTRIBUTE_ARCHIVE)
8.3 filename:                           EnCase.exe
Date created:                           01/15/2022 (09:05:24.0) [UTC]
Last accessed:                          01/15/2022 (09:12:42.0) [UTC]
Long filename:                          EnCase.exe

[Link Info]
Location flags:                         0x00000001      (VolumeIDAndLocalBasePath)
Drive type:                             3               (DRIVE_FIXED)
Drive serial number:                    d421-3ddd
Volume label (ASCII):
Local path (ASCII):                     C:\Program Files\EnCase21.4\EnCase.exe

[String Data]
Relative path (UNICODE):                ..\..\..\Program Files\EnCase21.4\EnCase.exe
Working Directory (UNICODE):            C:\Program Files\EnCase21.4\

[Known Folder Location]
Known folder GUID:                      905e63b6-c1bf-494e-b29c-65b732d3d21a = ProgramFiles
First child segment offset:             145 bytes

[Metadata Property Store]
Property set GUID:                      46588ae2-4cbc-4338-bbfc-139326986dce
ID:                                     4
Value:                                  0x001f (VT_LPWSTR)      S-1-5-21-4168624370-2151151290-4123834974-1001

Property set GUID:                      446d16b1-8dad-4870-a748-402ea43d788c
ID:                                     104
Value:                                  0x0048 (VT_CLSID)       CLSID: be21401b-2494-49a2-983c-593efc9b1259

[Special Folder Location]
Special folder identifier:              38              (ProgramFiles)
First child segment offset:             145 bytes

[Distributed Link Tracker Properties]
Version:                                0
NetBIOS name:                           desktop-3f9joqf
Droid volume identifier:                8e80a25c-2cb6-462c-ae5a-2db3ddf2b48a
Droid file identifier:                  937694df-75e1-11ec-90a7-e8f408da009c
Birth droid volume identifier:          8e80a25c-2cb6-462c-ae5a-2db3ddf2b48a
Birth droid file identifier:            937694df-75e1-11ec-90a7-e8f408da009c
MAC address:                            e8:f4:08:da:00:9c
UUID timestamp:                         01/15/2022 (09:00:24.375) [UTC]
UUID sequence number:                   4263


[Filename]:                             D:\NTU\Taiwan Holy High 8-th\Windows OS Forensics\LNK\Cavin Weapons.ppt.LNK

[Header]
Date created:                           02/03/2011 (00:53:00.789) [UTC]
Last accessed:                          02/03/2011 (00:53:00.789) [UTC]
Last modified:                          02/03/2011 (00:52:27.152) [UTC]
File size:                              441856 bytes
File attributes:                        0x00000020      (FILE_ATTRIBUTE_ARCHIVE)
Icon index:                             0
ShowWindow value:                       1               (SW_SHOWNORMAL / SW_NORMAL)
Hot key value:                          0x0000          (None)
Link flags:                             0x00000083      (HasLinkTargetIDList, HasLinkInfo, IsUnicode)

[Link Target ID List]
CLSID:                                  20d04fe0-3aea-1069-a2d8-08002b30309d = My Computer

Drive:                                  F:\

File size:                              441856 bytes
Last modified:                          02/03/2011 (00:52:28.0) [UTC]
File attributes:                        0x00000020      (FILE_ATTRIBUTE_ARCHIVE)
8.3 filename:                           CAVINW~2.PPT
Date created:                           02/03/2011 (00:53:02.0) [UTC]
Last accessed:                          02/03/2011 (00:53:02.0) [UTC]
Long filename:                          Cavin Weapons.ppt

[Link Info]
Location flags:                         0x00000001      (VolumeIDAndLocalBasePath)
Drive type:                             3               (DRIVE_FIXED)
Drive serial number:                    da1b-b94d
Volume label (ASCII):                   Secret
Local path (ASCII):                     F:\Cavin Weapons.ppt

[Distributed Link Tracker Properties]
Version:                                0
NetBIOS name:                           cavin
Droid volume identifier:                02ea32b0-f9e6-4e44-93b3-9f8f897419a5
Droid file identifier:                  bdbaaf06-2f2a-11e0-a073-000c297f12a0
Birth droid volume identifier:          02ea32b0-f9e6-4e44-93b3-9f8f897419a5
Birth droid file identifier:            bdbaaf06-2f2a-11e0-a073-000c297f12a0
MAC address:                            00:0c:29:7f:12:a0
UUID timestamp:                         02/03/2011 (00:15:43.937) [UTC]
UUID sequence number:                   8307


[Filename]:                             D:\NTU\Taiwan Holy High 8-th\Windows OS Forensics\LNK\OWAT Proposal - Malone.lnk

[Header]
Date created:                           02/01/2011 (01:42:46.831) [UTC]
Last accessed:                          02/01/2011 (01:42:49.753) [UTC]
Last modified:                          02/01/2011 (01:42:49.909) [UTC]
File size:                              47694 bytes
File attributes:                        0x00000020      (FILE_ATTRIBUTE_ARCHIVE)
Icon index:                             0
ShowWindow value:                       1               (SW_SHOWNORMAL / SW_NORMAL)
Hot key value:                          0x0000          (None)
Link flags:                             0x0020009b      (HasLinkTargetIDList, HasLinkInfo, HasRelativePath, HasWorkingDir, IsUnicode, DisableKnownFolderTracking)

[Link Target ID List]
CLSID:                                  031e4825-7b94-4dc3-b131-e946b44c8dd5 = UsersLibraries

CLSID:                                  7b0db17d-9cd2-4a93-9733-46cc89022e7c = DocumentsLibrary

[Property Store]
Property set GUID:                      b725f130-47ef-101a-a5f1-02608c9eebac
ID:                                     System.ItemTypeText
Value:                                  0x001f (VT_LPWSTR)      My Documents
ID:                                     System.DateCreated
Value:                                  0x0040 (VT_FILETIME)    04/30/2010 (00:10:56.0) [UTC]
ID:                                     System.FileAttributes
Value:                                  0x0013 (VT_UI4)         0x00000011 = 17
ID:                                     System.DateModified
Value:                                  0x0040 (VT_FILETIME)    02/01/2011 (01:43:28.0) [UTC]
ID:                                     System.DateAccessed
Value:                                  0x0040 (VT_FILETIME)    02/01/2011 (01:43:28.0) [UTC]

Property set GUID:                      446d16b1-8dad-4870-a748-402ea43d788c
ID:                                     System.ThumbnailCacheId
Value:                                  0x0015 (VT_UI8)         0xd3331b2d2174203b = 15218537446463774779

Property set GUID:                      28636aa6-953d-11d2-b5d6-00c04fd918d0
ID:                                     System.SFGAOFlags
Value:                                  0x0013 (VT_UI4)         0x7080017f = 1887437183
ID:                                     32
Value:                                  0x1011 (VT_VECTOR | VT_UI1)     Vector count: 385
                                        CLSID:                  20d04fe0-3aea-1069-a2d8-08002b30309d = My Computer

                                        Drive:                  C:\

                                        Last modified:          04/30/2010 (00:10:54.0) [UTC]
                                        Folder attributes:      0x00000011      (FILE_ATTRIBUTE_READONLY, FILE_ATTRIBUTE_DIRECTORY)
                                        Short directory name:   Users
                                        Date created:           07/14/2009 (02:37:06.0) [UTC]
                                        Last accessed:          04/30/2010 (00:10:54.0) [UTC]
                                        Long directory name:    Users
                                        Argument:               @shell32.dll,-21813

                                        Last modified:          04/30/2010 (00:11:30.0) [UTC]
                                        Folder attributes:      0x00000010      (FILE_ATTRIBUTE_DIRECTORY)
                                        Short directory name:   CLIFF~1.CAV
                                        Date created:           04/30/2010 (00:10:54.0) [UTC]
                                        Last accessed:          04/30/2010 (00:11:30.0) [UTC]
                                        Long directory name:    Cliff.Cavin

                                        Last modified:          02/01/2011 (01:43:28.0) [UTC]
                                        Folder attributes:      0x00000011      (FILE_ATTRIBUTE_READONLY, FILE_ATTRIBUTE_DIRECTORY)
                                        Short directory name:   DOCUME~1
                                        Date created:           04/30/2010 (00:10:56.0) [UTC]
                                        Last accessed:          02/01/2011 (01:43:28.0) [UTC]
                                        Long directory name:    Documents
                                        Argument:               @shell32.dll,-21770
ID:                                     System.ParsingName
Value:                                  0x001f (VT_LPWSTR)      Documents
ID:                                     System.ItemType
Value:                                  0x001f (VT_LPWSTR)      Directory

Property set GUID:                      1e3ee840-bc2b-476c-8237-2acd1a839b22
ID:                                     8
Value:                                  0x001f (VT_LPWSTR)      C:\Users\Cliff.Cavin\Documents
ID:                                     System.Kind
Value:                                  0x101f (VT_VECTOR | VT_LPWSTR)  Vector count: 1 : folder
[/Property Store]

[Property Store]
Property set GUID:                      b725f130-47ef-101a-a5f1-02608c9eebac
ID:                                     System.ItemTypeText
Value:                                  0x001f (VT_LPWSTR)      OWAT Proposal - Malone
ID:                                     System.DateCreated
Value:                                  0x0040 (VT_FILETIME)    02/01/2011 (01:42:48.0) [UTC]
ID:                                     System.Size
Value:                                  0x0015 (VT_UI8)         0x000000000000ba4e = 47694
ID:                                     System.FileAttributes
Value:                                  0x0013 (VT_UI4)         0x00000020 = 32
ID:                                     System.DateModified
Value:                                  0x0040 (VT_FILETIME)    02/01/2011 (01:42:50.0) [UTC]
ID:                                     System.DateAccessed
Value:                                  0x0040 (VT_FILETIME)    02/01/2011 (01:42:50.0) [UTC]

Property set GUID:                      446d16b1-8dad-4870-a748-402ea43d788c
ID:                                     System.ThumbnailCacheId
Value:                                  0x0015 (VT_UI8)         0x3b279efd2943a71e = 4262550382485677854

Property set GUID:                      28636aa6-953d-11d2-b5d6-00c04fd918d0
ID:                                     System.SFGAOFlags
Value:                                  0x0013 (VT_UI4)         0x48400177 = 1212154231
ID:                                     32
Value:                                  0x1011 (VT_VECTOR | VT_UI1)     Vector count: 513
                                        CLSID:                  20d04fe0-3aea-1069-a2d8-08002b30309d = My Computer

                                        Drive:                  C:\

                                        Last modified:          04/30/2010 (00:10:54.0) [UTC]
                                        Folder attributes:      0x00000011      (FILE_ATTRIBUTE_READONLY, FILE_ATTRIBUTE_DIRECTORY)
                                        Short directory name:   Users
                                        Date created:           07/14/2009 (02:37:06.0) [UTC]
                                        Last accessed:          04/30/2010 (00:10:54.0) [UTC]
                                        Long directory name:    Users
                                        Argument:               @shell32.dll,-21813

                                        Last modified:          04/30/2010 (00:11:30.0) [UTC]
                                        Folder attributes:      0x00000010      (FILE_ATTRIBUTE_DIRECTORY)
                                        Short directory name:   CLIFF~1.CAV
                                        Date created:           04/30/2010 (00:10:54.0) [UTC]
                                        Last accessed:          04/30/2010 (00:11:30.0) [UTC]
                                        Long directory name:    Cliff.Cavin

                                        Last modified:          02/01/2011 (01:43:28.0) [UTC]
                                        Folder attributes:      0x00000011      (FILE_ATTRIBUTE_READONLY, FILE_ATTRIBUTE_DIRECTORY)
                                        Short directory name:   DOCUME~1
                                        Date created:           04/30/2010 (00:10:56.0) [UTC]
                                        Last accessed:          02/01/2011 (01:43:28.0) [UTC]
                                        Long directory name:    Documents
                                        Argument:               @shell32.dll,-21770

                                        File size:              47694 bytes
                                        Last modified:          02/01/2011 (01:42:50.0) [UTC]
                                        File attributes:        0x00000020      (FILE_ATTRIBUTE_ARCHIVE)
                                        8.3 filename:           OWATPR~1.DOC
                                        Date created:           02/01/2011 (01:42:48.0) [UTC]
                                        Last accessed:          02/01/2011 (01:42:50.0) [UTC]
                                        Long filename:          OWAT Proposal - Malone.docx
ID:                                     System.ParsingName
Value:                                  0x001f (VT_LPWSTR)      OWAT Proposal - Malone.docx
ID:                                     System.ItemType
Value:                                  0x001f (VT_LPWSTR)      .docx

Property set GUID:                      1e3ee840-bc2b-476c-8237-2acd1a839b22
ID:                                     8
Value:                                  0x001f (VT_LPWSTR)      C:\Users\Cliff.Cavin\Documents\OWAT Proposal - Malone.docx
ID:                                     System.Kind
Value:                                  0x101f (VT_VECTOR | VT_LPWSTR)  Vector count: 1 : document
[/Property Store]

[Link Info]
Location flags:                         0x00000001      (VolumeIDAndLocalBasePath)
Drive type:                             3               (DRIVE_FIXED)
Drive serial number:                    78eb-e13b
Volume label (ASCII):
Local path (ASCII):                     C:\Users\Cliff.Cavin\Documents\OWAT Proposal - Malone.docx

[String Data]
Relative path (UNICODE):                ..\..\..\..\..\Documents\OWAT Proposal - Malone.docx
Working Directory (UNICODE):            C:\Users\Cliff.Cavin\Documents

[Metadata Property Store]
Property set GUID:                      46588ae2-4cbc-4338-bbfc-139326986dce

[Distributed Link Tracker Properties]
Version:                                0
NetBIOS name:                           cavin
Droid volume identifier:                35e6cda4-852f-4c89-87b8-1b863ffc4d04
Droid file identifier:                  ad7a62e2-2cd5-11e0-b805-000c297f12a0
Birth droid volume identifier:          35e6cda4-852f-4c89-87b8-1b863ffc4d04
Birth droid file identifier:            ad7a62e2-2cd5-11e0-b805-000c297f12a0
MAC address:                            00:0c:29:7f:12:a0
UUID timestamp:                         01/31/2011 (01:01:47.125) [UTC]
UUID sequence number:                   14341

Unknown data at end of file.


[Filename]:                             D:\NTU\Taiwan Holy High 8-th\Windows OS Forensics\LNK\[???]????_20230726.pptx.LNK

[Header]
Date created:                           07/26/2023 (01:33:25.69) [UTC]
Last accessed:                          07/28/2023 (07:57:36.437) [UTC]
Last modified:                          07/26/2023 (05:31:17.399) [UTC]
File size:                              106313921 bytes
File attributes:                        0x00000020      (FILE_ATTRIBUTE_ARCHIVE)
Icon index:                             0
ShowWindow value:                       1               (SW_SHOWNORMAL / SW_NORMAL)
Hot key value:                          0x0000          (None)
Link flags:                             0x00000083      (HasLinkTargetIDList, HasLinkInfo, IsUnicode)

[Link Target ID List]
CLSID:                                  20d04fe0-3aea-1069-a2d8-08002b30309d = My Computer

Drive:                                  D:\

Last modified:                          10/27/2022 (23:44:52.0) [UTC]
Folder attributes:                      0x00000010      (FILE_ATTRIBUTE_DIRECTORY)
Short directory name:                   Training Material
Date created:                           10/27/2022 (23:23:16.0) [UTC]
Last accessed:                          07/28/2023 (07:57:16.0) [UTC]
Long directory name:                    Training Material

File size:                              0 bytes
Last modified:                          07/26/2023 (05:31:30.0) [UTC]
File attributes:                        0x00000010      (FILE_ATTRIBUTE_DIRECTORY)
8.3 filename:                           [
Date created:                           10/27/2022 (23:30:44.0) [UTC]
Last accessed:                          07/28/2023 (07:57:16.0) [UTC]
Long filename:                          [2]????

File size:                              106313921 bytes
Last modified:                          07/26/2023 (05:31:18.0) [UTC]
File attributes:                        0x00000020      (FILE_ATTRIBUTE_ARCHIVE)
Long filename:                          [???]????_20230726.pptx
Date created:                           07/26/2023 (01:33:26.0) [UTC]
Last accessed:                          07/28/2023 (07:57:38.0) [UTC]
Long filename:                          [???]????_20230726.pptx

[Link Info]
Location flags:                         0x00000001      (VolumeIDAndLocalBasePath)
Drive type:                             3               (DRIVE_FIXED)
Drive serial number:                    12a0-18b7
Volume label (ASCII):                   新增磁碟區
Local path (ASCII):                     D:\Training Material\[2]技術課程\[台科大]資訊安全_20230726.pptx

[Metadata Property Store]
Property set GUID:                      446d16b1-8dad-4870-a748-402ea43d788c
ID:                                     104
Value:                                  0x0048 (VT_CLSID)       CLSID: ae790946-95c1-4d5f-b2cb-6d69c7e0fb6a

[Distributed Link Tracker Properties]
Version:                                0
NetBIOS name:                           desktop-3f9joqf
Droid volume identifier:                b60a791e-9325-4178-8dd5-522b787ff4f2
Droid file identifier:                  f6061f31-2b45-11ee-9545-e8f408da009c
Birth droid volume identifier:          b60a791e-9325-4178-8dd5-522b787ff4f2
Birth droid file identifier:            f6061f31-2b45-11ee-9545-e8f408da009c
MAC address:                            e8:f4:08:da:00:9c
UUID timestamp:                         07/25/2023 (23:49:57.539) [UTC]
UUID sequence number:                   5445

Unknown data at end of file.


[Filename]:                             D:\NTU\Taiwan Holy High 8-th\Windows OS Forensics\LNK\[???]????_v0.6.pptx.LNK

[Header]
Date created:                           07/28/2023 (09:12:00.832) [UTC]
Last accessed:                          09/09/2023 (05:22:47.979) [UTC]
Last modified:                          07/29/2023 (08:14:33.586) [UTC]
File size:                              51209593 bytes
File attributes:                        0x00000020      (FILE_ATTRIBUTE_ARCHIVE)
Icon index:                             0
ShowWindow value:                       1               (SW_SHOWNORMAL / SW_NORMAL)
Hot key value:                          0x0000          (None)
Link flags:                             0x00000083      (HasLinkTargetIDList, HasLinkInfo, IsUnicode)

[Link Target ID List]
CLSID:                                  20d04fe0-3aea-1069-a2d8-08002b30309d = My Computer

Drive:                                  D:\

Last modified:                          10/27/2022 (23:44:52.0) [UTC]
Folder attributes:                      0x00000010      (FILE_ATTRIBUTE_DIRECTORY)
Short directory name:                   Training Material
Date created:                           10/27/2022 (23:23:16.0) [UTC]
Last accessed:                          09/09/2023 (05:10:24.0) [UTC]
Long directory name:                    Training Material

File size:                              0 bytes
Last modified:                          07/26/2023 (05:31:28.0) [UTC]
File attributes:                        0x00000010      (FILE_ATTRIBUTE_DIRECTORY)
8.3 filename:                           [
Date created:                           10/27/2022 (23:28:02.0) [UTC]
Last accessed:                          09/09/2023 (05:10:24.0) [UTC]
Long filename:                          [1]????

File size:                              0 bytes
Last modified:                          08/31/2023 (13:40:22.0) [UTC]
File attributes:                        0x00000010      (FILE_ATTRIBUTE_DIRECTORY)
8.3 filename:                           盬弳'Y
Date created:                           07/26/2023 (05:31:24.0) [UTC]
Last accessed:                          09/09/2023 (05:10:24.0) [UTC]
Long filename:                          ???

File size:                              51209593 bytes
Last modified:                          07/29/2023 (08:14:34.0) [UTC]
File attributes:                        0x00000020      (FILE_ATTRIBUTE_ARCHIVE)
Long filename:                          [???]????_v0.6.pptx
Date created:                           07/28/2023 (09:12:02.0) [UTC]
Last accessed:                          09/09/2023 (05:22:44.0) [UTC]
Long filename:                          [???]????_v0.6.pptx

[Link Info]
Location flags:                         0x00000001      (VolumeIDAndLocalBasePath)
Drive type:                             3               (DRIVE_FIXED)
Drive serial number:                    12a0-18b7
Volume label (ASCII):                   新增磁碟區
Local path (ASCII):                     D:\Training Material\[1]課程簡報\台科大\[台科大]資訊安全_v0.6.pptx

[Metadata Property Store]
Property set GUID:                      446d16b1-8dad-4870-a748-402ea43d788c
ID:                                     104
Value:                                  0x0048 (VT_CLSID)       CLSID: ae790946-95c1-4d5f-b2cb-6d69c7e0fb6a

[Distributed Link Tracker Properties]
Version:                                0
NetBIOS name:                           desktop-3f9joqf
Droid volume identifier:                b60a791e-9325-4178-8dd5-522b787ff4f2
Droid file identifier:                  5099b7db-2d05-11ee-9549-e8f408da009c
Birth droid volume identifier:          b60a791e-9325-4178-8dd5-522b787ff4f2
Birth droid file identifier:            5099b7db-2d05-11ee-9549-e8f408da009c
MAC address:                            e8:f4:08:da:00:9c
UUID timestamp:                         07/28/2023 (05:12:14.540) [UTC]
UUID sequence number:                   5449

Unknown data at end of file.


Press any key to continue . . .
```
:::

### ==利用手動的方式parse lnk file==
SO代表offset，LE代表取多少個bytes
1. 標的檔案路徑
    ![](https://hackmd.io/_uploads/SJi5e37Ma.png)
    如果有特別幫Parition取名字的話，lnk就會把partition的名字放在兩個固定byte中間，也就是`10 00 00 00`和`00`中間，可以用以下的script把big5轉成中文
    ```python
    >>> partition_name = 'B7 73 BC 57 BA CF BA D0 B0 CF'.split(' ')
    >>> "".join([bytes.fromhex("".join(partition_name[i:i+2])).decode('big5') for i in range(0, len(partition_name), 2)])
    '新增磁碟區'
    ```
2. 標的檔案路徑之磁碟序號 (Drive serial number)
    ![](https://hackmd.io/_uploads/Hyrkc2Qza.png)
    順序是倒著看，以此為例就是`D4 21 3D DD`，如果把硬碟換掉/重灌/對partition有其他異動都會使這個serial number和原本不一樣
    :::info
    如何知悉本電腦的磁區序號:
    ```bash
    $ dir /a
     磁碟區 D 中的磁碟是 新增磁碟區
     磁碟區序號:  ECC7-4C55
     ...
    $ vol
     磁碟區 D 中的磁碟是 新增磁碟區
     磁碟區序號:  ECC7-4C55
    $ vol c:
     磁碟區 C 中的磁碟沒有標籤。
     磁碟區序號:  1AA2-C9B1
    ```
    :::
3. 標的檔案時間戳記(在Header欄位中，如下圖)
    SO = 28 / LE = 24(Timestamp開時前的四個bytes都是固定`20 00 00 00`)
    ![](https://hackmd.io/_uploads/ry58EhXza.png)
    因為我的HxD也沒有出現特別編輯器的視窗，所以就土法煉鋼的把東西轉換
    ```bash
    >>> create_time = '64 B4 1C 07 EF 09 D8 01'
    >>> create_time = int("".join(create_time.split(' ')[::-1]), 16)
    132867111228585060
    >>> access_time = '74 5A 85 0C F0 09 D8 01'
    >>> access_time = int("".join(access_time.split(' ')[::-1]), 16)
    132867115614296692
    >>> modify_time = '74 5A 85 0C F0 09 D8 01'
    >>> modify_time = int("".join(modify_time.split(' ')[::-1]), 16)
    132867115614296692
    >>> import datetime
    >>> def ad_timestamp(timestamp):
    ...     if timestamp != 0:
    ...         return datetime.datetime(1601, 1, 1) + datetime.timedelta(seconds=timestamp/10000000)
    ...     return np.nan
    ...
    >>> ad_timestamp(create_time)
    datetime.datetime(2022, 1, 15, 9, 5, 22, 858505)
    >>> ad_timestamp(access_time)
    datetime.datetime(2022, 1, 15, 9, 12, 41, 429668)
    >>> ad_timestamp(modify_time)
    datetime.datetime(2022, 1, 15, 9, 12, 41, 429668)
    ```
    的確和lnk parser上的時間一模一樣，或是也可以像講師上課的時候提到的線上工具[endian convert](https://blockchain-academy.hs-mittweida.de/litte-big-endian-converter/), [ldap timestamp convert](https://www.epochconverter.com/ldap)
4. 標的檔案大小
    SO = 52 / LE = 8
    順序也是倒著看
    ![](https://hackmd.io/_uploads/BywhO2XMa.png)
    ```bash
    >>> file_size = '70 8A 30 02 00 00 00 00'
    >>> int("".join(file_size.split(' ')[::-1]), 16)
    36735600
    ```
5. 標的檔案 ObjectID
    ![](https://hackmd.io/_uploads/SJXfIa7fp.png)
    有一點複雜，但從上往下看
    1. 紅色框起來的是不會變動的16 bytes
    2. 滑鼠反白起來的15 bytes代表NetBIOS name
    3. 後面跟著一格null byte代表隔斷符號
    4. 淺綠色+淺藍色 = New Volume ID
    5. 淺米色+淺黃色 = New Object ID
    6. 深綠色+深藍色 = Birth Volume ID
    7. 深紅色+深黃色 = Birth Object ID
    Birth和New的差別就是，如果哪一天把該檔案拉到其他地方，則new會和birth的部分不一樣，更準確的說，是把檔案從一個NTFS的檔案系統中換到另外一個NTFS的檔案系統時，才會更新此object/volume ID，如果是換到FAT32的話，會沒有變動
6. 標的檔案所在主機之 MAC Address
    就如上圖所列的最後一個欄位，也就是土黃色的區塊(其實如果new object ID沒變的話，最後6個bytes也會是MAC address)
7. UUID 時間戳記
    這個時間戳記是取自深黃色的前8個bytes，先像前面一樣轉換成big endian然後轉成int，再扣掉`5748192000000000`，詳細可以看[泛科學的文章](https://pansci.asia/archives/137717)
    ```bash
    >>> timestamp = 'DF 94 76 93 E1 75 EC 01'
    >>> timestamp = int("".join(timestamp.split(' ')[::-1]), 16)
    >>> timestamp -= 5748192000000000
    >>> ad_timestamp(timestamp)
    datetime.datetime(2022, 1, 15, 9, 0, 24, 375626)
    ```
8. UUID Sequence 編號
    這個講師沒有時間講，所以我自己用現有的檔案自己推敲應該是先取MAC address之前的兩個bytes，然後把第一個byte減掉0x80，再把全部的byte轉乘int就是了
    ```bash
    >>> uuid_num = '90 A7'.split(' ')
    >>> int(hex(int(uuid_num[0], 16)-0x80)[2:]+uuid_num[1], 16)
    4263
    ```

## 延伸閱讀
[Analyzing malicious LNK file](https://lifeinhex.com/analyzing-malicious-lnk-file/)
[EMF - Enhanced MetaFile format](https://web.archive.org/web/20190723103847/http://www.undocprint.org/formats/winspool/emf)