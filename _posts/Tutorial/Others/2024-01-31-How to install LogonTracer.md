---
title: "How to install LogonTracer"
tags: [Tutorial]

category: "Tutorial｜Others"
date: 2024-01-31
---

# How to install LogonTracer
<!-- more -->

## Installation
### 環境
WSL2 - Ubuntu 20.04
Docker

### Reference
[二刀流Windows日誌分析　精準掌握資安蛛絲馬跡](https://www.netadmin.com.tw/netadmin/zh-tw/technology/84E5EAA4BC494BB6A4B15607E62418A0)

### Docker Version
1. 安裝Docker(上網找)
2. Pull Image & Run
    ```bash
    $ docker pull jpcertcc/docker-logontracer
    $ docker run --detach --publish=7474:7474  --publish=7687:7687 --publish=8080:8080 -e LTHOSTNAME=0.0.0.0 jpcertcc/docker-logontracer
    ```
3. 先進入neo4j(`localhost:7474`)
    預設密碼: `neo4j/neo4j`
    :::info
    若有遇到登入不進去的問題，error message$\to$`Neo.ClientError.Security.Unauthorized: The client is unauthorized due to authentication failure.`
    可參考[訪問neo4j驗證失敗](https://blog.csdn.net/weixin_39198406/article/details/85068102)，我是直接把neo4j.conf的驗證註解拿掉
    ```bash
    $ docker exec -it {neo4j container name} bash
    root@5aac14bfd6fd:/var/lib/neo4j# find / -name neo4j.conf
    /var/lib/neo4j/conf/neo4j.conf
    root@5aac14bfd6fd:/var/lib/neo4j# cd conf/
    root@5aac14bfd6fd:/var/lib/neo4j/conf# apt install vim -y
    root@5aac14bfd6fd:/var/lib/neo4j/conf# vim neo4j.conf
    # 只要把dbms.security.auth_enabled=false的註解拿掉就可以了
    root@5aac14bfd6fd:/var/lib/neo4j/conf# exit
    exit
    $ docker restart nifty_stonebraker
    nifty_stonebraker
    ```
    之後再重新進入`localhost:7474`，用預設帳密登入就可以了
    :::
4. 進入LogonTracer(`localhost:8080`)
    預設帳密也是`neo4j/neo4j`

### Python Version (Recommended)
如果上面的版本不行用的話，就直接用他們發在[github的版本](https://github.com/JPCERTCC/LogonTracer/wiki/how-to-use)會比較穩定，詳細的步驟都已經寫在他們wiki了，不過有幾個問題還是需要先克服
1. 首先github version沒辦法用在windows上，只能運行在unix
2. 建議用conda創一個新環境
3. 如果用他們的requirement.txt安裝dependencies可能會有問題，會有一些版本上或是語法上的衝突，例如`Werkzeug`如果安裝最新版`3.0.1`，他沒有辦法`import url_encode, url_decode`，這是`2.3.7`以下才有的function name，而因為flask會用到但還沒有跟進，所以解決方式就是把`Werkzeug`的版本降到`2.3.7`
4. 但這樣會有conflic的問題，對於flask最新版來說，一定要`Werkzeug>=3.0.0`，所以我們還需要把flask降版本才行變成`flask==2.3.3`
5. 另外，python的版本也不能太高，目前最高是12，但hmmlearn還沒有支援到python12，所以也要特別注意，11是沒問題的
6. 最後安裝都沒問題後pandas的部分因為是安裝最新版，所以語法上會有差，若是在`2.0`以上，就不能用`append`，要改成`_append`，這個就要慢慢看logontrace的log慢慢去改

* 實作
    如下
    ```bash
    $ conda create --name test python=3.11 -y
    $ conda activate test
    $ pip install -r requirements.txt
    $ cat requirements.txt
    numpy
    py2neo>=2020.0.0
    evtx
    lxml
    scipy
    changefinder
    flask==2.3.3
    hmmlearn>=0.2.8
    scikit-learn
    elasticsearch-dsl>=7.0.0,<8.0.0
    pyyaml
    flask-sqlalchemy
    flask-login
    flask_wtf
    wtforms
    GitPython
    sigmatools
    Werkzeug==2.3.7
    $ pip install -r requirements.txt
    $ python logontracer.py -r -o 8000 -u neo4j -p neo4j -s localhost
    [+] Script start. 2023/10/25 23:28:44
    [+] Neo4j Kernel 4.4.14 (Community)
    [+] Can't create database. This feature is in Neo4j Enterprise.
        * Serving Flask app 'logontracer'
        * Debug mode: off
    ```

    我的requirements.txt和原本的有一點不一樣，然後只要按照這個步驟就可以正常啟動logontracer，前提是neo4j也有好好啟動(這部分可以用docker自行安裝)
    
:::info
在使用上有一點要特別注意，因為source code中的#1954的地方會判斷目前的紀錄是不是來自localhost，如果是就不儲存username/domain/hostname，我是不知道為甚麼要這樣設計，但反正如果給的evtx不夠大或是不夠複雜，他就沒辦法parse，或者應該說他認為沒必要parse，因為只是內部的log紀錄?我不確定
:::