---
title: NTU Operating System Review Notes
tags: [NTU_OS, NTU]

category: "Security/Course/NTU OS"
---

# NTU Operating System Review Notes
###### tags: `NTU_OS` `Operating System`
[TOC]

## Ch 6 Synchronization
### Process communication
![](https://imgur.com/zQM1oNq.png)
#### Race condition
就是Project1提到的共享記憶體的問題，導致multi-thread執行的結果會完全錯誤
* 解決策略
    * Disable interrupt
    process在對shared memory進行變數存取之前，先disable interrupt，直到完成此次存取後才enable，這樣的話這段時間，CPU就不會被其他processes搶走(preempted)
    * Critical section design
    必須滿足三個criteria
        * Mutual exclusion: 在任何時間點，最多只允許一個process在他自己的CS內活動，不可同時有多個process在各自的CS內活動
        * Progress: 如果有人想進去CS，遲早進的去
        * Bounded waiting: 在一定時間內一定進的去
    * 架構圖
    ![](https://imgur.com/q1iDFSC.png)
    * spinlock
    * busy waiting
#### Critical section design的方法
* Software solution
    * 兩個processes
        * Peterson's solution: 有turn和flag兩個變數，分別代表目前的token在誰手上(turn)，以及表示有無意願進入CS(flag)
    * N個processes
        * Bakery's ALG: 就是領號碼牌，號碼最小的人優先，若同時有多人持有相同的號碼牌，則以PID最小的優先
* Hardware 指令支援
* OS提出了mutex lock的概念，並用acquire()和release()的方法實踐
* Semaphore
    * 一種可以解決CS design和processes synchronization problem的data type，會提供兩個atomic operations: wait(s)和signal(s)
    * wait(s): `while(s<=0) {do nothing;}s--;`
    * signal(s): `s++`
    * 簡單來說，s就是看現在可以使用的資源有多少(例如有多少台printer)，如果資源被分出去一個，s就減一，如果都沒有資源了，就一直等待，直到有人釋放資源，釋放資源的時候，s就會加一，所以和前面提到的mutex lock幾乎一樣，wait(s)就是acquire()，而signal(s)就是release()
    * Semaphore的種類
        * 有使用busy-waiting: spinlock semaphore:其實就是上面說的mutex lock和正常semaphore的概念
        * 沒有使用busy-waiting: Non-Busy-Waiting semaphore: 看講義
* Monitor
用來解決synchronization problem的高階資料結構
其實就是物件導向的方式，利用private、initialization等方式，創造monitor這個class object
 
#### Message Passing技術
![](https://imgur.com/W7uTjET.png)
* Direct communication
    * Symmetric: 其實就是TCP的方式
    * Asymmetric: 就是UDP的方式
* Indirect communication
Sender和receiver是透過shared mailbox建立溝通管道

## Ch 7 Deadlock
### 形成deadlock的必要條件
* Mutual exclusion
    在任何時間點，此類型的資源最多只允許一個process使用，不可多個processes同時持有使用
* Hold & wait
持有部分資源，且又在等待其他Process身上的資源
* No preemption
process不能任意剝奪其他process正在持有的資源，給自己用，要等到對方用完並release後才可以用
* Circular waiting

### 處理方式
* Deadlock Prevention
讓必要的四個條件其中一個不成立即可
    * 破除mutual exclusion: 辦不到，因為此性質是大多數資源與生俱來的性質，所以無法破除
    * 破除Hold & wait: 
        * 法一: 除非此process能夠一次得到所需的所有資源，否則不能持有資源
        * 法二: 允許process先持有部分資源，但是一旦process要提出其他資源的申請之前，必須要釋放出所持有的全部資源才可提出申請
    * 破除No preemption: 改為preemptive就可以了
* Deadlock Avoidance(Banker's ALG)
就是看提出申請之後，用banker's alg.看有沒有一組逃生通道(safe state)，若有則核准申請
* Deadlock Detection & Recovery
    * Recovery
        * Kill process in the deadlock
            * All process: 成本太高
            * 先kill一個，再用detection檢查有沒有deadlock，若還有就再repeat，cost很高
        * Resources preemptive: 選擇一些lower priority的victim process，強行把資源搶過來，再紀錄這些victim是哪些，cost很高
* ignore deadlock
## Ch 8 Memory Management Strategies
### Contiguous Memory Management
連續性配置: process必須占用一個連續的記憶體空間，OS用link-list的方式管理free memory block
#### 配置方法
![](https://imgur.com/RSE8mst.png)
* First-Fit
尋找第一個能容納process的hole
* Best-Fit
尋找size夠小但仍能塞入process的hole，問題是這樣還是有可能會有hole，而這些hole，其他process大機率也是不能用(因為太小了)
* Worst-Fit
找最大的那個hole

### External & Internal Fragmentation
#### External Fragmentation
* 在連續性的配置策略下，全部的hole size加總**大於**要放入的process，但是卻沒有一個hole能夠容納此process就是外部碎裂
![](https://imgur.com/yAzl5ty.png)
* How to solve? 
    * compaction的技術(搬移)
    * Page Memory management(採取非連續性的配置策略)
    * 提供多套的base / limit registers for the code section and data section of a process，降低外碎的機率

#### Internal Fragmentation
* 配置給process的空間超過process需求大小，兩者之間的差值就是內部碎裂，這個概念比較直觀，就像前面說的，這樣的hole，對於其他process來說，大機率也是不能用的，形成浪費
### Page memory Management
![](https://imgur.com/9qCCfyJ.png)
* 優點：沒有external fragmentation，可支援virtual memory的實施
* 缺點：有internal fragmentation
* <font color="FF0000">利用register或memory或TLB來存取page table</font>
![](https://imgur.com/EsOE41W.png)
* Effective memory access time公式(P is TLB hit ratio)
$P*(TLB time+memory access time) + (1-P)*(TLBtime+2*memory access time)$
* Page Table Too large solution
    * Hierarchical paging
    ![](https://imgur.com/IUk4mig.png)
    * Hashing page table
    ![](https://imgur.com/luC3A3o.png)
    * Inverted page table
    以physical memory為記錄對象，若physical memory有n個frames，則Inverted page table就有n個entry，每個entry紀錄此frame是存放哪個process的哪個page
    ![](https://imgur.com/VYnsfwi.png)
### Segment Memory Management
其實就是以原始的logical memory中的每一個segmentation為一單位，當然每一個section的大小都不一樣(例如：code segment/data segment/stack segment等)，並分配到練續性的physical memory(單一一個segment，segment之間不一定要連續)
Kernel會替每個process建立一個segment table，並記錄每個segment的base和limit
![](https://imgur.com/7PmNPTl.png)
![](https://imgur.com/pRkWwOa.png)

![](https://imgur.com/rLgPK6W.png)
## Ch 9 Virtual-Memory Management
主要目的：允許process size在大於free physical memory space的情況下，仍能讓process執行，主要的概念是，我只把一些要用到的部分(目前需要的資源，比方說程式片段或是data)從disk存取到physical memory中，這樣就可以了，如果現在要用的page不在physical memory中，就再從disk中讀取近來
### Demand Paging
是建立在page memory management的基礎上，為了達到上述的要求，需要在page table中新增一個bit，用來表達此page有沒有在physical memory中
![](https://imgur.com/FRTWkX2.png)
### Page fault處理
![](https://imgur.com/yPid5OG.png)
### Effective memory access time計算
![](https://imgur.com/LYe7SjL.png)
### Page Replacement
當page fault發生，且physical memory已經沒有多餘的free frame時，就要做page replacement，也就是找一個苦主，寫回去disk，並把要存取的部分放到memory中
* FIFO: 最早仔入的page就要成為victim page
* OPT(optimal): 會依據未來長期不會用到的page當作victim page
* LRU: 最近不常使用的page就是victim page
    * Counter(假的LRU)
    * Stack(真的LRU)
* LRU近似作法
此作法會在page table中再增加一個新的bit，表示從上一次page fault到此次page fault中間有無被用過
    * Second chance: 簡單來說，就是從某一個page往下開始找，如果此page的reference bit是1，則變成零，如果原本就是零則當作victim page
* LFU & MFU
Lease frequently used & Most frequently used
選擇使用次數最少/多的page當作victim page
* Page buffering
系統保留一個free frame(私房錢)
### Thrashing及解決方法
1. CPU utilization急速下降
2. I/O-device 異常忙碌
3. Process花在page fault的處理時間遠大於正常執行時間
以上三點滿足就是thrashing
當process分配到的frame數量不足時，則process會經常page fault，需要做page replacement
* How to solve?
    * Decrease multi-programming
    * 利用page fault frequency控制機制，來限制thrashing
    ![](https://imgur.com/zKC7oCb.png)
    * 利用working set model技術，來預估各個process在不同執行時期所需要的frame數量
    ![](https://imgur.com/WXEYCcb.png)


## **超重要的總結**
![](https://imgur.com/3UQ1OZU.png)