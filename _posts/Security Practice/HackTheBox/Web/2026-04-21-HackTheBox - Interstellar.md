---
layout: post
title: "HackTheBox - Interstellar"
date: 2026-04-21
category: "Security Practice｜HackTheBox｜Web"
tags: [HackTheBox, CTF, Web, SSRF, Docker]
draft: false
toc: true
comments: true
---

# HackTheBox - Interstellar
這一題的漏洞利用如下
1. 透過前期的recon FFuF知道`communicate.php`
2. 查看source code或者看前端的操作了解可能有SSRF
3. 透過SSRF找到內網特定的操作而該操作還有另外一個SQLi漏洞
4. 利用SQLi就可以上傳webshell拿到RCE
<!-- more -->

## 前情提要
在build docker中需要改一些東西
```dockerfile
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i '/security.debian.org/s/^/#/' /etc/apt/sources.list && \
    sed -i '/stretch-updates/s/^/#/' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y mariadb-server mariadb-client git && \
    docker-php-ext-install mysqli && \
    apt-get clean

# Dockerfile #12 改成以下cmd

RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i '/stretch-updates/s/^/#/' /etc/apt/sources.list && \
    apt-get -o Acquire::Check-Valid-Until=false update && \
    apt-get install -y --allow-unauthenticated mariadb-server mariadb-client git && \
    docker-php-ext-install mysqli && \
    apt-get clean
```

## Recon
1. `Dockerfile`
    1. 開80 for website
    2. 執行entrypoint.sh
    3. 有init.sql
    4. 使用smarty這個PHP template engine → 可能有SSTI
    5. 使用PHP 7.0，很舊，可能有RCE漏洞
    6. flag放在root並且rename by random
2. `init.sql`
    1. 在`SET @sql = CONCAT('SELECT * FROM users WHERE name = \'', name, '\'');`可能有SQLi漏洞，使用字串拼接
    2. 開了4個不同的procedure(`searchUser`/`registerUser`/`loginUser`/`editName`)
3. `entrypoint.sh`
    1. 啟動mysql
    2. 把root改成用密碼登入
    3. 建立interstellar這個db
    4. root 沒有密碼，任何拿到 container 的人 = DB 全控
    5. Web app 用 root 操作 DB
    6. 權限過大: `GRANT ALL PRIVILEGES ON interstellar.* TO 'root'@'127.0.0.1';`
4. `communicate.php`: 給URL/Key/Value，他會送出去request，並且把reponse回傳 → SSRF的洞
5. `index.php`: 有一個edit action，是只允許localhost request

## 沒有SQLi
在`login.php`中看到代表他有做parameterized query，所以用這個角度打沒用
```php
...
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    $query = "CALL loginUser(?, ?)";
...
```

## SSRF