---
title: NTUSTISC - AD Note - 會後提及有用的工具
tags: [NTUSTISC, AD, information security]

category: "Security/Course/NTUST ISC/AD"
---

# NTUSTISC - AD Note - 會後提及有用的工具
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=JAnGtFoJlij-03nk&t=6024)

## Background

### [EDR(Endpoint Detection and Response)](https://www.trendmicro.com/zh_tw/what-is/xdr/edr.html)
> 端點偵測及回應 (EDR) 結合了即時的持續監控、端點資料蒐集，以及進階交叉關聯，來偵測並回應主機和端點連線的可疑活動。這套方法可讓資安團隊快速發掘並交叉分析各種活動來產生高可信度的偵測事件，並提供手動和自動化回應選項。
> 
> EDR 解決方案會記錄端點上發生的所有活動和事件。某些廠商或許還會將這項服務延伸至任何與您網路相連的工作負載。然後，這些記錄 (或事件記錄檔) 可用來發掘原本不會被發現的資安事件。即時的監控可以更快偵測威脅，不讓威脅有機會擴散至使用者端點之外。

其實就是把我們感興趣的log抓出來而已

### [XDR(Extended detection and response)](https://www.trendmicro.com/zh_tw/what-is/xdr.html)
> XDR (延伸式偵測及回應) 可蒐集並自動交叉關聯涵蓋多個防護層的資料，包括：電子郵件、端點、伺服器、雲端工作負載以及網路。如此可藉由資安分析來提供更快的威脅偵測，提升調查與回應時間。
> 
> XDR 能打破資安產品之間的藩籬，採用一種全方位面面俱到的偵測及回應方法。XDR 可蒐集並透過交叉關聯涵蓋多個防護層的偵測事件與深入的活動資料，包括：電子郵件、端點、伺服器、雲端工作負載以及網路。如此豐富的資料若能透過自動化分析，就能更快偵測威脅，同時也讓資安分析師擁有適當的工具可完成更多任務，並透過調查來採取更迅速的行動。
![](https://www.trendmicro.com/content/dam/trendmicro/global/en/what-is/xdr/XDR-new-market-iture.png)

簡單來說EDR只能特定範圍或是單一產品上做到端點偵測，但XDR是能夠跨各個資安產品或是layer達到更全面的偵測以及比對事件的結果

### [MDR(Managed Detection and Response)](https://ithelp.ithome.com.tw/articles/10307982)
> 提供專業的資安人員來協助企業進行監控網路、分析事件、並且回應所遭遇的資安狀況如何做出對應的應變
> * 是一種服務
> * 藉由資安專家的服務，提供及時、有效的處理，以避免損失擴大
> * 將安全專業知識外包給專業的人員
> * 分析警示當中潛藏的危險徵兆


### 如何滅證
只要讓windows保持預設值或是把event file砍掉就好了，因為windows10會記錄很多使用者的狀況，例如Quick Access的使用路徑或是使用者之前使用過的應用程式的縮圖等等，所以最暴力的方式是離開之前丟一個勒索病毒，它就會針對常見的file進行加密，這樣縱使不把東西刪掉，鑑識人員也不會知道裡面的內容是甚麼

### 如果正在使用Win2008/2012
請趕快升級成Win2016，因為有很多攻擊手段是到win2016的就失效的，例如前面提到的wdigest在2008/2012是會開的，因為這樣在認證上才會成功

### [什麼是誘捕系統（Honey Pot）？](https://www.ithome.com.tw/news/27824)
> 就像是一罐用來吸引、捕捉昆蟲的蜂蜜，所謂的誘捕系統（Honey Pot）就是一個吸引攻擊者的目標，透過誘捕的手法，吸引駭客發動攻擊，以蒐集攻擊者的來源以及攻擊手法，現在除了應用在蒐集病毒特徵、攻擊手法，也用來蒐集假網站的IP，以及散布木馬或間諜程式等惡意來源名單，藉此觀察病蠕蟲、駭客入侵或惡意攻擊的來源、手段、管道及模式，由於會將所有攻擊動作與過程記錄下來，已經成為蒐集駭客資訊的重要方式之ㄧ。 
> 
> 此外，誘捕系統還具有消耗攻擊時間、轉移攻擊目標等的功能。一個「接近真實」的誘補系統必須定期更新與維護，才能與駭客互動、吸引駭客長時間注意，除了提供詳盡的攻擊細節，研究人員必須觀察攻擊者的動機，並擬定因應對策，而系統也必須定期清除所遭受到的感染。

### [什麼是SCCM?](https://wwwstar.medium.com/mis-sccm簡介及安裝教學-1-前置安裝教學-dec6301ae6af)
> Microsoft System Center Configuration Manager
>
> 微軟系統中心配置管理器（Microsoft System Center Configuration Manager，英文縮寫SCCM，也稱為ConfigMgr），舊名系統管理服務（Systems Management Server，英文縮寫SMS），是由Microsoft開發的系統管理軟體。SCCM提供遠程控制，補丁程序管理，軟體分發，作業系統部署，網絡訪問保護以及羅列硬體和軟體詳細信息等功能。

又甚麼是系統管理?
> 系統管理可能涉及以下一項或多項任務：
    > * 硬體維護
    > * 監視伺服器
    > * 安裝軟體
    > * 反病毒和反惡意軟體
    > * 用戶活動監控
    > * 安全管理。
    > * 存儲管理
    > * 網絡容量和利用率監視

### [What is VNC(Virtual Network Computing)?](https://blog.csdn.net/Cheese_pop/article/details/102958997)
就類似TeamViewer那樣的遠端連線工具，它是使用RFB(Remote Frame Buffer)的協定，通常linux系統預設是用VNC，啟動VNC的教學可以這邊[^activate-vnc-teach][^activate-vnc-linux]，兩者的比較可以看一下這邊[^diff-vnc-&-rdp]

### [What is AAD(Azure Active Directory)?](https://learn.microsoft.com/zh-tw/azure/active-directory/fundamentals/whatis)
> Azure Active Directory (Azure AD) 是雲端式身分識別與存取管理服務。 Azure AD 可讓您的員工存取外部資源，例如 Microsoft 365、Azure 入口網站和數千個其他 SaaS 應用程式。 Azure Active Directory 也可協助他們存取內部資源，例如公司內部網路上的應用程式，以及為您自己的組織開發的任何雲端應用程式

如果想知道AD和AAD之間的差異，可以看[^diff-between-ad-&-aad]
如果官方的太雜或太深可以先看這個影片[[Azure]AD與AAD的區別是甚麼?](https://youtu.be/C-H9pbOFjVw?si=wnErFaMChkRm5Sr2)，講的非常的清楚
> AzureAD不是AD的雲端版本

原本本地端的AD就是一種樹系的分層控管結構，domain controller(Windows Server)會控管公司的每一台主機，或是分成區域、各種不同的domain(e.g. kuma.org)等等，而DC可以派發一些group policy達到控制底下的其他電腦，可能是安裝或卸載一些應用程式或是控制檔案的RWX的權限等等

試想，現在這種本地端的AD內的computer如果想要用雲端服務，會很麻煩，首先
1. 不同的雲端服務都會需要不同的帳密，對於使用者來說會麻煩，要記很多組，如果都用同一組又會有資安上的風險
2. 站在公司的立場也不好，因為如果使用者是用公司的帳號和密碼，萬一外部雲端服務的資料外洩，就會影響到公司內部的資安
3. 如果員工離職，雖然可以刪除AD上的帳號，但是外部的雲端服務的帳號就很難刪除
4. 站在雲端服務供應商的立場，也會很麻煩，因為每一次開發一個應用程式，都需要額外開發屬於自己應用程式的帳號認證或重製密碼的機制等等，會很繁瑣也很沒效率

所以基於以上需求和缺點，有了新的東西，也就是IdaaS(Identity as a Service)，簡單來說就是平常我們可以用Google或Facebook的帳號登入其他的網站或應用程式，而不用一定要重新註冊一組專屬於該網頁的帳號，這也代表該網站或應用程式它會信任google/facebook的用戶認證系統，實作上就可以不用實作這一塊，取而代之的是調用第三方身分驗證系統的機構達到同樣的效果，而AAD就是IdaaS的其中一種體現方式

|      | AD                         | AAD  |
| ---- | -------------------------- | ---- |
| 協定 | Kerberos</br>NTLM</br>LDAP | SAML</br>OAuth2</br>OIDC</br>WS-Fed |
|How to use cloud APP?|ADFS認證|IdaaS|
|特別的功能|無|Multi-Factor Authentication</br>條件訪問</br>Identity Protection|

### [ IR從零開始的自我修煉之路-Day 02 ](https://ithelp.ithome.com.tw/articles/10238765)
What is IR(incident response)?
> Incident Response 事件響應（事件管理）是企業或組織管理資安事件的處理方法。機敏資訊外洩或遭到攻擊破壞系統，且影響到客戶（遭詐騙、騷擾等）、知識產權、營業秘密、品牌價值等。IR用意是在為了減少企業損害並進快復原且避免再次發生同樣狀況。做調查就是為了從攻擊中吸取教訓並改善資安防護措施，由於當今有許多公司都會遇到類似的問題，因此制定完善且有明確的ＳＯＰ事件回報計畫是保護公司的不錯方式。

## 會後提及有用的工具

### [Ping Castle](https://www.pingcastle.com/)
這個工具可以幫AD環境做快速的稽核，然後會產生報表，讓使用者可以一目了然目前AD的狀況

### [WAZUH](https://wazuh.com/)
這個工具就是前面講到的XDR，可以幫用戶做弱掃、路徑偵測、安全分析之類的
> Wazuh provides analysts real-time correlation and context. Active responses are granular, encompassing on-device remediation so endpoints are kept clean and operational.

### [PsExec](https://learn.microsoft.com/zh-tw/sysinternals/downloads/psexec)
> psexec是windows下非常好的一款遠程命令行工具。psexec的使用不需要對方主機開機3389端口，只需要對方開啟admin共享或c(該共享默認開啟，依賴於445端口)。但是，假如目標主機開啟了防火墻(因為防火墻默認禁止445端口的連接)，psexec也是不能使用的，會提示找不到網絡路徑。由於psexec是windows提供的工具，所以殺毒軟件會將其添加到白名單中。 - by [^what-is-psexec]

詳細的提權教學可以看這邊[^psexec-teach-hackercat]

### SIEM廠商
[splunk](https://www.splunk.com/)
[ArcSight](https://www.microfocus.com/en-us/cyberres/secops/arcsight-esm) - 詳細可以看[TaiwanHolyHigh - SoC基礎維運](https://hackmd.io/@SBK6401/HJurzt98p)

## Reference
[^activate-vnc-teach]:[ VNC教學 ](https://www.youtube.com/watch?v=4Fc2hInOw3o&ab_channel=DSP202NCYU)
[^activate-vnc-linux]:[ vnc遠端桌面圖像界面 安裝與使用 ](https://youtu.be/_av-tO3dHAI?si=Cki11X8RLKOh-iHb)
[^diff-vnc-&-rdp]:[VNC與RDP區別](https://blog.csdn.net/Cheese_pop/article/details/102958997)
[^psexec-teach-hackercat]:[利用PsExec提權為system管理員教學(windows提權)](https://hackercat.org/windows/psexec-local-privilege-escalation)
[^what-is-psexec]:[psexec工具的使用](https://cloud.tencent.com/developer/article/1937700)
[^diff-between-ad-&-aad]:[比較 Active Directory 與 Azure Active Directory](https://learn.microsoft.com/zh-tw/azure/active-directory/fundamentals/compare)