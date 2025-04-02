---
title: Network Related
tags: [名詞解釋]

---

# What is HTTP/SSH Tunnel, TLS/SSL, WebSocket?
在讀When TLS Meets Proxy on Mobile[^paper]這篇paper的時候一直提到這些觀念，有時候會差點搞混中間的意思

## SSL Tunnel
根據[SSH Tunneling (Port Forwarding) 詳解 ](https://johnliu55.tw/ssh-tunnel.html)的說明:
> Tunneling 指的是將網路上的 A、B 兩個端點用某種方式連接起來，形成一個「隧道」，讓兩端的通訊能夠穿透某些限制（例如防火牆），或是能將通訊內容加密避免洩漏。而 SSH Tunneling 就是指利用 SSH 協定來建立這個隧道
> ![](https://johnliu55.tw/ssh-tunnel/images/tunneling.png =400x)

有分成以下三種，以下接取自[^link1]的說明，但不特別解釋，原文也有補充很多實際如何使用的Command和教學
* Local Port Forwarding
    * 使用情境一：連到位在防火牆後的開發伺服器上的服務
        ![](https://johnliu55.tw/ssh-tunnel/images/local_scenario1_problem.png =400x)
        ![](https://johnliu55.tw/ssh-tunnel/images/local_scenario1_solved.png =400x)
    * 使用情境二：透過防火牆後的機器，連到防火牆後的特定服務
        ![](https://johnliu55.tw/ssh-tunnel/images/local_scenario2_problem.png =400x)
        ![](https://johnliu55.tw/ssh-tunnel/images/local_scenario2_solved.png =400x)
* Remote Port Forwarding
    * 使用情境一：透過對外機器，讓其他人能夠連到你的電腦上的服務
        ![](https://johnliu55.tw/ssh-tunnel/images/remote_scenario1_problem.png =400x)
        ![](https://johnliu55.tw/ssh-tunnel/images/remote_scenario1_solved.png =400x)
    * 使用情境二：透過對外機器，從外面連回內部網路上的服務
        ![](https://johnliu55.tw/ssh-tunnel/images/remote_scenario2_problem.png =400x)
        ![](https://johnliu55.tw/ssh-tunnel/images/remote_scenario2_solved.png =400x)
* Dynamic Port Forwarding
    * 使用情境：建立一個 HTTP 代理伺服器連到內網的所有 HTTP(S) 服務
        ![](https://johnliu55.tw/ssh-tunnel/images/dynamic.png =400x)
## HTTP Tunnel
根據[http tunnel 原理及穿透防火牆方法](http://www.wiseuc.com/facontent.php?id=903)中提到的說明，其實和上述的SSH Tunnel的原理和功能差不多，只是建立tunnel的Port變成HTTP的80為主
> 舉例如下:
> A 主機系統在防火牆之後，受防火牆保護。防火牆配置的訪問控制原則是只允許80端口的數據進出，屏蔽了其他的所有端口。B主機系統在防火牆之外，是開放的。現在假設需要從A 系統Telnet到B系統上去，怎麽辦？
> 使用正常的Telnet肯定是不可能了，但我們知道可用的只有80端口，那麽這個時候使用http Tunnel，就是一個好的辦法。思路如下:  在A 機器上運行一個Tunnel 的Client端，讓它偵聽本機的一個不被使用的任意指定端口(Port>1024 and port < 65535)，如1234. 同時將來自1234端口上的數據導向到遠端(B機)的80端口上(注意，是80端口，防火牆允許通過)，然後在B機上運行一個tunnel Server，同樣在80端口上監聽，然後把80 端口上接收到的數據(數據由tunnel client傳來)轉到本機的Telnet 服務端口23，這樣就ok了。
> 
> 根據剛才的設置, 數據流程大概是:
> 
> [telnet.exe:任意端口]→[tunnel client.exe:1234]→[Firewall]→[tunnel server.exe:80]→[telnet Server.exe:23]

## TLS/SSL
### 簡答
> 參考資料：https://www.digicert.com/tw/what-is-ssl-tls-and-https

* SSL是一種用於保護網際網路連線的標準技術，保護方法是對在網站和瀏覽器（或兩個伺服器之間）之間寄送的資料進行加密。它能防止駭客查看或竊取傳輸的任何訊息，包括個人或財務資料。
* TLS是SSL的經過更新的、更安全的版本。我們仍將自己的安全性憑證稱為SSL，因為它是一個更通用的術語，但是當您從DigiCert購買憑證時，您將獲得最受信任的、最新的TLS憑證。
* 當網站受到SSL/TLS憑證的保護時，HTTPS會出現在URL中。使用者可以透過按一下瀏覽器網址列中的掛鎖標示來檢視憑證的詳細訊息，包括頒發機構和網站擁有者的公司名稱。
### 詳答
[什麼是 SSL/TLS 憑證？](https://aws.amazon.com/tw/what-is/ssl-certificate/)
> SSL/TLS 憑證是一種數位物件，允許系統驗證身分並隨後使用 Secure Sockets Layer/Transport Layer Security (SSL/TLS) 協定，與另一個系統建立加密網路連線。憑證是在稱為公開金鑰基礎設施 (PKI) 的加密系統內使用。如果雙方都信任第三方 (稱為憑證授權單位)，PKI 會使用憑證讓其中一方建立另一方的身分。因此，SSL/TLS 憑證可作為數位身份證，用於保護網路通訊安全，以及為網際網路上的網站和私有網路上的資源建立身分。
## WebSocket
根據[WebSocket 基本介紹及使用筆記](https://www.letswrite.tw/websocket/)的說明如下:
> ![](https://imgur.com/WurUgR9.png)

如果只在意這是什麼的話，那只要注意上半部就可以了，他和傳統的HTTP協定差異如下，HTTP協定必須要一來一回互相傳遞資料，但WebSocket只需要Handshake一次就可以開始互相主動傳遞資料，是HTML5提供的一種新的網路傳輸協定:
![](https://i.imgur.com/S3Mhxau.png =400x)
> 參考資料：https://hackmd.io/@Heidi-Liu/javascript-websocket
## Socket
這是根據[^socket1][^socket2]所得到的結論，我自己的理解是socket本身就是一種"網路中"Process之間互相通訊的"介面"，而websocket則是實踐這個介面的"協定"，或者說實踐出來的一種方法
> ![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgLns0xTxSh_5JSboS3fbyfAwQVTCzd3YIbL5nDCfYQH4wWPW7ZbaOh7gsJ5wquyuX_Gcxj82ixLC0voY2MbYmOv0Lx_C6K-29lJB-VFZNG6x0Q0GBVbdiezOLPPFhsfXhUfNAyZt429eI/s320/222.png =200x)
> * Socket簡單來說，就是以前的TCP/IP，實現繁瑣且困難，後來有人封裝成一個簡易的介面來讓開發人員使用。現在也變成通訊的標準之一。
> * Websocket，從字面上很容易就能理解。它是為了提升web通訊速度而被創造出來的一種「協議」，在七層模型中是屬於「應用層」它的原理是瀏覽器底層使用「socket」當作通訊介面，通訊協議才是採用它自身的「websocket協議」。可以想成，溝通的協議跟水管都裝在瀏覽器上。只要瀏覽器有支援，就可以使用這個協議透過web來跟伺服器做溝通。在前幾年可能會有很多瀏覽器不支援。但在現今，瀏覽器的版本都已經趨近成熟，大部分都支援websocket的協議。

在[^socket1]有說明如何寫socket，以及更詳細的說明何為socket，有需要可以直接看內文的範例
> ![](http://i.imgur.com/cqr4O2P.png =300x)

# What is Subject Alternative Name(SAN), Server Name Indication(SNI)
## SAN
資料來源: [使用 openssl 制作一個包含 SAN（Subject Alternative Name）的證書](https://www.z01.com/help/https/3173.shtml)
> SAN(Subject Alternative Name) 是 SSL 標準 x509 中定義的一個擴展。使用了 SAN 字段的 SSL 證書，可以擴展此證書支持的域名，使得一個證書可以支持多個不同域名的解析。先來看一看 Google 是怎樣使用 SAN 證書的，下面是 Youtube 網站的證書信息：
> ![6363260315098898213519066](https://hackmd.io/_uploads/rkY-awtBR.png =400x)
> 這里可以看到這張證書的 Common Name 字段是 \*.google.com，那麽為什麽這張證書卻能夠被 www.youtube.com 這個域名所使用呢。原因就是這是一張帶有 SAN 擴展的證書，下面是這張證書的 SAN 擴展信息：
> ![6363260315666115456453456](https://hackmd.io/_uploads/H1DfTwYHA.png =300x)
> ![6363260316281773611299520](https://hackmd.io/_uploads/SJmm6vKBA.png =300x)
> 這里可以看到，這張證書的 Subject Alternative Name 段中列了一大串的域名，因此這張證書能夠被多個域名所使用。對於 Google 這種域名數量較多的公司來說，使用這種類型的證書能夠極大的簡化網站證書的管理。

## SNI
資料來源: [Server Name Indication (SNI) 原理簡介](https://lichi-chen.medium.com/server-name-indication-sni-%E5%8E%9F%E7%90%86%E7%B0%A1%E4%BB%8B-f85e075e1d75)
> 如果你有接觸過 web server ，例如 apache 或是 nginx 或是 IIS，有個名詞叫做 virtual host 。意思是你可以在一台 web server 上面裝多個網站，可以讓 `a.com` 跟 `b.com` 對應到不同的處理邏輯。HTTP headers 裡面有個欄位叫做Host，會帶有 client 想要訪問的網站域名。 Server 可以根據這個訊息來判斷 client 到底想訪問 `a.com` 還是 `b.com` 。
> ### HTTPS 造成的問題
> HTTPS 把這件事變得有點麻煩。在 TCP 連線建立完成後，接著進行的是 TLS handshake ，這時候 Server 會需要回應一張證書給 client 。如果今天一個網站有一張以上的證書，事情就變得很麻煩，我到底要給哪一張。這時候沒辦法看 Host header ，原因是 TLS 會發生在 HTTP headers 訊息傳送之前。除非你可以預知未來，不然無法偷看到 Host header 。因此 SNI 要解決的問題，就是 server 不知道要給哪一張 certificate 的問題。SNI extensionSNI 是在 TLS handshake 的 client hello 規格部分加一個額外的欄位，裡面放的是 client 想訪問的域名。如此一來 server 就知道要回應哪一張證書了。
> ![](https://miro.medium.com/v2/resize:fit:4800/format:webp/1*IuBvaDxx276KOQi6QER_9w.png)

## Access Control List(ACL)
資料來源: [善用存取控制清單 Cisco網路設備變身防火牆](https://www.netadmin.com.tw/netadmin/zh-tw/technology/8AA504183CD84FEC8B32701550A9CB52)
>  眾所周知，防火牆可以透過設定來控制所通過的網路封包，以便於決定何種網路協定或何種埠的封包能夠通過，甚至可設定哪些來源端或目的地端套用這樣的設定。防火牆就是由許多這樣的規則所組成，以增加網路的安全性，而Cisco網路設備也可以提供這樣的功能，本文將示範如何設定Cisco路由器來當作網路防火牆。
> 為了讓Cisco路由器擁有如防火牆般的功能，最重要的技術就是透過Access Control List來完成。Access Control List簡稱ACL，可稱為存取控制清單。
> 簡單來說，存取控制清單包含一些規則，每一條規則可用來定義要允許或拒絕特定形式的網路封包，而這裡的特定形式，則包含網路協定的定義、來源端或目的地端的指定，或是埠的指定之類。接下來，說明Cisco路由器的存取控制清單的概念。 
## Reference
[^paper]:Debnath, J., Chau, S. Y., & Chowdhury, O. (2020). When tls meets proxy on mobile. In Applied Cryptography and Network Security: 18th International Conference, ACNS 2020, Rome, Italy, October 19–22, 2020, Proceedings, Part II 18 (pp. 387-407). Springer International Publishing.
[^link1]:[SSH Tunneling (Port Forwarding) 詳解 ](https://johnliu55.tw/ssh-tunnel.html)
[^socket1]:[ TCP Socket Programming 學習筆記 ](http://zake7749.github.io/2015/03/17/SocketProgramming/)
[^socket2]:[【筆記】Socket，Websocket，Socket.io的差異 ](https://leesonhsu.blogspot.com/2018/07/socketwebsocketsocketio.html)