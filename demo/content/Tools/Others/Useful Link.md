---
title: Useful Link
tags: [Tools]

---

# Useful Link
[TOC]
## Knowledge


|Knowledge                                                        | Comment|
|:-:|:- |
|[CRLF VS LF](http://violin-tao.blogspot.com/2016/04/crlflf-bug.html)||
|[magic method](https://www.analyticsvidhya.com/blog/2021/07/explore-the-magic-methods-in-python/)||
|[HttpOnly](https://devco.re/blog/2014/06/11/setcookie-httponly-security-issues-of-http-headers-2/)||
|[Encrypt VS Hash](https://ithelp.ithome.com.tw/articles/10193762)||
|[LFI VS RFI](https://ithelp.ithome.com.tw/articles/10240486)| LFI(Local File Inclusion)</br>產生的原因是程式設計師未對用戶參數未進行輸入檢查，導致駭客可以讀取server上的敏感文件。開發人員可能貪圖方便，將GET或POST參數直接設定為檔案名稱，直接include該檔案進網頁裡，結果就造成了引入其他檔案，造成資訊洩漏</br></br>RFI(Remote File Include)</br>基本上與LFI概念一樣，只是include的file來源變成從外部引入，觸發條件必須要把php設定參數allow_url_include 訂為ON" |
|[FTP](https://experience.dropbox.com/zh-tw/resources/what-is-ftp)||
|[WebDAV](https://experience.dropbox.com/zh-tw/resources/what-is-ftp)||
| [BitTorrent](https://johnpam11.pixnet.net/blog/post/120987008-%E4%BB%80%E9%BA%BC%E6%98%AFbt%E7%A8%AE%E5%AD%90%EF%BC%9F) ||
|[TrueNAS Setup](https://moptt.tw/p/Storage_Zone.M.1618079877.A.829)||
|[API VS Method VS Library](http://thecodingtime.blogspot.com/2014/02/apimethodlibrary.html)||
|[WebSocket](https://www.letswrite.tw/websocket/)||
|[JVM](https://www.jyt0532.com/2020/02/14/jvm-introduction/)| Briefly Introduction|
|[Thread VS Process](https://pjchender.dev/computer-science/cs-process-thread/)||
|[APT](https://blog.trendmicro.com.tw/?p=123)||
|[Arrow VS Dot VS Colon in C++](https://gist.github.com/LeeKLTW/e5004f2d7046d43676d0891af8a13ef7)||
|[payload VS formData](https://kknews.cc/zh-tw/code/ogmnm55.html)||
|[RAID 0, 1, 0+1, 1+0, 5, 6](https://raidnas.tw/hsinchu-nas-raid-explain-rescue/)||
|[How to use multiprocess in python & map VS pool VS apply_async](https://www.wongwonggoods.com/all-posts/python/python_parellel/python-multiprocessing-pool)||
|[Python asyncio 從不會到上路](https://myapollo.com.tw/blog/begin-to-asyncio/)||
|[JDK、JRE 和 JVM](https://ithelp.ithome.com.tw/articles/10264453)||
|||

## Tool-Page
|Tool| Comment|
|:-:|:- |
|[XSS-CheatSheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)||
| [All-Injection:](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%19Injection/README.md) ||
|[SQLMAP1](https://ithelp.ithome.com.tw/articles/10249487)</br>[SQLMAP2](https://ithelp.ithome.com.tw/articles/10202811)      ||
|[ViruTotal](https://www.virustotal.com/gui/)| 幫忙分析檔案是否有病毒的網站|
|[JS 混淆器](https://obfuscator.io/)| 把JS的程式變成可讀性很差的東西 |
|[JS 反混淆器](https://beautifier.io/)| 可以反混淆或解密JS的檔案       |
|[JS 壓縮+加密+混淆+美化](https://js.wfuapp.com/)||
|[Everything About Net Scanning](https://www.yougetsignal.com/)||
|[How to fetch SHA1 or MD5 in Win.](https://www.howtohaven.com/system/how-to-hash-file-on-windows.shtml#void)||
|[How to split windows in WSL?](https://www.netadmin.com.tw/netadmin/zh-tw/technology/EDC6D4560B184F0D9E7A750862D3C9E4)||
|[Docker基本命令](https://yingclin.github.io/2018/docker-basic.html)||
|||
|||

## Vocabulary


| Vocabulary    | Def.| Comment|
| - | - | - |
| Parse| 解析||
| query| 詢問、請求||
| dump| Also called a crash dump or memory dump, a dump is raw data from a computer's memory. It is written to the file system if software crashes" (terminates unexpectedly). This information is a snapshot of what was going on in the computer at the moment the error occurred. The dump can be analyzed by developers to help track down the error, understand it better, and fix it. | [Refer](https://www.computerhope.com/jargon/d/dump.htm)|
| intruder| 入侵者||
| vulnerability | 漏洞、脆弱||
| exploit| An exploit is a code that takes advantage of a software vulnerability or security flaw. It is written either by security researchers as a proof-of-concept threat or by malicious actors for use in their operations. When used, exploits allow an intruder to remotely access a network and gain elevated privileges, or move deeper into the network.| [Refer](https://www.trendmicro.com/vinfo/us/security/definition/exploit)|
| wrapper| 偽協議||
| Cipher| 密碼||
| nerf| cause to be weak or ineffective削弱、減弱| [Refer](https://english.cool/op-nerf-buff/)|
| Miscellaneous | 混雜的、各種各樣的||
| PoC| Proof of Concept：在 Binary Exploitation 通常指可以使程式發⽣ Crash 觸發異常的程式碼，⽤來證明程式存在漏洞||
| PWN| 1.具漏洞的服務</br>2.目標在是服務中找到該服務的漏洞並注入自己的程式碼，拿到 server 的控制權| [Refer1](https://csc.nccst.nat.gov.tw/shield.aspx/)</br>[Refer2](https://ithelp.ithome.com.tw/articles/10295763) |
|DHCP|主要功能是自動分配IP(192.168.xxx.xxx)，有時效限制(可能是一天)，當新設備加入區網時，會由DHCP自動分配一個IP給該設備，過了一天後如果設備再次訪問DHCP，則會在給予新的IP，否則該IP會直接回收||
|[秒懂Confusion Matrix](https://ycc.idv.tw/confusion-matrix.html)|![](https://ycc.idv.tw/media/mechine_learning_measure/mechine_learning_measure.002.jpeg)||
||||

## IThelp


| Information-Security| Web-Security| Python|
| - | - | - |
| [惡意程式(malware)](https://ithelp.ithome.com.tw/articles/10282551)                                                       | [Day 4 很像走迷宮的sqlmap](https://ithelp.ithome.com.tw/articles/10202811)                     | [[Series - 8] Python時間轉換介紹](https://ithelp.ithome.com.tw/articles/10235251)            |
| [不安全的連線？HTTPS與SSL憑證](https://ithelp.ithome.com.tw/articles/10240752)                                            | [[Day20]-新手的Web系列SQLmap](https://ithelp.ithome.com.tw/articles/10249489)                  | [[第06天] 資料結構（3）Data Frame](https://ithelp.ithome.com.tw/articles/10185182)           |
| [Day 018.聽起來好像很厲害的-密碼學](https://ithelp.ithome.com.tw/articles/10248442)                                       | [Day 12 - PHP 偽協議 (一) ](https://ithelp.ithome.com.tw/articles/10245020)                    | [dlib安裝心得 -- Windows 環境](https://ithelp.ithome.com.tw/articles/10231535)               |
| [Day21-針對Metasploitable 3進行滲透測試(2)-Shell & Reverse Shell基礎知識](https://ithelp.ithome.com.tw/articles/10278494) | [[Day13]-SSTI(Server-side template injection)](https://ithelp.ithome.com.tw/articles/10244403) | [【Day 9】Python打包程式](https://ithelp.ithome.com.tw/articles/10261688)|
| [[2018iThome鐵人賽]Day6:加密和雜湊有什麼不一樣？](https://ithelp.ithome.com.tw/articles/10193762)| [[Day11]SSTI(Server Side Template Injection)](https://ithelp.ithome.com.tw/articles/10272749)  | [[Day28] 儲存訓練好的模型](https://ithelp.ithome.com.tw/articles/10280076)|
| [[2018iThome鐵人賽]Day 4:如何區分加密、壓縮、編碼](https://ithelp.ithome.com.tw/articles/10193241)                        | [[Day7]-PHP(LFI/RFI)](https://ithelp.ithome.com.tw/articles/10240486)| [[Python]關鍵字yield和return究竟有什麼不同?](https://ithelp.ithome.com.tw/articles/10258195) |
| [Day 21.加密演算法要注意的那些毛(一)-加密模式](https://ithelp.ithome.com.tw/articles/10249953)| [[Day23]forensics的開始](https://ithelp.ithome.com.tw/articles/10208651)||
| [『Day 27』拜託別Pwn我啦！-常見的工具（下）](https://ithelp.ithome.com.tw/articles/10227380)|||
||||

|Deep-Learning | Big-Data |Linux|
|------------- | -------- |-----|
|[[演算法]K-means分群(K-means Clustering)](https://ithelp.ithome.com.tw/articles/10209058)|[[改善資料品質]Part-1 EDA ](https://ithelp.ithome.com.tw/articles/10200912)|[從沒圖進化到有圖有字的工具：cowsay](https://ithelp.ithome.com.tw/articles/10127590)|
|[[第24天] 機器學習（4）分群演算法](https://ithelp.ithome.com.tw/articles/10187314)|[Day18-shell是什麼？](https://ithelp.ithome.com.tw/articles/10207473)||
|[[AI#10]人臉辨識](https://ithelp.ithome.com.tw/articles/10227098)|[C語言工具使用，GDB個人學習筆記](https://ithelp.ithome.com.tw/articles/10257294)||
|[淺談機器學習的效能衡量指標(2)--ROC/AUC曲線](https://ithelp.ithome.com.tw/articles/10229049)|||
|[[Day15]機器學習常勝軍-XGBoost ](https://ithelp.ithome.com.tw/articles/10273094)|||
|[[Day20]Lasso和Ridge正規化回歸](https://ithelp.ithome.com.tw/articles/10227654)|||
||||

| Web-Develop| JS   | Webpage-Automation |
| - | ---- | - |
| [17. [FE] 為什麼現在的前端都在用「框架」？](https://ithelp.ithome.com.tw/articles/10224417) | [你不可不知的 JavaScript 二三事#Day3：資料型態的夢魘——動態型別加弱型別(2)](https://ithelp.ithome.com.tw/articles/10202260) |[鼠年全馬鐵人挑戰 WEEK 06：Selenium 自動化測試工具 ](https://ithelp.ithome.com.tw/articles/10229959)|
|[D29-如何打包Apps Script的程式碼？（二）包成HTML網頁與或API](https://ithelp.ithome.com.tw/articles/10274829)|[10. [JS] 一般函式與箭頭函式的差異？ ](https://ithelp.ithome.com.tw/articles/10221214)|[鼠年全馬鐵人挑戰 WEEK 09：Selenium WebDriver (下)](https://ithelp.ithome.com.tw/articles/10230717)|
|[Day03-深入理解網頁架構：DOM](https://ithelp.ithome.com.tw/articles/10202689)|      |[【Day 27】-再爬一次Dcard?(實戰向 Dcard API 發出請求)](https://ithelp.ithome.com.tw/articles/10281036)|
|[PHP物件導向的第四課：繼承](https://ithelp.ithome.com.tw/articles/10114805)|      |[[Day23]Beautiful Soup網頁解析！](https://ithelp.ithome.com.tw/articles/10196817)|
|[PHP物件導向的第二課：重談「方法」，物件「屬性」及「成員」](https://ithelp.ithome.com.tw/articles/10114707)|      |[[Day 17] Instagram - 模擬登入](https://ithelp.ithome.com.tw/articles/10247175)|
|[PHP物件導向的第一課：class](https://ithelp.ithome.com.tw/articles/10114633)|      |                    |
|[Day 20 Authentication基礎概念介紹：session、cookie and token](https://ithelp.ithome.com.tw/articles/10224935)|      |                    |
|[Day 17 - 會員登入系統](https://ithelp.ithome.com.tw/articles/10207241)|      |                    |
|[XAMPP安裝與操作初步](https://ithelp.ithome.com.tw/articles/10197921)|      |                    |
|[What is metadata?](https://ithelp.ithome.com.tw/articles/10237545)|      |                    |
||||
||||


| Reverse-Engineering| Others| PWN|
| - | - | --- |
| [[Day10]格式透視-解析PE文件格式（前篇）](https://ithelp.ithome.com.tw/articles/10187490)| [第二天：要了解DLL你要先講啊](https://ithelp.ithome.com.tw/articles/10237039)    |[『 Day 26』拜託別 Pwn 我啦！ - 常見的工具 （上） ](https://ithelp.ithome.com.tw/articles/10227326)|
| [[Day17] 行為分析－成為逆向大師的第一步－秒懂加殼技術](https://ithelp.ithome.com.tw/articles/10188209) | [第四天：Dll聽話 讓我看看](https://ithelp.ithome.com.tw/articles/10238425)|[『Day 27』拜託別Pwn我啦！-常見的工具（下）](https://ithelp.ithome.com.tw/articles/10227380)|
||[Day16-分散式系統溝通的方法-RPC](https://ithelp.ithome.com.tw/articles/10223580) |[Day25: [Misc] 我從來沒想過我會害怕寫 code](https://ithelp.ithome.com.tw/articles/10226977)|
||[C語言雜談01---如何理解條件編譯](https://ithelp.ithome.com.tw/articles/10283174) ||
||[C#編譯到執行與Java的相似之處](https://ithelp.ithome.com.tw/articles/10217608)||
||||
||||


## Conference & Journal For Information Security
* [IEEE TIFS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206)
* [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858)
* [ACM TISSEC](https://dl.acm.org/journal/tops)
* [ACSAC](https://www.acsac.org/)
* [Usenix security](https://www.usenix.org/conference/usenixsecurity22)
