---
layout: post
title: "Security Related"
date: 2026-02-25
category: "Terminology"
tags: []
draft: false
toc: true
comments: true
---

# Security Related
<!-- more -->

## 名詞解釋

| Vocabulary    | Def.| Comment|
| - | - | - |
| parse| 解析||
| query| 詢問、請求||
| dump| Also called a crash dump or memory dump, a dump is raw data from a computer's memory. It is written to the file system if software crashes" (terminates unexpectedly). This information is a snapshot of what was going on in the computer at the moment the error occurred. The dump can be analyzed by developers to help track down the error, understand it better, and fix it. | [Refer](https://www.computerhope.com/jargon/d/dump.htm)|
| intruder| 入侵者||
| vulnerability | 漏洞、脆弱||
| exploit| An exploit is a code that takes advantage of a software vulnerability or security flaw. It is written either by security researchers as a proof-of-concept threat or by malicious actors for use in their operations. When used, exploits allow an intruder to remotely access a network and gain elevated privileges, or move deeper into the network.| [Refer](https://www.trendmicro.com/vinfo/us/security/definition/exploit)|
| wrapper| 偽協議||
| cipher| 密碼||
| nerf| cause to be weak or ineffective削弱、減弱| [Refer](https://english.cool/op-nerf-buff/)|
| miscellaneous | 混雜的、各種各樣的||
| PoC| Proof of Concept：在 Binary Exploitation 通常指可以使程式發⽣ Crash 觸發異常的程式碼，⽤來證明程式存在漏洞||
| PWN| 1.具漏洞的服務<br>2.目標在是服務中找到該服務的漏洞並注入自己的程式碼，拿到 server 的控制權| [Refer1](https://csc.nccst.nat.gov.tw/shield.aspx/)<br>[Refer2](https://ithelp.ithome.com.tw/articles/10295763) |
|DHCP|主要功能是自動分配IP(192.168.xxx.xxx)，有時效限制(可能是一天)，當新設備加入區網時，會由DHCP自動分配一個IP給該設備，過了一天後如果設備再次訪問DHCP，則會在給予新的IP，否則該IP會直接回收||
|[Encrypt VS Hash](https://ithelp.ithome.com.tw/articles/10193762)|||
|[CRLF VS LF](http://violin-tao.blogspot.com/2016/04/crlflf-bug.html)|||
|[magic method](https://www.analyticsvidhya.com/blog/2021/07/explore-the-magic-methods-in-python/)|||

## 資安 基本教學
* [惡意程式(malware)](https://ithelp.ithome.com.tw/articles/10282551)
* [不安全的連線？HTTPS與SSL憑證](https://ithelp.ithome.com.tw/articles/10240752)
* [Day 018.聽起來好像很厲害的-密碼學](https://ithelp.ithome.com.tw/articles/10248442)
* [Day21-針對Metasploitable 3進行滲透測試(2)-Shell & Reverse Shell基礎知識](https://ithelp.ithome.com.tw/articles/10278494)
* [[2018iThome鐵人賽]Day6:加密和雜湊有什麼不一樣？](https://ithelp.ithome.com.tw/articles/10193762)
* [[2018iThome鐵人賽]Day 4:如何區分加密、壓縮、編碼](https://ithelp.ithome.com.tw/articles/10193241)
* [Day 21.加密演算法要注意的那些毛(一)-加密模式](https://ithelp.ithome.com.tw/articles/10249953)
* [『Day 27』拜託別Pwn我啦！-常見的工具（下）](https://ithelp.ithome.com.tw/articles/10227380)
* [payload VS formData](https://kknews.cc/zh-tw/code/ogmnm55.html)
* [APT](https://blog.trendmicro.com.tw/?p=123)

## Web 教學
### SQL
* [Day 4 很像走迷宮的sqlmap](https://ithelp.ithome.com.tw/articles/10202811)
* [[Day20]-新手的Web系列SQLmap](https://ithelp.ithome.com.tw/articles/10249489)
### SSTI
* [[Day11]SSTI(Server Side Template Injection)](https://ithelp.ithome.com.tw/articles/10272749)
* [[Day13]-SSTI(Server-side template injection)](https://ithelp.ithome.com.tw/articles/10244403)
### PHP
* [Day 12 - PHP 偽協議 (一) ](https://ithelp.ithome.com.tw/articles/10245020)
* [[Day7]-PHP(LFI/RFI)](https://ithelp.ithome.com.tw/articles/10240486)
### 其他
* [LFI VS RFI](https://ithelp.ithome.com.tw/articles/10240486): LFI(Local File Inclusion)<br>產生的原因是程式設計師未對用戶參數未進行輸入檢查，導致駭客可以讀取server上的敏感文件。開發人員可能貪圖方便，將GET或POST參數直接設定為檔案名稱，直接include該檔案進網頁裡，結果就造成了引入其他檔案，造成資訊洩漏<br><br>RFI(Remote File Include)<br>基本上與LFI概念一樣，只是include的file來源變成從外部引入，觸發條件必須要把php設定參數allow_url_include 訂為ON"
* [[Day23]forensics的開始](https://ithelp.ithome.com.tw/articles/10208651)

## Reverse-Engineering
* [[Day10]格式透視-解析PE文件格式（前篇）](https://ithelp.ithome.com.tw/articles/10187490)
* [[Day17] 行為分析－成為逆向大師的第一步－秒懂加殼技術](https://ithelp.ithome.com.tw/articles/10188209)

## PWN
* [『 Day 26』拜託別 Pwn 我啦！ - 常見的工具 （上） ](https://ithelp.ithome.com.tw/articles/10227326)
* [『Day 27』拜託別Pwn我啦！-常見的工具（下）](https://ithelp.ithome.com.tw/articles/10227380)
* [Day25: [Misc] 我從來沒想過我會害怕寫 code](https://ithelp.ithome.com.tw/articles/10226977)