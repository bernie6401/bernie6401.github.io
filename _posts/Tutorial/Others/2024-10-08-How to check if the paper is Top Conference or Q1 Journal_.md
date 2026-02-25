---
title: "How to check if the paper is Top Conference or Q1 Journal"
tags: [Tutorial]

category: "Tutorial｜Others"
date: 2024-10-08
---

# How to check if the paper is Top Conference or Q1 Journal
<!-- more -->

## Preliminary
* 先判斷該篇論文是Conference還是Journal
    > 有出現Conference, Symposium, Proceedings, ACM: SIG…, Ex. SIGSOFT, SIGGRAPH等關鍵字時，基本上是Conference
    > 有出現Journal或是Transactions基本上是Journal
    > [name=ianyang]

## Conference
* (不推薦)直接看有沒有在Google Scholar Ranking當中，如果是Engineer & Computer Science的，可以直接看 https://scholar.google.com/citations?view_op=top_venues&hl=zh-TW&vq=eng ，不過這個方法也要知道該篇論文在Subcatecory當中的哪一個類別，可能該篇論文有用到很多元素，就不太好判斷
* (推薦)直接丟 https://www.myhuiban.com/ (有收錄中國、巴西和澳洲的等第)或 https://portal.core.edu.au/conf-ranks/ (澳洲政府開的學術研討會搜尋網站)，如果這兩個網站找不到或是有找到但沒有標示等第，那可能是不入流或是比較新的研討會
* (推薦)直接問博班或是對該領域很熟的同學
    * 舉例來說IOP這個出版社我也沒聽過，但是@ian 說是一個以Open Source為主的出版社，所以他們出的一些Journal有機會是Q1，但如果是Conference可能就有點危
    * 再舉例想是Spinger出版的可能都不是頂會，以CS領域來說，Springer出版的論文很少出現在頂會，Elsevier也是一樣的狀況
* (最後的方法)丟Google或是進官網找，看會議是誰主辦
    只有很少的會議有這樣的狀況，例如[ICSE](https://conf.researchr.org/home/icse-2025)，他底下就有很多Co-Hosted的會議是切分出來的
    ![圖片](https://hackmd.io/_uploads/rJrV-uzkJx.png =500x)
    但本質上也還是ICSE主辦的，所以也算頂會，只是通常收錄的paper，他的reference citation會寫Co-Hosted的名稱而不是ICSE，這樣的話一般researcher可能會不知道這是什麼樣的conference，所以要往上一個level看他是誰主辦，但這是沒有辦法中的辦法，可能會走到這一步的情況是，有一個很多人cite的Paper也是自己的研究中主要比較對象，但透過以上方法都找不到，才會需要做到這個複雜

如果是IEEE或是ACM出版的，大部分都可能是頂會，但也要看，如果是自己論文的主要比較對象，就要再確定，但如果只是一般的引用，可以不用那麼detail或是執著一定要是頂會


## Journal
這個就簡單很多，直接用Clarivate查JCI，如果沒有就代表沒有收錄在JCR，那可能就先不要引用，或者是有Transactions的關鍵字，代表他一定曾經是頂會，https://jcr.clarivate.com/jcr/home

## Conference & Journal For Information Security
如果是資安相關的頂刊或頂會大概就是以下這幾個
* [IEEE TIFS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206)
* [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858)
* [ACM TISSEC](https://dl.acm.org/journal/tops)
* [ACSAC](https://www.acsac.org/)
* [Usenix security](https://www.usenix.org/conference/usenixsecurity22)