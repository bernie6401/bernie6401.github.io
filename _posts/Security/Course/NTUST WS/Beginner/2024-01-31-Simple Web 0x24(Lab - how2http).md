---
title: Simple Web 0x24(Lab - how2http)
tags: [NTUSTWS, CTF, Web]

category: "Security｜Course｜NTUST WS｜Beginner"
date: 2024-01-31
---

# Simple Web 0x24(Lab - how2http)
<!-- more -->

## Source code
```php
<?php
show_source(__FILE__);

include("flag.php");

if (!empty($_SERVER["HTTP_CLIENT_IP"])){
    $ip = $_SERVER["HTTP_CLIENT_IP"];
} elseif (!empty($_SERVER["HTTP_X_FORWARDED_FOR"])){
    $ip = $_SERVER["HTTP_X_FORWARDED_FOR"];
} else {
    $ip = $_SERVER["REMOTE_ADDR"];
}
if ($_COOKIE['user'] !== 'admin') die("Not admim");

if( $_SERVER["REQUEST_METHOD"] !== "FLAG" ) die("u don't need flag?");


if ($ip === "127.0.0.1") echo $FLAG;
else echo "NOPE!";
?>
```

## Recon
主要是參考之前寫過的[PicoCTF - Who are you?](https://hackmd.io/@SBK6401/B135SD0w2)和[PicoCTF - Who are you?](https://hackmd.io/@SBK6401/Syct_Ol0i#Challenge-picobrowser%F0%9F%8D%B0)，按照source code我們需要更改一些header讓他可以被forge然後bypass這些條件，首先是IP，他其實給的很寬鬆，還有X-Forwarded-For的header可以用，就直接==X-Forwarded-For: 127.0.0.1==；另外，cookie的user要等於admin→==Cookie: user=admin==；再來，request method要等於FLAG→==FLAG / HTTP/1.1==

## Exploit
![圖片](https://hackmd.io/_uploads/H14qGKvrp.png)

Flag: `FLAG{b4by_httttp!}`

## Reference
[X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For)