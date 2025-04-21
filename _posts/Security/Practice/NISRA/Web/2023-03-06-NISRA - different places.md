---
title: NISRA - different places
tags: [CTF, Web, NISRA, Book]

category: "Security/Practice/NISRA/Web"
---

# NISRA - different places
<!-- more -->
###### tags: `NISRA` `CTF` `Web`
Challenge: [different places](http://chall2.nisra.net:41025/)

## Exploit - Integrate Fragments Flags
1. View Page Sources
![](https://i.imgur.com/q3tSKo5.png)
![](https://i.imgur.com/yrKjnyr.png)

2. base64 decode
`dXNlcm5hbWU6YWRtaW5fcGFzc3dvcmQ6bmlzcmE=` $\to$ `username:admin_password:nisra`

3. Observe the form
It uses get method to fetch the parameters. So we can peek `login.php` first.
![](https://i.imgur.com/oGFwOoA.png)
Then we could use the username and password we got at previous step.
Payload: `view-source:http://chall2.nisra.net:41025/login.php?username=admin&password=nisra`
Then we got the last fragment flag.

    :::spoiler Whole flag
    `NISRA{KaN_y0u_fIND_FlA9_a7_dIff3R3n7_5Pac32}`
    :::