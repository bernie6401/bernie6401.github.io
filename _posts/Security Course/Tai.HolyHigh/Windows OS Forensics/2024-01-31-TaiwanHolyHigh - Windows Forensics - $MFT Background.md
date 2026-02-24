---
title: TaiwanHolyHigh - Windows Forensics - $MFT Background
tags: [TaiwanHolyHigh, Forensics, Windows]

category: "Security Course｜Tai.HolyHigh｜Windows OS Forensics"
date: 2024-01-31
---

# TaiwanHolyHigh - Windows Forensics - \$MFT Background
<!-- more -->
:::spoiler TOC
[TOC]
:::
:::info
以下引用若無特別說明皆來自於講師的上課簡報
:::

## Background
* `$`在windows代表系統檔案
* `$MFT`(Master File Table):
* [`FAT`(File Allocation Table)](https://tw.easeus.com/partition-manager-tips/fat-file-system-format.html):
    > Fat 檔案系統，簡稱 File Allocation Table，是微軟和 Caldera 開發組為 Windows 電腦開發的檔案系統
    > 雖然它主要是電腦磁區類型，但在過去幾年中它已作為主要檔案系統格式用於各種手機裝置中。此外，由於它是一個 8 位檔案系統，因此簇數會隨著磁碟容量的增加而增加。
    > FAT12 - 12 位
    > FAT16 - 16 位
    > FAT32 - 32 位
    > 我們還應該澄清，FAT 檔案系統從 1977 年開始使用，但 FAT32 是在 1996 年引入的
* `BIOS`(Basic Input Output System)
* [`POST`(Power On Self Test)](https://bbs.pigoo.com/thread-16131-1-1.html)
    > POST自檢測過程大致為：加電－CPU－ROM－BIOS－System Clock－DMA－64KB RAM－IRQ－顯卡等。檢測顯卡以前的過程稱過關鍵部件測試，如果關鍵部件有問題，計算機會處於掛起狀態，習慣上稱為核心故障。另一類故障稱為非關鍵性故障，檢測完顯卡後，計算機將對64KB以上內存、I／O口、軟硬盤驅動器、鍵盤、即插即用設備、CMOS設置等進行檢測，並在屏幕上顯示各種信息和出錯報告。在正常情況下，POST過程進行得非常快，我們幾乎無法感覺到這個過程。
    > POST自檢測代碼含義是什麼？
    > 當系統檢測到相應的錯誤時，會以兩種方式進行報告，即在屏幕上顯示出錯信息或以報警聲響次數的方式來指出檢測到的故障。
* [`MBR`(Master Boot Record)](https://tw.easeus.com/diskmanager/master-boot-record.html)
    > MBR 代表主開機記錄。它是一小段代碼，負責在您的電腦上加載作業系統。 MBR 還包含有關硬碟上的分割區及佈局的資訊。如果您曾經安裝過作業系統，您可能會看到詢問您是否要以 MBR 或 GPT 模式安裝它的提示。這是指硬碟上使用的分割區類型。
    > ### 主開機記錄在哪裡？
    > 主開機記錄代碼儲存在硬碟的第一個扇區（扇區 0）中。需要注意的是，這個扇區不是任何分割區的一部分，如果你刪除一個分區，MBR 代碼仍然存在。
    > ![](https://tw.easeus.com/images/en/screenshot/partition-manager/mbr-location.png)
    > ### 主開機記錄如何工作
    > 當電腦啟動後，MBR 開始啟動儲存在唯獨儲存器中的 BIOS 程式。這意味著當您打開電腦時，MBR 代碼首先執行並從硬碟加載作業系統。
    > 主開機記錄工作流程：
    > 1. 系統啟動自檢——BIOS檢查系統硬體和CMOS設定。
    > 2. 讀取主開機記錄——檢測可開機設備，BIOS將MBR扇區讀入內存。
    > 3. 檢查 MBR 的結束標誌是否為 0000:7C00H 等於 55AAH。當啟動設備滿足要求時，BIOS 將控制權移交給 MBR 啟動作業系統。
* 電腦開機訊續:
    1. Power
    2. POST
    3. BIOS
    4. MBR
    5. VBR
    6. $MFT
    7. ...

## \$MFT Background
* What is \$MFT?
    > 常見之 NTFS 系統檔案如下，多以`$`符號為開頭。
    > ![](https://hackmd.io/_uploads/B1u7eQtGa.png)
    > 其中`$MFT`檔案中記錄所有系統中存放之檔案相關屬性值，為 NTFS 分析之重點項目。
    > ![](https://hackmd.io/_uploads/r1ArgXFGT.png)

* \$MFT儲存的內容
    1. Timestamp
        * Standard File: SO=80, LE=32(Creat+Modified+\$MFT Modified+Access)
        * Filename: SO=184, LE=32(Creat+Modified+\$MFT Modified+Access)
    2. Status: SO=22, LE=2
        * `0000`: Delete File
        * `0100`: File
        * `0200`: Delete Folder
        * `0300`: Folder
    3. \$MFT Record(File Identify/Location): SO=44, LE=4
    4. Resident / non-Resident File
