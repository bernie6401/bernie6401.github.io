---
title: 利用Metasploit Framework測試一些網站
tags: [Tools, CTF]

category: "Tools > CTF"
---

# 利用Metasploit Framework測試一些網站
[TOC]
## [Cheat Sheet](https://ithelp.ithome.com.tw/articles/10279483?sc=hot)
```bash
$ sudo msfdb init && msfconsole
msf6 > nmap -vv {IP} # e.g. nmap -vv 127.0.0.1
msf6 > search {http/ssh/ftp...關鍵字} # e.g. search rce
msf6 > use {腳本位置} # e.g. use exploit/unix/http/cacti_filter_sqli_rce
msf6 exploit(XXX) > show option # 顯示該腳本需要哪一些參數
msf6 exploit(XXX) > set {option name} {參數} # e.g. set RHOST 127.0.0.1
```
## [SmartDaily](https://www.smartdaily.com.tw/)
IP: `34.81.5.101`
[Security Header Result](https://securityheaders.com/?q=https%3A%2F%2Fwww.smartdaily.com.tw%2F&followRedirects=on)
### nmap
:::spoiler nmap Result
```bash
nmap -vv 34.81.5.101
[*] exec: nmap -vv 34.81.5.101

Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-02 01:49 EDT
Initiating Ping Scan at 01:49
Scanning 34.81.5.101 [2 ports]
Completed Ping Scan at 01:49, 0.01s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 01:49
Completed Parallel DNS resolution of 1 host. at 01:49, 0.01s elapsed
Initiating Connect Scan at 01:49
Scanning 101.5.81.34.bc.googleusercontent.com (34.81.5.101) [1000 ports]
Discovered open port 443/tcp on 34.81.5.101
Discovered open port 80/tcp on 34.81.5.101
Increasing send delay for 34.81.5.101 from 0 to 5 due to 11 out of 14 dropped probes since last increase.
Increasing send delay for 34.81.5.101 from 5 to 10 due to 11 out of 11 dropped probes since last increase.
Increasing send delay for 34.81.5.101 from 10 to 20 due to 11 out of 11 dropped probes since last increase.
Increasing send delay for 34.81.5.101 from 20 to 40 due to 11 out of 15 dropped probes since last increase.
Completed Connect Scan at 01:50, 75.06s elapsed (1000 total ports)
Nmap scan report for 101.5.81.34.bc.googleusercontent.com (34.81.5.101)
Host is up, received syn-ack (0.0085s latency).
Scanned at 2023-10-02 01:49:05 EDT for 75s
Not shown: 998 filtered tcp ports (no-response)
PORT    STATE SERVICE REASON
80/tcp  open  http    syn-ack
443/tcp open  https   syn-ack

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 75.09 seconds
```
:::
開的Port: 80/443

---
## [NatureTEL](http://www.naturaltel.com/)
IP: `219.84.199.120`
[Security Header Result](https://securityheaders.com/?q=https%3A%2F%2Fwww.naturaltel.com%2F&followRedirects=on)
### nmap
:::spoiler nmap Result
```bash
$ nmap -vv 219.84.199.120
[*] exec: nmap -vv 219.84.199.120

Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-02 01:53 EDT
Initiating Ping Scan at 01:53
Scanning 219.84.199.120 [2 ports]
Completed Ping Scan at 01:53, 0.01s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 01:53
Completed Parallel DNS resolution of 1 host. at 01:53, 0.01s elapsed
Initiating Connect Scan at 01:53
Scanning so199-120.asiawhere.com (219.84.199.120) [1000 ports]
Discovered open port 80/tcp on 219.84.199.120
Discovered open port 443/tcp on 219.84.199.120
Discovered open port 21/tcp on 219.84.199.120
Discovered open port 110/tcp on 219.84.199.120
Discovered open port 143/tcp on 219.84.199.120
Discovered open port 25/tcp on 219.84.199.120
Completed Connect Scan at 01:53, 4.63s elapsed (1000 total ports)
Nmap scan report for so199-120.asiawhere.com (219.84.199.120)
Host is up, received syn-ack (0.0091s latency).
Scanned at 2023-10-02 01:53:07 EDT for 5s
Not shown: 994 filtered tcp ports (no-response)
PORT    STATE SERVICE REASON
21/tcp  open  ftp     syn-ack
25/tcp  open  smtp    syn-ack
80/tcp  open  http    syn-ack
110/tcp open  pop3    syn-ack
143/tcp open  imap    syn-ack
443/tcp open  https   syn-ack

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 4.67 seconds
```
:::
開的Port: 21/25/80/110/143/443

---
## [飛像資訊](https://www.flyelephant.com.tw/)
IP: `199.15.163.148`
[Security Header Result](https://securityheaders.com/?q=https%3A%2F%2Fwww.flyelephant.com.tw%2F&followRedirects=on)
### nmap
:::spoiler nmap Result
```bash
$ nmap -vv 199.15.163.148
[*] exec: nmap -vv  199.15.163.148 

Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-02 01:50 EDT
Initiating Ping Scan at 01:50
Scanning 199.15.163.148 [2 ports]
Completed Ping Scan at 01:50, 0.15s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 01:50
Completed Parallel DNS resolution of 1 host. at 01:50, 0.14s elapsed
Initiating Connect Scan at 01:50
Scanning unalocated.163.wixsite.com (199.15.163.148) [1000 ports]
Discovered open port 80/tcp on 199.15.163.148
Discovered open port 443/tcp on 199.15.163.148
Connect Scan Timing: About 18.15% done; ETC: 01:53 (0:02:20 remaining)
Connect Scan Timing: About 21.00% done; ETC: 01:55 (0:03:49 remaining)
Increasing send delay for 199.15.163.148 from 0 to 5 due to 11 out of 16 dropped probes since last increase.
Connect Scan Timing: About 68.50% done; ETC: 01:52 (0:00:42 remaining)
Completed Connect Scan at 01:52, 99.59s elapsed (1000 total ports)
Nmap scan report for unalocated.163.wixsite.com (199.15.163.148)
Host is up, received syn-ack (0.17s latency).
Scanned at 2023-10-02 01:50:41 EDT for 99s
Not shown: 998 filtered tcp ports (no-response)
PORT    STATE SERVICE REASON
80/tcp  open  http    syn-ack
443/tcp open  https   syn-ack

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 99.90 seconds
```
:::
開的Port: 80/443