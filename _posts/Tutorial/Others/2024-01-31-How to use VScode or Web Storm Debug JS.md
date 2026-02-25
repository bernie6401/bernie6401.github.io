---
title: "How to use VScode / Web Storm Debug JS"
tags: [Tutorial]

category: "Tutorial｜Others"
date: 2024-01-31
---

# How to use VScode / Web Storm Debug JS
<!-- more -->

## Background
[了解node.js nvm npm差別](https://a0910288060.medium.com/%E4%BA%86%E8%A7%A3node-js-nvm-npm%E5%B7%AE%E5%88%A5-47cda7c1d569)

## Prepare JS Modules
當拿到一個web題目，通常會包含Dockerfile / docker-compose.yml / package.json，我們要做的就是把這個專案所需要的library都載好，這些通常都會記錄在package.json中
* Windows
    在windows也需要下載js的interpreter，也就是node js / npm這些東西，詳細可以看[MSDN文件](https://learn.microsoft.com/zh-tw/windows/dev-environment/javascript/nodejs-on-windows)
    1. 到[nvm windows github官方](https://github.com/coreybutler/nvm-windows/releases)下載latest ==nvm-setup.exe==並安裝
        ```bash
        $ nvm --version
        1.1.12
        $ nvm ls # 列出目前node js的已安裝的版本有哪些
        No installations recognized. # 因為目前都沒有所以No installations
        $ nvm list available # 列出目前可安裝的版本有哪些
        |   CURRENT    |     LTS      |  OLD STABLE  | OLD UNSTABLE |
        |--------------|--------------|--------------|--------------|
        |    21.5.0    |   20.10.0    |   0.12.18    |   0.11.16    |
        |    21.4.0    |    20.9.0    |   0.12.17    |   0.11.15    |
        |    21.3.0    |   18.19.0    |   0.12.16    |   0.11.14    |
        |    21.2.0    |   18.18.2    |   0.12.15    |   0.11.13    |
        |    21.1.0    |   18.18.1    |   0.12.14    |   0.11.12    |
        |    21.0.0    |   18.18.0    |   0.12.13    |   0.11.11    |
        |    20.8.1    |   18.17.1    |   0.12.12    |   0.11.10    |
        |    20.8.0    |   18.17.0    |   0.12.11    |    0.11.9    |
        |    20.7.0    |   18.16.1    |   0.12.10    |    0.11.8    |
        |    20.6.1    |   18.16.0    |    0.12.9    |    0.11.7    |
        |    20.6.0    |   18.15.0    |    0.12.8    |    0.11.6    |
        |    20.5.1    |   18.14.2    |    0.12.7    |    0.11.5    |
        |    20.5.0    |   18.14.1    |    0.12.6    |    0.11.4    |
        |    20.4.0    |   18.14.0    |    0.12.5    |    0.11.3    |
        |    20.3.1    |   18.13.0    |    0.12.4    |    0.11.2    |
        |    20.3.0    |   18.12.1    |    0.12.3    |    0.11.1    |
        |    20.2.0    |   18.12.0    |    0.12.2    |    0.11.0    |
        |    20.1.0    |   16.20.2    |    0.12.1    |    0.9.12    |
        |    20.0.0    |   16.20.1    |    0.12.0    |    0.9.11    |
        |    19.9.0    |   16.20.0    |   0.10.48    |    0.9.10    |
        ```
    2. 選擇一個版本安裝
        ```bash
        $ nvm install 20.10.0
        Downloading node.js version 20.10.0 (64-bit)...
        Extracting node and npm...
        Complete
        npm v10.2.3 installed successfully.


        Installation complete. If you want to use this version, type

        nvm use 20.10.0
        ```
    3. 選擇已安裝的版本
        ```bash
        $ nvm use 20.10.0
        Now using node v20.10.0 (64-bit)
        ```
    4. 接著就可以只用npm / node安裝專案需要的package
        ```bash
        $ cd "Double Injection\app"
        $ ls


            目錄: D:\Double Injection\app


        Mode                 LastWriteTime         Length Name
        ----                 -------------         ------ ----
        -a----      2023/12/18  下午 05:52           1786 app.js
        -a----      2023/12/29  上午 01:19           1160 exp.py
        -a----      2023/12/18  下午 10:16             13 flag.json
        -a----      2023/12/18  下午 05:26            470 init-db.js
        -a----      2023/12/18  上午 06:16            110 package.json
        $ npm install # 安裝所有package.json中的library
        ```
* WSL / Linux
    同樣的操作需要再做一次，詳細可以看[MSDN - 在 Windows 子系統 Linux 版 (WSL2) 上安裝 Node.js](https://learn.microsoft.com/zh-tw/windows/dev-environment/javascript/nodejs-on-wsl)
    1. Install nvm
        ```bash
        $ sudo apt-get install curl
        $ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
        $ nvm --version
        0.39.7
        ```
    2. Check Current Available Version
        ```bash
        $ nvm ls

        ->       system
        iojs -> N/A (default)
        node -> stable (-> N/A) (default)
        unstable -> N/A (default)
        ```
    3. Install Long Term Support
        ```bash
        $ nvm install --lts
        Installing latest LTS version.
        Downloading and installing node v20.10.0...
        Downloading https://nodejs.org/dist/v20.10.0/node-v20.10.0-linux-x64.tar.xz...
        ############################################################################################################ 100.0%
        Computing checksum with sha256sum
        Checksums matched!
        Now using node v20.10.0
        Creating default alias: default -> lts/* (-> v20.10.0)
        $ nvm ls
        ->     v20.10.0
                 system
        default -> lts/* (-> v20.10.0)
        iojs -> N/A (default)
        unstable -> N/A (default)
        node -> stable (-> v20.10.0) (default)
        stable -> 20.10 (-> v20.10.0) (default)
        lts/* -> lts/iron (-> v20.10.0)
        lts/argon -> v4.9.1 (-> N/A)
        lts/boron -> v6.17.1 (-> N/A)
        lts/carbon -> v8.17.0 (-> N/A)
        lts/dubnium -> v10.24.1 (-> N/A)
        lts/erbium -> v12.22.12 (-> N/A)
        lts/fermium -> v14.21.3 (-> N/A)
        lts/gallium -> v16.20.2 (-> N/A)
        lts/hydrogen -> v18.19.0 (-> N/A)
        lts/iron -> v20.10.0
        ```
    4. Check npm / node Version
        ```bash
        $ npm --version
        10.2.3
        $ node --version
        v20.10.0
        ```
    5. 安裝Module(一樣是在有package.json的目錄下)
        ```bash
        $ npm install
        ```

## Debug By VScode
詳細可以看[MSDN的教學](https://learn.microsoft.com/zh-tw/training/modules/debug-nodejs/5-analyze-your-program-state)
:::info
在debug的過程中，有可能會因為是linux based的路徑，所以造成錯誤，所以最好還是在wsl中用`code .`的方式進入VScode，再進行debug，另外提醒，在linux or windows下npm install所載的package會根據OS不一樣而有差異，所以要搞清楚目前的平台是哪一個再進行debug；再另外，因為大部分的題目都是具備docker，所以在build之前要先確定有沒有都完成原本docker幫忙的事情，例如以下script:
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
這是NTU CS 2023 HW - Double Injection的題目，首先他有準備/flag1.txt以及/flag2-{random strings}.txt這兩個檔案，以及/etc/db.sqlite3這個file，並且run了init-db.js，這些都是要自己處理的部分，不然單單debug app.js會出一大堆問題
:::


## Download Web Storm
到[官網](https://www.jetbrains.com/webstorm/download/#section=windows)下載對應OS的Installer，不過這東西是要收費的，如果要白嫖的話可以參考[Jetbrain 軟體教育許可授權申請流程](https://hackmd.io/@nfu-johnny/B1yOz8KQs)，不過台大的帳號不知道為啥會過不了，所以要用提供**官方文件**的方式申請

:::danger
後續的操作其實就和vscode差不了多少，有點懶得寫了，而且web storm還需要收錢，但vscode也沒多難用，只是如果習慣用他們家的會蠻好操作的就是了，包含直接和docker連動之類的，但debug還是要用local端build起來(就是上面vscode的流程那樣)，也是沒有方便多少
:::