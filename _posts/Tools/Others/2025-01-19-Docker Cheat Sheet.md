---
title: Docker Cheat Sheet
tags: [Tools]

category: "Tools > Others"
---

# Docker Cheat Sheet
## Background
[Docker筆記 - Docker基礎教學](https://medium.com/alberthg-docker-notes/docker筆記-docker基礎教學-7bbe3a351caf)
[Docker筆記 - 進入Container，建立並操作 PostgreSQL Container](https://medium.com/alberthg-docker-notes/docker筆記-進入container-建立並操作-postgresql-container-d221ba39aaec)
[Docker筆記 - 更改Container的Configuration](https://medium.com/alberthg-docker-notes/docker筆記-更改container的configuration-5dc69d28a421)
[Docker筆記 - 讓資料遠離Container，使用 Volume、Bind Mount 與 Tmpfs Mount](https://medium.com/alberthg-docker-notes/docker筆記-讓資料遠離container-使用-volume-bind-mount-與-tmpfs-mount-6908da341d11)
[Docker Docker Compose與Dockerfile差別 ](https://matthung0807.blogspot.com/2020/12/docker-docker-compose-dockerfile-difference.html)
[Docker Compose 指令](https://osslab.tw/books/docker/page/docker-compose-%E6%8C%87%E4%BB%A4)
## Command
* [Know docker container name](https://www.ibm.com/docs/en/workload-automation/9.5.0?topic=compose-accessing-docker-containers)
    ```bash!
    $ docker ps
    # Then you'll find the container name at the end of the result
    ```
* [Go into container bash shell](https://matthung0807.blogspot.com/2020/10/docker-go-into-container-bash-shell.html)
    ```bash!
    $ docker exec -it <container_name> bash
    
    # 以root的身份進入container
    # 極度建議以此方法進入bash
    $ docker exec -u root -it <container_id> /bin/bash
    ```
* Check Log
    ```bash
    $ docker-compose logs
    ```
* 啟動所有的 Docker Container 指令如下
    ```bash
    $ docker-compose up -d
    ```
* 停止 docker-compose 執行的所有 Container
    ```bash
    $ docker-compose stop
    ```
* 刪除 docker-compose 的所有 Container
    ```bash
    $ docker-compose rm
    ```
* Leave Container
    `exit or ctrl-D`
* 利用Dockerfile build一個Images並且實際跑起來
    ```bash
    $ docker run -it --rm $(docker build -q .) /bin/sh
    ```
:::spoiler 實作
```bash
$ docker pull httpd    # with the latest version
$ docker images        # check the current images status
REPOSITORY   TAG       IMAGE ID       CREATED      SIZE
httpd        latest    75a48b16cd56   4 days ago   168MB
$ docker create --name test -p 8080:80 httpd    # create a container with the name test and port number is 80
70fd43b63fa04c0daebd8128eff7ec58de26cb5c4c7bf63c0cf30fd03d07f1ab
$ docker start 70fd43b63fa0    # start the container
70fd43b63fa0
$ docker ps -a                 # check container status
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS          PORTS                  NAMES
70fd43b63fa0   httpd     "httpd-foreground"       2 minutes ago   Up 27 seconds   0.0.0.0:8080->80/tcp   test
$ docker exec -it test bash    # get into container with bash shell as terminal
root@70fd43b63fa0:/usr/local/apache2#
```
:::
## Reference
[Day 24：使用 Docker-Compose 啟動多個 Docker Container ](https://ithelp.ithome.com.tw/articles/10194183)
[設定php.ini](https://campus-xoops.tn.edu.tw/modules/tad_book3/page.php?tbdsn=220)
[【Day 3】 - Docker 基本指令操作 ](https://ithelp.ithome.com.tw/articles/10186431)


## PADNS Midterm Reference
[使用 docker 架設 wordpress 網站 ](https://penueling.com/%E7%B7%9A%E4%B8%8A%E5%AD%B8%E7%BF%92/%E4%BD%BF%E7%94%A8-docker-%E6%9E%B6%E8%A8%AD-wordpress-%E7%B6%B2%E7%AB%99/)
[ubuntu安装nginx报错:Failed to start A high performance web server and a reverse proxy server](https://blog.csdn.net/daerzei/article/details/123488593)

### 執行步驟
1. Destroy Droplet
![](https://i.imgur.com/xBM8d8z.png)
2. Use the new password to login(be send by Digital Ocean)
![](https://i.imgur.com/X21VIIi.png)
And then change your password.
3. Follow the [note](https://github.com/fei3363/WebSecurityCourse/tree/main/server) to install requirement application
    ```bash
    $ apt-get update
    $ apt-get install ca-certificates curl gnupg lsb-release
    $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    $ echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    $ apt-get update
    $ apt-get install docker-ce docker-ce-cli containerd.io
    $ docker run hello-world
    $ curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    $ chmod +x /usr/local/bin/docker-compose
    $ docker-compose --version
    ```
4. Deploy docker
    ```bash
    $ docker-compose up -d
    ```
5. 外網掛域名
    ```bash
    $ apt install nginx -y
    $ vim /etc/nginx/sites-enabled/website
    $ vim docker-compose.yml
    # add hostname: test.fei.works
    $ service nginx restart
    ```
    :::danger
    It can not set https
    :::