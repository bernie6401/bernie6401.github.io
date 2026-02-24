---
title: A&D of Network Security Note
tags: [NTU, NTU_PADNS]

category: "Security Course｜NTU PADNS"
date: 2023-03-19
---

# A&D of Network Security Note
<!-- more -->
###### tags: `Practicum of A&D of NS` `NTU`

## Background
:::spoiler [IP / 遮罩 / 閘道 三者的關係](http://www.ess.nthu.edu.tw/p/16-1351-74716.php?Lang=zh-tw)
> 用日常生活中的例子來比喻，IP 就好比在社區中的門牌地址，如果是要找同社區(一樣遮罩範圍的)，就只要透過社區廣播喊一聲。如果找不到人，表示在社區外，就要出社區大門(閘道)去外面問
>
> 所以遮罩設定錯誤，代表硬把兩個不同社區的給劃在一起，但是實際上遞送封包就會找不到 (明明住光復國宅結果你跟郵差說光復國宅跟孟竹國宅都在一區)
>
> 閘道設定錯誤則是連大門都搞錯了，這樣蓮社區都出不去，自然網路也無法連線
:::

:::spoiler [[網路] 淺談 ARP (Address Resolution Protocol) 運作原理](https://blog.downager.com/2013/07/03/%E7%B6%B2%E8%B7%AF-%E6%B7%BA%E8%AB%87-ARP-Address-Resolution-Protocol-%E9%81%8B%E4%BD%9C%E5%8E%9F%E7%90%86/)
> 在乙太網路上，資料的傳遞必須要有實體位址 (MAC Address)，Layer 2 設備會驗證 Frame 的實體位址，不是找它的一律捨棄，但設備一開機總不可能就有所有設備的實體位址吧？所以就需要 ARP 協定來協助取得各個設備的實體位址
> 
> ARP 是利用乙太網路的廣播功能所設計出來的位址解析協定，它的主要特性是它的位址對應關係是動態的，以查詢的方式來獲得 I P位址 (IP Address) 和實體位址 (MAC Address / Physical Address) 的對應關係。
> 
> 只要是 Layer 3 的設備都一定會有 ARP Cache，並且會在 ARP 快取內建立 ARP 表格 (ARP Table) 用來記錄 IP 位址和實體位址的對應關係。這個 Table 會依據自身的存活時間遞減而消失，以確保資料的正確性。
> ![](https://i.imgur.com/Vg2RZHd.png)

簡單說明我的理解：
Assume在同一內網中有三台主機：PC0, PC1, PC2
Objective：PC0要ping PC1
Obstacle：但目前PC0的ARP cache中沒有PC1的MAC Address，所以不知道要寄給誰(沒有門牌號碼)
Solution：利用broadcast的方式向其他主機發送ARP Request的廣播封包，查詢目標主機的實體位址
Process：
1. 不是PC1的其他主機收到ARP Request的package就會直接丟掉，而PC1會將PC0的IP位址及MAC位址對應寫到ARP表格裡以及回傳一個ARP Reply封包給PC0
2. ARP Reply封包內包含Source MAC/IP及Target MAC/IP
3. PC0收到ARP Reply後，將目標MAC Address填入ICMP(Ping)封包的L2表頭之後就開始執行Ping PC1的動作
:::

:::spoiler [搞懂ICMP協定及工具 抵擋「死亡之Ping」攻擊](https://www.netadmin.com.tw/netadmin/zh-tw/technology/111381F2995A4AB48672E965F63133AE?page=1)
> ICMP是Internet Control Message Protocol的縮寫，這個網路協定運用在網路七層協定中的第三層。該協定的最主要目的，是用來解析網路封包或是分析路由的情況，大多是透過所傳回來的錯誤訊息進行分析，而網路管理人員則利用這個協定的工具來了解狀況，進而使用其他措施解決所遇到的問題
> 
> ICMP會使用TTL的概念，TTL的全名是Time To Live，其值代表還有多少「生存時間」，其實就是還可以被轉發處理多少次
> 每個路由器在轉發ICMP封包時，都會把IP Header的TTL的值減1，如果TTL的值已經到0，就代表TTL已經到期，接著就會傳送錯誤訊息給原本發送的網路設備
:::
:::spoiler [Broadcast Storm](https://ithelp.ithome.com.tw/articles/10247179)
![](https://ithelp.ithome.com.tw/upload/images/20200930/20129897wSHPL35T6g.png)
> 首先，當 PC A 發出了一個 L2 的廣播封包（像是之前介紹的 ARP 請求封包，就是廣播形式的）
PC A 將會發送至 Switch 2（他也只有連上 Switch 2，也沒辦法傳給其他人）
Switch 2 看到了這個封包，想說是廣播封包
所以複製了一份，傳給 Switch 1 與 Switch 3，這時候整個網路拓樸中就已經有兩份這個封包了，讓我們根據複製出來的封包做編號並分別講解
>
> 這時候 Switch 1 收到了一個廣播包，因為只有連接 Switch 1 與 Switch 3，而這個封包是從 Switch 2 收到了，所以只會被轉傳給 Switch 3
> Switch 3 也收到了一個廣播包，所以他決定複製一份，往其他實體網路接口傳送，也就是往 Switch 1 與 PC A
>
> 發現了嗎，這時候複製出來的這兩個封包就會留存在網路拓樸中
且因為 Layer 2 沒有 TTL（Time to Live）機制，沒辦法轉送超過一定數量設備後被丟棄
所以網路內的封包就會越來越多，且電腦也會一直收到複製出來的廣播封包
這時候就會造成 Switch 與終端設備要花資源來處理這些垃圾封包
而最終將會造成資源耗盡
:::
:::spoiler [Spanning Tree Protocol(STP)生成樹協定](https://www.jannet.hk/spanning-tree-protocol-stp-zh-hant/)
實作方式：`PVST+`
1. 選舉Root Switch
2. 選舉Root Port
3. 選擇Designated Port與Nondesignated Port
:::
---
:::spoiler [What is Storage Area Network(SAN)](https://ithelp.ithome.com.tw/articles/10008373)
> SAN技術廣泛的運用在企業裡，用以提供高速的、可管理的、具容錯能力的、富彈性的儲存服務。譬如作為資料儲存、備份、系統備援等。SAN不是單一設備或是某種協定，它是一種服務架構，結合多種硬體(如：光纖、HBA卡、高速交換機、伺服器、磁碟陣列等)與軟體(管理軟體、initator與target軟體、驅動程式等)的技術。採用SAN的架構，可以將各個單一的儲存設備連結起來，提供整合性的管理與應用。SAN最大的用途不僅在於做為資料的儲存，而是在於其容錯與災難備援的能力。
> 優點有：
>
> * 儲存設備的分享，具有經濟效益。透過網路架構，所有的用戶端不必直接連接到特定的儲存設備上就可以使用期資源。
> * 有效的管理。透過管理軟體，可以更有效的管理儲存的資料與制定備援計劃。
> * 容錯能力，降低風險。SAN提供多種容錯功能，從最簡單的mirror到進階的snapshot，在在可以減低資料遺失或是企業服務中斷的風險。

我自己的解讀就是不同架構且比較高級的NAS，因為:
> Target與Initator之間，透過高速的網路連結，這通常是光纖。而提供連接的介面我們稱之為HBA(Host Bus Adapter)，建構網路的方式則是光纖交換機。這些林林種種的設備，講求的是高速與穩定，但是相對的代表的就是高貴

---

NAS VS SAN
NAS使用基於文件的協議例如NFS或SMB/CIFS且是存取的電腦上的文件而不是硬碟。
而SAN是Client/Server架構，其中提供儲存能力的一端稱之為Target，而要求資源的一端稱為Initator，透過網路架構，所有的用戶端不必直接連接到特定的儲存設備上就可以使用期資源
:::
:::spoiler [What is TUN & TAP](https://zh.wikipedia.org/wiki/TUN%E4%B8%8ETAP)
> 在電腦網路中，TUN與TAP是作業系統核心中的虛擬網路裝置。不同於普通靠硬體網路配接器實現的裝置，這些虛擬的網路裝置全部用軟體實現，並向執行於作業系統上的軟體提供與硬體的網路裝置完全相同的功能。
> 
> TAP等同於一個乙太網路裝置，它操作第二層封包如乙太網路資料框。TUN類比了網路層裝置，操作第三層封包比如IP資料封包。 
:::

---
:::spoiler [ICMP協定功能](http://www.tsnien.idv.tw/Manager_WebBook/chap4/4-5%20ICMP%20%E5%8D%94%E5%AE%9A%E8%88%87%E5%88%86%E6%9E%90.html)
> 根據我們的瞭解 IP 網路是一種不可靠的傳輸方式，傳送中的封包必須經過多層路由器的轉送才能到達目的地，因此，在發送封包之前，我們很難預測該封包是否可以安全到達目的地。我們也很迫切地想知道目前網路的狀況，尤其在傳送失敗時，更想瞭解問題出在什麼地方。TCP/IP 網路中提供一種稱之為『網際控制訊息協定』（Internet Control Message Protocol, ICMP）的通訊軟體，用來偵測網路的狀況。在 IP 網路上，任何一部主機或路由器皆設置有 ICMP 協定，它們之間就可以利用 ICMP 來互相交換網路目前的狀況訊息，例如，主機不存在、網路斷線等等狀況。ICMP 訊息的產生有下列兩種情況：
>
> 1. 障礙通知：當 IP 封包傳送當中，在某一網路上發生問題而無法繼續傳送，則會回應 ICMP 訊息給原封包傳送端。如圖 4-14 所示，訊號_1是由 Router_A 回應；或是由 Router_B 回應訊號_2；也有可能是由主機 B 回應訊號_3。
> ![](https://i.imgur.com/Vh4RSWm.png)
> 
> 2. 狀況查詢：可以發送 ICMP 來查詢目前網路的情況。如圖 4-15 中，主機 A 發送 ICMP 查詢訊息，有可能由路由器回應（訊號_1 和 訊號_2），或由主機 B 回應訊號_3。
> ![](https://i.imgur.com/eNISOYF.png)
:::

[02-ICMPv6 - 网络工程师俱乐部的视频 - 知乎](https://www.zhihu.com/zvideo/1298003353810137088)