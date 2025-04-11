---
title: TaiwanHolyHigh - Windows Forensics - Windows檔案系統與還原
tags: [TaiwanHolyHigh, Forensics, Windows]

category: "Security/Course/Tai.HolyHigh/Windows OS Forensics"
---

# TaiwanHolyHigh - Windows Forensics - Windows檔案系統與還原
:::spoiler TOC
[TOC]
:::

## Background
* What is cluster or sector?
    > [基本磁碟結構](https://www.pcdvd.com.tw/showthread.php?t=674854)
    > 磁碟儲存最小單位為sector，每一個sector包含了512bytes的資訊內容。但用sector當單位來儲存效率會很差，一般不會以一個sector當作存取檔案的單位，而是以cluster為一基本檔案單位，每一個cluster是架構在sector的2次方倍數上。假定連續的8個sector所構成一個cluster，其大小就為512×8=4096bytes(4K)，如此在存取資料時會以8個sector連續讀取而提升了相對效率。但並不是讓單位cluster越大越好，因為cluster越大相對的可能會浪費許多磁碟空間，例如設定以4K為一個cluster而要儲存的檔案內容只有1K，但這個小檔案還是佔用掉一個cluster的空間，其他3K就浪費掉了。所在考慮cluster的規劃時，需要同時考慮到檔案讀取的效能與檔案大小是否會浪費硬碟空間。

    
* File Slack
    舉例來說如果一個檔案A，大小是4個sector(2048 bytes)，現在將其刪除後又存入一個檔案B在同一位置，但其大小只有1.5個sector(768 bytes)，則後面沒有被填滿的2.5個sector事實上還殘留檔案A的一些資訊，尚未填滿的該sector(Ram Slack)+完整的兩個sector(Disk/Residual Slack)就是file slack
    > ![](https://hackmd.io/_uploads/rk9GlEcG6.png)

    會有一點小複雜，反正file slack就是一個完整cluster(如果按照中FAT16來格式化128MB來說就是4個sectors)沒有被填滿的部分就對了，而ran slack或是disk(residual) slack只是在區分這些沒有被填滿的區塊而已

* ==比較表格==
    > ![](https://hackmd.io/_uploads/S1XGzEcfp.png)
    
    稍微解釋一下為甚麼FAT16是單一cluster的sector數量比較多，因為按照他自己的定義，最大的cluster數量不能超過65526，也就是說如果硬碟的容量變大，單一cluster所除下來的sector數量就越多，舉例:
    若一張記憶卡的大小是128MB$\to$134217728 bytes，單一cluster最少需要4個sectors
    $$
    134217728/512/65526\approx 4
    $$
    所以如果記憶卡大小是512MB$\to$，536870912 bytes，單一cluster最少需要16個sectors
    $$
    536870912/512/65526\approx 16
    $$
    當然，這樣的空間使用率是很差的，因為一個cluster就意味著一間總統套房，若所有的檔案不分大小都住進總統套房，就會造成很多浪費，或甚至是有很多file slack產生，試想如果像512MB一樣，一個cluster有16個sector，代表該總統套房可以容納$16*512=8192 bytes$，如果電腦中都是小檔案居多(1kB之類的)，那有很多空間就會浪費掉，但對於鑑識來說遺留的東西越多越能夠還原很多真相

* 以攻擊者或一般使用者來說，如何達到真正的毀屍滅跡?
    1. Encryption: 工具[veracrypt](https://sourceforge.net/projects/veracrypt/)
    2. File Wipe: 工具[file shredder](https://www.fileshredder.org/)
    3. Partition Wipe: 工具 Windows Format
        * Fast: 快速格式化
        * Non-Fast: 完整格式化
        [差別就是](https://www.pcdvd.com.tw/showthread.php?t=294869)
            > 儲存檔案的時候， 除了在儲存區寫入檔案資料以外，也會在開頭一個小區塊的"檔案表"輸入相關資訊;快速格式化是只把開頭的檔案表重寫，真正儲存檔案資訊的部份則沒有更動，但是系統讀到檔案表顯示是"空白"，就會把這張片子當成是空片，就不管儲存區有沒有資料，直接覆蓋過去；換句話說，若是檔案表有標明某區存有某資料，則儲存時就會跳過這區不覆蓋
            > 完整格式化會對格式化的區域進行讀寫測試，就是確定壞軌。快速格式化沒有
    4. Physical Destroy: 碎(記得敲碎一點才不容易在無塵室中還原) 燒 溶(不建議) 磁(消磁)

    以攻擊者的角度來說，最少要做到第四步之前，才比較沒有那麼容易的透過鑑識還原資料