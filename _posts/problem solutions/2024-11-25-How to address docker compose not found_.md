---
title: How to address docker compose not found?
tags: [problem solution]

category: "Problem Solutions"
---

# How to address docker compose not found?
## Problem Statement
如果之前有安裝過docker-compose，而且主要的command是中間有個dash，那是舊的版本，可以參考["docker compose"和"docker-compose"之間的區別](https://stackoverflow.com/questions/66514436/difference-between-docker-compose-and-docker-compose)，但更新的版其實是把dash拿掉，因為要把compose合併到docker的command，這樣的話就需要安裝plugin
## Solution
以結論來說就是只要安裝docker-compose-plugin，這個套件，但是我自己遇到以下問題，所以最後一部分是GPT給我的答案，也成功解決問題
```bash
$ sudo apt install docker-compose-plugin
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package docker-compose-plugin
```
Final Solution↓
```bash
$ sudo mkdir -p /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
$ sudo apt update
$ sudo apt install docker-compose-plugin
$ docker compose version
```